FROM python:3.6
COPY request.py nasa_request.txt /
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install requests
CMD python3 /request.py
