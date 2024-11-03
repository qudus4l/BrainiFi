import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiAward, FiStar, FiTrendingUp } from 'react-icons/fi';

interface Props {
    achievement: {
        title: string;
        description: string;
        type: 'milestone' | 'streak' | 'mastery';
    };
    onClose: () => void;
}

export const AchievementPopup: React.FC<Props> = ({ achievement, onClose }) => {
    const icons = {
        milestone: <FiAward className="w-8 h-8 text-yellow-400" />,
        streak: <FiTrendingUp className="w-8 h-8 text-green-400" />,
        mastery: <FiStar className="w-8 h-8 text-purple-400" />
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 50 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 50 }}
                className="fixed bottom-6 left-1/2 transform -translate-x-1/2 
                           glass-card p-6 flex items-center space-x-4"
            >
                <div className="p-3 bg-gray-800 rounded-full">
                    {icons[achievement.type]}
                </div>
                <div>
                    <h3 className="text-lg font-semibold text-gradient">
                        Achievement Unlocked!
                    </h3>
                    <p className="text-gray-300">{achievement.title}</p>
                    <p className="text-sm text-gray-400">{achievement.description}</p>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}; 