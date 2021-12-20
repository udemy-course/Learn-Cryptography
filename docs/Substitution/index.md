# 置换加密  Substitution Cipher


上一节我们聊了`凯撒密码`，在继续聊新内容之前，先想一下，为什么凯撒加密非常容易被破解？

原因就是因为字母表顺序平移这种算法的复杂度太低了，只有26种可能性的密钥，即使在没有计算机的古代也是非常容易破解的。

要提高破解的难度，就需要提高算法的复杂度。于是乎最容易想到的就是，既然有26个字母，那为啥不随机打乱顺序然后作为密钥呢？

OK，这就是这一期要聊的一种加密方法，叫Substitution Cipher，中文翻译成置换加密。

- 基于置换
- 密钥为26个字母的全排列之一
- 加密过程：对于每个单字母查表，改为对应字母
- 解密过程：反向查表
- 恺撒密码可以看作单表置换的一类特殊情况


![mkdocs](../img/Substitution_Cipher.png)


## 置换加密的安全性

26个英文字母的排列组合，也就是26的阶乘种可能性，结果是：

```
# python
>>> import math
>>> math.factorial(26)
403291461126605635584000000
>>>
```

`403291461126605635584000000`，这个基本是天文数字了，暴力破解的话，需要循环遍历所有可能，光是循环这么多次，对于我们个人的电脑，这是一个不可能完成的任务。

粗略的估计了一下，我的电脑做这个循环，大概需要10年的时间。不信大家可以试试。

好的，也就是说，我们从这么多的可能排列组合里，随机选一个作为我们的密钥，使用它进行加密，理论上应该是非常安全的，因为暴力破解的时间成本太高了。

刚才这个26阶乘种可能性的密钥，这个天文数字换算成2的乘方的话，大概是2的88次方，在加密领域，我们一般把这种密钥的安全性称之为 88 bit security，这个等后面我们还会再提到的。

说了这么多，这种密钥安全么？实际上远没有我们想的那么安全，两点：

- 88 bit这个级别的安全性是非常低的，个人电脑做不到暴力破解，不代表强力的计算机集群做不到，以空间换时间
- 这种加密有一个致命弱点，导致它可以轻松破解（我们下次聊）


## 置换加密的Python实现


```python
import string
import random


def generate_key():
    letters = [l for l in string.ascii_letters[26:]]
    random.shuffle(letters)
    
    return dict(zip(string.ascii_letters[26:], letters))


def encrypt(key, message):
    cipher = ""
    for l in message:
        if l in key:
            cipher += key[l]
        else:
            cipher += l
    return cipher

key = generate_key()
print(key)

print(encrypt(key, "ATTACK"))
```

以一次运行结果为例

```python
python .\substitution.py
{'A': 'P', 'B': 'J', 'C': 'X', 'D': 'B', 'E': 'I', 'F': 'L', 'G': 'D', 'H': 'N', 'I': 'H', 'J': 'G', 'K': 'W', 'L': 'E', 'M': 'Z', 'N': 'U', 'O': 'T', 'P': 'V', 'Q': 'Q', 'R': 'M', 'S': 'Y', 'T': 'C', 'U': 'A', 'V': 'R', 'W': 'S', 'X': 'F', 'Y': 'O', 'Z': 'K'}
PCCPXW
```

解密我们就不演示了。就是一个反向查表。


------


## 词频分析

置换加密的复杂度虽然很高，但是这种加密有一个非常大的漏洞，就是人类自然语言都有一个基于统计学的词频分析，因为置换加密的密文是字母的一一对应，所以密文就保留了原始明文的词频特性。

词频分析也是一门学科，对于英文来讲，比较公认的字母词频可以参考网络，比如https://en.wikipedia.org/wiki/Letter_frequency

在英文语言里出现频率最高的前10个字母及频率分别为：

| 字母       | 频率 |
| ----------- | ----------- |
| e      | 12.7%      |
| t   | 9.06%        |
| a    | 8.17%|
| o | 7.51%|
| i | 6.97%|


## 基于词频破解置换加密


假如我们有如下通过置换加密过的密文

```python
cipher = """lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi
bpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jx
ymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpr
yjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjk
lmird jk xjubt trmui jx ibndt
  wb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbi
iwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower m
vjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkd
wkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbr
jx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhrii
ijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmh
mnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlb
bpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkd
wkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bpr
riirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb"""
```

词频字典, 从高频到低频

```python
letter_freq = {
    "e": 0.127,
    "t": 0.0906,
    "a": 0.0817,
    "o": 0.0751,
    "i": 0.0697,
    "n": 0.0675,
    "s": 0.0633,
    "h": 0.0609,
    "r": 0.0599,
    "d": 0.0425,
    "l": 0.0403,
    "c": 0.0278,
    "u": 0.0276,
    "m": 0.0241,
    "w": 0.0236,
    "f": 0.0223,
    "g": 0.0202,
    "y": 0.0197,
    "p": 0.0193,
    "b": 0.015,
    "v": 0.0098,
    "k": 0.0077,
    "j": 0.0015,
    "x": 0.0015,
    "q": 0.001,
    "z": 0.0007,
}
```

计算密文的词频：


```python
import string

def cipher_frequency():
    cipher_freq = {k: 0 for k in string.ascii_letters[:26]}
    counter = 0
    for k in cipher:
        if k in cipher_freq:
            cipher_freq[k] += 1
            counter += 1
    for k in cipher_freq:
        cipher_freq[k] = round(cipher_freq[k] / counter, 4)

    cipher_freq = dict(
        sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True)
    )

    print(cipher_freq)


cipher_frequency()
```

结果如下：

```python
cipher_freq = {
    "r": 0.13,
    "b": 0.1053,
    "m": 0.096,
    "k": 0.0759,
    "j": 0.0743,
    "w": 0.0728,
    "i": 0.0635,
    "p": 0.0464,
    "u": 0.0372,
    "d": 0.0356,
    "h": 0.0356,
    "v": 0.0341,
    "x": 0.031,
    "y": 0.0294,
    "n": 0.0263,
    "s": 0.0263,
    "t": 0.0201,
    "l": 0.0124,
    "o": 0.0108,
    "q": 0.0108,
    "a": 0.0077,
    "c": 0.0077,
    "e": 0.0077,
    "f": 0.0015,
    "g": 0.0015,
    "z": 0.0,
}
```
### 第一轮解密

把``cipher_freq``和``letter_freq`` 对比，进行第一轮解密，比如把密文里的r替换成e，把b替换成t.....

```
r = e
b = t
...
...
```

```python
def guess():

    decrypt_key = dict(zip(cipher_freq.keys(), letter_freq.keys()))

    decrypted_str = ""
    for s in cipher:
        if s in decrypt_key:
            decrypted_str += decrypt_key[s]
        else:
            decrypted_str += s
    return decrypted_str
```

经过第一轮猜测，我们会得到解密后的“明文”

```python
yecawse the fractnce iu the yasnc mijemeots iu bata ns
the uicws aod masterg iu selu ns the esseoce iu
matswyagashn rgw barate di n shall trg ti elwcndate the
mijemeots iu the bata accirdnop ti mg noterfretatnio
yased io uirtg gears iu stwdg
  nt ns oit ao easg tasb ti evflano each mijemeot aod nts
snponuncaoce aod sime mwst remano woevflanoed ti pnje a
cimflete evflaoatnio ioe kiwld haje ti ye xwalnuned aod
nosfnred ti swch ao evteot that he ciwld reach the state
iu eolnphteoed mnod cafayle iu reciponqnop siwodless
siwod aod shafeless shafe n di oit deem mgselu the unoal
awthirntg ywt mg evferneoce knth bata has leut oi diwyt
that the uilliknop ns the frifer afflncatnio aod
noterfretatnio n iuuer mg theirnes no the hife that the
esseoce iu ibnoakao barate knll remano notact
```

### 第二轮调整

通过第一轮纯词频的解密，得到的结果实际上可读性有了很大的提高，接下来可以进行几轮人工的调整。

比如 ``easg`` 应该是 ``easy``, 所以可以修改下我们的解密词典， 原本t翻译成g，应该改成t翻译成y
比如 ``mwst`` 应该是 ``must``,  原本n翻译成w，应该改成n翻译成u


调整后解密为

```python
yecause the fractnce iu the yasnc mijemeots iu bata ns
the uicus aod mastery iu selu ns the esseoce iu
matsuyayashn ryu barate di n shall try ti elucndate the
mijemeots iu the bata accirdnop ti my noterfretatnio
yased io uirty years iu study
  nt ns oit ao easy tasb ti evflano each mijemeot aod nts
snponuncaoce aod sime must remano uoevflanoed ti pnje a
cimflete evflaoatnio ioe kiuld haje ti ye xualnuned aod
nosfnred ti such ao evteot that he ciuld reach the state
iu eolnphteoed mnod cafayle iu reciponqnop siuodless
siuod aod shafeless shafe n di oit deem myselu the unoal
authirnty yut my evferneoce knth bata has leut oi diuyt
that the uilliknop ns the frifer afflncatnio aod
noterfretatnio n iuuer my theirnes no the hif
```

继续调整，比如

yecause 应该是 because

tasb 应该是 task


### 第N论调整

以此类推，经过几轮调整，我们就可以基本得到加密前的明文了。 下面是几轮过后的样子

```
because the practice of the basic movements of kata is
the focus and mastery of self is the essence of
matsubayashi ryu karate do i shall try to elucidate the
movements of the kata according to my interpretation
based on forty years of study
  it is not an easy task to explain each movement and its
significance and some must remain unexplained to give a
complete explanation one could have to be qualified and
inspired to such an extent that he could reach the state
of enlightened mind capable of recognizing soundless
sound and shapeless shape i do not deem myself the final
authority but my experience cith kata has left no doubt
that the follocing is the proper application and
interpretation i offer my theories in the hope that the
essence of okinacan karate cill remain intact
```

附代码

```python
import string

cipher = """lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi
bpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jx
ymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpr
yjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjk
lmird jk xjubt trmui jx ibndt
  wb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbi
iwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower m
vjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkd
wkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbr
jx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhrii
ijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmh
mnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlb
bpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkd
wkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bpr
riirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb"""

letter_freq = {
    "e": 0.127,
    "t": 0.0906,
    "a": 0.0817,
    "o": 0.0751,
    "i": 0.0697,
    "n": 0.0675,
    "s": 0.0633,
    "h": 0.0609,
    "r": 0.0599,
    "d": 0.0425,
    "l": 0.0403,
    "c": 0.0278,
    "u": 0.0276,
    "m": 0.0241,
    "w": 0.0236,
    "f": 0.0223,
    "g": 0.0202,
    "y": 0.0197,
    "p": 0.0193,
    "b": 0.015,
    "v": 0.0098,
    "k": 0.0077,
    "j": 0.0015,
    "x": 0.0015,
    "q": 0.001,
    "z": 0.0007,
}


def cipher_frequency():
    cipher_freq = {k: 0 for k in string.ascii_letters[:26]}
    counter = 0
    for k in cipher:
        if k in cipher_freq:
            cipher_freq[k] += 1
            counter += 1
    for k in cipher_freq:
        cipher_freq[k] = round(cipher_freq[k] / counter, 4)

    return dict(sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True))


cipher_freq = cipher_frequency()


def guess():

    decrypt_key = dict(zip(cipher_freq.keys(), letter_freq.keys()))
    # 调整
    decrypted_str = ""
    for s in cipher:
        if s in decrypt_key:
            decrypted_str += decrypt_key[s]
        else:
            decrypted_str += s
    return decrypted_str


def improve(cipher):
    improved_key = {
        "g": "y",
        "w": "u",
        "y": "b",
        "b": "k",
        "n": "i",
        "o": "n",
        "i": "o",
        "u": "f",
        "j": "v",
        "f": "p",
        "p": "g",
        "v": "x",
        "k": "c",
        "x": "q",
        "q": "z",
    }
    decrypted_str = ""
    for s in cipher:
        if s in improved_key:
            decrypted_str += improved_key[s]
        else:
            decrypted_str += s
    return decrypted_str


print(improve(guess()))

```

可以自己玩玩。