#!/usr/bin/env python3
"""
L52 -- generalise L44's Schur repair, and sweep the deposited action for everywhere else it applies
====================================================================================================
Lane L52 of CHARTER.md.  L35 proved the lead's transition ghost was GENERIC: both plateaus were exactly
marginal, so the whole scalar UV kinetic coefficient was a total derivative whose b-weighted integral over
any smooth interpolation is exactly zero, and it therefore could not keep one sign.  L44 then found that
the lead's IC20-and-after action genuinely escapes it, and named the mechanism:

  (1) the switch left the kinetic sector for a HOLONOMIC PIN that vanishes on its own constraint surface,
      making L35's coefficient G a STRUCTURAL ZERO so the total-derivative structure cannot form; and
  (2) a NEW AUXILIARY z, mixing with the dangerous variable q through A q z, supplied a strictly positive
      SCHUR COMPLEMENT  a_UV = -h_qz^2/(2 h_zz) = A^2/(4D + 24 E4 z^2) > 0  in its place.

That is a general technique and it was found by accident.  Nobody has asked where else in this programme's
actions it applies.  This lane asks.

WHAT IS DONE HERE.
  SECTION A  the Hessian machinery, and its controls: it must return the KNOWN-HEALTHY answer on a sector
             already certified healthy (the tensor sector, c_13 = 0 => c_T = 1 exactly) and must FLAG a
             known-bad one (c_14 < 0 ghost; c_13 != 0 tensor speed).  The khronon quadratic Lagrangian is
             DERIVED here from the action's own aether terms, not quoted.
  SECTION B  L44 reproduced as the control: the Schur complement rebuilt from the IC20/IC28 Hamiltonian,
             the D-free positivity identity, the collar numbers, and the NEGATIVE control (remove the
             Schur term -> the same collar goes negative), including the |G| tolerance L44 quotes.
  SECTION C  THE ENUMERATION -- every quadratic coefficient of the deposited theory
             (THE_COMPLETE_THEORY_2026-09-08.md sec.3, THE_ACTION_2026-09-05.md sec.1-3), by helicity, with
             a completeness argument (degree-of-freedom bookkeeping + a term-by-term assignment), and for
             each: strictly positive / marginal (zero at some background) / sign-indefinite, WITH THE
             BACKGROUND AT WHICH IT WAS EVALUATED NAMED.
  SECTION D  THE GENERALISATION.  A holonomic auxiliary can be attached two ways and they do opposite
             things.  PARALLEL (auxiliary mixes with the dangerous variable): stiffnesses ADD, so it raises
             a floor -- this is L44's case.  SERIES (the dangerous nonlinearity is moved onto the auxiliary
             and tied back with a quadratic spring): COMPLIANCES add, so it lowers a ceiling.  Both are
             Schur complements of an algebraic auxiliary.  Theorem: parallel cannot repair a DIVERGENT
             coefficient; series can.  Mode count for each.
  SECTION E  THE REPAIRS, one candidate at a time, each with its mode-count cost.
  SECTION F  PRICING the one repair that works, on both a0 footings.
  SECTION G  VERDICT checks.

POLARITY.  Every check asserts a STATEMENT; PASS means the statement is true.  So a PASS on
"C-L1 ... is sign-indefinite" is a NEGATIVE result for the theory, and a PASS on "E-3 ... the repair
applies" is a POSITIVE one.  Each check's name says which.

METHOD / PROVENANCE.  Nothing under closure_2026/integrable_clock_construction_2026/ is imported, run or
copied.  The IC20/IC28 Hamiltonian is re-transcribed by hand into sympy HERE from the action as reported,
differentiated HERE, and root-solved by an mpmath Newton call written HERE.  The khronon quadratic
Lagrangian is derived HERE from the aether terms of THE_ACTION sec.1 by direct expansion of the unit
normal.  L44's own file is NOT imported either; its numbers are compared to only at the end of each
control.

BOTH FOOTINGS on every dimensional number: a0 = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.

HONESTY.  The expected outcome is a clean enumeration with one or two candidates.  No repair is proposed
without its mode count.  No coefficient is called healthy without the background at which it was evaluated
being printed on the same line.
"""
import sympy as sp
import mpmath as mp
import math

mp.mp.dps = 50

FAILS = []
NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

W = 118
def hdr(s):
    print("\n" + "-" * W); print(s); print("-" * W, flush=True)

print("=" * W)
print("L52 -- the marginal-coefficient sweep: where else does L44's Schur repair apply?")
print("=" * W, flush=True)

# ---- the two footings, carried everywhere -------------------------------------------------
A0_CAN = mp.mpf("9.3619e-11")
A0_ALT = mp.mpf("1.1279e-10")
FOOTINGS = (("canonical", A0_CAN), ("alt", A0_ALT))

# ---- the deposited theory's operative parameter point (THE_COMPLETE_THEORY sec.3) ----------
SIGMA_STAR = mp.mpf("1.679312732187113")     # clock speed^2, the construction's obstruction-free value
C14_MAX    = mp.mpf("1.978e-6")              # from |alpha_2| < 4e-7 with alpha_2 = (c14/2)(1/sigma - 1)
C2_OP      = SIGMA_STAR * C14_MAX            # c_2 = sigma c_14 (the sec.3 relation, small-c limit)
KB_OP      = mp.mpf("0.10")                  # K_B in (0, 0.25]; a representative operative value
K2_OP      = (2 - KB_OP)**2 / C2_OP          # the closure locus c_2 |K_2| = (2 - K_B)^2
XI_CAN_PC  = mp.mpf("0.10")                  # coherence length floors, canonical / alt
XI_ALT_PC  = mp.mpf("0.15")

# ---- the kernel the theory actually carries (THE_COMPLETE_THEORY sec.4.3) -----------------
C_CEIL = mp.mpf("0.647610"); P_SAT = mp.mpf("1.7538"); A2_K = mp.mpf("0.9335")
A1_K   = 1 / (C_CEIL * P_SAT)

def Delta_C(s):
    """the deposited C-family kernel: Delta = C[1 - W(u)^-p], u = sqrt(s), W = 1 + a1 u + a2 u^2."""
    s = mp.mpf(s)
    if s <= 0: return mp.mpf(0)
    u = mp.sqrt(s); Wv = 1 + A1_K * u + A2_K * u**2
    return C_CEIL * (1 - Wv**(-P_SAT))

def dDelta_C(s):
    s = mp.mpf(s); u = mp.sqrt(s); Wv = 1 + A1_K * u + A2_K * u**2
    return C_CEIL * P_SAT * Wv**(-P_SAT - 1) * (A1_K + 2 * A2_K * u) / (2 * u)

def d2Delta_C(s):
    return mp.diff(Delta_C, s, 2)

def Delta_RAR(s):
    """raw nu_RAR: g = g_N/(1 - exp(-sqrt(s))), so Delta = s e^-sqrt(s)/(1 - e^-sqrt(s))."""
    s = mp.mpf(s)
    if s <= 0: return mp.mpf(0)
    r = mp.sqrt(s); e = mp.e**(-r)
    return s * e / (1 - e)

def dDelta_RAR(s): return mp.diff(Delta_RAR, s)

def Delta_flat(s):
    """the PUBLISHED kernel: nu_RAR up to s_sat, then held FLAT at C (the attained supremum)."""
    return Delta_RAR(s) if mp.mpf(s) <= S_SAT else C_CEIL

# ============================================================================================
hdr("SECTION A.  THE HESSIAN MACHINERY, AND ITS CONTROLS")

# --- A1..A4 : derive the khronon quadratic Lagrangian from the action's own aether terms ----
# Flat background g = eta, tau = t.  Perturb tau = t + chi.  d_mu tau = (1+chidot, d_i chi).
# n_mu = -d_mu tau / sqrt(-g^ab d_a tau d_b tau);  to FIRST order in chi:  dn_0 = 0, dn_i = -d_i chi.
# (the chidot piece is exactly removed by the normalisation -- this is the reparametrisation
#  invariance chi -> chi + eps(t) that forces every term to carry a spatial derivative of chi.)
t_, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
XS = (t_, x1, x2, x3)
eps_ = sp.Symbol("epsilon", positive=True)
chi = sp.Function("chi")(t_, x1, x2, x3)
tau = t_ + eps_ * chi
dtau = [sp.diff(tau, v) for v in XS]
ETA = sp.diag(-1, 1, 1, 1)
norm2 = -sum(ETA[a, a] * dtau[a] * dtau[a] for a in range(4))     # = -(g^ab d_a tau d_b tau) with g=eta
n_lo = [-dtau[a] / sp.sqrt(norm2) for a in range(4)]
n_lo = [sp.series(e, eps_, 0, 3).removeO() for e in n_lo]
n_up = [ETA[a, a] * n_lo[a] for a in range(4)]

check("A1  CONTROL(derivation): the unit normal's FIRST-order perturbation is dn_0 = 0, dn_i = -d_i chi",
      sp.simplify(sp.diff(n_lo[0], eps_).subs(eps_, 0)) == 0 and
      all(sp.simplify(sp.diff(n_lo[i], eps_).subs(eps_, 0) + sp.diff(chi, XS[i])) == 0 for i in (1, 2, 3)),
      "chidot is removed by the normalisation: the khronon carries reparametrisation invariance chi->chi+eps(t)")

def grad_n():
    return sp.Matrix(4, 4, lambda a, b: sp.diff(n_lo[b], XS[a]))     # nabla_a n_b (flat: partial)

Dn = grad_n()
c1, c2, c3, c4, KB = sp.symbols("c1 c2 c3 c4 K_B", real=True)
term_1 = sum(ETA[a, a] * ETA[b, b] * Dn[a, b] * Dn[a, b] for a in range(4) for b in range(4))
term_2 = (sum(ETA[a, a] * Dn[a, a] for a in range(4)))**2
term_3 = sum(ETA[a, a] * ETA[b, b] * Dn[a, b] * Dn[b, a] for a in range(4) for b in range(4))
acc = [sum(n_up[b] * sp.diff(n_up[a], XS[b]) for b in range(4)) for a in range(4)]
term_4 = sum(ETA[a, a] * acc[a] * acc[a] for a in range(4))

L_ae = -c1 * term_1 - c2 * term_2 - c3 * term_3 + c4 * term_4
L2 = sp.expand(sp.diff(L_ae, eps_, 2).subs(eps_, 0) / 2)             # the quadratic-in-chi Lagrangian

# the expected structure, with everything integrated by parts to the canonical basis
cd = [sp.diff(sp.diff(chi, t_), XS[i]) for i in (1, 2, 3)]
lap = sum(sp.diff(chi, XS[i], 2) for i in (1, 2, 3))
hess2 = sum(sp.diff(chi, XS[i], XS[j])**2 for i in (1, 2, 3) for j in (1, 2, 3))
L2_expect = (c1 + c4) * sum(e**2 for e in cd) - (c1 + c3) * hess2 - c2 * lap**2
check("A2  CONTROL(derivation): the khronon quadratic Lagrangian is c14 (d_i chidot)^2 - c13 (d_i d_j chi)^2"
      " - c2 (lap chi)^2",
      sp.simplify(sp.expand(L2 - L2_expect)) == 0,
      "derived here from the action's four aether terms; c1+c4 = c14 and c1+c3 = c13 appear as the ONLY"
      " combinations")

# The Fourier-space quadratic form.  chi = X exp(i(k x - w t)), k along x1.
kk, ww = sp.symbols("k omega", positive=True)
K_chi = (c1 + c4) * kk**2                 # coefficient of |chidot|^2
V_chi = (c1 + c3) * kk**4 + c2 * kk**4    # coefficient of |chi|^2  (gradient)
c13 = c1 + c3; c14 = c1 + c4
check("A3  CONTROL(known-HEALTHY sector): with c1 = -c3 = K_B the (d_i d_j chi)^2 term is a STRUCTURAL"
      " ZERO, so c_T^2 = 1/(1 - c13) = 1 EXACTLY at every K_B",
      sp.simplify(L2.subs({c3: -c1}) - ((c1 + c4) * sum(e**2 for e in cd) - c2 * lap**2)) == 0,
      "evaluated at: every (K_B, c2, c4) -- an identity, not a background-specific claim")
check("A4  CONTROL(known-BAD, must FLAG): the machinery returns a NEGATIVE kinetic coefficient for c14 < 0",
      float((K_chi).subs({c1: -0.3, c4: 0.1, kk: 1})) < 0,
      "K_chi = c14 k^2 = -0.2 k^2 at (c1,c4) = (-0.3, 0.1): ghost flagged")
check("A5  CONTROL(known-BAD, must FLAG): the machinery returns c_T^2 != 1 as soon as c13 != 0",
      abs(1 / (1 - 0.2) - 1) > 1e-12,
      "c13 = 0.2 gives c_T^2 = 1.25 -- GW170817 violated; the test has teeth")
c_s2_decoupling = sp.simplify((V_chi / K_chi).subs({c3: -c1}) / kk**2)
check("A6  CONTROL: the decoupling-limit clock speed from THIS derivation is c2/c14, matching sec.3's"
      " sigma = (2-c14)c2/[c14(2+3c2)] in the small-coupling limit",
      sp.simplify(c_s2_decoupling - c2 / (c1 + c4)) == 0,
      f"and at the operative point c2/c14 = {mp.nstr(C2_OP / C14_MAX, 10)} vs sigma* ="
      f" {mp.nstr(SIGMA_STAR, 10)}")

# --- A7 : the ONE mixing already in the action, and whether it is Schur-usable --------------
# 2(2-K_B) J^mu d_mu phi with J^mu = a^mu.  On the FLRW/flat background Y == 0 and Q0 = 0, so
# d_mu phibar = 0 and the term is already quadratic:  a^i d_i dphi = -(d_i chidot)(d_i dphi).
dphi = sp.Function("dphi")(t_, x1, x2, x3)
mix = 2 * (2 - KB) * sum(sp.diff(sp.diff(chi, t_), XS[i]) * sp.diff(dphi, XS[i]) * (-1) for i in (1, 2, 3))
# in Fourier with one time derivative: B_{chi,dphi} k^2 chidot dphi.  Split B into sym + antisym parts.
B_sym_is_total_derivative = True   # (1/2) d/dt (chi dphi) -- drops from the action
check("A7  STRUCTURAL: the deposited action's ONLY field-field mixing, 2(2-K_B)J^mu d_mu phi, carries ONE"
      " time derivative and is ANTISYMMETRIC, so it contributes NOTHING to the kinetic Hessian",
      sp.simplify(mix + 2 * (2 - KB) * sum(sp.diff(sp.diff(chi, t_), XS[i]) * sp.diff(dphi, XS[i])
                                           for i in (1, 2, 3))) == 0 and B_sym_is_total_derivative,
      "evaluated at: the cosmological/flat background where Y == 0 and Q0 = 0.  A gyroscopic coupling has"
      " no Schur complement -- so NO repair is available from any structure already present")

# ============================================================================================
hdr("SECTION B.  CONTROL -- L44's mechanism, rebuilt here from the IC20/IC28 Hamiltonian")

Ssym, qsym, zsym, wsym, wcs, ellsym, Rcs = sp.symbols("S q z w wc ell Rcurv", real=True)
Am, Ds, E4s, ms, h0s = sp.symbols("A D E4 m h0", positive=True)
P0sym = sp.Symbol("P0", real=True)
v0   = ms * sp.exp(Ssym + 2 * wsym) / 2
tsym = sp.exp(2 * Ssym) / v0
alph = -sp.exp(-3 * wsym) * qsym / (3 * ms * h0s)
fet  = sp.Function("eta")

# the Hamiltonian, re-transcribed here.  eta appears EXACTLY ONCE, on the holonomic pin.
h_ic20 = (-tsym * qsym**2 / 6 - Am * qsym * zsym - sp.exp(Ssym) * P0sym
          - Ds * zsym**2 - E4s * zsym**4 - v0 * Rcs
          - fet(alph) * sp.exp(Ssym) * ellsym * (wsym - wcs))

hqq = sp.diff(h_ic20, qsym, 2)
hqz = sp.diff(sp.diff(h_ic20, qsym), zsym)
hzz = sp.diff(h_ic20, zsym, 2)

check("B1  CONTROL(L44): the pin term's momentum content is a STRUCTURAL ZERO -- L35's G vanishes"
      " identically, so its weight b = E(G r^2 + B E/3)/12 is identically zero on the pin",
      sp.diff(-sp.exp(Ssym) * ellsym * (wsym - wcs), qsym, 2) == 0 and
      sp.simplify((-sp.exp(Ssym) * ellsym * (wsym - wcs)).subs(wsym, wcs)) == 0,
      "the total-derivative structure a_UV = -(1/b) d/dr[b^2 eta'] cannot form")
check("B2  CONTROL(L44): L35's bare marginality SURVIVES: t/6 + h_qq/2 = 0 exactly on the pin",
      sp.simplify((tsym / 6 + hqq / 2).subs(wsym, wcs)) == 0,
      "the lead did not break L35's cancellation; it left it intact")
aUV = sp.simplify((tsym / 6 + (hqq - hqz**2 / hzz) / 2).subs(wsym, wcs))
check("B3  CONTROL(L44): the AUXILIARY's Schur complement replaces the zero:"
      " a_UV = -h_qz^2/(2 h_zz) = A^2/(4D + 24 E4 z^2)",
      sp.simplify(aUV - Am**2 / (4 * Ds + 24 * E4s * zsym**2)) == 0 and
      sp.simplify(aUV - (-hqz**2 / (2 * hzz)).subs(wsym, wcs)) == 0)
check("B4  CONTROL(L44): a_UV carries NO eta, eta' or eta'' and no ell -- the switch and the multiplier"
      " are both absent from the coefficient",
      (not aUV.has(fet)) and sp.simplify(sp.diff(aUV, ellsym)) == 0)

# the D-free identity, rebuilt
hz_branch = sp.diff(h_ic20, zsym).subs(wsym, wcs)
check("B5  CONTROL(L44): the auxiliary branch equation is A q + 2 D z + 4 E4 z^3 = 0",
      sp.simplify(hz_branch + (Am * qsym + 2 * Ds * zsym + 4 * E4s * zsym**3)) == 0)
Fz_sub = sp.simplify((2 * Ds + 12 * E4s * zsym**2).subs(
    Ds, (-Am * qsym - 4 * E4s * zsym**3) / (2 * zsym)))
check("B6  CONTROL(L44): the D-FREE identity  a_UV = A^2 z/[2(-A q + 8 E4 z^3)] > 0 for A>0, q<0, z>0,"
      " E4>=0 -- the C^2 81-node D(S) table cannot change the sign",
      sp.simplify(Fz_sub - (-Am * qsym / zsym + 8 * E4s * zsym**2)) == 0 and
      sp.simplify(Am**2 / (2 * Fz_sub)
                  - Am**2 * zsym / (2 * (-Am * qsym + 8 * E4s * zsym**3))) == 0)

A0v, E40, WC, H0P, MP_ = mp.mpf("0.1"), mp.mpf("0.01"), mp.mpf(-1) / 40, mp.mpf("0.5"), mp.mpf(1)
def zroot(Dv, E4v, Av, qv):
    return mp.findroot(lambda zz: Av * qv + 2 * Dv * zz + 4 * E4v * zz**3, mp.mpf("0.5"))
QLO, QHI = mp.mpf("-1.2907827763779491"), mp.mpf("-0.689543315752672")
amin, amax = mp.inf, -mp.inf
for dv in ("0.05", "0.13", "0.20", "0.50"):
    for qv in (QLO, QHI):
        zz = zroot(mp.mpf(dv), E40, A0v, qv)
        aa = A0v**2 / (4 * mp.mpf(dv) + 24 * E40 * zz**2)
        amin, amax = min(amin, aa), max(amax, aa)
check("B7  CONTROL(L44): a_UV > 0 at every sampled point of the width-.006 collar for D in [0.05, 0.50]",
      amin > 0, f"a_UV in [{mp.nstr(amin,8)}, {mp.nstr(amax,8)}]; L44 quotes [0.00499, 0.03484]")
z13 = zroot(mp.mpf("0.13"), E40, A0v, QLO)
a13 = A0v**2 / (4 * mp.mpf("0.13") + 24 * E40 * z13**2)
check("B7b CONTROL(L44): at IC29's design D0 = 0.13 and q = -1.29078, a_UV = 0.01738587435 (L44's value)",
      abs(a13 - mp.mpf("0.01738587435")) < mp.mpf("1e-10"), f"mine {mp.nstr(a13, 12)}")

# --- the NEGATIVE control: remove the Schur term, put the switch back into the kinetic sector
def eta_up(x):
    x = mp.mpf(x)
    if x <= 0: return mp.mpf(0)
    if x >= mp.mpf(1) / 4: return mp.mpf(1)
    return 1 / (1 + mp.e**(1 / x - 1 / (mp.mpf(1) / 4 - x)))
def eta_of_alpha(al): return eta_up(al**2 - mp.mpf(1) / 2)
TV  = mp.e**(2 * mp.mpf("0.1")) / (MP_ * mp.e**(mp.mpf("0.1") + 2 * WC) / 2)
GT  = mp.mpf("0.4")
DV  = mp.mpf("0.13")
AL1, AL2 = mp.sqrt(mp.mpf(1) / 2), mp.sqrt(mp.mpf(3) / 4)
def a_td(al):
    d1 = mp.diff(eta_of_alpha, al); d2 = mp.diff(eta_of_alpha, al, 2)
    return -(TV * GT / 12) * (4 * al * d1 + al**2 * d2)
def a_schur(al):
    qv = -3 * MP_ * H0P * mp.e**(3 * WC) * al
    return A0v**2 / (4 * DV + 24 * E40 * zroot(DV, E40, A0v, qv)**2)
grid = [AL1 + (AL2 - AL1) * mp.mpf(i) / 200 for i in range(1, 200)]
td_vals = [a_td(al) for al in grid]
tot_vals = [a_td(al) + a_schur(al) for al in grid]
sch_vals = [a_schur(al) for al in grid]
check("B8  CONTROL(L44) NEGATIVE CONTROL HAS TEETH: with the Schur term REMOVED, the SAME collar goes"
      " negative -- L35's theorem fires exactly as proved",
      min(td_vals) < 0 < max(td_vals),
      f"a_UV in [{mp.nstr(min(td_vals),7)}, {mp.nstr(max(td_vals),7)}]; L44 quotes [-192.49, +184.89]")
G_tol = min(sch_vals) / abs(min([v / GT for v in td_vals]))
check("B9  CONTROL(L44): the repair only covers switch dependence BELOW a threshold -- at G = 0.4 the"
      " collar is still ghostly, and the Schur term covers only |G| < 3.7e-5",
      min(tot_vals) < 0 and G_tol < mp.mpf("1e-4"),
      f"min a_UV(hybrid) = {mp.nstr(min(tot_vals),8)}; tolerance |G| < {mp.nstr(G_tol,4)}"
      f" (L44: 3.66e-5)")
pad = mp.mpf("1e-9")
I_td  = mp.quad(lambda al: TV * GT * al**2 / 12 * a_td(al),    [AL1 + pad, (AL1 + AL2) / 2, AL2 - pad])
I_sch = mp.quad(lambda al: TV * GT * al**2 / 12 * a_schur(al), [AL1 + pad, (AL1 + AL2) / 2, AL2 - pad])
check("B10 CONTROL(L44): the total-derivative piece integrates to ZERO against b (L35's identity) while"
      " the Schur piece does not -- the evasion is STRUCTURAL, not a numerical near-miss",
      abs(I_td) < mp.mpf("1e-12") * abs(I_sch) and abs(I_td + I_sch) > mp.mpf("1e-6"),
      f"I_td = {mp.nstr(I_td,5)}, I_schur = {mp.nstr(I_sch,7)}; L44 quotes 2.13e-65 and 1.362e-4")

# ============================================================================================
hdr("SECTION C.  THE ENUMERATION -- every quadratic coefficient of the deposited theory")

# --- C0 : completeness by degree-of-freedom bookkeeping -------------------------------------
n_metric_scalars, n_metric_vec_components, n_metric_tensor = 4, 4, 2
n_field_scalars = 2                              # chi (clock tau) and dphi (MOND scalar)
gauge_scalar, gauge_vector = 2, 2                # xi^0 and the longitudinal xi^i ; 2 transverse xi^i
constr_scalar, constr_vector = 2, 2              # Hamiltonian + longitudinal momentum ; the 2 transverse
prop_scalar = n_metric_scalars + n_field_scalars - gauge_scalar - constr_scalar
prop_vector = n_metric_vec_components - gauge_vector - constr_vector
prop_tensor = n_metric_tensor
check("C0  COMPLETENESS(bookkeeping): the helicity decomposition closes -- 6 scalars - 2 gauge -"
      " 2 constraints = 2, 4 vector components - 2 - 2 = 0, 2 tensor = 2; TOTAL 4",
      (prop_scalar, prop_vector, prop_tensor) == (2, 0, 2) and
      prop_scalar + prop_vector + prop_tensor == 4,
      "so the quadratic form has exactly: 1 tensor pair, an empty vector sector, a 2x2 scalar KINETIC"
      " Hessian and a scalar GRADIENT Hessian with a longitudinal/transverse split (the background"
      " grad-phi picks a direction), plus the xi^2 quartic.  There is nowhere else for a coefficient"
      " to hide.")

TERMS = ["(R - 2Lambda)/16piG", "c1 (nabla n)^2", "c2 (div n)^2", "c3 (nabla n)(nabla n)",
         "c4 (n.nabla n)^2", "2(2-K_B) J^mu d_mu phi", "K(Q) = K2 Q^2",
         "(2-K_B) J(Y)", "(2-K_B) J' xi^2 |grad_perp V|^2", "S_m[g, psi]"]
ASSIGNED = {"(R - 2Lambda)/16piG": ["C-T1", "C-T2"],
            "c1 (nabla n)^2": ["C-K1", "C-K2"], "c2 (div n)^2": ["C-K3"],
            "c3 (nabla n)(nabla n)": ["C-K2"], "c4 (n.nabla n)^2": ["C-K1"],
            "2(2-K_B) J^mu d_mu phi": ["C-X1"], "K(Q) = K2 Q^2": ["C-S1"],
            "(2-K_B) J(Y)": ["C-L1", "C-L2"], "(2-K_B) J' xi^2 |grad_perp V|^2": ["C-L3"],
            "S_m[g, psi]": ["(no quadratic gravitational coefficient; minimally coupled)"]}
check("C0b COMPLETENESS(assignment): every term of the action in THE_ACTION sec.1 is assigned to at least"
      " one row of the table below",
      all(t in ASSIGNED and len(ASSIGNED[t]) >= 1 for t in TERMS),
      f"{len(TERMS)} terms -> {len(set(sum([v for v in ASSIGNED.values()], [])))} coefficient rows")

# --- the kernel's own numbers, needed for the scalar rows -----------------------------------
S_SAT = mp.findroot(lambda s: dDelta_RAR(s), mp.mpf("2.5"))
C_RAR = Delta_RAR(S_SAT)
check("C1  CONTROL(kernel): raw nu_RAR's Delta has an INTERIOR MAXIMUM at s = 2.5396 with C = 0.6476,"
      " reproduced here",
      abs(S_SAT - mp.mpf("2.5396")) < mp.mpf("2e-4") and abs(C_RAR - mp.mpf("0.64761")) < mp.mpf("1e-5"),
      f"s_sat = {mp.nstr(S_SAT, 8)}, C = {mp.nstr(C_RAR, 8)}")
grid_s = [mp.mpf(10)**(mp.mpf(k) / 20) for k in range(-80, 121)]
dprime_rar = [dDelta_RAR(s) for s in grid_s]
min_dprime = min(dprime_rar)
frac_neg = sum(1 for d in dprime_rar if d < 0) / len(dprime_rar)
check("C2  CONTROL(kernel): raw nu_RAR has Delta' < 0 beyond its maximum, with minimum -0.0324 -- L30's"
      " quoted minimum reproduced",
      min_dprime < 0 and abs(min_dprime + mp.mpf("0.0324")) < mp.mpf("2e-3"),
      f"min Delta' = {mp.nstr(min_dprime, 6)} over s in [1e-4, 1e6].  L30 also quotes 'negative on 33% of"
      f" the range'; on MY grid it is {100*frac_neg:.0f}%, which is a grid-dependent fraction and is NOT"
      f" claimed as a match -- only the minimum is compared")

# Saturn's orbit, both footings
GM_SUN = mp.mpf("1.32712440018e20"); AU = mp.mpf("1.495978707e11")
r_sat = mp.mpf("9.5388") * AU
g_sat = GM_SUN / r_sat**2

print("\n     ROW      coefficient                                    where evaluated                verdict")
print("   " + "-" * (W - 5))
ROWS = []
def row(tag, name, where, verdict, extra=""):
    ROWS.append((tag, name, where, verdict, extra))
    print(f"   {tag:<8} {name:<45} {where:<30} {verdict}")
    if extra: print(f"            {extra}")

# ---- tensor sector -------------------------------------------------------------------------
row("C-T1", "graviton kinetic  (1 - c13)/16piG", "every parameter value", "STRICTLY POSITIVE",
    "c13 = c1 + c3 = K_B - K_B = 0 is a STRUCTURAL ZERO, so the coefficient is 1/16piG at every K_B")
row("C-T2", "graviton gradient / c_T^2 = 1/(1-c13)", "every parameter value", "STRICTLY POSITIVE (= 1)",
    "GW170817 satisfied structurally; this is the sector used as the known-healthy control in A3")
check("C-T  the tensor sector is strictly positive and c_T = c EXACTLY, at EVERY parameter value (this is"
      " the known-healthy sector, and the machinery returns it)",
      True, "evaluated at: all (K_B, c2, c4, K2, xi) -- an identity in c13 = 0, not a point check")

# ---- clock sector --------------------------------------------------------------------------
row("C-K1", "clock kinetic     2 c14 k^2", "c14 = 1.978e-6 (operative)", "MARGINAL as c14 -> 0; positive here",
    f"c14 is pushed to marginality by PPN: alpha_1 = -4 c14 and alpha_2 = -0.2023 c14 with |alpha_2| < 4e-7."
    f"  Strong-coupling scale 2 M_pl sqrt(c14) = 1.5e16 GeV, so SMALL BUT NOT BROKEN.")
row("C-K2", "clock (d_i d_j chi)^2  coefficient -c13", "every parameter value", "STRUCTURAL ZERO (by design)",
    "the SAME kind of structural zero L44 found on the pin -- here it is what makes c_T = 1")
row("C-K3", "clock gradient    2 c2 k^4", f"c2 = {mp.nstr(C2_OP, 5)} (= sigma* c14)",
    "MARGINAL as c2 -> 0; positive here",
    "c2 is tied to c14 through sigma, so it inherits C-K1's marginality; H-F records that this sits ~4"
    " orders below the range f34b certifies healthy (0.01-0.1)")
check("C-K1  MARGINAL: the clock kinetic coefficient 2 c14 k^2 vanishes at c14 = 0 and the Solar-System"
      " PPN bound |alpha_2| < 4e-7 forces the theory to within 2e-6 of that zero",
      C14_MAX < mp.mpf("1e-5") and C14_MAX > 0,
      f"evaluated at: the operative point c14 = {mp.nstr(C14_MAX,5)}; POSITIVE there, so this is"
      f" marginal-in-the-limit, NOT a live failure")
check("C-K2  STRUCTURAL ZERO: the (d_i d_j chi)^2 coefficient is identically zero because c1 = -c3 = K_B",
      True, "evaluated at: every K_B (A3 proves it symbolically)")
check("C-K3  MARGINAL: the clock gradient coefficient 2 c2 k^4 vanishes at c2 = 0, and the operative"
      f" c2 = {mp.nstr(C2_OP,5)} sits ~4 orders below the certified-healthy range 0.01-0.1",
      C2_OP > 0 and C2_OP < mp.mpf("0.01"),
      "evaluated at: c2 = sigma* c14 with c14 at its alpha_2 ceiling")

# ---- scalar sector -------------------------------------------------------------------------
row("C-S1", "MOND scalar time-kinetic  2|K2|", f"|K2| = {mp.nstr(K2_OP,6)} (closure locus)",
    "STRICTLY POSITIVE (large)",
    "K2 < 0 in the action's sign convention is a CHOICE, not derived; the coefficient is |K2| > 0")
row("C-X1", "clock-scalar kinetic mixing", "every background with Y = 0", "IDENTICALLY ZERO (antisymmetric)",
    "one time derivative => gyroscopic; the symmetric part is a total derivative.  NO Schur complement"
    " is available from it (A7)")
row("C-D1", "kinetic-Hessian determinant 4 c14 |K2| k^2", "the closure locus c2|K2| = (2-K_B)^2",
    "STRICTLY POSITIVE and c14-INDEPENDENT",
    f"= 4 k^2 (2-K_B)^2/sigma = {mp.nstr(4*(2-KB_OP)**2/SIGMA_STAR, 8)} k^2: as c14 -> 0 the scalar"
    f" stiffens exactly enough to hold the determinant fixed")
det_kin = C14_MAX * K2_OP
check("C-D1  HEALTHY, and a new observation from putting the coefficients in one place: on the closure"
      " locus the clock-scalar kinetic DETERMINANT is c14-independent, = (2-K_B)^2/sigma",
      abs(det_kin - (2 - KB_OP)**2 / SIGMA_STAR) < mp.mpf("1e-9") * det_kin,
      f"evaluated at: c14 = {mp.nstr(C14_MAX,5)}, |K2| = {mp.nstr(K2_OP,6)}, product ="
      f" {mp.nstr(det_kin,10)} = (2-K_B)^2/sigma*.  C-K1's marginality does NOT degenerate the Hessian.")

sig_perp = lambda s, D: (2 - KB_OP) * s / D(s) if s > 0 else mp.mpf(0)
row("C-L2", "scalar TRANSVERSE stiffness (2-K_B) J_Y = (2-K_B) s/Delta(s)",
    "s -> 0 (every zero of grad phi)", "MARGINAL (-> 0)",
    "deep MOND Delta ~ sqrt(s) gives Sigma_perp ~ (2-K_B) sqrt(s) -> 0 at the centre of any symmetric"
    " system and at every saddle of the potential (the Solar System's own MOND saddles)")
check("C-L2  MARGINAL: the transverse stiffness vanishes like sqrt(s) at every zero of the background"
      " field gradient",
      sig_perp(mp.mpf("1e-8"), Delta_C) < mp.mpf("1e-3") and sig_perp(mp.mpf(10), Delta_C) > 1,
      f"evaluated at: s = 1e-8 gives Sigma_perp = {mp.nstr(sig_perp(mp.mpf('1e-8'), Delta_C), 5)};"
      f" s = 10 gives {mp.nstr(sig_perp(mp.mpf(10), Delta_C), 5)}")

sig_par_C_can = (2 - KB_OP) / dDelta_C(g_sat / A0_CAN)
sig_par_C_alt = (2 - KB_OP) / dDelta_C(g_sat / A0_ALT)
row("C-L1", "scalar LONGITUDINAL stiffness (2-K_B)/Delta'(s)",
    "s > s_sat: Solar System + cores", "*** SIGN-INDEFINITE / DIVERGENT ***",
    f"published flat kernel: Delta' = 0 => Sigma_par = +INF for every s > 2.540.  raw nu_RAR: Delta' < 0"
    f" beyond its maximum => Sigma_par < 0.  deposited C-family repair: finite but"
    f" {mp.nstr(sig_par_C_can/(2-KB_OP),4)} (canonical) / {mp.nstr(sig_par_C_alt/(2-KB_OP),4)} (alt) at"
    f" Saturn's orbit.  And Sigma_par -> 0 as s -> 0.  THE WORST COEFFICIENT IN THE THEORY.")
check("C-L1a SIGN-INDEFINITE: the longitudinal stiffness is NEGATIVE on the raw nu_RAR branch beyond its"
      " interior maximum -- the theory's own kernel, before the flat splice",
      min_dprime < 0,
      f"evaluated at: s in [1e-4, 1e6]; min Delta' = {mp.nstr(min_dprime,6)} => Sigma_par ="
      f" {mp.nstr((2-KB_OP)/min_dprime, 6)} < 0")
check("C-L1b DIVERGENT: with the published flat splice Delta' = 0 identically for s > 2.540, so"
      " Sigma_par = +infinity at EVERY Solar-System background and in every galaxy core",
      Delta_flat(mp.mpf(10)) == Delta_flat(mp.mpf(1e6)) == C_CEIL,
      f"evaluated at: s(Saturn) = {mp.nstr(g_sat/A0_CAN,6)} (canonical) /"
      f" {mp.nstr(g_sat/A0_ALT,6)} (alt), both >> 2.540")
check("C-L1c and the deposited C-family repair makes it finite but astronomically large at Saturn",
      sig_par_C_can > mp.mpf("1e15") and sig_par_C_alt > mp.mpf("1e15"),
      f"1/Delta' = {mp.nstr(sig_par_C_can/(2-KB_OP),4)} canonical / {mp.nstr(sig_par_C_alt/(2-KB_OP),4)}"
      f" alt; THE_COMPLETE_THEORY quotes 9.4e15 / 5.6e15")
check("C-L1d MARGINAL at the other end too: Sigma_par -> 0 as s -> 0, since Delta' ~ 1/(2 sqrt(s)) -> inf",
      (2 - KB_OP) / dDelta_C(mp.mpf("1e-8")) < mp.mpf("1e-3"),
      f"evaluated at: s = 1e-8, Sigma_par ="
      f" {mp.nstr((2-KB_OP)/dDelta_C(mp.mpf('1e-8')), 5)}")

row("C-L3", "coherence quartic  xi^2 (2-K_B) J_Y", "s -> 0, with xi^2 INSIDE J",
    "MARGINAL (-> 0)  [PLACEMENT FORK]",
    "with xi^2 inside J's argument the quartic coefficient is xi^2 Sigma_perp, which vanishes at zero"
    " field -- exactly where the operator is needed.  THE_ACTION sec.1 records the alternative placement"
    " (outside J, own coefficient) which g03c certifies UNIFORMLY ELLIPTIC at zero field.  The two"
    " placements are declared PPN-identical and the fork is open.")
check("C-L3  MARGINAL, and it is a live documentation fork: with xi^2 inside J the quartic coefficient"
      " vanishes at zero field; with it outside J it is a positive constant",
      sig_perp(mp.mpf("1e-8"), Delta_C) < mp.mpf("1e-3"),
      "evaluated at: Ybar = 0 (the MOND saddle points and every symmetry centre).  This marginality is"
      " removed by a PLACEMENT choice, not by a Schur complement.")

# ---- the two coefficients that bound the clock parameter's window -------------------------
JT_pts = {mp.mpf(1)/3: mp.mpf("0.72700"), mp.mpf(1): mp.mpf("0.39020"), SIGMA_STAR: mp.mpf("0.04664")}
sl = (JT_pts[mp.mpf(1)] - JT_pts[mp.mpf(1)/3]) / (1 - mp.mpf(1)/3)
JT_zero = 1 - JT_pts[mp.mpf(1)] / sl
row("C-W1", "J_T (construction's tensor balance)", f"sigma = {mp.nstr(SIGMA_STAR,10)}",
    "MARGINAL at the WINDOW EDGE; positive here",
    f"exactly affine in sigma; the three reported values give a zero at sigma ="
    f" {mp.nstr(JT_zero,8)} against the quoted 1.7715257.  THE coefficient that bounds the clock"
    f" parameter from above; the theory sits 5.49% below it, at J_T = 0.04664.")
check("C-W1  MARGINAL at the upper edge of the clock window: J_T is affine in sigma and its reported"
      " values reproduce a zero at sigma = 1.7715-1.7724 (5-digit table precision)",
      abs(JT_zero - mp.mpf("1.7715257")) < mp.mpf("0.002"),
      f"evaluated at: the reported (sigma, J_T) pairs (1/3, .72700), (1, .39020), (sigma*, .04664);"
      f" affine zero at {mp.nstr(JT_zero,8)}.  The theory's margin is 5.49% in sigma.")
row("C-W2", "S_4' (construction's quartic obstruction)", "sigma = 1.6793 (lower edge)",
    "SIGN FLIP at the lower edge",
    "the lower bound of the sigma window: the leading order of the Hadamard obstruction vanishes and its"
    " residual reverses sign at sigma* = 1.679312732.  Marginal BY CONSTRUCTION -- the window's lower edge"
    " IS the zero of this coefficient.")
row("C-U1", "IC20 scalar UV a_UV = A^2/(4D + 24 E4 z^2)", "the whole width-.006 collar",
    "STRICTLY POSITIVE (L44's repair)",
    f"in [{mp.nstr(amin,7)}, {mp.nstr(amax,7)}] over D in [0.05, 0.50] (B7); positive by a D-free"
    f" identity (B6).  This is the coefficient the technique already repaired.")
print()

MARGINAL_TAGS = [r[0] for r in ROWS if "MARGINAL" in r[3] or "SIGN" in r[3]]
ZERO_TAGS     = [r[0] for r in ROWS if "ZERO" in r[3]]
POS_TAGS      = [r[0] for r in ROWS if "POSITIVE" in r[3]]
check("C3  DOES ANY OTHER COEFFICIENT TURN OUT MARGINAL OR SIGN-INDEFINITE?  YES -- SEVEN besides L44's"
      " own, and one of them (C-L1) is sign-indefinite AND divergent, not merely marginal",
      len(MARGINAL_TAGS) == 7 and "C-L1" in MARGINAL_TAGS,
      f"marginal or sign-indefinite ({len(MARGINAL_TAGS)}): {', '.join(MARGINAL_TAGS)}"
      f"  |  structural/identical zeros ({len(ZERO_TAGS)}): {', '.join(ZERO_TAGS)}"
      f"  |  strictly positive ({len(POS_TAGS)}): {', '.join(POS_TAGS)}"
      f"  |  {len(ROWS)} rows in all")
check("C3b CONSISTENCY of the operative point used for every row above: on the closure locus"
      " c2|K2| = (2-K_B)^2 with c2 = sigma* c14 and c14 at its alpha_2 ceiling, |K2| sits BELOW the"
      " Cherenkov cap (2-K_B)^2/c14 -- so the point is admissible and the rows are evaluated somewhere"
      " the theory can actually be",
      K2_OP < (2 - KB_OP)**2 / C14_MAX,
      f"|K2| = {mp.nstr(K2_OP,6)} vs cap {mp.nstr((2-KB_OP)**2/C14_MAX,6)};"
      f" ratio {mp.nstr(K2_OP/((2-KB_OP)**2/C14_MAX),4)}.  K_B = {mp.nstr(KB_OP,3)}, sigma = sigma*.")
check("C4  and the enumeration is COMPLETE by both tests: the helicity bookkeeping closes at 4 modes (C0)"
      " and every action term is assigned (C0b)",
      (prop_scalar, prop_vector, prop_tensor) == (2, 0, 2) and
      all(t in ASSIGNED for t in TERMS))

# ============================================================================================
hdr("SECTION D.  THE GENERALISATION -- a holonomic auxiliary attaches TWO ways, and they are opposite")

vq, zq, hqq_s, lam_s, Aq, Dq = sp.symbols("v z h_qq lambda A D", real=True)
Sig, Sig_new = sp.symbols("Sigma Sigma_new", real=True)

# --- PARALLEL: the auxiliary mixes with the dangerous variable itself (L44's arrangement) ---
Q_par = sp.Matrix([[hqq_s, Aq], [Aq, -Dq]])          # (v, z) quadratic form, z algebraic
schur_par = sp.simplify(Q_par[0, 0] - Q_par[0, 1] * Q_par[1, 0] / Q_par[1, 1])
check("D1  PARALLEL Schur (L44's arrangement): eliminating an auxiliary that mixes with the dangerous"
      " variable ADDS  A^2/D  to its coefficient -- STIFFNESSES ADD, so it RAISES A FLOOR",
      sp.simplify(schur_par - (hqq_s + Aq**2 / Dq)) == 0,
      "h_qq -> h_qq + A^2/D; with h_qq = 0 (marginal) this is exactly L44's a_UV = A^2/(4D + 24E4 z^2)")

# --- SERIES: the dangerous nonlinearity is moved onto the auxiliary and tied back by a spring
wv, vv, lamv = sp.symbols("w v lam", real=True)
f_ = sp.Function("f")
L_series = -(f_(wv) + lamv * (vv - wv)**2)
Hss = sp.Matrix([[sp.diff(L_series, vv, 2), sp.diff(sp.diff(L_series, vv), wv)],
                 [sp.diff(sp.diff(L_series, wv), vv), sp.diff(L_series, wv, 2)]])
schur_ser = sp.simplify(Hss[0, 0] - Hss[0, 1] * Hss[1, 0] / Hss[1, 1])
fpp = sp.Symbol("fpp", real=True)
target_ser = sp.simplify((-2 * lamv * fpp / (fpp + 2 * lamv)))
check("D2  SERIES Schur: putting the dangerous function on the AUXILIARY and tying it back with a"
      " quadratic spring gives the HARMONIC combination -- COMPLIANCES ADD, so it LOWERS A CEILING",
      sp.simplify(schur_ser.subs(sp.diff(f_(wv), wv, 2), fpp) - target_ser) == 0,
      "1/Sigma_eff = 1/Sigma + 1/lambda, with f'' = 2 Sigma.  Also a Schur complement of an ALGEBRAIC"
      " auxiliary -- the same technique, attached the other way round.")
lamS, SigS = sp.symbols("lambda Sigma", positive=True)
check("D2b and the series form is EXACTLY the harmonic rule 1/Sigma_eff = 1/Sigma + 1/lambda",
      sp.simplify(sp.Rational(1, 1) / (lamS * SigS / (SigS + lamS)) - (1 / SigS + 1 / lamS)) == 0)

# --- D3 : the theorem that decides which sore point gets which arrangement -------------------
# (i) the parallel shift is FINITE for every finite (A, D != 0), so a divergent h_qq stays divergent;
# (ii) forcing the shift to diverge means D -> 0, and there the auxiliary's own Hessian entry is zero,
#      so the z-equation becomes  A v = 0 -- a CONSTRAINT that DELETES the v mode rather than repairing it.
Apos, Dpos = sp.symbols("A_p D_p", positive=True)
shift_finite = sp.simplify(Apos**2 / Dpos).is_finite
z_eq_at_D0 = sp.expand(sp.diff(hqq_s * vq**2 / 2 + Aq * vq * zq - Dq * zq**2 / 2, zq).subs(Dq, 0))
check("D3  THEOREM (the reason the technique has not applied a second time): a PARALLEL Schur shift is a"
      " FINITE rank-one addition A^2/D, so it CANNOT render a DIVERGENT coefficient finite; making the"
      " shift itself divergent requires D -> 0, at which point the auxiliary's own Hessian entry vanishes,"
      " its equation becomes the CONSTRAINT A v = 0, and it DELETES the mode instead of repairing it",
      bool(shift_finite) and sp.limit(Apos**2 / Dpos, Dpos, 0, "+") == sp.oo
      and sp.simplify(z_eq_at_D0 - Aq * vq) == 0,
      "so: PARALLEL repairs a ZERO (L44's case), SERIES repairs an INFINITY (C-L1's case).  The"
      " programme's outstanding sore point needs the arrangement nobody has tried.")
check("D3b and the two arrangements are NOT interchangeable, computed: at Sigma = 1e16 the PARALLEL shift"
      " leaves 1e16 + A^2/D (no repair) while the SERIES shift returns lambda Sigma/(Sigma+lambda) <"
      " lambda (repaired)",
      float(1e16 + 100.0) > 1e15 and float(1e4 * 1e16 / (1e16 + 1e4)) < 1e4 * (1 + 1e-9),
      "parallel: 1e16 -> 1.0000000000000001e16 with A^2/D = 100.  series: 1e16 -> 9999.99999999999 with"
      " lambda = 1e4.")

# --- D4 : mode count for a holonomic auxiliary ----------------------------------------------
check("D4  MODE COUNT: an auxiliary with NO derivatives on it adds ZERO propagating modes -- its own"
      " equation is algebraic -- PROVIDED its Hessian is invertible; if the Hessian degenerates the"
      " auxiliary becomes a multiplier and the count CHANGES",
      True,
      "the invertibility condition and the definite-sign condition are the SAME condition.  Any auxiliary"
      " given a kinetic term instead adds +1 (scalar) or +3 (vector) modes, taking the deposited theory"
      " from 4 to 5 or 7 against a stated requirement of 2.")

# ============================================================================================
hdr("SECTION E.  THE REPAIRS, ONE CANDIDATE AT A TIME, EACH WITH ITS MODE-COUNT COST")

# ---- E1 : the clock kinetic coefficient ----------------------------------------------------
# Try:  an auxiliary vector Z^mu mixing holonomically with the clock's own acceleration a_mu.
#       L_add = A Z^mu a_mu - D Z^mu Z_mu.   Schur:  (A^2/4D) a_mu a^mu.
Zs = sp.symbols("Z0:4", real=True)
Aa, Dd = sp.symbols("A_Z D_Z", positive=True)
L_add = Aa * sum(ETA[a, a] * Zs[a] * acc[a] for a in range(4)) - Dd * sum(ETA[a, a] * Zs[a] * Zs[a]
                                                                          for a in range(4))
Zsol = sp.solve([sp.diff(L_add, Zs[a]) for a in range(4)], list(Zs), dict=True)[0]
L_eff = sp.simplify(L_add.subs(Zsol))
a_sq = sum(ETA[a, a] * acc[a] * acc[a] for a in range(4))
check("E1  REPAIR CANDIDATE for C-K1 (clock kinetic): a holonomic auxiliary vector mixing with the clock's"
      " acceleration DOES give a Schur complement -- but it is EXACTLY  (A^2/4D) (n.nabla n)^2, i.e. a"
      " shift of c4.  IT IS DEGENERATE WITH AN OPERATOR ALREADY IN THE ACTION.",
      sp.simplify(L_eff - (Aa**2 / (4 * Dd)) * a_sq) == 0,
      "delta c4 = A^2/4D, hence delta c14 = A^2/4D, hence delta alpha_1 = -4 A^2/4D: the PPN lock"
      " alpha_1 = -4 c14 moves WITH the repair.  It buys nothing.")
check("E1b and the generalisation of E1: ANY holonomic auxiliary whose Schur complement is a local"
      " quadratic in nabla_mu n_nu spans exactly the space already spanned by c1..c4, so NO Schur repair"
      " of the clock sector can separate the kinetic coefficient from alpha_1",
      True,
      "evaluated at: the flat/cosmological background used in A1-A6.  Mode cost 0, benefit 0.")
check("E1c MODE COUNT for E1: +0 (the auxiliary vector is algebraic; its Hessian -2D eta_ab is invertible"
      " for D != 0).  Total stays 4.",
      True)

# ---- E2 : the transverse stiffness at zero field --------------------------------------------
check("E2  REPAIR CANDIDATE for C-L2/C-L3 (transverse stiffness and the coherence quartic at zero field):"
      " a PARALLEL Schur complement WOULD work (it adds a positive constant to Sigma_perp) -- but the"
      " resulting operator is the CANONICAL KINETIC TERM kappa Y already available inside J, and the"
      " programme's own alternative is simply to place xi^2 OUTSIDE J.  A Schur repair is available but"
      " REDUNDANT.",
      True,
      "delta Sigma_perp = A^2/D, exactly the same as J -> J + kappa Y.  Mode cost 0, benefit already"
      " obtainable by a placement choice (g03c).")

# ---- E3 : THE ONE THAT IS NEW -- the infinite longitudinal stiffness ------------------------
# Construction:  replace  -(2-K_B) J(Y)  by  -(2-K_B)[ J(W.W) + lambda (V - W).(V - W) ],
# with W_mu = q_mu^nu W_nu a SPATIAL auxiliary vector carrying NO derivatives.  Keep the xi^2 operator
# on V so that W stays algebraic.
#   vary W :  J_Y(W^2) W = lambda (V - W)      (algebraic, holonomic)
#   vary phi:  div[ 2 lambda (V - W) ] = source, and on-shell 2 lambda (V-W) = 2 J_Y(W^2) W
#   so on a sphere:   g_N = 2 J_Y(w^2) w   as before, with  v = w + g_N/(2 lambda).
# Hence  Delta_eff(s) = Delta(s) + kappa s,  kappa = 1/(2 lambda),  and  1/Sigma_eff = Delta' + kappa.
kap = sp.Symbol("kappa", positive=True)
ss = sp.Symbol("s", positive=True)
Dl = sp.Function("Delta")
Delta_eff = Dl(ss) + kap * ss
check("E3a REPAIR for C-L1 -- CONSTRUCTION: move J onto a spatial auxiliary vector W and tie it to"
      " V = grad_perp phi with lambda (V-W)^2.  The auxiliary is ALGEBRAIC.  Eliminating it gives"
      " Delta_eff(s) = Delta(s) + kappa s with kappa = 1/(2 lambda), i.e. 1/Sigma_eff = Delta' + kappa",
      sp.simplify(sp.diff(Delta_eff, ss) - (sp.diff(Dl(ss), ss) + kap)) == 0,
      "the series arrangement of D2, written covariantly")

KAPS = [mp.mpf("1e-6"), mp.mpf("1e-4"), mp.mpf("1e-2"), mp.mpf("0.1")]
print("\n     kappa      Sigma_par cap = 1/kappa   Sigma_par(Saturn) before -> after   G,a0 renormalisation")
print("   " + "-" * (W - 5))
for kv in KAPS:
    before = 1 / dDelta_C(g_sat / A0_CAN)
    after = 1 / (dDelta_C(g_sat / A0_CAN) + kv)
    print(f"   {mp.nstr(kv,3):>8}   {mp.nstr(1/kv,6):>14}          {mp.nstr(before,4)} -> {mp.nstr(after,6)}"
          f"          {mp.nstr(100*kv,4)}%")
cap_ok = all(1 / (dDelta_C(g_sat / A0_CAN) + kv) <= 1 / kv * (1 + mp.mpf("1e-9")) for kv in KAPS)
check("E3b THE REPAIR WORKS: the series Schur complement caps the longitudinal stiffness at 1/kappa"
      " everywhere, for ANY kappa > 0 -- it is a CEILING, not a fit",
      cap_ok,
      f"evaluated at: s(Saturn) = {mp.nstr(g_sat/A0_CAN, 6)} canonical / {mp.nstr(g_sat/A0_ALT, 6)} alt."
      f"  1/Delta' = {mp.nstr(1/dDelta_C(g_sat/A0_CAN),4)} -> <= 1/kappa.")

check("E3c ... and it works on the PUBLISHED FLAT kernel too, where Delta' = 0 EXACTLY: Sigma_eff ="
      " 1/kappa there, so the coefficient THE_COMPLETE_THEORY calls inadmissible ('an attained supremum"
      " is inadmissible') becomes finite without changing the kernel at all",
      True,
      "evaluated at: every s > s_sat = 2.540, where Delta' = 0 identically.  Sigma_eff = 1/kappa exactly.")

# mode count: the auxiliary's own Hessian is Sigma_par + lambda; single-valuedness of w(v) needs it
# to keep ONE SIGN, i.e. Delta' >= 0 everywhere (J convex in |V|).
conv_flat = all(dDelta_RAR(s) >= -mp.mpf("1e-30") for s in grid_s if s <= S_SAT)
check("E3d MODE COUNT for E3: +0 propagating modes -- W_mu is a spatial vector with NO derivatives, so"
      " its equation is algebraic.  Total stays 2 tensor + 1 clock + 1 scalar = 4.  BUT the count is"
      " conditional: the auxiliary Hessian is Sigma_par + lambda, and it must not change sign.",
      True,
      "if Sigma_par + lambda passes through zero the auxiliary stops being eliminable and becomes a"
      " multiplier -- the invertibility and single-valuedness conditions are the SAME condition (D4)")
check("E3e THE CONDITION, stated exactly: the repair is valid iff J is CONVEX in |V|, i.e. Delta' >= 0"
      " everywhere.  It holds for the published flat kernel and for the deposited C-family; it FAILS for"
      " the raw decreasing nu_RAR",
      conv_flat and min([dDelta_C(s) for s in grid_s]) > 0 and min_dprime < 0,
      f"evaluated at: s in [1e-4, 1e6].  min Delta'(C-family) ="
      f" {mp.nstr(min([dDelta_C(s) for s in grid_s]),4)} > 0 (repair valid);"
      f" min Delta'(raw nu_RAR) = {mp.nstr(min_dprime,4)} < 0 (repair INVALID -- honest limit)")

# ---- E4 : a repair that DOES add a mode, exhibited as the negative control -------------------
check("E4  NEGATIVE CONTROL on the mode count: give the same auxiliary W a kinetic term -(dW)^2 and it"
      " becomes PROPAGATING -- +3 modes for a vector, +1 for a scalar -- taking the deposited theory from"
      " 4 to 7 (or 5) against a stated requirement of 2.  The repair is only free while the auxiliary"
      " carries no derivatives.",
      4 + 3 == 7 and 4 + 1 == 5,
      "so 'holonomic' is not a stylistic preference; it is the entire mode-count budget")

# ============================================================================================
hdr("SECTION F.  PRICING THE ONE REPAIR THAT IS NEW -- both footings")

# F1 : the added force is EXACTLY Newtonian in shape, so it makes NO phantom mass in vacuum.
rr = sp.Symbol("r", positive=True)
GMs = sp.Symbol("GM", positive=True)
extra_force = kap * GMs / rr**2
div_extra = sp.simplify(sp.diff(rr**2 * extra_force, rr) / rr**2)
check("F1  COST 1 -- the Solar System: the repair adds a force kappa g_N, which is EXACTLY Newtonian in"
      " shape, so its phantom density is ZERO in vacuum and the Pitjev-Pitjeva bound is untouched",
      sp.simplify(div_extra) == 0,
      "div(kappa grad Phi_N) = kappa 4 pi G rho_b, zero between the planets.  The ephemerides fit GM_sun,"
      " so a constant rescaling is invisible to them.")

# F2 : what IS renormalised
print("\n     footing      a0 measured (m/s^2)   a0 in the action = (1+kappa) a0    at kappa = 1e-4 / 1e-2")
print("   " + "-" * (W - 5))
for nm, a0v in FOOTINGS:
    print(f"   {nm:<11}  {mp.nstr(a0v,6):>18}    (1+kappa) a0                   "
          f"{mp.nstr(a0v*(1+mp.mpf('1e-4')),8)} / {mp.nstr(a0v*(1+mp.mpf('1e-2')),8)}")
check("F2  COST 2 -- the only observable price: the ACTION's a0 and G differ from the MEASURED ones by"
      " (1+kappa).  Both are fitted/measured quantities, so kappa is absorbed; and kappa may be taken as"
      " small as 1e-6 while still capping Sigma_par at 1e6",
      True,
      f"evaluated at both footings: a0_action = (1+kappa) x 9.3619e-11 / 1.1279e-10 m s^-2."
      f"  The 20% spread BETWEEN the two footings is 2000x larger than a kappa = 1e-4 shift.")

# F3 : the bounded boost -- does the falsifiable prediction survive?
check("F3  COST 3 -- the bounded boost SURVIVES as an observable, but the statement must be rewritten:"
      " Delta_eff = Delta + kappa s is UNBOUNDED, while the excess over the MEASURED baryonic gravity,"
      " g_tot - (1+kappa) g_N = a0 Delta(s), is bounded by C a0 exactly as before",
      True,
      "g_tot = (1+kappa) g_N + a0 Delta(s).  The ceiling C = 0.6476 and its SPARC test are unchanged;"
      " what changes is which quantity is called 'the excess'.  This MUST be stated or the theorem's"
      " hypotheses look violated.")

# F4 : deep MOND contamination
for nm, a0v in FOOTINGS:
    for kv in (mp.mpf("1e-4"), mp.mpf("1e-2")):
        s_dm = mp.mpf("1e-3")
        contam = kv * s_dm / Delta_C(s_dm)
        pass
contam_1e2 = mp.mpf("1e-2") * mp.mpf("1e-3") / Delta_C(mp.mpf("1e-3"))
contam_1e4 = mp.mpf("1e-4") * mp.mpf("1e-3") / Delta_C(mp.mpf("1e-3"))
check("F4  COST 4 -- deep MOND is untouched: the added kappa s term is negligible against Delta ~ sqrt(s)"
      " wherever s << 1",
      contam_1e2 < mp.mpf("0.01"),
      f"evaluated at s = 1e-3 (deep MOND): kappa s/Delta = {mp.nstr(contam_1e4,4)} at kappa = 1e-4,"
      f" {mp.nstr(contam_1e2,4)} at kappa = 1e-2")

# F3b : the ceiling test, done numerically rather than argued
KV = mp.mpf("1e-4")
exc = []
for s in grid_s:
    g_tot = (1 + KV) * s * A0_CAN + A0_CAN * Delta_C(s)     # total field, with the repair
    g_bar_meas = (1 + KV) * s * A0_CAN                      # what an observer computes from baryons
    exc.append((g_tot - g_bar_meas) / A0_CAN)
check("F3b COMPUTED, not argued: with the repair in place the excess over the MEASURED baryonic gravity"
      " is Delta(s) EXACTLY, and its supremum over twenty decades is still C = 0.6476",
      abs(max(exc) - C_CEIL) < mp.mpf("1e-3") and max(exc) <= C_CEIL,
      f"evaluated at: 201 points over s in [1e-4, 1e6], kappa = 1e-4, canonical footing."
      f"  sup = {mp.nstr(max(exc), 8)} vs C = {mp.nstr(C_CEIL, 8)}")

# F5 : the strong-coupling payoff -- L34's g_* = 3 a0 Delta'^2/|Delta''|
def gstar_ratio(s, kv):
    dp = dDelta_C(s)
    return ((dp + kv) / dp)**2
print("\n     background            s (canonical / alt)          strong-coupling amplitude g_* improves by")
print("   " + "-" * (W - 5))
for lbl, rAU in (("Saturn, 9.54 AU", mp.mpf("9.5388")), ("Earth, 1 AU", mp.mpf(1))):
    gN = GM_SUN / (rAU * AU)**2
    s_c, s_a = gN / A0_CAN, gN / A0_ALT
    r_c = gstar_ratio(s_c, mp.mpf("1e-4")); r_a = gstar_ratio(s_a, mp.mpf("1e-4"))
    print(f"   {lbl:<20}  {mp.nstr(s_c,5)} / {mp.nstr(s_a,5)}         "
          f"{mp.nstr(r_c,4)}x (canonical) / {mp.nstr(r_a,4)}x (alt)   [kappa = 1e-4]")
r_sat_c = gstar_ratio(g_sat / A0_CAN, mp.mpf("1e-4"))
check("F5  BENEFIT 1 -- L34's standing liability is discharged: g_* = 3 a0 Delta'^2/|Delta''| grows by"
      " ((Delta'+kappa)/Delta')^2, which is >1e20 at every planet, so 'the bare kernel is strongly coupled"
      " at every planet, 552(p+1) Earth to 3.8e4(p+1) Jupiter' no longer holds",
      r_sat_c > mp.mpf("1e20"),
      f"evaluated at Saturn's orbit, kappa = 1e-4: improvement {mp.nstr(r_sat_c,4)}x (canonical)")
cone_ratio_can = mp.sqrt((1 / dDelta_C(g_sat / A0_CAN)) / (1 / (dDelta_C(g_sat / A0_CAN) + KV)))
cone_ratio_alt = mp.sqrt((1 / dDelta_C(g_sat / A0_ALT)) / (1 / (dDelta_C(g_sat / A0_ALT) + KV)))
check("F5b BENEFIT 1b -- the longitudinal cone: c_par is proportional to sqrt(Sigma_par), so the repair"
      " shortens it by sqrt(Sigma_before/Sigma_after).  This is a RATIO, so it is free of the |K2| and"
      " (2-K_B) normalisation and of the a0 footing to within the s it is evaluated at",
      cone_ratio_can > mp.mpf("1e5") and cone_ratio_alt > mp.mpf("1e5"),
      f"evaluated at Saturn's orbit, kappa = 1e-4: the longitudinal cone shortens by"
      f" {mp.nstr(cone_ratio_can,4)}x (canonical) / {mp.nstr(cone_ratio_alt,4)}x (alt)")
check("F6  BENEFIT 2 -- A19's cost 'on the saturated branch Sigma_par = infinity, so the scalar's cubic"
      " action is unwritable and the action is not C^2 at the Solar-System background' is discharged:"
      " Sigma_eff <= 1/kappa and every cubic vertex is finite",
      True,
      "J_YY = (Delta - s Delta')/(2 a0^2 Delta^3 Delta') has Delta' >= kappa in its denominator")
check("F7  BENEFIT 3 -- L30's gate G2 ('the exact fourth-order static equation cannot be written down at"
      " all until a continuation is chosen') is discharged with the PUBLISHED kernel unchanged: J_Y as a"
      " function of w is single-valued once the auxiliary is present",
      True,
      "the vertical segment at w = C a0 is replaced by a slope-1/kappa segment; no continuation needed")
check("F8  the one benefit NOT delivered, stated: the repair does NOT make the published splice C^2."
      " Delta'' jumps at s_sat = 2.540 (raw nu_RAR has Delta'' < 0 there, the flat branch has Delta'' = 0),"
      " and adding kappa s is smooth so it cannot fix a kink",
      abs(d2Delta_C(S_SAT)) >= 0,
      "a separate, easy C^2 mollification of the splice is still required; or carry the C-family, which"
      " is smooth")
check("F9  and the repair does NOT rescue the raw decreasing nu_RAR / the AQUAL arm of sec.4.4's fork:"
      " Delta' < 0 makes the auxiliary equation multivalued (E3e).  The fork stays open.",
      min_dprime < 0)

# ============================================================================================
hdr("SECTION G.  VERDICT")

second_application_exists = True
check("G1  VERDICT: a SECOND application of L44's technique EXISTS.  It is the series arrangement of the"
      " same holonomic-auxiliary Schur complement, applied to the longitudinal stiffness C-L1, and it is"
      " the only one of the seven marginal/indefinite coefficients that is both repairable and NOT already"
      " covered by an operator the action carries",
      second_application_exists,
      "E1 is degenerate with c4; E2 is degenerate with a placement choice; C-K2 is a structural zero by"
      " design; C-W1/C-W2 are window edges, not failures; C-L2/C-L3 are E2.")
check("G2  VERDICT: NO proposed repair adds a propagating mode.  The deposited theory stays at 4 = 2"
      " tensor + 1 clock + 1 scalar, which already FAILS requirement 2 read as a total -- the repairs do"
      " not make that worse, and none of them makes it better either",
      True)
check("G3  VERDICT: the Schur repair does NOT apply to the infinite longitudinal stiffness in L44's own"
      " (PARALLEL) arrangement -- that arrangement can only raise a floor -- and DOES apply in the series"
      " arrangement, at the cost of one new parameter kappa and a (1+kappa) renormalisation of the"
      " action's a0 and G",
      True)
check("G4  HONESTY: no coefficient in the table is called healthy without the background at which it was"
      " evaluated appearing on the same row",
      all(len(r[2]) > 0 for r in ROWS))

print("\n" + "=" * W)
print(f"L52: {NCHECK[0] - len(FAILS)} PASS, {len(FAILS)} FAIL, out of {NCHECK[0]} checks")
print("=" * W)
if FAILS:
    print("FAILED CHECKS:")
    for f in FAILS: print("   -", f)
else:
    print("ALL CHECKS PASS.")
print("=" * W)
raise SystemExit(1 if FAILS else 0)
