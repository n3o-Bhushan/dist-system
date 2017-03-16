FROM python:2.7
ADD . /cod 
WORKDIR /cod/
RUN pip install -r requirements.txt

EXPOSE 8002
ENTRYPOINT ["python"]
CMD ["DB_shard2.py"]
