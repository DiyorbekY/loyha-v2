FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
