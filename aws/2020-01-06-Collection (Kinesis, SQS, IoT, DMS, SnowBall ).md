### Collection

<hr>
### 종류

RealTime - Immediate Actions (실시간으로 데이터나 이벤트에 반응하는 서비스)

- Kinesis Data Streams (KDS)
- Simple Queue Service (SQS)
- Internet of Things  (IoT)



Near-real time - Reactive actions 

- Kinesis Data Firehose (KDF)

- Database Migration Service (DMS)



Batch - Historical Analysis (대규모 데이터의 이동을 원할 때 사용하는 서비스)

- Snowball
- Data Pipeline



<hr>

### AWS Kinesis Overview

Kinesis는 AWS에서 제공하는 Apache Kafka라 보면됨

- real-time 데이터 처리에 탁월하며, 다양한 application logs, metrics, IoT 등을 처리한다.
- 다른 Streaming processing framework (Spark, Nifi 등)들과 연동하며, 자동으로 동기화를 위해 replicated 된다.



Kinesis는 3가지 서비스가 있다.

- Kinesis Streams: low latency의 streaming ingest를 수행한다.
- Kinesis Analytics: SQL을 통한 real-time analytics를 수행한다.
- Kinesis Firehose: stream을 S3, RedShift, ES 등에 load한다.

![1](https://user-images.githubusercontent.com/22383120/71798115-332b7300-3094-11ea-8888-2ea7c8d2ccba.PNG)



<hr>

### Kinesis Streams Overview

- Stream는 Shard (Partition)이라는 단위로 나뉜다.
  - 비용 청구는 Shard 규정에 따라 요금이 청구되며, Shard는 사용자가 원하는 만큼 가질 수 있다.
  - Batch를 수행할 수 있고, producer 단에서 shard 당 message를 입력할 수 있다.
  - Shard 수는 시간이 지남에 따라 늘어날 수 있고, re-shard나 merge를 수행할 수 있다.
  - Shard들은 Global 하게 정렬할 수 없고, 각 Shard 마다 정렬할 수 있다.
- 이렇게 나뉜 Shard들을 Consumer들이 읽는다.
  - Data retention은 기본 24시간이며, 최대 (?) 7일 까지 늘릴 수 있다.
- 여러 Application이 같은 stream을 consume 할 수 있으어 real-time processing이 가능하다.
- Streams는 Immutable한 특성을 지니고 있어, 삭제나 수정할 수 없으며 오로지 append만 할 수 있다.



### Kinesis Streams Records

- Producer가 shard에 record를 생성하며, record는 아래와 같이 이루어져 있다.
- Data Blob
  - bytes 단위로 serialized 된 data이며, 최대 1MB 이다.
- Record Key
  - 여러 shard에 record를 grouping 하기 위해 사용하며, 하나의 shard에 record가 몰리는것을 방지하기 위해 highly distributed key를 사용한다.
- Sequence number
  - shard 내 record들의 unique identifier이다. producer가 생성하지 않고, shard에 record를 입력하면 Kinesis가 추가한다.



### 참고사항

- Producer는 1MB/s or 1000 message/s를 shard에 쓸수 있다.
  - 만약 이를 넘어가면 `ProvisionedThroughputException`이 발생한다.
- Consumer는 두종류가 있다 (Consumer Classic, Consumer Enhanced Fan-Out)
  - Consumer Classic: 모든 Consumer들이 Shard 당 2MB/s를 읽을 수 있으며, 5 API calls을 할 수 있다.
  - Consumer Enhanced Fan-Out: Enhanced Consumer는 Shard 당 2MB/s를 읽을 수 있으며, API call을 하지 않는다.
    - 이는 `push model`이라 하는데, Server가 Client에게 데이터를 전송하는 기법을 뜻한다.
- Data Retention은 24시간이 디폴트이며 7일까지 늘릴수 있다.



### 참고

https://aws.amazon.com/ko/kinesis/







































