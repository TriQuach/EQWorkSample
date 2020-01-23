from Label.label import *
import numpy as np
def convertArrayPoiToHashMap():
    res = loadPOI()
    hashMapPOI = {}
    for poi in res:
        obj = Poin2d(poi.lat,poi.long)
        hashMapPOI[poi.POIID] = obj
    return hashMapPOI
def getAvgDistanceStdForEachPOI():
    hashMap = label()
    hashMapPOI = convertArrayPoiToHashMap()
    hashMapDistance = {}
    for poi in hashMap:
        point2dPoi = hashMapPOI[poi]
        arrayPoint = hashMap[poi]
        res = []
        for point in arrayPoint:
            dist = distance(point2dPoi,point)
            res.append(dist)
        averageDist = np.mean(res)
        std = np.std(res)
        obj = {'averageDist': averageDist, 'standardDeviation': std}
        hashMapDistance[poi] = obj
    return hashMapDistance
