# Spark DropDuplicate



Spark에서 중복된 값을 제거하기 위해 dropDuplicate를 수행해야 한다.

```scala
df
  .dropDuplicate("A", "B", "C")
```

디폴트로 first row를 남기고 나머지를 삭제한다. 



허나 row 중 특정 수치가 큰 값만 남기고 싶을 때도 있을텐데, 이럴땐 agg, max통해 쉽게 제거할 수 있다.

```scala
df
  .groupBy("A","B","C")
  .agg(max("count"))
  .select(
  $"A",
  $"B",
  $"C",
  $"max(count)".as("count)",
  )
```

또한, Streaming 상황에선 제일 늦게 유입된 데이터를 남기고 싶을 때가 있다.

이럴땐 `current_timestamp()`를 통해 유입된 시간을 추가로 기록하고 위 agg, max를 통해 제거한다.

