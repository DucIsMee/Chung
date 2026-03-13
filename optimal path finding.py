from collections import deque
import heapq
import random
import pygame
# ==================== BFS SEARCH ====================

def bfs(graph, start, goal):
    visited = set()
    queue = deque()
    queue.append((start, [start]))  # (node hiện tại, đường đi)
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # Không tìm thấy

# ==================== DFS SEARCH ====================

def dfs(graph, start, goal, max_depth = 50):
    visited = set()
    stack = [(start, [start], 0)]  # (node hiện tại, đường đi, độ sâu)

    while stack:
        state, path, depth = stack.pop()

        if state == goal:
            return path

        if depth < max_depth:
            if state not in visited:
                visited.add(state)

                for neighbor in graph[state]:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], depth + 1))

    return None

# ==================== A* SEARCH ====================

def heuristic(a, b):
    # khoảng cách Manhattan giữa hai node (giả sử node là tuple (x,y))
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, goal):
    # heap lưu (f, g, node, path)
    heap = [(heuristic(start, goal), 0, start, [start])]
    visited = set()

    while heap:
        f, g, current, path = heapq.heappop(heap)

        if current == goal:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))

    return None



def generate_maze(rows, cols, wall_prob=0.3):
    maze = [[0 if random.random() > wall_prob else 1 for _ in range(cols)] for _ in range(rows)]
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0
    return maze

def maze_to_graph(maze):
    rows, cols = len(maze), len(maze[0])
    graph = {}
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0:
                neighbors = []
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    ni, nj = i+dx, j+dy
                    if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] == 0:
                        neighbors.append((ni,nj))
                graph[(i,j)] = neighbors
    return graph
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
ROWS, COLS = 20, 30
CELL_SIZE = min(WIDTH//COLS, HEIGHT//ROWS)

font = pygame.font.SysFont("Arial", 30)

maze = generate_maze(ROWS, COLS)
graph = maze_to_graph(maze)
start, goal = (0,0), (ROWS-1,COLS-1)
path = None

def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255,255,255) if maze[i][j]==0 else (0,0,0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200,200,200), rect, 1)
    if path:
        for (i,j) in path:
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0,255,0), rect)

def draw_buttons():
    create_btn = font.render("Tạo mê cung", True, (255,255,255))
    bfs_btn = font.render("Giải BFS", True, (255,255,255))
    dfs_btn = font.render("Giải DFS", True, (255,255,255))
    astar_btn = font.render("Giải A*", True, (255,255,255))
    screen.blit(create_btn, (50, HEIGHT-150))
    screen.blit(bfs_btn, (300, HEIGHT-150))
    screen.blit(dfs_btn, (500, HEIGHT-150))
    screen.blit(astar_btn, (700, HEIGHT-150))

def button_clicked(pos, text_surface, x, y):
    rect = text_surface.get_rect(topleft=(x,y))
    return rect.collidepoint(pos)

running = True
while running:
    screen.fill((50,50,50))
    draw_maze()
    draw_buttons()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            create_btn = font.render("Tạo mê cung", True, (255,255,255))
            bfs_btn = font.render("Giải BFS", True, (255,255,255))
            dfs_btn = font.render("Giải DFS", True, (255,255,255))
            astar_btn = font.render("Giải A*", True, (255,255,255))

            if button_clicked(pos, create_btn, 50, HEIGHT-150):
                maze = generate_maze(ROWS, COLS)
                graph = maze_to_graph(maze)
                path = None
            elif button_clicked(pos, bfs_btn, 300, HEIGHT-150):
                path = bfs(graph, start, goal)
            elif button_clicked(pos, dfs_btn, 500, HEIGHT-150):
                path = dfs(graph, start, goal)
            elif button_clicked(pos, astar_btn, 700, HEIGHT-150):
                path = astar(graph, start, goal)

pygame.quit()
sys.exit()
