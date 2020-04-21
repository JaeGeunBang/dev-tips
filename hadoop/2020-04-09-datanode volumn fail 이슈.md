### datanode volumn fail 이슈

<hr>


Hadoop Datanode의 disk가 이상이 생겨 교체 작업을 진행했으며, 정상적으로 교체된것이 확인되었지만 실제 아래와 같은 이슈가 발생했다.

```
Too many failed volumns - current valid volumns: 8, volumes configured: 9, volumes failed: 1
```

실제 hdfs-site.xml에 `dfs.datanode.data.dir` 옵션에 9개 디스크 경로가 comma 단위로 씌어져 있다.

그리고, 현재 서버에 디스크 수는 9개가 꽂혀 있는데 (`df -h` 확인), 8개 밖에 사용을 못한다는 이슈인것으로 보인다.



해당 이슈는 해당 디스크와 마운트된 경로의 권한 문제로 발생했다.

즉, `root 계정의 디렉토리 소유`로 되어있었고, datanode가 해당 마운트된 경로를 접근을 할 수 없어 발생하는 이슈였고, 이는 권한과 소유자를 바꿔서 해결했다.

