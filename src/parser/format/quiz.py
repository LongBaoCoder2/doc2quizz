
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