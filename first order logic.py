# ==================== FIRST-ORDER LOGIC & INFERENCE ====================
# Giải câu đố số học chữ (Cryptarithmetic): SEND + MORE = MONEY
# Phần của Đức: Biểu diễn bộ ràng buộc bằng FOL
# =====================================================================

# ==================== BIỂU DIỄN RÀNG BUỘC BẰNG FOL ====================
#
# Bài toán:  S E N D
#           + M O R E
#           ---------
#           M O N E Y
#
# Biến: {S, E, N, D, M, O, R, Y} → mỗi biến nhận giá trị từ 0-9
#
# Biểu diễn FOL:
#   ∀x ∈ Variables: 0 ≤ x ≤ 9                     (miền giá trị)
#   ∀x,y ∈ Variables: x ≠ y → val(x) ≠ val(y)    (tất cả khác nhau)
#   S ≠ 0 ∧ M ≠ 0                                  (không bắt đầu bằng 0)
#   SEND + MORE = MONEY                             (ràng buộc số học)
#
# Ràng buộc số học chi tiết (theo cột, từ phải sang trái):
#   c0 = 0  (carry ban đầu)
#   D + E = Y + 10*c1
#   N + R + c1 = E + 10*c2
#   E + O + c2 = N + 10*c3
#   S + M + c3 = O + 10*c4
#   c4 = M
#   với c1, c2, c3, c4 ∈ {0, 1}


class CryptarithmeticFOL:
    """
    Biểu diễn bài toán Cryptarithmetic bằng First-Order Logic.
    Mỗi ràng buộc được mã hóa thành một hàm kiểm tra.
    """

    def __init__(self, word1, word2, result):
        self.word1 = word1    # "SEND"
        self.word2 = word2    # "MORE"
        self.result = result  # "MONEY"

        # Trích xuất biến (các chữ cái duy nhất)
        self.variables = list(set(word1 + word2 + result))
        self.variables.sort()

        # Các chữ cái đứng đầu (không được = 0)
        self.leading_chars = set()
        if word1:
            self.leading_chars.add(word1[0])
        if word2:
            self.leading_chars.add(word2[0])
        if result:
            self.leading_chars.add(result[0])

    def in_rang_buoc(self):
        """In tất cả ràng buộc FOL của bài toán"""
        print(f"Bài toán: {self.word1} + {self.word2} = {self.result}")
        print()
        print("Biến:", self.variables)
        print(f"Số biến: {len(self.variables)}")
        print()
        print("Ràng buộc FOL:")
        print(f"  1) ∀x ∈ {{{', '.join(self.variables)}}}: 0 ≤ val(x) ≤ 9")
        print(f"  2) ∀x,y ∈ Variables, x ≠ y → val(x) ≠ val(y)")
        for ch in sorted(self.leading_chars):
            print(f"  3) val({ch}) ≠ 0  (chữ đứng đầu)")
        print(f"  4) num({self.word1}) + num({self.word2}) = num({self.result})")
        print()
        print("Ràng buộc số học theo cột (phải → trái):")
        w1 = self.word1[::-1]
        w2 = self.word2[::-1]
        r = self.result[::-1]
        max_len = max(len(self.word1), len(self.word2))
        print(f"  c0 = 0")
        for i in range(max_len):
            ch1 = w1[i] if i < len(w1) else "0"
            ch2 = w2[i] if i < len(w2) else "0"
            ch_r = r[i] if i < len(r) else "0"
            print(f"  {ch1} + {ch2} + c{i} = {ch_r} + 10*c{i+1}")
        if len(self.result) > max_len:
            print(f"  c{max_len} = {r[max_len]}")

    # ---------- RÀNG BUỘC 1: Miền giá trị ----------

    def rang_buoc_mien_gia_tri(self, assignment):
        """∀x ∈ Variables: 0 ≤ val(x) ≤ 9"""
        for var, val in assignment.items():
            if not (0 <= val <= 9):
                return False
        return True

    # ---------- RÀNG BUỘC 2: Tất cả khác nhau ----------

    def rang_buoc_khac_nhau(self, assignment):
        """∀x,y ∈ Variables, x ≠ y → val(x) ≠ val(y) (AllDifferent)"""
        values = list(assignment.values())
        return len(values) == len(set(values))

    # ---------- RÀNG BUỘC 3: Chữ đứng đầu ≠ 0 ----------

    def rang_buoc_khong_bat_dau_bang_0(self, assignment):
        """Chữ cái đứng đầu mỗi từ không được bằng 0"""
        for ch in self.leading_chars:
            if ch in assignment and assignment[ch] == 0:
                return False
        return True

    # ---------- RÀNG BUỘC 4: Số học ----------

    def word_to_number(self, word, assignment):
        """Chuyển từ thành số dựa trên phép gán"""
        num = 0
        for ch in word:
            num = num * 10 + assignment[ch]
        return num

    def rang_buoc_so_hoc(self, assignment):
        """num(word1) + num(word2) = num(result)"""
        num1 = self.word_to_number(self.word1, assignment)
        num2 = self.word_to_number(self.word2, assignment)
        num_r = self.word_to_number(self.result, assignment)
        return num1 + num2 == num_r

    # ---------- KIỂM TRA TẤT CẢ RÀNG BUỘC ----------

    def kiem_tra_tat_ca_rang_buoc(self, assignment):
        """Kiểm tra tất cả ràng buộc FOL"""
        return (self.rang_buoc_mien_gia_tri(assignment) and
                self.rang_buoc_khac_nhau(assignment) and
                self.rang_buoc_khong_bat_dau_bang_0(assignment) and
                self.rang_buoc_so_hoc(assignment))


# ==================== CHẠY CHƯƠNG TRÌNH ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  FIRST-ORDER LOGIC & INFERENCE: CRYPTARITHMETIC")
    print("  Phần Đức: Biểu diễn bộ ràng buộc bằng FOL")
    print("=" * 60)
    print()

    # --- Bài toán SEND + MORE = MONEY ---
    puzzle = CryptarithmeticFOL("SEND", "MORE", "MONEY")

    print("📋 RÀNG BUỘC FOL:")
    print("-" * 50)
    puzzle.in_rang_buoc()
    print()

    # --- Kiểm tra ràng buộc ---
    print("🧪 KIỂM TRA RÀNG BUỘC:")
    print("-" * 50)

    # Nghiệm đúng: S=9, E=5, N=6, D=7, M=1, O=0, R=8, Y=2
    test_assignment = {'S': 9, 'E': 5, 'N': 6, 'D': 7, 'M': 1, 'O': 0, 'R': 8, 'Y': 2}

    print(f"  Gán: {test_assignment}")
    print(f"  Miền giá trị [0-9]:        {puzzle.rang_buoc_mien_gia_tri(test_assignment)}")
    print(f"  Tất cả khác nhau:          {puzzle.rang_buoc_khac_nhau(test_assignment)}")
    print(f"  Chữ đầu ≠ 0:              {puzzle.rang_buoc_khong_bat_dau_bang_0(test_assignment)}")
    print(f"  SEND + MORE = MONEY:       {puzzle.rang_buoc_so_hoc(test_assignment)}")
    print(f"  → Thỏa mãn tất cả:        {puzzle.kiem_tra_tat_ca_rang_buoc(test_assignment)}")
