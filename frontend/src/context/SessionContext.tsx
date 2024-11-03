import React, { createContext, useContext, useState, useEffect } from 'react';
import { StudyModeType, ModuleProgress } from '@/types';

interface ProgressState {
    [StudyModeType.QUICK_REVIEW]: ModuleProgress;
    [StudyModeType.DEEP_STUDY]: ModuleProgress;
    [StudyModeType.REVISION]: ModuleProgress;
    [StudyModeType.TEST_PREP]: ModuleProgress;
}

interface SessionContextType {
    questionsAnswered: number;
    incrementQuestionsAnswered: () => void;
    sessionId: string;
    answers: Record<string, string>;
    setAnswer: (questionId: string, answer: string) => void;
    feedback: Record<string, any>;
    setFeedback: (questionId: string, feedback: any) => void;
    hintsShown: Set<string>;
    toggleHint: (questionId: string) => void;
    currentMode: StudyModeType | null;
    setCurrentMode: (mode: StudyModeType | null) => void;
    progressByMode: ProgressState;
    incrementProgress: (mode: StudyModeType) => void;
    resetProgress: (mode: StudyModeType) => void;
    updateProgress: (mode: StudyModeType, score: number) => void;
    resetAllProgress: () => void;
    resetModeProgress: (mode: StudyModeType) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

const PASSING_SCORE = 80; // Define completion threshold

export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [questionsAnswered, setQuestionsAnswered] = useState(0);
    const [sessionId] = useState(() => String(Date.now()));
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [feedback, setFeedbackState] = useState<Record<string, any>>({});
    const [hintsShown, setHintsShown] = useState<Set<string>>(new Set());
    const [currentMode, setCurrentMode] = useState<StudyModeType | null>(null);
    const [progressByMode, setProgressByMode] = useState<ProgressState>({
        [StudyModeType.QUICK_REVIEW]: { attempted: 0, completed: 0, totalScore: 0 },
        [StudyModeType.DEEP_STUDY]: { attempted: 0, completed: 0, totalScore: 0 },
        [StudyModeType.REVISION]: { attempted: 0, completed: 0, totalScore: 0 },
        [StudyModeType.TEST_PREP]: { attempted: 0, completed: 0, totalScore: 0 }
    });

    // Load state from localStorage on mount
    useEffect(() => {
        const savedState = localStorage.getItem(`brainifi_session_${sessionId}`);
        if (savedState) {
            const { 
                questionsAnswered, 
                answers, 
                feedback, 
                hintsShown,
                currentMode,
                progressByMode
            } = JSON.parse(savedState);
            setQuestionsAnswered(questionsAnswered);
            setAnswers(answers);
            setFeedbackState(feedback);
            setHintsShown(new Set(hintsShown));
            setCurrentMode(currentMode);
            setProgressByMode(progressByMode);
        }
    }, [sessionId]);

    // Save state to localStorage on changes
    useEffect(() => {
        localStorage.setItem(`brainifi_session_${sessionId}`, JSON.stringify({
            questionsAnswered,
            answers,
            feedback,
            hintsShown: Array.from(hintsShown),
            currentMode,
            progressByMode
        }));
    }, [sessionId, questionsAnswered, answers, feedback, hintsShown, currentMode, progressByMode]);

    const incrementQuestionsAnswered = () => setQuestionsAnswered(prev => prev + 1);
    
    const setAnswer = (questionId: string, answer: string) => {
        setAnswers(prev => ({ ...prev, [questionId]: answer }));
    };

    const setFeedback = (questionId: string, newFeedback: any) => {
        setFeedbackState(prev => ({ ...prev, [questionId]: newFeedback }));
    };

    const toggleHint = (questionId: string) => {
        setHintsShown(prev => {
            const next = new Set(prev);
            if (next.has(questionId)) {
                next.delete(questionId);
            } else {
                next.add(questionId);
            }
            return next;
        });
    };

    const updateProgress = (mode: StudyModeType, score: number) => {
        console.log(`Updating progress for ${mode} with score ${score}`);
        
        setProgressByMode(prev => ({
            ...prev,
            [mode]: {
                attempted: prev[mode].attempted + 1,
                completed: prev[mode].completed + (score >= PASSING_SCORE ? 1 : 0),
                totalScore: prev[mode].totalScore + score
            }
        }));
    };

    const incrementProgress = (mode: StudyModeType) => {
        updateProgress(mode, 100); // Assuming 100 is the score for a completed question
    };

    const resetProgress = (mode: StudyModeType) => {
        setProgressByMode(prev => ({
            ...prev,
            [mode]: { attempted: 0, completed: 0, totalScore: 0 }
        }));
    };

    const resetModeProgress = (mode: StudyModeType) => {
        setProgressByMode(prev => ({
            ...prev,
            [mode]: { attempted: 0, completed: 0, totalScore: 0 }
        }));
        // Also clear related answers and feedback
        const newAnswers = { ...answers };
        const newFeedback = { ...feedback };
        Object.keys(newAnswers).forEach(key => {
            if (key.includes(mode)) {
                delete newAnswers[key];
                delete newFeedback[key];
            }
        });
        setAnswers(newAnswers);
        setFeedbackState(newFeedback);
    };

    const resetAllProgress = () => {
        setProgressByMode({
            [StudyModeType.QUICK_REVIEW]: { attempted: 0, completed: 0, totalScore: 0 },
            [StudyModeType.DEEP_STUDY]: { attempted: 0, completed: 0, totalScore: 0 },
            [StudyModeType.REVISION]: { attempted: 0, completed: 0, totalScore: 0 },
            [StudyModeType.TEST_PREP]: { attempted: 0, completed: 0, totalScore: 0 }
        });
        setAnswers({});
        setFeedbackState({});
        setHintsShown(new Set());
    };

    return (
        <SessionContext.Provider value={{
            questionsAnswered,
            incrementQuestionsAnswered,
            sessionId,
            answers,
            setAnswer,
            feedback,
            setFeedback,
            hintsShown,
            toggleHint,
            currentMode,
            setCurrentMode,
            progressByMode,
            incrementProgress,
            resetProgress,
            updateProgress,
            resetAllProgress,
            resetModeProgress,
        }}>
            {children}
        </SessionContext.Provider>
    );
};

export const useSession = () => {
    const context = useContext(SessionContext);
    if (context === undefined) {
        throw new Error('useSession must be used within a SessionProvider');
    }
    return context;
}; 