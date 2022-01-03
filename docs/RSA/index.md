# Public Key Encryption Systems - RSA

从这一期开始，我们要聊非对称加密了，非对称加密的代表就是公钥私钥加密。

上一期我们聊了 `Diffie–Hellman key exchange 迪菲-赫尔曼密钥交换`,受这个的启发，有三个人在1977年提出了RSA加密算法，这三个人分别是：罗纳德·李维斯特（Ron Rivest）、阿迪·萨莫尔（Adi Shamir）和伦纳德·阿德曼（Leonard Adleman），RSA 就是他们三人姓氏开头字母拼在一起组成的。

## RSA的数学原理和证明

网上关于RSA讲解的文章非常多，感兴趣的同学可以自行搜索，比如`阮一峰`老师曾讲过RSA的算法原理：

- RSA算法原理（一）[https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html](https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html)

- RSA算法原理（二）[https://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html](https://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html)

## RSA Python简单测试

我们这里就按照维基百科，简单的通过Python代码来做一个RSA算法的加密解密过程。其中可能会需要一些简单的数学知识，比如什么是`质数`，什么叫`互为质数`，欧拉函数等等。

### 公钥私钥的生成

生成公钥私钥一共有4步，具体的证明我们就不讲了。


第一步，随机选择俩个不同的`质数`，或者叫`素数`，p和q，得到 `N=p*q`

```python
import random


def is_prime(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def get_prime(size):

    while True:
        num = random.randrange(size, size ** 2)
        if is_prime(num):
            return num


p = get_prime(100)
q = get_prime(100)

N = p * q

print(f"p={p}")
print(f"q={q}")
print(f"N=p*q={p*q}")

```

比如结果如下（随机）


```python
p=421
q=5441
N=p*q=2290661
```


第二步，根据`欧拉函数` 求出 r, 证明方法就不展开了。

```
r =  φ(N) =  φ(p) x  φ(q) = (p-1)(q-1)
```

``` python
>>> p=421
>>> q=5441
>>> r = (p - 1)*(q - 1)
>>> r
2284800
>>>
```

第三步，随机选择一个整数e，条件是1< e < φ(N)，且e与φ(N) 互质。

 φ(N) = 2284800, 也就是在1到2284800之间，选择一个数e，e和2284800互为质数（也就是他俩的最大公约数=1）

满足条件的e很多，如果一个一个算，这一步会耗费大量时间，通常我们会让 `e=65537`，至于为什么，可以参考这篇文章[https://www.johndcook.com/blog/2018/12/12/rsa-exponent/](https://www.johndcook.com/blog/2018/12/12/rsa-exponent/)


下面是如果你真的想去随机找e，代码如下，如果r值很大，运行时间会很长。

```python
import math
import random

p=421
q=5441
r = (p - 1)*(q - 1)

def get_e(r):
    e_list = []
    for i in range(2, r):
        if math.gcd(i, r) == 1:
            e_list.append(i)
            print(i)
    return random.choice(e_list)

e = get_e(r)
print(e)
```

第四步，求得e关于r的模逆元，命名为d，如果模逆元不存在，则重复步骤一二三。


```python

p=421
q=5441
r = (p - 1)*(q - 1)
e = 65537

def get_d(e, r):
    for d in range(2, r):
        if d*e % r == 1:
            return d

    return False

d = get_d(e, r)
if d:
    print(d)
```

得到 `d=489473`

最后，将N和e封装成公钥，N和d封装成私钥。

公钥: N = 2290661, e = 65537

私钥：N = 2290661, d = 489473


### 加密和解密


加密用到公钥（N，e），假如要加密的消息m=100，则加密就是计算 m的e次方然后对n取模

```python
m = 100
N = 2290661
e = 65537

cipher = m**e % N

print(cipher)
```

密文为 cipher = 71194


解密要用到私钥（N，d），解密就是把密文进行d次方，然后对N取余

```python
N = 2290661
d = 489473
cipher = 71194

plaintext = cipher**d % N

print(plaintext)
```

得到明文 plaintext = 100


这一期先到这里，下次我们聊聊RSA的安全问题。