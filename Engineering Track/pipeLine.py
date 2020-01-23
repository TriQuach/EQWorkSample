from itertools import permutations
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction


def findPermutation(arrTask):
    res = []
    for p in permutations(arrTask):
        res.append(p)

    return res


def createNodes():
    f = open("task_ids.txt", "r")
    graph = {}
    for line in f:
        word = line.split(',')
        for w in word:
            if w not in graph:
                graph[w] = []
    return graph

def creatEdges(graph):

    f = open("relations.txt", "r")
    for line in f:
        word = line.split('->')
        tempArr = graph[word[1].strip('\n')]
        tempArr.append(word[0])
        graph[word[1].strip('\n')] = tempArr
    return graph

def getQuestion():
    f = open("question.txt", "r")
    res = []
    count = 0
    for line in f:
        count += 1
        word = line.split(' ')
        task = word[-1].strip('\n')
        if word[0] == 'starting':
            objStart = {'start': task}
            res.append(objStart)
        else:
            objEnd = {'end': task}
            res.append(objEnd)

    return res

graph = {
    'F': ['E', 'K'],
    'K': ['C'],
    'E': ['C'],
    'C': ['A','B'],
    'A': [],
    'B': []
}

def find_all_paths(graph, start, end, path):

    if start == end:
        return [path]
    paths = []

    for node in graph[start]:
        if node not in path:
            arrTask = graph[start]
            permutaionTask = findPermutation(arrTask)
            for permuation in permutaionTask:
                listTask = list(permuation)

                tempPath = path[:] + listTask
                newpaths = find_all_paths(graph, node, end, tempPath)
                for newpath in newpaths:
                    if newpath not in paths:
                        paths.append(newpath)
    return paths

def reverseArray(arr):
    start = 0
    end = len(arr) - 1
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

def getCorrectTopologicalOrder(arrTask):
    for pipeLine in arrTask:
        reverseArray(pipeLine)

def getNecessityAndSufficiency(start,arrTask):
    lastCheckPoint = start[-1]
    res = []
    for pipeLine in arrTask:
        index = pipeLine.index(lastCheckPoint)
        reducedLength = pipeLine[index:]
        if len(reducedLength) > 2:
            if reducedLength not in res:
                res.append(reducedLength)

    return res

def getPipiLine(question, graph):
    for i in range(0,len(question) - 1,2):
        start = question[i]['start']

        start = start.split(',')
        end = question[i+1]['end']
        path = [end]
        arrTask = find_all_paths(graph, end, start[0], path)
        getCorrectTopologicalOrder(arrTask)
        if len(start) > 1:
            arrTask = getNecessityAndSufficiency(start,arrTask)

        print('--------- *** ---------')
        print('PipeLine for starting task:' + str(start) + ', goal task:' + str([end]))
        print(arrTask)
        print('--------- *** ---------')
        print('\n')

graph = createNodes()
graph = creatEdges(graph)

question = getQuestion()

getPipiLine(question, graph)
