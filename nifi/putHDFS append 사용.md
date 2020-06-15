### putHDFS - append 사용

<hr>

Nifi를 통해 HDFS로 로그를 저장할 때, append를 통해 로그를 저장할 수 있다. (nifi 1.9 버전 기준)

- 기존 버전에서는 append 가 제공되지 않았던것 같다.



**Flow**

- consumerKafka -> UpdateAttribute -> putHDFS



**processor 설명**

1. consumerKafka processor
   - 필요한 topic에서 로그를 읽는다.
   - message demarcator property에 shift+enter를 입력한다.
     - 여러 kafka message를 하나에 flowfile에 저장하며, enter 값을 넣지 않으면 kafka message 당 flowfile이 생성된다.
     - 성능 차이가 많이 남.
2. UpdateAttribute processor
   - filename property를 추가한다.
   - filename을 지정한다.
   - 그 외에 year, month, day, hour 등과 같은 시간 property도 추가한다.
3. putHDFS processor
   - Conflict Resolution Strategy property를 append로 바꾼다.
   - Directory property에 HDFS 경로를 지정하면, 위에서 지정한 filename으로 로그가 저장되는 것을 확인할 수 있다.



