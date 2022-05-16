from problem import Problem
from problems.palindrome import IsPalindrome
from problems.invert_binary_tree import InvertBinaryTree
from problems.astmath import ASTMath
from typing import List

problems: List[Problem] = [IsPalindrome(), InvertBinaryTree(), ASTMath()]

print(
    "Welcome to JeetQode, a place where you can solve programming problems with jq (https://stedolan.github.io/jq/)."
)
for i, prob in enumerate(problems):
    print("=" * 40)
    print(f"Problem #{i+1}: {prob.name}")
    print(prob.desciption)
    print("=" * 40)
    prog = input("Input a jq program: ")
    if len(prog) > 512:
        print("Too long!")
        exit()
    success, error = prob.judge(prog)
    if not success:
        print(error)
        exit()
    print(f'Congratulations! You solved "{prob.name}".')
    print()

with open("flag.txt") as f:
    print("Here's your flag:", f.read().strip())
