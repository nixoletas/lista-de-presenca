FROM python:3-alpine3.15
ENV https_proxy=http://10.56.19.168:3128
ENV http_proxy=http://10.56.19.168:3128
ENV use_proxy=on
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]