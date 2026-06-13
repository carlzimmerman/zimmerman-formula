"""
agentSS Part 1 — set up the dS static-patch QNM spectral function and its moments,
test SL(2,R) ladder structure for forcing 4 j3/j2^2.

THE SETUP (from agentS_edge_qnm.md + agentRR_saturated_fold.md):
- dS static-patch scalar QNMs: omega_N = -i H (Delta + N), N=0,1,2,...  (purely imaginary ladder)
- The q-deformed (finite-lambda) version: Gamma_n = sinh((Delta+n) lambda), lambda = -ln q = H_eff
  (banked agentS: the DSSYK pole tower at center). lambda->0: Gamma_n -> (Delta+n) lambda = dS ladder.
- These are the WIDTHS (imaginary parts / decay rates) of the QNM poles.

THE EDGE SURFACE (agentRR): the active gain line must satisfy
    sigma4 = -G j2 c^2,   sigma6 = +G j3 c^2
where j2, j3 are the 2nd and 3rd MOMENTS of the (normalized) spectral line shape rho(s),
   j_n = int rho(s) s^n ds / (normalization),   s = spectral variable (= omega^2 offset / detuning).
The NO-fold / fold geometry: sigma6* = sigma4^2/(4 c^2). Edge coincidence sigma6 = sigma6* gives
    sigma6/sigma6* = 4 j3 /(G j2^2)   ==>  EDGE EQ:  G = 4 j3 / j2^2   (G_sat target).
So the question: does the QNM spectral function's OWN moment ratio  4 j3/j2^2  land on G_sat
BY A SYMMETRY, or only for tuned Delta, lambda?

KEY DISTINCTION I must keep straight:
 - j2, j3 are moments of the LINE-SHAPE rho(s) of a *single* peaked active resonance used as the
   roton-building kernel. The "QNM spectral function" is the FULL tower (a sum of poles). The brief's
   claim to test: the dS QNM ladder *is* an SL(2,R) representation; does the rep structure fix the
   moment ratio of the resulting spectral density?
"""
import sympy as sp

# ---------------------------------------------------------------
# 1. The QNM ladder rate spectrum.
# ---------------------------------------------------------------
n, N = sp.symbols('n N', integer=True, nonnegative=True)
Delta, lam, H = sp.symbols('Delta lambda H', positive=True)

# finite-lambda (DSSYK) widths
Gamma_n = sp.sinh((Delta + n)*lam)
# semiclassical dS limit lambda->0
Gamma_n_dS = (Delta + n)   # times lambda (H_eff); spacing is uniform

print("=== QNM ladder rates ===")
print("finite-lambda width  Gamma_n =", Gamma_n)
print("dS-limit (over lambda) Gamma_n/lambda ->", Gamma_n_dS)
print("spacing Gamma_{n+1}-Gamma_n (finite lambda) =",
      sp.simplify(sp.sinh((Delta+n+1)*lam) - sp.sinh((Delta+n)*lam)))
print()

# ---------------------------------------------------------------
# 2. SL(2,R): the QNM ladder as a representation.
#    The static-patch SL(2,R) (the dS_2 / near-horizon conformal algebra) acts on QNM modes.
#    A lowest-weight (discrete-series) rep has L_0 eigenvalues  Delta + n.  The generators
#    L_+, L_-, L_0 raise/lower n.  Question: does this REP STRUCTURE fix any ratio of the
#    SPECTRAL MOMENTS of the line shape built from the tower?
#
#    The rep fixes the SPACING (uniform, = lambda in dS units) and the OFFSET (Delta).
#    It does NOT, by itself, assign RESIDUES (spectral weights) to each rung. The line shape
#    rho(s) = sum_n a_n delta(s - s_n) needs the a_n (residues). Test: are a_n fixed by SL(2,R)?
# ---------------------------------------------------------------
print("=== SL(2,R) Casimir / rep test ===")
# Discrete-series lowest-weight rep: C2 = Delta(Delta-1), states |Delta+n>.
C2 = Delta*(Delta - 1)
print("SL(2,R) Casimir C2 = Delta(Delta-1) =", sp.expand(C2))
# L_0 spectrum:
print("L_0 eigenvalues: Delta + n  (uniform spacing 1, offset Delta) -> fixes SPACING & OFFSET")
print("Matrix elements |<Delta+n+1| L_+ |Delta+n>|^2 = (n+1)(2Delta+n)  [discrete series]")
me = (n+1)*(2*Delta + n)
print("   =", sp.expand(me))
print()
print(">>> These matrix elements are FIXED by the rep. Whether they ARE the spectral residues a_n")
print(">>> of the roton line shape is the load-bearing question -> Part 2.")
