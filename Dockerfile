
FROM python:3

WORKDIR /usr/src/app

ENV APP_NAME infopankki

COPY . .

RUN pip install --no-cache-dir -r deploy/requirements.txt

CMD deploy/server.sh
