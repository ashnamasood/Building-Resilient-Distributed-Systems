import requests
import threading
import time


def run_concurrent(path):
    url = f"http://127.0.0.1:8000{path}"

    def worker(idx, results):
        start = time.perf_counter()
        try:
            r = requests.get(url)
            elapsed = time.perf_counter() - start
            results[idx] = (r.status_code, r.text, r.headers.get("X-Student-ID"), elapsed)
        except Exception as e:
            elapsed = time.perf_counter() - start
            results[idx] = (None, str(e), None, elapsed)

    results = [None, None]
    t1 = threading.Thread(target=worker, args=(0, results))
    t2 = threading.Thread(target=worker, args=(1, results))

    t1.start(); time.sleep(0.05); t2.start()
    t1.join(); t2.join()

    for i, r in enumerate(results):
        print(f"Request {i}: status={r[0]} header=X-Student-ID={r[2]} elapsed={r[3]:.2f}s body={r[1][:200]}")


if __name__ == '__main__':
    print("Testing /broken (will block the server):")
    run_concurrent('/broken')

    print('\nTesting /fixed (timeout + circuit breaker):')
    run_concurrent('/fixed')