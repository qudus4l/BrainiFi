import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useThrottledValue } from '@/hooks/useThrottledValue';

interface Particle {
    x: number;
    y: number;
    size: number;
    color: string;
    velocity: { x: number; y: number };
}

export const AnimatedBackground: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const mouseRef = useRef({ x: 0, y: 0 });
    const particlesRef = useRef<Particle[]>([]);

    const throttledMousePos = useThrottledValue(mouseRef.current, 16); // ~60fps

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Set canvas size
        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight * 2; // Make it taller to cover scroll
        };
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Create particles with higher opacity
        const colors = ['rgba(139, 92, 246, 0.3)', 'rgba(14, 165, 233, 0.3)']; // Increased opacity
        const createParticles = () => {
            particlesRef.current = Array.from({ length: 100 }, () => ({ // More particles
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 6 + 3, // Larger particles
                color: colors[Math.floor(Math.random() * colors.length)],
                velocity: {
                    x: (Math.random() - 0.5) * 0.3, // Slightly faster
                    y: (Math.random() - 0.5) * 0.3
                }
            }));
        };
        createParticles();

        // Animation loop
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particlesRef.current.forEach(particle => {
                // Update position
                particle.x += particle.velocity.x;
                particle.y += particle.velocity.y;

                // Use throttled mouse position for smoother interaction
                const dx = throttledMousePos.x - particle.x;
                const dy = throttledMousePos.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 150) { // Increased interaction radius
                    particle.x -= dx * 0.02; // Stronger repulsion
                    particle.y -= dy * 0.02;
                }

                // Wrap around screen
                if (particle.x < 0) particle.x = canvas.width;
                if (particle.x > canvas.width) particle.x = 0;
                if (particle.y < 0) particle.y = canvas.height;
                if (particle.y > canvas.height) particle.y = 0;

                // Draw particle with glow effect
                ctx.save();
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fillStyle = particle.color;
                ctx.shadowColor = particle.color;
                ctx.shadowBlur = 15;
                ctx.fill();
                ctx.restore();
            });

            requestAnimationFrame(animate);
        };
        animate();

        // Mouse move handler
        const handleMouseMove = (e: MouseEvent) => {
            mouseRef.current = {
                x: e.clientX,
                y: e.clientY + window.scrollY // Account for scroll
            };
        };
        window.addEventListener('mousemove', handleMouseMove);

        return () => {
            window.removeEventListener('resize', resizeCanvas);
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, [throttledMousePos]);

    return (
        <canvas
            ref={canvasRef}
            className="fixed inset-0 pointer-events-none"
            style={{ 
                zIndex: 0,
                opacity: 1,
                mixBlendMode: 'screen'
            }}
        />
    );
}; 