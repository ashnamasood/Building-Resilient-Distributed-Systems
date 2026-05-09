ashna bscs23058

# Building-Resilient-Distributed-Systems

Project overview

- This repository is a minimal FastAPI demo for the StudySync bugfix assignment (Part 3).
- I implemented a fault-tolerance fix for Problem 3 (external LLM timeouts) using an
	async timeout + an in-memory circuit breaker and added a required middleware header
	`X-Student-ID: bscs23058` on every response.

What this repo contains

- `main.py` — FastAPI app with three demo endpoints:
	- `GET /broken` — intentionally blocks the event loop (bad behavior).
	- `GET /fixed` — uses `asyncio.wait_for` and a circuit breaker to fail fast (good behavior).
	- `GET /breaker-status` — inspect the circuit-breaker state.
- `test_fail.py` — demo script that issues two concurrent requests to `/broken` and `/fixed`
	and prints timings and the `X-Student-ID` header.

Quick start (recommended: use a virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" requests
```

Start the server

```bash
# preferred if uvicorn is on PATH
uvicorn main:app --reload

# or use the module form
python -m uvicorn main:app --reload
```

Run the demo script (in a separate terminal)

```bash
python test_fail.py
```

What to expect

- `/broken` will block the server (requests take a long time). The demo prints long
	elapsed times for both concurrent requests.
- `/fixed` returns quickly with a 502 fallback when the LLM call times out (default
	timeout=3s). The circuit breaker prevents repeated long waits.
- Every response includes the header `X-Student-ID: bscs23058` (required for submission).

Quick curl examples

```bash
curl -i http://127.0.0.1:8000/broken
curl -i http://127.0.0.1:8000/fixed
curl -i http://127.0.0.1:8000/breaker-status
```

Recording the demo (2 minutes max)

1. Start the server with `uvicorn main:app --reload`.
2. Record your screen and run `python test_fail.py` to show `/broken` first, then `/fixed`.
3. Narrate briefly: show blocked behavior, then show fast failure and header presence.
4. Stop recording and save as MP4 (or upload as unlisted YouTube/Loom).

Grading checklist (Part 3 requirements)

- Custom middleware header: every response contains `X-Student-ID: bscs23058` — YES.
- Implements a distributed pattern: uses a Circuit Breaker + timeout for fault tolerance — YES.
- Test/demo: `test_fail.py` triggers the failure and shows before/after — YES.
- README first line: contains my Name and Student ID — YES (this line).

Repository naming

- When you push to GitHub, name your repo exactly: `PDC-Sp24-[Your-ID]-[Your-LastName]`.

If you want, I can:

- prepare a short script for your 2-minute screencast (what to say and which commands to run);
- create a `requirements.txt` or `pyproject.toml` and commit it for easier installs;
- help you create the GitHub repository and push these files (you'll need to provide remote access).

Contact / Author

- ashna (bscs23058)