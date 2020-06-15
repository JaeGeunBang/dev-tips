### ssh 접속 이슈

<hr>


ssh 접속 시 아래 메시지가 뜨며 접속이 되지 않는다.

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
~~~
Please contact your system administrator.
Add correct host key in /home/jgb710/.ssh/known_hosts to get rid of this message.
Offending key in /home/jgb710/.ssh/known_hosts:73
RSA host key for [web26.start.lego]:6879 has changed and you have requested strict checking.
Host key verification failed.
```



/home/jgb710/.ssh/known_hosts에 `예전에 접속했던 서버의 공개키`가 저장되는데, 서버의 정보가 바뀌면서 이전 공개키로는 접속할 수 없다는 이슈이다. 즉, 해당줄을 삭제하면 다시 공개키를 받게 된다.