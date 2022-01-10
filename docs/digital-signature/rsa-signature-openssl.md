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
$ echo -n A message for signing> data.txt
$ ls
data.txt
$ more data.txt 
A message for signing
```

通过openssl生成签名文件,这里注意一点，数据文件经过SHA1得到的哈希值是160个bit，而我们的RSA key是1024bit的。

openssl在生成签名的时候，实际上是有对原始的SHA1哈希进行数据填充的，填充到1024bit，默认填充方式是`PCKS#1 v1.5`

最后得到的签名大小也是1024bit，通过`hexdump`看，每行16个bytes，一共8行。

16 x 8 x 8 = 1024

```bash
$ openssl dgst -sha1 -sign private.pem -out sha1.sign data.txt
$ ls
data.txt  private.pem  public.pem  sha1.sign 
$ hexdump sha1.sign 
0000000 7f42 1667 98ee 5f2b dbd0 d181 07df 0a6f
0000010 f48e 963a 1028 1c88 ff36 1d75 7cae 8969
0000020 1d34 44cb 61f0 71c7 2756 a233 ca2c 9092
0000030 b2fc 1bdd 6fd9 e1d2 c583 a2c2 0e94 7d29
0000040 8718 c2a9 1624 a38b 9961 5d20 dc10 1f82
0000050 51dd 3550 61c8 e3d1 af02 90be fdfa f128
0000060 30f5 1111 ca43 8bc7 709b a564 4665 bd72
0000070 2def 4a67 853f 7277 cd52 d8ad dd89 b7b0
0000080
```

## 签名的验证

```bash
$ openssl dgst -sha1 -verify public.pem -signature sha1.sign data.txt
Verified OK
```

通过公钥进行验证，得到结果为ok，验证通过。


## 参考资料

[https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2](https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2)