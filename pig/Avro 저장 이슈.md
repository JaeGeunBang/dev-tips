### Avro 저장 이슈

<hr>


Pig를 통해 Avro 형태로 저장하고자 할때, Pig에서 AvroStorage()를 제공한다.

https://cwiki.apache.org/confluence/display/PIG/AvroStorage



아래와 같이 사용했을 때, 이슈가 발생했다.

**test.pig**

```
...
STORE logs INTO '$output'USING AvroStorage();
```

```
while trying to store in AVRO format: Datum 2 is not in union [“null”,“string”]
...
```



특정 column에 Type이 맞지 않아서 발생하는 이슈로 보인다. 그래서 아래와 같이 AvroStorage()에 스키마를 추가해 보았다.

```
...
STORE logs INTO '$OUTPUT' USING AvroStorage('schema', '
 {
  "type":"record",
  "name":"test",
  "fields":[
    {"name":"col1", "type":"string"},
    {"name":"col2", "type":"string"}
  ]
 }
');
```

위와 같이 스키마를 추가했을 때, 아래와 같은 이슈가 발생했다.

```
Avro="string"
Pig=col2:bytearray
```

Avro에서는 string으로 선언했지만, 실제 col2의 type은 bytearray였던 것이다. 그래서 "col2"의 type을 bytes로 바꾸고 났지만, 맨 처음 발생했던 이슈가 또 나타났다.



구글링 결과 Pig 내에서 특정 Column의 Type을 Implicit Cast 해야 하는것을 알게되었고, Col2의 Type도 ["null", "bytes"]로 바꾸어 해결했다.



**최종 test.pig**

```
logs = FOREACH basic_logs GENERATE
  col1 AS (col1:chararray),
  col2 AS (col2:chararray);


STORE logs INTO '$OUTPUT' USING AvroStorage('schema', '
 {
  "type":"record",
  "name":"test",
  "fields":[
    {"name":"col1", "type":"string"},
    {"name":"col2", "type":["null", "string"]}
  ]
 }
');
```

- Pig 내 Column type은 implicit cast 하자.
- Avro schema는 굳이 쓰진 않아도 되지만, 가독성을 위해서 쓰는게 좋을것 같다. `특정 Column이 어떤 Type`인지, `Output Schema를 한눈에 볼 수 있다.`



https://stackoverflow.com/questions/44499202/pig-script-error-while-trying-to-store-in-avro-format-datum-2-is-not-in-union