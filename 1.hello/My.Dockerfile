FROM ubuntu

# 각 한줄이 한 레이어이므로 최대한 줄이는게 좋음
RUN apt update && \
    apt install nginx -y && \
    echo "Hello" > /hello.txt

#CMD로 실행해도 정상 동작됨
#CMD의 경우 명령어를 통해 인자값을 교체해서 실행 가능
#한개의 도커파일에는 한개씩만 (CMD, ENTRYPOINT)
ENTRYPOINT ["echo", "Hello, dockerfile~"]
