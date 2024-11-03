import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCommand } from 'react-icons/fi';

interface Props {
    show: boolean;
    keys: string[];
    action: string;
}

export const KeyboardIndicator: React.FC<Props> = ({ show, keys, action }) => {
    return (
        <AnimatePresence>
            {show && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="fixed bottom-6 left-1/2 transform -translate-x-1/2 
                             glass-card px-4 py-2 flex items-center space-x-2"
                >
                    {keys.map((key, index) => (
                        <React.Fragment key={key}>
                            <kbd className="px-2 py-1 bg-gray-800 rounded text-sm text-gray-200 
                                         border border-gray-700">
                                {key}
                            </kbd>
                            {index < keys.length - 1 && <span className="text-gray-400">+</span>}
                        </React.Fragment>
                    ))}
                    <span className="text-gray-400 ml-2">to {action}</span>
                </motion.div>
            )}
        </AnimatePresence>
    );
}; 