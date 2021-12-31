# Stream Cipher 流加密

这一期我们聊`流加密 Stream Cipher`，首先我们先看看为什么会出现流加密，以及流加密到底是一种什么样的加密算法。

先来看一个概念。

## 完善保密性（perfect secrecy）

以下内容来自`维基百科`：

`完善保密性`（perfect secrecy）是信息论安全性的一个特例，为香农提出的信息学观点，具有该性质的密文不应该透露任何明文的信息。在该观点中达成这项性质的方法，是使用与明文空间相等或更大的密钥空间。

（香农给出了详细证明，感兴趣的可以去看看）

One-Time Pad是符合`香农`提出的perfect secrecy，由于密钥空间等于或大于明文空间，所以对同一个密文以穷举法破解时，将会获得所有可能的明文，使得无法分辨何者为真正的消息。因此若没有密钥，即使敌手拥有无穷的计算时间和存储空间，密文仍然不可能破解。

具有完善保密性的密钥长度不可短于被加密的密文。此性质造成实际应用的不便。

为了消除这种不便，一般使用两种方法：

- 流加密（Stream cipher）
- 分组加密（也叫块加密，Block cipher）

只是这样的改变会缩小密钥空间，因而失去完善保密性。

## 流加密

在密码学中，流加密（英语：Stream cipher），是一种对称加密算法，加密和解密双方使用相同`伪随机加密数据流`（pseudo-random stream）作为密钥，明文数据每次与密钥数据流顺次对应加密，得到密文数据流。实践中数据通常是一个位（bit）并用异或（xor）操作加密。

该算法解决了对称加密完善保密性（perfect secrecy）的实际操作困难(key很难分发)。

流加密解决了One-Time Pad中的key生成和分发的问题。

- 生成，伪随机数生成算法
- 分发，伪随机数生成算法可以让发送者和接收者能生成相同的随机数作为key用于加密和解密消息(只要使用相同的种子)

## 流加密的Python演示

这里使用我们上一期聊的`线性同余方法`算法来生成随机数

```python
def generate_key_bytes(seed, m=2 ** 31, a=1103515245, c=12345):
    """Linear congruential generator."""
    return (a * seed + c) % m % 256


def encrypt(key, message):
    return bytes([message[i] ^ key for i in range(len(message))])


message = b"ATTACK"

key = generate_key_bytes(seed=654321)

encrypted_message = encrypt(key, message)
print(encrypted_message)

decrypted_message = encrypt(key, encrypted_message)

print(decrypted_message)
```


## 流加密的应用

流加密属于现代密码学的内容，曾经有比较多得实际应用，当然这个曾经并不遥远， 例如

- A5/1 (G2 encryption) - 54 bits
- A5/2 (export vesion出口版本，安全性比A5/1弱) - 17 bits
- RC4(WEP, SSL) - 40-2048 bits

其中 `A5/1` `A5/2` 是GSM标准中提供行动通信保密性的流密码，是GSM的7种加密算法之一。在2014年曾经有多达70个移动终端通过A5/1实现其语音通信的加密。

至于说在GSM系统中到底是如何使用流密码进行加密的，感兴趣的同学可以自行查找资料学习。

RC4加密也是流加密算法，曾经也是TSL可采用的算法之一，不过现在已经不推荐使用了，因为不安全。


## 流加密的问题

流加密存在很多问题，导致目前在实际中已经很少使用了，存在的问题比如：

- key的重复性使用
- 有一些key的空间不够大，导致暴力破解存在可能性
- 攻击者多次截取加密数据，可以比较容易破解

