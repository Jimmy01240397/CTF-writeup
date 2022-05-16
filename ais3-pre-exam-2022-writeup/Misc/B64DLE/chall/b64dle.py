from abc import ABC, abstractmethod
from enum import Enum
from base64 import b64encode, b64decode
from typing import List


class RoundResult(Enum):
    error = 0
    fail = 1
    win = 2


class Wordle(ABC):
    def __init__(self, target: str, rounds: int):
        self.target = target
        self.rounds = rounds
        self.cur_round = 1

    def play(self):
        while self.cur_round <= self.rounds:
            result = self.play_round(self.cur_round)
            if result == RoundResult.error:
                print("Invalid input")
                continue
            elif result == RoundResult.win:
                return True
            self.cur_round += 1
        return False

    def play_round(self, round) -> RoundResult:
        inp = input(f"Round {round} > ")
        if not self.check_input(inp):
            return RoundResult.error
        diff = self.compare(inp, self.target)
        if self.is_win(diff):
            return RoundResult.win
        else:
            print(diff)
            return RoundResult.fail

    @abstractmethod
    def check_input(self, s: str) -> bool:
        pass

    @abstractmethod
    def compare(self, s: str, target: str) -> str:
        pass

    @abstractmethod
    def is_win(self, s: str) -> bool:
        pass


class B64dle(Wordle):
    def __init__(self, words: List[str], target: str, rounds: int):
        super().__init__(b64encode(target.encode()).decode(), rounds)
        self.words = words
        self.exact = "O"
        self.contains = "-"
        self.wrong = "X"

    def check_input(self, s: str) -> bool:
        try:
            word = b64decode(s.encode()).decode()
            if word not in self.words:
                return False
            return len(s) == len(self.target)
        except:
            return False

    def compare(self, s: str, target: str) -> str:
        assert len(s) == len(target)
        ret = ""
        for i, c in enumerate(s):
            if c == target[i]:
                ret += self.exact
            elif c in target:
                ret += self.contains
            else:
                ret += self.wrong
        return ret

    def is_win(self, s: str) -> bool:
        return all([x == self.exact for x in s])


with open("five_letter_words.txt") as f:
    # https://raw.githubusercontent.com/charlesreid1/five-letter-words/b45fda30524a981c73ec709618271cecfb51c361/sgb-words.txt
    words = list(map(str.strip, f))
