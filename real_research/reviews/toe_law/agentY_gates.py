#!/usr/bin/env python3
# agentY_gates.py -- [SLOT-Y] the lens-only slip sector: numeric gates.
#  SG0  gate against banked numbers (agentW slip targets, Cassini margin) BEFORE any new use
#  SGA  the inversion: model functions from the lensing-RAR target, four banked nu shapes
#       (uses the matching relations DERIVED in agentY_quasistatic.py SC -- coefficients quoted there)
#  SGB  function health: monotonicity, J' > 0, ellipticity J' + 2Y J'' > 0 along each matched shape
#  SGC  solar system in-model: slip at Cassini conjunction; the chi-amplitude at Saturn; khronon-corner
#       feedback estimate
#  SGD  clusters x1.97 re-fail arithmetic; the agentZ type-split dial requirement in-model
#  SGE  tensor-sector numbers: c_T (exact theorem), alpha_M (exact zero + current siren bounds for
#       context), GW-chi mixing magnitude through a halo, graviton-decay comparison
# No git.

import numpy as np

out = []
def P(*s):
    line = " ".join(str(x) for x in s)
    out.append(line); print(line)

# constants (SI)
G   = 6.674e-11
c   = 2.998e8
A0_FW, A0_CAN = 9.36e-11, 1.2e-10          # the two banked footings (m s^-2)
Msun = 1.989e30
GMsun = 1.327e20                            # m^3 s^-2
Rsun = 6.957e8
pc   = 3.0857e16
kpc, Mpc = 1e3*pc, 1e6*pc
AU = 1.496e11

# the four banked nu shapes, verbatim from agentW_partner_uniqueness.py L59-62
def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))
NUS = {'McGaugh RAR': nu_rar, 'fw sqrt(1+1/y)': nu_fw, 'simple': nu_simple, 'F4 standard': nu_std}

P("="*100)
P("agentY_gates.py -- the lens-only slip sector: numeric gates")
P("="*100)

# ------------------------------------------------------------------------------------------------
P("\n[SG0] GATE against banked numbers (must reproduce agentW/agentI before any new use)")
# ------------------------------------------------------------------------------------------------
P("  slip amplitude targets Psi'/Phi' - 1 = 2(nu-1), McGaugh nu, framework a0:")
for gb, want in [(1e-13, 61.2), (1e-12, 19.4), (1e-11, 6.2)]:
    got = 2*nu_rar(gb/A0_FW) - 1
    P(f"    g_bar = {gb:.0e}: 2nu-1 = {got:.1f}   (banked {want})   {'GATE OK' if abs(got-want)<0.15*want else 'GATE FAIL'}")
y_cas = GMsun/(1.6*Rsun)**2/A0_FW
slip_cas_simple = 2*(nu_simple(y_cas) - 1)
P(f"  Cassini conjunction y = {y_cas:.2e} (banked 1.1e12); simple-nu slip = {slip_cas_simple:.2e}"
  f" (banked 1.8e-12); margin x{2.3e-5/slip_cas_simple:.1e} (banked x1.3e7)")
ok = abs(y_cas/1.1e12 - 1) < 0.05 and abs(slip_cas_simple/1.8e-12 - 1) < 0.15
P(f"  {'GATE OK' if ok else 'GATE FAIL'}")

with open('agentY_gates.out', 'w') as f: f.write("\n".join(out) + "\n")

# [SGA..SGE filled after the sympy matching relations land]

# ------------------------------------------------------------------------------------------------
P("\n[SGA] KINEMATIC TRACKABILITY: the slip operator CAN carry nu(y) -- the obstruction is mu=1")
# ------------------------------------------------------------------------------------------------
# The derived slip formula (minimal basis, J2 = 0, c10 = c30 = 0, J' = P const):
#   slip/Phi' = 2 Y (c20 + Y c20') ,  chi' = Phi'/(2P),  Y = y^2/(4P^2)
# Matching slip/Phi' = 2(nu(y)-1) is a first-order linear ODE with closed-form solution
#   Y c20(Y) = - Int_Y^inf (nu(2P sqrt(u)) - 1)/u du     [converges for all four banked shapes]
# (the homogeneous mode c20_h ~ 1/Y carries ZERO slip: the matching is unique up to it).
# So the OPERATOR KINEMATICS tracks any nu-shape; what fails is doing so WITH mu = 1 (SGB).
from scipy.integrate import quad

def c20_matched(nu, P):
    def Yc20(Yv):
        I, _ = quad(lambda u: (nu(2*P*np.sqrt(u)) - 1.0)/u, Yv, np.inf, limit=400)
        return -I
    def c20(Yv):
        Yv = np.atleast_1d(Yv); return np.array([Yc20(Y)/Y for Y in Yv])
    def c21(Yv, c20v=None):
        Yv = np.atleast_1d(Yv)
        c = c20(Yv) if c20v is None else c20v
        return (nu(2*P*np.sqrt(Yv)) - 1)/Yv**2 - c/Yv
    return c20, c21

P("  matching identity spot checks (P = 25, McGaugh nu): slip/Phi' vs 2(nu-1):")
Pv = 25.0
c20f, c21f = c20_matched(nu_rar, Pv)
for yv in [1e-3, 1e-1, 1.0, 10.0]:
    Yv = (yv/(2*Pv))**2
    c20v = c20f(Yv); c21v = c21f(Yv, c20v)
    got = 2*Yv*(c20v[0] + Yv*c21v[0]); want = 2*(nu_rar(yv) - 1)
    P(f"    y = {yv:8.1e}: 2Y(c20+Yc20') = {got:+.6e}   2(nu-1) = {want:.6e}   ratio-1 = {got/want-1:+.1e}")
P("  convergence of the matching integral, all four banked shapes (P = 25, y = 0.1):")
for name, nu in NUS.items():
    cf, _ = c20_matched(nu, Pv)
    P(f"    {name:18s}: c20(Y(y=0.1)) = {cf((0.1/(2*Pv))**2)[0]:.4e}   [finite: trackable]")

with open('agentY_gates.out', 'w') as f: f.write("\n".join(out) + "\n")

# ------------------------------------------------------------------------------------------------
P("\n[SGB] THE DECISIVE NUMBER: the matter-channel pollution of the nu-matched model")
# ------------------------------------------------------------------------------------------------
# The machine obstruction (agentY_quasistatic.out): EXACT mu = 1 + y-tracking slip has no solution
# in the minimal basis (all branches collapse to slip in {0, kappa Phi', -Phi'}). The physical
# question that remains: how BIG is Delta_Phi when c20 is nu-matched and the lens-only conditions
# are simply dropped? If the pollution is percent-level or P-suppressed, an approximate-(mu=1)
# member exists; if it is O(slip)-sized, the double-counting theorem (agentW: 8.7-21.6 sigma)
# kills the class outright.
import pickle, sympy as sp
with open('agentY_eqs.pkl', 'rb') as f:
    PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
Ch1s = sp.symbols('chi1', real=True)
J1, J2 = sp.symbols('J1 J2', real=True)
c10, c11, c20, c21, c30, c31 = sp.symbols('c10 c11 c20 c21 c30 c31', real=True)
rhob_f = sp.Function('rhob')(r_s)
rb0, rb1v = sp.symbols('rb0 rb1', real=True)

zero_c = {c10: 0, c11: 0, c30: 0, c31: 0, J2: 0, G_s: 1}
sg  = PK['slipgrad'].subs(zero_c)
dps = PK['DeltaPsi'].subs(zero_c)
ch2 = PK['Ch2_b'].subs(zero_c)
for name, e in [('slip', sg), ('DeltaPsi', dps), ('chi2', ch2)]:
    pass
args = [r_s, alp_s, J1, Ch1s, c20, c21, rb0, rb1v]
def lam(e):
    e = e.subs({sp.Derivative(rhob_f, r_s): rb1v, rhob_f: rb0})
    return sp.lambdify(args, e, 'numpy')
L_sg, L_dps, L_ch2 = lam(sg), lam(dps), lam(ch2)

GMc2 = 1e11*1.476e3/3.0857e19; a_h = 3.0
alp_n = A0_FW/c**2*3.0857e19
def Mb(r):  return GMc2*r**2/(r + a_h)**2
def dMb(r): return GMc2*2*r*a_h/(r + a_h)**3
def d2Mb(r): return GMc2*2*a_h*(a_h - 2*r)/(r + a_h)**4
nu = nu_rar
rg = np.logspace(-0.5, 4.2, 6000)
Ph1 = Mb(rg)/rg**2
Ph2 = dMb(rg)/rg**2 - 2*Mb(rg)/rg**3
Ph3 = d2Mb(rg)/rg**2 - 4*dMb(rg)/rg**3 + 6*Mb(rg)/rg**4
yv = Ph1/alp_n
rb0v = (Ph2 + 2*Ph1/rg)/(4*np.pi)
rb1n = (Ph3 + 2*Ph2/rg - 2*Ph1/rg**2)/(4*np.pi)

P("  Hernquist M = 1e11 Msun, a = 3 kpc, framework a0, McGaugh nu;")
P("  pollution diagnostics vs P (= J', the kinetic stiffness):")
P("    columns: y = 1.0, 0.3, 0.1, 0.03, 0.01;  entries: Delta_Phi/(4 pi G rhob_eff + |divslip|)")
P("    where rhob_eff is the local matter source -- and the OUTSKIRTS force ratio dg/g_bar")
for Pv in (1.0, 5.0, 25.0, 125.0):
    chi1 = Ph1/(2*Pv); Yv = (yv/(2*Pv))**2
    c20f, c21f = c20_matched(nu, Pv)
    c20v = c20f(Yv); c21v = c21f(Yv, c20v)
    slip = L_sg(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    dpsv = L_dps(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    # sanity: slip/Phi' should equal 2(nu-1)
    sfrac = slip/Ph1; tfrac = 2*(nu(yv)-1)
    serr = np.nanmax(np.abs(sfrac/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    divslip = np.gradient(slip*rg**2, rg)/rg**2
    DPhi = dpsv - divslip
    # matter-channel force pollution: dg(r) = (1/r^2) int r^2 DPhi dr
    dg = np.cumsum(np.concatenate([[0], 0.5*(DPhi[1:]*rg[1:]**2 + DPhi[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    frac = dg/Ph1
    row = []
    for t in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - t)); row.append(f"{frac[i]:+10.2e}")
    P(f"    P = {Pv:5.0f}:  dg/g_bar = " + " ".join(row) + f"    [slip-match check: {serr:.1e}]")
P("  context: the SPARC deep-regime kill bars (agentW): 0.165-0.49 dex coherent overshoot was")
P("  8.7-21.6 sigma; a |dg/g| of 0.01 ~ 0.004 dex; of 0.1 ~ 0.04 dex; of 1.0 ~ 0.3 dex.")

with open('agentY_gates.out', 'w') as f: f.write("\n".join(out) + "\n")

P("\n  READING (the channel-routing wall, quantified):")
P("  - the slip-match is exact (column check ~1e-15): the operators CAN carry nu(y) in the")
P("    ij-channel. But the SAME operators, at that amplitude, feed the N-channel (Hamiltonian")
P("    constraint) at |dg/g_bar| ~ 1e7-1e8: ~ (a0 r/c^2)^-1 x the phantom -- and the numbers are")
P("    P-INDEPENDENT: no kinetic-stiffness suppression. Physical root: a potential-amplitude")
P("    scalar's anisotropic-stress channel is its WEAKEST channel; forcing phantom-sized ij-stress")
P("    drives the C-sector Lagrangian ~(a0 r/c^2)^-1 above the EH scale locally. The approximate-mu")
P("    route is dead by ~7 orders against even the loosest SPARC bar. OBSTRUCTED.")

with open('agentY_gates.out', 'w') as f: f.write("\n".join(out) + "\n")

# ------------------------------------------------------------------------------------------------
P("\n[SGC] WHAT SURVIVES AS ARCHITECTURE (theorems for ANY future carrier on the u-frame)")
# ------------------------------------------------------------------------------------------------
P("  c_T = 1 IDENTICALLY and alpha_M = 0 IDENTICALLY for the entire leaf-tangential operator class")
P("  (machine theorem, agentY_quasistatic [SA]): no derivative of h_ij enters; GW170817 and the")
P("  GW-friction gate pass by architecture, INCLUDING inside halos (where Y != 0).")
P("  FRW quietness (a_mu = 0 comoving => sector off cosmologically): the 1809.03484-class")
P("  graviton-decay kill (|alpha_H| <~ 1e-10) and dark-energy perturbation bounds are evaded by")
P("  construction -- the sector has NO cosmological background to decay into.")
P("  Standard-siren context (pinned approximately, flagged as from-memory values): GW170817-era")
P("  and GWTC-3-era constraints on the friction parameter sit at sigma(alpha_M/c_M) ~ O(0.1-1)")
P("  (e.g. Lagos+ 2019-class analyses; dark-siren H0/friction fits). The u-frame class predicts 0.")
P("  Degeneracy/ghosts: in unitary gauge NO operator carries a time derivative (Y = gam^{ij}")
P("  d_i chi d_j chi exactly; a_i = d_i ln N exactly): the Ostrogradsky question never arises; the")
P("  chi-field is elliptic on the leaves (cuscuton-class precedent). The kill is NOT ghosts.")

# ------------------------------------------------------------------------------------------------
P("\n[SGD] THE GATES THE CALIBRATION WOULD HAVE INHERITED (recorded for the obstruction map)")
# ------------------------------------------------------------------------------------------------
P("  Solar (would-be): the nu-matched slip at the Cassini conjunction is the banked number by")
P("  construction (SG0: 1.75e-12 simple-nu, x1.3e7 inside the bound; exp-tail: dead-dead);")
P("  the matter channel of an exact-mu member is EXACTLY clean (no reflex, no precession, no Q2).")
P("  Clusters: an exactly-nu-keyed slip re-fails clusters at the banked x1.97 (agentW gate 2) --")
g_clu = G*7e13*Msun/(1.0*Mpc)**2
y_clu = g_clu/A0_FW
P(f"  in-model arithmetic: g_bar(1 Mpc, 7e13 Msun) = {g_clu:.2e} m/s^2, y = {y_clu:.1f},"
  f" nu = {nu_rar(y_clu):.2f}: M_lens/M_bar predicted = {nu_rar(y_clu):.2f} vs observed ~7.1 (x{7.1/nu_rar(y_clu):.2f} short).")
P("  The type split (agentZ, +0.194 dex TYPE-IRREDUCIBLE): the one structural insight that")
P("  SURVIVES the obstruction: the slip generators are TRANSVERSE-DIVERGENCE operators")
P("  ((a.q) P_T:Dq): their amplitude is keyed to the BENDING of the field lines -- zero for")
P("  planar, maximal for spherical configurations. ANY future geometry-keyed slip carrier")
P("  inherits a morphology-tracking dial with the agentZ sign (spheroids > disks at fixed g_bar).")
d194 = 10**0.194
P(f"  required dial: x{d194:.2f} in amplitude between types; available geometric range in this")
P("  operator class: [0 (planar) .. full (spherical)] -- the range covers it; the quantitative")
P("  disk-vs-spheroid contrast is the named non-spherical computation for the successor carrier.")

P("\n" + "="*100)
P("VERDICT: OBSTRUCTED -- see agentY_psislip_construction.md section 4 for the four-wall map.")
P("="*100)
with open('agentY_gates.out', 'w') as f: f.write("\n".join(out) + "\n")
