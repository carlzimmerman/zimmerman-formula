#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG120 script D -- G3 (T3a reciprocity/energy of the pair-potential structure, T3b self-force), G4 (T4 constant count) and G5 (T5: Poisson-operator sign,
hyperbolicity statement, Solar System, ownership statement), written to CFG120_FROZEN_CRITERIA.md (commit e8b9fbcdf).  (T3c, the cosmological Bianchi
check, is in script C because it needs the linear solver.)

Pass lines (frozen): G3 reaction on baryons beyond g_law <= 0.10 g_law and supplied energy <= orbital energy (both r_ta conventions: the supplied energy is
independent of r_ta because the map has no exchange); G4 zero constants beyond kappa and Omega_c h^2 and a0 tied as in CFG43 (inherited as an input);
G5a min_k(1 + Khat) > 0; G5b hyperbolicity/ghost UNDECIDED at this scope (a static instantaneous relation); G5c |g_D(9.5 AU)| <= 1e-13 m/s^2 (declared placeholder;
CFG7's committed Cassini line is a QUADRUPOLE TIDE bound, Q2 = 5.2e-27 s^-2, a different observable: reported POST-HOC beside it, see below).
Kernel used for the N-body and the Solar System: the recalled RM sets (closed forms), the T1g best fits, K* (extended inward with its local power-law slope, declared), and K_M(M_sun).
MUTATE=d : kernel sign flipped: the G5a claim '1 + Khat > 0' must FAIL.  MUTATE=a,b,c: no bite here (declared).
Run: python3 cfg120_D_g3_g4_g5.py    (MUTATE=d for the control)
"""
import os, sys, math, json
import numpy as np
from scipy import special
from scipy.integrate import quad, solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg120_common import *

R = Report("cfg120_D_g3_g4_g5")
P, check = R.P, R.check
R.head(__doc__.split("Run: python3")[0])
if MUTATE in ("a", "b", "c"):
    P(f"\n  MUTATE={MUTATE}: no bite in script D (declared); main claims evaluated unchanged.")
SGN = -1.0 if MUTATE == "d" else 1.0
AU_KPC = 1.495978707e11 / KPC_M
a0 = A0
kern_rec = RM(1.0, 3.0, 0.1)
fitfile = os.path.join(HERE, "cfg120_rmfit_canonical.json")
fit3 = json.load(open(fitfile))["fit3"] if os.path.isfile(fitfile) else fit_rm(a0, MASSES, None, None)
fit2 = json.load(open(fitfile))["fit2"] if os.path.isfile(fitfile) else fit_rm(a0, MASSES, 1.0, None)

# ================================================================================================================ T3a
R.banner("T3a  reciprocity and energy: a linear translation-invariant map is a FIXED two-body law F = G m1 m2 (1 + m(d))/d^2 with a symmetric pair potential")
A_, L_, MU_ = kern_rec.A, kern_rec.lam, kern_rec.mu
Wf = lambda d: kern_rec.m(d) / d + (A_ / L_) * (special.exp1(MU_ * d) + np.exp(-MU_ * d))     # W = K*(1/s) up to nothing (W(inf) = 0)
dv = np.geomspace(0.05, 200.0, 40)
eps = 1e-5
Wp = (Wf(dv * (1 + eps)) - Wf(dv * (1 - eps))) / (2 * dv * eps)
e1 = np.max(np.abs(Wp / (-kern_rec.m(dv) / dv ** 2) - 1))
check("T3a.1 the pair potential W(d) = (K*1/s)(d) has W'(d) = -m(d)/d^2 (analytic W against finite difference), so the pair force is G m1 m2 (1+m(d))/d^2", f"max rel err over d = 0.05-200 kpc: {e1:.2e} (line 1e-6)", e1 < 1e-6)


def force_numeric(d):
    """F_z on a unit test mass at distance d from a point mass with its cloud K, by direct integration over the cloud (no shell theorem)."""
    def inner(s):
        f = lambda mu: (d - s * mu) / (d * d + s * s - 2 * d * s * mu) ** 1.5
        return 2 * math.pi * quad(f, -1, 1, epsabs=0, epsrel=1e-11, limit=200)[0]
    fcl = lambda s: s * s * float(kern_rec.K(s)) * inner(s)
    v = quad(fcl, 1e-9, d, epsabs=0, epsrel=1e-9, limit=400)[0] + quad(fcl, d, 400.0, epsabs=0, epsrel=1e-9, limit=400)[0] + quad(fcl, 400.0, 2e4, epsabs=0, epsrel=1e-9, limit=400)[0]
    return v


e2 = 0.0
for d_ in (0.5, 5.0, 40.0):
    fn = force_numeric(d_)
    fa = float(kern_rec.m(d_)) / d_ ** 2
    # truncation at 2e4 kpc removes only the exterior shells (they exert no force inside); compare
    e2 = max(e2, abs(fn / fa - 1))
check("T3a.2 independent route: the force of the cloud on a test mass by direct 3-D integration over the cloud equals G m(d)/d^2 (shell theorem)", f"max rel err at d = 0.5, 5, 40 kpc: {e2:.2e} (line 1e-4)", e2 < 1e-4)


def accel(pos, m):
    d = pos[:, None, :] - pos[None, :, :]
    r = np.sqrt((d ** 2).sum(-1))
    np.fill_diagonal(r, 1.0)
    fac = G * (1.0 + kern_rec.m(r)) / r ** 3
    np.fill_diagonal(fac, 0.0)
    return -(fac[:, :, None] * d * m[None, :, None]).sum(1)


def energy(pos, vel, m):
    d = pos[:, None, :] - pos[None, :, :]
    r = np.sqrt((d ** 2).sum(-1))
    iu = np.triu_indices(len(m), 1)
    ri = r[iu]
    U = -G * (m[:, None] * m[None, :])[iu] * (1.0 / ri + Wf(ri))
    return 0.5 * (m * (vel ** 2).sum(1)).sum() + U.sum()


def nbody(pos0, vel0, m, T):
    N = len(m)

    def rhs(t, y):
        pos = y[:3 * N].reshape(N, 3)
        vel = y[3 * N:].reshape(N, 3)
        return np.concatenate([vel.ravel(), accel(pos, m).ravel()])
    y0 = np.concatenate([pos0.ravel(), vel0.ravel()])
    sol = solve_ivp(rhs, (0, T), y0, method="DOP853", rtol=1e-12, atol=1e-12, dense_output=True)
    return sol


def gradient_check(pos, m):
    """force from the pair-sum potential energy (numerical gradient) vs the analytic pair force: 'reaction beyond g_law'."""
    N = len(m)
    F = m[:, None] * accel(pos, m)
    Fn = np.zeros_like(F)
    for i in range(N):
        for c in range(3):
            h_ = 1e-6 * max(1.0, abs(pos[i, c]))
            pp, pm = pos.copy(), pos.copy()
            pp[i, c] += h_
            pm[i, c] -= h_
            Fn[i, c] = -(energy(pp, np.zeros_like(pos), m) - energy(pm, np.zeros_like(pos), m)) / (2 * h_)
    return np.max(np.abs(F - Fn)) / np.max(np.abs(F))


# N = 3 hierarchical
m3 = np.array([1e10, 3e9, 1e9])
pos3 = np.array([[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [12.0, 0.0, 0.0]])
vc = lambda M, r: math.sqrt(G * M * (1 + float(kern_rec.m(r))) / r)
vel3 = np.array([[0.0, 0.0, 0.0], [0.0, 0.9 * vc(1e10, 3.0), 0.0], [0.0, 0.9 * vc(1.4e10, 12.0), 0.0]])
vel3[0] = -(m3[1:, None] * vel3[1:]).sum(0) / m3[0]
T3 = 10 * 2 * math.pi * 3.0 / vc(1e10, 3.0)
sol3 = nbody(pos3, vel3, m3, T3)
ts = np.linspace(0, T3, 200)
E3 = np.array([energy(sol3.sol(t)[:9].reshape(3, 3), sol3.sol(t)[9:].reshape(3, 3), m3) for t in ts])
p3 = np.array([(m3[:, None] * sol3.sol(t)[9:].reshape(3, 3)).sum(0) for t in ts])
scale_p = np.sum(m3 * np.linalg.norm(vel3, axis=1))
dE3 = np.max(np.abs(E3 - E3[0])) / abs(E3[0])
dp3 = np.max(np.abs(p3 - p3[0])) / scale_p
gc3 = gradient_check(pos3, m3)
check("T3a.3 N = 3 (hierarchical, 10 inner periods, DOP853 rtol 1e-12): energy (kinetic + pair potentials) conserved to 1e-8 and total momentum to 1e-12", f"|dE/E| = {dE3:.2e}, |dp|/(sum m v) = {dp3:.2e}; force vs -grad(pair-sum energy): {gc3:.2e}", dE3 < 1e-8 and dp3 < 1e-12 and gc3 < 1e-6)
# N = 30
rng = np.random.default_rng(120)
N = 30
while True:
    pts = rng.normal(size=(N, 3))
    pts = pts / np.linalg.norm(pts, axis=1)[:, None] * (8.0 * rng.random(N) ** (1 / 3))[:, None]
    dd = np.linalg.norm(pts[:, None] - pts[None], axis=-1) + 10 * np.eye(N)
    if dd.min() > 0.8:
        break
m30 = 10 ** rng.uniform(9, 10, N)
sig = 0.4 * math.sqrt(G * m30.sum() / 8.0)
vel30 = rng.normal(size=(N, 3)) * sig / math.sqrt(3.0)
vel30 -= (m30[:, None] * vel30).sum(0) / m30.sum()
pos30 = pts - (m30[:, None] * pts).sum(0) / m30.sum()
tc = 8.0 / sig
T30 = 10 * tc * 0.5
sol30 = nbody(pos30, vel30, m30, T30)
ts = np.linspace(0, T30, 120)
E30 = np.array([energy(sol30.sol(t)[:3 * N].reshape(N, 3), sol30.sol(t)[3 * N:].reshape(N, 3), m30) for t in ts])
p30 = np.array([(m30[:, None] * sol30.sol(t)[3 * N:].reshape(N, 3)).sum(0) for t in ts])
dE30 = np.max(np.abs(E30 - E30[0])) / abs(E30[0])
dp30 = np.max(np.abs(p30 - p30[0])) / np.sum(m30 * np.linalg.norm(vel30, axis=1))
gc30 = gradient_check(pos30[:6], m30[:6])
check("T3a.4 N = 30 (random virialised-ish cluster, 10 median half-crossing times): energy conserved to 1e-8 and total momentum to 1e-12", f"|dE/E| = {dE30:.2e}, |dp|/(sum m v) = {dp30:.2e} (T = {T30:.3g} kpc/(km/s), crossing {tc:.3g}); gradient check (6 bodies) {gc30:.2e}", dE30 < 1e-8 and dp30 < 1e-12)
# self-force
mu_nodes, mu_w = np.polynomial.legendre.leggauss(64)
selfF = 0.0
for s in np.geomspace(1e-3, 1e3, 200):
    selfF += float(kern_rec.K(s)) * s ** 2 * (mu_nodes * mu_w).sum() * 2 * math.pi * 1.0 / s ** 2
check("T3b a baryon's own cloud exerts no net force on it (z-component of Int K(|y|) y/|y|^3 d^3y with symmetric quadrature)", f"|F_self| = {abs(selfF):.2e} (line 1e-12)", abs(selfF) < 1e-12)
R.num("T3a", dict(dE3=dE3, dp3=dp3, dE30=dE30, dp30=dp30, gradient_check3=gc3, W_prime_err=e1, force_integral_err=e2))
ok_g3 = dE3 < 1e-8 and dE30 < 1e-8 and gc3 < 1e-6
R.gate("G3 (Reading P, static instantaneous map: reciprocity and energy)", "PASS (by structure)" if ok_g3 else "FAIL", f"reaction beyond g_law: {gc3:.1e} g_law (line 0.10); supplied energy |dE|/E_orbit {max(dE3, dE30):.1e} (line 1), both r_ta conventions (r_ta does not enter: no exchange). This says only that a fixed pair law is reciprocal and conservative; the cosmological Bianchi check T3c is scored in script C")

# ================================================================================================================ T4
R.banner("T4  constants beyond kappa = 1/2 and Omega_c h^2 = 0.12 (a0 tie inherited as an input; the door does not derive a0)")
L_Lam = C_KMS / (0.06736 * math.sqrt(3 * 0.6847))
L_a0 = {f: (C_KMS ** 2) / a for f, a in FOOTINGS.items()}
P(f"  Hubble-scale lengths (the only lengths from G, a0, c, Lambda): c/(H0 sqrt(3 Omega_L)) = {L_Lam:.3e} kpc = {L_Lam / 1e6:.2f} Gpc; c^2/a0 = {L_a0['canonical']:.3e} kpc (canonical), {L_a0['second']:.3e} (second)")
rows = []
for name, Lval in (("c/sqrt(Lambda)-type", L_Lam), ("c^2/a0 canonical", L_a0["canonical"]), ("c^2/a0 second", L_a0["second"])):
    kern = RM(1.0, Lval, 0.0)
    Rmax = max(float(np.max(R_point(kern, rM(M, a0) * XGRID, M, a0))) for M in MASSES)
    Rmin = min(float(np.min(R_point(kern, rM(M, a0) * XGRID, M, a0))) for M in MASSES)
    rows.append((name, Rmin, Rmax))
    P(f"    universal kernel K = 1/(4 pi L s^2) with L = {name} ({Lval:.2e} kpc): zero new constants, R = C_model/C_target over the whole G1 domain in [{Rmin:.2e}, {Rmax:.2e}]")
P("  constant counts:")
P(f"    RM 3-parameter best fit (A, lambda0, mu0) = ({fit3['A']:.3g}, {fit3['lam']:.3g} kpc, {fit3['mu']:.2g}/kpc): 3 new constants (one degenerate: mu0 -> 0, so effectively the single number A/lambda0 = {fit3['A'] / fit3['lam']:.4g}/kpc); residual factor {math.exp(fit3['max_abs_lnR']):.1f}")
P(f"    RM 2-parameter (A = 1) best fit lambda0 = {fit2['lam']:.4g} kpc, mu0 = {fit2['mu']:.2g}/kpc: 2 new constants; recalled sets (lambda0, mu0): 2 new constants")
P("    K* (best universal kernel): a whole tabulated function with breakpoints at r = 0.1 rM(M_i) and 30 rM(M_i) (galactic lengths 0.12-1158 kpc): at least one new galactic length")
P("    K_M / K_Mtot: zero new constants (only a0, G and the baryon mass), but NOT universal (depends on M_b) and NOT linear in rho_b: a postulate of the target (CFG60 class P)")
hub_pass = all(r_[2] >= 0.9 for r_ in rows)
check("T4.1 no kernel is at once universal (fixed constants), free of new constants, and G1-passing: the zero-constant universal (Hubble-scale) kernels give R <= 1e-4 everywhere",
      "; ".join(f"{n}: R in [{lo:.1e}, {hi:.1e}]" for n, lo, hi in rows), max(r_[2] for r_ in rows) < 1e-4)
R.gate("G4 (constants)", "FAIL", "every universal kernel that reaches the galactic scale carries >= 1 new length (RM: 2-3 constants); the zero-constant universal kernels are Hubble-scale and give R <= 1e-6; K_M/K_Mtot have zero new constants but are mass-dependent (not universal, not linear) and postulate the target; a0's tie is inherited, not derived")

# ================================================================================================================ T5
R.banner("T5  well-posedness and the Solar System")
kk = np.geomspace(1e-9, 1e9, 4000)
minv = {}
for name, kern in (("K_M (M = 1e10)", KM(rM(1e10, a0))), ("RM recalled (1,3,0.1)", kern_rec), ("RM best fit (3-param)", RM(fit3["A"], fit3["lam"], fit3["mu"])), ("RM best fit (A=1)", RM(1.0, fit2["lam"], fit2["mu"]))):
    Kh = kern.Khat(kk)
    minv[name] = float(np.min(1.0 + SGN * Kh))
    P(f"    {name:26s}: min_k (1 + {'(-)' if SGN < 0 else ''}Khat) = {minv[name]:.4g}   (Khat range {Kh.min():.3g} .. {Kh.max():.3g})")
check("T5a the Newtonian-limit Poisson operator has 1 + Khat(k) > 0 at every k for every kernel tested (no pole)", f"min over kernels = {min(minv.values()):.4g}", min(minv.values()) > 0)
R.gate("G5a (sign of the Poisson operator)", "PASS" if min(minv.values()) > 0 else "FAIL", f"min_k(1+Khat) = {min(minv.values()):.3g}")
R.gate("G5b (hyperbolicity, ghosts, gradient instability)", "UNDECIDED", "the Newtonian-limit map is a static instantaneous relation, not a dynamical field; the DE12/DE13/XR criteria are undefined at this scope; a covariant (time-nonlocal) completion is not tested")

# Solar System
r_ss = 9.5 * AU_KPC
Msun_ = 1.0
conv = 1e6 / KPC_M                     # (km/s)^2/kpc -> m/s^2


def gD(kern_m_at_r):
    return G * Msun_ * kern_m_at_r / r_ss ** 2 * conv


rows5 = []
for lam0, mu0 in ((3.0, 0.06), (3.0, 0.1), (10.0, 0.06), (10.0, 0.1)):
    kk_ = RM(1.0, lam0, mu0)
    rows5.append((f"RM recalled lambda0={lam0:g}, mu0={mu0:g}", gD(float(kk_.m(r_ss)))))
kf3 = RM(fit3["A"], fit3["lam"], fit3["mu"])
kf2 = RM(1.0, fit2["lam"], fit2["mu"])
rows5.append(("RM best fit 3-param", gD(float(kf3.m(r_ss)))))
rows5.append(("RM best fit 2-param", gD(float(kf2.m(r_ss)))))
Ks, Bs, rs = build_Kstar(a0, MASSES, None)
# declared extrapolation: K*(s) = K*(s0) (s/s0)^n below s0 = first constrained radius 0.12 kpc, n = local log-slope over 0.12-1.2 kpc
s0 = 0.1 * rM(1e9, a0)
n_loc = (math.log(float(Ks.K(10 * s0))) - math.log(float(Ks.K(s0)))) / math.log(10.0)
m_ss = float(4 * math.pi * float(Ks.K(s0)) * s0 ** (-n_loc) * r_ss ** (3 + n_loc) / (3 + n_loc))
rows5.append((f"K* (extended inward, local slope n = {n_loc:.3f})", gD(m_ss)))
kMs = KM(math.sqrt(G * Msun_ / a0))
rows5.append(("K_M(M_sun): the target itself (r_M = %.0f AU)" % (kMs.rM / AU_KPC), gD(float(kMs.m(r_ss)))))
P(f"  Solar System: anomalous acceleration g_D(9.5 AU) from the Sun's phantom cloud, pass line 1e-13 m/s^2 (declared placeholder)")
for n_, g_ in rows5:
    P(f"    {n_:62s}: g_D = {g_:.3e} m/s^2   {'PASS' if abs(g_) <= 1e-13 else 'FAIL'}   ({abs(g_) / 1e-13:.3g} x the line)")
R.num("solar_system", {n: g for n, g in rows5})
rec_fail = all(abs(g) > 1e-13 for n, g in rows5 if n.startswith("RM recalled")) and abs(rows5[-1][1]) > 1e-13
check("T5c (frozen expectation) the recalled Rahvar-Mashhoon sets and K_M(M_sun) exceed 1e-13 m/s^2 at 9.5 AU (fail Cassini); ESTIMATE was ~1e-12 for lambda0 = 3 kpc and a0/2 = 4.7e-11 for K_M",
      "; ".join(f"{n}: {g:.2e}" for n, g in rows5), rec_fail)
# post-hoc tide comparison (label: POST-HOC; different observable)
Q2 = 5.2e-27
def tide_gD(mfun):
    e = 1e-3
    g1 = G * Msun_ * mfun(r_ss * (1 + e)) / (r_ss * (1 + e)) ** 2
    g0 = G * Msun_ * mfun(r_ss * (1 - e)) / (r_ss * (1 - e)) ** 2
    dgdr = (g1 - g0) / (2 * e * r_ss)                # (km/s)^2/kpc^2
    return abs(dgdr) * 1e6 / KPC_M ** 2            # (km/s)^2/kpc^2 -> s^-2


P("\n  POST-HOC (not frozen; different observable): CFG7's committed Cassini line is the quadrupole tide bound 5.2e-27 s^-2.  |d g_D/dr| at 9.5 AU for the same kernels (s^-2):")
mfuncs = [("RM recalled lambda0=3, mu0=0.1", lambda r: float(RM(1.0, 3.0, 0.1).m(r))), ("RM recalled lambda0=10, mu0=0.06", lambda r: float(RM(1.0, 10.0, 0.06).m(r))),
          ("RM best fit 3-param", lambda r: float(kf3.m(r))), ("K_M(M_sun)", lambda r: float(kMs.m(r)))]
for n_, mf in mfuncs:
    P(f"    {n_:36s}: |dg_D/dr| = {tide_gD(mf):.2e} s^-2  ({tide_gD(mf) / Q2:.2g} x 5.2e-27); the central-force gradient is not the same object as a quadrupole tide, so this is indicative only")
cass_pass = [n for n, g in rows5 if abs(g) <= 1e-13]
R.gate("G5c (Solar System, |g_D(9.5 AU)| <= 1e-13 m/s^2)", "FAIL" if (rec_fail) else "MIXED", "fail: " + "; ".join(n for n, g in rows5 if abs(g) > 1e-13) + ("; pass: " + "; ".join(cass_pass) if cass_pass else ""))
# ownership statement (structural, not scored)
Wt = RM(1.0, 3.0, 0.1).total()
P(f"\n  G5d ownership (structural, not scored): the map applies to EVERY baryon (the Sun, unbound gas, the intracluster medium); there is no bound-only switch. With the recalled kernel the cosmic mean dark/baryon ratio is {Wt:.2f} "
  f"(background required {OMEGA_C_OVER_B:.2f}); the unbound web carries a phantom, at odds with CFG4 H4 ('the unbound web carries no phantom'). The door is silent on Gap 1.")
R.gate("G5d (ownership)", "UNDECIDED / structural", "no bound-only switch; every baryon carries a cloud; not a scored pass")
nf = R.write()
sys.exit(1 if nf else 0)
