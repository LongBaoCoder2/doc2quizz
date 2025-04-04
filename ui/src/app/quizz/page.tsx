"use client"

import { Button } from "@/components/ui/button";
import { useState } from "react";
import ProgressBar from '@/components/ProgressBar'
import ResultBox from '@/components/ResultBox'
import { ChevronLeft, FileCheck, Upload, X } from "lucide-react";
import { Answer, Question, QuestionResponse } from "@/types/Question";
import { cn } from "@/lib/utils";



export default function Quizz() {
    const [started, setStarted] = useState<boolean>(false);  
    const [currentQuestion, setCurrentQuestion] = useState<number>(0);
    const [score, setScore] = useState<number | null>(null);
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
    const [uploadFile, setUploadFile] = useState<File | null>(null);
    const [listQuestions, setListQuestion] = useState<Question[] | null>(null);

    const handleFileChange = (event: any) => {
        if (event.target.files && event.target.files[0]) {
            console.log(event.target.files[0]);
            setUploadFile(event.target.files[0]);
        }
    };

    const handleCancelUpload = () => {
        setUploadFile(null);
    }

    const handleGenerateBtn = async () => {
        try {
            if (!uploadFile || listQuestions)
                return;
    
            const body = new FormData();
            body.append("file", uploadFile);
            const response = await fetch("http://127.0.0.1:8000/upload", {
                method: "POST",
                body
            });
    
            const data = await response.json();
            if (data) {
                const letterToNumber: { [key: string]: number } = {
                    'A': 0,
                    'B': 1,
                    'C': 2,
                    'D': 3
                  };
                const quizzes = data.quizzes;
                const listQuizzes = quizzes.map((quiz: QuestionResponse) => {
                    const correctAnswer = letterToNumber[quiz.answer];
                    const answer = quiz.options.map((op, id) => {
                        return {
                            id: id,
                            answerContent: op,
                            isCorrect: id === correctAnswer
                        } as Answer;
                    });

                    return {
                        questionContent: quiz.question,
                        reasoning: quiz.reasoning,
                        answers: answer
                    } as Question;
                })

                setListQuestion(listQuizzes);
            }

        } catch (err: any) {
            console.error(err);
        }

    }

    const handleCancelQuiz = () => {
        setListQuestion(null);
    }

    const handleNextButton = () => {
        if (!started) {
            setStarted(true);
            setScore(0);
            return;
        }
        
        if (listQuestions && currentQuestion < listQuestions.length - 1) 
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
        <div className="flex flex-col flex-1">
            {listQuestions ? <div className="flex flex-col flex-1">
                <div className="position-sticky top-0 z-10 shadow-md py-4 w-full">
                    <header className="grid grid-cols-[auto,1fr,auto] grid-flow-col items-center justify-between gap-5 py-2">
                        <Button size="icon" variant={'outline'} onClick={handlePrevAnswer}>
                            <ChevronLeft />
                        </Button>
                        <ProgressBar value={100 * currentQuestion / listQuestions.length} />
                        <Button size="icon" variant={'destructive'} onClick={handleCancelQuiz}>
                            <X />
                        </Button>
                    </header>
                </div>
                <main className="flex justify-center flex-1 mt-10">
                    {
                        !started ? <h1 className="text-4xl font-bold">Quiz 👋</h1> : 
                            <div>
                                <h2 className="text-2xl text-center font-bold">{listQuestions[currentQuestion]?.questionContent}</h2>
                                <div className="grid grid-cols-1 gap-6 mt-10">
                                    {
                                        listQuestions[currentQuestion]?.answers.map(ans => {
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
                    <ResultBox result={isCorrect} message={listQuestions[currentQuestion]?.reasoning}/>
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
                                        <Button size="icon" variant={'destructive'} onClick={handleCancelUpload}>
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
                <Button onClick={handleGenerateBtn}>Generate</Button>
            </div>
        }

        </div>
    )
}
