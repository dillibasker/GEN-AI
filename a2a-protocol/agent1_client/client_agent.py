"""
Agent-1: Client Agent (Orchestrator)
======================================
Responsibilities:
  1. Receive user request
  2. Fetch Agent-2's Agent Card
  3. Match request against declared skills
  4. Build and send an A2A Task message to Agent-2
  5. Receive & display the completed task + artifacts
  6. Save generated artifacts to disk
"""

import sys, os, json, time, urllib.request, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.models import (
    AgentCard, Skill, Task, TaskState, Message, MessageRole, A2ARequest,
)
import shared.logger as log

AGENT2_BASE_URL = "http://localhost:8080"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output_codes")


# ── Step 1: Fetch Agent Card ───────────────────────────────────────────────────
def fetch_agent_card(base_url: str) -> AgentCard:
    log.step("Agent-1", f"Fetching Agent Card from {base_url}/.well-known/agent.json")
    try:
        with urllib.request.urlopen(f"{base_url}/.well-known/agent.json", timeout=5) as r:
            data = json.loads(r.read())
            card = AgentCard.from_dict(data)
            log.success("Agent-1", f"Agent Card received: '{card.name}' v{card.version}")
            log.info("Agent-1", f"Available skills: {', '.join(s.name for s in card.skills)}")
            return card
    except urllib.error.URLError as e:
        log.error("Agent-1", f"Cannot reach Agent-2: {e}")
        raise ConnectionError(f"Agent-2 not reachable at {base_url}") from e


# ── Step 2: Skill matching ─────────────────────────────────────────────────────
def match_skill(user_request: str, card: AgentCard) -> Skill | None:
    """
    Simple keyword-based skill matching.
    Returns the best matching Skill or None if no match.
    """
    lower = user_request.lower()
    best_skill = None
    best_score = 0

    for skill in card.skills:
        score = 0
        for tag in skill.tags:
            if tag in lower:
                score += 1
        for example in skill.examples:
            # partial overlap scoring
            example_words = set(example.lower().split())
            request_words = set(lower.split())
            overlap = len(example_words & request_words)
            score += overlap * 0.5

        if score > best_score:
            best_score = score
            best_skill = skill

    if best_skill and best_score > 0:
        log.success("Agent-1", f"Skill match → '{best_skill.name}' (score={best_score:.1f})")
        return best_skill

    log.warn("Agent-1", "No specific skill matched — request may be unsupported.")
    return None


# ── Step 3: Build & send A2A task ─────────────────────────────────────────────
def send_task(user_request: str, skill: Skill | None) -> dict:
    task = Task(
        metadata={"skill_id": skill.id if skill else None,
                  "client_agent": "Agent-1"},
        messages=[
            Message(role=MessageRole.USER, content=user_request)
        ],
    )

    request = A2ARequest(method="tasks/send", task=task)
    payload = json.dumps(request.to_dict()).encode()

    log.protocol(f"Sending A2A task  task_id={task.task_id}")
    log.protocol(f"Method: {request.method}")
    log.protocol(f"Payload size: {len(payload)} bytes")

    req = urllib.request.Request(
        f"{AGENT2_BASE_URL}/tasks/send",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            response_data = json.loads(r.read())
            log.protocol("Response received from Agent-2")
            return response_data
    except urllib.error.HTTPError as e:
        body = e.read()
        log.error("Agent-1", f"HTTP {e.code}: {body}")
        raise
    except urllib.error.URLError as e:
        log.error("Agent-1", f"Network error: {e}")
        raise


# ── Step 4: Handle response ────────────────────────────────────────────────────
def handle_response(response: dict) -> list[str]:
    """Parse response, display result, save artifacts. Returns saved file paths."""
    if "error" in response:
        log.error("Agent-1", f"Agent-2 returned error: {response['error']}")
        return []

    result = response.get("result", {})
    state = result.get("state", "unknown")
    messages = result.get("messages", [])
    artifacts = result.get("artifacts", [])

    log.divider("Task Result")
    log.info("Agent-1", f"Task state: {state.upper()}")

    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "agent":
            log.success("Agent-2", f"📩 {content}")

    saved_paths = []
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for artifact in artifacts:
        fname = artifact.get("name", "output.txt")
        content = artifact.get("content", "")
        meta = artifact.get("metadata", {})

        out_path = os.path.join(OUTPUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

        saved_paths.append(out_path)
        log.success("Agent-1",
                     f"💾 Artifact saved → output_codes/{fname}  "
                     f"({len(content)} chars, {meta.get('attempts',1)} attempt(s))")

    return saved_paths


# ── Public API ─────────────────────────────────────────────────────────────────
def run(user_request: str):
    log.divider("Agent-1: Client Agent")
    log.info("Agent-1", f"User request: \"{user_request}\"")

    # Step 1 — Get Agent Card
    card = fetch_agent_card(AGENT2_BASE_URL)

    # Step 2 — Match skill
    skill = match_skill(user_request, card)

    if skill is None:
        log.warn("Agent-1",
                 "Request does not match any declared skill. "
                 "Proceeding anyway as generic code generation.")

    # Step 3 — Send A2A task
    log.step("Agent-1", "Sending A2A task to Agent-2 …")
    response = send_task(user_request, skill)

    # Step 4 — Handle response
    paths = handle_response(response)

    if paths:
        log.divider("Done")
        log.success("Agent-1", "✅ Workflow complete. Generated files:")
        for p in paths:
            log.info("", f"   → {os.path.abspath(p)}")
    else:
        log.error("Agent-1", "Workflow ended with no generated artifacts.")

    return paths


# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client_agent.py \"<user request>\"")
        sys.exit(1)

    user_request = " ".join(sys.argv[1:])
    run(user_request)
