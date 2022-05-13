FROM python:3.8-slim-buster

WORKDIR /usr/local/flask

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

# In case we want to create a different user to avoid the use of root
#RUN useradd -ms /bin/bash intern
#USER intern
#WORKDIR /home/intern


CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]