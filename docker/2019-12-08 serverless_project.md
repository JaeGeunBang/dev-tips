### 참가신청 어플리케이션

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











