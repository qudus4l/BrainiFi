import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSend, FiMessageCircle, FiUser, FiLoader, FiX } from 'react-icons/fi';

interface Message {
    id: string;
    type: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

interface Props {
    mode: 'floating' | 'fullpage';
    onClose?: () => void;
}

export const StudyCompanion: React.FC<Props> = ({ mode, onClose }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            type: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simulate AI response (replace with actual API call later)
        setTimeout(() => {
            const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                type: 'assistant',
                content: "I'm your study companion! I'll help explain concepts from your materials. (API integration pending)",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, aiMessage]);
            setIsTyping(false);
        }, 1500);
    };

    const chatInterface = (
        <div className="h-full flex flex-col">
            {/* Header with close button */}
            <div className="p-4 border-b border-gray-700 flex justify-between items-center">
                <div>
                    <h2 className="text-xl font-bold text-gradient">BrainiBuddy</h2>
                    <p className="text-sm text-gray-400">Your personal study companion</p>
                </div>
                {onClose && (
                    <button 
                        onClick={onClose}
                        className="p-2 hover:bg-gray-700 rounded-full transition-colors"
                    >
                        <FiX className="w-5 h-5" />
                    </button>
                )}
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <AnimatePresence>
                    {messages.map((message) => (
                        <motion.div
                            key={message.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`flex items-start space-x-2 max-w-[80%] ${
                                message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                            }`}>
                                <div className={`p-2 rounded-full ${
                                    message.type === 'user' ? 'bg-violet-500' : 'bg-blue-500'
                                }`}>
                                    {message.type === 'user' ? 
                                        <FiUser className="w-4 h-4" /> : 
                                        <FiMessageCircle className="w-4 h-4" />
                                    }
                                </div>
                                <div className={`p-3 rounded-lg ${
                                    message.type === 'user' 
                                        ? 'bg-violet-500/20 text-violet-100' 
                                        : 'bg-blue-500/20 text-blue-100'
                                }`}>
                                    {message.content}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                    {isTyping && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center space-x-2 text-gray-400"
                        >
                            <FiMessageCircle className="w-4 h-4" />
                            <div className="flex space-x-1">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask me anything about your study materials..."
                        className="flex-1 bg-gray-800/50 text-gray-100 rounded-lg px-4 py-2 
                                 focus:outline-none focus:ring-2 focus:ring-violet-500"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isTyping}
                        className={`glass-button px-4 py-2 ${
                            !input.trim() || isTyping ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    >
                        {isTyping ? (
                            <FiLoader className="w-5 h-5 animate-spin" />
                        ) : (
                            <FiSend className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </form>
        </div>
    );

    if (mode === 'fullpage') {
        return (
            <div className="min-h-screen p-4">
                <div className="max-w-4xl mx-auto">
                    <div className="glass-card h-[70vh]">
                        {chatInterface}
                    </div>

                    {/* Additional features for full page mode */}
                    <div className="mt-6 grid grid-cols-2 gap-4">
                        <div className="glass-card p-4">
                            <h3 className="text-lg font-semibold mb-2">Recent Topics</h3>
                            <div className="text-gray-400">Coming soon...</div>
                        </div>
                        <div className="glass-card p-4">
                            <h3 className="text-lg font-semibold mb-2">Saved Responses</h3>
                            <div className="text-gray-400">Coming soon...</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // Floating mode
    return (
        <div className="glass-card h-[600px] flex flex-col">
            {chatInterface}
        </div>
    );
}; 