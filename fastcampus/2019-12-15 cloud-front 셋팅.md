**Cloud-front 셋팅**



https://console.aws.amazon.com/cloudfront/home?#distributions:

Client가 S3에 있는 Index.html에 접근하는 것을 앞단에 Cloud-front가 제어할 수 있다.



Cloud-Front 서비스에 들어가 생성을 누른다.

- Select delivery method는 web으로 한다.
- Create distribution (현재 필요한 옵션만)
  - Origin Setting
    - Origin Domain Name - 앞서 생성한 S3 버킷을 선택한다.
    - Restrict Bucket Access - S3 버킷에 접근하기 위해선 무조건 Cloud-Front를 통해서만 접근할 수 있게 한다. (객체 엔드포인트론 접근할 수 없게 한다. 일반적으로 서비스 런칭할때 이렇게 해야한다.) 일단 No로 한다.
  - Default Cache Behavior Setting
    - Object Caching - Use Origin Cache Headers를 하면 Cache에 대한 컨트롤을 S3에서 관리하겠다는 의미인데, 보통은 Customize를 통해 Cloud-Front에서 관리할 수 있게 한다. 



이후 General - Domain Name에 있는 host를 입력하면, 연동한 index.html에 접근하는 것을 볼 수 있다.



