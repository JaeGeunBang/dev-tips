
## 클러스터 모드 (with Yarn)
```
./bin/spark-submit 
--master yarn 
--class jgb.test.app.WordCount 
target/scala-2.11/example_2.1.1.jar "args1" "args2"
```
> --master yarn: yarn에 spark application 제출을 위함
> --class jgb.test.app.WordCount: 메인 클래스
> target/scala-2.11/example_2.1.1.jar "args1" "args2": 제출할 jar 파일과 파라미터 값을 차례대로 작성함



## 스트리밍 어플리케이션 + Kafka
```
./bin/spark-submit 
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0
```
> --packages ...: 스트리밍 어플리케이션에 Kafka의 데이터 유입/저장을 하고 싶을 때 --package를 통해 kafka 패키지를 같이 넘겨준다.



## Config 파일 제출
```
./bin/spark-submit 
--master yarn 
--deploy-mode cluster 
--conf "spark.driver.extraJavaOptions=-Dconfig.file=application.conf" 
--conf "spark.executor.extraJavaOptions=-Dconfig.file=application.conf" 
--files "./application.conf"
```
> ConfigFactory를 통해 Config 파일을 읽고 싶다면 위와 같이 Config 파일을 스파크 어플리케이션 제출할 때 같이 넘겨준다.



또는 아래와 같이 작성한다.

```
./bin/spark-submit 
--master yarn 
--deploy-mode cluster 
--files ./application.conf
--driver-java-options='-Dconfig.file=application.conf'
```



## Spark executor, driver 조정 (클러스터 모드)
> --num-executor 1 (Executor 의 수)
> --executor-cores 1 (Executore의 코어 수)
> --executor_memory 1g (Executor의 메모리양)
> --conf spark.executor.memoryOverhead = 0 (Executor의 메모리 overHead의 양)
> --driver-cores 1 (드라이버의 코어 수)
> --driver-memory 2g (드라이버의 메모리 양)
> --conf spark.driver.memoryOverhead = 0 (드라이버의 메모리 overHead의 양)

***참고로 클라이언트 모드의 executor, driver 조정이 클러스터 모드와 다르기 때문에 이는 공식홈페이지에서 확인이 필요하다.*** 


보통 메모리 할당은 executor-memory + overHead memory 사이즈로 결정된다. 즉, 정확한 메모리 할당을 위해 executor memory 뿐만 아니라 overHead memory도 같이 조정해주어야 한다.

