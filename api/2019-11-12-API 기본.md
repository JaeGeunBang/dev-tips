### API 기초

<hr>

API란 두 개의 시스템이 서로 상호 작용하기 위한 인터페이스를 뜻함.

- 데이터를 주고 받는 인터페이스
- API는 보통 REST API를 지칭한다.
- 예를 들어 내 컴퓨터에 있는 계산기 프로그램은 계산 관련 API를 제공해준다고 볼 수 있다.



Web API는 웹을 통해 외부 서비스들로부터 정보를 불러오는 API.

- 내 컴퓨터에 있는 프로그램이 아닌 외부에 있는 서비스들의 정보를 받을 수 있다.
  - 특정 경로 어느 서버에 리퀘스트 메시지를 전송한다.
  - 해당 서버는 받은 내용을 바탕으로 데이터를 리턴한다.
  - 데이터 타입은 JSON, XML, CSV 등이 있다.
- 웹 사이트는 HTTP 프로토콜을 사용하는 REST API 기반으로 구축되어 있다고 볼 수 있다.



**API 접근권한**

Authentication

- 해당 사용자의 정체를 증명한다.

Authorization

- API를 통해 어떠한 액션을 허용한다.



API가 Authentication 했더라도, 어떠한 액션에 대해서는 Authorization을 허용하지 않을 수 있다.

- A 사용자는 API 사용 권한은 있지만, 데이터 등록만 가능하다. (데이터 삭제는 불가능...)



**API Key란**

- 보통 Request URL 이나 Request Header에 포함하는 긴 스트링을 뜻함.
- Request URL은 보안 요청을 할 때 API Key를 URL을 통해 요청한다.
  - 예제로 구글 MAP이 있다.
- Basic Auth는 username:password와 같은 Credential을 Base64로 인코딩한 값을 Request Header에 포함한다. 직접 API 서버에 요청을 보낸다.

- 최근 가장 많이 사용하는 보안 방법은 OAuth 2.0 (서비스가 클라이언트에게 동의를 받은 후 동의를 받은 유저에게 서비스를 제공한다(?))



**EndPoint 와 Methods**

- ENDPOINT: Resource를 액세스 하는 경로 / 방법 (``/v1/artists/{id}``)
- Methods: 자원 접근에 허용된 행위 (GET, POST, PUT, DELETE 등)
  - `GET` 해당 리소스를 조회하고 정보를 가져온다.
  - `HEAD` GET 방식과 동일하나 응답 코드와 HEAD만 가져온다.
  - `PUT` 요청된 리소스를 생성한다.
  - `DELETE` 요청된 리소스를 삭제한다.
  - `POST` 요청된 리소스를 업데이트한다.



**Parameter**

- 4가지 종류의 파라미터
  - Header: Authorization
  - Path: 특정 ID 값, ? 전에 나오는 부분
  - Query String: ? 후에 나오는 부분
  - Request Body: Request Body 포함되는 Parameter로 주로 JSON 형태



**예제 - Spotify API** https://developer.spotify.com/documentation/web-api/

- Basic Auth를 통해 직접 Client가 Spotify API에 접근해 데이터를 가져온다.
- 홈페이지에 REFERENCE를 클릭하면 API ENDPOINT를 볼 수 있다. (특정 데이터를 어떻게 요청해야하는지 참조 문서)





