import React from 'react';
import { useSession } from '../context/SessionContext';
import { FiAward, FiTrendingUp, FiCheck } from 'react-icons/fi';
import { StudyModeType } from '@/types';

export const ProgressTracker: React.FC = () => {
    const { 
        progressByMode, 
        currentMode, 
        resetModeProgress, 
        resetAllProgress 
    } = useSession();
    
    const getTargetQuestions = (mode: StudyModeType) => {
        switch (mode) {
            case StudyModeType.QUICK_REVIEW:
                return 3;
            default:
                return 5;
        }
    };

    const isModuleComplete = (mode: StudyModeType) => {
        const progress = progressByMode[mode];
        const target = getTargetQuestions(mode);
        
        return progress && progress.completed >= target;
    };

    // Calculate overall progress correctly
    const totalCompleted = Object.values(progressByMode).reduce(
        (sum, curr) => sum + curr.completed, 
        0
    );
    
    const totalTargets = Object.values(StudyModeType).reduce(
        (sum, mode: StudyModeType) => sum + getTargetQuestions(mode), 
        0
    );
    
    const overallProgress = Math.min((totalCompleted / totalTargets) * 100, 100);

    return (
        <div className="glass-card p-4">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-100">Overall Progress</h3>
                <button
                    onClick={() => {
                        if (window.confirm('Are you sure you want to reset all progress?')) {
                            resetAllProgress();
                        }
                    }}
                    className="text-xs text-red-400 hover:text-red-300 transition-colors"
                >
                    Reset All
                </button>
            </div>

            {/* Mode Progress */}
            <div className="space-y-2">
                {(Object.values(StudyModeType) as StudyModeType[]).map((mode: StudyModeType) => {
                    const progress = progressByMode[mode];
                    const target = getTargetQuestions(mode);
                    const avgScore = progress.attempted > 0 
                        ? Math.round(progress.totalScore / progress.attempted) 
                        : 0;
                    const isComplete = isModuleComplete(mode);

                    return (
                        <div key={mode} className="group relative">
                            <div 
                                className={`flex items-center justify-between p-2 rounded ${
                                    currentMode === mode ? 'bg-violet-500/20' : 
                                    isComplete ? 'bg-green-500/20' : 'bg-gray-800'
                                }`}
                            >
                                <div className="flex flex-col">
                                    <span className="text-sm font-medium text-gray-100">
                                        {mode.split('_').map(word => 
                                            word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                                        ).join(' ')}
                                    </span>
                                    <span className="text-xs text-gray-400">
                                        Avg. Score: {avgScore}%
                                    </span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <span className="text-sm text-gray-400">
                                        {progress.completed}/{target}
                                    </span>
                                    {isComplete && <FiCheck className="text-green-400" />}
                                </div>
                            </div>

                            <button
                                onClick={() => {
                                    if (window.confirm(`Reset progress for ${mode}?`)) {
                                        resetModeProgress(mode);
                                    }
                                }}
                                className="absolute right-0 top-1/2 -translate-y-1/2 mr-2 
                                         opacity-0 group-hover:opacity-100 transition-opacity
                                         text-red-400 hover:text-red-300"
                            >
                                Reset
                            </button>
                        </div>
                    );
                })}
            </div>

            {/* Achievement Badge */}
            {overallProgress === 100 && (
                <div className="mt-4 flex items-center justify-center text-green-400 bg-green-500/20 p-2 rounded">
                    <FiAward className="w-5 h-5 mr-2" />
                    <span className="font-medium">You're on fire! 🔥 All modes completed!</span>
                </div>
            )}
        </div>
    );
}; 