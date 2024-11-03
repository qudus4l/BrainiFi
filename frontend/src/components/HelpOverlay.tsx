import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCommand, FiKey, FiX } from 'react-icons/fi';

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export const HelpOverlay: React.FC<Props> = ({ isOpen, onClose }) => {
    const shortcuts = [
        { keys: ['⌘/Ctrl', 'Q'], description: 'Quick Review mode' },
        { keys: ['⌘/Ctrl', 'D'], description: 'Deep Study mode' },
        { keys: ['⌘/Ctrl', 'R'], description: 'Revision mode' },
        { keys: ['⌘/Ctrl', 'T'], description: 'Test Prep mode' },
        { keys: ['ESC'], description: 'Back to mode selection' },
        { keys: ['Space'], description: 'Show/Hide hint' },
    ];

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 0.5 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black"
                        onClick={onClose}
                    />
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="fixed inset-x-0 top-20 mx-auto max-w-2xl glass-card p-6"
                    >
                        <div className="flex justify-between items-start mb-6">
                            <h2 className="text-xl font-bold text-gradient">Keyboard Shortcuts</h2>
                            <button 
                                onClick={onClose}
                                className="text-gray-400 hover:text-gray-200"
                            >
                                <FiX className="w-6 h-6" />
                            </button>
                        </div>
                        
                        <div className="grid gap-4">
                            {shortcuts.map(({ keys, description }) => (
                                <div key={description} className="flex items-center justify-between">
                                    <span className="text-gray-300">{description}</span>
                                    <div className="flex items-center space-x-2">
                                        {keys.map(key => (
                                            <kbd 
                                                key={key}
                                                className="px-2 py-1 bg-gray-800 rounded text-sm text-gray-200 border border-gray-700"
                                            >
                                                {key}
                                            </kbd>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="mt-6 p-4 bg-violet-500/10 rounded-lg">
                            <h3 className="text-violet-300 font-medium mb-2">Pro Tips</h3>
                            <ul className="space-y-2 text-gray-300">
                                <li>• Use keyboard shortcuts for faster navigation</li>
                                <li>• Complete each mode in order for best results</li>
                                <li>• Review feedback carefully to improve your answers</li>
                            </ul>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}; 