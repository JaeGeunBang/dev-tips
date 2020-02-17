### Ambari - Pig 실행 이슈

<hr>
Ambari 기반에 pig를 실행하는데 아래 2가지 이슈가 발생했음.



**mapreduce.application.framework.path의 ${hdp.version} parsing 이슈**

```
java.lang.IllegalArgumentException: Unable to parse '/usr/hdp/${hdp.version}/mapreduce/mapreduce.tar.gz#mr-framework' as a URI, check the setting for mapreduce.application.framework.path
...
...
Caused by: java.net.URISyntaxException: Illegal character in path at index 11: /usr/hdp/${hdp.version}/mapreduce/mapreduce.tar.gz#mr-framework
```


찾아본 결과 pig 실행할때 hdfs 경로에 있는 /usr/hdp/${hdp.version}/mapreduce/mapreduce.tar.gz 파일을 읽어야 하는것 같은데, pig가 ${hdp.version} 문장을 parsing 하지 못하는 것 같다.



그래서 ambari에 mapreduce config에 있는 mapreduce.application.framework.path 값이 `/usr/hdp/${hdp.version}/mapreduce/mapreduce.tar.gz` 로 기본 셋팅 되어있는데, 이를 아래 처럼 바꾼다.

`/usr/hdp/3.1.4.0-315/mapreduce/mapreduce.tar.gz`



#### 참고

http://develop.sunshiny.co.kr/1044



<hr>



**pig 실행 도중 ${hdp.version}을 인식하지 못하는 이슈**

pig 실행 도중 실패했는데, Yarn에 찍힌 log는 아래와 같다.

```
/usr/hdp/${hdp.version}/hadoop/lib/hadoop-lzo-.6.0.${hdp.version}.jar:
/etc/hadoop/conf/secure: bad substitution
```



해당 이슈는 ${hdp.version}을 인식하지 못하는것으로 보였고, 이는 JAVA_OPTS 값에 아래 hdp.version값을 명시해주어야 한다.

`JAVA_OPTS="${JAVA_OPTS} -Dhdp.version=3.1.4.0-315"`



#### 참고

https://stackoverflow.com/questions/32341709/bad-substitution-when-submitting-spark-job-to-yarn-cluster









