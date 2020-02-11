### AWS Collection

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

- `Kinesis Streams`: low latency의 streaming ingest를 수행한다.
- `Kinesis Analytics`: SQL을 통한 real-time analytics를 수행한다.
- `Kinesis Firehose`: stream을 S3, RedShift, ES 등에 load한다.

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



**Kinesis Streams Records**

- Producer가 shard에 record를 생성하며, record는 아래와 같이 이루어져 있다.
- Data Blob
  - bytes 단위로 serialized 된 data이며, 최대 1MB 이다.
- Record Key
  - 여러 shard에 record를 grouping 하기 위해 사용하며, 하나의 shard에 record가 몰리는것을 방지하기 위해 highly distributed key를 사용한다.
- Sequence number
  - shard 내 record들의 unique identifier이다. producer가 생성하지 않고, shard에 record를 입력하면 Kinesis가 추가한다.



**참고사항**

- Producer는 1MB/s or 1000 message/s를 shard에 쓸수 있다.
  - 만약 이를 넘어가면 `ProvisionedThroughputException`이 발생한다.
- Consumer는 두종류가 있다 (Consumer Classic, Consumer Enhanced Fan-Out)
  - Consumer Classic: 모든 Consumer들이 Shard 당 2MB/s를 읽을 수 있으며, 5 API calls을 할 수 있다.
  - Consumer Enhanced Fan-Out: Enhanced Consumer는 Shard 당 2MB/s를 읽을 수 있으며, API call을 하지 않는다.
    - 이는 `push model`이라 하는데, Server가 Client에게 데이터를 전송하는 기법을 뜻한다.
- Data Retention은 24시간이 디폴트이며 7일까지 늘릴수 있다.



<hr>

### Kinesis Producer

다양한 Producer를 제공한다.

- Kinesis SDK , Kinesis Producer Library (KPL), Kinesis Agent
- 이외에 Spark, Kafka, Nifi 등 3rd party library와 연동할 수 있다.



**Kinesis SDK** (putRecord, putRecords) - CLI command

- API는 PutRecord (한개 레코드)와 PutRecords(두 개 이상의 레코드)를 지원한다. 
  - PutRecords를 사용하면, batching 처리를 할 수 있고 throughput을 향상시킬 수 있다. (HTTP request는 줄인다.)
- Producer SDK는 다양한 방법으로 사용된다 (AWS Mobile SDK: Android, iOS 등)
- Use Case
  - low throughput, higher latency, Simple API, AWS Lambda

- AWS Sources들도 관리할 수 있다.
  - CloudWatch Logs, AWS IoT, Kinesis Data Analystics (분석 결과를 다시 Kinesis에 저장)

- ProvisionedThroughputExceedde Exception
  - 프로비저닝된 throughput 보다 넘을 경우 (더 많은 데이터를 보낼 경우) 발생한다.
    - 예를들어, hot partition에만 데이터가 몰릴 경우
  - 해결책
    - backoff에서 retry를 할 것. (2초 후에 다시 시도하고 다시 동작하지 않으면 4초 후, 그 이후 8초 후..)
    - shard 수를 증가시킬 것 (Scaling)
    - 좋은 partition key를 골라 골구로 모든 partition에 분포되도록 할 것



**Kiness Producer Library (KPL)**

- C++, Java Library 에서 사용하기 쉬우며, 높은 성능과 long-running producer를 만들 수 있다.
- 자동으로 retry mechanism이 내장되어 있고, Synchronous와 Asynchronous API를 제공한다.
  - Synchronous는 위에서 설명한 SDK와 같다고 보면 되며, Asynchronous가 더 좋은 성능을 보인다.
- CloudWatch의 metrics 정보를 전송할 수 있어 minitoring 하는데 사용할 수 있다.
  - SDK는 CloudWatch의 logs만 전송했었음.
- Batching 처리를 하여 throughput을 높이고, 비용은 낮춘다.
  - Collect는 multiple shards에 record를 write할 수 있다.
  - Aggregation은 여러 record를 하나의 record로 저장할 수 있다. (Latency는 증가하지만, 효율성은 또한 증가한다.)
  - Batching 처리를 할 때, 데이터가 유입되자마자 Kinesis로 전송하지 않는다. (delay를 둔다.)
    - delay 후 모아둔 Record를 하나의 Record로 Aggregating 할 수 있으며, 여러 시간 때의 Record로 모은 후 PutRecords를 한번 호출해 총 7개의 Record를 전송할 수 있다.
    - RecordMaxBufferedTime (default 100ms)를 통해 delay를 조절함으로써 Batching 처리를 좀더 효율적으로 할 수 있다. (좀더 빠른 latency를 원하면 해당 parameter를 더 낮추면 된다.)

- 압축도 사용할 수 있다.



**Kinesis Agent**

- Java-기반 agent로 KPL기반으로 빌드된다.
- Linux 기반 servere 환경에 설치할 수 있다.
- 특징
  - multiple directoriy로 부터 write 할수 있고, multiple streams에 write할 수 있다.
  - Routing 기능을 제공한다 (?)
  - streams에 전송하기 전에 Pre-processing 할 수 있다. (single live, csv to json, log to json 등등)
  - file roattion, checkpointing, retry 등을 지원한다.



<hr>

### Kinesis Consumer

- Kinesis SDK (getRecord) - CLI command
  - Shard로부터 Consumer에게 Records를 pull 한다.
  - 각 Shard는 최대 `2MB` aggregate throughput을 가진다. (Producer는 최대 `1MB`)
    - 만약 3개의 Shard가 있다면 최대 6MB를 Consuming 할 수 있다.
  - Consumer가 Shard에 GetRecords API를 요청하면, Data를 반환해준다.
    - 여기서 GetRecords API로 받을 수 있는 최대 데이터 크기는 `10 MB or 10000 Records` 이다.
    - 여기서 **Shard는 Consumer 할 때 총 2MB이기 때문에, 5초를 기다려야 한다.**
  - 초당 Shard에 최대 `5개 GetRecords API`을 요청할 수 있으며, 이는 200ms latency이다.
    - 만약 20개의 GetRecords API가 요청이 왔다면, 5개씩 처리한다는 의미이다.
  - 만약 5개의 Application이 똑같은 Shard에 Consuming 요청을 한다면,
    - 각 Application은 `400KB`의 데이터를 받을 수 있다. (2MB / 5 = 400KB)
    - 이러한 성능을 위해 **Kinesis Enhance FanOut**을 사용한다.
- Kinesis Client Library (KCL)
  - Java 기반의 Library로 다른 언어들도 지원한다. (Golang, Python, Ruby 등)
  - 여러 Shard들은 1개의 Group 내 있는 여러 Consumer들을 공유한다.
    - 즉, 같은 Group 내 여러 Consumer가 있다고 하면, 중복 데이터 없이 Records를 Consuming한다.
  - Checkpointing은 나중에 같은 Group의 Consumer가 읽더라도, 마지막 위치를 기록하고 있기 때문에 과거에 읽었던 부분부터 Consuming 한다.
    - 이러한 메타 정보는 Amazon Dynamo DB에 저장한다. (coordination 용도)
      - Shard 당 Table의 1개 Row로 Checkpoint 정보를 저장한다.
      - **DynamoDB 사용시 주의사항**
        - 충분한 Write Capacity Unit (WCU), Reading Capacity Unit (RCU) 프로비저닝을 확인한다.
        - On-Demand를 사용한다. (스펙을 잘 모를때, 쓰는 만큼만 비용을 지불하고 싶을 때 사용함.)
        - 만약 그렇지 않다면 KCL이 느려질 수 있다.
- Kinesis Connector Library
  - KCL Library를 이용하는 Java Library로 S3, DynamoDB, Redshift, ES등에 data를 Write하는 역할을 한다.
    - Connector Library는 주로 EC2 Instance 위에서 동작한다.
  - Kinesis Firehose와 유사한데, Connector Library는 직접 EC2에서 동작시키고 싶을 때 사용한다.
    - Kinesis Firehose는 서비스이다.
- AWS Lambda
  - Kinesis Data Streams에서 Records를 얻을 수 있으녀, KPL을 사용한다.
  - Lambda는 lightweight한 ETL를 수행할 때 사용한다.
  - 이 외 Trigger notification이나 email을 실시간으로 전송할 수 있다.
  - 마지막으로, batch size를 조절할 수 있다.
- 3rd parth library (Spark, Log4j, Appenders, Flume 등)



<hr>

### Kinesis Enhanced Fan Out

- New game-Changing feature (?)

  - `기존 규칙을 깨고 새로운 규칙을 만들어 내는 것.(?)`

- KCL 2.0, AWS Lambda를 사용한다.

- 각 Consumer는 2MB/s의 Records를 각 Shard로 부터 얻을 수 있다.

  - SubscribeToShard()를 하면 Kinesis Data Streams가 Consumer에게 2MB/s의 데이터를 push 한다. (`HTTP/2를 사용해서 Enhanced Fan Out 인듯 하다.`)

    - 위 Pull 방식은 Shard가 총 2MB/s를 제공하는 것이기 때문에, Consumer들이 많으면 성능이 떨어진다.
    - 하지만, Push 방식 (Enhanced Fan Out)은 Consumer 당 2MB/s를 받을 수 있기 때문에, Consumer들이 많아도 성능이 떨어지지 않는다.
    - 예를 들어, 20 Consumer가 있을 때, 각 Shard 당 40 MB/s 를 받을 수 있다.

  - Latency는 평균 70 ms 내로 동작한다. (기존 200ms 보다 줄었다.)

    - push를 하기 때문임.

      

Enhanced Fan-Out, Standard Consumer 비교

- Standard Consumer
  - 적은 수의 Consumer ( 1개, 2개, 3개.. 등등)
  - 200 ms Latency여도 상관없는 Consumer들
  - 비용 최소화

- Enhanced Fan-Out
  - 수많은 Consumer들
  - 70 ms Latency 이하로 빠른 성능을 원함.
  - 높은 비용
  - Default로 5개 Consumers로 제한되어 있다.



<hr>

### Kinesis Scaling

- Shard 추가 (Shard Splitting 이라고도 함)
  - Stream Capacity를 향상 시킬수 있다. Shard 당 1MB/s 
    - 만약 Shard가 10개면 최대 10 MB/s Producing 가능.
    - 주로 hot shard에 사용하면 된다.
  - Shard를 추가하면, 기존 Shard는 종료되며 (더이상 데이터를 받지 않는다.) data가 expire 되면, shard는 삭제된다.
- Shard 합병 (추가의 반대 operation으로 Shard를 줄인다.)
  - 비용을 줄이기 위함이며, traffic이 낮은 2 shard를 합병한다.
  - 마찬가지로, shard를 하나 만들고, 기존 두 Shard는 종료되고 (더이성 데이터를 받지 않는다.) data가 expire되면, 두 shard는 삭제된다.

- Auto Scaling
  - 특징
    - native feature가 아니다.
    - shard의 수를 UpdateShardCount API 로 변경한다.
    - AWS Lambda를 통해 Auto Scaling을 실행할 수 있다.
  - 제한사항
    - 병렬로 Resharding 할 수 없다. 미리 capacity에 대한 plan이 필요하다. (resharding이 빠른 속도가 아니기 때문에 미리 plan이 필요하다는 뜻)
      - 즉, 동시에 여러 shard들이 reshard 되지 않는다는 의미이며, 하나씩 resharing 한다.
      - 만약 1000개 Shard를 2000개로 늘린다고 하면, 총 8.3 시간이 소요된다.
    - 그 외 여러 많이 있지만, 굳이 알 필요는 없다.



<hr>



### Kinesis Security

Kinesis Security 종류는 아래와 같다.

- IAM 정책을 통한 Control Access, Authorization
- HTTPS endpoint를 이용해 암호화
  - data를 Kinesis로 전송할 때 암호화를 하기 때문에 intercept 할 수 없다.
  - 또한 KMS (?)를 이용해 rest(?)에 암호화를 할 수 있다.
  - 이러한 암호화/복호화는 client 에서 수동으로 해야한다.
- VPC를 통해 Private Network를 만들어 public 하게 사용하지 않는다.



<hr>

### Kinesis Firehose

특징

- Fully Managed Service (완전히 관리된 서비스), no administration
- 근실시간 (60초 이내 latency를 가진다)
  - Kinesis Streams는 실시간이지만, Kinesis Firehose는 근실시간이다.
  - 이러한 이유는 Firehose는 batching 방식으로 동작하기 때문이다.
  - 만약 full batch가 아니라면, gurantee를 보장하지 못하고(?) 데이터를 바로 destination으로 보낼 것이다.

- 데이터를 `Redshift, AWS S3, ES, Splunk` 등에 Load 한다.
- Automatic Scaling을 가진다.
  - 더 많은 throughput을 원할 때 자동으로 scale을 늘릴 수 있다.
  - 반대로 더 적은 throughput을 원할 때는 scale을 줄일 수도 있다.
- 다양한 Data Format과 Data Conversion을 지원한다. Json --> Parquet/ ORC 등 (`S3 에서만 가능`)
  - 만약 다른 Type으로 변경하고 싶으면 AWS Lambda와 같이 활용한다. (ex. CSV --> JSON)
- 다양한 압축 방법 (Gzip, Zip, Snappy을 지원한다. (`S3 에서만 가능`)
  - 단 RedShift에서는 Gzip은 지원된다.
- 데이터를 전송한 만큼 비용을 지불하면 된다.
- 마지막으로, Spark, KCL은 Kinesis Data Firehouse로 부터 데이터를 읽을 수 없다. (참고할것. 시험에서 트릭)



**Kinesis Data Firehose Diagram**

- Kinesis Firehose에는 다양한 Source들이 연동될 수 있다. 
  - 위에서 설명한 KPL, Kinesis Agent 들도 Kinesis Data Streams가 아닌 Firehose에 바로 데이터를 전송할 수 있다.
- 데이터 변형을 위해 Lambda Function을 활용할 수 있다. (ex. CSV --> JSON)
  - Firehose에 온 데이터를 Lambda를 통해 변형 후 다시 Firehose로 전송한다.
- 이후 데이터는 Amazon S3, Redshift, ES, Splunk에 전송될 수 있다.
  - Amazon S3에 Lambda를 통해 변형된 데이터를 저장할 수 있으며, 이에 대한 Copy를 Redshift에도 복사할 수 있다.
  - 또한, 원본(Source data)를 S3에 다른 버킷에 저장하여, 데이터 유실이 발생하지 않게 한다.
  - 이외에도, Transformation 실패, Delivery 실패에 관한 로그도 아카이빙 용도로 저장하여 나중에 원인을 분석할 수 있다.



**Firehose Buffer Sizing**

- Firehose는 Source 로부터 Record들을 받을 것이고, 이를 Buffer에 모을 것이다.
  - Buffer는 항상 flushed되지 않으며, flushed되기 위해 몇가지 Rule이 있다. (time, size rule)
- Rule
  - Buffer Size를 정의해야한다. (ex. 32MB) 해당 사이즈를 도달했을 경우 flush한다.
  - Buffer Time을 정의해야한다. (ex. 2M) 해당 시간을 도달했을 경우 flush한다.
    - 2분이 지나면 buffer Size가 가득차지 않더라도 flush한다.
    - 결론적으로, 시간이든 사이즈든 먼저 도달한쪽이 발생하면, flush한다.
- Firehose는 throughput을 향상시키기 위해 자동으로 buffer size를 증가시킨다. (Auto Scaling)
  - High Throughput을 위해 보통 Buffer Size를 조절한다.
  - Low Throughput을 위해 보통 Buffer Size보다 Buffer Time을 조절한다.
  - **참고로 가장 작은 buffer time은 1분이다.**



**Kinesus Data Stream, Firehose의 비교**

Streams

- custom code (producer / consumer)를 작성할 수 있다.
- Real Time 내로 동작한다. (일반적으로 200 ms latency 내, enhanced fan-out은 70ms latency 내)
- Scaling을 관리해야 한다. (Shard Splitting, merge 등 - 비용, Throughput과 직결됨)
- 데이터는 1~7일 보관이 가능하며, multiple consumer가 사용할 수 있다.

Firehose

- 완전히 관리된 서비스이며, S3, Splunk, Redshift, ES로 데이터를 보낼수 있다.
- Lambda와 함께 서버리스 데이터 전송이 가능하다.
- Near Real Time 내로 동작한다. (가장 작은 buffer time이 1분)
- 자동 Scaling 이며, 데이터를 보관하지 않는다.



 

<hr>

### SQS

SQS도 Kinesis와 마찬가지로, Producer가 Message를 전송하면 이를 Consumer가 메시지를 받게된다.

- 하지만 Kinesis와는 다르다.



Standard Queue (AWS SQS) 특징

- Oldest Offering (10년 된 서비스)로 Fully Managed 서비스이다.
- Scale은 1 Message/s ~ 10,000 Message/s 까지 가능하다.
- Default retention은 4 days ~ 최대 14 days 까지 가능하다.
- queue에 얼마나 많은 메시지가 저장될 수 있는지에 대한 제한은 없다.
- Low Latency (10 ms 이내 publish, receive 가능)
- consumer 수에 따라 horizontal scaling 가능
- message를 복사할 수 있음.
- 메시지의 순서는 보장하지 않는다.
- 메시지당 256 KB 크기로 제한되어 있다.



Producing Message 구조

- Body
  - 256 KB 까지 저장 가능
  - String
- Message Attributes (Metadata - optional)
  - name - type - value
  - name - type - value ...
- Delay Delivery를 제공 (optional)
- `Kinesis 와 큰 차이점은...`
  - SQS는 256 KB의 String Body를 전송한다.
  - Kinesis는 1 MB의 byte code를 전송한다. 



Consuming Message

- 한번에 10 message를 consumer가 받을 수 있다.
- 메시지를 지울 땐 Consumer가 message를 전달 받아 처리후, SQS에 Message Id, receipt handle을 전달후 지운다.
  - 그러면, 다른 consumper application이 해당 message는 사용하지 못한다. (`Kinesis와 큰 차이점`)



FIFO QUEUE

- First In - First Out 방식.
- Lower throughput (3,000 message/s)
- 들어온 순서대로 consumer에 의해 처리된다. (메시지는 정확하게 한번 전송된다.)



SQS Extended Client

- 256 KB Message 크기가 제한되어있기 때문이 이를 더 늘리고 싶다면, SQS Extended Client (Java Library)를 사용한다.
- 처리 단계
  - Producer가 Amazon S3 Buket에 Large message (256 KB 초과)를 저장한다.
  - 이후 message의 metadata를 SQS Queue에 전송한다.
  - Consumer는 SQS Queue에서 message의 metadata를 읽는다.
  - 이후 Consumer는 Amazon S3 Bucket에 저장된 message를 읽는다. 



사용 사례

- Decouple Application (asynchronously payment를 다룰때,)
- Buffer Write to a database (DB에 데이터를 쓸때 buffer 역할로 쓴다.)
- Handle large loads of message coming in (대규모의 email sender가 있을 때 (?))
- SQS can be integrad with Auto Scaling Through CloudWatch (CloudWatch와 결합되어 모니터링 서비스와 같이 사용된다.)



제한사항

- 최대 120,000 in-flight message를 consumer에 의해 처리가 가능하다.  
- Batch Request는 최대 10 message, 256 KB 이다.
- Message Content는 XML, JSON, Unformatted text만 가능하다.
- Standard queue는 unlimited TPS (Transactions per second)를 가진다.
- FIFO queue는 3,000 message/s를 지원한다.
- Max message Size는 256 KB이지만, Extended Client를 사용하면 더 늘어날 수 있다.
- Date retention은 1분~14분 까지 가능하다.
- 가격 측정
  - API Request
  - Network usage



SQS 보안

- HTTPS endpoint를 사용한다.
- KMS (Key Management Service)를 사용해 SSE (Server Side Encripytion)이 가능하다.
- IAM policy를 반드시 써야한다.



<hr>

### Kinesis Data Streams 와 SQS의 비교

Kinesis Data Stream

- Message가 여러번 Consuming 될 수 있다.
- 특정 retention 기간이 지난 후에 message를 삭제한다.
- Shard 단위에서 record ordering이 가능하다.
- "Streaming MapReduce" Query가 가능하다
  - 실시간 처리가 가능하다는 의미인것 같음.
- Checkpoint를 제공한다. (With DynamoDB)
- Shard는 이전에 미리 정의해놔야 한다.
- 사용 유즈 케이스
  - 실시간 데이터 분석 및 실시간 Metric, Report 등
  - 모바일 데이터 Capture
  - 복잡한 Streaming Processing
  - IoT Data Feed



SQS

- Message는 한번만 Consuming 될 수 있다. 즉, 하나의 App이 하나의 Queue를 읽는다.
- Consumer에 의해 message를 삭제한다.
- Standard queue에서 ordering이 보장되지 않는다.
  - ordering 보장을 위해 FIFO queue를 사용해야한다.
- "delay" message가 가능하다.
- Dynalic 하게 Scaling 해야한다.
- 사용 유즈 케이스
  - Order Processing (FIFO QUEUE 사용함. 순서가 보장됨)
  - Image 처리
    - Image 데이터를 Extended library를 통해 S3에 저장하여 처리할 때 사용한다.
    - 일반적으로 Kinesis나 SQS broker에 Image를 저장하지 못하기 때문.
  - Message에 따라 Auto Scaling Queue를 하고 싶을 때.
  - Batch, Buffer 용도로 사용하기 위함.



모든 Streams 기술 비교

![3](https://user-images.githubusercontent.com/22383120/72723773-e3d16080-3bc4-11ea-8f0e-7f391e51fe5e.PNG)

- SQS FIFO는 Exactly Once 처리가 가능하다.
  - SQS FIFO Queue는 로그의 순서를 위한 Order 작업과 중복 제거 작업을 하기 때문이다.
- SQS FIFO는 ~3000 message로 제한된 이유도 위와 같이 전처리 (Order, 중복 제거)가 필요하기 때문이다.

<hr>

### IoT

 ![2](https://user-images.githubusercontent.com/22383120/73116571-d842b880-3f7b-11ea-8fc8-9b19de99c7b6.PNG)

- IoT Thing

  - IoT Device

- Thing Registry (**IAM of IoT**)

  - Device ID, authentication security 등 데이터를 받을 Device를 등록한다.
    - 각 Device는 Unique ID를 가지며, 각 Device마다 metadata를 지원한다.
  - Authentication을 위해 X.509 certication을 사용한다.
    - 이외에도 AWS SigV4, Custom token을 제공한다.  
  - Authorization
    - AWS IoT Policy
      - X.509 certifacate와 첨부(attach)할 수 있다.
      - JSON Documents로 되어있다.
      - 각 IoT Device 보단 group 별로 attach 한다.
    - IAM Policy
      - users, group, role에 attach 한다.
      - IoT AWS API를 제어할 수 있다.
  - IoT Group을 만들어 group 별로 permission을 할당할 수 있다.

- Device gateway

  - AWS IoT Cloud (Broker 등)과 IoT Thing의 Communication을 위해 사용하는 Manager Service
    - 즉, AWS IoT Cloud와 메시지를 주고 받기 위해 Device Gateway를 거쳐야 한다.
  - MQTT, WebSocket, HTTP 1.1 protocol을 지원한다.
  - Full managed, 자동 scale up을 지원한다. (bilion device)

- IoT Mesage Broker

  - Message를 임시 저장하는 역할을 한다. (pub/sub messaging pattern , low latency )
    -  Message는 topic으로 publish 된다.
    - 해당 topic과 연결된 모든 clinet에게 message를 전달한다.
  - MQTT, WebSocket, HTTP 1.1 protocol을 지원한다.

- IoT Rules Engine

  - Broker로 부터 Message를 받으며, 특정 조건이 발성하면 Kinesis, SQS, Lambda 등에 데이터를 전송한다.
  - Rule은 MQTT Topic에 정의된다.
    - **언제** 발생할 지 trigger를 만들 수 있고, **무엇을** 할지 결정할 수 있다.
    - ex)
      - file을 S3에 저장하라.
      - SQS queue에 data를 publish 하라.
      - Lambda function을 통해 data를 추출하라.
      - 등등..

- Device Shadow

  - AWS IoT Cloud와 통신이 끊켰을 때를 대비해 Device의 상태 정보 (state)를 임시 보관한다.
    - ex) light on, light off, light blue, light red 등등
  - JSON Document로 Device의 상태를 나타낼 수 있다.
  - 향후 online 상태가 되었을 때 먼저 IoT는 Device Shadow를 retrieve 한다.

- IoT Greengrass

  - device에 직접 compute layer (ex. lambda)를 제공한다.
    - 즉, device에 lambda function을 동작시킬 수 있다.
    - ex)
      - 데이터 전처리
      - ML model 기반의 prediction을 수행
      - device data의 sync
      - local device 간 commucation
      - 등등.
  - Offline에서도 동작할 수 있다. (AWS와 연결이 끊키더라도 동작할 수 있음)

  

<hr>

### DMS  - Database Migration Service

Migration 를 위한 서비스

- Securly, Quickly 하게 database를 AWS로 migration할 수 있다.
- migration 하는 동안 source database는 계속 사용할 수 있다.
- Support
  - Homogeneous Migation: Oracle --> Oracle
  - Heterogeneous Migration: SQL Server --> Autora
- CDC를 사용해 Data Replication으로 사용할 수 있다.
- Replication tasks를 수행하기 위해 반드시 EC2 Instance를 띄어야 한다.



Source, Target

- Source
  - On-Premise, EC2 Instance database (Oracle, MS SQL Server, MY SQL 등등)
  - Azure: Azure SQL Database
  - Amazon RDS
  - Amazon S3
- Target
  - On-Premise, EC2 Instance database (Oracle, MS SQL Server, MY SQL 등등)
  - Amazon RDS, Redshift, DynamoDB, S3
  - Elasticsearch Service
  - Kinesis Data Streams
  - Document DB



 AWS Schema Conversion Tool (SCT)

- Datacase schema를 다른 engine의 schema로 Convert 해주는 Tool
  - ex) MySQL 에서 Elasticsearch service로 Migration한다 했을 때, MySQL Schema를 Elasticserach에 저장할 수 있는 Schema 형태로 바꿔준다.
  - OLTP (SQL Server or Oracle to MySQL, PostgreSQL, Aurora)
  - OLAP (Teradata or Oracle to Amazon Redshift)
- **AWS SCT를 사용하기 위해 AWS DMS Endpoint와 Task를 반드시 생성해야 한다.**











### 참고

https://aws.amazon.com/ko/kinesis/







































