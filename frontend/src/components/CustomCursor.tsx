import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const CustomCursor: React.FC = () => {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isPointer, setIsPointer] = useState(false);

    useEffect(() => {
        const updatePosition = (e: MouseEvent) => {
            setPosition({ x: e.clientX, y: e.clientY });
            
            // Check if hovering over clickable element
            const target = e.target as HTMLElement;
            setIsPointer(
                window.getComputedStyle(target).cursor === 'pointer' ||
                target.tagName === 'BUTTON' ||
                target.tagName === 'A'
            );
        };

        window.addEventListener('mousemove', updatePosition);
        return () => window.removeEventListener('mousemove', updatePosition);
    }, []);

    return (
        <>
            <motion.div
                className="custom-cursor"
                animate={{
                    x: position.x - 16,
                    y: position.y - 16,
                    scale: isPointer ? 1.5 : 1,
                }}
                transition={{
                    type: "spring",
                    damping: 30,
                    mass: 0.5,
                }}
            />
            <motion.div
                className="fixed w-2 h-2 bg-white rounded-full pointer-events-none z-50 mix-blend-difference"
                animate={{
                    x: position.x - 4,
                    y: position.y - 4,
                }}
                transition={{
                    type: "spring",
                    damping: 50,
                    mass: 0.2,
                }}
            />
        </>
    );
}; 