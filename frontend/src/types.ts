export enum StudyModeType {
    QUICK_REVIEW = "QUICK_REVIEW",
    DEEP_STUDY = "DEEP_STUDY",
    REVISION = "REVISION",
    TEST_PREP = "TEST_PREP"
}

export interface ModuleProgress {
    attempted: number;
    completed: number;
    totalScore: number;
}

export interface Question {
    question: string;
    type: string;
    context: string;
    difficulty: string;
    hint: string;
    key_points: string[];
    mode?: StudyModeType;
}

export interface Feedback {
    score: number;
    feedback: string;
    strengths: string[];
    improvements: string[];
    tip: string;
}

export interface Questions {
    [StudyModeType.QUICK_REVIEW]: Question[];
    [StudyModeType.DEEP_STUDY]: Question[];
    [StudyModeType.REVISION]: Question[];
    [StudyModeType.TEST_PREP]: Question[];
} 