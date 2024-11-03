import { useState, useEffect, useRef } from 'react';

export function useThrottledValue<T>(value: T, delay: number): T {
    const [throttledValue, setThrottledValue] = useState(value);
    const lastRan = useRef(Date.now());

    useEffect(() => {
        const handler = window.setTimeout(() => {
            if (Date.now() - lastRan.current >= delay) {
                setThrottledValue(value);
                lastRan.current = Date.now();
            }
        }, delay - (Date.now() - lastRan.current));

        return () => window.clearTimeout(handler);
    }, [value, delay]);

    return throttledValue;
} 