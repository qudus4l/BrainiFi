import React from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

export const StudentSuccess: React.FC = () => {
    const stats = [
        { value: '80%', label: 'Faster Study Prep' },
        { value: '65%', label: 'Better Retention' },
        { value: '10k+', label: 'Active Students' }
    ];

    const testimonials = [
        {
            quote: "BrainiFi changed how I study completely!",
            author: "CS Student, Unilag",
            course: "Computer Science"
        },
        {
            quote: "The AI-generated questions are spot on!",
            author: "Med Student, LUTH",
            course: "Medicine"
        },
        {
            quote: "My grades improved significantly!",
            author: "Engineering Student, OAU",
            course: "Mechanical Engineering"
        }
    ];

    return (
        <motion.section
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="py-20 relative overflow-hidden"
        >
            {/* Background Effect */}
            <div className="absolute inset-0 bg-gradient-to-b from-violet-500/5 to-transparent" />

            <div className="max-w-6xl mx-auto px-4">
                {/* Stats */}
                <div className="grid md:grid-cols-3 gap-8 mb-20">
                    {stats.map((stat, index) => (
                        <motion.div
                            key={index}
                            className="text-center"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.2 }}
                        >
                            <motion.div 
                                className="text-5xl font-bold text-gradient mb-2"
                                initial={{ scale: 0.5 }}
                                whileInView={{ scale: 1 }}
                                viewport={{ once: true }}
                            >
                                {stat.value}
                            </motion.div>
                            <div className="text-gray-400">{stat.label}</div>
                        </motion.div>
                    ))}
                </div>

                {/* Testimonials */}
                <div className="grid md:grid-cols-3 gap-6">
                    {testimonials.map((testimonial, index) => (
                        <motion.div
                            key={index}
                            className="glass-card p-6"
                            initial={{ opacity: 0, x: 20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.2 }}
                            whileHover={{ y: -5 }}
                        >
                            <div className="text-2xl text-violet-400 mb-4">"</div>
                            <p className="text-gray-300 mb-4">{testimonial.quote}</p>
                            <div className="text-sm text-gray-400">{testimonial.author}</div>
                            <div className="text-xs text-gray-500">{testimonial.course}</div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </motion.section>
    );
}; 