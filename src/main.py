"""fastapi integration"""

import os
import tempfile
from fastapi import FastAPI, UploadFile
import uvicorn
from langchain_core.messages import AIMessage, HumanMessage

from .utils_custom import custom_agent
from .utils_custom.load_data import load_file

app = FastAPI()


@app.get("/")
async def root():
    """base path"""
    return {"message": "Welcome to railway bot application!"}


chat_history = []


@app.get("/get-answer/{question}")
async def get_answer(question: str):
    """ "Api endpoint for taking user query and returning relevant answer.
    arguments:
    question: the input question the bot should must answer
    returns:
    a dictionary containing the question and answer
    """
    answer = custom_agent.agent_executor.invoke(
        {"input": question, "chat_history": chat_history}
    )
    chat_history.extend(
        [
            HumanMessage(content=question),
            AIMessage(content=answer["output"]),
        ]
    )
    return {"human_message": question, "bot_response": answer["output"]}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """this api endpoint is for uploading filesin knowledgebase
    takes a file that will be uploaded to knowledgebase
    returns: a dictionary containing information if uploaded successfully
    or any error occured
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, file.filename)
            with open(path, "wb") as f:
                # shutil.copyfileobj(file.file, file)
                f.write(file.file.read())
            file_load = load_file(path)
            if not file_load:
                raise Exception('Error: Could not load file.')
        return {"filename": f"{file.filename} uploaded successfully."}
    except Exception as e:
        return {"message": e.args}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
