## td-agent 설치 by rpm without internet



1. https://www.fluentd.org/download 에 접속후 설치에 필요한 파일을 받는다.
   - OS 버전을 잘 확인하고 설치할 것 (CentOS 7버전이면 .rpm 파일을 받음)
2. 받은 파일을 설치하고자 하는 서버로 전송한다.



**설치**

```
sudo rpm -ivh td-agent-3.4.1-0.e17.x86_64.rpm
```

**삭제**

```
sudo rpm -qa | grep td-agent
sudo rpm -e td-agent
```


**필요한 plug-in 설치**

1. https://rubygems.org/ 에 접속후 필요한 plugin 을 다운 받는다. (.gem 파일)

2. Prometheus에 필요한 .gem 파일들

   - quantile.gem
   - prometheus.gem
   - prometheus-client.gem

3. plugin 설치

   ```
   sudo td-agent-gem install *.gem
   ```



**config 수정 및 실행**

config 경로

```/etc/td-agent/td-agent.conf```

log 경로

```/var/log/td-agent/td-agent.log```



