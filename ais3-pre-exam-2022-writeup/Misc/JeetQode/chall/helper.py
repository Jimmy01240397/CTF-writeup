from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
import json
from typing import Tuple


def run_jq(json_str: str, program: str) -> Tuple[bool, str]:
    with NamedTemporaryFile() as jf, NamedTemporaryFile() as pf:
        jf.write(json_str.encode())
        jf.flush()
        pf.write(program.encode())
        pf.flush()
        p = Popen(["jq", "-f", pf.name, jf.name], shell=False, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        if error:
            return False, error.decode().strip()
        else:
            return True, output.decode().strip()


if __name__ == "__main__":
    print(run_jq(json.dumps({"a": 1, "b": 2}), ".a+.b"))
