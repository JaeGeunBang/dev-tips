### hive table load

<hr>


pig 에서 hive table을 load하기 위해 아래와 같이 사용한다.

```
> pig -useHCatalog

...

graunt> A = LOAD 'database.table' USING org.apache.hive.hcatalog.pig.HCatLoader();
graunt> B = filter A by date = '20200819';
```

특정 날짜의 데이터만 읽고 싶다면, LOAD 이후에 filter를 따로 수행해야 한다. (성능이 이상이 없을려나..?)

- 실제 테스트 결과 바로 필터 작업을 수행하면, 필터 이후의 데이터만 읽는다.



**참고**

https://acadgild.com/blog/loading-and-storing-hive-data-into-pig