import numpy as np
import matplotlib.pyplot as plt
from Label.label import *
from scipy.stats import gaussian_kde
import geopandas as gpd
import scipy.stats as st
def plotWorldMap():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world.plot(figsize=(10, 6))
    return ax
def plotHeatMap(ax):
    df = labelWithDataFrameForPlot()

    for poi in df:
        lat = df[poi]['lat'].values
        long = df[poi]['long'].values
        lat_long = np.vstack([long,lat])
        z = gaussian_kde(lat_long)(lat_long)

        idx = z.argsort()
        x, y, z = long[idx], lat[idx], z[idx]

        ax.scatter(x, y, c=z, s=30, edgecolor='')

    plt.show()
    print('asd')

def performKDEandPlot(x,y,ax):
    xmin, xmax = min(x) - 1, max(x) + 1
    ymin, ymax = min(y) - 1, max(y) + 1

    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    # fig = plt.figure()

    # ax.set_xlim(xmin, xmax)
    # ax.set_ylim(ymin, ymax)
    # Contourf plot
    cfset = ax.contourf(xx, yy, f, cmap='Blues')
    # Or kernel density estimate plot instead of the contourf plot
    # ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
    # Contour plot
    cset = ax.contour(xx, yy, f, colors='k')
    # Label plot
    ax.clabel(cset, inline=1, fontsize=10)


def plotDensityWithContour(ax):
    df = labelWithDataFrameForPlot()

    for poi in df:
        lat = df[poi]['lat'].values
        long = df[poi]['long'].values
        performKDEandPlot(long,lat,ax)


ax = plotWorldMap()
# plotHeatMap(ax)
plotDensityWithContour(ax)
plt.show()


