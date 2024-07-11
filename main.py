# main.py
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import openai
from openai import OpenAI


load_dotenv()

app = FastAPI()

OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL = "gpt-3.5-turbo"

client = OpenAI(
    api_key = OPENAI_KEY
)
# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload/")
async def upload_file(user_id: str = Form(...), pdf: UploadFile = File(None), question: str = Form(...)):
    if pdf:
        pdf_path = f"pdfs/{user_id}_{pdf.filename}"
        with open(pdf_path, "wb") as buffer:
            buffer.write(await pdf.read())
        
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
        faiss_index = FAISS.from_documents(pages, embeddings)
        docs = faiss_index.similarity_search(question, k=4)
        
        # Prepare the context from the documents
        context = "\n\n".join([doc.page_content for doc in docs])

        # Create the ChatGPT prompt
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

        # Query the OpenAI API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # answer = response['choices'][0]['message']['content']
        answer = response.choices[0].message.content
    else:
        pdf_path = "None"
        # 일반 ChatGPT 사용
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        # answer = response['choices'][0]['message']['content']
        answer = response.choices[0].message.content

    # 답변 저장
    answer_filename = f"answers/{user_id}_{os.path.basename(pdf_path)}_{question[:20]}.txt"
    os.makedirs(os.path.dirname(answer_filename), exist_ok=True)
    with open(answer_filename, "w") as f:
        f.write(answer)

    return JSONResponse(content={"answer": answer})

@app.get("/read/")
async def read_answer(user_id: str, pdf_title: str, question: str):
    answer_filename = f"answers/{user_id}_{pdf_title}_{question[:20]}.txt"
    if os.path.exists(answer_filename):
        with open(answer_filename, "r") as f:
            answer = f.read()
        return JSONResponse(content={"answer": answer})
    else:
        return JSONResponse(content={"error": "Answer not found"}, status_code=404)

# HTML 파일 서빙
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
