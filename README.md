# idkmyfriends-prototype
IDK My Friends: Link analysis on social networks to mine surprise connections

## Dependencies:
* networkx
* matplotlib

## Usage:
* Create a file input.csv in the same directory of the program.
* Each line of input is of form a,b where a and b are nodes represented as numbers and if a and b are connected.
* Run IDKmyFriends.py. The output will be generated as png files representing the state of network, each time when a new community is formed.

## Sample Output:
![Graph Visualization of Community Detection for a Sample User](/graph_combined.PNG)

## Authors
* Praveen Mylavarapu, saipraveenmylavarapu@gmail.com
* Shubhashri AG, agshubhashri@gmail.com

## References
1. M.E.J. Newman (2014), Fast algorithm for detecting community structure in networks, Physical Review E 69, 48109-1120, USA.
2. Xingqin Qi, Huimin Song, Jianliang Wu, Edgar Fuller, Rong Luo, Cun-Quan Zhang (2017), Eb&D: A new clustering approach for signed social networks based on both edge-betweenness centrality and density of subgraphs, Elsevier Physics A.
