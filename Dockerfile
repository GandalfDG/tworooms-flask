FROM python

RUN pip install flask pymongo flask-socketio

COPY ./tworooms ./tworooms 

ENV FLASK_APP=tworooms
ENV FLASK_ENV=development

EXPOSE 5000

CMD flask run --host=0.0.0.0
