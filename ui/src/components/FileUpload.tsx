import { cn } from '@/lib/utils';
import React, { useState } from 'react';
import { Upload, FileCheck } from 'lucide-react';

type Props = {
    className: string
}

const FileUpload = (props : Props) => {
    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (event: any) => {
        if (event.target.files && event.target.files[0]) {
            console.log(event.target.files[0]);
            setFile(event.target.files[0]);
        }
    };

    return (
        <div className={cn("flex flex-col items-center justify-center", 
            "bg-secondary p-4 rounded-lg",
            "w-[18rem] border-2 border-dashed border-gray-400",
            props.className)}>
            {file ? (<div className="w-full text-center overflow-hidden break-words">
                        <p className="text-slate-50 ">{file.name}</p>
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
    );
};

export default FileUpload;
