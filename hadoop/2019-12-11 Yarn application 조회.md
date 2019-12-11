### Yarn application 조회

<hr>
Yarn에서 실행된 application은 web ui에서 확인할 수 있다.

- submitted, accpeted, running, finished, failed, killed 등

현재 Spark Streaming, Batch Job을 수행중이며, 이들 중 동작이 실패한 App에 대해 모니터링을 진행하고자 한다.



`yarn` 스크립트를 통해 단순히 application을 조회할 수 있지만, 특정 시간 때의 app을 조회한다던지 등과 같은 조건은 넣을 수 없다.

- 실제 yarn 스크립트를 통해 application id나 appTypes, appStates와 같은 간단한 것들만 조회할 수 있다.



그래서 Resouce manager API를 통해 더 디테일한 조건을 바탕으로 app을 조회할 수 있다.

```shell
curl '<Resource Manager URL:Port>/ws/v1/cluster/apps?startedTimeBegin=...&applicationTypes=...&finalStatus=...'
```

- startedTimeBegin: app의 시작 시간을 지정할 수 있다.
- finishedTimeBegin: app의 끝 시간을 지정할 수 있다.
- applicationTypes: app의 type을 지정할 수 있다.
- finalStatus: app의 상태를 지정할 수 있다.

이 외에도 다양한 파라미터들이 있다.



**1시간 단위로 failed한 app 조회**





### 참고

https://hadoop.apache.org/docs/r2.7.1/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Applications_API