### Nifi 가이드

<hr>

1. Nifi는 초당 몇 건 처리와 같은 디테일한 처리가 불가능함.
   - Processor의 스케줄링 처리는 가능하지만, "초당 몇 건씩 처리해라"와 같은 디테일한 처리는 불가능.
     - 예를 들어, API Server에 초당 100건만 요청할 것. 



2. Groovy 스크립트 
   - Groovy 스크립트는 자바 기반의 스크립트 
   - 인텔리제이 같은 IDE에서 작업 후 코드 복사



3. Attribute, Contents의 차이 
   - Attribute는 FlowFile의 Key/Value 형태의 데이터.
     - 주로 속성 정보들이 저장된다.
   - Content는 FlowFile의 Content.
   - Attribute는 데이터 조작하기가 쉽지만, 나중에 Kafka, HDFS, ES에 데이터를 input할 때는 Content로 변형해야함. 
     - 즉, 데이터 조작은 Attribute 에서 하며 모든 작업이 끝난 후 Attribute를 Content로 변형 후 Write 할 것. 



4. Nifi invokeHTTP의 GET은 body를 붙일 수 없음. 
   - 대부분에 많은 시스템들이 GET에 body를 붙일 수 없도록 설계되고 있음. 



5. if 문을 수행하고 싶으면 RouteOnAttribute processor를 사용하면 됨 