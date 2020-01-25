# EQWorksSample

### Libraries

- ##### `descartes`
- ##### `shapely`
- ##### `geopandas`
- ##### `matplotlib`
- ##### `pandas`
- ##### `numpy`

### The average and standard deviation between POI and requests

```
{'POI3': {'averageDist': 5.537950830488869, 'standardDeviation': 2.858544126885263}, 'POI1': {'averageDist': 3.3481830063256055, 'standardDeviation': 3.8582906342102525}, 'POI4': {'averageDist': 8.810410862715694, 'standardDeviation': 28.64549188435129}}
```

### Calculate the radius and density (requests/area) for each POI

```
{'POI3': {'radius': 19.73987039299441, 'density': 8.019371348116092}, 'POI1': {'radius': 19.8124370707908, 'density': 7.86423543738357}, 'POI4': {'radius': 10.821119877791817, 'density': 1.3156824222500376}}
```

### Circles include all of assigned requests

![pic5](https://user-images.githubusercontent.com/15681805/73040642-555d1900-3e28-11ea-9c56-78cb3deb0dee.png)
We can observe that there are some outliers appeared in the right of the map (somewhere in Europe and Asia), leading to the big radius and circle of POI4.


Anyway let's zoom to see it clearly.
![pic6](https://user-images.githubusercontent.com/15681805/73040662-6efe6080-3e28-11ea-8949-7f7d03518311.png)

So we can eliminate those outliers and plot them again in the world map:
![pic7](https://user-images.githubusercontent.com/15681805/73127086-388c2700-3f89-11ea-8149-afd4e56dcc11.png)
We can observe that after removing outliers, POI3 lies nearly in the circle border of POI 4.  So a hypothesis is that we can merge POI3 and POI4 to a single POI. 

### Data Science Track
We use Gaussian Kernel Density Estimate (`gaussian_kde`) from `scipy.stats` as the mathematical model to vissualize the popularity of each `POI`.  
Let's visuallize a heatmap of all requests:
![pic8](https://user-images.githubusercontent.com/15681805/73127898-55c6f280-3f95-11ea-8461-ea0936b7f761.png)
![pic9](https://user-images.githubusercontent.com/15681805/73127934-c2da8800-3f95-11ea-9d52-d35ca4c9433c.png)
![pic10](https://user-images.githubusercontent.com/15681805/73127935-c53ce200-3f95-11ea-92c4-f7f84fa21dd9.png)





