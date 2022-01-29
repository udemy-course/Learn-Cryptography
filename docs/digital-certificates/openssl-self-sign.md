# OpenSSL 生成自签名证书

如果大家理解了公钥私钥，以及前面讲过的数字签名后，那么生成证书这个就非常好理解了，因为证书实际上就是一种特殊的签名。

## CA证书颁发机构

因为是自签名，所以我们需要自己扮演CA，作为CA颁发证书的机构，需要准备：

- 一对公钥私钥public key，private key
- 把公钥包装成证书的格式，分发出去，在现实中，这些CA的证书（或者叫根证书）一般都已经包含在操作系统中了。


### 1. 生成私钥

在实际中建议大家对秘钥进行加密，比如通过 `-des3` 算法

```bash
demo@web-server:~/self-sign/ca$ openssl genrsa -out ca.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
.....+++++
..........................+++++
e is 65537 (0x010001)
demo@web-server:~/self-sign/ca$ ls
ca.key
demo@web-server:~/self-sign/ca$ more ca.key
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAyGrMYiFBMTdmJp5Fg1tOeo//i5WXbFPCmpuqt9Zq+YqqXp7s
192D3EHfIzSlETdAZwfkvqe1oHnChjL7Fc9+Y2qGwxc1U4Fo9mrYgnUzV0nmV5sg
q/baCg8fZ9ac/tbtg5vDee1z9PAB+NYXUBuQG5sxXjetK8kW4HvGwnaE0uIQtbCm
/89JjdTmNWLgYtVoxpayM6k8YWcBOHuh/PcCMswK+ezFadZ/xmGADW6RJdkOttKV
0LkRK0CFaNN9+CUI9FMqbEDi5/96Fx2OuKCfeFHC7NrEWJq2Oda7Sr7Cq8fQwAOC
/1QfxFuH9SfDz0JX3R1HOc1exLwem04EfJkytQIDAQABAoIBAQC18LZAc14Cdv9m
GZKTcAVroGPl7NR9RADLaHvvzlho16hYo7/xK6h0ANy30ifz3Au8PN888XUiDMc6
Gvfz0d00FVXnr576guWtpkuNCyajnHPenfZoBn3kWdwx4RO/CZCvRG2Nt7Hn7yZr
JrgdQhht51JG7RZpRHFfMx66FOv5oCE1MKMdFAzpSdgipYfrLxWXuTbcKK6GA+mt
xZ1Sof/sz/Vfak8PBf6BAai0KeVDWt+0+nuyOuYc/N1fBPvV51KVTKEAOYHRkBQ5
RNOuvClc9wpHAgySFkHxmanfRZtnnsXRldA2TmnNyOQ+erRo7ryIQWlVs1LHAARu
8LByEa2BAoGBAPoBMEIzKxKeIktX2CzDQXNNLrg6Gp4LKKV9+J2Pu+foAWtRtNC8
MFFkt4d/TDbSl+GrzI6mHQRQnipPUhRWThLzX2K82ZiZtp4aCRcVSTSWowqJE2q1
MP0nE9Dt15Qq+4qbekSKCGWf9+urbJjEz8mAdCFLlBM9qR3iR3AajvsVAoGBAM05
L5avFZHdBjMT5+ZQAlDdLqakwx1zHBiE1hwfILt0AC5LyiuEYl/EA6Ts1or1qXkn
MHxmU6PLm89D2luuxxyA1CcM80Rjl8m7+Qp9HGywMGL3/pEJkGxFkTTgToVlAT6x
YTB29m9V7w3L5L9S8jUtF7VMPkaVDQY1iIvpYMEhAoGASDVpq+U9jp4QB7TyolMv
J09mrB1ULMvKTKpq0Y9/VYckScwKrrN8PTYa8E7rQ3ZmGe9WIOmHvgRO+qd4bJlU
6ZJTvaAQNUxIe7fHYlxqjX7ozpUy/4IgCS5tQc5AkvIrPyiTExLPRBMFN5OGxUUr
QucQI8HBniEUJKaDvbReEdUCgYEAuA+xIem4Y9GjjM4usD9URGiMPcQKh3BFY6xI
SIKWnemle+BX2/3pKVEpn5MXvRwmOtYuQ3SXUZH9FcEaqB4y0Nqu7LNNwCm+6p1f
+MtLYiQH0cvxEu5MDP+8A3umkTeNDUiUDZ602hhtxqb3a62eNJlT6TQPqshmHQqI
hEv1jmECgYEAv0Y/L1oEJpHAerEa1c5kva3aMPXsRVLVyrmRbFncCplKJflHBLlv
fsr/l6pFxKHLGw5LQFi7AH3ySWb87ctlFyb5OtemsMTmKhc/o3vZNTN/TPhC1rx2
miqKfg8Pui4ak3fpcl3A0oa7bZJbhmK5J7aDSGoBlx0S7V6gFg6zzR4=
-----END RSA PRIVATE KEY-----
```

### 2. 生成根证书

这个根证书实际上是对刚才产生的私钥所对应的公钥进行的一个签名。里面包含了

- CA的`公钥`
- CA的基本信息（就是生成证书时填入的信息，如下所示，包含国家，公司等信息）


```bash
demo@web-server:~/self-sign/ca$ openssl req -new -x509 -key ca.key -out ca.crt -days 365
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:BJ
Locality Name (eg, city) []:BJ
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Test
Organizational Unit Name (eg, section) []:Test
Common Name (e.g. server FQDN or YOUR name) []:test.com
Email Address []:test@test.com
demo@web-server:~/self-sign/ca$ ls
ca.crt  ca.key
demo@web-server:~/self-sign/ca$ more ca.crt
-----BEGIN CERTIFICATE-----
MIIDzTCCArWgAwIBAgIUCkWoTFHzVsHAN3rLHmsvfQTjIEwwDQYJKoZIhvcNAQEL
BQAwdjELMAkGA1UEBhMCQ04xCzAJBgNVBAgMAkJKMQswCQYDVQQHDAJCSjENMAsG
A1UECgwEVGVzdDENMAsGA1UECwwEVGVzdDERMA8GA1UEAwwIdGVzdC5jb20xHDAa
BgkqhkiG9w0BCQEWDXRlc3RAdGVzdC5jb20wHhcNMjIwMTI5MTA0OTIyWhcNMjMw
MTI5MTA0OTIyWjB2MQswCQYDVQQGEwJDTjELMAkGA1UECAwCQkoxCzAJBgNVBAcM
AkJKMQ0wCwYDVQQKDARUZXN0MQ0wCwYDVQQLDARUZXN0MREwDwYDVQQDDAh0ZXN0
LmNvbTEcMBoGCSqGSIb3DQEJARYNdGVzdEB0ZXN0LmNvbTCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAMhqzGIhQTE3ZiaeRYNbTnqP/4uVl2xTwpqbqrfW
avmKql6e7Nfdg9xB3yM0pRE3QGcH5L6ntaB5woYy+xXPfmNqhsMXNVOBaPZq2IJ1
M1dJ5lebIKv22goPH2fWnP7W7YObw3ntc/TwAfjWF1AbkBubMV43rSvJFuB7xsJ2
hNLiELWwpv/PSY3U5jVi4GLVaMaWsjOpPGFnATh7ofz3AjLMCvnsxWnWf8ZhgA1u
kSXZDrbSldC5EStAhWjTffglCPRTKmxA4uf/ehcdjrign3hRwuzaxFiatjnWu0q+
wqvH0MADgv9UH8Rbh/Unw89CV90dRznNXsS8HptOBHyZMrUCAwEAAaNTMFEwHQYD
VR0OBBYEFA0OZjoqg2zR6Zk5xUKjX9VP2q+VMB8GA1UdIwQYMBaAFA0OZjoqg2zR
6Zk5xUKjX9VP2q+VMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEB
AIkytFqPouU43Ck/yW96qGGIndSMInvfHG1VgnYtigibAxsv9Bg3Y/3efkPqjPCj
yxaroci3sAAuMwRyJSgG1gRMa8paP+tsSgWpM/PRCLkCDagE5JG6TebYYk8MTa+V
O7TjQ9HvoOGC8JAPwGgnq+/+BzxY9Aq6/CEuq/uVYuVpK0/i17FvTLrVMaDgkY7F
tOFoUixgxMj6IsGrvbR/2Z/xfieyDdcmZD116PnslVxQqIhqLv7ZSNpaHbbuJAKG
OggJTn0iyIuPdlAnhSxxCshKOj8riKidEYgpd7y4BjQOJasV1ddRQkf3ynOKelcJ
g51c6FNqp33HoKxElkRByCU=
-----END CERTIFICATE-----
```

在现实中，这些CA机构所产生的根证书一般都安装在我们的操作系统中，比如在windows中，如果你运行 `certmgr.msc`

可以看到受信任的根证书，随便点开一个，比如GlobalSign，就可以看到这个根证书内包含的信息了，包含GlobalSign这家CA的基本信息，以及它的公钥，签名算法等。

![mkdocs](../img/certmgr.PNG)



## 证书的申请机构

证书的申请机构有很多，最多的就是个大网站，网站对外提供HTTPS服务，需要用到PKI，自然就需要对自家的公钥申请证书，去哪里申请呢？去CA那里申请。


### 1. 生成私钥


```bash
demo@web-server:~/self-sign/https$ openssl genrsa -out my-website.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
...................................................................................................+++++
....+++++
e is 65537 (0x010001)
demo@web-server:~/self-sign/https$
```

### 2. 生成csr(Certificate Signing Request)


CSR包括了你的网站的公钥，以及你网站相关的信息。

```bash
demo@web-server:~/self-sign/https$ openssl req -new -key my-website.key -out my-website.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:BJ
Locality Name (eg, city) []:BJ
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Peng Xiao
Organizational Unit Name (eg, section) []:Peng Xiao
Common Name (e.g. server FQDN or YOUR name) []:my-website.tips
Email Address []:test@test.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:********
An optional company name []:test
demo@web-server:~/self-sign/https$ ls
my-website.csr  my-website.key
demo@web-server:~/self-sign/https$ more my-website.csr
-----BEGIN CERTIFICATE REQUEST-----
MIIC+zCCAeMCAQAwgYcxCzAJBgNVBAYTAkNOMQswCQYDVQQIDAJCSjELMAkGA1UE
BwwCQkoxEjAQBgNVBAoMCVBlbmcgWGlhbzESMBAGA1UECwwJUGVuZyBYaWFvMRgw
FgYDVQQDDA9teS13ZWJzaXRlLnRpcHMxHDAaBgkqhkiG9w0BCQEWDXRlc3RAdGVz
dC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDDFqo9nx8WnZNl
HFyV2RtZREWu0i0VvTZ4IOIkGELe8NCsxBdwZbrDoVLhMkj+cRxHCU6xEh0FwQMz
3FXrR8m5VGmGt3CNH5IZLwDgRSlvVw5gVtdCimEcYZ5QBX9bjMA8F63kqv3jjEs1
glKvSK1LwnCzJ78s3oAC8Ii2UnroabkJisz1IJXVjt34oy4RxUsbW9OnAq7ppyan
4qkEQLorVAM/RQ7II4I/rG3Ycxgix596EjxCuufgOxB9kg9oc+TJpVhrXAL2FAiQ
7cHBpeiJPwg+hVqmsPerfNalUnw5luCRrkpT9nL+ELgXVNRzaoMuy8ET7Zt7TYvW
94mp4hJTAgMBAAGgLjATBgkqhkiG9w0BCQIxBgwEdGVzdDAXBgkqhkiG9w0BCQcx
CgwIY2lzY28xMjMwDQYJKoZIhvcNAQELBQADggEBAA7o14pjsSYvC9YNqKEdEYg2
gRaMv3iGH0vZFigTsevpzRJL5M6f+clTvExJHWQ9BI3NKs6Be9KWAr2O2WxjkbB+
aMriBKRIDTXjtGS+3FGdkX2MnJADVgQMGb6dSNOdQRK/UOHGIhm4NhBvYI8e+eJu
UXZmCxkcns87T0JZVbhZzqQlbWjhu+SiflkQOLK53XEjiVvU+W5l1BLxPFvOHEhZ
wPe9dBvL9oiZd+SzL6N7Pgm6Q4doZ5pbSolpkpqXkyPRAYxMvmfynRo9USSGQmZa
rbznBS8gc9kKrSdogNxDQ2CS4raX4lAKQ2XPvfCebXRKKw6FFca0PytTolj2n24=
-----END CERTIFICATE REQUEST-----
demo@web-server:~/self-sign/https$
```

通过这个命令可以查看CSR文件里都有啥信息

```bash
demo@web-server:~/self-sign/https$ openssl req -text -noout -verify -in my-website.csr
verify OK
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C = CN, ST = BJ, L = BJ, O = Peng Xiao, OU = Peng Xiao, CN = my-website.tips, emailAddress = test@test.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
                Modulus:
                    00:c3:16:aa:3d:9f:1f:16:9d:93:65:1c:5c:95:d9:
                    1b:59:44:45:ae:d2:2d:15:bd:36:78:20:e2:24:18:
                    42:de:f0:d0:ac:c4:17:70:65:ba:c3:a1:52:e1:32:
                    48:fe:71:1c:47:09:4e:b1:12:1d:05:c1:03:33:dc:
                    55:eb:47:c9:b9:54:69:86:b7:70:8d:1f:92:19:2f:
                    00:e0:45:29:6f:57:0e:60:56:d7:42:8a:61:1c:61:
                    9e:50:05:7f:5b:8c:c0:3c:17:ad:e4:aa:fd:e3:8c:
                    4b:35:82:52:af:48:ad:4b:c2:70:b3:27:bf:2c:de:
                    80:02:f0:88:b6:52:7a:e8:69:b9:09:8a:cc:f5:20:
                    95:d5:8e:dd:f8:a3:2e:11:c5:4b:1b:5b:d3:a7:02:
                    ae:e9:a7:26:a7:e2:a9:04:40:ba:2b:54:03:3f:45:
                    0e:c8:23:82:3f:ac:6d:d8:73:18:22:c7:9f:7a:12:
                    3c:42:ba:e7:e0:3b:10:7d:92:0f:68:73:e4:c9:a5:
                    58:6b:5c:02:f6:14:08:90:ed:c1:c1:a5:e8:89:3f:
                    08:3e:85:5a:a6:b0:f7:ab:7c:d6:a5:52:7c:39:96:
                    e0:91:ae:4a:53:f6:72:fe:10:b8:17:54:d4:73:6a:
                    83:2e:cb:c1:13:ed:9b:7b:4d:8b:d6:f7:89:a9:e2:
                    12:53
                Exponent: 65537 (0x10001)
        Attributes:
            unstructuredName         :test
            challengePassword        :cisco123
    Signature Algorithm: sha256WithRSAEncryption
         0e:e8:d7:8a:63:b1:26:2f:0b:d6:0d:a8:a1:1d:11:88:36:81:
         16:8c:bf:78:86:1f:4b:d9:16:28:13:b1:eb:e9:cd:12:4b:e4:
         ce:9f:f9:c9:53:bc:4c:49:1d:64:3d:04:8d:cd:2a:ce:81:7b:
         d2:96:02:bd:8e:d9:6c:63:91:b0:7e:68:ca:e2:04:a4:48:0d:
         35:e3:b4:64:be:dc:51:9d:91:7d:8c:9c:90:03:56:04:0c:19:
         be:9d:48:d3:9d:41:12:bf:50:e1:c6:22:19:b8:36:10:6f:60:
         8f:1e:f9:e2:6e:51:76:66:0b:19:1c:9e:cf:3b:4f:42:59:55:
         b8:59:ce:a4:25:6d:68:e1:bb:e4:a2:7e:59:10:38:b2:b9:dd:
         71:23:89:5b:d4:f9:6e:65:d4:12:f1:3c:5b:ce:1c:48:59:c0:
         f7:bd:74:1b:cb:f6:88:99:77:e4:b3:2f:a3:7b:3e:09:ba:43:
         87:68:67:9a:5b:4a:89:69:92:9a:97:93:23:d1:01:8c:4c:be:
         67:f2:9d:1a:3d:51:24:86:42:66:5a:ad:bc:e7:05:2f:20:73:
         d9:0a:ad:27:68:80:dc:43:43:60:92:e2:b6:97:e2:50:0a:43:
         65:cf:bd:f0:9e:6d:74:4a:2b:0e:85:15:c6:b4:3f:2b:53:a2:
         58:f6:9f:6e

```


## 生成签名

把CSR文件发给CA，请求CA签名。现实中，CA会验证你的身份，比如网站的话，会验证一下你是否是该网站的所有人等等信息。


```bash
demo@web-server:~/self-sign/https$ openssl x509 -req -in my-website.csr -CA ../ca/ca.crt -CAkey ../ca/ca.key -set_serial 01 -out my-website.crt -days 365
Signature ok
subject=C = CN, ST = BJ, L = BJ, O = Peng Xiao, OU = Peng Xiao, CN = my-website.tips, emailAddress = test@test.com
Getting CA Private Key
demo@web-server:~/self-sign/https$ ls
my-website.crt  my-website.csr  my-website.key
demo@web-server:~/self-sign/https$ more my-website.crt
-----BEGIN CERTIFICATE-----
MIIDcjCCAloCAQEwDQYJKoZIhvcNAQELBQAwdjELMAkGA1UEBhMCQ04xCzAJBgNV
BAgMAkJKMQswCQYDVQQHDAJCSjENMAsGA1UECgwEVGVzdDENMAsGA1UECwwEVGVz
dDERMA8GA1UEAwwIdGVzdC5jb20xHDAaBgkqhkiG9w0BCQEWDXRlc3RAdGVzdC5j
b20wHhcNMjIwMTI5MTEyMzU1WhcNMjMwMTI5MTEyMzU1WjCBhzELMAkGA1UEBhMC
Q04xCzAJBgNVBAgMAkJKMQswCQYDVQQHDAJCSjESMBAGA1UECgwJUGVuZyBYaWFv
MRIwEAYDVQQLDAlQZW5nIFhpYW8xGDAWBgNVBAMMD215LXdlYnNpdGUudGlwczEc
MBoGCSqGSIb3DQEJARYNdGVzdEB0ZXN0LmNvbTCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBAMMWqj2fHxadk2UcXJXZG1lERa7SLRW9Nngg4iQYQt7w0KzE
F3BlusOhUuEySP5xHEcJTrESHQXBAzPcVetHyblUaYa3cI0fkhkvAOBFKW9XDmBW
10KKYRxhnlAFf1uMwDwXreSq/eOMSzWCUq9IrUvCcLMnvyzegALwiLZSeuhpuQmK
zPUgldWO3fijLhHFSxtb06cCrumnJqfiqQRAuitUAz9FDsgjgj+sbdhzGCLHn3oS
PEK65+A7EH2SD2hz5MmlWGtcAvYUCJDtwcGl6Ik/CD6FWqaw96t81qVSfDmW4JGu
SlP2cv4QuBdU1HNqgy7LwRPtm3tNi9b3ianiElMCAwEAATANBgkqhkiG9w0BAQsF
AAOCAQEAi2W6FX7+/E+bvUwVjO2Ba9UudiApTpgXN5+iIEVwKuJ1XDcJvtt2lWZm
a6cgUDVLOzfWHhkjwnX+j55NDY1tAm22OZf41aSJTR0GemIjbjEha4wBj9pMdfSS
aFxJTg9ufnvJa87o4LYpKuRshObrGLV+iqqBBCvDz2Ea8FyC+st18HQJBQFyWluC
yir9YcviZENLz7QGrMc5FsmUtr4hfD6FjHSnnS1NmKdTFxOwmkOUHTUz7M0SIMFT
bjaBRtvv/dW1jXjlGTtAWEK44ETYLcH4A8Luwt2N3HmBcVcqmafRBVDdx6W0m0bX
8b1owP641uJM/1aIc1WY4PavxvnBWg==
-----END CERTIFICATE-----
demo@web-server:~/self-sign/https$
```

证书里有啥信息呢？

- CA的基本信息
- 申请者（网站的基本信息）
- 申请者（网站）的公钥
- 签名算法

```bash
demo@web-server:~/self-sign/https$ openssl x509 -in my-website.crt -text -noout
Certificate:
    Data:
        Version: 1 (0x0)
        Serial Number: 1 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = CN, ST = BJ, L = BJ, O = Test, OU = Test, CN = test.com, emailAddress = test@test.com
        Validity
            Not Before: Jan 29 11:23:55 2022 GMT
            Not After : Jan 29 11:23:55 2023 GMT
        Subject: C = CN, ST = BJ, L = BJ, O = Peng Xiao, OU = Peng Xiao, CN = my-website.tips, emailAddress = test@test.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
                Modulus:
                    00:c3:16:aa:3d:9f:1f:16:9d:93:65:1c:5c:95:d9:
                    1b:59:44:45:ae:d2:2d:15:bd:36:78:20:e2:24:18:
                    42:de:f0:d0:ac:c4:17:70:65:ba:c3:a1:52:e1:32:
                    48:fe:71:1c:47:09:4e:b1:12:1d:05:c1:03:33:dc:
                    55:eb:47:c9:b9:54:69:86:b7:70:8d:1f:92:19:2f:
                    00:e0:45:29:6f:57:0e:60:56:d7:42:8a:61:1c:61:
                    9e:50:05:7f:5b:8c:c0:3c:17:ad:e4:aa:fd:e3:8c:
                    4b:35:82:52:af:48:ad:4b:c2:70:b3:27:bf:2c:de:
                    80:02:f0:88:b6:52:7a:e8:69:b9:09:8a:cc:f5:20:
                    95:d5:8e:dd:f8:a3:2e:11:c5:4b:1b:5b:d3:a7:02:
                    ae:e9:a7:26:a7:e2:a9:04:40:ba:2b:54:03:3f:45:
                    0e:c8:23:82:3f:ac:6d:d8:73:18:22:c7:9f:7a:12:
                    3c:42:ba:e7:e0:3b:10:7d:92:0f:68:73:e4:c9:a5:
                    58:6b:5c:02:f6:14:08:90:ed:c1:c1:a5:e8:89:3f:
                    08:3e:85:5a:a6:b0:f7:ab:7c:d6:a5:52:7c:39:96:
                    e0:91:ae:4a:53:f6:72:fe:10:b8:17:54:d4:73:6a:
                    83:2e:cb:c1:13:ed:9b:7b:4d:8b:d6:f7:89:a9:e2:
                    12:53
                Exponent: 65537 (0x10001)
    Signature Algorithm: sha256WithRSAEncryption
         8b:65:ba:15:7e:fe:fc:4f:9b:bd:4c:15:8c:ed:81:6b:d5:2e:
         76:20:29:4e:98:17:37:9f:a2:20:45:70:2a:e2:75:5c:37:09:
         be:db:76:95:66:66:6b:a7:20:50:35:4b:3b:37:d6:1e:19:23:
         c2:75:fe:8f:9e:4d:0d:8d:6d:02:6d:b6:39:97:f8:d5:a4:89:
         4d:1d:06:7a:62:23:6e:31:21:6b:8c:01:8f:da:4c:75:f4:92:
         68:5c:49:4e:0f:6e:7e:7b:c9:6b:ce:e8:e0:b6:29:2a:e4:6c:
         84:e6:eb:18:b5:7e:8a:aa:81:04:2b:c3:cf:61:1a:f0:5c:82:
         fa:cb:75:f0:74:09:05:01:72:5a:5b:82:ca:2a:fd:61:cb:e2:
         64:43:4b:cf:b4:06:ac:c7:39:16:c9:94:b6:be:21:7c:3e:85:
         8c:74:a7:9d:2d:4d:98:a7:53:17:13:b0:9a:43:94:1d:35:33:
         ec:cd:12:20:c1:53:6e:36:81:46:db:ef:fd:d5:b5:8d:78:e5:
         19:3b:40:58:42:b8:e0:44:d8:2d:c1:f8:03:c2:ee:c2:dd:8d:
         dc:79:81:71:57:2a:99:a7:d1:05:50:dd:c7:a5:b4:9b:46:d7:
         f1:bd:68:c0:fe:b8:d6:e2:4c:ff:56:88:73:55:98:e0:f6:af:
         c6:f9:c1:5a
demo@web-server:~/self-sign/https$
```


## 总结一下

整个生产自签名的过程，都用到了那些数据？

- CA的RSA公钥私钥
- CA公钥生产的签名（根证书）
- 证书申请者（网站）的RSA公钥私钥
- 证书申请者（网站）公钥 + 网站信息，签名后生成CRS
- 证书申请者把CSR发给CA申请签名
- CA验证CSR，最后生成证书文件CRT发给证书申请者

## 通过Flask来测试一下HTTPS+证书

通过flask简单测试一下我们的证书，`ssl_context`里的参数，第一个是证书，第二个是你网站的RSA私钥

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(ssl_context=('my-website.crt', 'my-website.key'))
```


![mkdocs](../img/flask-https.PNG)

通过证书查看，能看到证书内包含的所有信息。如果查看certification path，我们是找不到根证书的，因为这个证书是自签名的。


![mkdocs](../img/flask-https-cert-path.PNG)

当然你也可以打开你的证书，,点击install certificate，把它安装到系统里，当然这样还是不能让你的CA被信任，具体如果想要让你的CA导入到系统信任的root CA里，具体操作大家可以自行研究一下。

![mkdocs](../img/flask-https-root-ca.PNG)