FROM python:3.10-alpine AS builder

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.10-alpine
WORKDIR /bot

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /bot

WORKDIR /bot

CMD ["python3", "bot.py"]
