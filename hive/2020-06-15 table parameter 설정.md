### table paramter 설정

<hr>


hive table에 paramter를 넣는 방법은 아래와 같다.

```
create table ...
TBLPROPERTIES('paramter1'='value1', 'parameter2'='value2')
```



수정하고 싶다면 아래와 같이 한다.

```
alter table ...
SET TBLPROPERTIES('paramter1'='value1', 'parameter2'='value2')
```

