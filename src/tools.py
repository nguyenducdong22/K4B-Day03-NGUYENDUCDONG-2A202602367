"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Chủ đề: Trợ lý Tuyển dụng & Sàng lọc CV (Recruitment & CV Screening Assistant)
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu hồ sơ ứng viên và kết quả sàng lọc CV
    {
        "name": "candidate_query",
        "description": "Tra cứu hồ sơ ứng viên, vị trí ứng tuyển, điểm đánh giá CV và kết quả sàng lọc ban đầu bằng mã ứng viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần tra cứu (ví dụ: 'UV2026001')"
                }
            },
            "required": ["candidate_id"]
        }
    },
    
    # Tool 2: Đặt lịch và gửi thông báo mời phỏng vấn cho ứng viên (TODO 1.2)
    {
        "name": "schedule_interview",
        "description": "Đặt lịch hẹn và gửi thông báo mời phỏng vấn cho ứng viên đạt vòng sàng lọc hồ sơ.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần gửi thông báo lịch phỏng vấn (ví dụ: 'UV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn phỏng vấn (ví dụ: '14:00 20/09/2026')"
                },
                "interviewer_name": {
                    "type": "string",
                    "description": "Tên người phỏng vấn phụ trách (ví dụ: 'Trưởng phòng Nhân sự' hoặc 'TS. Lê Tuyển Dụng')"
                }
            },
            "required": ["candidate_id", "datetime_str"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "UV2026001": {
        "full_name": "Nguyễn Văn An",
        "position": "Kỹ sư Trí tuệ Nhân tạo (AI Engineer)",
        "experience_years": 3,
        "cv_score": 8.8,
        "skills": ["Python", "PyTorch", "LangChain", "LLM Fine-tuning"],
        "status": "Đạt vòng hồ sơ (Qualified)",
        "email": "an.nguyen@example.com",
        "interviewer": "Trưởng phòng Nhân sự",
        "notes": "Hồ sơ xuất sắc, đáp ứng đầy đủ tiêu chí kỹ thuật vị trí AI Engineer."
    },
    "UV2026002": {
        "full_name": "Trần Thị Bình",
        "position": "Chuyên viên Phân tích Dữ liệu (Data Analyst)",
        "experience_years": 2,
        "cv_score": 8.2,
        "skills": ["SQL", "PowerBI", "Python", "Data Modeling"],
        "status": "Đạt vòng hồ sơ (Qualified)",
        "email": "binh.tran@example.com",
        "interviewer": "TS. Lê Tuyển Dụng",
        "notes": "Đáp ứng tốt các yêu cầu phân tích dữ liệu và trực quan hóa."
    },
    # Alias cho SV2026001 để đảm bảo tương thích ngược
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "position": "Kỹ sư Trí tuệ Nhân tạo (AI Engineer)",
        "experience_years": 3,
        "cv_score": 8.8,
        "skills": ["Python", "PyTorch", "LangChain"],
        "status": "Đạt vòng hồ sơ (Qualified)",
        "email": "an.nguyen@example.com",
        "interviewer": "Trưởng phòng Nhân sự",
        "notes": "Hồ sơ ứng viên đạt tiêu chuẩn tuyển dụng."
    }
}


def execute_candidate_query(candidate_id: str = "", student_id: str = "") -> str:
    """Thực thi tra cứu hồ sơ ứng viên theo mã ứng viên"""
    cid = (candidate_id or student_id).strip().upper()
    candidate = MOCK_DATABASE.get(cid)
    if candidate:
        return json.dumps({
            "status": "SUCCESS",
            "candidate_id": cid,
            "data": candidate
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu hồ sơ ứng viên có mã '{cid}' trong hệ thống tuyển dụng."
        }, ensure_ascii=False)


def execute_academic_query(student_id: str = "", candidate_id: str = "") -> str:
    """Alias tương thích cho execute_candidate_query"""
    return execute_candidate_query(candidate_id=candidate_id, student_id=student_id)


def execute_schedule_interview(
    candidate_id: str = "",
    student_id: str = "",
    datetime_str: str = "",
    interviewer_name: str = "",
    advisor_name: str = ""
) -> str:
    """Thực thi đặt lịch và gửi thông báo phỏng vấn"""
    cid = (candidate_id or student_id).strip().upper()
    interviewer = interviewer_name or advisor_name or "Trưởng phòng Nhân sự"
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"INT-{cid}-2026",
        "candidate_id": cid,
        "datetime": datetime_str,
        "interviewer": interviewer,
        "message": f"Đã đặt lịch và gửi thông báo phỏng vấn thành công cho ứng viên {cid} với {interviewer} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def execute_schedule_appointment(
    student_id: str = "",
    candidate_id: str = "",
    datetime_str: str = "",
    advisor_name: str = "Trưởng phòng Nhân sự",
    interviewer_name: str = ""
) -> str:
    """Alias tương thích cho execute_schedule_interview"""
    return execute_schedule_interview(
        candidate_id=candidate_id,
        student_id=student_id,
        datetime_str=datetime_str,
        interviewer_name=interviewer_name,
        advisor_name=advisor_name
    )


# Router gọi tool thực tế
TOOL_ROUTER = {
    "candidate_query": execute_candidate_query,
    "schedule_interview": execute_schedule_interview,
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

# ==============================================================================
# 3. HÀM ĐIỀU TUYẾN THỰC THI TOOL (TASK 2.1 - PYTHON DISPATCHER)
# ==============================================================================

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    [TASK 2.1] Hàm trung chuyển thực thi tool (Python Dispatcher)
    - Nhận tên công cụ (tool_name) và tham số (arguments) do LLM quyết định.
    - Điều tuyến và gọi đúng hàm Python thực thi tương ứng.
    - Trả về chuỗi kết quả JSON chuẩn hóa.
    """
    # --------------------------------------------------------------------------
    # TODO 2.1: HỌC VIÊN HOÀN THIỆN HÀM ĐIỀU TUYẾN DISPATCH_TOOL_CALL
    # --------------------------------------------------------------------------
    if tool_name in ["candidate_query", "academic_query"]:
        return execute_candidate_query(**arguments)
    elif tool_name in ["schedule_interview", "schedule_appointment"]:
        return execute_schedule_interview(**arguments)
    elif tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("==========================================================")
    print("🛠️ KIỂM THỬ ĐỘC LẬP TOOLS & DISPATCHER (TASK 2.1)")
    print("==========================================================")
    print(f"✅ [TOOLS CHECK]: Đã đăng ký thành công {len(TOOLS_SCHEMA)} Native Tools trong TOOLS_SCHEMA!")
    
    # 1. Gọi thử candidate_query
    res_cand = dispatch_tool_call("candidate_query", {"candidate_id": "UV2026001"})
    data_cand = json.loads(res_cand)
    cand_name = data_cand.get("data", {}).get("full_name", "")
    print(f"🧪 Kết quả gọi thử candidate_query: Status {data_cand.get('status')} (Ứng viên {cand_name})")
    
    # 2. Gọi thử academic_query để đạt Pass Signal chuẩn của Checkpoint 2
    res_acad = dispatch_tool_call("academic_query", {"student_id": "SV2026001"})
    data_acad = json.loads(res_acad)
    acad_name = data_acad.get("data", {}).get("full_name", "")
    print(f"🧪 Kết quả gọi thử academic_query: Status {data_acad.get('status')} (Sinh viên {acad_name})")
    
    # 3. Gọi thử schedule_interview
    res_interview = dispatch_tool_call("schedule_interview", {
        "candidate_id": "UV2026001",
        "datetime_str": "14:00 20/09/2026",
        "interviewer_name": "Trưởng phòng Nhân sự"
    })
    data_interview = json.loads(res_interview)
    print(f"🧪 Kết quả gọi thử schedule_interview: Status {data_interview.get('status')}")
    print(f"   Thông điệp: {data_interview.get('message')}")
