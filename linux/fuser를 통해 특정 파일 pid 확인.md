### fuset - 파일, port의 pid 확인

<hr>


특정 파일에 특정 PID가 write하고 있는데, 이를 조회하고 싶을때 `fuser`를 통해 알 수 있다.

**파일을 통한 pid 확인 방법**

```
> fuser -v /path/test.log
```

- 옵션
  - v: 자세한 출력 모드 (USER, PID, ACCESS, COMMAND)를 보여준다.



ACCESS의 의미

- c: 현재 디렉토리를 뜻함
- e: 실행 가능함을 표시함
- f: 열려진 파일을 뜻함.
- r: root 디렉토리를 뜻함.



**Port를 통한 pid 확인 방법**

```
> fuser -n tcp 8080
```

8080 포트를 실행하는 pid를 찾음