import React from "react";
import { BookCheck, BookOpen, MessageSquare, Search, TrendingUp, Trophy, Users } from "lucide-react";

export default function Home() {
  const features = [
    {
      icon: <BookOpen className="w-12 h-12" />,
      title: "Catalogue de Guides",
      description: "Découvre des articles détaillés sur les bases, les champions, les objets et les stratégies de League of Legends.",
      link: "/catalog",
      color: "from-purple-500 to-secondary-50"
    },
    {
      icon: <MessageSquare className="w-12 h-12" />,
      title: "Chatbot IA",
      description: "Pose tes questions à notre assistant IA bienveillant qui t'aidera à comprendre le jeu à ton rythme, sans te submerger d'informations.",
      link: "/chatbot",
      color: "from-secondary-50 to-purple-500"
    },
    // {
    //   icon: <TrendingUp className="w-12 h-12" />,
    //   title: "Comprendre la Méta",
    //   description: "Explore les tendances actuelles, les compositions d'équipe et les stratégies qui dominent le jeu.",
    //   link: "/catalog",
    //   color: "from-primary-100 to-purple-500"
    // },
    // {
    //   icon: <Users className="w-12 h-12" />,
    //   title: "Esport & Compétition",
    //   description: "Plonge dans l'univers de l'esport LoL, comprends les tournois et suis les équipes professionnelles.",
    //   link: "/catalog",
    //   color: "from-purple-500 to-primary-100"
    // }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background-50 via-background-100 to-background-50">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center px-6 py-20 text-center">
        <h1 className="mb-6 text-6xl font-bold text-transparent bg-clip-text bg-primary-100 font-titre">
          RuneBook
        </h1>
        <p className="mb-4 text-4xl font-semibold text-secondary-50 font-titre">
          Where League of Legends feel logical
        </p>
        <p className="max-w-3xl mb-12 text-xl leading-relaxed text-white font-text">
          Ton guide pour <span className="font-semibold text-secondary-50">comprendre</span> League of Legends et
          pas seulement devenir plus fort. Apprends la logique derrière chaque élément du jeu!
        </p>
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
        <h2 className="mb-4 text-4xl font-bold text-center text-primary-100 font-titre">
          Les différents objectif
        </h2>
        <p className="mb-16 text-xl text-center text-white font-text">
          Pour tout type de joueur voulant comprendre cet univers
        </p>
        
        <div className="flex items-center justify-center mb-16">
          <div className="flex items-center w-full max-w-4xl">
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-gradient-to-br from-white to-secondary-50">
                <Search className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-primary-100">Découvrir</p>
              <p className="text-sm text-center text-secondary-50">Les bases du jeu</p>
            </div>
            <div className="flex-1 h-1 bg-secondary-50"></div>
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-gradient-to-br from-secondary-50 to-purple-500">
                <BookCheck className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-primary-100">Assimiler</p>
              <p className="text-sm text-center text-secondary-50">Les mécaniques</p>
            </div>
            <div className="flex-1 h-1 bg-purple-500"></div>
            <div className="flex flex-col items-center flex-1">
              <div className="flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-gradient-to-br from-purple-500 to-primary-100">
                <Trophy className="w-2/4 h-2/4" />
              </div>
              <p className="text-lg font-semibold text-center text-primary-100">Comprendre</p>
              <p className="text-sm text-center text-secondary-50">La scène esport</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="px-6 py-16 mx-auto max-w-7xl">
        <h2 className="mb-16 text-4xl font-bold text-center text-primary-100 font-titre">
          Nos Fonctionnalités
        </h2>
        
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          {features.map((feature, index) => (
            <a 
              key={index}
              href={feature.link}
              className="relative p-8 transition-all duration-300 border rounded-2xl bg-primary-50 border-primary-50/20 hover:border-primary-100 hover:scale-105 group backdrop-blur-sm"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-10 rounded-2xl transition-opacity duration-300`}></div>
              
              <div className="relative">
                <div className={`inline-flex p-4 mb-6 rounded-xl bg-gradient-to-br ${feature.color} text-primary-50`}>
                  {feature.icon}
                </div>
                
                <h3 className="mb-4 text-2xl font-bold text-primary-100 font-titre">
                  {feature.title}
                </h3>
                
                <p className="mb-6 leading-relaxed text-white font-text">
                  {feature.description}
                </p>
                
                <div className="flex items-center transition-transform duration-300 text-primary-100 group-hover:translate-x-2">
                  <span className="mr-2 font-semibold">En savoir plus</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="px-6 py-20 mx-auto text-center max-w-7xl">
        <div className="p-12 border-2 rounded-3xl bg-gradient-to-br from-primary-50 to-background-100 border-primary-100/30">
          <h2 className="mb-6 text-4xl font-bold text-primary-100 font-titre">
            Prêt à Comprendre League of Legends ?
          </h2>
          <p className="max-w-2xl mx-auto mb-8 text-xl text-white font-text">
            Rejoins RuneBook et commence ton voyage d'apprentissage avec un guide bienveillant qui ne te submergera jamais d'informations.
          </p>
          <a 
            href="/inscription"
            className="inline-block px-10 py-5 text-xl font-bold transition-all duration-300 rounded-xl bg-gradient-to-r from-primary-100 to-purple-500 text-primary-50 hover:scale-110 hover:shadow-2xl hover:shadow-primary-100/50"
          >
            Commencer l'Aventure
          </a>
        </div>
      </div>
    </div>
  );
}