"""
A2A Protocol Demo — Main Runner
================================
Starts Agent-2 (server) in a background thread, then runs Agent-1 (client)
for one or more demo requests, showing the full A2A workflow end-to-end.

Usage:
    python run_demo.py                         # Run default demo requests
    python run_demo.py "create a landing page" # Run a single custom request
"""

import sys, os, time, threading, argparse

sys.path.insert(0, os.path.dirname(__file__))
import shared.logger as log

# ─────────────────────────────────────────────────────────────────────────────
DEMO_REQUESTS = [
    "create a landing page for a SaaS product called NovaDeploy",
    "write a python script that fetches and displays weather data",
    "create a react component for a user profile card",
]


def start_server():
    """Launch Agent-2 in a daemon thread."""
    from agent2_server.server_agent import run_server
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1.2)  # give the server a moment to bind
    return t


def wait_for_server(host="localhost", port=8080, retries=10):
    import urllib.request, urllib.error
    for i in range(retries):
        try:
            urllib.request.urlopen(f"http://{host}:{port}/.well-known/agent.json", timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def run_workflow(request: str) -> list[str]:
    from agent1_client.client_agent import run
    return run(request)


def main():
    parser = argparse.ArgumentParser(description="A2A Protocol Demo")
    parser.add_argument("request", nargs="*",
                        help="User request(s). If omitted, runs all demo requests.")
    args = parser.parse_args()

    log.divider("A2A Protocol Demo")
    log.info("Demo", "Initialising Agent-to-Agent workflow …")
    log.info("Demo", "Agent-1 = Client/Orchestrator Agent")
    log.info("Demo", "Agent-2 = CodeCraft Server Agent (code generation + verification)")

    # Start Agent-2
    log.step("Demo", "Starting Agent-2 server …")
    start_server()

    if not wait_for_server():
        log.error("Demo", "Agent-2 failed to start. Aborting.")
        sys.exit(1)
    log.success("Demo", "Agent-2 is online ✓")

    requests_to_run = args.request if args.request else DEMO_REQUESTS

    all_outputs = []
    for idx, req in enumerate(requests_to_run, 1):
        log.divider(f"Request {idx}/{len(requests_to_run)}")
        paths = run_workflow(req)
        all_outputs.extend(paths)
        if idx < len(requests_to_run):
            time.sleep(0.5)

    log.divider("All Workflows Complete")
    if all_outputs:
        log.success("Demo", f"Generated {len(all_outputs)} artifact(s):")
        for p in all_outputs:
            log.info("", f"   📄 {os.path.abspath(p)}")
    else:
        log.warn("Demo", "No artifacts were produced.")


if __name__ == "__main__":
    main()
