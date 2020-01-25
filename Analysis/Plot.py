import matplotlib.pyplot as plt
import shapely

from Analysis.analysis import *
from Label.label import *
from Analysis.analysis import *
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import numpy as np
import plotly.express as px
#
# def convertArrayToDatafram(arr):
#     col_names = ['lat', 'long']
#     dfLatLong = pd.DataFrame(columns=col_names)
#     for point in arr:
#         obj = {'lat': point.lat, 'long': point.long}
#         dfLatLong.loc[len(dfLatLong)] = obj
#
#     return dfLatLong
#
# def getHashMapLatLongofPOI():
#     hashMap = label()
#     hashMapLatLong = {}
#     for poi in hashMap:
#         arrPoints = hashMap[poi]
#         dfLatLong = convertArrayToDatafram(arrPoints)
#         hashMapLatLong[poi] = dfLatLong
#
#     return hashMapLatLong
def getDFOfPOI(hashMapPOI):
    res = []


    for poi in hashMapPOI:
        col_names = ['lat', 'long']
        df = pd.DataFrame(columns=['lat','long'])

        obj = {'lat': hashMapPOI[poi].lat, 'long': hashMapPOI[poi].long}
        df = df.append(obj,ignore_index=True)
        res.append(df)
    return res

def plotWorldMap():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world.plot(figsize=(10, 6))

    return ax
def plotPoint(ax):
    hashMapLatLong = labelWithDataFrameForPlot()



    count = 0


    for poi in hashMapLatLong:

        df = hashMapLatLong[poi]

        geometry = [Point(xy) for xy in zip(df['long'], df['lat'])]
        gdf = GeoDataFrame(df, geometry=geometry)

        legend.append('points around ' + poi )

        r, g, b = np.random.uniform(0, 1, 3)

        gdf.plot(ax=ax, marker='o', color=(r, g, b, 1), markersize=15)
        count += 1

    # for poi in hashMapLatLong:
    #     arrayPoints = hashMapLatLong[poi]['arrayPoints']
    #     # legend.append('points around ' + poi)
    #     r, g, b = np.random.uniform(0, 1, 3)
    #     for point in arrayPoints:
    #         request = plt.Circle((point.long, point.lat),1.0,
    #                              color=(r,g,b,1), fill=True)
    #         ax.add_artist(request)







def plotAllPOI(ax):
    hashMapPOI = convertArrayPoiToHashMap()
    arrDfOfPOI = getDFOfPOI(hashMapPOI)

    for poi in hashMapPOI:

        r, g, b = np.random.uniform(0, 1, 3)
        df = pd.DataFrame(
    {
     'lat': [hashMapPOI[poi].lat],
     'long': [hashMapPOI[poi].long]}
        )

            # point = Point(row['long'],row['lat'])
        gdf = GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.long, df.lat))

        # gdf = GeoDataFrame(df, geometry=geometry)
        gdf.plot(ax=ax, marker='o', color=(r, g, b, 1), markersize=30)
        legend.append(poi)

    # for poi in hashMapPOI:
    #     # legend.append(poi)
    #     r, g, b = np.random.uniform(0, 1, 3)
    #     poiCirecle = plt.Circle((hashMapPOI[poi].long, hashMapPOI[poi].lat),2.0,
    #                          color=(r, g, b, 1), fill=True, label = 'asd')
    #     ax.add_artist(poiCirecle)
    #     ax.legend()


def plotCircle(ax):
    hashMapPOI = convertArrayPoiToHashMap()
    hashMapRadiusDensity = getRadiusDensity()
    for poi in hashMapRadiusDensity:
        circle2 = plt.Circle((hashMapPOI[poi].long, hashMapPOI[poi].lat), hashMapRadiusDensity[poi]['radius'], color='r', fill=False)
        ax.add_artist(circle2)


legend = []
ax = plotWorldMap()
plotPoint(ax)
plotAllPOI(ax)

plotCircle(ax)

plt.legend(legend)
plt.show()