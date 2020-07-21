### hive table load

<hr>


pig 에서 hive table을 load하기 위해 아래와 같이 사용한다.

```
> pig -useHCatalog

...

graunt> A = LOAD 'database.table' USING org.apache.hive.hcatalog.pig.HCatLoader();
```



**참고**

https://acadgild.com/blog/loading-and-storing-hive-data-into-pig