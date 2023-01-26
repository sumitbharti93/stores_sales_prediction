FROM python:3.7 
RUN apt update -y && apt install awscli -y

WORKDIR /app 
COPY . /app
RUN pip install -r requirements.txt 
EXPOSE $PORT
CMD ["python3", "app.py"]