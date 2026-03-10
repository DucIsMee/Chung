# ==================== PROBABILISTIC REASONING ====================
# Phát hiện thư rác: Naive Bayes Spam Classifier
# Phần của Đức: Đánh giá mô hình (Precision, Recall, F1)
# ================================================================

import re
import math
from collections import Counter, defaultdict

# ==================== DỮ LIỆU MẪU ====================

# Tập huấn luyện
train_data = [
    ("Bạn trúng thưởng 1 tỷ đồng, nhấn link nhận thưởng ngay", "spam"),
    ("Giảm giá sốc 90%, mua ngay hôm nay, ưu đãi có hạn", "spam"),
    ("Chúc mừng bạn đã được chọn nhận iPhone miễn phí", "spam"),
    ("Kiếm tiền online dễ dàng, thu nhập 50 triệu mỗi tháng", "spam"),
    ("Click vào link này để nhận quà tặng giá trị", "spam"),
    ("Vay tiền nhanh không cần thế chấp lãi suất 0%", "spam"),
    ("Bạn có tin nhắn chưa đọc, đăng nhập ngay để xem", "spam"),
    ("Khuyến mãi đặc biệt chỉ dành riêng cho bạn hôm nay", "spam"),
    ("Anh ơi chiều nay họp nhóm lúc 3 giờ nhé", "ham"),
    ("Em gửi anh báo cáo tuần này, anh xem giúp em", "ham"),
    ("Lịch họp ngày mai đã được cập nhật trên calendar", "ham"),
    ("Chị ơi cho em hỏi deadline dự án là khi nào ạ", "ham"),
    ("Mình gửi bạn tài liệu tham khảo cho bài thuyết trình", "ham"),
    ("Cảm ơn bạn đã gửi file, mình sẽ review sớm", "ham"),
    ("Nhắc lịch: buổi seminar AI vào thứ 6 tuần này", "ham"),
    ("Anh có thể giúp em debug đoạn code này không", "ham"),
]

# Tập kiểm thử
test_data = [
    ("Trúng thưởng xe hơi, nhấn link nhận ngay miễn phí", "spam"),
    ("Giảm giá 95% tất cả sản phẩm chỉ hôm nay", "spam"),
    ("Kiếm tiền tại nhà dễ dàng thu nhập cao", "spam"),
    ("Vay nhanh online lãi suất thấp không thế chấp", "spam"),
    ("Em gửi anh slide bài thuyết trình tuần tới", "ham"),
    ("Họp nhóm dự án lúc 2 giờ chiều mai nhé", "ham"),
    ("Bạn ơi cho mình xin tài liệu buổi học hôm qua", "ham"),
    ("Cảm ơn anh đã review code, em sẽ sửa lại", "ham"),
    ("Nhận thưởng 500 triệu ngay bây giờ click link", "spam"),
    ("Lịch thi cuối kỳ đã được cập nhật trên hệ thống", "ham"),
]


# ==================== TIỀN XỬ LÝ ĐƠN GIẢN ====================

def tien_xu_ly(text):
    """Tokenization đơn giản: tách từ, chuyển lowercase"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens


# ==================== NAIVE BAYES (HUẤN LUYỆN) ====================

class NaiveBayesSpam:
    """Bộ phân loại Naive Bayes cho spam detection"""

    def __init__(self):
        self.word_counts = defaultdict(Counter)  # {label: Counter(word: count)}
        self.class_counts = Counter()             # {label: count}
        self.vocab = set()
        self.total_words = defaultdict(int)

    def huan_luyen(self, data):
        """Huấn luyện mô hình trên tập dữ liệu"""
        for text, label in data:
            tokens = tien_xu_ly(text)
            self.class_counts[label] += 1
            for token in tokens:
                self.word_counts[label][token] += 1
                self.vocab.add(token)
                self.total_words[label] += 1

# ---------- HIỂN THỊ MÔ HÌNH SAU HUẤN LUYỆN ----------

    def hien_thi_mo_hinh(self):
        """In xác suất prior và một số xác suất từ vựng"""

        total_docs = sum(self.class_counts.values())

        print("XÁC SUẤT PRIOR P(class):")
        for label in self.class_counts:
            prob = self.class_counts[label] / total_docs
            print(f"  P({label}) = {prob:.4f}")

        print()
        print("MỘT SỐ XÁC SUẤT P(word | class):")

        vocab_sample = list(self.vocab)[:10]  # lấy 10 từ ví dụ
        vocab_size = len(self.vocab)

        for word in vocab_sample:
            print(f"\n  Từ: '{word}'")
            for label in self.class_counts:
                count = self.word_counts[label].get(word, 0)
                prob = (count + 1) / (self.total_words[label] + vocab_size)
                print(f"    P({word}|{label}) = {prob:.4f}")

    def du_doan(self, text):
        """Dự đoán nhãn cho một email"""
        tokens = tien_xu_ly(text)
        total_docs = sum(self.class_counts.values())
        vocab_size = len(self.vocab)

        best_label = None
        best_log_prob = float('-inf')

        for label in self.class_counts:
            # P(class) - prior
            log_prob = math.log(self.class_counts[label] / total_docs)

            # P(word|class) với Laplace smoothing
            for token in tokens:
                count = self.word_counts[label].get(token, 0)
                prob = (count + 1) / (self.total_words[label] + vocab_size)
                log_prob += math.log(prob)

            if log_prob > best_log_prob:
                best_log_prob = log_prob
                best_label = label

        return best_label

    def du_doan_tap(self, data):
        """Dự đoán trên tập dữ liệu, trả về (y_true, y_pred)"""
        y_true = []
        y_pred = []
        for text, label in data:
            pred = self.du_doan(text)
            y_true.append(label)
            y_pred.append(pred)
        return y_true, y_pred


# ==================== ĐÁNH GIÁ MÔ HÌNH (PHẦN CỦA ĐỨC) ====================

def tinh_confusion_matrix(y_true, y_pred, positive_label="spam"):
    """
    Tính confusion matrix:
      TP: dự đoán spam đúng
      FP: dự đoán spam nhưng thực tế ham
      FN: dự đoán ham nhưng thực tế spam
      TN: dự đoán ham đúng
    """
    tp = fp = fn = tn = 0
    for true, pred in zip(y_true, y_pred):
        if true == positive_label and pred == positive_label:
            tp += 1
        elif true != positive_label and pred == positive_label:
            fp += 1
        elif true == positive_label and pred != positive_label:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def tinh_precision(tp, fp):
    """
    Precision = TP / (TP + FP)
    Tỷ lệ dự đoán spam đúng trong tổng số dự đoán là spam
    """
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)


def tinh_recall(tp, fn):
    """
    Recall = TP / (TP + FN)
    Tỷ lệ spam thực tế được phát hiện đúng
    """
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)


def tinh_f1(precision, recall):
    """
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    Trung bình điều hòa của Precision và Recall
    """
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)


def tinh_accuracy(tp, tn, total):
    """Accuracy = (TP + TN) / Total"""
    if total == 0:
        return 0.0
    return (tp + tn) / total


def danh_gia_mo_hinh(y_true, y_pred, positive_label="spam"):
    """Đánh giá toàn diện mô hình: Precision, Recall, F1, Accuracy"""
    tp, fp, fn, tn = tinh_confusion_matrix(y_true, y_pred, positive_label)

    precision = tinh_precision(tp, fp)
    recall = tinh_recall(tp, fn)
    f1 = tinh_f1(precision, recall)
    accuracy = tinh_accuracy(tp, tn, len(y_true))

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }


def in_confusion_matrix(tp, fp, fn, tn):
    """In confusion matrix dạng bảng"""
    print("                  Dự đoán")
    print("                SPAM    HAM")
    print(f"  Thực tế SPAM   {tp:<6}  {fn}")
    print(f"  Thực tế HAM    {fp:<6}  {tn}")


def in_danh_gia(metrics):
    """In kết quả đánh giá"""
    print(f"  Precision : {metrics['precision']:.4f}  "
          f"(Trong {metrics['tp'] + metrics['fp']} dự đoán spam, "
          f"{metrics['tp']} đúng)")
    print(f"  Recall    : {metrics['recall']:.4f}  "
          f"(Trong {metrics['tp'] + metrics['fn']} spam thực tế, "
          f"phát hiện {metrics['tp']})")
    print(f"  F1-Score  : {metrics['f1']:.4f}")
    print(f"  Accuracy  : {metrics['accuracy']:.4f}  "
          f"({metrics['tp'] + metrics['tn']}/{metrics['tp'] + metrics['fp'] + metrics['fn'] + metrics['tn']} đúng)")


# ==================== CHẠY CHƯƠNG TRÌNH ====================

if __name__ == "__main__":
    print("=" * 65)
    print("  PROBABILISTIC REASONING: NAIVE BAYES SPAM CLASSIFIER")
    print("  Phần Đức: Đánh giá mô hình (Precision, Recall, F1)")
    print("=" * 65)
    print()

    # --- Huấn luyện ---
    model = NaiveBayesSpam()
    model.huan_luyen(train_data)

    print()
    print(" MÔ HÌNH SAU HUẤN LUYỆN:")
    print("-" * 50)
    model.hien_thi_mo_hinh()

    print(f"📚 HUẤN LUYỆN:")
    print(f"-" * 50)
    print(f"  Số email huấn luyện: {sum(model.class_counts.values())}")
    print(f"    Spam: {model.class_counts['spam']}")
    print(f"    Ham:  {model.class_counts['ham']}")
    print(f"  Kích thước từ vựng:  {len(model.vocab)}")
    print()

    # --- Dự đoán trên tập kiểm thử ---
    y_true, y_pred = model.du_doan_tap(test_data)

    # --- Đánh giá mô hình ---
    print("📊 ĐÁNH GIÁ MÔ HÌNH:")
    print("-" * 50)

    metrics = danh_gia_mo_hinh(y_true, y_pred, positive_label="spam")

    print()
    print("  Confusion Matrix:")
    in_confusion_matrix(metrics["tp"], metrics["fp"], metrics["fn"], metrics["tn"])
    print()
    in_danh_gia(metrics)
