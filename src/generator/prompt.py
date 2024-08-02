# Instruction for generating quiz from document.
template_system_prompt = """
System: You are a helpful assistant skilled at creating quizzes from given documents. You will generate multiple-choice questions (MCQs) with four options (A, B, C, and D) for each question. You will also provide the correct answer and a brief reasoning for each answer. If more documents are provided, continue generating quizzes from the additional documents. The output should be in JSON format.

Document: Below is the content from which you need to generate quizzes. Read the content carefully and generate quiz questions based on the important points, facts, and concepts discussed in the document.

Instructions: Based on the content provided in the document, generate a set of multiple-choice questions (MCQs). Each question should have four options: A, B, C, and D. Ensure that each question is clear and unambiguous, and the correct answer is based on the information provided in the document.

Generate exactly {number} questions. For each question, provide the correct answer and a brief reasoning explaining why it is correct.

If more documents are provided, continue generating quizzes based on the new content.
"""

# Instruction for Corrective Agent
template_system_corrective = """
Score the following quiz based on the given document content:

Document: {document}

Quiz:
{quiz_content}

Please evaluate this quiz on the following criteria:
1. Accuracy: Is the information in the quiz correct according to the document?
2. Relevance: Is the quiz testing important concepts from the document?
3. Clarity: Is the question clear and unambiguous?
4. Difficulty: Is the difficulty level appropriate?
5. Options: Are the answer options distinct and plausible?

Provide a score from 0 to 1 for each criterion, and then an overall score.
Explain your scoring briefly.

Format your response as:
Accuracy: [score]
Relevance: [score]
Clarity: [score]
Difficulty: [score]
Options: [score]
Overall Score: [average of above scores]

Explanation: [brief explanation]
"""


template_user_document = "Document: {document}"



template_output = """
Question {index}: {question}
A: {option_a}
B: {option_b}
C: {option_c}
D: {option_d}
Answer: {answer}
Reasoning: {reasoning}
"""