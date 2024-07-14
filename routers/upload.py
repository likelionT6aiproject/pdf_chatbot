from fastapi import File, UploadFile, Form, APIRouter
from fastapi.responses import JSONResponse
from utils.load_pdf import load_pdf
from utils.save_answer import save_pdf_answer, save_none_pdf_answer
from utils.gpt_config import get_answer
from dotenv import load_dotenv
from utils.save_pdf import save_pdf
from datetime import datetime

load_dotenv()

router = APIRouter()
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@router.post("")
async def upload_file(user_id: str = Form(...), pdf: UploadFile = File(None), question: str = Form(...)):
    pdf_path = await save_pdf(pdf, user_id, now)
    context = await load_pdf(pdf_path, question)
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    answer = get_answer(prompt)
    save_pdf_answer(user_id, pdf_path, answer, pdf, now)

    return JSONResponse(content={"answer": answer}) 


@router.post("/nonepdf")
async def upload_file(user_id: str = Form(...), pdf: UploadFile = File(None), question: str = Form(...)):
    prompt = f"Question: {question}\n\nAnswer:"
    answer = get_answer(prompt)
    save_none_pdf_answer(user_id, answer, pdf, now)

    return JSONResponse(content={"answer": answer})