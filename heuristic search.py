import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
import copy

# ==================== CONSTRAINT SATISFACTION PROBLEM (CSP) ====================


class CSP:
    """Lớp tổng quát cho bài toán Constraint Satisfaction"""

    def __init__(self, variables, domains, neighbors_dict):
        """
        variables:      danh sách biến
        domains:        dict {biến: [giá trị có thể]}
        neighbors_dict: dict {biến: set(các biến ràng buộc)}
        Ràng buộc mặc định: các biến hàng xóm phải khác giá trị (all-different)
        """
        self.variables = variables
        self.domains = {v: list(d) for v, d in domains.items()}
        self.neighbors = neighbors_dict

    def is_consistent(self, var, value, assignment):
        """Kiểm tra giá trị có thỏa mãn ràng buộc (khác giá trị với hàng xóm)"""
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    # ==================== AC-3 Algorithm ====================
    def ac3(self):
        """Thuật toán AC-3 để giảm miền giá trị"""
        queue = deque()
        for var in self.variables:
            for neighbor in self.neighbors[var]:
                queue.append((var, neighbor))

        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        """Loại bỏ giá trị không thỏa mãn arc consistency"""
        revised = False
        for val in self.domains[xi][:]:
            # Phải tồn tại ít nhất 1 giá trị trong domain xj khác val
            if not any(val != val_j for val_j in self.domains[xj]):
                self.domains[xi].remove(val)
                revised = True
        return revised

    # ==================== Backtracking Search ====================
    def backtracking_search(self):
        """Tìm kiếm quay lui với MRV + Forward Checking"""
        print("Chạy AC-3 để giảm miền giá trị...")
        if not self.ac3():
            print("AC-3 phát hiện không có lời giải!")
            return None

        # Đếm ô đã giảm còn 1 giá trị
        fixed = sum(1 for v in self.variables if len(self.domains[v]) == 1)
        print(f"AC-3 xác định được {fixed}/{len(self.variables)} ô")
        print()

        # Gán các ô đã xác định
        assignment = {}
        for v in self.variables:
            if len(self.domains[v]) == 1:
                assignment[v] = self.domains[v][0]

        return self._backtrack(assignment)

    def _backtrack(self, assignment):
        """Thuật toán backtracking đệ quy"""
        if len(assignment) == len(self.variables):
            return assignment

        var = self._select_unassigned_var(assignment)

        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value

                # Forward checking: lưu và cắt miền
                saved_domains = {}
                feasible = True
                for neighbor in self.neighbors[var]:
                    if neighbor not in assignment and value in self.domains[neighbor]:
                        saved_domains[neighbor] = list(self.domains[neighbor])
                        self.domains[neighbor].remove(value)
                        if len(self.domains[neighbor]) == 0:
                            feasible = False
                            break

                if feasible:
                    result = self._backtrack(assignment)
                    if result is not None:
                        return result

                # Khôi phục miền
                del assignment[var]
                for nb, dom in saved_domains.items():
                    self.domains[nb] = dom

        return None

    def _select_unassigned_var(self, assignment):
        """MRV: chọn biến có ít giá trị hợp lệ nhất"""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(self.domains[v]))


# ==================== BÀI TOÁN SUDOKU ====================

def create_sudoku_csp(puzzle):
    """
    Tạo CSP cho bài toán Sudoku 9x9
    puzzle: mảng numpy 9x9, ô trống = 0
    """
    variables = []
    domains = {}
    neighbors = {}

    # Tạo biến cho mỗi ô (row, col)
    for r in range(9):
        for c in range(9):
            var = (r, c)
            variables.append(var)

            if puzzle[r][c] != 0:
                domains[var] = [puzzle[r][c]]  # Ô đã điền
            else:
                domains[var] = list(range(1, 10))  # Ô trống: 1-9

            neighbors[var] = set()

    # Xây dựng ràng buộc: cùng hàng, cùng cột, cùng khối 3x3
    for r in range(9):
        for c in range(9):
            var = (r, c)

            # Cùng hàng
            for c2 in range(9):
                if c2 != c:
                    neighbors[var].add((r, c2))

            # Cùng cột
            for r2 in range(9):
                if r2 != r:
                    neighbors[var].add((r2, c))

            # Cùng khối 3x3
            br, bc = 3 * (r // 3), 3 * (c // 3)
            for r2 in range(br, br + 3):
                for c2 in range(bc, bc + 3):
                    if (r2, c2) != (r, c):
                        neighbors[var].add((r2, c2))

    return CSP(variables, domains, neighbors)


# ==================== HIỂN THỊ SUDOKU ====================

def visualize_sudoku(original, solved):
    """Hiển thị Sudoku gốc và lời giải bằng matplotlib"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('CSP: GIẢI SUDOKU\nBacktracking + AC-3 + Forward Checking',
                 fontsize=16, fontweight='bold')

    titles = ['Đề Bài', 'Lời Giải']
    grids = [original, solved]

    for ax, title, grid in zip(axes, titles, grids):
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
        ax.axis('off')

        # Vẽ nền ô
        for r in range(9):
            for c in range(9):
                # Tô màu khối 3x3 xen kẽ
                block = (r // 3) * 3 + (c // 3)
                if block % 2 == 0:
                    bg_color = '#F0F4FF'
                else:
                    bg_color = '#E8F5E9'

                rect = patches.Rectangle((c, 8 - r), 1, 1,
                                          facecolor=bg_color, edgecolor='#CCCCCC',
                                          linewidth=0.5)
                ax.add_patch(rect)

                val = grid[r][c]
                if val != 0:
                    # Ô gốc: đậm, ô giải: màu xanh
                    is_original = original[r][c] != 0
                    color = '#1A1A2E' if is_original else '#E74C3C'
                    weight = 'bold' if is_original else 'normal'
                    fontsize = 16 if is_original else 14

                    ax.text(c + 0.5, 8 - r + 0.5, str(val),
                            ha='center', va='center',
                            fontsize=fontsize, fontweight=weight, color=color)

        # Vẽ viền khối 3x3 đậm
        for i in range(0, 10, 3):
            ax.plot([i, i], [0, 9], 'k-', linewidth=2.5)
            ax.plot([0, 9], [i, i], 'k-', linewidth=2.5)

        # Vẽ viền ngoài
        for i in range(10):
            ax.plot([i, i], [0, 9], color='#666666', linewidth=0.5)
            ax.plot([0, 9], [i, i], color='#666666', linewidth=0.5)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()


def print_sudoku(grid, title=""):
    """In Sudoku ra terminal"""
    if title:
        print(title)
    print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    for r in range(9):
        row_str = "| "
        for c in range(9):
            val = grid[r][c]
            row_str += str(val) if val != 0 else "."
            row_str += " "
            if (c + 1) % 3 == 0:
                row_str += "| "
        print(row_str)
        if (r + 1) % 3 == 0:
            print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    print()


# ==================== CHẠY CHƯƠNG TRÌNH ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  CONSTRAINT SATISFACTION: GIẢI SUDOKU 9x9")
    print("  Thuật toán: Backtracking + AC-3 + Forward Checking + MRV")
    print("=" * 60)
    print()

    # Đề bài Sudoku (0 = ô trống)
    puzzle = np.array([
        [5, 3, 0,  0, 7, 0,  0, 0, 0],
        [6, 0, 0,  1, 9, 5,  0, 0, 0],
        [0, 9, 8,  0, 0, 0,  0, 6, 0],

        [8, 0, 0,  0, 6, 0,  0, 0, 3],
        [4, 0, 0,  8, 0, 3,  0, 0, 1],
        [7, 0, 0,  0, 2, 0,  0, 0, 6],

        [0, 6, 0,  0, 0, 0,  2, 8, 0],
        [0, 0, 0,  4, 1, 9,  0, 0, 5],
        [0, 0, 0,  0, 8, 0,  0, 7, 9],
    ])

    empty_count = np.sum(puzzle == 0)
    print(f"Số ô trống: {empty_count}/81")
    print(f"Số biến CSP: 81 (mỗi ô là 1 biến)")
    print(f"Miền giá trị: {{1, 2, 3, 4, 5, 6, 7, 8, 9}}")
    print(f"Ràng buộc: All-different cho mỗi hàng, cột, khối 3x3")
    print()

    print_sudoku(puzzle, "ĐỀ BÀI:")
