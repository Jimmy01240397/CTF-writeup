import string
import random


def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x


def encrypt(T, file):
    with open(file) as f:
        pt = f.read()
    with open(f"{file}.enc", "w") as f:
        f.write(pt.translate(T))


charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
shuffled = "".join(shuffle(charset))
T = str.maketrans(charset, shuffled)

encrypt(T, "flag.txt")
encrypt(T, __file__)

"""
Substitution cipher
From Wikipedia, the free encyclopedia
Jump to navigationJump to search

This article needs additional citations for verification. Please help improve this article by adding citations to reliable sources. Unsourced material may be challenged and removed.
Find sources: "Substitution cipher" – news · newspapers · books · scholar · JSTOR (March 2009) (Learn how and when to remove this template message)
In cryptography, a substitution cipher is a method of encrypting in which units of plaintext are replaced with the ciphertext, in a defined manner, with the help of a key; the "units" may be single letters (the most common), pairs of letters, triplets of letters, mixtures of the above, and so forth. The receiver deciphers the text by performing the inverse substitution process to extract the original message.

Substitution ciphers can be compared with transposition ciphers. In a transposition cipher, the units of the plaintext are rearranged in a different and usually quite complex order, but the units themselves are left unchanged. By contrast, in a substitution cipher, the units of the plaintext are retained in the same sequence in the ciphertext, but the units themselves are altered.

There are a number of different types of substitution cipher. If the cipher operates on single letters, it is termed a simple substitution cipher; a cipher that operates on larger groups of letters is termed polygraphic. A monoalphabetic cipher uses fixed substitution over the entire message, whereas a polyalphabetic cipher uses a number of substitutions at different positions in the message, where a unit from the plaintext is mapped to one of several possibilities in the ciphertext and vice versa.


Contents
1	Simple substitution
1.1	Security for simple substitution ciphers
2	Nomenclator
3	Homophonic substitution
4	Polyalphabetic substitution
5	Polygraphic substitution
6	Mechanical substitution ciphers
7	The one-time pad
8	Substitution in modern cryptography
9	Substitution ciphers in popular culture
10	See also
11	References
12	External links
"""
