FROM python

RUN pip install flask pymongo

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development
