import os
from fastapi import File, UploadFile

def save_pdf_answer(user_id: str, pdf_path: str, answer: str, pdf: UploadFile = File(None), time: str = None) -> bool:
    try:
        answer_filename = f"answers/pdfs/{os.path.basename(pdf_path) if pdf else 'no_pdf'}_{time}.txt"
        os.makedirs(os.path.dirname(answer_filename), exist_ok=True)
        with open(answer_filename, "w") as f:
            f.write(answer)
        return True
    except Exception as e:
        print(e)   
        return False
    
    
def save_none_pdf_answer(user_id: str, answer: str, pdf: UploadFile = File(None), time: str = None) -> bool:
    try:
        answer_filename = f"answers/nonepdfs/{user_id}_none_pdf_{time}.txt"
        os.makedirs(os.path.dirname(answer_filename), exist_ok=True)
        with open(answer_filename, "w") as f:
            f.write(answer)
        return True
    except Exception as e:
        print(e)   
        return False