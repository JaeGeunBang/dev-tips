### Nifi Error Handling

<Hr>
Nifi Processor 수행 중 에러 발생 시 Processor 오른쪽 상단에 빨간 문서가 뜨면서 에러 메시지를 보여준다.



새로운 Attribute를 추가할 때 주로 UpdateAttribute를 사용하는데, 해당 Processor에서 에러가 발생할 수 있음.

- UrlDecode()를 수행하는 UpdateAttribute Processor에  UrlDecode()가 실패했을 경우.
- 이럴 경우 실패한 메시지에 대해 따로 Handling 할 수 있는 방법이 없다.



이땐 ExecuteScript Processor (Groovy)를 사용해 Error Handling 하자.

```groovy
import org.apache.commons.io.IOUtils
import org.apache.nifi.flowfile.FlowFile
import org.apache.nifi.processor.io.InputStreamCallback

import java.nio.charset.*
import java.util.regex.*
import groovy.json.*

// 한번에 가져올 메시지의 최대 수를 지정.
// 10000개의 flowfile를 가지는 flowFileList 객체가 생성된다.
List<FlowFile> flowFileList = session.get(10000);

if (!flowFileList.isEmpty()) {
    flowFileList.each {flowFile ->
        try {
            // ... url decode 수행
            // 성공시 REL_SUCCESS
            session.transfer(flowFile, REL_SUCCESS)
        } catch (Exception e) {
            // 실패시 REL_FAILURE
            session.transfer(flowFile, REL_FAILURE)
        }
    }
}

```



실패된 메시지는 따로 flow를 만들어 무시(버리거나)하거나, 다시 새로 가공해서 ExecuteScript Processor로 다시 전송하여 처리한다.

![Screenshot from 2019-07-29 16-15-13](https://user-images.githubusercontent.com/22383120/62028721-e6598b80-b21b-11e9-89b4-fc23fe14bbe7.png)