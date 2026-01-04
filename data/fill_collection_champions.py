"""
Scraper -> API MediaWiki (Fandom)
Dépendances : requests, beautifulsoup4, lxml
pip install requests beautifulsoup4 lxml
"""

import requests
from bs4 import BeautifulSoup, Tag
import re
from typing import Optional, Dict, List
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import uuid
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

HEADERS = {"User-Agent": "Mozilla/5.0"}

client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def toText(champ, type_data, data):
    out = []

    out.append(f"Champion {champ} - {type_data}")

    if isinstance(data, str):
        out.append(data.strip())

    elif isinstance(data, dict):
        for key, value in data.items():
            out.append(f"- {key} : {value}")

    # out.append("Spells :")
    # for i, spell in enumerate(spells):
    #     out.append("")
    #     out.append(f"{spell_names[i] if i < len(spell_names) else f'Ability {i+1}'} :")
    #     for key, value in spell.items():
    #         out.append(f"- {key} : {value}")
    # out.append("")

    return "\n".join(out)  


def fetch_page_html(wiki_base: str, page_title: str) -> Optional[str]:
    """
    Récupère le HTML principal d'une page via l'API MediaWiki (action=parse).
    wiki_base: exemple "https://leagueoflegends.fandom.com"
    page_title: exemple "Blitzcrank/LoL"
    """
    api_url = f"{wiki_base.rstrip('/')}/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text"  # HTML de la page
    }

    with requests.get(
        api_url,
        params=params,
        headers=HEADERS,
        timeout=30
    ) as resp:
        resp.raise_for_status()
        data = resp.json()    

    if "error" in data:
        print("API error:", data["error"])
        return None
    return data["parse"]["text"]["*"]



def clean_text_basic(text: str) -> str:
    # enlever les références [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # normaliser retours à la ligne
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()



def get_section_by_headline(soup: BeautifulSoup, headline_texts: List[str]) -> Optional[str]:
    """
    Cherche une section dont l'entête (.mw-headline) contient un des headline_texts,
    retourne le texte de cette section (jusqu'à la prochaine balise h2/h3 du même niveau).
    """
    for span in soup.select(".mw-headline"):
        if span.string and any(span.string.strip().lower() == h.strip().lower() for h in headline_texts):
            # remontons au parent heading (h2/h3) pour capter le niveau
            heading = span.find_parent(re.compile("^h[1-6]$"))
            if not heading:
                continue
            section_text_parts = []
            # parcourir frères suivants jusqu'au prochain heading de même niveau ou supérieur
            for sib in heading.next_siblings:
                if isinstance(sib, Tag) and re.match(r"h[1-6]", sib.name or "", re.I):
                    break
                if isinstance(sib, Tag):
                    section_text_parts.append(sib.get_text("\n", strip=True))
            return "\n\n".join(p for p in section_text_parts if p.strip())
    return None


def extract_lore(soup: BeautifulSoup) -> Optional[str]:
    # 1) fallback par classe spécifique Fandom
    lore_block = soup.select_one(".skinviewer-info-lore")
    if lore_block:
        return lore_block.get_text("\n", strip=True)
    # 2) fallback par section "Lore"
    lore_by_headline = get_section_by_headline(soup, ["Lore", "Lore (background)"])
    if lore_by_headline:
        return lore_by_headline
    # 3) ultime fallback: chercher "Background" ou "Story"
    return get_section_by_headline(soup, ["Background", "Story"])


def extract_infobox(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extrait les paires label:value de l'infobox portable (Fandom MediaWiki).
    """
    keywords_to_remove = [
        "Store price",
        "Crafting",
        "Ratings",
        "Style",
        "Difficulty"
    ]
    data = {}
    # 1) type-lol-champion (cas spécifique Fandom LoL)
    box = soup.select_one(".type-lol-champion") or soup.select_one(".portable-infobox") or soup.select_one(".infobox")
    if not box:
        return data
    # méthode : chercher les items .pi-item et pi-data-label/pi-data-value (structure Fandom)
    items = box.select(".pi-item")
    if items:
        for item in items:
            label = item.select_one(".pi-data-label")
            value = item.select_one(".pi-data-value")
            if label and value:
                label_text = label.get_text(strip=True)
                if label_text not in keywords_to_remove:
                    if label_text == "Adaptive type":
                        data[label_text] = value.get_text(" ", strip=True).replace("Champions stunned with Pyromania (P) ", "")
                    else:
                        data[label_text] = value.get_text(" ", strip=True)
            else:
                # certains items ont structure différente : attempt split by ":" or br
                text = item.get_text(" ", strip=True)
                if ":" in text:
                    label_part, val_part = text.split(":", 1)
                    data[label_part.strip()] = val_part.strip()
    else:
        # fallback : parcourir tous les li ou div directs
        for child in box.find_all(["div", "li"], recursive=True):
            text = child.get_text(" ", strip=True)
            if ":" in text:
                k, v = text.split(":", 1)
                data[k.strip()] = v.strip()
    return data


def extract_abilities_simple(soup: BeautifulSoup) -> list:
    ability_nodes = soup.select(".ability-info-container")
    abilities_slot = ["Passive", "Q", "W", "E", "R"]
    abilities = []

    if not ability_nodes:
        return abilities

    for index, node in enumerate(ability_nodes):
        for unwanted in node.find_all("span", class_="ll-item navbox"):
            unwanted.decompose()  # supprime complètement l'élément du tree
        for br in node.find_all("br"):
            br.replace_with("\n")

        text = node.get_text()

        text = re.sub(r'champions[^)]*', '', text)

        text = re.sub(
            r"\b[A-Z][A-Za-z' ]+\s*\([QWERP]\)",
            "",
            text
        )

        parts = re.split(r'\n{2,}', text)
        data = {"name" : parts[0]}
        data["slot"] = abilities_slot[index] if index < len(abilities_slot) else f"Ability {index+1}"
        for part in parts[2:]:
            part = part.strip()
            if part:
                part_list = part.split(":")
                if len(part_list) == 2:
                    data[part_list[0].strip()] = part_list[1].strip()


        abilities.append(data)

    return abilities




def champion_exists(champion_name: str) -> bool:
    # Filtre sur le champ "name"
    filt = Filter(
        must=[
            FieldCondition(
                key="champion",
                match=MatchValue(value=champion_name)
            )
        ]
    )
    # Recherche d’un point correspondant
    result = client.query_points(
        collection_name="lol_champions",
        query_filter=filt,
        limit=1
    )

    return len(result.points) > 0




def insert_chunk(payload: dict):
    vector = model.encode(payload["text"]).tolist()

    point_id = str(uuid.uuid4())

    client.upsert(
        collection_name="lol_champions",
        points=[
            {
                "id": point_id,
                "vector": vector,
                "payload": payload
            }
        ]
    )

    print(f"{payload['champion']} {payload['chunk_type']} inserted into Qdrant.")




if __name__ == "__main__":
    champions_list = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Aurora',
'Azir', 'Bard', "Bel'Veth", 'Blitzcrank', 'Brand', 'Braum', 'Briar', 'Caitlyn', 'Camille', 'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 
'Draven', 'Dr. Mundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 
'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', "Kai'Sa", 
'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred', 'Kled', "Kog'Maw", "K'Sante", 'LeBlanc', 
'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Milio', 'Miss Fortune', 
'Wukong', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 
'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', "Rek'Sai", 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 
'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 
'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 
'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', "Vel'Koz", 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 
'Volibear', 'Warwick', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 
'Zilean', 'Zoe', 'Zyra'] # , 'Ambessa', 'Mel', 'Yunara', 'Zaahen'
    
    for champ in champions_list:
        if champion_exists(champ):
            print(f"{champ} déjà présent !")
            continue

        WIKI_BASE = "https://leagueoflegends.fandom.com"
        PAGE = f"{champ}/LoL"

        html = fetch_page_html(WIKI_BASE, PAGE)
        if not html:
            raise SystemExit("Impossible de récupérer la page via l'API")

        soup = BeautifulSoup(html, "lxml")

        lore = extract_lore(soup)
        # print(lore)
        if lore:
            lore = clean_text_basic(lore)


        stats = extract_infobox(soup)

        champ_info_block = soup.select_one(".stat-wheel")
        text = champ_info_block.get_text(separator=" : ", strip=True)
        # transformer en dictionnaire
        parts = text.split(" : ")
        ratings = {}
        for i in range(0, len(parts)-1, 2):
            key = parts[i].strip()
            value = parts[i+1].strip()
            ratings[key] = value


        spells = extract_abilities_simple(soup)

        # data = {
        #     "champion": champion,
        #     "lore": lore,
        #     "stats": stats,
        #     "ratings": ratings,
        #     "spells": spells,
        # }

        # print(json.dumps(data, indent=4, ensure_ascii=False)) # Dictionnaire
        # print(toText(champion, lore, info, ratings, spells)) # Texte



        # data["aliases"] = []
        # data["aliases"]["lane"] = ["position", "voie", "lane"]
        # if data["slot"] == "R":
        #     data["spell_aliases"] = ["ultimate", "ultime", "spell R", "sort R"]



        # LORE
        payload_lore = {
            "champion": champ,
            "chunk_type": "lore",
            # "aliases": {"position": ["lane", "voie", ]
            "lore": lore,
            "text": toText(
                champ,
                "lore",
                lore
            )
        }

        insert_chunk(payload_lore)

        # infos
        payload_infos = {
            "champion": champ,
            "chunk_type": "stats",
            "stats": stats,
            "text": toText(
                champ,
                "stats",
                stats
            )
        }

        insert_chunk(payload_infos)

        # raitings
        payload_ratings = {
            "champion": champ,
            "chunk_type": "ratings",
            "ratings": ratings,
            "text": toText(
                champ,
                "ratings",
                ratings
            )
        }

        insert_chunk(payload_ratings)

        # spells
        for i, spell in enumerate(spells):
            payload_spell = {
                "champion": champ,
                "chunk_type": "spell",
                "spell_slot": spell.get("slot", i),
                "spell": spell,
                "text": toText(
                    champ,
                    f"Spell {spell.get('slot', i)}",
                    spell
                )
            }


            insert_chunk(payload_spell)


        # payload = {
        #     "champion": champ,
        #     "lore": lore,
        #     "metadata": info,
        #     "stats": ratings,
        #     "spells": spells,
        #     "text": toText(
        #         champ,
        #         lore,
        #         info,
        #         ratings,
        #         spells
        #     )
        # }

        # insert_champion(payload)