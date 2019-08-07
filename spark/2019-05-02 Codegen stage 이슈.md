> Compiling "GeneratedClass": Code of method

해당 이슈는 Catalyst가 Java Program을 컴파일 후 바이트코드로 변경하는데, 이때 1개 메서드의 바이트코드 크기가 64KB를 넘어서면 발생하는 에러이다.

스파크 어플리케이션 제출 때 아래 config를 추가함.

> spark.sql.codegen.wholeStage = "false"



### 참고

https://stackoverflow.com/questions/50891509/apache-spark-codegen-stage-grows-beyond-64-kb