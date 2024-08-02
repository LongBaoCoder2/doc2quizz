from langchain.agents import AgentType, initialize_agent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import List, Dict
import logging

from src.generator.prompt import template_system_corrective



class Corrective:
    def __init__(self, llm, quiz_generator, documents, score_threshold=0.7):
        self.llm = llm
        self.quiz_generator = quiz_generator
        self.documents = documents
        self.score_threshold = score_threshold
        self.tools = self._create_tools()
        self.agent = self._create_agent()

    def _create_tools(self):
        score_quiz_tool = Tool(
            name="ScoreQuiz",
            func=self._score_quiz,
            description="Score a quiz question based on accuracy, relevance, and quality."
        )
        regenerate_quiz_tool = Tool(
            name="RegenerateQuiz",
            func=self._regenerate_quiz,
            description="Request the QuizGenerator to regenerate a quiz question."
        )
        return [score_quiz_tool, regenerate_quiz_tool]

    def _create_agent(self):
        return initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def _score_quiz(self, quiz: Dict):
        prompt = PromptTemplate(
            input_variables=["document", "quiz_content"],
            template=template_system_corrective
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(document=self.documents, quiz_content=quiz)

    async def _regenerate_quiz(self, feedback: str):
        return await self.quiz_generator.generate_from_documents(self.documents, feedback)

    async def correct_quizzes(self, quizzes: List[Dict]) -> List[Dict]:
        corrected_quizzes = []
        for quiz in quizzes:
            score_result = await self.agent.arun(f"Score this quiz: {quiz}")
            
            # Extract overall score from the result
            overall_score = float(score_result.split('Overall Score:')[1].split('\n')[0].strip())
            
            if overall_score >= self.score_threshold:
                corrected_quizzes.append(quiz)
            else:
                logging.info(f"Quiz needs regeneration. Score: {overall_score}. Feedback: {score_result}")
                new_quiz = await self._regenerate_quiz(score_result)
                corrected_quizzes.append(new_quiz)
        
        return corrected_quizzes
