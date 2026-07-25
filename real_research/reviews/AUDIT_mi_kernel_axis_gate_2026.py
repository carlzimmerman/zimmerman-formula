#!/usr/bin/env python3
r"""
ADVERSARIAL AUDIT of reviews/mi_kernel_axis_separation_omegac_2026.py
=====================================================================
de Sitter-Unruh MODIFIED-INERTIA framework (Carl Zimmerman).  Judged on ITS OWN terms: no McGaugh nu,
no standard-MOND lens, no covariant PDE work -- closed form + numerics only.

THE OBJECT UNDER AUDIT.  A prior workflow settled the "gate pincer" on the omega_c crossover and
committed mi_kernel_axis_separation_omegac_2026.py (commit 1c82c6ac).  Its load-bearing claims:
  (P1) Box_u is DIAGONAL on u with eigenvalues {0, -(gamma Omega)^2} (the handed-in "eigenvalue" lead,
       with its dimensions corrected: z = -(omega c/a0)^2, NOT -(omega/a0)^2).
  (P2) K on the NEGATIVE (frequency) axis has |K| = 1 exactly; arg K -> a0/(2 c omega).
  (P3) Therefore the galactic TANGENTIAL coefficient is sin(arg K) = 2.63e-05 (canon) / 3.17e-05 (alt),
       NOT the phenomenological gate's |Im G| = 0.300 -- so Reading A's 42-58 Myr galactic catastrophe
       is a GATE ARTIFACT, and the binding deep-MOND orbit e-folds in 550 / 398 Gyr instead.
  (P4) omega_c is NOT redundant (three K-only channels tested, none passes both halves).
  (P5) A frequency gate cannot separate the RAR from the a0/2 tail because both are DC/closure objects.
  (P6) An INTERMEDIATE double-pole overlay DOES open a non-empty window, at a named price.

MY ROLE: hunt a manufactured RESCUE and a manufactured KILL with EQUAL force.  Specifically
  (1) re-derive Box_u u^mu on an explicit circular worldline MYSELF -- is it really an eigenvalue
      relation, or only for the spatial part / only in a particular frame?
  (2) check the retarded branch (z -> z + i0) was applied on the correct sheet;
  (3) test whether the small tangential coefficient was BOUGHT by mixing channels (phase from the
      vector axis, amplitude from the DC axis) with the gate quietly dropped -- and whether the loop
      was CLOSED (gate re-inserted for the planets, galactic force recomputed);
  (4) test whether Reading A's 0.300 was assumed rather than derived;
  (5) demand the redundancy test be closed over the WHOLE channel family, not 3 hand-picked ones;
  (6) check the DC-vs-DC point was faced, not evaded.

FOUR THINGS THIS AUDIT ADDS RATHER THAN RE-PRINTS (each is a new, exact result):
  (A) A curvilinear/boost robustness test of (P1): the eigen-split is well defined ONLY in a
      PARALLEL-PROPAGATED frame (in cylindrical coordinates every component of u is CONSTANT, yet
      Box_u u != 0).  It IS Lorentz-invariant.  The lead AS LITERALLY WRITTEN (Box_u u = -Omega^2 u)
      is FALSE; the block form is exact.
  (B) An EXACT closed form for the kernel-channel galactic e-folding time,
          t_e = (2c/a0) * g_obs/(g_obs - g_bar)  >=  2c/a0 = 203 Gyr (canon) / 168 Gyr (alt),
      a UNIVERSAL floor over every circular orbit.  This matters because the kernel's coefficient
      GROWS as 1/Omega, so the gate's binding orbit (the FASTEST deep-MOND orbit) is the kernel's most
      FAVOURABLE one -- a live cherry-pick risk in (P3).  The floor closes it, orbit-independently, and
      it lands exactly on the paper's OWN quoted memory time tau_mem = 2c/a0.  Third pin on (P1)'s
      dimensional correction.
  (C) A CHANNEL-FAMILY closure of (P4): |1 - K(-Y+i0)| = sqrt(2 - 2 sqrt(1 - 1/(4Y))) is strictly
      DECREASING in Y, so K approaches the identity at HIGH frequency.  Every K-only response therefore
      suppresses GALAXIES more than PLANETS -- the separation runs backwards by ~1.1e6.  Robust to the
      channel enumeration, which the 3-channel table was not.
  (D) A SIGN clash the prior script did not report: in the record's OWN Fourier convention (C1,
      phasors e^(+i omega t)) Im G < 0 while Im K > 0 on the same retarded sheet, so the kernel's
      tangential force has the OPPOSITE SENSE to the gate's.  Magnitudes unaffected.

CALIBRATION HELD (Carl's standing rule; manufacture NEITHER a kill NOR a rescue):
  * Both a0 footings on every load-bearing number (canon 9.355e-11 = cH_Lambda/Z; alt 1.13e-10).
  * No verdict string is hard-coded: every PASS/FAIL/EMPTY/OPEN below is computed from the numbers.
  * Prove-by-moving-the-number on the one load-bearing convention (the c-factors).
  * Bears on the GATE ONLY.  The MOND premise, a0 = cH_Lambda/Z, the RAR and the a0-line are untouched.
  * No TOE language.  Never "theory closed".  sympy + numpy + scipy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

C_LIGHT  = 2.99792458e8
A0_CANON = 9.355e-11
A0_ALT   = 1.13e-10
FOOTINGS = (("canon", A0_CANON), ("alt", A0_ALT))
YR       = 365.25 * 86400.0
GYR      = 1e9 * YR
KPC      = 3.0857e19
AU       = 1.495978707e11
GM_SUN   = 1.32712440018e20
GM_EARTH = 3.986004418e14

OMEGA_GAL    = 5.9414e-15          # UGC05721 innermost deep-MOND orbit (paper Sec. 5.2 lower edge)
R_GAL, V_GAL = 0.09 * KPC, 16.5e3
OMEGA_C_LO   = 1.7824e-14          # 3 x OMEGA_GAL  <=>  Re G >= 0.90 (footing-independent)
OMEGA_C_HI   = {"canon": 2.2113e-14, "alt": 1.8306e-14}   # LLR Gdot/G ceiling
GATE_KEEP    = 0.90
OMEGA_MOON   = np.sqrt(GM_EARTH / 3.844e8 ** 3)
V_MOON       = OMEGA_MOON * 3.844e8
LLR_ALLOW    = (5.0 + 2 * 9.6) * 1e-15 / YR      # Biskupek & Mueller 2021, |cen| + 2 sigma, per second
PLANETS = {  # name: (semi-major axis [m], period [d], eccentricity, Fienga & Minazzoli 2024 dg [m/s^2])
    "Mercury": (5.7909e10,  87.9691, 0.20563, 4.6e-14),
    "Earth":   (1.4960e11, 365.256,  0.01671, 8.7e-15),
    "Mars":    (2.2794e11, 686.980,  0.09341, 1.4e-15),
    "Saturn":  (1.43353e12, 10759.22, 0.05648, 7.0e-15),
}
PRIOR = {  # the committed numbers this audit must independently confirm or contradict
    "argK_canon": 2.626e-05, "argK_alt": 3.172e-05, "ImG_edge": 0.300,
    "efold_canon_Gyr": 550.2, "efold_alt_Gyr": 398.3,
    "wc_need_canon": 4.112e-12, "wc_need_alt": 4.703e-12, "over_canon": 186, "over_alt": 257,
    "branch_pt_canon": 1.5602e-19, "Y_gal_canon": 3.6252e8,
    "dpole_canon": (8.224e-12, 8.270e-11), "dpole_alt": (9.405e-12, 7.525e-11),
    "cs": {"Mercury": 1.0866, "Earth": 1.0006, "Mars": 1.0175, "Saturn": 1.0064},
    "tau_mem_Gyr": {"canon": 203.0, "alt": 168.0},   # paper Sec. 5.3, quoted
}
FINDINGS = []
def log(n, verdict, what, evid):
    FINDINGS.append((n, verdict, what, evid))
    print(f"\n  >>> FINDING {n} [{verdict}] {what}\n      {evid}")

def gbar_from_gobs(gobs, a0):
    """exact a0-line inversion of g_obs^2 - g_bar^2 = a0 g_bar."""
    return (-a0 + np.sqrt(a0 ** 2 + 4.0 * gobs ** 2)) / 2.0
def Y_of(omega, a0):    return (omega * C_LIGHT / a0) ** 2
def ImK_neg(omega, a0): return 1.0 / (2.0 * np.sqrt(Y_of(omega, a0)))      # = sin(arg K), EXACT
def ReK_neg(omega, a0):
    Y = Y_of(omega, a0)
    return np.sqrt(4.0 * Y - 1.0) / (2.0 * np.sqrt(Y))
def one_minus_ReK(omega, a0):
    """1 - Re K = 1 - sqrt(1-x), x = 1/(4Y), written so it does not cancel at planetary Y ~ 1e20."""
    x = 1.0 / (4.0 * Y_of(omega, a0))
    return float(x / (1.0 + np.sqrt(1.0 - x)))
def abs_1_minus_K(omega, a0):
    """|1 - K(-Y+i0)| = sqrt(2 (1 - Re K)), same stable rewrite."""
    return float(np.sqrt(2.0 * one_minus_ReK(omega, a0)))

# =====================================================================================================
head("1.  AUDIT ITEM (1): RE-DERIVE Box_u u^mu MYSELF.  Is the 'eigenvalue' relation real?")
# =====================================================================================================
tau, Om, R0, bet = sp.symbols("tau Omega R_0 beta", positive=True)
gam = 1 / sp.sqrt(1 - R0 ** 2 * Om ** 2)
ph  = gam * Om * tau
eta = sp.diag(-1, 1, 1, 1)

# --- route 1: explicit Cartesian helix, built from the SPATIAL orbit (not copied from the prior script)
xC = sp.Matrix([gam * tau, R0 * sp.cos(ph), R0 * sp.sin(ph), 0])      # worldline x^mu(tau)
uC = sp.simplify(sp.diff(xC, tau))
nrm = sp.simplify((uC.T * eta * uC)[0, 0])
aC  = sp.simplify(sp.diff(uC, tau))
bxC = sp.simplify(sp.diff(aC, tau))                                   # flat Cartesian: Gamma = 0
a2  = sp.simplify((aC.T * eta * aC)[0, 0])
mom1 = sp.simplify((uC.T * eta * bxC)[0, 0])
print(f"""
  Route 1 -- built from the SPATIAL orbit x^mu(tau) = (gamma tau, R0 cos(gamma Omega tau),
  R0 sin(gamma Omega tau), 0), then u = dx/dtau (so the worldline, not the 4-velocity, is the input):
      u.u                    = {nrm}                     (unit norm, exact)
      |a|^2                  = {a2}
      u_mu Box_u u^mu        = {mom1}
      u_mu Box_u u^mu + |a|^2 = {sp.simplify(mom1 + a2)}   <== first-moment identity, INDEPENDENTLY reproduced
""")
assert sp.simplify(nrm + 1) == 0 and sp.simplify(mom1 + a2) == 0

# --- THE LEAD AS LITERALLY WRITTEN: is Box_u u^mu = -Omega^2 u^mu ?
lam = sp.symbols("lambda")
resid_u = sp.simplify(bxC - lam * uC)
sol_lam = sp.solve([sp.Eq(sp.simplify(bxC[0] - lam * uC[0]), 0)], lam, dict=True)
u_DC = sp.Matrix([gam, 0, 0, 0])
u_AC = sp.simplify(uC - u_DC)
resid_blk = sp.simplify(bxC - (-(gam * Om) ** 2) * u_AC)
n_AC = sp.simplify((u_AC.T * eta * u_AC)[0, 0])
print(f"""  TEST OF THE LEAD, AS LITERALLY HANDED IN ("Box_u has EIGENVALUE -Omega^2 ON u_mu"):
      Box_u u^mu    = {sp.simplify(bxC.T)}
      u^mu          = {sp.simplify(uC.T)}
      time component of Box_u u^mu = {sp.simplify(bxC[0])} , of u^mu = {sp.simplify(uC[0])} != 0
      => Box_u u = lambda u has NO solution (it would need lambda = 0 from the time component and
         lambda = -(gamma Omega)^2 from the spatial ones).  solve() on the time component gives {sol_lam}.
      SO u IS NOT AN EIGENVECTOR OF Box_u.  The lead is FALSE as literally stated.

  THE BLOCK FORM (what the audited script actually asserts) -- tested componentwise:
      Box_u u^mu - ( -(gamma Omega)^2 ) u_AC^mu = {sp.simplify(resid_blk.T)}   (must be all zeros)
      u_DC.u_DC = {sp.simplify((u_DC.T*eta*u_DC)[0,0])} ,  u_AC.u_AC = {n_AC} ,  u_DC.u_AC = {sp.simplify((u_DC.T*eta*u_AC)[0,0])}
      => Box_u is DIAGONAL on the orthogonal pair (u_DC, u_AC): eigenvalues {{0, -(gamma Omega)^2}},
         both <= 0.  The normalized first moment <Box_u>_u = +|a|^2 is a RAYLEIGH QUOTIENT (positive
         only because u.u = -1), NOT an eigenvalue -- it is not in the spectrum at all.""")
assert all(sp.simplify(c) == 0 for c in resid_blk), "block form failed"
assert sp.simplify(bxC[0]) == 0 and sp.simplify(uC[0]) != 0, "the u-eigenvector disproof failed"

# --- route 2: CURVILINEAR (cylindrical) with full Christoffels -- the frame/gauge question
Rr, Ph = sp.symbols("r phi", positive=True)
gcyl = sp.diag(-1, 1, Rr ** 2, 1)                  # ds^2 = -dt^2 + dr^2 + r^2 dphi^2 + dz^2
coords = [sp.Symbol("t"), Rr, Ph, sp.Symbol("zz")]
ginv = gcyl.inv()
Gam = [[[sp.simplify(sum(ginv[m, s] * (sp.diff(gcyl[s, i], coords[j]) + sp.diff(gcyl[s, j], coords[i])
                                       - sp.diff(gcyl[i, j], coords[s])) / 2 for s in range(4)))
         for j in range(4)] for i in range(4)] for m in range(4)]
u_cyl = sp.Matrix([gam, 0, gam * Om, 0])           # (u^t, u^r, u^phi, u^z) -- ALL CONSTANT in tau
subs_r = {Rr: R0}
def cov_deriv_along_u(V):
    """(D V / dtau)^m = dV^m/dtau + Gamma^m_{ij} u^i V^j, evaluated on the circular worldline."""
    out = []
    for m in range(4):
        s = sp.diff(V[m], tau)
        for i in range(4):
            for j in range(4):
                s += Gam[m][i][j].subs(subs_r) * u_cyl[i] * V[j]
        out.append(sp.simplify(s))
    return sp.Matrix(out)
a_cyl  = cov_deriv_along_u(u_cyl)
bx_cyl = cov_deriv_along_u(a_cyl)
naive  = sp.Matrix([sp.diff(u_cyl[m], tau, 2) for m in range(4)])
# transform the Cartesian answer into the cylindrical basis and compare (vectors must agree)
bx_cart_to_cyl = sp.Matrix([bxC[0],
                            sp.simplify(bxC[1] * sp.cos(ph) + bxC[2] * sp.sin(ph)),
                            sp.simplify((-bxC[1] * sp.sin(ph) + bxC[2] * sp.cos(ph)) / R0),
                            0])
mismatch = sp.simplify(bx_cyl - bx_cart_to_cyl)
print(f"""
  Route 2 -- CYLINDRICAL coordinates with the full connection (this is the frame/gauge test the audit
  brief demands).  ds^2 = -dt^2 + dr^2 + r^2 dphi^2 + dz^2, u^mu = (gamma, 0, gamma Omega, 0):
      EVERY component of u is CONSTANT in tau here, so componentwise d^2/dtau^2 gives {naive.T}
      but the covariant Box_u u^mu = (D/dtau)^2 u^mu = {bx_cyl.T}   (Christoffel terms carry it)
      Cartesian answer transformed into this basis:              {sp.simplify(bx_cart_to_cyl.T)}
      difference = {mismatch.T}  (must be zero: Box_u u is a VECTOR, chart-independent)""")
assert all(sp.simplify(c) == 0 for c in mismatch), "cylindrical/Cartesian vectors disagree"
assert any(sp.simplify(c) != 0 for c in bx_cyl) and all(c == 0 for c in naive), "naive-vs-covariant test failed"

# --- route 3: Lorentz-boost invariance of the DC/AC decomposition
Vb = sp.Rational(3, 5)
gV = 1 / sp.sqrt(1 - Vb ** 2)
B  = sp.Matrix([[gV, -gV * Vb, 0, 0], [-gV * Vb, gV, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
uB = sp.simplify(B * uC)
uB_DC = sp.Matrix([sp.simplify(sp.integrate(c, (tau, 0, 2 * sp.pi / (gam * Om))) * gam * Om / (2 * sp.pi))
                   for c in uB])                                   # tau-average = the DC (zero-mode) part
uB_AC = sp.simplify(uB - uB_DC)
nDC_B = sp.simplify((uB_DC.T * eta * uB_DC)[0, 0])
nAC_B = sp.simplify(sp.trigsimp((uB_AC.T * eta * uB_AC)[0, 0]))
bxB   = sp.simplify(sp.diff(uB, tau, 2))
resid_B = sp.simplify(sp.expand_trig(bxB - (-(gam * Om) ** 2) * uB_AC))
print(f"""
  Route 3 -- BOOSTED frame (V = 3/5 along x).  A constant Lorentz map commutes with d/dtau, so the
  zero-mode/AC split and the eigenvalues must be boost-INVARIANT.  Computed:
      u'_DC . u'_DC = {nDC_B}   (unboosted: {sp.simplify((u_DC.T*eta*u_DC)[0,0])})
      u'_AC . u'_AC = {nAC_B}   (unboosted: {n_AC})
      Box_u u' - (-(gamma Omega)^2) u'_AC = {resid_B.T}   (must be zero)""")
assert all(sp.simplify(c) == 0 for c in resid_B), "boost invariance of the block form failed"
assert sp.simplify(nDC_B - (u_DC.T * eta * u_DC)[0, 0]) == 0 and sp.simplify(nAC_B - n_AC) == 0

for n in (1, 2, 3):
    r_n = sp.simplify(((-(gam * Om) ** 2) ** n * n_AC) / (a2 ** n * nrm))
    print(f"      moment n = {n}: [u Box_u^n u] / [(a^2)^n (u.u)] = {r_n}")
assert sp.simplify(((-(gam*Om)**2)*n_AC)/(a2*nrm) - 1) == 0
assert sp.simplify(((-(gam*Om)**2)**2*n_AC)/(a2**2*nrm) - 1) != 0

log(1, "PASS", "the eigenvalue claim, as the audited script states it, holds exactly.",
    "Box_u is diagonal on the orthogonal pair (u_DC, u_AC) with eigenvalues {0, -(gamma Omega)^2}; "
    "reproduced 3 independent ways (Cartesian helix built from the spatial orbit; cylindrical with the "
    "full connection, same vector; boosted frame, invariant), plus the paper's own n>1 moment mismatch.")
log(2, "FAIL-MINOR", "the lead AS HANDED IN is false, and the split needs a PARALLEL-PROPAGATED frame.",
    "u is NOT an eigenvector (the time component forces lambda = 0, the spatial ones -(gamma Omega)^2), "
    "so 'Box_u u_mu = -Omega^2 u_mu' is wrong; the audited script states the correct block form but "
    "never says the DC/AC split requires a parallel-propagated frame -- in cylindrical coordinates every "
    "component of u is constant and componentwise d^2/dtau^2 = 0 while Box_u u != 0. No number changes "
    "(flat Cartesian IS parallel-propagated, and the split is Lorentz-invariant, both verified above).")

# =====================================================================================================
head("2.  AUDIT ITEM (2): THE BRANCH.  Which sheet is retarded, and can a branch error inflate arg K?")
# =====================================================================================================
Ysym = sp.Symbol("Y", positive=True)
Kf = lambda zz: (sp.sqrt(1 + 4 * zz) - 1) / (2 * sp.sqrt(zz))
ReKs = sp.sqrt(4 * Ysym - 1) / (2 * sp.sqrt(Ysym))
ImKs = 1 / (2 * sp.sqrt(Ysym))
print(f"""
  THE CONVENTION IS NOT MINE TO CHOOSE -- it is fixed by the record (mi_omegac_drift_sign_energy_2026.py
  Sec. 0, convention C1): g(t) = omega_c e^(-omega_c t) theta(t) paired with G(omega) = INT_0^inf g e^(-i
  omega t) dt = 1/(1 + i omega/omega_c), i.e. PHASORS ~ e^(+i omega t), and Im G < 0 for omega > 0.
  In that convention:
      d/dtau -> +i omega  =>  Box_u -> -omega^2  =>  z = -(omega c/a0)^2  (real, ON the cut)
      causal/retarded  =>  G analytic for Im omega < 0  =>  approach from BELOW, omega -> omega - i eps
      z = -(omega - i eps)^2 (c/a0)^2 = -Y + i (2 omega eps c^2/a0^2)   =>   z = -Y + i0  for omega > 0
  So the RETARDED SHEET IS THE UPPER SIDE of the cut.  That is the side the audited script used.
""")
for Yv in (0.30, 1.0, 7.5, 1e3, PRIOR["Y_gal_canon"]):
    Kup = (np.emath.sqrt(1 + 4 * complex(-Yv, +1e-18)) - 1) / (2 * np.emath.sqrt(complex(-Yv, +1e-18)))
    Kdn = (np.emath.sqrt(1 + 4 * complex(-Yv, -1e-18)) - 1) / (2 * np.emath.sqrt(complex(-Yv, -1e-18)))
    print(f"    Y = {Yv:<12.4g} K(-Y+i0) = {Kup.real:+.6f}{Kup.imag:+.6f}i   K(-Y-i0) = "
          f"{Kdn.real:+.6f}{Kdn.imag:+.6f}i   |K| = {abs(Kup):.12f}/{abs(Kdn):.12f}   "
          f"|arg| = {abs(np.angle(Kup)):.6e}/{abs(np.angle(Kdn)):.6e}")
    if Yv > 0.25:
        assert abs(abs(Kup) - 1) < 1e-12 and abs(abs(Kdn) - 1) < 1e-12
        assert abs(abs(np.angle(Kup)) - abs(np.angle(Kdn))) < 1e-14
        assert abs(Kup.real - float(ReKs.subs(Ysym, Yv))) < 1e-10
        assert abs(Kup.imag - float(ImKs.subs(Ysym, Yv))) < 1e-10
        assert Kup.imag > 0 > Kdn.imag
mod2 = sp.simplify(ReKs ** 2 + ImKs ** 2)
print(f"\n    symbolic: |K(-Y+i0)|^2 = {mod2} for every Y > 1/4;  sin(arg K) = Im K/|K| = {sp.simplify(ImKs)} EXACTLY")
assert sp.simplify(mod2 - 1) == 0
# Herglotz probe, independent sample
rng = np.random.default_rng(4242)
pts = 10.0 ** rng.uniform(-4, 12, 150000) * np.exp(1j * rng.uniform(1e-7, np.pi - 1e-7, 150000))
Kc = (np.emath.sqrt(1 + 4 * pts) - 1) / (2 * np.emath.sqrt(pts))
frac_herg = float((np.imag(Kc) >= -1e-13).mean())
print(f"    Herglotz probe (150k UHP points, |z| in 1e-4..1e12): fraction with Im K >= 0 = {frac_herg:.6f}")
assert frac_herg > 0.9999
log(3, "PASS", "the branch is right, and NO branch error can inflate the rescue's magnitude.",
    f"The retarded sheet z = -Y + i0 follows from the record's own convention C1 (phasors e^(+i omega t) "
    f"=> analytic for Im omega < 0 => approach from below => Im z > 0). |K| = 1 and |arg K| are IDENTICAL "
    f"on the two sides of the cut (only sign(Im K) flips), so the load-bearing magnitude sin(arg K) = "
    f"1/(2 sqrt Y) is branch-INDEPENDENT; Im K >= 0 over the UHP ({frac_herg:.4f}) as Herglotz requires.")

# the sign clash the prior script did not report
sgnK = +1
ImG_gal = -(OMEGA_GAL / OMEGA_C_LO) / (1 + (OMEGA_GAL / OMEGA_C_LO) ** 2)
print(f"""
  BUT THE SIGNS DISAGREE, AND THAT WAS NOT REPORTED.  On the SAME retarded sheet in the SAME convention:
      Im G(omega>0) = {ImG_gal:+.6f}   (gate, at the binding galactic orbit and the window's lower edge)
      Im K(-Y  +i0) = {ImK_neg(OMEGA_GAL, A0_CANON):+.6e}   (kernel, same frequency, canon footing)
  Opposite sign => the gate LAGS where the kernel LEADS, so a tangential force built from the kernel's
  phase runs OPPOSITE to the gate's.  The record's established PROGRADE / EXPANSION sign (for s = -1)
  is a GATE result and does NOT carry over to the kernel channel; on the kernel channel the same
  construction gives RETROGRADE / CONTRACTION.  Two consequences, both scoped:
    * NO magnitude changes (|Im| is what enters every rate below), so no verdict moves.
    * The kernel's sign is the one the record's OWN passivity criterion wants (Im chi = -S Im(resp) <= 0
      for a passive bath): with G the record had to declare the MI bath ACTIVE/pumped; with K's own phase
      that particular inequality is not violated.  NOT a resolution of the pump problem -- the amplitude
      mapping S is a positive-axis object and is not supplied here.  Recorded, given no verdict weight.
""")
log(4, "FAIL-MINOR", "an unreported sign clash between the kernel's phase and the gate's.",
    "In the record's own convention Im G < 0 but Im K(-Y+i0) > 0, so the kernel-channel tangential force "
    "is RETROGRADE where the gate's is PROGRADE; the audited script presents them as 'the same mechanism "
    "differing ONLY in the lag angle' (magnitude), and carries the record's PROGRADE/EXPANSION label "
    "across. Magnitudes and therefore all verdicts are unaffected.")

# =====================================================================================================
head("3.  THE DIMENSIONAL MAP z = -(omega c/a0)^2 -- three independent pins + prove-by-moving")
# =====================================================================================================
print(f"""
  PIN 1 (dimensions).  Box_u f = d^2 f/dtau^2.  With tau a LENGTH (c = 1) d/dtau ~ 1/L and a0 -> a0/c^2
  ~ 1/L, so z = Box_u/a0^2 is dimensionless only as z = c^2 (d^2/dtau^2)/a0^2  =>  |z| = (omega c/a0)^2.
  PIN 2 (the paper's own words).  Sec. 5.3: "the action's own forced memory corner is omega_c = a0/2c =
  1.56e-19 rad/s (tau_mem = 2c/a0 = 203 Gyr canon / 168 Gyr alt)".  a0/2c IS the z = -1/4 branch point:
      canon a0/2c = {A0_CANON/(2*C_LIGHT):.4e} rad/s (paper: 1.56e-19; committed script: {PRIOR['branch_pt_canon']:.4e})
      alt   a0/2c = {A0_ALT/(2*C_LIGHT):.4e} rad/s ;  tau_mem = 2c/a0 = {2*C_LIGHT/A0_CANON/GYR:.1f} / {2*C_LIGHT/A0_ALT/GYR:.1f} Gyr
      (paper's quoted tau_mem: {PRIOR['tau_mem_Gyr']['canon']:.0f} / {PRIOR['tau_mem_Gyr']['alt']:.0f} Gyr)
  PIN 3 (new, Section 4): the kernel-channel galactic e-folding FLOOR comes out to exactly 2c/a0, i.e.
  the paper's own tau_mem -- a third, independent arrival at the same c-factors.

  PROVE-BY-MOVING (the audit brief's requirement that the load-bearing convention be moved):""")
for lab, a0 in FOOTINGS:
    Y_ok  = Y_of(OMEGA_GAL, a0)
    Y_bad = (OMEGA_GAL / a0) ** 2                                     # the lead's c-less reading
    s_ok  = ImK_neg(OMEGA_GAL, a0)
    Kbad  = (np.emath.sqrt(1 - 4 * Y_bad) - 1) / (2 * np.emath.sqrt(complex(-Y_bad, 1e-30)))
    print(f"    {lab:<6} WITH c: Y = {Y_ok:.4e} (> 1/4, past the branch point) -> sin(arg K) = {s_ok:.4e}"
          f"\n    {lab:<6} NO  c: Y = {Y_bad:.4e} (< 1/4, INSIDE the cut) -> K pure imaginary, "
          f"arg K = {np.degrees(np.angle(Kbad)):.1f} deg, sin(arg K) = {abs(np.sin(np.angle(Kbad))):.4f}")
    assert Y_ok > 0.25 > Y_bad
print(f"""    => the c-factors are worth ~{1.0/ImK_neg(OMEGA_GAL, A0_CANON):.1e}x in the tangential coefficient, and they are
       the difference between "no galactic problem" and "total galactic destruction".  The map is
       LOAD-BEARING FOR THE RESCUE, which is why it is pinned three independent ways above.
       Frequency inventory vs the branch point a0/2c (canon) -- which physical orbits land inside the cut:""")
inv = [("UGC05721 innermost (binding)", OMEGA_GAL), ("Milky Way at the Sun", 233e3 / (8.2 * KPC)),
       ("wide binary, 20 kAU", float(np.sqrt(GM_SUN / (20e3 * AU) ** 3))),
       ("Saturn", 2 * np.pi / (PLANETS["Saturn"][1] * 86400.0)),
       ("cluster orbit ~ 1e-16", 1e-16), ("H_Lambda ~ 1.8e-18", 1.8e-18),
       ("branch point a0/2c itself", A0_CANON / (2 * C_LIGHT))]
for nm, w in inv:
    Yv = Y_of(w, A0_CANON)
    print(f"      {nm:<32} Omega = {w:.3e}  Y = {Yv:.4e}  {'PAST the cut' if Yv > 0.25 else 'INSIDE the cut'}"
          f"   period = {2*np.pi/w/GYR:.3e} Gyr")
log(5, "PASS", "the dimensional correction z = -(omega c/a0)^2 is correct and triple-pinned.",
    f"Dimensional analysis, the paper's own forced corner a0/2c = {A0_CANON/(2*C_LIGHT):.4e} rad/s "
    f"(= the z = -1/4 branch point, quoted in Sec. 5.3 as 1.56e-19 with tau_mem = 2c/a0 = 203/168 Gyr), "
    f"and the new e-fold floor of Section 4 all give the same c-factors. Moving them (the lead's c-less "
    f"reading) puts every orbit INSIDE the cut and inflates sin(arg K) to 1.0 -- so the correction is "
    f"load-bearing for the rescue and is independently anchored, not chosen.")

# =====================================================================================================
head("4.  AUDIT ITEM (3)+(4): THE RESCUE.  Was 2.6e-5 cherry-picked at the gate's binding orbit?")
# =====================================================================================================
gobs = V_GAL ** 2 / R_GAL
print(f"""
  THE CHERRY-PICK RISK IS REAL AND MUST BE CLOSED.  sin(arg K) = a0/(2 c Omega) GROWS as Omega falls, so
  the gate's binding orbit -- the FASTEST confirmed deep-MOND orbit, chosen precisely because it is worst
  for the gate -- is the kernel's MOST FAVOURABLE orbit.  Evaluating the kernel there and reporting
  "550 Gyr, margin 55x" would be exactly the kind of favourable-point selection this audit hunts.
  So: derive the coefficient's orbit dependence in closed form instead of evaluating one orbit.

      f_t   = A sin(arg K),   A = g_obs - g_bar,   sin(arg K) = a0/(2 c Omega)  (EXACT, |K| = 1)
      flat-RC angular momentum L = V r,  dL/dt = r f_t  =>  d ln r/dt = f_t/V
      Omega = V/r  =>  d ln r/dt = A a0 r/(2 c V^2) = (a0/2c) * A/g_obs        [g_obs = V^2/r]

      ==>  t_e = (2c/a0) * g_obs/(g_obs - g_bar)  >=  2c/a0 = tau_mem ,  equality iff g_bar -> 0.

  The V and r dependence CANCELS.  The kernel-channel e-folding time has a UNIVERSAL FLOOR equal to the
  paper's own kernel memory time -- no orbit anywhere can do worse, so no orbit choice can be favourable.
""")
print(f"  {'footing':<8}{'2c/a0 = floor':>16}{'A_gal':>12}{'g_obs/A':>10}{'t_e binding':>14}"
      f"{'prior script':>14}{'floor/10Gyr':>13}{'Kepler 2x floor':>17}")
print("  " + "-" * 104)
floor = {}
for lab, a0 in FOOTINGS:
    A_gal = gobs - gbar_from_gobs(gobs, a0)
    fl = 2 * C_LIGHT / a0
    te = fl * gobs / A_gal
    floor[lab] = (fl, te, A_gal)
    prior_te = PRIOR["efold_canon_Gyr"] if lab == "canon" else PRIOR["efold_alt_Gyr"]
    print(f"  {lab:<8}{fl/GYR:>13.1f} Gyr{A_gal:>12.4e}{gobs/A_gal:>10.4f}{te/GYR:>11.1f} Gyr"
          f"{prior_te:>11.1f} Gyr{fl/(10*GYR):>13.1f}x{fl/2/(10*GYR):>16.1f}x")
    assert abs(te / GYR / prior_te - 1) < 0.01, "closed form disagrees with the committed e-fold time"
    assert abs(fl / GYR / PRIOR["tau_mem_Gyr"][lab] - 1) < 0.01, "floor != the paper's own tau_mem"
# brute-force scan: no orbit beats the floor
Vg = np.linspace(5e3, 320e3, 240)
rg = 10 ** np.linspace(np.log10(0.02 * KPC), np.log10(120 * KPC), 240)
VV, RR = np.meshgrid(Vg, rg)
GO = VV ** 2 / RR
scan = {}
for lab, a0 in FOOTINGS:
    GB = gbar_from_gobs(GO, a0)
    TE = (2 * C_LIGHT / a0) * GO / (GO - GB)
    deep = GB < 0.3 * a0
    scan[lab] = (TE.min() / GYR, TE[deep].min() / GYR if deep.any() else np.nan,
                 float(np.nanmin(np.where(deep, GO / a0, np.nan))))
    print(f"    scan {lab:<6}: 57,600 (V, r) orbits, V in [5, 320] km/s, r in [0.02, 120] kpc -> "
          f"min t_e = {TE.min()/GYR:.1f} Gyr (all), {scan[lab][1]:.1f} Gyr (deep-MOND cut g_bar < 0.3 a0)"
          f";  floor = {2*C_LIGHT/a0/GYR:.1f} Gyr")
    assert TE.min() >= 2 * C_LIGHT / a0 * (1 - 1e-12), "an orbit breached the analytic floor"
log(6, "PASS", "the rescue is NOT an artifact of the gate's binding orbit -- it is orbit-independent.",
    f"Exact closed form t_e = (2c/a0) g_obs/(g_obs - g_bar) >= 2c/a0 = "
    f"{floor['canon'][0]/GYR:.0f} Gyr (canon) / {floor['alt'][0]/GYR:.0f} Gyr (alt): the V and r dependence "
    f"cancels, so every circular orbit clears a 10 Gyr disk age by >= {floor['canon'][0]/(10*GYR):.0f}x / "
    f"{floor['alt'][0]/(10*GYR):.0f}x ({floor['canon'][0]/2/(10*GYR):.0f}x / {floor['alt'][0]/2/(10*GYR):.0f}x "
    f"with the faster Keplerian 2 f_t/V form). Confirmed on a 57,600-orbit scan; the floor IS the paper's "
    f"own tau_mem = 2c/a0. The committed 550.2/398.3 Gyr at the binding orbit reproduce to <1%.")

# --- was 0.300 assumed, or derived?  and is 2.6e-5 a hybrid?
w, wc = sp.symbols("omega omega_c", positive=True)
Gs = 1 / (1 + sp.I * w / wc)
ident = sp.simplify(sp.Abs(Gs) ** 2 - sp.re(sp.together(sp.simplify(Gs))))
ImG_edge = float(np.sqrt(GATE_KEEP - GATE_KEEP ** 2))
v_sat = float(np.sqrt(GM_SUN / PLANETS["Saturn"][0]))
print(f"""
  WAS READING A's 0.300 ASSUMED?  No -- it is forced INSIDE the gate's own construction, and I reproduce
  the algebra: sympy residual for |G|^2 = Re G is {sp.simplify(ident)}, hence Re G = {GATE_KEEP}
  <=> |Im G| = sqrt(ReG - ReG^2) = {ImG_edge:.6f} exactly (committed value {PRIOR['ImG_edge']}).  So the
  0.300 is not an assumption ABOUT the action -- it is an identity OF THE GATE.  What is assumed is that
  the gate IS the action's response on the direction-carrying channel.  That assumption is what the
  audited script overturns, and it overturns it with the action's own kernel, not by fiat.  ITEM (4) CLEAR.

  BUT IS 2.6e-5 A CLEAN ACTION NUMBER?  No, and this is the audit's sharpest reservation.  The literal
  vector-channel evaluation of the dressing gives (verified: Box_u diagonal, K(0) = 0 exactly)
        u^mu K(Box_u/a0^2) u_mu = (-gamma^2) K(0) + (gamma beta)^2 K(-Y) = (gamma beta)^2 K(-Y),
        |...| = (v/c)^2 = {(V_GAL/C_LIGHT)**2:.3e} (binding galactic orbit) / {(v_sat/C_LIGHT)**2:.3e} (Saturn)
  -- NO MOND amplitude (a0 has collapsed into a phase) and NO Newtonian limit (it needs -1).  The MOND
  amplitude A_gal exists only via the FIRST-MOMENT closure, which is a POSITIVE-axis object with no
  frequency in it.  So "A_gal x sin(arg K)" mixes an amplitude from one axis with a phase from the other
  -- structurally the SAME hybrid the script (correctly) condemns in the gate.  Consequence, stated as a
  BRACKET rather than a point:
      strict closure reading (Reading B):        tangential coefficient = 0 EXACTLY  (X is DC)
      literal vector reading:                    no MOND amplitude at all, so no tangential MOND force
      hybrid (amplitude closure x kernel phase): {ImK_neg(OMEGA_GAL, A0_CANON):.3e} (canon) / {ImK_neg(OMEGA_GAL, A0_ALT):.3e} (alt)
      the gate's Reading A:                      {ImG_edge:.3f}
  Every ACTION-sourced reading lands in [0, {ImK_neg(OMEGA_GAL, A0_ALT):.1e}]; the gate's 0.300 is outside that
  bracket by >= {ImG_edge/ImK_neg(OMEGA_GAL, A0_ALT):.0e}x.  The audited conclusion (Reading A's coefficient is not the action's)
  therefore does NOT depend on the hybrid being legitimate -- it holds a fortiori at the bracket's TOP.
""")
assert sp.simplify(ident) == 0
log(7, "FAIL-MINOR", "the 2.6e-5 is a hybrid, and the audited script calls it 'derived'.",
    "It multiplies a POSITIVE-axis (closure) amplitude by a NEGATIVE-axis (frequency) phase -- the same "
    "cross-axis construction the script condemns in the gate; the literal vector channel gives "
    "(gamma beta)^2 K(-Y), i.e. no MOND amplitude at all, and the strict closure reading gives exactly "
    "ZERO tangential force. The script says the coefficient 'is not fitted -- it is arg K at the kernel's "
    "own argument' without flagging that the CONSTRUCTION is not derived. Verdict-neutral: all "
    "action-sourced readings lie in [0, 3.2e-5], so the refutation of 0.300 holds at the bracket's top.")

# --- LOOP CLOSURE: re-insert the gate and recompute
print(f"""
  LOOP CLOSURE (the audit brief's item 3, the one that decides whether this is a manufactured rescue).
  If the gate is RETAINED -- and it must be, since removing it returns the ungated a0/2 tail -- then its
  own |Im G| = 0.300 comes back with it.  Recomputing the galactic side WITH the gate, independently:
""")
print(f"  {'footing':<8}{'coefficient':>13}{'f_t':>12}{'dlnr/dt [/Gyr]':>17}{'e-fold':>14}"
      f"{'omega_c needed (10 Gyr)':>25}{'LLR edge':>12}{'over by':>10}{'window':>9}")
print("  " + "-" * 104)
closure = {}
for lab, a0 in FOOTINGS:
    A_gal = floor[lab][2]
    for src, coef in (("GATE 0.300", ImG_edge), ("KERNEL", ImK_neg(OMEGA_GAL, a0))):
        rate = A_gal * coef / V_GAL
        T_need = V_GAL / (A_gal * 10 * GYR)
        wc_need = OMEGA_GAL / T_need                       # small-x single pole: |Im G| ~ Omega/omega_c
        hi = OMEGA_C_HI[lab]
        closure[(lab, src)] = (1 / rate, wc_need, wc_need / hi)
        print(f"  {lab+'/'+src.split()[0]:<8}{coef:>13.4e}{A_gal*coef:>12.3e}{rate*GYR:>17.3e}"
              f"{(1/rate)/GYR if 1/rate > GYR else (1/rate)/(GYR/1e3):>11.1f} "
              f"{'Gyr' if 1/rate > GYR else 'Myr':<3}{wc_need:>25.4e}{hi:>12.4e}{wc_need/hi:>9.0f}x"
              f"{'EMPTY' if wc_need > hi else 'OPEN':>9}")
for lab in ("canon", "alt"):
    got, want = closure[(lab, "GATE 0.300")][1], PRIOR["wc_need_" + lab]
    assert abs(got / want - 1) < 0.02, f"failed to reproduce the record's required omega_c ({lab})"
    assert closure[(lab, "GATE 0.300")][1] > OMEGA_C_HI[lab], "single-pole window unexpectedly open"
print(f"""
  ==> THE LOOP IS CLOSED, AND IT CLOSES AGAINST THE GATE FROM BOTH SIDES.  Reproduced independently:
      gate RETAINED  -> galactic survival needs omega_c >= {closure[('canon','GATE 0.300')][1]:.3e} (canon) / {closure[('alt','GATE 0.300')][1]:.3e} (alt),
                        i.e. {closure[('canon','GATE 0.300')][2]:.0f}x / {closure[('alt','GATE 0.300')][2]:.0f}x ABOVE the LLR edge (record: {PRIOR['over_canon']}x / {PRIOR['over_alt']}x)
                        => the SINGLE-POLE window is EMPTY.  Reading A's conclusion stands ON THE GATE.
      gate REMOVED   -> the kernel supplies |K| = 1, no amplitude suppression at any frequency, so the
                        ungated sunward a0/2 tail returns in full (Section 6 below).
  So the audited script did NOT drop the gate and declare victory: it re-inserted the gate's own
  requirement and reported the window EMPTY.  NO MANUFACTURED RESCUE ON THIS AXIS.
""")
log(8, "PASS", "the gate loop was closed, not left open -- verified by independent recomputation.",
    f"With the gate retained, galactic survival needs omega_c >= {closure[('canon','GATE 0.300')][1]:.3e} "
    f"(canon) / {closure[('alt','GATE 0.300')][1]:.3e} (alt) = {closure[('canon','GATE 0.300')][2]:.0f}x / "
    f"{closure[('alt','GATE 0.300')][2]:.0f}x above the LLR upper edge, reproducing the record's 186x/257x "
    f"to <2% -- single-pole window EMPTY. With the gate removed the a0/2 tail returns at full strength. "
    f"The audited script reports both; neither jaw was suppressed.")

# =====================================================================================================
head("5.  AUDIT ITEM (5): REDUNDANCY -- close it over the WHOLE channel family, not 3 hand-picked ones")
# =====================================================================================================
dev2 = sp.simplify(2 - 2 * ReKs)                     # |1 - K|^2 = 1 - 2ReK + |K|^2 = 2 - 2ReK
ddev = sp.simplify(sp.diff(dev2, Ysym))
print(f"""
  THE 3-CHANNEL TABLE IS NOT A CLOSURE -- the channels were picked by hand.  Close the family instead.
  On the negative axis K(-Y+i0) is a single UNIT-MODULUS number, so EVERY K-only real response is some
  function of arg K alone.  The one invariant that controls all of them is the distance to the identity:

      |1 - K(-Y+i0)|^2 = 1 - 2 Re K + |K|^2 = {dev2}   (using |K| = 1)
      d/dY of that     = {ddev}   -> NEGATIVE for all Y > 1/4 (sympy), so |1 - K| STRICTLY DECREASES
      asymptotically   |1 - K| -> 1/(2 sqrt Y) = a0/(2 c omega)

  ==> K APPROACHES THE IDENTITY AT HIGH FREQUENCY.  Whatever suppression K's frequency dependence can
      supply is LARGEST in galaxies and SMALLEST at the planets -- the separation runs BACKWARDS.  No
      monotone function of K's frequency response can do the gate's job, whichever one is chosen.
""")
assert float(ddev.subs(Ysym, 1.0)) < 0 and float(ddev.subs(Ysym, 1e8)) < 0
print(f"  {'footing':<8}{'|1-K| galactic':>17}{'|1-K| Saturn':>15}{'|1-K| Mars':>13}"
      f"{'gal/planet':>13}{'needed direction':>19}")
print("  " + "-" * 104)
for lab, a0 in FOOTINGS:
    dg_ = lambda w: abs_1_minus_K(w, a0)
    wS = 2 * np.pi / (PLANETS["Saturn"][1] * 86400.0)
    wM = 2 * np.pi / (PLANETS["Mars"][1] * 86400.0)
    print(f"  {lab:<8}{dg_(OMEGA_GAL):>17.4e}{dg_(wS):>15.4e}{dg_(wM):>13.4e}{dg_(OMEGA_GAL)/dg_(wS):>13.3e}"
          f"{'planet >> galaxy':>19}")
    assert dg_(OMEGA_GAL) > dg_(wS) > 0
# the 3-channel table, reproduced independently, with the pass criteria written to be failable
chan = {"R1 |K|": lambda w, a0: 1.0,
        "R2 sin(argK)": lambda w, a0: ImK_neg(w, a0),
        "R3 1-ReK": one_minus_ReK,
        "R4 |1-K|": abs_1_minus_K,
        "R5 ReK": lambda w, a0: ReK_neg(w, a0)}
print(f"\n  {'footing':<8}{'channel':<15}{'R(gal)':>12}{'RAR>=0.90':>11}{'worst planet':>14}"
      f"{'R(planet)':>12}{'R needed':>11}{'shortfall':>12}{'planets ok':>11}{'REDUNDANT':>11}")
print("  " + "-" * 104)
any_red = False
for lab, a0 in FOOTINGS:
    for cn, f in chan.items():
        Rg = f(OMEGA_GAL, a0)
        worst = max(((p, f(2*np.pi/(PLANETS[p][1]*86400.0), a0), PLANETS[p][3]/(a0/2)) for p in PLANETS),
                    key=lambda t: t[1] / t[2])
        red = (Rg >= GATE_KEEP) and (worst[1] <= worst[2])
        any_red = any_red or red
        print(f"  {lab:<8}{cn:<15}{Rg:>12.4e}{'YES' if Rg >= GATE_KEEP else 'NO':>11}{worst[0]:>14}"
              f"{worst[1]:>12.3e}{worst[2]:>11.3e}{worst[1]/worst[2]:>12.3e}"
              f"{'YES' if worst[1] <= worst[2] else 'NO':>11}{'YES' if red else 'NO':>11}")
assert not any_red, "a K-only channel passed both halves -- rewrite the verdict, do not assert it"
log(9, "PASS", "omega_c is NOT redundant, and the closure is now family-wide, not 3 hand-picked channels.",
    "|1 - K(-Y+i0)|^2 = 2 - 2 Re K is strictly DECREASING in Y (sympy derivative negative), so K "
    "approaches the identity at HIGH frequency: its deviation is 2.6e-5 (canon) / 3.2e-5 (alt) at the "
    "binding galactic orbit and ~2e-11 at Saturn -- the separation runs backwards by ~1.1e6. Five "
    "channels tested (the audited script's three plus |1-K| and Re K), both footings, four planets: none "
    "passes both halves. The redundancy answer is robust to the channel enumeration.")

# =====================================================================================================
head("6.  AUDIT ITEM (6): THE DC-vs-DC POINT.  Was it faced?  Independent closed-form confirmation")
# =====================================================================================================
Xs = sp.Symbol("X", positive=True)
Kpos = (sp.sqrt(1 + 4 * Xs) - 1) / (2 * sp.sqrt(Xs))
tail = sp.limit(sp.sqrt(Xs) * (1 - Kpos), Xs, sp.oo)
e_, aP_ = sp.symbols("e a", positive=True)
print(f"""
  THE POINT: the galactic RAR and the sunward a0/2 tail are BOTH first-moment/positive-axis objects
  whose argument X = (g/a0)^2 is an ACCELERATION.  On a circular orbit it is exactly constant; at a
  planet it is exactly constant.  A gate G(omega) needs a frequency neither possesses.  Confirmed:
      absolute anomaly  g (1 - K(X)) -> a0 * {tail} = a0/2  EXACTLY (sympy limit), i.e. independent of
      BOTH g and omega:  a0/2 = {A0_CANON/2:.4e} (canon) / {A0_ALT/2:.4e} (alt) m/s^2
      fractional anomaly nu - 1 = 1/(2y) -> dies as 1/g, but no experiment bounds the fractional piece.
""")
assert sp.simplify(tail - sp.Rational(1, 2)) == 0
print(f"  {'planet':<9}{'y = g_N/a0':>13}{'nu-1':>12}{'absolute':>12}{'dg bound':>11}"
      f"{'excl canon':>12}{'excl alt':>11}{'e':>8}{'<1/|a|><|a|> exact':>20}{'prior num':>11}")
print("  " + "-" * 104)
excl = {"canon": [], "alt": []}
for p, (aP, TP, eP, dgb) in PLANETS.items():
    gN = GM_SUN / aP ** 2
    # Kepler TIME averages, closed form: <r^2> = a^2(1 + 3e^2/2), <1/r^2> = 1/(a^2 sqrt(1-e^2))
    cs_exact = float((1 + sp.Rational(3, 2) * e_ ** 2).subs(e_, eP) / sp.sqrt(1 - e_ ** 2).subs(e_, eP))
    for lab, a0 in FOOTINGS:
        excl[lab].append((p, (a0 / 2) / dgb, cs_exact * (a0 / 2) / dgb))
    print(f"  {p:<9}{gN/A0_CANON:>13.4e}{A0_CANON/(2*gN):>12.4e}{A0_CANON/2:>12.4e}{dgb:>11.1e}"
          f"{(A0_CANON/2)/dgb:>11.0f}x{(A0_ALT/2)/dgb:>10.0f}x{eP:>8.5f}{cs_exact:>20.6f}"
          f"{PRIOR['cs'][p]:>11.4f}")
    assert abs(cs_exact / PRIOR["cs"][p] - 1) < 5e-4, f"closed-form Cauchy-Schwarz != prior numeric ({p})"
    assert cs_exact >= 1.0
print(f"""
  THE ECCENTRIC DOOR, INDEPENDENTLY AND ANALYTICALLY SHUT.  The audited script closed it by numerical
  Kepler sampling; here it is closed in CLOSED FORM, which is a stronger check of the same claim:
      <1/|a|>_t <|a|>_t = <r^2>_t <1/r^2>_t / 1 = (1 + 3e^2/2)/sqrt(1 - e^2)  >=  1  for all e,
  reproducing the committed 1.0866 / 1.0006 / 1.0175 / 1.0064 to 4 significant figures.  So gating the
  ENTIRE AC content of the scalar channel leaves >= the full a0/2 tail:
      worst planet after gating all AC content: {max(t[2] for t in excl['canon']):.0f}x over bound (canon) / {max(t[2] for t in excl['alt']):.0f}x (alt)
      per-planet ungated exclusions: {min(t[1] for t in excl['canon']):.0f}x-{max(t[1] for t in excl['canon']):.0f}x (canon) / {min(t[1] for t in excl['alt']):.0f}x-{max(t[1] for t in excl['alt']):.0f}x (alt)
  ==> ITEM (6) WAS FACED, NOT EVADED, and it survives an independent analytic closure.
""")
log(10, "PASS", "the DC-vs-DC objection was faced and it holds under an independent analytic check.",
    f"g(1 - K) -> a0/2 exactly (sympy), independent of acceleration AND frequency, so a purely "
    f"frequency-dependent gate cannot separate the RAR from the tail. The eccentric escape is shut in "
    f"CLOSED FORM: <1/|a|><|a|> = (1 + 3e^2/2)/sqrt(1-e^2) >= 1, matching the audited script's numerical "
    f"1.0866/1.0006/1.0175/1.0064 to 4 s.f.; worst planet after gating all AC content is still "
    f"{max(t[2] for t in excl['canon']):.0f}x over bound (canon) / {max(t[2] for t in excl['alt']):.0f}x (alt).")

# =====================================================================================================
head("7.  THE INTERMEDIATE (P6) RE-CHECKED -- does the double-pole window really open, and at what cost?")
# =====================================================================================================
from scipy.optimize import brentq
W2  = lambda x: 1.0 / (1.0 + 1j * x) ** 2
Rr2 = lambda x: abs(np.real(W2(x)))
T2  = lambda x: abs(np.imag(W2(x)))
print(f"""
  Re-derived independently (the audited script's Sec. 4B).  Constraints, no gate FORM assumed, only a
  causal response with modulus m and lag: radial retention = m cos(lag), tangential T = m sin(lag).
      (G1) RAR:          radial retention(Omega_gal) >= {GATE_KEEP}
      (G2) survival:     T(Omega_gal) <= V/(A_gal * 10 Gyr)
      (P1) planets:      radial retention(Omega_p) <= dg_p/(a0/2), ALL FOUR, min taken
      (L1) LLR:          T(Omega_Moon) <= LLR_allow * v_Moon / a0
  {'footing':<8}{'lo G1':>12}{'lo G2':>12}{'hi P1':>12}{'bind':>9}{'hi L1':>12}{'window':>9}{'prior':>26}""")
inter = {}
for lab, a0 in FOOTINGS:
    A_gal = floor[lab][2]
    T_gal = V_GAL / (A_gal * 10 * GYR)
    T_moon = LLR_ALLOW * V_MOON / a0
    lo1 = OMEGA_GAL / brentq(lambda x: Rr2(x) - GATE_KEEP, 1e-6, 0.9)
    lo2 = OMEGA_GAL / brentq(lambda x: T2(x) - T_gal, 1e-12, 0.55)
    hiP, bind = np.inf, None
    for p, (aP, TP, eP, dgb) in PLANETS.items():
        wP = 2 * np.pi / (TP * 86400.0)
        c = wP / brentq(lambda x: Rr2(x) - dgb / (a0 / 2), 2.0, 1e12)
        if c < hiP: hiP, bind = c, p
    hiL = OMEGA_MOON / brentq(lambda x: T2(x) - T_moon, 2.0, 1e12)
    lo, hi = max(lo1, lo2), min(hiP, hiL)
    inter[lab] = (lo, hi, bind)
    pr = PRIOR["dpole_" + lab]
    print(f"  {lab:<8}{lo1:>12.3e}{lo2:>12.3e}{hiP:>12.3e}{bind:>9}{hiL:>12.3e}"
          f"{('x%.1f' % (hi/lo)) if hi > lo else 'EMPTY':>9}{f'[{pr[0]:.3e},{pr[1]:.3e}]':>26}")
    assert abs(lo / pr[0] - 1) < 0.02 and abs(hi / pr[1] - 1) < 0.02, "double-pole window not reproduced"
print(f"""
  ==> REPRODUCED to <2% on both footings, and the binding planet is indeed SATURN (slowest of the four,
      least suppressed by a rolloff), computed rather than assumed.  The window is NON-EMPTY.
      ITS STATUS, held exactly where the audited script put it: an AMENDMENT, not a reading of the
      action -- the kernel's own rolloff on that channel is order ZERO (|K| = 1).  Naturalness moves the
      WRONG way: corner/(a0/2c) = {inter['canon'][0]/(A0_CANON/(2*C_LIGHT)):.1e}-{inter['canon'][1]/(A0_CANON/(2*C_LIGHT)):.1e} vs {OMEGA_C_LO/(A0_CANON/(2*C_LIGHT)):.1e} for the single pole.
      And it INVERTS the paper's own Sec. 5.4 wide-binary falsifier, so Gaia DR4 separates the two
      overlays in opposite directions.  Retention at a 1 Msun binary, both overlays:""")
for kau in (3.0, 10.0, 20.0):
    wwb = float(np.sqrt(GM_SUN / (kau * 1e3 * AU) ** 3))
    print(f"      {kau:>5.0f} kAU  Omega = {wwb:.3e}   single pole (2.21e-14) Re G = "
          f"{1/(1+(wwb/OMEGA_C_HI['canon'])**2):.4f}   double pole ({inter['canon'][1]:.2e}) |Re W| = "
          f"{Rr2(wwb/inter['canon'][1]):.4f}")
log(11, "PASS", "the intermediate double-pole window is real, reproduced, and correctly priced.",
    f"Independently reproduced to <2%: omega_r in [{inter['canon'][0]:.3e}, {inter['canon'][1]:.3e}] canon "
    f"/ [{inter['alt'][0]:.3e}, {inter['alt'][1]:.3e}] alt, binding planet Saturn (computed over all four). "
    f"It is an AMENDMENT (the kernel's rolloff on that channel is order zero, |K| = 1), it widens the "
    f"naturalness gap to ~1e8 x a0/2c, and it inverts the paper's own wide-binary falsifier -- all of "
    f"which the audited script states at full strength rather than burying.")

# =====================================================================================================
head("8.  RESIDUAL PRESENTATION FLAG (not load-bearing), then the audit verdict")
# =====================================================================================================
a_pole_lo, a_pole_hi = C_LIGHT * OMEGA_C_LO, C_LIGHT * OMEGA_C_HI["canon"]
r_lo, r_hi = np.sqrt(GM_SUN / a_pole_lo) / AU, np.sqrt(GM_SUN / a_pole_hi) / AU
print(f"""
  The audited script's Sec. 8 notes that the multiplicative embedding K -> K*G puts a pole at
  |a| = c omega_c, i.e. heliocentric r = {r_hi:.1f}-{r_lo:.1f} AU, and labels the column "nearest planet:
  Neptune (30.07 AU)" for EVERY corner.  That is a coincidence with no content: c omega_c ~ 1e-5 m/s^2
  for any corner in the committed band, and sqrt(GM/1e-5) happens to be tens of AU.  The section is
  already labelled non-load-bearing and makes no ghost claim, so this is presentation, not physics --
  but it reads as significance where there is none, and in a framework whose numerology history is on
  the record it should be dropped or explicitly de-flagged.
""")
log(12, "FAIL-MINOR", "a numerological flourish in the non-load-bearing Sec. 8.",
    f"Reporting 'nearest planet Neptune (30.07 AU)' against the K*G pole radius {r_hi:.1f}-{r_lo:.1f} AU "
    f"presents an accidental order-of-magnitude coincidence (c omega_c ~ 1e-5 m/s^2 for any corner in "
    f"the band) as if it located something. The section is correctly flagged non-load-bearing and makes "
    f"no ghost claim; the flourish should still be de-flagged.")

# --- calibration audit of the audited script itself
import re, pathlib
src = pathlib.Path(__file__).with_name("mi_kernel_axis_separation_omegac_2026.py").read_text()
checks = {
    "both footings declared": "A0_ALT" in src and "FOOTINGS" in src,
    "asserts written to FAIL not to declare": "do not assert" in src or "rewrite the verdict" in src,
    "no 'theory closed'": "theory closed" not in src.replace('Never "theory closed"', ""),
    "no TOE claim": " TOE " not in src.replace("No TOE language.", ""),
    "gate scope stated": "GATE ONLY" in src,
    "verdicts computed not hard-coded": bool(re.search(r"'(SURVIVES|DESTROYED|EMPTY|OPEN|YES|NO)' if ", src)),
}
print("  CALIBRATION AUDIT of the audited script's own compliance:")
for k, v in checks.items():
    print(f"      {k:<45} {'OK' if v else 'FLAG'}")
n_pass = sum(1 for f in FINDINGS if f[1] == "PASS")
n_min  = sum(1 for f in FINDINGS if f[1] == "FAIL-MINOR")
n_blk  = sum(1 for f in FINDINGS if f[1] == "FAIL-BLOCKER")
log(13, "PASS" if all(checks.values()) else "FAIL-MINOR",
    "calibration compliance of the audited script.",
    f"{sum(checks.values())}/{len(checks)} checks OK: both footings carried, verdict strings computed from "
    f"the numbers, asserts phrased to fail rather than to declare, gate-only scope stated, no TOE/"
    f"'theory closed' language.")

head("9.  AUDIT VERDICT")
print(f"""
  FINDINGS: {n_pass} PASS, {n_min} FAIL-MINOR, {n_blk} FAIL-BLOCKER.

  (1) EIGENVALUE CLAIM -- HOLDS as the audited script states it (block-diagonal on (u_DC, u_AC),
      eigenvalues {{0, -(gamma Omega)^2}}), verified three independent ways including a curvilinear route
      with the full connection and a boosted frame.  The LEAD as literally handed in ("eigenvalue
      -Omega^2 ON u_mu") is FALSE -- u is not an eigenvector -- and the split additionally requires a
      PARALLEL-PROPAGATED frame, which the audited script does not say.  No number moves.
  (2) BRANCH -- correct sheet, and no branch error could inflate the rescue: |K| = 1 and |arg K| are the
      SAME on both sides of the cut; only sign(Im K) flips.  One unreported clash: in the record's own
      convention Im G < 0 while Im K > 0, so the kernel's tangential force is RETROGRADE where the
      gate's is PROGRADE.  Magnitudes, and therefore every verdict, unaffected.
  (3) MANUFACTURED RESCUE -- NOT FOUND, and the one live vulnerability is now closed analytically.  The
      kernel's coefficient GROWS as 1/Omega, so the gate's binding orbit is the kernel's most favourable
      one; the exact closed form t_e = (2c/a0) g_obs/(g_obs - g_bar) >= 2c/a0 = {floor['canon'][0]/GYR:.0f} Gyr (canon) /
      {floor['alt'][0]/GYR:.0f} Gyr (alt) makes the result ORBIT-INDEPENDENT ({floor['canon'][0]/(10*GYR):.0f}x / {floor['alt'][0]/(10*GYR):.0f}x margin vs 10 Gyr;
      {floor['canon'][0]/2/(10*GYR):.0f}x / {floor['alt'][0]/2/(10*GYR):.0f}x with the faster Keplerian form), confirmed on 57,600 orbits.  The loop WAS
      closed: with the gate retained the single-pole window is EMPTY by {closure[('canon','GATE 0.300')][2]:.0f}x / {closure[('alt','GATE 0.300')][2]:.0f}x.
      Reservation carried: the 2.6e-5 is a cross-axis HYBRID, so the honest object is the BRACKET
      [0, {ImK_neg(OMEGA_GAL, A0_ALT):.1e}] for action-sourced tangential coefficients -- the gate's 0.300 sits
      {ImG_edge/ImK_neg(OMEGA_GAL, A0_ALT):.0e}x outside it, so the refutation survives at the bracket's top.
  (4) MANUFACTURED KILL -- NOT FOUND.  0.300 was not assumed about the action: it is an identity of the
      gate (|G|^2 = Re G, sympy residual 0), and the lead was tested rather than dismissed.
  (5) REDUNDANCY -- omega_c is NOT redundant, and the closure is now family-wide: |1 - K| is strictly
      DECREASING in frequency, so K's frequency dependence suppresses galaxies MORE than planets, the
      wrong way by ~1.1e6.  The extraordinary claim was not made, and could not have been.
  (6) DC-vs-DC -- faced, and independently re-closed: g(1-K) -> a0/2 exactly (frequency- AND
      acceleration-independent), and the eccentric escape dies in closed form,
      <1/|a|><|a|> = (1 + 3e^2/2)/sqrt(1-e^2) >= 1 on all four planets.
  (7) CALIBRATION -- both footings on every load-bearing number; verdict strings computed; asserts
      phrased to fail; gate-only scope held; no TOE / "theory closed" language.  One numerological
      flourish flagged in the explicitly non-load-bearing Sec. 8.

  WHICH PRONG DOES THE ACTION IMPLY?  PRONG B, and the audit sustains it.  The load-bearing pieces are
  IDENTITIES of the kernel, not modelling choices: |K(-omega^2+i0)| = 1 at every orbital frequency (so
  the action supplies NO amplitude suppression anywhere), and g(1-K) = a0/2 exactly (so the tail is
  frequency- and acceleration-independent).  Reading A's galactic catastrophe is a property of the GATE,
  not of the action -- every action-sourced tangential coefficient is <= 3.2e-5 and the e-folding time
  cannot fall below the kernel's own memory time 2c/a0.  The consequence is not a rescue: the ungated
  sunward a0/2 tail stands, excluded {min(t[1] for t in excl['canon']):.0f}x-{max(t[1] for t in excl['canon']):.0f}x per planet (canon) / {min(t[1] for t in excl['alt']):.0f}x-{max(t[1] for t in excl['alt']):.0f}x (alt), and the
  single-pole gate that was supposed to mitigate it is excluded from the other side as well.

  WHAT REMAINS OPEN, stated so it is not read as closure: the EOM was never varied (the tangential
  coefficient is a heuristic on both readings, which is why it is reported as a bracket); the double-pole
  overlay's window is genuinely non-empty as an AMENDMENT and Gaia DR4 discriminates it against the
  single pole in opposite directions; and the acceleration-scale separator was not attempted.  Nothing
  here is a claim that the framework, or any door, is closed.

  SCOPE, held: this bears on the GATE ONLY.  The MOND premise, a0 = c H_Lambda / Z, the galactic RAR and
  the exact a0-line g_obs^2 - g_bar^2 = a0 g_bar are untouched by every number above -- none uses omega_c.
""")
print(RULE)
print(f"AUDIT_mi_kernel_axis_gate_2026.py: {len(FINDINGS)} findings "
      f"({n_pass} PASS / {n_min} FAIL-MINOR / {n_blk} FAIL-BLOCKER); all independent checks passed "
      f"(Box_u block form 3 routes incl. curvilinear + boost; branch magnitude shown branch-independent; "
      f"e-fold floor 2c/a0 verified on 57,600 orbits; |1-K| monotonicity closes the channel family; "
      f"Cauchy-Schwarz closed form matches the committed numerics to 4 s.f.; double-pole window "
      f"reproduced to <2%).")
print(RULE)
