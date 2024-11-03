import React from 'react';
import { Questions, StudyModeType } from '@/types';
import { StudyMode } from './StudyMode';
import { FiBook, FiClock, FiEdit3, FiClipboard } from 'react-icons/fi';

interface Props {
    questions: Questions;
    currentMode: StudyModeType | null;
    onModeChange: (mode: StudyModeType) => void;
}

export const StudyView: React.FC<Props> = ({ questions, currentMode, onModeChange }) => {
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

    return (
        <div>
            {!currentMode ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {(Object.values(StudyModeType) as StudyModeType[]).map((mode) => (
                        <button
                            key={mode}
                            onClick={() => onModeChange(mode)}
                            className="glass-card floating-card p-6 text-center"
                        >
                            <div className="flex flex-col items-center">
                                <div className="text-violet-400 mb-4">
                                    {getModeIcon(mode)}
                                </div>
                                <h3 className="text-lg font-semibold text-gray-100 mb-2">
                                    {mode.split('_').map(word => 
                                        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                                    ).join(' ')}
                                </h3>
                                <p className="text-sm text-gray-400">
                                    {questions[mode].length} questions available
                                </p>
                            </div>
                        </button>
                    ))}
                </div>
            ) : (
                <div>
                    <button
                        onClick={() => onModeChange(null)}
                        className="glass-button mb-6 flex items-center"
                    >
                        ← Back to Study Modes
                    </button>
                    <StudyMode
                        mode={currentMode}
                        questions={questions[currentMode]}
                    />
                </div>
            )}
        </div>
    );
}; 