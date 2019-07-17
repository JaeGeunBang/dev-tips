### retention 설정

<hr>

Prometheus는 time series DB이며 클러스터를 구성해 운영하지 않다보니, 데이터를 무제한으로 저장하기에 적합하지 않다.

이는 retention flag를 통해 저장할 크기나 기간을 설정할 수 있다.



retention 관련 flags

- --storage.tsdb.retention.size
  - retention의 size를 설정할 수 있다.
- --storage.tsdb.retention.time
  - retention의 시간을 설정할 수 있다. 디폴트는 15일 이다.
- *--storage.tsdb.retention*
  - 없어질 flag이므로 사용하지 않을 것



retention.size와 time 중 하나만 설정할 수 있고, 둘 다 모두 설정할 수 있다. 둘 모두를 설정할 경우 먼저 발생하는 flag에 따라 데이터 보관을 결정한다.

만약 size는 100GB, time은 15d 일 때, 데이터 사이즈가 100GB가 넘어가면 보관 주기가 15일이 되지 않아도 삭제된다.



#### 사용

```
./prometheus --storage.tsdb.retention.size=100GB --storage.tsdb.retention.time=15d
```



