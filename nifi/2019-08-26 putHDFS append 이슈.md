### putHDFS - append 이슈

<hr>
putHDFS processor를 append 방식으로 write할 때 아래와 같은 이슈가 생긴다.

> Failed to APPEND_FILE ... because this file lease is currently owned by DFSClient_NONMAPREDUCE on ...



해당 이슈는 nifi 서버가 한대일때는 문제가 없지만, 여러대 일경우 문제가 생길 수 있다. 하나의 file에 append 할 때 하나의 client만 접근할 수 있다. 



**해결방법**

1. PutHDFS의 SCHEDULING에 execution을 Primary node로 바꾼다. 오로지 primary node만 putHDFS를 실행한다. 
   - 하지만 primary node가 바뀌면 에러가 발생함
   - 또한, 로그 양이 많으면 큐에 데이터가 점점 쌓일 것이며, nifi 서버를 여러대로 운영하는 의미가 없어진다.

2. hdfs file 이름에 hostname을 붙여서 write한다.
   - UpdateAttribute에 filename property에 ${hostname()}을 추가한다.
     - ex) ***${topicName}-${hostname()}.log***
   - 대신 서버 수 만큼 로그가 생성되기 때문에, 네임노드 메모리에 부담이 될 수 있다.
     - 후처리 작업이 추가로 필요하다.



