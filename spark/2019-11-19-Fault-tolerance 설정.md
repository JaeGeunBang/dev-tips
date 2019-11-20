# Fault-tolerance 설정

Spark Streaming App은 Long running app이기 때문에 장애에 대응이 필요하며, 이와 관련된 옵션은 아래와 같다.

```
--conf spark.yarn.maxAppAttempts=4 \
--conf spark.yarn.am.attemptFailuresValidityInterval=1h \
--conf spark.yarn.max.executor.failures={8 * num_executors} \
--conf spark.yarn.executor.failuresValidityInterval=1h \
--conf spark.task.maxFailures=8
```



**spark.yarn.maxAppAttempts=4**

- 어플리케이션 실패시 re-run 할 수 있는 최대 횟수
- Spark Streaming App 실행시 ERROR가 발생하면 `ATTEMPS --> RUNNING --> ATTEMPS --> RUNNING --> Fail` 순으로 동작하는 것을 볼 수 있는데, 이는 Default가 2이기 때문이다.



**spark.yarn.am.attempFailuresValidityInterval=1h**

- attemps 수를 초기화 하는데 걸리는 시간.
- 위 옵션은 총 attemps는 4번 수행하지만, 해당 count는 1시간마다 초기화 하겠다는 의미이다.
- 즉, 1시간 내로 attemps가 4번이 넘어간다면, 해당 app은 죽지만, 그렇지 않다면 app은 계속 살아남는다.



**spark.yarn.max.executor.failures={8 * num_executors}**

- executor의 최대 실패 수이며, 해당 수가 넘어가면 app은 죽는다.
- 위 옵션은 batch job에 적합하기 때문에, streaming job에서 사용하려면 아래 옵션도 같이 사용한다.
- `spark.yarn.executor.failuresValidityInterval=1h`
  - 위 옵션은 바로 위에서 소개한 `spark.yarn.am.attempFailuresValidityInterval`과 동일한 옵션이다.



**spark.task.maxFailures=8**

- task의 최대 실패 수이며, 해당 수가 넘어가면 app은 죽는다.
- 디폴트는 4이다.



### 참고

http://mkuthan.github.io/blog/2016/09/30/spark-streaming-on-yarn/