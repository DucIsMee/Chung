import sys
import time
import numpy as np 
from queue import Queue
import pygame
import heapq

WIDTH, HEIGHT = 300, 350
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

def dfs(start, goal):
    stack = [(start, [start])]   
    visited = {tuple(np.array(start).reshape(-1))}

    while stack:
        state, path = stack.pop()

        if state == goal:
            return path

        x, y = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]

        moves = [(-1,0),(1,0),(0,-1),(0,1)]

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                flat = tuple(np.array(new_state).reshape(-1))

                if flat not in visited:
                    visited.add(flat)
                    stack.append((new_state, path + [new_state]))

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

#==================================Vẽ giao diện==================================

def draw_state(screen,font,state):
    screen.fill((255,255,255))
    for i in range(3):
        for j in range(3):
            val=state[i][j]
            if val!=0:
                pygame.draw.rect(screen,(0,128,255),(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))
                text=font.render(str(val),True,(255,255,255))
                screen.blit(text,(j*TILE_SIZE+TILE_SIZE//3,i*TILE_SIZE+TILE_SIZE//4))
    pygame.display.flip()

def draw_buttons(screen, font):
    button_width = WIDTH // 4

    pygame.draw.rect(screen,(0,200,0),(0,300,button_width,BUTTON_HEIGHT))                 
    pygame.draw.rect(screen,(200,100,0),(button_width,300,button_width,BUTTON_HEIGHT))   
    pygame.draw.rect(screen,(200,0,0),(2*button_width,300,button_width,BUTTON_HEIGHT))   
    pygame.draw.rect(screen,(0,0,200),(3*button_width,300,button_width,BUTTON_HEIGHT))    

    bfs_text = font.render("BFS",True,(255,255,255))
    dfs_text = font.render("DFS",True,(255,255,255))
    astar_text = font.render("A*",True,(255,255,255))
    reset_text = font.render("Reset",True,(255,255,255))

    screen.blit(bfs_text,(button_width//2-20,310))
    screen.blit(dfs_text,(button_width + button_width//2-20,310))
    screen.blit(astar_text,(2*button_width + button_width//2-20,310))
    screen.blit(reset_text,(3*button_width + button_width//2-30,310))

    pygame.display.flip()

def run_solution(screen,font,solution):
    for state in solution:
        draw_state(screen,font,state)
        draw_buttons(screen,font)
        pygame.display.flip()
        time.sleep(1)
    print(f"Số bước: {len(solution)-1}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8 Puzzle Solver")
    font = pygame.font.SysFont(None, FONT_SIZE)

    start_state = [[7,2,4],[5,0,6],[8,3,1]]
    current_state = start_state
    solution = []
    running = True

    # Vẽ giao diện ban đầu
    draw_state(screen, font, current_state)
    draw_buttons(screen, font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= y <= 350:
                    if x < WIDTH//3: 
                        solution = bfs(start_state, GOAL_STATE)
                        run_solution(screen, font, solution)
                    elif x < 2*WIDTH//3: 
                        solution = astar(start_state)
                        run_solution(screen, font, solution)
                    elif x < 2*WIDTH//3:
                        solution = dfs(start_state, GOAL_STATE)
                        run_solution(screen, font, solution)
                    else:  # Reset
                        current_state = start_state
                        solution = []
                        draw_state(screen, font, current_state)
                        draw_buttons(screen, font)
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()
