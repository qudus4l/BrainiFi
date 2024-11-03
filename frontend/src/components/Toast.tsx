import React, { useEffect } from 'react';
import { FiCheck, FiX, FiInfo, FiAlertTriangle } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastProps {
    message: string;
    type: ToastType;
    onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
    useEffect(() => {
        const timer = setTimeout(onClose, 5000);
        return () => clearTimeout(timer);
    }, [onClose]);

    const icons = {
        success: <FiCheck className="w-5 h-5 text-green-400" />,
        error: <FiX className="w-5 h-5 text-red-400" />,
        info: <FiInfo className="w-5 h-5 text-blue-400" />,
        warning: <FiAlertTriangle className="w-5 h-5 text-yellow-400" />
    };

    const bgColors = {
        success: 'bg-green-500/10',
        error: 'bg-red-500/10',
        info: 'bg-blue-500/10',
        warning: 'bg-yellow-500/10'
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className={`fixed bottom-4 right-4 ${bgColors[type]} backdrop-blur-sm 
                       border border-gray-700/50 rounded-lg p-4 shadow-lg 
                       flex items-center space-x-3 max-w-md`}
        >
            {icons[type]}
            <span className="text-gray-200">{message}</span>
            <button 
                onClick={onClose}
                className="text-gray-400 hover:text-gray-200 transition-colors"
            >
                <FiX className="w-4 h-4" />
            </button>
        </motion.div>
    );
}; 