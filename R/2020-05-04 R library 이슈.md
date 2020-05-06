### R library 이슈

<hr>



R을 설치 후 실행하다보면 아래와 같은 Library를 찾지 못하는 이슈가 발생한다.

```
> unable to load shared object rlang.so
```



R command 실행 후, library 경로 확인

```
> .libPaths()

[1] ...
[2] ...
```

경로가 2개가 나오는데, 1번은 특정 계정에서 사용하는 library 경로인것 같고, 2번은 공용으로 사용하는 library 경로인것으로 보인다.



1번 경로로 가서 rlang.so가 있는지 확인 후 없다면 설치한다.

```ㅇ
> install.packages("rlang")
```



만약 특정 function을 못찾아 lib 경로를 R scripts 내에서 지정하고 싶다면, 아래와 같이 입력한다.

```
> could not find function "summarise"
```



summarise를 수행하는 R library가 무엇인지 확인 후, R scripts 내 `lib 명`과 `위치`를 명시한다.

```
library("dplyr", lib.loc="<위 1번 경로>")
```



### 참고

https://stackoverflow.com/questions/15170399/change-r-default-library-path-using-libpaths-in-rprofile-site-fails-to-work





