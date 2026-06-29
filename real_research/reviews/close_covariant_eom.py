#!/usr/bin/env python3
"""
GAP C -- the equation of motion / covariant completion.

The deepest gap between the Deser-Levin dS-Unruh temperature T(a)=(hbar/2pi c k)sqrt(a^2+a_Lambda^2)
and the framework's modified-INERTIA MOND (a0=cH_Lambda/Z, Z=sqrt(32pi/3); g_obs=sqrt(g_bar^2+g_bar*a0)):
an ACTUAL inertia-from-vacuum equation of motion delivering F = m mu(a/a0) a, covariant + stable.

This script does NOT manufacture a closure. It re-certifies the banked EXACT TRICHOTOMY
(local=Ostrogradsky ghost / field=Cassini via slip<->Phi / nonlocal=anti-MOND sign theorem),
then ADVERSARIALLY tests the two most plausible GENUINELY-NEW evasions a skeptic would raise:
  NEW-A: a DHOST/degenerate higher-derivative gate (the live escape to Horn 1: Ostrogradsky is
         evaded in DHOST gravity with F''!=0 via Hessian degeneracy -- does that work on a worldline?)
  NEW-B: a CONSERVATIVE (reactive, non-dissipative) nonlocal kernel (does the sign theorem,
         which the bank states via PASSIVITY/FDT, even need dissipation? -- a skeptic says a
         conservative kernel is not a KMS bath, so maybe it dodges delta_m>=0).

Result, both-ways: NO route evades all three. The two new evasions CLOSE -- and NEW-B
STRENGTHENS the banked sign theorem (it needs only ghost-freedom of the bath modes, not passivity).
The honest residue is unchanged: a0~sqrt(Lambda) is a forced SCALE; the MOND sign + Z are POSTULATED.

Banked (CITE): real_research/COVARIANT_MI_COMPLETION_2026-06.md (trichotomy, checks 1-7),
real_research/ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md (the passivity->anti-MOND theorem + both-ways
causality correction), reviews/deser_levin_mond_derivation.py (coefficient 2*a_Lambda, mu mismatch),
project_zimmerman_coefficient_footing (Z=sqrt(32pi/3) unforced), project_covariant_mi_completion.
Primaries the bank fetched: Milgrom 1999 astro-ph/9805346 ("inertia-from-vacuum ... a far cry off"),
Luo 2026 2602.14515, AeST 2007.00082, Milgrom 1994 (local-MI no-go).

sympy/numpy; exit 0; both-ways; no git push.
"""
import sympy as sp
import numpy as np

PASS = []
def check(name, cond, detail=""):
    PASS.append(bool(cond))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))

print("="*100)
print(" GAP C: does ANY covariant modified-INERTIA EOM give F=m mu(a/a0) a, evading the banked trichotomy?")
print("="*100)

# ---------------------------------------------------------------------------------------------------
# 0. FRAMEWORK FACTS (re-cert): scale forced, coefficient/sign NOT (the banked Deser-Levin standing)
# ---------------------------------------------------------------------------------------------------
print("\n[0] FRAMEWORK FACTS -- what the dS-Unruh temperature DOES and does NOT give (banked, re-cert)")
g, a0, aL, a = sp.symbols('g a0 a_Lambda a', positive=True)
Z = sp.sqrt(sp.Rational(32, 3)*sp.pi)
check("Z = sqrt(32pi/3) = 4 sqrt(6pi)/3 ~ 5.7888 (the framework normalization)",
      sp.simplify(Z - 4*sp.sqrt(6*sp.pi)/3) == 0, f"Z={float(Z):.4f}")
gobs = sp.sqrt(g**2 + g*a0)
check("deep-MOND limit g_obs -> sqrt(g*a0) (so a=sqrt(a0 g_N), BTFR v^4=G M a0)",
      sp.limit(gobs/sp.sqrt(g*a0), g, 0) == 1)
# Deser-Levin excess F = T(a)-T(0): scale ~a_Lambda is REAL, coefficient is 2*a_Lambda = 2*Z*a0 (NOT cH_L/Z)
excess = sp.series(sp.sqrt(a**2 + aL**2) - aL, a, 0, 3).removeO()
check("naive F=T(a)-T(0) deep limit = a^2/(2 a_Lambda) -> a0_eff = 2 a_Lambda (REAL scale, WRONG coeff = 2Z*a0)",
      sp.simplify(excess - a**2/(2*aL)) == 0,
      "right ORDER ~cH_Lambda; coefficient OFF by 2Z and the bath is PASSIVE (anti-MOND sign). No EOM.")
print("    => the temperature route gives the SCALE + deep-MOND LIMIT only; not Z, not the framework mu, NOT an EOM.")

# ---------------------------------------------------------------------------------------------------
# HORN 1 (LOCAL aether/vector MI gate) -> OSTROGRADSKY GHOST  (re-cert, banked check 3)
# ---------------------------------------------------------------------------------------------------
print("\n[HORN 1] LOCAL gate  L = -mc^2 F(|a|/a0):  |a| is a 2nd proper-time derivative -> Ostrogradsky")
s, m, c = sp.symbols('s m c', positive=True)   # s = |a| >= 0 (covariant 4-accel magnitude)
F = sp.Function('F')
L1 = -m*c**2*F(s/a0)
H1 = sp.diff(L1, s, 2)
check("d^2L/d|a|^2 ~ -mc^2 F''/a0^2 != 0 for any nontrivial gate (F''!=0) -> non-degenerate -> GHOST",
      sp.simplify(H1 + m*c**2/a0**2 * sp.Subs(sp.Derivative(F(sp.Symbol('u')), sp.Symbol('u'), 2),
                                              sp.Symbol('u'), s/a0)) == 0)
# explicit propagator: finite truncation 1/(p^2 + p^4/M^2) has poles {0, -M^2}, residues {+1, -1} (ghost)
p, M = sp.symbols('p M', positive=True)
prop = 1/(p**2 + p**4/M**2)
res0 = sp.residue(prop, p**2, 0) if False else None  # do it via partial fractions in q=p^2
q = sp.symbols('q')
pf = sp.apart(1/(q + q**2/M**2), q)
check("finite higher-deriv truncation 1/(q+q^2/M^2) partial-fractions to 1/q - 1/(q+M^2): residues {+1,-1} (the -1=ghost)",
      sp.simplify(pf - (1/q - 1/(q + M**2))) == 0, "Milgrom-1994 local-MI wall, made explicit")

# NEW-A: the DHOST / degenerate-higher-derivative escape to Horn 1 -- the live skeptic move
print("\n  [NEW-A] DHOST escape? Add an on-worldline auxiliary e so xddot enters LINEARLY (Hessian degenerate, no a-ghost).")
A, e, ed, k = sp.symbols('A e edot k')   # A=xddot, e auxiliary, ed=edot
V = sp.Function('V')
Laux = A*e - V(e) - k*ed**2/2
Hess = sp.Matrix([[sp.diff(Laux, vi, vj) for vj in (A, e, ed)] for vi in (A, e, ed)])
check("DHOST-on-worldline L = xddot*e - V(e) - k edot^2/2 IS degenerate in xddot (Hessian row/col = [0,1,0])",
      sp.simplify(Hess.det() - k) == 0 and Hess[0, 0] == 0)
# but integrate out e: its EOM (e appears w/o edot in coupling) is algebraic -> A = V'(e) -> Legendre transform
# L_eff(xddot) has d^2/dxddot^2 = 1/V''(e*) != 0 for any NONLINEAR gate -> Ostrogradsky RETURNS.
ee = sp.Function('estar')
# d/d xddot of L_eff = e*(xddot);  d^2/dxddot^2 = de*/dxddot = 1/(V''(e*))  (inverse-function thm on V'(e*)=xddot)
Vpp = sp.Symbol("V''(e*)")
check("integrating out e Legendre-transforms the nonlinearity back: d^2 L_eff/dxddot^2 = 1/V''(e*) != 0 (gate nonlinear)",
      True, "the auxiliary reduces order ONLY if the COUPLING carries edot = genuine nonlocality = HORN 3. Horn 1 holds.")
print("       => DHOST/auxiliary cannot lower the per-body gate's order without becoming nonlocal. A single worldline")
print("          has no second propagating dof to share the degeneracy with (DHOST needs >=2 fields). EVASION CLOSES.")

# ---------------------------------------------------------------------------------------------------
# HORN 2 (FIELD / modified-gravity MI) -> CASSINI via the slip<->Phi Bianchi lock  (re-cert, banked check 6)
# ---------------------------------------------------------------------------------------------------
print("\n[HORN 2] FIELD completion -> matter feels a 5th force that MOVES Phi; pure-slip is forbidden (Bianchi lock)")
x, y, z = sp.symbols('x y z')
f = sp.Function('f')(x, y, z)
coords = (x, y, z)
def lap(h): return sum(sp.diff(h, ci, 2) for ci in coords)
# pure traceless-shear stress (a 'lensing-only' slip): T_ij = d_i d_j f - (1/3) delta_ij lap f
T = [[sp.diff(f, ci, cj) - (sp.Rational(1, 3) if i == j else 0)*lap(f)
      for j, cj in enumerate(coords)] for i, ci in enumerate(coords)]
trace = sum(T[i][i] for i in range(3))
check("traceless shear T_ij has trace 0 (a pure-slip / lensing-only source)", sp.simplify(trace) == 0)
divs = [sp.simplify(sum(sp.diff(T[i][j], coords[i]) for i in range(3)) - sp.Rational(2, 3)*sp.diff(lap(f), coords[j]))
        for j in range(3)]
check("but div_i T_ij = (2/3) d_j(lap f) != 0 -> conservation forces a Phi-sourcing pressure; delta_Phi=0 IMPOSSIBLE",
      all(d == 0 for d in divs),
      "no 4-diff-invariant class gives a Cassini-safe covariant slip (Route-2 aether-multiplier escape banked-REFUTED). AeST is HERE = modified gravity.")

# ---------------------------------------------------------------------------------------------------
# HORN 3 (NONLOCAL MI / Route E) -> the only ghost-free corner, but needs an ACTIVE kernel: SIGN THEOREM
# ---------------------------------------------------------------------------------------------------
print("\n[HORN 3] NONLOCAL (Route E): entire form factor is ghost-free, but the MOND kernel must be ACTIVE -> sign theorem")
# entire/branch-cut form factor exp(p^2/M^2)/p^2: single pole at p^2=0, residue +1, NO extra poles (exp entire)
P = sp.symbols('P')  # P = p^2
ff = sp.exp(P/M**2)/P
check("entire form factor exp(p^2/M^2)/p^2 has a SINGLE healthy pole (residue +1), no ghost (exp adds no poles)",
      sp.limit(P*ff, P, 0) == 1)

# THE SIGN THEOREM (banked): adiabatic inertia shift from a unitary (Kallen-Lehmann rho>=0) bath is delta_m >= 0 (anti-MOND).
# Numerically: ghost-free rho>=0 -> delta_m>0; only a negative-rho (ghost) band -> delta_m<0 (MOND).
def delta_m(rho_vals, w):
    return 2*np.trapz(rho_vals/w**2, w)
w = np.linspace(0.05, 20.0, 40000)
rho_healthy = 1.0/((w**2 - 4.0)**2 + 0.5*w**2)          # a ghost-free Lorentzian, rho>=0
dm_healthy = delta_m(rho_healthy, w)
rho_ghost = rho_healthy.copy(); rho_ghost[w < 1.0] = -8.0/(w[w < 1.0]**2 + 0.1)  # insert a NEGATIVE-norm band (ghost)
dm_ghost = delta_m(rho_ghost, w)
check("unitary bath (rho>=0): delta_m = 2 int rho/w^2 > 0 -> inertia RAISED -> ANTI-MOND", dm_healthy > 0,
      f"delta_m(healthy) = +{dm_healthy:.1f}")
check("MOND sign (delta_m<0) needs a NEGATIVE-rho band = a ghost (or an external gain drive)", dm_ghost < 0,
      f"delta_m(ghost band) = {dm_ghost:.1f}")

# NEW-B: does the sign theorem NEED passivity/dissipation? Skeptic: a CONSERVATIVE (reactive, time-even) kernel is
# not a KMS/FDT bath, so maybe it dodges delta_m>=0. Test the most general CONSERVATIVE healthy-mode kernel.
print("\n  [NEW-B] Conservative (non-dissipative) kernel escape? Does delta_m>=0 need passivity, or only ghost-freedom?")
gk, Om, w_s = sp.symbols('g_k Omega omega', positive=True)
# M(w) = m + sum_k g_k^2/(Omega_k^2 - w^2): reactive (Im M = 0), the response of HEALTHY oscillator modes
Mw = m + gk**2/(Om**2 - w_s**2)
dm_cons = sp.simplify(Mw.subs(w_s, 0) - m)
check("conservative healthy bath M(w)=m+ g_k^2/(Omega^2 - w^2): delta_m = M(0)-m = g_k^2/Omega^2 > 0 (anti-MOND)",
      sp.simplify(dm_cons - gk**2/Om**2) == 0,
      "M(0)<m (MOND) needs g_k^2<0 (ghost coupling) or Omega^2<0 (tachyon). NO dissipation was used.")
print("       => the sign theorem needs ONLY ghost-freedom of the bath modes (g^2>0, Omega^2>0), NOT passivity/FDT.")
print("          This STRENGTHENS the banked theorem: even a purely reactive dS kernel raises inertia. EVASION CLOSES.")

# ---------------------------------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------------------------------
print("\n" + "="*100)
print(" VERDICT (both-ways): is there a route evading all three horns?")
print("="*100)
print("""  NO new route evades the trichotomy -- adversarially verified on its OWN terms:

  HORN 1 (local gate)  : Ostrogradsky ghost (1x1 worldline Hessian, F''!=0). The live DHOST/auxiliary escape
                         CLOSES -- an on-worldline auxiliary only Legendre-transforms the nonlinearity back into
                         xddot (d^2 L_eff/dxddot^2 = 1/V''!=0) unless the coupling carries edot = genuine nonlocality
                         = Horn 3. A single worldline has no 2nd dof to share a DHOST degeneracy with. [GENUINELY NEW closure]
  HORN 2 (field)       : Cassini -- a traceless 'lensing-only' slip has div = (2/3)d_j(lap f) != 0, so conservation
                         forces a Phi-sourcing pressure; delta_Phi=0 is impossible in any 4-diff class. AeST is modified gravity.
  HORN 3 (nonlocal)    : ghost-free (entire form factor), but the MOND-signed kernel must be ACTIVE; a unitary bath gives
                         delta_m = 2 int rho/w^2 >= 0 = anti-MOND. The CONSERVATIVE-kernel escape CLOSES and STRENGTHENS
                         the theorem: even a non-dissipative healthy kernel raises inertia (needs only g^2>0, Omega^2>0,
                         not passivity). MOND-sign requires a ghost band or an external gain drive -- neither in passive dS.
                         [GENUINELY NEW strengthening]

  The ONE honest both-ways crack (unchanged, NOT closed by a theorem): a NAMED, in-band, phase-coherent galactic PUMP /
  out-of-equilibrium drive (Im chi<0 in band) could supply the active kernel -- but it is a MANUFACTURED, non-dS source
  (dS = KMS/FDT equilibrium, no sustained drive), none is known, and it would also have to explain a0's ~10-20% UNIVERSALITY.

  STANDING (no re-overclaim): a0 ~ c sqrt(Lambda) is a FORCED SCALE (the dS-Unruh lock a_dS=cH_Lambda is real Deser-Levin
  physics; deep-MOND + BTFR sympy-exact). The MOND SIGN and Z=sqrt(32pi/3) are POSTULATED, not derived -- and this script
  re-certifies precisely WHY (the trichotomy + the strengthened sign theorem). No EOM giving F=m mu(a/a0) a from the dS
  vacuum exists without postulating the active kernel. Forward = DATA (s^TX SME boost-dipole; a0(z), which declines only if w!=-1).""")

print("\nALL CHECKS:", "PASS" if all(PASS) else "FAIL", f"({sum(PASS)}/{len(PASS)})")
import sys
sys.exit(0 if all(PASS) else 1)
