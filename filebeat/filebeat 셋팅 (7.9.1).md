## FileBeat 셋팅 (7.9.1)



서버 로그 수집을 위해 Filebeat를 셋팅하고 이를 Fluentd와 연동을 해보자.



**filebeat 셋팅**

먼저 Filebeat를 다운받는다. 

- https://www.elastic.co/kr/downloads/beats/filebeat

- 현재 `Centos` 환경이므로, RPM 64-BIT를 다운받는다.



Filebeat를 설치(`sudo rpm -ivh filebeat-7.9.1-x86_64.rmp`) 후 `sudo service filebeta status`를 통해 정상적으로 service가 등록되었음을 확인한다.



filebeat의 yml파일은 `/etc/filebeat/filebeat.yml` 경로에서 확인가능하며, output 설정을 Logstash로 설정한다.

> 참고로 filebeat는 fluentd output plugin이 따로 없으며, logstash output plugin을 사용하면 된다.

```
output.logstash:
  hosts: ["localhost:5044"]
```



**Fluentd 셋팅**

Filebeat가 전송하는 데이터를 받기 위해, Fluentd에 beats plugin(https://github.com/repeatedly/fluent-plugin-beats)을 설치한다.

- https://rubygems.org/ 에 접속 후 fluent-plugin-beats 를 찾아서 다운로드 한다.
- `sudo td-agnet-gem install *.gem` 명령을 통해 beats plugin을 설치한다.



아래 Fluentd .conf 파일과 같이 설정한다.

```
<source>
  @type beats
  metadata_as_tag
</source>

<match *beats>
  @stdout
</match>
```

실제 filebeat에서 전송하는 데이터가 `/var/log/td-agent/td-agent.log` 에 출력이 되는지 확인한다.