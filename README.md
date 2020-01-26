# EQWorksSample

### Libraries

- ##### `descartes`
- ##### `shapely`
- ##### `geopandas`
- ##### `matplotlib`
- ##### `pandas`
- ##### `numpy`
- ##### `scipy.stats`
- ##### `tensorflow`

### The average and standard deviation between POI and requests

```
{
    'POI3': {'averageDist': 5.537950830488869, 'standardDeviation': 2.858544126885263}, 
    'POI1': {'averageDist': 3.3481830063256055, 'standardDeviation': 3.8582906342102525}, 
    'POI4': {'averageDist': 8.810410862715694, 'standardDeviation': 28.64549188435129}
}
```

### Calculate the radius and density (requests/area) for each POI

```
{
    'POI3': {'radius': 19.73987039299441, 'density': 8.019371348116092}, 
    'POI1': {'radius': 19.8124370707908, 'density': 7.86423543738357}, 
    'POI4': {'radius': 10.821119877791817, 'density': 1.3156824222500376}
}
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
We use Gaussian Kernel Density Estimate (`gaussian_kde`) from `scipy.stats` as the mathematical model to visualize the popularity of each `POI`.  
Let's visuallize a heatmap of all requests:
![pic8](https://user-images.githubusercontent.com/15681805/73141484-7739e400-4052-11ea-84db-47a2ed1f771b.png)
Let's zoom to see them clearly:
![pic30](https://user-images.githubusercontent.com/15681805/73141461-38a42980-4052-11ea-9b4f-d71d851fe3b2.png)
![pic31](https://user-images.githubusercontent.com/15681805/73141462-38a42980-4052-11ea-8dda-1dfa2878e4b4.png)
![pic33](https://user-images.githubusercontent.com/15681805/73141463-38a42980-4052-11ea-8382-01c6e8aad256.png)

In the figures above, the lighter points are denser than darker ones.  Let's focus and make more analyses on those dense areas.
The figures below show some contour plots on those areas.  The values on the contour show the level of density, i.e. bigger number means denser.


![pic20](https://user-images.githubusercontent.com/15681805/73128370-8b230e80-3f9c-11ea-9eaf-3c3d0fc162b5.png)
![pic21](https://user-images.githubusercontent.com/15681805/73128371-8b230e80-3f9c-11ea-9274-2ca8e11590ab.png)
![pic22](https://user-images.githubusercontent.com/15681805/73128372-8bbba500-3f9c-11ea-8825-fded6230dd38.png)

To map the popularity of a `POI` to a scale that ranges from -10 to 10, we can perform the following steps:
1) For each POI, get the values of density on the contour plot around the average density area
2) Caculate the average density score
3) After getting an array of the average density score of all `POIs`, make the `normalization` of that array in the range from -10 to 10.  That `normalization` function is:
```
def normalizationInRange(from, to, array):
    firstNorm = [float(i) / max(array) for i in array]
    norm = [from + (to - from) * x for x in firstNorm]
```
#### Bonus
Please visit `DataScience Track/Bonus.pdf` to see my ideas for the bonus question.
### Data Engineer Track
Please visit `Data Engineering Track/pipeLine.py` to see the detailed implementation of the algorithm.  These are some descriptions:
1. Rather than making a correct topological ordering of the DAG, we build a graph data structure with a reverse topological order.  For example: `A -> C` is reversed to `C -> A`.  By this way, the `start` and `goal` tasks are become `goal` and `start` tasks, respectively.
2. Perform a backtracking algorithm to find all paths from the `start` node to `goal` node.  During this running, at each node, perform a `permutation` between all children nodes of that node and add to the current path, before performing a new recursive call.
3. A recursive call ends and returns the path if the `start` node is the `end` node.
4. To avoid duplicates, we only add new paths to the result list if those paths have not existed yet.
5. To get the correct topological order, we perform a `reverse()` function on the result list, this can be done in `O(n)`
6. To get the `necessity` and `sufficiency`, given the result from step 3, for each path, we truncate the unnecessary tasks by only getting tasks from the last task of the `start` task to the `goal` task.  Please visit function `getNecessityAndSufficiency(start, arrayTask)` to see more details of the implementation. 

## Complexity Analysis
I will demonstrate how my solutions are capable of handling beyond the sample scale.

### For Data Science Track
#### 1) Hashmap Data Structure
I use a hashmap to store our data, so a key is a `POI`, and the value is an array of objects, the farest Point from that `POI`, and the farest distance (the `radius`).  Each object is a `2DPoint` with two attributes: `lat` and `long`.  Since the given dataset is time-series, so the objects inside of the array are stored in the chronological order.
This is an example of the hashmap:
```
{
    'POI3': {'arrayPoints': [2DPoint, 2DPoint, ...], 'farestPoint': 2DPoint, 'farestDist': 18.91}
    'POI1': {'arrayPoints': [2DPoint, 2DPoint, ...], 'farestPoint': 2DPoint, 'farestDist': 10.56}
    'POI4': {'arrayPoints': [2DPoint, 2DPoint, ...], 'farestPoint': 2DPoint, 'farestDist': 3.47}
}
```
This data structure can be easily adapted to other kinds of time-series datasets.
#### 2) Algorithms
With the hashmap data structure above, depending on a specific algorithm, the complexity can be `O(k*n)` (`k` is the number of `POI` and `n` is the number of reuqests around that POI); `O(n)` or even `O(1)`

**Example**: since the given dataset is time-series, a regular query can be to get the last request of `POI1`.  Searching for `POI1` in the hashMap is `O(1)`, and finding the last element in an array is `O(1)`, so the total complexity is `O(1)`.

**Experiments**: after removing all suspicious records in step 1 `Cleanup` (I still kept the 1st record), the total records are 19,999.  The total time to get average distance and standard deviation in question 3.1 is `3 seconds 17 miliseconds`.

### For Data Engineer Track
#### 1) DAG Data Structure
I use a hashmap for the DAG data structure.  The key is the parent node, and the value is an array of childrent nodes.  For example: if we have `A->C, B->C, C->K, C->E, K->F, E->F`, a graph can be illustrated by:
```
graph = {
    'A': ['C'],
    'B': ['C'],
    'C': ['K','E'],
    'K': ['F'],
    'E': ['F']
}
```
**Advantage**: when we iterate the graph, at a spefic node, it takes `O(1)` to get the list of its children.
#### 2) Algorithm
Please visit function `find_all_paths` in `Engineering Track/pipeLine.py` to see more details of the backtracking algorithm.  The complexity of this algorithm is `O(k*n)`, where `n` is the number of nodes in the graph and `k` is the number of permutations between children of a specific node. 

#### 3) Result
Please vist `Engineering Track/result.txt` to find the result of engineering track.  I have added `starting task: 73,112,97` and `goal task: 36` to test the necessity and sufficiency of the algorithm.
