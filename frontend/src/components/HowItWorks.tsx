import React from 'react';
import { motion } from 'framer-motion';
import { FiUpload, FiCpu, FiAward } from 'react-icons/fi';

export const HowItWorks: React.FC = () => {
    const steps = [
        {
            icon: <FiUpload className="w-8 h-8" />,
            title: "Drop Your Notes",
            description: "Just upload your PDF and watch the magic unfold ✨",
            animation: {
                y: [0, -10, 0],
                transition: { repeat: Infinity, duration: 2 }
            }
        },
        {
            icon: <FiCpu className="w-8 h-8" />,
            title: "AI Does Its Thing",
            description: "Our smart AI breaks it down into bite-sized questions 🤖",
            animation: {
                scale: [1, 1.1, 1],
                transition: { repeat: Infinity, duration: 1.5 }
            }
        },
        {
            icon: <FiAward className="w-8 h-8" />,
            title: "Level Up",
            description: "Learn faster with personalized feedback 🚀",
            animation: {
                rotate: [0, 10, -10, 0],
                transition: { repeat: Infinity, duration: 2 }
            }
        }
    ];

    return (
        <motion.section
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="py-20"
        >
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gradient mb-4">
                    How It Works
                </h2>
                <p className="text-gray-400">
                    Three simple steps to transform your study material
                </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                {steps.map((step, index) => (
                    <motion.div
                        key={index}
                        className="glass-card p-6 text-center"
                        whileHover={{ scale: 1.05 }}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.2 }}
                    >
                        <motion.div 
                            className="text-violet-400 mb-4 flex justify-center"
                            animate={step.animation}
                        >
                            {step.icon}
                        </motion.div>
                        <h3 className="text-xl font-semibold mb-2">
                            {step.title}
                        </h3>
                        <p className="text-gray-400">
                            {step.description}
                        </p>
                    </motion.div>
                ))}
            </div>
        </motion.section>
    );
}; 