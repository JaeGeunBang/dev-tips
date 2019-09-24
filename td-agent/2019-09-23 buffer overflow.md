##  Buffer overflow

td-agent 로그에 아래 이슈가 발생했다.

>  buffer overflow - buffer space has too many data

해당 이슈는 td-agent buffer에 쌓이는 로그 양이 td-agent가 처리 속도보다 더 빠른 것을 의미한다.



buffer_chuck_limit, buffer_queue_limit 등을 높이는 것은 근본적인 해결책이 되지 않는 것으로 보인다.

flushing parameter에 flush_thread_count default가 1로 되어있는데 이를 높이거나 multiple process를 사용해서 해결 할 수 있었다.



**해결책**

1. buffer flushing parameter에 있는 flush_tread_count 수를 높여서 처리한다.
   - 허나 td-agent가 HDFS에 저장하는 경우라면, HDFS에 file은 하나의 client만 접근이 가능하기 때문에 이를 구분해 주어야 한다.
   - 이를 위해 workers를 사용하며 각 worker마다 WebHdfs를 사용해 file 이름을 구분해준다.
   - worker 수는 kafka topic의 partition과 1:1로 매칭해주는 것이 제일 안전하다. 만약 그렇게 해도 위와 같은 문제가 발생하면, kafka topic의 partition 수를 늘려준다.

```
<system>
  workers N
</system>
```

2. buffer는 memory를 사용한다.
   - buffer를 file로 사용할 경우, worker 수에 맞게 disk가 mounted 되어야 병렬로 실행될 수 있는것으로 보인다.
   - 그렇기 때문에 buffer는 memory로 설정후 사용한다.



며칠 모니터링 해본 결과 이상 없이 동작하는 것을 확인했다.



### 참고

https://docs.fluentd.org/configuration/buffer-section