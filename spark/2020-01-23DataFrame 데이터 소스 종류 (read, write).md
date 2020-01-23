# DataFrame 데이터 소스 종류 (Read, Write)



Spark는 다양한 데이터 소스를 지원한다.

- CSV
- JSON
- **Parquet** (default)
- ORC
- JDBC/ODBC 연결
- 일반 텍스트 파일



다양한 압축 방법을 제공한다.

- None
- Gzip
- **Snappy** (default)
- zlip 등



다양한 Read,Write 모드를 지원한다.

- Read
  - **permissive**: 오류 레코드의 모든 필드를 null로 설정. 오류 레코드를 _corrupt_record라는 문자열 컬럼에 기록함. (default)
  - dropMalformed: 형식에 맞지 않는 레코드가 포함되면 제거한다.
  - failFast: 형식에 맞지 않은 레코드가 포함되면 종료한다.
- Write
  - append: 해당 경로에 이미 존재하는 파일 목록에 결과 파일을 추가한다.
  - overwrite: 이미 존재하는 모든 데이터를 덮어쓴다.
  - **errorIfExists**: 해당 경로에 파일이 존재하면, 오류를 발생시키면서 작업을 실패한다. (default)
  - ignore: 해당 경로에 파일이 존재하면, 아무런 처리도 하지 않는다.



**사용 방법**

- 데이터 소스는 Text, 압축은 Gzip, Write 모드는 append로 하고싶을 때.

```scala
dataframe
  .write
  .format("text")
  .option("compression", "gzip")
  .mode("append")
  .save(path)
```



- 데이터 소스는 CSV, 압축은 None, Write 모드는 overwrite로 하고싶을 때.

```scala
dataframe
  .write
  .format("csv")
  .option("compression", "none")
  .mode("overwrite")
  .save(path)
```

