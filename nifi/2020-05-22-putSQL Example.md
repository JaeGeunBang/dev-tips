### putSQL Example

<hr>



Kafka에 저장된 JSON 데이터를 MySQL에 Input 하고자 한다.

**준비사항**

JDBC Connector를 위해 com.mysql.jdbc.Driver가 필요하다. 먼저 MySQL 버전에 맞는 .jar 파일을 다운 받아 모든 Nifi 서버에 배포한다.

- 참고로 .jar 파일을 배포할 경로는 Nifi가 접근가능한 위치여야 한다. (읽을 수 있는 권한이 있어야함)
- .jar 파일을 정상적으로 읽지 못하면 `Can't read Driver`와 같은 에러가 발생한다.



**DataFlow**

DataFlow는 아래와 같다

- ConsumerKafka --> ExecuteScript --> ReplacaText --> PutSQL

- 각 역할은 아래와 같다.

  - `ConsumerKafka`: Kafka로 부터 Message를 받는다.

  - `ExecuteScript`: Kafka Message (Nifi Contents)를 Nifi Attributes로 바꾸기 위함이다. 코드는 아래와 같다. (Contents를 Attribute로 바꾸는 방법은 다양하게 있다.)

    - Property

      - Script Body

        ```Groovy
        import org.apache.commons.io.IOUtils
        import org.apache.nifi.flowfile.FlowFile
        import org.apache.nifi.processor.io.InputStreamCallback
        
        import java.nio.charset.*
        
        List<FlowFile> flowFileList = session.get(10000);
        
        def slurper = new groovy.json.JsonSlurper()
        if (!flowFileList.isEmpty()) {
            flowFileList.each {flowFile ->
                def attrs = [:] as Map<String, String>
                session.read(flowFile,
                        { inputStream ->
                            def text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
                            def obj = slurper.parseText(text)
                            obj.each { k, v ->
                                attrs[k] = v.toString()
                            }
                        } as InputStreamCallback)
                flowFile = session.putAllAttributes(flowFile, attrs)
                session.transfer(flowFile, REL_SUCCESS)
            }
        }
        ```
        
      - JSON 형태의 Message를 Parsing 하여 Nifi Attribute로 만든다.

  - `ReplaceText`: Attributes를 통해 MySQL 문법을 만든다.

    - Property
      - Replacement Value: `INSERT INTO test_table (col1, col2) VALUES ('${col1}', '${col2}')`

  - `PutSQL`: 만든 MySQL 문법을 MySQL에 적용한다.

    - JDBC Connection Pool은 아래와 같이 설정한다.

- JDBC Connection Pool을 위한 DBCP Controller Service를 만들어야 한다.
  - Property
    - Database Connection URL: `jdbc:mysql://localhost:3306/db`
    - Database Driver Class Name: `com.mysql.jdbc.Driver`
    - Database Driver Location(s): `file:///home/jaegeun/mysql-connector-java-5.1.49.jar`
    - 그 외에 Database User, Password 설정

