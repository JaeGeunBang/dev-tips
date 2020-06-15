### hdfs balancer 이슈

<hr>


balancer를 아래 옵션과 함께 실행했을시,

```
> hdfs balancer -include node1,node2,node3,node4,node5 -source node1,node2 -threshold 5
```

balancer를 수행할 노드는 node[1-5] 이며, node[1-2]는 source node로 동작시키고자 하며, threshold는 5로 조정했다.

허나 아래 이슈가 발생한다.

```
Not able to receive block 1083404960 from /10.10.10.10:38809 because threads quota is exceeded.
```

thread 기본 할당량을 초과하여 발생하는 이슈로 보인다. 기본 default thread는 5개로 알고있는데, 이를 늘려주는 작업이 필요해 보인다.



아래와 같이 thread 관련 옵션을 추가로 할당해준다.

```
hdfs balancer 
  -Ddfs.balancer.movedWinWidth=5400000 
  -Ddfs.balancer.moverThreads=1000 
  -Ddfs.balancer.dispatcherThreads=200 
  -Ddfs.datanode.balance.bandwidthPerSec=100000000 
  -Ddfs.balancer.max-size-to-move=10737418240 
  -threshold 20
```

간혹 실패 메시지가 뜨긴 하지만 정상적으로 동작하는 것을 확인했다.



balancer가 실패 후 다시 실행하기 위해 기존 생성된 .pid를 지운다. pid는 hdfs 경로 `/system/balancer.id` 에 저장된다.



### 참고

https://community.cloudera.com/t5/Support-Questions/Help-with-exception-from-HDFS-balancer/td-p/160081