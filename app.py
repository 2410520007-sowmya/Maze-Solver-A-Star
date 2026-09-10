import streamlit as st
import heapq
import matplotlib.pyplot as plt

st.title("Maze Solver using A* Search")
st.write("A* Search Algorithm with Manhattan Distance Heuristic")

maze = [
    ['S', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
    ['#', '#', '.', '#', '.', '#', '#', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '#', '#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'G']
]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    open_list = []
    heapq.heappush(open_list, (0, start))

    g_cost = {start: 0}
    parent = {start: None}

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == '#':
                    continue

                neighbor = (nr, nc)
                new_cost = g_cost[current] + 1

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    f_cost = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))
                    parent[neighbor] = current

    return None

start = (0, 0)
goal = (4, 9)

path = a_star(maze, start, goal)

if path:
    st.success(f"Path found! Path length: {len(path)}")

    fig, ax = plt.subplots()

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == '#':
                ax.add_patch(plt.Rectangle((c, r), 1, 1))

    path_rows = [p[0] for p in path]
    path_cols = [p[1] for p in path]

    ax.plot(
        [c + 0.5 for c in path_cols],
        [r + 0.5 for r in path_rows],
        marker='o'
    )

    ax.text(0.5, 0.5, 'S', ha='center', va='center', fontsize=14)
    ax.text(9.5, 4.5, 'G', ha='center', va='center', fontsize=14)

    ax.set_xlim(0, 10)
    ax.set_ylim(5, 0)
    ax.set_xticks(range(11))
    ax.set_yticks(range(6))
    ax.grid(True)

    st.pyplot(fig)
else:
    st.error("No path found!")
