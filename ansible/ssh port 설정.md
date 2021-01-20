### ssh port 설정

<hr>
필요한 template을 생성후 playbook 실행시 아래 이슈가 발생한다.

```
UNREACHABLE! ..
Failed to connect to the host via ssh: ssh: connect to host localhost port 22: Connection timed out
```



현재 접속하고자 하는 서버의 ssh port를 확인해야하며, 만약 ssh port가 22가 아닌 경우 아래 template에 `Extra Variables에 ssh port 파라미터`를 넣어주면 된다.

```
---
ansible_ssh_port: 6879
```

