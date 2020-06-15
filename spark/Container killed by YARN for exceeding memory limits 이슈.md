# Container killed by YARN for exceeding memory limits


spark structured streaming app 실행중 아래와 같은 이슈가 발생한다.

```
ERROR YarnClusterScheduler: Lost executor 2 on test01.server.com: Container killed by YARN for exceeding memory limits. 9.1 GB of 9 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.
```



Aggregation 할 때 발생했으며, 메모리가 초과되다 보니 Yarn이 Container를 Kill 하는것으로 보인다.

아래것들을 시도해보았다.

- 메모리 오버헤드 늘림
- 코어 수 줄임
- 파티션 수 늘림
- driver 및 executor 메모리 늘림



**메모리 오버헤드 늘림**

메모리 오버헤드는 executor 메모리의 10%, 384 중 높은 값으로 설정된다. 메모리 오버헤드는 조금씩 점직적으로 최대 25%까지 늘리는 것이 좋다.

또한, executor의 메모리 + executor의 메모리 오버헤드의 합이 yarn의 nodemanager가 container에 할당할 수 있는 최대 메모리를 넘지 않도록 해야한다.

```
--conf "spark.driver.memoryOverhead=2024"
--conf "spark.executor.memoryOverhead=2024"
```



**코어 수 줄임**

코어 수를 줄이면 그만큼 executor가 실행할 작업 수가 줄어들기 때문에 메모리 용량도 줄어든다. core 수보다 executor의 수를 늘려주는 것이 더 좋은 선택이다.

```
--conf "spark.driver.cores 1"
--conf "spark.executor.cores 1"
```



**파티션 수 늘림**

파티션 수가 작으면 작을 수록, 처리할 task의 수도 줄어든다. 보통 파티션 1개당 1개 task가 생성되므로, 파티션이 많을수록 많은 task가 생성된다.

그렇기 때문에, task 수가 줄면 해당 task가 처리할 양이 많아 aggregation 실행에서 더 많은 메모리 부담이 되기 때문에 파티션 수를 늘려주는게 좋다.



데이터를 Kafka에서 Consumer하는 경우라면, Kafka Topic의 Partition을 우선적으로 늘려준다.

이후 spark에서 `spark.default.parallelism` 프로퍼티를 통해 parallelism을 늘려주거나, dataframe.repartition() 을 통해 파티션 개수를 늘려주도록 한다.

```
df = df.repartition(100)
```

파티션 수는 Spark UI에서 Job에서 Task가 몇개 생성되었는지 보면 알 수 있다.



**driver 및 executor 메모리 늘림**

말그대로 driver, executor의 메모리를 더 늘려준다.

```
--conf "spark.driver.memory 8g"
--conf "spark.executor.memory 8g"
```



### 참고

https://aws.amazon.com/ko/premiumsupport/knowledge-center/emr-spark-yarn-memory-limit/

why your spark applications are slow or failing, part 1: memory management - https://dzone.com/articles/common-reasons-your-spark-applications-are-slow-or