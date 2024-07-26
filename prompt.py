template_prompt = """
System: You are a helpful assistant skilled at creating quizzes from given documents. You will generate multiple-choice questions (MCQs) with four options (A, B, C, and D) for each question.

Document: Below is the content from which you need to generate quizzes. Read the content carefully and generate quiz questions based on the important points, facts, and concepts discussed in the document.

{document}

Instructions: Based on the content provided in the document, generate a set of multiple-choice questions (MCQs). Each question should have four options: A, B, C, and D. Ensure that each question is clear and unambiguous, and the correct answer is based on the information provided in the document.

Format:
1. Question: [Write the question here]
   - A: [Option A]
   - B: [Option B]
   - C: [Option C]
   - D: [Option D]

2. Question: [Write the question here]
   - A: [Option A]
   - B: [Option B]
   - C: [Option C]
   - D: [Option D]

[Repeat the format for as many questions as needed]

Example:
1. Question: What is the capital of France?
   - A: Berlin
   - B: Madrid
   - C: Paris
   - D: Rome
"""