# RSA Sign/Verify with OpenSSL

我们继续演示RSA数字签名和验证，这次使用OpenSSL， OpenSSL比Python更简单。

## 生成公钥私钥

通过openssl生成RSA公钥私钥是非常容易的，方法有几种，这里演示其中一种。

```bash
$ openssl genrsa -out private.pem 1024
Generating RSA private key, 1024 bit long modulus (2 primes)
..................+++++
..................................+++++
e is 65537 (0x010001)
$ ls
data.txt  private.pem
$ openssl rsa -in private.pem -pubout > public.pem
writing RSA key
$ ls
data.txt  private.pem  public.pem
$ cat private.pem 
-----BEGIN RSA PRIVATE KEY-----
MIICXwIBAAKBgQDPn+MaRqfYn208oWhPOYUlGyUInO5lEck7QyzyJSfVf0SNLcCt
Hr9mNIXkcjRqG4+6RNklJgKP2zLlJw41/6sBWRoIk7XPkdiiGsxeMQU7pPYOD9YR
02HR40e8Bygs0l6B6i/D26oge0tvHBGLKxc/YZnPpc9ySryrdKTvP0Q1IQIDAQAB
AoGBAJdP/OCfcZ+rwJ6ZOz3Ru7kpKTo3tH2wEqm/8Tef4IH1uG3zVCJW8EJ6MMIm
gRB7eanUlzQ9mUxiAZuDdRXheCu4wzYrg59Z/Aq1Sn1D5Vd16yQu0kB48t3oTTP0
obgjny79Aks8E6NMk+VMENOr/TS2YQo88iXysvGEnS0iTz1JAkEA8+YfX4YI/Bb9
U3VBHhukBPpZnay7MHsCApBmfFIERCwV2G6Be6sVf55ieZB3xNguTtrYbNmEW2UV
ACq0uBmSlwJBANntBsli3JsIqKQxvcXKdGSSHTX/4ME4hk0poKKzW5XYBMWrY7js
VxT6o9wGraR7HYgpVc208OvU/Ku8Aby1xQcCQQCdqNgG66HLMyE2XclmKP/xp9Ne
NVYblKhL+AQHwQy49LZ6XZSd2I3hHQUTB+wj9oqYtqbIViNU4RaeMPz5NK6pAkEA
rrN/b05bv8VPPGHL2pYUfNNNq453ZS6lK5Klfgj+8L7+BGEDTqnYna7YUXjhFyzD
XfaVHJVjVgumix3q3pdxXQJBANFMJuOixBME5zDoUDWWcCMFMeOc8xwNVNSabZjq
oRHIUageFcO8H83EIvFHWC7IdW61sm/pMD3PJF/1p5iCI4c=
-----END RSA PRIVATE KEY-----
$ cat public.pem 
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPn+MaRqfYn208oWhPOYUlGyUI
nO5lEck7QyzyJSfVf0SNLcCtHr9mNIXkcjRqG4+6RNklJgKP2zLlJw41/6sBWRoI
k7XPkdiiGsxeMQU7pPYOD9YR02HR40e8Bygs0l6B6i/D26oge0tvHBGLKxc/YZnP
pc9ySryrdKTvP0Q1IQIDAQAB
-----END PUBLIC KEY-----

```

## 生成签名

先准备一个明文信息，存储到一个文本文件里。

```bash
$ echo A message for signing> data.txt
$ ls
data.txt
$ more data.txt 
A message for signing
```

通过openssl生成签名文件,这里注意一点，数据文件经过SHA256得到的哈希值是256个bit，而我们的RSA key是1024bit的。

openssl在生成签名的时候，实际上是有对原始的SHA256哈希进行数据填充的，填充到1024bit，默认填充方式是`PCKS#1 v1.5`,这里就不展开了，感兴趣的可以查找相关资料阅读。

最后得到的签名大小也是1024bit，通过`hexdump`看，每行16个bytes，一共8行。

16 x 8 x 8 = 1024

```bash
$ openssl dgst -sha256 -sign private.pem -out sha256.sign data.txt 
$ ls
data.txt  private.pem  public.pem  sha256.sign
$ hexdump sha256.sign
0000000 a3bd e74d 44f6 0bd4 7a9d edf9 d198 d35e
0000010 5b40 7b49 3fb4 ca7c eb11 8db9 d829 3244
0000020 2854 762f 8edb d2db ec5f b42a d184 2618
0000030 3b20 e418 fe43 67c1 8a81 1162 52e1 4e03
0000040 754e 0a42 9935 06f1 57ea 7269 1943 9c3b
0000050 07f4 a4f9 c579 de37 37e5 c91d 04b8 2cc4
0000060 5f13 a098 8225 09bf c3b5 9ab1 e256 9e0c
0000070 8e92 81db a93f 92ff f690 666b b91c f73c
0000080
$ 
```

## 签名的验证

```bash
$ openssl dgst -sha256 -verify public.pem -signature sha256.sign data.txt 
Verified OK
```

通过公钥进行验证，得到结果为ok，验证通过。


## 背后细节大揭秘

openssl整个的签名验证过程实际上隐藏了很多细节，我们把它扒开看看。

## 扒一下公钥私钥

openssl产生的key文件实际上是格式化了，但是我们可以通过openssl的命令参数去查看具体公钥私钥里使用的几个重要的数


```
$ openssl rsa -in private.pem -text -noout
RSA Private-Key: (1024 bit, 2 primes)
modulus:
    00:cf:9f:e3:1a:46:a7:d8:9f:6d:3c:a1:68:4f:39:
    85:25:1b:25:08:9c:ee:65:11:c9:3b:43:2c:f2:25:
    27:d5:7f:44:8d:2d:c0:ad:1e:bf:66:34:85:e4:72:
    34:6a:1b:8f:ba:44:d9:25:26:02:8f:db:32:e5:27:
    0e:35:ff:ab:01:59:1a:08:93:b5:cf:91:d8:a2:1a:
    cc:5e:31:05:3b:a4:f6:0e:0f:d6:11:d3:61:d1:e3:
    47:bc:07:28:2c:d2:5e:81:ea:2f:c3:db:aa:20:7b:
    4b:6f:1c:11:8b:2b:17:3f:61:99:cf:a5:cf:72:4a:
    bc:ab:74:a4:ef:3f:44:35:21
publicExponent: 65537 (0x10001)
privateExponent:
    00:97:4f:fc:e0:9f:71:9f:ab:c0:9e:99:3b:3d:d1:
    bb:b9:29:29:3a:37:b4:7d:b0:12:a9:bf:f1:37:9f:
    e0:81:f5:b8:6d:f3:54:22:56:f0:42:7a:30:c2:26:
    81:10:7b:79:a9:d4:97:34:3d:99:4c:62:01:9b:83:
    75:15:e1:78:2b:b8:c3:36:2b:83:9f:59:fc:0a:b5:
    4a:7d:43:e5:57:75:eb:24:2e:d2:40:78:f2:dd:e8:
    4d:33:f4:a1:b8:23:9f:2e:fd:02:4b:3c:13:a3:4c:
    93:e5:4c:10:d3:ab:fd:34:b6:61:0a:3c:f2:25:f2:
    b2:f1:84:9d:2d:22:4f:3d:49
prime1:
    00:f3:e6:1f:5f:86:08:fc:16:fd:53:75:41:1e:1b:
    a4:04:fa:59:9d:ac:bb:30:7b:02:02:90:66:7c:52:
    04:44:2c:15:d8:6e:81:7b:ab:15:7f:9e:62:79:90:
    77:c4:d8:2e:4e:da:d8:6c:d9:84:5b:65:15:00:2a:
    b4:b8:19:92:97
prime2:
    00:d9:ed:06:c9:62:dc:9b:08:a8:a4:31:bd:c5:ca:
    74:64:92:1d:35:ff:e0:c1:38:86:4d:29:a0:a2:b3:
    5b:95:d8:04:c5:ab:63:b8:ec:57:14:fa:a3:dc:06:
    ad:a4:7b:1d:88:29:55:cd:b4:f0:eb:d4:fc:ab:bc:
    01:bc:b5:c5:07
exponent1:
    00:9d:a8:d8:06:eb:a1:cb:33:21:36:5d:c9:66:28:
    ff:f1:a7:d3:5e:35:56:1b:94:a8:4b:f8:04:07:c1:
    0c:b8:f4:b6:7a:5d:94:9d:d8:8d:e1:1d:05:13:07:
    ec:23:f6:8a:98:b6:a6:c8:56:23:54:e1:16:9e:30:
    fc:f9:34:ae:a9
exponent2:
    00:ae:b3:7f:6f:4e:5b:bf:c5:4f:3c:61:cb:da:96:
    14:7c:d3:4d:ab:8e:77:65:2e:a5:2b:92:a5:7e:08:
    fe:f0:be:fe:04:61:03:4e:a9:d8:9d:ae:d8:51:78:
    e1:17:2c:c3:5d:f6:95:1c:95:63:56:0b:a6:8b:1d:
    ea:de:97:71:5d
coefficient:
    00:d1:4c:26:e3:a2:c4:13:04:e7:30:e8:50:35:96:
    70:23:05:31:e3:9c:f3:1c:0d:54:d4:9a:6d:98:ea:
    a1:11:c8:51:a8:1e:15:c3:bc:1f:cd:c4:22:f1:47:
    58:2e:c8:75:6e:b5:b2:6f:e9:30:3d:cf:24:5f:f5:
    a7:98:82:23:87
```