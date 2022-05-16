from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Tuple
from helper import run_jq
import json


class Problem(ABC):
    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def desciption(self) -> str:
        pass

    @abstractproperty
    def rounds(self) -> int:
        pass

    @abstractmethod
    def generate_testcase(self) -> Tuple[Any, Any]:
        pass

    def dumps(self, x):
        return json.dumps(x)

    def judge_one(self, program: str) -> Tuple[bool, Any]:
        data, answer = self.generate_testcase()
        success, output = run_jq(self.dumps(data), program)
        _, answer_normalized = run_jq(self.dumps(answer), ".")  # normalize
        if success:
            if output != answer_normalized:
                return (
                    False,
                    f"Expecting {answer_normalized}, but got {output} instead.",
                )
            return True, None
        else:
            return False, output

    def judge(self, program: str) -> Tuple[bool, Any]:
        for _ in range(self.rounds):
            success, err = self.judge_one(program)
            if not success:
                return False, err
        return True, None
