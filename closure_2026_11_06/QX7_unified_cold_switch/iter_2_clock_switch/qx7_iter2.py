#!/usr/bin/env python3
"""QX7 iter_2 (criteria d9d76d87a2): clock-switched cold dark energy, lambda_J(a) = lambda_3 (a/a_3)^m (physical).
    python3 qx7_iter2.py            # graded: qx7_iter2.json / .out
    python3 qx7_iter2.py --mutate   # MUTATE 1 (G3b flipped), 2 (f_cap = 0), 3 (f_cap x 3): qx7_iter2_MUTATE.*
G2' reuses QX3 iter3's solver (beta = -m/3, mu0 = 2 pi a_3^m / lambda_3). kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter2_MUTATE" if MUT else "qx7_iter2"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
DATA = os.path.join(REPO, "real_research", "data")

# ---- QX5 samples (X-COP, groups) ----
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
exec(compile(src[:cut], Q5, "exec"), NS); sys.argv = argv0
G, MS, KPC, C, A0, glaw, XC, GR = (NS[k] for k in ("G", "MS", "KPC", "C", "A0", "glaw", "XC", "GR"))

# ---- QX3 iter3 solver (executed up to its K check; defines g2(beta, mu0), ob, od, H0, h, GMSUN, rho_m0) ----
D3 = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter3_barotropic_family")
s3 = open(os.path.join(D3, "iter3.py")).read(); c3 = s3.index("# K: beta = 0")
cwd = os.getcwd(); os.chdir(D3); env_m = os.environ.pop("QX3_MUTATE", None)
N3 = {"__file__": os.path.join(D3, "iter3.py"), "__name__": "iter3_reused"}
exec(compile(s3[:c3], os.path.join(D3, "iter3.py"), "exec"), N3); os.chdir(cwd)
g2, ob, od, H0, h, GMSUN, rho_m0, I2, it2 = (N3[k] for k in ("g2", "ob", "od", "H0", "h", "GMSUN", "rho_m0", "I2", "it2"))
R = od / ob; FCAP = 0.76; A3 = 0.25
P(f"QX7 iter2 {TAG}: background omega_b {ob} omega_d {od:.4f} H0 {H0}; R = omega_d/omega_b = {R:.3f}; f_cap {FCAP}")

def r_ta(M, zc):  # Mpc physical, iter3's convention
    return (M / (4 * math.pi / 3 * 5.55 * rho_m0 * (1 + zc) ** 3)) ** (1 / 3)
def lam(l3, m, z): return l3 * ((1 / (1 + z)) / A3) ** m

# ---- law-obeying massive systems ----
ell = []
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
for r in rows[1:]:
    d = dict(zip(rows[0], r)); ell.append((d["name"], float(d["ups_krou"]) * float(d["LK_1e11"]) * 1e11))
sp = []
for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: nm = t[0]; L = float(t[7]); MHI = float(t[13]); q = int(t[17]); inc = float(t[5])
    except ValueError: continue
    if q <= 2 and inc >= 30: sp.append((nm, (0.5 * L + 1.33 * MHI) * 1e9))
sp = sorted(sp, key=lambda x: -x[1])[:5]
MASSIVE = ell + sp
P("  massive law-obeying systems (M_b): " + ", ".join(f"{n} {m:.2e}" for n, m in MASSIVE))
Mt_max = max(m for _, m in MASSIVE) * (1 + R)

def gates(l3, m, flipG3b=False, zc_b=2.0, mt_fac=1 + R):
    g4 = lam(l3, m, 3.0) <= (0.42 / h) / 4
    g3 = lam(l3, m, 2.0) >= r_ta(10 ** 11.5, 2.0)
    g3b_each = [lam(l3, m, zc_b) >= r_ta(mb * mt_fac, zc_b) for _, mb in MASSIVE]
    g3b = (not all(g3b_each)) if flipG3b else all(g3b_each)
    return g4, g3, g3b

ms = np.arange(0, 8.0001, 0.25); l3s = np.geomspace(1e-4, 0.2, 41)
cells = [(float(l3), float(m)) for m in ms for l3 in l3s if all(gates(l3, m, flipG3b=MUT))]
P(f"  analytic gates (G4' forest, G3' reference galaxy, G3b massive{' FLIPPED' if MUT else ''}): {len(cells)} of {len(ms) * len(l3s)} cells pass")
# sensitivity (no label): z_c for G3b in {1, 3}, and M_t = M_b
sens = {}
for zc_b in (1.0, 3.0):
    sens[f"zc{zc_b:g}"] = sum(all(gates(l3, m, zc_b=zc_b)) for m in ms for l3 in l3s)
sens["Mt_eq_Mb"] = sum(all(gates(l3, m, mt_fac=1.0)) for m in ms for l3 in l3s)
P(f"  sensitivity (cells passing analytic gates): G3b at z_c=1 {sens['zc1']}, z_c=3 {sens['zc3']}, M_t = M_b {sens['Mt_eq_Mb']}")

# ---- K1: m = 0 reproduces iter2's G2 at the same mu ----
gw = [g for g in it2["G2"] if g["corner"] == [ob, H0, N3["ns"]]][0]
rk = min(gw["rows"], key=lambda x: abs(math.log(x["mu"] / 1e3)))
l3_k = 2 * math.pi / rk["mu"]; d_k = g2(0.0, 2 * math.pi * A3 ** 0 / l3_k)
K1 = dict(mu=rk["mu"], iter2=rk["dchi2"], qx7=d_k, pass_=bool(abs(d_k - rk["dchi2"]) <= 1e-2 * max(1, abs(rk["dchi2"]))))
P(f"  K1 (m = 0 == iter2 G2 at mu {rk['mu']:.3g}): iter2 {rk['dchi2']:.4f} vs QX7 {d_k:.4f} -> {'PASS' if K1['pass_'] else 'FAIL'}")

RES = dict(tag=TAG, criteria="d9d76d87a2", R=R, f_cap=FCAP, massive=[dict(name=n, M_b=m) for n, m in MASSIVE],
           n_analytic=len(cells), sensitivity=sens, K1=K1, note="kappa = 1/2 FITTED; not theory closed")

# ---- G2' on analytic cells (all of them, or the first passing ones under MUTATE) ----
window = []; evaluated = []
order = sorted(cells, key=lambda c: (c[1], -c[0]))
for (l3, m) in order:
    d = g2(-m / 3.0, 2 * math.pi * A3 ** m / l3); evaluated.append(dict(lambda_3=l3, m=m, dchi2=d))
    if d <= I2.DCHI2_LINE: window.append(evaluated[-1])
    if MUT and window: break
P(f"  G2' evaluated on {len(evaluated)} cells; window (all gates) {len(window)} members" + (f"; closest dchi2 {min(e['dchi2'] for e in evaluated):.2f}" if evaluated else ""))
if window:
    P("  window m range %.2f-%.2f, lambda_3 %.2e-%.2e Mpc" % (min(w['m'] for w in window), max(w['m'] for w in window),
                                                       min(w['lambda_3'] for w in window), max(w['lambda_3'] for w in window)))
RES.update(evaluated=evaluated, window=window)

# ---- cluster predictions (no cluster input) ----
def predict_sets(l3, m, fcap):
    out = {}
    for f, a0 in A0.items():
        xd = []
        for z in XC:
            Mb_tot = z["Mb_last"][0]; cap = lam(l3, m, 0.5) < r_ta(Mb_tot * (1 + R), 0.5)
            Md = fcap * R * z["M_b"] if cap else 0.0
            rm = z["r_kpc"] * KPC; gN = G * (z["M_b"] + Md) * MS / rm ** 2; Mp = glaw(gN, a0) * rm ** 2 / G / MS
            xd.append(math.log10(z["M_obs"] / Mp))
        xd = np.array(xd); ncapX = None
        grp = {}
        for fst in (0.0, 1.0):
            npass = 0; dl = []; ncap = 0
            for gp in GR:
                Mb5 = gp["g5"] * (1 + fst); cap = lam(l3, m, 1.0) < r_ta(Mb5 * (1 + R), 1.0); ncap += cap; ok = True
                for p in gp["pts"]:
                    Mb = p["M_gas"] * (1 + fst); Md = fcap * R * Mb if cap else 0.0
                    rm = p["r_kpc"] * KPC; Mp = glaw(G * (Mb + Md) * MS / rm ** 2, a0) * rm ** 2 / G / MS
                    dlt = math.log10(p["M_obs"] / Mp); sl = p["eM"] / (p["M_obs"] * math.log(10)); dl.append(dlt)
                    ok &= abs(dlt) <= 2 * sl
                npass += ok
            grp[f"fst{fst:g}"] = dict(n_pass=npass, median_delta=float(np.median(dl)), n_captured=int(ncap), pass_=bool(npass >= 16))
        xcap = sum(lam(l3, m, 0.5) < r_ta(z["Mb_last"][0] * (1 + R), 0.5) for z in XC)
        out[f] = dict(X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())), X_pass=bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10),
                      X_points_captured=int(xcap), groups=grp, groups_pass_strict=bool(all(g["pass_"] for g in grp.values())),
                      groups_pass_either=bool(any(g["pass_"] for g in grp.values())))
    return out

if not MUT:
    preds = []
    for w in window:
        pr = predict_sets(w["lambda_3"], w["m"], FCAP); preds.append(dict(member=w, pred=pr))
    RES["predictions"] = preds
    for f in A0:
        if preds:
            xm = [p["pred"][f]["X_mean"] for p in preds]; xr = [p["pred"][f]["X_rms"] for p in preds]
            xp = sum(p["pred"][f]["X_pass"] for p in preds); gs = sum(p["pred"][f]["groups_pass_strict"] for p in preds)
            ge = sum(p["pred"][f]["groups_pass_either"] for p in preds); both = sum(p["pred"][f]["X_pass"] and p["pred"][f]["groups_pass_strict"] for p in preds)
            P(f"  [{f}] over {len(preds)} window members: X-COP mean {min(xm):+.3f}..{max(xm):+.3f}, rms {min(xr):.3f}..{max(xr):.3f}; X-COP pass {xp}; groups strict pass {gs} (either-allowance {ge}); both {both}")
            g0 = [p["pred"][f]["groups"]["fst0"] for p in preds]; g1 = [p["pred"][f]["groups"]["fst1"] for p in preds]
            P(f"        groups captured {min(g['n_captured'] for g in g0)}..{max(g['n_captured'] for g in g0)}/20; n_pass fst0 {min(g['n_pass'] for g in g0)}..{max(g['n_pass'] for g in g0)}, fst1 {min(g['n_pass'] for g in g1)}..{max(g['n_pass'] for g in g1)}; median delta fst0 {min(g['median_delta'] for g in g0):+.3f}..{max(g['median_delta'] for g in g0):+.3f}")
            RES[f] = dict(n_members=len(preds), X_pass_members=xp, groups_strict_members=gs, both_members=both)
    # galaxy-side recheck: hot dust at the cosmic mean near the Sun
    rho_d0 = od / h ** 2 * 3 * (H0 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G); AU = 1.496e11
    ratio = (4 * math.pi / 3) * G * rho_d0 * AU / (G * 1.989e30 / AU ** 2)
    RES["solar_ratio"] = ratio; P(f"  Solar recheck: g_d(1 AU)/g_N = {ratio:.2e} (line 1e-15) -> {'PASS' if ratio <= 1e-15 else 'FAIL'}")
    if not window: lab = "FAIL (no window: no member passes G2', G3', G3b and G4')"
    else:
        okf = {f: RES[f]["both_members"] > 0 for f in A0}
        allf = {f: RES[f]["both_members"] == len(window) for f in A0}
        lab = ("PASS" if all(okf.values()) else "FAIL (clusters)") + f" [members passing X-COP+groups: " + ", ".join(f"{f} {RES[f]['both_members']}/{len(window)}" for f in A0) + "]"
    RES["label"] = lab; P(f"  LABEL: {lab}")
else:
    RES["MUTATE1_bites"] = bool(len(window) > 0); P(f"  MUTATE 1 (G3b flipped): {len(window)} member(s) pass all gates -> {'BITES' if window else 'NO BITE'}")
    # MUTATE 2 and 3 on an arbitrary capturing member (lambda_3 small, m = 0): everything captured
    l3c, mc = 1e-4, 0.0
    p0 = predict_sets(l3c, mc, 0.0); p1 = predict_sets(l3c, mc, FCAP); p3 = predict_sets(l3c, mc, 3 * FCAP)
    for f, ref in (("canonical", 0.4675), ("alt", 0.4345)):
        b2 = abs(p0[f]["X_mean"] - ref) <= 1e-3; mv = p1[f]["X_mean"] - p3[f]["X_mean"]; b3 = abs(mv) > 0.1
        RES[f"MUTATE2_{f}"] = dict(X_mean=p0[f]["X_mean"], ref=ref, bites=bool(b2)); RES[f"MUTATE3_{f}"] = dict(move=mv, bites=bool(b3))
        P(f"  [{f}] MUTATE 2 (f_cap = 0): X-COP mean {p0[f]['X_mean']:+.4f} vs QX2 {ref:+.4f} -> {'BITES' if b2 else 'NO BITE'}; MUTATE 3 (f_cap x3): move {mv:+.3f} -> {'BITES' if b3 else 'NO BITE'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
