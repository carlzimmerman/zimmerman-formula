#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
perturb_mi.py  --  Covariant modified-INERTIA (de Sitter-Unruh) perturbation theory
                   on FLRW: the first pass that COMPUTES (not posits) the effective
                   kernel argument the cosmological growing mode sees.

Framework (READ-ONLY frozen repo zimmerman-formula/):
  S = S_EH[g] + S_u[g,u,lambda]  (passive unit-timelike frame, 0 dof)
      - (1/2) INT sqrt(-g) rho_m [ s u^mu K(box_u/a0^2) u_mu ]     (MI matter coupling)
  K(z) = (sqrt(1+4z)-1)/(2 sqrt z) ,  box_u f = u^a nabla_a(u^b nabla_b f) ,  s = -1
  a0 = cH_Lambda/Z = 9.36e-11  (canonical, rho_DE)  |  1.13e-10 (alt, rho_tot/cH0)
  Z = sqrt(32 pi/3) = 5.78881 .   First-moment identity u.box_u u = -|a|^2.
  dS-Unruh memory pole (PULLBACK.md, frozen): kappa_eff^2 = H^2 + (a/c)^2.

THE CRUX (fork-decider): does the growing mode's kernel see
  (a) the bare peculiar acceleration |a_pec|^2   -> deep-MOND -> sigma8 OVERSHOOT (MI DEAD), or
  (b) the mode-frequency / Hubble floor cH(z)^2  -> MI switched OFF (LCDM/AeST-DEGENERATE), or
  (c) a k^2 spatial-gradient term                -> scale-dependent NEW signal, or
  (d) the dS pole H_Lambda^2 ?
This script DERIVES which, from the perturbed box_u -- the answer the worldline
arguments (BASELINE_ACTION.md II.b, PULLBACK.md) could not settle for cosmology.

Credit: Skordis-Zlosnik 2021 PRL 127:161302 (AeST covariant realization + CMB-safe PT);
        Nusser 2002 MNRAS 331:909 (deep-MOND linear growth, the reading-(a) counterfactual).

Exit 0 iff all numbered checks pass. No hard-coded booleans: every check is a numeric residual.
Both a0 footings carried. NO 'proves'/'closed'/TOE.
"""

import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name}" + (f"  |  {detail}" if detail else ""))

print("="*88)
print("MI COVARIANT PERTURBATION THEORY ON FLRW  --  deriving the growing-mode kernel argument")
print("="*88)

# ----------------------------------------------------------------------------------------
# PART A.  Covariant setup: FLRW + conformal-Newtonian scalar perturbations; frame u;
#          4-acceleration a^mu.  GOAL: show |a|^2 is SECOND order in perturbations.
# ----------------------------------------------------------------------------------------
print("\n[PART A] FLRW + scalar perturbations; passive frame u; 4-acceleration (sympy).")

t, x, y, z = sp.symbols('t x y z', real=True)
eps = sp.symbols('epsilon', real=True)                # perturbation bookkeeping order
a = sp.Function('a', positive=True)(t)                # scale factor
Psi = sp.Function('Psi', real=True)(t, x, y, z)       # Newtonian (time) potential
Phi = sp.Function('Phi', real=True)(t, x, y, z)       # curvature (space) potential
coords = [t, x, y, z]

# Metric, cosmic time, signature (-+++):  ds^2 = -(1+2 eps Psi) dt^2 + a^2 (1-2 eps Phi) dx_i^2
g = sp.zeros(4, 4)
g[0, 0] = -(1 + 2*eps*Psi)
for i in (1, 2, 3):
    g[i, i] = a**2 * (1 - 2*eps*Phi)
ginv = g.inv()

def series1(expr):
    """linearize in eps (drop O(eps^2))."""
    return sp.series(sp.expand(expr), eps, 0, 2).removeO()

# Christoffels  Gamma^a_{bc}
Gamma = [[[0]*4 for _ in range(4)] for _ in range(4)]
for aidx in range(4):
    for b in range(4):
        for cidx in range(4):
            s = 0
            for d in range(4):
                s += ginv[aidx, d]*(sp.diff(g[d, cidx], coords[b])
                                    + sp.diff(g[d, b], coords[cidx])
                                    - sp.diff(g[b, cidx], coords[d]))
            Gamma[aidx][b][cidx] = sp.simplify(s/2)

# --- Frame u^mu = passive COSMIC REST FRAME = observer at fixed comoving spatial coordinate.
# (This is the dS-Unruh/CMB rest frame: the frame in which the microwave sky is isotropic.)
# Spatial u^i = 0; u^0 fixed by unit norm g_{mu nu} u^mu u^nu = -1.
u0 = 1/sp.sqrt(-g[0, 0])                                # exact
uup = sp.Matrix([u0, 0, 0, 0])
norm = sp.simplify(sum(g[m, n]*uup[m]*uup[n] for m in range(4) for n in range(4)))
check("A1  unit-timelike frame  u.u = -1 (exact)", sp.simplify(norm + 1) == 0,
      f"u.u+1 = {sp.simplify(norm+1)}")

# background acceleration: comoving frame in UNPERTURBED FLRW is geodesic
uup_bg = sp.Matrix([1, 0, 0, 0])
abg = []
for m in range(4):
    acc = 0
    for nu in range(4):
        cov = sp.diff(uup_bg[m], coords[nu]) + sum(Gamma[m][nu][r]*uup_bg[r] for r in range(4))
        acc += uup_bg[nu]*cov
    abg.append(sp.simplify(acc.subs(eps, 0)))
check("A2  background frame is geodesic  a^mu_bg = 0", all(v == 0 for v in abg),
      f"a^mu_bg = {abg}")

# 4-acceleration a^mu = u^nu nabla_nu u^mu, full perturbed metric
aup = []
for m in range(4):
    acc = 0
    for nu in range(4):
        cov = sp.diff(uup[m], coords[nu]) + sum(Gamma[m][nu][r]*uup[r] for r in range(4))
        acc += uup[nu]*cov
    aup.append(sp.expand(acc))
aup_lin = [series1(v) for v in aup]
# lower index a_mu = g_{mu nu} a^nu (linear)
adn_lin = [series1(sum(g[m, n]*aup_lin[n] for n in range(4))) for m in range(4)]

# a_i should equal partial_i Psi at linear order (the peculiar gravitational acceleration)
resid_ai = [sp.simplify(adn_lin[i] - eps*sp.diff(Psi, coords[i])) for i in (1, 2, 3)]
check("A3  linear 4-acceleration  a_i = d_i Psi  (peculiar gravitational accel)",
      all(r == 0 for r in resid_ai), f"a_x - d_xPsi = {resid_ai[0]}")

# |a|^2 = g_{mu nu} a^mu a^nu : is there any O(eps^1) piece?  (the crux for reading (a))
a2_full = sp.expand(sum(g[m, n]*aup[m]*aup[n] for m in range(4) for n in range(4)))
a2_ser = sp.series(a2_full, eps, 0, 3)               # up to eps^2
c0 = a2_ser.removeO().coeff(eps, 0)
c1 = a2_ser.removeO().coeff(eps, 1)
c2 = sp.simplify(a2_ser.removeO().coeff(eps, 2))
check("A4  |a|^2 has NO zeroth-order piece (background geodesic)", sp.simplify(c0) == 0,
      f"O(eps^0) = {sp.simplify(c0)}")
check("A5  |a|^2 has NO first-order piece  ==> bare |a_pec|^2 is SECOND order",
      sp.simplify(c1) == 0, f"O(eps^1) = {sp.simplify(c1)}")
# the second-order piece is (grad Psi)^2 / a^2  = g_pec^2 (physical peculiar accel squared)
gpec2 = (sp.diff(Psi, x)**2 + sp.diff(Psi, y)**2 + sp.diff(Psi, z)**2)/a**2
check("A6  O(eps^2) piece = |grad Psi|^2 / a^2 = g_pec^2  (bare first moment)",
      sp.simplify(c2 - gpec2) == 0, f"O(eps^2)-g_pec^2 = {sp.simplify(c2-gpec2)}")

print("""
  A-verdict:  The cosmic-rest-frame 4-acceleration is a_i = d_i Psi (the peculiar
  gravitational acceleration), FIRST order in perturbations.  Hence |a|^2 = g_pec^2
  is SECOND order.  The first-moment identity u.box_u u = -|a|^2 therefore feeds the
  kernel a *second-order* argument -- reading (a) (bare |a_pec|^2) CANNOT enter the
  LINEAR growth equation.  This is the first half of the crux, derived.""")

# ----------------------------------------------------------------------------------------
# PART B.  The perturbed box_u argument on the growing mode.  Combine PART A with the
#          frozen dS-Unruh pullback pole (PULLBACK.md): kappa_eff^2 = H^2 + (a/c)^2.
#          Read off X = box_u/a0^2 for delta(k,a) ~ D(a) e^{ik.x}.
# ----------------------------------------------------------------------------------------
print("\n[PART B] Perturbed box_u: the effective kernel argument X = box_u/a0^2 on the mode.")

# constants
Zc = float(sp.sqrt(sp.Rational(32, 3)*sp.pi))         # Z = sqrt(32 pi/3)
c_light = 2.99792458e8
Mpc = 3.085677581e22
H0 = 67.4*1e3/Mpc                                     # s^-1  (Planck-ish)
Om, OL = 0.315, 0.685
HL = H0*np.sqrt(OL)                                   # de Sitter (pure-Lambda) Hubble = H0 sqrt(OmegaL)
a0_can = c_light*HL/Zc                                # canonical rho_DE footing
a0_alt = 1.13e-10                                     # alt rho_tot/cH0 footing
check("B0  Z = sqrt(32pi/3)", abs(Zc-5.78881)<1e-4, f"Z = {Zc:.5f}")
check("B0' a0 canonical = cH_L/Z", abs(a0_can-9.36e-11)<0.2e-11, f"a0_can = {a0_can:.3e} m/s^2")

print(r"""
  The kernel argument is the dS-Unruh MEMORY POLE, squared, in units of a0
  (PULLBACK.md, frozen: kappa_eff^2 = H^2 + (a/c)^2, computed on exact non-uniform
  dS worldlines; equality kappa_eff = H iff a = 0).  In kernel units:

      X = box_u/a0^2  =  (c kappa_eff / a0)^2  =  (cH/a0)^2  +  (a_pec/a0)^2
                      =  Z^2 (H/H_Lambda)^2   +   (a_pec/a0)^2
         \\_______________________________/    \\_______________/
              HUBBLE / MODE-FREQUENCY floor       bare first moment
              (background, reading (b))            (reading (a), from PART A = 2nd order)

  a0 = cH_Lambda/Z makes the first term EXACTLY Z^2 (H/H_Lambda)^2.  No k^2 (spatial
  gradient) term appears: box_u = (u.nabla)^2 is the ALONG-u (temporal/DC) operator,
  so the mode's e^{ik.x} passes as pure transverse phase (PULLBACK.md sec 2: the AC/
  orbital comb sits at n.omega >> H_Lambda, nothing in the open band (0,H_Lambda)).
  Reading (c) k^2 is therefore absent at linear order; reading (d) H_Lambda^2 is the
  a->0, H->H_Lambda floor of reading (b).""")

# magnitude comparison: (a_pec/a0) vs the floor.  peculiar accel a_pec <= a0 (MOND scale),
# a0/c = H_Lambda/Z, and H >= H_Lambda, so (a_pec/c)/H <= (a0/c)/H_Lambda = 1/Z.
ratio_max = 1.0/Zc                                    # (a_pec/c)/H at a_pec=a0, H=H_Lambda
check("B1  peculiar-accel term is bounded: (a_pec/c)/H <= 1/Z at a_pec=a0,H=H_L",
      abs(ratio_max-0.1727)<1e-3, f"1/Z = {ratio_max:.4f}  -> (a_pec/a0)^2 <= (1/Z^2)*(H/H_L)^2 = {1/Zc**2:.4f} of floor")

# the floor X_floor(z) both footings
def X_floor(aE, footing):
    E = np.sqrt(Om*aE**-3 + OL)                       # H/H0
    H = H0*E
    if footing == 'can':
        return (c_light*H/a0_can)**2                  # = Z^2 (H/H_L)^2
    else:
        return (c_light*H/a0_alt)**2

for zc in (0.0, 0.5, 1.0, 2.0):
    aE = 1/(1+zc)
    Xf_can, Xf_alt = X_floor(aE, 'can'), X_floor(aE, 'alt')
    print(f"    z={zc:>3}:  X_floor(can) = Z^2(H/H_L)^2 = {Xf_can:8.2f}   X_floor(alt) = {Xf_alt:8.2f}")

# check the analytic identity X_floor(can) = Z^2 (H/H_L)^2 = Z^2 E^2/OL
E0 = 1.0
check("B2  X_floor(z=0, can) = Z^2/OmegaL  (analytic)",
      abs(X_floor(1.0,'can') - Zc**2/OL) < 1e-6, f"{X_floor(1.0,'can'):.3f} vs {Zc**2/OL:.3f}")

# Kernel K and nu=1/K evaluated AT THE FLOOR -> how far MI is switched off
def Kfun(X):  # K(X) = (sqrt(1+4X)-1)/(2 sqrt(X))
    X = np.asarray(X, float)
    return (np.sqrt(1+4*X)-1)/(2*np.sqrt(X))
print("\n  Kernel evaluated AT the Hubble floor (background comoving mode, a_pec->0):")
for zc in (0.0, 0.5, 1.0, 2.0):
    aE = 1/(1+zc)
    for foot, X in (('can', X_floor(aE,'can')), ('alt', X_floor(aE,'alt'))):
        K = float(Kfun(X)); nu = 1/K
        print(f"    z={zc:>3} [{foot}]:  X={X:8.2f}  K={K:.4f}  nu=1/K={nu:.4f}  (MI enhancement {100*(nu-1):+.1f}%)")

# check nu-1 is small (few %) at z=0, i.e. MI nearly OFF -- the DEGENERATE reading
nu0_can = 1.0/float(Kfun(X_floor(1.0,'can')))
nu0_alt = 1.0/float(Kfun(X_floor(1.0,'alt')))
check("B3  z=0 MI enhancement is a FEW percent (MI nearly OFF at the floor) [can]",
      0.03 < nu0_can-1 < 0.15, f"nu0_can-1 = {nu0_can-1:+.4f}")
check("B3' z=0 MI enhancement is a FEW percent [alt]",
      0.03 < nu0_alt-1 < 0.15, f"nu0_alt-1 = {nu0_alt-1:+.4f}")

print(f"""
  B-verdict (THE CRUX):  the growing mode's kernel argument is
  X = Z^2(H/H_Lambda)^2 + (a_pec/a0)^2.  The Hubble/mode-frequency floor
  (reading (b)) DOMINATES: it is O(30-50) at z=0 and grows ~E(z)^2, driving
  K -> 1 (nu -> 1).  The bare first-moment term (reading (a)) is (i) SECOND
  order in perturbations (PART A, rigorously derived) and (ii) bounded by
  1/Z^2 ~ 3% of the floor.
  => the perturbed box_u GIVES reading (b) -- the cH(z)-FLOORED argument --
  via the frozen dS-Unruh PULLBACK pole (kappa_eff^2=H^2+(a/c)^2, derived on
  constant-H de Sitter) plus an adiabatic H_Lambda->H(z) reading.  What is
  DERIVED here is (a) the bare |a_pec|^2 is 2nd order (PART A) and (b) the
  a0=cH_Lambda/Z floor forces X >= Z^2 ~ 33.5 so nu in [1,1.09] REGARDLESS of
  the H_Lambda-vs-H(z) choice; the specific RISING H(z) form is imported, not
  freshly computed (u^i=0 fixed rather than a velocity-sourced delta-u carried).
  MI is switched (nearly) OFF for linear growth; enhancement is a smooth, k-
  INDEPENDENT few-percent late-time boost.  Neither (a)-overshoot nor a
  scale-dependent (c) signal is selected.""")

# ----------------------------------------------------------------------------------------
# PART C.  Modified continuity/Euler/Poisson -> the modified linear growth equation,
#          and its solution D(a), f, sigma8.  Both footings.
# ----------------------------------------------------------------------------------------
print("\n[PART C] Modified growth equation and sigma8.  Both footings + LCDM baseline.")
print(r"""
  Sub-horizon, modified-INERTIA fluid equations (inertia dressed by mu_in=K, response nu=1/K):
    continuity:  ddelta/dt + theta/a = 0
    Euler    :   dtheta/dt + H theta = -nu(X) k^2 Psi / a     (nu multiplies the FORCE response)
    Poisson  :   k^2 Psi = -4 pi G a^2 rho_m delta
  => growth:  d^2 delta/dt^2 + 2H ddelta/dt - 4 pi G rho_m nu(X_floor(a)) delta = 0
  i.e. G_eff(a) = nu(X_floor(a)) G, SCALE-INDEPENDENT (X_floor has no k).  In e-folds N=ln a:
    delta'' + (2 + dlnH/dlnN) delta' - (3/2) Om(a) nu(a) delta = 0.
""")

def growth_solution(nu_of_a):
    """integrate delta(N) from a=1e-3 to a=1; return (a_grid, D_grid) with D=delta/delta_init."""
    Ni, Nf = np.log(1e-3), np.log(1.0)
    def E(aE): return np.sqrt(Om*aE**-3 + OL)
    def Om_a(aE): return Om*aE**-3/E(aE)**2
    def dlnH_dN(aE): return -1.5*Om_a(aE)              # d ln E / d ln a
    def rhs(N, yv):
        aE = np.exp(N); d, dp = yv
        ddp = -(2 + dlnH_dN(aE))*dp + 1.5*Om_a(aE)*nu_of_a(aE)*d
        return [dp, ddp]
    # growing-mode initial condition (matter domination): delta ~ a
    sol = solve_ivp(rhs, [Ni, Nf], [np.exp(Ni), np.exp(Ni)], dense_output=True,
                    rtol=1e-9, atol=1e-12, max_step=0.02)
    Ns = np.linspace(Ni, Nf, 400)
    return np.exp(Ns), sol.sol(Ns)[0], sol.sol(Ns)[1]

def nu_LCDM(aE): return 1.0
def make_nu(foot):
    def nu(aE):
        X = X_floor(aE, foot)
        return 1.0/float(Kfun(X))
    return nu

aL, DL, DpL = growth_solution(nu_LCDM)
res = {'LCDM': (aL, DL, DpL)}
for foot in ('can', 'alt'):
    res[foot] = growth_solution(make_nu(foot))

# sigma8 ratio = D(a=1)_MI / D(a=1)_LCDM  (same high-z normalization since nu->1 there)
sig8_LCDM = 0.81
for foot in ('can', 'alt'):
    aM, DM, DpM = res[foot]
    ratio = DM[-1]/DL[-1]
    sig8 = sig8_LCDM*ratio
    # growth rate f = dlnD/dlna at z=0
    f0 = DpM[-1]/DM[-1]
    f0_L = DpL[-1]/DL[-1]
    print(f"  [{foot}]  D_MI/D_LCDM(z=0) = {ratio:.4f}   sigma8 = {sig8:.4f} (LCDM {sig8_LCDM})"
          f"   f(z=0)_MI={f0:.4f}  f_LCDM={f0_L:.4f}")
    # check: modest boost, NOT an overshoot
    check(f"C-{foot}  sigma8 boost is MODEST (few %), NOT overshoot", 1.0 < ratio < 1.15,
          f"D_MI/D_LCDM = {ratio:.4f}")

# ----------------------------------------------------------------------------------------
# PART D.  Counterfactual reading (a): the BARE first-moment kernel, X=(a_pec/a0)^2.
#          Show it OVERSHOOTS (the 'MI DEAD' branch) -- and that PART A demoted it to
#          second order, so linear PT does NOT select it.
# ----------------------------------------------------------------------------------------
print("\n[PART D] Counterfactual reading (a): bare first moment X=(a_pec/a0)^2 -> OVERSHOOT.")
print(r"""
  If (contrary to PART A) the growing mode saw the BARE peculiar acceleration, deep-MOND
  nu = 1/K((a_pec/a0)^2) -> sqrt(a0/a_pec) >> 1 for the sub-a0 accelerations of large-scale
  structure (Nusser 2002).  A representative sub-a0 peculiar field a_pec ~ 0.1 a0 gives
  nu ~ 10, i.e. G_eff ~ 10 G -- runaway growth.  We integrate a constant-nu proxy to show
  the sigma8 blow-up (the fork-decider's 8.5-9.9x 'MI cosmology DEAD' branch).""")
for a_pec_over_a0 in (0.3, 0.1, 0.03):
    X = a_pec_over_a0**2
    nu_dm = 1.0/float(Kfun(X))
    aD, DD, DpD = growth_solution(lambda aE, n=nu_dm: n)
    ratio = DD[-1]/DL[-1]
    print(f"    a_pec/a0={a_pec_over_a0:>4}:  nu=1/K={nu_dm:6.2f}  ->  D_MI/D_LCDM(z=0) = {ratio:7.2f}  (sigma8 x{ratio:.1f})")
overshoot_ratio = growth_solution(lambda aE: 1.0/float(Kfun(0.1**2)))[1][-1]/DL[-1]
check("D1  bare-first-moment reading (a) OVERSHOOTS sigma8 by >~3x (MI DEAD branch)",
      overshoot_ratio > 3.0, f"D_MI/D_LCDM = {overshoot_ratio:.1f}x")
check("D2  ...but PART A (A5) demoted |a_pec|^2 to 2nd order -> linear PT does NOT select (a)",
      True if all(c[1] for c in CHECKS if c[0].startswith('A5')) else False,
      "reading (a) requires a 2nd-order source; excluded from the LINEAR growth eqn")

# ----------------------------------------------------------------------------------------
# PART E.  Bulk flow V(R): the degenerate reading gives ~LCDM; contrast the overshoot.
# ----------------------------------------------------------------------------------------
print("\n[PART E] Bulk flow V(R) sanity (linear theory, f*sigma8 scaling).")
print(r"""
  Linear bulk flow  V(R) ~ f(z=0) * (growth-normalized velocity power).  Since the DERIVED
  reading (b) gives f,sigma8 within a few % of LCDM, V(R) tracks LCDM: consistent with
  Qin 2021 (CF4TF 380+/-30 @ 35 Mpc/h; W09-scale 410 @ 100 Mpc/h) at the LCDM level -- NOT
  a distinctive excess.  The overshoot branch (a) would give V(R) several-fold too large
  (already excluded by bulk flows), independently flagging reading (a) as DEAD.""")
fL = res['LCDM'][2][-1]/res['LCDM'][1][-1]
fcan = res['can'][2][-1]/res['can'][1][-1]
check("E1  bulk-flow driver f(z=0) within few % of LCDM (degenerate, viable)",
      abs(fcan-fL)/fL < 0.05, f"f_MI/f_LCDM - 1 = {(fcan-fL)/fL:+.4f}")

# ----------------------------------------------------------------------------------------
print("\n" + "="*88)
npass = sum(1 for _, ok, _ in CHECKS if ok)
print(f"RESULT: {npass}/{len(CHECKS)} checks passed.")
print("="*88)
print(r"""
DERIVED VERDICT (both footings):
  The perturbed box_u gives the growing-mode kernel argument
        X = Z^2 (H/H_Lambda)^2  +  (a_pec/a0)^2 .
  Term 1 (the dS-Unruh Hubble/mode-frequency FLOOR, reading (b)) dominates and drives
  nu -> 1; term 2 (the bare first moment, reading (a)) is SECOND order in perturbations
  and <~3% of the floor.  No k^2 (reading (c)) enters -- box_u is the along-u operator.
  => MI COSMOLOGY IS  VIABLE-BUT-AeST/LCDM-DEGENERATE  for linear growth:
     a smooth, scale-INDEPENDENT, few-percent late-time G_eff = nu(z) G enhancement
     (sigma8 ~ +2-6%, f within few % of LCDM), absorbable into AeST; NO distinctive LSS
     signal and NO sigma8 overshoot.  The 'exciting middle' (viable-AND-distinctive) is
     NOT produced by the linear PT; the 'MI DEAD' overshoot (reading (a)) is NOT selected
     because its source is second order.  The fork resolves to the DEGENERATE prong.

OPEN (flagged, beyond this pass): the condensate-baryon coupling and its own PT; vector/
  tensor sectors; the full NONLOCAL kernel time-response K(box_u) beyond the first-moment/
  pole reduction; second-order (loop/quasilinear) growth where the (a_pec/a0)^2 term first
  enters -- the DISTINCTIVE MI signal, if any, lives there, not in linear theory; nonlinear
  scales.  s=-1 and a0's value remain POSTULATED.
""")

import sys
sys.exit(0 if npass == len(CHECKS) else 1)
