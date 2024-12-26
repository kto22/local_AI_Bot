FROM python:3.12-slim

WORKDIR /bot

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /bot

CMD ["python3", "bot.py"]
