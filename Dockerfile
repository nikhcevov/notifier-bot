FROM python:3.9-alpine

WORKDIR /work
COPY . .

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --system --deploy

EXPOSE 8080

CMD exec python app.py
