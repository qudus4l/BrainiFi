import React from 'react';
import { motion } from 'framer-motion';
import { FiHeart } from 'react-icons/fi';

export const Footer: React.FC = () => {
    return (
        <footer className="glass-card mt-auto py-4">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-center space-x-2">
                    <span className="text-gray-400">Made with</span>
                    <motion.div
                        animate={{ 
                            scale: [1, 1.2, 1],
                            rotate: [0, 10, -10, 0]
                        }}
                        transition={{ 
                            duration: 1.5,
                            repeat: Infinity,
                            repeatType: "reverse"
                        }}
                    >
                        <FiHeart className="w-4 h-4 text-red-400 fill-current" />
                    </motion.div>
                    <span className="text-gray-400">for</span>
                    <span className="text-gradient font-semibold">Nigerian Students</span>
                    <span className="text-green-500">🇳🇬</span>
                </div>
            </div>
        </footer>
    );
}; 