from PIL import Image

def readPixels(path):
    im = Image.open(path, 'r')
    pixVals = list(im.getdata())
    for i in range(len(pixVals)):
        if (pixVals[i] == (255, 255, 255, 255)):
            pixVals[i] = 0
        else:
            pixVals[i] = 1
    realPixVals = []
    #turns to 2D array
    for i in range(32):
        realPixVals +=  [pixVals[32 * i: 32 * (i + 1)]]
    return realPixVals

def printVals(pixVals):
    for i in range(32):
        print pixVals[32 * i: 32 * (i + 1)]

def readWeightedVals(path):
    f = open(path, 'rU').read().split('\n')
    for i in range(len(f)):
        f[i] = f[i].split(',')
    for i in range(len(f)):
        for x in range(len(f[i])):
            f[i][x] = float(f[i][x])
    return f

#number is the word: ex. seven; eleven; twentyone
def teach(number, start, end):
    store = []
    for i in range(32):
        store += [[0]*32]
    for i in range(start, end + 1):
        pix = readPixels(number + '/' + number + str(i) + '.png')
        for row in range(32):
            for col in range(32):
                store[row][col] += pix[row][col]
    for row in range(32):
        for col in range(32):
            store[row][col] /= float(end - start + 1)

    f = open(number + '.store', 'w+')
    toWrite = store
    for i in range(len(toWrite)):
        for x in range(32):
            toWrite[i][x] = str(toWrite[i][x])
        toWrite[i] = ','.join(toWrite[i])
    toWrite = '\n'.join(toWrite)
    f.write(toWrite)
    f.close()

    f = open('knownVals.store', 'rU')
    text = f.read().split(',')
    while '' in text:
        text.remove('')
    if number not in text:
        text += [number]
    text = ','.join(text)
    f = open('knownVals.store', 'w+')
    f.write(text)
    f.close()


def recognize(path):
    knownVals = open('knownVals.store', 'rU').read().split(',')

    toTest = readPixels(path)
    grades = []

    for testingAgainstNum in knownVals:
        toAdd = [0, testingAgainstNum]
        weigths = readWeightedVals(testingAgainstNum + '.store')
        for row in range(32):
            for col in range(32):
                if toTest[row][col] == 1:
                    toAdd[0] += weigths[row][col]
                    #print toAdd
        grades += [toAdd]

    grades = sorted(grades, key=lambda x: x[0], reverse=True)

    return grades











