### Classpath 추가

<hr>


Pig에 외부 라이브러리를 추가하고 싶을 때 아래 여러 방법들이 있다.



1. PIG_CLASSPATH 환경 변수 추가

2. pig 실행 옵션 `pig -Dpig.additional.jars=jar1:jar2:jar3...`

3. .pig 코드 내 register <jar_path>



되도록이면, `pig-env.sh` 에 PIG_CLASSPATH 환경 변수 추가와 pig 실행 옵션을 넣어서 처리한다. 

***pig-env.sh***

````shell
JAVA_HOME=/usr/java/default/
HADOOP_HOME=${HADOOP_HOME:-/home/test/hadoop}
PIG_CLASSPATH="${PIG_CLASSPATH}"

PIG_OPTS="$PIG_OPTS -Dpig.additional.jars=/lib/jar1.jar:/lib2/jar2.jar"

if [ -d "/usr/lib/tez" ]; then
  PIG_OPTS="$PIG_OPTS -Dmapreduce.framework.name=yarn"
fi

for f in /lib/jar1.jar:/lib2/jar2.jar ; do
    PIG_CLASSPATH=${PIG_CLASSPATH}:$f;
done
````



register는 테스트 해보고 싶을 때 사용하면 좋은것 같다.

***test.pig***

```pig
register /lib/jar1.jar
register /lib/jar2.jar

...
```





