### Kafka Consumer 성능

<Hr>

Kafka Consumer Processor를 사용할 때, 메시지 생성 속도 보다 Consumer 하는 속도가 느린 이슈가 있었다.

- Kafka Topic에 초당 메시지가 1000건씩 생성되는데 Nifi Consumer Processor는 초당 500건 정도만 가져오고 있었음. (max.poll.records 조정)
- 하지만 너무 높게 설정하지 말고, topic 별로 초당 생성되는 메시지 수를 보고 결정 할 것.




1. message demarcator를 사용하자. 
   - Nifi의 성능의 핵심은 1개의 flowfile에 최대한 많은 메시지를 넣어서 보내는 것.
   - 현재는 flowfile 당 1개의 메시지를 대응하고 있었음. 그렇다보니 정상적인 속도가 나오지 않았었다.
   - Max Poll Records 옵션을 통해 flowfile에 넣고싶은 메시지의 최대 수를 조정할 수 있다. (디폴트는 10000)

2. Concurrent task의 수를 topic partition 수 - concurrent tasks 수와 동일하게 조정하자.
   - topic partition 수 3, nifi 서버가 4대인데, concurrent tasks가 1개라면
     - 1개 nifi 서버의 1개의 thread가 topic partition 3개를 모두 consuming 한다.
     - 그렇기 때문에 모든 topic partition을 동시에 consuming 하고 싶다면 concurrent tasks를 3개로 수정한다.
     - nifi 서버의 전체 사용 가능한 thread 수는 Controller Setting에 들어가 Maximum Thread 수를 높여준다.



**참고**

https://kafka.apache.org/0100/javadoc/index.html?org/apache/kafka/clients/consumer/KafkaConsumer.html



https://bryanbende.com/development/2016/09/15/apache-nifi-and-apache-kafka