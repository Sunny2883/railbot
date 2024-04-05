FROM python:3.11.7
WORKDIR /app
COPY requirment.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirment.txt
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
