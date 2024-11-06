# maze
This project is based on python to create some maze and try some simple algorithm to solve it. There are also several MDP iteration and reinforce algorithm. this project is simple and just for learning(it my homework of a course). you are welcome to make a contribution to improve it.

the num_row and num_col better no bigger than 30, otherwise it could be very long to generate a map

under this environment, it always can't have a result because if the minmax depth is too large, the dfs will take a lot time. but if the depth is too small, the agent always find a wrong way so can't reach the end.  mamybe a better Heuristic function can figure out this problem, unfortunately I haven't find it.