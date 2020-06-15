### fabric을 통한 원격 command 실행 및 config 배포



fabric은 원격 host에 ssh를 통해 접속 후 shell command를 실행하는 python api 이다.

하둡 벤치마크를 할 때, 수많은 노드에 command 명령을 실행하거나 config 배포를 할 때 사용한다.



fabric 실행 (helloworld)

```python
from fabric import Connection, task

@task
def helloworld(ctx):
    result = Connection('remoteHost').run('ls -al', hide=True)
    print(result.stdout)
```



실행

```
> fab helloworld
```



command 실행 및 config 배포

```python
from fabric import SerialGroup, task

@task
def runCommand(ctx):
    for cnx in SerialGroup('remoteHost1', 'remoteHost2')
        print("{}: {}".format(cnx, cnx.run('dd ....', hide=True).stdout))
        
@task
def getConfigFile(ctx):
    for cnx in SerialGroup('remoteHost1', 'remoteHost2')
        print("{}: {}".format(cnx, cnx.run('scp <user@localhost>:/path remoteHost_path', hide=True).stdout))
```




## 참고
Fabric 이슈[https://github.com/fabric/fabric/issues/1854]