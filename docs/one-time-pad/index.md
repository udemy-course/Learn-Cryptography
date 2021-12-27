# One-Time Pad 一次性密码本

前面一节我们聊了置换加密，这一期我们继续聊古典加密，看另外一种加密方法，One-Time Pad，翻译成中文可以理解为一次性密码本。

这种加密方法是以随机的密钥（key）组成明文，且只使用一次。

## 理论上的安全性

以下内容来自维基百科。

在理论上，此种密码具有完善保密性，是牢不可破的。它的安全性已由克劳德·艾尔伍德·香农所证明。

虽然它在理论上的安全性无庸置疑，但在实际操作上却有着以下的问题：

- 用以加密的文本，也就是一次性密码本，必须确实是随机产生的。
- 它至少必须和被加密的文件等长。
- 用以加密的文本只能用一次，且必须对非关系人小心保密，不再使用时，用以加密的文本应当要销毁，以防重复使用。

所以One-Time Pad基本没有现实的可行性。

## One-Time Pad的一种Python实现

### XOR 异或操作

先来回顾一下数学里的异或操作。如果大家在大学学过计算机或者数字电路的话，应该会异或门(XOR gate)很熟悉，如下图：

![mkdocs](../img/XOR_gate.png)


### Python里的异或操作

```python
>>> a = 65
>>> b = 21
>>> a ^ b
84
>>> bin(84)
'0b1010100'
>>>
```

假如65为明文，21为密钥，一次异或完成加密，得到密文84，把密文84，通过密钥21再进行一次XOR即完成解密。

```python
>>> 84 ^ 21
65
>>>
```

### 按字节进行加密解密

有了前面的解释，就可以试着给明文信息的二进制内容，进行One-Time Pad加密了，首先我们需要一个能产生随机key的方法

```python
def generate_key(n):
    # 以byte为单位生成长度为N个bytes的密钥key
    return bytes([random.randrange(0, 256) for i in range(n)])

```

然后定义个xor的操作，把明文message（bytes）和随机的key（相同长度）进行XOR操作即完成了加密。

```python
def xor(key, message):
    length = min(len(key), len(message))
    return bytes([key[i] ^ message[i] for i in range(length)])
```

加密解密测试


```python
message = b"ATTACK"
key = generate_key(len(message))
cipher = xor(key=key, message=message)

print(cipher)

print(xor(key=key, message=cipher))
```

得到的结果(第一行为密文)

```
b'\rZk\xa4\xc2\xc9'
b'ATTACK'
```

## 为啥 One-Time Pad无法破解

以上面长度为6个字节的明文 ATTACK为例，生成的随机key是长度为6个bytes的字符，也就是48个bit，可能性是2的48次方，`281474976710656`种可能性, 这个破解难度已经挺高了，而且如果我们继续提高明文长度，破解难度为呈指数型增加。

