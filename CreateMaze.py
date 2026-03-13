import random

def create_maze(rows, cols):
    maze = [[1 for _ in range(cols + 2)] for _ in range(rows + 2)]
    stack = [(1, 1)]

    maze[1][1] = 0
    while stack:
        x, y = stack[-1]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        carved = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < rows + 1 and 1 <= ny < cols + 1 and maze[nx][ny] == 1:
                maze[x + dx // 2][y + dy // 2] = 0
                maze[nx][ny] = 0
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()
        maze[1][1] = 'S'
        maze[rows][cols] = 'G'
    return maze

maze = create_maze(15, 20)

for row in maze:
    print("".join(
        "█" if cell == 1 else
        "S" if cell == 'S' else
        "G" if cell == 'G' else
        " " for cell in row))