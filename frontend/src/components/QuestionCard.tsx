import React, { useState } from 'react';
import { Question, Feedback } from '@/types';
import { validateAnswer } from '@services/api';
import { FiCheckCircle, FiHelpCircle, FiAlertCircle } from 'react-icons/fi';
import { useSession } from '@context/SessionContext';
import { motion } from 'framer-motion';

interface Props {
    question: Question;
    index: number;
    onAnswered?: () => void;
}

export const QuestionCard: React.FC<Props> = ({ question, index, onAnswered }) => {
    const {
        answers,
        setAnswer,
        feedback,
        setFeedback,
        hintsShown,
        toggleHint,
        currentMode,
        updateProgress
    } = useSession();

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isExpanded, setIsExpanded] = useState(false);

    const questionId = `${question.type}_${question.mode}_${index}`;
    const currentAnswer = answers[questionId] || '';
    const currentFeedback = feedback[questionId] as Feedback | undefined;
    const isHintShown = hintsShown.has(questionId);

    const isPassing = currentFeedback && currentFeedback.score >= 80;

    const handleSubmit = async () => {
        if (!currentAnswer.trim()) return;
        
        setIsSubmitting(true);
        setError(null);
        
        try {
            const result = await validateAnswer(
                question.question,
                question.context,
                currentAnswer
            );
            setFeedback(questionId, result);
            
            if (currentMode && result.score) {
                updateProgress(currentMode, result.score);
                onAnswered?.();
            }
        } catch (error) {
            setError('Failed to validate answer. Please try again.');
            console.error('Error validating answer:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <motion.div 
            className={`glass-card p-6 mb-4 cursor-pointer relative overflow-hidden
                       ${isPassing ? 'border-green-500/50' : ''}`}
            onClick={() => !isExpanded && setIsExpanded(true)}
            initial={false}
            animate={{ height: isExpanded ? 'auto' : '100px' }}
            transition={{ duration: 0.3 }}
        >
            <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-100">
                    Question {index + 1}
                    {isPassing && (
                        <span className="ml-2 text-green-400 text-sm">
                            (Completed)
                        </span>
                    )}
                </h3>
                <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded text-sm ${
                        question.difficulty === 'easy' ? 'bg-green-500/20 text-green-300' :
                        question.difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                        'bg-red-500/20 text-red-300'
                    }`}>
                        {question.difficulty}
                    </span>
                    <span className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-sm">
                        {question.type}
                    </span>
                </div>
            </div>

            <p className="text-gray-300 mb-4">{question.question}</p>

            <div className="mb-4">
                <textarea
                    value={currentAnswer}
                    onChange={(e) => setAnswer(questionId, e.target.value)}
                    className="w-full p-3 bg-gray-800/50 border border-gray-700 rounded-lg 
                             text-gray-100 placeholder-gray-500 focus:ring-2 
                             focus:ring-violet-500 focus:border-transparent"
                    rows={4}
                    placeholder="Write your answer here..."
                    disabled={isSubmitting}
                />
            </div>

            {error && (
                <div className="mb-4 p-3 bg-red-500/10 text-red-400 rounded-lg flex items-center">
                    <FiAlertCircle className="mr-2" />
                    {error}
                </div>
            )}

            <div className="flex space-x-4 mb-4">
                <button
                    onClick={handleSubmit}
                    disabled={isSubmitting || !currentAnswer.trim()}
                    className={`glass-button flex items-center ${
                        isSubmitting || !currentAnswer.trim() 
                            ? 'opacity-50 cursor-not-allowed'
                            : ''
                    }`}
                >
                    <FiCheckCircle className="mr-2" />
                    {isSubmitting ? 'Thinking... 🤔' : 'Check My Answer'}
                </button>

                <button
                    onClick={() => toggleHint(questionId)}
                    className="glass-button flex items-center"
                >
                    <FiHelpCircle className="mr-2" />
                    {isHintShown ? 'Hide the Hint' : 'Need a Hint?'}
                </button>
            </div>

            {isHintShown && (
                <div className="bg-violet-500/10 border border-violet-500/20 p-4 rounded-lg mb-4">
                    <p className="text-violet-300">💡 {question.hint}</p>
                </div>
            )}

            {currentFeedback && (
                <div className="mt-4 space-y-4">
                    <div className="flex items-center space-x-4">
                        <div className="bg-violet-500/10 text-violet-300 px-4 py-2 rounded-lg">
                            Score: {currentFeedback.score}%
                        </div>
                        <p className="text-gray-300">{currentFeedback.feedback}</p>
                    </div>

                    <div className="bg-green-500/10 border border-green-500/20 p-4 rounded-lg">
                        <h4 className="font-semibold text-green-300 mb-2">Strengths</h4>
                        <ul className="list-disc list-inside space-y-1">
                            {currentFeedback.strengths.map((strength: string, i: number) => (
                                <li key={i} className="text-green-200">{strength}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="bg-yellow-500/10 border border-yellow-500/20 p-4 rounded-lg">
                        <h4 className="font-semibold text-yellow-300 mb-2">Areas for Improvement</h4>
                        <ul className="list-disc list-inside space-y-1">
                            {currentFeedback.improvements.map((improvement: string, i: number) => (
                                <li key={i} className="text-yellow-200">{improvement}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}

            {!isExpanded && (
                <div className="absolute bottom-0 left-0 right-0 h-20 
                              bg-gradient-to-t from-gray-900 to-transparent
                              flex items-end justify-center pb-4">
                    <span className="text-sm text-gray-400">
                        Tap to see more ✨
                    </span>
                </div>
            )}

            {isPassing && (
                <span className="ml-2 text-green-400 text-sm flex items-center">
                    <FiCheckCircle className="mr-1" /> Nailed it! 🎯
                </span>
            )}
        </motion.div>
    );
}; 