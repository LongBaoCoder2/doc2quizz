"use client"

import { Button } from "@/components/ui/button";
import { useState } from "react";
import ProgressBar from '@/components/ProgressBar'
import { ChevronLeft, X } from "lucide-react";


type Answer = {
    id: number,
    answerContent: string,
    isCorrect: boolean,
}

type Question = {
    questionContent: string,
    answers: Answer[]
}

const questions: Question[] = 
[
    {
        "questionContent": "What is the chemical symbol for gold?",
        "answers": [
            {
                "id": 1,
                "answerContent": "Au",
                "isCorrect": true
            },
            {
                "id": 2,
                "answerContent": "Ag",
                "isCorrect": false
            },
            {
                "id": 3,
                "answerContent": "Pb",
                "isCorrect": false
            },
            {
                "id": 4,
                "answerContent": "Fe",
                "isCorrect": false
            }
        ]
    },
    {
        "questionContent": "Who wrote 'To Kill a Mockingbird'?",
        "answers": [
            {
                "id": 1,
                "answerContent": "Harper Lee",
                "isCorrect": true
            },
            {
                "id": 2,
                "answerContent": "Mark Twain",
                "isCorrect": false
            },
            {
                "id": 3,
                "answerContent": "Ernest Hemingway",
                "isCorrect": false
            },
            {
                "id": 4,
                "answerContent": "J.D. Salinger",
                "isCorrect": false
            }
        ]
    },
    {
        "questionContent": "What is the capital city of Japan?",
        "answers": [
            {
                "id": 1,
                "answerContent": "Tokyo",
                "isCorrect": true
            },
            {
                "id": 2,
                "answerContent": "Osaka",
                "isCorrect": false
            },
            {
                "id": 3,
                "answerContent": "Kyoto",
                "isCorrect": false
            },
            {
                "id": 4,
                "answerContent": "Hiroshima",
                "isCorrect": false
            }
        ]
    }
]



export default function Quizz() {
    const [started, setStarted] = useState<boolean>(false);  
    const [currentQuestion, setCurrentQuestion] = useState<number>(0);
    const [score, setScore] = useState<number | null>(null);
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);


    const handleNextButton = () => {
        if (!started) {
            setStarted(true);
            setScore(0);
            return;
        }
        
        if (currentQuestion < questions.length - 1) 
            setCurrentQuestion(currentQuestion + 1);

        setIsCorrect(null);
        setSelectedAnswer(null);
    }

    const handleAnswer = (answer: Answer) => {
        setSelectedAnswer(answer.id);
        const currentCorrect = answer.isCorrect;
        
        if (currentCorrect) {
            const nextScore = score ? score + 1 : 1;
            setScore(nextScore);
            console.log(score);
        }
        setIsCorrect(currentCorrect);
    }

    return (
        <div className="flex flex-col flex-1">
            <div className="position-sticky top-0 z-10 shadow-md py-4 w-full">
                <header className="grid grid-cols-[auto,1fr,auto] grid-flow-col items-center justify-between gap-5 py-2">
                    <Button size="icon" variant={'outline'}>
                        <ChevronLeft />
                    </Button>
                    <ProgressBar value={100 * currentQuestion / questions.length} />
                    <Button size="icon" variant={'secondary'}>
                        <X />
                    </Button>
                </header>
            </div>
            <main className="flex justify-center flex-1 mt-10">
                {
                    !started ? <h1 className="text-4xl font-bold">Quiz 👋</h1> : 
                        <div>
                            <h2 className="text-2xl text-center font-bold">{questions[currentQuestion]?.questionContent}</h2>
                            <div className="grid grid-cols-1 gap-6 mt-10">
                                {
                                    questions[currentQuestion]?.answers.map(ans => {
                                        return <Button key={ans.id} variant={'secondary'} onClick={() => handleAnswer(ans)}>{ans.answerContent}</Button>
                                    })
                                }
                            </div>
                        </div>
                }
            </main>
            <footer className="footer flex flex-col items-center pb-9 px-6 py-5 relative mb-0">
                <p>{isCorrect ? "Correct" : "Incorrect"}</p> 
                <Button onClick={handleNextButton}>{started ? "Next" : "Start"}</Button>
            </footer>
        </div>
    )
}
