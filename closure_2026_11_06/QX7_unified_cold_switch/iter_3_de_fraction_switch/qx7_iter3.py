#!/usr/bin/env python3
"""QX7 iter_3 (criteria f9020230b6): cold dark energy heated by the dark-energy fraction, lambda_J = lambda_* Omega_DE(a)^p.
    python3 qx7_iter3.py            # graded: qx7_iter3.json / .out
    python3 qx7_iter3.py --mutate   # MUTATE 1 (massive M_b x 10), 2 (f_cap = 0), 3 (f_cap x 3): qx7_iter3_MUTATE.*
G2' uses QX3 iter3's ODE generalised to any k_J(a) (K1 against iter3's g2). kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter3_MUTATE" if MUT else "qx7_iter3"; OUT = []
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
P(f"QX7 iter3 {TAG}: background omega_b {ob} omega_d {od:.4f} H0 {H0}; R = omega_d/omega_b = {R:.3f}; f_cap {FCAP}")

def r_ta(M, zc):  # Mpc physical, iter3's convention
    return (M / (4 * math.pi / 3 * 5.55 * rho_m0 * (1 + zc) ** 3)) ** (1 / 3)
MC = N3["M"]; OL0 = MC.Omega_Lambda(); H0c_ = MC.Hubble(0.0)
def ode(z): return OL0 / (MC.Hubble(z) / H0c_) ** 2
_zt = np.linspace(0, 3500, 1); 
def lam(l3, m, z): return l3 * ode(z) ** m          # here l3 = lambda_*, m = p
P(f"  Omega_DE(z): z=0 {ode(0):.3f}, 0.5 {ode(0.5):.3f}, 1 {ode(1):.3f}, 2 {ode(2):.4f}, 3 {ode(3):.4f}")

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

MBFAC = 10.0 if MUT else 1.0
def gates(l3, m, flipG3b=False, zc_b=2.0, mt_fac=1 + R, mbfac=1.0):
    g4 = lam(l3, m, 3.0) <= (0.42 / h) / 4
    g3 = lam(l3, m, 2.0) >= r_ta(10 ** 11.5, 2.0)
    g3b_each = [lam(l3, m, zc_b) >= r_ta(mb * mbfac * mt_fac, zc_b) for _, mb in MASSIVE]
    g3b = (not all(g3b_each)) if flipG3b else all(g3b_each)
    return g4, g3, g3b

ms = np.arange(0, 6.0001, 0.125); l3s = np.geomspace(1e-3, 1e3, 61)
cells0 = [(float(l3), float(m)) for m in ms for l3 in l3s if all(gates(l3, m))]
cells = cells0 if not MUT else [(float(l3), float(m)) for m in ms for l3 in l3s if all(gates(l3, m, mbfac=MBFAC))]
P(f"  analytic gates (G4' forest, G3' reference galaxy, G3b massive{' M_b x10' if MUT else ''}): {len(cells)} of {len(ms) * len(l3s)} cells pass (unmutated {len(cells0)})")
# sensitivity (no label): z_c for G3b in {1, 3}, and M_t = M_b
sens = {}
for zc_b in (1.0, 3.0):
    sens[f"zc{zc_b:g}"] = sum(all(gates(l3, m, zc_b=zc_b)) for m in ms for l3 in l3s)
sens["Mt_eq_Mb"] = sum(all(gates(l3, m, mt_fac=1.0)) for m in ms for l3 in l3s)
P(f"  sensitivity (cells passing analytic gates): G3b at z_c=1 {sens['zc1']}, z_c=3 {sens['zc3']}, M_t = M_b {sens['Mt_eq_Mb']}")

# ---- generalised G2' solver (QX3 iter3's ODE, any k_J(a)) ----
import math as _m
def solve_gen(kJ):
    lna_t, lnH_t, dlnH_t, H0c, Om_b0, Om_d0, ai, adec, lnz, kgrid, nk = (N3[k] for k in ("lna_t", "lnH_t", "dlnH_t", "H0c", "Om_b0", "Om_d0", "ai", "adec", "lnz", "kgrid", "nk"))
    grid = np.unique(np.concatenate([np.linspace(_m.log(ai), 0.0, 6001), lnz]))
    y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai
    rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
    for n in range(len(grid) - 1):
        hh = grid[n + 1] - grid[n]; lna = 0.5 * (grid[n] + grid[n + 1]); a = _m.exp(lna)
        E2 = _m.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c**2; dl = float(np.interp(lna, lna_t, dlnH_t))
        Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; on = a > adec
        jeans = (kgrid / (a * kJ(a))) ** 2
        A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od * (1 - jeans); A[:, 1, 1] = -(2 + dl)
        if on:
            A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * hh * A, ((I4 + 0.5 * hh * A) @ y[:, :, None]))[:, :, 0]
        t = float(grid[n + 1])
        if t in tset: rec[tset[t]] = y.copy()
    zgrid = N3["zgrid"]; dm = np.empty((nk, len(zgrid)))
    for jz in range(len(zgrid)):
        yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = _m.exp(2 * np.interp(_m.log(a), lna_t, lnH_t)) / H0c**2
        Od = Om_d0 * a**-3 / E2; Ob = Om_b0 * a**-3 / E2; dm[:, jz] = (Od * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
    return dm
def g2gen(kJ):
    Rr = solve_gen(kJ) / N3["ref"]; S = I2.limber_ratio(MC, H0, N3["kgrid"], N3["zgrid"], Rr); c, _ = I2.best_amp_chi2(N3["X0"] * S)
    return float(c - N3["c0"])
# Omega_DE on the solver's a-grid via interpolation (CLASS H(z) per call is slow)
_lza = np.linspace(_m.log(1 / 3500.0), 0.0, 3000); _ode = np.array([ode(1 / _m.exp(x) - 1) for x in _lza])
def kJ_of(l3, m): return lambda a: 2 * np.pi / (l3 * float(np.interp(_m.log(a), _lza, _ode)) ** m)
d_iter3 = g2(-1.0, 1e3); d_gen = g2gen(lambda a: 1e3 * a ** -3.0)
K1 = dict(beta=-1.0, mu0=1e3, iter3=d_iter3, generalised=d_gen, pass_=bool(abs(d_iter3 - d_gen) <= 1e-6 * max(1.0, abs(d_iter3))))
d3b = g2(-1.0, 1.0); dgb = g2gen(lambda a: 1.0 * a ** -3.0); K1["extra_beta-1_mu1"] = [d3b, dgb]
P(f"  K1b (reported, not frozen: same at mu0 1, a non-trivial point): {d3b:.4f} vs {dgb:.4f}")
P(f"  K1 (generalised solver == iter3 g2 at beta -1, mu0 1e3): {d_iter3:.6f} vs {d_gen:.6f} -> {'PASS' if K1['pass_'] else 'FAIL'}")
RES = dict(tag=TAG, criteria="f9020230b6", R=R, f_cap=FCAP, massive=[dict(name=n, M_b=m) for n, m in MASSIVE],
           n_analytic=len(cells), sensitivity=sens, K1=K1, note="kappa = 1/2 FITTED; not theory closed")

# ---- G2' on analytic cells (all of them, or the first passing ones under MUTATE) ----
window = []; evaluated = []
order = sorted(cells, key=lambda c: (c[1], -c[0]))
for (l3, m) in (order if not MUT else []):
    d = g2gen(kJ_of(l3, m)); evaluated.append(dict(lambda_star=l3, p=m, dchi2=d))
    if d <= I2.DCHI2_LINE: window.append(evaluated[-1])
    if MUT and window: break
P(f"  G2' evaluated on {len(evaluated)} cells; window (all gates) {len(window)} members" + (f"; closest dchi2 {min(e['dchi2'] for e in evaluated):.2f}" if evaluated else ""))
if window:
    P("  window p range %.3f-%.3f, lambda_* %.2e-%.2e Mpc" % (min(w['p'] for w in window), max(w['p'] for w in window),
                                                       min(w['lambda_star'] for w in window), max(w['lambda_star'] for w in window)))
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
        pr = predict_sets(w["lambda_star"], w["p"], FCAP); preds.append(dict(member=w, pred=pr))
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
    # sensitivity of the cluster stage to the assembly epochs (no label)
    if window:
        sensp = {}
        for zx, zg in ((0.3, 0.5), (1.0, 2.0)):
            pass_n = 0
            for w in window:
                ok = True
                for f, a0 in A0.items():
                    xd = []
                    for z in XC:
                        cap = lam(w["lambda_star"], w["p"], zx) < r_ta(z["Mb_last"][0] * (1 + R), zx); Md = FCAP * R * z["M_b"] if cap else 0.0
                        rm = z["r_kpc"] * KPC; Mp = glaw(G * (z["M_b"] + Md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; xd.append(math.log10(z["M_obs"] / Mp))
                    xd = np.array(xd); ok &= bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10)
                pass_n += ok
            sensp[f"zX{zx}_zG{zg}"] = pass_n
        RES["sensitivity_cluster_epochs_Xpass"] = sensp; P(f"  sensitivity (no label): members passing X-COP both footings at other epochs: {sensp}")
        okf = {f: RES[f]["both_members"] > 0 for f in A0}
        allf = {f: RES[f]["both_members"] == len(window) for f in A0}
        lab = ("PASS" if all(okf.values()) else "FAIL (clusters)") + f" [members passing X-COP+groups: " + ", ".join(f"{f} {RES[f]['both_members']}/{len(window)}" for f in A0) + "]"
    RES["label"] = lab; P(f"  LABEL: {lab}")
else:
    b1 = set(cells) < set(cells0); RES["MUTATE1_bites"] = bool(b1); RES["MUTATE1_cells"] = [len(cells0), len(cells)]
    P(f"  MUTATE 1 (massive M_b x10): analytic cells {len(cells0)} -> {len(cells)} -> {'BITES' if b1 else 'NO BITE'}")
    # MUTATE 2 and 3 on an arbitrary capturing member (lambda_3 small, m = 0): everything captured
    l3c, mc = 1e-3, 0.0
    p0 = predict_sets(l3c, mc, 0.0); p1 = predict_sets(l3c, mc, FCAP); p3 = predict_sets(l3c, mc, 3 * FCAP)
    for f, ref in (("canonical", 0.4675), ("alt", 0.4345)):
        b2 = abs(p0[f]["X_mean"] - ref) <= 1e-3; mv = p1[f]["X_mean"] - p3[f]["X_mean"]; b3 = abs(mv) > 0.1
        RES[f"MUTATE2_{f}"] = dict(X_mean=p0[f]["X_mean"], ref=ref, bites=bool(b2)); RES[f"MUTATE3_{f}"] = dict(move=mv, bites=bool(b3))
        P(f"  [{f}] MUTATE 2 (f_cap = 0): X-COP mean {p0[f]['X_mean']:+.4f} vs QX2 {ref:+.4f} -> {'BITES' if b2 else 'NO BITE'}; MUTATE 3 (f_cap x3): move {mv:+.3f} -> {'BITES' if b3 else 'NO BITE'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
