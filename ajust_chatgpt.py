import os

PATH = '.'
for fileName in os.listdir(PATH):
    if fileName.startswith('Saved_Chat_GPT_') and fileName.endswith('.txt'):
        newName = fileName[:-4] + '.md'
        print(fileName, '->', newName)

        title = 1
        if PATH == '.':
            PATH = ''
        with open(PATH + newName, 'w') as w:
            for line in open(PATH + fileName):
                if line == '--------------------------\n':
                    if title:
                        w.write(line)
                    else:
                        w.write('\n\n')
                    title = 1 - title
                elif not line.startswith('NEW'):
                    w.write(line.replace('# ', '### '))
        os.remove(PATH + fileName)