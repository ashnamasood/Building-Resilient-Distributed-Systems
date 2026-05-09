ashna bscs23058

# Building-Resilient-Distributed-Systems

Run instructions:

- Install dependencies:

```bash
python -m pip install fastapi uvicorn requests
```

- Start the server:

```bash
uvicorn main:app --reload
```

- In another terminal run the demo script:

```bash
python test_fail.py
```

The demo will run two concurrent requests against `/broken` (which blocks the server) and
then two concurrent requests against `/fixed` (which uses a timeout + circuit breaker). Every
response includes the required header `X-Student-ID: bscs23058`.