FROM python:3.8.6

EXPOSE 8000
WORKDIR /img

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./store /img
COPY ./app /img

CMD ["python", "manage.py", "runserver"]