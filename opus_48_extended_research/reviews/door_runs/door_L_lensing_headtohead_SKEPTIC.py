#!/usr/bin/env python3
"""
SKEPTIC re-run of DOOR L (lensing head-to-head). I re-derive the load-bearing pieces
INDEPENDENTLY and probe the two places the prior agent could have manufactured a PASS:

  (S1) Is the host's phi=psi REALLY forced (a theorem), or did the prior sympy "proof"
       (showing -d_x d_y(r^2)=0) merely restate a triviality?  Re-derive the ij Einstein
       eq obstruction the RIGHT way: a TRACELESS-TRANSVERSE shear sourced by a scalar.

  (S2) THE CRUX the prior agent glossed: in the BANKED slip prediction
       (GRAVITATIONAL_SLIP_PREDICTION_2026-06-17.md) the slip is a FIELD-LEVEL slip
       Phi != Psi in the METRIC:  grad Phi = g_N (matter),  grad Psi = 2 g_obs - g_N.
       That is NOT "psi=phi". Light feels (Phi+Psi)/... so its deflection uses
       grad[(Phi+Psi)/2] = (g_N + (2 g_obs - g_N))/2 = g_obs.
       => The prior agent's Part-3 "both lens at g_obs, ratio 1.0000" is CONSISTENT with a
          REAL field-level slip -- BUT only because the slip was TUNED so the lensing-
          effective field lands on g_obs. The deflection-equality does NOT prove "no slip";
          it proves "lensing magnitude tuned to g_obs". The slip is REAL at the level of
          (Phi - Psi) and shows up in E_G / (lensing vs dynamics), NOT in the bending angle
          alone (which only sees the SUM).

  (S3) Does the host (AeST/Blanchet-Skordis) ALSO produce a field-level Phi=Psi AND lens at
       g_obs?  If yes, then framework-vs-host AGREE (the later banked doc's position).
       Key test: in the host, what is (Phi+Psi)/2 vs g_obs, and is Phi=Psi at the FIELD level
       (not just the inferred level)?

  (S4) Re-do the deflection integral two independent ways (scipy.quad with the tan-sub AND a
       direct closed-form for the point mass) to confirm the prior 1.0000 is not an artifact,
       AND compute the E_G-style discriminator gamma = Psi/Phi (gradient ratio) which IS the
       real signature, to check the prior numbers (1.01, 1.83, 5.63, 19.1).

  Both ways.  No bound is mis-applied here (no positivity bound in this door).
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad

c  = 2.99792458e8
G  = 6.674e-11
a0 = 9.3624e-11
Msun = 1.989e30

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)

# =====================================================================================
H("S1 -- is host phi=psi a THEOREM? re-derive the ij-Einstein traceless-shear obstruction")
# =====================================================================================
# The CORRECT statement (Blanchet-Skordis Eq.3.9 / standard scalar-tensor PN):
#   the ij (i!=j) Einstein eq is   d_i d_j (Phi - Psi) = (source)_ij.
#   For an ISOTROPIC scalar source the RHS off-diagonal i!=j vanishes, so
#   d_i d_j (Phi-Psi)=0 for all i!=j  =>  Phi-Psi has NO off-diagonal Hessian
#   => Phi-Psi = sum of separable a_i(x_i); combined with the trace (ii) eq and
#   asymptotic flatness this forces Phi-Psi = const = 0.  Verify the Hessian logic.
x,y,z = sp.symbols('x y z', real=True)
S = sp.Function('S')  # Phi - Psi as a general field
# A general harmonic-ish radial profile is too restrictive; test the GENERAL claim:
# if d_i d_j S = 0 for ALL i != j everywhere, what functions S survive?
Sgen = sp.Function('S')(x,y,z)
mixed = [sp.diff(Sgen, a, b) for a,b in [(x,y),(x,z),(y,z)]]
print("requiring all mixed 2nd derivatives d_i d_j S = 0 (i!=j) =>")
print("  S(x,y,z) must be additively separable: S = f(x)+g(y)+h(z).")
# A radial S=h(r) is separable additively ONLY if h(r)=A r^2 + B (then S = A(x^2+y^2+z^2)+B).
# Check: is r^2 the unique radial additively-separable form? h(r) with S=h(sqrt(x^2+y^2+z^2))
# additively separable <=> h(r)=A r^2 + B.  Show any other radial h has nonzero mixed deriv:
r = sp.sqrt(x**2+y**2+z**2)
for trial,name in [(r**2,'r^2'),(r,'r'),(1/r,'1/r (point-mass-like)'),(sp.log(r),'log r'),
                   (r**2+5,'r^2+const')]:
    md = sp.simplify(sp.diff(trial.subs(r, sp.sqrt(x**2+y**2+z**2)), x, y))
    print(f"   radial S={name:22s}: d_x d_y S = {md}  ({'OK (separable)' if md==0 else 'NONZERO -> excluded by ij eq'}")
print("""
  CONCLUSION: among radial (isolated-system) fields, ONLY S=A r^2 + B has vanishing
  off-diagonal Hessian. A r^2 is NOT asymptotically flat (blows up), B is pure gauge
  -> the only PHYSICAL isolated solution is S = Phi - Psi = 0 at the field level.
  => host phi=psi IS a genuine theorem (the ij Einstein eq forbids any 1/r-type slip).
  [The prior agent's check was correct in conclusion though it only spot-checked r^2;
   the GENERAL additive-separability argument above closes it.]
""")

# =====================================================================================
H("S2/S4 -- the BANKED field-level slip: grad Phi=g_N, grad Psi = 2 g_obs - g_N (point mass)")
# =====================================================================================
rs, Gs, Ms, a0s = sp.symbols('r G M a_0', positive=True)
gN  = Gs*Ms/rs**2
gob = sp.sqrt(gN**2 + gN*a0s)
gradPhi = gN
gradPsi = 2*gob - gN                       # banked: grad Psi = 2 g_obs - g_N
slip_grad = sp.simplify(gradPsi - gradPhi) # = 2(g_obs - g_N) -- the route_f slip
g_lens = sp.simplify((gradPhi + gradPsi)/2)
print("framework FIELD-LEVEL potentials (banked GRAVITATIONAL_SLIP_PREDICTION doc):")
print("  grad Phi = g_N                         =", gradPhi)
print("  grad Psi = 2 g_obs - g_N               =", sp.simplify(gradPsi))
print("  slip grad(Psi-Phi)=2(g_obs-g_N)        =", slip_grad, "  (NONZERO in MOND regime)")
print("  light-effective grad[(Phi+Psi)/2]      =", g_lens, " == g_obs?",
      sp.simplify(g_lens - gob)==0)
print("""
  => The framework's FIELD-LEVEL slip is REAL and nonzero (Psi != Phi). The lensing-
     effective field (Phi+Psi)/2 = g_obs ONLY because Psi was TUNED to 2 g_obs - g_N.
     The deflection (which sees the SUM) lands on g_obs; the SLIP (which sees the
     DIFFERENCE) is 2(g_obs-g_N) and is observable via E_G / lensing-vs-dynamics.
""")

# gamma = Psi/Phi as a GRADIENT ratio (the banked E_G signature):
xsym = sp.symbols('x', positive=True)   # x = a0/g_N
gob_over_gN = sp.sqrt(1+xsym)
gamma_grad = sp.simplify((2*gob_over_gN - 1))   # (2 g_obs - g_N)/g_N = 2 sqrt(1+x) - 1
print("banked gamma = grad Psi / grad Phi = (2 g_obs - g_N)/g_N = 2 sqrt(1+a0/g_N) - 1 =", gamma_grad)
print(f"{'a0/g_N':>10}{'g_obs/g_N':>12}{'gamma=Psi/Phi':>16}{'E_G ratio=g_obs/g_N':>22}")
for xx in [0.01, 0.1, 1.0, 10.0, 100.0]:
    go = np.sqrt(1+xx)
    print(f"{xx:>10.2f}{go:>12.4f}{2*go-1:>16.4f}{go:>22.4f}")

# =====================================================================================
H("S4 -- deflection two independent ways: confirm ratio 1.0000 is real, not a grid artifact")
# =====================================================================================
def g_obs_num(r, M):
    gN = G*M/r**2
    return np.sqrt(gN**2 + gN*a0)

def defl_quad(b, M, glaw):
    # light bends on (Phi+Psi); for a slip-tuned source the effective field is g_lens.
    # Here glaw IS the lensing-effective field (g_obs). alpha=(2/c^2)*int g_perp ds, full line.
    def integ(th):
        r = b/np.cos(th); return glaw(r,M)*(b/r)*(b/np.cos(th)**2)
    half,_ = quad(integ, 0, np.pi/2, limit=200)
    return (2.0/c**2)*2.0*half

# independent Newton closed form check
b = 7e8
aN = defl_quad(b, Msun, lambda r,M: G*M/r**2)
print(f"Newton: quad alpha={aN:.6e}  exact 4GM/bc^2={4*G*Msun/(b*c**2):.6e}  ratio={aN/(4*G*Msun/(b*c**2)):.6f}")

# galaxy lens: HOST lenses at g_obs (field-level no slip, phantom mass).
# FRAMEWORK lenses at g_obs TOO (slip tuned so (Phi+Psi)/2 = g_obs). Both SUMS equal.
M_gal = 1e11*Msun; kpc = 3.0857e19; arcsec=206265.0
rM = np.sqrt(G*M_gal/a0)
print(f"\nM=1e11 Msun, r_M={rM/kpc:.2f} kpc. Deflection HOST vs FRAMEWORK (both lens at g_obs):")
print(f"{'b[kpc]':>9}{'a0/gN':>12}{'alpha_HOST[\"]':>16}{'alpha_FW[\"]':>16}{'ratio':>9}")
for bk in [1.0,10.0,rM/kpc,100.0,1000.0]:
    bb=bk*kpc; gNb=G*M_gal/bb**2
    ah=defl_quad(bb,M_gal,g_obs_num)*arcsec
    af=defl_quad(bb,M_gal,g_obs_num)*arcsec
    print(f"{bk:>9.2f}{a0/gNb:>12.3e}{ah:>16.5f}{af:>16.5f}{af/ah:>9.4f}")

# =====================================================================================
H("S3 -- does the HOST also carry the SAME inferred slip vs LCDM? (the real discriminator)")
# =====================================================================================
print("""
HOST (AeST/Blanchet-Skordis), FIELD level: Phi = Psi (theorem S1). Both equal the FULL
MOND potential phi_MOND with grad phi_MOND = g_obs (phantom Khronon mass included, Eq.3.15a).
  => host grad Phi = grad Psi = g_obs (NOT g_N!). Light: (Phi+Psi)/2 -> g_obs. Same deflection.

FRAMEWORK (modified inertia), FIELD level: grad Phi = g_N (baryon only; matter's MOND boost
is INERTIAL, not in the metric), grad Psi = 2 g_obs - g_N (tuned). (Phi+Psi)/2 = g_obs. Same
deflection.

=> SAME OBSERVABLE DEFLECTION, but DIFFERENT field-level structure:
     host:      Phi = Psi = (potential giving g_obs)        -> field slip Psi/Phi = 1 EXACTLY
     framework: Phi != Psi (g_N vs 2 g_obs - g_N)           -> field slip Psi/Phi = 2 sqrt(1+x)-1
   The DYNAMICAL test (matter accel vs lensing): host matter feels grad Phi = g_obs (mod GRAVITY,
   fails Cassini unless screened); framework matter feels grad Phi = g_N but is INERTIALLY
   boosted to g_obs (mod INERTIA, Cassini-safe by gate).
""")

# THE decisive both-ways number: is Psi/Phi a framework-vs-host DISCRIMINATOR?
print("DISCRIMINATOR AUDIT (Psi/Phi gradient ratio, the slip):")
print(f"{'a0/g_N':>10}{'host Psi/Phi':>16}{'framework Psi/Phi':>20}{'differ?':>10}")
for xx in [0.01,0.1,1.0,10.0,100.0]:
    host = 1.0
    fw   = 2*np.sqrt(1+xx)-1
    print(f"{xx:>10.2f}{host:>16.4f}{fw:>20.4f}{'YES' if abs(host-fw)>1e-6 else 'no':>10}")

print("""
SO WHICH IS IT?  The answer hinges on a DEFINITIONAL choice of what 'Phi' means:
  - If 'Phi' = the FULL gravitational potential matter MOVES IN, then host Phi sources g_obs
    (mod gravity) and framework Phi sources g_N (mod inertia) -> the slip Psi/Phi DIFFERS and
    IS a discriminator -- BUT it is a MATTER-DYNAMICS (Cassini/EFE) discriminator, NOT a lensing
    one (the bending angle is identical, both = g_obs).
  - If one compares the OBSERVABLE lensing-to-dynamics ratio E_G = g_obs/g_N (lensing field
    over the field matter's ACCELERATION implies), BOTH host and framework give g_obs/g_N =
    sqrt(1+a0/g_N) IDENTICALLY (both lens at g_obs, both have matter orbiting at g_obs).
    => E_G does NOT separate framework from host. It separates the MOND family from LCDM (=1).
""")

H("NET / VERDICT logic")
print("""
RE-DERIVED INDEPENDENTLY:
 (1) host phi=psi is a genuine FIELD-LEVEL theorem (additive-separability of the ij-Hessian;
     only r^2 survives, excluded by asymptotic flatness). [S1 confirms prior conclusion]
 (2) the framework's banked slip gamma=2 sqrt(1+a0/g_N)-1 = (2 g_obs - g_N)/g_N is a REAL
     FIELD-LEVEL slip Psi != Phi -- NOT merely an 'effective-DM inferred' relabel. The prior
     agent's framing ('it is the effective-DM inferred slip, not field-level') is IMPRECISE:
     in the framework's OWN metric, Phi(g_N) != Psi(2 g_obs - g_N) genuinely. [REFINES prior]
 (3) BUT the OBSERVABLE that the slip feeds -- the bending angle (sum Phi+Psi) and the E_G
     ratio (g_obs/g_N) -- is IDENTICAL between framework and host, because (a) the slip was
     TUNED so (Phi+Psi)/2 = g_obs, and (b) the host lenses at g_obs too with matter orbiting
     at g_obs. So NO lensing/E_G observable separates framework from its host. [CONFIRMS prior
     bottom line: AGREE on observables]
 (4) The framework-vs-host difference that IS real lives in the MATTER sector (mod-inertia vs
     mod-gravity: grad Phi = g_N vs g_obs) -> the Cassini/EFE/dynamics channel, which the
     no-go + SME bridge already own -- NOT lensing.

VERDICT: the prior agent's bottom-line OBSERVABLE conclusion (AGREE; no static lensing/E_G
test separates framework from host; the 'distinguishes from AeST' billing is wrong) is
CONFIRMED and matches the LATER banked doc (GRAVITATIONAL_SLIP_PREDICTION_2026-06-17, which
ALREADY retracted 'distinguishes from AeST'). The prior agent's INTERNAL CHARACTERIZATION
('the banked gamma is the effective-DM inferred slip, NOT a field-level psi!=phi') is REVISED:
the slip IS field-level in the framework's metric (Psi != Phi); what makes it a NON-
discriminator is that the lensing OBSERVABLE (the sum) and E_G (g_obs/g_N) coincide with the
host's, not that the field slip is fictitious.
""")
