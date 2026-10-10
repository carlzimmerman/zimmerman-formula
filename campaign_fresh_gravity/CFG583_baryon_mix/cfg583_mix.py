"""CFG583: does the law's SPARC residual track the baryon mix at fixed baryonic mass? Criteria: FROZEN_CRITERIA.md (ba12dc107).
MUTATE: CFG583_MUTATE=1 injects Delta_out += -0.20 f_gas (must be recovered).
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("CFG583_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
CONV = 3.0857e19 / 1e6                    # (km/s)^2/kpc -> m/s^2 : 1 (km/s)^2/kpc = 1e6/3.0857e19 m/s^2
YB = 0.7
NPERM = 2000


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


def nu(y):
    y = np.maximum(y, 1e-30); return 1.0 / (-np.expm1(-np.sqrt(y)))


tab = {}
KEYS = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):           # same parser as CFG516
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        v = dict(zip(KEYS, [float(t) for t in tok[1:18]]))
    except ValueError:
        continue
    tab[tok[0]] = dict(T=int(v["T"]), inc=v["Inc"], L36=v["L36"] * 1e9, MHI=v["MHI"] * 1e9, Q=int(v["Q"]))


def load(name):
    a = np.loadtxt(os.path.join(DATA, "sparc_data", f"{name}_rotmod.dat"), comments="#")
    return dict(R=a[:, 0], V=a[:, 1], eV=a[:, 2], Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5], SBb=a[:, 7])


def galaxies(Yd):
    rows = []
    for name, t in tab.items():
        if t["Q"] > 2 or t["inc"] < 30:
            continue
        fn = os.path.join(DATA, "sparc_data", f"{name}_rotmod.dat")
        if not os.path.exists(fn):
            continue
        d = load(name)
        R = d["R"]
        gobs = d["V"] ** 2 / R / CONV
        gbar = (d["Vg"] * np.abs(d["Vg"]) + Yd * d["Vd"] ** 2 + YB * d["Vb"] ** 2) / R / CONV
        Lb = 2 * math.pi * np.trapz(d["SBb"] * (R * 1e3), R * 1e3) if np.any(d["SBb"] > 0) else 0.0
        Ld = max(t["L36"] - Lb, 0.0)
        Mb = 1.33 * t["MHI"] + Yd * Ld + YB * Lb
        rows.append(dict(name=name, T=t["T"], gobs=gobs, gbar=gbar, Mb=Mb, fgas=1.33 * t["MHI"] / Mb,
                         fbul=(YB * Lb / (Yd * Ld + YB * Lb)) if (Yd * Ld + YB * Lb) > 0 else 0.0))
    return rows


def residuals(rows, a0, outer=True):
    out = []
    for r in rows:
        ok = (r["gbar"] > 0) & (r["gobs"] > 0)
        D = np.log10(r["gobs"][ok]) - np.log10(nu(r["gbar"][ok] / a0) * r["gbar"][ok])
        sel = (r["gbar"][ok] < a0 / 3) if outer else np.ones(ok.sum(), bool)
        out.append(float(np.mean(D[sel])) if sel.sum() >= 3 else np.nan)
    return np.array(out)


def fit(D, lM, fg, fb):
    X = np.column_stack([np.ones_like(D), lM - 10, fg, fb])
    beta, *_ = np.linalg.lstsq(X, D, rcond=None)
    return beta


def perm_p(D, lM, fg, fb, which, rng):
    b0 = fit(D, lM, fg, fb)[2 if which == "fgas" else 3]
    q = np.digitize(lM, np.quantile(lM, [0.2, 0.4, 0.6, 0.8]))
    cnt = 0
    for _ in range(NPERM):
        x = (fg if which == "fgas" else fb).copy()
        for k in range(5):
            m = q == k; x[m] = rng.permutation(x[m])
        b = fit(D, lM, x, fb)[2] if which == "fgas" else fit(D, lM, fg, x)[3]
        cnt += abs(b) >= abs(b0)
    return b0, (cnt + 1) / (NPERM + 1)


P("=" * 100)
P(f"CFG583  baryon mix vs the law's residual (SPARC)  {'*** MUTATE: Delta_out -= 0.20 f_gas ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
res = {}
for Yd in (0.5, 0.4, 0.6):
    rows = galaxies(Yd)
    for foot, a0 in A0.items():
        for outer in (True, False):
            D = residuals(rows, a0, outer)
            ok = np.isfinite(D)
            lM = np.log10([r["Mb"] for r in rows])[ok]; fg = np.array([r["fgas"] for r in rows])[ok]; fb = np.array([r["fbul"] for r in rows])[ok]
            Dk = D[ok] + (-0.20 * fg if MUTATE else 0.0)
            rng = np.random.default_rng(583)
            bg, pg = perm_p(Dk, lM, fg, fb, "fgas", rng)
            bb, pb = perm_p(Dk, lM, fg, fb, "fbul", rng)
            key = f"Yd{Yd}|{foot}|{'out' if outer else 'all'}"
            res[key] = dict(n=int(ok.sum()), median=float(np.median(Dk)), b_logM=float(fit(Dk, lM, fg, fb)[1]), c_fgas=float(bg), p_fgas=pg,
                            d_fbul=float(bb), p_fbul=pb, n_bulge=int((fb > 0.05).sum()))
            if Yd == 0.5 or outer:
                P(f"  [{key:22s}] n {ok.sum():3d} (bulge>5%: {(fb > 0.05).sum():2d})  median {np.median(Dk):+.3f}  "
                  f"b(logM) {res[key]['b_logM']:+.3f}  c(f_gas) {bg:+.3f} (p {pg:.4f})  d(f_bul) {bb:+.3f} (p {pb:.4f})")

P("\n--- controls")
p05 = res["Yd0.5|canonical|out"]
check(p05["n"] >= 100, f"C1 galaxies with >= 3 outer points: {p05['n']} (>= 100)")
check(all(abs(res[f'Yd0.5|{f}|out']['median']) < 0.1 for f in A0), "C2 |median Delta_out| < 0.1 dex: " + ", ".join(f"{f} {res[f'Yd0.5|{f}|out']['median']:+.3f}" for f in A0))
if not MUTATE:
    rows = galaxies(0.5); D = residuals(rows, A0["canonical"], True); ok = np.isfinite(D)
    lM = np.log10([r["Mb"] for r in rows])[ok]; fg = np.array([r["fgas"] for r in rows])[ok]; fb = np.array([r["fbul"] for r in rows])[ok]
    q = np.digitize(lM, np.quantile(lM, [0.2, 0.4, 0.6, 0.8])); rng = np.random.default_rng(5830); hits = 0
    NP0 = NPERM; NPERM = 200
    for i in range(200):
        Ds = D[ok].copy()
        for k in range(5):
            m = q == k; Ds[m] = rng.permutation(Ds[m])
        _, p = perm_p(Ds, lM, fg, fb, "fgas", rng); hits += p < 0.05
    NPERM = NP0
    check(abs(hits / 200 - 0.05) <= 0.035, f"C3 null calibration: fraction p < 0.05 over 200 shuffled datasets = {hits / 200:.3f} (0.05 +- 0.035)")

P("\n--- verdict (primary: outer residual)")
calls = {}
for pred, ck, pk, exp in (("f_gas", "c_fgas", "p_fgas", -1), ("f_bul", "d_fbul", "p_fbul", +1)):
    base = [res[f"Yd0.5|{f}|out"] for f in A0]
    sig = all(b[pk] < 0.005 for b in base) and np.sign(base[0][ck]) == np.sign(base[1][ck])
    robust = all(np.sign(res[f"Yd{y}|{f}|out"][ck]) == np.sign(base[0][ck]) for y in (0.4, 0.6) for f in A0)
    if sig and robust:
        calls[pred] = "RELATION FOUND, " + ("KIDS-CONSISTENT" if np.sign(base[0][ck]) == exp else "OPPOSITE to the KiDS pattern")
    else:
        calls[pred] = "NO RELATION"
    P(f"  {pred}: {calls[pred]}  (coef {base[0][ck]:+.3f} / {base[1][ck]:+.3f}, p {base[0][pk]:.4f} / {base[1][pk]:.4f}, Y-robust sign {robust})")
if MUTATE:
    P("MUTATE reading: f_gas must be RELATION FOUND with a negative coefficient.")
J531 = os.path.join(REPO, "campaign_fresh_gravity", "CFG531_inner_halo_shortfall", "README.md")
P("\n--- context (CFG531, KiDS, as recorded): early +0.832 +- 0.127, late -0.31; M* tertiles -0.65 / +0.48 / +0.60 (canonical)")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(calls=calls, res=res, checks=CHECKS), open(os.path.join(HERE, f"cfg583_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg583_mix{TAG}.out"), "w").write("\n".join(OUT) + "\n")
