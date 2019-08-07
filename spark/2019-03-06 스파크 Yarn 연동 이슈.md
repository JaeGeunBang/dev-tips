스파크를 Yarn에 제출했을 때 아래 에러가 발생하는데 , 이는 아래 Yarn 설정을 해준다.

> Comtainer is running beyond memory limits



아래 부분을 추가하면 "yarn.nodemanager.vmem-pmem-ratio에서 설정한 가상메모리 사용 제한값(기본값 2.1 = 각각 맵/리듀스 작업시 mapreduce.map.memory.mb/mapreduce.map.memory.mb에서 설정한 값의 2.1)를 초과하여 가상메모리 사용시 프로세스를 자동으로 kill하는 기능"을 false 설정한다. 

간단히 말하면 가상메모리 사용에 제한을 두는 기능을 끈다. 메모리가 충분하지 않다면 신경써야 하는 부분이다.    

```
<property>      
  <name>yarn.nodemanager.vmem-check-enabled</name>      
  <value>false</value>    
</property>
```



### 참고

[https://m.blog.naver.com/PostView.nhn?blogId=superbag2010&logNo=220791657218&proxyReferer=https%3A%2F%2Fwww.google.com%2F](https://m.blog.naver.com/PostView.nhn?blogId=superbag2010%26logNo=220791657218%26proxyReferer=https://www.google.com/)

