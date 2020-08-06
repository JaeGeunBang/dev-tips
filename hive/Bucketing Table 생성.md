### Bucketing Table 생성

<hr>


Bucket Table을 만들기 위해 아래와 같이 입력한다.

```
​```
PARTITIONED BY (dt)
CLUSTERED BY (event) SORTED BY (user_id) INTO 32 BUCKETS
        STORED AS ORC;
```



CLUSTERED .. 이부분부터 Bucketing 할 Field를 입력한다. (=event)

이후 정렬하고 싶은 Field를 써주면 되는데, 필요 없다면 굳이 쓰지 않아도 된다. (=user_id)

INTO 32 BUCKETS은 event field를 32개의 BUCKETS으로 만들겠다는 의미이다. BUCKET의 수를 정하기 전에 미리 event field의 들어가는 `값의 종류가 몇개인지 세보면 좋다.`



**Insert**

Bucket된 Table에 data를 넣기 위해 LOAD 와 같은 방법으로 넣을 수 없다. `INSERT OVERWRITE`를 써야한다.

```
INSERT OVERWRITE TABLE bucket_table 
PARTITION (dt)
       SELECT firstname,
        lastname ,
        address ,
        city,
       state,
        post,
        phone1,
        phone2,
        email,
        web,
        country   
        FROM temp.table;

```



INSERT OVERWRITE를 위해 `temp.table`을 임시로 만든다. temp.table은 EXTERNAL Table로 만들고 값만 bucket_table에 insert 한 이후에 바로 Drop 해주는게 좋다.



이후 bucket table의 hdfs 경로에 들어가보면 `../bucket-00.. ` 와 같이 bucket 별로 파일을 저장하는 것을 볼 수 있다.



### 참고

https://data-flair.training/blogs/bucketing-in-hive/