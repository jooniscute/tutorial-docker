FROM python:3.8-alpine

RUN pip install flask

WORKDIR /app
#.dockerignore에서 copy에 제외할 것을 정의
COPY . /app

# CMD ["python", "app.py"] 혹은
ENTRYPOINT ["python"]
CMD ["app.py"]

EXPOSE 5000
