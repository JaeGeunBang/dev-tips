### Kafka Java Client Consumer 성능

<hr>

카프카 Consumer 할 때, producing 속도보다 Consuming 속도를 더 빠르게 하고 싶을 때. 

```java
props.put("auto.commit.interval.ms", "1000"); 
props.put("auto.offset.reset", "latest"); 
props.put("fetch.min.bytes", "10"); 
props.put("max.partition.fetch.bytes", "10485760"); 
props.put("fetch.max.bytes", "104857600"); 
props.put("max.poll.records", "10000") ; 
```



auto.offset.reset: latest 

- 마지막 offset 부터 읽을 것. 만약 기존에 group.id가 있다면 마지막으로 읽었던 offset부터  



fetch.min.bytes 

- 최소 fetch 할 바이트 



max.partition.fetch.bytes 

- 파티션 별 최대 fetch 할 바이트 

- 예를 들어 초당 1M 바이트 데이터가 producing 되고 있으며, 파티션이 10개라면 파티션 별 최소 100KB는 읽을 수 있어야 함. 
- 즉, 최소 100KB는 설정해야 밀리지 않고 consuming 할 것. 



fetch.max.bytes 

- 최대 fetch 할 바이트 
- 모든 파티션을 다 합쳐서 계산함. 위 상황에서 파티션이 10개라면 최소 1MB는 읽을 수 있어야 함. 
- 즉, 최소 1MB는 설정해야함. 



max.poll.records 

- 최대 읽을 레코드 수 
- 기본 값은 500이라, 최대 500개 밖에 읽지 않는다. 그렇기 때문에 초당 생성되는 메시지 수를 보고 설정해줄 것. 