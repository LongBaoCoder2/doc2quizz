"use client"

import { Button } from "@/components/ui/button";
import { useState } from "react";
import ProgressBar from '@/components/ProgressBar'
import ResultBox from '@/components/ResultBox'
import { ChevronLeft, FileCheck, Upload, X } from "lucide-react";
import { Answer, Question } from "@/types/Question";
import FileUpload from "@/components/FileUpload";
import { cn } from "@/lib/utils";


const questions: Question[] = [
    {
        "questionContent": "What is the capital of France?",
        "answers": [
            { "id": 1, "answerContent": "Paris", "isCorrect": true },
            { "id": 2, "answerContent": "Lyon", "isCorrect": false },
            { "id": 3, "answerContent": "Marseille", "isCorrect": false },
            { "id": 4, "answerContent": "Nice", "isCorrect": false }
        ],
        "reasoning": "Paris is the capital and most populous city of France."
    },
    {
        "questionContent": "Which element has the chemical symbol 'O'?",
        "answers": [
            { "id": 1, "answerContent": "Oxygen", "isCorrect": true },
            { "id": 2, "answerContent": "Gold", "isCorrect": false },
            { "id": 3, "answerContent": "Silver", "isCorrect": false },
            { "id": 4, "answerContent": "Osmium", "isCorrect": false }
        ],
        "reasoning": "The chemical symbol 'O' stands for Oxygen, which is a key element in the periodic table."
    },
    {
        "questionContent": "Who wrote 'Pride and Prejudice'?",
        "answers": [
            { "id": 1, "answerContent": "Jane Austen", "isCorrect": true },
            { "id": 2, "answerContent": "Charlotte Brontë", "isCorrect": false },
            { "id": 3, "answerContent": "Mary Shelley", "isCorrect": false },
            { "id": 4, "answerContent": "Emily Brontë", "isCorrect": false }
        ],
        "reasoning": "'Pride and Prejudice' is a novel by Jane Austen, first published in 1813."
    },
    {
        "questionContent": "What is the largest planet in our solar system?",
        "answers": [
            { "id": 1, "answerContent": "Jupiter", "isCorrect": true },
            { "id": 2, "answerContent": "Saturn", "isCorrect": false },
            { "id": 3, "answerContent": "Neptune", "isCorrect": false },
            { "id": 4, "answerContent": "Earth", "isCorrect": false }
        ],
        "reasoning": "Jupiter is the largest planet in our solar system, with a diameter of about 142,984 km."
    },
    {
        "questionContent": "In which year did the Titanic sink?",
        "answers": [
            { "id": 1, "answerContent": "1912", "isCorrect": true },
            { "id": 2, "answerContent": "1905", "isCorrect": false },
            { "id": 3, "answerContent": "1920", "isCorrect": false },
            { "id": 4, "answerContent": "1918", "isCorrect": false }
        ],
        "reasoning": "The RMS Titanic sank on April 15, 1912, after hitting an iceberg during its maiden voyage."
    }
]


export default function Quizz() {
    const [started, setStarted] = useState<boolean>(false);  
    const [currentQuestion, setCurrentQuestion] = useState<number>(0);
    const [score, setScore] = useState<number | null>(null);
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
    const [uploadFile, setUploadFile] = useState<File | null>(null);
    const [listQuestions, setListQuestion] = useState<Question[] | null>(questions);

    const handleFileChange = (event: any) => {
        if (event.target.files && event.target.files[0]) {
            console.log(event.target.files[0]);
            setUploadFile(event.target.files[0]);
        }
    };


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
        if (selectedAnswer === null)
            setSelectedAnswer(answer.id);
        const currentCorrect = answer.isCorrect;
        
        if (currentCorrect) {
            const nextScore = score ? score + 1 : 1;
            setScore(nextScore);
            console.log(score);
        }

        if (isCorrect === null)
            setIsCorrect(currentCorrect);
    }

    const handlePrevAnswer = () => {
        if (currentQuestion > 0)
            setCurrentQuestion(currentQuestion - 1);
    }

    return (
        <div className="pt-10">
            {listQuestions ? <div className="flex flex-col flex-1">
                <div className="position-sticky top-0 z-10 shadow-md py-4 w-full">
                    <header className="grid grid-cols-[auto,1fr,auto] grid-flow-col items-center justify-between gap-5 py-2">
                        <Button size="icon" variant={'outline'} onClick={handlePrevAnswer}>
                            <ChevronLeft />
                        </Button>
                        <ProgressBar value={100 * currentQuestion / questions.length} />
                        <Button size="icon" variant={'destructive'}>
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
                                            return <Button key={ans.id} 
                                                        variant={'secondary'} 
                                                        onClick={() => handleAnswer(ans)}
                                                        className={selectedAnswer && selectedAnswer == ans.id ? "bg-lime-500" : ""}>
                                                                {ans.answerContent}
                                                </Button>
                                        })
                                    }
                                </div>
                            </div>
                    }
                </main>
                <footer className="footer flex flex-col items-center pb-9 px-6 py-5 relative mb-0 gap-6">
                    <ResultBox result={isCorrect} message={questions[currentQuestion]?.reasoning}/>
                    <Button onClick={handleNextButton}>{started ? "Next" : "Start"}</Button>
                </footer>
            </div>
        : <div className="flex flex-col mt-10 gap-10 justify-center items-center">
            <div className={cn("flex flex-col items-center justify-center", 
                        "bg-secondary p-4 rounded-lg",
                        "w-[30rem] border-2 border-dashed border-gray-400")}>
                        {uploadFile ? (<div className="flex justify-center items-center gap-6 w-full text-center overflow-hidden break-words">
                                        <FileCheck />
                                        <p className="text-slate-50">{uploadFile.name}</p>
                                        <Button size="icon" variant={'destructive'}>
                                            <X />
                                        </Button>
                                    </div>) 
                            : (<div>
                                    <input
                                        type="file"
                                        accept="application/pdf"
                                        onChange={handleFileChange}
                                        className="hidden"
                                        id="pdf-upload"
                                    />
                                    <label htmlFor="pdf-upload" className="flex items-center cursor-pointer gap-4">
                                        <Upload />
                                        <span className="text-slate-50 text-lg">Upload PDF</span>
                                    </label>
                                </div>)}
                    </div>
                <Button>Generate</Button>
            </div>
        }

        </div>
    )
}
