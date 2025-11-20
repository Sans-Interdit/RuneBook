import React, { useState } from "react";
import { BookOpen, Search, Filter, Tag, ExternalLink } from "lucide-react";
import { useAppContext } from "../context/appContext";
// Mock data based on the provided structure
const mockGuides = [
  {
    id_guide: 1,
    title: "Objectifs du jeu",
    content: "La Faille de l'invocateur est le mode de jeu principal de League of Legends, et le seul, si l'on exclut Teamfight Tactics, à disposer d'une scène compétitive professionnelle\n\nDans ce mode de jeu, deux équipes de cinq joueurs s'affrontent sur une carte symétrique...",
    level: "New Player",
    source: "wikipédia",
    tags: ["bases", "explication"]
  },
  {
    id_guide: 2,
    title: "Rôles des joueurs",
    content: "Dans l'immense majorité des parties, sur les cinq champions présents dans chaque équipe, un joueur commence le match en se rendant sur la voie du haut...",
    level: "New Player",
    source: "wikipédia",
    tags: ["bases", "explication"]
  },
  {
    id_guide: 3,
    title: "Autres modes de jeu",
    content: "En plus de la Faille de l'invocateur, plusieurs modes de jeu alternatifs existent. Deux d'entre eux sont présents de manière permanente : le premier, l'ARAM...",
    level: "New Player",
    source: "wikipédia",
    tags: ["bases", "aram", "explication"]
  },
  {
    id_guide: 4,
    title: "Possible improvements",
    content: "As you approach level 30 you should at least know about last hitting even if you're not good at it yet. Gold is probably the most important thing in the game...",
    level: "Average Player",
    source: "leagueoflegendsguideforall",
    tags: ["macro", "conseil"]
  },
  {
    id_guide: 5,
    title: "Ce qu'est un bon crossmap",
    content: "La question du macro est assez vaste et il serait impossible de vous donner une réponse définitive sans contexte ni replays. Cependant, je peux vous donner quelques directives générales...",
    level: "Confirmed Player",
    source: "reddit",
    tags: ["macro", "conseil", "explication"]
  }
];

export default function Catalog() {
  const { guides } = useAppContext();
  
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedLevel, setSelectedLevel] = useState("all");
  const [selectedTag, setSelectedTag] = useState("all");
  const [selectedGuide, setSelectedGuide] = useState(null);

  // Extract all unique tags
  const allTags = [...new Set(guides.flatMap(guide => guide.tags))];

  // Filter guides based on search and filters
  const filteredGuides = guides.filter(guide => {
    const matchesSearch = guide.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         guide.content.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLevel = selectedLevel === "all" || guide.level === selectedLevel;
    const matchesTag = selectedTag === "all" || guide.tags.includes(selectedTag);
    
    return matchesSearch && matchesLevel && matchesTag;
  });

  const getLevelColor = (level) => {
    if (level === "New Player") return "bg-green-400";
    if (level === "Average Player") return "bg-secondary-50";
    return "bg-red-400";
  };

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Header */}
      <div className="px-6 py-16 text-center">
        <h1 className="mb-4 text-5xl font-bold text-transparent bg-clip-text bg-secondary-50 font-titre">
          Catalogue de Guides
        </h1>
        <p className="max-w-2xl mx-auto text-xl text-white font-text">
          Explore notre collection de guides pour comprendre League of Legends à ton rythme
        </p>
      </div>

      <div className="px-6 pb-16 mx-auto max-w-7xl">
        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
            <input
              type="text"
              placeholder="Rechercher un guide..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full py-4 pl-12 pr-4 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 border-primary-100/30 placeholder-white/50 focus:border-secondary-50 focus:outline-none font-text"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-4">
            {/* Level Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-secondary-50" />
              <select
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
                className="px-4 py-2 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 border-primary-100/30 focus:border-secondary-50 focus:outline-none font-text"
              >
                <option value="all">Tous les niveaux</option>
                <option value="New Player">New Player</option>
                <option value="Average Player">Average Player</option>
                <option value="Confirmed Player">Confirmed Player</option>
              </select>
            </div>

            {/* Tag Filter */}
            <div className="flex items-center gap-2">
              <Tag className="w-5 h-5 text-secondary-50" />
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="px-4 py-2 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 border-primary-100/30 focus:border-secondary-50 focus:outline-none font-text"
              >
                <option value="all">Tous les tags</option>
                {allTags.map(tag => (
                  <option key={tag} value={tag}>#{tag}</option>
                ))}
              </select>
            </div>

            {/* Results Count */}
            <div className="flex items-center px-4 py-2 ml-auto border-2 rounded-lg bg-primary-50 border-secondary-50/30">
              <span className="text-sm font-semibold text-secondary-50 font-text">
                {filteredGuides.length} guide{filteredGuides.length > 1 ? 's' : ''} trouvé{filteredGuides.length > 1 ? 's' : ''}
              </span>
            </div>
          </div>
        </div>

        {/* Guides Grid */}
        {filteredGuides.length === 0 ? (
          <div className="py-20 text-center">
            <BookOpen className="w-16 h-16 mx-auto mb-4 text-primary-100/30" />
            <p className="text-xl text-white font-text">
              Aucun guide ne correspond à ta recherche
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredGuides.map((guide) => (
              <div
                key={guide.id_guide}
                onClick={() => setSelectedGuide(guide)}
                className="p-6 transition-all duration-300 border-2 cursor-pointer rounded-2xl bg-background-50 border-primary-100/30 hover:border-secondary-50 hover:shadow-xl hover:shadow-secondary-50/20 hover:scale-105"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <h3 className="flex-1 text-xl font-bold text-secondary-50 font-titre line-clamp-2">
                    {guide.title}
                  </h3>
                  <span className={`ml-2 px-3 py-1 text-xs font-semibold rounded-full text-primary-50 whitespace-nowrap ${getLevelColor(guide.level)}`}>
                    {guide.level}
                  </span>
                </div>

                {/* Content Preview */}
                <p className="mb-4 text-sm text-white line-clamp-4 font-text">
                  {guide.content.substring(0, 150)}...
                </p>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {guide.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 text-xs border rounded-full text-primary-100 border-primary-100/50"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between pt-4 border-t-2 border-primary-100/20">
                  <span className="text-xs text-secondary-50 font-text">
                    {guide.source}
                  </span>
                  <button className="flex items-center gap-1 text-xs font-semibold transition-all duration-300 text-primary-100 hover:text-secondary-50">
                    Lire <ExternalLink className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal for Guide Details */}
      {selectedGuide && (
        <div
          onClick={() => setSelectedGuide(null)}
          className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/70"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto p-8 border-2 rounded-2xl bg-background-50 border-secondary-50/50"
          >
            {/* Close Button */}
            <button
              onClick={() => setSelectedGuide(null)}
              className="absolute text-3xl text-white transition-all duration-300 top-4 right-6 hover:text-secondary-50"
            >
              ×
            </button>

            {/* Guide Header */}
            <div className="mb-6">
              <div className="flex items-start justify-start mb-4">
                <h2 className="flex-1 pr-8 text-3xl font-bold text-secondary-50 font-titre">
                  {selectedGuide.title}
                </h2>
              </div>

              <div className="flex flex-row items-center justify-between w-full mb-4">
                {/* Tags */}
                <div className="flex flex-wrap gap-2">
                  {selectedGuide.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 text-sm border rounded-full text-primary-100 border-primary-100/50"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
                <span className={`px-4 py-2 text-sm font-semibold rounded-full text-primary-50 whitespace-nowrap ${getLevelColor(selectedGuide.level)}`}>
                  {selectedGuide.level}
                </span>
              </div>

              {/* Source */}
              <p className="text-sm text-secondary-50 font-text">
                Source: {selectedGuide.source}
              </p>
            </div>

            {/* Guide Content */}
            <div className="prose prose-lg max-w-none">
              <p className="text-base leading-relaxed text-white whitespace-pre-line font-text">
                {selectedGuide.content}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}