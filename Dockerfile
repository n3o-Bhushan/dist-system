FROM python:2.7
MAINTAINER Your Name “yourid@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["exp_mgmt.py"]
