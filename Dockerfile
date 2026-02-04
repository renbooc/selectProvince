FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt -q

COPY . .

ENV PORT=7860
EXPOSE 7860

CMD ["python", "app.py"]
