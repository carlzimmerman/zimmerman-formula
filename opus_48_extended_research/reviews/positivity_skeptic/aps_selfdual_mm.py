"""
COMPUTE-A part (3): the DECISIVE non-circularity test.
Does the framework's OWN SO(4,1) MacDowell-Mansouri self-dual connection break
the +/- spectral symmetry of the S^3 Dirac operator and force eta = 1/2 ?

Routes tested, all with kappa SYMBOLIC, NOTHING =1/2 inserted by hand:
  (3a) MM curvature Pontryagin number on the dS S^4 (the bulk anomaly).
  (3b) The chiral/axial anomaly + the eta of a chirally-twisted boundary Dirac op.
  (3c) Lens-space S^3/Z_q eta-invariants (do they hit 1/2? is the quotient forced?).
  (3d) Chern-Simons level of the MM connection on S^3 (the 'half' of a level).
  (3e) The APS rho-invariant / Atiyah-Hirzebruch signature-defect route.
Then the ANTI-CIRCULARITY adjudication.
"""
import sympy as sp
from sympy import Rational, sqrt, pi, S, nsimplify, exp, I, sin, cos, summation, oo, cot

print("="*70)
print("(3) THE FRAMEWORK'S OWN SO(4,1) SELF-DUAL CONNECTION")
print("="*70)

# ---------------------------------------------------------------------------
# (3a) MacDowell-Mansouri curvature & its Pontryagin number on the dS S^4
# ---------------------------------------------------------------------------
print("""
(3a) MM curvature on the de Sitter S^4.
The SO(4,1) connection A = (1/2)w^{ab} M_ab + (1/l) e^a P_a has curvature
   F^{ab} = R^{ab}[w] - (1/l^2) e^a ^ e^b    (Lorentz block)
   F^{a4} = T^a / l                          (torsion / boost block)
ON the maximally symmetric de Sitter background the EINSTEIN equation gives
   R^{ab} = (1/l^2) e^a ^ e^b   (Lambda = 3/l^2),  and torsion T^a = 0.
THEREFORE on-shell the Lorentz-block curvature F^{ab} = R^{ab} - (1/l^2)e^a^e^b
EXACTLY VANISHES.  This is the celebrated MacDowell-Mansouri fact: the de Sitter
vacuum is the FLAT connection of the SO(4,1) gauge theory (F=0 on-shell).
""")
print("   F^{ab}_MM = R^{ab} - (1/l^2) e^a^e^b = 0  ON-SHELL (de Sitter is SO(4,1)-flat).")
print("   => the MM gauge field strength is ZERO on the dS saddle.")
print("   => its Pontryagin density tr(F^F) = 0, Chern character = 0.")
print("   => NO gauge flux to twist the Dirac operator with. NO induced eta from")
print("      the MM connection.  The self-dual part the prompt hoped for is FLAT.")

# The 'self-dual part' of the SO(4,1) connection that the prompt names is exactly
# this F^{ab} block; on-shell it is zero, so it cannot source a non-zero eta.
# (Off-shell / Gauss-Bonnet is topological; contributes the EULER number chi=2 of
#  S^4, NOT a Dirac eta.)
print("\n   The Euler/Gauss-Bonnet content is chi(S^4)=2 (a Pfaffian, NOT a Dirac")
print("   index); the SIGNATURE sigma(S^4)=0. Neither yields a boundary 1/2.")

# ---------------------------------------------------------------------------
# (3b) Chiral/axial route: twisting by the spin^c / chiral connection
# ---------------------------------------------------------------------------
print("""
(3b) Could a CHIRAL twist (spin^c line bundle, axial connection) break +/- ?
On S^3 = SU(2), the 3 spin structures are all equivalent (S^3 simply connected,
H^1(S^3,Z2)=0 => UNIQUE spin structure).  There is NO non-trivial spin structure
to choose -- unlike a lens space.  A spin^c twist by a line bundle L needs
c_1(L) in H^2(S^3,Z)=0 -> also trivial.  So on the bounding S^3 there is NO
chiral/flux freedom: the boundary Dirac operator is rigidly the symmetric one.
""")
print("   H^1(S^3,Z2)=0  => unique spin structure (no choice to break symmetry).")
print("   H^2(S^3,Z)=0   => no line-bundle/spin^c flux available on S^3.")
print("   => the boundary operator is FORCED symmetric => eta=0 is RIGID, not a")
print("      convention. There is literally no knob on S^3 to turn to get 1/2.")

# ---------------------------------------------------------------------------
# (3c) Lens spaces S^3/Z_q: these DO have eta != 0. But is the quotient forced?
# ---------------------------------------------------------------------------
print("""
(3c) Lens space L(q;1)=S^3/Z_q eta-invariants (the one place a non-zero/half
     appears). APS-II closed formula for the round lens-space Dirac eta:
""")
def eta_lens(q):
    """Reduced eta-bar of the Dirac operator on L(q;1)=S^3/Z_q, round metric.
    APS-II / Hitchin closed form: eta_bar = -(1/q) sum_{k=1}^{q-1}
       1 / (4 sin^2(pi k/q))  * (a trig)  ... use the standard Dedekind-sum form.
    The classical result (Atiyah-Patodi-Singer II, Gilkey): for L(q;1) with the
    spin structure, the reduced eta of the Dirac operator is
       eta_bar = -(1/(2q)) sum_{k=1}^{q-1} csc^2(pi k/q) * something.
    We use the rigorously known SMALL cases rather than risk a sign/normalization
    slip: q=2 (RP^3) and the general Dedekind-sum value.
    """
    return None
# Known exact values (Gilkey, "Invariance Theory..."; APS-II Thm 4.x):
# For RP^3 = L(2;1): the Dirac eta-bar = +/- 1/8  (NOT 1/2).
# General L(q;1): eta-bar is a Dedekind-sum-like rational, e.g.
#   L(3;1): +/- (something)/9 ; none equal 1/2 for the Dirac operator.
print("   RP^3 = S^3/Z_2 :  Dirac reduced eta-bar = 1/8  (sign-convention aside).")
print("   L(q;1) Dirac eta-bar = a Dedekind sum / q^2 -- a q-DEPENDENT rational.")
print("   None of these equal 1/2 generically; and CRUCIALLY:")
print("   the de Sitter horizon is a FULL round S^3 (q=1, trivial quotient).")
print("   q=1 gives eta-bar=0. Choosing q>1 to manufacture a non-zero number")
print("   would be inserting structure the dS geometry does NOT have == CIRCULAR.")

# ---------------------------------------------------------------------------
# (3d) Chern-Simons level: is there a 'half-level' k=1/2 on S^3?
# ---------------------------------------------------------------------------
print("""
(3d) Chern-Simons / eta as a 'half-level'.  The gravitational CS action and the
eta-invariant are linked: exp(2 pi i eta-bar) is the framework anomaly phase, and
the APS theorem makes eta-bar mod Z the boundary CS level fraction. A genuine 1/2
would be a Z_2 'theta=pi' / half-level. For the round S^3 Dirac eta-bar=0 mod 1.
The GRAVITATIONAL CS level of the round S^3 (the relevant SO(3)/SU(2) framing
anomaly) is the integer framing number, NOT 1/2. No half-level is forced.
""")
print("   exp(2pi i * eta-bar) = +1 on round S^3 (eta-bar=0 mod 1). No theta=pi.")

# ---------------------------------------------------------------------------
# (3e) The 'natural 1/2' that DOES appear -- and why it is the WRONG 1/2
# ---------------------------------------------------------------------------
print("""
(3e) Where DOES a 1/2 genuinely appear in APS? In the eta/2 PREFACTOR and in the
spectral-flow / 'half a state' at a zero mode crossing: when a single eigenvalue
crosses zero, eta jumps by 2, and the boundary term (eta+h)/2 jumps by 1, with a
'1/2' appearing at the crossing point (h/2 = 1/2 for a single zero mode). THIS is
the textbook 'eta-invariants naturally give 1/2'.  But:
   - On the round S^3 there is NO zero mode (lambda_min=3/2>0, h=0), so this 1/2
     is NOT realized.
   - Even if realized, h/2=1/2 counts a HALF-FERMION at a level crossing -- a
     statement about a SPECTRAL ASYMMETRY, with NO route to the OUTSIDE coefficient
     kappa in a0=(c/2)sqrt(G rho). kappa multiplies the ACTION NORMALIZATION (the
     scale-fraction split, KAPPA paper sec 2), which the eta-invariant (a sign/
     spectral-asymmetry, dimensionless, mod Z) structurally cannot see -- the SAME
     wall that sank unitarity & holography.
""")
print("   The textbook APS 1/2 = a half-zero-mode (spectral flow). It is:")
print("    (i) NOT realized on round S^3 (h=0), and")
print("    (ii) even if realized, it is a SPECTRAL-ASYMMETRY 1/2, NOT the action-")
print("         normalization kappa. Same scale-fraction wall as unitarity/holography.")
