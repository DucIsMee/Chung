import numpy as np

# ==================== RANDOMIZED SEARCH: RANDOM FOREST ====================

np.random.seed(42)

# Sinh ngẫu nhiên số lượng cây (n_estimators)
n_iterations = 10  # Số lần thử ngẫu nhiên
min_trees = 10
max_trees = 300

random_n_estimators = np.random.randint(min_trees, max_trees + 1, size=n_iterations)

print("=" * 60)
print("  SINH NGẪU NHIÊN SỐ LƯỢNG CÂY CHO RANDOM FOREST")
print("=" * 60)
print()
print(f"Số lần thử:  {n_iterations}")
print(f"Khoảng giá trị: [{min_trees}, {max_trees}]")
print()
print(f"Các giá trị n_estimators được sinh ngẫu nhiên:")
for i, n in enumerate(random_n_estimators):
    print(f"  Lần {i+1}: {n} cây")
