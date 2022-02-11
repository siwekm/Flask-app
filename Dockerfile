FROM python:3.7

RUN mkdir -p /var/rossum-flask-app

WORKDIR /var/rossum-flask-app

COPY ./ /var/rossum-flask-app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV BASIC_AUTH_USERNAME=myUser123
ENV BASIC_AUTH_PASSWORD=secretSecret

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]