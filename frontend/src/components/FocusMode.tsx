import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMinimize2, FiMaximize2 } from 'react-icons/fi';

interface Props {
    isActive: boolean;
    onToggle: () => void;
}

export const FocusMode: React.FC<Props> = ({ isActive, onToggle }) => {
    return (
        <motion.button
            onClick={onToggle}
            className={`fixed top-4 right-4 glass-button p-2 ${
                isActive ? 'bg-violet-500/20' : 'bg-gray-700/20'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
        >
            {isActive ? (
                <FiMinimize2 className="w-5 h-5" />
            ) : (
                <FiMaximize2 className="w-5 h-5" />
            )}
        </motion.button>
    );
}; 