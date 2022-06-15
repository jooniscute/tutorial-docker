FROM python:3.8-alpine

WORKDIR /app
#.dockerignore에서 copy에 제외할 것을 정의
COPY . /app

RUN pip install -r ./requirements.txt

# CMD ["python", "app.py"] 혹은
ENTRYPOINT ["python"]
CMD ["app.py"]

EXPOSE 5000
