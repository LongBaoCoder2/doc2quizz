import pytest
import warnings

from src.parser import QuizParse, Quiz
from src.config.quiz_generation import QuizGeneratorConfig

warnings.filterwarnings("ignore", category=DeprecationWarning)


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