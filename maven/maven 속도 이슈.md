## Maven 속도 이슈



https://www.jrebel.com/blog/how-to-speed-up-your-maven-build

1. maven을 parallel 하게 build
2. 필요한 modules만 build
3. 인터넷 속도 제한(?)
4. java StartUp 속도 증가(?)



https://stackoverflow.com/questions/7074040/maven-failing-to-download-jar-dependencies

maven opt 환경 변수에 메모리를 높게 설정

`export MAVEN_OPTS="-Xmx1024m"`