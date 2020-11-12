### Erasure-Coding 설정

<hr>

Erasure-Coding은 Hadoop 3.0 이상부터 적용가능하다.

 Erasure-Coding은 파일을 N개의 블록으로 나누면서 N의 절반인 M개의 Parity 블록을 생성해 Fault-tolerance를 보장하는 방식.

기존 Replica 3 방식보다 공간 효율성은 50% 이상 좋아지지만, 추가 Encoding, Decoding 비용 (CPU 비용)과 더불어 블록을 Rack 단위로 분포하기 때문에 네트워크 비용이 추가로 든다.

추가 CPU 비용은 ISA-L Coder를 사용함으로써 어느정도 해결이 가능하다. (디폴트는 Java Coder)



**사용**

```
> hdfs ec [option]
```

기본 옵션들

- -setPolicy -path <path> [-policy <policyName>] [-replicate]
  - 특정 hdfs directory에 Erasure Coding을 적용한다. 
  - -policy는 여러 ES 방법 중 하나를 선택하며, 디폴트는 RS-6-3-1024K이다.
  - -policy, -replicate는 동시에 적용할 수 없다.

- -getPolicy -path <path>
  - 특정 hdfs directory에 적용된 ES 정책이 무엇인지 출력한다.
- -listPolicies
  - 모든 ES 정책들을 출력한다. (RS-10-4-1024K, RS-3-2-1024K, RS-6-3-1024K 등등)
  - 정책들은 기본적으로 DISABLED 상태인데, 이를 사용하기 위해 -enablePloicy를 통해 ENABLED로 바꿀 수 있다.
- -addPolicies -policyFile <file>
  - 기존 ES 정책 외에 Custom 정책을 추가할 수 있다.
  - etc/hadoop/user_ec_policies.xml.template에 기본 template이 있다.



참고로 기존 hdfs directory 경로에 -setPolicy를 적용한다고 directory내 있는 파일들에 EC 정책이 적용되지 않는다.

즉, EC 정책을 적용 후 저장되는 파일들에 대해서만 Replica 기반이 아닌 EC 기반으로 저장된다.



**ISA-L 코더 사용**

https://github.com/intel/isa-l

ISA-L 코더를 사용해 Erasure Coding의 성능을 높일 수 있다. 디폴트 설정이 아니기 때문에 Enable 상태로 해주어야 한다.

Git에 나와있는데로 진행하면 /usr/lib/ 경로에 ISA-L library가 생성된 것을 볼 수 있다.

> libsial.so.2

이후 해당 library를 /lib64로 복사해준다.



**ISA-L 코더 설정 확인**

```
> hadoop chacknative
```

위 명령을 통해 `ISA-L: true /lib64/libisal.so.2`를 확인할 수 있다. 

이는 ISA-L 코더를 사용할 수 있음을 의미한다.



**Replica --> EC**

기존 Replica로 운영되던 파일들 EC로 변경하기 위해 distCP를 이용한다.

```
> hadoop distcp -overwrite -pb -skipcrccheck <replica_path> <ec_path>
```

EC는 주로 사용 빈도수가 월/년 에 몇번 사용하지 않는 Cold, Frozen 데이터에 적용한다. 



```
> hadoop distcp -Dmapred.job.queue.name=root.default -overwrite -pb -skipcrccheck <replica_path> <ec_path>
```

yarn queue setting




### 참고

http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html