FROM python

RUN pip install flask Flask-PyMongo

ENV FLASK_APP=tworooms
ENV FLASK_ENV=development

CMD bash
