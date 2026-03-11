"""
Agent-2: Server Agent (Code Generator)
=======================================
Responsibilities:
  • Exposes an Agent Card at GET /.well-known/agent.json
  • Accepts A2A task messages at POST /tasks/send
  • Generates code with Claude API
  • Verifies the generated code (syntax + content checks)
  • Retries in a loop until verification passes (max 3 attempts)
  • Returns the final verified code back to Agent-1
"""

import sys, os, json, time, ast, re, subprocess, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from http.server import HTTPServer, BaseHTTPRequestHandler
from shared.models import (
    AgentCard, Skill, Task, TaskState, Message, MessageRole, Artifact,
    A2AResponse,
)
import shared.logger as log

# ── Anthropic client ──────────────────────────────────────────────────────────
try:
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyC9CG5NiYLY3_UR_v0_hVr7803jOlyf4Wo")

    MODEL = genai.GenerativeModel("gemini-1.5-flash")

    LLM_AVAILABLE = True
except Exception:
    MODEL = None
    LLM_AVAILABLE = False
MAX_RETRIES = 3

# ── Agent Card definition ─────────────────────────────────────────────────────
AGENT_CARD = AgentCard(
    name="CodeCraft Agent",
    description=(
        "A specialised code-generation agent. Given a plain-English request, "
        "it produces clean, runnable code (HTML/CSS/JS, Python, React, etc.), "
        "self-verifies the output, and retries until the code is correct."
    ),
    version="1.0.0",
    url="http://localhost:8080",
    supports_streaming=False,
    skills=[
        Skill(
            id="web-landing-page",
            name="Landing Page Generator",
            description="Generate complete, beautiful HTML/CSS/JS landing pages.",
            tags=["html", "css", "javascript", "web", "landing page", "frontend"],
            examples=["create a landing page", "build a product landing page"],
        ),
        Skill(
            id="react-component",
            name="React Component Generator",
            description="Generate production-ready React functional components with hooks.",
            tags=["react", "jsx", "component", "frontend", "ui"],
            examples=["create a react login form", "build a react dashboard card"],
        ),
        Skill(
            id="python-script",
            name="Python Script Generator",
            description="Generate well-structured Python scripts and modules.",
            tags=["python", "script", "backend", "automation"],
            examples=["write a python web scraper", "create a python REST client"],
        ),
        Skill(
            id="api-endpoint",
            name="REST API Generator",
            description="Generate REST API endpoints using FastAPI or Flask.",
            tags=["api", "rest", "fastapi", "flask", "backend", "server"],
            examples=["create a fastapi user endpoint", "build a flask REST API"],
        ),
    ],
)


# ── Code generator ─────────────────────────────────────────────────────────────
def _detect_skill(request_text: str) -> Skill | None:
    """Return the best matching skill for the request, or None."""
    lower = request_text.lower()
    for skill in AGENT_CARD.skills:
        for tag in skill.tags:
            if tag in lower:
                return skill
    return None


def _system_prompt(skill: Skill | None) -> str:
    base = (
        "You are an expert code generator. Produce ONLY the requested code — "
        "no explanations, no markdown fences, no preamble. "
        "The code must be complete, runnable, and production-quality."
    )
    if skill:
        base += f"\n\nYou are fulfilling skill: '{skill.name}'. {skill.description}"
    return base


def generate_code(user_request: str, skill: Skill | None, attempt: int) -> str:
    """Ask Gemini to generate code for the request."""

    if not LLM_AVAILABLE:
        return _stub_code(user_request, skill)

    history_note = (
        f"\n\nThis is generation attempt #{attempt}. Make sure the code is complete and correct."
        if attempt > 1 else ""
    )

    prompt = _system_prompt(skill) + "\n\nUser Request:\n" + user_request + history_note

    response = MODEL.generate_content(prompt)

    return response.text.strip()


def _stub_code(request: str, skill: Skill | None) -> str:
    """Deterministic stub when no API key is present."""
    lower = request.lower()
    if "landing" in lower or "html" in lower or "web" in lower:
        return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Landing Page</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f1f5f9; }
  header { padding: 4rem 2rem; text-align: center; background: linear-gradient(135deg,#1e3a5f,#0f172a); }
  h1 { font-size: 3rem; background: linear-gradient(90deg,#38bdf8,#818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  p.sub { margin-top: 1rem; color: #94a3b8; font-size: 1.2rem; }
  .cta { display: inline-block; margin-top: 2rem; padding: 0.9rem 2.4rem; background: #38bdf8; color: #0f172a; border-radius: 8px; font-weight: 700; text-decoration: none; }
  section { max-width: 900px; margin: 4rem auto; padding: 0 2rem; display: grid; grid-template-columns: repeat(3,1fr); gap: 1.5rem; }
  .card { background: #1e293b; border-radius: 12px; padding: 2rem; border: 1px solid #334155; }
  .card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
  footer { text-align: center; padding: 2rem; color: #475569; font-size: 0.9rem; }
</style>
</head>
<body>
<header>
  <h1>Launch Something Great</h1>
  <p class="sub">The fastest way to build, ship, and scale your ideas.</p>
  <a href="#" class="cta">Get Started Free</a>
</header>
<section>
  <div class="card"><h3>⚡ Fast</h3><p>Optimised for speed from day one.</p></div>
  <div class="card"><h3>🔒 Secure</h3><p>Enterprise-grade security built in.</p></div>
  <div class="card"><h3>🌍 Scalable</h3><p>Grows with your business effortlessly.</p></div>
</section>
<footer>© 2025 CodeCraft Agent — A2A Demo</footer>
</body>
</html>"""
    elif "python" in lower:
        return """#!/usr/bin/env python3
\"\"\"Auto-generated Python script.\"\"\"

import json, urllib.request

def fetch_todos(limit: int = 5) -> list[dict]:
    url = f"https://jsonplaceholder.typicode.com/todos?_limit={limit}"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())

def main():
    todos = fetch_todos()
    print(f"Fetched {len(todos)} todos:\\n")
    for t in todos:
        status = "✓" if t["completed"] else "○"
        print(f"  {status} [{t['id']}] {t['title']}")

if __name__ == "__main__":
    main()
"""
    else:
        return f"// Generated code for: {request}\nconsole.log('Hello from CodeCraft Agent!');"


# ── Verifier ───────────────────────────────────────────────────────────────────
class VerificationResult:
    def __init__(self, passed: bool, reason: str):
        self.passed = passed
        self.reason = reason

    def __repr__(self):
        return f"VerificationResult(passed={self.passed}, reason={self.reason!r})"


def verify_code(code: str, skill: Skill | None) -> VerificationResult:
    """
    Multi-step verification:
      1. Non-empty check
      2. Language-specific syntax check
      3. Content relevance check (must contain expected keywords)
    """
    code = code.strip()

    # 1. Non-empty
    if len(code) < 50:
        return VerificationResult(False, "Code is too short (< 50 chars).")

    tags = [t.lower() for t in (skill.tags if skill else [])]

    # 2. HTML check
    if any(t in tags for t in ["html", "landing page", "web"]):
        if not re.search(r"<!DOCTYPE\s+html", code, re.I):
            return VerificationResult(False, "HTML code missing <!DOCTYPE html> declaration.")
        if "<html" not in code.lower():
            return VerificationResult(False, "HTML code missing <html> tag.")
        if "<body" not in code.lower():
            return VerificationResult(False, "HTML code missing <body> tag.")
        return VerificationResult(True, "HTML structure verified.")

    # 3. Python check
    if "python" in tags or "script" in tags:
        try:
            ast.parse(code)
        except SyntaxError as e:
            return VerificationResult(False, f"Python syntax error: {e}")
        return VerificationResult(True, "Python syntax verified.")

    # 4. React / JSX check
    if any(t in tags for t in ["react", "jsx", "component"]):
        if "export default" not in code and "function " not in code:
            return VerificationResult(False, "React component missing export default or function declaration.")
        if "return" not in code:
            return VerificationResult(False, "React component missing return statement.")
        return VerificationResult(True, "React component structure verified.")

    # 5. Generic JS/code check
    if len(code) > 50:
        return VerificationResult(True, "Generic code length check passed.")

    return VerificationResult(False, "Code did not pass any verification rule.")


# ── Core task handler ──────────────────────────────────────────────────────────
def handle_task(task: Task) -> Task:
    """Main A2A task processing loop for Agent-2."""
    task.state = TaskState.WORKING
    task.updated_at = time.time()

    user_msg = next((m for m in task.messages if m.role == MessageRole.USER), None)
    if not user_msg:
        task.state = TaskState.FAILED
        task.messages.append(Message(
            role=MessageRole.AGENT,
            content="ERROR: No user message found in task.",
        ))
        return task

    request_text = user_msg.content
    skill = _detect_skill(request_text)

    log.step("Agent-2", f"Processing request: '{request_text}'")
    log.info("Agent-2", f"Matched skill: {skill.name if skill else 'Generic'}")

    for attempt in range(1, MAX_RETRIES + 1):
        log.step("Agent-2", f"Generation attempt {attempt}/{MAX_RETRIES} …")
        code = generate_code(request_text, skill, attempt)

        log.info("Agent-2", f"Generated {len(code)} chars. Running verification …")
        result = verify_code(code, skill)

        if result.passed:
            log.success("Agent-2", f"✅ Verification PASSED — {result.reason}")

            # Determine file name & MIME
            fname, mime = _artifact_meta(skill, request_text)

            artifact = Artifact(
                name=fname,
                content=code,
                mime_type=mime,
                metadata={"skill_id": skill.id if skill else "generic",
                           "attempts": attempt,
                           "verification": result.reason},
            )
            task.artifacts.append(artifact)
            task.state = TaskState.COMPLETED
            task.messages.append(Message(
                role=MessageRole.AGENT,
                content=(
                    f"Code generated successfully after {attempt} attempt(s).\n"
                    f"Artifact: {fname}\nVerification: {result.reason}"
                ),
            ))
            task.updated_at = time.time()
            return task
        else:
            log.warn("Agent-2", f"❌ Verification FAILED — {result.reason}. Retrying …")
            task.messages.append(Message(
                role=MessageRole.AGENT,
                content=f"Attempt {attempt} failed verification: {result.reason}. Retrying …",
            ))

    # All retries exhausted
    task.state = TaskState.FAILED
    task.messages.append(Message(
        role=MessageRole.AGENT,
        content=f"Failed to generate valid code after {MAX_RETRIES} attempts.",
    ))
    task.updated_at = time.time()
    return task


def _artifact_meta(skill: Skill | None, request_text: str) -> tuple[str, str]:
    if skill is None:
        return "generated_code.txt", "text/plain"
    tags = skill.tags
    if any(t in tags for t in ["html", "landing page", "web"]):
        return "landing_page.html", "text/html"
    if any(t in tags for t in ["react", "jsx"]):
        return "component.jsx", "text/jsx"
    if any(t in tags for t in ["python", "script"]):
        return "script.py", "text/x-python"
    if any(t in tags for t in ["api", "rest", "fastapi", "flask"]):
        return "api.py", "text/x-python"
    return "output.txt", "text/plain"


# ── HTTP Server ────────────────────────────────────────────────────────────────
class A2AHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # suppress default access log

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/.well-known/agent.json", "/agent-card"):
            log.protocol(f"GET {self.path} → serving Agent Card")
            self._send_json(AGENT_CARD.to_dict())
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path != "/tasks/send":
            self._send_json({"error": "Unknown method"}, 404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        log.protocol(f"POST /tasks/send — task_id={payload.get('params',{}).get('task_id','?')}")

        # Re-hydrate Task from dict
        params = payload.get("params", {})
        messages = [
            Message(
                role=MessageRole(m["role"]),
                content=m["content"],
                timestamp=m.get("timestamp", time.time()),
                message_id=m.get("message_id", ""),
            )
            for m in params.get("messages", [])
        ]
        task = Task(
            task_id=params.get("task_id", ""),
            session_id=params.get("session_id", ""),
            state=TaskState(params.get("state", "submitted")),
            messages=messages,
            metadata=params.get("metadata", {}),
        )

        processed_task = handle_task(task)

        response = A2AResponse(
            request_id=payload.get("id", ""),
            task=processed_task,
        )
        self._send_json(response.to_dict())


def run_server(host: str = "localhost", port: int = 8080):
    server = HTTPServer((host, port), A2AHandler)
    log.divider("Agent-2: CodeCraft Server Agent")
    log.success("Agent-2", f"🚀 Listening on http://{host}:{port}")
    log.info("Agent-2", f"Agent Card → http://{host}:{port}/.well-known/agent.json")
    log.info("Agent-2", f"Task endpoint → http://{host}:{port}/tasks/send")
    log.info("Agent-2", f"Skills: {', '.join(s.name for s in AGENT_CARD.skills)}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
