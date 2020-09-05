FROM python

RUN pip install flask Flask-PyMongo

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development
