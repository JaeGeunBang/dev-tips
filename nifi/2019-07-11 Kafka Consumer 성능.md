### Kafka Consumer 성능

<Hr>

Kafka Consumer Processor를 사용할 때, 메시지 생성 속도 보다 Consumer 하는 속도가 느린 이슈가 있었다.

- Kafka Topic에 초당 메시지가 1000건씩 생성되는데 Nifi Consumer Processor는 초당 500건 정도만 가져오고 있었음.



1. message demarcator를 사용하자. 
   - Nifi의 성능의 핵심은 1개의 flowfile에 최대한 많은 메시지를 넣어서 보내는 것.
   - 현재는 flowfile 당 1개의 메시지를 대응하고 있었음. 그렇다보니 정상적인 속도가 나오지 않았었다.
   - Max Poll Records 옵션을 통해 flowfile에 넣고싶은 메시지의 최대 수를 조정할 수 있다. (디폴트는 10000)

2. Concurrent task의 수를 topic partition 수 - nifi 서버 대수를 통해 조정하자. 
   - topic partition 수 3, nifi 서버 3대 라면, 서로 1:1 대응이기 때문에 concurrent task 수를 높여도 의미가 없다. 
   - 만약 topic partition 수 6이라면, concurrent task 수를 2로 둠으로써 최적의 성능을 낼 수 있다. 