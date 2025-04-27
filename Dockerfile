FROM python:3.12-slim

# set working dir
WORKDIR /app

# copy to avoid reinstalling libs on code changes
COPY python/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY python/src /app/src

# make sure Python will look in /app/src
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# this will run main.py as a module
CMD ["python", "-m", "main"]
