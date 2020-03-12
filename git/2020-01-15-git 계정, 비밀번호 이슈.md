### git 계정, 비밀번호 이슈

<hr>



**repository remote 시 Access Denied 이슈**

```
remote: HTTP Basic: Access denied
fatal: Authentication failed for 
```



인증 관련 데이터들을 초기화 하는 것이 좋다.

```
> 관리자 권한으로 git-bash 실행
> git config --system --unset credential.helper // system 적용
> git config --global --unset credential.helper // global 적용 (system 적용을 했을시 안될경우)
```

https://imitursa.tistory.com/3213





**username, password 없이 push 방법**

```
> git config credential.helper store
```

Credential 정보 저장을 위한 방법.

만약 일정 시간동안만 저장하고 싶다면 cache를 사용한다. 사용법은 아래 링크 참조

https://www.hahwul.com/2018/08/git-credential-helper.html

















