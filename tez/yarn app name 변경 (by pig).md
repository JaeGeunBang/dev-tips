### yarn app name 변경 (by pig)

<hr>


pig를 tez로 실행시 기존 mapreduce에서 사용하던 option은 yarn app name을 변경하지 못한다.



이를 변경하기 위해 .pig 스크립트 내 `SET job.name 'Define Yarn App Name'` 를 정의한다.

