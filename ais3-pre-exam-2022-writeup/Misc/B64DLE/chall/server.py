from b64dle import B64dle, words
from Crypto.Cipher import AES
from os import urandom
from base64 import b64decode, b64encode
from random import choice
import pickle
import io


class Player:
    def __init__(self, name, wins=0, words=[]):
        self.name = name
        self.wins = wins
        self.words = words
        self.profile_tmpl = "=== Player {user.name} ===\nWins: {user.wins}\nGuessed words: {user.words}\n"

    def __repr__(self):
        return self.profile_tmpl.format(user=self)

    def __reduce__(self):
        return (
            Player,
            (
                self.name,
                self.wins,
                self.words,
            ),
        )


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == __name__ and name == "Player":
            return Player
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))


def restricted_loads(s):
    return RestrictedUnpickler(io.BytesIO(s)).load()


def encrypt(key: bytes, msg: bytes, nonce=urandom(8)):
    cip = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cip.encrypt(msg), nonce


def decrypt(key: bytes, ct: bytes, nonce: bytes):
    cip = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cip.encrypt(ct)


def game_loop(player: Player):
    while True:
        # fmt: off
        print("""
=== B64DLE ===
1. Show status
2. Play game
3. Save progress
4. Logout
"""[1:-1])
        # fmt: on
        c = int(input("> "))
        print(c)
        if c == 1:
            print(player)
        elif c == 2:
            target = choice(words)
            game = B64dle(words, target, 6)
            win = game.play()
            if win:
                player.wins += 1
                player.words.append(target)
                print("You win!")
            else:
                print("You lose...")
        elif c == 3:
            if player.wins == 0:
                print("Sorry, your game progress isn't worth saving...")
                continue
            data = pickle.dumps(player)
            ct, nonce = encrypt(KEY, data)
            print("Login token:", b64encode(nonce + ct).decode())
        elif c == 4:
            print("Logging out...")
            return
        else:
            print("???")


def menu():
    while True:
        # fmt: off
        print("""
=== B64DLE ===
1. Register
2. Login
3. Exit
"""[1:-1])
        # fmt: on
        c = int(input("> "))
        if c == 1:
            name = input("What's your name? ")
            player = Player(name)
            game_loop(player)
        elif c == 2:
            tmp = b64decode(input("Login token: ").encode())
            nonce, ct = tmp[:8], tmp[8:]
            try:
                player = restricted_loads(decrypt(KEY, ct, nonce))
            except ValueError:
                print("Login Failed...")
                continue
            game_loop(player)
        elif c == 3:
            print("Bye")
            return
        else:
            print("???")


if __name__ == "__main__":
    KEY = urandom(16)
    menu()
