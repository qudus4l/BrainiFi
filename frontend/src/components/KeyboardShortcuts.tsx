import React, { useEffect } from 'react';
import { useSession } from '@context/SessionContext';
import { StudyModeType } from '@/types';

export const useKeyboardShortcuts = () => {
    const { currentMode, setCurrentMode } = useSession();

    useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            // Only if not in an input/textarea
            if (e.target instanceof HTMLElement && 
                (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
                return;
            }

            switch (e.key.toLowerCase()) {
                case 'q':
                    if (e.ctrlKey || e.metaKey) {
                        setCurrentMode(StudyModeType.QUICK_REVIEW);
                    }
                    break;
                case 'd':
                    if (e.ctrlKey || e.metaKey) {
                        setCurrentMode(StudyModeType.DEEP_STUDY);
                    }
                    break;
                case 'r':
                    if (e.ctrlKey || e.metaKey) {
                        setCurrentMode(StudyModeType.REVISION);
                    }
                    break;
                case 't':
                    if (e.ctrlKey || e.metaKey) {
                        setCurrentMode(StudyModeType.TEST_PREP);
                    }
                    break;
                case 'escape':
                    setCurrentMode(null);
                    break;
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [setCurrentMode]);
}; 