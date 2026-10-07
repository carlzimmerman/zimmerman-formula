#!/usr/bin/env python3
"""CFG443: halo concentration of CFG378's settled cold component vs the law's target (FROZEN_CRITERIA.md). Read-only on CFG378.
Run: python3 cfg443_halo_shape.py [--mutate]"""
import os, sys, json, math, io, contextlib
os.environ.setdefault("CFG378_THREADS", "2")
import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.join(LANES, "CFG378_two_fluid_ot_settling"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg378_pm as E
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
RADII = np.array([2, 3, 4, 6]); NH = 20; SEP = 8
M = 256; rng0 = np.arange(-6, 7)
OFF = np.array([(i, j, k) for i in rng0 for j in rng0 for k in rng0]); DIST = np.sqrt((OFF ** 2).sum(1))
def cum_profiles(field, centre):
    idx = (centre[None, :] + OFF) % M
    v = field[idx[:, 0], idx[:, 1], idx[:, 2]]
    return np.array([v[DIST <= r].sum() for r in RADII])
def find_halos(rho):
    s = gaussian_filter(rho, 1.0, mode="wrap")
    pk = (s == maximum_filter(s, size=3, mode="wrap"))
    cand = np.argwhere(pk); order = np.argsort(-s[pk]); cand = cand[order]
    out = []
    for c in cand:
        if all(np.sqrt((((c - o + M // 2) % M - M // 2) ** 2).sum()) >= SEP for o in out):
            out.append(c)
        if len(out) == NH: break
    return np.array(out)
def slopes(num, den):
    lr = np.log10(RADII); return np.array([np.polyfit(lr, np.log10(n / d), 1)[0] for n, d in zip(num, den)])
def boot(x, seed=61):
    r = np.random.default_rng(seed); return float(np.median(x)), float(np.std([np.median(x[r.integers(0, len(x), len(x))]) for _ in range(2000)]))
res = {}; checks = {}
for foot in ("canonical", "alt"):
    per = {}
    for g in ("1", "0.1", "0"):
        tag = f"TWO_g{g}_FLAT_{foot}_N256"
        d = np.load(os.path.join(E.WORK, f"cfg378_{tag}_z0.npz"))
        pos_c = d["pos_c"].astype(np.float64); pos_b = d["pos_b"].astype(np.float64)
        if MUT: pos_c = pos_b.copy()
        st = E.State("TWO", foot, 256, float(g))
        db, dc, dt, rc = st.fields(pos_b, pos_c)
        checks[f"K1_{tag}"] = bool(abs(rc.sum() - st.N) / st.N < 1e-10)
        rho_t, _ = E.target_field(st.mesh, db, 1.0, foot)
        rho_c = (1.0 - E.FB) * (1.0 + dc); rho_b = E.FB * (1.0 + db)
        fsw = E.switch_field(st.mesh, st.mesh.fwd(dt), 1.0, st.dta)
        Q = float(np.sum(fsw * rho_c) / np.sum(fsw * rho_t))
        js = json.load(open(os.path.join(E.WORK, f"cfg378_{tag}.json")))
        qref = (js.get("snap", {}).get("z0") or {}).get("Q")
        checks[f"K2_{tag}"] = (abs(Q / qref - 1) < 1e-3) if qref else "n/a"
        halos = find_halos((1.0 + dt).astype(np.float64))
        Mc = np.array([cum_profiles(rho_c, c) for c in halos]); Mt = np.array([cum_profiles(rho_t, c) for c in halos]); Mb = np.array([cum_profiles(rho_b, c) for c in halos])
        st_t, st_b = slopes(Mc, Mt), slopes(Mc, Mb)
        per[g] = dict(ct=boot(st_t), cb=boot(st_b), Q=Q, Qref=qref, raw_t=st_t.tolist())
        P(f"{foot:9s} g={g:3s}: slope log(Mc/Mt) {per[g]['ct'][0]:+.3f} +- {per[g]['ct'][1]:.3f} | slope log(Mc/Mb) {per[g]['cb'][0]:+.3f} +- {per[g]['cb'][1]:.3f} | Q(z0) {Q:.4f} (CFG378 {qref})")
    for g in ("1", "0.1"):
        m, s = per[g]["ct"]
        v = "X-COP-LIKE" if (m < -0.1 and m / s < -3) else "TARGET-SHAPED" if abs(m) < 2 * s else "ANTI-CONCENTRATED" if (m > 0.1 and m / s > 3) else "INCONCLUSIVE"
        dd = m - per["0"]["ct"][0]; sd = math.hypot(s, per["0"]["ct"][1])
        vis = "settling measurable" if abs(dd) > 2 * sd else "settling invisible at these radii"
        res[f"{foot}|g{g}"] = dict(slope_t=per[g]["ct"], slope_b=per[g]["cb"], minus_g0=dd, sd=sd, verdict=v, visibility=vis)
        P(f"  -> {foot} g={g}: {v}; g{g} - g0 = {dd:+.3f} +- {sd:.3f} ({vis})")
    res[f"{foot}|g0"] = dict(slope_t=per["0"]["ct"], slope_b=per["0"]["cb"])
P("controls: " + ", ".join(f"{k}={v}" for k, v in checks.items()))
json.dump(dict(res=res, checks=checks), open(os.path.join(HERE, f"cfg443_halo_shape{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg443_halo_shape{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = abs(res["canonical|g1"]["slope_b"][0]) < 0.01; P(f"MUTATE: |slope Mc/Mb| < 0.01 -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if all(v is True or v == "n/a" for v in checks.values()) else 1)
