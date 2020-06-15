### fsck 명령



fsck는 HDFS의 상태를 점검할 수 있는 명령어이다. 보통 HDFS block에 문제가 생기면 NameNode WEB UI에 표시가 된다.

```
hdfs fsck <HDFS 경로>
```



**옵션**

```
Usage: hdfs fsck <path> [-list-corruptfileblocks | [-move | -delete | -openforwrite] [-files [-blocks [-locations | -racks]]]]
	<path>	start checking from this path
	-move	move corrupted files to /lost+found
	-delete	delete corrupted files
	-files	print out files being checked
	-openforwrite	print out files opened for write
	-includeSnapshots	include snapshot data if the given path indicates a snapshottable directory or there are snapshottable directories under it
	-list-corruptfileblocks	print out list of missing blocks and files they belong to
	-blocks	print out block report
	-locations	print out locations for every block
	-racks	print out network topology for data-node locations
	-storagepolicies	print out storage policy summary for the blocks

	-blockId	print out which file this blockId belongs to, locations (nodes, racks) of this block, and other diagnostics info (under replicated, corrupted or not, etc)

```



**예**

```
hdfs fsck -openforwrite -files -blocks -locations /log_test/2019/08/28/12
```

/log_test/2019/08/28/12 디렉토리 내 있는 파일의 점검 결과를 print 하며, 맨 아래 HEALTHY 한지 아닌지 나타내준다.



...

The filesystem under path '/log_test/2019/08/28/12' is HEALTHY