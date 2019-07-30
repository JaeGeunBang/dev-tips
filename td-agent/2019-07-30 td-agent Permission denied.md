### td-agent Permission denied

<hr>
td-agnet 에서 nginx 로그를 읽을 때 permission denied 에러가 뜨는 경우가 있다.

```
[error]: #0 Permission denied @ rb_sysopen - ...log
```



기본적으로 td-agent 의 user:group은 td-agent:td-agent로 설정되어 있기 때문에, 읽으려는 log의 퍼미션을 확인하거나 td-agent의 user을 바꿔주면 된다.



vim /etc/init.d/td-agent

```java
TD_AGENT_USER=nginx or root // nginx 또는 root로 바꿔준다.
TD_AGENT_GROUP=td-agent
```



이를 바꾸기 싫다면 log의 퍼미션에 read 권한을 부여한다.

```
sudo chmod 644 *.log
```



참고

http://bong8nim.com/post/programming/fluentd/fluentd-error-permission-denied/