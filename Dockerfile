FROM python:3.7-slim-stretch

COPY requirements.txt .
COPY news_dataset.tar.gz .
COPY app app/

RUN tar -xzf news_dataset.tar.gz -C app && \ 
    rm news_dataset.tar.gz
    
RUN pip install --upgrade -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app/server.py"]