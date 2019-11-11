##  WebHDFS connection error_2



전에 발생한 이슈처럼 똑같은 아래와 같은 이슈가 발생했다.

>  failed to flush the buffer. retry_time=??, error_class=WebHDFS::ServerError error="Failed to connect to host hostname, Broken pipe - sendfile



종종 아래와 같은 이슈도 발생했다.

> webhdfs unexpected error error_class=TypeError error=no implicit conversion of nill into integer



전에 문제처럼 로그 유입양이 많아 worker를 늘려 발생하는 문제는 아닌것으로 보인다.

이것저것 만져보다 WebHDFS에 consumer_group 설정에 문제가 있는것으로 보인다.



현재 Fluentd는 멀티 process를 통해 여러 topic을 consuming 후 HDFS에 저장하고 있다.

그러나 Kafka manager에서 하나의 consumer_group을 통해 모든 Topic을 보고 싶어, 하나의 consumer_group 으로 설정했을 때 위와 같은 이슈가 발생했다.

```
<source>
  @type kafka_group
  consumer_group fluentd
  topic topic_1
  add_prefix topic_1
</source>

<source>
  @type kafka_group
  consumer_group fluentd
  topic topic_2
  add_prefix topic_2
</source>
```

topic 1,2를 consuming 하기 위해 consumer_group을 모두 fluentd로 설정했었다.



결론적으로 서로 다른 Topic들은 각각의 consumer_group을 설정했을 때 위 에러가 더이상 발생하지 않았다.

며칠 모니터링 해본 결과 이상 없이 동작하는 것을 확인했다.

```
<source>
  @type kafka_group
  consumer_group fluentd_topic_1 // group명 변경.
  topic topic_1
  add_prefix topic_1
</source>

<source>
  @type kafka_group
  consumer_group fluentd_topic_2
  topic topic_2
  add_prefix topic_2
</source>
```

