#!/usr/bin/env python3
"""W2 (a): critical coupling for chiral symmetry breaking (pre-registered A1, A2, A3 in W2_PREREGISTRATION.md).
A1  bare-vertex Landau-gauge ladder bifurcation equation: sympy derivation of lam_c = 1/4 (alpha_c = pi/3) and Nystrom eigenvalues lam_1(L).
A2  positive control (QCD, one-loop alpha_s reaches C_F alpha_s = pi/3 in [0.15, 2] GeV) and the SM scan R = C2 alpha/alpha_c.
A3  twelve hit-tests 'C2_max alpha(X) = alpha_c'.
Run:    python3 w2_a1_ladder_critical.py           (from this directory; exit 0 iff every check passes)  -> writes w2_a1_results.json
MUTATE: python3 w2_a1_ladder_critical.py MUTATE    (kernel term (lam/x) Int_0^x dropped in A1; positive control applied to U(1)_em in A2)
        must exit 1 (exit 3 if the control is broken)  -> writes w2_a1_results_MUTATE.json
"""
import sys
sys.dont_write_bytecode = True
import json, math
import numpy as np
import sympy as sp
import w2_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)

PI = math.pi
res = {}

# ------------------------------------------------------------------ A1
print("== A1 ladder bifurcation equation ==")
s, lam, x = sp.symbols("s lambda x", positive=True)
# power-law ansatz f = x^(-s) in the UV region (y >> 1, where y+1 -> y): f(x) = (lam/x) Int_0^x f dy + lam Int_x^inf f y^-1 dy  ->  differentiate twice:  x^2 f'' + 2x f' + lam f = 0
ftry = x ** (-s)
ode = sp.simplify((x ** 2 * sp.diff(ftry, x, 2) + 2 * x * sp.diff(ftry, x) + lam * ftry) / ftry)
chk("A1a  x^2 f'' + 2 x f' + lam f = 0 gives s(1-s) = lam  (indicial equation)", sp.simplify(ode - (s * (s - 1) * 1 + (-2 * s) + lam) ) == 0 or sp.simplify(sp.expand(ode) - (s ** 2 - s + lam)) == 0, f"(indicial polynomial: {sp.expand(ode)})")
disc = sp.discriminant(s ** 2 - s + lam, s)
chk("A1b  discriminant 1 - 4 lam vanishes at lam = 1/4 only", sp.solve(sp.Eq(disc, 0), lam) == [sp.Rational(1, 4)])
alpha_c_sym = sp.solve(sp.Eq(3 * sp.Symbol("a", positive=True) / (4 * sp.pi), sp.Rational(1, 4)), sp.Symbol("a", positive=True))[0]
chk("A1c  lam = 3 alpha/(4 pi) = 1/4  =>  alpha_c = pi/3", sp.simplify(alpha_c_sym - sp.pi / 3) == 0)

def lam1(Lx, N, t0=-20.0, mutate=False):
    t = np.linspace(t0, Lx, N)
    h = t[1] - t[0]
    w = np.full(N, h); w[0] = w[-1] = h / 2
    y = np.exp(t)
    K = np.zeros((N, N))
    for i in range(N):
        xi = y[i]
        below = (np.arange(N) < i)
        above = (np.arange(N) > i)
        K[i, below] = 0.0 if mutate else (w[below] * (y[below] ** 2 / (y[below] + 1)) / xi)
        K[i, above] = w[above] * y[above] / (y[above] + 1)
        # diagonal: both integrals have integrand f/(x+1) at y = x (with y dy measure = y_i); trapezoid half-weight each
        K[i, i] = w[i] * (y[i] / (y[i] + 1)) * (0.5 if mutate else 1.0)
    ev = np.linalg.eigvals(K)
    mu = max(ev.real)
    return 1.0 / mu

Ls = [10, 20, 40, 80]
lam_vals = {}
for Lx in Ls:
    v = lam1(Lx, 1600 if Lx <= 40 else 2400, mutate=MUT)
    lam_vals[Lx] = v
    print(f"   L = {Lx:3d}: lam_1 = {v:.6f}   lam_1 - 1/4 = {v-0.25:.6f}   (pi/L)^2 = {(PI/Lx)**2:.6f}   ratio = {(v-0.25)/(PI/Lx)**2:.3f}")
v2 = lam1(80, 3200, mutate=MUT)
print(f"   convergence: L = 80 with N = 3200: lam_1 = {v2:.6f} (N = 2400: {lam_vals[80]:.6f})")
chk("A1d  numerics converged (|dlam| < 1e-4 between N = 2400 and 3200 at L = 80)", abs(v2 - lam_vals[80]) < 1e-4)
lc_est = (4 * lam_vals[80] - lam_vals[40]) / 3.0          # Richardson for lam = lam_c + a/L^2
print(f"   Richardson extrapolation lam_c = (4 lam(80) - lam(40))/3 = {lc_est:.6f}  ->  alpha_c = 4 pi lam_c/3 = {4*PI*lc_est/3:.5f}  (pi/3 = {PI/3:.5f})")
ok_ii = all(abs((lam_vals[Lx] - 0.25) / (PI / Lx) ** 2 - 1) <= 0.15 for Lx in (40, 80))
chk("A1e  (ii) lam_1(L) - 1/4 within 15% of (pi/L)^2 at L = 40 and 80 (Miransky scaling, no O(1) shift)", ok_ii)
chk("A1f  (iii) extrapolated lam_c within 2% of 1/4  (alpha_c = pi/3 to 2%)", abs(lc_est / 0.25 - 1) <= 0.02)
res["A1"] = dict(lam1=lam_vals, lam_c_richardson=lc_est, alpha_c=4 * PI * lc_est / 3)

# ------------------------------------------------------------------ A2
print("== A2 positive control (QCD) and SM scan ==")
def alpha_s_oneloop(mu):
    """one-loop alpha_s from m_Z with n_f thresholds at m_b = 4.18, m_c = 1.27 (running DOWN); dalpha^-1/dlnmu = +b0/2pi, b0 = 11 - 2 nf/3."""
    u = 1.0 / L.RGC.ALPHA_S
    mus = L.MZ
    for m, nf in ((4.18, 5), (1.27, 4), (0.0, 3)):
        lo = max(mu, m)
        if lo < mus:
            u -= (11 - 2 * nf / 3) / (2 * PI) * math.log(mus / lo)
            mus = lo
        if mu >= m:
            break
    return 1.0 / u
mus = np.geomspace(0.15, 2.0, 400)
def R_control(mu):
    if MUT:      # MUTATE: apply the control to U(1)_em: R = Q^2 alpha_em/alpha_c with the running em coupling (one loop, toy)
        return (1.0 / (L.ALPHA_INV0 - L.S_oneloop(L.toy_table(1), mu))) / (PI / 3) if mu > 5.1e-4 else 0.0
    return (4 / 3) * alpha_s_oneloop(mu) / (PI / 3)
Rc = np.array([R_control(m) for m in mus])
cross = [m for m, r in zip(mus, Rc) if r >= 1.0]
mu_qcd = min(cross) if False else (max(m for m, r in zip(mus, Rc) if r >= 1.0) if cross else None)
print(f"   control: R = C_F alpha_s/(pi/3) reaches 1 at mu_c = {mu_qcd} GeV (ladder estimate; one-loop running is unreliable there)")
chk("A2a  POSITIVE CONTROL: the ladder criterion fires for the non-abelian SM sector in [0.15, 2] GeV", mu_qcd is not None)
res["A2_control_mu_c_GeV"] = mu_qcd

sol, lp, Rn = L.sm_twoloop_run("A", tmax=math.log(L.XP) + 1e-9)
def A_at(mu):
    return sol.sol(math.log(mu))[:3]
ac = PI / 3
scan = {}
for name, mu in (("MZ", L.MZ), ("1e10", 1e10), ("X_G", L.XG), ("M_P", L.XP)):
    aY, a2, a3 = A_at(mu) if mu <= L.XP else (None,) * 3
    scan[name] = dict(R_Y=(1 / aY) / ac, R_2=0.75 * (1 / a2) / ac, R_3=(4 / 3) * (1 / a3) / ac)
    print(f"   mu = {name:5s}: R_Y(Y=1) = {scan[name]['R_Y']:.4f}   R_SU2 = {scan[name]['R_2']:.4f}   R_SU3 = {scan[name]['R_3']:.4f}   (two loop, alpha_c = pi/3)")
rows1 = L.toy_table(1)
R_em_MP = (1 / (L.ALPHA_INV0 - L.S_oneloop(rows1, L.XP))) / ac
print(f"   QED-only toy at M_P: 1/alpha = {L.ALPHA_INV0 - L.S_oneloop(rows1, L.XP):.3f}, R_em = alpha/alpha_c = {R_em_MP:.4f}")
Rmax_abelian = max(scan["M_P"]["R_Y"], R_em_MP)
chk("A2b  no abelian factor is near-critical (R >= 0.5) at any mu <= M_P (declared expectation)", Rmax_abelian < 0.5, f"(max abelian R at M_P = {Rmax_abelian:.4f})")
# inverse map (reported): scale where each abelian factor would reach R = 1
lnmu_em = L.pole_scale_oneloop(rows1, u0=L.ALPHA_INV0 - 1 / ac)      # 1/alpha = 1/alpha_c
lnmu_Y = math.log(L.MZ) + (L.A_Y_MZ["A"] - 1 / ac) * 2 * PI / L.B_Y
print(f"   INVERSE MAP (reported, not a test): R = 1 reached at mu = 10^{lnmu_em/math.log(10):.2f} GeV (QED-only toy, one loop) and 10^{lnmu_Y/math.log(10):.2f} GeV (U(1)_Y, one loop); M_P = 10^{math.log10(L.XP):.2f}")
res["A2_scan"] = scan; res["A2_R_em_MP"] = R_em_MP; res["A2_scale_R1_log10GeV"] = dict(em_toy=lnmu_em / math.log(10), Y=lnmu_Y / math.log(10))

# ------------------------------------------------------------------ A3
print("== A3 twelve hit-tests: C2_max alpha(X) = alpha_c ==")
variants = []
for Xn in ("M_P", "M_red", "X_S"):
    for acn, acv in (("pi/3", PI / 3), ("0.933667", 0.933667)):
        X = L.SCALES[Xn]
        # QED-only toy (Q=1): 1/alpha_pred(0) = 1/alpha_c + S(X); spread over mass table 1/2
        pr = [1 / acv + L.S_oneloop(L.toy_table(k), X) for k in (1, 2)]
        variants.append(dict(coupling="QED-toy Q=1", X=Xn, alpha_c=acn, pred=pr[0], spread=abs(pr[0] - pr[1]) / L.ALPHA_INV0))
        # U(1)_Y (Y=1) one loop: a_Y(X) = 1/alpha_c; pred a_Y(MZ) = 1/alpha_c + B_Y/2pi ln(X/MZ); 1/alpha_pred(0) = 137.036 + (pred - A_Y(MZ))
        pa = [L.ALPHA_INV0 + (1 / acv + L.B_Y / (2 * PI) * math.log(X / L.MZ)) - L.A_Y_MZ[k] for k in ("A", "B")]
        variants.append(dict(coupling="U(1)_Y Y=1", X=Xn, alpha_c=acn, pred=pa[0], spread=abs(pa[0] - pa[1]) / L.ALPHA_INV0))
assert len(variants) == 12
for v in variants:
    v["miss"] = v["pred"] / L.ALPHA_INV0 - 1
    v["tol"] = max(2 * v["spread"], 0.01)
    v["within_tol"] = abs(v["miss"]) <= v["tol"]
    print(f"   {v['coupling']:13s} X = {v['X']:6s} alpha_c = {v['alpha_c']:9s}: 1/alpha_pred(0) = {v['pred']:9.3f}  miss = {v['miss']:+.4f}  tol = {v['tol']:.4f}  within tol: {v['within_tol']}")
chk("A3a  twelve variants scored", len(variants) == 12)
chk("A3b  no variant lies within its tolerance (declared expectation: all miss by > 20%)", not any(v["within_tol"] for v in variants) and min(abs(v["miss"]) for v in variants) > 0.20, f"(smallest |miss| = {min(abs(v['miss']) for v in variants):.4f})")
res["A3"] = variants
json.dump(res, open("w2_a1_results_MUTATE.json" if MUT else "w2_a1_results.json", "w") , indent=1, default=float)
L.finish(fails, MUT, "w2_a1")
