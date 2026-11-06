#!/usr/bin/env python3
"""QX10 iter_1 (FROZEN_CRITERIA.md, c1f0cadb7a): primary CMB TT/TE/EE for QX7 iter_4's window, footing background.
Modes (run from the repo root, one thread each):
  python3 qx10_i1.py fit  <canonical|alt> <main|MA|MB>   -> fit_<foot>_<mode>.json/.npz   (Nelder-Mead, two starts)
  python3 qx10_i1.py k1                                   -> k1.json  (Planck 2018 best fit: data/code calibration only)
  python3 qx10_i1.py jcheck                               -> jcheck.json (J0 Jeans gate, J1 late-lensing bound per cell)
  python3 qx10_i1.py grade                                -> qx10_i1.json/.out, qx10_i1_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Footings never pooled."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize
from classy import Class

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
F_TT = os.path.join(EXT, "cmb_lensing_raw/planck_PR4_lensing/planckpr4lensing/data_pr4/iswliks/COM_PowerSpect_CMB-TT-full_R3.01.txt")
F_TE = os.path.join(EXT, "planck_pr3_spectra_2026_10_22/COM_PowerSpect_CMB-TE-full_R3.01.txt")
F_EE = os.path.join(EXT, "planck_pr3_spectra_2026_10_22/COM_PowerSpect_CMB-EE-full_R3.01.txt")
TCMB = 2.7255; G = 6.67430e-11; C = 2.99792458e8; MPC = 3.0856775814913673e22
RHO_C100 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)                  # kg/m^3 for h = 1
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OMEGA_G = 2.4728e-5 * (TCMB / 2.7255) ** 4; OMEGA_R = OMEGA_G * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
OB_BR = (0.0215, 0.0230); TAU_BR = (0.01, 0.15)
CELLS = {"C1": (2.6102, 4.25), "C2": (1.4678, 3.5), "C3": (8.254, 5.625), "C4": (2.1544, 3.75)}
LMAXC = 2600


def load(f):
    a = np.loadtxt(f); return dict(l=a[:, 0].astype(int), D=a[:, 1], e=0.5 * (a[:, 2] + a[:, 3]))


DATA = {"tt": load(F_TT), "te": load(F_TE), "ee": load(F_EE)}


def rho_foot(a0):
    return 4 * a0 ** 2 / (G * C ** 2) / RHO_C100                       # omega units


def background(foot, ob, od):
    """framework-native: canonical fixes omega_DE, alt fixes h^2 (frozen text)."""
    w = rho_foot(FOOT[foot])
    if foot == "canonical":
        h2 = w + ob + od + OMEGA_R; ode = w
    else:
        h2 = w; ode = w - ob - od - OMEGA_R
    return math.sqrt(h2), ode


def spectra(foot, th, mode):
    ob, od, lnA, ns, tau = th
    h, ode = background(foot, ob, od)
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAXC, 'h': h, 'omega_b': ob,
         'A_s': math.exp(lnA) * 1e-10, 'n_s': ns, 'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': TCMB}
    if mode == "MA":            # p = 0: w = 0 fluid with c_s^2 = 1, abundance omega_d
        p.update({'omega_cdm': 1e-7, 'Omega_fld': od / h ** 2, 'w0_fld': -1e-3, 'wa_fld': 0.0, 'cs2_fld': 1.0, 'use_ppf': 'no'})
    elif mode == "MB":
        p.update({'omega_cdm': 1e-7})
    else:
        p.update({'omega_cdm': od})
    M = Class(); M.set(p); M.compute()
    cl = M.lensed_cl(2508); f = (TCMB * 1e6) ** 2
    out = {}
    for X in ("tt", "te", "ee"):
        l = np.arange(len(cl[X])); out[X] = l * (l + 1) * cl[X] * f / (2 * np.pi)
    ol = M.Omega_Lambda(); M.struct_cleanup(); M.empty()
    return out, h, ode, ol


def chi2s(out):
    r = {}
    for X, d in DATA.items():
        m = out[X][d["l"]]; r[X] = float(np.sum(((d["D"] - m) / d["e"]) ** 2))
    r["sum"] = sum(r.values()); return r


def fit(foot, mode):
    fixed_od = (mode == "MB")
    def unpack(x):
        ob, od, lnA, ns, tau = x
        if fixed_od: od = 1e-7
        return (ob, od, lnA, ns, tau)
    def pen(x):
        ob, od, lnA, ns, tau = x; s = 0.0
        s += 1e4 * (max(0, OB_BR[0] - ob) + max(0, ob - OB_BR[1])) / 1e-4
        s += 1e4 * (max(0, TAU_BR[0] - tau) + max(0, tau - TAU_BR[1])) / 1e-3
        if not fixed_od: s += 1e4 * (max(0, 0.005 - od) + max(0, od - 0.4)) / 1e-3
        s += 1e4 * (max(0, 0.7 - ns) + max(0, ns - 1.3)) / 1e-3
        return s
    cache = {}
    def f(x):
        key = tuple(np.round(x, 9))
        if key in cache: return cache[key]
        pp = pen(x)
        if pp > 0: cache[key] = 1e7 + pp; return cache[key]
        try:
            out, h, ode, ol = spectra(foot, unpack(x), mode); v = chi2s(out)["sum"]
        except Exception:
            v = 1e8
        cache[key] = v; return v
    starts = [np.array([0.0224, 0.120, 3.04, 0.965, 0.055]), np.array([0.0219, 0.105, 3.10, 0.94, 0.08])]
    if mode == "MB": starts = [np.array([0.0224, 1e-7, 3.04, 0.965, 0.055]), np.array([0.0228, 1e-7, 2.9, 1.05, 0.10])]
    best = None
    for s in starts:
        step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02]); simplex = [s] + [s + np.eye(5)[i] * step[i] for i in range(5)]
        r = minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=700, xatol=1e-5, fatol=0.05))
        if best is None or r.fun < best.fun: best = r
    th = unpack(best.x); out, h, ode, ol = spectra(foot, th, mode); cs = chi2s(out)
    res = dict(foot=foot, mode=mode, theta=dict(omega_b=th[0], omega_d=th[1], lnAs1e10=th[2], n_s=th[3], tau=th[4]),
               h=h, omega_DE=ode, class_Omega_Lambda_h2=ol * h * h, chi2=cs, nfev=len(cache), note="kappa = 1/2 FITTED; not theory closed")
    tag = f"fit_{foot}_{mode}"
    json.dump(res, open(os.path.join(HERE, tag + ".json"), "w"), indent=1)
    np.savez(os.path.join(HERE, tag + ".npz"), **{X: out[X] for X in out})
    print(json.dumps(res), flush=True)


def k1():
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAXC, 'h': 0.6732, 'omega_b': 0.02237, 'omega_cdm': 0.1200,
         'A_s': math.exp(3.044) * 1e-10, 'n_s': 0.9649, 'tau_reio': 0.0544, 'N_ur': 3.046, 'T_cmb': TCMB}
    M = Class(); M.set(p); M.compute(); cl = M.lensed_cl(2508); f = (TCMB * 1e6) ** 2; out = {}
    for X in ("tt", "te", "ee"):
        l = np.arange(len(cl[X])); out[X] = l * (l + 1) * cl[X] * f / (2 * np.pi)
    res = dict(chi2=chi2s(out), note="Planck 2018 best fit used only as a data/code calibration, never as an input")
    json.dump(res, open(os.path.join(HERE, "k1.json"), "w"), indent=1)
    np.savez(os.path.join(HERE, "k1.npz"), **out); print(json.dumps(res), flush=True)


def jcheck():
    """J0 (comoving Jeans wavenumber at z >= 10) and J1 (late lensing bound on TT), QX7's corner background and solver."""
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity/CFG917_cmb_lensing_gate"))
    D3 = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter3_barotropic_family")
    s3 = open(os.path.join(D3, "iter3.py")).read(); c3 = s3.index("# K: beta = 0")
    cwd = os.getcwd(); os.chdir(D3); os.environ.pop("QX3_MUTATE", None)
    N3 = {"__file__": os.path.join(D3, "iter3.py"), "__name__": "iter3_reused"}
    argv0, sys.argv = sys.argv, [os.path.join(D3, "iter3.py")]
    exec(compile(s3[:c3], os.path.join(D3, "iter3.py"), "exec"), N3); os.chdir(cwd); sys.argv = argv0
    I2, H0 = N3["I2"], N3["H0"]
    S7 = open(os.path.join(REPO, "closure_2026_11_06", "QX7_unified_cold_switch", "iter_3_de_fraction_switch", "qx7_iter3.py")).read()
    blk = S7[S7.index("# ---- generalised G2' solver"):S7.index("d_iter3 = g2(")]
    MC = N3["M"]; OL0 = MC.Omega_Lambda(); H0c = MC.Hubble(0.0)
    def ode(z): return OL0 / (MC.Hubble(z) / H0c) ** 2
    LOC = dict(np=np, N3=N3, I2=I2, MC=MC, H0=H0, ode=ode); exec(blk, LOC); solve_gen, kJ_of = LOC["solve_gen"], LOC["kJ_of"]
    OD0 = ode(0.0)
    # Limber ratio to L 2500 (same formula as QX3 I2.limber_ratio, extended in L)
    kgrid, zgrid = N3["kgrid"], N3["zgrid"]
    chis = MC.angular_distance(1089.0) * 1090.0
    chi = np.array([MC.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
    P = np.array([[MC.pk_lin(k, z) for z in zgrid] for k in kgrid])
    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + zgrid) ** 2 / np.array([MC.Hubble(z) for z in zgrid])
    Ls = np.arange(2, 2501)
    def Sfull(Rr):
        num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
        for j in range(len(zgrid)):
            kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
            Pj = np.interp(np.log(kk[m]), lnk, P[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rr[:, j])
            num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2; den[m] += w[j] * Pj / chi[j] ** 2
        S = np.ones(len(Ls)); ok = den > 0; S[ok] = num[ok] / den[ok]; return S
    # lensed - unlensed TT at the K1 reference (shape of the lensing contribution), mean data errors
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAXC, 'h': 0.6732, 'omega_b': 0.02237, 'omega_cdm': 0.1200,
         'A_s': math.exp(3.044) * 1e-10, 'n_s': 0.9649, 'tau_reio': 0.0544}
    M = Class(); M.set(p); M.compute(); f = (TCMB * 1e6) ** 2
    cl = M.lensed_cl(2508); ru = M.raw_cl(2508); l = np.arange(2509)
    dL = (l * (l + 1) * (cl["tt"] - ru["tt"]) * f / (2 * np.pi))
    d = DATA["tt"]
    res = dict(note="kappa = 1/2 FITTED; not theory closed", Omega_DE0_corner=OD0, cells={})
    for cname, (l0, pp) in CELLS.items():
        lst = l0 / OD0 ** pp; kJ = kJ_of(lst, pp)                      # physical k_J(a) = 2 pi/lambda_J
        zz = np.geomspace(10, 3400, 400); kc = np.array([kJ(1 / (1 + z)) / (1 + z) for z in zz])
        zl = np.linspace(0, 10, 201); kcl = np.array([kJ(1 / (1 + z)) / (1 + z) for z in zl])
        Rr = solve_gen(kJ) / N3["ref"]; S = Sfull(Rr)
        delta = float(np.max(np.abs(1 - S)))
        dD = delta * np.abs(dL[d["l"]]); dchi = float(np.sum((dD / d["e"]) ** 2))
        res["cells"][cname] = dict(lambda_0=l0, p=pp, lambda_star=lst, kJ_com_min_z_ge_10=float(kc.min()),
                                   J0=bool(kc.min() >= 50.0), kJ_com_min_z_lt_10=float(kcl.min()),
                                   S_min=float(S.min()), S_max=float(S.max()), S_L100=float(S[98]), S_L400=float(S[398]), S_L1000=float(S[998]),
                                   max_abs_1mS=delta, J1_dchi2_TT=dchi, J1=bool(dchi <= 1.0))
        print(cname, json.dumps(res["cells"][cname]), flush=True)
    json.dump(res, open(os.path.join(HERE, "jcheck.json"), "w"), indent=1)


def peak_fit(l, D, e, lo, hi, rng, nmc=400):
    m = (l >= lo) & (l <= hi); x = l[m].astype(float); y = D[m]; w = 1 / e[m] ** 2
    c, cov = np.polyfit(x - x.mean(), y, 4, w=np.sqrt(w), cov='unscaled')
    xs = np.linspace(x.min(), x.max(), 4000); ys = np.polyval(c, xs - x.mean())
    hs = [np.polyval(rng.multivariate_normal(c, cov), xs - x.mean()).max() for _ in range(nmc)]
    return float(ys.max()), np.array(hs)


WIN = {1: (150, 300), 2: (440, 640), 3: (720, 920)}


def peaks_data():
    rng = np.random.default_rng(20261106); d = DATA["tt"]; H = {}; S = {}
    for k, (lo, hi) in WIN.items(): H[k], S[k] = peak_fit(d["l"], d["D"], d["e"], lo, hi, rng)
    r21 = S[2] / S[1]; r31 = S[3] / S[1]
    return dict(H=H, r21=(H[2] / H[1], float(np.std(r21))), r31=(H[3] / H[1], float(np.std(r31))))


def peaks_model(Dm):
    d = DATA["tt"]; H = {}
    for k, (lo, hi) in WIN.items():
        m = (d["l"] >= lo) & (d["l"] <= hi); x = d["l"][m].astype(float); y = Dm[d["l"][m]]
        c = np.polyfit(x - x.mean(), y, 4, w=1 / d["e"][m]); xs = np.linspace(x.min(), x.max(), 4000)
        H[k] = float(np.polyval(c, xs - x.mean()).max())
    return H[2] / H[1], H[3] / H[1]


def lines(spec, chi):
    o = {}
    for X, d in DATA.items():
        N = len(d["l"]); o[f"L1_{X}"] = dict(chi2=chi[X], N=N, line=N + 3 * math.sqrt(2 * N), pass_=bool(chi[X] <= N + 3 * math.sqrt(2 * N)))
    Nt = sum(len(d["l"]) for d in DATA.values()); o["L1_sum"] = dict(chi2=chi["sum"], N=Nt, line=Nt + 3 * math.sqrt(2 * Nt), pass_=bool(chi["sum"] <= Nt + 3 * math.sqrt(2 * Nt)))
    bands = []
    for X, d in DATA.items():
        r = ((d["D"] - spec[X][d["l"]]) / d["e"]) ** 2
        for lo in range(2, int(d["l"].max()) + 1, 100):
            m = (d["l"] >= lo) & (d["l"] < lo + 100); n = int(m.sum())
            if n == 0: continue
            v = float(r[m].sum() / n); bands.append(dict(X=X, lo=lo, n=n, chi2n=v, line=1 + 3 * math.sqrt(2 / n), pass_=bool(v <= 1 + 3 * math.sqrt(2 / n))))
    o["L2_bands_failing"] = [b for b in bands if not b["pass_"]]; o["L2_pass"] = not o["L2_bands_failing"]; o["L2_n_bands"] = len(bands)
    o["L1_pass"] = all(o[k]["pass_"] for k in o if k.startswith("L1_"))
    return o


def grade():
    OUT = []; P = lambda s="": (print(s, flush=True), OUT.append(str(s)))
    P("QX10 iter_1: primary CMB TT/TE/EE (raw Planck PR3 CMB-only spectra, diagonal), framework-native footing background.")
    P("kappa = 1/2 FITTED; not theory closed. Footings never pooled. Criteria c1f0cadb7a.")
    RES = dict(lane="QX10 iter_1", criteria="c1f0cadb7a", note="kappa = 1/2 FITTED; not theory closed")
    k = json.load(open(os.path.join(HERE, "k1.json"))); ks = dict(np.load(os.path.join(HERE, "k1.npz")))
    LK = lines(ks, k["chi2"]); RES["K1"] = dict(chi2=k["chi2"], lines=LK, pass_=bool(LK["L1_pass"] and LK["L2_pass"]))
    P(f"K1 (Planck 2018 best fit, calibration only): chi2 TT {k['chi2']['tt']:.1f}/{LK['L1_tt']['N']} TE {k['chi2']['te']:.1f}/{LK['L1_te']['N']} "
      f"EE {k['chi2']['ee']:.1f}/{LK['L1_ee']['N']}; L1 {'PASS' if LK['L1_pass'] else 'FAIL'}, L2 {'PASS' if LK['L2_pass'] else 'FAIL'} "
      f"({len(LK['L2_bands_failing'])} of {LK['L2_n_bands']} bands fail) -> K1 {'PASS' if RES['K1']['pass_'] else 'FAIL'}")
    J = json.load(open(os.path.join(HERE, "jcheck.json"))); RES["J"] = J
    for c, v in J["cells"].items():
        P(f"{c} (lambda_0 {v['lambda_0']}, p {v['p']}): J0 min comoving k_J (z>=10) {v['kJ_com_min_z_ge_10']:.3g} /Mpc -> {'PASS' if v['J0'] else 'FAIL'}; "
          f"z<10 min {v['kJ_com_min_z_lt_10']:.3g}; J1 max|1-S| {v['max_abs_1mS']:.4f}, Delta chi2_TT bound {v['J1_dchi2_TT']:.3f} -> {'PASS' if v['J1'] else 'FAIL'}")
    PD = peaks_data(); RES["peaks_data"] = dict(r21=PD["r21"], r31=PD["r31"])
    P(f"data peaks: H2/H1 {PD['r21'][0]:.4f} +- {PD['r21'][1]:.4f}, H3/H1 {PD['r31'][0]:.4f} +- {PD['r31'][1]:.4f}")
    RES["footings"] = {}
    for foot in FOOT:
        r = json.load(open(os.path.join(HERE, f"fit_{foot}_main.json"))); s = dict(np.load(os.path.join(HERE, f"fit_{foot}_main.npz")))
        L = lines(s, r["chi2"]); m21, m31 = peaks_model(s["tt"])
        L3 = bool(abs(m21 - PD["r21"][0]) <= 3 * PD["r21"][1] and abs(m31 - PD["r31"][0]) <= 3 * PD["r31"][1])
        th = r["theta"]; Cwd = bool(abs(th["omega_d"] - 0.1196) / 0.1196 <= 0.10 and 0.65 <= r["h"] <= 0.75)
        ok = L["L1_pass"] and L["L2_pass"] and L3 and Cwd
        RES["footings"][foot] = dict(fit=r, lines=L, peaks_model=dict(r21=m21, r31=m31), L3=L3, C_wd=Cwd, pass_=bool(ok))
        P(f"\n=== {foot}: omega_b {th['omega_b']:.5f} omega_d {th['omega_d']:.4f} ln(1e10 A_s) {th['lnAs1e10']:.3f} n_s {th['n_s']:.4f} tau {th['tau']:.3f}; "
          f"h {r['h']:.4f} (omega_DE {r['omega_DE']:.4f}; CLASS Omega_L h^2 {r['class_Omega_Lambda_h2']:.4f})")
        for X in ("tt", "te", "ee"):
            q = L[f"L1_{X}"]; P(f"  L1 {X}: chi2 {q['chi2']:.1f} / N {q['N']} (line {q['line']:.1f}) -> {'PASS' if q['pass_'] else 'FAIL'}")
        q = L["L1_sum"]; P(f"  L1 sum: {q['chi2']:.1f} / {q['N']} (line {q['line']:.1f}) -> {'PASS' if q['pass_'] else 'FAIL'}")
        P(f"  L2 bands: {len(L['L2_bands_failing'])} of {L['L2_n_bands']} fail" + (": " + ", ".join(f"{b['X']} {b['lo']} ({b['chi2n']:.2f}>{b['line']:.2f})" for b in L['L2_bands_failing']) if L['L2_bands_failing'] else ""))
        P(f"  L3 peaks: model H2/H1 {m21:.4f}, H3/H1 {m31:.4f} -> {'PASS' if L3 else 'FAIL'}")
        P(f"  C-wd: omega_d {th['omega_d']:.4f} vs 0.1196 ({100 * (th['omega_d'] / 0.1196 - 1):+.1f} %), h {r['h']:.4f} in [0.65, 0.75] -> {'PASS' if Cwd else 'INCONSISTENT'}")
    # MUTATE
    MRES = {}; Mout = []
    for foot in FOOT:
        for mode in ("MA", "MB"):
            r = json.load(open(os.path.join(HERE, f"fit_{foot}_{mode}.json"))); s = dict(np.load(os.path.join(HERE, f"fit_{foot}_{mode}.npz")))
            L = lines(s, r["chi2"]); bites = not L["L1_pass"]
            MRES[f"{foot}_{mode}"] = dict(fit=r, L1_pass=L["L1_pass"], bites=bool(bites))
            Mout.append(f"{foot} {mode}: chi2 sum {r['chi2']['sum']:.1f} (TT {r['chi2']['tt']:.1f}, TE {r['chi2']['te']:.1f}, EE {r['chi2']['ee']:.1f}); L1 {'PASS' if L['L1_pass'] else 'FAIL'} -> {'BITES' if bites else 'DOES NOT BITE'}")
    mut_ok = all(v["bites"] for v in MRES.values())
    json.dump(dict(MUTATE=MRES, all_bite=mut_ok, note="kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "qx10_i1_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "qx10_i1_MUTATE.out"), "w").write("\n".join(Mout + [f"all bite: {mut_ok}"]) + "\n")
    P("\nMUTATE (separate outputs qx10_i1_MUTATE.*):"); [P("  " + x) for x in Mout]
    # labels per cell
    RES["labels"] = {}
    for c, v in J["cells"].items():
        if not RES["K1"]["pass_"] or not mut_ok: lab = "NO VERDICT (gate uncalibrated or MUTATE does not bite)"
        elif not (v["J0"] and v["J1"]): lab = "NO VERDICT (CDM proxy invalid)"
        elif all(RES["footings"][f]["pass_"] for f in FOOT): lab = "PASS"
        else: lab = "FAIL" + ("" if all(RES["footings"][f]["C_wd"] for f in FOOT) else " (INCONSISTENT)")
        RES["labels"][c] = lab
    P("\nLabels: " + "; ".join(f"{c} {l}" for c, l in RES["labels"].items()))
    json.dump(RES, open(os.path.join(HERE, "qx10_i1.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "qx10_i1.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fit": fit(a[1], a[2])
    elif a[0] == "k1": k1()
    elif a[0] == "jcheck": jcheck()
    elif a[0] == "grade": grade()
