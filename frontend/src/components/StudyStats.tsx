import React from 'react';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiClock, FiCheckCircle } from 'react-icons/fi';

interface Props {
    questionsAnswered: number;
    averageScore: number;
    timeSpent: number;  // in minutes
}

export const StudyStats = React.memo<Props>(({ questionsAnswered, averageScore, timeSpent }) => {
    const stats = [
        {
            icon: <FiCheckCircle className="w-5 h-5 text-green-400" />,
            label: 'Questions Completed',
            value: questionsAnswered,
            suffix: ''
        },
        {
            icon: <FiTrendingUp className="w-5 h-5 text-blue-400" />,
            label: 'Average Score',
            value: averageScore,
            suffix: '%'
        },
        {
            icon: <FiClock className="w-5 h-5 text-violet-400" />,
            label: 'Time Studying',
            value: timeSpent,
            suffix: 'm'
        }
    ];

    return (
        <div className="grid grid-cols-3 gap-4">
            {stats.map(({ icon, label, value, suffix }) => (
                <motion.div
                    key={label}
                    className="glass-card p-4 text-center"
                    whileHover={{ scale: 1.02 }}
                >
                    <div className="flex justify-center mb-2">{icon}</div>
                    <div className="text-2xl font-bold text-gradient">
                        {value}{suffix}
                    </div>
                    <div className="text-sm text-gray-400">{label}</div>
                </motion.div>
            ))}
        </div>
    );
}); 