### Queue 비워지지 않는 이슈

<hr>


Nifi Processor간 연결 후에 에러가 발생했을 때, Queue를 비우고 싶을때가 있다.

보통 오늘쪽 버튼을 누르고 `Empty queue`를 선택하면 Queue가 비워지지만 비워지지 않는 경우게 있다.



이럴땐, Queue의 `Configuration`에 들어가 FlowFile Expiration을 설정해준다. 

- 디폴트는 0초로 되어있는데 이는 FlowFile을 Queue에 계속 담아두겠다는 의미이다.
- 적절한 Expiration을 설정하여, FlowFile의 Queue을 비워주도록 한다.

