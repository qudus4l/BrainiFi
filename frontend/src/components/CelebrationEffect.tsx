import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';

interface Props {
    onComplete: () => void;
}

export const CelebrationEffect: React.FC<Props> = ({ onComplete }) => {
    useEffect(() => {
        const duration = 3000;
        const end = Date.now() + duration;

        const frame = () => {
            confetti({
                particleCount: 2,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: ['#8B5CF6', '#3B82F6']
            });
            
            confetti({
                particleCount: 2,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: ['#8B5CF6', '#3B82F6']
            });

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            } else {
                onComplete();
            }
        };

        frame();
    }, [onComplete]);

    return null;
}; 