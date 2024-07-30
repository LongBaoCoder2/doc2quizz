import os
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException   
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from generator import QuizGenerator, merge_quizzes, Quiz

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = { 'pdf' }

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize QuizGenerator
class QuizResponse(BaseModel):
    message: str
    quizzes: List[Quiz]

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/")
async def home():
    return "Hello world"

@app.post("/upload", response_model=QuizResponse)
async def upload_file(file: UploadFile | None = File(...)):
    logging.debug("Start generate: ")

    if not file:
        raise HTTPException(status_code=400, detail="No file sent")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    logging.debug("Start generate: ")

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Save the file
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Generate quizzes from the uploaded PDF
        # Load the PDF file and split it into documents
        quiz_generator = QuizGenerator()
        quizzes = await quiz_generator.generate(filepath)

        # Clean up: remove the uploaded file
        os.remove(filepath)

        return QuizResponse(
            message="Generate quizzes from full document.",
            quizzes=quizzes
        )

    except Exception as e:
        # Clean up in case of error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)