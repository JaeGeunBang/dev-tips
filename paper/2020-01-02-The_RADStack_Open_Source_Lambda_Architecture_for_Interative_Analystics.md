### The RADStack: Open Source Lambda Archietecture for Interactive Analystics

<hr>


### 개요

- RADStack은 Real-Time Anlaytics Data Stack
  - 정확한 계산, 스트리밍이 가지는 low-latency 의 보장, 배치가 가지는 flexibility의 보장을 결합한다.
  - 대표적인 Stack으로 Apache Kafka, Apache Samza, Apache Hadoop, Druid 이다.
  - 여기서 Druid는 `Serving layer`, Apache Samza, Apache Hadoop은 `데이터 프로세싱`, Apache Kafka는 `event delivery` 역할을 한다.



<hr>

### Background

- TimeStamp, Dimension, Metric을 가진 데이터를 OLAP workflows의 표준이라 한다.
  - 해당 데이터를 기반으로 "일주일 동안 얼마나 많은 클릭이 발생했는지?"와 같은 쿼리를 분석(drill-down, aggregate)할 수 있다.
  - 유연한 쿼리와 빠른 응답 시간이 필요하다.
- 이를 위해 적절한 Serving Layer가 필요하다.
  1. PostgreSQL (RDBMS)
     - 데이터 웨어 하우스로써, star schema를 구축하여 aggregate table과 캐시를 사용해 성능을 높일 수 있다. (`Apache Kylin도 star schema기반으로 동작하는 기술이지만, 해당 기술은 미리 N-1 차원의 큐보이드를 만들어 둚`)
     - 허나 캐시가 되어 있지 않으면 성능이 느리며, aggregation 하는데 몇 분이 소요된다. (빠른 응답을 못함)
  2. HBase (No SQL)
     - 미리 total set에 대한 aggregation을 저장해두면, O(1) 만에 lookup이 가능하다.
     - 허나 유연하지 못하고, 미리 계산해두지 않았다면 성능에 치명적이며, 쿼리가 불가능하다.
  3. **Druid**
     - 빠른 응답 시간 (low latency aggregation), 유연한 쿼리 (arbitrary data exploration), 빠른 데이터 ingestion이 가능하다.
     - 허나 Druid에서 ingest, query를 하기 위해서는 `사전에 전처리가 필요하며, 이는 streaming 기술과 반드시 결합`되어 사용해야 한다.
     - 또한, `여러 Source에서 데이터를 받기 위해 Message Bus 기술과 결합`되어야 한다.
     - 위 두 기술을 통해 real-time processing이 완벽하지만, 아직 streaming 기술이 오래되지 않아 노하우가 부족할 수 있다. 
     - 그렇기 때문에, production 환경에선 실제 hadoop과 결합하여 streaming 에서 만든 데이터를 clean up 하고, 저장한다. 이후 batch processing 작업도 같이 운영을 한다.



결론적으로, Druid, Apache Samza, Apache, Hadoop, Apache Kafka를 사용한다. 



<hr>

### Druid (Serving Layer)



