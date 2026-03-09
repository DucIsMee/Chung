import sys
import time
import numpy as np 
from queue import Queue
import pygame
import heapq

WIDTH, HEIGHT = 550, 600
TILE_SIZE = WIDTH // 3
FONT_SIZE = 40
BUTTON_HEIGHT = 50 
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def bfs(start, goal):
    queue = Queue()
    queue.put((start, [start]))
    visited = {tuple(np.array(start).reshape(-1))}
    while not queue.empty():
        state, path = queue.get()
        if state == goal:
            return path
        x, y = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                flat = tuple(np.array(new_state).reshape(-1))
                if flat not in visited:
                    visited.add(flat)
                    queue.put((new_state, path + [new_state]))
    return None

def dfs(start, goal, max_depth=50):
    stack = [(start, [start], 0)]   
    visited = set()

    while stack:
        state, path, depth = stack.pop()

        if state == goal:
            return path

        if depth >= max_depth:
            continue

        flat = tuple(np.array(state).reshape(-1))
        if flat in visited:
            continue
        visited.add(flat)

        x, y = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]

        moves = [(-1,0),(1,0),(0,-1),(0,1)]

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                stack.append((new_state, path + [new_state], depth + 1))

    return None

def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_x, goal_y = (val - 1) // 3, (val - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def neighbors(state):
    x, y = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
    result = []
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            result.append(new_state)
    return result

def astar(start):
    heap = [(manhattan(start), 0, start, [])]
    visited = set()
    while heap:
        est, cost, state, path = heapq.heappop(heap)
        if state == GOAL_STATE:
            return path + [state]
        visited.add(str(state))
        for neighbor in neighbors(state):
            if str(neighbor) not in visited:
                heapq.heappush(heap, (cost + 1 + manhattan(neighbor), cost + 1, neighbor, path + [state]))
    return []

def Greedy(start, goal):
    heap = [(manhattan(start), start, [])]
    visited = set()
    while heap:
        h, state, path = heapq.heappop(heap)
        if state == goal:
            return path + [state]
        visited.add(str(state))
        for neighbor in neighbors(state):
            if str(neighbor) not in visited:
                heapq.heappush(heap, (manhattan(neighbor), neighbor, path + [state]))
    return [] 

#==================================Vẽ giao diện==================================

def draw_state(screen, font, state):
    screen.fill((240,240,240))
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen,(200,200,200),rect,0)
            pygame.draw.rect(screen,(100,100,100),rect,2)
            if val != 0:
                pygame.draw.rect(screen,(0,128,255),rect.inflate(-10,-10))
                text = font.render(str(val),True,(255,255,255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text,text_rect)
    pygame.display.flip()

def draw_buttons(screen, font):
    button_width = WIDTH // 4
    labels = ["BFS","DFS","A*","Greedy"]
    colors = [(0,200,0),(200,100,0),(200,0,0),(0,0,200)]
    for i,label in enumerate(labels):
        rect = pygame.Rect(i*button_width,550,button_width,BUTTON_HEIGHT)
        pygame.draw.rect(screen,colors[i],rect,border_radius=8)
        text = font.render(label,True,(255,255,255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text,text_rect)
    pygame.display.flip()

def run_solution(screen, font, solution):
    for state in solution:
        draw_state(screen,font,state)
        draw_buttons(screen,font)
        pygame.display.flip()
        time.sleep(0.8)
    print(f"Số bước: {len(solution)-1}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8 Puzzle Solver")
    font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)

    start_state = [[7,2,4],[5,0,6],[8,3,1]]
    current_state = start_state
    solution = []
    running = True

    draw_state(screen,font,current_state)
    draw_buttons(screen,font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if 550 <= y <= 600:
                    button_width = WIDTH // 4
                    if x < button_width:          # BFS
                        solution = bfs(start_state, GOAL_STATE)
                        run_solution(screen,font,solution)
                    elif x < 2*button_width:      # DFS
                        solution = dfs(start_state, GOAL_STATE)
                        run_solution(screen,font,solution)
                    elif x < 3*button_width:      # A*
                        solution = astar(start_state)
                        run_solution(screen,font,solution)
                    else:     # Greedy
                        solution = Greedy(start_state, GOAL_STATE)
                        run_solution(screen,font,solution)

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()
