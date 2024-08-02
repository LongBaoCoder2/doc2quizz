import re
import logging
from typing import List, Dict, Optional, Any, Tuple, Union

from langchain.agents import Agent, AgentExecutor, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from langchain.schema import AgentAction, AgentFinish
from langchain.output_parsers import RegexParser
from pydantic import BaseModel

from langchain_core.language_models import LLM

from src.generator.generator import QuizGenerator


class WebSearchTool:
    def search(self, query: str) -> str:
        # Implement web search API call here
        pass

class VectorDBTool:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def search(self, query: str) -> List[str]:
        # Implement vector store search here
        pass

class SyntheticDataTool:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt: str) -> str:
        # Implement synthetic data generation using LLM
        pass

class AgentWatcher(Agent):
    llm: LLM
    embeddings: Embeddings
    vector_store: VectorStore

    def __init__(self, llm: LLM, embeddings: Embeddings, vector_store: VectorStore):
        self.llm = llm
        self.embeddings = embeddings
        self.vector_store = vector_store
        self.tools = self._create_tools()
        super().__init__(llm=llm, tools=self.tools)

    def _create_tools(self) -> List[Tool]:
        return [
            Tool(
                name="WebSearch",
                func=WebSearchTool().search,
                description="Search the web for additional information."
            ),
            Tool(
                name="VectorDBSearch",
                func=VectorDBTool(self.vector_store).search,
                description="Search the vector database for relevant documents."
            ),
            Tool(
                name="SyntheticDataGeneration",
                func=SyntheticDataTool(self.llm).generate,
                description="Generate synthetic data for additional insights."
            )
        ]

    def input_keys(self) -> List[str]:
        return ["user_prompt", "documents", "topic"]

    def output_keys(self) -> List[str]:
        return ["documents", "web_search", "vector_db_search", "synthetic_data"]

    def plan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], 
        user_prompt: str | None = None,
        documents: str | None = None,
        topic: str | None = None,
    ) -> Union[AgentAction, AgentFinish]:
        prompt = self.create_prompt()

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(user_prompt=user_prompt, documents=documents, topic=topic, intermediate_steps=intermediate_steps)

        if "Action:" in response:
            action_parser = self._get_default_output_parser().parse(response)
            # action_parser = re.search(r"Action: (\w+)\nAction Input: (.*)", response, re.DOTALL)
            if action_parser:
                action = action_parser['action']
                action_input = action_parser['action']
                return AgentAction(tool=action, tool_input=action_input, log=response)
        elif "Final Answer:" in response:
            return AgentFinish(return_values=self._parse_final_answer(response), log=response)

        # If no action or final answer is found, return a default finish
        return AgentFinish(return_values={"documents": documents}, log="No specific action or final answer found.")

    def _parse_final_answer(self, response: str) -> Dict[str, Any]:
        final_answer = response.split("Final Answer:")[1].strip()
        need_more_info = "Yes" in final_answer.split("Need More Info:")[1].split("\n")[0]
        relevant_docs = final_answer.split("Relevant Documents:")[1].split("\n")[0].strip()
        additional_actions = final_answer.split("Additional Actions:")[1].split("\n")[0].strip().split("/")

        return {
            "need_more_info": need_more_info,
            "relevant_docs": relevant_docs,
            "additional_actions": additional_actions
        }

    async def process_request(self, user_prompt: str, documents: List[str], topic: Optional[str] = None) -> Dict:
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self,
            tools=self.tools,
            verbose=True
        )

        result = await agent_executor.arun(user_prompt=user_prompt, documents=documents, topic=topic)

        final_data = {"documents": documents}

        if result.get("need_more_info", False):
            for action in result.get("additional_actions", []):
                if action == "WebSearch":
                    final_data["web_search"] = await self.tools[0].arun(f"Perform a web search related to: {user_prompt}")
                elif action == "VectorDBSearch":
                    final_data["vector_db_search"] = await self.tools[1].arun(f"Search the vector database for: {user_prompt}")
                elif action == "SyntheticDataGeneration":
                    final_data["synthetic_data"] = await self.tools[2].arun(f"Generate synthetic data for: {user_prompt}")

        if result.get("relevant_docs") != "All":
            final_data["documents"] = [documents[int(i)] for i in result.get("relevant_docs", "").split(",")]

        return final_data

    @property
    def _agent_type(self) -> str:
        return "watcher-agent"

    def create_prompt(self, tools: List[Tool]) -> PromptTemplate:
        return PromptTemplate(
            input_variables=["user_prompt", "documents", "topic", "intermediate_steps"],
            template="""
            Analyze the following user prompt and documents:

            User Prompt: {user_prompt}
            Documents: {documents}
            Topic (if specified): {topic}
            Intermediate Steps: {intermediate_steps}

            Your tasks are:
            1. Determine if more information is needed to generate quizzes effectively.
            2. If a specific topic is given, select only the relevant documents.
            3. Decide if web search, vector database search, or synthetic data generation is needed.

            Provide your analysis and decisions in the following format:
            Need More Info: [Yes/No]
            Relevant Documents: [List of relevant document indices or 'All' if no specific topic]
            Additional Actions: [List of required actions: WebSearch/VectorDBSearch/SyntheticDataGeneration/None]
            Reasoning: [Brief explanation of your decisions]

            If you need to use a tool, respond with:
            Action: [Tool Name]
            Action Input: [Input for the tool]

            If you have all the necessary information, respond with:
            Final Answer: [Your final analysis and decisions]
            """
        )

    @property
    def observation_prefix(self) -> str:
        return "Observation: "

    @property
    def llm_prefix(self) -> str:
        return "AgentWatcher: "

    def _get_default_output_parser(self):
        return RegexParser(
            regex=r"Action: (.*?)[\n]*Action Input:[\s]*(.*)",
            output_keys=["action", "action_input"],
        )

class QuizApplication:
    def __init__(self, llm, embeddings: Embeddings, vector_store: VectorStore):
        self.agent_watcher = AgentWatcher(llm, embeddings, vector_store)
        self.quiz_generator = QuizGenerator(llm)
        self.corrective = Corrective(llm, self.quiz_generator, None)  # We'll set documents later

    async def generate_quizzes(self, user_prompt: str, documents: List[str], topic: Optional[str] = None) -> List[Dict]:
        # Process the request through AgentWatcher
        processed_data = await self.agent_watcher.process_request(user_prompt, documents, topic)

        # Update the Corrective with the final documents
        self.corrective.documents = processed_data["documents"]

        # Generate quizzes
        quizzes = await self.quiz_generator.generate_from_documents(processed_data["documents"], user_prompt)

        # Correct quizzes
        corrected_quizzes = await self.corrective.correct_quizzes(quizzes)

        return corrected_quizzes

# Usage
# async def main():
#     llm = # Initialize your LLM
#     embeddings = # Initialize your embeddings
#     vector_store = # Initialize your vector store

#     app = QuizApplication(llm, embeddings, vector_store)

#     user_prompt = "Generate quizzes about machine learning algorithms"
#     documents = # Load your documents
#     topic = "supervised learning"

#     quizzes = await app.generate_quizzes(user_prompt, documents, topic)
#     print(quizzes)

# # Run the application
# import asyncio
# asyncio.run(main())