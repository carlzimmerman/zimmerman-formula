#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG72 -- does relaxing CFG70's three restrictions (time-kernel only, point-mass baryons, stability untested) change its verdict on the enclosed-mass exchange?

FROZEN QUESTION (verbatim, declared before the first run):
 'Does relaxing CFG70's three restrictions change its verdict? (Q1) With a retarded kernel supported inside the past light cone in SPACE and time
  (a 1+1 radial or a spherical-shell model with speed c), does the late-time reaction on the baryons at x = r/r_M in [0.3, 30] still equal CFG48's
  G4 (pass line 0.10 g_law) for M_b = 1e9, 1e10, 1e12 Msun, and does the energy budget (P2) change from CFG70's kernel-independent value?
  (Q2) With EXTENDED baryons (an exponential sphere as CFG44's exp_sphere, scale h chosen as CFG44 did; also the Freeman disc reading if CFG44 provides
  it) rather than a point mass, do the reaction and energy figures change by more than a factor 2 at any x? (Q3) Is the coupled fluid+baryon+exchange
  operator STABLE (no negative-norm mode, no gradient instability, hyperbolic: compute the linearised operator about the static target on a radial
  grid, its principal symbol and its spectrum, for the r = 1 closed action and for CFG70's open class r = 0 with eps_c = 1)?'
PASS LINES (declared):  P1 reaction <= 0.10 g_law for all x in [0.3, 30];  P2 energy <= (1/2) M_b V_f^2 in BOTH r_ta conventions (CFG48's and B's committed
  CFG4 r_ta_law);  P3 retarded in space AND time (advanced / spacelike dependence 0 on the discrete action) and reciprocal;  P4 stable (all eigenvalues
  real / no growing mode; no ghost).  Each of Q1-Q3 is classified CHANGES THE VERDICT / DOES NOT CHANGE IT (rules below).

INHERITED (read-only): CFG48 G4 (target theta^T = (3 a0/4) M_b(<r) pressure-slaved, (3/2) 4 pi r^2 rho_c sigma^2 sigma-slaved, reaction a = r_led theta^T_M),
 CFG70 (SK cross term, a/theta^T_M = r Theta_K + eps_c (Thetabar * mdot), F = r theta + (c/2)(theta - theta^T)^2, K1 = Newton kernel; committed results JSON).
 theta = fluid heat per unit radius; r_led in {0,1} the ledger fraction (r_led = 1 closed, 0 open); eps_c = c_f theta^T_full; theta^T_M = d theta^T / d M_b at the probe.

THE MODEL (declared: 'GS', a Gauss-law scalar mediator, 1+1 radial half-line r >= 0, characteristic speed c).
 CFG70's cross term was instantaneous in space.  A causal completion with light-cone support needs a MEDIATOR (a local hyperbolic field), because a nonlocal
 time-kernel action has no unique retarded reading.  Choose a scalar phi(r,t) with the enclosed mass as its Gauss law:  E = -d_r phi, Neumann/Gauss at r = 0,
 static limit E(r) = (g_b/N) M_b(<r).  Doubled fields phi_pm = phi_S +- phi_D/2 etc. (Galley type; physical limit D = 0):
   S = int dt { (m/2)(qdot_+^2 - qdot_-^2) - m[Phi(q_+) - Phi(q_-)] }
     + int dr dt { (N/2)[ (phi_{+,t}^2 - phi_{-,t}^2)/c_m^2 - (phi_{+,r}^2 - phi_{-,r}^2) ] + g_b [ rho(r;q_+) phi_+ - rho(r;q_-) phi_- ]
                   - [ F(theta_+, E_+) - F(theta_-, E_-) ] - theta_D (Gamma * thetadot_S) }
   F(theta, E) = r_led theta + (c_f/2)(theta - vt E)^2,      vt = vartheta' the fluid-to-mediator coupling,  E = -d_r phi.
 Physical (D = 0) equations (sympy, S1):  N (phi_tt/c_m^2 - phi_rr) = g_b rho + d_r( c_f vt eps ),  eps = theta - vt E;  r_led + c_f eps + Gamma*thetadot = 0;
   m qddot = -m Phi' + g_b d_q(phi at q)  (the baryon feels the mediator at its own position).   Retarded by construction (finite characteristic speed).
 Target identification: theta^T = vt E^(b) = vartheta M_b(<r) with vartheta = vt g_b / N = 3 a0/4 (pressure-slaved; the sigma reading is the same vertex with a
 nonlinear target).  Two dimensionless couplings appear, which the action leaves FREE (flagged NEW, untied):  lam = vt/g_b (mediator fluid-to-baryon strength,
 lam_t = lam/M_b) and beta = c_f vt^2/N = eps_c lam_t (mediator back-reaction).  Derived consequences to be verified: characteristic speed^2 = c_m^2 (1+beta) (declared
 to equal c^2, i.e. the BARE speed is c_m = c/sqrt(1+beta)); the fluid enters the static enclosed field only through the offset (theta = vartheta M - (1+beta) r_led/c_f);
 the reaction on a baryon is F/vartheta = r_led - 1/lam_t  (the -1/lam_t is the mediator's own baryon-baryon force);  contamination delta = lam_t r_led and relative
 baryon-baryon force f_bb = 1/(lam_t r_led):  delta * f_bb = 1  (a structural trade-off of this completion, not an added knob).

READINGS AND PROFILES (declared).  Pressure-slaved (linear; theta^T = vartheta M_b(<r)), sigma-slaved (theta^T_M = (3/8) a0 (2 g_N + a0)/(g_N + a0), g_N = G M_b(<u)/u^2,
 = G4's (3/8) a0 (2+x^2)/(1+x^2) for a point mass), and for extended baryons also the CFG44 exact hydrostatic reading 'hyd' (theta^T = vartheta M_b(<r) + 3 pi a0 r^2 Sigma_out(r);
 STATIC value only: no retarded completion is built).  Extended profiles: CFG44's exp_sphere with h = 2.0 kpc (the value CFG44 B1 uses for its exp. sphere at every mass),
 CFG44's freeman_disc with h = 3.0 kpc (B1's value; the helper's monotone envelope saturates at 1.20 M_b, an artefact of its running maximum, used AS IS and flagged),
 and, declared here as the self-similar family, h = 0.5 r_M(M_b) for both.  x = r/r_M(M_tot).  g_law for extended baryons = sqrt(g_N^2 + a0 g_N), g_N = G M_b(<u)/u^2 (P2 kernel).

Q3 MODEL (declared; a Lagrangian shell gas, cfg72_stability.py):  spherical cold fluid, gamma = 5/3, self-gravity in the conservative shell form, fixed central point mass M_b, inner
 wall pinned at r_in = 0.05 r_M, outer edge r_out = 0.4 r_ta (CFG48) held at the target pressure P_ext = a0 M_b/(8 pi r_out^2); static state = the exact DISCRETE equilibrium (node
 force balance solved from the edge, discretisation error vs the CFG44 target printed); heat bath dU/dt = -P dV/dt + (U^T - U)/tau, K1 (CFG70's Newton kernel), tau = gamma_diss/c_f the
 fluid's own relaxation time.  Reading P: Eulerian pressure target P^T(r) = a0 M/(8 pi r^2) at the cell's CURRENT centre (state-independent pressure: CFG44 B2's ill-posed structure,
 regularised by tau).  Reading S: temperature bath, target specific energy fixed by the position (G4's sigma-slaved with fixed shell mass).  ASSUMPTION A_fluid: the exchange free energy F
 depends on the Eulerian site heat and the BARYONS only, so it exerts no force on fluid shells; this is exact for reading P with a point mass (theta^T is constant in r) and an approximation
 for reading S in the closed class (the derived force -r_led d theta^T/dr is omitted).  Closed (r_led = 1, eps_c = 100) and open (r_led = 0, eps_c = 1) differ only in the probe/mediator sector
 (S3 of this file); the fluid+bath operator depends on tau only.  tau list (declared, no scan): r_e/c, 0.01, 0.1, 1 Gyr, t_dyn(r_e), 10 Gyr and inf (ideal control), with M_b = 1e10 (1e9, 1e12 reported).
 Grids N = 60 and 120 nodes (log-spaced).  The dissipative half-line operator of GS is analysed by its Fourier symbol.

CHECKS AND PASS LINES (frozen here, before the first run)
 S1 (sympy)  D1 the doubled GS action's Delta-variations at Delta = 0 give exactly the phi, theta equations above (residual 0); D2 Sigma-equations vanish at Delta = 0; D3 the static
       structure (E, theta_static, reaction F/vartheta = r_led - 1/lam_t, contamination, delta*f_bb = 1); D4 quasi-static retardation: E = E_qs + w with
       N(w_tt/c_m^2 - w_rr) = -(g_b M_tt + S_tt)/c_m^2 (the retardation correction is SECOND order in 1/c); D5 principal symbol: eigenvalues {0, +-c_m sqrt(1+beta)} (hyperbolic);
       D6 G4's closed forms, extended: (3/4) a0, (3/8) a0 (2 g_N + a0)/(g_N + a0), and the hyd reaction (2/3)(3/4) a0 = a0/2 by finite difference of the discretised functional (2e-3).
 S2 (discrete SK action on the LIGHT-CONE LATTICE, c_eff dt = dr, 5 x 5 sites, doubled fields phi, theta (on links), q, CIC baryon vertex, retarded time memory on theta, fixed test values):
       C1 CAUSALITY (residual stencil, CFG70's measure extended to space): the EL residual at an update point (i_u, j_u) has no dependence on data outside the closed past cone widened by the
          vertex stencil (|dj| <= (i_u - i') + 1): c_adv < 1e-12.   C1r (response support, the real test): the inverse of the linearised residual map (the discrete retarded Green function)
          has support only in the future cone widened by 1: c_resp < 1e-12.   C2 (context, load-bearing): the same wave operator with the instantaneous (elliptic) space term has c_resp > 1e-4.
       R1 RECIPROCITY: (i) the mixed blocks dR^theta/dphi = (dR^phi/dtheta)^T and dR^q/dphi = (dR^phi/dq)^T to 1e-12; (ii) independently hand-coded residuals equal the action's to 1e-12.
 S3 (Q1 numerics)  N1 CONTROL: the reaction in the light-cone width -> 0 limit (beta = 0, chi = R_f/(c t_f) -> 0, point mass) equals CFG70's committed late-time reaction (results JSON) to 1e-6, both slavings, and
          the quasi-static reduction of GS is CFG70's closed form with eps_c -> eps_c/(1+beta), tau -> (1+beta) tau (to 1e-3); N2 the coupled wave+fluid+probe simulation (staggered leapfrog, J = 100 sites, R_f = 1,
          t_f = 1, c_eff = R_f/(chi t_f), K1 kernel tau = 0.1 t_f, beta = 1, closed (r_led=1, eps_c=100) and open (r_led=0, eps_c=1)) at chi in {0.5, 0.05, 0.005}: late-time reaction = r_led (1e-6); the peak/transient
          deviation from the chi -> 0 solution is measured and extrapolated to chi_phys = R_f/(c t_f) (an EXTRAPOLATION, declared, not a solve); N3 the late-time reaction/g_law table, x in {0.3,1,3,10,30},
          M_b = 1e9,1e10,1e12, point / exp_sphere / freeman, all readings, and the x at which 0.10 is crossed; N4 (extended baryons in the simulation, M_b = 1e10, exp sphere) same late-time limit.
 S4 (P2)  E1 E_c/((1/2) M_b V_f^2) by quadrature (closed form 1.5 x_e for the point mass) in CFG48's r_ta and B's committed r_ta, point vs extended (enc and hyd), control vs CFG70's JSON (1e-6);
       E2 the energy delivered by the GS memory law = f_real E_c with f_real = 1 - (1+beta) r_led/eps_c (simulation), kernel- and speed-independent.
 S5 (Q3)  T0 control: the discrete equilibrium is a fixed point (|f| < 1e-9 relative) and the ideal (tau = inf) operator has NO growing mode: max Re lambda <= 1e-8 max|lambda| (MUTATE c must fail this);
       T1 hydrostatic discretisation error (reported); T2 the principal symbol of the fluid+bath system (sympy) has real eigenvalues {0, +-c_s} (hyperbolic), relaxation only zeroth order;
       T3 the Fourier symbol of the GS half-line dissipative operator: max Re lambda <= 1e-8 max|lambda| over k, the energy Hessian positive (no ghost); MUTATE c flips N and must fail;
       T4 (reported, classification) spectra at the tau list, readings P and S, N = 60 and 120: max Re lambda in 1/Gyr, growth rate vs tau, convergence of the growth rate between N = 60 and 120.
CLASSIFICATION RULES (declared).  Q1 DOES NOT CHANGE iff the late-time reaction equals G4's/CFG70's to 1e-6 for every kernel speed simulated AND the P2 ratios equal CFG70's to 1e-6 AND P1 stays FAIL.
 Q2 CHANGES THE FIGURES iff the extended/point ratio of reaction/g_law or of the energy ratio leaves [1/2, 2] at some x or mass; it CHANGES THE VERDICT iff P1 or P2 flips to PASS in some reading.
 Q3 CHANGES THE VERDICT iff the operator has a growing mode (max Re lambda > 1e-8 max|lambda| of that operator, converged between N = 60 and 120) in a reading/tau CFG70's passing cells use, or a ghost.
MUTATE controls (each must exit rc = 1):  MUTATE=a: a kernel with SPACELIKE support (an instantaneous long-range theta-E coupling) is added to the discrete action -> C1/C1r must FAIL;
 MUTATE=b: the reciprocity partners are dropped (prescribed drives, no phi_D/q_D partners) -> R1 must FAIL;  MUTATE=c: the sign of the fluid's kinetic term (and of the mediator's N) is flipped -> T0/T3 must FAIL;
 MUTATE=1: all three.  Outputs are named by mode.
DISCLOSED.  Before this file was written a one-line numpy check of the LOCAL pressure-bath dispersion cubic (planar, gravity g) was run; it showed growth for the pressure bath at every tau tried.
 The model, readings and pass lines above were NOT changed after it.  No parameter is fitted; beta = 1 (and lam_t = beta/eps_c) is a declared representative value of an UNTIED coupling.
DISCLOSED AFTER THE FIRST RUN (the declared model, pass lines and classification rules above were not changed; these are corrections and additions, each reported as such):
 (i) the first run showed a slowly decaying ringing at chi = 0.5 from the outflow boundary (late R_force 1.0074); a damping sponge layer was tried and REJECTED (it reflects the low frequencies), and the run time after the formation was extended to 40 light-crossings instead;  (ii) D4's stated IMPLICATION (retardation is second order) is wrong for
 boundary-driven (point-mass) sources: N2b measures FIRST-order scaling in chi (the algebraic identity D4 stands);  (iii) A_fluid's claim of exactness for reading P was wrong for the Lagrangian implementation (the target depends on the cell
 volume and position, so F has a derived force on the shells): added T5: a label-slaved control bath, the reciprocal completion with the derived shell force for the open class, the closed-class static imbalance, and a density-contrast control
 (T5c, r_out/r_in in {2, 3, 5, 8, 15, 30}, chosen before it was coded but AFTER an informal scan of the same values had been seen).  The T5a hypothesis printed with its check (that a label bath would be stable, so that the growth came from the position
 dependence of the target) was written after the first run and is REFUTED by its own result: the label bath grows too; the density-contrast control points to the canonical (fixed-temperature-bath) gravothermal instability of a high-contrast isothermal-like sphere;
 (iv) N1b's 1e-2 line is marginally missed by the open class (1.05e-2); it is kept as a failure (the deviation is O(chi), N2b).
SCOPE.  Spherical Newtonian, canonical a0, P2 law; GS is ONE causal completion (a Gauss-law scalar with a derivative fluid vertex): other mediators (a different spatial kernel or vertex) are untested;
 the fluid shells feel no exchange force (A_fluid); point-mass baryons in Q3; the hyd reading has no retarded completion; the probe is a test shell.  kappa = 1/2 FITTED.  Nothing here says the theory is closed.
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp

HERE0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE0)
from cfg72_common import *   # noqa
from cfg72_stability import ShellGas   # noqa

MUT = os.environ.get("MUTATE", "")
MUT_A = MUT in ("a", "1")
MUT_B = MUT in ("b", "1")
MUT_C = MUT in ("c", "1")
R = Report("cfg72_lightcone_exchange", MUT)
P = R.P
P(__doc__.strip())
if MUT:
    P(f"\n  *** MUTATE={MUT}: spacelike kernel = {MUT_A}, reciprocity partners dropped = {MUT_B}, kinetic sign flipped = {MUT_C}; the corresponding claims must FAIL ***")

MASSES = (1e9, 1e10, 1e12)
XS5 = np.array([0.3, 1.0, 3.0, 10.0, 30.0])
J70 = json.load(open(CFG70_JSON))

# =====================================================================================================================  S1 sympy
R.banner("S1  the GS action -> equations, static structure, retardation order, principal symbol (sympy)")
rr_, tt_ = sp.symbols("r t", real=True)
Ns, cs, gbs, cfs, vts, rls = sp.symbols("N c_m g_b c_f vt r_led", positive=True)
phS, phD, thS, thD = [sp.Function(n)(rr_, tt_) for n in ("phS", "phD", "thS", "thD")]
rho_f = sp.Function("rho")(rr_, tt_)
Jf = sp.Function("Jmem")(rr_, tt_)
php, phm = phS + phD / 2, phS - phD / 2
thp, thm = thS + thD / 2, thS - thD / 2
Ep, Em = -sp.diff(php, rr_), -sp.diff(phm, rr_)
Fn = lambda th, E: rls * th + cfs / 2 * (th - vts * E) ** 2
L_gs = (Ns / 2 * ((sp.diff(php, tt_) ** 2 - sp.diff(phm, tt_) ** 2) / cs ** 2 - (sp.diff(php, rr_) ** 2 - sp.diff(phm, rr_) ** 2))
        + gbs * rho_f * (php - phm) - (Fn(thp, Ep) - Fn(thm, Em)) - thD * Jf)
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L_gs, [phD, thD, phS, thS], [rr_, tt_])
zero = {phD: 0, thD: 0}
Eq0 = [sp.simplify((e.lhs - e.rhs).subs(zero).doit()) for e in eqs]
eps_e = thS + vts * sp.diff(phS, rr_)                                   # eps = theta - vt E,  E = -phi_r
want_phi = Ns * (sp.diff(phS, tt_, 2) / cs ** 2 - sp.diff(phS, rr_, 2)) - gbs * rho_f - sp.diff(cfs * vts * eps_e, rr_)
want_th = rls + cfs * eps_e + Jf
d1a = min(sp.simplify(Eq0[0] - want_phi), sp.simplify(Eq0[0] + want_phi), key=lambda z: sp.count_ops(z))
d1b = min(sp.simplify(Eq0[1] - want_th), sp.simplify(Eq0[1] + want_th), key=lambda z: sp.count_ops(z))
P(f"    phi_D-equation: {sp.simplify(Eq0[0])} = 0\n    theta_D-equation: {sp.simplify(Eq0[1])} = 0\n    Sigma-equations at Delta = 0: {Eq0[2]}, {Eq0[3]}")
R.check("D1 the Delta-variations at Delta = 0 are N(phi_tt/c_m^2 - phi_rr) = g_b rho + d_r(c_f vt eps) and r_led + c_f eps + J = 0 (up to an overall sign; sympy residual 0)",
        f"residuals {d1a}, {d1b}", d1a == 0 and d1b == 0)
R.check("D2 the Sigma-equations vanish identically at Delta = 0 (no advanced or extra equation)", f"{Eq0[2]}, {Eq0[3]}", Eq0[2] == 0 and Eq0[3] == 0)

# D3 static structure
Msym, lam_s, eps_c_s = sp.symbols("M lam eps_c", positive=True)
vth_s = sp.symbols("vartheta", positive=True)                            # = vt g_b / N
Nval = vts * gbs / vth_s                                                 # N eliminated by vartheta = vt g_b/N
beta_s = cfs * vts ** 2 / Nval
S_st = cfs * vts * (-rls / cfs)                                          # S = c_f vt eps, eps = -r_led/c_f (static fluid equation)
E_st = (gbs * Msym + S_st) / Nval                                        # E = (g_b M + S)/N, fluid occupying r > r_in (S(0) = 0)
theta_st = -rls / cfs + vts * E_st                                       # theta = eps + vt E
d3a = sp.simplify(theta_st - (vth_s * Msym - (1 + beta_s) * rls / cfs))
F_over_vth = sp.simplify((-gbs * E_st) / vth_s)                          # force on the probe / vartheta
lam_t_sym = (vts / gbs) / Msym
d3b = sp.simplify(F_over_vth - (rls - 1 / lam_t_sym))
delta_c = lam_t_sym * rls
fbb = (vth_s * Msym / (vts / gbs)) / (vth_s * rls)
d3c = sp.simplify(delta_c * fbb - 1)
E_ode = sp.Function("Ee")(rr_)
static_ode = sp.simplify((Ns * sp.diff(E_ode, rr_) - (gbs * sp.diff(sp.Function("Mb")(rr_), rr_) + sp.diff(S_st, rr_))).subs(E_ode, (gbs * sp.Function("Mb")(rr_) + S_st) / Ns).doit())
P(f"    static: theta - (vartheta M - (1+beta) r_led/c_f) = {d3a};  F/vartheta - (r_led - 1/lam_t) = {d3b};  delta * f_bb - 1 = {d3c};  Gauss ODE residual {static_ode}")
R.check("D3 static structure of GS: theta = vartheta M - (1+beta) r_led/c_f; the probe force is F/vartheta = r_led - 1/lam_t (r_led is G4's reaction, 1/lam_t the mediator's baryon-baryon force); delta*f_bb = 1 exactly",
        f"residuals {d3a}, {d3b}, {d3c}, {static_ode}", d3a == 0 and d3b == 0 and d3c == 0 and static_ode == 0)

# D4 quasi-static retardation order
Mrt = sp.Function("Mrt")(rr_, tt_)
Srt = sp.Function("Srt")(rr_, tt_)
E_qs = (gbs * Mrt + Srt) / Ns
wsym = sp.Function("w")(rr_, tt_)
E_full = E_qs + wsym
# phi-equation differentiated in r:  N(E_tt/c^2 - E_rr) = -g_b rho_r - S_rr,  rho = M_r
lhs_pde = Ns * (sp.diff(E_full, tt_, 2) / cs ** 2 - sp.diff(E_full, rr_, 2))
rhs_pde = -gbs * sp.diff(Mrt, rr_, 2) - sp.diff(Srt, rr_, 2)
w_source = sp.simplify(lhs_pde - rhs_pde - Ns * (sp.diff(wsym, tt_, 2) / cs ** 2 - sp.diff(wsym, rr_, 2)))
want_w = (gbs * sp.diff(Mrt, tt_, 2) + sp.diff(Srt, tt_, 2)) / cs ** 2
d4 = sp.simplify(w_source - want_w)
P(f"    E = E_qs + w: N(w_tt/c^2 - w_rr) = -(g_b M_tt + S_tt)/c^2 (algebraic residual {d4}).  NOTE (added after the first run): for a source that changes AT THE BOUNDARY (the point mass) the homogeneous solution fixed by the Gauss boundary condition is a pure delay m(t - r/c), FIRST order in R/(c t_f); the second-order statement holds only for bulk sources with no boundary-driven part (N2b measures first order)")
R.check("D4 (algebra) E = E_qs + w with N(w_tt/c_m^2 - w_rr) = -(g_b M_tt + S_tt)/c_m^2 (sympy residual 0); its stated implication 'second order' does NOT hold for boundary-driven sources (see N2b)", f"residual {d4}", d4 == 0)

# D5 principal symbol
kk, bt, cm = sp.symbols("k beta c_m", positive=True)
B5 = sp.Matrix([[0, -1, 0], [-cm ** 2 * (1 + bt), 0, cm ** 2 * bt], [0, 0, 0]])         # (e, p, y): e_t = -p_r, p_t = c_m^2[-(1+beta) e_r + beta y_r], y_t = lower order
ev5 = list(B5.eigenvals().keys())
sp_ok = set(sp.simplify(x) for x in ev5) == set([0, sp.sqrt(1 + bt) * cm, -sp.sqrt(1 + bt) * cm])
P(f"    GS principal symbol eigenvalues: {ev5}  (characteristic speed c_m sqrt(1+beta))")
R.check("D5 the GS principal symbol has real distinct eigenvalues {0, +-c_m sqrt(1+beta)}: hyperbolic; the exchange (theta relaxation, r_led) is zeroth order", f"{ev5}", sp_ok)

# D6 G4 closed forms (point mass) and the extended generalisation; hyd reaction by finite difference of the functional
gN_s, a0_s, x_s = sp.symbols("g_N a0 x", positive=True)
sig_gen = sp.Rational(3, 8) * a0_s * (2 * gN_s + a0_s) / (gN_s + a0_s)
d6a = sp.simplify(sig_gen.subs(gN_s, a0_s / x_s ** 2) - sp.Rational(3, 8) * a0_s * (2 + x_s ** 2) / (1 + x_s ** 2))
u_s, r_s, R_s, dm_s = sp.symbols("u r R dm", positive=True)
E_hyd_shell = sp.Rational(3, 4) * a0_s * dm_s * (sp.integrate(1, (r_s, u_s, R_s)) + sp.integrate(r_s ** 2 / u_s ** 2, (r_s, 0, u_s)))
a_hyd = sp.simplify(-sp.diff(E_hyd_shell, u_s) / dm_s)
d6b = sp.simplify(a_hyd - a0_s / 2)
# finite difference of the discretised hyd functional for a shell dm at u (fluid held at the target): a = -(1/dm) dE/du
def E_hyd_num(u, dm=1e-7, Rmax=100.0, n=2_000_001):
    rgn = np.linspace(1e-4, Rmax, n)
    th_ = 0.75 * (dm * (rgn > u) + dm * (rgn ** 2 / u ** 2) * (rgn < u))     # theta^T shell part / a0 (per unit radius)
    return float(np.trapz(th_, rgn))
uu, hh_ = 3.0, 2e-3
a_fd = -(E_hyd_num(uu + hh_) - E_hyd_num(uu - hh_)) / (2 * hh_ * 1e-7)
d6c = abs(a_fd / 0.5 - 1)
P(f"    sigma-slaved theta^T_M (general g_N) reduces to G4's (residual {d6a}); hyd (Sigma_out) reaction of a shell = {a_hyd}  (= a0/2, residual {d6b}); finite difference of the discretised functional {a_fd:.5f} a0 (rel. dev. {d6c:.1e})")
R.check("D6 sigma-slaved reaction (3/8) a0 (2 g_N + a0)/(g_N + a0) reduces to G4's for a point mass; the hydrostatic (Sigma_out) reading gives a0/2 for a shell (sympy, and a finite difference of the discretised functional to 2e-3)", f"residuals {d6a}, {d6b}, {d6c:.1e}", d6a == 0 and d6b == 0 and d6c < 2e-3)

# =====================================================================================================================  S2 discrete SK action
R.banner("S2  discrete GS action on the light-cone lattice: retardation in space and time, reciprocity")
JS, TS = 4, 4                                                             # nodes j = 0..4, times i = 0..4
Nm, gbm, thm_, cfm, rlm, mm_, tv = 1.3, 0.9, 0.7, 1.1, 0.6, 1.4, 0.7      # numerical TEST values (not model numbers)
betam = cfm * thm_ ** 2 / Nm
Dr = 1.0
Dt = 0.1
cm2 = Dr ** 2 / Dt ** 2 / (1 + betam)                                     # bare c_m^2 = c_eff^2/(1+beta): the COUPLED characteristic speed is c_eff = dr/dt
Gam = [0.5 * math.exp(-0.4 * k) for k in range(TS + 1)]
phS_ = sp.Matrix(JS + 1, TS + 1, lambda j, i: sp.Symbol(f"pS_{i}_{j}", real=True))
phD_ = sp.Matrix(JS + 1, TS + 1, lambda j, i: sp.Symbol(f"pD_{i}_{j}", real=True))
thS_ = sp.Matrix(JS, TS + 1, lambda l, i: sp.Symbol(f"tS_{i}_{l}", real=True))
thD_ = sp.Matrix(JS, TS + 1, lambda l, i: sp.Symbol(f"tD_{i}_{l}", real=True))
qS_ = [sp.Symbol(f"qS_{i}", real=True) for i in range(TS + 1)]
qD_ = [sp.Symbol(f"qD_{i}", real=True) for i in range(TS + 1)]
rng = np.random.default_rng(20260928)
phv = rng.uniform(-0.5, 0.5, (JS + 1, TS + 1)); thv = rng.uniform(0.2, 0.9, (JS, TS + 1)); qv = rng.uniform(2.25, 2.75, TS + 1)   # q in the cell between nodes 2 and 3
rext = rng.uniform(0.0, 0.3, (JS + 1, TS + 1))                            # external baryon source at nodes (numerical test data)
IA = 2                                                                    # CIC cell index
Phi_q = lambda z: z ** 2 / 2 + z ** 4 / 8
wA = lambda q: (IA + 1 - q) / Dr
wB = lambda q: (q - IA) / Dr
Fd = lambda th, E: rlm * th + cfm / 2 * (th - thm_ * E) ** 2


def build_action(spacelike=False, no_recip=False):
    S = 0
    for i in range(1, TS + 1):
        qp, qm = qS_[i] + qD_[i] / 2, qS_[i] - qD_[i] / 2
        qpo, qmo = qS_[i - 1] + qD_[i - 1] / 2, qS_[i - 1] - qD_[i - 1] / 2
        S += Dt * (mm_ / 2 * (((qp - qpo) / Dt) ** 2 - ((qm - qmo) / Dt) ** 2) - mm_ * (Phi_q(qp) - Phi_q(qm)))
        for j in range(JS + 1):                                             # wave kinetic (time) term at node j
            pp, pm = phS_[j, i] + phD_[j, i] / 2, phS_[j, i] - phD_[j, i] / 2
            ppo, pmo = phS_[j, i - 1] + phD_[j, i - 1] / 2, phS_[j, i - 1] - phD_[j, i - 1] / 2
            S += Dt * Dr * Nm / 2 * (((pp - ppo) / Dt) ** 2 - ((pm - pmo) / Dt) ** 2) / cm2
    for i in range(0, TS + 1):
        for l in range(JS):
            pp1, pm1 = phS_[l + 1, i] + phD_[l + 1, i] / 2, phS_[l + 1, i] - phD_[l + 1, i] / 2
            pp0, pm0 = phS_[l, i] + phD_[l, i] / 2, phS_[l, i] - phD_[l, i] / 2
            Ep_l, Em_l = -(pp1 - pp0) / Dr, -(pm1 - pm0) / Dr
            if i >= 1:
                S += -Dt * Dr * Nm / 2 * ((-Ep_l) ** 2 - (-Em_l) ** 2)      # gradient energy on link l at time i (times i = 1..TS), leapfrog structure
    for i in range(1, TS + 1):
        for l in range(JS):
            tp, tm = thS_[l, i] + thD_[l, i] / 2, thS_[l, i] - thD_[l, i] / 2
            pp1, pm1 = phS_[l + 1, i] + phD_[l + 1, i] / 2, phS_[l + 1, i] - phD_[l + 1, i] / 2
            pp0, pm0 = phS_[l, i] + phD_[l, i] / 2, phS_[l, i] - phD_[l, i] / 2
            Ep_l, Em_l = -(pp1 - pp0) / Dr, -(pm1 - pm0) / Dr
            EpS, EmS = -(phS_[l + 1, i] - phS_[l, i]) / Dr, None
            ED = -(phD_[l + 1, i] - phD_[l, i]) / Dr
            ES = -(phS_[l + 1, i] - phS_[l, i]) / Dr
            if no_recip:                                                      # MUTATE b: prescribed drive, no partner
                Fterm = rlm * thD_[l, i] + cfm * thS_[l, i] * thD_[l, i] - cfm * thm_ * thD_[l, i] * ES
            else:
                Fterm = Fd(tp, Ep_l) - Fd(tm, Em_l)
            S += -Dt * Dr * Fterm
            jr = sum(Gam[i - k] * (thS_[l, k] - thS_[l, k - 1]) / Dt * Dt for k in range(1, i + 1))
            S += -Dt * Dr * thD_[l, i] * jr
            if spacelike:                                                     # MUTATE a: instantaneous coupling of theta at link l to E at links l' with |l - l'| >= 2
                for l2 in range(JS):
                    if abs(l - l2) >= 2:
                        ES2 = -(phS_[l2 + 1, i] - phS_[l2, i]) / Dr
                        ED2 = -(phD_[l2 + 1, i] - phD_[l2, i]) / Dr
                        S += -Dt * Dr * 0.6 * math.exp(-abs(l - l2)) * (thS_[l, i] * ED2 + thD_[l, i] * ES2)
        # baryon vertex (CIC) at time i: g_b [w_j(q_+) phi_+ - w_j(q_-) phi_-]  (Dt weight); external source couples to phi_D only
        qp, qm = qS_[i] + qD_[i] / 2, qS_[i] - qD_[i] / 2
        for j, wf in ((IA, wA), (IA + 1, wB)):
            pp, pm = phS_[j, i] + phD_[j, i] / 2, phS_[j, i] - phD_[j, i] / 2
            if no_recip:
                S += Dt * gbm * wf(qS_[i]) * phD_[j, i]
            else:
                S += Dt * gbm * (wf(qp) * pp - wf(qm) * pm)
        for j in range(JS + 1):
            S += Dt * gbm * rext[j, i] * phD_[j, i]
    return S


P("    building the doubled discrete action (sympy) ...")
S_dbl = build_action(spacelike=MUT_A, no_recip=MUT_B)
allD = list(phD_) + list(thD_) + qD_
allS = list(phS_) + list(thS_) + qS_
zeroD = {v: 0 for v in allD}
rows = []                               # (kind, i, idx)
for i in range(1, TS):
    for j in range(1, JS):
        rows.append(("phi", i, j))
for i in range(1, TS + 1):
    for l in range(JS):
        rows.append(("th", i, l))
for i in range(1, TS):
    rows.append(("q", i, 0))
Rexpr = []
for kind, i, j in rows:
    v = phD_[j, i] if kind == "phi" else (thD_[j, i] if kind == "th" else qD_[i])
    Rexpr.append(sp.diff(S_dbl, v).subs(zeroD))
Jsym = sp.Matrix(Rexpr).jacobian(allS)
ptS = {}
for j in range(JS + 1):
    for i in range(TS + 1):
        ptS[phS_[j, i]] = phv[j, i]
for l in range(JS):
    for i in range(TS + 1):
        ptS[thS_[l, i]] = thv[l, i]
for i in range(TS + 1):
    ptS[qS_[i]] = qv[i]
Jnum = np.array(sp.lambdify(allS, Jsym, "numpy")(*[ptS[v] for v in allS]), float)
Rnum = np.array(sp.lambdify(allS, sp.Matrix(Rexpr), "numpy")(*[ptS[v] for v in allS]), float).ravel()
# column bookkeeping
col_info = []
for v in allS:
    nm = str(v)
    if nm.startswith("pS_"):
        _, i, j = nm.split("_"); col_info.append(("phi", int(i), float(j)))
    elif nm.startswith("tS_"):
        _, i, l = nm.split("_"); col_info.append(("th", int(i), int(l) + 0.5))
    else:
        i = int(nm.split("_")[1]); col_info.append(("q", i, IA + 0.5))
row_upd = []
for kind, i, j in rows:
    row_upd.append((i + 1, float(j)) if kind == "phi" else ((i, j + 0.5) if kind == "th" else (i + 1, IA + 0.5)))
W_SLACK = 1.0


def outside_cone(upd, col):
    iu, ju = upd
    ic, jc = col[1], col[2]
    return (ic > iu) or (abs(jc - ju) > (iu - ic) + W_SLACK + 1e-9)


c_adv = 0.0
for ri, upd in enumerate(row_upd):
    row = np.abs(Jnum[ri]); sc = row.max()
    bad = [row[ci] for ci, col in enumerate(col_info) if outside_cone(upd, col)]
    if bad and sc > 0:
        c_adv = max(c_adv, max(bad) / sc)
P(f"    residual-stencil causality measure (dependence outside the closed past cone of the update point, widened by 1 site): c_adv = {c_adv:.2e}")
R.check("C1 CAUSALITY (stencil): the EL residuals depend on no data outside the closed past light cone of their update point (widened by the 1-site vertex stencil): c_adv < 1e-12"
        + ("  [MUTATE a: spacelike kernel added]" if MUT_A else ""), f"c_adv = {c_adv:.2e}", c_adv < 1e-12)

# response support: unknowns = phi_{i+1,j} (rows phi), theta_{i,l} (rows th), q_{i+1} (rows q); known data (unperturbed) = everything else
unk_cols = []
for kind, i, j in rows:
    if kind == "phi":
        unk_cols.append(("phi", i + 1, float(j)))
    elif kind == "th":
        unk_cols.append(("th", i, j + 0.5))
    else:
        unk_cols.append(("q", i + 1, IA + 0.5))
ci_index = {(c[0], c[1], c[2]): k for k, c in enumerate(col_info)}
sel = [ci_index[u] for u in unk_cols]
Jsub = Jnum[:, sel]


def resp_measure(Jsub_, upd_rows, unk):
    Gm = np.linalg.inv(Jsub_)             # Gm[a, b] = d unknown_a / d source_b
    worst = 0.0
    sc = np.abs(Gm).max()
    for a, ua in enumerate(unk):
        for b, ub in enumerate(upd_rows):
            ib, jb = ub
            ia, ja = ua[1], ua[2]
            if (ia < ib) or (abs(ja - jb) > (ia - ib) + W_SLACK + 1e-9):
                worst = max(worst, abs(Gm[a, b]) / sc)
    return worst, sc


c_resp, gsc = resp_measure(Jsub, row_upd, unk_cols)
P(f"    response-support measure (the discrete retarded Green function outside the future cone of its source, widened by 1): c_resp = {c_resp:.2e}  (scale {gsc:.3e})")
R.check("C1r CAUSALITY (response): the inverse of the linearised residual map (the discrete retarded Green function) is supported in the future light cone of its source (widened by 1 site): c_resp < 1e-12"
        + ("  [MUTATE a: spacelike kernel added]" if MUT_A else ""), f"c_resp = {c_resp:.2e}", c_resp < 1e-12)

# C2 context: the same wave term with the instantaneous (elliptic) space Laplacian at the NEW time (c -> infinity: no retardation)
Jel = Jsub.copy()
idx_phi = [k for k, u in enumerate(unk_cols) if u[0] == "phi"]        # row k updates unknown k
for k in idx_phi:
    ua = unk_cols[k]
    Jel[k, :] = 0.0
    Jel[k, k] = -2.0 * Nm * Dt / Dr
    for k2 in idx_phi:
        ub = unk_cols[k2]
        if ub[1] == ua[1] and abs(ub[2] - ua[2]) == 1.0:
            Jel[k, k2] = Nm * Dt / Dr
c_resp_el, _ = resp_measure(Jel, row_upd, unk_cols)
P(f"    context: the same wave term with an instantaneous (elliptic) space Laplacian at the new time: c_resp = {c_resp_el:.2e}")
R.check("C2 (context) a non-retarded (elliptic) scalar has response outside the light cone: c_resp > 1e-4 (the check can fail)", f"c_resp = {c_resp_el:.2e}", c_resp_el > 1e-4)

# reciprocity: blocks and hand-coded residuals
def idx_col(kind, i, pos):
    return ci_index[(kind, i, pos)]


def idx_row(kind, i, j):
    return rows.index((kind, i, j))


asym = 0.0; scaleR = 1e-300
for i in range(1, TS):
    for l in range(JS):
        for j in range(1, JS):
            a_th_phi = Jnum[idx_row("th", i, l), idx_col("phi", i, float(j))]
            b_phi_th = Jnum[idx_row("phi", i, j), idx_col("th", i, l + 0.5)]
            asym = max(asym, abs(a_th_phi - b_phi_th)); scaleR = max(scaleR, abs(a_th_phi), abs(b_phi_th))
for i in range(1, TS):
    for j in (IA, IA + 1):
        a_q_phi = Jnum[idx_row("q", i, 0), idx_col("phi", i, float(j))]
        b_phi_q = Jnum[idx_row("phi", i, j), idx_col("q", i, IA + 0.5)] if 1 <= j <= JS - 1 else a_q_phi
        asym = max(asym, abs(a_q_phi - b_phi_q)); scaleR = max(scaleR, abs(a_q_phi), abs(b_phi_q))
asym_rel = asym / scaleR
Ehand = lambda phi_, i, l: -(phi_[l + 1, i] - phi_[l, i]) / Dr
Rh = []
for kind, i, j in rows:
    if kind == "phi":
        eps = lambda l: thv[l, i] - thm_ * Ehand(phv, i, l)
        val = (-(Nm * Dr / (cm2 * Dt)) * (phv[j, i + 1] - 2 * phv[j, i] + phv[j, i - 1]) + (Nm * Dt / Dr) * (phv[j + 1, i] - 2 * phv[j, i] + phv[j - 1, i])
               + Dt * cfm * thm_ * (eps(j) - eps(j - 1)) + gbm * Dt * ((wA(qv[i]) if j == IA else (wB(qv[i]) if j == IA + 1 else 0.0)) + rext[j, i]))
    elif kind == "th":
        eps = thv[j, i] - thm_ * Ehand(phv, i, j)
        val = -Dt * Dr * (rlm + cfm * eps) - Dt * Dr * sum(Gam[i - k] * (thv[j, k] - thv[j, k - 1]) / Dt * Dt for k in range(1, i + 1))
    else:
        dq = -(1.0 / Dr)
        val = Dt * (-mm_ * (qv[i + 1] - 2 * qv[i] + qv[i - 1]) / Dt ** 2 - mm_ * (qv[i] + qv[i] ** 3 / 2)) + gbm * Dt * (phv[IA, i] * (-1.0 / Dr) + phv[IA + 1, i] * (1.0 / Dr))
    Rh.append(val)
dev_hand = float(np.max(np.abs(np.array(Rh) - Rnum)) / max(np.abs(Rnum).max(), 1e-300))
P(f"    reciprocity: mixed-block asymmetry (theta-phi and q-phi) = {asym_rel:.2e};  hand-coded (independent) residuals vs the action's: {dev_hand:.2e}")
R.check("R1 RECIPROCITY: the mixed blocks dR^theta/dphi = (dR^phi/dtheta)^T and dR^q/dphi = (dR^phi/dq)^T (1e-12), and independently hand-coded residuals equal the action's (1e-12): the coupling is DERIVED from F"
        + ("  [MUTATE b: partners dropped]" if MUT_B else "") + ("  [MUTATE a: the mutated kernel changes the residual]" if MUT_A else ""),
        f"asymmetry {asym_rel:.2e}; hand-coded deviation {dev_hand:.2e}", asym_rel < 1e-12 and dev_hand < 1e-12)

# =====================================================================================================================  S3 numerics
R.banner("S3  Q1: the reaction with a light-cone kernel (coupled wave + fluid + probe simulation), the late-time table, the control against CFG70")
smooth = lambda u: np.where(u <= 0, 0.0, np.where(u >= 1, 1.0, 3 * u ** 2 - 2 * u ** 3))
gN_pt = lambda Mb, r: G * Mb / r ** 2
g_law_from_gN = lambda gN: np.sqrt(gN ** 2 + A0 * gN)


def qs_ode(eps_c, r_led, tau, beta, tend, dtm):
    """quasi-static (chi -> 0) GS = CFG70 with eps_c' = eps_c/(1+beta), tau' = (1+beta) tau.  Returns t, R(t) = -eps_c (y - e) with e = (m + beta y)/(1+beta)."""
    n = int(round(tend / dtm)) + 1
    t = np.arange(n) * dtm
    m = smooth(t)
    y = np.zeros(n)
    taup = (1 + beta) * tau
    off = r_led * (1 + beta) / eps_c
    ex = math.exp(-dtm / taup)
    for i in range(1, n):
        y[i] = ex * y[i - 1] + (1 - ex) * (m[i] - off)
    Rr = -eps_c / (1 + beta) * (y - m)
    return t, Rr, y


def wave_sim(chi, beta, eps_c, r_led, tau, J=100, rho_hat=None, tend=6.0, fluid=True, probe_x=0.5, rin=0.02, dt_fac=0.4, rec_every=None, Lx=1.0):
    """staggered leapfrog for the GS half-line in units R_f = 1, t_f = 1, c_eff = 1/chi; E, y on nodes, P on centres.  Point-mass baryons: E(0,t) = m(t) (Gauss BC); extended: bulk source rho_hat m(t), E(0) = 0.
    The fluid occupies R_f >= r >= rin; outer boundary = the outflow (advective) condition.  (After the first run a damping sponge layer was tried and REJECTED: it reflects the low frequencies; the ringing at chi = 0.5 is
    instead removed by running 40 light-crossing times after the formation, tend = 1 + 25 (1+beta) tau + 40 chi.)"""
    Dl = 1.0 / J
    Jt = int(round(Lx * J))
    ce = 1.0 / chi
    cm2_ = ce ** 2 / (1 + beta) if fluid else ce ** 2
    dt = dt_fac * Dl / ce
    nst = int(round(tend / dt))
    E = np.zeros(Jt + 1); y = np.zeros(Jt + 1); Pc = np.zeros(Jt)
    rn = np.arange(Jt + 1) * Dl
    fm = ((rn >= rin - 1e-12) & (rn <= 1.0 + 1e-12)).astype(float) if fluid else np.zeros(Jt + 1)
    rcn = (np.arange(Jt) + 0.5) * Dl
    sig = np.zeros(Jt)
    rh = None
    if rho_hat is not None:
        rh = np.zeros(Jt)
        rh[:len(rho_hat)] = rho_hat
    ex = math.exp(-dt / tau)
    jp = int(round(probe_x * J))
    rec = max(1, nst // 4000) if rec_every is None else rec_every
    T, EU, YU, EN = [], [], [], []
    for n in range(nst):
        tn = n * dt
        mn = float(smooth(tn))
        S = beta * fm * (y - E)
        src = (rh * mn) if rh is not None else 0.0
        Pc = (Pc + dt * cm2_ * (-(E[1:] - E[:-1]) / Dl + src + (S[1:] - S[:-1]) / Dl)) / (1.0 + dt * sig)
        En = E.copy()
        En[1:Jt] = E[1:Jt] - dt * (Pc[1:] - Pc[:-1]) / Dl
        En[0] = float(smooth(tn + dt)) if rho_hat is None else 0.0
        En[Jt] = E[Jt] - ce * dt / Dl * (E[Jt] - E[Jt - 1])
        E = En
        if fluid:
            y = fm * (ex * y + (1 - ex) * (E - r_led / eps_c))
        if n % rec == 0:
            T.append(tn + dt); EU.append(E[jp]); YU.append(y[jp]); EN.append(float(np.sum(y[1:]) / max(np.sum(fm[1:]), 1.0)))
    return np.array(T), np.array(EU), np.array(YU), np.array(EN)


# ---- N1 control: light-cone width -> 0, point mass, beta = 0 vs CFG70's committed late-time reaction
def late_G4(slav, Mb, x):
    """late-time reaction / g_law from R_late (= r_led) times theta^T_M, evaluated on the point mass."""
    rM = r_M_kpc(Mb)
    gN = A0 / x ** 2 if True else None
    gl = float(g_law_from_gN(gN))
    a4 = 0.75 * A0 if slav == "P" else 0.375 * A0 * (2 * gN + A0) / (gN + A0)
    return a4 / gl


tq, Rq0, yq0 = qs_ode(100.0, 1.0, 1.0, 0.0, 41.0, 0.005)
R_late_cfg70 = float(Rq0[-1])
dev70 = 0.0
for slav in ("P", "S"):
    for x in XS5:
        want = J70["numbers"]["late_reaction_over_glaw"][slav][f"{x:g}"]
        got = R_late_cfg70 * late_G4(slav, 1e10, float(x))
        dev70 = max(dev70, abs(got / want - 1))
R.check("N1 CONTROL: light-cone width -> 0 (chi -> 0, beta = 0), point mass: the late-time reaction/g_law equals CFG70's committed values (results JSON) to 1e-6, both slavings, x in {0.3,1,3,10,30}",
        f"R_late = {R_late_cfg70:.10f} (r_led = 1); worst relative deviation from the JSON {dev70:.2e}", dev70 < 1e-6)

# quasi-static reduction: GS at small chi vs CFG70's closed form with the mapped parameters
sim_qs = {}
for label, (epsc, rled) in (("closed", (100.0, 1.0)), ("open", (0.0 + 1.0, 0.0))):
    beta_ = 1.0
    tau_ = 0.1
    Tn, EU, YU, EN = wave_sim(0.005, beta_, epsc, rled, tau_, J=100, tend=1.0 + 25 * (1 + beta_) * tau_ + 40 * 0.005)
    lam_t_ = beta_ / epsc
    # reference field without the fluid coupling (same c_eff): exact retarded step of the boundary source: e^b(u, t) = m(t - u/c_eff)
    eb = smooth(Tn - 0.5 * 0.005)
    Rforce = (eb - EU) / lam_t_
    Rloc = -epsc * (YU - EU)
    sim_qs[label] = (Tn, Rforce, Rloc)
    tq_, Rq_, yq_ = qs_ode(epsc, rled, tau_, beta_, Tn[-1], 0.0025)
    Rq_i = np.interp(Tn, tq_, Rq_)
    pk = max(np.abs(Rq_i).max(), 1e-12)
    dq = np.abs(Rforce - Rq_i).max() / pk
    dl = np.abs(Rloc - Rq_i).max() / pk
    P(f"    {label:6s} (r_led = {rled:g}, eps_c = {epsc:g}, beta = 1, tau = 0.1, chi = 0.005): |R_force - R_qs|/peak = {dq:.2e}, |R_local - R_qs|/peak = {dl:.2e}; R_qs peak {pk:.3f}; late R_force = {Rforce[-1]:.6f}, R_local = {Rloc[-1]:.6f}")
    sim_qs[label] = dict(dq=dq, dl=dl, peak=pk, late_force=Rforce[-1], late_local=Rloc[-1], rled=rled)
okqs = all(v["dl"] < 1e-2 for v in sim_qs.values())
R.check("N1b the simulated GS at chi = 0.005 reproduces the quasi-static (CFG70 with eps_c -> eps_c/(1+beta), tau -> (1+beta) tau) reaction time series (misfit-at-the-probe R_local within 1e-2 of the peak; the propagated R_force is reported: its baryon-only reference has an O(chi/lam_t) ambiguity because the fluid renormalises the mediator speed)",
        f"{ {k: (round(v['dl'], 4), round(v['dq'], 4)) for k, v in sim_qs.items()} }", okqs)

# ---- N2: transient deviation vs chi, late-time limit, extrapolation to chi_phys
chis = (0.5, 0.05, 0.005)
dev_tab = {}
late_tab = {}
for label, (epsc, rled) in (("closed", (100.0, 1.0)), ("open", (1.0, 0.0))):
    beta_ = 1.0; tau_ = 0.1; lam_t_ = beta_ / epsc
    tq_, Rq_, yq_ = qs_ode(epsc, rled, tau_, beta_, 1.0 + 25 * (1 + beta_) * tau_ + 40 * 0.5 + 1.0, 0.0025)
    dev_tab[label] = []
    late_tab[label] = []
    for chi in chis:
        tend_ = 1.0 + 25 * (1 + beta_) * tau_ + 40 * chi
        Tn, EU, YU, EN = wave_sim(chi, beta_, epsc, rled, tau_, J=100, tend=tend_)
        eb = smooth(Tn - 0.5 * chi)
        Rforce = (eb - EU) / lam_t_
        Rq_i = np.interp(Tn, tq_, Rq_)
        pk = max(np.abs(Rq_i).max(), 1e-12)
        Rloc_ = -epsc * (YU - EU)
        dev_tab[label].append(np.abs(Rloc_ - Rq_i).max() / pk)
        late_tab[label].append((Rforce[-1], (-epsc * (YU - EU))[-1], EN[-1]))
        P(f"      {label:6s} chi = {chi:<6g}: late R_force = {Rforce[-1]:.8f}, R_local = {-epsc * (YU[-1] - EU[-1]):.8f} (want r_led = {rled:g}); max_t |R_local - R_qs|/peak = {dev_tab[label][-1]:.3e}; delivered heat/E_c = {EN[-1]:.5f} (want {1 - (1 + beta_) * rled / epsc:.5f})")
late_ok = all(abs(v[0] - (1.0 if lab == "closed" else 0.0)) < 1e-6 and abs(v[1] - (1.0 if lab == "closed" else 0.0)) < 1e-6 for lab in late_tab for v in late_tab[lab])
R.check("N2 the late-time reaction on the probe equals r_led (G4's value at r_led = 1, zero at r_led = 0) to 1e-6 for every light-cone speed simulated (chi = 0.5, 0.05, 0.005), closed and open",
        f"late values {late_tab}", late_ok)
Ed_ok = all(abs(late_tab[lab][k][2] - (1 - 2 * (1.0 if lab == 'closed' else 0.0) / (100.0 if lab == 'closed' else 1.0))) < 5e-3 for lab in late_tab for k in range(3))
R.check("E2 the heat delivered to the fluid by the GS memory law at late times is f_real E_c with f_real = 1 - (1+beta) r_led/eps_c (0.98 closed, 1.0 open), independent of the light-cone speed",
        f"delivered/E_c: { {lab: [round(v[2], 5) for v in late_tab[lab]] for lab in late_tab} }", Ed_ok)
chi_phys = {}
extrap = {}
for Mb in MASSES:
    Rf = 0.4 * r_ta_comm_kpc(Mb)                                         # fluid edge (B's committed r_e)
    chi_phys[Mb] = Rf * KPC_M / 1e3 / C_KMS / (1e9 * 3.15576e7)         # R_f / (c t_f), t_f = 1 Gyr
for label in dev_tab:
    lx = np.log(np.array(chis)); ly = np.log(np.maximum(np.array(dev_tab[label]), 1e-300))
    slope, icpt = np.polyfit(lx[1:], ly[1:], 1)                          # the two smaller chi
    extrap[label] = (slope, {Mb: float(math.exp(icpt + slope * math.log(chi_phys[Mb]))) for Mb in MASSES})
    P(f"    {label}: transient deviation from the chi -> 0 reaction ~ chi^{slope:.2f}; measured {['%.2e' % v for v in dev_tab[label]]} at chi = {chis}; EXTRAPOLATED to chi_phys "
      + ", ".join(f"{Mb:.0e}: {chi_phys[Mb]:.1e} -> {extrap[label][1][Mb]:.1e}" for Mb in MASSES))
R.num("chi_phys", chi_phys); R.num("transient_deviation", {k: dict(measured=dev_tab[k], chis=chis, slope=extrap[k][0], extrapolated=extrap[k][1]) for k in dev_tab})
R.check("N2b the transient deviation of the light-cone misfit reaction R_local from the chi -> 0 (instantaneous-in-space) reaction shrinks with chi (measured at three speeds; extrapolated, not solved, to chi_phys ~ 1e-3)",
        f"deviations closed {['%.2e' % v for v in dev_tab['closed']]}, open {['%.2e' % v for v in dev_tab['open']]}", dev_tab["closed"][2] < dev_tab["closed"][0] and dev_tab["open"][2] < dev_tab["open"][0])

# ---- N4: extended baryons in the simulation (exp sphere, M_b = 1e10, h/R_f from B's h = 2 kpc and R_f = r_e(CFG48))
Rf48 = 0.4 * r_ta48_kpc(1e10)
hRf = 2.0 / Rf48
Jx = 200
rc_ = (np.arange(Jx) + 0.5) / Jx
rho_hat = rc_ ** 2 * np.exp(-rc_ / hRf) / (2 * hRf ** 3)
rho_hat = rho_hat / (np.sum(rho_hat) / Jx)
Tn, EU, YU, EN = wave_sim(0.05, 1.0, 100.0, 1.0, 0.1, J=Jx, rho_hat=rho_hat, tend=1.0 + 25 * 0.2 + 40 * 0.05)
ebx = None
Tb, EUb, _, _ = wave_sim(0.05, 0.0, 100.0, 1.0, 0.1, J=Jx, rho_hat=rho_hat, tend=1.0 + 1.0, fluid=False)
Eb_late = float(EUb[-1])                                                  # = M_b(<u)/M_b (baryon-only static field at the probe)
Rf_ext_late = (Eb_late - float(EU[-1])) / (1.0 / 100.0)
Menc_u = float(np.sum(rho_hat[:int(0.5 * Jx)]) / Jx)
P(f"    extended baryons (exp sphere, h/R_f = {hRf:.4f}, J = {Jx}, chi = 0.05, closed): baryon-only late field at the probe {Eb_late:.6f} (M_b(<u)/M_b = {Menc_u:.6f}); late reaction (e_b - e)/lam_t = {Rf_ext_late:.6f} (want r_led = 1)")
R.check("N4 extended baryons (exp sphere) in the coupled light-cone simulation: the late-time reaction on the probe is r_led = 1 again (the exchange reaction is local at the probe: profile-independent)",
        f"late reaction {Rf_ext_late:.6f}; baryon-only field {Eb_late:.6f} vs enclosed fraction {Menc_u:.6f}", abs(Rf_ext_late - 1.0) < 2e-3 and abs(Eb_late - Menc_u) < 3e-3)

# ---- N3: the late-time reaction/g_law tables: point / exp / freeman, readings, masses, x
R.banner("N3  late-time reaction / g_law at x = r/r_M(M_tot):  point mass (control) vs extended baryons (CFG44 exp_sphere, freeman_disc), readings pressure (enc), sigma, hyd")


_PC = {}


def profile_cases(Mb):
    if Mb in _PC:
        return _PC[Mb]
    rM = r_M_kpc(Mb)
    _PC[Mb] = _profile_cases(Mb)
    return _PC[Mb]


def _profile_cases(Mb):
    rM = r_M_kpc(Mb)
    return [("point", None),
            ("exp h=2kpc", exp_sphere(Mb, 2.0)), ("exp h=0.5rM", exp_sphere(Mb, 0.5 * rM)),
            ("freeman h=3kpc", freeman_disc(Mb, 3.0)), ("freeman h=0.5rM", freeman_disc(Mb, 0.5 * rM))]


def reaction_over_glaw(prof, Mb, x, reading):
    rM = r_M_kpc(Mb)
    u = float(x) * rM
    gN = gN_pt(Mb, u) if prof is None else float(prof.u(u)) / u ** 2
    gl = float(g_law_from_gN(gN))
    if reading == "P":
        a = 0.75 * A0
    elif reading == "S":
        a = 0.375 * A0 * (2 * gN + A0) / (gN + A0)
    else:
        a = 0.5 * A0
    return a / gl, gN


tab3 = {}
ratio_max = 0.0; ratio_min = 1e9
for Mb in MASSES:
    for name, prof in profile_cases(Mb):
        for reading in ("P", "S", "hyd"):
            vals = [reaction_over_glaw(prof, Mb, x, reading)[0] for x in XS5]
            tab3[(Mb, name, reading)] = vals
            if name != "point":
                ref = [reaction_over_glaw(None, Mb, x, "P" if reading == "hyd" else reading)[0] for x in XS5]
                for v, r0 in zip(vals, ref):
                    if reading != "hyd":
                        ratio_max = max(ratio_max, v / r0); ratio_min = min(ratio_min, v / r0)
xg = np.geomspace(0.3, 30, 3000)
worst_low = 1e9; worst_by_case = {}
for Mb in MASSES:
    for name, prof in profile_cases(Mb):
        for reading in ("P", "S", "hyd"):
            vals = np.array([reaction_over_glaw(prof, Mb, x, reading)[0] for x in xg[::30]])
            worst_by_case[(Mb, name, reading)] = float(vals.min())
            worst_low = min(worst_low, float(vals.min()))
for Mb in MASSES:
    P(f"    M_b = {Mb:.0e}   (r_M = {r_M_kpc(Mb):.2f} kpc)   reaction/g_law at x = 0.3, 1, 3, 10, 30")
    for name, prof in profile_cases(Mb):
        P("      " + f"{name:17s}" + " | ".join(f"{rd}: " + " ".join(f"{v:9.3g}" for v in tab3[(Mb, name, rd)]) for rd in ("P", "S", "hyd")))
# x at which the point-mass reaction crosses 0.10 (P, S) and the minimum over x of the extended reaction/g_law (does any reading pass P1 at all x in [0.3,30]?)
from scipy.optimize import brentq
xc = {rd: brentq(lambda lx: reaction_over_glaw(None, 1e10, math.exp(lx), rd)[0] - 0.10, math.log(0.05), math.log(30)) for rd in ("P", "S")}
xc = {k: math.exp(v) for k, v in xc.items()}
p1_pass_any = {}
for (Mb, name, reading), vv in tab3.items():
    dense = np.array([reaction_over_glaw(dict(profile_cases(Mb))[name], Mb, x, reading)[0] for x in np.geomspace(0.3, 30, 60)])
    p1_pass_any[(Mb, name, reading)] = bool(dense.max() <= 0.10)
P(f"    the point-mass reaction reaches 0.10 g_law at x = {xc['P']:.2f} (pressure) / {xc['S']:.2f} (sigma); extended/point ratio of reaction/g_law over the table: min {ratio_min:.3g}, max {ratio_max:.3g};"
  f" P1 (<= 0.10 at every x in [0.3,30]) passes in {sum(p1_pass_any.values())} of {len(p1_pass_any)} (mass, profile, reading) cells")
R.num("reaction_table", {f"{k[0]:.0e}/{k[1]}/{k[2]}": v for k, v in tab3.items()})
R.check("N3 CLAIM (Q1/Q2, P1): with a light-cone kernel and with extended baryons the late-time reaction still exceeds 0.10 g_law somewhere on x in [0.3, 30] in EVERY (mass, profile, reading) cell -- P1 stays FAIL",
        f"cells passing P1: {sum(p1_pass_any.values())} of {len(p1_pass_any)}; crossing x = {xc['P']:.2f}/{xc['S']:.2f} (point)", sum(p1_pass_any.values()) == 0)
R.check("N3b (control) the point-mass rows equal CFG48/CFG70's G4 numbers (0.0647, 0.530, 2.13, 7.46, 22.5 pressure; 0.0620, 0.398, 1.17, 3.77, 11.3 sigma) to 1e-6",
        f"{[round(v, 4) for v in tab3[(1e10, 'point', 'P')]]}", max(abs(tab3[(1e10, 'point', 'P')][k] / J70['numbers']['late_reaction_over_glaw']['P'][f'{XS5[k]:g}'] - 1) for k in range(5)) < 1e-6
        and max(abs(tab3[(1e10, 'point', 'S')][k] / J70['numbers']['late_reaction_over_glaw']['S'][f'{XS5[k]:g}'] - 1) for k in range(5)) < 1e-6)

# =====================================================================================================================  S4 energy
R.banner("S4  energy budget (P2): kernel, speed and profile dependence, in CFG48's r_ta and B's committed r_ta")
E1 = {}
P("    M_b        conv.        r_e    x_e   ratio(point) | exp h=2 enc / hyd | exp h=.5rM enc / hyd | freeman h=3 enc / hyd | freeman h=.5rM enc / hyd   (ratio = E_c/((1/2) M_b V_f^2))")
worstE = 0.0; e_ratio_extremes = [1e9, 0.0]; pass_p2 = []
for Mb in MASSES:
    rM = r_M_kpc(Mb)
    KE = 0.5 * Mb * math.sqrt(G * Mb * A0)
    vth_ = 0.75 * A0
    for conv, rta in (("CFG48", r_ta48_kpc(Mb)), ("committed", r_ta_comm_kpc(Mb))):
        re = 0.4 * rta
        rg = np.geomspace(1e-3 * rM, re, 200001)
        row = {}
        Ec_pt = vth_ * np.trapz(np.full_like(rg, Mb), rg)                    # theta^T = vartheta M_b: (3 a0/4) M (r_e - r_min)
        row["point"] = Ec_pt / KE
        for name, prof in profile_cases(Mb)[1:]:
            Menc = prof.u(rg) / G
            Ec_enc = vth_ * np.trapz(Menc, rg)
            rho_b = prof.rho_b(rg)
            seg = (rho_b[1:] + rho_b[:-1]) * np.diff(rg) / 2
            tailrg = np.geomspace(re, 1e4 * rM, 20001)
            tail = np.trapz(prof.rho_b(tailrg), tailrg)
            Sig = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + tail          # Sigma_out(r) = int_r^inf rho_b dr'
            Ec_hyd = Ec_enc + 3 * math.pi * A0 * np.trapz(rg ** 2 * Sig, rg)
            row[name] = (Ec_enc / KE, Ec_hyd / KE)
        E1[(Mb, conv)] = row
        ratios = [row[n][k] for n in row if n != "point" for k in (0, 1)]
        e_ratio_extremes = [min(e_ratio_extremes[0], min(r / row["point"] for r in ratios)), max(e_ratio_extremes[1], max(r / row["point"] for r in ratios))]
        pass_p2.append(min([row["point"]] + ratios) <= 1.0)
        P(f"    {Mb:.0e}  {conv:9s} {re:8.1f} {re / rM:6.1f}  {row['point']:9.1f} | " + " | ".join(f"{row[n][0]:8.1f} / {row[n][1]:8.1f}" for n in row if n != "point"))
        cl = 1.5 * re / rM
        worstE = max(worstE, abs(row["point"] / cl - 1))
R.num("E1", {f"{k[0]:.0e}/{k[1]}": {n: v for n, v in row.items()} for k, row in E1.items()})
ctrlE = 0.0
for Mb in MASSES:
    key = f"{Mb:.0e}"
    for conv, jk in (("CFG48", "CFG48"), ("committed", "committed_nu_mono")):
        ctrlE = max(ctrlE, abs(E1[(Mb, conv)]["point"] / J70["numbers"]["E1"][key][jk]["ratio_num"] - 1))
R.check("E1 (control) the point-mass energy ratios E_c/((1/2) M_b V_f^2) reproduce CFG70's committed values (72.8/49.6/23.0 in CFG48's r_ta; 318/179/57 in B's) to 1e-6, and equal 1.5 x_e to 2e-3",
        f"worst deviation from the JSON {ctrlE:.2e}; closed-form agreement {worstE:.2e}", ctrlE < 1e-6 and worstE < 2e-3)
R.check("E1b CLAIM (Q1/Q2, P2): the energy the exchange must supply exceeds (1/2) M_b V_f^2 in BOTH r_ta conventions for every mass and every profile/reading (P2 stays FAIL); extended/point energy ratio within a factor 2",
        f"smallest ratio over all cells {min(min(([r['point']] + [r[n][k] for n in r if n != 'point' for k in (0, 1)])) for r in E1.values()):.1f}; extended/point energy ratio range [{e_ratio_extremes[0]:.3f}, {e_ratio_extremes[1]:.3f}]",
        not any(pass_p2) and 0.5 <= e_ratio_extremes[0] and e_ratio_extremes[1] <= 2.0)

# =====================================================================================================================  S5 Q3 stability
R.banner("S5  Q3: the coupled operator about the static target -- principal symbol, ideal control, Fourier symbol, spectra (readings P and S, tau list, N = 60 and 120)")
kin = -1.0 if MUT_C else 1.0
# T2 principal symbol of the fluid + bath system (planar patch, Lagrangian): y = (u = xi_t, p = dP_L, w = xi_r)
rho0, gam, P0, tauS, gg = sp.symbols("rho gamma P0 tau g", positive=True)
Bf = sp.Matrix([[0, -1 / rho0, 0], [-gam * P0, 0, 0], [1, 0, 0]])
evf = list(Bf.eigenvals().keys())
cs_sym = sp.sqrt(gam * P0 / rho0)
symb_ok = set(sp.simplify(e) for e in evf) == set([0, cs_sym, -cs_sym])
P(f"    fluid+bath principal symbol eigenvalues: {evf}  (0, +-c_s; the bath (U^T - U)/tau, gravity and the ledger are zeroth order)")
R.check("T2 the principal symbol of the coupled fluid+bath system has real distinct eigenvalues {0, +-c_s}: hyperbolic; the exchange changes only lower-order terms", f"{evf}", symb_ok)

# T0 controls at Mb = 1e10
GYR = GYR_PER_KPC_KMS
sg0 = ShellGas(1e10, N=60, reading="P", tau=np.inf, kin=kin)
fres = float(np.max(np.abs(sg0.residual())) / max(np.max(np.abs(np.real(sg0.f(sg0.y0() * (1 + 1e-3))))), 1e-300))
ev0, J0 = sg0.spectrum()
spec_scale = np.abs(ev0).max()
growth0 = float(ev0.real.max() / spec_scale)
P(f"    ideal (tau = inf) control, M_b = 1e10, N = 60: hydrostatic discretisation error vs CFG44 target {sg0.disc_err:.2e}; residual at the static state {fres:.1e}; max Re lambda / max|lambda| = {growth0:.2e}; max |Im| = {np.abs(ev0.imag).max():.3e}; {int(np.sum(np.abs(ev0.imag) < 1e-9 * spec_scale))} zero modes")
w2 = ev0[np.abs(ev0.imag) > 1e-9 * spec_scale]
R.check("T0 control: the discrete equilibrium is a fixed point of the ideal operator and the ideal spectrum has no growing mode (max Re lambda <= 1e-8 max|lambda|): no gradient instability, no ghost"
        + ("  [MUTATE c: kinetic sign flipped]" if MUT_C else ""), f"residual {fres:.1e}; growth {growth0:.2e}; discretisation error {sg0.disc_err:.1e}", fres < 1e-9 and growth0 <= 1e-8)

# T3 Fourier symbol of the GS half-line dissipative operator
def gs_symbol(kv, beta_, tau_, cm_, sgnN=1.0):
    M3 = np.array([[0, -1j * kv, 0], [-cm_ ** 2 * (1 + beta_) * 1j * kv * sgnN, 0, cm_ ** 2 * beta_ * 1j * kv * sgnN], [1.0 / tau_, 0, -1.0 / tau_]], dtype=complex)
    return np.linalg.eigvals(M3)


sgnN = -1.0 if MUT_C else 1.0
kgrid = np.geomspace(1e-3, 1e3, 60)
worstRe = -1e9
for beta_ in (0.0, 1.0):
    for tau_ in (0.01, 0.1, 1.0, 10.0):
        for kv in kgrid:
            ev = gs_symbol(kv, beta_, tau_, 1.0 / math.sqrt(1 + beta_), sgnN)
            worstRe = max(worstRe, float(ev.real.max() / max(np.abs(ev).max(), 1e-300)))
qq = cfm * thm_ ** 2
Hess = np.array([[Nm + qq, 0, -qq], [0, sgnN * Nm / cm2, 0], [-qq, 0, qq]])
hmin = float(np.linalg.eigvalsh(Hess).min())
P(f"    GS Fourier symbol: max over k, tau, beta of Re lambda/|lambda|_max = {worstRe:.2e}; energy Hessian (e, p, y) min eigenvalue {hmin:.3e} (positive: no ghost)")
R.check("T3 the GS half-line operator (mediator + fluid heat relaxation) has no growing Fourier mode (max Re lambda <= 1e-8 |lambda|) and a positive energy Hessian (no negative-norm mode)"
        + ("  [MUTATE c: N flipped]" if MUT_C else ""), f"worst Re lambda {worstRe:.2e}; Hessian min eigenvalue {hmin:.2e}", worstRe <= 1e-8 and hmin > 0)

# T4 spectra
Mb0 = 1e10
re48 = 0.4 * r_ta48_kpc(Mb0)
Vc_re = math.sqrt(re48 * float(g_law_from_gN(G * Mb0 / re48 ** 2)))
tdyn_re = re48 / Vc_re * GYR
tau_list = [("r_e/c", re48 / C_KMS * GYR), ("0.01 Gyr", 0.01), ("0.1 Gyr", 0.1), ("1 Gyr", 1.0), (f"t_dyn(r_e) = {tdyn_re:.2f} Gyr", tdyn_re), ("10 Gyr", 10.0)]
spec_res = {}
spec_flag = {}
conv_ok = True
P(f"    M_b = 1e10 (r_M = {r_M_kpc(Mb0):.2f} kpc, r_e = {re48:.1f} kpc, discretisation error of the hydrostatic target N=60: {ShellGas(Mb0, 60).disc_err:.1e}, N=120: {ShellGas(Mb0, 120).disc_err:.1e}); max Re lambda in 1/Gyr (positive = growth), converged?")
for reading in ("P", "S"):
    P(f"      reading {reading}:")
    for lab, tg in tau_list:
        gr = []; flg = []
        for Nn in (60, 120):
            sg = ShellGas(Mb0, N=Nn, reading=reading, tau=tg / GYR, kin=kin)
            ev, _ = sg.spectrum()
            gr.append(float(ev.real.max()) / GYR)
            flg.append(bool(ev.real.max() > 1e-8 * np.abs(ev).max()))
        spec_flag[(reading, lab)] = all(flg)
        rel = abs(gr[1] - gr[0]) / max(abs(gr[0]), abs(gr[1]), 1e-30)
        spec_res[(reading, lab)] = gr
        P(f"        tau = {lab:24s}: N=60 {gr[0]:+.3e}  N=120 {gr[1]:+.3e}   (1/H0 = {1 / (H0_KMS_KPC * 1e0) * GYR:.1f} Gyr; growth e-folding {(1 / gr[1]) if gr[1] > 1e-30 else float('inf'):.3g} Gyr)")
R.num("spectra_max_Re_lambda_per_Gyr", {f"{k[0]}/{k[1]}": v for k, v in spec_res.items()})
unstable = sorted(k for k, v in spec_flag.items() if v)
P(f"    unstable cells (max Re lambda > 1e-8 max|lambda| of the operator): {unstable}")
for Mb in (1e9, 1e12):
    for reading in ("P", "S"):
        for lab, tg in (("0.1 Gyr", 0.1), ("1 Gyr", 1.0)):
            ev, _ = ShellGas(Mb, N=60, reading=reading, tau=tg / GYR, kin=kin).spectrum()
            P(f"      M_b = {Mb:.0e}, reading {reading}, tau = {lab}: max Re lambda = {float(ev.real.max()) / GYR:+.3e} /Gyr")
R.check("T4 (reported) the spectra are computed at every declared tau for both readings; the growth rates are converged between N = 60 and N = 120 to 20% where nonzero",
        f"{ {k: [f'{x:+.2e}' for x in v] for k, v in spec_res.items()} }",
        all((not spec_flag[k]) or abs(v[1] - v[0]) / max(abs(v[0]), abs(v[1])) < 0.2 for k, v in spec_res.items()), load_bearing=False)

# ---- T5 (DISCLOSED ADDITION after the first run, reported only): mechanism control (label-slaved bath), the reciprocal completion (derived shell force), the closed-class static imbalance
R.banner("T5  (disclosed after the first run, reported) what drives the growth: a label-slaved bath, the action-derived shell force, the closed-class static imbalance")
spec_L = {}
for lab, tg in tau_list:
    gr = []
    for Nn in (60, 120):
        ev, _ = ShellGas(Mb0, N=Nn, reading="L", tau=tg / GYR, kin=kin).spectrum()
        gr.append((float(ev.real.max()) / GYR, bool(ev.real.max() > 1e-8 * np.abs(ev).max())))
    spec_L[lab] = gr
    P(f"      reading L (label-slaved: each shell relaxes to its OWN constant energy), tau = {lab:24s}: max Re lambda N=60 {gr[0][0]:+.3e}, N=120 {gr[1][0]:+.3e} /Gyr   growing = {gr[0][1] or gr[1][1]}")
recip_open = {}
for reading in ("P", "S"):
    for lab, tg in tau_list:
        gr = []
        for Nn in (60, 120):
            sgr = ShellGas(Mb0, N=Nn, reading=reading, tau=tg / GYR, kin=kin, recip=True, r_led=0.0, eps_c=1.0)
            ev, _ = sgr.spectrum()
            gr.append((float(ev.real.max()) / GYR, bool(ev.real.max() > 1e-8 * np.abs(ev).max())))
        recip_open[(reading, lab)] = gr
        P(f"      reciprocal OPEN class (r_led = 0, eps_c = 1, derived shell force kappa eps dU^T/dr included), reading {reading}, tau = {lab:24s}: N=60 {gr[0][0]:+.3e}, N=120 {gr[1][0]:+.3e} /Gyr  growing = {gr[0][1] and gr[1][1]}")
imb = {}
for reading in ("P", "S"):
    sgc = ShellGas(Mb0, N=60, reading=reading, tau=1.0, recip=True, r_led=1.0, eps_c=100.0)
    imb[reading] = sgc.imbalance
    P(f"      CLOSED class (r_led = 1): the static exchange force on the fluid nodes at the CFG44 target is {sgc.imbalance:.3g} x the pressure force per node (reading {reading}; independent of eps_c, since kappa eps = -r_led): the CFG44 target is NOT a static solution of the closed reciprocal action")
R.num("T5", dict(label_bath={k: v for k, v in spec_L.items()}, recip_open={f"{k[0]}/{k[1]}": v for k, v in recip_open.items()}, closed_static_imbalance=imb))
L_stable = all(not (v[0][1] or v[1][1]) for v in spec_L.values())
ct = {}
rMc = r_M_kpc(Mb0)
for ratio in (2, 3, 5, 8, 15, 30):
    for reading in ("L", "S"):
        ev, _ = ShellGas(Mb0, N=60, reading=reading, tau=1.0 / GYR, rin_x=1.0, rout=ratio * rMc).spectrum()
        contrast = (1 / (rMc * math.sqrt(2))) / (1 / (ratio * rMc * math.sqrt(1 + ratio ** 2)))
        ct[(ratio, reading)] = (float(ev.real.max()) / GYR, contrast, bool(ev.real.max() > 1e-8 * np.abs(ev).max()))
P("      density-contrast control (tau = 1 Gyr, fluid from r_in = r_M to r_out = ratio r_M; contrast = rho_c(r_in)/rho_c(r_out) of the target): "
  + "; ".join(f"{k[0]}/{k[1]}: contrast {v[1]:.0f}, max Re lambda {v[0]:+.3f}/Gyr" for k, v in ct.items()))
lowc = [v[2] for k, v in ct.items() if v[1] < 20]
highc = [v[2] for k, v in ct.items() if v[1] > 40]
R.check("T5c (reported) the growth of the label and S baths switches on with the DENSITY CONTRAST of the target (stable below ~20, growing above ~40; the canonical isothermal-sphere threshold is 32): the gravothermal instability of an isothermal-like self-gravitating fluid held at fixed temperature by a bath",
        f"stable at contrast < 20: {not any(lowc)}; growing at contrast > 40: {all(highc)}", (not any(lowc)) and all(highc), load_bearing=False)
R.num("T5c_density_contrast", {f"{k[0]}/{k[1]}": v for k, v in ct.items()})
R.check("T5a (reported) a LABEL-slaved bath (no position dependence of the target) has no growing mode at any tau: the growth of readings P and S comes from the position dependence of the target (heat added in phase with compression)",
        f"growing cells: {[k for k, v in spec_L.items() if v[0][1] or v[1][1]]}", L_stable, load_bearing=False)
grow_recip = sorted(k for k, v in recip_open.items() if v[0][1] and v[1][1])
R.check("T5b (reported) with the action-derived exchange force on the fluid shells included (reciprocal completion, open class r_led = 0, eps_c = 1) the growing modes of readings P and S remain",
        f"growing cells: {grow_recip}", len(grow_recip) > 0, load_bearing=False)

# =====================================================================================================================  verdicts
R.banner("VERDICTS")
stab_P = {lab: spec_res[("P", lab)][1] for lab, _ in tau_list}
stab_S = {lab: spec_res[("S", lab)][1] for lab, _ in tau_list}
grow_P = [lab for lab, _ in tau_list if spec_flag[("P", lab)]]
grow_S = [lab for lab, _ in tau_list if spec_flag[("S", lab)]]
q1_change = not (late_ok and ctrlE < 1e-6 and sum(p1_pass_any.values()) == 0)
q2_fig = not (0.5 <= ratio_min and ratio_max <= 2.0) or not (0.5 <= e_ratio_extremes[0] and e_ratio_extremes[1] <= 2.0)
q2_verdict = sum(p1_pass_any.values()) > 0 or any(pass_p2)
q3_change = bool(grow_P or grow_S)
R.verdict("Q1 light-cone kernel (space and time), point-mass baryons", "CHANGES THE VERDICT" if q1_change else "DOES NOT CHANGE IT",
          f"late-time reaction = r_led (G4/CFG70) to 1e-6 at every speed simulated; transient deviation ~ chi^{extrap['closed'][0]:.1f}, extrapolated to chi_phys {min(chi_phys.values()):.0e}-{max(chi_phys.values()):.0e} it is {min(min(extrap[l][1].values()) for l in extrap):.0e}-{max(max(extrap[l][1].values()) for l in extrap):.0e} of the peak; P2 ratios unchanged")
R.verdict("Q2 extended baryons", ("CHANGES THE FIGURES" if q2_fig else "does not change the figures") + ("; CHANGES THE VERDICT" if q2_verdict else "; does NOT change the verdict"),
          f"reaction/g_law ratio (extended/point) in [{ratio_min:.3g}, {ratio_max:.3g}]; energy ratio in [{e_ratio_extremes[0]:.3f}, {e_ratio_extremes[1]:.3f}]; P1 passes in {sum(p1_pass_any.values())} cells, P2 passes in {sum(pass_p2)} cells")
R.verdict("Q3 stability (declared operator)", "CHANGES THE VERDICT (growing mode)" if q3_change else "DOES NOT CHANGE IT (no growing mode)",
          f"reading P growing at tau in {grow_P}; reading S growing at tau in {grow_S}; GS Fourier symbol worst Re lambda {worstRe:.1e}; ideal control {growth0:.1e}; hyperbolic (T2, D5); "
          f"(T5, reported) label-slaved bath growing: {[k for k, v in spec_L.items() if v[0][1] or v[1][1]]}; reciprocal open class growing at {grow_recip}; closed-class static imbalance {imb}")
R.verdict("P1", "FAIL", f"late-time reaction exceeds 0.10 g_law in all cells; point-mass crossing x = {xc['P']:.2f}/{xc['S']:.2f}; extra mediator baryon-baryon force 1/lam_t against the reaction r_led: delta*f_bb = 1")
R.verdict("P2", "FAIL", "energy ratios 72.8/49.6/23.0 (CFG48) and 318/179/57 (committed) unchanged by kernel speed; extended baryons within a factor 2")
R.verdict("P3", "PASS as a structure" if (c_adv < 1e-12 and c_resp < 1e-12 and asym_rel < 1e-12 and dev_hand < 1e-12) else "FAIL",
          f"discrete GS action: c_adv {c_adv:.1e}, c_resp {c_resp:.1e} (elliptic context {c_resp_el:.1e}); reciprocity {asym_rel:.1e}; the price: characteristic speed c_m sqrt(1+beta) and delta*f_bb = 1")
R.verdict("P4", "see Q3", f"growth: P {grow_P}, S {grow_S}")
nf = R.write()
sys.exit(1 if nf else 0)
