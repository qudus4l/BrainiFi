import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiAlertCircle } from 'react-icons/fi';

interface Props {
    onUpload: (file: File) => void;
    isLoading: boolean;
}

export const FileUpload: React.FC<Props> = ({ onUpload, isLoading }) => {
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        setError(null);
        if (acceptedFiles.length > 0) {
            const file = acceptedFiles[0];
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                setError('File size too large. Please upload a file smaller than 10MB.');
                return;
            }
            onUpload(file);
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        multiple: false,
        disabled: isLoading
    });

    return (
        <div>
            <div 
                {...getRootProps()} 
                className={`
                    p-8 border-2 border-dashed rounded-lg
                    ${isDragActive ? 'border-violet-500 bg-violet-500/10' : 'border-gray-700'}
                    transition-all duration-200 ease-in-out
                    cursor-pointer hover:border-violet-500
                    flex flex-col items-center justify-center
                    ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
                `}
            >
                <input {...getInputProps()} disabled={isLoading} />
                <FiUploadCloud className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-gray-600 text-center">
                    {isDragActive
                        ? "Drop your PDF here..."
                        : "Drag & drop your PDF here, or click to select"}
                </p>
                <p className="text-sm text-gray-400 mt-2">
                    Only PDF files up to 10MB are supported
                </p>
                {isLoading && (
                    <div className="mt-4">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
                    </div>
                )}
            </div>
            
            {error && (
                <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center">
                    <FiAlertCircle className="mr-2" />
                    {error}
                </div>
            )}
        </div>
    );
}; 