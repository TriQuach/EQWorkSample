from CleanUp.cleanUp import *
import math
class POI:
    def __init__(self, POIID, lat, long):
        self.POIID = POIID
        self.lat = lat
        self.long = long
class Poin2d:
    def __init__(self,lat, long):
        self.lat = lat
        self.long = long
def loadPOI():
    res = []
    df = pd.read_csv('../Data/POIList.csv')
    for index, row in df.iterrows():
        point = POI(row['POIID'], row['Latitude'], row['Longitude'])
        res.append(point)
    return res

def convertArrayPoiToHashMap():
    res = loadPOI()
    hashMapPOI = {}
    for poi in res:
        obj = Poin2d(poi.lat,poi.long)
        hashMapPOI[poi.POIID] = obj
    return hashMapPOI

def sqr(x) :
    return x*x

def distance(a, b):
  return math.sqrt(sqr(a.lat-b.lat)+sqr(a.long-b.long))

def getClosestPOI(point,arrayPOI):
    closestPOI = ''

    minDist = float('inf')
    for poi in arrayPOI:
        point2dPoi = Poin2d(poi.lat,poi.long)
        dist = distance(point,point2dPoi)
        if dist < minDist:
            minDist = dist
            closestPOI = poi.POIID

    return closestPOI


def assignPOI2Request(df):
    arrayPOI = loadPOI()
    hashMapPOI = convertArrayPoiToHashMap()
    hashMap = {}

    for index, row in df.iterrows():
        requestGeo = Poin2d(row['Latitude'], row['Longitude'])
        closestPOI = getClosestPOI(requestGeo,arrayPOI)
        dist = distance(requestGeo, hashMapPOI[closestPOI])
        if closestPOI not in hashMap:
            tempObj = {'arrayPoints': [requestGeo], 'farestPoint': requestGeo, 'farestDist': dist}
            hashMap[closestPOI]= tempObj
        else:
            tempArrPoint = hashMap[closestPOI]['arrayPoints']
            tempArrPoint.append(requestGeo)
            hashMap[closestPOI]['arrayPoints'] = tempArrPoint
            if dist > hashMap[closestPOI]['farestDist'] and dist < 20:
                hashMap[closestPOI]['farestDist'] = dist
                hashMap[closestPOI]['farestPoint'] = requestGeo



    return hashMap

def getHashMapLatLongForPlot(df):
    arrayPOI = loadPOI()
    hashMapPOI = convertArrayPoiToHashMap()
    hashMapLatLong = {}
    for index, row in df.iterrows():
        requestGeo = Poin2d(row['Latitude'], row['Longitude'])
        closestPOI = getClosestPOI(requestGeo,arrayPOI)
        if distance(requestGeo,hashMapPOI[closestPOI]) < 20:
            if closestPOI not in hashMapLatLong:

                col_names = ['lat', 'long']
                dfLatLong = pd.DataFrame(columns=col_names)
                obj = {'lat': requestGeo.lat, 'long': requestGeo.long}
                dfLatLong.loc[len(dfLatLong)] = obj
                hashMapLatLong[closestPOI] = dfLatLong

            else:
                dfLatLong = hashMapLatLong[closestPOI]
                obj = {'lat': requestGeo.lat, 'long': requestGeo.long}
                dfLatLong.loc[len(dfLatLong)] = obj
                hashMapLatLong[closestPOI] = dfLatLong

    return hashMapLatLong

def getDataFrameForClassification(df):
    arrayPOI = loadPOI()
    df['POI'] = None
    for index, row in df.iterrows():
        requestGeo = Poin2d(row['Latitude'], row['Longitude'])
        closestPOI = getClosestPOI(requestGeo, arrayPOI)
        df.at[index,'POI'] = closestPOI

    return df
def label():
    df = cleanUp()


    hashMap = assignPOI2Request(df)
    return hashMap

def labelWithDataFrameForPlot():
    df = cleanUp()
    hashMapLatLong = getHashMapLatLongForPlot(df)
    return hashMapLatLong

def labelWithDataFrameForModel():
    df = cleanUp()

    return getDataFrameForClassification(df)


