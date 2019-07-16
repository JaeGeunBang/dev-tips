### docker 기본

<hr>
Java + Maven 으로 개발한 어플리케이션을 컨테이너에서 동작시키고자 한다.

- docker 설치 필요
- dockerfile 작성
- privaty repository에 image 업로드



#### 1. window 10에서 docker 설치

- 링크: https://docs.docker.com/docker-for-windows/
- 설치 후 window 내 가상화 기술이 사용가능한 상태여야 한다.
  - BIOS에 들어가 가상화 기술 enabled
  - 제어판 - 프로그램 - Windows 기능 켜기/끄기 에서 `Hyper-V` 를 체크한다.
  - 작업 관리자 - 성능 - CPU에 가상화가 `사용`으로 되어있는지 확인
- cmd에서 docker --version을 통해 설치 여부를 확인할 수 있다.



> 허나 docker를 실행해보면 아래 에러가 발생한다.
>
> java.util.concurrent.ExecutionException: com.spotify.docker.client.shaded.javax.ws.rs.ProcessingException: org.apache.http.conn.HttpHostConnectException: Connect to localhost:2375 [localhost/127.0.0.1, localhost/0:0:0:0:0:0:0:1] failed: Connection refused: connect



이는 docker Setting - General에 Expose daemon on tcp://local:2375 without TLS를 체크해준다.



#### 2. Dockerfile 작성

```dockerfile
FROM maven:3.6.1-jdk-8 AS build
COPY src /usr/src/app/src
COPY pom.xml /usr/src/app
RUN mvn -f /usr/src/app/pom.xml clean compile assembly:single

FROM openjdk:8-jdk-alpine
COPY --from=build /usr/src/app/target/monitoring* /usr/app/app.jar
ENTRYPOINT ["java", "-jar", "/usr/app/app.jar"]
```

dockerfile을 작성 후 `docker build -t test`를 통해 image를 생성한다.

생성된 이미지는 `docker images`를 통해 확인할 수 있고, `docker run --rm -it test:latest`를 통해 실행할 수 있다.



#### 3. privaty repository에 image 업로드

```
# 로그인
> docker login <private repository>

# pull
> docker pull private-repository.com/myimage:latest

# tag & push
> docker tag <image id> private-repository.com/myimage:latest
> docker push private-repository.com/myimage:latest
```



