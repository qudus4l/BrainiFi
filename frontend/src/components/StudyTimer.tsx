import React, { useState, useEffect } from 'react';
import { FiClock } from 'react-icons/fi';

interface Props {
    mode: string;
    onTimeUpdate?: (seconds: number) => void;
}

export const StudyTimer: React.FC<Props> = ({ mode, onTimeUpdate }) => {
    const [seconds, setSeconds] = useState(0);
    const [isPaused, setIsPaused] = useState(false);

    useEffect(() => {
        const timer = setInterval(() => {
            if (!isPaused) {
                setSeconds(prev => prev + 1);
                onTimeUpdate?.(seconds + 1);
            }
        }, 1000);

        return () => clearInterval(timer);
    }, [isPaused, seconds, onTimeUpdate]);

    const formatTime = (totalSeconds: number) => {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const secs = totalSeconds % 60;

        return `${hours > 0 ? `${hours}h ` : ''}${minutes}m ${secs}s`;
    };

    return (
        <div className="glass-card p-3 flex items-center space-x-3">
            <FiClock className="text-violet-400" />
            <span className="text-gray-300">{formatTime(seconds)}</span>
            <button
                onClick={() => setIsPaused(!isPaused)}
                className="text-sm text-gray-400 hover:text-gray-300"
            >
                {isPaused ? 'Resume' : 'Pause'}
            </button>
        </div>
    );
}; 