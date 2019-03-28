FROM python:3-alpine
WORKDIR /usr/src/app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app.py app.py
CMD [ "python", "app.py" ]