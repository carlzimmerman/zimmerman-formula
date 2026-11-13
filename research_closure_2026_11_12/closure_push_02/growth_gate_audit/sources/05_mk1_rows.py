#!/usr/bin/env python3
"""MK1 rows 1, 2, 3, 4, 7, 8 (criteria b1fbded1e2, amendment A1 916f4e0e22) and known answers KA1, KA4, KA5, KA7, KA8, KA9, KA10.
    python3 mk1_rows.py   -> mk1_rows.json / mk1_rows.out, mk1_rows_MUTATE.json / mk1_rows_MUTATE.out (M-SIGN rows 3-4, M-2X row 8)
Read-only inputs: kd1.json (KD1: I0, mu_B1a, mu_B1b, mu_J), QX3 iter2.json (G2 corners), QX2's X-COP builder and psi_profile
(qx2.py source, executed read-only up to its iteration 1, plus the psi_profile function), QX5's groups() (source, read-only), S4's
lam_max (source), EW2 iter4's constants.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk1_lib as LB
MUT = "--mutate" in sys.argv
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MS, KPC, MPC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
C_KMS = 299792.458
CL6 = os.path.join(REPO, "closure_2026_11_06")
KD1 = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
ONE = json.load(open(os.path.join(REPO, "fable52_push", "ONE1_counted_once", "one1.json")))
XP = {f: float(ONE["foot"][f]["X"]) for f in LB.FOOT}
RES = dict(lane="MK1", file="mk1_rows", criteria="b1fbded1e2 (A1 916f4e0e22)", note=LB.NOTE, KA={}, rows={}, mutate={})
SIG = 1.0
P(f"MK1 rows 1-4, 7, 8. X = {XP['canonical']:.4f} / {XP['alt']:.4f} (PD1's share via one1.json). {LB.NOTE}")

# ============================================================== row 1: CMB and background (KD1's B1a line; closed form)
H_LIT = 0.674; Z_B1A = 3400.0
P("\nROW 1 CMB and background: w(a) = w0/(w0 + a^3), w0 = I0/(4 mu^2); graded line KD1 B1a w(z 3400) <= 0.01")
ka4 = 3 * (70.0 / C_KMS) ** 2 * 0.26 / 4
RES["KA"]["KA4 FB1 arithmetic I0/4 (H0 70, Omega_c 0.26)"] = dict(value=ka4, ref=1.063e-8, ok=bool(abs(ka4 / 1.063e-8 - 1) <= 1e-3))
P(f"KA4 FB1's w0 arithmetic: I0/4 = {ka4:.5e} Mpc^-2 (FB1 1.063e-8) -> {'PASS' if RES['KA']['KA4 FB1 arithmetic I0/4 (H0 70, Omega_c 0.26)']['ok'] else 'FAIL'}")
R1 = {}
for f in LB.FOOT:
    kd = KD1["footings"][f]; I0 = kd["setting"]["I0_Mpc-2"]; a = 1 / (1 + Z_B1A)
    muB1a = math.sqrt(I0 * 0.99 / (4 * 0.01 * a ** 3)); ref = kd["B1"]["mu_B1a"]
    RES["KA"][f"KA7 KD1 mu_B1a {f}"] = dict(value=muB1a, ref=ref, ok=bool(abs(muB1a / ref - 1) <= 1e-6))
    Om_r = kd["B1"]["Omega_r"]; Om_d = I0 / (3 * (100 * H_LIT / C_KMS) ** 2)
    rows = []
    for mu in (0.1, 1.0, 37.0, muB1a, 1e3, 2.51e4, 1e5, kd["B1"]["mu_B1b"]):
        w0 = I0 / (4 * mu * mu); w1100 = w0 / (w0 + (1 / 1101.0) ** 3); zd = (4 * mu * mu / I0) ** (1 / 3) - 1; ax = math.sqrt(Om_d * w0 / Om_r)
        rows.append(dict(mu=mu, w0=w0, w_z1100=w1100, w_z3400=w0 / (w0 + a ** 3), z_dustlike=zd, a_stiff_eq_radiation=ax, z_stiff_eq_radiation=1 / ax - 1))
    R1[f] = dict(interval=[muB1a, None], I0=I0, Omega_d=Om_d, Omega_r=Om_r, mu_B1b_BBN_reported=kd["B1"]["mu_B1b"], table=rows,
                 quality="background line (KD1 B1a), not a likelihood: the record's CAMB machinery cannot take the stiff partner (criteria section 2)")
    P(f"[{f}] I0 {I0:.4e} Mpc^-2; mu_B1a = {muB1a:.3f} Mpc^-1 (KD1 {ref:.3f}) -> interval [{muB1a:.1f}, inf). BBN B1b (reported) {kd['B1']['mu_B1b']:.4g}")
    for r in rows:
        P(f"   mu {r['mu']:.4g}: w0 {r['w0']:.3e}, w(z 1100) {r['w_z1100']:.3e}, w(z 3400) {r['w_z3400']:.3e}, dust-like below 1+z = {r['z_dustlike'] + 1:.4g}; "
          f"stiff = radiation at a {r['a_stiff_eq_radiation']:.2e} (z {r['z_stiff_eq_radiation']:.3g})")
RES["rows"]["1 CMB and background"] = R1

# ============================================================== row 2: clustering scale (KD1 G9a / QX3 iter2 G2)
P("\nROW 2 clustering scale: Jeans wavenumber k_J = mu_K (physical, QX3 Lean); graded line KD1 G9a mu_K >= mu_J")
QX3 = json.load(open(os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.json")))
def find_key(o, name, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if name in k and isinstance(v, (int, float)): acc.append((k, v))
            find_key(v, name, acc)
    elif isinstance(o, list):
        for v in o: find_key(v, name, acc)
    return acc
mumins = find_key(QX3, "mu_min", [])
R2 = {}
for f in LB.FOOT:
    kd = KD1["footings"][f]; muJ = kd["G9a_jeans"]["mu_J"]; I0 = kd["setting"]["I0_Mpc-2"]
    rho_d0 = I0 * (C_KMS * 1e3) ** 2 / (8 * math.pi * G) / MPC ** 2      # rho_d0 = 3 H0^2 Omega_d/(8 pi G) = I0 c^2/(8 pi G) [kg/m^3]
    def cs(z, mu): return math.sqrt(4 * math.pi * G * rho_d0 * (1 + z) ** 3) / (mu / MPC) / 1e3   # km/s
    stand = dict(growth_k_0p2h_from_z3400=0.2 * H_LIT * 3401, forest_k_3h_from_z3400=3.0 * H_LIT * 3401)
    R2[f] = dict(interval=[muJ, None], mu_J=muJ, QX3_G2_mu_min=[v for _, v in mumins], cs_today_kms_at_muJ=cs(0, muJ), cs_z3400_kms_at_muJ=cs(3400, muJ),
                 jeans_length_kpc_at_muJ=2 * math.pi / muJ * 1e3, stand_ins=stand, quality="record value (KD1 G9a on QX3 iter2's CLASS machinery), not recomputed here")
    P(f"[{f}] mu_J = {muJ:.4g} Mpc^-1 (lambda_J = 2 pi/mu_J = {2 * math.pi / muJ * 1e3:.3f} kpc physical) -> interval [{muJ:.4g}, inf). QX3 G2 mu_min values {[round(v) for _, v in mumins][:8]}")
    P(f"   sound speed at the mean density, mu_J: today {cs(0, muJ):.3e} km/s, z 3400 {cs(3400, muJ):.3e} km/s; comoving Jeans wavenumber mu/(1+z): z 0 {muJ:.3g}, z 1100 {muJ / 1101:.3g}, z 3400 {muJ / 3401:.3g} Mpc^-1")
    P(f"   stand-ins (reported): growth k <= 0.2 h/Mpc from z 3400 needs mu >= {stand['growth_k_0p2h_from_z3400']:.0f}; forest k <= 3 h/Mpc from z 3400 needs mu >= {stand['forest_k_3h_from_z3400']:.0f}")
RES["rows"]["2 clustering scale"] = R2

# ============================================================== rows 3 and 4: X-COP and groups
# QX2's builder (read-only exec up to iteration 1) and its psi_profile
q2src = open(os.path.join(CL6, "QX2_clusters", "qx2.py")).read()
pre = q2src[:q2src.index("# ---------- iter 1: plain law ----------")]
Q2 = dict(__file__=os.path.join(CL6, "QX2_clusters", "qx2.py"), __name__="qx2_prefix"); _argv = sys.argv; sys.argv = [sys.argv[0]]
exec(compile(pre, "qx2.py", "exec"), Q2); sys.argv = _argv
fsrc = q2src[q2src.index("def psi_profile(c):"):q2src.index("for c in XC:\n    rr, psi = psi_profile(c)")]
exec(compile(fsrc, "qx2.py:psi_profile", "exec"), Q2)
XC, law_M, gateQ2, A0Q = Q2["XC"], Q2["law_M"], Q2["gate"], Q2["A0"]
def psi_prof_zero(c, zero_mult):
    """QX2's psi_profile with the zero at zero_mult x R200 (3 = QX2's graded, 10 = QX6's variant)."""
    if zero_mult == 3: return Q2["psi_profile"](c)
    c2 = dict(c); c2["R200_kpc"] = c["R200_kpc"] * zero_mult / 3.0; return Q2["psi_profile"](c2)
def IK(c, zero_mult):
    rr, psi = psi_prof_zero(c, zero_mult)
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (np.abs(psi[1:]) * (rr[1:] * KPC) ** 2 + np.abs(psi[:-1]) * (rr[:-1] * KPC) ** 2) * np.diff(rr * KPC))])
    return rr, integ
for zm in (3, 10):
    for c in XC: c[f"_IK{zm}"] = IK(c, zm)
def MKc(c, r_kpc, mu, zm=3):
    rr, integ = c[f"_IK{zm}"]; m = mu / MPC
    return m * m / G * float(np.interp(r_kpc, rr, integ)) / MS
def gate_x(mu, form, sig=1.0, zm=3):
    if form == "exact":
        model = lambda c, z, a0: law_M(z["M_b"] + sig * MKc(c, z["r_kpc"], mu, zm), z["r_kpc"], a0)[0] if z["M_b"] + sig * MKc(c, z["r_kpc"], mu, zm) > 0 else 1e-30
    else:
        model = lambda c, z, a0: max(law_M(z["M_b"], z["r_kpc"], a0)[0] + sig * MKc(c, z["r_kpc"], mu, zm), 1e-30)
    return gateQ2(model)
MUGRID = 10 ** np.arange(-3.0, 4.0001, 0.01)
def interval_of(passes):
    idx = np.where(passes)[0]
    if len(idx) == 0: return None, []
    runs = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p + 1: runs.append((MUGRID[s], MUGRID[p])); s = i
        p = i
    runs.append((MUGRID[s], MUGRID[p])); return [float(MUGRID[idx[0]]), float(MUGRID[idx[-1]])], [(float(a), float(b)) for a, b in runs]

P("\nROW 3 X-COP (QX2 builder, 35 points; G-X |mean| <= 0.05, rms <= 0.10)")
# KA1: QX2 iteration 5 (ADDITIVE, zero 3 R200)
k1 = gate_x(0.1, "additive")
def mean0(form, f, sig=1.0, zm=3):
    a0 = A0Q[f]
    def mean_at(mu): return gate_x(mu, form, sig, zm)[f]["mean"]
    lo, hi = 0.1, 1e3
    if mean_at(lo) * mean_at(hi) > 0: return None
    for _ in range(80):
        mid = math.sqrt(lo * hi); lo, hi = (mid, hi) if mean_at(mid) > 0 else (lo, mid)
    return math.sqrt(lo * hi)
for f, rm, rz in (("canonical", 0.4644, 1.778), ("alt", 0.4317, 1.736)):
    m0 = mean0("additive", f)
    RES["KA"][f"KA1 QX2 iter5 {f}"] = dict(mean_at_0p1=k1[f]["mean"], ref=rm, mu_mean0=m0, ref_mu=rz, ok=bool(abs(k1[f]["mean"] - rm) <= 1e-3 and abs(m0 - rz) <= 0.01))
    P(f"KA1 [{f}] ADDITIVE at mu 0.1: mean {k1[f]['mean']:+.4f} (QX2 {rm:+.4f}); mean-zero mu {m0:.3f} (QX2 {rz}) -> {'PASS' if RES['KA'][f'KA1 QX2 iter5 {f}']['ok'] else 'FAIL'}")
R3 = {}
for form in ("exact", "additive"):
    for zm in (3, 10):
        sc = [gate_x(mu, form, SIG, zm) for mu in MUGRID]
        for f in LB.FOOT:
            ps = np.array([s[f]["PASS"] for s in sc]); rms = np.array([s[f]["rms"] for s in sc]); mn = np.array([s[f]["mean"] for s in sc])
            iv, runs = interval_of(ps); ib = int(np.argmin(rms)); m0 = mean0(form, f, SIG, zm)
            key = f"{form} zero {zm} R200 {f}"
            R3[key] = dict(interval=iv, runs=runs, n_pass=int(ps.sum()), min_rms=float(rms[ib]), mu_min_rms=float(MUGRID[ib]), mean_at_min_rms=float(mn[ib]), mu_mean0=m0,
                           rms_at_mean0=(gate_x(m0, form, SIG, zm)[f]["rms"] if m0 else None), graded=bool(form == "exact" and zm == 3))
            P(f"  [{key}]{' GRADED' if R3[key]['graded'] else ''}: passing grid points {int(ps.sum())} -> interval {iv}; min rms {rms[ib]:.3f} at mu {MUGRID[ib]:.3g} (mean {mn[ib]:+.3f}); "
              f"mean 0 at mu {m0 if m0 is None else round(m0, 3)} (rms {R3[key]['rms_at_mean0'] if m0 is None else round(R3[key]['rms_at_mean0'], 3)})")
RES["rows"]["3 X-COP"] = R3

P("\nROW 4 groups (Lovisari 2015, 20 groups, R2500 and R500; bracket of mean Delta over stars 0..gas must overlap [-0.05, 0.05])")
q5src = open(os.path.join(CL6, "QX5_cluster_terms", "qx5.py")).read()
Q5 = dict(os=os, np=np, math=math, DATA=os.path.join(REPO, "real_research", "data"))
exec(compile(q5src[q5src.index("def groups():"):q5src.index("XC, SP, EL, LE, GR = ")], "qx5.py:groups", "exec"), Q5)
GR = Q5["groups"]()
def glaw_(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)
for gp in GR:
    sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"]); rz = 3 * 1.5 * gp["R5"]
    rr = np.geomspace(1e-3 * gp["R25"], rz, 4000); Mr = gp["M25"] * (rr / gp["R25"]) ** sl
    gacc = G * Mr * MS / (rr * KPC) ** 2; seg = 0.5 * (gacc[1:] + gacc[:-1]) * np.diff(rr * KPC)
    psi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (np.abs(psi[1:]) * (rr[1:] * KPC) ** 2 + np.abs(psi[:-1]) * (rr[:-1] * KPC) ** 2) * np.diff(rr * KPC))])
    gp["_IK"] = (rr, integ); gp["_sl"] = sl
def gate_g(mu, form, sig=1.0, share=5.41):
    out = {}
    for f, a0 in A0Q.items():
        gm = {}; ch = []
        for fst in (0.0, 1.0):
            d = []
            for gp in GR:
                for p in gp["pts"]:
                    rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); mk = sig * (mu / MPC) ** 2 / G * float(np.interp(p["r_kpc"], *gp["_IK"])) / MS
                    if form == "exact":
                        Mt = Mb + mk; Ml = glaw_(G * Mt * MS / rm ** 2, a0) * rm ** 2 / G / MS if Mt > 0 else 1e-30
                    else:
                        Ml = max(glaw_(G * Mb * MS / rm ** 2, a0) * rm ** 2 / G / MS + mk, 1e-30)
                    d.append(math.log10(p["M_obs"] / Ml))
                    if p["r_kpc"] == gp["R5"]: ch.append((Ml - Mb) / (share * Mb))
            gm[fst] = float(np.mean(d))
        lo, hi = sorted([gm[0.0], gm[1.0]])
        out[f] = dict(mean_star0=gm[0.0], mean_star1=gm[1.0], PASS=bool(lo <= 0.05 and hi >= -0.05), charge_over_share_R500_median=float(np.median(ch)))
    return out
g0 = gate_g(0.0, "exact")
for f, ref in (("canonical", (0.196, 0.359)), ("alt", (0.158, 0.320))):
    v = (g0[f]["mean_star1"], g0[f]["mean_star0"]); dv = max(abs(v[0] - ref[0]), abs(v[1] - ref[1]))
    RES["KA"][f"KA9 QX5 groups {f}"] = dict(value=v, ref=ref, ok=bool(dv <= 2e-3))
    P(f"KA9 [{f}] groups at mu 0: [{v[0]:+.3f}, {v[1]:+.3f}] (QX5 [{ref[0]:+.3f}, {ref[1]:+.3f}]) -> {'PASS' if dv <= 2e-3 else 'FAIL'}")
R4 = {}
for form in ("exact", "additive"):
    sc = [gate_g(mu, form, SIG) for mu in MUGRID]
    for f in LB.FOOT:
        ps = np.array([s[f]["PASS"] for s in sc]); iv, runs = interval_of(ps)
        best = int(np.argmin([min(abs(s[f]["mean_star0"]), abs(s[f]["mean_star1"])) for s in sc]))
        key = f"{form} {f}"
        R4[key] = dict(interval=iv, runs=runs, graded=bool(form == "exact"),
                       RB1_charge_over_share_at_pass=([sc[i][f]["charge_over_share_R500_median"] for i in np.where(ps)[0][[0, -1]]] if ps.any() else None),
                       bracket_at_mu_0p1=[sc[int(np.argmin(np.abs(MUGRID - 0.1)))][f]["mean_star1"], sc[int(np.argmin(np.abs(MUGRID - 0.1)))][f]["mean_star0"]],
                       closest_mu=float(MUGRID[best]))
        P(f"  [{key}]{' GRADED' if form == 'exact' else ''}: interval {iv} (runs {[(round(a, 3), round(b, 3)) for a, b in runs]}); RB1 charge/(5.41 M_b) at R500 at the interval ends "
          f"{None if R4[key]['RB1_charge_over_share_at_pass'] is None else [round(x, 3) for x in R4[key]['RB1_charge_over_share_at_pass']]}")
RES["rows"]["4 groups"] = R4

# ============================================================== row 7: Solar System (EW2 iter4's cassini)
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; R_SAT = 9.5826 * AU; PHI0 = (600e3) ** 2; SAT, HEES = 7.0e-15, 9.0e-27
def cassini(mu, phi0=PHI0):
    m2 = (mu / MPC) ** 2; dg = m2 * GM_SUN / 2 + m2 * phi0 * R_SAT / 3; return dg, m2 * phi0 / 3
dg8, _ = cassini(2.04e4)
RES["KA"]["KA8 EW2 Saturn at 2.04e4"] = dict(value=dg8, ref=7.5e-14, ok=bool(abs(dg8 / 7.5e-14 - 1) <= 0.02))
P(f"\nROW 7 Solar System (EW2 iter4 cassini; Saturn line 7.0e-15 m/s^2, Hees Q2 9e-27 s^-2; Phi0 (600 km/s)^2)")
P(f"KA8 EW2's number: dg(Saturn) at mu 2.04e4 = {dg8:.3e} (EW2 7.5e-14) -> {'PASS' if RES['KA']['KA8 EW2 Saturn at 2.04e4']['ok'] else 'FAIL'}")
mu_sat = MPC * math.sqrt(SAT / (GM_SUN / 2 + PHI0 * R_SAT / 3)); mu_q2 = MPC * math.sqrt(3 * HEES / PHI0); mu7 = min(mu_sat, mu_q2)
# reported: a capped Milky Way potential at the Sun (M_b 6e10 Msun, point mass on the law, X = PD1's share; this lane's solver at m -> 0)
R7 = {}
for f in LB.FOOT:
    a0 = LB.A0[f]; Mmw = 6e10 * MS; rM = math.sqrt(G * Mmw / a0); s = math.sqrt(G * Mmw * a0); p0 = LB.capped_profile(0.0, XP[f])
    phis = abs(float(np.interp(math.log(8.2 * KPC / rM), np.log(p0["x"]), p0["phi"]))) * s
    mu_cap = MPC * min(math.sqrt(SAT / (GM_SUN / 2 + phis * R_SAT / 3)), math.sqrt(3 * HEES / phis))
    R7[f] = dict(interval=[0.0, mu7], mu_saturn=mu_sat, mu_hees=mu_q2, reported_capped_MW=dict(Phi_sun=phis, sqrtPhi_kms=math.sqrt(phis) / 1e3, mu_max=mu_cap))
    P(f"[{f}] Saturn line -> mu <= {mu_sat:.4g}; Q2 line -> mu <= {mu_q2:.4g}; interval [0, {mu7:.4g}]. Reported: capped MW (M_b 6e10) |Phi_sun| = ({math.sqrt(phis) / 1e3:.0f} km/s)^2 -> mu <= {mu_cap:.4g}")
RES["rows"]["7 Solar System"] = R7

# ============================================================== row 8 (reported): where the static dust alone exceeds the share; SCS1 reading
P("\nROW 8 consistency (reported, not graded)")
def m_alone(X):
    p0 = LB.capped_profile(0.0, X); x = p0["x"]; I = float(np.trapz(x * x * np.abs(p0["phi"]), x)); return math.sqrt(X / I), I, p0["xc"]
R8 = {}
for f in LB.FOOT:
    a0 = LB.A0[f]; rowa = []
    for lm, X in [(8, XP[f]), (9, XP[f]), (10, XP[f]), (11, XP[f]), (12, XP[f]), (13, 5.41), (14, 5.41)]:
        mX, I, xc = m_alone(X); rM = math.sqrt(G * 10 ** lm * MS / a0); mu = mX / rM * MPC
        rowa.append(dict(logMb=lm, share=X, m_alone=mX, mu_alone=mu, r_c_kpc=xc * rM / KPC, deep_closed_form_m=math.sqrt(9 / (4 * X * X))))
    R8[f] = dict(alone=rowa)
    P(f"[{f}] mu_K above which the static dust alone exceeds the share (dust-free capped potential, to r_c): " + "; ".join(f"log M_b {r['logMb']} (share {r['share']:.2f}): {r['mu_alone']:.3g}/Mpc (r_c {r['r_c_kpc']:.0f} kpc)" for r in rowa))
P("   SCS1 closed form omega^2 = K G[(1 - K m) k^2 - mu_K^2]/(mu_K^2 + K m k^2): modes with k < mu_K/sqrt(1 - K m) grow (Jeans, at the free-fall rate, bounded in k).")
RES["rows"]["8 consistency"] = R8

# ============================================================== KA5 and KA10 (solver)
P("\nSolver known answers")
X = XP["canonical"]; br = LB.capped_branch([1e-3, 1e-2, 0.1], X); d5 = []
for m, p in zip([1e-3, 1e-2, 0.1], br):
    kd_ = LB.enclosed_dust_direct(p, m); d5.append(float(np.max(np.abs(kd_ - p["kap"])) / abs(p["kap"][-1])))
x = np.geomspace(1e-6, 50.0, 200001); rc = 50.0; phic = 1.7; phi = -(phic + np.log(rc / x))
num = np.concatenate([[0.0], np.cumsum(0.5 * (x[1:] ** 2 * np.abs(phi[1:]) + x[:-1] ** 2 * np.abs(phi[:-1])) * np.diff(x))])
cf = LB.deep_dust_closed(x, rc, phic, 1.0, 1.0); sel = x > 1e-2; dcf = float(np.max(np.abs(num[sel] / cf[sel] - 1)))
RES["KA"]["KA5 dust enclosed mass"] = dict(direct_vs_ode=d5, closed_form=dcf, ok=bool(max(d5) <= 1e-5 and dcf <= 1e-4))
P(f"KA5 static dust: direct quadrature vs the solver at m 1e-3/1e-2/0.1: rel {', '.join(f'{v:.1e}' for v in d5)} (line 1e-5); deep-law closed form vs quadrature max rel {dcf:.1e} (line 1e-4) -> "
  f"{'PASS' if RES['KA']['KA5 dust enclosed mass']['ok'] else 'FAIL'}")
s4src = open(os.path.join(REPO, "rebuild_2026_10_22", "S4_v3_muK_clusters", "s4_v3_muk_clusters.py")).read()
S4 = dict(np=np); exec(compile([l for l in s4src.splitlines() if l.startswith("def lam_max(")][0], "s4:lam_max", "exec"), S4)
m10 = 0.003; x3 = 3 * MPC / (12 * KPC); lam_s4 = float(S4["lam_max"](m10 / (12 * KPC), 12 * KPC)); lam_me = LB.lam_max(m10)
pu = LB.uncapped_profile(0.0, x3, 30 * MPC / (12 * KPC)); C = (-1 / x3 + lam_me + math.log(x3)) - float(LB.phi_law(x3))
xx = np.geomspace(1.0, x3, 400001); ell = 0.5 + np.sqrt(0.25 + xx * xx); integ = ell / xx ** 2
ph_num = float(LB.phi_law(1.0, C)) + float(np.sum(0.5 * (integ[1:] + integ[:-1]) * np.diff(xx)))
d10 = max(abs(lam_s4 / lam_me - 1), abs(ph_num / (-1 / x3 + lam_me + math.log(x3)) - 1))
RES["KA"]["KA10 S4 zero point"] = dict(lam_s4=lam_s4, lam_mine=lam_me, phi3_numeric=ph_num, phi3_target=-1 / x3 + lam_me + math.log(x3), rel=d10, ok=bool(d10 <= 1e-6))
P(f"KA10 S4 zero point: lambda_max S4 {lam_s4:.8f} vs mine {lam_me:.8f}; law potential integrated numerically to 3 Mpc {ph_num:.8f} vs target {-1 / x3 + lam_me + math.log(x3):.8f}; rel {d10:.1e} -> "
  f"{'PASS' if d10 <= 1e-6 else 'FAIL'}")

# ============================================================== MUTATE: M-SIGN on rows 3 and 4; M-2X on row 8 (separate outputs)
MU = dict(lane="MK1", file="mk1_rows_MUTATE", criteria=RES["criteria"], arms={})
OUTM = []
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
sc = [gate_x(mu, "exact", -1.0, 3) for mu in MUGRID]
for f in LB.FOOT:
    ps = np.array([s[f]["PASS"] for s in sc]); rms = np.array([s[f]["rms"] for s in sc]); iv, runs = interval_of(ps); ib = int(np.argmin(rms))
    MU["arms"][f"M-SIGN row 3 {f}"] = dict(interval=iv, min_rms=float(rms[ib]), mu_min_rms=float(MUGRID[ib]), mean_at_0p1=sc[int(np.argmin(np.abs(MUGRID - 0.1)))][f]["mean"],
                                           mean_at_1=sc[int(np.argmin(np.abs(MUGRID - 1)))][f]["mean"])
    g = R3[f"exact zero 3 R200 {f}"]
    PM(f"M-SIGN row 3 [{f}]: interval {iv}; min rms {rms[ib]:.3f} at {MUGRID[ib]:.3g}; mean at mu 1 {MU['arms'][f'M-SIGN row 3 {f}']['mean_at_1']:+.3f} "
       f"(primary: min rms {g['min_rms']:.3f} at {g['mu_min_rms']:.3g})")
sc = [gate_g(mu, "exact", -1.0) for mu in MUGRID]
for f in LB.FOOT:
    ps = np.array([s[f]["PASS"] for s in sc]); iv, runs = interval_of(ps)
    MU["arms"][f"M-SIGN row 4 {f}"] = dict(interval=iv, runs=runs); PM(f"M-SIGN row 4 [{f}]: interval {iv} (primary {R4[f'exact {f}']['interval']})")
for f in LB.FOOT:
    a0 = LB.A0[f]; rows2 = []
    for lm in (8, 10, 12):
        mX, I, xc = m_alone(2 * XP[f]); rM = math.sqrt(G * 10 ** lm * MS / a0); rows2.append(dict(logMb=lm, mu_alone=mX / rM * MPC))
    MU["arms"][f"M-2X row 8 {f}"] = rows2
    prim = {r["logMb"]: r["mu_alone"] for r in R8[f]["alone"]}
    PM(f"M-2X row 8 [{f}]: mu where the dust alone exceeds the share: " + "; ".join(f"log M_b {r['logMb']}: {r['mu_alone']:.3g} (primary {prim[r['logMb']]:.3g})" for r in rows2))

ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all_pass"] = ka_ok
P(f"\nKnown answers here: {sum(v['ok'] for v in RES['KA'].values())} of {len(RES['KA'])} PASS -> {'ALL PASS' if ka_ok else 'A KNOWN ANSWER FAILED'}")
P(f"runtime {time.time() - T0:.0f} s"); P(LB.NOTE)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "mk1_rows.json"), "w"), indent=1)
open(os.path.join(HERE, "mk1_rows.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(MU), open(os.path.join(HERE, "mk1_rows_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "mk1_rows_MUTATE.out"), "w").write("\n".join(OUTM + [LB.NOTE]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
