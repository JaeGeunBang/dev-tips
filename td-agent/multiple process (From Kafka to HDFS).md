##  multiple processor (From Kafka to HDFS)



Fluentd는 기본 1 CPU Core를 사용하도록 설정되어있다. 그렇기 때문에, Kafka에서 수많은 Topic들을 Consumer 할 땐 Multi Process 기능을 사용하는 것이 좋다.



Kafka plugin

https://github.com/fluent/fluent-plugin-kafka



HDFS plugin (webhdfs)

https://docs.fluentd.org/output/webhdfs



**worker 지정 방법**

```
<system>
  workers 4
</system>
```

위와 선언 후 Fluentd를 시작하면, 알아서 4개의 CPU Core가 자동으로 동작한다.



**worker 수동 사용**

```
<worker 0>
  <source> ... </source>
  <match> ... </match>
</worker>

<worker 1>
  <source> ... </source>
  <match> ... </match>
</worker>
```

위 방법처럼 각 CPU Core 마다 작업을 수동으로 할당 하는 방법도 있다. 

Kafka에서 로그를 읽어 HDFS에 쓸 때는 multi process를 수동으로 해야한다.



**HDFS에 저장**

기본적으로 Fluentd에서 HDFS에 데이터를 쓸 때 append 방식으로 쓴다. 참고로 append 방식은 하나의 HDFS File을 하나의 Client만 접근이 가능하다. 



만약 여러 Fluentd 서버를 운영하여 HDFS에 로그를 Write 한다고 했을 때, 각 Fluentd는 서로 다른 Topic을 Consuming 하여 처리해야 한다.

- 즉, 여러 Fluentd 서버가 중복 Topic을 처리하지 않도록 한다. (에러가 발생함)



만약 Fluentd 1번, 2번 서버가 있고, Topic 6개를 처리한다고 했을 때,

**Fluentd 1 서버**

- Topic 1,2,3번을 consuming 후 HDFS에 write
- worker는 각 topic 별로 하나씩 지정 (로그 양에 맞춰 1개 worker에 여러 topic 처리도 가능)



**Fluentd 2 서버**

- Topic 4,5,6번을 consuming 후 HDFS write
- worker는 각 topic 별로 하나씩 지정 (로그 양에 맞춰 1개 worker에 여러 topic 처리도 가능)



만약 로그가 너무 많아서 이를 여러 fluentd 서버로 처리하고 싶다면, HDFS file 이름에 ${hostname} 을 추가해 처리해야 한다.





