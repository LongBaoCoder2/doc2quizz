
JSON_FORMAT = """
The output should be in the following JSON format:

```json
[
    {
        "question": "[Write the question here]",
        "options": ["[Option A]", "[Option B]", "[Option C]", "[Option D]"],
        "answer": "[Specify the correct option]",
        "reasoning": "[Provide reasoning here]"
    },
    {
        "question": "[Write the question here]",
        "options": ["[Option A]", "[Option B]", "[Option C]", "[Option D]"],
        "answer": "[Specify the correct option]",
        "reasoning": "[Provide reasoning here]"
    },
    [More if needed]
]
```

Example:
[
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "C",
        "reasoning": "Paris is the capital city of France, known for its cultural, political, and economic significance."
    },
    ...
]
"""

BULLET_FORMAT = """
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