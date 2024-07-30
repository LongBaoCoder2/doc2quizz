import pytest
from src.parser import QuizParse, Quiz

@pytest.fixture
def quiz_parser():
    return QuizParse()

def test_parse_quizzes_from_response(quiz_parser):
    # Create a mock LLM response containing quiz data
    response_content = '[{"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"], "answer": "Paris", "reasoning": "Paris is the capital of France."}]'
    
    # Parse the quiz data from the response
    quizzes = quiz_parser.parse(response_content)
    
    # Assert that the quizzes were parsed correctly
    assert len(quizzes) == 1
    assert isinstance(quizzes[0], Quiz)