# ==================== LOGIC & INFERENCE IN AI ====================
# Hệ thống suy luận cây gia phả
# Phần của Đức: Mã hóa luật quan hệ cha, mẹ -> con
# ================================================================

# ==================== CƠ SỞ TRI THỨC (KNOWLEDGE BASE) ====================

class FamilyKnowledgeBase:
    """
    Cơ sở tri thức lưu trữ các sự kiện và luật quan hệ gia đình.
    Sự kiện: cha(A, B) nghĩa là A là cha của B
              mẹ(A, B) nghĩa là A là mẹ của B
    Luật:     cha_mẹ(X, Y) ← cha(X, Y) ∨ mẹ(X, Y)
              con(Y, X)    ← cha_mẹ(X, Y)
    """

    def __init__(self):
        # Sự kiện cơ bản: cha(X, Y) và mẹ(X, Y)
        self.cha = []   # danh sách (cha, con)
        self.me = []     # danh sách (mẹ, con)

    # ---------- THÊM SỰ KIỆN ----------

    def them_cha(self, cha, con):
        """Thêm sự kiện: cha là cha của con"""
        fact = (cha, con)
        if fact not in self.cha:
            self.cha.append(fact)

    def them_me(self, me, con):
        """Thêm sự kiện: mẹ là mẹ của con"""
        fact = (me, con)
        if fact not in self.me:
            self.me.append(fact)

    # ---------- LUẬT SUY DIỄN: CHA MẸ -> CON ----------

    def la_cha(self, nguoi_a, nguoi_b):
        """Kiểm tra: A có phải là cha của B không?"""
        return (nguoi_a, nguoi_b) in self.cha

    def la_me(self, nguoi_a, nguoi_b):
        """Kiểm tra: A có phải là mẹ của B không?"""
        return (nguoi_a, nguoi_b) in self.me

    def la_cha_me(self, nguoi_a, nguoi_b):
        """
        Luật: cha_mẹ(X, Y) ← cha(X, Y) ∨ mẹ(X, Y)
        A là cha/mẹ của B nếu A là cha của B HOẶC A là mẹ của B
        """
        return self.la_cha(nguoi_a, nguoi_b) or self.la_me(nguoi_a, nguoi_b)

    def la_con(self, nguoi_a, nguoi_b):
        """
        Luật: con(Y, X) ← cha_mẹ(X, Y)
        A là con của B nếu B là cha/mẹ của A
        """
        return self.la_cha_me(nguoi_b, nguoi_a)

    # ---------- TRUY VẤN ----------

    def tim_con(self, nguoi):
        """Tìm tất cả con của một người"""
        ds_con = set()
        for cha, con in self.cha:
            if cha == nguoi:
                ds_con.add(con)
        for me, con in self.me:
            if me == nguoi:
                ds_con.add(con)
        return list(ds_con)

    def tim_cha_me(self, nguoi):
        """Tìm cha và mẹ của một người"""
        ds_cha_me = []
        for cha, con in self.cha:
            if con == nguoi:
                ds_cha_me.append(("cha", cha))
        for me, con in self.me:
            if con == nguoi:
                ds_cha_me.append(("mẹ", me))
        return ds_cha_me

    # ---------- IN CÂY GIA PHẢ ----------

    def in_tat_ca_su_kien(self):
        """In tất cả sự kiện trong cơ sở tri thức"""
        print("Sự kiện CHA:")
        for cha, con in self.cha:
            print(f"  cha({cha}, {con})")
        print("Sự kiện MẸ:")
        for me, con in self.me:
            print(f"  mẹ({me}, {con})")


# ==================== DỮ LIỆU MẪU: CÂY GIA PHẢ ====================

#           Ông Hùng --- Bà Lan
#              |              |
#        +-----+-----+
#        |            |
#   Minh(♂)      Hoa(♀)
#   + Linh(♀)    + Tuấn(♂)
#     |              |
#  +--+--+        +--+--+
#  |     |        |     |
# An    Bình    Cường  Duyên

# ==================== CHẠY CHƯƠNG TRÌNH ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  LOGIC & INFERENCE IN AI: HỆ THỐNG SUY LUẬN CÂY GIA PHẢ")
    print("  Phần Đức: Mã hóa luật quan hệ cha, mẹ → con")
    print("=" * 60)
    print()

    kb = FamilyKnowledgeBase()

    # --- Nhập sự kiện ---
    # Thế hệ 1 → 2
    kb.them_cha("Ông Hùng", "Minh")
    kb.them_cha("Ông Hùng", "Hoa")
    kb.them_me("Bà Lan", "Minh")
    kb.them_me("Bà Lan", "Hoa")

    # Thế hệ 2 → 3
    kb.them_cha("Minh", "An")
    kb.them_cha("Minh", "Bình")
    kb.them_me("Linh", "An")
    kb.them_me("Linh", "Bình")

    kb.them_cha("Tuấn", "Cường")
    kb.them_cha("Tuấn", "Duyên")
    kb.them_me("Hoa", "Cường")
    kb.them_me("Hoa", "Duyên")

    # --- In sự kiện ---
    print("📋 CƠ SỞ TRI THỨC:")
    print("-" * 40)
    kb.in_tat_ca_su_kien()
    print()

    # --- Kiểm tra quan hệ cha mẹ → con ---
    print("🔍 KIỂM TRA LUẬT CHA, MẸ → CON:")
    print("-" * 40)

    queries = [
        ("Ông Hùng", "Minh"),
        ("Bà Lan", "Hoa"),
        ("Minh", "An"),
        ("Linh", "Bình"),
        ("Hoa", "Cường"),
    ]

    for a, b in queries:
        is_cha = kb.la_cha(a, b)
        is_me = kb.la_me(a, b)
        is_cha_me = kb.la_cha_me(a, b)
        is_con = kb.la_con(b, a)

        print(f"  {a} → {b}:")
        print(f"    cha({a}, {b})     = {is_cha}")
        print(f"    mẹ({a}, {b})      = {is_me}")
        print(f"    cha_mẹ({a}, {b}) = {is_cha_me}")
        print(f"    con({b}, {a})     = {is_con}")
        print()

    # --- Truy vấn nâng cao ---
    print("🔎 TRUY VẤN NÂNG CAO:")
    print("-" * 40)

    # Tìm con
    for nguoi in ["Ông Hùng", "Minh", "Hoa"]:
        ds_con = kb.tim_con(nguoi)
        print(f"  Con của {nguoi}: {ds_con}")

    print()

    # Tìm cha mẹ
    for nguoi in ["Minh", "An", "Cường"]:
        ds_cha_me = kb.tim_cha_me(nguoi)
        print(f"  Cha mẹ của {nguoi}: {ds_cha_me}")
