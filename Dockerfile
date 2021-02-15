FROM python:3.9-slim-buster

EXPOSE 80

WORKDIR /app

COPY ./Pipfile* ./

RUN echo ' ---> Install additional dependencies' && apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pip install pipenv && \
    rm -rf /var/lib/apt/lists/* && \
    #BUG https://github.com/pypa/pipenv/issues/1002
    ln -sf /usr/local/bin/python /bin/python && \
    pipenv install --python="/usr/local/bin/python" --dev --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y

COPY . .

CMD [ "python", "-m", "sanic", "server.app", "--host=0.0.0.0", "--port=80"]