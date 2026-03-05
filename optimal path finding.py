from collections import deque

# ==================== OPTIMAL PATH FINDING: BFS ====================

def bfs(graph, start, goal):
    """
    BFS tìm đường đi ngắn nhất (ít cạnh nhất) từ start đến goal
    graph: dict {node: [neighbors]}
    """
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


# ==================== ĐỒ THỊ MẪU ====================

#       A --- B --- E
#       |    / \    |
#       |   /   \   |
#       C--D     F--G
#            \  /
#             H

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D', 'E', 'F'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C', 'H'],
    'E': ['B', 'G'],
    'F': ['B', 'G', 'H'],
    'G': ['E', 'F'],
    'H': ['D', 'F'],
}

# ==================== CHẠY CHƯƠNG TRÌNH ====================

if __name__ == "__main__":
    print("=" * 50)
    print("  OPTIMAL PATH FINDING: BFS")
    print("=" * 50)
    print()

    # In đồ thị
    print("Đồ thị:")
    for node in sorted(graph):
        print(f"  {node} → {graph[node]}")
    print()

    # Tìm đường đi ngắn nhất
    start = 'A'
    goal = 'H'

    print(f"Tìm đường ngắn nhất từ {start} → {goal}:")
    path = bfs(graph, start, goal)

    if path:
        print(f"  Đường đi: {' → '.join(path)}")
        print(f"  Số bước:  {len(path) - 1}")
    else:
        print("  Không tìm thấy đường đi!")

    # Thử thêm các cặp đỉnh khác
    print()
    pairs = [('A', 'G'), ('C', 'H'), ('D', 'G'), ('A', 'F')]
    for s, g in pairs:
        path = bfs(graph, s, g)
        if path:
            print(f"  {s} → {g}: {' → '.join(path)} ({len(path)-1} bước)")
        else:
            print(f"  {s} → {g}: Không tìm thấy")
