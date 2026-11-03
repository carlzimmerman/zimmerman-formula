"""AN2 diagnostic SL (SPHERE_LAG_NOTE.md): e = 0 sphere with dust, baryon stop, hold term and kernel switched one at a time.
python3 sphere_lag.py ID KEY N   (ID in D0, D1, D2, D3, D4)"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import an2  # noqa: E402


def cic(x, m):
    """CIC on the same grid convention as an2.tsc (grid points at i dx), as 3 points with the last weight 0."""
    N = m.N; u = np.mod(x, m.L) / m.dx; i = np.floor(u).astype(np.int64); d = u - i
    return [i % N, (i + 1) % N, (i + 2) % N], [1 - d, d, 0 * d]


def main(rid, key, N):
    dust = rid in ("D0", "D1", "D3")
    stop = rid in ("D1", "D4")
    if rid == "D3": an2.tsc = cic
    S = an2.build_row(key, 56.6, "canonical", "0", N, 0.05, 8, dust=dust)
    if not stop: S.rf = None
    o = S.run(S.t0, cap=an2.CPU_CAP)
    f = o.get("fold_q") or {}
    r = dict(id=rid, key=key, N=N, dust=dust, stop=stop, kernel="CIC" if rid == "D3" else "TSC", status=o["status"],
             t_q=f.get("t_Gyr"), z=f.get("z"), shape=f.get("shape"), nstep=o.get("nstep"), cpu_s=o.get("cpu_s"), rss_gb=o.get("rss_gb"))
    print(json.dumps(r), flush=True)
    with open(os.path.join(HERE, "sphere_lag.jsonl"), "a") as fh: fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
