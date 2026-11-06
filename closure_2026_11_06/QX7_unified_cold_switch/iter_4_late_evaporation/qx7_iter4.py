#!/usr/bin/env python3
"""QX7 iter_4 (criteria 22af3e7b43): early capture allowed; today's dust in n = 1 cores of radius lambda_J(0)/2.
    python3 qx7_iter4.py            # graded: qx7_iter4.json / .out
    python3 qx7_iter4.py --mutate   # MUTATE 1 (lambda_0 = 1e-3 Mpc), 2 (f_cap = 0), 3 (f_cap x 3): qx7_iter4_MUTATE.*
lambda_J = lambda_* Omega_DE(a)^p (iter_3 switch); growth uses iter_3's generalised solver (executed from its source).
kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter4_MUTATE" if MUT else "qx7_iter4"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
DATA = os.path.join(REPO, "real_research", "data")

Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
exec(compile(src[:cut], Q5, "exec"), NS); sys.argv = argv0
G, MS, KPC, C, A0, glaw, XC, GR, LE, EL = (NS[k] for k in ("G", "MS", "KPC", "C", "A0", "glaw", "XC", "GR", "LE", "EL"))

D3 = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter3_barotropic_family")
s3 = open(os.path.join(D3, "iter3.py")).read(); c3 = s3.index("# K: beta = 0")
cwd = os.getcwd(); os.chdir(D3); os.environ.pop("QX3_MUTATE", None)
N3 = {"__file__": os.path.join(D3, "iter3.py"), "__name__": "iter3_reused"}
exec(compile(s3[:c3], os.path.join(D3, "iter3.py"), "exec"), N3); os.chdir(cwd)
g2, ob, od, H0, h, rho_m0, I2 = (N3[k] for k in ("g2", "ob", "od", "H0", "h", "rho_m0", "I2"))
# iter_3's generalised solver, executed from its own source
S3 = open(os.path.join(HERE, "..", "iter_3_de_fraction_switch", "qx7_iter3.py")).read()
blk = S3[S3.index("# ---- generalised G2' solver"):S3.index("d_iter3 = g2(")]
MC = N3["M"]; OL0 = MC.Omega_Lambda(); H0c_ = MC.Hubble(0.0)
def ode(z): return OL0 / (MC.Hubble(z) / H0c_) ** 2
LOC = dict(np=np, N3=N3, I2=I2, MC=MC, H0=H0, ode=ode); exec(blk, LOC); g2gen, kJ_of = LOC["g2gen"], LOC["kJ_of"]
K1 = dict(iter3=g2(-1.0, 1.0), generalised=g2gen(lambda a: 1.0 * a ** -3.0))
K1["pass_"] = bool(abs(K1["iter3"] - K1["generalised"]) <= 1e-6 * max(1, abs(K1["iter3"])))
R = od / ob; FCAP = 0.76; OD0 = ode(0.0)
P(f"QX7 iter4 {TAG}: R {R:.3f}, f_cap {FCAP}; Omega_DE(0) {OD0:.3f}; K1 (solver reuse, beta -1 mu0 1) {K1['iter3']:.4f} vs {K1['generalised']:.4f} -> {'PASS' if K1['pass_'] else 'FAIL'}")
MPC_M = 1e3 * KPC
def r_ta0(Mb): return (Mb * (1 + R) / (4 * math.pi / 3 * 5.55 * rho_m0)) ** (1 / 3)   # Mpc, z = 0
def encl(r_mpc, Rc):
    if r_mpc >= Rc: return 1.0
    xi = math.pi * r_mpc / Rc; return (math.sin(xi) - xi * math.cos(xi)) / math.pi
def Md(Mb_tot, r_mpc, lam0, fcap):
    Rc = lam0 / 2
    if Rc >= r_ta0(Mb_tot): return 0.0
    return fcap * R * Mb_tot * encl(r_mpc, Rc)

sp = []
for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: nm = t[0]; L = float(t[7]); MHI = float(t[13]); q = int(t[17]); inc = float(t[5])
    except ValueError: continue
    if q <= 2 and inc >= 30: sp.append((nm, (0.5 * L + 1.33 * MHI) * 1e9))
sp = sorted(sp, key=lambda x: -x[1])[:5]
G5SYS = [("reference", 1e10, 0.010)] + [(n, m, 0.020) for n, m in sp]

def lens_mean(a0, lam0, fcap):
    d = []
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G * p["Mb"] / p["gbar"]); md = Md(Mb, r / MPC_M, lam0, fcap)
        gp = glaw(p["gbar"] + G * md * MS / r ** 2, a0); d.append(math.log10(p["gobs"] / gp))
    return float(np.mean(d))
def ell_mean(a0, lam0, fcap):
    d = []
    for e in EL:
        Mbt = e["Mbar"](1e9)
        for mlt in (2, 4, 8):
            r = mlt * e["Re"]; rm = r * KPC; Mb = e["Mbar"](r); md = Md(Mbt, r / 1e3, lam0, fcap)
            Mp = glaw(G * (Mb + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; d.append(math.log10(e["Mtot"](r) / Mp))
    return float(np.mean(d))
BASE = {f: dict(L=lens_mean(a0, 1e9, 0.0), E=ell_mean(a0, 1e9, 0.0)) for f, a0 in A0.items()}

def gal_gates(lam0, fcap=FCAP):
    g5 = all(Md(Mb, ro, lam0, fcap) / Mb <= 0.3 for _, Mb, ro in G5SYS)
    g6 = all(abs(lens_mean(a0, lam0, fcap) - BASE[f]["L"]) <= 0.05 for f, a0 in A0.items())
    g7 = all(abs(ell_mean(a0, lam0, fcap) - BASE[f]["E"]) <= 0.15 for f, a0 in A0.items())
    return g5, g6, g7

def predict(lam0, fcap):
    out = {}
    for f, a0 in A0.items():
        xd = []
        for z in XC:
            md = Md(z["Mb_last"][0], z["r_kpc"] / 1e3, lam0, fcap); rm = z["r_kpc"] * KPC
            Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; xd.append(math.log10(z["M_obs"] / Mp))
        xd = np.array(xd); grp = {}
        for fst in (0.0, 1.0):
            npass = 0; dl = []
            for gp in GR:
                Mbt = gp["g5"] * (1 + fst); ok = True
                for p in gp["pts"]:
                    Mb = p["M_gas"] * (1 + fst); md = Md(Mbt, p["r_kpc"] / 1e3, lam0, fcap); rm = p["r_kpc"] * KPC
                    Mp = glaw(G * (Mb + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; dlt = math.log10(p["M_obs"] / Mp); dl.append(dlt)
                    ok &= abs(dlt) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
                npass += ok
            grp[f"fst{fst:g}"] = dict(n_pass=int(npass), median_delta=float(np.median(dl)), pass_=bool(npass >= 16))
        out[f] = dict(X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())), X_pass=bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10),
                      groups=grp, groups_strict=bool(all(g["pass_"] for g in grp.values())), groups_either=bool(any(g["pass_"] for g in grp.values())))
    return out

RES = dict(tag=TAG, criteria="22af3e7b43", R=R, f_cap=FCAP, K1=K1, baselines=BASE, note="kappa = 1/2 FITTED; not theory closed")
ps = np.arange(0, 6.0001, 0.125); l0s = np.geomspace(1e-3, 1e2, 61)
if not MUT:
    # galaxy gates depend on lambda_0 only; forest and growth on (lambda_0, p)
    galok = {}
    for l0 in l0s: galok[float(l0)] = gal_gates(l0)
    l0_gal = [l0 for l0, g in galok.items() if all(g)]
    P(f"  galaxy gates G5/G6/G7 pass for lambda_0 in {len(l0_gal)}/61 values" + (f": {min(l0_gal):.3g}-{max(l0_gal):.3g} Mpc" if l0_gal else ""))
    RES["galaxy_gates_by_lambda0"] = {f"{k:.4g}": list(map(bool, v)) for k, v in galok.items()}
    cells = []
    for p in ps:
        for l0 in l0_gal:
            lst = l0 / OD0 ** p
            if lst * ode(3.0) ** p <= (0.42 / h) / 4: cells.append((float(l0), float(p), float(lst)))
    P(f"  + forest G4': {len(cells)} cells")
    evaluated = []; window = []
    for (l0, p, lst) in sorted(cells, key=lambda c: (c[0], c[1])):
        d = g2gen(kJ_of(lst, p)); evaluated.append(dict(lambda_0=l0, p=p, lambda_star=lst, dchi2=d))
        if d <= I2.DCHI2_LINE: window.append(evaluated[-1])
    P(f"  G2' on {len(evaluated)} cells: window {len(window)}" + (f"; closest dchi2 {min(e['dchi2'] for e in evaluated):.2f}" if evaluated else ""))
    RES.update(evaluated=evaluated, window=window)
    preds = [dict(member=w, pred=predict(w["lambda_0"], FCAP)) for w in window]; RES["predictions"] = preds
    # report cluster predictions also over the galaxy-gate lambda_0 range regardless of growth (no label)
    RES["cluster_vs_lambda0_galaxyok"] = {f"{l0:.4g}": predict(l0, FCAP) for l0 in l0_gal}
    for l0 in l0_gal:
        pr = RES["cluster_vs_lambda0_galaxyok"][f"{l0:.4g}"]
        P(f"   lambda_0 {l0:.3g} Mpc (galaxy-ok): " + "; ".join(f"{f} X {pr[f]['X_mean']:+.3f}/{pr[f]['X_rms']:.3f} groups fst0 {pr[f]['groups']['fst0']['n_pass']} fst1 {pr[f]['groups']['fst1']['n_pass']} (med {pr[f]['groups']['fst0']['median_delta']:+.2f})" for f in A0))
    if not window: lab = "FAIL (no window)"
    else:
        both = {f: sum(p["pred"][f]["X_pass"] and p["pred"][f]["groups_strict"] for p in preds) for f in A0}
        lab = ("PASS" if all(v > 0 for v in both.values()) else "FAIL (clusters)") + " [" + ", ".join(f"{f} {both[f]}/{len(preds)}" for f in A0) + "]"
    RES["label"] = lab; P(f"  LABEL: {lab}")
else:
    g = gal_gates(1e-3); b1 = not (g[0] and g[1]); RES["MUTATE1"] = dict(gates=list(map(bool, g)), bites=bool(b1))
    P(f"  MUTATE 1 (lambda_0 1e-3 Mpc): G5 {g[0]} G6 {g[1]} G7 {g[2]} -> {'BITES' if b1 else 'NO BITE'}")
    p0 = predict(1e-3, 0.0); lb = {f: dict(L=lens_mean(a0, 1e-3, 0.0), E=ell_mean(a0, 1e-3, 0.0)) for f, a0 in A0.items()}
    for f, ref in (("canonical", 0.4675), ("alt", 0.4345)):
        b2 = abs(p0[f]["X_mean"] - ref) <= 1e-3 and lb[f]["L"] == BASE[f]["L"] and lb[f]["E"] == BASE[f]["E"]
        mv = predict(0.1, FCAP)[f]["X_mean"] - predict(0.1, 3 * FCAP)[f]["X_mean"]; b3 = abs(mv) > 0.1
        RES[f"MUTATE2_{f}"] = dict(X_mean=p0[f]["X_mean"], bites=bool(b2)); RES[f"MUTATE3_{f}"] = dict(move=mv, bites=bool(b3))
        P(f"  [{f}] MUTATE 2 (f_cap 0): X-COP {p0[f]['X_mean']:+.4f} vs {ref:+.4f}, baselines equal -> {'BITES' if b2 else 'NO BITE'}; MUTATE 3 (f_cap x3 at lambda_0 0.1): move {mv:+.3f} -> {'BITES' if b3 else 'NO BITE'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
