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
from qdrant_client import QdrantClient
import uuid
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import os
import dotenv

dotenv.load_dotenv(".env.development")
HEADERS = {"User-Agent": "Mozilla/5.0"}

client = QdrantClient(
    url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_KEY"), timeout=5.0
)

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {os.getenv('HF_KEY')}"}


def embed(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    response.raise_for_status()
    return response.json()


def toText(champ, type_data, data):
    out = []

    out.append(f"Champion {champ} - {type_data}")

    if isinstance(data, str):
        out.append(data.strip())

    elif isinstance(data, dict):
        for key, value in data.items():
            out.append(f"- {key} : {value}")

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
        "prop": "text",
    }

    with requests.get(api_url, params=params, headers=HEADERS, timeout=30) as resp:
        resp.raise_for_status()
        data = resp.json()

    if "error" in data:
        print("API error:", data["error"])
        return None
    return data["parse"]["text"]["*"]


def clean_text_basic(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_section_by_headline(
    soup: BeautifulSoup, headline_texts: List[str]
) -> Optional[str]:
    """
    Cherche une section dont l'entête (.mw-headline) contient un des headline_texts,
    retourne le texte de cette section (jusqu'à la prochaine balise h2/h3 du même niveau).
    """
    for span in soup.select(".mw-headline"):
        if span.string and any(
            span.string.strip().lower() == h.strip().lower() for h in headline_texts
        ):
            heading = span.find_parent(re.compile("^h[1-6]$"))
            if not heading:
                continue
            section_text_parts = []
            for sib in heading.next_siblings:
                if isinstance(sib, Tag) and re.match(r"h[1-6]", sib.name or "", re.I):
                    break
                if isinstance(sib, Tag):
                    section_text_parts.append(sib.get_text("\n", strip=True))
            return "\n\n".join(p for p in section_text_parts if p.strip())
    return None


def extract_lore(soup: BeautifulSoup) -> Optional[str]:
    lore_block = soup.select_one(".skinviewer-info-lore")
    if lore_block:
        return lore_block.get_text("\n", strip=True)
    lore_by_headline = get_section_by_headline(soup, ["Lore", "Lore (background)"])
    if lore_by_headline:
        return lore_by_headline
    return get_section_by_headline(soup, ["Background", "Story"])


def extract_infobox(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extrait les paires label:value de l'infobox portable (Fandom MediaWiki).
    """
    keywords_to_remove = ["Store price", "Crafting", "Ratings", "Style", "Difficulty"]
    data = {}
    box = (
        soup.select_one(".type-lol-champion")
        or soup.select_one(".portable-infobox")
        or soup.select_one(".infobox")
    )
    if not box:
        return data
    items = box.select(".pi-item")
    if items:
        for item in items:
            label = item.select_one(".pi-data-label")
            value = item.select_one(".pi-data-value")
            if label and value:
                label_text = label.get_text(strip=True)
                if label_text not in keywords_to_remove:
                    if label_text == "Adaptive type":
                        data[label_text] = value.get_text(" ", strip=True).replace(
                            "Champions stunned with Pyromania (P) ", ""
                        )
                    else:
                        data[label_text] = value.get_text(" ", strip=True)
            else:
                text = item.get_text(" ", strip=True)
                if ":" in text:
                    label_part, val_part = text.split(":", 1)
                    data[label_part.strip()] = val_part.strip()
    else:
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
            unwanted.decompose()
        for br in node.find_all("br"):
            br.replace_with("\n")

        text = node.get_text()

        text = re.sub(r"champions[^)]*", "", text)

        text = re.sub(r"\b[A-Z][A-Za-z' ]+\s*\([QWERP]\)", "", text)

        parts = re.split(r"\n{2,}", text)
        data = {"name": parts[0]}
        data["slot"] = (
            abilities_slot[index]
            if index < len(abilities_slot)
            else f"Ability {index+1}"
        )
        for part in parts[2:]:
            part = part.strip()
            if part:
                part_list = part.split(":")
                if len(part_list) == 2:
                    data[part_list[0].strip()] = part_list[1].strip()

        abilities.append(data)

    return abilities


def champion_exists(champion_name: str) -> bool:
    filt = Filter(
        must=[FieldCondition(key="champion", match=MatchValue(value=champion_name))]
    )
    result = client.query_points(
        collection_name="lol_champions", query_filter=filt, limit=1
    )

    return len(result.points) > 0


def insert_chunk(payload: dict):
    vector = embed(payload["text"])

    point_id = str(uuid.uuid4())

    client.upsert(
        collection_name="lol_champions",
        points=[{"id": point_id, "vector": vector, "payload": payload}],
    )


if __name__ == "__main__":
    champions_list = [
        "Aatrox",
        "Ahri",
        "Akali",
        "Akshan",
        "Alistar",
        "Amumu",
        "Anivia",
        "Annie",
        "Aphelios",
        "Ashe",
        "Aurelion Sol",
        "Aurora",
        "Azir",
        "Bard",
        "Bel'Veth",
        "Blitzcrank",
        "Brand",
        "Braum",
        "Briar",
        "Caitlyn",
        "Camille",
        "Cassiopeia",
        "Cho'Gath",
        "Corki",
        "Darius",
        "Diana",
        "Draven",
        "Dr. Mundo",
        "Ekko",
        "Elise",
        "Evelynn",
        "Ezreal",
        "Fiddlesticks",
        "Fiora",
        "Fizz",
        "Galio",
        "Gangplank",
        "Garen",
        "Gnar",
        "Gragas",
        "Graves",
        "Gwen",
        "Hecarim",
        "Heimerdinger",
        "Hwei",
        "Illaoi",
        "Irelia",
        "Ivern",
        "Janna",
        "Jarvan IV",
        "Jax",
        "Jayce",
        "Jhin",
        "Jinx",
        "Kai'Sa",
        "Kalista",
        "Karma",
        "Karthus",
        "Kassadin",
        "Katarina",
        "Kayle",
        "Kayn",
        "Kennen",
        "Kha'Zix",
        "Kindred",
        "Kled",
        "Kog'Maw",
        "K'Sante",
        "LeBlanc",
        "Lee Sin",
        "Leona",
        "Lillia",
        "Lissandra",
        "Lucian",
        "Lulu",
        "Lux",
        "Malphite",
        "Malzahar",
        "Maokai",
        "Master Yi",
        "Milio",
        "Miss Fortune",
        "Wukong",
        "Mordekaiser",
        "Morgana",
        "Naafiri",
        "Nami",
        "Nasus",
        "Nautilus",
        "Neeko",
        "Nidalee",
        "Nilah",
        "Nocturne",
        "Nunu",
        "Olaf",
        "Orianna",
        "Ornn",
        "Pantheon",
        "Poppy",
        "Pyke",
        "Qiyana",
        "Quinn",
        "Rakan",
        "Rammus",
        "Rek'Sai",
        "Rell",
        "Renata Glasc",
        "Renekton",
        "Rengar",
        "Riven",
        "Rumble",
        "Ryze",
        "Samira",
        "Sejuani",
        "Senna",
        "Seraphine",
        "Sett",
        "Shaco",
        "Shen",
        "Shyvana",
        "Singed",
        "Sion",
        "Sivir",
        "Skarner",
        "Smolder",
        "Sona",
        "Soraka",
        "Swain",
        "Sylas",
        "Syndra",
        "Tahm Kench",
        "Taliyah",
        "Talon",
        "Taric",
        "Teemo",
        "Thresh",
        "Tristana",
        "Trundle",
        "Tryndamere",
        "Twisted Fate",
        "Twitch",
        "Udyr",
        "Urgot",
        "Varus",
        "Vayne",
        "Veigar",
        "Vel'Koz",
        "Vex",
        "Vi",
        "Viego",
        "Viktor",
        "Vladimir",
        "Volibear",
        "Warwick",
        "Xayah",
        "Xerath",
        "Xin Zhao",
        "Yasuo",
        "Yone",
        "Yorick",
        "Yuumi",
        "Zac",
        "Zed",
        "Zeri",
        "Ziggs",
        "Zilean",
        "Zoe",
        "Zyra",
    ]  # , 'Ambessa', 'Mel', 'Yunara', 'Zaahen', 'Locke'

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
        if lore:
            lore = clean_text_basic(lore)

        stats = extract_infobox(soup)

        champ_info_block = soup.select_one(".stat-wheel")
        text = champ_info_block.get_text(separator=" : ", strip=True)
        parts = text.split(" : ")
        ratings = {}
        for i in range(0, len(parts) - 1, 2):
            key = parts[i].strip()
            value = parts[i + 1].strip()
            ratings[key] = value

        spells = extract_abilities_simple(soup)

        # LORE
        payload_lore = {
            "champion": champ,
            "chunk_type": "lore",
            "lore": lore,
            "text": toText(champ, "lore", lore),
        }

        insert_chunk(payload_lore)

        # infos
        payload_infos = {
            "champion": champ,
            "chunk_type": "stats",
            "stats": stats,
            "text": toText(champ, "stats", stats),
        }

        insert_chunk(payload_infos)

        # raitings
        payload_ratings = {
            "champion": champ,
            "chunk_type": "ratings",
            "ratings": ratings,
            "text": toText(champ, "ratings", ratings),
        }

        insert_chunk(payload_ratings)

        # spells
        for i, spell in enumerate(spells):
            payload_spell = {
                "champion": champ,
                "chunk_type": "spell",
                "spell_slot": spell.get("slot", i),
                "spell": spell,
                "text": toText(champ, f"Spell {spell.get('slot', i)}", spell),
            }

            insert_chunk(payload_spell)
