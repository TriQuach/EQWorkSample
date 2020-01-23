from LoadData.loadData import *

def cleanUp():
    df = loadData()
    df = df.drop_duplicates(subset=['TimeSt','Latitude','Longitude'], keep='first')
    return df
