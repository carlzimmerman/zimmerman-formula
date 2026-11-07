#!/usr/bin/env python3
"""SV1 iter_1 (criteria 74a07762ff): source geometry in the action's exact AQUAL field (mu = x/(1+x)); QX4's solver
imported read-only. Statistics O1 (solid-angle shell mean of g_r = stacked lensing) and O2 (source-weighted shell mean
= spherical HSE / Jeans) against the law at g_N_sph = G M(<r)/r^2. kappa = 1/2 FITTED; not theory closed.

  OMP_NUM_THREADS=1 nice -n 15 python3 sv1_geometry.py table [--newton]   -> table.npz / table_MUTATE_newton.npz
  OMP_NUM_THREADS=1 nice -n 15 python3 sv1_geometry.py grade              -> sv1_geometry.out / .json (+ MUTATE M1-M3)
"""
import os, sys, math, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX4_udg"))
import aqual as A                                                       # noqa: E402  read-only

FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BRM = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
QS = [0.4, 0.6, 0.8, 1.0, 1.5, 2.5]
PROF = ["hernquist", "plummer", "expdisc"]
RB = np.exp(np.linspace(np.log(0.1), np.log(300.0), 70))               # output radii r/b
MTOT = 1e10                                                             # Msun (scale symmetry: only b/r_M matters)
GRID = (200, 48)


def rho_fn(prof, b, q):
    if prof == "hernquist":
        return lambda R, z: (lambda m: 1.0 / (m * (m + b) ** 3))(np.sqrt(R ** 2 + (z / q) ** 2) + 1e-12 * b)
    if prof == "plummer":
        return lambda R, z: (1.0 + (R ** 2 + (z / q) ** 2) / b ** 2) ** -2.5
    zd = 0.1 * b                                                         # exponential disc, Rd = b
    return lambda R, z: np.exp(-R / b) / np.cosh(np.clip(z / zd, -300, 300)) ** 2


def deposit(g, f, nsub=6):
    u = (np.arange(nsub) + 0.5) / nsub
    r = np.exp(g.xf[:-1, None] + u[None, :] * g.dx)
    dt = (g.tf[1:] - g.tf[:-1]) / nsub
    t = g.tf[:-1, None] + u[None, :] * (g.tf[1:] - g.tf[:-1])[:, None]
    R = r[:, None, :, None] * np.sin(t)[None, :, None, :]; z = r[:, None, :, None] * np.cos(t)[None, :, None, :]
    w = 2 * np.pi * (r ** 3)[:, None, :, None] * np.sin(t)[None, :, None, :] * (g.dx / nsub) * dt[None, :, None, None]
    return np.sum(f(R, z) * w, axis=(2, 3))


def law(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)


def one(prof, q, brm, a0_si, newton=False, grid=GRID):
    a0 = A.a0_kpc(a0_si); rM = math.sqrt(A.G * MTOT / a0); b = brm * rM
    g = A.Grid(1e-2 * b, 3e3 * b * max(1.0, q), grid[0], grid[1])
    M = deposit(g, rho_fn(prof, b, q)); M *= (0.5 * MTOT) / M.sum()   # northern hemisphere carries M/2
    Phi, res, it = A.solve(g, M, a0, mu_one=newton, tol=1e-9, maxit=600)
    gr, gt = A._gradients(g, Phi)
    w = (np.cos(g.tf[:-1]) - np.cos(g.tf[1:]))                           # solid-angle weights per hemisphere, sum 1
    rho = M / (2 * np.pi * (g.rf[1:, None] ** 3 - g.rf[:-1, None] ** 3) / 3 * w[None, :])   # cell-mean density
    Menc = 2 * (np.cumsum(M.sum(1)) - 0.5 * M.sum(1))                    # inside the cell-centre sphere
    gN = A.G * Menc / g.rc ** 2; gl = law(gN, a0)                         # law reference in both modes (M1)
    G_ = np.sqrt(gr ** 2 + gt ** 2); mu = np.ones_like(G_) if newton else (G_ / a0) / (1 + G_ / a0)
    g1 = (gr * w).sum(1); g2 = (rho * gr * w).sum(1) / (rho * w).sum(1)
    gauss = (mu * gr * w).sum(1) / gN
    x = np.log(g.rc / b)
    I = lambda y: np.interp(np.log(RB), x, y)
    return dict(O1=I(np.log10(g1 / gl)), O2=I(np.log10(g2 / gl)), gauss=I(gauss), grneg=I((gr < 0).any(1).astype(float)),
                res=float(res), it=int(it), Mloss=float(1 - 2 * M.sum() / MTOT))


def table(newton):
    tag = "table_MUTATE_newton" if newton else "table"
    out = {}; t0 = time.time()
    for prof in PROF:
        for q in (QS if prof != "expdisc" else [1.0]):
            for brm in BRM:
                d = one(prof, q, brm, FOOT["canonical"], newton)
                for k, v in d.items(): out[f"{prof}|{q}|{brm}|{k}"] = np.asarray(v)
                print(f"{prof:9s} q {q:3.1f} b/rM {brm:5.2f}  it {d['it']:3d} res {d['res']:.1e}  "
                      f"O1(1b) {np.interp(1, RB, d['O1']):+.4f} O2(1b) {np.interp(1, RB, d['O2']):+.4f} "
                      f"O1(30b) {np.interp(30, RB, d['O1']):+.4f} gauss-1 max {np.max(np.abs(d['gauss'][RB < 100] - 1)):.1e}  {time.time()-t0:.0f}s", flush=True)
    np.savez_compressed(os.path.join(HERE, tag + ".npz"), RB=RB, **out)



# ------------------------------------------------------------------ grading
OUT = []
def P(s_): print(s_, flush=True); OUT.append(s_)
TEFF = {"canonical": 0.0090, "alt": 0.0094}                              # QX8 fixed-U = 0.50 law -> exact mean shift
DELTA = {"canonical": dict(E=0.209888 - 0.027383, X=0.467499 - 0.027383, G=0.263752 - 0.027383, dSph=0.199, KiDS=0.158),
         "alt": dict(E=0.188763 + 0.000603, X=0.434523 + 0.000603, G=0.225997 + 0.000603, dSph=0.188, KiDS=0.158)}
E_IMF = {"canonical": 0.093 - 0.027383, "alt": 0.074 + 0.000603}
SIG_FIX = {"canonical": dict(E=0.158, dSph=0.062, KiDS=0.064), "alt": dict(E=0.155, dSph=0.061, KiDS=0.064)}
GFST = {"canonical": (0.358644 - 0.195519) / 2, "alt": (0.320274 - 0.158280) / 2}


def qx20_points():
    """QX20's build() (QX5 loaders, QX16-fixed), read-only, executed up to its main loop."""
    src = open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py")).read()
    NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py"), "__name__": "qx20_lib"}
    argv = sys.argv; sys.argv = [sys.argv[0]]
    exec(compile(src[:src.index("BGRID = ")], "qx20_lib", "exec"), NS); sys.argv = argv
    return NS


def inv_s(prof, f):
    f = min(f, 0.995)
    if prof == "hernquist": r = math.sqrt(f); return r / (1 - r)
    return f ** (1 / 3) / math.sqrt(1 - f ** (2 / 3))


class Tab:
    def __init__(self, path):
        z = np.load(path); self.z = z; self.RB = z["RB"]
    def get(self, prof, q, brm, key): return self.z[f"{prof}|{q}|{brm}|{key}"]
    def at(self, prof, q, brm, s, key):
        lb = np.log(BRM); x = float(np.clip(math.log(brm), lb[0], lb[-1])); k = int(np.clip(np.searchsorted(lb, x) - 1, 0, len(BRM) - 2))
        t = (x - lb[k]) / (lb[k + 1] - lb[k])
        y = lambda b_: np.interp(math.log(max(s, self.RB[0])), np.log(self.RB), self.get(prof, q, b_, key))
        return (1 - t) * y(BRM[k]) + t * y(BRM[k + 1])


def classes(NS, f, a0):
    H, S = NS["build"](a0)
    XC, GR = NS["XC"], NS["GR"]; nE = 3 * len(NS["EL"]); nX = len(XC)
    names = ["E%d" % (i // 3) for i in range(nE)] + [z["name"] for z in XC] + [gp["name"] for gp in GR for _ in gp["pts"]]
    assert len(names) == len(H)
    pts = []
    for h, nm in zip(H, names):
        prof = "hernquist" if h["cls"] == "E" else "plummer"
        fr = h["V4_gN"] * h["V5_r_over_rM"] ** 2; s = inv_s(prof, fr)
        pts.append(dict(cls=h["cls"], name=nm, D=h["D"], prof=prof, s=s, brm=h["V5_r_over_rM"] / s, capped=fr >= 0.995))
    return pts, float(np.mean([x["D"] for x in S]))


def grade():
    T = Tab(os.path.join(HERE, "table.npz")); TN = Tab(os.path.join(HERE, "table_MUTATE_newton.npz"))
    NS = qx20_points(); R = dict(tag="sv1_geometry", criteria="74a07762ff", note="kappa = 1/2 FITTED; not theory closed")
    # ---- NUM-T1 and KA1 / KA2 on the whole table
    mx1, mx2, kag = -9, 0.0, 0.0; nneg = 0
    for prof in PROF:
        for q in (QS if prof != "expdisc" else [1.0]):
            for brm in BRM:
                ok = (T.get(prof, q, brm, "grneg") == 0) & (T.RB <= 100)
                nneg += int((~ok & (T.RB <= 100)).sum())
                mx1 = max(mx1, float(T.get(prof, q, brm, "O1")[ok].max()))
                sel = (T.RB >= 0.3) & (T.RB <= 100); kag = max(kag, float(np.abs(T.get(prof, q, brm, "gauss")[sel] - 1).max()))
                if q == 1.0 and prof != "expdisc":
                    mx2 = max(mx2, float(np.abs(T.get(prof, q, brm, "O1")[sel]).max()), float(np.abs(T.get(prof, q, brm, "O2")[sel]).max()))
    R.update(NUM_T1_maxO1=mx1, NUM_T1=bool(mx1 <= 1e-3), KA1_max=mx2, KA1=bool(mx2 <= 2e-3), KA2_max=kag, KA2=bool(kag <= 2e-3), n_grneg=nneg)
    P(f"NUM-T1 max O1 over every solve (g_r >= 0 on the shell, r <= 100 b): {mx1:+.2e} (line +1e-3) -> {'PASS' if R['NUM_T1'] else 'FAIL'}; shells with g_r < 0: {nneg}")
    P(f"KA1 sphere |O1|,|O2| max (0.3 <= r/b <= 100): {mx2:.2e} (line 2e-3) -> {'PASS' if R['KA1'] else 'FAIL'}")
    P(f"KA2 Gauss <mu g_r>/g_N_sph - 1 max (0.3 <= r/b <= 100): {kag:.2e} (line 2e-3) -> {'PASS' if R['KA2'] else 'FAIL'}")
    # ---- KA3 ladder, KA4 scale symmetry
    cells = [("hernquist", 0.4, 1.0), ("hernquist", 1.0, 1.0), ("plummer", 0.4, 10.0), ("plummer", 0.6, 0.3), ("hernquist", 2.5, 3.0), ("plummer", 0.8, 30.0)]
    sel = (RB >= 0.3) & (RB <= 100); dl = 0.0
    for c in cells:
        lo = one(*c, FOOT["canonical"], grid=(120, 40)); hi = one(*c, FOOT["canonical"], grid=(180, 60))
        dl = max(dl, float(np.abs(lo["O2"] - hi["O2"])[sel].max()), float(np.abs(lo["O1"] - hi["O1"])[sel].max()))
    c0 = one("plummer", 0.6, 3.0, FOOT["canonical"]); c1 = one("plummer", 0.6, 3.0, FOOT["alt"])
    d4 = max(float(np.abs(c0["O2"] - c1["O2"]).max()), float(np.abs(c0["O1"] - c1["O1"]).max()))
    R.update(KA3_max=dl, KA3=bool(dl <= 3e-3), KA4_max=d4, KA4=bool(d4 <= 1e-6))
    P(f"KA3 ladder 120x40 vs 180x60 (6 cells): max |dO| {dl:.2e} (line 3e-3) -> {'PASS' if R['KA3'] else 'FAIL'}")
    P(f"KA4 scale symmetry canonical vs alt a0 at b/r_M 3: max |dO| {d4:.2e} (line 1e-6) -> {'PASS' if R['KA4'] else 'FAIL'}")
    # ---- M1 Newton
    m1 = min(abs(float(np.interp(1.3, RB, TN.get(p_, q, b_, k)) - np.interp(1.3, RB, T.get(p_, q, b_, k))))
             for p_ in ("hernquist", "plummer") for q in QS for b_ in BRM if b_ >= 1 for k in ("O1", "O2"))
    R.update(M1_min_move=m1, M1_bites=bool(m1 >= 0.1))
    P(f"MUTATE M1 Newton: min |dO| at r = 1.3 b over b/r_M >= 1: {m1:.3f} dex (line 0.1) -> {'BITES' if R['M1_bites'] else 'DOES NOT BITE'}")
    QALL = QS
    for f, a0 in A0F.items():
        pts, smean = classes(NS, f, a0); RF = dict(sparc_mean=smean); P(f"\n[{f}] SPARC mean {smean:+.6f}; T_eff {TEFF[f]:.4f}")
        sig = dict(SIG_FIX[f])
        for c in "XG":
            sysm = {}
            for x in pts:
                if x["cls"] == c: sysm.setdefault(x["name"], []).append(x["D"])
            mm = np.array([np.mean(v) for v in sysm.values()]); se = float(mm.std(ddof=1) / math.sqrt(len(mm)))
            sig[c] = math.hypot(se, GFST[f]) if c == "G" else se
            RF[f"N_sys_{c}"] = len(mm)
        rows = {}
        for c in ("E", "X", "G"):
            cp = [x for x in pts if x["cls"] == c]
            byq = {q: float(np.mean([T.at(x["prof"], q, x["brm"], x["s"], "O2") for x in cp])) for q in QALL}
            byq1 = {q: float(np.mean([T.at(x["prof"], q, x["brm"], x["s"], "O1") for x in cp])) for q in QALL}
            qb = max(byq, key=byq.get)
            rows[c] = dict(O2_by_q=byq, O1_by_q=byq1, q_best=qb, P=byq[qb] + TEFF[f], P_sphere=byq[1.0] + TEFF[f],
                           brm_range=[float(min(x["brm"] for x in cp)), float(max(x["brm"] for x in cp))],
                           s_range=[float(min(x["s"] for x in cp)), float(max(x["s"] for x in cp))], n_capped=int(sum(x["capped"] for x in cp)), N=len(cp))
        d = {(q, b_): float(np.interp(1.305, RB, T.get("plummer", q, b_, "O2"))) for q in QALL for b_ in (1.0, 3.0, 10.0, 30.0)}
        kb = max(d, key=d.get); rows["dSph"] = dict(P=d[kb] + TEFF[f], best=list(kb), P_sphere=max(v for k_, v in d.items() if k_[0] == 1.0) + TEFF[f])
        selk = (RB >= 10) & (RB <= 300)
        e_ = max(float(T.get("hernquist", q, b_, "O1")[selk].max()) for q in QALL for b_ in (0.1, 0.3))
        l_ = min(float(T.get("expdisc", 1.0, b_, "O1")[selk].min()) for b_ in (0.1, 0.3))
        rows["KiDS"] = dict(P=e_ - l_, O1_early_max=e_, O1_late_min=l_)
        e1 = max(float(T.get("hernquist", 1.0, b_, "O1")[selk].max()) for b_ in (0.1, 0.3))
        rows["KiDS"]["P_sphere"] = e1 - l_
        for c in ("E", "X", "G", "dSph", "KiDS"):
            r_ = rows[c]; D_ = DELTA[f][c]; s_ = sig[c]; Pp = r_["P"]
            lab = lambda Pv: ("OVER" if Pv > D_ + 2 * s_ else "SHORT" if Pv < D_ - 2 * s_ else ("EXPLAINED" if D_ > 2 * s_ else "COMPATIBLE, NOT NEEDED"))
            r_.update(Delta=D_, sigma=s_, label=lab(Pp), shortfall=D_ - Pp, M2_label=lab(Pp + 0.30))
            P(f"[{f}] {c:4s} Delta {D_:+.4f} +- {s_:.4f}  P(best geometry) {Pp:+.4f}  P(sphere) {r_['P_sphere']:+.4f}  "
              f"shortfall {D_ - Pp:+.4f}  -> {r_['label']}   [M2 planted +0.30: {r_['M2_label']}]")
        for c in ("E", "X", "G"):
            r_ = rows[c]
            P(f"      {c}: N {r_['N']}, b/r_M {r_['brm_range'][0]:.3f}-{r_['brm_range'][1]:.2f}, r/b {r_['s_range'][0]:.2f}-{r_['s_range'][1]:.2f}, capped {r_['n_capped']}; "
              "mean O2 by q " + " ".join(f"{q}:{v:+.4f}" for q, v in r_["O2_by_q"].items()) + "; mean O1 by q " + " ".join(f"{q}:{v:+.4f}" for q, v in r_["O1_by_q"].items()))
        P(f"      dSph best (q, b/r_M) {rows['dSph']['best']}; KiDS O1 early max {rows['KiDS']['O1_early_max']:+.5f}, late min {rows['KiDS']['O1_late_min']:+.5f}")
        eimf = E_IMF[f]; RF["E_IMF_secondary"] = dict(Delta=eimf, label=("SHORT" if rows["E"]["P"] < eimf - 2 * sig["E"] else "COMPATIBLE"))
        P(f"[{f}] secondary E after Posacki IMF: Delta {eimf:+.4f}: P {rows['E']['P']:+.4f} -> {RF['E_IMF_secondary']['label']}")
        m3 = max(abs(rows[c]["P"] - rows[c]["P_sphere"]) for c in ("E", "X", "G", "dSph", "KiDS"))
        RF.update(rows=rows, sigma=sig, M3_max_P_minus_sphere=m3, M3_bites=bool(m3 > 2e-3),
                  M2_bites=bool(any(rows[c]["label"] in ("SHORT", "OVER") and rows[c]["M2_label"] in ("EXPLAINED", "COMPATIBLE, NOT NEEDED") for c in rows)),
                  label=("GEOMETRY EXPLAINS THE STEP" if all(rows[c]["label"] not in ("SHORT", "OVER") for c in rows) else
                         "GEOMETRY SHORT" if all(rows[c]["label"] != "OVER" for c in rows) else "GEOMETRY OVER"))
        P(f"[{f}] MUTATE M2 (planted +0.30): {'BITES' if RF['M2_bites'] else 'DOES NOT BITE'}; M3 (sphere for every class): max |P - P_sphere| {m3:.4f} (line > 2e-3) -> {'BITES' if RF['M3_bites'] else 'DOES NOT BITE'}")
        P(f"[{f}] LABEL: {RF['label']}")
        R[f] = RF
    json.dump(R, open(os.path.join(HERE, "sv1_geometry.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "sv1_geometry.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed.\n")


A0F = FOOT

if __name__ == "__main__":
    if sys.argv[1] == "grade": grade()
    elif sys.argv[1] == "table": table("--newton" in sys.argv)
    elif sys.argv[1] == "probe":
        for q in (1.0, 0.4):
            d = one("hernquist", q, 1.0, FOOT["canonical"])
            print(q, d["it"], d["res"], d["Mloss"]); print(np.round(d["O1"][::7], 4)); print(np.round(d["O2"][::7], 4)); print(np.round(d["gauss"][::7] - 1, 4))
