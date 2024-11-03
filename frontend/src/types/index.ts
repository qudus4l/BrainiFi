export interface Question {
    question: string;
    type: 'knowledge' | 'application' | 'analysis' | 'evaluation';
    context: string;
    difficulty: 'easy' | 'medium' | 'hard';
    hint: string;
    key_points: string[];
}

export interface Feedback {
    score: number;
    feedback: string;
    strengths: string[];
    improvements: string[];
    tip: string;
}

export enum StudyMode {
    QUICK_REVIEW = "quick_review",
    DEEP_STUDY = "deep_study",
    REVISION = "revision",
    TEST_PREP = "test_prep"
}

export interface Questions {
    [StudyMode.QUICK_REVIEW]: Question[];
    [StudyMode.DEEP_STUDY]: Question[];
    [StudyMode.REVISION]: Question[];
    [StudyMode.TEST_PREP]: Question[];
}

export interface APIResponse<T> {
    status: 'success' | 'error';
    data?: T;
    error?: string;
} 