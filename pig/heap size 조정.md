### Heap size 조정

<hr>


pig 실행 도중 Heap size가 모자라다는 이슈가 발생했다.

해당 이슈는 MapReduce에서 Heap Size를 조정하면 된다. 만약 Tez 기반으로 동작하는 pig 라면 Tez Config를 수정해야한다.



**mapred-site.xml**

*mapreduce.map.java.opts*

- -Xmx2000m

*mapreduce.reduce.java.opts*

- -Xmx4000m

*mapreduce.map.memory.mb*

- map heap size 보다 크게

*mapreduce.reduce.memory.mb*

- reduce heap size 보다 크게



map, reduce의 memory를 너무 크게 잡으면 hadoop cluster에서 전체 vCore가 남는 경우가 발생할 수 있다.

- 메모리는 전체 클러스터의 모든 메모리를 사용하지만, vCore는 남는 상황.
- 즉, memory 설정도 모니터링 진행 후 정해야한다.



설정 후 설정이 잘 되었는지 Yarn - ApplicationMaster에서 확인한다.

- Yarn - ApplicationMaster - Application - Job - Configuration