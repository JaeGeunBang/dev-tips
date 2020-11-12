### add chmod permissions file

<hr>


실제 linux 서버에 쉘 스크립트를 배포하려 하는데, 쉘 스크립트의 실행 권한을 주고싶을때.

```
> git update-index --chmod=+x ./file
```

권한을 뺄때

```
> git update-index --chmod=-x ./file
```



실제 commit을 해보면 `mode change 100644 => 100755` 로 바뀌었다는 것을 볼 수 있다. 실행 권한이 추가되었기 때문에 각 1씩 더해졌음.