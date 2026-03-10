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
        self.ong = []       # danh sách (ông, cháu)
        self.ba = []        # danh sách (bà, cháu)
        self.anh_chi_em = []  # danh sách (người1, người2)

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
    def them_ong(self, ong, chau):
        """Thêm sự kiện: ông là ông của cháu"""
        fact = (ong, chau)
        if fact not in self.ong:
            self.ong.append(fact)
    def them_ba(self, ba, chau):
        """Thêm sự kiện: bà là bà của cháu"""
        fact = (ba, chau)
        if fact not in self.ba:
            self.ba.append(fact)
    def them_anh_chi_em(self, a, b):
        """Thêm sự kiện: a và b là anh chị em"""
        fact = (a, b)
        if fact not in self.anh_chi_em:
            self.anh_chi_em.append(fact)
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
    def la_ong(self, nguoi_a, nguoi_b):
        """Kiểm tra: A có phải là ông của B không"""
        return (nguoi_a, nguoi_b) in self.ong
    def la_ba(self, nguoi_a, nguoi_b):
        """Kiểm tra: A có phải là bà của B không"""
        return (nguoi_a, nguoi_b) in self.ba
    def la_anh_chi_em(self, nguoi_a, nguoi_b):
        """Kiểm tra hai người có phải anh chị em không"""
        return (nguoi_a, nguoi_b) in self.anh_chi_em or (nguoi_b, nguoi_a) in self.anh_chi_em
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
    def tim_chau(self, nguoi):
        """Tìm tất cả cháu của một người"""
        ds_chau = set()

        for ong, chau in self.ong:
            if ong == nguoi:
                ds_chau.add(chau)

        for ba, chau in self.ba:
            if ba == nguoi:
                ds_chau.add(chau)

        return list(ds_chau)
    def tim_anh_chi_em(self, nguoi):
        """Tìm tất cả anh chị em của một người"""
        ds = set()

        for a, b in self.anh_chi_em:
            if a == nguoi:
                ds.add(b)
            elif b == nguoi:
                ds.add(a)

        return list(ds)
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

    kb.them_ong("Ông Hùng", "An")
    kb.them_ong("Ông Hùng", "Bình")

    kb.them_ba("Bà Lan", "An")
    kb.them_ba("Bà Lan", "Bình")

    kb.them_anh_chi_em("An", "Bình")
    kb.them_anh_chi_em("Cường", "Duyên")
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
    #tìm ông bà
    queries_ong_ba = [
        ("Ông Hùng", "An"),
        ("Ông Hùng", "Bình"),
        ("Bà Lan", "An"),
        ("Bà Lan", "Bình")
    ]

    for a, b in queries_ong_ba:
        is_ong = kb.la_ong(a, b)
        is_ba = kb.la_ba(a, b)

        print(f"  {a} → {b}:")
        print(f"    ông({a}, {b}) = {is_ong}")
        print(f"    bà({a}, {b})  = {is_ba}")
        print()
    #tìm anh chị em
        queries_ace = [
            ("An", "Bình"),
            ("Cường", "Duyên"),
            ("An", "Cường")
        ]

        for a, b in queries_ace:
            is_ace = kb.la_anh_chi_em(a, b)

            print(f"  anh_chi_em({a}, {b}) = {is_ace}")