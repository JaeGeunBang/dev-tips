### hadoop distcp 이슈

<hr>


hadoop distcp 를 아래와 같이 수행했을때,

```
> hadoop distcp /logs/source /logs/desc
```



아래와 같은 이슈가 발생한다.

```
Check-sum mismatch between hdfs://... and hdfs://...
```

아무래도 source, desc 사이의 check-sum 체크 결과 실패했다는 의미로 보인다.



이를 위해 아래와 같이 distcp를 수행한다.

```
> hadoop distcp -update -pb -skipcrccheck /logs/source /logs/desc
```

`checksum-check`는 skip할 수 있으나 이는 문제가 생길수 있어서, `-pb` 옵션을 통해 block-size를 보존할 수 있다. 만약 보존하지 않는다면 복사시 데이터 유실이 발생할 수 있다.



크게 복사하는 방법은 크게 2가지가 있다.

- `-update` (default)
  - source, destination의 blocksize, checksum, size가 서로 다를 경우 overwrite 한다.
  - **blocksize, checksum, size가 완전 똑같은 파일이 있다면 무시하고 그렇지 않는 파일들만 덮어씌운다는 의미**.
  - 참고로 Sync를 위한 operation이 아니다.
- `-overwrite`
  - destination으로 그냥 overwrite 한다.
  - **같은 파일이 있든간에 그냥 덮어씌운다는 의미**



예제)

- source (filename / size)
  - 1 / 32 MB
  - 2 / 32 MB
  - 10 / 64 MB
  - 20 / 32 MB
- dest (filename / size)
  - 1 / 32 MB
  - 10 /32 MB
  - 20 / 64 MB
- 결과
  - `-update` 1은 skip (file size, content 같기 때문), 2는 copy (없어서) 10, 20 은 overwrite (content가 다르기 때문)
  - `-overwrite` 1,2,10,20 모두 overwrite
  - `-update -append` 10은 overwrite (source 파일 size가 dest보다 더 작기 때문), 20은 append (source 파일 size가 dest보다 더 크기 때문)
    - `-append`는 `-update`랑 같이 쓰인다.



<hr>

distcp 수행 중 memory 이슈가 발생했다.

```
15/01/31 16:03:58 INFO mapreduce.Job: Task Id : attempt_1422733582475_0003_m_000008_0, Status : FAILED
Container [pid=22881,containerID=container_1422733582475_0003_01_000011] is running beyond physical memory limits. Current usage: 1.0 GB of 1 GB physical memory used; 3.6 GB of 2.1 GB virtual memory used. Killing container.
...

Container killed on request. Exit code is 143
Container exited with a non-zero exit code 143
```



distcp 수행시 아래와 같이 추가 parameter를 수행한다.

```
hadoop distcp -Dmapreduce.map.memory.mb=3000 -Dmapreduce.reduce.memory.mb=6000 ...
```





### 참고 

https://hadoop.apache.org/docs/current/hadoop-distcp/DistCp.html

https://community.cloudera.com/t5/Support-Questions/Container-Memory-Error-Hadoop-CDH-5-2/td-p/24265