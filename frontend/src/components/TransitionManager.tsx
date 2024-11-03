import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
    children: React.ReactNode;
    isTransitioning: boolean;
    onTransitionComplete: () => void;
}

export const TransitionManager: React.FC<Props> = ({ 
    children, 
    isTransitioning, 
    onTransitionComplete 
}) => {
    return (
        <AnimatePresence mode="wait">
            {isTransitioning ? (
                <div className="fixed inset-0 z-50">
                    {/* Current page lifting up */}
                    <motion.div
                        initial={{ y: 0 }}
                        animate={{ y: '-100vh' }}
                        transition={{ 
                            duration: 1,
                            ease: [0.43, 0.13, 0.23, 0.96]
                        }}
                        className="fixed inset-0 bg-gray-900"
                    >
                        {/* Rocket */}
                        <motion.div
                            initial={{ y: '50vh', x: '-50%' }}
                            animate={{ y: '-100vh' }}
                            transition={{ 
                                duration: 1,
                                ease: [0.43, 0.13, 0.23, 0.96]
                            }}
                            className="fixed left-1/2 z-50"
                        >
                            <div className="relative">
                                {/* Rocket body */}
                                <motion.div
                                    animate={{ rotate: [0, -5, 5, 0] }}
                                    transition={{ repeat: Infinity, duration: 2 }}
                                    className="w-12 h-24 bg-violet-500 rounded-full relative"
                                >
                                    {/* Rocket tip */}
                                    <div className="absolute -top-6 left-1/2 -translate-x-1/2 
                                                  border-l-[24px] border-l-transparent
                                                  border-r-[24px] border-r-transparent
                                                  border-b-[24px] border-b-violet-500" />
                                    {/* Rocket windows */}
                                    <div className="absolute top-4 left-1/2 -translate-x-1/2 
                                                  w-4 h-4 bg-white rounded-full" />
                                    <div className="absolute top-12 left-1/2 -translate-x-1/2 
                                                  w-4 h-4 bg-white rounded-full" />
                                </motion.div>
                                {/* Rocket flames */}
                                <motion.div
                                    animate={{ 
                                        scaleY: [1, 1.5, 1],
                                        opacity: [0.5, 1, 0.5]
                                    }}
                                    transition={{ 
                                        repeat: Infinity, 
                                        duration: 0.3 
                                    }}
                                    className="absolute -bottom-12 left-1/2 -translate-x-1/2 
                                             w-8 h-16 bg-gradient-to-t from-orange-500 via-yellow-500 to-transparent
                                             rounded-full blur-sm"
                                />
                            </div>
                        </motion.div>
                    </motion.div>

                    {/* New page sliding up */}
                    <motion.div
                        initial={{ y: '100vh' }}
                        animate={{ y: 0 }}
                        transition={{ 
                            duration: 0.8,
                            delay: 0.5,
                            ease: [0.43, 0.13, 0.23, 0.96]
                        }}
                        onAnimationComplete={onTransitionComplete}
                        className="fixed inset-0 bg-gray-900"
                    />

                    {/* Particle effects */}
                    <div className="fixed inset-0 pointer-events-none">
                        {Array.from({ length: 20 }).map((_, i) => (
                            <motion.div
                                key={i}
                                initial={{ 
                                    y: Math.random() * window.innerHeight,
                                    x: Math.random() * window.innerWidth,
                                    scale: 0
                                }}
                                animate={{ 
                                    y: -100,
                                    scale: Math.random() * 2,
                                    opacity: [0, 1, 0]
                                }}
                                transition={{ 
                                    duration: Math.random() * 1 + 0.5,
                                    delay: Math.random() * 0.5,
                                    repeat: Infinity
                                }}
                                className="absolute w-2 h-2 bg-violet-500 rounded-full"
                            />
                        ))}
                    </div>
                </div>
            ) : (
                children
            )}
        </AnimatePresence>
    );
}; 