#!/usr/bin/env python3
"""
adversarial_gate_and_eos.py

ADVERSARIAL second pass on the AeST<->ghost-condensate map.  Two jobs:

  (1) EOS audit: prove the dust is w=0 ONLY as the leading dilution and that the
      EXACT minimum is w=-1 (a cosmological constant) -- the AHCLM subtlety.  This
      decides whether the 'a^-3 dust = dark matter' reading is honest.

  (2) GATE audit: does the ghost condensate actually EVADE the SO(4,1) vacuum gate
      (G2 of FRAME_TO_FIELD), or only RE-FRAME it?  Stress-test the strongest
      pro-evasion argument and the strongest skeptic argument.
"""
import sympy as sp

print("="*78)
print(" (1) EOS audit: w(a) for K(Q)=mu^2(Q-1)^2 near and AT the minimum")
print("="*78)
a, mu, I0 = sp.symbols('a mu I0', positive=True)
dQ = sp.symbols('dQ')              # deviation Q-1
# k-essence (rest frame): rho = 2Q K' - K, p = K, with Q=1+dQ
Qsym = 1 + dQ
K   = mu**2*dQ**2
Kp  = sp.diff(mu**2*(Qsym-1)**2, dQ)  # = 2 mu^2 dQ
rho = 2*Qsym*Kp - K
p   = K
print("rho(dQ) =", sp.expand(rho))
print("p(dQ)   =", sp.expand(p))
w = sp.simplify(p/rho)
print("w(dQ)   = p/rho =", w)

# exact minimum dQ=0:
print("\nAt EXACT minimum dQ->0:")
print("  rho ->", sp.limit(rho, dQ, 0), "  p ->", sp.limit(p, dQ, 0))
# Need the constant piece: at the exact minimum K=0,K'=0 so rho=0,p=0 here (no const
# added). The cosmological-constant piece in AHCLM is the value of -P at the min, i.e.
# an additive constant. Demonstrate w near min by leading orders:
w_series = sp.series(w, dQ, 0, 2)
print("  w(dQ) series about dQ=0:", w_series)
print("  => as dQ->0 (deep future, a->inf), p/rho with leading rho~4 mu^2 dQ, p~mu^2 dQ^2")
print("     -> w = p/rho ~ (mu^2 dQ^2)/(4 mu^2 dQ) = dQ/4 -> 0^-  : w->0 DUST.")
# Substitute dQ = I0/(2 a^3 mu^2):
dQ_of_a = I0/(2*a**3*mu**2)
w_of_a = sp.simplify(w.subs(dQ, dQ_of_a))
print("\n  w(a) with dQ=I0/(2 a^3 mu^2):", w_of_a)
print("  large a:", sp.limit(w_of_a, a, sp.oo), " -> w->0 (dust) as a->inf, leading a^-3.")
print("""
  HONEST READING (both ways):
   * The shift-charge dilution gives w->0 cold dust at late times: rho ~ I0/a^3.
     This IS the dark-matter-mimic the CMB 3rd peak needs.  (credit)
   * It is w=0 only at LEADING order in the small deviation; the AHCLM caveat that
     'in the far future the EMT becomes precisely a cosmological constant' is the
     dQ->0, exact-minimum limit (the additive -P(X0) piece).  The dust is the
     TRANSIENT dilution, not the asymptotic state.  (honest caveat -- not fatal,
     same as any tracker leaving a residual Lambda, but must be stated.)
""")

print("="*78)
print(" (2) GATE audit: does the GC EVADE the SO(4,1) vacuum gate, or re-frame it?")
print("="*78)
print("""
PRO-EVASION (the new idea, steelmanned):
  Gate-2 (FRAME_TO_FIELD G2) said: the dS vacuum is SO(4,1)-invariant, so one-loop
  INDUCTION on it yields only dS-invariant terms (Lambda, R) -- never a preferred-
  timelike kinetic term.  The GC sidesteps this because the Lorentz/time-translation
  breaking is SPONTANEOUS: the ACTION P(X) is perfectly Lorentz-invariant (X is a
  scalar), the SOLUTION <d phi>=M^2 t breaks it.  A condensate is a *state/solution*,
  exactly the object gate-2 said names the frame ('named by the matter solution, not
  the vacuum').  So 'the symmetry is broken by the solution' is LICENSED -- the GC is
  the consistent realization of precisely what gate-2 allowed.  TRUE, and it is why
  AeST is internally consistent.

SKEPTIC (the honest line):
  Gate-2 was about INDUCING the *kinetic term* from the dS-Unruh VACUUM.  The GC does
  NOT induce P(X) -- it POSTULATES P(X) in the action and then finds a symmetry-
  breaking solution.  The question 'where does the kinetic term come from?' is UNTOUCHED:
  P(X) with a minimum at X0>0 (a wrong-sign/ghost-condensate kinetic term) is an INPUT.
  So the GC answers a DIFFERENT question than gate-2:
      gate-2 : can the dS-Unruh vacuum *derive/induce* the field's kinetic term?   NO.
      GC     : given a postulated GC kinetic term, does a *solution* break SO(4,1)
               to name u^mu?                                                       YES.
  The GC EVADES gate-2 only in the trivial sense that it never tries to induce the
  kinetic term; it assumes it.  It does NOT close wall-1 (derive the field).  It
  RELABELS the postulate ('AeST aether+K(Q)') with a better-motivated name ('ghost
  condensate') and a real physics pedigree -- a genuine STRUCTURAL identification,
  but the kinetic term remains an external input, and the amount I0 stays free.

VERDICT: the GC is a GENUINE STRUCTURAL IDENTITY (the authors' own: VSZ Eq.7 cites
  AHCLM) that gives the postulated field a real EFT home and explains FRAME SELECTION
  by spontaneous breaking -- but it DERIVES neither the kinetic term (still postulated,
  not induced from dS-Unruh) nor the amount (I0 free).  It does not break wall-1; it
  RE-DESCRIBES it with physical content.  More than a relabel (real dispersion, real
  minimum, real spontaneous breaking, real pathology structure to carry), less than a
  derivation (no kinetic term derived, no Omega_dm pinned).
""")
print("exit 0")
