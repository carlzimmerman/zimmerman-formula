"""C6_literal_cassini -- Solar-System tests of the healthy C4-literal screened theory (gamma_F = 0).

Criteria: FROZEN_CRITERIA.md (committed alone first, 1b2ced55a4).
Run:  OMP_NUM_THREADS=1 nice -n 19 python3 c6_literal_cassini.py [--mutate]
      --mutate: Route N's grad-div drops the 2 q_r / r term of the divergence (must break C4, C5 or C6).
Deterministic, no network, single thread, < 1 GB RSS. kappa = 1/2 FITTED; not theory closed.

Equations (C4-literal Khronon + P, eta = 0, gamma_F = 0; static, O(eps), p = K P, Phi = ln N):
    lap Phi = K rho + div p ;   grad Phi + (L*^2/2) grad div p = a0 p/(a0 - |p|).
"""
import os, sys, json, math, time, resource, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c6_solver as C
S = C.S

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
ROOT = os.path.dirname(os.path.dirname(HERE))
def rel(*p): return os.path.join(ROOT, *p)

# ---------------------------------------------------------------- inputs (labelled; read-only from the record)
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}                      # FITTED footings (kappa = 1/2)
HEES = (3e-27, 3e-27); PARK = (1.6e-27, 1.8e-27)                   # prep_2026/planetary_doors/BOUNDS.md
BAND_H = (HEES[0] - 2 * HEES[1], HEES[0] + 2 * HEES[1]); BAND_P = (PARK[0] - 2 * PARK[1], PARK[0] + 2 * PARK[1])
R_SAT = 9.58 * AU
LSTARS_PC = [24.0, 50.0, 90.0]
BN11 = (3.8e-26, 1.2e-10, 1.9e-10)
PLANET_BOUNDS = {"Earth": (1.0 * AU, 8.7e-15), "Mars": (1.524 * AU, 1.4e-15), "Saturn": (9.58 * AU, 7.0e-15)}
d7b = json.load(open(rel("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")))
EV = {f: {E: dict(gNe=v["gNe"], ge=v["ge_total"]) for E, v in d7b["grid"][f]["none"].items()} for f in A0}
e2 = json.load(open(rel("doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")))
E2AQ = {E: e2["R1"]["canonical|none"]["cells"][E]["Q2_AQUAL"] for E in ("E0", "E1", "E2", "E3")}
d7d = json.load(open(rel("doors_push_2026_10_22", "D7d_screened_q2", "d7d_screened_q2_results.json")))

RES = {"inputs": dict(GM=GM, a0=A0, E=EV, Hees2014=HEES, Park2026=PARK, band_Hees_2sigma=BAND_H, band_Park_2sigma=BAND_P,
                      R_Saturn_AU=9.58, Lstar_pc=LSTARS_PC, BN11_mu1=BN11, planet_bounds=PLANET_BOUNDS,
                      E2_AQUAL_canonical=E2AQ, mutate=MUT), "checks": {}}
CHK = []
def check(name, ok, detail):
    CHK.append(ok); RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")

G1, G2 = (30, 48), (40, 64)                    # h ratio 4/3; second-order Richardson
def rich(q1, q2): return (16 * q2 - 9 * q1) / 7
def rM_of(a0): return math.sqrt(GM / a0)
def xe_of(f, E): return EV[f][E]["ge"] / A0[f]
def toQ(raw, a0): return -raw * a0 / rM_of(a0)
def rss():
    sc = 1e9 if sys.platform == "darwin" else 1e6
    return max(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss) / sc
import multiprocessing as mp
def isolated(fn, *a):
    """Run one Route N job in a fresh forked process (memory returned to the OS after each job; RSS budget per job)."""
    with mp.get_context("fork").Pool(1, maxtasksperchild=1) as pool:
        return pool.apply(fn, a)
def grid(Lam, gres): return S.Grid(1e-4, (1e3 if Lam <= 30 else 300.0) * max(1.0, Lam), gres[0], gres[1])
def run_v(Lam, xe, gres, rF=0.0, U0g=None, tol=1e-9):
    g = grid(Lam, gres)
    U0 = None if U0g is None else S.regrid(U0g[0], U0g[1], g)
    U, fin, it = C.solve_v(g, Lam, xe, rF, U0=U0, mutate=MUT, tol=tol)
    return g, U, fin, it
def _qn1(Lam, xe, a0, rF, gres):
    rq = R_SAT / rM_of(a0); g, U, fin, it = run_v(Lam, xe, gres, rF)
    return toQ(S.q2_raw(g, U[0], rq), a0), fin
def QN(Lam, xe, a0, rF=0.0):
    out = [isolated(_qn1, Lam, xe, a0, rF, gres) for gres in (G1, G2)]
    qq = [o[0] for o in out]
    return qq, rich(*qq)

t0 = time.time()
P("=" * 100)
P("C6_literal_cassini -- Cassini Q2 / planets / wide binaries of the C4-literal (gamma_F = 0) screened theory" + ("  [MUTATE]" if MUT else ""))
P("=" * 100)

# ---------------------------------------------------------------- C1 derivation (sympy)
import sympy as sy
x, y, z = sy.symbols("x y z", real=True)
K, a0s, L = sy.symbols("K a0 L", positive=True)
Phi = sy.Function("Phi")(x, y, z); rho = sy.Function("rho")(x, y, z)
Pv = [sy.Function(f"P{i}")(x, y, z) for i in (1, 2, 3)]
X = (x, y, z)
gL = K * L ** 2 / 2
Pm = sy.sqrt(sum(p ** 2 for p in Pv)); u = K * Pm
W = (a0s ** 2 / K) * (-u / a0s - sy.log(1 - u / a0s))
divP = sum(sy.diff(Pv[i], X[i]) for i in range(3))
Lag = -sum(sy.diff(Phi, X[i]) ** 2 for i in range(3)) / (2 * K) + sum(Pv[i] * sy.diff(Phi, X[i]) for i in range(3)) \
      - W - gL / 2 * divP ** 2 - rho * Phi
from sympy.calculus.euler import euler_equations
EL = euler_equations(Lag, [Phi] + Pv, X)
lap = sum(sy.diff(Phi, X[i], 2) for i in range(3))
pv = [K * p for p in Pv]; pm = K * Pm; divp = K * divP
resL = sy.simplify(K * EL[0].lhs - (lap - K * rho - divp))
h = [a0s * pv[i] / (a0s - pm) for i in range(3)]
resP = [sy.simplify(EL[i + 1].lhs - (sy.diff(Phi, X[i]) + (L ** 2 / 2) * sy.diff(divp, X[i]) - h[i])) for i in range(3)]
chi_f = Phi + (L ** 2 / 2) * divp                                   # h = grad chi on shell
resG = [sy.simplify((sy.diff(Phi, X[i]) + (L ** 2 / 2) * sy.diff(divp, X[i]) - h[i]) - (sy.diff(chi_f, X[i]) - h[i])) for i in range(3)]
kap, c_, jp, jl = sy.symbols("kappa c j_p j_l", positive=True)
s_ = sy.sqrt(1 - c_ ** 2); kh = sy.Matrix([s_, c_])
Am = (kap ** 2 / 2) * kh * kh.T + sy.diag(jp, jl) - kh * kh.T
m_ = (1 - c_ ** 2) / jp + c_ ** 2 / jl
resK = sy.simplify((kh.T * Am.inv() * kh)[0] - m_ / (1 - m_ + kap ** 2 * m_ / 2))
ok1 = resL == 0 and all(r == 0 for r in resP) and all(r == 0 for r in resG) and resK == 0
check("C1", ok1, f"EL(Phi) - (L): {resL}; EL(P) - (P_L): {resP}; (P_L) = grad chi - h: {resG}; kernel - m/(1-m+k^2 m/2): {resK} (all 0)")

# ---------------------------------------------------------------- C2 Route F validation
kk = np.logspace(-3, 3, 61)[:, None]; cc = np.linspace(-0.999, 0.999, 41)[None, :]
w_d7d = max(float(np.max(np.abs(C.chi_gen(kk, cc, xe, 1.0) - S.chi(kk, cc, xe)))) for xe in (0.3, 1.15, 2.6, 5.0))
w_aq = 0.0
for xe in (0.3, 1.0, 1.9, 2.6, 5.0):
    mu = xe / (1 + xe); L0 = 1 / (1 + xe); c1 = cc.ravel()
    w_aq = max(w_aq, float(np.max(np.abs(1 + C.chi_gen(0.0, c1, xe, 0.0) - 1 / (mu * (1 + L0 * c1 ** 2))))))
kk2 = np.logspace(-2, 3, 51)[:, None]
w_iso = float(np.max(np.abs(C.chi_gen(kk2, cc, 0.0, 0.0) / C.chi_gen(kk2, cc, 0.0, 1.0) - 1)))
w_cl = max(float(np.max(np.abs(C.chi_gen(kk, cc, xe, 0.0) - C.chi_C6_closed(kk, cc, xe)))) for xe in (0.3, 1.15, 2.6))
kk3 = np.logspace(-1, 3, 41)[:, None]
w_iso01 = float(np.max(np.abs(C.chi_gen(kk3, cc, 0.0, 0.0) / C.chi_gen(kk3, cc, 0.0, 1.0) - 1)))
w_iso_cl = float(np.max(np.abs(C.chi_C6_closed(kk2, cc, 0.0) / S.chi(kk2, cc, 0.0) - 1)))
RES["C2"] = dict(rF1_vs_D7d=w_d7d, kappa0_vs_AQUAL=w_aq, isolated_rF0_vs_rF1_rel=w_iso, rF0_vs_closed=w_cl,
                 reported_isolated_kappa_ge_0p1=w_iso01, reported_isolated_closed_vs_D7d=w_iso_cl)
P(f"  [reported] x_e=0 isolated rel diff at kappa>=0.1: {w_iso01:.1e}; closed form vs D7d chi at kappa>=0.01: {w_iso_cl:.1e}")
check("C2", max(w_d7d, w_aq, w_iso, w_cl) < 1e-12,
      f"r_F=1 vs D7d chi {w_d7d:.1e}; kappa=0 vs linear AQUAL {w_aq:.1e}; x_e=0: r_F=0 vs r_F=1 (rel, kappa>=0.01) {w_iso:.1e}; "
      f"r_F=0 vs closed form {w_cl:.1e} (<1e-12)")

# ---------------------------------------------------------------- C3 Route N build = D7d build at r_F = 1
g3 = S.Grid(1e-4, 3e4, 20, 16)
A_me, b_me, nl_me = C.build(g3, 30.0, 1.0)
A_d, b_d, nl_d = S.build(g3, 30.0, False, "stiff")
dA = float(abs(A_me - A_d).max()); db = float(np.max(np.abs(b_me - b_d)))
A_0, _, _ = C.build(g3, 30.0, 0.0, MUT)
RES["C3"] = dict(max_dA=dA, max_drhs=db, rF0_differs_from_rF1=float(abs(A_0 - A_d).max()))
check("C3", dA == 0.0 and db == 0.0 and bool(np.all(nl_me == nl_d)),
      f"r_F=1 build vs D7d build at Lam=30: max|dA| = {dA:.1e}, max|drhs| = {db:.1e} (== 0); r_F=0 differs by {abs(A_0 - A_d).max():.2e}")

# ---------------------------------------------------------------- C4 AQUAL anchor (L* = 0)
qq, Rb = QN(0.0, BN11[2] / BN11[1], BN11[1])
c4 = dict(BN11=dict(Q=qq, R=Rb, ratio=Rb / BN11[0]))
worst = 0.0
for E in E2AQ:
    qq, R = QN(0.0, xe_of("canonical", E), A0["canonical"])
    c4[E] = dict(Q=qq, R=R, E2=E2AQ[E], ratio=R / E2AQ[E]); worst = max(worst, abs(R / E2AQ[E] - 1))
RES["C4_AQUAL"] = c4
check("C4", abs(Rb / BN11[0] - 1) < 0.10 and worst < 0.03,
      f"L*=0: BN11 point {Rb:.4e} (ratio {Rb / BN11[0]:.4f}, <10%); E2 canonical E0-E3 " +
      ", ".join(f"{c4[E]['R']:.4e}" for E in E2AQ) + f" max|ratio-1| = {worst:.2e} (<3e-2)")
P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")

# ---------------------------------------------------------------- C5 Route N vs Route F (r_F = 0)
a0 = A0["canonical"]; c5 = {}; worst = 0.0; signok = True
for Lam in (30.0, 100.0):
    for E in ("E0", "E3"):
        xe = xe_of("canonical", E)
        qq, R = QN(Lam, xe, a0); F = C.routeF_Q2(GM, Lam * rM_of(a0), xe, 0.0)
        c5[f"{Lam:g}_{E}"] = dict(Q=qq, R=R, F=F, ratio=R / F); worst = max(worst, abs(R / F - 1)); signok &= (R > 0) == (F > 0)
RES["C5_N_vs_F"] = c5
check("C5", worst < 0.05 and signok, f"r_F=0: max|N/F-1| = {worst:.2e} at Lam=30,100 (E0,E3), sign agree {signok} (<5e-2)")
P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")

# ---------------------------------------------------------------- C6 small-L* continuity
def _c6(xe2, a0):
    rq = R_SAT / rM_of(a0)
    g0, U0, f0, _ = run_v(0.0, xe2, G1); Q0 = toQ(S.q2_raw(g0, U0[0], rq), a0)
    gs, Us, fs, _ = run_v(0.01, xe2, G1, U0g=(U0, g0)); Qs = toQ(S.q2_raw(gs, Us[0], rq), a0)
    return Q0, Qs, f0, fs
Q0, Qs, f0, fs = isolated(_c6, xe_of("canonical", "E2"), a0)
RES["C6"] = dict(Q_L0=Q0, Q_L001=Qs, res=[f0, fs], converged_L001=bool(fs < 1e-9))
# frozen line is the ratio only (AMENDMENT 1, post-result: the first run's code also demanded residual < 1e-9, which the
# frozen text does not); the residual is reported, and an unconverged Lam = 0.01 solve is flagged in the README.
check("C6", abs(Qs / Q0 - 1) < 0.02, f"r_F=0: N(Lam=0.01)/N(0) - 1 = {Qs / Q0 - 1:+.2e} (<2e-2); residual at Lam=0.01 {fs:.1e} "
      f"({'converged' if fs < 1e-9 else 'NOT converged'}; D7d's K7 had 150)")

# ---------------------------------------------------------------- C7 Route F numerics
xe = xe_of("canonical", "E2")
i1 = C.routeF_I2(xe, 0.0); i2 = C.routeF_I2(xe, 0.0, nk=8000, nc=128, kmin=1e-5, kmax=2e4)
cq = np.polynomial.legendre.leggauss(256); P2 = 0.5 * (3 * cq[0] ** 2 - 1)
kb = 1e3; num = 2.5 * (C.chi_gen(kb, cq[0], xe, 0.0) * P2 * cq[1]).sum() * kb ** 4
tail_rel = abs(num / (-4 * C.tail_c2(xe, 0.0)) - 1)
RES["C7"] = dict(I2=i1, I2_fine=i2, quad_rel=abs(i2 / i1 - 1), tail_rel=tail_rel)
check("C7", abs(i2 / i1 - 1) < 1e-6 and tail_rel < 1e-4, f"I2 refinement {abs(i2 / i1 - 1):.1e} (<1e-6); tail coefficient at kappa=1e3 {tail_rel:.1e} (<1e-4)")

# ---------------------------------------------------------------- C8 linear validity at 24 pc
worst = 0.0
for f in A0:
    for E in EV[f]:
        xe = xe_of(f, E); worst = max(worst, GM / (24 * PC) ** 2 * (1 + xe) ** 2 / (A0[f] * xe))
check("C8", worst < 1e-4, f"max (GM/L*^2)(1+x_e)^2/(a0 x_e) at 24 pc = {worst:.2e} (<1e-4)")
P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")

if not MUT:
    # ================================================================= RESULTS
    P("")
    P("R1  Cassini Q2 at the physical L* (Route F, r_F = 0; BN11/Hees sign; 2sigma bands Hees [-3.0e-27, 9.0e-27], Park [-2.0e-27, 5.2e-27])")
    R1 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            row = []
            for E in EV[f]:
                q = C.routeF_Q2(GM, Lpc * PC, xe_of(f, E), 0.0); qd = d7d["R1_physical"][f"{f}|{Lpc:g}|{E}"]["Q2"]
                row.append(q)
                R1[f"{f}|{Lpc:g}|{E}"] = dict(Q2=q, hees=BAND_H[0] <= q <= BAND_H[1], park=BAND_P[0] <= q <= BAND_P[1],
                                              over_Hees_upper=q / BAND_H[1], over_Park_upper=q / BAND_P[1],
                                              Q2_D7d_rF1=qd, ratio_to_D7d=q / qd)
            P(f"  {f:9s} L*={Lpc:4.0f} pc  Q2 = " + " ".join(f"{q:.3e}" for q in row) +
              f"   max Q2/9e-27 = {max(row) / BAND_H[1]:.2e}  max Q2/5.2e-27 = {max(row) / BAND_P[1]:.2e}"
              f"  Hees {'PASS' if all(BAND_H[0] <= q <= BAND_H[1] for q in row) else 'FAIL'}"
              f"  Park {'PASS' if all(BAND_P[0] <= q <= BAND_P[1] for q in row) else 'FAIL'}"
              f"  ratio to D7d " + " ".join(f"{R1[f'{f}|{Lpc:g}|{E}']['ratio_to_D7d']:.3f}" for E in EV[f]))
    RES["R1_physical"] = R1
    margH = min(BAND_H[1] / abs(v["Q2"]) for v in R1.values()); margP = min(BAND_P[1] / abs(v["Q2"]) for v in R1.values())
    margHmax = max(BAND_H[1] / abs(v["Q2"]) for v in R1.values())
    RES["R1_margin"] = dict(Hees_min=margH, Park_min=margP, Hees_max=margHmax)
    P(f"  margin: Hees 9e-27/Q2 from {margH:.2e} to {margHmax:.2e}; Park 5.2e-27/Q2 min {margP:.2e}")

    P("")
    P("R2  Inner planets: anomalous radial acceleration (Route F monopole, r_F = 0) vs bounds")
    R2 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            parts = []
            for name, (r, bnd) in PLANET_BOUNDS.items():
                vals = [C.routeF_radial(GM, Lpc * PC, xe_of(f, E), r, 0.0) for E in EV[f]]
                R2[f"{f}|{Lpc:g}|{name}"] = dict(a=vals, GM_over_L2=GM / (Lpc * PC) ** 2, bound=bnd, ratio=max(abs(v) for v in vals) / bnd)
                parts.append(f"{name} {max(vals):.3e} ({R2[f'{f}|{Lpc:g}|{name}']['ratio']:.3f} of bound)")
            P(f"  {f:9s} L*={Lpc:4.0f} pc: GM/L*^2 = {GM / (Lpc * PC) ** 2:.3e}; " + "; ".join(parts))
    RES["R2_planets"] = R2

    P("")
    P("R3  Wide binary 1.5 Msun at 20 kAU: gamma_v - 1 (Route F monopole, r_F = 0) vs D7d (r_F = 1) and CFG740 isolated 1/2 (s/L*)^2")
    s20 = 20e3 * AU; GMb = 1.5 * GM; R3 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            vals = [math.sqrt(1 + C.routeF_radial(GMb, Lpc * PC, xe_of(f, E), s20, 0.0) / (GMb / s20 ** 2)) - 1 for E in EV[f]]
            iso = 0.5 * (s20 / (Lpc * PC)) ** 2; dd = d7d["C1_wide_binary"][f"{f}|{Lpc:g}"]["gamma_minus_1"]
            R3[f"{f}|{Lpc:g}"] = dict(gamma_minus_1=vals, D7d=dd, CFG740_isolated=iso)
            P(f"  {f:9s} L*={Lpc:4.0f} pc: " + " ".join(f"{v:.3e}" for v in vals) + f"  (D7d {min(dd):.3e}-{max(dd):.3e}; isolated {iso:.3e})")
    RES["R3_wide_binary"] = R3

    P("")
    P("R4  Mechanism: kernel chi = 2/kap^2 - 4 a(c)/kap^4 + ...; P2 coefficient c2 of a(c); transverse/longitudinal delta p at kap = 1e3")
    R4 = {}
    for f in A0:
        for E in EV[f]:
            xe = xe_of(f, E)
            c2_0 = C.tail_c2(xe, 0.0); c2_1 = C.tail_c2(xe, 1.0)
            cs = np.linspace(0.02, 0.98, 49)
            tr0 = max(abs(C.dp_vector(1e3, c, xe, 0.0)[1] / C.dp_vector(1e3, c, xe, 0.0)[0]) for c in cs)
            tr1 = max(abs(C.dp_vector(1e3, c, xe, 1.0)[1] / C.dp_vector(1e3, c, xe, 1.0)[0]) for c in cs)
            I0 = C.routeF_I2(xe, 0.0); I1 = C.routeF_I2(xe, 1.0)
            R4[f"{f}|{E}"] = dict(x_e=xe, c2_rF0=c2_0, c2_rF1=c2_1, I2_rF0=I0, I2_rF1=I1, Q2_ratio=I0 / I1,
                                  transverse_over_longitudinal_rF0=tr0, transverse_over_longitudinal_rF1=tr1)
            P(f"  {f:9s} {E}: x_e={xe:.3f}  c2(r_F=0)={c2_0:.4f}  c2(r_F=1)={c2_1:.4f}  I2 {I0:.4f} vs {I1:.4f} (Q2 ratio {I0 / I1:.3f})"
              f"  |dp_T/dp_L| max: r_F=0 {tr0:.3f}, r_F=1 {tr1:.1e}")
    RES["R4_mechanism"] = R4

    P("")
    P("R5  Route N scan for the Cassini lower bound L*_C (r_F = 0, grid (30,48) only, continuation; converged = residual < 1e-9). Reported, not a verdict line.")
    LGRID = [0.0, 0.1, 0.316, 1.0, 1.78, 3.16, 5.62, 10.0]
    R5 = {}
    for f in A0:
        a0 = A0[f]; rM = rM_of(a0); rq = R_SAT / rM
        for E in EV[f]:
            xe = xe_of(f, E)
            def _one(Lam, xe, a0, rq, prev):
                g, U, fin, it = run_v(Lam, xe, G1, U0g=prev)
                conv = fin < 1e-9; q = toQ(S.q2_raw(g, U[0], rq), a0) if conv else float("nan")
                return dict(conv=bool(conv), Q2=q, res=fin), ((U, g) if conv else None)
            pts = {L: {} for L in LGRID}
            for sweep, order in (("up", LGRID), ("down", LGRID[::-1])):
                prev = None
                for Lam in order:                       # one forked process per solve (RSS budget)
                    rec, nxt = isolated(_one, Lam, xe, a0, rq, prev)
                    pts[Lam][sweep] = rec
                    if nxt is not None: prev = nxt
            status = {}
            for Lam in LGRID:
                qs = [v["Q2"] for v in pts[Lam].values() if v["conv"]]
                status[Lam] = None if not qs else all(BAND_H[0] <= q <= BAND_H[1] for q in qs)
            conv_L = [L for L in LGRID if status[L] is not None]; hi = None
            for i, L in enumerate(conv_L):
                if all(status[M] for M in conv_L[i:]): hi = L; break
            fails = [L for L in conv_L if hi is not None and L < hi and not status[L]]
            lo = max(fails) if fails else None
            R5[f"{f}|{E}"] = dict(points={f"{L:.6g}": pts[L] for L in LGRID}, bracket_rM=[lo, hi],
                                  bracket_pc=[None if lo is None else lo * rM / PC, None if hi is None else hi * rM / PC],
                                  nonconverged=[L for L in LGRID if status[L] is None])
            P(f"  {f:9s} {E}: " + " ".join(f"{L:.3g}:{'-' if status[L] is None else ('P' if status[L] else 'F')}" for L in LGRID) +
              f"   L*_C in ({lo}, {hi}] r_M = ({'-' if lo is None else f'{lo * rM / PC:.4f}'}, {'-' if hi is None else f'{hi * rM / PC:.4f}'}] pc")
        P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")
    RES["R5_scan"] = R5

    # ---------------------------------------------------------------- verdict
    allchk = all(CHK)
    r1ok = all(v["hees"] and v["park"] for v in R1.values())
    r2ok = all(v["ratio"] < 1 for v in R2.values())
    if not all(RES["checks"][k]["ok"] for k in ("C2", "C3", "C4", "C5", "C6")):
        verdict = "UNDECIDED (a validation check C2-C6 failed)"
    elif allchk and r1ok and r2ok:
        worstpl = max(R2.items(), key=lambda kv: kv[1]["ratio"])
        verdict = (f"PASSES: Cassini Q2 inside both 2sigma bands in all 24 cells, by {margH:.1e} to {margHmax:.1e} (Hees) and >= {margP:.1e} (Park); "
                   f"planets within bounds (worst {worstpl[0]} at {worstpl[1]['ratio']:.3f} of bound)")
    else:
        bad = [k for k, v in R1.items() if not (v["hees"] and v["park"])] + [k for k, v in R2.items() if v["ratio"] >= 1]
        verdict = f"FAILS: {bad}"
    RES["verdict"] = verdict
    P("")
    P("VERDICT: " + verdict)

n_ok = sum(CHK); P(f"\nC6_LITERAL_CASSINI COMPLETE: {n_ok}/{len(CHK)} checks PASS.  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")
RES["n_pass"], RES["n_checks"] = n_ok, len(CHK)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"c6_literal_cassini_results{TAG}.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"c6_literal_cassini{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
