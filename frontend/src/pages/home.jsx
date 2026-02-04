import React, { useState } from "react";
import { BookCheck, ChevronLeft, ChevronRight, MessageSquare, Search, Trophy } from "lucide-react";
import { useAppContext } from "../context/appContext";
import paysage from "/assets/paysage.png";
import search from "/assets/search.png";
import living_library from "/assets/living_library.png";
import gif4 from "/assets/ezgif-349f579d4f79ced3.gif";
import img4 from "/assets/faker.png";
import gif5 from "/assets/ezgif-4be597bc5e6fa90a.gif";
import img5 from "/assets/baron.png";
import gif7 from "/assets/ezgif-5c6a9a0b15a5c4d2.gif";
import img7 from "/assets/ezreal.png";

export default function Home() {
  const [currentGuideIndex, setCurrentGuideIndex] = useState(0);
  const { guides } = useAppContext();
  const [selectedGuide, setSelectedGuide] = useState(null);

  const getLevelColor = (level) => {
    if (level === "New Player") return "bg-green-400";
    if (level === "Average Player") return "bg-secondary-50";
    return "bg-red-400";
  };

  const map_fr = (level) => {
    if (level === "New Player") return "Nouveau Joueur";
    if (level === "Average Player") return "Joueur Medium";
    if (level === "Confirmed Player") return "Joueur Confirmé";
  }

  return (
    <div className="flex flex-col overflow-auto bg-primary-50">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center px-6 py-12 text-center">
        <h1 className="mb-4 text-6xl font-bold text-transparent bg-clip-text bg-secondary-50 font-titre">
          RuneBook
        </h1>
        <p className="mb-8 text-4xl font-semibold text-secondary-50 font-titre">
          Where League of Legends feel logical
        </p>
        <p className="max-w-3xl text-xl leading-relaxed text-white font-text">
          Ton guide pour <span className="font-semibold text-secondary-50">comprendre</span> League of Legends et
          pas seulement devenir plus fort. Apprends la logique derrière chaque élément du jeu!
        </p>
        <img 
          src={paysage}
          alt="heatmap" 
          className="object-contain my-12 rounded-full h-[450px]">
        </img>
        <div className="flex gap-10 py-8">
          <a 
            href="/catalog"
            className="px-10 py-6 text-xl font-semibold transition-all duration-300 rounded-lg bg-secondary-50 text-primary-50 hover:scale-105"
          >
            Explorer le Catalogue
          </a>
          <a 
            href="/chatbot"
            className="px-10 py-6 text-xl font-semibold transition-all duration-300 rounded-lg bg-primary-100 text-primary-50 hover:scale-105"
          >
            Parler au Chatbot
          </a>
        </div>
      </div>

    <div className="flex flex-col items-center px-6 py-16">
      <h2 className="mb-4 text-4xl font-bold text-center text-secondary-50 font-titre">
        Les différents objectifs
      </h2>
      <p className="mb-16 text-xl text-center text-white font-text">
        Pour tout type de joueur voulant comprendre cet univers
      </p>
      
      <div className="grid w-3/4 grid-cols-1 gap-8 md:grid-cols-3">
        {/* Découvrir */}
        <div className="relative overflow-hidden transition-all duration-500 border-2 bg-gradient-to-br from-primary-100/20 to-transparent border-primary-100/30 rounded-3xl hover:scale-105 hover:border-primary-100 group">
          <div className="p-8">
            <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-primary-100/10 to-primary-100/5 group">
          
              {/* Image statique */}
              <img
                src={img7} // image fixe (jpg/png)
                alt="Découvrir"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-100 group-hover:opacity-0"
              />

              {/* GIF */}
              <img
                src={gif5}
                loading="lazy"
                alt="Découvrir animé"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-0 group-hover:opacity-100"
              />

              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div>
            {/* GIF Container */}
            {/* <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-primary-100/10 to-primary-100/5">
              <img 
                src={gif5}
                alt="Découvrir"
                className="object-cover w-full h-full transition-opacity duration-300 opacity-80 group-hover:opacity-100"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div> */}
            
            <h3 className="mb-3 text-2xl font-bold text-white">Découvrir</h3>
            <p className="text-lg text-white/80">Les bases du jeu</p>
            
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary-100 to-transparent"></div>
          </div>
        </div>

        {/* Assimiler */}
        <div className="relative overflow-hidden transition-all duration-500 border-2 bg-gradient-to-br from-secondary-50/20 to-transparent border-secondary-50/30 rounded-3xl hover:scale-105 hover:border-secondary-50 group">
          <div className="p-8">
            <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-primary-100/10 to-primary-100/5 group">
              
              {/* Image statique */}
              <img
                src={img5} // image fixe (jpg/png)
                alt="Découvrir"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-100 group-hover:opacity-0"
              />

              {/* GIF */}
              <img
                src={gif7}
                loading="lazy"
                alt="Découvrir animé"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-0 group-hover:opacity-100"
              />

              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div>
            {/* GIF Container */}
            {/* <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-secondary-50/10 to-secondary-50/5">
              <img 
                src={gif7}
                alt="Assimiler"
                className="object-cover w-full h-full transition-opacity duration-300 opacity-80 group-hover:opacity-100"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div> */}
            
            <h3 className="mb-3 text-2xl font-bold text-white">Assimiler</h3>
            <p className="text-lg text-white/80">Les mécaniques</p>
            
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-secondary-50 to-transparent"></div>
          </div>
        </div>

        {/* Comprendre */}
        <div className="relative overflow-hidden transition-all duration-500 border-2 bg-gradient-to-br from-red-400/20 to-transparent border-red-400/30 rounded-3xl hover:scale-105 hover:border-red-400 group">
          <div className="p-8">
            <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-primary-100/10 to-primary-100/5 group">
              {/* Image statique */}
              <img
                src={img4} // image fixe (jpg/png)
                alt="Découvrir"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-100 group-hover:opacity-0"
              />

              {/* GIF */}
              <img
                src={gif4}
                loading="lazy"
                alt="Découvrir animé"
                className="absolute inset-0 object-cover w-full h-full transition-opacity duration-300 opacity-0 group-hover:opacity-100"
              />

              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div>
            {/* GIF Container */}
            {/* <div className="relative mb-6 overflow-hidden rounded-2xl h-52 bg-gradient-to-br from-red-400/10 to-red-400/5">
              <img 
                src={gif4} 
                alt="Comprendre"
                className="object-cover w-full h-full transition-opacity duration-300 opacity-80 group-hover:opacity-100"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div> */}
            
            <h3 className="mb-3 text-2xl font-bold text-white">Comprendre</h3>
            <p className="text-lg text-white/80">La scène esport</p>
            
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-400 to-transparent"></div>
          </div>
        </div>
      </div>

      {/* Progress indicator */}
      <div className="flex items-center justify-center gap-3 mt-12">
        <div className="w-3 h-3 rounded-full bg-primary-100 animate-pulse"></div>
        <div className="w-12 h-1 bg-primary-100/50"></div>
        <div className="w-3 h-3 rounded-full bg-secondary-50 animate-pulse" style={{animationDelay: '0.2s'}}></div>
        <div className="w-12 h-1 bg-secondary-50/50"></div>
        <div className="w-3 h-3 bg-red-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
      </div>
    </div>

      <div className="px-6 py-16 mx-auto max-w-7xl">
        <h2 className="mb-4 text-4xl font-bold text-center text-secondary-50 font-titre">
          Notre Chatbot
        </h2>
        <p className="mb-12 text-xl text-center text-white font-text">
          Un assistant IA qui comprend tes besoins et ton niveau
        </p>
        <div className="flex items-center justify-center w-full">
          <img 
            src={living_library} 
            alt="heatmap" 
            className="object-contain mb-12 rounded-full md:w-1/2 sm:w-full">
          </img>
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          {/* Left side - Description */}
          <div className="flex flex-col justify-center p-8 border-2 rounded-2xl bg-background-50 border-primary-100/30">
            <MessageSquare className="w-16 h-16 mb-6 text-secondary-50" />
            <h3 className="mb-4 text-2xl font-bold text-secondary-50 font-titre">
              Un Apprentissage à Ton Rythme
            </h3>
            <p className="mb-6 text-lg leading-relaxed text-white font-text">
              Notre chatbot IA est conçu pour être <span className="font-semibold text-secondary-50">bienveillant</span> et <span className="font-semibold text-secondary-50">pédagogue</span>. 
              Il adapte ses réponses à ton niveau et ne te submergera jamais d'informations complexes.
            </p>
            <ul className="mb-8 space-y-5">
              <li className="flex items-center">
                <div className="flex items-center justify-center flex-shrink-0 w-6 h-6 mr-3 rounded-full bg-secondary-50">
                  <span className="text-sm font-bold text-primary-50">✓</span>
                </div>
                <span className="text-white font-text">Explications claires et adaptées à ton niveau</span>
              </li>
              <li className="flex items-center">
                <div className="flex items-center justify-center flex-shrink-0 w-6 h-6 mr-3 rounded-full bg-secondary-50">
                  <span className="text-sm font-bold text-primary-50">✓</span>
                </div>
                <span className="text-white font-text">Répond à toutes tes questions sans jugement</span>
              </li>
              <li className="flex items-center">
                <div className="flex items-center justify-center flex-shrink-0 w-6 h-6 mr-3 rounded-full bg-secondary-50">
                  <span className="text-sm font-bold text-primary-50">✓</span>
                </div>
                <span className="text-white font-text">Disponible 24/7 pour t'accompagner</span>
              </li>
            </ul>
            <a 
              href="/chatbot"
              className="inline-block px-8 py-4 text-lg font-semibold text-center transition-all duration-300 rounded-lg bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-105"
            >
              Essayer le Chatbot
            </a>
          </div>

          {/* Right side - Example conversation */}
          <div className="flex flex-col p-8 border-2 rounded-2xl bg-background-50 border-primary-100/30">
            <h3 className="mb-6 text-xl font-bold text-center text-secondary-50 font-titre">
              Exemple de Conversation
            </h3>
            <div className="flex-1 space-y-4">
              {/* User message */}
              <div className="flex justify-end">
                <div className="max-w-xs p-4 rounded-lg bg-primary-100 text-primary-50">
                  <p className="text-sm font-text">C'est quoi le farming et pourquoi c'est important ?</p>
                </div>
              </div>
              
              {/* Bot message */}
              <div className="flex justify-start">
                <div className="max-w-xs p-4 border-2 rounded-lg bg-background-50 border-secondary-50/30">
                  <p className="text-sm text-white font-text">
                    Le farming, c'est simplement tuer les petits monstres (les sbires) pour gagner de l'or. 
                    C'est important car plus tu as d'or, plus tu peux acheter d'objets puissants ! 
                    Veux-tu que je t'explique comment bien farmer ?
                  </p>
                </div>
              </div>

              {/* User message */}
              <div className="flex justify-end">
                <div className="max-w-xs p-4 rounded-lg bg-primary-100 text-primary-50">
                  <p className="text-sm font-text">Oui s'il te plaît !</p>
                </div>
              </div>

              {/* Bot message */}
              <div className="flex justify-start">
                <div className="max-w-xs p-4 border-2 rounded-lg bg-background-50 border-secondary-50/30">
                  <p className="text-sm text-white font-text">
                    Parfait ! Le secret c'est de donner le coup final aux sbires. 
                    Attends que leur vie soit très basse avant de frapper...
                  </p>
                </div>
              </div>
            </div>
            
            <div className="pt-6 mt-6 text-center border-t-2 border-primary-100/30">
              <p className="text-sm text-secondary-50 font-text">
                Des réponses simples, claires et adaptées à toi
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Guides Carousel */}
      <div className="px-6 py-16 mx-auto max-w-7xl">
        <h2 className="mb-4 text-4xl font-bold text-center text-secondary-50 font-titre">
          Nos Guides
        </h2>
        <p className="mb-12 text-xl text-center text-white font-text">
          Découvre nos guides adaptés à tous les niveaux
        </p>
        <div className="flex items-center justify-center w-full">
          <img 
            src={search} 
            alt="heatmap" 
            className="object-contain mb-12 rounded-full md:w-1/2 sm:w-full">
          </img>
        </div>
        <div className="relative">
          <div className="w-5/6 mx-auto overflow-hidden">
            <div 
              className="flex transition-transform duration-500 ease-in-out"
              style={{ transform: `translateX(-${currentGuideIndex * 100}%)` }}
            >
              {Array.isArray(guides) && 
              guides?.slice(0,5).map((guide, index) => (
                <div 
                  key={guide.id_guide}
                  onClick={() => setSelectedGuide(guide)}
                  className="flex-shrink-0 w-full px-4 cursor-pointer"
                >
                  <div className="p-8 transition-all duration-300 border-2 rounded-2xl bg-background-50 border-primary-100/30 hover:border-secondary-50 hover:shadow-xl hover:shadow-secondary-50/20">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-2xl font-bold text-secondary-50 font-titre">
                        {guide.title}
                      </h3>
                      <span className={`px-4 py-2 text-sm font-semibold rounded-full text-primary-50 ${guide.level == "New Player" ? "bg-green-400" : guide.level == "Average Player" ? "bg-secondary-50" : "bg-red-400"}`}>
                        {guide.level}
                      </span>
                    </div>
                    
                    <p className="mb-6 text-white line-clamp-4 font-text">
                      {guide.content.substring(0, 250)}...
                    </p>
                    
                    <div className="flex flex-wrap gap-2 mb-6">
                      {guide.tags.map((tag, tagIndex) => (
                        <span 
                          key={tagIndex}
                          className="px-3 py-1 text-sm border rounded-full text-primary-100 border-primary-100/50"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-secondary-50">
                        Source: {guide.source}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Navigation Buttons */}
          <button
            onClick={() => setCurrentGuideIndex(currentGuideIndex === 0 ? guides.slice(0,5).length - 1 : currentGuideIndex-1)}
            className="absolute left-0 p-3 transition-all duration-300 transform -translate-y-1/2 rounded-full top-1/2 bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
          
          <button
            onClick={() => setCurrentGuideIndex(currentGuideIndex === guides.slice(0,5).length - 1 ? 0 : currentGuideIndex+1)}
            className="absolute right-0 p-3 transition-all duration-300 transform -translate-y-1/2 rounded-full top-1/2 bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
          
          {/* Indicators */}
          <div className="flex justify-center gap-2 mt-8">
            
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="flex flex-col items-center px-6 py-20 text-center">
        <div className="w-4/6 p-12 border-2 rounded-3xl bg-background-50 border-primary-100/30">
          <h2 className="mb-6 text-4xl font-bold text-secondary-50 font-titre">
            Prêt à Comprendre League of Legends ?
          </h2>
          <p className="max-w-2xl mx-auto mb-8 text-xl text-white font-text">
            Rejoins RuneBook et commence ton voyage d'apprentissage avec un guide bienveillant qui ne te submergera jamais d'informations.
          </p>
          <a 
            href="/inscription"
            className="inline-block px-10 py-5 text-xl font-bold transition-all duration-300 rounded-xl bg-primary-100 text-primary-50 hover:scale-110 hover:shadow-2xl hover:shadow-primary-100/50"
          >
            Inscrivez vous
          </a>
        </div>
      </div>

      {/* Modal for Guide Details */}
      {selectedGuide && (
        <div
          onClick={() => setSelectedGuide(null)}
          className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/70"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="relative overflow-y-scroll w-full max-w-4xl max-h-[90vh] p-8 border-2 rounded-2xl bg-primary-50 border-secondary-50/50"
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
                  {map_fr(selectedGuide.level)}
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