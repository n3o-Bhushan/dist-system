FROM python:2.7
ADD . /cod 
WORKDIR /cod/
RUN pip install -r requirements.txt

EXPOSE 5003
ENTRYPOINT ["python"]
CMD ["DB_shard3.py"]
