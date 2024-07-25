FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip setuptools wheel
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
