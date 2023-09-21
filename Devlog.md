# Wed Sep 20 20:36:42 PDT 2023

Here's an update. I'm calling Rover1 complete. Like Rover0 Rover1 uses a kind of A* or Dijkstra's path finding algorithm.

Here's the method.

The rover initially assumes that there are no blockades on the map. Under this assumption the rover plots the optimal route to the destination. Once plotted the rover takes a step on that route and repeats. If the rover is ever unable to take the step due to a blockade, the rover updates its assumptions on the existing blockades and tries again.

![](pics/rover1-sm.gif)

I initially thought this is good enough but then I realized there are points where the steps could be optimized. This is much more clearly visible when the grid size is increased so that the rover needs to plot much longer routes.

![](pics/slow_huristic_far_away-sm.gif)

What we see is that the rover acts slowly when its charting a route from far away from the destination, and it acts faster when its charting a route from near the destination.

I know this can be optimized because I implemented the route charting using Dijkstra's algorithm. If I implement it using A* then the route charting will be faster. The funny thing is that this will technically be a heuristic on top of a heuristic. The first heuristic is Dijkstra's charting a route with reduced knowledge of the blockades. The second heuristic is the Manhattan distance from a point to the destination.

Also I should add in a visualization for the paths explored while searching for the heuristic path.

---
> endlog - Wed Sep 20 21:08:35 PDT 2023

## Tue Sep 19 17:03:17 PDT 2023

This looks fun. I cant belive I went so long without knowing about pygame!

---
> endlog - Tue Sep 19 17:05:11 PDT 2023
