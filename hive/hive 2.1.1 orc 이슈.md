### Hive 2.1.1 Orc 이슈

<hr>


현재 Hive의 버전이 2.1.1을 사용하고 있다. 그리고 Hadoop 버전은 2->3으로 올리는 도중 아래와 같은 이슈가 발생했다.

```
 java.lang.RuntimeException: ORC split generation failed
```

현재 Hive Table은 Orc 기반의 Table이며, Hadoop이 RawData를 Orc 포맷으로 변형한 이후에 Hive Table로 ETL을 수행한다. 허나 Hadoop 버전을 올려서 수행했는데 기존에 동작하던 ETL 잡이 수행하지 않는다.



찾아본 결과, Hive 2.1.1 버전에서 발생하는 이슈인것 같다. `실제 높은 버전의 Hadoop에서 Orc Writer를 수행했을 때, 발생하는 이슈`로 보인다. 그리고, Hive 3.0로 테스트 했을 땐 정상적으로 동작한것으로 보아 Hive 버전을 올리는게 최선의 방법으로 보인다. 허나 Production 환경에서 바로 버전을 올리는건 꽤 껄끄러운 일이기 때문에...

https://issues.apache.org/jira/browse/HIVE-14483

https://stackoverflow.com/questions/45977647/hive-llap-orc-split-generation-failed



버전을 올리는 방법 말고 다른 방법으로 기존의 ETL 작업을 변경하였다.

- 기존 ETL
  - Hadoop (Raw) -> Hadoop (Orc) -> Hive (Orc Table)
- 수정된 ETL
  - Hadoop (Raw) -> Hive (Raw Table) -> Hive (Orc Table)

Hadoop에서 RawData를 Orc로 변환하는 것이 아닌, Hive에서 Raw Data를 Orc로 변환하는 방법으로 위 문제를 해결했다. Hive Raw Table은 임시 테이블로 사용하며, Orc Table로 데이터를 Load 했다면 그 즉시 Partition을 삭제하여 메타데이터를 관리했다.

