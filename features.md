# Features:

- [] **Supported Documents**: Initially, this project is only supported PDF format. We will development to add more document format.
- [] **Vector database**: Chroma
- [] **Personal concept**
- [] **User custom**: Allow users to choose their subject of focus for quiz generation..
  - Give user 2 options: _Generate based on full documents_ or _Specify a topic_.

# Todos:

- [] **Load Documents**: Implement functionality to load the documents.
- [] **Build Quiz System**: Develop a simple system to generate quizzes from the loaded documents.
- [] **Object Parser**: Create a parser to handle and process the document content.

# Problems:

**Large Context Windows**: Address the issue of handling full documents, which may involve large context windows.
**Missing Content**: Ensure that no content is missing, especially from the middle sections of the documents.

# Solutions:

1. Load full text and embed all into context windows.
2. Load each split documents to context windows and multi call LLM
