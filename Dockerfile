# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
RUN apk add --no-cache gcc make build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["source", "./venv/bin/activate"]
CMD ["python", "bot.py"]
