"""
🌐 WEB UI DEMO - REACT RECRUITMENT AGENT (MCP ENHANCED)
Giao diện trực quan phục vụ thuyết trình Demo theo yêu cầu của Giảng viên Dudumi.
Chạy không cần cài thêm thư viện (dùng built-in http.server).
"""

import json
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Thêm đường dẫn src vào hệ thống
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from mcp_server import MCPAcademicServer
from providers import get_llm_provider
from app import run_react_agent, load_test_cases

provider = get_llm_provider()
mcp_server = MCPAcademicServer()

HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VinUni AI Demo - ReAct Recruitment Agent</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0f172a;
            --bg-card: #1e293b;
            --bg-chat: #090d16;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.2);
            --border: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --thought: #fbbf24;
            --action: #a855f7;
            --obs: #10b981;
            --final: #38bdf8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-main);
            color: var(--text);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        /* Sidebar */
        .sidebar {
            width: 340px;
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .logo h2 { font-size: 16px; font-weight: 700; color: #fff; }
        .logo p { font-size: 11px; color: var(--accent); }
        .info-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            font-size: 12px;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        .info-card strong { color: var(--accent); }
        .section-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 10px;
        }
        .quick-tests {
            display: flex;
            flex-direction: column;
            gap: 8px;
            overflow-y: auto;
            flex: 1;
        }
        .test-btn {
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px;
            color: var(--text);
            text-align: left;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .test-btn:hover {
            border-color: var(--accent);
            background: rgba(56, 189, 248, 0.1);
        }
        .test-badge {
            display: inline-block;
            background: #334155;
            color: var(--accent);
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            margin-bottom: 4px;
            font-weight: 600;
        }
        /* Chat Main */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-chat);
        }
        .chat-header {
            padding: 16px 24px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-header h1 { font-size: 17px; font-weight: 600; }
        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
        .chat-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .message-user {
            align-self: flex-end;
            background: #2563eb;
            color: #fff;
            padding: 12px 16px;
            border-radius: 12px 12px 2px 12px;
            max-width: 75%;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        .message-agent {
            align-self: flex-start;
            width: 100%;
            max-width: 88%;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px 12px 12px 2px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .react-step {
            border-left: 3px solid #38bdf8;
            padding-left: 12px;
            margin-bottom: 8px;
            font-size: 13px;
        }
        .react-step.thought { border-color: var(--thought); color: #fef08a; }
        .react-step.action { border-color: var(--action); color: #e9d5ff; font-family: monospace; background: rgba(168, 85, 247, 0.1); padding: 8px; border-radius: 4px; }
        .react-step.observation { border-color: var(--obs); color: #a7f3d0; font-family: monospace; background: rgba(16, 185, 129, 0.1); padding: 8px; border-radius: 4px; }
        .step-label { font-weight: 700; text-transform: uppercase; font-size: 11px; margin-bottom: 4px; display: block; }
        .final-answer {
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 8px;
            padding: 14px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #f8fafc;
        }
        .chat-input-area {
            padding: 16px 24px;
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            display: flex;
            gap: 12px;
        }
        .chat-input {
            flex: 1;
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 16px;
            color: #fff;
            font-size: 14px;
            outline: none;
            font-family: inherit;
        }
        .chat-input:focus { border-color: var(--accent); }
        .send-btn {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            border: none;
            border-radius: 8px;
            padding: 0 20px;
            color: #fff;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .send-btn:hover { opacity: 0.9; }
        .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="logo">
            <div class="logo-icon">🤖</div>
            <div>
                <h2>VinUni AI Agent</h2>
                <p>ReAct + MCP Screening</p>
            </div>
        </div>
        <div class="info-card">
            <strong>Học viên:</strong> Nguyễn Đức Đông<br>
            <strong>MSSV:</strong> 2A202602367<br>
            <strong>Mô hình:</strong> Groq (openai/gpt-oss-120b)<br>
            <strong>MCP Server:</strong> recruitment-screening
        </div>
        <div class="section-title">Test Cases mẫu (Click để Demo)</div>
        <div class="quick-tests">
            <button class="test-btn" onclick="sendPrompt('Chào bạn, bạn có thể giới thiệu quy trình sàng lọc hồ sơ CV và các tiêu chí tuyển dụng chung của công ty không?')">
                <span class="test-badge">TC01 - Direct Query</span><br>
                Quy trình sàng lọc hồ sơ & tiêu chí chung
            </button>
            <button class="test-btn" onclick="sendPrompt('Hãy tra cứu thông tin hồ sơ, điểm đánh giá CV và kết quả sàng lọc của ứng viên UV2026001.')">
                <span class="test-badge">TC02 - Tool Query</span><br>
                Tra cứu điểm CV ứng viên UV2026001
            </button>
            <button class="test-btn" onclick="sendPrompt('Hãy gửi thông báo mời phỏng vấn cho ứng viên UV2026001 vào lúc 14:00 ngày 20/09/2026 với người phỏng vấn Trưởng phòng Nhân sự.')">
                <span class="test-badge">TC03 - Appointment</span><br>
                Gửi thông báo & Đặt lịch phỏng vấn
            </button>
            <button class="test-btn" onclick="sendPrompt('Hãy kiểm tra thông tin của ứng viên UV2026001, xem ứng viên ứng tuyển vị trí nào và nếu kết quả sàng lọc CV đạt yêu cầu thì hãy gửi thông báo mời phỏng vấn vào lúc 09:00 ngày 25/09/2026.')">
                <span class="test-badge">TC04 - Multi-Step ReAct</span><br>
                Kiểm tra điều kiện rồi mới đặt lịch
            </button>
            <button class="test-btn" onclick="sendPrompt('Hãy tra cứu thông tin hồ sơ và kết quả sàng lọc CV của ứng viên có mã số UV9999999.')">
                <span class="test-badge">TC05 - Edge Case</span><br>
                Mã ứng viên không tồn tại (Anti-Hallucination)
            </button>
        </div>
    </div>

    <!-- Chat Container -->
    <div class="chat-container">
        <div class="chat-header">
            <div>
                <h1>Trợ lý Tuyển dụng & Sàng lọc CV (ReAct Agent)</h1>
                <span style="font-size: 12px; color: var(--text-muted);">Quan sát vòng lặp Thought ➔ Action ➔ Observation ➔ Final Answer thời gian thực</span>
            </div>
            <div class="status-pill">
                <div class="status-dot"></div>
                <span>LLM Live Connected</span>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message-agent">
                <div class="final-answer">
                    👋 <strong>Xin chào Thầy và các bạn!</strong><br>
                    Tôi là <strong>Trợ lý Tác tử Tuyển dụng & Sàng lọc CV</strong> xây dựng trên kiến trúc ReAct kết hợp chuẩn giao thức MCP Server.<br>
                    Bạn có thể chọn một trong các Test Cases mẫu bên trái hoặc nhập câu hỏi trực tiếp bên dưới để xem toàn bộ quá trình suy luận!
                </div>
            </div>
        </div>

        <div class="chat-input-area">
            <input type="text" id="userInput" class="chat-input" placeholder="Nhập câu hỏi tra cứu hồ sơ hoặc đặt lịch phỏng vấn..." onkeydown="if(event.key==='Enter') submitChat()">
            <button id="sendBtn" class="send-btn" onclick="submitChat()">Gửi câu hỏi</button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        function appendUserMessage(text) {
            const div = document.createElement('div');
            div.className = 'message-user';
            div.innerText = text;
            chatMessages.appendChild(div);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function appendAgentResponse(logs) {
            const container = document.createElement('div');
            container.className = 'message-agent';

            logs.forEach(log => {
                if (log.thought) {
                    const t = document.createElement('div');
                    t.className = 'react-step thought';
                    t.innerHTML = `<span class="step-label">🧠 THOUGHT (Suy luận):</span>${log.thought}`;
                    container.appendChild(t);
                }
                if (log.action_type === 'TOOL_EXECUTION') {
                    const act = document.createElement('div');
                    act.className = 'react-step action';
                    act.innerHTML = `<span class="step-label">🛠️ ACTION PROPOSED:</span>${log.tool_name}(${JSON.stringify(log.arguments)})`;
                    container.appendChild(act);

                    const obs = document.createElement('div');
                    obs.className = 'react-step observation';
                    obs.innerHTML = `<span class="step-label">👁️ OBSERVATION TỪ MCP SERVER:</span>${JSON.stringify(log.observation)}`;
                    container.appendChild(obs);
                }
                if (log.action_type === 'FINAL_ANSWER') {
                    const f = document.createElement('div');
                    f.className = 'final-answer';
                    f.innerHTML = `<strong>🏁 FINAL ANSWER:</strong><br><br>${log.output.replace(/\\n/g, '<br>')}`;
                    container.appendChild(f);
                }
            });

            chatMessages.appendChild(container);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendPrompt(text) {
            userInput.value = text;
            submitChat();
        }

        async function submitChat() {
            const query = userInput.value.trim();
            if (!query) return;

            appendUserMessage(query);
            userInput.value = '';
            userInput.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = 'Đang suy luận...';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                appendAgentResponse(data.logs);
            } catch (err) {
                alert('Lỗi kết nối Agent: ' + err);
            } finally {
                userInput.disabled = false;
                sendBtn.disabled = false;
                sendBtn.innerText = 'Gửi câu hỏi';
                userInput.focus();
            }
        }
    </script>
</body>
</html>
"""

class ReActRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                query = data.get("query", "")
                # Gọi trực tiếp ReAct Agent Loop
                logs = run_react_agent(query, provider, mcp_server)
                response_payload = json.dumps({"status": "SUCCESS", "logs": logs}, ensure_ascii=False)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(response_payload.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Ẩn bớt log request mặc định cho gọn terminal
        pass


def run_server(port=7860):
    server = HTTPServer(("localhost", port), ReActRequestHandler)
    print(f"\n========================================================")
    print(f"🚀 [VINUNI WEB UI DEMO] Sẵn sàng phục vụ thuyết trình!")
    print(f"🔗 Mở trình duyệt tại: http://localhost:{port}")
    print(f"========================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Đã dừng Web UI Server.")


if __name__ == "__main__":
    port = 7860
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
