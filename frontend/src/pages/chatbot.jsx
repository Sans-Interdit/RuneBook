import React, { useState, useRef, useEffect } from "react";
import { Send, MessageSquare, Plus, Trash2, Clock, Sparkles, User, Bot } from "lucide-react";
import { addConv, delConv, getConv } from "../api/conversation";
import { addMsg } from "../api/message"
import { chat } from "../api/chat";
import { useAppContext } from "../context/appContext";

export default function Chatbot() {
  const [conversations, setConversations] = useState([]);
  const { getIdContext } = useAppContext();

  const [currentConversationId, setCurrentConversationId] = useState(0);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const currentConversation = conversations.find(conv => conv.id === currentConversationId);

  useEffect(() => {
    getIdContext()
    .then((token) => {
       if (token) {
        getConversations();
       }
       else {
          window.location.href = '/login';
       }
    })
  }, [])

  const getConversations = async () => {
    const res = await getConv();
    if (res.status == 200) {
      const conversations = res.data.map(conv => ({
        ...conv,
        timestamp: new Date(conv.timestamp)
      }));
      setConversations(conversations);
      setCurrentConversationId(conversations[0].id);
    }
  }

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation?.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { role: "user", content: inputMessage };
    
    // Add user message
    setConversations(prev => prev.map(conv => 
      conv.id === currentConversationId 
        ? { ...conv, messages: [...conv.messages, userMessage] }
        : conv
    ));
    addMsg(currentConversationId, inputMessage, "user");

    setInputMessage("");
    setIsTyping(true);

    // AI response
    const res = await chat(inputMessage);
    const aiResponse = {role: "assistant", content: res}
    setConversations(prev => prev.map(conv => 
      conv.id === currentConversationId 
        ? { ...conv, messages: [...conv.messages, aiResponse] }
        : conv
    ));
    addMsg(currentConversationId, res, "assistant");

    setIsTyping(false);

    getConversations();
  };

  const handleNewConversation = async () => {
    const title = "Nouvelle conversation " + (conversations.length + 1);
    const res = await addConv(title);
    const id_conv = res?.data?.id

    if (id_conv) {
      const newConv = {
        id: id_conv,
        title: title,
        timestamp: new Date(),
        messages: []
      };

      setConversations(prev => [newConv, ...prev]);
      setCurrentConversationId(newConv.id);
    }
  };

  const handleDeleteConversation = async (id) => {
    if (conversations.length === 0) return;

    const res = await delConv(id);
    if (res.status === 200) {
      setConversations(prev => prev.filter(conv => conv.id !== id));
      if (currentConversationId === id) {
        setCurrentConversationId(conversations.find(conv => conv.id !== id)?.id || conversations[0].id);
      }
    }
  };

  const formatTimestamp = (date) => {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return "À l'instant";
    if (minutes < 60) return `Il y a ${minutes} min`;
    if (hours < 24) return `Il y a ${hours}h`;
    return `Il y a ${days}j`;
  };

  return (
    <div className="flex flex-1 min-h-0 bg-primary-50">
      {/* Sidebar - Conversations History */}
      <div className="flex flex-col h-full min-h-0 border-r-2 w-80 border-primary-100/30">
        {/* Sidebar Header */}
        <div className="p-6 border-b-2 border-primary-100/30">
          <h2 className="mb-4 text-2xl font-bold text-secondary-50 font-titre">
            Mes Conversations
          </h2>
          <button
            onClick={handleNewConversation}
            className="flex items-center justify-center w-full gap-2 px-4 py-3 font-semibold transition-all duration-300 rounded-lg bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-105"
          >
            <Plus className="w-5 h-5" />
            Nouvelle conversation
          </button>
        </div>

        {/* Conversations List */}
        <div className="flex-1 min-h-0 overflow-y-auto scrollbar-thin scrollbar-thumb-primary-100/40 ">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setCurrentConversationId(conv.id)}
              className={`p-4 border-b border-primary-100/20 cursor-pointer transition-all duration-300 group hover:bg-primary-100/10 ${
                currentConversationId === conv.id ? 'bg-primary-100/20 border-l-4 border-l-secondary-50' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="mb-1 font-semibold truncate text-secondary-50 font-titre">
                    {conv.title}
                  </h3>
                  <div className="flex items-center gap-1 text-xs text-primary-100">
                    <Clock className="w-3 h-3" />
                    {formatTimestamp(conv.timestamp)}
                  </div>
                  {conv.messages.length > 0 && (
                    <p className="mt-2 text-sm text-white truncate">
                      {conv.messages[conv.messages.length - 1].content}
                    </p>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteConversation(conv.id);
                  }}
                  className="flex-shrink-0 p-2 ml-2 transition-all duration-300 rounded-lg opacity-0 text-primary-100 hover:bg-red-400/20 hover:text-red-400 group-hover:opacity-100"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1">
        {/* Chat Header */}
        <div className="p-6 border-b-2 border-primary-100/30">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-12 h-12 rounded-full bg-primary-100">
              <MessageSquare className="w-6 h-6 text-primary-50" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-secondary-50 font-titre">
                {currentConversation?.title || "Chatbot RuneBook"}
              </h1>
              <p className="text-sm text-primary-100 font-text">
                Pose-moi toutes tes questions sur League of Legends
              </p>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 p-6 overflow-y-auto">
          {currentConversation?.messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="flex items-center justify-center w-20 h-20 mb-6 rounded-full bg-secondary-50">
                <MessageSquare className="w-10 h-10 text-primary-50" />
              </div>
              <h2 className="mb-2 text-2xl font-bold text-secondary-50 font-titre">
                Prêt à Apprendre ?
              </h2>
              <p className="max-w-md text-white font-text">
                Je suis là pour t'aider à comprendre League of Legends. 
                Pose-moi n'importe quelle question, je répondrai de manière simple et claire !
              </p>
              <div className="grid grid-cols-2 gap-4 mt-8">
                <button
                  onClick={() => setInputMessage("C'est quoi le farming ?")}
                  className="p-4 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105"
                >
                  <p className="text-sm font-semibold text-secondary-50">C'est quoi le farming ?</p>
                </button>
                <button
                  onClick={() => setInputMessage("Explique-moi les rôles")}
                  className="p-4 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105"
                >
                  <p className="text-sm font-semibold text-secondary-50">Explique-moi les rôles</p>
                </button>
                <button
                  onClick={() => setInputMessage("Comment bien débuter ?")}
                  className="p-4 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105"
                >
                  <p className="text-sm font-semibold text-secondary-50">Comment bien débuter ?</p>
                </button>
                <button
                  onClick={() => setInputMessage("C'est quoi la méta ?")}
                  className="p-4 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105"
                >
                  <p className="text-sm font-semibold text-secondary-50">C'est quoi la méta ?</p>
                </button>
              </div>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto space-y-6">
              {currentConversation?.messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
                >
                  {/* Avatar */}
                  <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                    message.role === 'user' 
                      ? 'bg-primary-100' 
                      : 'bg-secondary-50'
                  }`}>
                    {message.role === 'user' ? (
                      <User className="w-5 h-5 text-primary-50" />
                    ) : (
                      <Bot className="w-5 h-5 text-primary-50" />
                    )}
                  </div>

                  {/* Message Bubble */}
                  <div className={`flex-1 max-w-2xl ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                    <div className={`inline-block p-4 rounded-2xl ${
                      message.role === 'user'
                        ? 'bg-primary-100 text-primary-50 rounded-tr-none'
                        : 'bg-background-50 border-2 border-primary-100/30 text-white rounded-tl-none'
                    }`}>
                      <p className="text-sm leading-relaxed whitespace-pre-wrap font-text">
                        {message.content}
                      </p>
                    </div>
                  </div>
                </div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <div className="flex gap-4">
                  <div className="flex items-center justify-center flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-primary-100 to-secondary-50">
                    <Bot className="w-5 h-5 text-primary-50" />
                  </div>
                  <div className="inline-block p-4 border-2 rounded-tl-none rounded-2xl bg-primary-50 border-primary-100/30">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-secondary-50 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 rounded-full bg-secondary-50 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 rounded-full bg-secondary-50 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-6 border-t-2 border-primary-100/30">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-4">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Pose ta question ici..."
                className="flex-1 px-6 py-4 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 border-primary-100/30 placeholder-white/50 focus:border-secondary-50 focus:outline-none font-text"
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="px-6 py-4 font-semibold transition-all duration-300 rounded-lg bg-primary-100 text-primary-50 hover:bg-secondary-50 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="mt-3 text-xs text-center text-primary-100">
              L'assistant peut faire des erreurs. Vérifie les informations importantes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}