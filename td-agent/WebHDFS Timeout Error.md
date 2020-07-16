##  WebHDFS Read Timeout Error



간혈적으로 web-hdfs 사용 도중 아래와 같은 이슈가 발생한다.

>  2020-07-16 02:28:04 +0900 [warn]: #1 failed to flush the buffer. retry_time=0 next_retry_seconds=2020-07-16 02:28:05 +0900 chunk="5aa7e341744b96fbe48ae8d47118ec90" error_class=WebHDFS::ServerError error="Failed to connect to host test.host.com:50075, Net::ReadTimeout"



fluentd에 Read Timeout 에러가 발생하는데, 금방 복구가 되곤 한다. 허나 간혹 Fluentd가 web-hdfs로 데이터를 전송하지 않은 이슈가 발생하는 경우가 있다.

이때는 fluentd를 재시작을 해도 td-agent process가 정상적으로 stop되지 않아 강제로 kill 하는 경우가 종종 발생한다.



일단 web-hdfs의 Read Timeout 이슈가 발생하지 않도록 아래와 같이 open_timeout, read_timeout 값을 높여보았다.

```
open_timeout 180 # default 30
read_timeout 180 # default 60
```

공식 문서에서는 `For high load cluster nodes, you can specify timeouts for HTTP requests.` 라고 적혀있어, 위 에러가 발생한 시간 때에 잠깐 Cluster가 고부하가 발생한것으로 예측된다.

