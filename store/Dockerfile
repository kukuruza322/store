FROM python:3.8.6

EXPOSE 8000

WORKDIR /img

COPY . .

RUN pip install -r requirements.txt

CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
