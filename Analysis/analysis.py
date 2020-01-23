from Label.label import *
import numpy as np

def calculateArea(radius):
    area = (math.pi * (radius**2))
    return area

def getAvgDistanceStdForEachPOI():
    hashMap = label()
    hashMapPOI = convertArrayPoiToHashMap()
    hashMapDistance = {}
    for poi in hashMap:
        point2dPoi = hashMapPOI[poi]
        arrayPoint = hashMap[poi]['arrayPoints']
        res = []
        for point in arrayPoint:
            dist = distance(point2dPoi,point)
            res.append(dist)
        averageDist = np.mean(res)
        std = np.std(res)
        obj = {'averageDist': averageDist, 'standardDeviation': std}
        hashMapDistance[poi] = obj
    return hashMapDistance

def getRadiusDensity():
    hashMap = label()
    hashMapRadiusDensity = {}

    for poi in hashMap:
        numberRequests = len(hashMap[poi]['arrayPoints'])
        radius = hashMap[poi]['farestDist']
        area = calculateArea(radius)
        density = numberRequests / area
        tempObj = {'radius': radius, 'density': density}
        hashMapRadiusDensity[poi] = tempObj

    return hashMapRadiusDensity

print(getRadiusDensity())
