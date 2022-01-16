# leetcall

## 題目
![image](https://user-images.githubusercontent.com/57281249/149655714-e6376ea0-d898-4f29-9de4-d3036977f841.png)

## 限制
![image](https://user-images.githubusercontent.com/57281249/149655738-eba68a84-87fb-4f74-9869-4241f4084258.png)

## payload
``` python
# Problem 1: Hello
print(getattr("Hello, {:}!", 'format')(getattr('!\nHello, ', 'join')(getattr(getattr(open(0),'read')(),'splitlines')())))

# Problem 2: Fibonacci
print(getattr('\n','join')(map(str,map(round,map(getattr(0.4472135954999579,'__mul__'),map(getattr(1.618033988749895,'__pow__'),map(int,getattr(open(0),'readlines')())))))))

# Problem 3: FizzBuzz
getattr('','format')(setattr(__builtins__,'a',range(1,10001)),setattr(__builtins__,'b',list(map(bool,map(getattr(3,'__rmod__'),a)))),setattr(__builtins__,'c',list(map(bool,map(getattr(5,'__rmod__'),a)))),print(getattr('\n','join')(map(getattr(str,'__add__'),map(getattr(str,'__add__'),map(getattr(str,'__mul__'),map(str,a),map(getattr(bool,'__and__'),b,c)),map(getattr('Fizz','__mul__'),map(getattr(0,'__eq__'),b))),map(getattr('Buzz','__mul__'),map(getattr(0,'__eq__'),c))))))
```

![image](https://user-images.githubusercontent.com/57281249/149656065-11129a7b-6f05-44c2-b292-965b80a5de0b.png)
