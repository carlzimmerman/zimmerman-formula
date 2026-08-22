"""
Weak-field metric, MOND dynamics, and lensing FROM the LY/CMC solution of the
CMC-gauge MOND-deformed theory.  DOF phase verdict: 2 DOF (conditional on LY
unique solvability).  This script does the weak-field consequences.

Conventions: c=1 (restored in prose), static, asymptotically flat local patch.
The GLOBAL CMC number q=K=3H and a0=cq/Z are treated as fixed constants; the
cosmological (2/3)K^2 and A^2 momentum terms are second order in the local patch
and dropped (standard PPN of a slice).

Metric ansatz:
  N        = 1 + Phi_g            (lapse -> TIME potential Phi_g)
  h_ij     = psi^4 delta_ij,  psi = 1 + psi1,   g_ij=(1-2 Psi_g) delta_ij
             => psi1 = -Psi_g/2   (SPACE potential Psi_g)
  shift    = 0.

Field content:
  Phi   : SEPARATE MOND scalar, solves AQUAL   D.[mu(|DPhi|/a0) DPhi] = 4 pi G rho,
          mu(x)=x/sqrt(1+x^2),  g_MOND := |DPhi|.
  phi   : disformal scalar, "related to Phi", enters gtilde (matter coupling).

Sources (from the two elliptic equations of the reduced theory):
  LY (Hamiltonian constraint) linearised:
        8 Lap(psi1) = -16 pi G rho - 2 a0^2 U(ybar)
     => Lap(Psi_g)  = 4 pi G rho + (1/2) a0^2 U(ybar)         [SPACE]
  CMC lapse-fixing (time potential), source 4 pi G (E+S):
        Lap(Phi_g)  = 4 pi G (rho + 3p) + a0^2 (ybar U' - U)   [TIME]
     (dust: rho+3p = rho; the MOND (E+S) = a0^2(ybar U'-U)/4piG verified earlier.)
  ybar = |DPhi|^2/a0^2,  U'(y)=sqrt(y)/sqrt(1+y),  U=sqrt(y(1+y))-asinh(sqrt y).

We test, symbolically:
 (1) gamma_PPN of the METRIC sector = whether Psi_g = Phi_g, i.e. whether the two
     MOND stress sources coincide:  (1/2)U  vs  (yU'-U).  Mismatch M(y)=yU'-(3/2)U.
 (2) disformal weak field: gtilde_00 = e^{2phi} g_00,  gtilde_ij = e^{-2phi} g_ij,
     so phi enters TIME and SPACE potentials with the SAME sign & magnitude.
 (3) lensing (Phi_eff+Psi_eff) vs dynamics (Phi_eff): the ratio that decides
     lensing=dynamics, and WHERE that equality comes from.
 (4) Cassini: anomalous sunward acceleration for mu=x/sqrt(1+x^2).
"""
import sympy as sp

y = sp.symbols('y', positive=True)          # y = ybar = |DPhi|^2/a0^2
Uprime = sp.sqrt(y)/sp.sqrt(1+y)
U = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))

print("="*72)
print("(1) METRIC-SECTOR gamma_PPN: is Psi_g = Phi_g ?")
print("="*72)
print("  SPACE source (LY):    (1/2) a0^2 U(y)")
print("  TIME  source (lapse): a0^2 (y U' - U)")
print("  Equal  <=>  y U' - U = (1/2) U  <=>  M(y):= y U' - (3/2) U = 0")
M = sp.simplify(y*Uprime - sp.Rational(3,2)*U)
print("  M(y) =", M)
print("  deep-MOND  y->0 :", sp.simplify(sp.series(M, y, 0, 3).removeO()))
print("  Newtonian  y->oo:", sp.limit(M, y, sp.oo), " ; M/sqrt(y)->",
      sp.limit(M/sp.sqrt(y), y, sp.oo))
# The physically meaningful comparison is the FRACTIONAL mismatch of the two
# MOND stress sources relative to the SPACE source (1/2)U:
frac = sp.simplify(M/(sp.Rational(1,2)*U))       # = (Phi_g - Psi_g)_MOND / Psi_g,MOND
print("  fractional (Phi_g-Psi_g)/Psi_g from MOND stress = 2M/U =",
      sp.simplify(2*M/U))
print("    deep-MOND y->0 :", sp.limit(2*M/U, y, 0), " (EXACT gamma=1)")
print("    y=1 (transition):", sp.N(sp.simplify((2*M/U).subs(y,1))))
print("    Newtonian y->oo:", sp.limit(2*M/U, y, sp.oo))
print("  INTERPRETATION of 2M/U (fractional split WITHIN the MOND/phantom stress):")
print("   * deep-MOND (g<<a0): 2M/U -> 0 like y^{5/2}. This is the OPERATIVE regime")
print("     for galaxy/cluster lensing AND where the phantom energy is the")
print("     DOMINANT source. => metric gamma_PPN = 1 to high order EXACTLY where")
print("     the lensing=dynamics question actually lives.  <-- the load-bearing PASS")
print("   * Newtonian (g>>a0): 2M/U -> -1 (order 1), BUT the phantom stress a0^2 U")
print("     ~ |DPhi|^2 is then a NEGLIGIBLE fraction of 4piG rho_baryon, so the")
print("     physical gamma deviation = (2M/U) x (phantom/total) -> 0.")
print("   * transition (g~a0, y~1): 2M/U ~ -0.35 AND phantom ~ baryon => a genuine,")
print("     LOCAL, order ~10-30% source-level split. The PHYSICAL gamma(r) here is")
print("     set by nonlocal Poisson integration over a mass model -> NOT a single")
print("     number. Labelled INCOMPLETE: needs a concrete rho(r) solve, not asserted.")

print()
print("="*72)
print("(2) DISFORMAL weak field: how phi enters gtilde")
print("="*72)
phi, Phig, Psig = sp.symbols('phi Phi_g Psi_g')
# gtilde_00 = e^{-2phi} g_00 - 2 sinh(2phi) u_0 u_0, static u: u_0^2 = -g_00.
g00 = -(1 + 2*Phig)
u0sq = -g00
gt00 = sp.exp(-2*phi)*g00 - 2*sp.sinh(2*phi)*u0sq
gt00_lin = sp.series(gt00, phi, 0, 2).removeO()
gt00_lin = sp.expand(gt00_lin.subs(Phig, Phig))   # keep first order
print("  gtilde_00 =", sp.simplify(gt00), " = e^{2phi} g_00 ? ->",
      sp.simplify(gt00 - sp.exp(2*phi)*g00) == 0)
# first order: gtilde_00 = -(1 + 2(Phi_g + phi))
gt00_1 = sp.expand(sp.series(sp.exp(2*phi)*g00, phi, 0, 2).removeO())
print("  linearised gtilde_00 =", gt00_1, " => TIME potential Phi_eff = Phi_g + phi")
# spatial: gtilde_ij = e^{-2phi} g_ij (u has no spatial part)
gij = (1 - 2*Psig)
gtij = sp.exp(-2*phi)*gij
gtij_1 = sp.expand(sp.series(gtij, phi, 0, 2).removeO())
print("  linearised gtilde_ij =", gtij_1, "* delta_ij")
print("     write gtilde_ij=(1-2 Psi_eff): => Psi_eff = Psi_g + phi")
print("  KEY: the conformal factor e^{-2phi} multiplies g_ij ISOTROPICALLY and")
print("  e^{+2phi} multiplies g_00 => phi enters TIME and SPACE with EQUAL weight.")

print()
print("="*72)
print("(3) DYNAMICS vs LENSING")
print("="*72)
print("  Test-particle (slow) acceleration = grad(Phi_eff) = grad(Phi_g + phi).")
print("  Photon deflection ~ grad(Phi_eff + Psi_eff) = grad(Phi_g+Psi_g + 2 phi).")
print("  If metric gamma=1 (Phi_g=Psi_g), then")
print("     Phi_eff+Psi_eff = 2(Phi_g+phi) = 2 Phi_eff  => LENSING mass = DYN mass.")
print("  The phi-part contributes to lensing with weight 2 and to dynamics with")
print("  weight 1 AUTOMATICALLY, because e^{-2phi} is a metric CONFORMAL factor.")
print("  => lensing tracks the SAME potential as dynamics (= MOND, if phi carries")
print("     the MOND enhancement), NOT the bare Newtonian one.")
print("  ADVERSARIAL: the weight-2/weight-1 split is a PROPERTY OF THE DISFORMAL")
print("  ANSATZ (conformal coupling), NOT derived from the LY/momentum")
print("  constraints. The constraints only deliver metric gamma=1. See report.")

print()
print("="*72)
print("(4) CASSINI: anomalous sunward acceleration for mu=x/sqrt(1+x^2)")
print("="*72)
# Spherical AQUAL outside a point mass: mu(|Phi'|/a0) Phi' = g_N = GM/r^2.
# Newtonian deviation delta_a = Phi' - g_N = g_N (1/mu - 1).
# High-acc limit x=|Phi'|/a0 >>1: 1-mu ~ 1/(2x^2), so 1/mu-1 ~ 1/(2x^2)=a0^2/(2 g_N^2)
# (using Phi'~g_N). => delta_a ~ a0^2/(2 g_N).
x = sp.symbols('x', positive=True)
mu = x/sp.sqrt(1+x**2)
inv = sp.simplify(1/mu - 1)
print("  1/mu - 1 =", inv, " ; large-x ->",
      sp.simplify(sp.series(inv, x, sp.oo, 3).removeO()))
print("  => delta_a(r) ~ g_N * (a0^2/(2 g_N^2)) = a0^2/(2 g_N),  g_N=GM/r^2")
# numbers
G=6.674e-11; Msun=1.989e30; a0=1.2e-10; AU=1.496e11
for rAU in [1.0, 9.5, 10.0, 50.0]:
    r=rAU*AU; gN=G*Msun/r**2; da=a0**2/(2*gN)
    print(f"    r={rAU:5.1f} AU: g_N={gN:.3e} m/s^2, delta_a={da:.3e} m/s^2, "
          f"delta_a/g_N={da/gN:.3e}")
print("  Cassini range-rate bound on a constant anomalous accel at Saturn ~ 1e-14")
print("  m/s^2 (Hees+2014). delta_a(9.5 AU)~1e-16 SATISFIES that direct bound,")
print("  BUT the ephemeris/gamma_PPN test bounds 1-mu itself: the 'standard'")
print("  mu=x/sqrt(1+x^2) has 1-mu ~ 1/(2x^2), the SAME slow x^-2 approach that")
print("  Hees+2016 & Milgrom find in TENSION with planetary ranging. Report as")
print("  the inherited Cassini liability (memory: 3-15 sigma), NOT a clean pass.")
