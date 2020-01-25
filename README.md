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
We can observe that there are some outliers appeared in the right of the map (somewhere in Europe and Asia), leading to the big radius and circle of `POI4`.


Anyway let's zoom to see it clearly.
![pic6](https://user-images.githubusercontent.com/15681805/73040662-6efe6080-3e28-11ea-8949-7f7d03518311.png)

So we can eliminate those outliers and plot them again in the world map:
![pic7](https://user-images.githubusercontent.com/15681805/73127086-388c2700-3f89-11ea-8149-afd4e56dcc11.png)
We can observe that after removing outliers, `POI3` lies nearly in the circle border of `POI4`.  So a hypothesis is that we can merge `POI3` and `POI4` to a single `POI`. 

### Data Science Track
We use Gaussian Kernel Density Estimate (`gaussian_kde`) from `scipy.stats` as the mathematical model to vissualize the popularity of each `POI`.  
Let's visuallize a heatmap of all requests:
![pic8](https://user-images.githubusercontent.com/15681805/73127898-55c6f280-3f95-11ea-8461-ea0936b7f761.png)
![pic9](https://user-images.githubusercontent.com/15681805/73127934-c2da8800-3f95-11ea-9d52-d35ca4c9433c.png)
![pic10](https://user-images.githubusercontent.com/15681805/73127935-c53ce200-3f95-11ea-92c4-f7f84fa21dd9.png)

In the figures above, the lighter points are denser than darker ones.  Let's focus and make more analyses on those dense areas.
The figures below show some contour plots on those areas.  The values on the contour show the level of density, i.e. bigger number means denser.

![pic20](https://user-images.githubusercontent.com/15681805/73128370-8b230e80-3f9c-11ea-9eaf-3c3d0fc162b5.png)
![pic21](https://user-images.githubusercontent.com/15681805/73128371-8b230e80-3f9c-11ea-9274-2ca8e11590ab.png)
![pic22](https://user-images.githubusercontent.com/15681805/73128372-8bbba500-3f9c-11ea-8825-fded6230dd38.png)

To map the popularity of a `POI` to a scale that ranges from -10 to 10, we can perform the following steps:
1) For each POI, get the values of density on the contour plot around the average density area
2) Caculate the average density score
3) After getting an array of the average density score of all `POIs`, make the `normalization` of that array in the range from -10 to 10.  That `normalization` function can be like this
```
def normalizationInRange(from, to, array):
    firstNorm = [float(i) / max(array) for i in array]
    norm = [from + (to - from) * x for x in firstNorm]
```
### Data Engineer Track
Please visit `Data Engineering Track/pipeLine.py` to see the detailed implementation of the algorithm.  These are some descriptions:
1. Rather than making a correct topological ordering of the DAG, we build a graph data structure with a reverse topological order.  For example: `A -> C` is reversed to `C -> A`.  By this way, the `start` and `goal` tasks are become `goal` and `start` tasks, respectively.
2. Perform a backtracking algorithm to find all paths from the `start` node to `goal` node.  During this running, at each node, perform a `permutation` between all children nodes of that node and add to the current path, before performing a new recursive call.
3. A recursive call ends and returns the path if the `start` node is the `end` node.
4. To avoid duplicates, we only add new paths to the result list if those paths have not existed yet.
5. To get the correct topological order, we perform a `reverse()` function on the result list, this can be done in `O(n)`
6. To get the `necessity` and `sufficiency`, given the result from step 3, for each path, we truncate the unnecessary tasks by only getting tasks from the last task of the `start` task to the `goal` task.  Please visit function `getNecessityAndSufficiency(start, arrayTask)` to see more details of the implementation. 


