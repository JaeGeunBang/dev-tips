##  WebHDFS connection error

td-agent 로그에 아래 이슈가 발생했다.

>  failed to flush the buffer. retry_time=??, error_class=WebHDFS::ServerError error="Failed to connect to host hostname, Broken pipe - sendfile

현재 td-agent가 HDFS로 로그를 저장하는데, HDFS에 연결할 수 없다는 이슈이다.

Kafka에서 로그를 consuming해 HDFS로 저장하고 있다. 또한, consuming 중인 로그 유입양이 많아 multiple worker로 td-agent를 수행하고 있으며, 각 worker 마다 1,2,3... 숫자를 붙여 HDFS에 저장 중이다.

```
worker 1 --> HDFS 경로 (/user/fluentd/test.log.1)
worker 2 --> HDFS 경로 (/user/fluentd/test.log.2)
worker 3 --> HDFS 경로 (/user/fluentd/test.log.3)
```



위 이슈가 새벽시간 때나 저녁 시간 때쯤 발생을 한걸로 보아 로그양이 많아서 발생한 이슈는 아닌 것으로 보인다. 주로 낮에 로그 유입 양이 많기 때문에



**해결책**

1. 하나의 서버에 여러 worker를 띄어서 HDFS에 저장하지 않고, 여러 서버에 사용해 처리한다. 그렇게 함으로써 위 이슈가 발생 하지 않았다.
2. 즉, 하나의 Topic에 유입되는 로그가 많으며 이를 td-agent를 통해 HDFS에 저장하고 싶을 때, worker를 늘리지 않고 서버를 늘리자.



며칠 모니터링 해본 결과 이상 없이 동작하는 것을 확인했다.



<hr>

추가로 아래 이슈가 발생할 수 있다.

>failed to communicate hdfs cluster, path: /logs/file.log.2020-01-28-01-03-35



특정 경로에 파일을 write 할 때 위와 같은 이슈가 추가로 발생한다.

hdfs 경로 `/logs/file.log.2020-01-28-01-03-35`에 file을 쓰지못하는 이슈이다.

- hdfs namenode의 master-standby node가 전환되면서 발생한 이슈로 보인다.

- 그렇기 때문에 fluentd는 이미 같은 경로에 파일이 있을 경우 file을 쓰지 못한다. (하나의 hdfs file엔 하나의 client만 접근할 수 있기 때문)



**해결책**

1. hdfs에 저장된 `/logs/file.log.2020-01-28-01-03-35` 파일의 이름을 바꾼다. (ex. `/logs/file.log.2020-01-28-01-03-35.tmp` )
   - 파일 이름을 바꾸면 새로 `/logs/file.log.2020-01-28-01-03-35` file이 생성되면서 정상 동작하는 것을 확인할 수 있다.
2. flush_interval을 조정한다. 만약 1분 단위로 file에 쓴다고 가정했을 때, flush_interval은 1m으로 조정하는게 좋다.
   - hdfs에 데이터를 쓸때는 append으로 쓰기 때문에, 하나의 HDFS File에 하나의 Client만 접근이 된다.
   - 그렇기 때문에, `1분에 1개의 file만 쓸수 있도록 조정`해야한다.
   - 만약 10초당 한번씩 flush 하고 싶다면, file 이름에 `%S`를 붙여야 한다.


