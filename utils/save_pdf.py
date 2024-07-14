from fastapi import UploadFile

async def save_pdf(pdf: UploadFile, user_id: str, time: str) -> str:
    try:
        pdf_path = f"pdfs/{user_id}_{pdf.filename}_{time}"
        with open(pdf_path, "wb") as buffer:
            buffer.write(await pdf.read())
        return pdf_path
    except Exception as e:
        print(e)
        return None
