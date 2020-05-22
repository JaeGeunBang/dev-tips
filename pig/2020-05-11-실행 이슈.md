### "expecting one of:" 이슈

<hr>


pig 실행 도중 아래와 같은 이슈가 발생한다.

```
Was expecting one of:
    <IDENTIFIER> ...
    <OTHER> ...
    <LITERAL> ...
    <SHELLCMD> ...
```



구글링해본 결과 pig 스크립트에 `;`가 빠져서 라고 하던데, 나는 정상적인 상황이였다.

하나씩 실행해본 결과, pig job을 실행할 때 아무도 선언하지 않는 환경 변수가 있는데 이때문에 발생한 이슈이다.



**기존**

```
$PIG_HOME/bin/pig ... -p input=${INPUT} ...
```

위 `input=${INPUT}`에서 $INPUT 환경 변수를 아무도 선언해 주지 않고 있었다. (기존에 사용중이던 환경 변수였는데 시간이 지남에 따라 사용하지 않게 된것 같다.)

그래서 위 필요없는 parameter를 제거한 후 정상 동작이 되는것을 확인했다.