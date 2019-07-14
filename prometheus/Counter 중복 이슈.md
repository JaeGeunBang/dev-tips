### Counter 중복 이슈

<hr>

현재 Java를 통해 10개 토픽에서 Consuming 하는 중이며, 각 토픽에서 읽는 메시지의 수를 Count하여 Prometheus로 전송하고 있다. 

- 각 토픽별로 Count가 다르게 측정되야 하는데, 비슷하게 Count되는 현상이 발견됨.
  - 원했던 결과
    - topic 1 - Count: 20
    - topic 2 - Count: 20
  - 현재 결과
    - topic 1 - Count: 40
    - topic 2 - Count: 40
- 원인은 Count를 같은 객체에서 측정하고 있었기 때문. 



Count를 기록할 때 Counter, CollectorRegistry 객체가 필요함. (Gauge는 Gauge 객체가 필요) 

- 현재 코드는 카프카 Consuming 이 후 프로메테우스 객체를 새로 생성해 Count를 세고 있었음. 
  - 그러다보니 카프카 프로메테우스 내 Counter, CollectorRegistry 를 static 객체로 선언해서 사용했음. 
  - 그렇다보니 모든 Topic의 Count가 계속 기록되고 있었음. 
- Counter, CollectorRegistry는 Thread 별로 가지도록 만들 것. 
  - 이 후 프로메테우스 객체를 생성할 때, 파라미터로 Counter, CollectorRegistry를 전달해서 사용함. 