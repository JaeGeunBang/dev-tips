# crontab에 output file에 timestamp 추가

Crontab은 default shell에서 동작하지 않기 때문에 명령어 처리에 있어 shell과 약간 차이점이 있다.



shell에서 $(date +%Y%m%d_%H)와 같은 동작이 crontab에선 동작하지 않는다.

crontab으로 timestamp 가 붙은 log를 출력하고 싶을 때 아래와 같이 쓴다. (%앞에 \를 붙인다)

```
* * * * * command > /tmp/test.$(date +\%Y\%m\%d_\%H).log 2>&1
```



표준 출력, 표준 에러

```
>, 1> 는 표준 출력
2>는 표준 에러
2>&1은 표준 에러를 표준 출력과 동일하게 사용
```

cat test.txt > stdout.txt 

> stdout.txt로 표준 출력

cat test.txt >2 stderr.txt

> stderr.txt로 표준 에러 출력

cat test.txt > stdout.txt 2>&1

> stdout.txt로 표준 출력, 표준 에러 출력

cat test.txt > stdout.txt 2> stderr.txt

> stdout.txt로 표준 출력, stderr.txt로 표준 에러 출력



## 참고

https://blogger.pe.kr/369

https://superuser.com/questions/38278/how-can-i-add-a-timestamp-to-the-end-of-a-cron-jobs-output-file-name