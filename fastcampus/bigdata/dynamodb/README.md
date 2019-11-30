### boto3

boto란?

- Boto is the Amazon Web Services (AWS) SDK for Python



 AWS dynamoDB나 AWS S3를 사용하기 위해 boto3 package가 필요하다.

> pip3 install boto3



```python
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://dynamodb.ap-northeast-2.anazonaws.com')
```



boto3를 통해 AWS에 접근하기 위해 Credential 정보가 셋팅 되어 있어야 한다. 아래 링크를 통해 확인하자.

- Credential: aws_access_key_id, aws_secret_access_key

https://stackoverflow.com/questions/21440709/how-do-i-get-aws-access-key-id-for-amazon



Credential 정보를 찾았다면, awscli를 통해 키를 셋팅한다.

```
> aws configure
```



**AWS**

https://ap-northeast-2.console.aws.amazon.com/dynamodb/home?region=ap-northeast-2

해당 URL에서 DynamoDB 테이블을 생성할 수 있다.



옵션

- Read/Write capacity mode
  - Provisioned (프리티어 사용 가능)
    - 미리 특정 스펙에 셋팅을 해두는 것.
  - On-demand
    - 어느 정도의 스펙을 잘 모를때, 쓰는 만큼만 비용을 지불하고 싶을 때 사용함.
- Provisioned capacity
  - Read/Write Capacity Unit
    - consistent read/write per second할 때, 읽고 쓸 Throughput 을 뜻함.
- indexex
  - 같은 데이터, 같은 테이블이지만 서로 다른 파티션을 제공할 수 있다.
  - 위 Read/Write Capacity Unit을 설정할 수 있다.



**dynamodb 데이터조회**

현재 dynamodb 테이블에 artist_id, id로 키로 설정했을 때.

```python
# 해당 방법은 artist_id, id를 모두 알아야 함. (key를 두개로 설정했기 때문에)
response = table.get_item (
  Key={
    'artist_id':'artist_id',
    'id':'id'
  }
)

# query (artist_id만 알고 있을 때,).
response = table.query (
  KeyConditionExpression=Key('artist_id').eq('artist_id'),
  FilterExpression=Attr('count').gt(80)
)

# scan (artist_id도 모를때)
response = table.scan (
  FilterExpression=Attr('count').gt(80)
)
```

