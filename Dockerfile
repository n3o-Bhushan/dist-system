FROM python:2.7
MAINTAINER Your Name “Bhushan.deshmukh2012@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["assignment1.py"]