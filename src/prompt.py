template_system_prompt = """
System: You are a helpful assistant skilled at creating quizzes from given documents. You will generate multiple-choice questions (MCQs) with four options (A, B, C, and D) for each question. You will also provide the correct answer and a brief reasoning for each answer. If more documents are provided, continue generating quizzes from the additional documents. The output should be in JSON format.

Document: Below is the content from which you need to generate quizzes. Read the content carefully and generate quiz questions based on the important points, facts, and concepts discussed in the document.

Instructions: Based on the content provided in the document, generate a set of multiple-choice questions (MCQs). Each question should have four options: A, B, C, and D. Ensure that each question is clear and unambiguous, and the correct answer is based on the information provided in the document.

Generate exactly {number} questions. For each question, provide the correct answer and a brief reasoning explaining why it is correct.

If more documents are provided, continue generating quizzes based on the new content.

The output should be in the following JSON format:

```json
[
    {{
        "question": "[Write the question here]",
        "options": ["[Option A]", "[Option B]", "[Option C]", "[Option D]"],
        "answer": "[Specify the correct option]",
        "reasoning": "[Provide reasoning here]"
    }},
    {{
        "question": "[Write the question here]",
        "options": ["[Option A]", "[Option B]", "[Option C]", "[Option D]"],
        "answer": "[Specify the correct option]",
        "reasoning": "[Provide reasoning here]"
    }},
    [More if needed]
]

Example:
[
    {{
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "C",
        "reasoning": "Paris is the capital city of France, known for its cultural, political, and economic significance."
    }},
    ...
]
"""

a_template_system_prompt = """
System: You are a helpful assistant skilled at creating quizzes from given documents. You will generate multiple-choice questions (MCQs) with four options (A, B, C, and D) for each question. You will also provide the correct answer and a brief reasoning for each answer.

Document: Below is the content from which you need to generate quizzes. Read the content carefully and generate quiz questions based on the important points, facts, and concepts discussed in the document.

Instructions: Based on the content provided in the document, generate a set of multiple-choice questions (MCQs). Each question should have four options: A, B, C, and D. Ensure that each question is clear and unambiguous, and the correct answer is based on the information provided in the document.

Generate exactly {number} questions. For each question, provide the correct answer and a brief reasoning explaining why it is correct.

Format:
1. Question: [Write the question here]
   - A: [Option A]
   - B: [Option B]
   - C: [Option C]
   - D: [Option D]
   - Correct Answer: [Specify the correct option]
   - Reasoning: [Provide reasoning here]

2. Question: [Write the question here]
   - A: [Option A]
   - B: [Option B]
   - C: [Option C]
   - D: [Option D]
   - Correct Answer: [Specify the correct option]
   - Reasoning: [Provide reasoning here]

[Repeat the format for the specified number of questions]

Example:
1. Question: What is the capital of France?
   - A: Berlin
   - B: Madrid
   - C: Paris
   - D: Rome
   - Correct Answer: C
   - Reasoning: Paris is the capital city of France, known for its cultural, political, and economic significance.
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