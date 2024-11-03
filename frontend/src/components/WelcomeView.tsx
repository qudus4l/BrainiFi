import React, { useState } from 'react';
import { FileUpload } from './FileUpload';
import { HeroSection } from './HeroSection';
import { motion, AnimatePresence } from 'framer-motion';
import { TransitionManager } from './TransitionManager';

interface Props {
    onUpload: (file: File) => void;
    isLoading?: boolean;
}

export const WelcomeView: React.FC<Props> = ({ onUpload, isLoading = false }) => {
    const [showUpload, setShowUpload] = useState(false);
    const [isTransitioning, setIsTransitioning] = useState(false);

    const handleGetStarted = () => {
        setIsTransitioning(true);
    };

    const handleTransitionComplete = () => {
        setIsTransitioning(false);
        setShowUpload(true);
    };

    return (
        <TransitionManager 
            isTransitioning={isTransitioning}
            onTransitionComplete={handleTransitionComplete}
        >
            {!showUpload ? (
                <HeroSection onGetStarted={handleGetStarted} />
            ) : (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="max-w-3xl mx-auto"
                >
                    <div className="text-center mb-12">
                        <h1 className="text-4xl font-bold text-gradient mb-4">
                            Ready to Level Up Your Study Game? 🚀
                        </h1>
                        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                            Are those your study materials?
                            Bring am, drop am!
                        </p>
                    </div>
                    <div className="glass-card p-8">
                        <FileUpload onUpload={onUpload} isLoading={isLoading} />
                    </div>
                </motion.div>
            )}
        </TransitionManager>
    );
}; 