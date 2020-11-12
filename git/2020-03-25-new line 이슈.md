### New line 이슈

<hr>


개발 환경이 window, linux 등 다르다 보면 New Line 이슈가 발생할 수 있다.

윈도우는 `CRLF`, Mac 이나 linux는 `LF` 문자만 사용하기 때문에, 윈도우로 개발한 `.sh`를 linux 환경에서 실행하려다 보면 `'\r' command` 를 찾을 수 없다는 이슈가 발생할 수 있다.

- 여기서 CR이 `\r`로 표현된다.

또한, git diff 할 때도 `^M` 이 각 라인 맨 뒤에 추가되며 수정하지 않은 라인 까지 +/- 되는 것을 확인할 수 있다.

- git에선 CR을 `^M`으로 표현하는것 같다.



가장 일반적인 방법은 sed 명령을 통해 \r을 공백으로 바꿔주는 방법이다.

```
> sed -i -e 's/\r$//' file.sh
```



허나 매번 이렇게 바꿔줄순 없기 때문에 아래 git 명령을 통해 바꿔준다.

```
> git config --global core.autocrlf true
```

해당 명령은 git 커밋할 때 CRLF를 LF로 변환하고, checkout 할때 LF를 CRLF로 자동으로 변환한다.

개발환경이 Window 인 경우에 위와 같이 설정하며, linux나 mac에선 사용할 필요 없다.



```
> git config --global core.autocrlf input
```

우연히 리눅스 환경에 CRLF가 들어간 파일이 있을 때, 또는 Window 환경에 LF가 들어간 파일이 있을 때, 해당 명령을 통해 git이 알아서 고쳐준다.

Window에서는 CRLF, Mac, Linux는 LF로 자동 변환해준다.



```
> git configg --global core.autocrlf false
```

해당 명령은 autocrlf를 사용하지 않을 때 사용한다.



https://www.snoopybox.co.kr/1613

[https://git-scm.com/book/ko/v2/Git%EB%A7%9E%EC%B6%A4-Git-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0](https://git-scm.com/book/ko/v2/Git맞춤-Git-설정하기)