### invalid configuration of tez jars

<hr>



Tez로 실행시 아래와 같은 이슈가 발생했다.

```
: org.apache.spark.sql.AnalysisException: java.lang.RuntimeException: org.apache.tez.dag.api.TezUncheckedException: Invalid configuration of tez jars, tez.lib.uris is not defined in the configuration;
```



해당 이슈는 `tez-site.xml` 에 tez.lib.uris를 설정해주면 된다.

```
<property>
  <name>tez.lib.urls</name>
  <value>/path/tez.tar.gz</value>
</property>
```

참고로 path는 HDFS path이다. hdfs path에 해당 파일이 있는지 확인한다.