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
    hashMap = {}

    for index, row in df.iterrows():
        requestGeo = Poin2d(row['Latitude'], row['Longitude'])
        closestPOI = getClosestPOI(requestGeo,arrayPOI)
        if closestPOI not in hashMap:
            hashMap[closestPOI] = [requestGeo]

        else:
            tempArrPoint = hashMap[closestPOI]
            tempArrPoint.append(requestGeo)
            hashMap[closestPOI] = tempArrPoint


    return hashMap

def getHashMapLatLong(df):
    arrayPOI = loadPOI()

    hashMapLatLong = {}
    for index, row in df.iterrows():
        requestGeo = Poin2d(row['Latitude'], row['Longitude'])
        closestPOI = getClosestPOI(requestGeo,arrayPOI)
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

def label():
    df = cleanUp()


    hashMap = assignPOI2Request(df)
    return hashMap

def labelWithDataFrame():
    df = cleanUp()
    hashMapLatLong = getHashMapLatLong(df)
    return hashMapLatLong