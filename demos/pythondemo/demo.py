import string

fin = open('emory.txt')
fout = open('emory.txt.tokenized', 'w')

tokens = list()

for line in fin:
    l = line.split()

    for token in l:
        beginIndex = 0
        currIndex = 0

        for c in token:
            if c in string.punctuation:
                if beginIndex < currIndex:
                    tokens.append(token[beginIndex:currIndex])
                tokens.append(c)
                beginIndex = currIndex + 1

            currIndex += 1

        if beginIndex < len(token):
            tokens.append(token[beginIndex:])

for token in tokens:
    fout.write(token + '\n')

fin.close()
fout.close()
