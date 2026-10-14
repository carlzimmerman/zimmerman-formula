"""CFG787 -- CFG776's surplus expulsion with angular momentum and gradual baryon loss.  Criteria: FROZEN_CRITERIA.md (7ca119528).
CFG747/776 integrator (units G = a0 = M_now = 1) + centrifugal term j^2/r^3 + time-dependent baryon mass M_b(t).
Run after T1x:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg787.py   (CFG787_MUTATE=1: no cubic push).
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG787_MUTATE", "0") == "1"
N, RMIN, R0, DT, CORE = 4000, 0.5, 50.0, 0.005, 0.5
TS = [100, 200, 500, 1000, 2000]; RAD = [2.0, 5.0, 8.0, 11.0, 25.0]
OUT = []
def P(s): print(s, flush=True); OUT.append(s)

def run(p, eps_on, tau):
    mtot = math.sqrt(p) * (R0 - CORE); dm = mtot / N
    q = (np.arange(N) + 0.5) / N; r = RMIN + q * (R0 - RMIN); v = np.zeros(N)
    rng = np.random.default_rng(787)
    eps = rng.uniform(0, 1, N) if eps_on else np.zeros(N)
    m_enc = CORE + dm * np.arange(N)
    j = eps * r * np.sqrt((p + m_enc) / r)                    # j = eps r V_c, V_c^2 = (M_b,peak + m(<r)) / r at start
    Mb = lambda t: p - (p - 1.0) * (min(t / tau, 1.0) if tau > 0 else 1.0)
    def acc(r, t):
        order = np.argsort(r); rs = r[order]; mi = CORE + dm * np.arange(N)
        a_s = -Mb(t) / rs ** 2
        if not MUT:
            a_s = a_s + ((mi + dm) ** 3 - mi ** 3) / (3 * dm * rs ** 4)
        a = np.empty(N); a[order] = a_s
        return a + j ** 2 / r ** 3
    a = acc(r, 0.0); win = {T: [] for T in TS}
    for n in range(int(TS[-1] / DT)):
        t = n * DT
        v += 0.5 * DT * a; r += DT * v
        low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
        a = acc(r, t + DT); v += 0.5 * DT * a
        if n % 100 == 0:
            for T in TS:
                if 0.9 * T <= t + DT <= T:
                    rs = np.sort(r); win[T].append([(CORE + dm * np.searchsorted(rs, R)) / R for R in RAD])
    res = {}
    for T in TS:
        mr = np.mean(win[T], axis=0); fr = (mr - 1) / (math.sqrt(p) - 1)
        res[str(T)] = dict(m_over_r=[float(x) for x in mr], relic=[float(x) for x in fr])
    return res

def cls_of(res):
    f = res["200"]["relic"]; f5_11 = f[1:4]
    if all(x <= 0.2 for x in f5_11): return "EXPELLED"
    if f[1] >= 0.5 and f[2] >= 0.5: return "RETAINED"
    return "PARTIAL"

P("CFG787  surplus expulsion with angular momentum / gradual loss" + ("  [MUTATE no push]" if MUT else ""))
cases = [("K1 sudden radial", False, 0)] if MUT else [("K1 sudden radial", False, 0), ("A ang. mom.", True, 0), ("B tau 10", False, 10), ("B tau 50", False, 50), ("B tau 200", False, 200), ("A+B tau 50", True, 50)]
R = {}
c776 = json.load(open(os.path.join(HERE, "..", "CFG776_frozen_relic", "cfg776_results.json")))["runs"]
for p in (1.5, 3.0):
    for lab, e, tau in cases:
        res = run(p, e, tau); c = cls_of(res); R[f"p{p}|{lab}"] = dict(res=res, cls=c)
        P(f"  p {p} {lab:18s}: relic at t 200 (r 2/5/8/11/25) " + "/".join(f"{x:+.2f}" for x in res["200"]["relic"]) + f"  -> {c}")
        if lab.startswith("K1") and not MUT:
            ref = c776[str(p)]["snaps"]
            d = max(abs(res[str(T)]["m_over_r"][k] - ref[str(T)]["m_over_r"][k]) for T in (100, 200, 500, 1000, 2000) for k in range(5))
            P(f"    K1 vs CFG776 tables: max |d m/r| {d:.3f} -> {'PASS' if d <= 0.01 else 'FAIL'}")
            R[f"p{p}|K1_dev"] = d
if not MUT:
    test = [v["cls"] for k, v in R.items() if isinstance(v, dict) and "cls" in v and "K1" not in k]
    verdict = "CFG776 ROBUST" if all(c == "EXPELLED" for c in test) else "CFG776 QUALIFIED: " + ", ".join(k for k, v in R.items() if isinstance(v, dict) and v.get("cls") not in (None, "EXPELLED") and "K1" not in k)
    P(f"\n  VERDICT: {verdict}")
    R["verdict"] = verdict
json.dump(R, open(os.path.join(HERE, f"cfg787_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg787{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
