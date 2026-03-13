from collections import deque
import heapq
import random
import sys
import pygame
# ==================== BFS SEARCH ====================

def bfs(graph, start, goal):
    visited = set()
    queue = deque()
    queue.append((start, [start]))
    visited.add(start)
    visited_order = []

    while queue:
        current, path = queue.popleft()
        visited_order.append(current)

        if current == goal:
            return path, visited_order

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, visited_order

# ==================== DFS SEARCH ====================

def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]
    visited_order = []
    while stack:
        state, path = stack.pop()
        visited_order.append(state)

        if state == goal:
            return path, visited_order

        if state not in visited:
            visited.add(state)

        for neighbor in graph[state]:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None, visited_order

# ==================== A* SEARCH ====================

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, goal):

    heap = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    visited_order = []

    while heap:
        f, g, current, path = heapq.heappop(heap)
        visited_order.append(current)

        if current == goal:
            return path, visited_order

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))

    return None, visited_order

def create_maze(rows, cols):
    maze = [[1 for _ in range(cols+2)] for _ in range(rows+2)]
    stack = [(1,1)]
    maze[1][1] = 0
    while stack:
        x,y = stack[-1]
        directions = [(0,2),(2,0),(0,-2),(-2,0)]
        random.shuffle(directions)
        carved = False
        for dx,dy in directions:
            nx,ny = x+dx,y+dy
            if 1 <= nx < rows+1 and 1 <= ny < cols+1 and maze[nx][ny]==1:
                maze[x+dx//2][y+dy//2] = 0
                maze[nx][ny] = 0
                stack.append((nx,ny))
                carved = True
                break
        if not carved:
            stack.pop()
    maze[1][1] = 'S'
    maze[rows][cols] = 'G'
    return maze

def maze_to_graph(maze):
    rows, cols = len(maze), len(maze[0])
    graph = {}
    start = goal = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] in (0,'S','G'):
                if maze[i][j]=='S': start=(i,j)
                if maze[i][j]=='G': goal=(i,j)
                neighbors=[]
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    ni,nj=i+dx,j+dy
                    if 0<=ni<rows and 0<=nj<cols and maze[ni][nj] in (0,'S','G'):
                        neighbors.append((ni,nj))
                graph[(i,j)] = neighbors
    return graph,start,goal

def draw_maze(screen, visited, maze, path=None, cell_size=20):
    for i,row in enumerate(maze):
        for j,val in enumerate(row):
            rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
            if val==1:
                pygame.draw.rect(screen,(0,0,0),rect)
            elif val=='S':
                pygame.draw.rect(screen,(0,0,255),rect)
            elif val=='G':
                pygame.draw.rect(screen,(255,0,0),rect)
            else:
                pygame.draw.rect(screen,(255,255,255),rect)
                pygame.draw.rect(screen,(200,200,200),rect,1)

    if visited:
        for (i,j) in visited:
            if maze[i][j] not in ('S','G'):
                rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen,(255,255,0),rect)

    if path:
        for (i,j) in path:
            if maze[i][j] not in ('S','G'):
                rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen,(0,255,0),rect)

def main():
    pygame.init()
    WIDTH, HEIGHT = 900, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")

    rows, cols = 51, 61
    cell_size = min((HEIGHT-100)//(rows+2), WIDTH//(cols+2))
    font = pygame.font.SysFont("Arial", 28)

    maze = create_maze(rows, cols)
    graph, start, goal = maze_to_graph(maze)
    path = None
    visited_order = []
    visited_display = []
    step_index = 0
    clock = pygame.time.Clock()

    button_y = HEIGHT - 80
    buttons = {
        "create": (50, button_y),
        "bfs": (300, button_y),
        "dfs": (500, button_y),
        "astar": (750, button_y)
    }

    running = True
    while running:
        screen.fill((50,50,50))
        if visited_order and step_index < len(visited_order):
            
            visited_display.append(visited_order[step_index])
            step_index += 1
            draw_maze(screen, visited_display, maze, None, cell_size)
        elif visited_order and step_index >= len(visited_order):
            draw_maze(screen, visited_display, maze, path, cell_size)
        else:
            draw_maze(screen, visited_display, maze, None, cell_size)

        create_btn = font.render("Create Maze", True, (255,255,255))
        bfs_btn = font.render("Solve BFS", True, (255,255,255))
        dfs_btn = font.render("Solve DFS", True, (255,255,255))
        astar_btn = font.render("Solve A*", True, (255,255,255))

        screen.blit(create_btn, buttons["create"])
        screen.blit(bfs_btn, buttons["bfs"])
        screen.blit(dfs_btn, buttons["dfs"])
        screen.blit(astar_btn, buttons["astar"])

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if create_btn.get_rect(topleft=buttons["create"]).collidepoint(pos):
                    maze = create_maze(rows, cols)
                    graph, start, goal = maze_to_graph(maze)
                    path = None
                    visited_order = []
                    visited_display = []
                    step_index = 0
                elif bfs_btn.get_rect(topleft=buttons["bfs"]).collidepoint(pos):
                    path, visited_order = bfs(graph, start, goal)
                    visited_display = []
                    step_index = 0
                elif dfs_btn.get_rect(topleft=buttons["dfs"]).collidepoint(pos):
                    path, visited_order = dfs(graph, start, goal)
                    visited_display = []
                    step_index = 0
                elif astar_btn.get_rect(topleft=buttons["astar"]).collidepoint(pos):
                    path, visited_order = astar(graph, start, goal)
                    visited_display = []
                    step_index = 0
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
