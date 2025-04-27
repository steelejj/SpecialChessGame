FROM python:3.12-slim

# set working dir
WORKDIR /app

# copy only your source tree into /app/src
COPY python/src /app/src

# make sure Python will look in /app/src
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# this will run main.py as a module
CMD ["python", "-m", "main"]
