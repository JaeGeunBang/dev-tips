### Materialized View 생성, 이슈

<hr>


사전에 original_table은 transactional 특성을 true로 해주어야 한다.

```
> ALTER TABLE original_table SET TBLPROPERTIES('transactional'='true');
```



hive에서 materialized view를 생성하기 위해 아래와 같이 선언한다.

```
CREATE MATERIALIZED VIEW mv_table
AS 
  SELECT originl_col1 as col1 , original_col2 as col2
  FROM original_table;
```



`desc formatted mv_table`을 통해 Table Type이 `MATERIALIZED_VIEW` 인것을 확인할 수 있다. 



최신 데이터를 반영하고 싶다면, Rebuild를 수행한다.

```
> ALTER MATERIALIZED VIEW mv_table REBUILD ;
```

이를 주기적으로 수행하고 싶다면 아래 옵션을 넣어야 한다. (10분에 한번씩)

`hive.materializedview.rewriting.time.window=10min`



### 이슈

<hr>



Materialized view 생성시 아래와 같은 이슈가 발생한다.

```
SemanticException 0:0 Error creating temporary folder on: maprfs:/user/hive/warehouse/wh_db.db. Error encountered near token 'TOK_TMP_FILE'
```

해당 경로에 임시파일을 write 하지 못하는 이슈이기 때문에, hdfs permission 을 확인해야 한다.

