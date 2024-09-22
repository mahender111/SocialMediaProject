FROM python:3.11 

ENV PYTHONUNBUFFERED=1

WORKDIR /socialmediaproject

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /socialmediaproject

EXPOSE 8000

CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]

