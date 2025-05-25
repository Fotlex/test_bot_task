FROM python:3.13

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "shop/tg_bot/main.py"]