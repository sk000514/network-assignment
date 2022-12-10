import enchant as en
import random


def isword(word: str):
    d = en.Dict("en_US")
    return d.check(word)

# green 2 yellow 1 gray 0


def wordcheck(word1: str, word2: str):
    result = [0 for i in range(5)]
    tmp = {}

    word1 = word1.lower()
    word2 = word2.lower()
    for i in range(5):
        if word2[i] not in tmp:
            tmp[word2[i]]=1
        else:
            tmp[word2[i]]+=1
    for i in range(5):
        if word1[i] == word2[i]:
            result[i] = 2
            tmp[word2[i]]-=1
    for i in range(5):
        if word1[i] in tmp and tmp[word1[i]]!=0 and result[i]!=2:
            result[i] = 1
            tmp[word1[i]]-=1
    return result

#print(wordcheck("adieu",'punts'))
# print(isword("word"))


def word_generator():
    r = random.randint(1, 5152)
    with open('./wordle_word.txt', 'r') as f:
        word = f.readlines()[r-1]
    return word
