# Docker 실습

## 계정
user1@15.164.96.255
SKT20220614

## 설치
`sudo apt install docker.io`

## 권한
`sudo user mod -aG docker $USER`

## 재실행
`newgrp docker`

## 도커 실행 환경 확인
`docker info`
(root dir: /var/lib/docker)
(예시) 도커 설정파일 생성 (-> docker 실행 시 먼저 돌아감. root dir 변경)
`sudo touch /etc/docker/daemon.json`
`sudo vi /etc/docker/daemon.json`
{
	“data-root”: “/data/docker_dir”
}

## 도커 테스트
`docker run hello-world`
`docker run docker/whalesay cowsay boo`
run: pull, create, execute
실행 시 초기엔 이미지가 없어서 docker-hub에서 가져옴

## 도커 이미지 리스트
`docker images`
`docker rmi $(docker ps -aq)`

## 도커 컨테이너 리스트
`docker ps -a` (종료된 것도 포함)
`docker ps` (실행 중인 것만)

## 도커 이미지 가져오기
`docker pull ubuntu:14.04`
`docker pull ubuntu:16.04`
`docker pull ubuntu:18.04`
각 도커마다 이미지 레이어가 다름~ (만드는 사람 마음)

## 도커 컨테이너 실행
`docker run ubuntu:14.04 sleep 3`
원하는 binary 실행 가능~
`docker run -it ubuntu:14.04 bash`
-it 추가 시 bash 실행하고 종료하는게 아니라 interactive 하게~
매번 실행할 때마다 새로운 container를 띄우게 됨

## 컨테이너 버전 정보 등 보기
`cat /etc/*-release`
14 / 16/ 18 버전 3개 각각 다른 터미널에서 띄우고 정보 확인해보기
`cd /lib/x86_64-linux-gnu/`
라이브러리 버전 등이 다 다름 -> 파일 시스템이 다름!
`uname -a`
kernel 정보 확인해보기 -> 모든 docker container는 host kernel을 share 한다 (VM과 다른 점)
cf) 우분투 버전 별 커널 버전이 각각 정해져 있음

## 컨테이너 지우기
`docker rm 컨테이너ID`
컨테이너ID 일부만 쳐도 지울 수 있음
실행 중인 건 지울 수 없음
이름으로도 지울 수 있으나 이름은 full로 쳐야함
한번에 지우려면?
`docker rm $(docker ps -aq)`
q: 컨테이너ID만 반환함

## 컨테이너 종료
`docker kill 컨테이너ID`
`docker rm -f $(docker ps -aq)`

## 웹서버 설치 (nginx)
`docker run nginx`
서버가 뜨지만, 격리가 되어 있어서 주소로 접속해도 아무것도 뜨지 않는다 -> 내부가 궁금하면?
`docker run -d nginx`
데몬으로 띄우기
`docker run -d -p 80:80 nginx`
컨테이너 밖에서 80으로 들어온 걸 컨테이너 안의 80으로 돌려줌
즉, 호스트의 80 포트를 컨테이너에 할당하는 것임

## 컨테이너 접속
`docker exec -it 컨테이너ID bash`
있는 컨테이너 안에 들어가서 확인해보기~
`curl localhost`

웹서버 구분을 위해 각각에 접속해서 
`vi /usr/share/nginx/html/index.html`

## 컨테이너에 VIM 설치..
`apt update`
`apt install vim`

## 로그 확인
`docker logs 컨테이너ID`
`docker logs -f 컨테이너ID`

## redis
`docker run -d -p 6379:6379 redis`

## mysql
`docker run -p 3306:3306 --name mysqldb -d mysql:5.7`
이름 지정해서 띄울 수 있음!
근데 위에 실행하자마자 죽음 (docker ps 로 확인해보기)
디버깅!
`docker logs mysqldb`
오류 확인 (비밀번호 없음)
`docker run -p 3306:3306 --name mysqldb -e MYSQL_ROOT_PASSWORD=wldls143 -d mysql:5.7`
이거 실행 전에 mysqldb 컨테이너를 지워주어야 함

DB를 띄워서 실행을 했다가, 컨테이너를 삭제한 경우에는 해당 컨테이너가 떴을 때 만든 데이터들이 다 사라지게 됨
그렇기 때문에 mysql 저장소를 host에 연결
`docker run -p 3306:3306 --name mysqldb -e MYSQL_ROOT_PASSWORD=wldls143 -v /home/user1/database:/var/lib/mysql -d mysql:5.7`
/var/lib/mysql에 생성되는 파일들이 host의 /data/database에 저장되게 됨

그치만 바인딩보다 볼륨 생성이 관리하기 용이함
`docker volume create mysql_volume`
`docker volume ls`
`docker run -p 3306:3306 --name mysqldb -e MYSQL_ROOT_PASSWORD=wldls143 -v mysql_volume:/var/lib/mysql -d mysql:5.7`
이때 mysql_volume의 경로: /var/lib/docker/volumes/mysql_volume

## 떠있는 컨테이너 살펴보기
`docker inspect mysqldb`

## 네트워크
`ifconfig -a` 로 확인
docker0 대역: 172.17.0.0 (`route -n`으로 확인)

`docker run -d -p8000:80 --name my-nginx1 nginx`
`docker run -d -p8001:80 --name my-nginx2 nginx`
`docker inspect my-nginx1 | grep "IPAddress"`
`apt update`
`apt install iputils-ping -y`
새로운 네트워크 생성
`docker network create --driver bridge --subnet 192.168.222.0/24 my-network`
`docker run -it --network=my-network ubuntu:16.04 bash`
`docker network ls`
`docker network prune` -> 쓰이지 않는 것 삭제 (`docker volume prune` 도 가능)

## 워드프레스 & DB 도커간 연동 실습
`docker volume create mysql_database`
`docker run -d -p 3306:3306 -v mysql_database:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysqldb mysql:5.7`
`docker run -d -p 8080:80 --link mysqldb:mydatabase -e WORDPRESS_DB_HOST=mydatabase -e WORDPRESS_DB_NAME=wp -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp wordpress`
link: 다른 컨테이너와 연결

## 컨테이너 이미지 저장
`docker run --name my-nginx -p 80:80 -d nginx`
`docker exec -it my-nginx bash`
`docker commit -m 'this is my-nginx image' my-nginx hello-nginx:1.0`
현재 돌고 있는 컨테이너를 나만의 이미지로 저장 (name: hello-nginx, tag: 1.0)
`docker history hello-nginx:1.0`
만들어진 과정을 볼 수 있다

## 이미지 만들기 실습 (1.hello)
Dockerfile 작성
`docker build . --tag myhello:1.0`
`docker build -f 파일명 . --tag myhello:1.0` (Dockerfile 이랑 이름 다를때)
실행해보기
`docker run myhello:1.0`
알파인으로 다시
`docker build -f ./Alpine.dockerfile . --tag myhello:1.1`
직접 만들기
`docker build -f ./My.Dockerfile . --tag myimage:2.0`
파일 줄인 후 (레이어 줄이기)
`docker build -f ./My.Dockerfile . --tag myimage:2.1`

## 실용적으로 만들기 (2.nginx)
실행했는데 죽어버리는 경우 -> 데몬 모드를 꺼야 함!
지우는 부분을 추가할 때, 기존 레이어 위에 쌓이면 용량이 줄어들 지 않는다.
그렇기 때문에 레이어를 통합하여야 함 (apt-get clean 부분)

## 실제 개발 (3.flask, 4.flask)
mkdir venv
cd venv
python3 -m venv flask
source flask/bin/activate
cd ~/tutorial-docker/3.flask/
pip install flask
python app.py

위 과정을 Dockerfile로!
`docker build . --tag myapp:1.0`
`docker run -p 80:5000 -d myapp:1.0`
`docker excec -it 컨테이너ID sh`
들어가서 확인해보면 /app/app.py 있음 (WORKDIR에 COPY를 통해 복사된 파일)
`docker kill 컨테이너ID`
4.flask에서 이어서 진행, 파일들 수정 후
`docker run --name my-flask1 -p 8000:5000 -e APP_COLOR=yellow -d myapp:2.0`
`docker run --name my-flask2 -p 8001:5000 -e APP_COLOR=orange -d myapp:2.0`
`docker run --name my-flask3 -p 8002:5000 -e APP_COLOR=cyan -d myapp:2.0`
호스트에 nginx 설치
`sudo apt install nginx -y`
`sudo vi /var/www/html/index.html`
nginx 설정
/etc/nginx/sites-available/default 에서 프록시 설정
location 등 설정파일 수정 후
`sudo systemctl restart nginx`

## 도커 이미지 푸쉬
`docker login`
`docker tag 로컬이미지이름:태그 repo계정/repo이름:태그`
`docker push repo계정/repo이름`
`docker tag 로컬이미지이름:태그 chlwnsrms5/repo이름:latest`

## docker-compose

