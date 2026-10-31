#!/usr/bin/env python3
"""X80 AMENDMENT A1, reported lines 1-3: converged-cusp eta on the X48 zooms at 1e10, 1e11 (1e12 as the check), ratios to 1e12, and the reading against NF1's window.
    python3 x80_converged.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); X48 = os.path.join(REB, "X48_native_cf_zoom")
X81P = os.path.join(REB, "X81_core_convergence", "x80_core_convergence.py"); argv0 = sys.argv; sys.argv = [X81P]
src = open(X81P).read(); src = src[:src.index("# K1: exact smooth core")]; NS = dict(__file__=X81P, __name__="x81_prefix"); exec(compile(src, X81P, "exec"), NS); sys.argv = argv0
import numpy as np
fit, a_fit, M_nfw, eta_of = NS["fit"], NS["a_fit_profile"], NS["M_nfw"], NS["eta_of"]; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("X80 converged-cusp eta (exact NFW at each run's c_nfw, x_c 0.001); kappa = 1/2 FITTED; footings never pooled; not theory closed")
runs, S = {}, {}
for M in (1e10, 1e11, 1e12):
    for ng in (64, 48):
        v = []; nf = 0
        for s in range(1, 10):
            k = f"M{M:.0e}".replace("+", "") + f"_s{s}_ng{ng}"; sn = os.path.join(X48, "runs", k, "snap_zf.npz")
            if not os.path.exists(sn): continue
            Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"])); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
            o, res = fit(x, m, rho, meta["eps"]); c = o.get("c_nfw_fit") if res is not None else None
            if not c: nf += 1; runs[k] = dict(flag=o.get("flag"), c_nfw=c); continue
            e = float(eta_of(a_fit(M_nfw(c), 0.001))); v.append(e); runs[k] = dict(c_nfw=c, eta_conv=e, eta_cut=res["S"]["eta"], xc=o["rconv"] / o["rvir"], zf=meta["zf"])
        if not v: continue
        v = np.array(v); b = np.median(v[np.random.default_rng(20261030).integers(0, len(v), (10000, len(v)))], axis=1)
        S[f"{M:.0e}_ng{ng}"] = dict(n=len(v), n_flagged=nf, med=float(np.median(v)), p16=float(np.percentile(b, 16)), p84=float(np.percentile(b, 84)), per_run=v.tolist(), boot=b.tolist())
        P(f"  M {M:.0e} ng {ng} (n {len(v)}, flagged {nf}): eta_conv {np.median(v):.2f} [68% {np.percentile(b, 16):.2f}, {np.percentile(b, 84):.2f}]")
K = "1e+12_ng64" in S and abs(S["1e+12_ng64"]["med"] - 25.94) <= 0.01; P(f"K 1e12 ng 64 vs X81 and CE1's 25.94: {S.get('1e+12_ng64', {}).get('med', float('nan')):.4f}: {'PASS' if K else 'FAIL'}")
RES = dict(amendment="X80 AMENDMENT A1", K=bool(K), runs=runs, summary={k: {q: w for q, w in v.items() if q != "boot"} for k, v in S.items()})
a, b, c = S.get("1e+10_ng64"), S.get("1e+11_ng64"), S.get("1e+12_ng64")
if a and b and c and a["n"] >= 6 and b["n"] >= 6:
    G = np.random.default_rng(20261030); med = lambda A: np.median(np.array(A["per_run"])[G.integers(0, A["n"], (10000, A["n"]))], axis=1); den = med(c)
    r10, r11 = a["med"] / c["med"], b["med"] / c["med"]; l10, h10 = np.percentile(med(a) / den, [16, 84]); l11, h11 = np.percentile(med(b) / den, [16, 84])
    cl = lambda r: "N OVER" if r > 1.9 else "N SHORT" if r < 1.1 else "N IN WINDOW"; lab = cl(r10); lab += " [NOISE-LIMITED]" if cl(l10) != lab or cl(h10) != lab else ""
    RES.update(r10=r10, r11=r11, r10_68=[float(l10), float(h10)], r11_68=[float(l11), float(h11)], reading=lab, s10_12=math.log10(r10) / 2, s11_12=math.log10(r11)); P(f"rho10 {r10:.3f} [{l10:.3f}, {h10:.3f}], rho11 {r11:.3f} [{l11:.3f}, {h11:.3f}]; slope per dex 1e10-1e12 {math.log10(r10) / 2:.4f}, 1e11-1e12 {math.log10(r11):.4f}; READING: {lab}")
else: RES["reading"] = "NOT YET: fewer than 6 of 9 ng 64 seeds at 1e10 or 1e11"; P(f"READING: {RES['reading']}")
json.dump(RES, open(os.path.join(HERE, "x80_converged.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "x80_converged.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if K else 1)
