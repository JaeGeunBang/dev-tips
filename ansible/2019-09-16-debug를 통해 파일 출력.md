### debug를 통해 파일 출력

<hr>
awx를 통해 benchmark를 진행함에 있어 출력된 파일을 awx ui 상에서 보고 싶을때 debug를 사용한다.



**예제 script**

```
for n in $(seq 0 10); do
  of="/data${n}/ddtest"
  dd if=/dev/zero bs=10M count=1000 of=${of} conv=fdatasync 2>/home/test/ddtest${n}.out &
  WAITPIDS="$WAITPIDS ${!}"
done
wait $WAITPIDS
grep copied /home/test/ddtest?.out
grep copied /home/test/ddtest??.out
```

해당 스크립트를 수행하면, 각 disk에 write throughput을 출력한다.

이를 awx ui 상에서 모아서 보고 싶을 때 아래와 같이 debug를 추가한다.



**playbook 예제**

```sh
tasks:
  - name: disk_write_test_dd.sh copy
    copy:
      src: disk_write_test_dd.sh
      dest: /home/test/
      remote_src: no
  - name: write test
    shell: sh /home/test/disk_write_test_dd.sh
    register: test_write_result
  - name: output test write
    debug:
      var: test_write_result.stdout_lines
```

두번째 task "write test"에 `register: test_write_result`를 추가하고, 이를 세번째 task "output test write"에서 debug로 `test_write_result.stdout_lines` 를 출력할 수 있다.



**AWX UI**

![Screenshot from 2019-09-16 14-17-54](https://user-images.githubusercontent.com/22383120/64935615-2dafe000-d88d-11e9-9b3e-a1c154de9b11.png)



