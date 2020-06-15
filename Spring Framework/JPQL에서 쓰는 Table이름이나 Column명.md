## JPQL에서 쓰는 Table이름이나 Column명

JPQL에서 쓰는 Table이름이나 Column명은 **객체에 선언된 명칭**을 그대로 사용해야 함 (DB에 등록된 Table이름이나 Column명이 아님.)

```
class Customer
{
	String date;
	String ID;
}
```


@Query(SELECT x FROM **Customer** x WHERE **date** = '' AND **ID** = '')

