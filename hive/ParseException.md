### ParseException

<hr>


hive table에서 select를 했을 때 아래와 같은 ParseException이 발생했다.

```
Hive: ParseException line 5:20 missing EOF at 'tabid' near ..
```

tabid Column의 오류인줄 알았는데, time 이름을 가진 Column 때문이였다.

time이나 timestamp는 hive에서 사용하는 예약어(?)로 생각이 된다. 그래서 그레이브 엑센트 (`)를 붙여 select 를 하니 정상 동작하는 것을 확인했다.

```
select tabid, `time` from table
```



되도록 다른 이름으로 바꾸는것도 좋을것 같다.



