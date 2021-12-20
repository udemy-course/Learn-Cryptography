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
