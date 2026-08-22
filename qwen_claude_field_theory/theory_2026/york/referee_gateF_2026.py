"""
HOSTILE REFEREE -- GATE F (PPN / lensing / Cassini) of the CMC-elliptic-MOND theory.

Three attacks, each backed by sympy/numpy, no scaling-argument-as-result:

  (1) Is gamma_PPN = 1 DERIVED, or smuggled in via a disformal metric hand-tuned for it?
      -> Re-do the weak-field disformal shift ALGEBRA in sympy for the exact coupling the
         theory writes, gtilde = e^{-2phi} g - 2 sinh(2phi) n n (n = CMC unit normal, static).
         Show what shift each of Phi_phys, Psi_phys receives, and whether ANY choice of the
         free function phi(Phi) can set Phi_phys = Psi_phys (gamma=1) at fixed metric g.

  (2) Recompute the Cassini quadrupole INDEPENDENTLY for mu = x/sqrt(1+x^2) (the theory's
      OWN mu, i.e. the n=2 'standard' function) with the FROZEN convention
         |Q2| = (3/2) q(eta) a0^{3/2}/sqrt(GM_sun),   eta = g_ext/a0 (true field).
      q(eta) from Milgrom 2009 Eq.24-25 quadrature (validated vs Milgrom Table 1 mu_2).
      Compare to the Cassini bound Q2 = (3 +- 3)e-27 s^-2.  How many sigma REALLY?
      Also do the framework's phenomenological RAR/MS08 kernel for completeness.

  (3) Does the MOND anisotropic stress leak into any OTHER bound (binary pulsar,
      light-bending residual)?  Give the acceleration regime and the (a0/g) scaling.

The Task-F script claims Cassini is 'PASS, <<1 sigma'.  We test that head-on.
"""
import sympy as sp
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "gates_2026"))
from munu import nu_n_fn         # validated stable mu_n/nu_n family (callable in y)

def head(t): print("\n"+"="*80+"\n"+t+"\n"+"="*80)
def line(t): print("  "+t)

# =====================================================================================
head("(1)  Is gamma_PPN=1 DERIVED?  -- disformal-shift algebra, exact coupling, sympy")
# =====================================================================================
# Weak field, static, isotropic:  g_00 = -(1+2 Ph),  g_ij = (1-2 Ps) delta.
# CMC unit normal n_mu = (-N,0,0,0), N = sqrt(-g_00) = 1+Ph  => n_0 n_0 = N^2 = 1+2Ph.
# Physical (matter) metric the theory WRITES:
#      gtilde_mn = e^{-2 phi} g_mn - 2 sinh(2 phi) n_m n_n ,  phi = phi(Phi) free function.
eps = sp.symbols('epsilon', positive=True)     # linearization bookkeeper
Ph, Ps, phi = sp.symbols('Phi_g Psi_g phi', real=True)

g00 = -(1 + 2*eps*Ph)
gij =  (1 - 2*eps*Ps)
n0n0 = (1 + 2*eps*Ph)                            # = N^2 = -g_00
conf = sp.exp(-2*eps*phi)
disf = -2*sp.sinh(2*eps*phi)

gt00 = sp.series(conf*g00 + disf*n0n0, eps, 0, 2).removeO()
gt00_lin = sp.expand(gt00)
# read physical time potential:  gtilde_00 = -(1 + 2 Phi_phys)
Phi_phys = sp.simplify(-(gt00_lin + 1)/(2*eps))
line(f"gtilde_00 (linear) = {sp.simplify(gt00_lin)}")
line(f"  => Phi_phys = {Phi_phys}")

gtij = sp.series(conf*gij, eps, 0, 2).removeO()   # n_i = 0 spatial => no disformal piece in ij
gtij_lin = sp.expand(gtij)
Psi_phys = sp.simplify((1 - gtij_lin)/(2*eps))
line(f"gtilde_ij (linear) = {sp.simplify(gtij_lin)} * delta_ij")
line(f"  => Psi_phys = {Psi_phys}")

slip_phys = sp.simplify(Phi_phys - Psi_phys)
slip_geo  = Ph - Ps
line("")
line(f"PHYSICAL slip  Phi_phys - Psi_phys = {slip_phys}")
line(f"GEOMETRIC slip Phi_g   - Psi_g     = {slip_geo}")
line(f"  difference (phys - geo slip) = {sp.simplify(slip_phys - slip_geo)}")
verdict1_invariant = sp.simplify(slip_phys - slip_geo) == 0
line("")
line(f"RESULT: the disformal term as WRITTEN shifts BOTH potentials by +phi equally,")
line(f"        so the slip D = Phi-Psi is INVARIANT under phi(Phi):  invariant = {verdict1_invariant}")
line("        => NO choice of the free function phi(Phi) sets Phi_phys=Psi_phys at fixed g.")
line("        gamma_phys=1 is therefore NOT delivered by this coupling acting on the")
line("        Einstein-frame slip; it requires the fuller TeVeS/AeST construction in which")
line("        the scalar ALSO sources g's own potentials.  Either way phi(Phi) and the")
line("        n-n coefficient are CHOSEN to engineer lensing=dynamics -> it is an INPUT.")

# For contrast: a PURE conformal coupling (drop the n-n term) gives UNEQUAL shifts:
gt00_conf = sp.expand(sp.series(conf*g00, eps, 0, 2).removeO())
Phi_phys_conf = sp.simplify(-(gt00_conf + 1)/(2*eps))
line("")
line(f"CONTRAST (pure conformal, no n-n): Phi_phys={Phi_phys_conf}, Psi_phys={Psi_phys}")
line(f"   slip = {sp.simplify(Phi_phys_conf - Psi_phys)}  (phi-dependent) -- but null geodesics")
line("   are conformally invariant, so that 'fix' cannot change LENSING, only dynamics.")

# =====================================================================================
head("(2)  Cassini quadrupole for mu=x/sqrt(1+x^2), INDEPENDENT recompute, frozen convention")
# =====================================================================================
G_, MSUN = 6.6743e-11, 1.98892e30
GM = G_*MSUN

# ---- q(eta) via Milgrom 2009 Eq.24-25 quadrature (independent reimplementation) ----
def eta_N_of(nu, eta):
    f = lambda t: t*float(nu(np.array([t]))[0]) - eta
    hi = max(10.0*eta, 10.0)
    while f(hi) < 0: hi *= 2
    return brentq(f, 1e-8, hi, xtol=1e-14, rtol=1e-15)

def c2_raw(nu, etaN, nr=2600, nth=96, rmin=3e-4, rmax=400.0):
    mu_g, w_g = leggauss(nth)
    r = np.geomspace(rmin, rmax, nr)
    R, MUv = np.meshgrid(r, mu_g, indexing="ij")
    ST = np.sqrt(np.clip(1-MUv**2, 0, None))
    gs = 1.0/R**2
    gz, gp = etaN - gs*MUv, -gs*ST
    gN = np.sqrt(gz**2+gp**2)
    A = nu(gN)-1.0
    Ar = A*(gz*MUv+gp*ST); At = A*(-gz*ST+gp*MUv)
    dAr = np.gradient(R**2*Ar, r, axis=0)/R**2
    dAt = np.gradient(At*ST, np.arccos(mu_g), axis=1)/(R*np.maximum(ST,1e-12))
    S2 = 2.5*np.sum((dAr+dAt)*(0.5*(3*MUv**2-1))*w_g[None,:], axis=1)
    ok = np.isfinite(S2)
    return -0.2*np.trapz((S2/r)[ok], r[ok])

def q_of(nu, eta):  return 2.0*abs(c2_raw(nu, eta_N_of(nu, eta)))   # = q_zz = q_Milgrom

# nu for the theory's mu = x/sqrt(1+x^2) is the n=2 'standard' conjugate:
nu_standard = nu_n_fn(2.0)   # exact conjugate of mu_2 = x/sqrt(1+x^2)
# nu for the framework's phenomenological MS08/Route-A RAR kernel:
def nu_RAR(y):
    y = np.maximum(np.asarray(y,float), 1e-300)
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))

# ---- validation: Milgrom 2009 Table 1 gives -q~(eta=1.5) = 0.11 for mu_2 (standard) ----
q_std_15 = q_of(nu_standard, 1.5)
line(f"VALIDATION  standard mu_2:  q(1.5) computed = {q_std_15:.4f}  vs Milgrom Tab.1 = 0.11")
line(f"            frac diff {q_std_15/0.11-1:+.1%}   (machinery trusted if within a few %)")
# RAR anchors (DHF Fig.1): q(1)=0.094, q(1.5)=0.159, q(2)=0.221
for e in (1.0,1.5,2.0):
    line(f"VALIDATION  RAR kernel:     q({e}) computed = {q_of(nu_RAR,e):.4f}  vs DHF Fig.1 "
         f"{ {1.0:0.094,1.5:0.159,2.0:0.221}[e] }")

# ---- the actual Cassini number ----
Q2_bound_center, Q2_bound_sigma = 3.0e-27, 3.0e-27     # DHF Eq.2 / Hees+2014: (3 +- 3)e-27 s^-2
# external field at the Sun (DHF Gaia-EDR3): g_ext = 2.32e-10 (range 2.00-2.48); placeholder 2.146e-10
g_ext_cases = {"DHF Gaia-EDR3 2.32e-10": 2.32e-10,
               "DHF low-Q2 end 2.00e-10": 2.00e-10,
               "repo placeholder 2.146e-10": 2.1456e-10}
a0_cases = {"standard-MOND 1.20e-10": 1.20e-10,
            "framework canonical 9.3619e-11": 9.3619e-11,
            "framework alt 1.1279e-10": 1.1279e-10}

def Q2_and_sigma(nu, a0, g_ext):
    eta = g_ext/a0
    pref = np.sqrt(a0**3/GM)                 # = a0/R_M
    q = q_of(nu, eta)
    Q2 = 1.5*q*pref                           # |Q2| = (3/2) q a0^{3/2}/sqrt(GM)
    sig = (Q2 - Q2_bound_center)/Q2_bound_sigma
    return eta, q, pref, Q2, sig

print()
line("--- THEORY'S OWN mu = x/sqrt(1+x^2)  (n=2 standard) ---")
line(f"{'a0':<32}{'g_ext':<26}{'eta':>6}{'q(eta)':>9}{'|Q2|[s^-2]':>13}{'sigma':>9}")
worst_std = 0.0
for aname,a0 in a0_cases.items():
    for gname,ge in g_ext_cases.items():
        eta,q,pref,Q2,sig = Q2_and_sigma(nu_standard, a0, ge)
        worst_std = max(worst_std, sig)
        line(f"{aname:<32}{gname:<26}{eta:>6.3f}{q:>9.4f}{Q2:>13.3e}{sig:>9.2f}")
print()
line("--- framework's phenomenological RAR / MS08 kernel (DHF Table-1 headline object) ---")
line(f"{'a0':<32}{'g_ext':<26}{'eta':>6}{'q(eta)':>9}{'|Q2|[s^-2]':>13}{'sigma':>9}")
worst_rar = 0.0
for aname,a0 in a0_cases.items():
    for gname,ge in g_ext_cases.items():
        eta,q,pref,Q2,sig = Q2_and_sigma(nu_RAR, a0, ge)
        worst_rar = max(worst_rar, sig)
        line(f"{aname:<32}{gname:<26}{eta:>6.3f}{q:>9.4f}{Q2:>13.3e}{sig:>9.2f}")

print()
line(f"MIN across all cases (standard mu):  most FAVORABLE sigma still = "
     f"{min(Q2_and_sigma(nu_standard,a0,ge)[4] for a0 in a0_cases.values() for ge in g_ext_cases.values()):.2f}")
line(f"MIN across all cases (RAR kernel):    most FAVORABLE sigma still = "
     f"{min(Q2_and_sigma(nu_RAR,a0,ge)[4] for a0 in a0_cases.values() for ge in g_ext_cases.values()):.2f}")
line("")
line("REFUTATION: the Task-F script's Cassini claim ('Q2 ~ 1e-25 m/s^2, ~11 orders below,")
line("PASS, <<1 sigma') used a wrong (a0/g)^3-scaling ESTIMATE, not the EFE quadrupole.")
line("The proper DHF-convention quadrupole is Q2 ~ (20-26)e-27 s^-2 vs bound (3+-3)e-27,")
line("i.e. ~6-8 sigma tension -- for BOTH the theory's own mu AND the RAR kernel.")

# Cross-check: what anomalous tidal acceleration does that Q2 give at Saturn?
AU = 1.495978707e11
r_sat = 9.58*AU
eta,q,pref,Q2,sig = Q2_and_sigma(nu_standard, 1.20e-10, 2.32e-10)
a_anom = Q2*r_sat
line("")
line(f"Cross-check (standard mu, a0=1.2e-10, g_ext=2.32e-10):  Q2={Q2:.3e} s^-2")
line(f"   anomalous quadrupole tidal accel at Saturn ~ Q2*r = {a_anom:.3e} m/s^2")
line(f"   vs Cassini range-rate sensitivity ~1e-14 m/s^2  =>  ABOVE it, not 11 orders below.")

# =====================================================================================
head("(3)  Does the MOND anisotropic stress leak into OTHER bounds?")
# =====================================================================================
# The anisotropic stress amplitude (from Task F): 8piG(p_r-p_t) = 2 U'(Y) P^2, U'=mu(sqrt Y).
# Its RELATIVE size vs the isotropic Newtonian source scales with mu-deviation & (a0/g).
Y = sp.symbols('Y', positive=True)
Up = sp.sqrt(Y)/sp.sqrt(1+Y)
x = sp.symbols('x', positive=True)           # x = g/a0 = sqrt(Y) in the single-field radial map
# High-acceleration (x>>1) expansion of the pieces that carry the slip:
one_minus_mu = sp.series(1 - x/sp.sqrt(1+x**2), x, sp.oo, 4).removeO()
line(f"1 - mu(x)  (x=g/a0 >> 1) = {one_minus_mu}   -> falls as 1/(2x^2)")
mu_prime = sp.simplify(sp.diff(x/sp.sqrt(1+x**2), x))
line(f"mu'(x) = {mu_prime}  ~ 1/x^3 at large x  (governs EFE quadrupole amplitude)")
line("")
line("BINARY PULSARS: internal accelerations g ~ 1e2-1e5 m/s^2 => x=g/a0 ~ 1e12-1e15.")
line("  anisotropic-stress / slip terms ~ (a0/g)^2 ~ 1e-24 .. 1e-30  => utterly negligible.")
line("  MOND (and this theory) reduce to GR there; no binary-pulsar leak. SAFE.")
line("")
line("LIGHT-BENDING RESIDUAL: the slip D = Phi_g - Psi_g IS the light-bending anomaly.")
line("  In the Einstein frame gamma_PPN = log(r)/(log(r)-2) != 1 -> AQUAL under-lenses by O(1).")
line("  The disformal coupling is invoked precisely to hide this in lensing = the SAME")
line("  engineered input as attack (1).  So the anisotropic stress does NOT leak into an")
line("  independent NEW bound -- it is the ONE object behind BOTH the lensing slip AND the")
line("  Cassini quadrupole.  The solar-system quadrupole is where it is NOT (a0/g)-suppressed,")
line("  because the Galactic external field g_ext ~ 2 a0 keeps eta = O(1) at the Sun.")

# =====================================================================================
head("VERDICT ON GATE F")
# =====================================================================================
line("(1) gamma_PPN = 1 is NOT derived. It is engineered by adopting the disformal matter")
line("    coupling; moreover the exact form written (e^{-2phi}g - 2 sinh(2phi) nn) leaves the")
line("    Einstein-frame slip D INVARIANT (sympy), so gamma=1 needs the fuller TeVeS/AeST")
line("    construction, not this coupling alone. Lensing=dynamics is an INPUT, not a prediction.")
line("(2) Cassini FAILS, not passes. Independent frozen-convention recompute gives")
line(f"    Q2 ~ 20-26e-27 s^-2 vs bound (3+-3)e-27 => ~6-8 sigma for BOTH the theory's own")
line("    mu=x/sqrt(1+x^2) AND the RAR kernel. The Task-F 'PASS <<1 sigma' is WRONG (it")
line("    priced the isotropic radial 1-mu term, not the EFE quadrupole Cassini actually bounds).")
line("(3) No NEW independent leak: binary pulsars are (a0/g)^2-safe; the light-bending slip")
line("    and the Cassini quadrupole are the SAME anisotropic-stress object, hidden in lensing")
line("    only by the same engineered disformal input.")
line("")
line("OVERALL: Gate F should be graded FAIL on the Cassini leg (the standard/RAR mu is in")
line("~6-8 sigma tension with Cassini's Q2 under the theory's own frozen convention), and")
line("CONDITIONAL/ENGINEERED on the gamma_PPN=1 leg. The previous 'CONDITIONAL/PASS' overstated it.")
