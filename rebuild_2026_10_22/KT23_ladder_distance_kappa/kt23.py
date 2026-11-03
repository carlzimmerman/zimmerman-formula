#!/usr/bin/env python3
"""KT23: kappa from SPARC outer rotation curves, ladder distances only (TRGB, Cepheid, SN), per-galaxy a0 solved with the
board law's simple nu. python3 kt23.py [--mutate]. kappa = 1/2 FITTED in the record; not theory closed."""
import glob, json, math, os, sys
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); DD = os.path.join(HERE, "../../real_research/data"); MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
CONV = 1e6 / 3.0857e19; A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; ND = 400; NB = 2000
NU = {"simple": lambda y: 0.5 + np.sqrt(0.25 + 1 / y), "standard": lambda y: np.sqrt((1 + np.sqrt(1 + 4 / y ** 2)) / 2)}
tab = {}
for line in open(os.path.join(DD, "SPARC_Lelli2016c.mrt")):
    p = line.split()
    if len(p) >= 18 and p[1].isdigit(): tab[p[0]] = dict(D=float(p[2]), eD=float(p[3]), fD=int(p[4]), inc=float(p[5]), einc=float(p[6]), Rd=float(p[11]), Vf=float(p[15]), Q=int(p[17]))
GAL = []
for fn in sorted(glob.glob(os.path.join(DD, "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", ""); t = tab.get(nm)
    if t is None or t["Q"] > 2 or t["inc"] < 30 or t["Vf"] <= 0: continue
    d = np.genfromtxt(fn, comments="#")
    if d.ndim != 2 or d.shape[1] < 6: continue
    d = d[np.argsort(d[:, 0])]; d = d[(d[:, 0] > 0) & (d[:, 1] > 0) & (d[:, 2] / np.maximum(d[:, 1], 1e-9) < 0.1)]
    if len(d) < 4: continue
    k = max(3, int(math.ceil(0.3 * len(d)))); o = d[-k:]; sl = np.polyfit(np.log(o[:, 0]), np.log(o[:, 1]), 1)[0]
    if abs(sl) >= 0.15 or o[-1, 0] <= 2 * t["Rd"]: continue
    GAL.append(dict(name=nm, R=o[:, 0], V=o[:, 1], G2=o[:, 3] * np.abs(o[:, 3]), D2=o[:, 4] * np.abs(o[:, 4]), B2=o[:, 5] * np.abs(o[:, 5]), **t))
def gb_go(g, f=1.0, sinr=1.0, ud=0.5, ub=0.7, gas=1.33):
    R = g["R"] * f; Vb2 = (gas / 1.33 * g["G2"] + ud * g["D2"] + ub * g["B2"]) * f; go = (g["V"] * sinr) ** 2 / R * CONV; gb = Vb2 / R * CONV
    return gb, (gb if MUT else go)
def solve(gb, go, nu):
    ok = gb > 0; gb, go = gb[ok], go[ok]
    F = lambda la: float(np.sum(np.log(go) - np.log(nu(gb / math.exp(la)) * gb)))
    a, b = math.log(1e-12), math.log(1e-8)
    if F(a) * F(b) > 0: return None
    return brentq(F, a, b, xtol=1e-12)
def sample(sel, nu, rng, **kw):
    """central ln a0_i, MC draws (ND per galaxy)."""
    cen, draws, names = [], [], []
    for g in sel:
        gb, go = gb_go(g, **kw); la = solve(gb, go, nu)
        if la is None: continue
        dr = []
        for _ in range(ND):
            f = max(rng.normal(g["D"], g["eD"]), 0.1 * g["D"]) / g["D"]; ip = min(max(rng.normal(g["inc"], g["einc"]), 15.0), 90.0); sr = math.sin(math.radians(g["inc"])) / math.sin(math.radians(ip)); u = 10 ** rng.normal(0, 0.1)
            gb2, go2 = gb_go(g, f * kw.get("f", 1.0), sr, kw.get("ud", 0.5) * u, kw.get("ub", 0.7) * u, kw.get("gas", 1.33)); l2 = solve(gb2, go2, nu); dr.append(l2 if l2 is not None else la)
        cen.append(la); draws.append(dr); names.append(g["name"])
    return np.array(cen), np.array(draws), names
def central(sel, nu, **kw):
    v = [solve(*gb_go(g, **kw), nu) for g in sel]; v = [x for x in v if x is not None]; return float(np.median(v)) if v else None
prim = [g for g in GAL if g["fD"] in (2, 3, 5)]; uma = [g for g in GAL if g["fD"] in (2, 3, 4, 5)]; hub = [g for g in GAL if g["fD"] == 1]
P(f"flat-outer galaxies: primary (TRGB/Cepheid/SN) {len(prim)}, with UMa {len(uma)}, Hubble flow {len(hub)}")
ok3 = len(prim) >= 12; fail += not ok3; P(f"C3 primary sample {len(prim)} >= 12: {'PASS' if ok3 else 'FAIL (NOT EVALUABLE)'}")
if MUT:
    v = [solve(*gb_go(g), NU["simple"]) for g in prim]; n = sum(x is None for x in v); P(f"MUTATE (g_obs = g_bar): {n}/{len(v)} galaxies have no a0 solution")
    RES.update(n_none=n, n=len(v)); open(os.path.join(HERE, "kt23_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "kt23_MUTATE.json"), "w"), indent=1); sys.exit(1)
# C1, C2
e1 = 0.0
for g in prim:
    gb, go = gb_go(g); la = solve(gb, go, NU["simple"]); m = gb > 0; e1 = max(e1, abs(float(np.sum(np.log(go[m]) - np.log(NU["simple"](gb[m] / math.exp(la)) * gb[m])))))
ok = e1 <= 1e-8; fail += not ok; P(f"C1 summed log residual at a0_i, max {e1:.1e}: {'PASS' if ok else 'FAIL'}")
e2 = 0.0
for g in prim:
    gb, _ = gb_go(g); m = gb > 0; la = solve(gb[m], NU["simple"](gb[m] / 1e-10) * gb[m], NU["simple"]); e2 = max(e2, abs(math.exp(la) / 1e-10 - 1))
ok = e2 <= 1e-6; fail += not ok; P(f"C2 injection a_inj 1e-10 recovered, max rel {e2:.1e}: {'PASS' if ok else 'FAIL'}")
yout = [float(gb_go(g)[0][-1] / A0F["canonical"]) for g in prim]; P(f"primary depth: y_out = g_bar(R_last)/a0_canonical median {np.median(yout):.3f}, range {min(yout):.3f}-{max(yout):.3f}")
def measure(sel, nu, tag, graded):
    rng = np.random.default_rng(20261103); cen, dr, names = sample(sel, nu, rng); n = len(cen); med = float(np.median(cen))
    bs = [float(np.median(dr[i, rng.integers(0, ND, n)])) for i in rng.integers(0, n, (NB, n))]
    st = float(np.std(bs)); var = np.var(dr, axis=1); w = 1 / np.maximum(var, 1e-6); wm = float(np.sum(w * cen) / np.sum(w))
    sy = {}
    for k, kws in (("upsilon", [dict(ud=0.5 * 10 ** 0.1, ub=0.7 * 10 ** 0.1), dict(ud=0.5 * 10 ** -0.1, ub=0.7 * 10 ** -0.1)]), ("gas1.40", [dict(gas=1.40)]), ("ladder3pct", [dict(f=1.03), dict(f=0.97)])):
        sy[k] = max(abs(central(sel, nu, **kw) - med) for kw in kws)
    sl = math.sqrt(st ** 2 + sum(v * v for v in sy.values())); a0m = math.exp(med); R = dict(n=n, ln_a0=med, a0=a0m, a0_wmean=math.exp(wm), sigma_stat=st, sys=sy, sigma_ln=sl, galaxies=names, ln_a0_i=cen.tolist())
    P(f"\n[{tag}] n {n}: a0 {a0m:.4e} m/s^2 (weighted mean {math.exp(wm):.4e}); sigma_ln stat {st:.3f}, sys " + ", ".join(f"{k} {v:.3f}" for k, v in sy.items()) + f"; total {sl:.3f}")
    for foot, af in A0F.items():
        kap = 0.5 * a0m / af; sk = kap * sl; z = (kap - 0.5) / sk; zv = (kap - 0.482) / sk
        lab = "1/2 CONSISTENT" if abs(z) <= 2 else "1/2 IN TENSION" if abs(z) <= 3 else "1/2 EXCLUDED"; res = "RESOLVES 1/2 FROM 0.482" if 0.018 > 2 * sk else "does not resolve 1/2 from 0.482"
        R[foot] = dict(kappa=kap, sigma=sk, z_half=z, z_0482=zv, label=lab if graded else "beside", resolve=res)
        P(f"[{tag}] {foot}: kappa {kap:.3f} +- {sk:.3f}; z(1/2) {z:+.2f}, z(0.482) {zv:+.2f}; {lab if graded else '(beside, not graded)'}; {res}")
    return R
if ok3:
    RES["primary"] = measure(prim, NU["simple"], "PRIMARY simple nu", True)
    RES["primary_standard_nu"] = measure(prim, NU["standard"], "beside: primary, standard nu", False)
    RES["with_UMa"] = measure(uma, NU["simple"], "beside: + Ursa Major", False)
    RES["hubble_flow_H0_73"] = measure(hub, NU["simple"], "beside: Hubble flow at H0 73 (a0 scales as H0^2)", False)
    c = RES["primary"]; P("primary galaxies: " + ", ".join(f"{n} {math.exp(l):.2e}" for n, l in zip(c["galaxies"], c["ln_a0_i"])))
RES["fail"] = fail; P(f"failed checks: {fail}")
open(os.path.join(HERE, "kt23.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "kt23.json"), "w"), indent=1)
sys.exit(1 if fail else 0)
