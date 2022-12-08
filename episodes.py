#
# @author: Brian
#
import datetime
import time
import random
import math
import pprint

class Episodes():
    def __init__(self, episode):
        self.name = episode["name"]
        self.number = episode["number"]
        self.fileName = episode["fileName"]
        self.wordList = []
        self.characterList = []
        self.knowledgeBase = []
        self.wordStats = []
        self.wordListStats = []
        self.characterListStats = []
        self.pp = pprint.PrettyPrinter(width=70, compact=True)

    def readEpisode(self, episode):
        words = []
        with open(episode) as f:
            n = 0
            w = f.readline()
            #print("readEpisode: %s"%(w))
            while (w):
                n += 1
                xList = w.split(' ')
                for y in xList:
                    x = self.cleanData(y)
                    if(x):
                        words.append(x)
                w = f.readline()
                #print("# readEpisode: %s, \n%s \n%s"%(n, w, len(words)))
        print("fileLines: ", n)
        #print("words: ", words)
        self.wordStats = self.wordStatsAnalysis(words)
        print("#1-------------#\n")
        self.wordListStats = self.wordStatistics(words)
        print("#2-------------#\n")
        characterListX = readCharacters(self, words)
        self.characterListStats = self.wordStatistics(characterListX, True)
        print("#3-------------#\n")
        self.wordList = words
        self.characterList = characterListX
        print("\n")
        self.pp.pprint("wordListStats: %s \n"%(self.wordListStats))
        print("\n")
        self.pp.pprint("characterListStats: %s \n"%(self.characterListStats))
        print("\n")
        self.pp.pprint("knowledgeBase: %s \n"%(self.knowledgeBase))
        print("\n")
        return words


    def wordStatsAnalysis(self, listx):
        shortest = len(listx[0])
        shortestWord = listx[0]
        longest = len(listx[0])
        longestWord = listx[0]
        n = len(listx)
        sumx = 0
        listXY = []
        listY = []
        for x in listx:
            y = len(x)
            if(y < shortest):
                shortest = y
                shortestWord = x
            if(y > longest):
                longest = y
                longestWord = x
            sumx += y
            listXY.append({x, y})
            listY.append(y)
        mean = self.average(sumx, n)
        s = self.standardDeviation(listY, mean)
        listXY.append({"firstShortestWord": shortestWord, "shortest": shortest})
        listXY.append({"firstLongestWord": longestWord, "longest": longest})
        listXY.append({"mean": mean, "standardDeviation": s})
        #print("wordStatsAnalysis: %s"%(listXY))
        return listXY

    def wordStatistics(self, listx, symbols=False):
        self.sortList(listx)
        n = len(listx)
        wordx = listx[0]
        countx = 0
        least = n
        most = 0
        listY = []
        listXY = []
        sumx = 0
        leastWord = wordx
        mostWord = wordx
        done = False
        def addCountX(wordx2, x2, countx2, sumx2, least2, leastWord2, most2, mostWord2, done2):
            #print("wordx: %s, leastWord: %s, least: %s"%(wordx2, leastWord2, least2))
            #print("countx: %s, mostWord: %s, most: %s"%(countx2, mostWord2, most2))
            if(countx2 < least2):
                least2 = countx2
                leastWord2 = wordx2
            if(countx2 > most2):
                most2 = countx2
                mostWord2 = wordx2
            done2 = True
            listXY.append({wordx2, countx2})
            listY.append(countx2)
            self.knowledgeBase.append(wordx2)
            sumx2 += countx2
            wordx2 = x2
            countx2 = 1
            return [wordx2, x2, countx2, sumx2, least2, leastWord2, most2, mostWord2, done2]

        for x in listx:
            if(wordx == x):
               countx += 1
               done = False
            else:
               wordx, x23, countx, sumx, least, leastWord, most, mostWord, done = addCountX(wordx, x, countx, sumx, least, leastWord, most, mostWord, done)
        if (done == False):
            wordx, x23, countx, sumx, least, leastWord, most, mostWord, done = addCountX(wordx, wordx, countx, sumx, least, leastWord, most, mostWord, done)
        #print("listXY: %s"%(listXY))
        #print("listY: %s"%(listY))
        #print("knowledgeBase: %s"%(self.knowledgeBase))
        mean = self.average(sumx, n)
        s = self.standardDeviation(listY, mean)
        if(symbols):
           listXY.append({"firstLeastCharacter": leastWord, "least": least})
           listXY.append({"firstMostCharacter": mostWord, "most": most})
        else:
            listXY.append({"firstLeastWord": leastWord, "least": least})
            listXY.append({"firstMostWord": mostWord, "most": most})
        listXY.append({"mean": mean, "standardDeviation": s})
        #print("wordStatistics: %s, \n knowledgeBase: %s, \nsize: %s"%(listXY, self.knowledgeBase, len(self.knowledgeBase)))
        return listXY


    def averageX(self, listx):
        n = len(listx)
        sumx = 0
        if(n == 0):
            return None
        for y in listx:
            sumx += y
        mean = (sumx/n)
        #print("average: %s / %s = %s"%(sumx, n, mean))
        return mean

    def average(self, sumx, n):
        if(n > 0):
            mean = (sumx/n)
            print("average: %s / %s = %s"%(sumx, n, mean))
            return mean

    def standardDeviation(self, listx, mean):
        n = len(listx)
        sumy = 0
        for y in listx:
            sumy += ((y - mean)*(y - mean))
        if(n > 0):
            xy = (sumy/n)
            s = math.sqrt(xy)
            print("standardDeviation: sqrt(%s / %s) = %s"%(sumy, n, s))
            return s


    def decode(self, data, pasw):
        info = data^pasw
        return info

    def encode(self, data, pasw):
        info = data^pasw
        return info

    def cleanData(self, data, symbols=False):
        reserved = ['~', '`', '.', ',', '!', '?', ';', ':', '\'', '\"', '\n', '[', ']', '(', ')', '{', '}', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#']
        if(symbols == True):
            reserved = ['~', '`', '.', ',', '!', '?', ';', ':', '\'', '\"', '\n', '[', ']', '(', ')', '{', '}', '#']
        if(data in reserved):
            return False
        n = len(data)
        #print("n: %s, data: %s"%(n, data))
        if(n < 1):
            return False
        x = data[n-1]
        if(x in reserved):
            data = data[:n-1]
        #check for '.'.
        n2 = len(data)
        x2 = data[n2-1]
        while ((x2 in reserved) & (n2 > 0)):
            if(x2 in reserved):
                data = data[:n2-1]
            n2 = len(data)
            #print("#x2 n2: %s, data: %s"%(n2, x2))
            if(n2 > 0):
                x2 = data[n2-1]
            else:
                return False
        #check for '[],{},()'.
        n1 = len(data)
        x1 = data[0]
        while ((x1 in reserved) & (n1 > 0)):
            if(x1 in reserved):
                data = data[1:]
            n1 = len(data)
            #print("#x1 n1: %s, data: %s"%(n1, x1))
            if(n1 > 0):
                x1 = data[0]
            else:
                return False
        #print("n1: %s, data: %s"%(n1, data))
        return data

    def sortList(self, listx):
        sortListX(listx)

    def printStatsX(self, listx):
        n = len(listx)
        if(n > 0):
            listXY = listx[n-3:]
            self.pp.pprint(listXY)
        else:
            self.pp.pprint("n: %s"%(n))
        print("n: %s\n------------"%(n))

    def printStats(self):
        print("### Statistical analysis for: ###")
        print("Name: %s, \nNumber: %s, \nFileName: %s"%(self.name, self.number, self.fileName))
        print("### Date: %s ### \n---------------------------------"%(myDbtime()))
        #
        print("#1-------------#\n")
        self.printStatsX(self.wordStats)
        print("#2-------------#\n")
        self.printStatsX(self.wordListStats)
        print("#3-------------#\n")
        self.printStatsX(self.characterListStats)
        #

def sortListX(listx):
    sortWordList(listx, 0, len(listx) - 1)
    #print("#1 sortListX: %s"%(listx))

def sortWordList(dataList, leftIndex, rightIndex):
    if(leftIndex >= rightIndex):
        return
    left = leftIndex
    right = rightIndex
    m = (leftIndex + rightIndex)//2
    DataLen = len(dataList)
    middle = dataList[m]
    #print("DataLen: %s, left: %s, right: %s, middle: %s"%(DataLen, left, right, m))
    while (left <= right):
        #print('left: ',left,'right: ',right)
        while ((left < rightIndex) & (dataList[left] < middle)):
            left += 1
            #print(dataList[left])

        while ((right > leftIndex) & (dataList[right] > middle)):
            right -= 1
            #print(dataList[right])
            #print('dataList[',right,']')

        if(left <= right):
            if(left < right):
                temp = dataList[left]
                dataList[left] = dataList[right]
                dataList[right] = temp
            left += 1
            right -= 1

    sortWordList(dataList, leftIndex, right)
    sortWordList(dataList, left, rightIndex)

def readCharacters(episode, listx):
    symbols = []
    for x in listx:
        for y in x:
            xy = episode.cleanData(y)
            if(xy):
                symbols.append(y)
    n = len(symbols)
    print("readCharacters: %s"%(n))
    return symbols

def testData():
    episode23 = {"name": "Cool23", "number": 23, "fileName": "sound.txt"}
    test23 = Episodes(episode23)
    print("Episodes: %s, name: %s, number: %s, fileName: %s"%(test23, test23.name, test23.number, test23.fileName))
    #
    data23 = test23.readEpisode(test23.fileName)
    test23.printStats()
    #

def testDataX():
    episode23 = {"name": "CoolData", "number": 26, "fileName": "README.md"}
    test23 = Episodes(episode23)
    print("Episodes: %s, name: %s, number: %s, fileName: %s"%(test23, test23.name, test23.number, test23.fileName))
    #
    data23 = test23.readEpisode(test23.fileName)
    test23.printStats()
    #


def testEpisde():
    test1 = Episodes
    print("Episodes: %s"%(test1))

    episode = {"name": "Cool", "number": 23, "fileName": "README.md"}
    test2 = Episodes(episode)
    print("Episodes: %s, %s, %s"%(test2.name, test2.number, test2.fileName))

    episode3 = {"name": "Cool3", "number": 323, "fileName": "sound.txt"}
    test3 = Episodes(episode3)
    print("Episodes: %s, name: %s, number: %s, fileName: %s"%(test3, test3.name, test3.number, test3.fileName))

    average = test2.averageX(test2.wordList)
    print("Stats: %s"%(average))

    mean = test2.average(10, 5)
    print("Stats: %s"%(mean))

    info = test2.encode(100, 352)
    print("encode: %s"%(info))

    info2 = test2.decode(info, 352)
    print("decode: %s"%(info2))
    ##############

    data3 = test3.readEpisode(test3.fileName)
    print("readEpisode: %s"%(data3))

    test4 = "test4"
    n = len(test4)
    test5 = test4[:n-1]
    print("test5: %s, %s"%(test5, test4))

def myDbtime():
    now = datetime.datetime.now()
    return now


if __name__ == '__main__':
    try:
        #testEpisde()
        print("#\n#testData-------------------#\n#\n")
        testData()
        print("#\n#testDataX------------------#\n#\n")
        testDataX()
    except Exception as e:
        print("@main: %s, \nTime: %s"%(e, myDbtime()))
