### Snappy 처리

<hr>



Pig에서 데이터를 읽기 위해 `load` , 저장하기 위해 `store`를 사용한다.



만약 아무 Storage를 따로 설정하지 않으면 PigStorage()를 통해 수행하는데, PigStorage()는 기본 `gzip`, `bzip`만 제공한다.

- bzip은 gzip보다 압축률이 더 좋지만, 성능이 떨어진다. 
- 아래 공식문서 Handling Compress에서 볼 수 있다.

https://pig.apache.org/docs/r0.17.0/func.html



그외 다른 Compression들 (Snappy, Lzo, ZLIB 등)은 OrcStorage()를 사용해야할것으로 보인다.

**a.pig**

```
A = LOAD 'path'
STORE A INTO 'snappy_path' USING OrcStorage('-c SNAPPY')
```

**b.pig**

```
B = LOAD 'snappy_path' USING OrcStorage('-c SNAPPY')
```

