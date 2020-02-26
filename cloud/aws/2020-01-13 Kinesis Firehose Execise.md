### Kinesis Firehose Execise

<hr>



필요한 서비스


- Kinesis Firehose, S3, EC2(Kinesis Agent)



Kinesis Firehose, S3 생성한다. (Default Option)

- Firehose는 Destination을 S3로 설정한다.
- S3 설정 중에 Buffer Size, Buffer Interval을 설정할 수 있다. 
  - Buffer Size는 최대 Firehose를 통해 보낼 수 있는 사이즈이다. 여기선 5 MB로 설정한다.
  - Buffer Interval은 FIrehose가 interval 단위로 보낼지 결정한다. 여기선 60으로 하며, 1분 단위로 데이터를 전송한다는 의미이다. (Firehose는 준실시간이기 때문에 60초 미만으론 떨어질 수 없다.)
- S3는 Unique한 Butket 이름으로 설정한다.
- 이후 EC2를 띄우고, 필요한 설정을 마무리 한다.



Kinesis Agent 설치

```
sudo yum install -y aws-kinesis-agent
```



LogGenerator 설치 후 실행

```
wget http://media.sundog-soft.com/AWSBigData/LogGenerator.zip
unzip LogGenerator.zip
chmod a+x LogGenerator.py
sudo mkdir /var/log/cadabra

cd ~
sudo ./LogGenerator.py 500000
cd /var/log/cadabra # 파일 생성 확인
```



Kinesis Agent 수정

```
cd /etc/aws-kinesis/
vim agent.json
```

Kinesis Firehose에 들어가 생성한 Firehose의 `Delivery stream ARN`을 확인한다.



**agent.json**

```
{
  "cloudwatch.emitMetrics": true,
  "kinesis.endpoint": "",
  "firehose.endpoint": "firehose.us-east-1.amazonaws.com",

  "awsAccessKeyId":"",
  "awsSecretAccessKey":"",

  "flows": [
    {
      "filePattern": "/var/log/cadabra/*.log",
      "deliveryStream": "PurchaseLogs"
    }
  ]
}
```

위 awsAccessKeyId, awsSecretAccessKey는 넣을 수 있지만, Config 파일에 직접 넣는 것은 권장하지 않으며 이를 위해 IAM Role을 변경해주는 것이 좋다.

- EC2에 IAM Role을 새로 만든다. (AdministratorAccess)
- 해당 권한은 EC2를 통해 모든 AWS Service를 접근할 수 있도록 제공한다.
  - 즉, Agent가 실행하는 EC2에서 Kinesis Firehose에 데이터를 전송하기 위해 `관리자 권한`을 주겠다는 의미이다.



서비스 실행

```
sudo service aws-kinesis-agent start
```



이후 `/var/log/aws-kinesis-agent/aws-kinesis-agent.log` 경로에 로그를 수집하는 것을 볼 수 있다.

최종 S3에 로그가 저장된 것을 확인할 수 있다.



### 참고

https://aws.amazon.com/ko/kinesis/







































