FROM python:3.10-alpine3.20

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD ["python", "./generator.py", "-u", "admin", "-p", "admin"]