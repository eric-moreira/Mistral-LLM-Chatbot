FROM python:3.14-rc-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000
ENV FLASK_APP=smol.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV MONGO_URI=mongodb://mongo:27017/chatbot_db

CMD ["flask", "run"]
