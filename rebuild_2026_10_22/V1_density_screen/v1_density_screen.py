#!/usr/bin/env python3
"""V1_density_screen -- can a well-posed, one-constant, potential-type density screen replace gamma_L / L*?

Screen (FROZEN_CRITERIA.md section 1): v3 with gamma_L -> 0, its P sector multiplied by s(psi) = psi^2, plus a symmetron psi
(potential (mu_psi^2/2)(psi^2-1)^2, matter coupling A = 1 + v^2 psi^2 / 2M^2).  One allowed constant rho_* = mu_psi^2 M^2;
lambda_C = 1/mu_psi and v^2/M^2 must decouple.  Criteria: FROZEN_CRITERIA.md (28ee4db0a8; A1 f21753f370, pre-result).

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 v1_density_screen.py            -> v1_density_screen.out, _results.json
      OMP_NUM_THREADS=1 nice -n 15 python3 v1_density_screen.py --mutate   -> _MUTATE.out, _results_MUTATE.json (validations only)
Deterministic, no network, record files read-only.  kappa = 1/2 FITTED.  Footings never pooled.  Not theory closed.
"""
import os, sys, json, math, time, csv, resource, subprocess, warnings
import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import v1_solvers as V  # noqa: E402

S10, S7, S4 = V.S10, V.S7, V.S4
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
def rel(*p): return os.path.join(REPO, *p)
def rss_gb(who=resource.RUSAGE_SELF):
    return resource.getrusage(who).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)


# ===================================================================================================== child: Part D Q2 solves
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; R_SAT = 9.58 * AU
A0_D7 = {"canonical": 9.36e-11, "alt": 1.13e-10}                 # D7d / E2 footing values
BN11 = (3.8e-26, 1.2e-10, 1.9e-10)
SQ = (1.0, 0.3, 0.15)
G1, G15 = (30, 48), (45, 72)                                      # AMENDMENT A1
def rM_of(a0): return math.sqrt(GM_SUN / a0)
def toQ(raw, a0): return -raw * a0 / rM_of(a0)                     # Phi convention -> BN11/Hees convention (D7d)
def rich15(q1, q15): return (2.25 * q15 - q1) / 1.25

if "--child-q2" in sys.argv:
    # AMENDMENT A2: one child per job ("BN11" or "<footing>|<field>") so that every child stays < 1 GB RSS
    outp = sys.argv[sys.argv.index("--child-q2") + 1]; job = sys.argv[sys.argv.index("--job") + 1]
    d7b = json.load(open(rel("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")))
    EV = {f: {E: v["ge_total"] for E, v in d7b["grid"][f]["none"].items()} for f in A0_D7}
    res = {"BN11": {}, "Q": {}, "worst_res": 0.0, "nscored_fail": 0}
    def run(xe, s, a0, rq, gres, U0=None):
        g = S7.Grid(1e-5, 1e4, gres[0], gres[1])
        U, fin, it = V.solve_q2_S(g, xe, s, mutate=MUT, U0=U0)
        res["worst_res"] = max(res["worst_res"], fin)
        if fin >= 1e-9: res["nscored_fail"] += 1
        return toQ(S7.q2_raw(g, U[0], rq), a0), U.ravel(), fin
    if job == "BN11":
        a0b = BN11[1]; xb = BN11[2] / a0b; rqb = R_SAT / rM_of(a0b)
        for s in (1.0, 0.0):
            q1, _, f1 = run(xb, s, a0b, rqb, G1); q15, _, f15 = run(xb, s, a0b, rqb, G15)
            res["BN11"][str(s)] = dict(G1=q1, G15=q15, R=rich15(q1, q15), res=[f1, f15])
    else:
        f, E = job.split("|"); a0 = A0_D7[f]; rq = R_SAT / rM_of(a0); ge = EV[f][E]
        xe = ge / a0; row = {}
        U1 = None
        for s in SQ:                                              # G1 ladder with continuation
            q1, U1, f1 = run(xe, s, a0, rq, G1, U0=U1); row[str(s)] = dict(G1=q1, res=[f1])
        U1 = None
        for s in SQ:                                              # G1.5 ladder with continuation
            q15, U1, f15 = run(xe, s, a0, rq, G15, U0=U1)
            row[str(s)].update(G15=q15, R=rich15(row[str(s)]["G1"], q15)); row[str(s)]["res"].append(f15)
        res["Q"][f"{f}|{E}"] = dict(x_e=xe, ge=ge, rows=row)
    res["rss_gb"] = rss_gb()
    json.dump(res, open(outp, "w"), indent=1)
    sys.exit(0)


# ===================================================================================================== bookkeeping
OUT, CHK = [], {}
R = dict(lane="V1_density_screen", frozen="28ee4db0a8", amendment_A1="f21753f370", amendment_A2="b7fb82fd8d", mutate=MUT)
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def check(cid, ok, val, thr, label):
    CHK[cid] = dict(ok=bool(ok), value=str(val), threshold=str(thr), label=label)
    P(f"{cid} {'PASS' if ok else 'FAIL'} {val} {thr} :: {label}")
T0 = time.time()
P("=" * 110)
P("V1_density_screen -- one-constant symmetron-type density screen in place of gamma_L / L*"
  + ("   *** MUTATE: s multiplies source and phantom (wrong insertion point) ***" if MUT else ""))
P("=" * 110)

# constants (record values; labelled)
G, MSUN, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16      # D10 / S1
G_H4 = 6.6743e-11                                                   # H4
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                   # D10 / S1 / P4 record values
FOOTS = ("canonical", "alt")
R_SUN = 6.957e8                                                     # IAU nominal (m)
PHI_STAR = GM_SUN / R_SUN                                           # Sun's surface potential (m^2/s^2), reference star
A_H = 3.0 * KPC
LN10 = math.log(10.0)
SEC_GYR = 3.15576e16

# ===================================================================================================== PART A (sympy)
import sympy as sy
P("\n[Part A] sympy: the screen's equations")
g_, K_, a0_, s_, u_, x_ = sy.symbols("g K a0 s u x", positive=True)
Wp = u_ * a0_ / (K_ * (a0_ - u_))                                   # W'(u) (H4 / C5)
usol = sy.solve(sy.Eq(g_, K_ * Wp), u_)[0]                          # P equation (s cancels)
muS = 1 - s_ * usol / g_                                            # flux (grad phi/K - s P) = mu_S grad phi / K
a1 = sy.simplify(muS - (1 - s_ / (1 + g_ / a0_)))
a1b = sy.simplify(muS.subs(s_, 1) - (g_ / a0_) / (1 + g_ / a0_))
a1c = sy.simplify(muS.subs(s_, 0) - 1)
up = sy.symbols("up", positive=True)
Wint = sy.integrate(Wp.subs(u_, up), (up, 0, u_))
LP0 = sy.simplify((usol / K_) * g_ - Wint.subs(u_, usol))
a1d = sy.simplify(LP0.subs(g_, x_ * a0_) - (a0_ ** 2 / K_) * (x_ - sy.log(1 + x_)))
check("A1", a1 == 0 and a1b == 0 and a1c == 0 and a1d == 0, f"{a1}/{a1b}/{a1c}/{a1d}", "all 0",
      "uniform s: mu_S = 1 - s/(1+x); s=1 -> x/(1+x); s=0 -> 1; on-shell P-sector L_P0 = (a0^2/K)(x - ln(1+x))")
psi, mu_p, v_, Msym, rho_, c_, LP_, rs_ = sy.symbols("psi mu_psi v M rho c L_P rho_s", positive=True)
zz = sy.symbols("zz")
pf = sy.Function("p")(zz)
Lpsi = (-(v_ ** 2 / 2) * (sy.diff(pf, zz) ** 2 + (mu_p ** 2 / 2) * (pf ** 2 - 1) ** 2) - rho_ * c_ ** 2 * v_ ** 2 * pf ** 2 / (2 * Msym ** 2)
        + pf ** 2 * LP_)
from sympy.calculus.euler import euler_equations
el = euler_equations(Lpsi, [pf], [zz])[0]
rhs_target = sy.diff(pf, zz, 2) - (mu_p ** 2 * pf * (pf ** 2 - 1) + rho_ * c_ ** 2 * pf / Msym ** 2 - 2 * pf * LP_ / v_ ** 2)
a2 = sy.simplify(el.lhs / v_ ** 2 - rhs_target)
a2v = sy.simplify(sy.diff((el.lhs / v_ ** 2).subs(LP_, 0), v_))
rho_star = mu_p ** 2 * Msym ** 2 / c_ ** 2
p2_ = sy.symbols("p2")
ps2 = sy.solve(sy.Eq(mu_p ** 2 * (p2_ - 1) + rho_ * c_ ** 2 / Msym ** 2, 0), p2_)
a2u = sy.simplify(ps2[0] - (1 - rho_ / rho_star)) if ps2 else "none"
check("A2", a2 == 0 and a2v == 0 and a2u == 0, f"{a2}/{a2v}/{a2u}", "all 0",
      "psi EL / v^2 = lap psi - mu^2 psi(psi^2-1) - (rho c^2/M^2) psi + (2/v^2) psi L_P0; v-free at L_P0 = 0; uniform psi^2 = 1 - rho/rho_*")
pa_, r_, R_ = sy.symbols("psi_a r R", positive=True)
a3a = sy.factor(-psi * (psi ** 2 - pa_ ** 2))                     # -lap psi / m^2 outside, for 0 <= psi <= psi_a: >= 0
a3b = sy.simplify((1 - (pa_ * (1 - R_ / r_)) ** 2 / pa_ ** 2) - (2 * R_ / r_ - R_ ** 2 / r_ ** 2))
check("A3", sy.simplify(a3a - psi * (pa_ - psi) * (pa_ + psi)) == 0 and a3b == 0, f"{a3a}; {a3b}", "psi(psi_a-psi)(psi_a+psi) >= 0; 0",
      "exterior u = psi_a - psi subharmonic -> u <= u(R) R/r; then 1 - s/s_a <= 2R/r - R^2/r^2 <= 2R/r")
# A4: the coupled dispersion
t_, z_ = sy.symbols("t z", real=True)
Kd, Md, Sd, muK, rt_, cm, vv, m2, k_, w_ = sy.symbols("K M S mu_K rho_tau c v m2 k omega", real=True)
ph = sy.Function("phi")(t_, z_); sg = sy.Function("sigma")(t_, z_); pq = sy.Function("q")(t_, z_)
dXi = sy.diff(ph, z_) - sy.diff(sg, t_, z_)
L2 = (-sy.diff(ph, z_) ** 2 / (2 * Kd) + Sd / (2 * Kd * Md) * dXi ** 2 + muK ** 2 / (2 * Kd) * (ph - sy.diff(sg, t_)) ** 2
      - rt_ / 2 * sy.diff(sg, z_) ** 2 + cm * pq * dXi + vv ** 2 / 2 * (sy.diff(pq, t_) ** 2 - sy.diff(pq, z_) ** 2 - m2 * pq ** 2))
eqs = euler_equations(L2, [ph, sg, pq], [t_, z_])
Am = sy.symbols("A0:3"); Ex = sy.exp(sy.I * (k_ * z_ - w_ * t_))
sub = {ph: Am[0] * Ex, sg: Am[1] * Ex, pq: Am[2] * Ex}
rows = []
for e in eqs:
    ex = sy.expand(sy.simplify((e.lhs - e.rhs).subs(sub).doit() / Ex))
    rows.append([ex.coeff(a) for a in Am])
DET = sy.factor(sy.simplify(sy.Matrix(rows).det()))
DET0 = sy.factor(sy.simplify(sy.Matrix(rows).subs(cm, 0).det()))
Xs = sy.symbols("X")
khron = sy.factor(DET0 / (vv ** 2 * (w_ ** 2 - k_ ** 2 - m2)))
kh_roots = sy.solve(khron.subs(w_, sy.sqrt(Xs)), Xs)
chiS = Sd * k_ ** 2 / (Kd * Md) + muK ** 2 / Kd
a4a = [sy.simplify(r - rt_ * (k_ ** 2 / chiS - Kd)) for r in kh_roots]
a4b = sy.simplify(kh_roots[0].subs({Sd: 1}) - rt_ * (k_ ** 2 / (k_ ** 2 / (Kd * Md) + muK ** 2 / Kd) - Kd)) if kh_roots else "none"
a4c = sy.limit(kh_roots[0], k_, sy.oo) if kh_roots else "none"
a4c_ok = sy.simplify(a4c - Kd * rt_ * (Md - Sd) / Sd) == 0
check("A4", a4a == [0] and a4b == 0 and a4c_ok, f"{a4a}; {a4b}; lim k->oo omega^2 = {a4c}", "[0]; 0; K rho_tau (M - S)/S (finite)",
      "c=0: omega^2 = rho_tau (k^2/chi_S - K), chi_S = S k^2/(K M) + mu_K^2/K; S=1 is H4's gamma_L=0 relation; UV limit finite for S>0")
R["A4_det"] = str(DET)
POLY = sy.Poly(sy.expand(-DET * Kd ** 2 * Md / k_ ** 2).subs(w_ ** 2, Xs), Xs)
COEF = [sy.lambdify((Kd, Md, Sd, muK, rt_, cm, vv, m2, k_), cc, "math") for cc in POLY.all_coeffs()]
P(f"   coupled det (c != 0) is a polynomial of degree {POLY.degree()} in omega^2")

# ===================================================================================================== PART B1/B2 (own symmetron BVP)
P("\n[Part B] the screen's regimes: own 1D symmetron BVP (lengths in the body radius R = 1; m = R/lambda_C = 0.01)")
mB = 0.01
B12 = {}; b1w = -1e9; b2q = None
for sa in (0.3, 0.9):
    for tsp in (0.1, 10.0, 1e3):
        db = tsp / mB ** 2
        rc, ps_, pa, info = V.symmetron_radial(mB, db, 1.0 - sa)
        out = rc >= 1.0
        u = pa - ps_
        ratio = float(np.max(u[out] * rc[out] / pa))                # must be <= 1 (u <= psi_a R / r)
        b1w = max(b1w, float(np.max(u[out] - pa / rc[out])))
        i30 = int(np.argmin(abs(rc - 30.0))); ma = info["ma"]
        ulin = mB ** 2 * pa * (db - (1.0 - sa)) / 3.0 * V.form_factor(ma) * math.exp(-ma * rc[i30]) / rc[i30]
        q = float(u[i30] / ulin)
        B12[f"s_a={sa}|rhoR2/M2={tsp:g}"] = dict(max_u_r_over_psia_R=ratio, q_charge=q, iters=info["iters"], res=info["res"],
                                                  psiR_over_psia=float(np.interp(1.0, rc, ps_) / pa))
        if tsp >= 100: b2q = q if b2q is None else max(b2q, q)
        P(f"   s_a {sa}, rho R^2/M^2 {tsp:7g}: max r u/(psi_a R) {ratio:.6f}; charge fraction q {q:.4f}; psi(R)/psi_a {B12[f's_a={sa}|rhoR2/M2={tsp:g}']['psiR_over_psia']:.4f} (res {info['res']:.1e})")
R["B12"] = B12
check("B1", b1w <= 1e-6, f"max(u - psi_a R/r) = {b1w:.2e}", "<= 1e-6", "exterior bound u(r) <= psi_a R/r (linear and thin-shell bodies)")
check("B2", b2q is not None and b2q < 0.1, f"q = {b2q:.4f} at rho R^2/M^2 = 1e3", "< 0.1", "thin-shell body's exterior psi-charge is a small fraction of its mass")

# ===================================================================================================== PART C (globular fit)
P("\n[Part C] the one-constant fit to the outer globulars: D10's data, likelihood tables and statistic; parameter S_GC")
D10 = json.load(open(rel("doors_push_2026_10_22", "D10_native_Lstar", "d10_native_lstar_results.json")))
CFG332 = json.load(open(rel("campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))
UMF = CFG332["route2"]["ups_mf"]
CLU = D10["clusters"]; NAMES = list(CLU.keys()); PRIMARY = ["NGC 2419", "Pal 4", "Pal 14"]
UPSG = np.array(D10["Ups_grid"]); SIGI = np.array(D10["sigma_int_grid"])
LIK = {k: np.array(v) for k, v in D10["lik_tables"].items()}
EBR = D10["MW_Mb"]
SG = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
GR = S10.Grid2D(nper=24, Nt=16)

def g_mw(R_kpc, Mb, a0, s=1.0, mutate=False):
    gN = G * Mb * MSUN / (R_kpc * KPC + A_H) ** 2
    return float(V.g_law(gN / a0, s, mutate)) * a0

LU = np.linspace(math.log(UPSG[0]), math.log(UPSG[-1]), 600)
def prior_of(pk, name):
    if pk == "P1": return 1.6, 0.15
    br = "K" if pk == "P2" else "S"; return UMF[br][name][0], UMF[br][name][1]
def lnL(sig, name, pk, f=0.3):
    lsig = np.interp(LU, np.log(UPSG), np.log(sig))
    lp = np.interp(lsig, np.log(SIGI), LIK[f"{name}|{f}"], left=-690.0, right=-690.0)
    c, w = prior_of(pk, name); z = (LU / LN10 - math.log10(c)) / w; pr = np.exp(-0.5 * z * z); pr /= TRAPZ(pr, LU)
    mx = lp.max(); return mx + math.log(max(TRAPZ(pr * np.exp(lp - mx), LU), 1e-300))

SIG = {}          # (foot, ek, name, treat) -> array (len(SG), 15) of sigma_p (km/s)
c1_worst = 0.0; nsolve = 0; worst_res = 0.0
c1_nodes = 0
if MUT:
    plan = [("canonical", "E_mid", "Pal 4")]
else:
    plan = [(f, ek, n) for f in FOOTS for ek in ("E_lo", "E_mid", "E_hi") for n in NAMES]
for (f, ek, n) in plan:
    a0 = A0[f]; cl = CLU[n]; a = cl["rhl"] * PC; Rbin = cl["Rbin"]; unit = math.sqrt(a0 * a) / 1e3; Mb = EBR[f][ek]
    ref = np.array(D10["sigma_tables"][f"{f}|{ek}|{n}"])           # (3 est, 15 Ups, 26 cols)
    treats = ("FD10",) if (n == "Pal 3" or MUT) else ("FD10", "FS")
    for tr in treats:
        arr = np.full((len(SG), len(UPSG)), np.nan)
        for iu, ups in enumerate(UPSG):
            y = G * ups * cl["LV"] * MSUN / (a * a * a0)
            U = None
            for js in range(len(SG) - 1, -1, -1):
                s = SG[js]
                if tr == "FS" and s == 1.0:
                    continue
                xe = g_mw(cl["RGC"], Mb, a0, 1.0) / a0 if tr == "FD10" else g_mw(cl["RGC"], Mb, a0, s) / a0
                s2, vir, wo, U, res = V.gc_sigma(GR, y, xe, s, Rbin, mutate=MUT, U0=U)
                nsolve += 1; worst_res = max(worst_res, res)
                arr[js, iu] = math.sqrt(max(s2, 0.0)) * unit
                if tr == "FD10" and s in (1.0, 0.0):
                    col = 0 if s == 1.0 else -1
                    c1_worst = max(c1_worst, abs(arr[js, iu] / ref[0, iu, col] - 1)); c1_nodes += 1
        if tr == "FS":
            arr[-1] = SIG[(f, ek, n, "FD10")][-1]
        SIG[(f, ek, n, tr)] = arr
    if not MUT and ek == "E_hi" and n == NAMES[-1]:
        P(f"   [{f}] solved ({nsolve} solves, worst scaled residual {worst_res:.1e}, {time.time() - T0:.0f} s)")
check("C1", c1_worst <= 1e-6, f"{c1_worst:.2e} over {c1_nodes} nodes", "<= 1e-6",
      "S=1 reproduces D10's AQUAL sigma_p and S=0 its Newton sigma_p (E-P), every node used")
R["C_solves"] = nsolve; R["C_worst_residual"] = worst_res

def chi2_curve(f, pk, ek, tr, names):
    return np.array([-2 * sum(lnL(SIG[(f, ek, n, tr if n != "Pal 3" else "FD10")][js], n, pk) for n in names) for js in range(len(SG))])
def S95_of(c):
    d = c - c.min()
    if d[-1] <= 3.84: return 1.0, d
    for js in range(len(SG) - 1, 0, -1):
        if d[js - 1] <= 3.84 < d[js]:
            x1, x2 = SG[js - 1], SG[js]; y1, y2 = d[js - 1] - 3.84, d[js] - 3.84
            return float(x1 + (x2 - x1) * (-y1) / (y2 - y1)), d
    return 0.0, d

S95 = {}; CELLS = {}
if not MUT:
    c2w = 0.0
    for f in FOOTS:
        for pk in ("P1", "P2", "P3"):
            for ek in ("E_lo", "E_mid", "E_hi"):
                bc = D10["band_cells"][f"{f}|{pk}|{ek}"]
                cA = chi2_curve(f, pk, ek, "FD10", PRIMARY)
                c2w = max(c2w, abs((cA[-1] - bc["chi2_min"]) - bc["dchi2_AQUAL"]), abs((cA[0] - bc["chi2_min"]) - bc["dchi2_Newton"]))
                for tr in ("FD10", "FS"):
                    c = cA if tr == "FD10" else chi2_curve(f, pk, ek, "FS", PRIMARY)
                    s95, d = S95_of(c)
                    S95[f"{f}|{pk}|{ek}|{tr}"] = s95
                    CELLS[f"{f}|{pk}|{ek}|{tr}"] = dict(S=SG, dchi2=d.tolist(), S95=s95, argmin_S=SG[int(np.argmin(c))],
                                                        dchi2_S1=float(d[-1]), dchi2_S0=float(d[0]))
                P(f"   [{f:9s} {pk} {ek:5s}] S_95 = {S95[f'{f}|{pk}|{ek}|FD10']:.3f} (F-D10) / {S95[f'{f}|{pk}|{ek}|FS']:.3f} (F-S); "
                  f"dchi2 at S=1 {CELLS[f'{f}|{pk}|{ek}|FD10']['dchi2_S1']:.2f}, at S=0 {CELLS[f'{f}|{pk}|{ek}|FD10']['dchi2_S0']:.2f}; "
                  f"min at S = {CELLS[f'{f}|{pk}|{ek}|FD10']['argmin_S']}")
    check("C2", c2w <= 0.01, f"{c2w:.2e}", "<= 0.01", "S=1 / S=0 chi2 columns reproduce D10's band-cell dchi2_AQUAL / dchi2_Newton (18 cells)")
    for f in FOOTS:
        cen = CELLS[f"{f}|P1|E_mid|FS"]
        per = {n: (np.array([-2 * lnL(SIG[(f, "E_mid", n, "FS" if n != "Pal 3" else "FD10")][js], n, "P1") for js in range(len(SG))])) for n in NAMES}
        for n in NAMES:
            v = per[n] - per[n].min()
            P(f"      {f:9s} {n:9s} dchi2(S): " + " ".join(f"{SG[j]:.2f}:{v[j]:.2f}" for j in (0, 3, 6, 9, 11)))
        c4 = chi2_curve(f, "P1", "E_mid", "FD10", NAMES); s4, _ = S95_of(c4)
        R[f"C_all_four|{f}"] = s4
        P(f"   [{f}] all four clusters (F-D10, P1, E_mid): S_95 = {s4:.3f}")
    R["C_cells"] = CELLS; R["S95"] = S95
    S95C = {f: S95[f"{f}|P1|E_mid|FS"] for f in FOOTS}                 # central, regime-B-consistent field
    S95MAX = {f: max(v for k, v in S95.items() if k.startswith(f + "|")) for f in FOOTS}
    R["S95_central_FS"] = S95C; R["S95_max_over_cells"] = S95MAX
    P(f"   S_95 central (P1, E_mid, F-S): canonical {S95C['canonical']:.3f}, alt {S95C['alt']:.3f}; max over the 36 cells "
      f"{S95MAX['canonical']:.3f} / {S95MAX['alt']:.3f}")

# ===================================================================================================== PART D (Cassini, planets)
P("\n[Part D] (a) Cassini Q2 and planets (D7d Route N at L* = 0 with the phantom rows x s; child process)")
JOBS = ["BN11"] + ([] if MUT else [f"{f}|{E}" for f in FOOTS for E in ("E0", "E1", "E2", "E3")])
QJ = {"BN11": {}, "Q": {}, "worst_res": 0.0, "nscored_fail": 0, "rss_gb": 0.0, "rss_by_job": {}}
for job in JOBS:
    qpath = os.path.join(HERE, f"_v1_q2_child{TAG}.json")
    cmd = [sys.executable, os.path.abspath(__file__), "--child-q2", qpath, "--job", job] + (["--mutate"] if MUT else [])
    subprocess.run(cmd, check=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    cj = json.load(open(qpath)); os.remove(qpath)
    QJ["BN11"].update(cj["BN11"]); QJ["Q"].update(cj["Q"]); QJ["worst_res"] = max(QJ["worst_res"], cj["worst_res"])
    QJ["nscored_fail"] += cj["nscored_fail"]; QJ["rss_gb"] = max(QJ["rss_gb"], cj["rss_gb"]); QJ["rss_by_job"][job] = cj["rss_gb"]
P(f"   {len(JOBS)} child processes; peak child RSS {QJ['rss_gb']:.3f} GB")
d7d = json.load(open(rel("doors_push_2026_10_22", "D7d_screened_q2", "d7d_screened_q2_results.json")))
K4R = d7d["K4_AQUAL_BN11"]["R"]
qb1 = QJ["BN11"]["1.0"]["R"]; qb0 = max(abs(QJ["BN11"]["0.0"]["G1"]), abs(QJ["BN11"]["0.0"]["G15"]))
check("D1", abs(qb1 / K4R - 1) <= 1e-3 and qb0 < 1e-40, f"Q2(S=1) {qb1:.6e} vs {K4R:.6e} (rel {abs(qb1 / K4R - 1):.1e}); |Q2(S=0)| {qb0:.1e}",
      "<= 1e-3; 0", "BN11 AQUAL anchor reproduced (G1/G1.5 Richardson); S=0 gives no anomalous quadrupole")
R["D_child_rss_gb"] = QJ["rss_gb"]; R["D_worst_res"] = QJ["worst_res"]
HEES_HI, HEES_LO, PARK_HI, PARK_LO = 9e-27, -3e-27, 5.2e-27, -2.0e-27
SC = {}; SPARK = {}; SPL = {}
if not MUT:
    e2 = json.load(open(rel("doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")))
    d2w = 0.0; mono = True; scored_ok = QJ["nscored_fail"] == 0
    for f in FOOTS:
        sc_list, sp_list = [], []
        for E in ("E0", "E1", "E2", "E3"):
            rows = QJ["Q"][f"{f}|{E}"]["rows"]
            q = {float(k): v["R"] for k, v in rows.items()}
            ref = e2["R1"][f"{f}|none"]["cells"][E]["Q2_AQUAL"]
            d2w = max(d2w, abs(q[1.0] / ref - 1))
            mono &= (q[0.15] < q[0.3] < q[1.0])
            xs = [0.0, 0.15, 0.3, 1.0]; ys = [0.0, q[0.15], q[0.3], q[1.0]]
            def cross(line):
                if ys[-1] <= line: return 1.0
                for i in range(1, 4):
                    if ys[i] > line:
                        return xs[i - 1] + (xs[i] - xs[i - 1]) * (line - ys[i - 1]) / (ys[i] - ys[i - 1])
            sc_list.append(cross(HEES_HI)); sp_list.append(cross(PARK_HI))
            P(f"   {f:9s} {E}: x_e {QJ['Q'][f'{f}|{E}']['x_e']:.3f}  Q2(S=1) {q[1.0]:.3e} (E2 {ref:.3e})  Q2(0.3) {q[0.3]:.3e}  Q2(0.15) {q[0.15]:.3e}  "
              f"Q2(0.3)/0.3Q2(1) {q[0.3] / (0.3 * q[1.0]):.3f}")
        SC[f] = min(sc_list); SPARK[f] = min(sp_list)
        P(f"   [{f}] S_C (Hees 2 sigma, all four fields) = {SC[f]:.4f};  Park = {SPARK[f]:.4f}")
    check("D2", d2w <= 0.03, f"{d2w:.2e}", "<= 3e-2", "S=1 Q2 at E0-E3 agrees with E2's R1 AQUAL values (both footings)")
    R["D_Q"] = QJ["Q"]; R["S_C"] = SC; R["S_Park"] = SPARK; R["D_monotone"] = bool(mono); R["D_all_scored"] = bool(scored_ok)
    P(f"   Q2 monotone in S at every field: {mono}; all points scored (residual < 1e-9): {scored_ok} (worst {QJ['worst_res']:.1e}); child RSS {QJ['rss_gb']:.3f} GB")
    from scipy.optimize import brentq
    PLANETS = {"Earth": (1.0 * AU, 8.7e-15), "Mars": (1.524 * AU, 1.4e-15), "Saturn": (9.58 * AU, 7.0e-15)}
    for f in FOOTS:
        a0 = A0_D7[f]; lst = {}
        for pn, (r, bnd) in PLANETS.items():
            y = GM_SUN / r ** 2 / a0
            an = lambda s: (float(V.g_from_gN_S(y, s)) - y) * a0
            lst[pn] = dict(a_S1=an(1.0), bound=bnd, ratio_S1=an(1.0) / bnd, S_max=brentq(lambda s: an(s) - bnd, 0.0, 1.0, xtol=1e-14))
        SPL[f] = min(v["S_max"] for v in lst.values()); R[f"D_planets|{f}"] = lst
        P(f"   [{f}] planets at S=1: " + ", ".join(f"{k} {v['ratio_S1']:.2e}x bound" for k, v in lst.items()) + f";  S_pl = {SPL[f]:.3e}")
    R["S_pl"] = SPL

# ===================================================================================================== PART B3/B4 (regime map)
REG = {}
if not MUT:
    P("\n[Part B3/B4] regimes: A (stars linear: rho_* lambda_C^2 >= M_sun/(4 pi R_sun)) and B (stars thin-shell)")
    p4w = {}
    # MW baryons (McMillan17, P4's T4 model) Newtonian potential at R0
    R0_MW = 8.122
    PC2, PC3 = 1e6, 1e9
    S0_THIN, RD_THIN, ZD_THIN = 896.0 * PC2, 2.50, 0.300                 # McMillan 2017 Table 3 (as P4 / CFG514)
    S0_THICK, RD_THICK, ZD_THICK = 183.0 * PC2, 3.02, 0.900
    RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = 98.4 * PC3, 1.8, 0.075, 2.1, 0.5
    R_FID = 8.33
    S0_HI = 10.0 * PC2 / math.exp(-4.0 / R_FID - R_FID / 7.0)
    S0_H2 = 2.0 * PC2 / math.exp(-12.0 / R_FID - R_FID / 1.5)
    def rho_mcm(Rr, zr):
        zr = np.abs(zr)
        thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-zr / ZD_THIN - Rr / RD_THIN)
        thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-zr / ZD_THICK - Rr / RD_THICK)
        rp = np.maximum(np.sqrt(Rr * Rr + (zr / Q_B) ** 2), 1e-7)
        bulge = RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)
        Rs = np.maximum(Rr, 1e-6)
        hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zr / (2 * 0.085), 300)) ** 2
        h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zr / (2 * 0.045), 300)) ** 2
        return thin + thick + bulge + hi + h2
    MWG = {}
    for f in FOOTS:
        a0 = A0[f]; Mu = S4.mass_unit(a0); Mt0 = 6.6e10 / Mu
        re_ = S4.log_edges(0.005, 300.0 * max(60.0, math.sqrt(Mt0)), 30)
        gmw = S4.Grid(re_, S4.theta_edges(48, full=False, stretch_min=0.002))
        rho1 = gmw.rho_axisym(lambda Rr, zr: rho_mcm(Rr, zr) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * gmw.vol))
        MWG[f] = (gmw, rho1, Mt, Mu)
        prN = V.ProblemS(gmw, rho1, Mt, 0.0, sfun=0.0); PhiN = prN.solve_newton()
        phi0 = float(gmw.interp_cells(PhiN, np.array([R0_MW]), np.array([0.0]))[0]) * a0 * S4.KPC
        p4w[f] = abs(phi0)
    PHI_SUN_AV = {"McMillan17": p4w["canonical"]}
    for ek in ("E_lo", "E_mid", "E_hi"):
        PHI_SUN_AV[f"Hernquist {ek} (can/alt)"] = max(G * EBR[f][ek] * MSUN / (R0_MW * KPC + A_H) for f in FOOTS)
    best = max(PHI_SUN_AV.values())
    sA = {f: (1.0 - min(1.0, best / PHI_STAR)) ** 2 for f in FOOTS}
    for f in FOOTS:
        st = min(SC[f], SPL[f]); req = (1.0 - math.sqrt(st)) * PHI_STAR
        REG[f"Sun|{f}"] = dict(available=PHI_SUN_AV, required=req, shortfall=req / best, s_Sun_min_A=sA[f], s_target=st)
        P(f"   Sun [{f}]: |Phi_N,bar,MW(R0)| up to {best:.3e} m^2/s^2 ({math.sqrt(best) / 1e3:.0f} km/s)^2 vs required "
          f"(1 - sqrt(s_t)) GM/R_sun = {req:.3e} ({math.sqrt(req) / 1e3:.0f} km/s)^2 -> shortfall x{req / best:.2f}; "
          f"Regime A leaves s_Sun >= {sA[f]:.3f}")
    R["PHI_SUN_available"] = PHI_SUN_AV
    gcA = {}
    for f in FOOTS:
        for n in PRIMARY:
            cl = CLU[n]; a = cl["rhl"] * PC
            av = max(G * ups * cl["LV"] * MSUN / a + G * EBR[f][ek] * MSUN / (cl["RGC"] * KPC + A_H)
                     for ups in (1.6, 1.6 * 10 ** 0.3) for ek in ("E_lo", "E_mid", "E_hi"))
            for lab, s95 in (("central", S95C[f]), ("max", S95MAX[f])):
                req = (1.0 - math.sqrt(s95)) * PHI_STAR
                gcA[f"{f}|{n}|{lab}"] = dict(available=av, required=req, shortfall=req / av if req > 0 else 0.0)
            Nst = 1.6 * 10 ** 0.3 * cl["LV"] / 0.5
            a_pc = cl["rhl"]; Rs_pc = R_SUN / PC
            reqB = (1.0 - math.sqrt(S95MAX[f])) * a_pc / (Nst * Rs_pc)
            gcA[f"{f}|{n}|B4"] = dict(N_star=Nst, shortfall=reqB)
            P(f"   {n:9s} [{f}] Regime A: |Phi_N,c| <= {av:.3e} m^2/s^2 vs required {gcA[f'{f}|{n}|max']['required']:.3e} (S_95 max) -> "
              f"shortfall x{gcA[f'{f}|{n}|max']['shortfall']:.3g} (central x{gcA[f'{f}|{n}|central']['shortfall']:.3g}); "
              f"Regime B self-screening (capacitance): N* R_sun / a short by x{reqB:.3g}")
    REG["GC"] = gcA
    # frozen fit line (AMENDMENT A2 fixes run 1, which used the 36-cell maximum): every P1 E_mid cell, both treatments
    for f in FOOTS:
        for n in PRIMARY:
            for tr in ("FD10", "FS"):
                s95 = S95[f"{f}|P1|E_mid|{tr}"]; req = (1.0 - math.sqrt(s95)) * PHI_STAR
                gcA[f"{f}|{n}|P1Emid|{tr}"] = dict(S95=s95, required=req, shortfall=req / gcA[f"{f}|{n}|central"]["available"])
    fitA = all(gcA[f"{f}|{n}|P1Emid|{tr}"]["shortfall"] <= 1.0 for f in FOOTS for n in PRIMARY for tr in ("FD10", "FS"))
    REG["fitA_P1Emid_min_shortfall"] = min(gcA[f"{f}|{n}|P1Emid|{tr}"]["shortfall"] for f in FOOTS for n in PRIMARY for tr in ("FD10", "FS"))
    REG["fitA_36cell_max_sensitivity"] = all(gcA[f"{f}|{n}|max"]["shortfall"] <= 1.0 for f in FOOTS for n in PRIMARY)
    fitB_self = all(gcA[f"{f}|{n}|B4"]["shortfall"] <= 1.0 for f in FOOTS for n in PRIMARY)
    REG["fit_exists_A"] = fitA; REG["fit_B_self_screening"] = fitB_self
    REG["fit_exists_B"] = True; REG["fit_B_condition"] = "only via the halo's diffuse gas (P-mono): rho_* <= rho_gas(R_GC) / (1 - S_95)"
    P(f"   fit exists in Regime A (frozen: P1 E_mid cells, both treatments): {fitA} (smallest shortfall x{REG['fitA_P1Emid_min_shortfall']:.2f}); "
      f"with the 36-cell maximum S_95 (sensitivity): {REG['fitA_36cell_max_sensitivity']}; Regime B by GC self-screening: {fitB_self}; "
      "Regime B via ambient halo gas: conditional (rho_* <= rho_gas(R_GC) / (1 - S_95))")
    R["REG"] = REG

# ===================================================================================================== PART E (satellites)
P("\n[Part E] (b) dwarfs: S1's satellites with the screen (D10 solver, s uniform at each system)")
rowsS1 = list(csv.DictReader(open(rel("rebuild_2026_10_22", "S1_v3_hosted_small", "s1_per_system.csv"))))
R12 = 4.0 / 3.0
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
def logG_EW(y, xe, s):
    sv = V.GCSolverS(GR, y, xe, s, mutate=MUT); U, res, it = sv.solve()
    rf, gr = sv.field_monopole(); _, vir, wo = S10.jeans(rf, gr, [])
    return math.log10(6 * wo * R12 / y), res
e1w = 0.0; xew = 0.0; SATS = {}
RCUT = CLU["Pal 4"]["RGC"]
for r in (rowsS1 if not MUT else rowsS1[:6]):
    f = r["footing"]; a0 = A0[f]; y = float(r["y_plummer"]); xe = float(r["x_e_mid"]); dh = float(r["d_host_kpc"])
    xe_chk = g_mw(dh, MHOST[r["host"]], a0, 1.0) / a0
    xew = max(xew, abs(xe_chk / xe - 1))
    lg1, _ = logG_EW(y, xe, 1.0)
    e1w = max(e1w, abs(lg1 - float(r["logG_emb0"])))
    SATS[(f, r["name"])] = dict(row=r, lg1=lg1)
check("E1", e1w <= 1e-6, f"{e1w:.2e} ({len(SATS)} systems; host-field recompute max rel {xew:.1e})", "<= 1e-6",
      "S=1 reproduces S1's per-system logG_emb0 (E-W, central y, E_mid)")
SATR = {}
if not MUT:
    for f in FOOTS:
        s95 = S95C[f]
        sel = [v for (ff, nm), v in SATS.items() if ff == f]
        obs = np.array([float(v["row"]["log_gobs_gbar"]) for v in sel])
        v3d = np.array([float(v["row"]["Delta_v3_Lfloor"]) for v in sel])
        lg_unscr = np.array([float(v["row"]["logG_emb0"]) for v in sel])
        cfg = {"B95_MW": [], "B0_MW": [], "B95_MW+M31": []}
        nnew = {"MW": 0, "M31": 0}
        for v in sel:
            r = v["row"]; dh = float(r["d_host_kpc"]); host = r["host"]; y = float(r["y_plummer"]); a0 = A0[f]
            inside = dh <= RCUT and host in ("MW", "M31")
            if inside:
                xe95 = g_mw(dh, MHOST[host], a0, s95) / a0
                l95, _ = logG_EW(y, xe95, s95)
                l0, _ = logG_EW(y, xe95, 0.0)
                nnew[host] += 1
            cfg["B95_MW"].append(l95 if (inside and host == "MW") else float(r["logG_emb0"]))
            cfg["B0_MW"].append(l0 if (inside and host == "MW") else float(r["logG_emb0"]))
            cfg["B95_MW+M31"].append(l95 if inside else float(r["logG_emb0"]))
        med_v3 = float(np.median(v3d)); med_un = float(np.median(obs - lg_unscr))
        out = dict(N=len(sel), median_v3=med_v3, median_unscreened_noL=med_un, newly_screened=nnew, S95=s95)
        for k, arr in cfg.items():
            m = float(np.median(obs - np.array(arr))); out[k] = dict(median=m, shift_vs_v3=m - med_v3)
        SATR[f] = out
        P(f"   [{f}] N {len(sel)}: v3 median Delta {med_v3:+.3f} (S1 central values); no-gamma_L unscreened {med_un:+.3f}; "
          f"B95 (MW sats <= {RCUT:.1f} kpc at S {s95:.3f}) {out['B95_MW']['median']:+.3f} (shift {out['B95_MW']['shift_vs_v3']:+.3f}); "
          f"B0 {out['B0_MW']['median']:+.3f} (shift {out['B0_MW']['shift_vs_v3']:+.3f}); +M31 {out['B95_MW+M31']['median']:+.3f}; "
          f"newly screened MW {nnew['MW']}, M31 {nnew['M31']}")
    R["SATS"] = SATR

# ===================================================================================================== PART F (wide binaries)
P("\n[Part F] (c) wide binaries at 20 kAU (1+1 Msun, orientation-averaged, linear EFE of mu_S anchored to E2)")
e2j = json.load(open(rel("doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")))
GLc = np.array([0.0, -math.sqrt(0.6), math.sqrt(0.6)]); GLw = np.array([8 / 9, 5 / 9, 5 / 9])
def gam_lin(xe, s):
    mu = 1 - s / (1 + xe); dmu = s / (1 + xe) ** 2; L = xe * dmu / mu
    q = np.sqrt(1 - GLc ** 2 * L / (1 + L)); B = 1 / (mu * math.sqrt(1 + L) * q)
    return float(np.sum(GLw * np.sqrt(B)) / 2)
WB = {}; f1w = 0.0
for f in FOOTS:
    for gk in ("PREREG_primary", "PREREG_alt"):
        rr = e2j["R2"][f"{f}|{gk}"]; xe = rr["x_e"]; gE2 = rr["gamma_AQUAL_anch"]
        gl1 = gam_lin(xe, 1.0); f1w = max(f1w, abs(gl1 - gE2))
        def gam_S(s, xe=xe, gE2=gE2, gl1=gl1):
            return 1 + (gam_lin(xe, s) - 1) * (gE2 - 1) / (gl1 - 1)
        WB[f"{f}|{gk}"] = dict(x_e=xe, gamma_E2=gE2, gamma_lin_S1=gl1, by_S={str(s): gam_S(s) - 1 for s in (1.0, 0.5, 0.2, 0.0)})
check("F1", f1w <= 0.02, f"{f1w:.4f}", "<= 0.02", "linear EFE response at S=1 vs E2's registered AQUAL gamma_v (anchoring error)")
if not MUT:
    for f in FOOTS:
        for gk in ("PREREG_primary", "PREREG_alt"):
            w = WB[f"{f}|{gk}"]; sAf = REG[f"Sun|{f}"]["s_Sun_min_A"]
            gA = 1 + (gam_lin(w["x_e"], sAf) - 1) * (w["gamma_E2"] - 1) / (w["gamma_lin_S1"] - 1)
            w["Regime_A_s_Sun_min"] = sAf; w["Regime_A_gamma_minus_1_at_most_screened"] = gA - 1; w["Regime_B_gamma_minus_1"] = 0.0
            P(f"   [{f} {gk}] x_e {w['x_e']:.3f}: gamma_v - 1 = {w['by_S']['1.0']:.4f} (S=1, E2 anchor) / {w['by_S']['0.5']:.4f} (0.5) / "
              f"{w['by_S']['0.2']:.4f} (0.2) / 0 (S=0);  Regime A (s_Sun >= {sAf:.3f}) >= {gA - 1:.4f};  Regime B: 0")
R["WB"] = WB

# ===================================================================================================== PART G (SPARC RAR guard)
P("\n[Part G] (d) guard: SPARC RAR (P4's iso_perUps statistic) and the thin-slab test")
DATA = rel("real_research", "data")
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2); KPC_S = 3.0857e19
def load_sparc_own():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for fn in sorted(os.listdir(d_)):
        if not fn.endswith("_rotmod.dat"): continue
        try: d = np.genfromtxt(os.path.join(d_, fn), comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        gal.append(dict(name=fn.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))
    return gal
GALS = load_sparc_own()
def rar_stat(a0, s):
    num = den = 0.0; Us = []
    for q in GALS:
        Rm = q["R"] * KPC_S
        VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2
        GB = VB2 * 1e6 / Rm[:, None]; GO = ((q["Vobs"] * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
        OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
        W = (1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2)
        gb = np.maximum(GB, 1e-300)
        lgp = np.log10(np.where(GB > 0, V.g_law(gb / a0, s, MUT) * a0, 1e-300))
        r = np.where(OK, np.log10(np.where(OK, GO, 1.0)) - lgp, 0.0)
        Wm = np.where(OK, W[:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300); i = int(np.argmin(mse))
        num += float((Wm[:, i] * r[:, i] ** 2).sum()); den += float(Wm[:, i].sum()); Us.append(float(UPS[i]))
    return math.sqrt(num / den), float(np.median(Us))
p4 = json.load(open(rel("rebuild_2026_10_22", "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")))
RAR = {}; g1w = 0.0; g1u = True
for f in FOOTS:
    ref = p4["tiles"]["T1"]["footings"][f]["iso_perUps"]
    rms1, U1 = rar_stat(A0[f], 1.0)
    g1w = max(g1w, abs(rms1 - ref["rms"])); g1u &= (abs(U1 - ref["U_median"]) < 1e-9)
    RAR[f] = dict(P4_rms=ref["rms"], P4_U=ref["U_median"], S1=(rms1, U1))
check("G1", g1w <= 1e-4 and g1u, f"max|drms| {g1w:.1e}; U equal {g1u}", "<= 1e-4; equal",
      f"P4's iso_perUps reproduced ({len(GALS)} galaxies)")
SLAB = {}
if not MUT:
    for f in FOOTS:
        for lab, s in (("S95", S95C[f]), ("S0", 0.0)):
            RAR[f][lab] = rar_stat(A0[f], s)
        P(f"   [{f}] rms / median Ups: P4 {RAR[f]['P4_rms']:.4f}/{RAR[f]['P4_U']:.2f}; S=1 {RAR[f]['S1'][0]:.4f}/{RAR[f]['S1'][1]:.2f}; "
          f"S_95 {S95C[f]:.3f}: {RAR[f]['S95'][0]:.4f}/{RAR[f]['S95'][1]:.2f}; S=0: {RAR[f]['S0'][0]:.4f}/{RAR[f]['S0'][1]:.2f}")
    # thin slab (dimensionless: G = a0 = 1, R_d = 1; footing-free by construction, run once and reported for both)
    Rs_ = np.array([0.5, 1.0, 2.0, 3.0, 4.0, 6.0]); hdisc = 0.05
    for fac in (3.0, 0.3):
        Sig0 = fac / (2 * math.pi); Md_ = 2 * math.pi * Sig0
        rhof = lambda Rr, zr, Sig0=Sig0: Sig0 / (2 * hdisc) * np.exp(-Rr - np.abs(zr) / hdisc)
        gsl = S4.Grid(S4.log_edges(1e-3, 300 * max(10.0, math.sqrt(Md_)), 30), S4.theta_edges(48, full=False, stretch_min=0.002))
        rho = gsl.rho_axisym(rhof, nq=4); Mt = 2 * float(np.sum(rho * gsl.vol))
        gin = {}
        for lab, sf in (("S1", 1.0), ("slab0.1", lambda Rr, zr: np.where(np.abs(zr) < 0.1, 0.0, 1.0)),
                        ("slab0.3", lambda Rr, zr: np.where(np.abs(zr) < 0.3, 0.0, 1.0)), ("S0", 0.0)):
            pr = V.ProblemS(gsl, rho, Mt, 0.0, sfun=sf); pr.solve()
            dr, dt = gsl.grad_cells(pr.Phi); dR = np.sin(gsl.t2d) * dr + np.cos(gsl.t2d) * dt
            gin[lab] = gsl.interp_cells(dR, Rs_, np.zeros_like(Rs_))
        for lab in ("slab0.1", "slab0.3", "S0"):
            dl = np.log10(gin[lab] / gin["S1"])
            SLAB[f"Sigma0={fac}SigM|{lab}"] = dict(R_over_Rd=Rs_.tolist(), dlog_g=dl.tolist(), max_abs=float(np.max(np.abs(dl))))
            P(f"   slab test Sigma0 = {fac} Sigma_M, {lab:7s}: dlog g(R = 0.5..6 R_d) = " + " ".join(f"{v:+.3f}" for v in dl))
    R["RAR"] = RAR; R["SLAB"] = SLAB

# ===================================================================================================== PART H (well-posedness)
P("\n[Part H] (e) well-posedness: the khronon/dust pair + the screening field")
def gam_poly(Kv, Mv, Sv, mK, rh, cv, vv_, m2v, kk):
    a = [fn(Kv, Mv, Sv, mK, rh, cv, vv_, m2v, kk) for fn in COEF]
    rts = np.roots(a)
    return max(abs(np.sqrt(complex(x)).imag) for x in rts)
def gam_gammaL(kk, gL, Mv=1.21, rh=-1.0, Kv=1.0):
    chi = kk * kk / (Kv * Mv + gL * kk * kk)
    w2 = rh * (kk * kk / chi - Kv)
    return math.sqrt(max(-w2, 0.0))
ks = np.geomspace(1e-3, 1e8, 300); i5 = int(np.argmin(abs(ks - 1e5)))
h1ok = True; H1 = {}
if not MUT:
    for Sv in (1.0, 0.5, 0.1, 0.01):
        for mK in (0.0, 1.0):
            g0 = np.array([gam_poly(1.0, 1.21, Sv, mK, -1.0, 0.0, 1.0, 1.0, kk) for kk in ks])
            for cv in (0.0, 1.0, 10.0):
                gg = np.array([gam_poly(1.0, 1.21, Sv, mK, -1.0, cv, 1.0, 1.0, kk) for kk in ks])
                rat = gg[-1] / gg[i5]; ok = rat <= 1.01 and gg.max() <= g0.max() * (1 + 1e-6)
                h1ok &= ok; H1[f"S={Sv}|muK={mK}|c={cv}"] = dict(ratio_1e8_1e5=float(rat), Gmax=float(gg.max()), Gmax_uncoupled=float(g0.max()))
    check("H1", h1ok, f"max ratio {max(v['ratio_1e8_1e5'] for v in H1.values()):.6f}", "<= 1.01 and Gmax <= uncoupled cap",
          "rho_tau < 0, S in {1,.5,.1,.01}, mu_K in {0,1}, mixing c in {0,1,10}: growth rate bounded in k")
else:
    gg = np.array([gam_gammaL(kk, 0.5) for kk in ks]); rat = gg[-1] / gg[i5]
    check("H1", rat <= 1.01, f"ratio {rat:.1f} (gamma_L restored)", "<= 1.01", "MUTATE: H1 run with gamma_L restored must read unbounded")
gg = np.array([gam_gammaL(kk, 0.5) for kk in ks]); rat2 = gg[-1] / gg[i5]
check("H2", 900 <= rat2 <= 1100, f"{rat2:.1f}", "[900, 1100]", "gamma_L restored (H4's term): Gamma ~ k, unbounded (reproduces H4)")
R["H1"] = H1
h4 = json.load(open(rel("rebuild_2026_10_22", "H4_v3_saddle_stability", "h4_v3_saddle_stability_results.json")))
KH4 = 4 * math.pi * G_H4
h3w = 0.0; H3 = {}
for key, e in h4["efolds"].items():
    sysk = "|".join(key.split("|")[:3])
    if sysk in H3: continue
    reg = h4["regions"][sysk]["f0"]["fine"]["near"]
    if reg.get("empty"): continue
    T = e["T_Gyr"] * SEC_GYR
    rows = {}
    for lab, rk, xk in (("median", "median_abs_rho", "x_median"), ("max", "max_abs_rho_excl_null", "x_at_max")):
        rho = reg[rk]; xx = reg[xk]
        G1_ = math.sqrt(KH4 * rho * ((1 + xx) ** 2 - 1.0)); G0_ = math.sqrt(KH4 * rho * (1 + xx) ** 2)
        h3w = max(h3w, abs(G1_ / e[lab]["Gamma_bounded_s-1"] - 1))
        rows[lab] = dict(N_S1=G1_ * T, N_S0=G0_ * T, H4_N_bounded=e[lab]["N_bounded"])
    H3[sysk] = dict(T_Gyr=e["T_Gyr"], **rows)
check("H3", h3w <= 1e-6, f"{h3w:.1e}", "<= 1e-6", "S=1 bounded rate reproduces H4's Gamma_bounded on every region (median and max)")
if not MUT:
    for k, v in H3.items():
        P(f"   {k:32s} T {v['T_Gyr']:5.2f} Gyr: N(S=1) median {v['median']['N_S1']:.3f} max {v['max']['N_S1']:.3f};  N(S=0) median {v['median']['N_S0']:.3f} max {v['max']['N_S0']:.3f}")
R["H3"] = H3
# the Sun's would-be phantom without gamma_L (S -> 0 inside a screened region)
HS = {}
if not MUT:
    rr = np.geomspace(0.01, 100, 600); th = np.linspace(1e-3, math.pi - 1e-3, 601)
    RR, TT = np.meshgrid(rr, th, indexing="ij")
    for f in FOOTS:
        a0 = A0_D7[f]; rM = rM_of(a0)
        for xe in (0.0, 1.15, 2.6):
            vr = 1 / RR ** 2 + xe * np.cos(TT); vt = -xe * np.sin(TT); vm = np.hypot(vr, vt)
            dd = -(vm ** 2 - 3 * vr ** 2) / (RR ** 3 * vm * (1 + vm) ** 2)
            neg = dd < 0
            if xe == 0.0:
                HS[f"{f}|isolated_min_d"] = float(dd.min()); continue
            DP = a0 / (4 * math.pi * G_H4 * rM) * dd                    # kg/m^3
            Gam = np.sqrt(np.where(neg, (a0 / rM) * np.abs(dd) * (1 + vm) ** 2, 0.0))
            near = neg & (RR < 10)
            msun_pc3 = MSUN / PC ** 3
            HS[f"{f}|x_e={xe}"] = dict(min_DP_Msun_pc3=float(DP.min() / msun_pc3), frac_volume_neg_r_lt_10=float(near.sum() / (RR < 10).sum()),
                                       Gamma_max=float(Gam.max()), N_4p6Gyr=float(Gam.max() * 4.6 * SEC_GYR), N_60Myr=float(Gam.max() * 0.06 * SEC_GYR),
                                       Gamma_median_neg=float(np.median(Gam[near])), N_median_60Myr=float(np.median(Gam[near]) * 0.06 * SEC_GYR))
            h = HS[f"{f}|x_e={xe}"]
            P(f"   Sun [{f}] x_e {xe}: would-be D.P min {h['min_DP_Msun_pc3']:.1f} Msun/pc^3; negative lobes; S->0 rate max {h['Gamma_max']:.2e} s^-1 "
              f"-> N {h['N_60Myr']:.0f} (60 Myr) / {h['N_4p6Gyr']:.0f} (4.6 Gyr); median over lobes N(60 Myr) {h['N_median_60Myr']:.0f}; "
              "metric coupling of the mode ~ s")
        P(f"   Sun [{f}] isolated: min would-be D.P {HS[f'{f}|isolated_min_d']:.3e} (>= 0 expected)")
R["H_sun"] = HS
R["H5_symmetron_tachyon"] = "rate (c/lambda_C) sqrt(1 - rho/rho_*) in the symmetric phase below rho_*; k-independent cap; saturates at the VEV (quartic)"

# ===================================================================================================== PART I (constants, f)
if not MUT:
    P("\n[Part I] constants and (f)")
    I1 = (REG["fit_exists_A"] == REG["fit_exists_B"])
    check("I1", I1, f"fit exists: Regime A {REG['fit_exists_A']}, Regime B {REG['fit_exists_B']}", "same in A and B",
          "lambda_C decouples from the tested verdicts (it sets the A/B boundary)")
    I2 = {}; i2ok = True
    Rs_k = CLU["Pal 4"]["RGC"]
    for f in FOOTS:
        a0 = A0[f]
        x = g_mw(Rs_k, EBR[f]["E_mid"], a0, 1.0) / a0
        LP = a0 ** 2 / (4 * math.pi * G) * (x - math.log1p(x))
        phiN = G * EBR[f]["E_mid"] * MSUN / (Rs_k * KPC + A_H)
        out = {}
        for lab, A_ in (("strict 0.1x2|Phi_N|", 0.1 * 2 * phiN), ("generous (300 km/s)^2", 9e10)):
            rho_min = 10 * LP / A_
            Mimp = (4 * math.pi / 3) * (Rs_k * KPC) ** 3 * rho_min / MSUN
            out[lab] = dict(allowance=A_, rho_min_kg_m3=rho_min, rho_min_Msun_pc3=rho_min / (MSUN / PC ** 3),
                            n_H_cm3=rho_min / (1.4 * 1.6726e-27) / 1e6, M_implied=Mimp, over_Mb_Ehi=Mimp / EBR[f]["E_hi"])
        i2ok &= out["generous (300 km/s)^2"]["M_implied"] <= EBR[f]["E_hi"]
        I2[f] = dict(x=x, L_P0=LP, R_s_kpc=Rs_k, **out)
        P(f"   I2 [{f}] at R_s = {Rs_k:.1f} kpc, x = {x:.3f}: L_P0 = {LP:.2e} J/m^3; window needs rho_gas >= "
          f"{out['generous (300 km/s)^2']['rho_min_Msun_pc3']:.2e} Msun/pc^3 (n_H {out['generous (300 km/s)^2']['n_H_cm3']:.2e} cm^-3; generous) / "
          f"{out['strict 0.1x2|Phi_N|']['rho_min_Msun_pc3']:.2e} (strict) -> implied gas inside R_s >= {out['generous (300 km/s)^2']['M_implied']:.2e} Msun "
          f"= {out['generous (300 km/s)^2']['over_Mb_Ehi']:.1f} x M_b(E_hi)")
    check("I2", i2ok, f"implied/M_b(E_hi) = {I2['canonical']['generous (300 km/s)^2']['over_Mb_Ehi']:.1f} / {I2['alt']['generous (300 km/s)^2']['over_Mb_Ehi']:.1f}",
          "<= 1 (both footings)", "a v^2/M^2 window exists (back-reaction <= 10% and fifth-force step within the allowance)")
    R["I2"] = I2
    # (f) MW and clusters under the fit's regime (MW halo at s <= S_95)
    BR = {}
    for fn, key in (("mw_kz11_bovyrix2013_table3.tsv", "BR"), ("mw_rc_eilers2019_table1.tsv", "EIL")):
        rws = [l.split() for l in open(os.path.join(DATA, fn)) if l.strip() and not l.startswith("#")]
        hdr = rws[0]; arr = np.array([[float(x) for x in rw] for rw in rws[1:]]); BR[key] = {h: arr[:, i] for i, h in enumerate(hdr)}
    BR_R = BR["BR"]["R_kpc"] + (R0_MW - 8.0); BR_K = BR["BR"]["Kz11_o2piG"]; BR_E5 = np.hypot(BR["BR"]["dKz11_o2piG"], 0.05 * BR_K)
    EIL_R, EIL_V = BR["EIL"]["R_kpc"], BR["EIL"]["vc_kms"]; EIL_E = np.hypot(0.5 * (BR["EIL"]["sig_minus"] + BR["EIL"]["sig_plus"]), 0.02 * EIL_V)
    SIGU = S4.MSUN / (S4.KPC / 1e3) ** 2
    MWR = {}
    for f in FOOTS:
        gmw, rho1, Mt, Mu = MWG[f]; a0 = A0[f]
        for lab, s in (("S1", 1.0), ("S95", S95C[f]), ("S0", 0.0)):
            pr = V.ProblemS(gmw, rho1, Mt, 0.0, sfun=s); pr.solve()
            dr, dt = gmw.grad_cells(pr.Phi)
            dz = np.cos(gmw.t2d) * dr - np.sin(gmw.t2d) * dt; dR = np.sin(gmw.t2d) * dr + np.cos(gmw.t2d) * dt
            conv = a0 / (2 * math.pi * S4.G_SI) / SIGU
            K = gmw.interp_cells(dz, BR_R, np.full_like(BR_R, 1.1)) * conv
            K0 = float(gmw.interp_cells(dz, np.array([R0_MW]), np.array([1.1]))[0] * conv)
            vc = np.sqrt(np.maximum(gmw.interp_cells(dR, EIL_R, np.zeros_like(EIL_R)), 0) * a0 * EIL_R * S4.KPC) / 1e3
            vc0 = float(np.sqrt(max(gmw.interp_cells(dR, np.array([R0_MW]), np.array([0.0]))[0], 0) * a0 * R0_MW * S4.KPC) / 1e3)
            MWR[f"{f}|{lab}"] = dict(S=s, K_R0=K0, chi2_Kz=float(np.sum(((K - BR_K) / BR_E5) ** 2)), vc_R0=vc0,
                                     chi2_RC=float(np.sum(((vc - EIL_V) / EIL_E) ** 2)), N_Kz=len(BR_K), N_RC=len(EIL_V))
        P(f"   MW [{f}] K_z(R0, 1.1) S=1 {MWR[f'{f}|S1']['K_R0']:.1f} (P4 {p4['tiles']['T4']['models']['B1_McMillan17'][f]['F0|L0']['K_R0']:.1f}) / "
          f"S_95 {MWR[f'{f}|S95']['K_R0']:.1f} / S=0 {MWR[f'{f}|S0']['K_R0']:.1f} vs 66.4 +- 2.2; chi2_Kz {MWR[f'{f}|S1']['chi2_Kz']:.0f} / "
          f"{MWR[f'{f}|S95']['chi2_Kz']:.0f} / {MWR[f'{f}|S0']['chi2_Kz']:.0f} (N {len(BR_K)}); v_c(R0) {MWR[f'{f}|S1']['vc_R0']:.1f} / "
          f"{MWR[f'{f}|S95']['vc_R0']:.1f} / {MWR[f'{f}|S0']['vc_R0']:.1f} km/s; chi2_RC {MWR[f'{f}|S1']['chi2_RC']:.0f} / "
          f"{MWR[f'{f}|S95']['chi2_RC']:.0f} / {MWR[f'{f}|S0']['chi2_RC']:.0f} (N {len(EIL_V)})")
    R["MW"] = MWR
    f1 = json.load(open(rel("rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))
    R["clusters_newton_h070"] = f1["newton_h070"]
    P(f"   clusters: if the ICM is screened (it is far denser than halo gas at 100 kpc) the prediction is Newtonian baryons: "
      f"F1's A_MID {f1['newton_h070']['MID'][0]:.2f} +- {f1['newton_h070']['MID'][1]:.2f} (law: 1.68-1.85 can / 1.54-1.70 alt)")

# ===================================================================================================== verdict
rss_p = rss_gb(); rss_c = max(rss_gb(resource.RUSAGE_CHILDREN), R.get("D_child_rss_gb", 0.0))
check("K-RSS", rss_p < 1.0 and rss_c < 1.0, f"parent {rss_p:.3f} GB, child {rss_c:.3f} GB", "< 1 GB", "peak RSS")
if not MUT:
    P("\n--- verdict lines ---")
    one = CHK["I1"]["ok"] and CHK["I2"]["ok"]
    count = "ONE CONSTANT" if one else ">= 2 constants (" + ", ".join(n for n, ok in (("lambda_C", CHK["I1"]["ok"]), ("v^2/M^2", CHK["I2"]["ok"])) if not ok) + " do not decouple)"
    P(f"   COUNT: {count}")
    fitA = REG["fit_exists_A"]
    P(f"   FIT: Regime A {'EXISTS' if fitA else 'DOES NOT EXIST'}; Regime B EXISTS only via halo gas (P-mono): S_95 central {S95C['canonical']:.3f} / {S95C['alt']:.3f}")
    Va = {}
    for f in FOOTS:
        sAf = REG[f"Sun|{f}"]["s_Sun_min_A"]; st = min(SC[f], SPL[f])
        Va[f] = dict(A="PASS" if sAf <= st else "FAIL", B="PASS (s_Sun = 0 under P-mono)")
    P(f"   V-a Cassini/planets: Regime A {Va['canonical']['A']} / {Va['alt']['A']}; Regime B {Va['canonical']['B']}")
    Vb = all(abs(SATR[f]["B95_MW"]["shift_vs_v3"]) <= 0.05 for f in FOOTS)
    P(f"   V-b dwarfs (Regime B, the fit's regime): shift vs v3 {SATR['canonical']['B95_MW']['shift_vs_v3']:+.3f} / {SATR['alt']['B95_MW']['shift_vs_v3']:+.3f} dex -> {'PASS' if Vb else 'FAIL'}")
    halo_ok = all(RAR[f]["S95"][0] <= RAR[f]["P4_rms"] + 0.010 and abs(RAR[f]["S95"][1] - RAR[f]["P4_U"]) <= 0.05 for f in FOOTS)
    slab_ok = max(v["max_abs"] for k, v in SLAB.items() if "slab" in k) <= 0.01
    Vd = "PASS" if halo_ok else ("CONDITIONAL" if slab_ok else "FAIL")
    P(f"   V-d SPARC RAR: halo-screened (S_95) {'passes' if halo_ok else 'fails'}; slab-only max |dlog g| {max(v['max_abs'] for k, v in SLAB.items() if 'slab' in k):.3f} -> {Vd}")
    Ve = "ILL-POSED" if not CHK["H1"]["ok"] else "BOUNDED"
    P(f"   V-e well-posedness: {Ve} (gamma_L's Hadamard instability removed; bounded khronon rates; s -> 0 decouples and strongly couples the khronon)")
    # per regime where the fit exists: (Va, Vb, Vd) and whether a pass rests on an unmeasured input
    regs = {}
    if fitA:
        regs["A"] = dict(Va=all(Va[f]["A"] == "PASS" for f in FOOTS), Va_cond=False, Vb=None, Vd=Vd)
    regs["B"] = dict(Va=True, Va_cond=True, Vb=Vb, Vd=Vd)          # Regime B: Va passes only under P-mono (unmeasured halo gas)
    verdict = "NO-GO"
    for rk, rv in regs.items():
        okall = rv["Va"] and bool(rv["Vb"]) and rv["Vd"] in ("PASS", "CONDITIONAL") and Ve != "ILL-POSED"
        if one and okall and not rv["Va_cond"] and rv["Vd"] == "PASS":
            verdict = "PASS"; break
        if one and okall:
            verdict = "CONDITIONAL"
    R["verdict_regimes"] = regs
    P(f"   VERDICT: {verdict} for 'a well-posed one-constant density screen replaces gamma_L'")
    R["verdict"] = dict(count=count, fit_A=fitA, Va=Va, Vb=Vb, Vd=Vd, Ve=Ve, verdict=verdict)

npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
R["checks"] = CHK; R["runtime_s"] = time.time() - T0; R["rss_parent_gb"] = rss_p; R["rss_child_gb"] = rss_c
P(f"\nV1_DENSITY_SCREEN COMPLETE: {npass}/{ntot} checks PASS.  {time.time() - T0:.0f} s" + ("  (MUTATE: validations only)" if MUT else ""))
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
json.dump(clean(R), open(os.path.join(HERE, f"v1_density_screen_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"v1_density_screen{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
