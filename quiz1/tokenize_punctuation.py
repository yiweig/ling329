import string

fin = open('emory.txt')
fout = open('emory.txt.tokenized', 'w')

tokens = list()

for line in fin:
    l = line.split()

    for token in l:
        beginIndex = 0

        for currIndex, c in enumerate(token):
            if c in string.punctuation:
                if c == '.' and 0 < currIndex and token[currIndex - 1].isupper():
                    continue

                if beginIndex < currIndex:
                    tokens.append(token[beginIndex:currIndex])

                if c == "'" and token[currIndex + 1] == 's':
                    newEnd = currIndex + 2
                    tokens.append(token[currIndex:newEnd])
                    beginIndex = newEnd

                    if newEnd == len(token):
                        break
                else:
                    tokens.append(c)
                    beginIndex = currIndex + 1

        if beginIndex < len(token):
            pass
        tokens.append(token[beginIndex:])

for token in tokens:
    fout.write(token + '\n')

fin.close()
fout.close()
