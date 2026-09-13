# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Đức Đông  
> **Mã Sinh Viên / Mã Học viên:** 2A202602367  
> **Chủ đề Lựa chọn:** *Trợ lý Tuyển dụng & Sàng lọc CV:* Tra cứu tiêu chí tuyển dụng vị trí và gửi thông báo lịch phỏng vấn.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | Bài toán đòi hỏi chuỗi suy luận liên tiếp: (1) Tiếp nhận hồ sơ/mã ứng viên, (2) Tra cứu tiêu chí vị trí tuyển dụng (kỹ năng, kinh nghiệm), (3) Thẩm định và đối chiếu hồ sơ với tiêu chuẩn, (4) Ra quyết định Đạt/Không đạt, (5) Lên lịch hoặc chuẩn bị nội dung thông báo phỏng vấn. |
| **2. Tool Interaction** | 5 / 5 | Cần tương tác tối thiểu 2 công cụ: 1 công cụ tra cứu dữ liệu (tra cứu tiêu chí tuyển dụng/thông tin ứng viên từ DB) và 1 công cụ hành động (gửi email thông báo mời phỏng vấn / cập nhật trạng thái tuyển dụng). |
| **3. Dynamic Decision** | 5 / 5 | Bước tiếp theo phụ thuộc hoàn toàn vào Observation của bước trước: nếu ứng viên không đáp ứng tiêu chuẩn thì từ chối/báo thiếu tiêu chí; chỉ khi đủ điều kiện mới tiến hành kích hoạt công cụ gửi lịch phỏng vấn. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải bám sát mục tiêu hoàn tất quy trình sàng lọc và gửi thư mời xuyên suốt qua nhiều bước gọi công cụ và phân tích kết quả trả về mà không bị lệch ngữ cảnh. |
| **TỔNG ĐIỂM AGENTIC FIT** | **19 / 20** | *Tổng điểm 19/20 (> 12/20): Bài toán rất phù hợp triển khai Agentic System (ReAct pattern).* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin hồ sơ, điểm đánh giá CV và kết quả sàng lọc của ứng viên UV2026001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "candidate_query",
    "arguments": {
      "candidate_id": "UV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "candidate_id": "UV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "position": "Kỹ sư Trí tuệ Nhân tạo (AI Engineer)",
        "experience_years": 3,
        "cv_score": 8.8,
        "skills": [
          "Python",
          "PyTorch",
          "LangChain",
          "LLM Fine-tuning"
        ],
        "status": "Đạt vòng hồ sơ (Qualified)",
        "email": "an.nguyen@example.com",
        "interviewer": "Trưởng phòng Nhân sự",
        "notes": "Hồ sơ xuất sắc, đáp ứng đầy đủ tiêu chí kỹ thuật vị trí AI Engineer."
      }
    },
    "latency_ms": 1055.75
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin hồ sơ, điểm đánh giá CV và kết quả sàng lọc của ứng viên UV2026001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Mô hình LLM phân tích kết quả từ MCP Server và sinh câu trả lời hoàn chỉnh.",
    "output": "Ứng viên Nguyễn Văn An (UV2026001) ứng tuyển Kỹ sư AI với điểm CV 8.8/10, kinh nghiệm 3 năm, đạt vòng sàng lọc hồ sơ và sẵn sàng phỏng vấn.",
    "latency_ms": 1174.13
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã cấu hình và kiểm thử Agent chạy mượt mà chuỗi suy luận Thought -> Action -> Observation với MCP Server.
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 / 4 lượt (TC02, TC03, TC04, TC05).
- **Kết quả đẩy Repo nộp bài:** [x] Sẵn sàng Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
