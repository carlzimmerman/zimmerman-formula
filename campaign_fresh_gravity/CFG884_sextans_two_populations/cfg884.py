"""CFG884 -- do the two Sextans stellar populations need extended mass beyond one CFG877 finite clump?
Criteria: FROZEN_CRITERIA.md (eb5c21709, committed alone before this script).
Run: OMP_NUM_THREADS=1 python3 cfg884.py   (CFG884_MUTATE=injectC|injectX -> separate outputs).
kappa = 1/2 FITTED; footings never pooled; raw data, framework-native only; not theory closed."""
import os, csv, json, math, itertools, numpy as np
from scipy.integrate import cumulative_simpson

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG884_MUTATE", ""); assert MUT in ("", "injectC", "injectX"); SUF = f"_MUTATE_{MUT}" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16          # CFG877's constants
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0          # pc
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))    # CFG877's nu
NG = 20001                                                             # nodes per Simpson segment (odd)

# ---------------- inputs ----------------
INP = json.load(open(os.path.join(HERE, "inputs_tolstoy2025_table2.json")))
POPS = {p["label"]: p for p in INP["populations"]}; D0 = INP["distance_kpc"] * 1e3      # pc
LVD = [r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))) if r["key"] == "sextans_1"][0]
MV_APP, ELL, RH_LVD_ARCMIN = float(LVD["apparent_magnitude_v"]), float(LVD["ellipticity"]), float(LVD["rhalf"])
R870 = json.load(open(os.path.join(LANES, "CFG870_cored_component_joint", "cfg870_results.json")))
R877 = json.load(open(os.path.join(LANES, "CFG877_finite_cold_clump", "cfg877_results.json")))
VX = {f: R870[f]["Vx"] for f in A0}
MCL = {f: 81 * (VX[f] * 1e3 / math.sqrt(2)) ** 4 / (4 * G * A0[f]) for f in A0}      # kg
def LV(D_pc): return 10 ** (0.4 * (4.83 - (MV_APP - 5 * math.log10(D_pc / 10.0))))
def ang(D_pc, deg): return D_pc * math.tan(math.radians(deg))

# ---------------- Jeans kernel: <sigma_los^2>_aperture = sum(w * g(s)) * PC ----------------
def simpson_w(n, h):
    w = np.ones(n); w[1:-1:2] = 4.0; w[2:-1:2] = 2.0; return w * h / 3.0
def nu_plummer(s, a): return 3.0 / (4 * math.pi * a ** 3) * (1 + (s / a) ** 2) ** -2.5
_KC = {}
def kernel(a, beta, Rmax, cache=True):
    """Plummer tracer (scale a, pc), constant beta, projected-number-weighted average inside circular aperture Rmax (pc
    or inf). Returns nodes s (pc) and weights w (1/pc * pc = dimensionless per pc) so that <sigma^2> = sum(w g) * PC."""
    key = (round(a, 9), beta if math.isfinite(Rmax) else 0.0, round(Rmax, 9) if math.isfinite(Rmax) else -1)
    if key in _KC: return _KC[key]
    lo, hi = 1e-4 * a, 1e4 * a
    if not math.isfinite(Rmax):
        u = np.linspace(math.log(lo), math.log(hi), NG); s = np.exp(u)
        W = (4 * math.pi / 3) * s ** 3 * nu_plummer(s, a)
        res = (s, simpson_w(NG, u[1] - u[0]) * s * W)
    else:
        Nap = Rmax ** 2 / (Rmax ** 2 + a ** 2); cJ = 4 * math.pi * (1 - 2 * beta / 3) / (3 - 2 * beta)
        u = np.linspace(math.log(min(lo, 1e-4 * Rmax)), math.log(Rmax), NG); s1 = np.exp(u)
        W1 = nu_plummer(s1, a) * cJ * s1 ** 3 / Nap; w1 = simpson_w(NG, u[1] - u[0]) * s1 * W1
        tmax = math.acosh(max(hi / Rmax, 2.0)); t = np.linspace(0.0, tmax, NG); h = t[1] - t[0]
        r = Rmax * np.cosh(t); q = Rmax * np.sinh(t); d = Rmax * np.exp(-t)                     # d = r - q (stable)
        K = 4 * math.pi * r * (d - beta * d * d * (2 * r + q) / (3 * r * r))
        J = cJ * Rmax ** (3 - 2 * beta) + cumulative_simpson(r ** (-2 * beta) * K * q, dx=h, initial=0.0)
        W2 = nu_plummer(r, a) * r ** (2 * beta) * J / Nap; w2 = simpson_w(NG, h) * q * W2
        res = (np.concatenate([s1, r]), np.concatenate([w1, w2]))
    if cache: _KC[key] = res
    return res
def sig2(kern, g): s, w = kern; return float(np.dot(w, g(s))) * PC          # m^2/s^2

# ---------------- potentials (g in m/s^2, r in pc) ----------------
def Fpl(r, b): x = r / b; return x ** 3 / (1 + x * x) ** 1.5
def g_N(r, Mst_kg, comps): return G * Mst_kg * sum(f * Fpl(r, b) for f, b in comps) / (r * PC) ** 2
def g_law(r, Mst_kg, comps, a0, gext=0.0):
    gN = g_N(r, Mst_kg, comps); return gN * nu_e((gN + gext) / a0)
def g_comp(r, Vx, Mcl):
    rm = r * PC; M = np.minimum((Vx * 1e3) ** 2 * rm ** 3 / (G * (rm ** 2 + (RC * PC) ** 2)), Mcl); return G * M / rm ** 2

# ---------------- statistic and classes ----------------
FLOOR = 0.05
def zstat(so, em, ep, sp):
    e = math.log(so / (so - em)) if sp < so else math.log((so + ep) / so)
    return math.log(so / sp) / math.sqrt(e * e + FLOOR ** 2)

UPS = (1.0, 2.0, 3.0); CG = (math.sqrt(1 - ELL), 1.0); DS = (D0 * 10 ** -0.02, D0, D0 * 10 ** 0.02)
RMX = (1.0, 1.5, math.inf); STL = ("two-Plummer", "LVD single"); BETA = (-0.5, 0.0, 0.3); RHI = (-1, 0, 1)
TH0 = dict(ups=2.0, c=CG[0], D=D0, rmax=math.inf, stl="two-Plummer", beta=0.0, rhi=0)
def comps_for(stl, c, D):
    if stl == "two-Plummer":
        return [(POPS["MR"]["fraction"], ang(D, POPS["MR"]["Rh_deg"]) * c), (POPS["MP"]["fraction"], ang(D, POPS["MP"]["Rh_deg"]) * c)]
    return [(1.0, ang(D, RH_LVD_ARCMIN / 60.0) * c)]

def run_grid():
    """sigma_pred (km/s) for every footing, model, population and grid point."""
    R = {}
    for pop in ("MR", "MP"):
        p = POPS[pop]
        for c, D, rmx, beta, rhi in itertools.product(CG, DS, RMX, BETA, RHI):
            if not math.isfinite(rmx) and beta != 0.0:              # whole population is exactly beta-free (K1b)
                continue
            a = ang(D, p["Rh_deg"] + rhi * p["Rh_error_deg"]) * c; Rm = ang(D, rmx) * c if math.isfinite(rmx) else math.inf
            kern = kernel(a, beta, Rm, cache=False)
            cmp_s2 = {(f, m): sig2(kern, lambda s, f=f, m=m: g_comp(s, VX[f], MCL[f] if m == "C" else math.inf)) for f in A0 for m in "CX"}
            for stl in STL:
                cps = comps_for(stl, c, D)
                for ups in UPS:
                    Mst = ups * LV(D) * Msun
                    for f in A0:
                        sL = sig2(kern, lambda s: g_law(s, Mst, cps, A0[f]))
                        for m in "LCX":
                            s2 = sL + (cmp_s2[(f, m)] if m != "L" else 0.0)
                            betas = BETA if not math.isfinite(rmx) else (beta,)
                            for bb in betas:
                                R[(f, m, pop, ups, c, D, rmx, stl, bb, rhi)] = math.sqrt(s2) / 1e3
    return R

def keyof(f, m, pop, th): return (f, m, pop, th["ups"], th["c"], th["D"], th["rmax"], th["stl"], th["beta"], th["rhi"])
def classify(R, OBS, f):
    def zs(m, pop, ups, c, D, rmx, stl, bb, rhi):
        o = OBS[pop]; return zstat(o["s"], o["em"], o["ep"], R[(f, m, pop, ups, c, D, rmx, stl, bb, rhi)])
    info = {}
    for m in "LCX":
        allz = {pop: [zs(m, pop, *k) for k in itertools.product(UPS, CG, DS, RMX, STL, BETA, RHI)] for pop in ("MR", "MP")}
        ru = {pop: min(allz[pop]) >= 3 for pop in allz}; ro = {pop: max(allz[pop]) <= -3 for pop in allz}
        match = False; best = None; mm = None                   # mm: closest shared point (reported, added post-freeze)
        for ups, c, D, rmx, stl in itertools.product(UPS, CG, DS, RMX, STL):
            okp, arg = {}, {}
            for pop in ("MR", "MP"):
                cand = [(abs(zs(m, pop, ups, c, D, rmx, stl, bb, rhi)), bb, rhi) for bb, rhi in itertools.product(BETA, RHI)]
                okp[pop], arg[pop] = min(cand)[0], min(cand)[1:]
            pt = dict(ups=ups, c=c, D=D, rmax=rmx, stl=stl, minabsz=okp, beta_rhi=arg)
            if max(okp.values()) < 2 and not match:
                match = True; best = pt
            if mm is None or max(okp.values()) < max(mm["minabsz"].values()): mm = pt
        z0 = {pop: zs(m, pop, *[TH0[k] for k in ("ups", "c", "D", "rmax", "stl", "beta", "rhi")]) for pop in ("MR", "MP")}
        info[m] = dict(z_range={pop: [min(allz[pop]), max(allz[pop])] for pop in allz}, robust_under=ru, robust_over=ro,
                       matches=match, match_point=best, closest_point=mm, z0=z0, fails=any(ru.values()) or any(ro.values()))
    C, X = info["C"], info["X"]
    if C["matches"]: cls = "FINITE CLUMP CONSISTENT"
    elif C["robust_under"]["MP"]:
        if X["matches"]: cls = "SEXTANS NEEDS EXTENDED MASS"
        elif X["fails"]:
            why = [f"{pop} {'under' if X['robust_under'][pop] else 'over'}-predicted by X" for pop in ("MR", "MP") if X["robust_under"][pop] or X["robust_over"][pop]]
            cls = "BOTH FORMS FAIL (" + "; ".join(why) + ")"
        else: cls = "CLUMP SHORT, EXTENDED MARGINAL"
    else:
        cls = "UNDECIDED" + (" (clump over-predicts " + ",".join(p for p in ("MR", "MP") if C["robust_over"][p]) + ")" if any(C["robust_over"].values()) else "")
    return cls, info

def floor2(y1, y2, a1, a2):
    h = a2 / a1; Rr = y2 / y1
    if not (1 < Rr < h ** 3): return dict(possible=False, h=h, R=Rr)
    M = y1 * ((h * h - 1) / (h * h / Rr ** (2 / 3) - 1)) ** 1.5; u = y1 / M
    return dict(possible=True, h=h, R=Rr, M=M, shell_pc=a1 * math.sqrt(u ** (-2 / 3) - 1))

# =====================================================================================================
P("CFG884  Sextans two populations: law (L), law + CFG877 finite clump (C), law + CFG870 extended component (X)" + (f"  [MUTATE {MUT}]" if MUT else ""))
P("  inputs PROVISIONAL (web-tool extraction of Tolstoy+2025 Table 2, copied from the CFG853 packet)")
RES = dict(lane="CFG884", criteria="eb5c21709", mutate=MUT or None)

# ---------------- controls ----------------
if not MUT:
    P("\n  CONTROLS")
    a, Mt = 500.0, 1e6 * Msun
    gpl = lambda s: G * Mt * (s * PC) / (((s * PC) ** 2 + (a * PC) ** 2) ** 1.5)
    ana = lambda X: (math.pi * G * Mt / (32 * a * PC)) * ((1 + X * X) * (1 - (1 + X * X) ** -1.5) / (X * X) if math.isfinite(X) else 1.0)
    k1a = {}
    for X in (0.5, 1.0, 3.0, math.inf):
        num = sig2(kernel(a, 0.0, X * a if math.isfinite(X) else math.inf), gpl); k1a[str(X)] = abs(num / ana(X) - 1)
    ok1a = max(k1a.values()) < 1e-6
    P(f"  K1a analytic Plummer-in-Plummer aperture average, rel. err at X=0.5,1,3,inf: " + ", ".join(f"{v:.1e}" for v in k1a.values()) + f" -> {'PASS' if ok1a else 'FAIL'}")
    # K1b (as frozen): whole-population moment through kernel(.., inf) for each beta, and spread of the three beta at Rmax = 50a
    k1b_inf = {b: abs(sig2(kernel(a, b, math.inf), gpl) / ana(math.inf) - 1) for b in BETA}
    s50 = {b: sig2(kernel(a, b, 50 * a), gpl) for b in BETA}; k1b_50 = max(abs(s50[b] / s50[0.0] - 1) for b in BETA)
    ok1b = max(k1b_inf.values()) < 1e-6 and k1b_50 < 1e-3
    P(f"  K1b beta-independence: Rmax=inf, beta=-0.5/0/+0.3 vs analytic: " + ", ".join(f"{v:.1e}" for v in k1b_inf.values())
      + f"; spread of the three beta at Rmax=50a {k1b_50:.1e} -> {'PASS' if ok1b else 'FAIL'}")
    # K1e (ADDED AFTER FREEZING, reported): independent brute-force nested quad (Jeans integral, Abel projection with
    # r = R cosh u, aperture average) for beta = -0.5 and +0.3 at Rmax = a; tests the finite-aperture beta path of the kernel
    from scipy.integrate import quad
    def brute(beta, Rmax):
        nus = lambda r: r ** (-2 * beta) * quad(lambda x: x ** (2 * beta) * nu_plummer(x, a) * gpl(x), r, np.inf, epsrel=1e-11, epsabs=0, limit=200)[0]
        Ss = lambda R: 2 * quad(lambda u: (1 - beta / math.cosh(u) ** 2) * nus(R * math.cosh(u)) * R * math.cosh(u), 0, 12, epsrel=1e-9, epsabs=0, limit=200)[0]
        num = quad(lambda R: 2 * math.pi * R * Ss(R), 0, Rmax, epsrel=1e-8, epsabs=0, limit=100)[0]
        return num / (Rmax ** 2 / (Rmax ** 2 + a ** 2)) * PC
    k1e = {b: abs(sig2(kernel(a, b, a), gpl) / brute(b, a) - 1) for b in (-0.5, 0.3)}
    P(f"  K1e (added post-freeze, reported) kernel vs brute-force quad at Rmax=a, beta=-0.5/+0.3: " + ", ".join(f"{v:.1e}" for v in k1e.values()))
    # K1c: CFG877 identity
    k1c = {}
    for f in A0:
        dM = abs(MCL[f] / Msun / R877[f]["Mcl_Msun"] - 1)
        Acap = G * MCL[f] / (VX[f] * 1e3) ** 2 / PC; rt = max(x.real for x in np.roots([1, -Acap, 0, -Acap * RC ** 2]) if abs(x.imag) < 1e-9)
        rh = (4 / 3) * float(LVD["rhalf_sph_physical"]) * PC; Ms = 2.0 * 10 ** (0.4 * (4.83 - float(LVD["M_V"])))
        gN = G * (Ms / 2) * Msun / rh ** 2; sl = math.sqrt(float(gN * nu_e(gN / A0[f])) * rh / 3 / 1e6)
        sx = float(g_comp(rh / PC, VX[f], MCL[f])) * rh / 3 / 1e6                 # G M_x(<r12)/(3 r12)
        pred = math.sqrt(sl ** 2 + sx); stored = [r for r in R877[f]["groups"]["large out-of-sample"]["rows"] if r["name"] == "Sextans"][0]["pred"]
        k1c[f] = dict(dMcl=dM, cap_radius_pc=rt, pred=pred, stored=stored, dpred=abs(pred - stored))
        P(f"  K1c [{f}] M_cl {MCL[f]/Msun:.6e} (|rel diff| vs CFG877 {dM:.1e}); cap radius {rt:.1f} pc; Wolf-form Sextans {pred:.12f} vs stored {stored:.12f} (|diff| {abs(pred-stored):.1e})")
    ok1c = all(v["dMcl"] < 1e-9 and v["dpred"] < 1e-9 for v in k1c.values()) and abs(k1c["canonical"]["cap_radius_pc"] - 237) <= 1 and abs(k1c["alt"]["cap_radius_pc"] - 205) <= 1
    P(f"  K1c -> {'PASS' if ok1c else 'FAIL'}")
    # K1d: Wolf form vs Jeans whole population in potential C at theta0 (informational)
    k1d = {}
    cps0 = comps_for("two-Plummer", CG[0], D0); Mst0 = 2.0 * LV(D0) * Msun
    for f in A0:
        for pop in ("MR", "MP"):
            a_ = ang(D0, POPS[pop]["Rh_deg"]) * CG[0]; gC = lambda s: g_law(s, Mst0, cps0, A0[f]) + g_comp(s, VX[f], MCL[f])
            jeans = sig2(kernel(a_, 0.0, math.inf), gC); r12 = 4 / 3 * a_; wolf = float(gC(np.array([r12]))[0]) * r12 * PC / 3
            k1d[f"{f}|{pop}"] = jeans / wolf
    P("  K1d (reported) Jeans/Wolf sigma^2 ratio in potential C at theta0: " + ", ".join(f"{k} {v:.3f}" for k, v in k1d.items()))
    # K3: CFG853 external cross-check (their inputs: M_V -8.72, Ups 2, c = 1, D0, two-Plummer .63/.37)
    ref = {"canonical": (16.45296499734775, 21.02270560988932, 764473991.5905964), "alt": (18.06946562541827, 23.09293681847922, 920637559.9823813)}
    Mst853 = 2.0 * 10 ** (0.4 * (4.83 + 8.72)) * Msun; a853 = [ang(D0, POPS[p]["Rh_deg"]) for p in ("MR", "MP")]
    cps853 = [(0.63, a853[0]), (0.37, a853[1])]; k3 = {}
    for f in A0:
        mom = [sig2(kernel(a_, 0.0, math.inf), lambda s: g_law(s, Mst853, cps853, A0[f])) / 1e6 for a_ in a853]
        ys = [3 * (a_ * PC) * (POPS[p]["sigma_kms"] ** 2 - mm) * 1e6 / G / Msun for a_, p, mm in zip(a853, ("MR", "MP"), mom)]
        fl = floor2(ys[0], ys[1], a853[0], a853[1])
        k3[f] = max(abs(mom[0] / ref[f][0] - 1), abs(mom[1] / ref[f][1] - 1), abs(fl["M"] / ref[f][2] - 1))
        P(f"  K3 [{f}] CFG853 baseline moments {mom[0]:.6f} / {mom[1]:.6f} km^2/s^2 (theirs {ref[f][0]:.6f} / {ref[f][1]:.6f}); floor {fl['M']:.5e} (theirs {ref[f][2]:.5e}); max rel diff {k3[f]:.1e}")
    ok3 = max(k3.values()) < 1e-4
    P(f"  K3 (reported, external) -> {'REPRODUCED' if ok3 else 'NOT REPRODUCED'}")
    RES["controls"] = dict(K1a=k1a, K1a_pass=ok1a, K1b_inf=k1b_inf, K1b_50=k1b_50, K1b_pass=ok1b, K1e=k1e, K1c=k1c, K1c_pass=ok1c, K1d=k1d, K3=k3, K3_reproduced=ok3)
    RES["K_pass"] = ok1a and ok1b and ok1c

# ---------------- main grid ----------------
R = run_grid()
OBS = {pop: dict(s=POPS[pop]["sigma_kms"], em=POPS[pop]["sigma_error_minus_kms"], ep=POPS[pop]["sigma_error_plus_kms"]) for pop in POPS}
ARGS0 = [TH0[k] for k in ("ups", "c", "D", "rmax", "stl", "beta", "rhi")]
CLS = {}
for f in A0:
    obs = {pop: dict(OBS[pop]) for pop in OBS}
    if MUT:
        m_inj = MUT[-1]
        for pop in obs: obs[pop]["s"] = R[(f, m_inj, pop, *ARGS0)]
    a0 = A0[f]
    P(f"\n  [{f}] a0 {a0:.4e}  V_x {VX[f]:.4f} km/s  M_cl {MCL[f]/Msun:.3e} Msun  L_V(84.7 kpc) {LV(D0):.4e}  M_* (Ups 2) {2*LV(D0):.4e} Msun")
    P(f"    observed: MR {obs['MR']['s']:.3f} km/s (a = {ang(D0, POPS['MR']['Rh_deg'])*CG[0]:.1f} pc circ.), MP {obs['MP']['s']:.3f} km/s (a = {ang(D0, POPS['MP']['Rh_deg'])*CG[0]:.1f} pc circ.)")
    cls, info = classify(R, obs, f)
    P("    model  sigma_pred at theta0 (MR / MP)   z0 (MR / MP)       range over grid MR | MP (km/s)       robust under / over / matches")
    rows = {}
    for m in "LCX":
        p0 = {pop: R[(f, m, pop, *ARGS0)] for pop in ("MR", "MP")}
        rng = {pop: [min(v for k, v in R.items() if k[0] == f and k[1] == m and k[2] == pop), max(v for k, v in R.items() if k[0] == f and k[1] == m and k[2] == pop)] for pop in ("MR", "MP")}
        I = info[m]; rows[m] = dict(pred0=p0, range=rng, **I)
        P(f"    {m}      {p0['MR']:6.3f} / {p0['MP']:6.3f}            {I['z0']['MR']:+6.2f} / {I['z0']['MP']:+6.2f}     "
          f"{rng['MR'][0]:5.2f}-{rng['MR'][1]:5.2f} | {rng['MP'][0]:5.2f}-{rng['MP'][1]:5.2f}     "
          f"U {' '.join(p for p in ('MR','MP') if I['robust_under'][p]) or '-'} "
          f"O {' '.join(p for p in ('MR','MP') if I['robust_over'][p]) or '-'} M {'yes' if I['matches'] else 'no'}")
        P(f"           z range over grid: MR [{I['z_range']['MR'][0]:+.2f}, {I['z_range']['MR'][1]:+.2f}]  MP [{I['z_range']['MP'][0]:+.2f}, {I['z_range']['MP'][1]:+.2f}]"
          + (f"   first matching shared point: Ups {I['match_point']['ups']}, c {I['match_point']['c']:.3f}, D {I['match_point']['D']/1e3:.1f}, Rmax {I['match_point']['rmax']}, {I['match_point']['stl']}" if I["matches"] else ""))
        cp = I["closest_point"]
        P(f"           closest shared point (min over grid of the larger |z|): Ups {cp['ups']}, c {cp['c']:.3f}, D {cp['D']/1e3:.1f} kpc, Rmax {cp['rmax']}, {cp['stl']}; "
          + ", ".join(f"{p} |z| {cp['minabsz'][p]:.2f} (beta {cp['beta_rhi'][p][0]:+.1f}, Rh {cp['beta_rhi'][p][1]:+d} err)" for p in ("MR", "MP")))
    # reported: global mixture, EFE variant, required mass
    fr = {pop: POPS[pop]["fraction"] for pop in POPS}
    glob = {m: math.sqrt(sum(fr[p] * rows[m]["pred0"][p] ** 2 for p in fr)) for m in "LCX"}
    P(f"    global mixture sqrt(sum f sigma^2) at theta0: L {glob['L']:.2f}, C {glob['C']:.2f}, X {glob['X']:.2f}; observed mixture "
      f"{math.sqrt(sum(fr[p]*obs[p]['s']**2 for p in fr)):.2f}; measured global {INP['global_sigma_kms']} +- {INP['global_sigma_error_kms']}")
    gext = G * 6.0e10 * Msun / (float(LVD["distance_gc"]) * KPC) ** 2
    cps0 = comps_for("two-Plummer", CG[0], D0); Mst0 = 2.0 * LV(D0) * Msun; efe = {}
    for pop in ("MR", "MP"):
        kern = kernel(ang(D0, POPS[pop]["Rh_deg"]) * CG[0], 0.0, math.inf)
        sL = sig2(kern, lambda s: g_law(s, Mst0, cps0, a0, gext))
        efe[pop] = {m: math.sqrt(sL + (sig2(kern, lambda s, m=m: g_comp(s, VX[f], MCL[f] if m == "C" else math.inf)) if m != "L" else 0)) / 1e3 for m in "LCX"}
    P(f"    EFE variant (reported; g_ext {gext:.2e} = {gext/a0:.2f} a0): MR L/C/X {efe['MR']['L']:.2f}/{efe['MR']['C']:.2f}/{efe['MR']['X']:.2f}, "
      f"MP {efe['MP']['L']:.2f}/{efe['MP']['C']:.2f}/{efe['MP']['X']:.2f} km/s")
    need = {}
    for cg_lab, cg in (("circ", CG[0]), ("major", 1.0)):
        cps = comps_for("two-Plummer", cg, D0); aa = [ang(D0, POPS[p]["Rh_deg"]) * cg for p in ("MR", "MP")]
        for base in ("L", "C"):
            ys = []
            for a_, pop in zip(aa, ("MR", "MP")):
                kern = kernel(a_, 0.0, math.inf); sB = sig2(kern, lambda s: g_law(s, Mst0, cps, a0)) + (sig2(kern, lambda s: g_comp(s, VX[f], MCL[f])) if base == "C" else 0)
                ys.append(3 * a_ * PC * (obs[pop]["s"] ** 2 * 1e6 - sB) / G / Msun)
            fl = floor2(ys[0], ys[1], aa[0], aa[1]) if min(ys) > 0 else dict(possible=False)
            if base == "C":     # (added post-freeze, reported) smallest sigma_MR for which R < h^3, i.e. a finite extra mass can exist
                sMR = obs["MR"]["s"] ** 2 - ys[0] * G * Msun / (3 * aa[0] * PC) / 1e6; sMPres = ys[1] * G * Msun / (3 * aa[1] * PC) / 1e6
                fl["sigma_MR_needed_kms"] = math.sqrt(sMR + sMPres / (aa[1] / aa[0]) ** 2)
            need[f"{cg_lab}|{base}"] = dict(y=ys, **fl)
            P(f"    required extra Newtonian mass on top of {base} ({cg_lab}): single-tracer MR {ys[0]:.3e}, MP {ys[1]:.3e} Msun"
              + (f"; two-tracer floor {fl['M']:.3e} Msun = {fl['M']/(MCL[f]/Msun):.0f} M_cl, shell radius {fl['shell_pc']:.0f} pc (h {fl['h']:.3f}, R {fl['R']:.3f})" if fl.get("possible") else
                 f"; two-tracer floor not defined (R {fl.get('R', float('nan')):.3f}, h^3 {fl.get('h', float('nan'))**3:.3f})")
              + (f"; finite extra mass possible only if sigma_MR >= {fl['sigma_MR_needed_kms']:.2f} km/s" if "sigma_MR_needed_kms" in fl else ""))
    P(f"    -> {cls}")
    CLS[f] = cls
    RES[f] = dict(obs=obs, cls=cls, models=rows, global_mixture=glob, efe=efe, g_ext=gext, required=need,
                  Vx=VX[f], Mcl_Msun=MCL[f] / Msun, LV=LV(D0))

cc, ca = CLS["canonical"], CLS["alt"]; overall = cc if cc == ca else f"{cc} (alt: {ca})"
P(f"\n  CLASS: {overall}")
if MUT == "injectC":
    ok = cc == ca == "FINITE CLUMP CONSISTENT"; RES["mutate_ok"] = ok
    P(f"  MUTATE-injectC (required FINITE CLUMP CONSISTENT on both footings): {'control behaves as required' if ok else 'CONTROL FAILED'}")
if MUT == "injectX":
    ok = all(RES[f]["models"]["X"]["matches"] and not CLS[f].startswith("BOTH FORMS FAIL") for f in A0); RES["mutate_ok"] = ok
    P(f"  MUTATE-injectX (required X matches and not BOTH FORMS FAIL on both footings): {'control behaves as required' if ok else 'CONTROL FAILED'}")
if not MUT: P(f"  K1a/K1b/K1c: {'PASS' if RES['K_pass'] else 'FAIL'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg884_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg884{SUF}.out"), "w").write("\n".join(OUT) + "\n")
