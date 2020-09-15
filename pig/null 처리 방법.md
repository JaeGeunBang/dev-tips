### null 처리 방법

<hr>
pig에서 hive table을 읽는 방법을 아래와 같다.

```
> pig -useHCatalog

...

graunt> A = LOAD 'database.table' USING org.apache.hive.hcatalog.pig.HCatLoader();
graunt> B = filter A by date == '20200819';
```



위와같이 읽은 후 `FOREACH` 구문을 실행할 수 있는데, 만약 NULL이 들어가 있는 Column이 있다면, 해당 Column은 FOREACH 구문에서 Filtering 된다.

```
graunt> C = FOREACH B GENERATE col1 as new_col1;
```

위처럼, col1에 NULL값이 들어있다면, NULL은 자동 Filter가 되어서 `new_col1` Column이 만들어진다.

만약, NULL 값도 분석에 활용을 하고 싶다면, 위와같이 Filter가 되어서 안되기 때문에, 아래와 같이 NULL은 문자열로 바꿔준다.

```
graunt> C = FOREACH B GENERATE (col1 is null ? 'NULL':col1) AS new_col1;
```

