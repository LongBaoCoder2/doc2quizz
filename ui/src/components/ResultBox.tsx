import React from 'react'
import { Alert, AlertTitle, AlertDescription } from './ui/alert'
import { Sparkles, CloudLightning  } from 'lucide-react'

type Props = {
    result: boolean | null,
    message: string | null,
}

const ResultBox = (props: Props) => {
    const resultClass = props.result 
        ? "bg-green-100 border-green-400 text-green-700"
        : "bg-red-100 border-red-400 text-red-700";

    const messageIcon = props.result ? <Sparkles className="text-lg text-slate-400"/> 
                                     : <CloudLightning className="text-lg text-slate-400"/> 

    return (
        <div className='w-full'>
            {props.result !== null && 
                <Alert 
                    className={`border-dashed border-2 ${resultClass} bg-secondary py-4 px-6 rounded-lg shadow-md transition-all`}>
                    <div className='flex gap-3 justify-center items-center'>
                        {messageIcon}
                        <AlertTitle className="font-bold text-lg">{props.result ? "Correct" : "Oohs"}</AlertTitle>
                    </div>
                    <AlertDescription className='text-slate-200'>
                        {props.message}
                    </AlertDescription>
                </Alert>
            }
        </div>
    );
};

export default ResultBox;