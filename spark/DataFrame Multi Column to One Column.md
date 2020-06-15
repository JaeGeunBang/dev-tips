# DataFrame Multi Column to One Column



DataFrame은 여러 Column을 가질 수 있는데, 이를 1개의 Column으로 변환후 저장해야 하는 경우가 있다.

- Text File Format으로 Write하기 위해
- Kafka에 Write 하기 위해 ( kafka에 write하기 위해서는 value column이 있어야 한다.)



**코드**

```scala
val df2 = df
	.map(_.toSeq.map(_+"").reduce(_+"\t"+_))
	.toDF()

df2.write...
```

- Dataframe각 row의 column을 Reduce하는데, 각 Column은 `\t`으로 구분한다.

- 변환 후 DataSet 형태로 변하며, 이를 다시 toDF()를 통해 DataFrame으로 바꾼다.



