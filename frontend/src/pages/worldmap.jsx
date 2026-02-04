import { ArrowLeft, Loader2 } from "lucide-react";
import { useState } from "react";

export default function WorldMap() {
  const [loaded, setLoaded] = useState(false);
  const [hoveredId, setHoveredId] = useState(null);
  const mapPoints = [
    {
      id: "heimerdinger",
      name: "Heimerdinger",
      image: "/assets/heimerdinger.jpg",
      position: { left: "62%", top: "55%" },
      description: "L'excentrique professeur Cecil B. Heimerdinger est l'un des inventeurs les plus novateurs et les plus estimés que le monde ait jamais connus. Membre le plus ancien du Conseil de Piltover, il a été témoin des excès et des dérives de la soif de progrès incessante de la ville. Malgré tout, ce brillant scientifique et enseignant est resté fidèle à sa vocation : mettre ses inventions originales au service de l'amélioration du quotidien.",
    },
    {
      id: "shen",
      name: "Shen",
      image: "/assets/shen.jpg",
      position: { left: "75%", top: "20%" },
      description: "Parmi les mystérieux guerriers ioniens connus sous le nom de Kinkou, Shen est leur chef, l'Œil du Crépuscule. Il aspire à demeurer libre de toute confusion émotionnelle, de tout préjugé et de tout ego, et chemine sur la voie invisible du jugement impartial entre le monde spirituel et le monde physique. Chargé de maintenir l'équilibre entre eux, Shen manie des lames d'acier et d'énergie arcanique contre quiconque oserait le menacer.",
    },
    {
      id: "leblanc",
      name: "Leblanc",
      image: "/assets/leblanc.jpg",
      position: { left: "53%", top: "35%" },
      description: "Mystérieuse même pour les autres membres de la cabale de la Rose Noire, LeBlanc n'est qu'un nom parmi tant d'autres pour cette femme à la peau pâle qui manipule les personnes et les événements depuis les origines de Noxus. Grâce à sa magie de duplication, la sorcière peut apparaître à n'importe qui, n'importe où, et même être à plusieurs endroits à la fois. Toujours en train de comploter dans l'ombre, les véritables motivations de LeBlanc sont aussi impénétrables que son identité changeante.",
    },
    {
      id: "morgana",
      name: "Morgana",
      image: "/assets/morgana.jpg",
      position: { left: "30%", top: "41%" },
      description: "Partagée entre sa nature céleste et mortelle, Morgana a lié ses ailes pour embrasser l'humanité et inflige sa douleur et son amertume aux malhonnêtes et aux corrompus. Elle rejette les lois et les traditions qu'elle juge injustes et lutte pour la vérité depuis l'ombre de Demacia – même lorsque d'autres cherchent à la réprimer – en forgeant des boucliers et des chaînes de feu noir. Plus que tout, Morgana croit sincèrement que même les bannis et les parias peuvent un jour se relever.",
    },
    {
      id: "azir",
      name: "Azir",
      image: "/assets/azir.jpg",
      position: { left: "54%", top: "82%" },
      description: "Azir était un empereur mortel de Shurima en une époque lointaine, un homme fier au seuil de l'immortalité. Son orgueil le mena à la trahison et à l'assassinat au moment de son plus grand triomphe, mais à présent, des millénaires plus tard, il renaît en tant qu'être ascensionné d'une puissance immense. Sa cité enfouie surgie des sables, Azir cherche à restaurer la gloire passée de Shurima.",
    },
    {
      id: "ornn",
      name: "Ornn",
      image: "/assets/ornn.jpg",
      position: { left: "28%", top: "20%" },
      description: "Ornn est l'esprit de la forge et de l'artisanat de Freljordia. Il travaille dans la solitude d'une immense forge, creusée dans les cavernes de lave sous le volcan Foyer-Maison. Là, il attise des chaudrons bouillonnants de roche en fusion pour purifier les minerais et façonner des objets d'une qualité inégalée. Lorsque d'autres divinités — en particulier Volibear — parcourent la terre et s'immiscent dans les affaires des mortels, Ornn se lève pour remettre ces êtres impétueux à leur place, soit avec son fidèle marteau, soit avec la puissance ardente des montagnes elles-mêmes.",
    },
    {
      id: "pantheon",
      name: "Panthéon",
      image: "/assets/pantheon.jpg",
      position: { left: "40%", top: "87%" },
      description: "Jadis hôte malgré lui de l'Aspect de la Guerre, Atréus survécut à la destruction du pouvoir céleste qui l'habitait, refusant de succomber à un coup qui arracha des étoiles aux cieux. Avec le temps, il apprit à accepter sa propre mortalité et la force inébranlable qui l'accompagne. Désormais, Atréus s'oppose au divin en tant que Panthéon renaissant, sa volonté inébranlable alimentant les armes de l'Aspect déchu sur le champ de bataille.",
    },
  ];

  return (
    <div className="relative flex flex-1 min-h-0 overflow-hidden bg-primary-50">
      <a
        href="/chatbot"
        className="absolute z-50 p-4 m-6 font-semibold transition-all duration-300 rounded-lg bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
      >
        <ArrowLeft className="w-8 h-8" />
      </a>
      {!loaded && (
        <div className="absolute inset-0 z-40 flex items-center justify-center bg-primary-50">
          <Loader2 className="w-10 h-10 animate-spin text-primary-100" />
        </div>
      )}
      <div className={`
          relative inset-0 object-contain w-full
          transition-opacity duration-1000 ease-in-out
          ${loaded ? "opacity-100" : "opacity-0"}
        `}
      >
        <img
          src="https://vainkeurz.com/wp-content/uploads/2023/06/runeterra-map-1024x611.png"
          className="object-contain w-full h-auto"
          onLoad={() => setLoaded(true)}
        />

        <div className="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-primary-50 to-transparent" />

        <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-primary-50 to-transparent" />
        
        {/* Points dynamiques */}
        {mapPoints.map((point) => (
          <a
            href={`/chatbot?character=${point.id}`}
            key={point.id}
            className="absolute"
            style={{
              left: point.position.left,
              top: point.position.top,
              transform: "translate(-50%, -50%)",
            }}
          >
            <img
              onMouseEnter={() => setHoveredId(point.id)}
              onMouseLeave={() => setHoveredId(null)}
              src={point.image}
              alt={point.name}
              className="z-0 object-cover w-32 h-32 transition-transform duration-200 border-4 rounded-full cursor-pointer border-secondary-50 hover:scale-110"
            />

            {hoveredId === point.id && (
              <div className="absolute z-10 p-4 ml-4 -translate-y-1/2 border-4 rounded-lg shadow-xl w-[360px] bg-background-50 left-full top-1/2 border-secondary-50">
                <h3 className="mb-2 text-lg font-bold text-secondary-50">
                  {point.name}
                </h3>
                <p className="text-sm text-gray-50">
                  {point.description}
                </p>
              </div>
            )}
          </a>
        ))}
      </div>

    </div>
  );
}
