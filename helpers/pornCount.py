def countPorn():
    usersByLine = {}
    lines = []

    with open('pornCounter.txt', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        name, count = line.split('\t')
        usersByLine[name] = int(count)

    returnString = ''
    for name in usersByLine:
        returnString = returnString + name + ': ' + str(usersByLine[name]) + '\n'

    return returnString

def addPorn(user):
    usersByLine = {}
    lines = []
    
    with open('pornCounter.txt', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        name, count = line.split('\t')
        usersByLine[name] = int(count)

    try:
        usersByLine[user] = usersByLine[user] + 1
    except KeyError:
        usersByLine[user] = 1

    with open('pornCounter.txt', 'w') as f:
        for keyName in usersByLine:
            f.write(keyName + '\t' + str(usersByLine[keyName]) + '\n')
