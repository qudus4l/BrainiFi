import React from 'react';
import { motion } from 'framer-motion';

interface Props {
    className?: string;
}

export const Skeleton: React.FC<Props> = ({ className = '' }) => {
    return (
        <motion.div
            className={`bg-gray-700/50 rounded-lg ${className}`}
            animate={{
                opacity: [0.5, 0.7, 0.5],
                transition: {
                    duration: 1.5,
                    repeat: Infinity,
                }
            }}
        />
    );
};

export const QuestionSkeleton: React.FC = () => {
    return (
        <div className="glass-card p-6 space-y-4">
            <div className="flex justify-between items-start">
                <Skeleton className="h-6 w-32" />
                <div className="flex space-x-2">
                    <Skeleton className="h-6 w-16" />
                    <Skeleton className="h-6 w-16" />
                </div>
            </div>
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-32 w-full" />
        </div>
    );
}; 