### scala기초 (일급 함수, 클로저 등)

<hr>
**일급 함수 (일급 객체)**

- 일급 함수는 스스로 객체로 취급되는 함수로써, 아래 조건을 만족한다.
  - 변수에 할당할 수 있어야 한다.
  - 파라미터로 전달받을 수 있어야 한다.
  - 반환 값으로 전달할 수 있어야 한다.

```scala
// 변수에 할당함. (add라는 변수에 함수가 할당되어 있다.)
var add = function(a, b) {
  return a + b;
}

// 파라미터로 함수를 전달받으며, add2라는 변수에 할당함.
var add2 = function(func) {
  return func();
}

// 반환 값을 함수로 선언함.
add2( function(a, b, c) { return a + b + c } );
```



**고차 함수**

- 다른 함수를 파라미터로 받거나, 반환 값으로 함수를 사용하는 함수

```scala
def safeStringOp(s:String, f:String => String) = {
      if (s != null) f(s) else s
    }
```

- 두개의 파라미터를 받으며, 첫번째 파라미터는 String, 두번째 파라미터는 함수이다.
  - 두번째 파라미터로 받은 함수는 일급 함수이다.



**리터럴(literal) 함수 (=익명 함수)**

- 말그대로 함수 이름이 없는 함수이다.

```scala
val doubler = (x: Int) => x * 2
val doubled = doubler(22)
```



**클로저**

- Function literal + Referencing Enviroment

```scala
function outer(){
     var title = "hello"
 
     return function(){
          alert(title)
     }
}
 
var inner = outer()
inner() 
```

여기서 outer()내부에 있는 function()을 **클로저**라 한다.

- 내부함수가 외부함수의 맥락(context, 여기선 title 변수)에 접근할 수 있는 것을 가르킨다.

또한, 클로저는 값을 참조하는 것이 변화가 생겼을 때 캡쳐를 한다.

- 이는 외부 변수가 소멸되더라도 내부 함수는 외부 변수에 접근할 수 있게한다.

클로저의 사용 이유

[https://medium.com/sjk5766/javascript-closure%EB%8A%94-%EC%99%9C-%EC%93%B8%EA%B9%8C-81bcdef6352](https://medium.com/sjk5766/javascript-closure는-왜-쓸까-81bcdef6352)

https://meetup.toast.com/posts/90

- 클로저는 일반 OOP 언어의 private과 같은 효과를 지닌다.
- 위 예제에서 title 변수는 외부에서 접근할 수 없고, 오로지 내부에 있는 function()을 통해서만 접근을 할 수 있다.
- 그래서, 무분별한 변수의 수정을 줄일 수 있다.

