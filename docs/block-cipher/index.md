# Block Cipher 块加密

前面我们聊了流加密，流加密是通过一个随机的码流和明文进行bit级别的异或操作进行加密。今天我们聊了Block Cipher，块加密或者叫分组加密，这种加密方法是把明文分成几个固定大小的block块，然后分别对其进行加密。

块加密的加密算法有很多，而且很多目前还在使用。我们今天介绍里面一个相对简单的，叫DES（Data Encryption Standard）


## DES 介绍


DES是1970年代由IBM开发出来的，1977年被美国联邦政府的国家标准局确定为联邦资料处理标准（FIPS）。

## DES 原理及实现

关于DES的详细原理，以及Python实现，这里我就偷个懒，感兴趣的同学可以参考这一篇博客 [https://www.ruanx.net/des/](https://www.ruanx.net/des/)

个人认为讲的非常好，而且附带Python的DES代码实现。
