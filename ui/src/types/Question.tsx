export type Answer = {
    id: number,
    answerContent: string,
    isCorrect: boolean,
}

export type Question = {
    questionContent: string,
    answers: Answer[],
    reasoning: string | null,
}