### topic offset 초기화

<hr>

마지막 offset으로 초기화 하는 방법

```
kafka-consumer-groups.sh --bootstrap-server <bootstrap-server> --group <group> --topic <topic> --reset-offsets --to-latest --execute
```



첫 offset으로 초기화 하는 방법

```
kafka-consumer-groups.sh --bootstrap-server <bootstrap-server> --group <group> --topic <topic> --reset-offsets --to-earliest --execute
```