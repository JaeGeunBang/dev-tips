### 2019-07-03 Latency 측정

<hr>

Kafka의 메시지에는 메시지 생성 시간이 출력된다 (CreateTime)



DataFlow

- Fluentd (log 발생) —> Fluentd (Aggregation) —> Kafka —> Consumer 
  - 각 —> 지점을 A, B, C 라 함. 
  - 여기서 C는 Consumer가 소비하는 Queue Time

- log 발생 서버에서 Kafka에 저장되는 시간을 측정하자.

  - A + B  지점을 계산 하자.
  - A + B + C는 Consumer의 스펙에 따라 제각각이 될 수 있기 때문에 일반적으로 A + B 까지 측정하자.

  

Latency 측정

- Latency 측정은 아래 3가지로 진행했다.
  - 평균: 전체적으로 평균 Latency를 알 수 있다. 
  - 백분위수 (Percentile): 90%, 95%, 99%로 측정. 이상치 값이 얼마나 많은지 확인. 많다면 보완이 필요. 
  - 표준편차: 평균으로부터 얼마나 멀어졌는지 알 수 있음. 평균이 3이고, 표준편차가 1.4라면, 3으로부터 1.4가 멀어졌다는 의미. 표준편차가 높을 수록 보완이 필요. 

