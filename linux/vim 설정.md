# vim 설정



- vim 설정은 사용자 디렉토리에 `.vimrc` 에서 수정한다.

```
if has("syntax")
	syntax on # 형식별 구문 강조
endif

set hlsearch # 검색된 결과 강조
set ignorecase # 검색시 대소문자 구분 안함
set nu # 라인 넘버 표시
set autoindent # 새로운 라인 추가시, 이전 라인의 들여쓰기에 자동으로 맞춤
set ts=4 # 스페이스바 개수
set sts=4 # 스페이스바 n개를 하나의 탭으로 처리
set cindent #
set laststatus=2 # 상태바 표시 (2는 항상 표시)
set shiftwidth=4 # <<, >> 으로 들여쓰기시 사용할 스페이스 개수
set showmatch # 현재 선택된 괄호의 쌍을 표시
set smartcase # ignore 옵션이 켜저있더라도, 검색어에 대문자가 있다면 정확히 일치하는 문자를 찾음
set ruler # 커서 위치 표시
set paste # 계단 복사 제거
set smarttab 
set smartindent
set fileencodings=utf8,euc-kr
```



### Plugin 설치

- 아래 명령을 통해 plug.vim을 설치한다

```
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```



이후 `~/.vimrc`에서 플러그인을 설정한다

```
call plug#begin('~/.vim/plugged')

Plug 'scrooloose/nerdtree'

call plug#end()
```

이후 `:PlugInstall`을 통해 Plugin을 설치한다.



만약 인터넷이 안되는 상황이라면, 직접 git에서 파일을 다운받아 `~/.vim/plugged` 경로에 복사해줘야함

- https://github.com/preservim/nerdtree



### 사용

- 다운로드 후 `:NERDTree`를 통해 Tree view를 볼수 있다.
- 단축키를 아래와 같이 설정할수도 있다. (`F3` 을 누르면 Tree view가 나타난다.)

```
map <F3> :NERDTree<CR>
```

- `ctrl+w+w` 를 누르면 다시 Tree 쪽으로 이동할수 있다.
- 그외 유용한 단축키
  - 파일 생성
    - 원하는 위치에서 `m` 을 누른후 a,b,d,c,l 중 원하는 명령을 수행한다.





