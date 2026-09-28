#!/usr/bin/env python3
"""Bounded launcher for as069_audit.py (macOS-compatible bound enforcement).

Declared bounds:  <= 120 s wall/CPU, <= 512 MB RSS, 1 thread.
Enforced:
  - RLIMIT_CPU = 120 s (soft+hard)  ......... enforced (setrlimit succeeds)
  - threads = 1 via env  .................. enforced (OPENBLAS/OMP/MKL/VECLIB/NUMEXPR)
  - RLIMIT_AS = 512 MB  ................... NOT enforceable on this macOS host:
        macOS kernel refuses setrlimit(RLIMIT_AS, finite) ("current limit exceeds
        maximum limit" even for a soft-only lowering; only infinity is accepted).
        Recorded limitation; actual memory is MEASURED (getrusage maxrss) instead.
Actual wall time and max RSS are also measured externally with /usr/bin/time -l.
"""
import resource, os, sys, time

CPU_S = 120
MEM_B = 512 * 1024 * 1024

t0 = time.time()
res_cpu = resource.setrlimit(resource.RLIMIT_CPU, (CPU_S, CPU_S))
try:
    resource.setrlimit(resource.RLIMIT_AS, (MEM_B, MEM_B))
    as_state = f"RLIMIT_AS set to {MEM_B} (enforced)"
except Exception as e:
    as_state = f"RLIMIT_AS NOT enforceable on this macOS host ({e}); memory measured only"

for k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
          "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[k] = "1"

print(f"[bounded-launcher] RLIMIT_CPU={CPU_S}s ok; {as_state}; threads=1", flush=True)
os.execv(sys.executable, [sys.executable, "as069_audit.py"])