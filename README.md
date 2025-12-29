# 🧠 AI Data Validator & Anomaly Detection Tool

Hệ thống **AI Data Validator & Anomaly Detection Tool** là một dự án phân tích dữ liệu thông minh, ứng dụng các phương pháp thống kê và học máy cơ bản nhằm **đánh giá chất lượng dữ liệu đầu vào** và **phát hiện các điểm dữ liệu dị thường (outliers)** một cách **minh bạch, dễ giải thích (Explainable AI)**.

---

## 📌 Mục tiêu dự án

* Phát hiện dữ liệu dị thường trong các tập dữ liệu số (numerical datasets)
* Đánh giá mức độ “sạch” và độ tin cậy của dữ liệu
* Tránh sử dụng các mô hình AI dạng *black-box*, ưu tiên phương pháp khoa học có thể kiểm chứng
* Phù hợp cho các bài toán kiểm định dữ liệu, tiền xử lý dữ liệu (Data Preprocessing), và Audit dữ liệu

---

## 🔬 Scientific Methodology (Phương pháp khoa học)

Dự án áp dụng **kiểm định thống kê (Statistical Validation)** thay vì các mô hình học sâu phức tạp, nhằm đảm bảo:

* **Tính minh bạch (Transparency)**
* **Khả năng giải thích (Explainability)**
* **Tính tái lập (Reproducibility)**

---

## 1️⃣ Thuật toán phát hiện dị thường – Z-Score

Hệ thống sử dụng **Z-Score (Standard Score)** để đo lường mức độ lệch của từng điểm dữ liệu so với giá trị trung bình của toàn bộ tập dữ liệu.

### 📐 Công thức toán học

```
z = (x - μ) / σ
```

Trong đó:

* **x**: Giá trị quan sát hiện tại
* **μ (Mean)**: Giá trị trung bình của tập dữ liệu
* **σ (Standard Deviation)**: Độ lệch chuẩn – mức độ phân tán của dữ liệu

### 🎯 Ngưỡng quyết định (Threshold)

* Ngưỡng áp dụng: **|z| > 2.0**
* Theo phân phối chuẩn, các điểm vượt ngưỡng này có xác suất xuất hiện < 5% (**p < 0.05**)
* Các điểm này được xác định là **Outliers (Dữ liệu dị thường)**

---

## 2️⃣ AI Score – Confidence Level

Sau khi phát hiện và loại bỏ dữ liệu nhiễu, hệ thống tính toán **AI Score** nhằm đánh giá độ tin cậy tổng thể của tập dữ liệu.

### 📊 Công thức tính

```
AI Score = ((N - N_outliers) / N) × 100
```

Trong đó:

* **N**: Tổng số điểm dữ liệu
* **N_outliers**: Số lượng điểm dữ liệu dị thường

### 📈 Mức đánh giá

| AI Score       | Đánh giá                                                      |
| -------------- | ------------------------------------------------------------- |
| **90% – 100%** | Dữ liệu rất tốt, tuân thủ phân phối chuẩn                     |
| **70% – 89%**  | Dữ liệu ổn định, có một số sai số ngẫu nhiên                  |
| **< 70%**      | ❌ Reject – Dữ liệu bị nhiễu nặng hoặc có can thiệp bất thường |

---

## 🏗 System Architecture (Kiến trúc hệ thống)

Hệ thống được xây dựng theo mô hình **Client–Server**, tách biệt rõ ràng giữa phần xử lý và phần hiển thị.

### 🎨 Frontend (UI/UX)

* **Tailwind CSS**: Xây dựng giao diện Dashboard hiện đại, responsive
* **Chart.js**: Trực quan hóa phân phối dữ liệu và tần suất outliers theo thời gian thực

### ⚙️ Backend – Processing Engine

* **FastAPI**: Xây dựng RESTful API hiệu năng cao
* **Pandas**: Đọc và cấu trúc dữ liệu từ file **CSV / Excel**
* **NumPy**: Tính toán vector hóa (Mean, Std, Z-Score) với hiệu suất cao

### 💾 Data Persistence

* **SQLite**:

  * Lưu lịch sử kiểm định dữ liệu
  * Ghi log kết quả phân tích
  * Hỗ trợ **Audit Trail** và đối soát dữ liệu

---

## 🚀 Ứng dụng thực tế

* Kiểm tra chất lượng dữ liệu trước khi huấn luyện ML Model
* Phát hiện lỗi nhập liệu, lỗi cảm biến (Sensor Error)
* Hỗ trợ phân tích dữ liệu trong Finance, IoT, Data Engineering
* Làm sản phẩm Portfolio / CV cho Data Analyst, Data Scientist, AI Engineer

---

## 📎 Ghi chú

> Đây là một dự án tập trung vào **tư duy khoa học, dữ liệu sạch và khả năng giải thích**, rất phù hợp để trình bày trong CV hoặc public trên GitHub.

---

✨ *Built with Data, Science & Explainable AI*

## Cấu trúc của Project

```
Python Data Validation & Bug Detection Tool
├─ app.py
├─ core
│  └─ analyzer.py
├─ pictures
│  ├─ dashboard.png
│  ├─ test 1.png
│  └─ test 2.png
├─ README.md
├─ requirements.txt
├─ static
│  └─ style.css
└─ templates
   └─ index.html

```