import React, { useState } from 'react';
import { Question, StudyModeType } from '../types';
import { QuestionCard } from './QuestionCard';
import { QuestionProgress } from './QuestionProgress';
import { StudyTimer } from './StudyTimer';
import { FocusMode } from './FocusMode';
import { useSession } from '@context/SessionContext';

interface Props {
    mode: StudyModeType;
    questions: Question[];
}

export const StudyMode: React.FC<Props> = ({ mode, questions }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isFocusMode, setIsFocusMode] = useState(false);
    const { progressByMode } = useSession();

    const getModeTitle = () => {
        switch (mode) {
            case StudyModeType.QUICK_REVIEW:
                return '🎯 Quick Review';
            case StudyModeType.DEEP_STUDY:
                return '📚 Deep Study';
            case StudyModeType.REVISION:
                return '🔄 Revision';
            case StudyModeType.TEST_PREP:
                return '📝 Test Prep';
            default:
                return '';
        }
    };

    const getModeDescription = () => {
        switch (mode) {
            case StudyModeType.QUICK_REVIEW:
                return "Quick hits to test your knowledge. Perfect for a confidence boost! ⚡";
            case StudyModeType.DEEP_STUDY:
                return "Time to dig deep and really master this stuff. You've got this! 💪";
            case StudyModeType.REVISION:
                return "Let's make sure everything's sticking. Think of it as a knowledge check-up! 🔄";
            case StudyModeType.TEST_PREP:
                return "Game time! Get ready to ace that exam with real test conditions. 🎯";
            default:
                return '';
        }
    };

    return (
        <div className="max-w-4xl mx-auto py-8">
            <div className={`transition-all duration-300 ${
                isFocusMode ? 'opacity-0 pointer-events-none' : 'opacity-100'
            }`}>
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h2 className="text-2xl font-bold text-gradient mb-2">
                            {getModeTitle()}
                        </h2>
                        <p className="text-gray-400">
                            {getModeDescription()}
                        </p>
                    </div>
                    <StudyTimer mode={mode} />
                </div>
            </div>

            <QuestionProgress
                currentIndex={currentIndex}
                totalQuestions={questions.length}
                mode={mode}
            />

            <div className="space-y-6">
                {questions.map((question, index) => (
                    <QuestionCard
                        key={index}
                        question={{ ...question, mode }}
                        index={index}
                    />
                ))}
            </div>

            <FocusMode
                isActive={isFocusMode}
                onToggle={() => setIsFocusMode(!isFocusMode)}
            />
        </div>
    );
}; 