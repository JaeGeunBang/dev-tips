## Vue axios에서 Spring Boot의 RestController 네트워크 이슈

.vue

```
axios.get('localhost:8080/api/search/one').then(response => {this.todos = response})
```



Spring boot을 통해 실행 중인 톰캣 서버 (8080)에 api 호출을 수행했을 때, Network Error 이슈가 발생한다.
이를 해결하기 위해, Spring Boot에서 CORS Annotaion을 추가해주어야 한다.

```java
@CrossOrigin // 추가
@RestController
public class RestController {
}
```