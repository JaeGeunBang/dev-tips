### Nginx 테스트

<hr>



**GET**

GET 테스트를 위해 웹 브라우저에서 아래와 같이 입력한다.

```
http://localhost:8000/v1/event?id=jgb710&data=test
```



**POST**

POST 테스트를 위해 command 창에서 아래와 같이 입력한다.

```
curl -d "id=jgb710&data=test" -X POST http://localhost:8000/v1/event
```

