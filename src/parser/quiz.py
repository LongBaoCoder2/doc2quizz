import logging
from typing import List
from pydantic import BaseModel as PydanticBaseModel, TypeAdapter, ValidationError

from parser.format.quiz import JSON_FORMAT
from parser.format.utils import _escape_curly_braces


# Define the Pydantic Quiz class
class Quiz(PydanticBaseModel):
    question: str
    options: List[str]
    answer: str
    reasoning: str

class QuizParse:
    FORMAT_STR: str = JSON_FORMAT

    def __init__(self):
        self.quiz_ta = TypeAdapter(List[Quiz])
        
    def parse(self, content: str) -> List[Quiz]:
        """
        This function takes a string response from a LLM and 
        parses it into a list of Quiz objects.
        """

        # Find the start and end indices of the quiz data in the response
        # This is done by finding the first occurrence of '[' and the last occurrence of ']'
        left = content.find("[")
        right = content.rfind("]")

        # Extract the quiz data from the response using the found indices
        content = content[left: right + 1]

        try:
            # Attempt to validate the extracted quiz data as JSON
            # This will raise a ValidationError if the data is invalid
            list_quizzes = self.quiz_ta.validate_json(content)
        except ValidationError as e:
            # Log any validation errors that occur
            logging.error(f"Validation error: {e}")
            return []

        return list_quizzes 

    def format(self, prompt_template: str) -> str:
        return prompt_template + "\n\n" + _escape_curly_braces(self.FORMAT_STR)