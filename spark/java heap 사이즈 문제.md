
## java-heap 사이즈 문제


spark structured streaming app 실행중 아래와 같은 이슈가 발생한다.

```
ERROR YarnClusterScheduler: Lost executor 1 on test01.server.com: Container marked as failed: container_e26_1572403347906_0217_01_000002 on host: test01.server.com. Exit status: 143. Diagnostics: [2019-11-07 23:23:39.645]Container killed on request. Exit code is 143
[2019-11-07 23:23:39.645]Container exited with a non-zero exit code 143. 
[2019-11-07 23:23:39.647]Killed by external signal
```



streaming app은 batch 처리와 다르게 app이 계속 실행중이기 때문에 중간 상태 정보를 잘 정리해주는 것이 중요해보인다.

Spark Structred Streaming은 중간 상태 정보를 저장하며, 이를 watermark를 통해 예전 상태 정보는 제거할 수 있다. 해당 watermark가 제대로 동작하는지 확인이 필요하다.



**중복제거**

중복제거는 Dropduplicates()를 통해 진행한다. 허나, watermark를 할 때, 맨 마지막 파라미터에 시간 정보를 넣어주어야 제대로 watermark가 동작한다.

```scala
df
.withWatermark("timestamp", "1 minutes")
.dropDuplicates("A", "B", "C", "timestamp")
```



> 2019-11-20 기준
>
> 위와 같은 방식으론 중복 제거가 불가능하다. timestamp를 window로 변경해서 진행해야 하는데 window로 변경하면 제대로 상태정보가 제가 되지 않는다.

https://codeday.me/ko/qa/20190629/914476.html



1시간 단위 중복제거

```scala
df
  .withColumn("time", date_format(col("timestamp"), "yyyy-MM-dd HH:00:00")
    + expr("INTERVAL 1 hours")
  .select(
    $"time".cast("timestamp"),
    $"A", $"B", $"C"
  )
  .withWatermark("time", "1 hours")
  .dropDuplicates("queryForPageView", "time")
```

현재는 위와같이 코드를 변경해서 중복 제거를 하고 있다. 따로 time이라는 column을 만들고 해당 column을 통해 중복을 제거한다. 



1분 단위로 중복을 제거하고 싶다면, 2번째 라인을 아래와 같이 변경한다.

```scala
df
  .withColumn("time", date_format(col("timestamp"), "yyyy-MM-dd HH:mm:00") 
    + expr("INTERVAL 1 minutes")
```



**Join, Aggregation**

Join

```scala
df
.withWatermark("date1", "5 minutes")
.join(pageViewDistinctDF.withWatermark("date2", "10 minutes"), expr(
    """
    	query1 = query2 AND
    	date2 >= date1 AND
    	date2 <= date1 + interval 5 minute
    """))
```

위 `시간` 정보도 같이 넣어주어야 중간 상태 정보가 삭제된다.



Aggregation

```scala
df
.withWatermark("timestamp", "5 minutes")
.groupBy(
    window($"timestamp",
           "5 minuites",
           "1 minutes"),
    $"A", $"B")
.count()
```



이후 모니터링은 Spark UI에 SQL 창에서 특정 Job을 클릭하고 StateStoreSave에서 확인할 수 있다.

- number of total state rows: 현재 state에 저장된 정보의 row 수이며, 해당 수가 무한 증가 되지 않는지 확인
- memory used by state total: 현재 state 정보의 용량 확인
- total time to remove rows total: 기존 오래된 state 정보가 삭제되었는지 확인



Watermark를 통해 상태정보를 제거했는데도 똑같은 java heap 이슈가 발생한다면 executor, driver 메모리 양을 늘려야한다.



**다른 이슈**

<hr>

```
StreamingQueryException: Java heap space
```

이외에도 Spark App을 실행하자 마자 위와 같은 에러가 발생하는 경우도 있다.

이는 Kafka Consumer의 option 값을 설정한다. 즉, 할당 받은 자원 대비 Consumer의 option 값이 높다보니 발생하는 이슈이다.



Spark Streaming에서 사용하는 Kafka Consumer option들

- kafka.max.partition.fetch.bytes
- kafka.max.poll.records
- kafka.auto.commit.interval.ms
- kafka.startingOffsets
- failOnDataLost

각 옵션에 대한 설명은 아래 참조문서 참고



### 참고

스파크잡 튜닝 - https://blog.cloudera.com/how-to-tune-your-apache-spark-jobs-part-2/

스택오버플로우 - https://stackoverflow.com/questions/41002340/spark-on-yarn-container-exited-with-a-non-zero-exit-code-143 

스택오버플로우 - https://stackoverflow.com/questions/51118204/spark-java-heap-space-issue-executorlostfailure-container-exited-with-stat

네이버 D2 가비지 컬렉터 - https://d2.naver.com/helloworld/1329?source=post_page-----c18e39af942e----------------------

JVM Option - https://imp51.tistory.com/entry/G1-GC-Garbage-First-Garbage-Collector-Tuning

Why your spark Apps are Slow Or Failing, Part II: Data Swew and Garbage Collection - https://dzone.com/articles/why-your-spark-apps-are-slow-or-failing-part-ii-da

off-heap, on-heap - https://www.tutorialdocs.com/article/spark-memory-management.html

Spark Streaming + Kafka Ingegration Guide - https://spark.apache.org/docs/2.2.0/structured-streaming-kafka-integration.html