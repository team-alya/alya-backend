FROM python:3.11.5
EXPOSE 8000
WORKDIR /alyabackend
COPY requirements.txt /alyabackend
RUN pip3 install -r requirements.txt --no-cache-dir --timeout=1000
COPY . /alyabackend/ 
RUN chmod +x start.sh
RUN useradd arvolaskuri
RUN chown -R arvolaskuri:arvolaskuri /alyabackend/
USER arvolaskuri:arvolaskuri 
ENTRYPOINT ["/alyabackend/start.sh"] 