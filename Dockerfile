FROM python:2

COPY . belch/
WORKDIR belch/
RUN pip install -r requirements.txt
