### BigTable_A_Distributed_Storage_System_for_Structured_data (OSDI 2006)

<hr>



### Data Model


- BigTable은 sparse, distributed, persistent, multi-dimensional sorted map 이다.
- 여기서 map은 row key, column key, timestamp로 인덱스 되어져 있다.
  - (row, column, timestamp) -> value
  - **Rows**
    - 하나의 row key는 읽기, 쓰기에 대해 atomic 하다.
    - 그리고 row key를 모아 `row range(= tablet)`라 한다.
      - 이는 load balancing, distribution을 위한 단위.
      - 만약, 몇 row range만 read한다고 했을 때, 특정 machine만 읽으면 된다.
  - **Column Families**
    - Column key가 그루핑이 되어 `Column Families`라 부른다.
      - 이는 access control을 위한 단위.
      - 컬럼 패밀리는 데이터를 저장하기 전에 미리 만들어 두어야 한다.
    - Column key는 아래와 같이 구성된다.
      - `family:qualifier`
        - family는 반드시 나타나야한다.
    - Access control을 통해 서로 다른 종류의 app들을 관리할 수 있다.
      - A app은 new base data를 입력한다.
      - B app은 base data를 읽고, 파생된 column family를 생성한다.
      - C app은 특정 data에 대해서만 view를 제공한다.
  - **TimeStamp**
    - BigTable의 각 cell (Row, Column Families)은 여러 version (=TimeStamp)을 가지고 있다.
      - timestamp를 통해 내림차순 정렬이 되며, 만약 특정 row, column key를 읽을 때 `가장 최신 데이터를 읽는다.`
        - 같은 row, column을 가진 12시 timestamp 데이터와 1시 timestamp 데이터가 있다면, 1시 데이터를 읽겠다는 뜻.



<hr>

### API

- Bigtable API는 다양한 function을 제공한다.
  - 테이블, column families 생성, 삭제
  - 클러스터, 테이블, column family metadata 변경
- 여러 특징을 가진다.
  - 1. single-row transaction
    2. integer counter와 같은 cell을 제공한다.
    3. client-supplied script를 실행할 수 있다. (ex. Sawzall)



<hr>

### Building Block

- BigTable은 GFS (Google File System)를 기본으로 사용한다.
  - 내부적으로 BigTable은 데이터를 저장하기 위해 `SSTable` 이라는 포맷을 사용한다.
    - SSTable은 persistent, ordered immutable map을 제공한다.
    - 그리고 제공해주는 몇 Operation을 통해 SStable에 key를 통해 look up할 수 있다.
    - SStable은 block의 sequence를 가지며, `block index를 통해 block이 SSTable 어디에 위치되어 있는지 알 수 있다.`
      - SSTable을 open하면, 먼저 block index 정보를 메모리에 load한다.
      - 이후 look up을 하게되면 하나의 disk seek를 수행하며, 먼저 인-메모리 block index에 binary search를 수행해 대략적으로 block의 위치를 찾는다.
      - 찾은 block의 정보를 바탕으로 실제 block을 disk에서 읽는다.
  - BigTable은 `Chubby`라는 highly-available, persistent distributed lock service를 의존한다.
    - Chubby는 5개의 active replica로 이루어져 있으며, 하나는 선출된 master이다.
    - lock service를 제공하며 Client가 Chubby에서 제공하는 directory, small file들을 read, write를 할 때, atomic한 처리를 할수 있게 한다.
    - 각 Chubby client는 Chubby service의 ***session***을 유지하며, 더이상 사용하지 않을 때 session은 만료된다.
    - session이 만료가 되어야 특정 파일이나 디렉토리의 lock이 풀리며, 다른 client가 이용할 수 있다.
  - BigTable은 다양한 task를 수행하기 위해 Chubby를 사용한다.
    - 1. 1개의 active master를 유지하기 위함.
      2. BigTable data의 Tablet Location을 저장하기 위함.
      3. table server를 찾기 위해, tablet server의 죽음을 알기 위함.
      4. BigTable schema (metadata) 정보를 저장하기 위함.
      5.  access control list를 저장하기 위함.
  - 만약 Chubby service를 이용하지 못한다면, Bigtable 또한 이용할 수 없다.



<hr>

### Implementation

- BigTable을 실행하기 위해 크게 3가지 component가 필요하다.
  - client와 연결하기 위한 library, master server, many tablet servers
  - master
    - master는 tablet을 tablet server에 할당하며, tablet server의 추가, 만료를 감지하며, load-balancing을 한다.
    - 추가로, column family나 table의 schema 수정에 관해서 다룰 수 있다.
  - tablet server
    - 각 tablet server는 tablet 의 집합을 관리하며, read, write 요청을 다룰 수 있다.
  - BigTable은 여러 Table을 저장하며, 각 Table은 여러 tablet으로 이루어져 있으며, 각 tablet은 row range와 연관된 모든 데이터를 저장한다.
    - 첫 Table은 하나의 tablet만 가지며, table이 점점 커짐에 따라, tablet은 자동으로 여러 tablets로 split된다. (디폴트는 100~200 MB 사이즈)
- **1. Tablet Location**
  - Tablet은 3 level의 계층 구조를 가진다. (B+ Tree 형태이며 `tablet location hierarchy`라 함)
    - Chubby file --> Root tablet (=METADATA Table) --> Other METADATA tablets --> User Table1, User Table2..
  - Client library를 tablet location을 cache한다.
    - 만약 cache가 되지 않은 상태거나, tablet location을 모른다고 하면, tablet location hierarchy에서 찾아야 한다.
      - Chubby file부터 시작해 Client가 필요로 하는 tablet location을 찾는다.
- **2. Tablet Assignment**
  - Tablet은 하나의 tablet server에 할당된다.
    - mater가 할당되지 않은 tablet을 충분한 공간을 가진 server에 할당한다.
  - Tablet 서버가 시작하면, 가장 먼저 Chubby Directory에 대한 `전용 락` 을 얻어야 한다.
    - 특정 Tablet 서버에서 특정 Chubby Directory에 접근하기 위함.
    - 이후 master는 Chubby Directory를 monitoring 하여 tablet server를 찾을 수 있다.
    - 만약 Tablet 서버가 전용 락을 잃어 버린다면, file이 존재하는한 전용 락을 다시 얻기 위해 계속 재시도를 할 것.
      - Tablet 서버가 종료된다면, 전용 락을 푼다.
  - master는 tablet 서버의 상태를 주기적으로 detecting 한다.
    - 주기적으로 tablet 서버에게 전용 락에 대한 상태 정보를 요청한다.
    - 만약 Tablet 서버에 문제가 생기면, master가 해당 전용 락을 얻어 해당 Tablet 서버가 더이상 serving 하지 못하게 막는다.
  - master를 시작했을 때 단계.
    - 1. Chubby에게 master lock을 얻는다.
      2. Chubby의 server directory를 scan하여, 현재 live한 tablet 서버들을 찾는다.
      3. 각 live한 tablet 서버와 커뮤니케이션을 하며, 어떤 tablet을 할당 받았는지 찾는다.
      4. tablet의 집합을 알기 위해 METADATA table을 scan한다.
- **3. Tablet Serving**

















