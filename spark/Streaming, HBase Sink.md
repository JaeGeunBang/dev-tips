# Streaming, HBase Sink



Spark Structurec Streaming에서 기본 HBase Sink를 제공하지 않기 때문에, HBase에 데이터를 저장하기 위해 Spark Structured Streaming -> Kafka -> HBase 의 과정을 거쳐야 한다.



하지만, 바로 Spark Structured Streaming에서 HBase로 저장하기 위해 HBaseForeach Sink를 직접 구현해야한다.



먼저 hbase 의존성을 추가한다.

**pom.xml**

```xml
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-client</artifactId>
    <version>2.0.2</version>
</dependency>
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-common</artifactId>
    <version>2.0.2</version>
</dependency>
```



이후 HBaseForeachWriter.scala를 생성한다.

**HBaseForeachWriter.scala**

```scala
import java.util.concurrent.ExecutorService
import org.apache.hadoop.hbase.client.{Connection, ConnectionFactory, Put, Table}
import org.apache.hadoop.hbase.security.User
import org.apache.hadoop.hbase.{HBaseConfiguration, TableName}
import org.apache.spark.sql.ForeachWriter

trait HBaseForeachWriter[RECORD] extends ForeachWriter[RECORD] {

  val tableName: String
  val hbaseConfResources: Seq[String]

  def pool: Option[ExecutorService] = None
  def user: Option[User] = None

  private var hTable: Table = _
  private var connection: Connection = _

  override def open(partitionId: Long, version: Long): Boolean = {
    connection = createConnection()
    hTable = getHTable(connection)
    true
  }

  def createConnection(): Connection = {
    val hbaseConfig = HBaseConfiguration.create()
    hbaseConfResources.foreach(hbaseConfig.addResource)
    ConnectionFactory.createConnection(hbaseConfig, pool.orNull, user.orNull)

  }

  def getHTable(connection: Connection): Table = {
    connection.getTable(TableName.valueOf(tableName))
  }

  override def process(record: RECORD): Unit = {
    val put = toPut(record)
    hTable.put(put)
  }

  override def close(errorOrNull: Throwable): Unit = {
    hTable.close()
    connection.close()
  }

  def toPut(record: RECORD): Put
}
```

HBase Connection과 record Put 등 관련된 메서드를 정의한다.



이후 실제 writeStream을 진행한다.

**HBaseWriter.class**

```scala
// Case Class 선언. class 외부에 선언한다.
case class CassClassTest
	(key: String, test_date: Timestamp, value1: String, value2: String, value3: String)

class HBaseWriter {
  def saveResult(dataframe: DataFrame): = {
    val spark = SparkSession
      .builder
      .appName("SparkSQL")
      .master("local[*]")
      .getOrCreate()
	import spark.implicits._

    // DataFrame은 DataSet으로 변경한다. (Case Class를 적용하기 위함)
    val dataset = dataframe.as[CassClassTest]

    // Foreach 구문에 위에서 구현한 HBaseForeachWriter를 사용한다.
    val query = dataset
    .writeStream
    .foreach(new HBaseForeachWriter[CassClassTest] {
        override val tableName: String = "hbase-table"
        override val hbaseConfResources: Seq[String] = Seq("resource/core-site.xml", "resource/hbase-site.xml")

        override def toPut(record: CassClassTest): Put = {
            val rowKey = record.key.toString() // row key 선언
            val p = new Put(Bytes.toBytes(rowKey))
            // column family: info
            // qualifier: value1, value2, value3
            p.addColumn(Bytes.toBytes("info"), Bytes.toBytes("value1"), Bytes.toBytes(record.value1))
            p.addColumn(Bytes.toBytes("info"), Bytes.toBytes("value2"), Bytes.toBytes(record.value2))
            p.addColumn(Bytes.toBytes("info"), Bytes.toBytes("value3"), Bytes.toBytes(record.value3))
            p
        }
    }
    )

    query.start().awaitTermination()
  }
}
```



HBase Sink를 사용하기 위해, 기존 DataFrame은 DataSet으로 변경해야하며, case class를 선언해야 한다.



이후 table name, config file을 정의한다. (config file은 resource/ 위치에 넣어 사용했다.)



마지막으로 row key, column family, qualifier를 각 Put Object에 추가한다.



### 참고

https://stackoverflow.com/questions/47152015/spark-structured-streaming-with-hbase-integration