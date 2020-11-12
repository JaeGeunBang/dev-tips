### 두 directory의 file 존재 여부 확인

<hr>
parameter

1. source dir
2. dest dir
3. 날짜



```shell
source=$1
dest=$2

for file in $(find $source -type f) # file만 찾는다. (directory 제외)
do
  IFS='/' read -ra vStr <<< "$file" # '/'로 split
  result=''

  for x in ${vStr[@]}
  do
    if [ $x = "." ] || [[ "$x" = "$1" ]]; then # 특정 조건은 제외
      continue
    fi
    result=$result/$x # 특정 조건을 제외한 후 나머지 값으로 조합
  done

  if [[ "$result" =~ "$3" ]]; then # 특정 날짜만 가진 값만 추출
    if [ -f $dest$result ]; then # 파일 존재 여부 체크
      #echo 'exist' $dest$result
      :
    else
      echo 'not exist' $dest$result
    fi
  fi
done

```

