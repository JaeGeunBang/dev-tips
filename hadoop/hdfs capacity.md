### hdfs capacity

<hr>


Hadoop 2.0에서 DataNode 정보를 HDFS WEB UI에서 볼 수 있다.

![image](https://user-images.githubusercontent.com/22383120/87365978-8980ed80-c5b2-11ea-8b4f-a29d11e661f1.png)

위 Web UI에서 Capacity가 `91.54GB`로 나와있지만, 실제 서버에 할당된 Disk의 전체 Capacity는 `50GB` 정도 밖에 되지 않는다.

Web UI에서 추출되는 Capacity는 `hdfs-site.xml`에 `dfs.datanode.data.dir` 옵션에 설정된 디스크 정보들을 바탕으로 계산이 된다.

- 현재 서버의 각 Disk 크기가 다르다. (ex. /hdfs1 - 10GB, /hdfs2 - 20GB)
- 그러다보니 둘의 밸런스를 맞추기 위해 `dfs.datanode.data.dir`을 /hdfs1, /hdfs2/1, /hdfs2/2 와 같이 설정한 것이 문제였다.
- 위 예제에서 총 `30GB` 였던 Capacity가 위와같이 설정되면 `50GB`로 Web UI에서 나타나게 된다.



이를 해결하기 위해서는 `dfs.datanode.data.dir`을 /hdfs1, /hdfs2와 같이 설정해야 하지만, Disk 밸런스가 맞지 않게 된다.

- 이는 용량이 작은 Disk가 먼저 100%가 되며, 이럴경우 Hadoop 운영상 문제는 없지만 용량이 100%가 된 Disk는 더 이상 최신 로그가 Write 되지 않아 Read 성능에 영향을 끼칠 수 있다.

  

결론적으로.. 정확한 모니터링을 위해서 Web UI를 보지말고, `hdfs dfsadmin -report` 를 통해 계산된 `DFS Used`를 볼것.

- Hadoop 3.0부터는 DataNode의 Disk Balancer가 가능하니 위와 같이 Disk Balancer 문제로 신경쓰지 않아도  될것으로 보인다.