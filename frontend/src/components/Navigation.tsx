import React from 'react';
import { useSession } from '@context/SessionContext';
import { StudyModeType } from '@/types';
import { FiHome, FiChevronRight } from 'react-icons/fi';

export const Navigation: React.FC = () => {
    const { currentMode } = useSession();

    return (
        <div className="flex items-center space-x-2 text-sm text-gray-400 mb-6">
            <FiHome className="w-4 h-4" />
            <span>BrainiFi</span>
            {currentMode && (
                <>
                    <FiChevronRight className="w-4 h-4" />
                    <span className="text-violet-400">
                        {currentMode.split('_').map(word => 
                            word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                        ).join(' ')}
                    </span>
                </>
            )}
        </div>
    );
}; 