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

graph = {
    'F': ['E'],
    'E': ['C'],
    'C': ['A','B'],
    'A': [],
    'B': []
}
# def find_all_paths(graph, start, end, path=[]):
#     path = path + [start]
#     # if start == end:
#     #     return [path]
#     if start not in graph:
#         return []
#     paths = []
#     arrTask = graph[start]
#     if end in arrTask:
#         permuationTask = findPermutation(arrTask)
#         for permuation in permuationTask:
#             listTask = list(permuation)
#             tempPath = path[:]
#             tempPath = tempPath + listTask
#             paths.append(tempPath)
#     else:
#         for node in graph[start]:
#             if node not in path:
#
#                 newpaths = find_all_paths(graph, node, end, path)
#                 for newpath in newpaths:
#                     paths.append(newpath)
#     return paths

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


graph = createNodes()
graph = creatEdges(graph)

path = ['36']
arrTask = find_all_paths(graph,'36', '73', path)
getCorrectTopologicalOrder(arrTask)
print(arrTask)


# arr = ['112', '20']
# arr = ['a', 'b']
# print(findPermutation(arr))