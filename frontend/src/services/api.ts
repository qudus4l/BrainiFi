import axios, { AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

interface APIError {
    message: string;
    details?: string;
}

const handleError = (error: unknown): never => {
    if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<{ detail: string }>;
        if (axiosError.response) {
            throw new Error(axiosError.response.data.detail || 'Server error occurred');
        } else if (axiosError.request) {
            throw new Error('No response from server. Please check your connection.');
        }
    }
    throw new Error('An unexpected error occurred');
};

export const uploadPDF = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        console.log('Attempting to upload file to:', `${API_BASE_URL}/upload`);
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server error:', errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        console.log('Server response:', data);
        return data;
    } catch (error) {
        console.error('Detailed upload error:', error);
        if (error instanceof TypeError && error.message === 'Failed to fetch') {
            throw new Error("Hmm, can't reach the server. Mind checking your internet? 🌐");
        }
        throw error;
    }
};

export const validateAnswer = async (question: string, context: string, answer: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question, context, answer }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error validating answer:', error);
        throw error;
    }
};

// Add request interceptor for common headers
api.interceptors.request.use((config) => {
    // You could add auth tokens here if needed
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Add response interceptor for common error handling
api.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response?.status === 429) {
        return Promise.reject(new Error("Whoa there, speedster! Let's take a quick breather. 😅"));
    }
    return Promise.reject(error);
}); 