import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiPlus, FiHelpCircle, FiMoon, FiSun, FiDownload } from 'react-icons/fi';

interface Props {
    onHelp: () => void;
    onExport?: () => void;
}

export const FloatingActions: React.FC<Props> = ({ onHelp, onExport }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isDark, setIsDark] = useState(true);

    const toggleTheme = () => {
        setIsDark(!isDark);
        // Theme implementation to be added
    };

    return (
        <div className="fixed bottom-6 right-6 z-50">
            <AnimatePresence>
                {isOpen && (
                    <div className="absolute bottom-16 right-0 space-y-2">
                        <motion.button
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="glass-button w-12 h-12 flex items-center justify-center"
                            onClick={onHelp}
                        >
                            <FiHelpCircle className="w-5 h-5" />
                        </motion.button>
                        
                        <motion.button
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="glass-button w-12 h-12 flex items-center justify-center"
                            onClick={toggleTheme}
                        >
                            {isDark ? (
                                <FiSun className="w-5 h-5" />
                            ) : (
                                <FiMoon className="w-5 h-5" />
                            )}
                        </motion.button>

                        {onExport && (
                            <motion.button
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: 20 }}
                                className="glass-button w-12 h-12 flex items-center justify-center"
                                onClick={onExport}
                            >
                                <FiDownload className="w-5 h-5" />
                            </motion.button>
                        )}
                    </div>
                )}
            </AnimatePresence>

            <button
                className="glass-button w-14 h-14 rounded-full flex items-center justify-center"
                onClick={() => setIsOpen(!isOpen)}
            >
                <motion.div
                    animate={{ rotate: isOpen ? 45 : 0 }}
                    transition={{ duration: 0.2 }}
                >
                    <FiPlus className="w-6 h-6" />
                </motion.div>
            </button>
        </div>
    );
}; 