from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha1
import os

flag = os.environb[b"FLAG"]


# parameters generation
# openssl dhparam 2048 > params.dh
# openssl asn1parse < params.dh
p = 0xAFCAFD4482568D44AF985A4E4575AE8EAF3C843E69C1D4E4AFAE1B4BCDABE0034D7010C845A88BE94BDA402B9ACE25ADD7378A6AFAFE0E9798C9C0C93C6C81439E872DC77078CBD2BA0E140C29AEBCE89854D43700D4946B6C8E4BA5E6058FA2794207AD1F2CA9CCE64DE971F99EFDAA6AFD34B0B98F0132A8689DB5B371E6602C3A81D17D1BAE4FD350217A8C531555DF1FB06A9BDB536AE8F2A23EF04FC9D1825A3280F3ADAD4A2B34C4C04040AC748E72D953EB15EA743A5C4D941641874AD79DABD35A47394124BF1944BD84E64D094AC1442C49A293EF7B52DB3A7C1D67F1DE80AA4DF4E0221B43194C0721F9183199CD0991BDBA45FAE080B68EAE184B
q = (p - 1) // 2
g = 2
assert isPrime(p) and isPrime(q) and pow(g, q, p) != 1


def keygen():
    x = getRandomRange(1, p)
    y = pow(g, x, p)
    return x, y


def H(m: bytes):
    return sha1(m).digest()


def gen_k(m: bytes, x: int):
    # generate a deterministic nonce
    k = H(m + long_to_bytes(x))
    while len(k) < 256:
        # ensure k is long enough to prevent lattice attacks
        k += H(k + long_to_bytes(x))
    return bytes_to_long(k) % q


def sign(m: bytes, x: int):
    h = bytes_to_long(H(H(m) + m))
    k = gen_k(m, x)
    r = pow(g, k, p) % q
    s = (pow(k, -1, q) * (h + r * x)) % q
    return r, s


print(
    "Welcome to our signing service, you can sign anything you want but you can't get our private key."
)

x, y = keygen()
print("Our public key:")
print(f"{y = }")

key = sha1(str(x).encode()).digest()[:16]
flag_ct = AES.new(key, AES.MODE_ECB).encrypt(pad(flag, 16))
print("Flag encryted with our private key:")
print(f"{flag_ct.hex() = }")

for _ in range(16):
    m = bytes.fromhex(input("m = "))
    if len(m) > 512:
        print("Why would you want to sign such a long message?")
        break
    if len(m) == 0:
        print("Bye~")
        break
    print(f"{sign(m, x) = }")
else:
    print("Too much signature signed...")
