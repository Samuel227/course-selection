FROM python:3.7
ADD . /enrollment
WORKDIR /enrollment
RUN pip install -r requirements.txt