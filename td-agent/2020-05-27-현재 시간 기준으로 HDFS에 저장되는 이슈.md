##  현재 시간 기준으로 HDFS에 저장되는 이슈



**이슈**

Kafka의 로그를 Fluentd가 Consuming 하여 HDFS에 저장하는 상황에서, HDFS 경로는 아래와 같다.

- /logs/test/%y/%M/%d/%h

허나 Fluentd와 HDFS 사이에 이슈가 생겨 HDFS로 로그를 Write하지 못하는 상황이 발생한다. 만약, 해당 이슈를 일정 시간이 지난 후 처리하게 되면, `이전에 Write 하지 못했던 로그들이 현재 시간 기준으로 Write` 된다.

즉, `어제 로그가 현재 시간 기준으로 HDFS에 저장`되는 상황이 발생한다.



**해결**

어제 로그를 그대로 어제 시간대 HDFS에 저장하고 싶다면, Fluentd가 Kafka 로그를 가져올 때 Kafka 시간대로 변경해준다.

Kafka는 Topic에 로그가 유입되면, 유입된 시간을 기록해두기 때문에 이를 활용한다.

```.yaml
<source>
  @type kafka_group
  ...
  time_source <source for message timestamp (now|kafka|record)> :default => now
  ...

</source>
```

`time_source`를 설정하지 않으면 기본값은 `now` 인데 이는 현재 시간을 기반으로 한다. 이를 kafka로 바꾸어 `kafka에 유입된 시간대로 변경`할 수 있다.