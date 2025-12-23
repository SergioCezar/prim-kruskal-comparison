import time
import tracemalloc
import threading

def medir_execucao(func, *args, repeats=3, timeout=300):

    times = []
    mem_peaks = []
    last_value = None

    def run_target(storage):
        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            storage["value"] = func(*args)
            storage["error"] = None
        except Exception as e:
            storage["value"] = None
            storage["error"] = e
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        storage["time"] = t1 - t0
        storage["mem"] = peak

    for _ in range(repeats):
        storage = {"value": None, "time": None, "mem": None, "error": None}
        th = threading.Thread(target=run_target, args=(storage,))
        th.daemon = True
        th.start()
        th.join(timeout)

        if th.is_alive():
            return {
                "timeout": True,
                "timeout_seconds": timeout,
                "value": None,
                "time_mean": None,
                "time_min": None,
                "time_all": [],
                "mem_peak_bytes": None
            }

        if storage["error"] is not None:
            raise RuntimeError(f"Erro na execução do algoritmo: {storage['error']}")

        last_value = storage["value"]
        times.append(storage["time"])
        mem_peaks.append(storage["mem"])

    return {
        "timeout": False,
        "value": last_value,
        "time_mean": sum(times) / len(times),
        "time_min": min(times),
        "time_all": times,
        "mem_peak_bytes": max(mem_peaks) if mem_peaks else None
    }
