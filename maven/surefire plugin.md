## surefire plugin



unit test의 결과를 txt, xml 포멧으로 제공되며, 파일은 ${baseDir}/target/surefire-reports 경로에 생성된다.



만약 surfire를 사용하고 싶지 않다면

`mvn -Dsurefire.useFile=false clean test`

or

`pom.xml` 파일 아래 구문을 추가한다.

```
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.9</version>
            <configuration>
                <useFile>false</useFile>
            </configuration>
        </plugin>
    </plugins>
</build>
```



https://ys87.tistory.com/entry/Maven-Surefire-Plugin

https://stackoverflow.com/questions/7016263/how-do-i-configure-maven-to-print-junit-assertion-failure-message-to-console