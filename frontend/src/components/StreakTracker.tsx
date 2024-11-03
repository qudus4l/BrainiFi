import React from 'react';
import { motion } from 'framer-motion';
import { FiZap } from 'react-icons/fi';

interface Props {
    streak: number;
    todayProgress: number;
}

export const StreakTracker: React.FC<Props> = ({ streak, todayProgress }) => {
    return (
        <div className="glass-card p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
                <div className="relative">
                    <FiZap className="w-6 h-6 text-yellow-400" />
                    <motion.div
                        className="absolute inset-0 text-yellow-400"
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    >
                        <FiZap className="w-6 h-6" />
                    </motion.div>
                </div>
                <div>
                    <div className="text-lg font-bold text-gradient">{streak} Day Streak!</div>
                    <div className="text-sm text-gray-400">Keep it going! 🔥</div>
                </div>
            </div>
            <div className="text-right">
                <div className="text-sm text-gray-400">Today's Progress</div>
                <div className="text-lg font-bold">{todayProgress}%</div>
            </div>
        </div>
    );
}; 