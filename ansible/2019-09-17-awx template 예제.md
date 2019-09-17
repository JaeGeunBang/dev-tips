

### awx template 예제

<hr>


![Screenshot from 2019-09-16 14-35-15](https://user-images.githubusercontent.com/22383120/64936193-b0399f00-d88f-11e9-90d6-6a0bf0d9c513.png)



**기본 특성들**

NAME

- Template 이름을 정한다.



INVENTORY

- INVENTORY를 선택한다.
- INVENTORY는 해당 template을 수행하고 싶은 target host들을 정의한다.



CREDENTIAL

- target host에 접속하기 위한 계정 정보를 가진 CREDENTIAL을 선택한다.
- ssh 또는 password를 설정할 수 있다.



PROJECT

- 해당 template을 저장할 project를 선택한다.
- project는 template을 모아둔 개념이다.



PLAYBOOK

- 해당 template을 실행할 playbook을 선택한다.
- playbook은 보통 .yml파일 형식이며 각종 명령이나 변수들이 정의되어 있다.



FORKS

- playbook을 동시에 실행할 process 수를 결정한다.
- inventory의 노드가 8개라면, forks를 8로 함으로써 동시에 모든 노드에 playbook을 실행한다.
- FORKS 값을 넣지 않으면, 노드 하나하나씩 수행된다. 즉, 첫번째 노드가 완료된 이후 다음 노드로 넘어가게 된다.



VERBOSITY

- template의 log 수준을 결정한다.
- 0은 가장 기본적인 log만 출력되며, 숫자가 높아질수록 더 디테일한 log를 볼 수 있다.



