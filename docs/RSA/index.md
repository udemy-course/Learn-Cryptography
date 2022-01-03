# Public Key Encryption Systems - RSA

从这一期开始，我们要聊非对称加密了，非对称加密的代表就是公钥私钥加密。

上一期我们聊了 `Diffie–Hellman key exchange 迪菲-赫尔曼密钥交换`,受这个的启发，有三个人在1977年提出了RSA加密算法，这三个人分别是：罗纳德·李维斯特（Ron Rivest）、阿迪·萨莫尔（Adi Shamir）和伦纳德·阿德曼（Leonard Adleman），RSA 就是他们三人姓氏开头字母拼在一起组成的。

## RSA的数学原理和证明

网上关于RSA讲解的文章非常多，感兴趣的同学可以自行搜索，比如`阮一峰`老师曾讲过RSA的算法原理：

- RSA算法原理（一）https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html

- RSA算法原理（二）https://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html

## RSA Python简单测试

我们这里就按照维基百科，简单的通过Python代码来做一个RSA算法的加密解密过程。