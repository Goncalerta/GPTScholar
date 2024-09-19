# syntax=docker/dockerfile:1
FROM python:3.11.2-alpine3.17
WORKDIR /app/backend/
COPY . /app/backend/
RUN pip3 install -r requirements.txt
CMD ["python3", "-m" , "flask", "run", "--debug", "--host=0.0.0.0"]
