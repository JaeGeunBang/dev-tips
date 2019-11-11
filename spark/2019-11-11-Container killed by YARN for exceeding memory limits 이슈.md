# Container killed by YARN for exceeding memory limits


spark structured streaming app 실행중 아래와 같은 이슈가 발생한다.

```
ERROR YarnClusterScheduler: Lost executor 2 on test01.server.com: Container killed by YARN for exceeding memory limits. 9.1 GB of 9 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.
```







### 참고

https://aws.amazon.com/ko/premiumsupport/knowledge-center/emr-spark-yarn-memory-limit/