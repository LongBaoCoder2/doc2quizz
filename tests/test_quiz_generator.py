import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from langchain_core.documents import Document
from pydantic import ValidationError

from src.generator import QuizGenerator, Quiz, merge_quizzes


@pytest.fixture
def mock_pdf_file():
    pdf_file = "data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf"
    return pdf_file

@pytest.fixture
def quiz_generator():
    return QuizGenerator()

def test_load_pdf(quiz_generator, mock_pdf_file):
    # Create a mock PDF file
    pdf_path = mock_pdf_file
    
    # Load the PDF file
    documents = quiz_generator.load_pdf(pdf_path)
    
    # Assert that the documents were loaded correctly
    assert len(documents) > 0

def test_parse_quizzes_from_response(quiz_generator):
    # Create a mock LLM response containing quiz data
    response_content = '[{"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"], "answer": "Paris", "reasoning": "Paris is the capital of France."}]'
    
    # Parse the quiz data from the response
    quizzes = quiz_generator.parse_quizzes_from_response(response_content)
    
    # Assert that the quizzes were parsed correctly
    assert len(quizzes) == 1
    assert isinstance(quizzes[0], Quiz)

# def test_generate_quizzes_from_full_documents(quiz_generator):
#     # Create mock documents
#     documents = [
#         Document(page_content="This is document 1."),
#         Document(page_content="This is document 2.")
#     ]
    
#     # Generate quizzes from the documents
#     quizzes = quiz_generator.generate_quizzes_from_full_documents(documents)
    
#     # Assert that the quizzes were correctly
#     assert len(quizzes) > 0
#     assert all(isinstance(quiz, Quiz) for quiz in quizzes)

# def test_generate(quiz_generator, mock_pdf_file):
#     # Create a mock PDF file
#     pdf_path = mock_pdf_file
    
#     # Generate quizzes from the PDF file
#     quizzes = quiz_generator.generate(pdf_path)
    
#     # Assert that the quizzes were generated correctly
#     assert len(quizzes) > 0
#     assert all(isinstance(quiz, Quiz) for quiz in quizzes)

def test_merge_quizzes():
    quizzes = [
        Quiz(question="Q1?", options=["A", "B", "C", "D"], answer="A", reasoning="R1"),
        Quiz(question="Q2?", options=["W", "X", "Y", "Z"], answer="Z", reasoning="R2")
    ]
    merged = merge_quizzes(quizzes)

    assert "Q1?" in merged
    assert "Q2?" in merged
    assert "A: A" in merged
    assert "D: Z" in merged
    assert "Answer: A" in merged
    assert "Answer: Z" in merged
    assert "Reasoning: R1" in merged
    assert "Reasoning: R2" in merged


# ======================================================

# def test_load_pdf(quiz_generator, mocker):
#     mock_loader = MagicMock()
#     mock_loader.load_and_split.return_value = [Document(page_content="Test content")]
#     mocker.patch.dict(quiz_generator.loader_classes, {'pdf': mock_loader})

#     documents = quiz_generator.load_pdf("dummy.pdf")

#     assert len(documents) == 1
#     assert documents[0].page_content == "Test content"

# def test_parse_quizzes_from_response(quiz_generator):
#     response = '[{"question": "Test?", "options": ["A", "B", "C", "D"], "answer": "A", "reasoning": "Because"}]'
#     quizzes = quiz_generator.parse_quizzes_from_response(response)

#     assert len(quizzes) == 1
#     assert quizzes[0].question == "Test?"
#     assert quizzes[0].options == ["A", "B", "C", "D"]
#     assert quizzes[0].answer == "A"
#     assert quizzes[0].reasoning == "Because"

# def test_parse_quizzes_from_response_invalid_json(quiz_generator):
#     response = 'Invalid JSON'
#     quizzes = quiz_generator.parse_quizzes_from_response(response)

#     assert len(quizzes) == 0

# def test_generate_quizzes_from_full_documents(quiz_generator, mocker):
#     mock_model = MagicMock()
#     mock_model.batch.return_value = [
#         MagicMock(content='[{"question": "Test?", "options": ["A", "B", "C", "D"], "answer": "A", "reasoning": "Because"}]')
#     ]
#     mocker.patch.object(quiz_generator, 'model', mock_model)

#     documents = [Document(page_content="Test content")]
#     quizzes = quiz_generator.generate_quizzes_from_full_documents(documents)

#     assert len(quizzes) == 1
#     assert quizzes[0].question == "Test?"

# def test_generate(quiz_generator, mocker):
#     mock_load_pdf = mocker.patch.object(quiz_generator, 'load_pdf')
#     mock_load_pdf.return_value = [Document(page_content="Test content")]

#     mock_generate_quizzes = mocker.patch.object(quiz_generator, 'generate_quizzes_from_full_documents')
#     mock_generate_quizzes.return_value = [
#         Quiz(question="Test?", options=["A", "B", "C", "D"], answer="A", reasoning="Because")
#     ]

#     quizzes = quiz_generator.generate("dummy.pdf")

#     assert len(quizzes) == 1
#     assert quizzes[0].question == "Test?"


