import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("")
async def read_answer(user_id: str, pdf_title: str, question: str):
    answer_filename = f"answers/{user_id}_{pdf_title}_{question[:20]}.txt"
    if os.path.exists(answer_filename):
        with open(answer_filename, "r") as f:
            answer = f.read()
        return JSONResponse(content={"answer": answer})
    else:
        return JSONResponse(content={"error": "Answer not found"}, status_code=404)
