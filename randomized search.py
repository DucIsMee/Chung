import numpy as np

# ==================== RANDOMIZED SEARCH: RANDOM FOREST ====================

np.random.seed(42)

# Sinh ngẫu nhiên số lượng cây (n_estimators)
n_iterations = 10  # Số lần thử ngẫu nhiên
min_trees = 10
max_trees = 300
# Sinh ngẫu nhiên độ sâu tối đa của cây (max_depth) khoảng giá trị sinh ngẫu nhiên
min_depth = 3
max_depth = 20

random_n_estimators = np.random.randint(min_trees, max_trees + 1, size=n_iterations)

random_max_depth = np.random.randint(min_depth, max_depth + 1, size=n_iterations)

print("=" * 60)
print("  SINH NGẪU NHIÊN SỐ LƯỢNG CÂY CHO RANDOM FOREST")
print("=" * 60)
print()
print(f"Số lần thử:  {n_iterations}")
print(f"Khoảng giá trị: [{min_trees}, {max_trees}]")
print()
print(f"Các giá trị n_estimators được sinh ngẫu nhiên:")
for i in range(n_iterations):
    print(f"  Lần {i+1}:")
    print(f"     n_estimators = {random_n_estimators[i]}")
    print(f"     max_depth    = {random_max_depth[i]}")
