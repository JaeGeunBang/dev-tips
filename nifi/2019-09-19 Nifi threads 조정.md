### Nifi threads 조정

<hr>
각 Processor들은 동시에 수행하기 위해 Thread수를 조정할 수 있는데 이는 Concurrent Tasks에서 조정할 수 있다. 디폴트는 1이다.



![1_9Hw8brYtokfQSQddR-v7sw](https://user-images.githubusercontent.com/22383120/65207474-b4063500-dacc-11e9-95e2-fe1dc1372b90.png)



하지만 Concurrent Tasks를 100개로 지정한다고 해도 동시에 100개의 thread가 동작하는 것은 아니며, thread 수는 Controller Setting에 **Maximum Timer Driven Thread Count** 수에 따라 달라진다.

Maximum Timer Driven Thread Count 디폴트는 10이며, 전체 Nifi 서버에서 총 10개의 Thread들이 동작하는 것을 뜻한다.

그렇기 때문에 Processor에서 Concurrent Tasks를 100개로 한다고 한들, Maximum Timer Driven Thread Count가 10개라면, 최대 10개 Thread 밖에 동작하지 못한다.



Kafka Topic 을 Consuming 할 때, Total Lag가 많이 벌어져 있는 상황에 Consuming 하면 순간 CPU 자원을 많이 사용한다. 

이때 Maximum Timer Driven Thread Count 수가 적절하게 설정되어 있지 않다면 다른 Processor 들의 동작도 멈추는 현상이 발생하기 때문에 Nifi 서버에 스펙에 맞게 설정해주는 것이 좋다.



### 참고

https://medium.com/@ben2460/nifi-scheduling-a522a1c9e740

https://bryanbende.com/development/2016/09/15/apache-nifi-and-apache-kafka

















