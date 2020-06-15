실제 스파크 어플리케이션 (WordCount) 작성 후 이클립스에서 수행 시 위와 같은 에러가 발생한다.

>  Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 10582



이 이슈는 파라미터 version에 따른 이슈라 하며, 아래 dependency를 추가하면 된다.

```
<dependency>
  <groupId>com.thoughtworks.paranamer</groupId>
  <artifactId>paranamer</artifactId>
  <version>2.8</version>
</dependency>
```



### 참고

https://stackoverflow.com/questions/53315677/spark-java-saveastable-failes-with-arrayindexoutofboundsexception