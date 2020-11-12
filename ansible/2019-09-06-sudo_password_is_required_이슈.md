### sudo_password_is_required, not_writable 이슈

<hr>

Ansible의 Web UI인 awx에서 각 서버에 배포할 때 아래 이슈가 발생했다.

> fatal: [xxx0?]: FAILED! => {"changed": false, "failed": true, "module_stderr": "Connection to xxx0? closed.\r\n", "module_stdout": "sudo: a password is required\r\n", "msg": "MODULE FAILURE", "rc": 1}



해당 이슈는 서버에 접속을 못하는 것은 아니지만, 내부적으로 sudo가 필요한 명령어를 수행할 때 위와 같은 에러가 발생한다.



**해결방법**

```
> vim /etc/sudoers
```

각 머신 접속 하려는 계정에 NOPASSWD:ALL 권한을 부여하면된다.

```
<계정>	ALL=(ALL)	ALL

--> 아래처럼 바꾼다.

<계정>	ALL=(ALL)	NOPASSWD: ALL
```



또한, 파일을 배포할 때 특정 경로에 파일을 복사하지 못할때가 있는데 이는 계정에 대한 root 권한을 주어야함.

아래 playbook 파일에 `become:yes`를 추가해준다.

```
---
- hosts: all
  become: yes
  
  tasks:
  - name: td-agent.conf copy
    copy:
        src: td-agent.conf
        dest: /etc/td-agent/
        remote_src: no
```

