### Drop table 이후 테이블이 지워지지 않는 이슈 (Hive 3.1.2)

<hr>


[https://issues.apache.org/jira/browse/HIVE-22566?jql=project%20%3D%20HIVE%20AND%20text%20~%20%22Unable%20to%20fetch%20table%20null%22](https://issues.apache.org/jira/browse/HIVE-22566?jql=project %3D HIVE AND text ~ "Unable to fetch table null")



위와 동일한 이슈로, Transactional Table을 생성하고 이를 통해 Materialized View를 생성한 경우 Transactional Table이 삭제가 되지 않는 이슈.

database를 지워봐도, 똑같은 에러가 발생한다. sys db에 table 정보를 삭제하라고 하는데, sys db내 table들은 transactional table이 아니여서 delete가 되지도 않는다...



Hive 4.0 에서 이슈가 처리될것으로 보이지만, 현재로써는 딱히 해결 방법은 없는것 같다.