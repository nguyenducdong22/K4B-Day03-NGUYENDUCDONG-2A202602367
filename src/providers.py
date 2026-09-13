"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        prompt_lower = prompt.lower()
        if "quy trình" in prompt_lower or "tuyển dụng" in prompt_lower or "sàng lọc" in prompt_lower:
            return "[Mock Chatbot Response]: Xin chào! Quy trình tuyển dụng của công ty bao gồm 3 vòng: (1) Sàng lọc hồ sơ CV, (2) Phỏng vấn chuyên môn kỹ thuật, (3) Phỏng vấn văn hóa và thỏa thuận Offer. (Chế độ Chatbot không có Tool tra cứu dữ liệu thời gian thực)."
        return f"[Mock Chatbot Response]: Xin chào! Tôi đã nhận được câu hỏi '{prompt}'. (Chế độ Chatbot không có Tool tra cứu dữ liệu thời gian thực)."

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        
        # 1. Direct query: Quy trình tuyển dụng chung (TC01)
        if ("quy trình" in prompt_lower or "giới thiệu" in prompt_lower) and "uv2026" not in prompt_lower:
            return {
                "type": "text",
                "content": "[Mock Agent Response]: Xin chào! Quy trình tuyển dụng của công ty bao gồm 3 vòng: (1) Sàng lọc hồ sơ CV dựa trên tiêu chí chuyên môn, (2) Phỏng vấn năng lực kỹ thuật với chuyên gia, (3) Phỏng vấn văn hóa và thỏa thuận Offer.",
                "thought": "Câu hỏi chung về quy trình tuyển dụng và tiêu chí công ty, trả lời trực tiếp từ kiến thức nền tảng mà không cần gọi Tool."
            }
        # 2. Edge case: Tra cứu mã không tồn tại (UV9999999 / SV9999999) - TC05
        elif "uv9999999" in prompt_lower or "sv9999999" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "candidate_query",
                "arguments": {"candidate_id": "UV9999999"},
                "thought": "Người dùng yêu cầu tra cứu hồ sơ ứng viên có mã UV9999999. Tôi sẽ gọi tool candidate_query để kiểm tra dữ liệu."
            }
        # 3. Multi-step reasoning: Kiểm tra hồ sơ rồi lên lịch phỏng vấn (TC04)
        elif ("uv2026001" in prompt_lower or "ứng viên" in prompt_lower) and ("phỏng vấn" in prompt_lower or "đặt lịch" in prompt_lower or "thông báo" in prompt_lower) and ("25/09/2026" in prompt_lower):
            return {
                "type": "tool_call",
                "tool_name": "schedule_interview",
                "arguments": {"candidate_id": "UV2026001", "datetime_str": "09:00 25/09/2026", "interviewer_name": "Trưởng phòng Nhân sự"},
                "thought": "Hồ sơ ứng viên UV2026001 đã đạt chuẩn sàng lọc. Tôi sẽ gọi công cụ schedule_interview để gửi thông báo mời phỏng vấn vào lúc 09:00 ngày 25/09/2026."
            }
        # 4. Booking appointment / schedule interview (TC03)
        elif ("uv2026001" in prompt_lower or "ứng viên" in prompt_lower) and ("phỏng vấn" in prompt_lower or "đặt lịch" in prompt_lower or "thông báo" in prompt_lower):
            return {
                "type": "tool_call",
                "tool_name": "schedule_interview",
                "arguments": {"candidate_id": "UV2026001", "datetime_str": "14:00 20/09/2026", "interviewer_name": "Trưởng phòng Nhân sự"},
                "thought": "Người dùng yêu cầu gửi thông báo lịch phỏng vấn cho ứng viên UV2026001. Tôi sẽ gọi tool schedule_interview."
            }
        # 5. Single tool query: Tra cứu hồ sơ ứng viên (TC02)
        elif "uv2026001" in prompt_lower or ("tra cứu" in prompt_lower and "hồ sơ" in prompt_lower):
            return {
                "type": "tool_call",
                "tool_name": "candidate_query",
                "arguments": {"candidate_id": "UV2026001"},
                "thought": "Người dùng muốn tra cứu thông tin hồ sơ và kết quả sàng lọc của ứng viên UV2026001. Tôi sẽ gọi tool candidate_query."
            }
        # 6. Tương thích sinh viên (SV2026001)
        elif "sv2026001" in prompt_lower and "đặt lịch" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "schedule_appointment",
                "arguments": {"student_id": "SV2026001", "datetime_str": "14:00 15/09/2026", "advisor_name": "PGS.TS Nguyễn Văn A"},
                "thought": "Người dùng yêu cầu đặt lịch hẹn tư vấn cho sinh viên SV2026001. Tôi sẽ gọi tool schedule_appointment."
            }
        elif "sv2026001" in prompt_lower or "tra cứu" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "academic_query",
                "arguments": {"student_id": "SV2026001"},
                "thought": "Người dùng muốn tra cứu thông tin học vụ của sinh viên SV2026001. Tôi sẽ gọi tool academic_query."
            }
        # 7. Fallback direct text
        else:
            return {
                "type": "text",
                "content": "[Mock Agent Response]: Xin chào! Quy trình tuyển dụng của công ty bao gồm 3 vòng: (1) Sàng lọc hồ sơ CV, (2) Phỏng vấn chuyên môn kỹ thuật, (3) Phỏng vấn văn hóa và thỏa thuận Offer.",
                "thought": "Câu hỏi chung về quy trình tuyển dụng và tiêu chí công ty, trả lời trực tiếp từ kiến thức nền tảng mà không cần gọi Tool."
            }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class GroqProvider(BaseLLMProvider):
    """Groq Provider (Tốc độ siêu nhanh, tương thích hoàn toàn chuẩn OpenAI API)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "openai/gpt-oss-120b"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key:
            return "[Groq Error]: Chưa cấu hình GROQ_API_KEY trong file .env!"
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=750
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[Lỗi gọi Groq LLM {self.model_name}]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key:
            return {
                "type": "text",
                "content": "[Groq Error]: Chưa tìm thấy GROQ_API_KEY trong .env.",
                "thought": "Chưa có API Key để kết nối mô hình LLM thật."
            }

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                max_tokens=750
            )

            msg = response.choices[0].message
            reasoning = getattr(msg, "reasoning", None) or getattr(msg, "reasoning_content", None) or ""

            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                thought_msg = reasoning if reasoning else f"Mô hình LLM ({self.model_name}) quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": thought_msg
                }
            else:
                thought_msg = reasoning if reasoning else f"Mô hình LLM ({self.model_name}) suy luận và phản hồi trực tiếp (không cần gọi công cụ)."
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": thought_msg
                }
        except Exception as e:
            print(f"❌ [Groq API Error]: {str(e)}")
            return {
                "type": "text",
                "content": f"[Lỗi thực thi mô hình LLM ({self.model_name})]: {str(e)}",
                "thought": f"Gặp lỗi khi gọi mô hình LLM: {str(e)}"
            }


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "groq":
        key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        if key and key != "your_groq_api_key_here":
            return GroqProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
