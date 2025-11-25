import React, { useState } from "react";
import { BookCheck, BookOpen, ChevronLeft, ChevronRight, MessageSquare, Search, TrendingUp, Trophy, Users } from "lucide-react";
import { useAppContext } from "../context/appContext";
import paysage from "/assets/paysage.png";

export default function Home() {
  const [currentGuideIndex, setCurrentGuideIndex] = useState(0);
  const { guides } = useAppContext();
  console.log(guides)

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
        <h1 className="mb-6 text-6xl font-bold text-transparent bg-clip-text bg-secondary-50 font-titre">
          RuneBook
        </h1>
        <p className="mb-4 text-4xl font-semibold text-secondary-50 font-titre">
          Where League of Legends feel logical
        </p>
        <p className="max-w-3xl mb-8 text-xl leading-relaxed text-white font-text">
          Ton guide pour <span className="font-semibold text-secondary-50">comprendre</span> League of Legends et
          pas seulement devenir plus fort. Apprends la logique derrière chaque élément du jeu!
        </p>
        <img 
          src={paysage} 
          alt="heatmap" 
          className="w-5/12 mb-12 rounded-full">
        </img>
        <div className="flex gap-6">
          <a 
            href="/catalog"
            className="px-8 py-4 text-lg font-semibold transition-all duration-300 border-2 rounded-lg border-secondary-50 text-secondary-50 hover:bg-secondary-50 hover:text-primary-50 hover:scale-105"
          >
            Explorer le Catalogue
          </a>
          <a 
            href="/chatbot"
            className="px-8 py-4 text-lg font-semibold transition-all duration-300 border-2 rounded-lg border-primary-100 text-primary-100 hover:bg-primary-100 hover:text-primary-50 hover:scale-105"
          >
            Parler au Chatbot
          </a>
        </div>
      </div>

      {/* Journey Section */}
      <div className="px-6 py-16 mx-auto max-w-7xl">
        <h2 className="mb-4 text-4xl font-bold text-center text-secondary-50 font-titre">
          Les différents objectifs
        </h2>
        <p className="mb-16 text-xl text-center text-white font-text">
          Pour tout type de joueur voulant comprendre cet univers
        </p>
        
        <div className="flex items-center justify-center mb-16">
          <div className="flex items-center w-full max-w-4xl">
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-primary-100">
                <Search className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-white">Découvrir</p>
              <p className="text-sm text-center text-white">Les bases du jeu</p>
            </div>
            <div className="flex-1 h-1 bg-primary-100"></div>
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-secondary-50">
                <BookCheck className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-white">Assimiler</p>
              <p className="text-sm text-center text-white">Les mécaniques</p>
            </div>
            <div className="flex-1 h-1 bg-secondary-50"></div>
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 bg-red-400 rounded-full">
                <Trophy className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-white">Comprendre</p>
              <p className="text-sm text-center text-white">La scène esport</p>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 py-16 mx-auto max-w-7xl">
        <h2 className="mb-4 text-4xl font-bold text-center text-secondary-50 font-titre">
          Notre Chatbot
        </h2>
        <p className="mb-12 text-xl text-center text-white font-text">
          Un assistant IA qui comprend tes besoins et ton niveau
        </p>

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
        
        <div className="relative">
          <div className="w-5/6 mx-auto overflow-hidden">
            <div 
              className="flex transition-transform duration-500 ease-in-out"
              style={{ transform: `translateX(-${currentGuideIndex * 100}%)` }}
            >
              {guides.map((guide, index) => (
                <div key={guide.id_guide} className="flex-shrink-0 w-full px-4">
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
                      <button className="px-6 py-2 font-semibold transition-all duration-300 rounded-lg bg-secondary-50 text-primary-50 hover:bg-secondary-50 hover:scale-105">
                        Lire le guide
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Navigation Buttons */}
          <button
            onClick={() => setCurrentGuideIndex(currentGuideIndex === 0 ? guides.length - 1 : currentGuideIndex-1)}
            className="absolute left-0 p-3 transition-all duration-300 transform -translate-y-1/2 rounded-full top-1/2 bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
          
          <button
            onClick={() => setCurrentGuideIndex(currentGuideIndex === guides.length - 1 ? 0 : currentGuideIndex+1)}
            className="absolute right-0 p-3 transition-all duration-300 transform -translate-y-1/2 rounded-full top-1/2 bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
          
          {/* Indicators */}
          <div className="flex justify-center gap-2 mt-8">
            {guides.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentGuideIndex(index)}
                className={`h-2 rounded-full transition-all duration-300 ${
                  index === currentGuideIndex 
                    ? 'w-8 bg-primary-100' 
                    : 'w-2 bg-primary-100/30 hover:bg-primary-100/50'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="px-6 py-20 mx-auto text-center max-w-7xl">
        <div className="p-12 border-2 rounded-3xl bg-background-50 border-primary-100/30">
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
            Commencer l'Aventure
          </a>
        </div>
      </div>
    </div>
  );
}