## <router-link>를 통한 파라미터 전달 및 페이지 refresh

<router-link>를 통해 파라미터와 함께 새로운 page로 이동했을 때, 다시 해당 page로 이동하면 refresh가 되지 않는다.

```
<router-link :to="googlechart", param: { ... }> test</router-link>

<router-view>
```


"test" 버튼을 누르고, "googlechart" 페이지로 이동한 후 URL은 "/googlechart/" 로 변경되며, 다시 "test"버튼을 누르면 해당 페이지는 아무 일도 수행하지 않는다.(이미 "/googlechart"에 있기 때문에, vue-router가 아무런 동작도 취하지 않는 것으로 보임.)



이를 위해, 아래 코드와 같이 바꾼다.

```
<router-link :to=**"this.curPage + '?date_type=' + date_type + '&start_date=' + start_date** > test</router-link>

<router-view :**key="$route.fullPath"**>
```

파라미터 전달을 param을 이용하지 않고, URL에 붙여서 보내고, router-view의 key 프로퍼티에 위 값을 넣음으로써,같은 URL을 접속하더라도 다른 파라미터 전달과 동시에 새로운 page로 refresh 된다.

이는 "googlechart"가 가진 created() 훅이 동작한다.