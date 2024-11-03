import React from 'react';
import { motion } from 'framer-motion';
import { FiCheckCircle } from 'react-icons/fi';
import { useSession } from '@context/SessionContext';
import { StudyModeType } from '@/types';

interface Props {
    currentIndex: number;
    totalQuestions: number;
    mode: StudyModeType;
}

export const QuestionProgress: React.FC<Props> = ({ 
    currentIndex, 
    totalQuestions,
    mode
}) => {
    const { progressByMode } = useSession();
    const progress = progressByMode[mode];

    return (
        <div className="glass-card p-4 mb-6">
            <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-400">
                    Question {currentIndex + 1} of {totalQuestions}
                </span>
                <span className="text-sm text-gray-400">
                    {progress.completed} Completed
                </span>
            </div>
            <div className="relative h-2 bg-gray-700 rounded-full overflow-hidden">
                <motion.div
                    className="absolute left-0 top-0 h-full bg-violet-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${(progress.completed / totalQuestions) * 100}%` }}
                    transition={{ duration: 0.5 }}
                />
                {Array.from({ length: totalQuestions }).map((_, i) => (
                    <div
                        key={i}
                        className={`absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full 
                                  ${i === currentIndex ? 'bg-violet-400' : 
                                    i < progress.completed ? 'bg-green-400' : 
                                    'bg-gray-600'}`}
                        style={{ left: `${(i / (totalQuestions - 1)) * 100}%` }}
                    >
                        {i < progress.completed && (
                            <FiCheckCircle className="absolute -top-6 left-1/2 -translate-x-1/2 text-green-400" />
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}; 