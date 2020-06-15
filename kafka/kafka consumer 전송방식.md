### Kafka consumer 전송방식 

<hr>
카프카의 메시지를 consumer 할 때 방식은 3가지가 있다.

- At-Most-Once(최대 한번), At-Least-Once(최소 한번), Exactly-Once(정확히 한번)



At-Most-Once (최대 한번)

- 메시지의 중복은 없으나 유실이 있을 수 있음.
- Kafka Consumer의 default.

```
enable.auto.commit = true
auto.commit.interval.ms은 낮게 설정
consumer.commitSync()는 consumer에서 호출하지 않음. (특정 interval 마다 자동으로 commit 하게 둠)
```



At-Least-Once (최소 한번)

- 메시지의 중복은 발생할 수 있으나 유실이 없다.

```
enable.auto.commit = false
consumer.commitSync()는 consumer에서 호출함.
```

or

```
enable.auto.commit = true
auto.commit.interval.ms은 높게 설정
consumer.commitSync()는 consumer에서 호출함.
```



Exactly-Once (정확히 한번)

- 정확히 한번 전송 (중복 발생 X, 유실 X)
- Subscribe, Assign 방식이 있음. 자세한 내용은 아래 내용 참고



참고

https://dzone.com/articles/kafka-clients-at-most-once-at-least-once-exactly-o