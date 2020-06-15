## 에러 메시지

Circular view path [welcome]: would dispatch back to the current handler URL [/welcome] again. Check your ViewResolver setup! (Hint: This may be the result of an unspecified view, due to default view name generation.)



스프링 초기 설정 시 위와같은 에러가 발생해 .html파일로 넘어가지 않는 현상이 있음.

이는 thymeleaf 의존성을 추가함

```
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

