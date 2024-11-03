import React from 'react';
import { FiFileText, FiUpload } from 'react-icons/fi';
import { motion } from 'framer-motion';

interface Props {
    title: string;
    description: string;
    icon?: React.ReactNode;
    action?: {
        label: string;
        onClick: () => void;
    };
}

export const EmptyState: React.FC<Props> = ({ 
    title, 
    description, 
    icon = <FiFileText className="w-12 h-12" />,
    action 
}) => {
    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-12 text-center"
        >
            <div className="flex flex-col items-center">
                <div className="text-violet-400 mb-4">
                    {icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-100 mb-2">
                    {title}
                </h3>
                <p className="text-gray-400 max-w-md mb-6">
                    {description}
                </p>
                {action && (
                    <button
                        onClick={action.onClick}
                        className="glass-button flex items-center"
                    >
                        <FiUpload className="w-4 h-4 mr-2" />
                        {action.label}
                    </button>
                )}
            </div>
        </motion.div>
    );
}; 