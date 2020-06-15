### SSH-Credential-접속

<hr>

ansible awx에서 특정 machine에 접속할 때 credential이 필요하다.

특정 machine에 접속할 때 id // pwd 정보가 필요하다. 

허나 hadoop에서 hdfs 계정 같은 경우는 비밀번호를 따로 설정하지 않기 때문에, ssh 설정을 통해 접속해야 한다.



먼저 접속을 원하는 서버에 ssh 키를 생성해야한다.

hdfs 계정으로 접속 후 key 생성

> hdfs@admin > ssh-keygen -t rsa



키는 ~/.ssh 경로에 id_rsa, id_rsa.pub가 생성된다.

id_rsa는 private key, id_rsa.pub는 public key.

- private key를 가지고 있는 클라이언트만 public key를 가진 서버에 접속할 수 있다.

- 즉, ansible 서버가 클라이언트이며 private key를 가지고, hdfs 계정을 가진 서버가 public key를 가져야한다.



![Screenshot from 2019-10-07 14-44-25](https://user-images.githubusercontent.com/22383120/66287489-fc1cb880-e910-11e9-9dd2-802b6a773667.png)

위 awx credential을 만드는 부분에서 SSH PRIVATE KEY에 아까 생성한 id_rsa에 있는 private key를 복사한다.

이후 ~/.ssh 경로에 authorized_keys를 만들어 id_rsa.pub에 있는 public key를 그대로 복사한다. 그래야만 ansible이 가진 private key와 서버가 가진 authorized_keys 파일내 public key를 비교 후 접속을 할 수 있다.



이후 ping 을 통해 접속이 되는지 확인하면 된다.



### 참고

https://opentutorials.org/module/432/3742





