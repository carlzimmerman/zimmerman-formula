#!/usr/bin/env python3
"""KT15: filtered QUMOND (phantom sourced by rho smoothed over xi) on Local Group dwarfs, McConnachie 2012. Arms A0 xi = 0, A1 xi = 2 kpc, A2 xi = eps r_M. python3 kt15.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "../../real_research/data/dsph/mcconnachie2012_dsph.csv")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
G = 4.30091e-6; CONV = 3.0857e19 / 1e6; A0 = {"canonical": 9.3603e-11 * CONV, "alt": 1.1312e-10 * CONV}; UPS = np.linspace(1, 3, 41)
nu = (lambda y: np.ones_like(y)) if MUT else (lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth(r, rho, s):
    if s <= 0: return rho
    R, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * s * R)) * (np.exp(-(R - Rp) ** 2 / (2 * s * s)) - np.exp(-(R + Rp) ** 2 / (2 * s * s)))
    return np.trapz(K * rho[None, :], r, axis=1)
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; m = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]); return m + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, xi, a0, ge=0.0):
    r = rgrid(a, xi); rho = plummer(r, M, a); gN = G * menc(r, rho) / r ** 2; gh = gN if xi <= 0 else G * menc(r, smooth(r, rho, xi)) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M)), r, rho
# checks
a0 = A0["alt"]; s, _, _ = sig_los(1e6, 2.0, 0.0, a0); ex = (4 / 81 * G * 1e6 * a0) ** 0.25; e1 = abs(s / ex - 1); ok = e1 <= 0.03 or MUT; fail += not ok; P(f"C1 deep-MOND estimator: sigma {s:.4f} vs {ex:.4f}, rel {e1:.4f}: {'PASS' if ok else 'FAIL'}")
for xi in (0.05, 0.5, 2.0):
    r = rgrid(0.3, xi); rho = plummer(r, 1e7, 0.3); m0 = menc(r, rho)[-1]; m1 = menc(r, smooth(r, rho, xi))[-1]; e2 = abs(m1 / m0 - 1)
    w = 0.4; rg = rho * 0 + np.exp(-r ** 2 / (2 * w * w)); sm = smooth(r, rg, xi); exg = (w / math.hypot(w, xi)) ** 3 * np.exp(-r ** 2 / (2 * (w * w + xi * xi))); e3 = float(np.max(np.abs(sm - exg)))
    ok = e2 <= 1e-3 and e3 <= 1e-3; fail += not ok; P(f"C2/C3 xi {xi}: mass ratio - 1 {m1 / m0 - 1:+.1e}; Gaussian width max abs err {e3:.1e}: {'PASS' if ok else 'FAIL'}")
rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
P(f"sample {len(rows)}: " + ", ".join(r["name"].split(" (")[0] for r in rows))
rM = lambda M, a0: math.sqrt(G * M / a0); EPS = 2.0 / rM(7.0e10, A0["alt"]); P(f"A2 eps = 2.0 / r_M,MW ({rM(7.0e10, A0['alt']):.2f} kpc) = {EPS:.4f}")
ARMS = [("A0", "canonical", lambda M, a0: 0.0), ("A0", "alt", lambda M, a0: 0.0), ("A1", "alt", lambda M, a0: 2.0), ("A2", "alt", lambda M, a0: EPS * rM(M, a0))]
for arm, foot, xif in ARMS:
    a0 = A0[foot]
    for case in ("EFE", "isolated"):
        k = f"{arm}|{foot}|{case}"; res = []; n = 0
        for d in rows:
            ge = (200.0 ** 2 / d["D"]) if (case == "EFE" and d["sub"] == "MW") else 0.0; sp = []
            for u in UPS:
                M = u * d["L"] + 1.33 * d["MHI"]; sp.append(sig_los(M, d["a"], xif(M, a0), a0, ge)[0])
            sp = np.array(sp); ok = np.abs(sp - d["s"]) <= 2 * d["e"]; ups_ok = UPS[ok]; n += bool(ok.any())
            res.append(dict(name=d["name"], obs=d["s"], e=d["e"], pred_U1=float(sp[0]), pred_U2=float(sp[20]), pred_U3=float(sp[-1]), xi_U2=float(xif(2 * d["L"] + 1.33 * d["MHI"], a0)), passed=bool(ok.any()), ups=[float(ups_ok.min()), float(ups_ok.max())] if ok.any() else None))
        RES[k] = dict(n_pass=n, n=len(rows), rows=res); P(f"\n[{k}] pass {n}/{len(rows)}")
        for x in res: P(f"   {x['name'][:22]:22s} obs {x['obs']:5.1f}+-{x['e']:.1f}  pred U1/2/3 {x['pred_U1']:5.1f} {x['pred_U2']:5.1f} {x['pred_U3']:5.1f}  xi {x['xi_U2']:.3f}  {'PASS ' + str([round(v, 2) for v in x['ups']]) if x['passed'] else 'fail'}")
for case in ("EFE", "isolated"):
    ref = RES[f"A0|alt|{case}"]["n_pass"]
    for arm in ("A1", "A2"):
        n = RES[f"{arm}|alt|{case}"]["n_pass"]; lab = "KILLED BY DSPH" if n <= ref / 2 else "SURVIVES DSPH" if n >= ref - 2 else "HURT"; RES[f"label|{arm}|{case}"] = lab; P(f"LABEL {arm} {case}: {lab} ({n} vs A0-alt {ref})")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt15{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt15{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
