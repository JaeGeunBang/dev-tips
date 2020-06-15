### Kafka consumer group 삭제

<hr>

Kafka Consumer Group 삭제는 여러 방법이 있다.

- Zookeeper-shell에 접속 후 제거
- kafka-consumer-groups.sh 을 통한 제거



그러나 위 방법들은 Kafka 0.9.0 이하 버전에서 사용하는 방법이다. 이후 버전(0.10.0)부터는 메시지와 partition offset 정보 등 kafka broker가 관리한다.

- kafka broker가 모두 관리하기 때문에 쉽게 관리가 가능하며 consumer는 kafka, zookeeper 각각들과 통신하지 않아도 된다.



실제 kafka-consumer-groups.sh에 bootstrap-server 를 통해 delete를 하면 아래 메시지를 볼 수 있다.

```
Note that there's no need to delete group metadata for the new consumer as the group is deleted when the last committed offset for that group expires.
```

즉, 마지막 commit 시점과 만료 시점(디폴트 7일)을 바탕으로 consumer group이 자동으로 삭제가 되므로, 사용자가 수동으로 삭제할 필요가 없어보인다.



`offsets.retention.minutes`와 `offsets.retention.check.interval.ms` 옵션을 조정함으로써 consumer group 삭제 시기를 조절할 수 있다.



참고

https://stackoverflow.com/questions/40146921/how-to-list-all-available-kafka-brokers-in-a-cluster

https://stackoverflow.com/questions/29243896/removing-a-kafka-consumer-group-in-zookeeper

https://stackoverflow.com/questions/45515994/how-to-manage-expiration-of-kafka-groups