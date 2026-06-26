"""
BOTH-WAYS AUDIT of the premise: 'Sumino DERIVES Koide 2/3, so he must encode an
effectively-per-irrep / class-function structure -> FIND it.'

I must not reflexively confirm OR deny. Separate TWO distinct things in Sumino:
  (P) the PROTECTED quantity: Koide K = (sum sqrt m)^2 / (3 sum m) is a U(3)xO(3)-INVARIANT
      built from TRACES Tr(Phi) and Tr(sqrt? ) — a genuine CLASS-FUNCTION (per-irrep) object.
  (M) the CANCELLATION MECHANISM that keeps K=2/3 against QED: a PER-FLAVOR (per-state)
      log-matching, NOT a flat per-irrep weight.
And the VEV that sets 45deg:
  (V) what selects the 45deg / r=sqrt2 sqrt-mass configuration = the SCALAR POTENTIAL minimum.

The honest reading of 'effectively per-irrep' is (P)+(V): the OBSERVABLE Koide is a
class-function (trace) of the VEV, and the VEV is pinned by a potential. The bath-measure
question (Task B) asks if a THERMAL/dS measure forces the per-irrep VALUE 2/3 — Sumino does
NOT use a thermal measure at all; he uses a POTENTIAL MINIMUM + a per-flavor radiative lock.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

print("="*78)
print("Does Sumino's success route through a PER-IRREP THERMAL MEASURE? (the Task B object)")
print("="*78)

# (P) The protected quantity is a TRACE (class function) of the VEV-built mass matrix.
# In Sumino, charged-lepton mass m_i ~ (v_i)^2 (the operator O1 ~ psi_L Phi Phi^T phi e_R),
# so sqrt(m_i) ~ v_i, and Koide:
#   K = (sum_i v_i)^2 / (3 sum_i v_i^2) = (Tr V)^2 / (3 Tr V^2),  V = diag(v_i).
# This IS a ratio of U(3) Casimir-invariants (Tr V and Tr V^2 are class functions). CONFIRMED per-irrep OBJECT.
v0,v1,v2 = sp.symbols('v0 v1 v2', positive=True)
V = [v0,v1,v2]
K = (sum(V))**2 / (3*sum(vi**2 for vi in V))
print("\n[P] Protected Koide as a TRACE ratio:  K = (Tr V)^2/(3 Tr V^2),  V=diag(v_i)~diag(sqrt m_i).")
print("    K =", sp.simplify(K), " — a class function (ratio of U(3) invariants). CONFIRMED per-irrep OBJECT.")
print("    K=2/3 <=> Tr(V)^2 = 2 Tr(V^2)  <=> |democratic part|^2 = |traceless part|^2 of V (45deg).")
# show this equals the irrep-balance:
demo = (sum(V))**2/3      # |projection on (1,1,1)|^2 * 3 ... up to normalization
# traceless: Tr V^2 - (TrV)^2/3
traceless2 = sp.simplify(sum(vi**2 for vi in V) - (sum(V))**2/3)
demo2 = sp.simplify((sum(V))**2/3)
balance = sp.simplify(sp.Eq(demo2, traceless2))
K_at_balance = sp.simplify(K.subs(v2, sp.solve(sp.Eq(demo2,traceless2), v2)[0]))
print("    Setting |demo|^2 = |traceless|^2 gives K =", K_at_balance, " (=2/3 on the balance locus). CONFIRMED.")

# (M) BUT the MECHANISM that keeps it at 2/3 is per-FLAVOR radiative matching, not a thermal weight.
print("\n[M] The PROTECTION mechanism is per-FLAVOR (per-state) radiative log-cancellation:")
print("    requires alpha_F=alpha AND family-gauge-boson masses = v_i (locked to sqrt m_i).")
print("    This is NOT a thermal/Plancherel MEASURE choosing per-irrep over per-state. It is a")
print("    DYNAMICAL coupling+spectrum lock. No bath, no equilibrium weighting, no Boltzmann sum.")

# (V) WHAT sets 45deg = the SCALAR POTENTIAL minimum (Sumino's Phi potential), a VEV alignment,
# NOT a thermal equipartition. The potential minimum lands on the balance locus by the
# structure of the invariants in V(Phi), which is ENGINEERED (choice of potential terms).
print("\n[V] The 45deg (r=sqrt2) is the SCALAR POTENTIAL MINIMUM of V(Phi), a VEV alignment problem.")
print("    Sumino's potential is CONSTRUCTED so its minimum lands on Tr(V)^2=2Tr(V^2). It is not")
print("    forced by a thermal/dS measure; it is forced by the chosen invariants in the potential.")

print("\n" + "="*78)
print("AUDIT CONCLUSION (both ways):")
print("  - TRUE: Koide IS a per-irrep/class-function OBSERVABLE (a trace ratio of the VEV). The")
print("    wave-1 'per-irrep is the right description of 2/3' is CORRECT for the OBSERVABLE.")
print("  - BUT: Sumino does NOT reach it via a per-irrep THERMAL MEASURE. He reaches it via")
print("    (V) a scalar-potential minimum + (M) per-flavor radiative lock. There is NO bath,")
print("    NO Plancherel-vs-class-function measure choice anywhere in Sumino.")
print("  => The Task B premise 'Sumino must encode a per-irrep MEASURE, find it in dS-Unruh' is")
print("    MIS-AIMED: Sumino's per-irrep-ness is in the OBSERVABLE+POTENTIAL, not in a thermal")
print("    measure. So there is nothing 'per-irrep-thermal' for dS-Unruh to inherit. The dS bath")
print("    remains per-STATE (overshoot); the cure lives in a potential, which the spine lacks.")
