FROM python:3.7-slim-stretch

COPY requirements.txt .
COPY app app/

RUN pip install --upgrade -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app/server.py"]