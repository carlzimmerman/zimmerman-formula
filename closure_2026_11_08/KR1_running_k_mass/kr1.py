#!/usr/bin/env python3
"""KR1 (FROZEN_CRITERIA.md, 77ebbd6ad2): running K-mass from Blanchet-Skordis's DBI K(Q).
    python3 kr1.py            -> kr1.json / kr1.out
    python3 kr1.py --mutate   -> kr1_MUTATE.json / kr1_MUTATE.out  (M-A quadratic K, M-B constant mu, M-C GC power)
CK4's engine (solve3, fs8, P1D) and GL1's corrected limber_n (n = 4) are exec'd read-only. One thread.
Cold dark energy (the action's K(Q) sector), never dark matter; no particle. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6, CL7 = os.path.join(REPO, "closure_2026_11_06"), os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "kr1_MUTATE" if MUT else "kr1"; OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def J(p): return json.load(open(p))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20)   # MB on macOS (bytes)

C_KMS = 299792.458
M_LINE = 630.9573444801937          # GL1 L2 mu_min_n4 (Mpc^-1)
M_361 = 361.0                       # the brief's number, reported only
Z_RUN = 3.0
MEMBERS = {"D0": 1e-3, "D1": 0.1, "D2": 9.998, "D3": 79.43282347242821}
W_LINE_A, X_LINE_B = 0.01, 0.067
A34 = 1 / 3401.0; ABBN = 1 / (1 + 1e5 / (8.617333262e-5 * 2.7255))
OMR_H2 = 2.47e-5 * (1 + 0.2271 * 3.046)
KMAX_CMB = 0.25
S0_LINES = {"solar_system_1AU": 9.87e-9, "milky_way_220": 5.38e-7, "cluster_1000": 1.11e-5}
AU_MPC = 1.495978707e11 / 3.0856775814913673e22
CASSINI = 2.3e-5
R_TA = 0.234; ZC = 2.0; TA = 5.55
III_LINE, S4_LINE = 79.43282347242821, 0.1
RES = dict(tag=TAG, criteria="77ebbd6ad2", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", KA={}, footings={})
P(f"KR1 {'MUTATE' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ DBI background (Q7's cancellation-free forms)
def bg(mu, lam, I0, a):
    """K(Q) = (2 mu^2/lam)[1 - sqrt(1 - lam q^2)] on K'(Qbar) = I0/a^3. Returns 8 pi G rho, w, M, excess, Qbar."""
    Z = I0 / (2 * mu * mu * a ** 3); r = math.sqrt(1 + lam * Z * Z)
    Qb = 1 + Z / r; K = 2 * mu * mu * Z * Z / (r * (r + 1)); Kp = 2 * mu * mu * Z
    rho8 = Qb * Kp - K; ex = 2 * mu * mu * Z * Z / (r + 1)
    return dict(Z=Z, r=r, Qb=Qb, K=K, Kp=Kp, Kpp=2 * mu * mu * r ** 3, rho8=rho8, w=K / rho8, M=mu * Qb * r ** 1.5, ex=ex)
def M_of(mu, lam, I0): return lambda a: bg(mu, lam, I0, a)["M"]
def lam_fix(mu, I0, Mline=M_LINE, z=Z_RUN):
    a = 1 / (1 + z)
    if bg(mu, 0.0, I0, a)["M"] >= Mline: return 0.0
    f = lambda x: math.log(bg(mu, 10.0 ** x, I0, a)["M"] / Mline)
    return 10.0 ** brentq(f, -30, 150, xtol=1e-13, rtol=1e-15)
def X_bbn(mu, lam, I0, a=ABBN): return bg(mu, lam, I0, a)["ex"] / (3 * (100 / C_KMS) ** 2 * OMR_H2 * a ** -4)
def q_of_Z(mu, lam, Z): r = math.sqrt(1 + lam * Z * Z); return Z / r
def M_at_q(mu, lam, q):
    s = 1 - lam * q * q
    return None if s <= 0 else (1 + q) * math.sqrt(mu * mu * s ** -1.5)
def rho8_Z(mu, lam, Z):
    r = math.sqrt(1 + lam * Z * Z); return (1 + Z / r) * 2 * mu * mu * Z - 2 * mu * mu * Z * Z / (r * (r + 1))
def M_at_density(mu, lam, I0, ratio):
    """local M at 8 pi G rho = ratio x today's background (exact inverse of rho(Z))."""
    Z0 = I0 / (2 * mu * mu); target = ratio * rho8_Z(mu, lam, Z0)
    lz = brentq(lambda x: math.log(rho8_Z(mu, lam, math.exp(x)) / target), math.log(Z0) - 5, math.log(Z0) + 60, xtol=1e-14)
    Z = math.exp(lz); r = math.sqrt(1 + lam * Z * Z); return mu * (1 + Z / r) * r ** 1.5, Z

F1A = J(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")); KD1 = J(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json"))
FOOT = ("canonical", "alt")
SET = {}
for f in FOOT:
    b = F1A[f]["best_B2"]; SET[f] = dict(ob=b["ob"], od=b["oc"], h=b["h"], I0=3 * (100 / C_KMS) ** 2 * b["oc"])

# ------------------------------------------------------------------ KA1 / KA2 / KA3 (main run only)
if not MUT:
    ok1 = True; d1 = {}
    for f in FOOT:
        st = KD1["footings"][f]["setting"]; I0k = st["I0_Mpc-2"]; Omr = OMR_H2 / st["h"] ** 2; Omd = st["omega_d"] / st["h"] ** 2
        # B1a: w(3400) = 0.01 ; B1b: X = 0.067, solved with the general (lambda = 0) machinery
        mua = math.exp(brentq(lambda x: bg(math.exp(x), 0.0, I0k, A34)["w"] - W_LINE_A, 0, 20, xtol=1e-14, rtol=1e-15))
        # KD1's B1b uses Om_d w0/(Om_r a^2) with Om_r from h: identical to X with omega_r (3 (100/c)^2 cancels via I0 = 3 H0^2 Om_d)
        mub = math.exp(brentq(lambda x: math.log(X_bbn(math.exp(x), 0.0, I0k) / X_LINE_B), 0, 40, xtol=1e-14, rtol=1e-15))
        ra = abs(mua / KD1["footings"][f]["B1"]["mu_B1a"] - 1); rb = abs(mub / KD1["footings"][f]["B1"]["mu_B1b"] - 1)
        d1[f] = dict(mu_B1a=mua, ref_a=KD1["footings"][f]["B1"]["mu_B1a"], rel_a=ra, mu_B1b=mub, ref_b=KD1["footings"][f]["B1"]["mu_B1b"], rel_b=rb)
        ok1 &= ra <= 1e-9 and rb <= 1e-9
        P(f"[{f}] KA1 KD1 FRW at lambda 0: mu_B1a {mua:.9e} vs {d1[f]['ref_a']:.9e} (rel {ra:.1e}); mu_B1b {mub:.9e} vs {d1[f]['ref_b']:.9e} (rel {rb:.1e})")
    RES["KA"]["KA1"] = dict(rows=d1, pass_=bool(ok1))
    d2 = {f: abs(SET[f]["od"] / SET[f]["ob"] - F1A[f]["R_B2"]) for f in FOOT}
    RES["KA"]["KA2"] = dict(R={f: SET[f]["od"] / SET[f]["ob"] for f in FOOT}, maxdiff=max(d2.values()), pass_=bool(max(d2.values()) <= 1e-9))
    P(f"KA2 F1A cold fit: R = {SET['canonical']['od']/SET['canonical']['ob']:.6f} / {SET['alt']['od']/SET['alt']['ob']:.6f}; max|d| {max(d2.values()):.1e}")
    import sympy as sp
    mu_, lam_, I0_, a_, q_ = sp.symbols("mu lam I0 a q", positive=True)
    Ks = 2 * mu_ ** 2 / lam_ * (1 - sp.sqrt(1 - lam_ * q_ ** 2))
    Zs = I0_ / (2 * mu_ ** 2 * a_ ** 3); rs = sp.sqrt(1 + lam_ * Zs ** 2); qb = Zs / rs
    res = [sp.simplify(sp.diff(Ks, q_).subs(q_, qb) - I0_ / a_ ** 3),
           sp.simplify(sp.diff(Ks, q_, 2).subs(q_, qb) - 2 * mu_ ** 2 * rs ** 3),
           sp.simplify(((1 + qb) * sp.diff(Ks, q_) - Ks).subs(q_, qb) - I0_ / a_ ** 3 - 2 * mu_ ** 2 * Zs ** 2 / (rs + 1)),
           sp.simplify(Ks.subs(q_, qb) - 2 * mu_ ** 2 * Zs ** 2 / (rs * (rs + 1)))]
    w0 = I0_ / (4 * mu_ ** 2); lim = sp.limit(((1 + qb) * sp.diff(Ks, q_) - Ks).subs(q_, qb), lam_, 0)
    res.append(sp.simplify(lim - I0_ * (1 + w0 / a_ ** 3) / a_ ** 3))
    mq = bg(79.43, 0.0, SET["canonical"]["I0"], 1.0); res_num = abs(mq["M"] / (79.43 * mq["Qb"]) - 1)
    ok3 = all(x == 0 for x in res) and res_num <= 1e-15
    RES["KA"]["KA3"] = dict(residuals=[str(x) for x in res], M_over_muQ_minus1=res_num, pass_=bool(ok3))
    P(f"KA3 kernel (sympy): residuals {[str(x) for x in res]}; quadratic M/(mu Qbar) - 1 = {res_num:.1e} -> {'PASS' if ok3 else 'FAIL'}")

# ------------------------------------------------------------------ engine: CK4 prefix + GL1 limber_n (n = 4)
CK4P = os.path.join(CL7, "CK4_kicked_carrier_cosmology", "ck4.py")
s4 = open(CK4P).read(); cut = s4.index("def grade(vk, Mmin, reading):")
E = {"__file__": CK4P, "__name__": "ck4_reused"}; argv0 = sys.argv; sys.argv = [CK4P]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s4[:cut], CK4P, "exec"), E)
sys.argv = argv0
gs = open(os.path.join(CL7, "GL1_limber_kernel_reread", "gl1.py")).read()
blk = gs[gs.index("NPOW = {\"n\": 0}"):gs.index("I2.limber_ratio = limber_n")]
L = dict(np=np, I2=E["I2"]); exec(compile(blk, "gl1_limber_n", "exec"), L); L["NPOW"]["n"] = 4; limber4 = L["limber_n"]
N3 = E["N3"]; I2 = E["I2"]; MC = E["MC"]; kgrid, zgrid, ref, c0 = E["kgrid"], E["zgrid"], E["ref"], E["c0"]
solve3, fs8_ratio, fs8_gate, p1d, kF, zF, PF, P1ref, dmF_ref = (E[k] for k in ("solve3", "fs8_ratio", "fs8_gate", "p1d", "kF", "zF", "PF", "P1ref", "dmF_ref"))
corner = [float(N3["ob"]), float(N3["H0"]), float(N3["ns"])]
P(f"engine: CK4 prefix + GL1 limber_n (n = 4); N3 corner omega_b {corner[0]} H0 {corner[1]} n_s {corner[2]}; c0 {c0:.6f}; RSS {rss():.0f} MB")
def GL(Mfun):
    R = solve3(kgrid, zgrid, jeans_all=Mfun) / ref
    S = limber4(MC, N3["H0"], kgrid, zgrid, R); c, _ = I2.best_amp_chi2(N3["X0"] * S)
    return R, dict(chi2=float(c), dchi2=float(c - c0), pass_=bool(c <= 18.48 and c - c0 <= 4.0))
def GF(R):
    rf, s8r, s80 = fs8_ratio(R); return dict(fs8_gate(rf), sigma8_ratio_z0=s80)
def GFo(Mfun):
    RF = solve3(kF, zF, jeans_all=Mfun) / dmF_ref; rat = p1d(PF * RF ** 2) / P1ref
    return dict(ratio_min=float(rat.min()), ratio_max=float(rat.max()), pass_=bool(np.all(np.abs(1 - rat) <= 0.10)))

if not MUT:
    gl1 = J(os.path.join(CL7, "GL1_limber_kernel_reread", "gl1.json"))
    cr = [c for c in gl1["labels"]["L2_QX3_iter2"]["corners"] if all(abs(x - y) < 1e-9 for x, y in zip(c["corner"], corner))]
    rows = cr[0]["rows_n4"] if cr else []
    ka4 = []; ok4 = bool(cr)
    for mu in (63.09573444801933, 100.0, 251.18864315095823, 630.9573444801937, 1000.0):
        refv = min(rows, key=lambda r: abs(math.log(r["mu"] / mu)))["dchi2"] if rows else float("nan")
        _, g = GL(lambda a, m=mu: m); d = abs(g["dchi2"] - refv); ok4 &= d <= max(0.05, 0.01 * abs(refv))
        ka4.append(dict(mu=mu, dchi2=g["dchi2"], ref=refv, absdiff=d))
        P(f"KA4 constant mu {mu:9.3f}: Delta chi2 {g['dchi2']:9.4f} vs GL1 L2 {refv:9.4f} (|d| {d:.2e})")
    b3 = [c for c in gl1["labels"]["L3_QX3_iter3"]["cells"] if abs(c["beta"] - 0.8) < 1e-9][0]
    _, g = GL(lambda a: b3["mu0"] * a ** (3 * b3["beta"])); d = abs(g["dchi2"] - b3["n4"]); ok4 &= d <= 0.05
    ka4.append(dict(beta=0.8, mu0=b3["mu0"], dchi2=g["dchi2"], ref=b3["n4"], absdiff=d))
    P(f"KA4 iter3 member beta 0.8 mu0 {b3['mu0']:.2f}: Delta chi2 {g['dchi2']:.4f} vs GL1 L3 {b3['n4']:.4f} (|d| {d:.2e})")
    RES["KA"]["KA4"] = dict(rows=ka4, corner_found=bool(cr), pass_=bool(ok4))
    Rc, gc = GL(lambda a: 1e12); gfc = GF(Rc); foc = GFo(lambda a: 1e12)
    dev = max([abs(r["Rf"] - 1) for r in gfc["rows"]] + [abs(foc["ratio_min"] - 1), abs(foc["ratio_max"] - 1)])
    ok5 = dev <= 1e-3 and abs(gc["dchi2"]) <= 0.01
    RES["KA"]["KA5"] = dict(max_ratio_dev=dev, dchi2=gc["dchi2"], pass_=bool(ok5))
    P(f"KA5 cold limit kJ 1e12: max |ratio - 1| {dev:.1e}, Delta chi2 {gc['dchi2']:.2e} -> {'PASS' if ok5 else 'FAIL'}")
    RES["KA_all"] = bool(all(v["pass_"] for v in RES["KA"].values()))
    P(f"KA all: {'PASS' if RES['KA_all'] else 'FAIL'}; RSS {rss():.0f} MB")

ZTAB = (0.0, 3.0, 10.0, 100.0, 1100.0, 3400.0, 1e5)
zr = np.logspace(math.log10(1 + Z_RUN), math.log10(1101.0), 200) - 1
zc1 = np.logspace(math.log10(101.0), math.log10(3401.0), 200) - 1

def member(mu, lam, I0, ob):
    """every column except GL/GF/GFo for one (mu, lam, I0)."""
    o = dict(mu=mu, lam=lam, q_max=(lam ** -0.5 if lam > 0 else None))
    Mz = {f"{z:g}": bg(mu, lam, I0, 1 / (1 + z))["M"] for z in ZTAB}; o["M_table"] = Mz; o["mu_K0"] = Mz["0"]
    o["B1a"] = dict(w=bg(mu, lam, I0, A34)["w"]); o["B1a"]["pass_"] = bool(o["B1a"]["w"] <= W_LINE_A)
    o["B1b"] = dict(X=X_bbn(mu, lam, I0)); o["B1b"]["pass_"] = bool(o["B1b"]["X"] <= X_LINE_B)
    Ms = np.array([bg(mu, lam, I0, 1 / (1 + z))["M"] for z in zr]); mono = bool(np.all(np.diff(Ms) > 0))   # zr increasing in z
    o["R2"] = dict(min_M=float(Ms.min()), z_at_min=float(zr[int(np.argmin(Ms))]), M_increasing_with_z=mono,
                   pass_=bool(Ms.min() >= M_LINE * (1 - 1e-9)), reading_361=bool(Ms.min() >= M_361))
    o["wrong_way"] = bool(not mono)
    ws = [bg(mu, lam, I0, 1 / (1 + z))["w"] for z in zc1]; hold = [bg(mu, lam, I0, 1 / (1 + z))["M"] / (1 + z) for z in zc1]
    b11 = bg(mu, lam, I0, 1 / 1101.0); ab = b11["rho8"] * (1 / 1101.0) ** 3 / I0 - 1
    o["C1"] = dict(max_w=float(max(ws)), min_comoving_hold=float(min(hold)), abundance_dev_1100=float(ab),
                   residual_hold_factor=float((KMAX_CMB / min(hold)) ** 2),
                   pass_=bool(max(ws) <= 1e-3 and min(hold) >= 10 * KMAX_CMB and abs(ab) <= 1e-3))
    o["CT"] = dict(c_T=1.0, pass_=True, reason="K depends on Q only; TT modes leave Q unchanged at linear order; no anisotropic stress")
    s0 = {}
    for k, v in S0_LINES.items(): s0[k] = dict(line=v, pass_=bool(lam == 0 or lam ** -0.5 >= v))
    o["S0"] = dict(rows=s0, pass_=bool(all(x["pass_"] for x in s0.values())))
    ql = S0_LINES["solar_system_1AU"] + S0_LINES["milky_way_220"]; Ml = M_at_q(mu, lam, ql)
    nf = None if Ml is None else (Ml * 9.58 * AU_MPC) ** 2 / 2
    o["CS"] = dict(M_loc=Ml, near_field=nf, pass_=bool(s0["solar_system_1AU"]["pass_"] and s0["milky_way_220"]["pass_"] and nf is not None and nf <= CASSINI))
    ratio_ta = TA * (1 + ZC) ** 3 * bg(mu, lam, I0, 1.0)["rho8"] / bg(mu, lam, I0, 1.0)["rho8"]   # = 5.55 x 27 in rho units
    Mta, Zta = M_at_density(mu, lam, I0, TA * (1 + ZC) ** 3)
    r3 = bg(mu, lam, I0, 1 / (1 + Z_RUN))["rho8"] / bg(mu, lam, I0, 1.0)["rho8"]
    zeq = brentq(lambda z: bg(mu, lam, I0, 1 / (1 + z))["rho8"] / bg(mu, lam, I0, 1.0)["rho8"] - TA * (1 + ZC) ** 3, 0, 100)
    zc_min = (r3 / TA) ** (1 / 3) - 1
    o["GC"] = dict(rho_ta_over_rho0=TA * (1 + ZC) ** 3, rho_z3_over_rho0=r3, z_where_background_equals_rho_ta=zeq, zc_min_inside_window=zc_min,
                   M_ta=Mta, q_ta=q_of_Z(mu, lam, Zta), jeans_length_Mpc=2 * math.pi / Mta, r_ta=R_TA,
                   captured=bool(2 * math.pi / Mta < R_TA), pass_=bool(not 2 * math.pi / Mta < R_TA))
    o["iii"] = dict(mu_K0=Mz["0"], line=III_LINE, pass_=bool(Mz["0"] <= III_LINE), S4_reported=bool(Mz["0"] <= S4_LINE))
    return o

# ------------------------------------------------------------------ MUTATE twin
if MUT:
    bites = {}
    for f in FOOT:
        I0 = SET[f]["I0"]; FO = {}
        for nm, mu in MEMBERS.items():
            o = member(mu, 0.0, I0, SET[f]["ob"])
            _, g = GL(lambda a, m=mu: m)
            FO[nm] = dict(MA_B1a=o["B1a"], MA_B1b=o["B1b"], MB_GL=g)
            P(f"[{f}] {nm} mu {mu:g}: M-A quadratic K: w(3400) {o['B1a']['w']:.3g} [{'PASS' if o['B1a']['pass_'] else 'FAIL'}], BBN X {o['B1b']['X']:.3g} "
              f"[{'PASS' if o['B1b']['pass_'] else 'FAIL'}]; M-B constant mu: GL Delta chi2 {g['dchi2']:.2f} [{'PASS' if g['pass_'] else 'FAIL'}]")
        st = KD1["footings"][f]["setting"]; cv = KD1["footings"][f]["converse"]["79.43282347242821"]["B1"]
        w_ = bg(79.43282347242821, 0.0, st["I0_Mpc-2"], A34)["w"]; x_ = X_bbn(79.43282347242821, 0.0, st["I0_Mpc-2"])
        rw, rx = abs(w_ / cv["w_z3400"] - 1), abs(x_ / cv["stiff_over_rad_BBN"] - 1)
        FO["MA_KD1_converse"] = dict(w=w_, w_ref=cv["w_z3400"], X=x_, X_ref=cv["stiff_over_rad_BBN"], rel=max(rw, rx), pass_=bool(max(rw, rx) <= 1e-6))
        P(f"[{f}] M-A at 79.43 on KD1's setting: w {w_:.6g} vs {cv['w_z3400']:.6g}, X {x_:.6g} vs {cv['stiff_over_rad_BBN']:.6g} (rel {max(rw, rx):.1e})")
        g0 = 2 * math.pi / 0.1 < R_TA; FO["MC_GC_const_0p1"] = dict(captured=bool(g0), pass_=bool(not g0))
        bites[f] = dict(MA=bool(all(not FO[n]["MA_B1b"]["pass_"] for n in MEMBERS) and FO["MA_KD1_converse"]["pass_"]),
                        MB=bool(all(not FO[n]["MB_GL"]["pass_"] for n in MEMBERS)), MC=bool(FO["MC_GC_const_0p1"]["pass_"]))
        P(f"[{f}] bites: M-A {bites[f]['MA']}, M-B {bites[f]['MB']}, M-C {bites[f]['MC']} (constant M 0.1: Jeans 62.8 Mpc vs r_ta 0.234, not captured)")
        RES["footings"][f] = FO
    RES["bites"] = bites; RES["MUTATE_all_bite"] = bool(all(all(v.values()) for v in bites.values()))
    P(f"MUTATE: {'ALL BITE' if RES['MUTATE_all_bite'] else 'SOME DO NOT BITE'}")
else:
    COLS = ("B1a", "B1b", "R2", "C1", "GL", "GF", "GFo", "CT", "S0", "CS", "GC", "iii")
    for f in FOOT:
        I0 = SET[f]["I0"]; FO = {}
        P(f"[{f}] setting: F1A B2 omega_b {SET[f]['ob']:.6f} omega_d {SET[f]['od']:.6f} h {SET[f]['h']:.5f}; I0 {I0:.6e} Mpc^-2")
        for nm, mu in MEMBERS.items():
            lam = lam_fix(mu, I0); o = member(mu, lam, I0, SET[f]["ob"]); Mf = M_of(mu, lam, I0)
            R, g = GL(Mf); o["GL"] = g; o["GF"] = GF(R); o["GFo"] = GFo(Mf)
            o["table"] = {c: ("PASS" if o[c]["pass_"] else "FAIL") for c in COLS}
            o["member_pass"] = bool(all(v == "PASS" for v in o["table"].values()))
            FO[nm] = o
            P(f"[{f}] {nm} mu {mu:g} lambda {lam:.4e} q_max {o['q_max']:.3e}: mu_K(0) READ {o['mu_K0']:.4f} Mpc^-1")
            P(f"[{f}]    M(z): " + ", ".join(f"z {k}: {v:.4g}" for k, v in o["M_table"].items()))
            P(f"[{f}]    B1a w {o['B1a']['w']:.2e} | B1b X {o['B1b']['X']:.2e} | R2 min M {o['R2']['min_M']:.2f} at z {o['R2']['z_at_min']:.2f} (M rises with z: {o['R2']['M_increasing_with_z']})"
              f" | C1 max w {o['C1']['max_w']:.1e}, min aM {o['C1']['min_comoving_hold']:.3g}, abund {o['C1']['abundance_dev_1100']:.1e}")
            P(f"[{f}]    GL chi2 {g['chi2']:.3f} d {g['dchi2']:+.3f} | GF Rf " + " ".join(f"{r['Rf']:.4f}" for r in o['GF']['rows'])
              + f" | GFo {o['GFo']['ratio_min']:.4f}-{o['GFo']['ratio_max']:.4f}")
            P(f"[{f}]    S0 " + ", ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in o["S0"]["rows"].items())
              + f" | CS M_loc {o['CS']['M_loc']} nf {o['CS']['near_field']} | GC M_ta {o['GC']['M_ta']:.4g} (q_ta {o['GC']['q_ta']:.2e}), Jeans {o['GC']['jeans_length_Mpc']*1e3:.3g} kpc vs 234 -> {'CAPTURED' if o['GC']['captured'] else 'free'}"
              f" | zc_min {o['GC']['zc_min_inside_window']:.3f}")
            P(f"[{f}]    table: " + " ".join(f"{k} {v}" for k, v in o["table"].items()) + f" -> member {'PASS' if o['member_pass'] else 'FAIL'}")
        RES["footings"][f] = FO
    # reported row RB: GL1's corrected-kernel iter3 member (beta 0.8, mu0 1258.93)
    beta, mu0 = 0.8, 1258.9254117941687; n = (2 + 2 * beta) / (1 + 2 * beta)
    RB = {}
    for f in FOOT:
        I0 = SET[f]["I0"]; q0 = (n - 1) * I0 / (2 * mu0 ** 2); A = I0 / (n * q0 ** (n - 1))
        lq = lambda a: math.log10(q0) - 3 / (n - 1) * math.log10(a)
        def Mpl(a):
            q = 10 ** lq(a); return (1 + q) * math.sqrt(n * (n - 1) * A * q ** (n - 2) / 2)
        a1 = 10 ** (math.log10(q0) * (n - 1) / 3)
        lX = math.log10((n - 1) / n) + lq(ABBN) + math.log10(I0) - 3 * math.log10(ABBN) - math.log10(3 * (100 / C_KMS) ** 2 * OMR_H2) + 4 * math.log10(ABBN)
        q11 = 10 ** lq(1 / 1101.0); w11 = q11 / (n * (1 + q11) - q11)
        Mw = np.array([Mpl(1 / (1 + z)) for z in zr])
        RB[f] = dict(n=n, q0=q0, z_q_equals_1=1 / a1 - 1, M_1100=Mpl(1 / 1101.0), M_3=Mpl(0.25), M_0=Mpl(1.0), w_1100=w11, w_early_limit=1 / (n - 1),
                     min_M_z3_1100=float(Mw.min()), z_at_min=float(zr[int(np.argmin(Mw))]),
                     log10_X_BBN=lX, i_pass=bool(lX <= math.log10(X_LINE_B)), ii_pass=bool(Mw.min() >= M_LINE), runs_wrong_way=bool(Mpl(0.25) < Mpl(1.0)))
        P(f"[{f}] RB iter3 member (beta 0.8, mu0 1259): K ~ q^{n:.4f}; q reaches 1 at z {1/a1-1:.1f}; w(1100) {w11:.3f} (early limit {1/(n-1):.2f});"
          f" M(1100) {Mpl(1/1101.0):.3e}, M(3) {Mpl(0.25):.3g}, M(0) {Mpl(1.0):.4g}; min M over z 3-1100 {Mw.min():.3g} at z {RB[f]['z_at_min']:.1f}; wrong way below: {RB[f]['runs_wrong_way']}; log10 X_BBN {lX:.1f} -> (i) {'PASS' if RB[f]['i_pass'] else 'FAIL'}, (ii) {'PASS' if RB[f]['ii_pass'] else 'FAIL'}")
    RES["RB"] = RB
    # curve infimum of mu_K(0): early-regime limit
    RES["mu_K0_infimum_analytic"] = M_LINE * (1 / (1 + Z_RUN)) ** 4.5
    # labels
    lab = {}; kill = {}
    for f in FOOT:
        FO = RES["footings"][f]; passing = [nm for nm in MEMBERS if FO[nm]["member_pass"]]
        block = {nm: [c for c, v in FO[nm]["table"].items() if v != "PASS"] for nm in MEMBERS}
        lab[f] = ("NO VERDICT (KA FAIL)" if not RES["KA_all"] else ("PASS: " + ", ".join(passing) if passing else
                  "FAIL: " + "; ".join(f"{nm} blocked by {', '.join(b)}" for nm, b in block.items())))
        meets = [nm for nm in MEMBERS if FO[nm]["B1b"]["pass_"] and FO[nm]["R2"]["pass_"] and FO[nm]["iii"]["pass_"]]
        wrong = any(FO[nm]["wrong_way"] for nm in MEMBERS)
        kill[f] = dict(fires=bool(not meets or wrong), members_meeting_i_ii_iii=meets, wrong_way=bool(wrong))
        P(f"[{f}] LABEL: {lab[f]}")
        P(f"[{f}] brief kill: {'FIRES' if kill[f]['fires'] else 'does not fire'} (members meeting (i)+(ii)+(iii): {meets}; wrong way: {wrong})")
    RES["label"] = lab; RES["brief_kill"] = kill
P(f"peak RSS {rss():.0f} MB; {time.time() - T0:.0f} s")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES["peak_rss_MB"] = rss(); RES["seconds"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
