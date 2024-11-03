import React, { useEffect, useRef } from 'react';
import { motion, useAnimation, useInView } from 'framer-motion';
import { FiArrowRight, FiZap, FiClock, FiBookOpen } from 'react-icons/fi';
import { AnimatedBackground } from './AnimatedBackground';
import { HowItWorks } from './HowItWorks';
import { PowerFeatures } from './PowerFeatures';
import { StudentSuccess } from './StudentSuccess';

interface Props {
    onGetStarted: () => void;
}

export const HeroSection: React.FC<Props> = ({ onGetStarted }) => {
    const controls = useAnimation();
    const ref = useRef(null);
    const isInView = useInView(ref);

    useEffect(() => {
        if (isInView) {
            controls.start('visible');
        }
    }, [controls, isInView]);

    const benefits = [
        {
            icon: <FiZap className="w-6 h-6" />,
            title: "Smart Analysis",
            description: "AI-powered question generation that adapts to your content"
        },
        {
            icon: <FiClock className="w-6 h-6" />,
            title: "Time Saver",
            description: "Transform documents into study materials in seconds"
        },
        {
            icon: <FiBookOpen className="w-6 h-6" />,
            title: "Deep Learning",
            description: "Multiple study modes for better understanding"
        }
    ];

    return (
        <div className="relative">
            <AnimatedBackground />
            
            <motion.div 
                ref={ref}
                initial="hidden"
                animate="visible"
                className="min-h-screen flex flex-col items-center justify-center px-4"
            >
                {/* Main Content */}
                <motion.div
                    variants={{
                        hidden: { opacity: 0, y: 20 },
                        visible: { 
                            opacity: 1, 
                            y: 0,
                            transition: { 
                                duration: 0.8,
                                staggerChildren: 0.2 
                            }
                        }
                    }}
                    className="max-w-4xl mx-auto text-center"
                >
                    <motion.h1 
                        className="text-5xl md:text-7xl font-bold mb-6"
                        variants={{
                            hidden: { opacity: 0, y: 20 },
                            visible: { opacity: 1, y: 0 }
                        }}
                    >
                        <span className="text-gradient">Transform</span> Your Study Experience
                    </motion.h1>

                    <motion.p 
                        className="text-xl md:text-2xl text-gray-400 mb-12"
                        variants={{
                            hidden: { opacity: 0, y: 20 },
                            visible: { opacity: 1, y: 0 }
                        }}
                    >
                        Turn any document into an interactive learning experience
                    </motion.p>

                    {/* Benefits */}
                    <motion.div 
                        className="grid md:grid-cols-3 gap-8 mb-12"
                        variants={{
                            hidden: { opacity: 0 },
                            visible: { opacity: 1 }
                        }}
                    >
                        {benefits.map((benefit, index) => (
                            <motion.div
                                key={index}
                                className="glass-card p-6 hover:scale-105 transition-transform"
                                variants={{
                                    hidden: { opacity: 0, y: 20 },
                                    visible: { opacity: 1, y: 0 }
                                }}
                            >
                                <div className="text-violet-400 mb-4">{benefit.icon}</div>
                                <h3 className="text-lg font-semibold mb-2">{benefit.title}</h3>
                                <p className="text-gray-400">{benefit.description}</p>
                            </motion.div>
                        ))}
                    </motion.div>

                    {/* CTA Button */}
                    <motion.button
                        onClick={onGetStarted}
                        className="glass-button group text-lg px-8 py-4"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <span className="flex items-center">
                            Get Started
                            <motion.div
                                className="ml-2"
                                animate={{ x: [0, 5, 0] }}
                                transition={{ repeat: Infinity, duration: 1.5 }}
                            >
                                <FiArrowRight />
                            </motion.div>
                        </span>
                    </motion.button>
                </motion.div>

                {/* Scroll Indicator */}
                <motion.div
                    className="absolute bottom-8"
                    animate={{ y: [0, 10, 0] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                >
                    <div className="text-gray-400 text-sm">Scroll to explore</div>
                    <div className="w-0.5 h-8 bg-gradient-to-b from-violet-500 to-transparent mx-auto mt-2" />
                </motion.div>
            </motion.div>

            {/* Feature Sections */}
            <div className="space-y-20">
                {/* How It Works Section */}
                <HowItWorks />

                {/* Power Features Section */}
                <PowerFeatures />

                {/* Student Success Section */}
                <StudentSuccess />

                {/* Final CTA Section */}
                <motion.div
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                    className="py-20 text-center"
                >
                    <h2 className="text-4xl font-bold text-gradient mb-6">
                        Ready to Transform Your Learning?
                    </h2>
                    <p className="text-gray-400 text-xl mb-8 max-w-2xl mx-auto">
                        Join thousands of students who are already learning smarter with BrainiFi
                    </p>
                    <motion.button
                        onClick={onGetStarted}
                        className="glass-button group text-lg px-8 py-4"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <span className="flex items-center">
                            Get Started Now
                            <motion.div
                                className="ml-2"
                                animate={{ x: [0, 5, 0] }}
                                transition={{ repeat: Infinity, duration: 1.5 }}
                            >
                                <FiArrowRight />
                            </motion.div>
                        </span>
                    </motion.button>
                </motion.div>
            </div>
        </div>
    );
}; 