### copyFile 이슈

<hr>



 beeline을 통해 hive에 접속 후 생성된 Table에 `LOAD DATA INPATH`를 했을 때 아래와 같은 이슈가 발생한다.

```
hive copyFiles: error while checking/creating destination directory
```



위 에러는 보통 권한 문제로 발생하지 않는것으로 보인다.

먼저 Hive Table의 meta 정보를 확인한다.

```
> desc formatted <Table name>
```

해당 Table의 meta 정보가 출력이 되는데, `Location`와 `Owner`를 본다.



먼저, `Location` 에 디렉토리 권한이 Owner와 동일한지, 또는 write 권한이 있는지 확인한다.

권한의 문제가 없다면, beeline으로 hive 서버에 접속할 때 계정을 parameter (-n 옵션)로 같이 넣어준다.

```
> /bin/beeline ... -n Owner
```

