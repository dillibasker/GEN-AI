# A2A Protocol Demo — Agent-to-Agent Code Generation

A complete, runnable demonstration of the **Agent-to-Agent (A2A) protocol** featuring two autonomous agents collaborating to generate, verify, and deliver code.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        A2A WORKFLOW                          │
│                                                              │
│  User Request                                                │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────────────┐                            │
│  │   Agent-1 (Client Agent)    │                            │
│  │   agent1_client/            │                            │
│  │   • Receives user request   │                            │
│  │   • Fetches Agent Card      │◄──── GET /.well-known/ ───┐│
│  │   • Matches skills          │                            ││
│  │   • Sends A2A task          │──── POST /tasks/send ────►││
│  │   • Saves artifacts         │◄─── Response (task+code)──┘│
│  └─────────────────────────────┘                            │
│                                         │                    │
│                              ┌──────────┴──────────────┐    │
│                              │  Agent-2 (Server Agent)  │    │
│                              │  agent2_server/          │    │
│                              │  • Exposes Agent Card    │    │
│                              │  • Accepts A2A tasks     │    │
│                              │  • Generates code (LLM)  │    │
│                              │  • Verifies code         │    │
│                              │  • Retries on failure    │    │
│                              │  • Returns artifact      │    │
│                              └──────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
a2a-protocol/
├── run_demo.py                  # ← START HERE: demo runner
│
├── agent1_client/
│   └── client_agent.py         # Agent-1: orchestrator / client
│
├── agent2_server/
│   └── server_agent.py         # Agent-2: code generator / server
│
├── shared/
│   ├── models.py               # A2A protocol data models
│   └── logger.py               # Pretty coloured logger
│
├── output_codes/               # Generated artifacts appear here
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key (optional but recommended)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

> Without an API key the demo still runs using built-in stub responses so
> you can explore the A2A protocol flow without any cloud calls.

### 3. Run the demo

```bash
python run_demo.py
```

This starts Agent-2, then runs Agent-1 through **three demo requests**:
- A SaaS landing page (HTML/CSS/JS)
- A Python weather-fetching script
- A React user profile card component

### 4. Custom request

```bash
python run_demo.py "create a landing page for my coffee shop"
python run_demo.py "write a python script to parse CSV files"
```

### 5. Run agents separately (two terminals)

**Terminal 1 — Start Agent-2:**
```bash
python agent2_server/server_agent.py
```

**Terminal 2 — Run Agent-1:**
```bash
python agent1_client/client_agent.py "create a react login form"
```

---

## A2A Protocol Details

### Agent Card

Agent-2 exposes its capabilities at `GET /.well-known/agent.json`:

```json
{
  "name": "CodeCraft Agent",
  "version": "1.0.0",
  "protocol_version": "1.0",
  "skills": [
    {
      "id": "web-landing-page",
      "name": "Landing Page Generator",
      "tags": ["html", "css", "javascript", "landing page"]
    },
    ...
  ]
}
```

### A2A Task Message

Agent-1 sends tasks via `POST /tasks/send` using JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "id": "<request-id>",
  "params": {
    "task_id": "<uuid>",
    "state": "submitted",
    "messages": [
      { "role": "user", "content": "create a landing page" }
    ]
  }
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "id": "<request-id>",
  "result": {
    "state": "completed",
    "artifacts": [
      {
        "name": "landing_page.html",
        "mime_type": "text/html",
        "content": "<!DOCTYPE html>...",
        "metadata": { "attempts": 1, "verification": "HTML structure verified." }
      }
    ]
  }
}
```

---

## Verification Loop (Agent-2)

```
generate_code(request)
      │
      ▼
verify_code(code)
      │
   passed?──Yes──► return artifact
      │
      No
      │
  attempt < MAX_RETRIES?──No──► return FAILED task
      │
      Yes
      │
      └──► generate_code(request, attempt+1)  [loop]
```

Verification checks (per skill type):
| Skill        | Checks                                                  |
|--------------|---------------------------------------------------------|
| HTML/Web     | `<!DOCTYPE html>`, `<html>`, `<body>` presence          |
| Python       | `ast.parse()` — actual syntax validation                |
| React/JSX    | `export default` + `function` + `return` present        |
| Generic      | Minimum length (50 chars)                               |

---

## Output

Generated files are saved in `output_codes/`:
- `landing_page.html` — open in any browser
- `script.py` — run with `python script.py`
- `component.jsx` — use in any React project

---

## Supported Skills

| Skill                 | Example Requests                             |
|-----------------------|----------------------------------------------|
| Landing Page          | "create a landing page for …"               |
| React Component       | "create a react login form"                  |
| Python Script         | "write a python script to …"                |
| REST API              | "create a fastapi user endpoint"             |

---

## Key Files

| File | Purpose |
|------|---------|
| `shared/models.py` | `AgentCard`, `Skill`, `Task`, `Message`, `Artifact`, `A2ARequest`, `A2AResponse` |
| `agent2_server/server_agent.py` | HTTP server, code gen, verifier, retry loop |
| `agent1_client/client_agent.py` | Agent Card fetch, skill match, task send, response handle |
| `run_demo.py` | End-to-end orchestration, starts both agents |
