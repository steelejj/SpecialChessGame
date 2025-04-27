FROM python:3.12-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r python/requirements.txt

ENV PYTHONPATH="/app/python/src:${PYTHONPATH}"

CMD ["python", "-m", "main"]
