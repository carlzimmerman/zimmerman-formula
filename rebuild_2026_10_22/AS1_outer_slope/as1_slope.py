#!/usr/bin/env python3
"""AS1_outer_slope (criteria in FROZEN_CRITERIA.md): Argon's power-law slope over 150-800 kpc on B21's isolated mass bins, then on SI1's spectroscopic stacks and the models.
    OMP_NUM_THREADS=1 nice -n 15 python3 as1_slope.py <kids_source_cache_dir> <work_dir> [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
HEREA = os.path.dirname(os.path.abspath(__file__)); RBA = os.path.dirname(HEREA); MUTA = "--mutate" in sys.argv; SCALEC = "--scaled" in sys.argv; ARGV = [a for a in sys.argv[1:] if not a.startswith("--")]
SI2F = os.path.join(RBA, "SI2_spec_isolated_colour", "si2_grade.py"); srcx = open(SI2F).read(); cutx = 'J1 = None if MUT2 else'; assert srcx.count(cutx) == 1
sys.argv = [SI2F] + ARGV; __file__ = SI2F; exec(compile(srcx[:srcx.index(cutx)], "si2_head", "exec"))
OUTA = []
def A(s): print(s, flush=True); OUTA.append(str(s))
GRID = np.arange(-1.0, 5.0 + 5e-4, 1e-3)
def fit(R, d, C, hart=1.0):
    Ci = hart * np.linalg.inv(C); x = np.log(R / 0.3); best = None; chi = np.empty(len(GRID)); amp = np.empty(len(GRID))
    for i, g in enumerate(GRID):
        t = np.exp(-g * x); a = float(t @ Ci @ d) / float(t @ Ci @ t); r = d - a * t; chi[i] = float(r @ Ci @ r); amp[i] = a
    j = int(np.argmin(chi)); ins = GRID[chi <= chi[j] + 1.0]
    return dict(g=float(GRID[j]), s=float((ins[-1] - ins[0]) / 2), A=float(amp[j]), chi2=float(chi[j]), p=float(stats.chi2.sf(chi[j], len(d) - 2)), lo=float(ins[0]), hi=float(ins[-1]), sn=float(math.sqrt(max(d @ Ci @ d, 0))))
def label(f):
    if f["s"] > 0.225: return "NOT POWERED"
    if 0.85 <= f["g"] <= 1.20 and (1.675 - f["g"]) / f["s"] > 3: return "FAVOURS LAW"
    if f["g"] >= 1.45: return "FAVOURS FINITE HALO"
    return "OTHER"
def mslope(R, m, C, hart=1.0): return fit(R, m, C, hart)
RES = dict(criteria=None, mutate=MUTA, D1={}, D2={}, k={}); OK = True; dg = 0.0; k1 = 0.0
A(f"\nAS1 slope of Delta Sigma over 150-800 kpc; bins 0.15 < R < 0.80 Mpc; kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE data x (R/0.3)^-0.5]" if MUTA else ""))
# ---- D1: B21 mass bins, released covariance
B21 = os.path.join(os.path.dirname(RBA), "real_research", "data", "lensing_rar", "brouwer2021_rar"); COVF = np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
EDG = {1: 8.5, 2: 10.3, 3: 10.6, 4: 10.8}; k2 = 0.0; MFAC = lambda R: (R / 0.3) ** (-0.5) if MUTA else 1.0
for b in (1, 2, 3, 4):
    T = np.loadtxt(os.path.join(B21, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")); R_, esd, err, bias = T[:, 0], T[:, 1], T[:, 3], T[:, 4]; mk = (R_ > 0.15) & (R_ < 0.80); assert mk.sum() == 6
    m_ = np.isclose(COVF[:, 0], EDG[b]) & np.isclose(COVF[:, 1], EDG[b]); C_ = np.full((15, 15), np.nan)
    for row in COVF[m_]:
        i = int(np.argmin(np.abs(R_ / row[2] - 1))); j = int(np.argmin(np.abs(R_ / row[3] - 1))); C_[i, j] = row[4] / row[6]
    assert np.isfinite(C_).all(); C_ = 0.5 * (C_ + C_.T); dd = esd / bias; k2 = max(k2, float(np.max(np.abs(np.sqrt(np.diag(C_)) / (err / bias) - 1))))
    Rb, db, Cb = R_[mk], dd[mk], C_[np.ix_(mk, mk)]; db = db * MFAC(Rb); Cb = Cb * np.outer(MFAC(Rb), MFAC(Rb)) if SCALEC else Cb; f = fit(Rb, db, Cb); t = (Rb / 0.3) ** -1.3; a_ = float(t @ np.linalg.solve(Cb, np.ones(6))) ; k1 = max(k1, abs(fit(Rb, t, Cb)["g"] - 1.3)); f["cls"] = label(f); RES["D1"][f"bin{b}"] = dict(f, R=Rb.tolist(), d=db.tolist(), sig=np.sqrt(np.diag(Cb)).tolist())
    A(f"  D1 B21 mass bin {b} (lg M* from {EDG[b]}): gamma {f['g']:.3f} +- {f['s']:.3f}; A(300 kpc) {f['A']:.2f}; chi2 {f['chi2']:.1f} (p {f['p']:.3f}); S/N {f['sn']:.1f}; {f['cls']}")
ok2 = k2 <= 0.02; A(f"K2 B21 sqrt(diag C) vs error/bias, max frac diff {k2:.2e}: {'PASS' if ok2 else 'FAIL'}"); OK &= ok2; RES["k"]["K2"] = k2
# ---- D2 and D3: spectroscopic stacks and the models
MK = (RCEN > 0.15) & (RCEN < 0.80); assert MK.sum() == 6; RK = RCEN[MK]; H6 = (36 - 6 - 2) / 35; J1_ = json.load(open(os.path.join(RBA, "SI1_spec_isolated_route_e", "si1_results.json")))["foot"]
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TNL0 = N["TN"][(foot, "a")]; TOWN[(foot, "red")] = law_table(foot, SHIFT); TOWN[(key, "red")] = town_H(foot, dMs=SHIFT)
    N["tix"], N["MBN_g"] = TIX2, MBN2; TNH2 = tnbr(key, node=0); TNL2 = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0
    mods = dict(L_R0=modl(foot, TNL0, "R0"), H_R0=modl(key, TNH0, "R0"), L_R2=modl(foot, TNL2, "R2"), H_R2=modl(key, TNH2, "R2")); RES["D2"][foot] = {}
    for sm in ("S3", "S1"):
        for raw in (False, True):
            s0 = st(mods["L_R0"], sm, "all", raw=raw); d6 = s0["d"][MK] * MFAC(RK); C6 = cov_of(s0)[np.ix_(MK, MK)]; C6 = C6 * np.outer(MFAC(RK), MFAC(RK)) if SCALEC else C6; f = fit(RK, d6, C6, H6); f["cls"] = label(f); lab = f"{sm}{' raw L-R' if raw else ''}"; k1 = max(k1, abs(fit(RK, (RK / 0.3) ** -1.3, C6, H6)["g"] - 1.3))
            if not raw and not MUTA: dg = max(dg, float(np.max(np.abs(s0["d"] - np.array(J1_[foot][sm]["d"])))))
            row_ = dict(f, d=d6.tolist(), sig=np.sqrt(np.diag(C6)).tolist(), R=RK.tolist(), models={}); A(f"  [{foot}] {'D3' if raw else 'D2'} {lab:11s}: gamma {f['g']:.3f} +- {f['s']:.3f}; A(300 kpc) {f['A']:.2f}; chi2 {f['chi2']:.1f} (p {f['p']:.3f}); S/N {f['sn']:.1f}; {f['cls']}")
            for nm, mo in mods.items():
                sm_ = st(mo, sm, "all", raw=raw); m6 = sm_["m"][MK]; g_ = fit(RK, m6, C6, H6); pull = (f["g"] - g_["g"]) / f["s"]; row_["models"][nm] = dict(g=g_["g"], pull=pull, m=m6.tolist(), ratio=(d6 / m6).tolist())
                A(f"      {nm}: gamma {g_['g']:.3f}; A(300 kpc) {g_['A']:.2f}; data pull {pull:+.2f} sigma; d/m " + " ".join(f"{x:5.2f}" for x in d6 / m6))
            RES["D2"][foot][lab] = row_
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
ok1 = k1 <= 0.002; A(f"K1 noise-free gamma 1.3 returned, max |d| {k1:.2e}: {'PASS' if ok1 else 'FAIL'}"); OK &= ok1; RES["k"]["K1"] = k1
if not MUTA:
    ok3 = dg <= 1e-9; A(f"K3 stack vs SI1's committed d, max |d| {dg:.1e}: {'PASS' if ok3 else 'FAIL'}"); OK &= ok3; RES["k"]["K3"] = dg
else:
    J0 = json.load(open(os.path.join(HEREA, "as1_results.json"))); dm = 0.0
    for b in J0["D1"]: dm = max(dm, abs(RES["D1"][b]["g"] - J0["D1"][b]["g"] - 0.5))
    for foot in J0["D2"]:
        for lab in J0["D2"][foot]: dm = max(dm, abs(RES["D2"][foot][lab]["g"] - J0["D2"][foot][lab]["g"] - 0.5))
    A(f"MUTATE gamma rises by 0.5, max |d| {dm:.2e}: {'PASS' if dm <= 0.002 else 'FAIL'}"); RES["k"]["MUTATE"] = dm
RES["verdict_ok"] = bool(OK); tag = ("_MUTATE_scaled" if SCALEC else "_MUTATE") if MUTA else ""; json.dump(RES, open(os.path.join(HEREA, f"as1_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HEREA, f"as1{tag}.out"), "w").write("\n".join(OUTA) + "\n")
