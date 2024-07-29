export interface Answer {
    id: number,
    answerContent: string,
    isCorrect: boolean,
}

export interface Question {
    questionContent: string,
    answers: Answer[],
    reasoning: string | null,
}

export interface QuestionResponse {
    question: string,
    options: string[],
    answer: string,
    reasoning: string,
}