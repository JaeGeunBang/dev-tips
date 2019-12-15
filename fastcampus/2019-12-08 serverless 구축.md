### serverless 구축

<hr>

참가 신청 어플리케이션 흐름

1. 참가신청 화면 (신청서 작업 및 전송)
2. 신청내역 화면 (신청내역 리스트업)
3. 신청결과 화면 (참가증 확인)



필요한 서비스 분포도

- SNS (특정 람다에게 이벤트 트리거 역할 (=업무 배정))
- Lambda
- S3 (정적 포스팅을 위함 - 이미지 데이터 등)
- DynanmoDB (데이터 적재 용도)
- CloudFront (CDN 역할 (캐시))
- API Gateway (프록시 역할)



호스팅 아키텍처

- Client --> CloudFront --> S3



비즈니스 아키텍쳐

- 참가 조회
  - API Gateway -> Lambda (**Get data**) -> DynamoDB
- 참가 신청 입력
  - API Gateway -> Lambda (**submit**) -> DynamoDB, SNS (뒤에 붙은 알람들을 트리거 하기 위함)
  - SNS, DynamoDB -> Lambda (**Make Image**) -> S3 (알람을 받아 이미지를 만들어 이를 S3에 저장)



## 환경 설치

```bash
docker run -it amazonlinux bash # docker를 통해 amazonlinux bash를 띄운다.
yum update -y # yum update
yum install python3 -y # python3 install
pip3 install virtualenv # 도커 내 여러 가상환경을 띄우기 위함 (각 환경들을 고립시켜주기 위함)
mkdir venv # 작업할 디렉토리 생성
virtualenv -p /usr/bin/python3 py37 # py37이라는 가상 환경을 생성 (python 3.7을 사용하는 가상 환경을 띄움)
source py37/bin/activate # py37 가상환경에 진입
pip install awscli # awscli 설치
aws configure # aws 사용을 위해 configure를 입력해야한다. (액세스 키가 필요)
```



**액세스키를 위한 사용자 추가방법**

1. AWS IAM에 접속한다.
   Identity and Access Management

2. 그룹을 생성한다. 
   AdministratorAccess 권한을 부여한다. (어드민에 접속할 수 있는 권한)

3. 사용자를 생성한다.
   사용자의 그룹은 위에서 생성한 그룹을 선택한다.
   해당 사용자의 액세스 키와 시큐리티 키를 확인할 수 있으며, awscli를 통해 접속할 수 있다.

4. aws configure를 통해 액세스 키와 시큐리티 키를 입력한다.
   확인은 `~/.aws/credentials` 에서 확인한다.

> 참고) `aws configure --profile s3` --profile을 이용하면 액세스 키와 시큐리티 키를 분리되어 사용할 수 있다. 


