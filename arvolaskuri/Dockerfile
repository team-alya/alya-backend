FROM python:3.11.5
EXPOSE 8000
WORKDIR /alyabackend
COPY requirements.txt /alyabackend
RUN pip3 install -r requirements.txt --no-cache-dir --timeout=1000
COPY . /alyabackend/ 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"] 