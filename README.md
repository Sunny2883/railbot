# **Project Title:** Railway chatbot

**Description:**

This project is to make a chatbot that will help railway users to get answers of their queries. It will leverage the power of llm models and langchain agents.


**Key points:**
- ***knowledgebase: *** The chatbot has access to a knowledge base containing information related to the trains. the data is stored in a vector database. Chromadb has been used as a vector database.
- ***External API call: *** The chatbot can call external API and get relevan information
- ***Web search: *** The chatbot can access web through tools like duckduckgo search and find answers or information regarding user queries
- ***Langchain agents: *** The chatbot uses Langchain agent to utilize all the available options and tools properly.
- ***FastAPI integration*** The functionalities like file upload and question-answer or chat is integrated with FastAPI and can be accessed in other projects by using proper url.


**Tech Stacks:**
1. Python
2. Langchain
3. FastAPI
4. OpenAI LLM model
5. Huggingface embedding model


**Usage instruction:**
1. install python >3.11.0 <3.12.0 (3.11.7 preffered) in your system. prefer python official website for installation guides: <https://www.python.org/downloads/>
2. install poetry for project management, package and dependency management
   pip install poetry
   (follow poetry official docs for reference: <https://python-poetry.org/docs/>
3. clone the git repository in a new created folder.
4. initialize a poetry project in it.
    poetry init
5. create a virtual environment by poetry shell.
    poetry shell
6. add a .env file and add all the api keys and other secrets, take help from .env.example file.
7. get openai api key: <https://platform.openai.com/api-keys>
8. run the project by using uvicorn run.
    uvicorn src.main:app
