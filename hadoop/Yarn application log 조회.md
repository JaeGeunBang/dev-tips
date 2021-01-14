### Yarn application 조회

<hr>



Yarn에서 실행된 application은 web ui에서 확인할 수 있다.


- submitted, accpeted, running, finished, failed, killed 등

현재 Spark Streaming, Batch Job을 수행중이며, 이들 중 동작이 실패한 App에 대해 모니터링을 진행하고자 한다.



## API를 통한 Application 상태 조회

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



**1시간 사이 failed한 app의 name만 조회**

check_yarn_failed_app.sh

```bash
curTime=$(date +"%s")
curTimeMinusHour=`expr $curTime - 3600`
curTimeMinusHour000="$curTimeMinusHour"000

curl -s 'url:8088/ws/v1/cluster/apps?startedTimeBegin='$curTimeMinusHour000'&finalStatus=FAILED' | python -m json.tool | grep application_ | grep -v trackingUrl | awk '{print $2}'
```



## Yarn 명령을 통한 log 조회

- 아래 명령을 통해 특정 Application Id의 log를 조회할 수 있다.

```
# 일반 조회
yarn logs -applicationId <application Id>

# 에러 로그만 확인
yarn logs -applicationId <application Id> -log_files stderr

# application에서 사용하는 container 전체출력
yarn logs -applicationId <application_id> -show_application_log_info 

# 위에 container정보에서 특정 container에 대한 로그 확인
yarn logs -applicationId <application_id> -containerId <container_id>
```



- 해당 log 파일은 아래 hdfs 경로에 저장된다. 

**yarn-site.xml**

```
...
  <property>
      <name>yarn.log-aggregation-enable</name>
      <value>true</value>
  </property>
  <property>
     <name>yarn.nodemanager.remote-app-log-dir</name>
     <value>/app-logs</value>
  </property>
  <property>
      <name>yarn.nodemanager.remote-app-log-dir-suffix</name>
      <value>logs</value>
  </property>
...
```

- /app-logs 경로 + app을 실행시킨 user name + suffix (logs) 정보로 경로가 결정된다.

- ex)
  - username: `jgb710`
  - 최종 application 경로
    - `/app-logs/jgb710/logs/<application Id>`



### 참고

https://hadoop.apache.org/docs/r2.7.1/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Applications_API