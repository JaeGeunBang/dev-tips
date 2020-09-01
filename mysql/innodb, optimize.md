## InnoDB, optimize



MySQL은 MyISAM, InnoDB와 다양한 스토리지 엔진을 제공한다.

https://blog.lael.be/post/150

위 블로그 글은 두 스토리지 엔진을 비교한 글이다.



각 Table의 스토리지 엔진은 `show table status` 명령을 통해 확인할 수 있다.



### Optimize

MySQL에서 DB에서 사용하는 스토리지 사이즈, 즉 테이블 사이즈를 줄이기 위해 Optimize를 사용한다.

- delete 로 데이터를 지우더라도, `실제 스토리지 사이즈는 줄어들지 않는다.` 아무래도 데이터를 실제 지우는 작업이 디스크 I/O 일어나는 비싼 연산이라 그런것으로 보임.

- 이럴때, `optimize` 명령을 통해 실제 스토리지 사이즈를 줄일 수 있다.

  

스토리지 엔진이 Inno DB라면 **내부적으로 ALTER TABLE문을 실행하여, MySQL 서버에 대해 테이블과 인덱스를 재생성**하도록 요청한다.

- `analyze 명령어`가 인덱스를 재생성하여 성능을 최적화하는 명령어인데, Optimize 과정에 포함되어 있음.
- analyze를 수행하면 read 락이 걸리기 때문에, 신중해야한다.



**사용 방법**

```
> optimize table <table name> ;
```



### 참고

http://blog.syszone.co.kr/3333