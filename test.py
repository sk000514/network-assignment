import enchant as en

g=open ("wordle_word_final.txt", 'w')
with open("wordle_word.txt", "r") as f:
    d=en.Dict("en_US")
    for line in f:
        if d.check(line[:5]):
            g.write(line)
	
g.close()
