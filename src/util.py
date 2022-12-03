import enchant as en
import random


def isword(word: str):
    d = en.Dict("en_US")
    return d.check(word)

# green 2 yellow 1 gray 0


def wordcheck(word1: str, word2: str):
    result = [0 for i in range(5)]
    word1 = word1.lower()
    word2 = word2.lower()
    for i in range(5):
        if word1[i] in word2:
            result[i] += 1
        if word1[i] == word2[i]:
            result[i] += 1
    return result

# print(wordcheck("hello", "helow"))
# print(isword("word"))


def word_generator():
    r = random.randint(1, 6580)
    with open('./wordle_word.txt', 'r') as f:
        word = f.readlines()[r-1]
    return word
