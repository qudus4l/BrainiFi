import React, { useState, useEffect } from 'react';
import { FileUpload } from '@components/FileUpload';
import { StudyMode } from '@components/StudyMode';
import { ProgressTracker } from '@components/ProgressTracker';
import { Questions, StudyModeType, Question } from '@/types';
import { uploadPDF } from '@services/api';
import { FiBook, FiClock, FiEdit3, FiClipboard } from 'react-icons/fi';
import { SessionProvider } from '@context/SessionContext';
import { ErrorBoundary } from '@components/ErrorBoundary';
import { WelcomeView } from '@components/WelcomeView';
import { StudyView } from '@components/StudyView';
import { FloatingActions } from '@components/FloatingActions';
import { HelpOverlay } from '@components/HelpOverlay';
import { Toast, ToastType } from '@components/Toast';
import { AnimatePresence } from 'framer-motion';
import { ThemeProvider } from '@context/ThemeContext';
import { CustomCursor } from '@components/CustomCursor';
import { AchievementPopup } from '@components/AchievementPopup';
import { Footer } from '@components/Footer';

const App: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [questions, setQuestions] = useState<Questions | null>(null);
    const [currentMode, setCurrentMode] = useState<StudyModeType | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isHelpOpen, setIsHelpOpen] = useState(false);
    const [toast, setToast] = useState<{ message: string; type: ToastType } | null>(null);
    const [achievement, setAchievement] = useState<{ title: string; description: string; type: 'milestone' | 'streak' | 'mastery' } | null>(null);

    useEffect(() => {
        if (questions) {
            console.log("Rendering questions:", questions);
        }
    }, [questions]);

    const handleFileUpload = async (file: File) => {
        setIsLoading(true);
        setError(null);
        try {
            console.log("Uploading file...");
            const response = await uploadPDF(file);
            console.log("Response received:", response);
            
            if (response.questions) {
                console.log("Questions structure:", JSON.stringify(response.questions, null, 2));
                // Verify the structure matches our types
                if (
                    Array.isArray(response.questions.QUICK_REVIEW) &&
                    Array.isArray(response.questions.DEEP_STUDY) &&
                    Array.isArray(response.questions.REVISION) &&
                    Array.isArray(response.questions.TEST_PREP)
                ) {
                    setQuestions(response.questions);
                    console.log("Questions set successfully");
                } else {
                    throw new Error("Invalid questions structure received from server");
                }
            } else {
                throw new Error("No questions received from server");
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setError(error instanceof Error ? error.message : 'Failed to process PDF');
        } finally {
            setIsLoading(false);
        }
    };

    const getModeIcon = (mode: StudyModeType) => {
        switch (mode) {
            case StudyModeType.QUICK_REVIEW:
                return <FiClock className="w-6 h-6" />;
            case StudyModeType.DEEP_STUDY:
                return <FiBook className="w-6 h-6" />;
            case StudyModeType.REVISION:
                return <FiEdit3 className="w-6 h-6" />;
            case StudyModeType.TEST_PREP:
                return <FiClipboard className="w-6 h-6" />;
        }
    };

    const handleModeChange = (mode: StudyModeType) => {
        setCurrentMode(mode);
        // Reset answers and feedback for clean state
        localStorage.removeItem(`brainifi_answers_${mode}`);
        localStorage.removeItem(`brainifi_feedback_${mode}`);
    };

    // Move keyboard shortcuts directly into App
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

    const showToast = (message: string, type: ToastType = 'info') => {
        setToast({ message, type });
    };

    const handleExport = () => {
        // TODO: Implement export functionality
        showToast('Export feature coming soon!', 'info');
    };

    return (
        <ErrorBoundary>
            <ThemeProvider>
                <SessionProvider>
                    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100 flex flex-col">
                        <CustomCursor />
                        {/* Animated background elements */}
                        <div className="fixed inset-0 -z-10">
                            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(139,92,246,0.1),transparent_50%)]" />
                            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-violet-500/10 rounded-full blur-3xl" />
                            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-sky-500/10 rounded-full blur-3xl" />
                        </div>

                        {/* Header */}
                        <nav className="glass-card sticky top-0 z-50 mb-8">
                            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                                <div className="flex items-center space-x-4">
                                    <div className="text-2xl font-bold text-gradient">
                                        BrainiFi
                                    </div>
                                    <div className="text-sm text-gray-400">
                                        Smart Learning Assistant
                                    </div>
                                </div>
                            </div>
                        </nav>

                        {/* Main content */}
                        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-grow">
                            {error && (
                                <div className="mb-6 p-4 glass-card text-red-400 rounded-lg">
                                    {error}
                                </div>
                            )}
                            
                            {isLoading ? (
                                <LoadingState />
                            ) : !questions ? (
                                <WelcomeView onUpload={handleFileUpload} isLoading={isLoading} />
                            ) : (
                                <StudyView 
                                    questions={questions}
                                    currentMode={currentMode}
                                    onModeChange={setCurrentMode}
                                />
                            )}
                        </main>

                        <Footer />

                        {/* Floating Actions */}
                        <FloatingActions 
                            onHelp={() => setIsHelpOpen(true)}
                            onExport={handleExport}
                        />

                        {/* Help Overlay */}
                        <HelpOverlay 
                            isOpen={isHelpOpen}
                            onClose={() => setIsHelpOpen(false)}
                        />

                        {/* Toast Notifications */}
                        <AnimatePresence>
                            {toast && (
                                <Toast
                                    message={toast.message}
                                    type={toast.type}
                                    onClose={() => setToast(null)}
                                />
                            )}
                        </AnimatePresence>

                        {/* Achievement Popup */}
                        {achievement && (
                            <AchievementPopup 
                                achievement={achievement}
                                onClose={() => setAchievement(null)}
                            />
                        )}
                    </div>
                </SessionProvider>
            </ThemeProvider>
        </ErrorBoundary>
    );
};

// New component for loading state
const LoadingState: React.FC = () => (
    <div className="glass-card p-8 max-w-3xl mx-auto text-center">
        <div className="relative w-20 h-20 mx-auto mb-6">
            <div className="absolute inset-0 rounded-full border-t-2 border-violet-500 animate-spin" />
            <div className="absolute inset-2 rounded-full border-t-2 border-sky-500 animate-spin-slow" />
            <div className="absolute inset-4 rounded-full border-t-2 border-violet-400 animate-spin-slower" />
        </div>
        <p className="text-lg text-gray-300">
            Brewing up some smart questions for you... ✨
        </p>
        <p className="text-sm text-gray-400 mt-2">
            (This usually takes about 30 seconds)
        </p>
    </div>
);

export default App;
