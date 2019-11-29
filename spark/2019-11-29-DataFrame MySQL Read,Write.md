# DataFrame MySQL Read,Write



Spark DataFrame에서 MySQL에 Write 코드는 아래와 같다.



**write**

```scala
import org.apache.spark.sql.SaveMode
import java.util.Properties

val properties = new Properties()
properties.put("user", "admin")
properties.put("password", "1234")
properties.put("driver", "com.mysql.jdbc.Driver")

dataframe
.write
.mode(SaveMode.Append)
.jdbc("jdbc:mysql://url/database",
      "table",
      properties)
```



properties

- properties 객체에 user, password, driver 정보를 입력한다.

dataframe

- mode는 Append, Overwrite를 설정할 수 있다. 
- jdbc에 mysql의 host, table, 위에서 선언한 properties를 파라미터로 입력한다.



**spark-submit**

Spark-submit 할 때, 두가지 방법으로 mysql 드라이버를 추가해주어야 한다.



packages

```scala
.spark-submit
  --name "SPARK_APP"
  --packages mysql:mysql-connector-java:5.1.27
  Spark_test.jar
```



jars

````scala
.spark-submit
  --name "SPARK_APP"
  --jars /location/mysql-connector-java.5.1.27.jar
  Spark_test.jar
````



