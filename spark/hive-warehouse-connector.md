

### Hive-Warehouse-Connector

<hr>



### 셋팅

https://thisdataguy.com/2019/01/03/reaching-hive-from-pyspark-on-hdp3/

- pyspark로 job을 제출할때, `--jars`, `--py-files`를 각 설정해주어야 함.
- 또한, `spark.sql.hive.hiveserver2.jdbc.url`, `spark.datasource.hive.warehouse.metastoreUri`, `spark.sql.streaming.checkpointLocation` 도 기재해주어야 함



### Spark - Hive Connection

https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.4/integrating-hive/content/hive_configure_a_spark_hive_connection.html

- 필요한 요구조건 확인



- HiveWarehouseSession 사용

```python
from pyspark_llap import HiveWarehouseSession
hive = HiveWarehouseSession.session(spark).build()
```



- Spark Stream을 Hive로 Write

```
stream.writeStream.format(HiveWarehouseSession().STREAM_TO_STREAM).option("table", "web_sales").start()
```





