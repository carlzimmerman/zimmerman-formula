#!/usr/bin/env python3
"""CFG430: does the LMP coexistence field h_c (CFG481 operator) land on y = g_b/a0 = 1
from the operator itself?  FROZEN_CRITERIA.md (committed before this ran).

Usage:
  python3 cfg430_hc_map.py            -> main run: cfg430_hc_map.out / cfg430_results.json
  python3 cfg430_hc_map.py MUTATE     -> planted h_c controls M1 (-1) and M2 (-2):
                                          cfg430_hc_map_MUTATE.out / cfg430_results_MUTATE.json
Operator conventions are CFG481's (weights e^{beta X n}, F_h(X) = Q(X) - (X-h)^2/(2 beta a),
Kac coupling K = beta^3 a).  CFG481 and the CFG424 engine are imported read-only.
"""
import os, sys, json, math, importlib.util
os.environ.setdefault("CFG424_THREADS", "4")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
MODE = sys.argv[1] if len(sys.argv) > 1 else "MAIN"
WIN = 0.1                                     # |log10 y_c| window
GAMMA_480 = 6.25

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

# ------------------------------------------------------------------ operator (n_max general)
def tm(beta, X, U, J, N):
    n = np.arange(N + 1, dtype=float)
    on = 0.5 * U * n * (n - 1)
    E = on[:, None] + on[None, :] + J * n[:, None] * n[None, :] - 0.5 * X * (n[:, None] + n[None, :])
    lw = -beta * E
    s = lw.max()
    return np.exp(lw - s), s

def Q(beta, X, U, J, N):
    M, s = tm(beta, X, U, J, N)
    return float(np.log(np.linalg.eigvalsh(M)[-1])) + s

def m(beta, X, U, J, N):
    M, _ = tm(beta, X, U, J, N)
    lam, v = np.linalg.eigh(M); p = v[:, -1] ** 2; p /= p.sum()
    return float((np.arange(N + 1) * p).sum())

def chi(beta, X, U, J, N, d=1e-4):
    """per-site susceptibility dm/d(beta X) (exact for the infinite chain via Perron)."""
    return (m(beta, X + d / beta, U, J, N) - m(beta, X - d / beta, U, J, N)) / (2 * d)

def Xs(U, J, N):                               # particle-hole point of the core
    # run-1 used ((N-1)U + 2NJ)/2 and C0 failed: CFG481's transfer matrix adds the on-site
    # term U*C(n,2) at BOTH ends of every bond, i.e. 2U*C(n,2) per site, so the U shift doubles.
    return (N - 1) * U + N * J

def hc_I1(beta, a, U, J, N):                   # identity I1
    return Xs(U, J, N) - 0.5 * N * beta ** 2 * a

def onset_beta(a, U, J, N):
    """K chi(X_s) = 1 with K = beta^3 a  (identity I2); bisection in beta."""
    g = lambda b: b ** 3 * a * chi(b, Xs(U, J, N), U, J, N) - 1.0
    lo, hi = 1e-3, 1e-3
    while g(hi) < 0:
        hi *= 1.2
    lo = hi / 1.2
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if g(mid) < 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def gamma_at(beta, a, U, J, N):
    """density ratio of the two coexisting phases at h_c (symmetric maxima X_s +/- t*)."""
    xs, h = Xs(U, J, N), hc_I1(beta, a, U, J, N)
    F = lambda t: Q(beta, xs + t, U, J, N) - (xs + t - h) ** 2 / (2 * beta * a)
    ts = np.linspace(1e-4, 40.0 / beta, 4001)
    Fv = np.array([F(t) for t in ts]); i = int(np.argmax(Fv))
    if i == 0:
        return 1.0, 0.0
    lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
    for _ in range(60):                        # golden-ish refine
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if F(m1) < F(m2): lo = m1
        else: hi = m2
    t = 0.5 * (lo + hi)
    return m(beta, xs + t, U, J, N) / m(beta, xs - t, U, J, N), t

def beta_for_gamma(target, a, U, J, N, b_on):
    lo, hi = b_on * (1 + 1e-6), b_on * 1.05
    while gamma_at(hi, a, U, J, N)[0] < target:
        hi *= 1.05
        if hi > 20 * b_on: return None
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if gamma_at(mid, a, U, J, N)[0] < target: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def maxwell_generic(beta, a, U, J, N):
    """symmetry-free Maxwell root: Delta(h) = F(top max) - F(other max) sign change, bisection."""
    Xg = np.linspace(-25.0, 25.0, 5001)
    QX = np.array([Q(beta, x, U, J, N) for x in Xg])
    def delta(h):
        F = QX - (Xg - h) ** 2 / (2 * beta * a)
        ism = np.where((F[1:-1] >= F[:-2]) & (F[1:-1] >= F[2:]))[0] + 1
        if len(ism) < 2: return None
        top = ism[np.argsort(F[ism])[-2:]]       # the two highest maxima, ordered in X
        lo_i, hi_i = top.min(), top.max()
        return F[hi_i] - F[lo_i]
    h0 = hc_I1(beta, a, U, J, N)
    for w in (0.5, 0.2, 0.05, 0.01):            # run 2: near onset both maxima exist only in a narrow h window
        a_, b_ = h0 - w, h0 + w
        da, db = delta(a_), delta(b_)
        if da is not None and db is not None and da * db < 0: break
    else:
        return None
    for _ in range(80):
        mid = 0.5 * (a_ + b_); dm = delta(mid)
        if dm is None: return None
        if dm == 0.0: return mid                  # run 3: an exact zero froze da = 0 and walked to the bracket edge
        if dm * da < 0: b_, db = mid, dm
        else: a_, da = mid, dm
    return 0.5 * (a_ + b_)

def D1(bh): return bh ** 2                    # kernel-Bose: e^{beta h} = e^{-sqrt y}
def D2(bh): return math.exp(bh)              # log-fugacity: e^{beta h} = y
def inwin(y): return abs(math.log10(y)) <= WIN if y > 0 else False

# ------------------------------------------------------------------ C5 PM boundary
def pm_boundary(tag, work, foot):
    eng = load("cfg424_eng", os.path.join(CFG, "CFG424_turnaround_catchment", "cfg424_pm.py"))
    npz = np.load(os.path.join(work, tag + "_z0.npz"))
    M = int(npz["f"].shape[0]); mesh = eng.Mesh(M)
    delta = mesh.deposit(npz["pos"]); a = 1.0
    dk = mesh.fwd(delta); phik = (-1.5 * eng.Om / a) * dk * mesh.ik2; del dk
    fc, fh, fs = eng.MIXES["MIXA"]; kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * eng.Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    gb = [eng.FB * (-mesh.inv(1j * kv * phik * Wk)) for kv in mesh.kvec]; del Wk, phik
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * eng.a0_code(a, "FLAT", foot))
    w = (eng.nu_mono(y) - 1.0).astype(np.float32)
    divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w
    s_ph = -mesh.inv(divk); del divk
    s_c = (1.5 * eng.Om * (1.0 - eng.FB) / a) * (1.0 + delta)
    r = (s_ph - s_c) / s_c
    f = npz["f"].astype(np.float32)
    bnd = np.abs(r) < 0.05; on = f > 0.5
    out = dict(tag=tag, foot=foot, y_median_box=float(np.median(y)),
               n_bnd=int(bnd.sum()), y_med_bnd=float(np.median(y[bnd])) if bnd.any() else None,
               n_bnd_on=int((bnd & on).sum()),
               y_med_bnd_on=float(np.median(y[bnd & on])) if (bnd & on).any() else None,
               n_on=int(on.sum()), y_med_on=float(np.median(y[on])) if on.any() else None,
               frac_on_r_pos=float((r[on] > 0).mean()) if on.any() else None,
               y_med_rpos=float(np.median(y[r > 0])),
               y_p99=float(np.percentile(y, 99)), y_p999=float(np.percentile(y, 99.9)), y_max=float(y.max()),
               frac_y_ge_0p5=float((y >= 0.5).mean()))
    return out

# ------------------------------------------------------------------ main
def main():
    P = print
    P("=" * 78); P(f"CFG430: LMP coexistence field h_c vs y = 1   mode={MODE}"); P("=" * 78)
    plant = {"MAIN": None, "MUTATE": None}
    res = {"mode": MODE}
    # C0: identities
    c481 = load("cfg481", os.path.join(CFG, "CFG481_lmp_operator_exact", "cfg481_lmp.py"))
    band = c481.scan_band(0.56, 4.0, 0.0, 0.02, np.linspace(-20.0, 20.0, 4001))
    h481 = band[2]; hI1 = hc_I1(0.56, 4.0, 0.0, 0.02, 4)
    P(f"[C0] CFG481 scan_band h_c(beta=0.56,a=4,U=0,J=0.02) = {h481:.5f}   I1 = {hI1:.5f}   |d| = {abs(h481-hI1):.2e}")
    gens = []
    for (b, a, U, J) in [(0.6, 4.0, 0.0, 0.0), (0.45, 8.0, 0.1, 0.05), (1.2, 2.0, 0.1, 0.02)]:
        hg = maxwell_generic(b, a, U, J, 4); hi = hc_I1(b, a, U, J, 4)
        gens.append(abs(hg - hi) if hg is not None else 1e9)
        P(f"[C0] generic Maxwell beta={b} a={a} U={U} J={J}: h_c = {hg}   I1 = {hi:.5f}")
    # I3 analytic check at U=J=0
    for N in (3, 4, 5):
        bo = onset_beta(4.0, 0.0, 0.0, N)
        P(f"[C0] I3 n_max={N}: beta_on*h_c(onset) numeric = {bo*hc_I1(bo,4.0,0,0,N):.5f}   analytic -6/(N+2) = {-6/(N+2):.5f}")
    c0 = abs(h481 - hI1) <= 1e-3 and max(gens) <= 1e-3
    P(f"[C0] identities {'PASS' if c0 else 'FAIL -> INVALID'}")
    res["C0"] = dict(h481=h481, hI1=hI1, generic_dev=gens, pass_=c0)

    # grid
    rows = []
    P(f"\n{'U':>4} {'J':>5} {'a':>3} | {'beta_on':>8} {'bh_on':>8} {'D1 y':>7} {'D2 y':>7} | {'beta480':>8} {'bh_480':>8} {'D1 y':>7} {'D2 y':>7}")
    for U in (0.0, 0.1):
        for J in (0.0, 0.02, 0.05):
            for a in (2.0, 4.0, 8.0):
                bo = onset_beta(a, U, J, 4); bh_on = bo * hc_I1(bo, a, U, J, 4)
                b4 = beta_for_gamma(GAMMA_480, a, U, J, 4, bo)
                bh_4 = b4 * hc_I1(b4, a, U, J, 4) if b4 else None
                rows.append(dict(U=U, J=J, a=a, beta_on=bo, bh_on=bh_on, beta480=b4, bh_480=bh_4))
    if MODE == "MUTATE":
        variants = [("M1", -1.0), ("M2", -2.0)]
    else:
        variants = [("MAIN", None)]
    verdicts = {}
    for name, pv in variants:
        P(f"\n--- variant {name}" + (f": planted beta*h_c = {pv}" if pv is not None else ": computed beta*h_c"))
        for r in rows:
            bo_h = pv if pv is not None else r["bh_on"]
            b4_h = pv if pv is not None else r["bh_480"]
            r[name] = dict(D1_on=D1(bo_h), D2_on=D2(bo_h),
                           D1_480=D1(b4_h) if b4_h is not None else None,
                           D2_480=D2(b4_h) if b4_h is not None else None)
            q = r[name]
            P(f"{r['U']:4.1f} {r['J']:5.2f} {r['a']:3.0f} | {r['beta_on']:8.4f} {bo_h:8.4f} {q['D1_on']:7.3f} {q['D2_on']:7.3f} | "
              f"{(r['beta480'] or float('nan')):8.4f} {(b4_h if b4_h is not None else float('nan')):8.4f} "
              f"{(q['D1_480'] or float('nan')):7.3f} {(q['D2_480'] or float('nan')):7.3f}")
        pure = [r for r in rows if r["U"] == 0 and r["J"] == 0]
        C1 = all(inwin(r[name]["D1_on"]) for r in pure)
        C2 = all(inwin(r[name]["D1_on"]) for r in rows)
        C3_D1 = sum(inwin(r[name]["D1_480"]) for r in rows if r[name]["D1_480"] is not None)
        C3_D2 = sum(inwin(r[name]["D2_480"]) for r in rows if r[name]["D2_480"] is not None)
        C4 = all(inwin(r[name]["D2_on"]) for r in rows)
        d1on = [r[name]["D1_on"] for r in rows]; d1_480 = [r[name]["D1_480"] for r in rows if r[name]["D1_480"]]
        P(f"C1 (D1 at onset, U=J=0, 3 a's): {'PASS' if C1 else 'FAIL'}   y_c = {[round(r[name]['D1_on'],4) for r in pure]}")
        P(f"C2 (D1 at onset, 18 settings):  {'PASS' if C2 else 'FAIL'}   y_c range [{min(d1on):.3f}, {max(d1on):.3f}]  "
          f"({sum(inwin(v) for v in d1on)}/18 in window)")
        P(f"C3 (P_480, fitted gamma=6.25): D1 in window {C3_D1}/18 (y_c [{min(d1_480):.3f}, {max(d1_480):.3f}]), D2 in window {C3_D2}/18  [reported only]")
        P(f"C4 (D2 at onset, 18 settings):  {'PASS' if C4 else 'FAIL'}   y_c range [{min(r[name]['D2_on'] for r in rows):.3f}, {max(r[name]['D2_on'] for r in rows):.3f}]")
        verdicts[name] = dict(C1=C1, C2=C2, C3_D1=C3_D1, C3_D2=C3_D2, C4=C4,
                              D1_on_range=[min(d1on), max(d1on)], D1_480_range=[min(d1_480), max(d1_480)])
    res["rows"] = rows

    # C5
    if MODE == "MAIN":
        ext = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
        snaps = [("cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_alt_N256_seed360", os.path.join(ext, "cfg424_work"), "alt"),
                 ("cfg410_RES_Rc3_MIXA_FLAT_canonical_N256", os.path.join(ext, "cfg410_work"), "canonical")]
        c5 = []
        for tag, work, foot in snaps:
            o = pm_boundary(tag, work, foot); c5.append(o)
            P(f"\n[C5] {tag} ({foot}): box median y = {o['y_median_box']:.4f}")
            P(f"     switch boundary |r|<0.05: n = {o['n_bnd']}, median y = {o['y_med_bnd']:.4f}")
            P(f"     boundary within ON cells: n = {o['n_bnd_on']}, median y = {o['y_med_bnd_on']}")
            P(f"     ON cells n = {o['n_on']}: median y = {o['y_med_on']}, frac with s_ph > s_c = {o['frac_on_r_pos']}")
            P(f"     all cells with s_ph > s_c: median y = {o['y_med_rpos']:.4f}")
            P(f"     reach of the mesh: y p99 = {o['y_p99']:.4f}, p99.9 = {o['y_p999']:.4f}, max = {o['y_max']:.3f}, "
              f"fraction of cells with y >= 0.5 = {o['frac_y_ge_0p5']:.2e}")
        c5ok = all(o["y_med_bnd"] is not None and 0.5 <= o["y_med_bnd"] <= 2.0 for o in c5)
        P(f"[C5] PM switch fires at y in [0.5, 2]: {c5ok}")
        res["C5"] = dict(snaps=c5, consistent=c5ok)
    else:
        try:
            c5ok = json.load(open(os.path.join(HERE, "cfg430_results.json")))["C5"]["consistent"]
        except Exception:
            c5ok = None
        P(f"\n[C5] reused from the main run: consistent = {c5ok}")

    P("\nVERDICT")
    for name, v in verdicts.items():
        if not c0:
            vv = "INVALID (C0 failed)"
        elif v["C1"] and v["C2"]:
            vv = "PASS" if c5ok else "CONDITIONAL (PASS downgraded by C5: the PM switch does not fire at y=1)"
        elif v["C1"]:
            vv = "CONDITIONAL: y=1 only in the pure-cap limit U=J=0, n_max=4, D1 reading"
        else:
            vv = "FAIL: needs a constant" + (" (convention-dependent: D2 passes)" if v["C4"] else "")
        v["verdict"] = vv
        P(f"  [{name}] {vv}")
    if MODE == "MUTATE":
        flip = verdicts["M1"]["C1"] and verdicts["M1"]["C2"] and (not verdicts["M2"]["C1"])
        P(f"  MUTATE flips (M1 -> C1,C2 PASS; M2 -> C1 FAIL): {'YES' if flip else 'NO -> harness broken, INVALID'}")
        res["mutate_flips"] = flip
    res["verdicts"] = verdicts
    fn = "cfg430_results.json" if MODE == "MAIN" else "cfg430_results_MUTATE.json"
    json.dump(res, open(os.path.join(HERE, fn), "w"), indent=1, default=float)
    P(f"wrote {fn}")

if __name__ == "__main__":
    main()
