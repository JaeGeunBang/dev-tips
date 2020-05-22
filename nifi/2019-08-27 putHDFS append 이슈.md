### putHDFS - append 이슈

<hr>



putHDFS processor를 append 방식으로 write할 때 아래와 같은 이슈가 생긴다.


> Failed to APPEND_FILE ... because this file lease is currently owned by DFSClient_NONMAPREDUCE on ...



해당 이슈는 nifi 서버가 한대일때는 문제가 없지만, 여러대 일경우 문제가 생길 수 있다. 기본적으로 하나의 file에 append 할 때 하나의 client만 접근할 수 있다. 



**해결방법**

1. PutHDFS의 SCHEDULING에 execution을 Primary node로 바꾼다. 오로지 primary node만 putHDFS를 실행한다. 
   - 하지만 primary node가 바뀌면 에러가 발생함
   - 또한, 로그 양이 많으면 큐에 데이터가 점점 쌓일 것이며, nifi 서버를 여러대로 운영하는 의미가 없어진다.

2. hdfs file 이름에 hostname을 붙여서 write한다.
   - UpdateAttribute에 filename property에 ${hostname()}을 추가한다.
     - ex) ***${topicName}-${hostname()}.log***
   - 대신 서버 수 만큼 로그가 생성되기 때문에, 네임노드 메모리에 부담이 될 수 있다.
     - 후처리 작업이 추가로 필요하다.



아래 다른 이슈가 발생할 수 있다.

> block ... is not replicated yet.

아직 block이 replication이 되지 않았는데, append 요청이 들어온 경우이다. 즉, small data에 대해 자주 append를 수행하면, 위와 같은 에러가 발생할 수 있다.



**해결방법**

1. MergeContent processor를 사용해서 flowfile들을 최대한 locally하게 merge 후 append를 수행한다. 

   - MergeContent properties의 **Minumum Number of Entries, Minimum Group Size** 값을 적절히 조정한다.

2. MergeContent의 properties의 값을 바꾸는것 외에 **Run Schedule**를 조정할 수 있다. 

   - 약 1분 정도로 조정하면, 안전성과 성능 모두 향상될 수 있다.

   - 또한, HDFS에서 시간 별로 디렉토리를 운영한다고 했을 때 (ex. /nifi/log/2019/08/29/01) 실제 새벽 시간에 로그가 적게 들어와 Minumum Number of Entries나 Minimum Group Size 값에 못미치는 경우가 있다. 이럴 경우 실제 들어온 데이터는 1시지만 이후 로그가 많이 유입되는 시간 디렉토리 (ex. 8시 등)에 같이 저장되는 경우도 있는데, 이를 해결할 수 있다.

































