"""AN2 A2 driver: KT, KB, KE, KG, then the 16 S1 rows (FROZEN_CRITERIA sections 6-8, A2 section 5).
At most 2 jobs, one thread, nice 15. Rows already in an2_rows.jsonl are skipped; a preempted row
resumes from its checkpoint on the next call. Stops if free disk < 15 GB or a row hits the CPU cap."""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, "an2_rows.jsonl")
CHK = os.path.join(HERE, "an2_checks.jsonl")
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONUNBUFFERED="1")
REF = {("1e12", 56.6): 5.277, ("1e12", 0.1): 13.709, ("1e15", 56.6): 4.701, ("1e15", 0.1): 13.783}  # A2 section 1, canonical t Gyr
STOP = []


def tag(key, mu, foot, shape, N, eta, L):
    return f"{key}_{mu}_{foot}_{shape}_N{N}_e{eta}_L{L}"


def done():
    d = {}
    if os.path.exists(ROWS):
        for ln in open(ROWS):
            o = json.loads(ln); d[o["id"]] = o
    return d


def tq(o):
    f = o.get("fold_q")
    return f["t_Gyr"] if (o["status"] == "FOLD" and f) else None


def run(r):
    key, mu, foot, shape, N, eta, L = r
    t = tag(*r)
    if t in done(): return done()[t]
    if STOP: return None
    if shutil.disk_usage(HERE).free < 15e9:
        STOP.append("disk under 15 GB"); return None
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(HERE, "an2.py"), "row", key, str(mu), foot, shape, str(N), str(eta), str(L)],
                       env=ENV, cwd=HERE, capture_output=True, text=True)
    print(t, "exit", p.returncode, p.stdout.strip()[-400:], flush=True)
    if p.returncode == 76: STOP.append(f"CPU cap at {t}")
    if p.returncode == 75: STOP.append(f"preempted at {t}")
    if p.returncode not in (0, 75, 76): STOP.append(f"error at {t}: {p.stderr[-300:]}")
    return done().get(t)


def batch(rows):
    with ThreadPoolExecutor(2) as ex:
        return list(ex.map(run, rows))


def out(nm, d):
    d = dict(check=nm, **d); print(json.dumps(d), flush=True)
    with open(CHK, "a") as f: f.write(json.dumps(d) + "\n")


def rel(a, b):
    return None if (a is None or b is None) else abs(a - b) / b


def main():
    # KT: T1, T2 at N 64 over eta 0.05, 0.025, 0.0125
    T = [("1e12", 0.1, "canonical", "B"), ("1e15", 56.6, "canonical", "B")]
    E = [0.05, 0.025, 0.0125]
    res = batch([(*t, 64, e, 8) for t in T for e in E])
    if STOP: return print("STOP", STOP)
    t = {(T[i // 3], E[i % 3]): tq(res[i]) for i in range(6)}
    moves = {e: [rel(t[(x, e)], t[(x, e / 2)]) for x in T] for e in E[:2]}
    adopt = next((e for e in E[:2] if all(m is not None and m <= 0.01 for m in moves[e])), None)
    out("KT", dict(t_q={f"{x[0]}_{x[1]}_{e}": t[(x, e)] for x in T for e in E}, moves=moves, line=0.01, adopted=adopt, ok=adopt is not None))
    eta = adopt if adopt is not None else 0.0125  # no pass: NO VERDICT, numbers at the smallest eta
    # KB: (N 64, L) against (N 128, 2L)
    b = batch([("1e12", 0.1, "canonical", "B", 64, eta, 8), ("1e12", 0.1, "canonical", "B", 128, eta, 16)])
    if STOP: return print("STOP", STOP)
    m = rel(tq(b[0]), tq(b[1]))
    out("KB", dict(eta=eta, t64=tq(b[0]), t128_2L=tq(b[1]), err=m, line=0.03, ok=m is not None and m <= 0.03))
    # KE: e = 0 at 128^3, canonical
    ke = [("1e12", 56.6), ("1e15", 56.6), ("1e15", 0.1), ("1e12", 0.1)]
    k = batch([(a, mu, "canonical", "0", 128, eta, 8) for a, mu in ke])
    if STOP: return print("STOP", STOP)
    kr = {f"{a}_{mu}": dict(t_q=tq(o), t_ref=REF[(a, mu)], err=rel(tq(o), REF[(a, mu)]), shape=(o.get("fold_q") or {}).get("shape"), status=o["status"]) for (a, mu), o in zip(ke, k)}
    graded = [kr[x] for x in ("1e12_56.6", "1e15_56.6", "1e15_0.1")]
    out("KE", dict(eta=eta, rows=kr, line=0.05, graded="1e12_56.6, 1e15_56.6, 1e15_0.1; 1e12_0.1 reported (A2 gives it a t_ref)",
                   ok=all(g["err"] is not None and g["err"] <= 0.05 and g["shape"] == "point" for g in graded)))
    # KG: 64 and 96 first, then the rows
    G = [("1e12", 0.1, "canonical", "A"), ("1e15", 56.6, "canonical", "A")]
    batch([(*g, n, eta, 8) for g in G for n in (64, 96)])
    if STOP: return print("STOP", STOP)
    # 16 S1 rows, N 128
    S1 = [(a, mu, f, s, 128, eta, 8) for a in ("1e12", "1e15") for mu in (0.1, 56.6) for s in ("A", "B") for f in ("canonical", "alt")]
    batch(S1)
    if STOP: return print("STOP", STOP)
    d = done(); kg = {}
    for g in G:
        tt = {n: tq(d[tag(*g, n, eta, 8)]) for n in (64, 96, 128)}
        kg["_".join(map(str, g))] = dict(t=tt, err_128_96=rel(tt[128], tt[96]), err_96_64=rel(tt[96], tt[64]))
    out("KG", dict(eta=eta, rows=kg, line=0.05, ok=all(v["err_128_96"] is not None and v["err_128_96"] <= 0.05 for v in kg.values())))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
