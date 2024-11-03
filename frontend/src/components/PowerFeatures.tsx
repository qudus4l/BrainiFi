import React from 'react';
import { motion } from 'framer-motion';
import { FiLayers, FiActivity, FiTarget } from 'react-icons/fi';

export const PowerFeatures: React.FC = () => {
    const features = [
        {
            icon: <FiLayers />,
            title: "Smart Flashcards",
            description: "AI-generated cards that adapt to your learning style",
            preview: (
                <motion.div 
                    className="glass-card p-4 aspect-video"
                    whileHover={{ rotateY: 180 }}
                    transition={{ duration: 0.8 }}
                >
                    <div className="text-center">
                        <span className="text-gradient">Interactive Preview</span>
                    </div>
                </motion.div>
            )
        },
        {
            icon: <FiActivity />,
            title: "Dynamic Quizzes",
            description: "Questions that evolve with your understanding",
            preview: (
                <div className="relative h-40">
                    {[1, 2, 3].map((i) => (
                        <motion.div
                            key={i}
                            className="absolute inset-0 glass-card p-4"
                            initial={{ rotate: (i-2) * 5, y: (i-2) * 10 }}
                            whileHover={{ y: -5 }}
                            transition={{ duration: 0.2 }}
                        >
                            Question {i}
                        </motion.div>
                    ))}
                </div>
            )
        },
        {
            icon: <FiTarget />,
            title: "Progress Tracking",
            description: "Visual insights into your learning journey",
            preview: (
                <div className="h-40 flex items-end justify-around p-4 glass-card">
                    {[40, 65, 85, 95].map((height, i) => (
                        <motion.div
                            key={i}
                            className="w-4 bg-violet-500/50 rounded-t"
                            initial={{ height: 0 }}
                            whileInView={{ height: `${height}%` }}
                            transition={{ delay: i * 0.1, duration: 0.5 }}
                        />
                    ))}
                </div>
            )
        }
    ];

    return (
        <motion.section
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="py-20"
        >
            <div className="text-center mb-16">
                <motion.h2 
                    className="text-4xl font-bold text-gradient mb-4"
                    initial={{ y: 20, opacity: 0 }}
                    whileInView={{ y: 0, opacity: 1 }}
                    viewport={{ once: true }}
                >
                    Power Features
                </motion.h2>
                <motion.p 
                    className="text-gray-400 text-xl"
                    initial={{ y: 20, opacity: 0 }}
                    whileInView={{ y: 0, opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 }}
                >
                    Tools that transform how you learn
                </motion.p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto px-4">
                {features.map((feature, index) => (
                    <motion.div
                        key={index}
                        className="glass-card p-6"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.2 }}
                        whileHover={{ y: -5 }}
                    >
                        <div className="text-violet-400 text-3xl mb-4">
                            {feature.icon}
                        </div>
                        <h3 className="text-xl font-semibold mb-2">
                            {feature.title}
                        </h3>
                        <p className="text-gray-400 mb-6">
                            {feature.description}
                        </p>
                        {feature.preview}
                    </motion.div>
                ))}
            </div>
        </motion.section>
    );
}; 