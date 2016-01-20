fin = open('emory.txt')
fout = open('emory.txt.tokenized', 'w')

for line in fin:
    print line,
    fout.write(line)

fin.close()
fout.close()
