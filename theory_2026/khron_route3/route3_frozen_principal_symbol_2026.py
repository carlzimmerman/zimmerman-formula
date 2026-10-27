#!/usr/bin/env python3
"""
ROUTE 3: LOCAL FROZEN FLAT-BACKGROUND principal symbol of FC-KH khronometric-MOND.

Full generalized khronometric class (beta,lambda != 0), ADM/unitary gauge:
  S = (1/16 pi G) INT N sqrt(gamma) [ (1-beta) K_ij K^ij - (1+lambda) K^2 + R3 + f_FC(a) ]

Background (frozen at r*): Minkowski, N_bar=1 at r*, uniform accel a_i = abar xhat const,
K_bar_ij = 0, gamma_bar = delta.  Scalar perturbations, unitary gauge (khronon eaten):
  N = 1 + phi        (lapse, non-dynamical -> Hamiltonian constraint)
  N_i = d_i B        (scalar shift, non-dynamical -> momentum constraint)
  gamma_ij = (1+2psi) delta_ij   (gauge E=0; psi is the single propagating scalar)

Principal symbol = two-derivative quadratic terms only (drop mass-like background*field^2 and
single-derivative terms -> they are lower order in the WKB/high-k symbol).

Two-derivative quadratic Lagrangian (real space, 1/16piG factored out):
  L = (1-beta)[3 psidot^2 - 2 psidot lap B + (d_i d_j B)^2]
    - (1+lambda)[9 psidot^2 - 6 psidot lap B + (lap B)^2]
    + 2 (grad psi)^2                                   # from INT sqrt(g) R3
    - 4 phi lap psi                                    # lapse-psi coupling (measure x linear R3)
    + (1/2) fpp (d_x phi)^2 + chi (grad_perp phi)^2    # accel-Hessian: radial f'', transverse f'/a=2chi

Fourier: build 3x3 Hermitian symbol M(omega,kpar,kperp) in X=(psi,B,phi), integrate out
the non-dynamical phi and B (Schur complement), read off dispersion A omega^2 + G(k)=0.
"""
import sympy as sp

omega, kpar, kperp = sp.symbols('omega kpar kperp', real=True)
beta, lam, alpha = sp.symbols('beta lambda alpha', real=True)
fpp, chi = sp.symbols('fpp chi', real=True)      # f''(y) and chi(y)=f'/2a
k2 = kpar**2 + kperp**2
I = sp.I

# --- Build the Hermitian symbol matrix. Convention: L = sum_ab Mstar_ab Xa* Xb. ---
# Diagonal real terms c|X|^2 -> add c. Cross c*(D1 f)(D2 g) real-space -> Hermitian off-diag.
# psidot^2 -> omega^2 |psi|^2 ; (grad psi)^2 -> k2 |psi|^2 ; (d_id_j B)^2 -> k2^2|B|^2 ;
# (lap B)^2 -> k2^2 |B|^2 ; (d_x phi)^2 -> kpar^2|phi|^2 ; (grad_perp phi)^2 -> kperp^2|phi|^2.
# cross c*psidot*lap B : term c INT psidot lapB -> Hermitian, |M_psiB|^2 = (1/4)c^2 omega^2 k2^2
#   M_Bpsi = (I/2) c omega k2 ,  M_psiB = -(I/2) c omega k2
# cross c*phi*lap psi : M_phipsi = M_psiphi = (1/2)c*(k2) with sign; here c=-4, lap psi->-k2 psi
#   -4 INT phi lap psi -> +4 k2 phi psi -> Hermitian (1/2)*4k2*(...*) => M_phipsi = 2 k2

# psi-psi
Mpp = (1-beta)*3*omega**2 - (1+lam)*9*omega**2 + 2*k2
# B-B
MBB = (1-beta)*k2**2 - (1+lam)*k2**2
# phi-phi
Mff = sp.Rational(1,2)*fpp*kpar**2 + chi*kperp**2
# psi-B cross:  coeff of (psidot lap B) is cx
cx = (1-beta)*(-2) - (1+lam)*(-6)     # = 4 + 2beta + 6 lambda
MpB = -(I/2)*cx*omega*k2
MBp =  (I/2)*cx*omega*k2
# psi-phi cross:
Mpf = 2*k2
Mfp = 2*k2
# B-phi cross: none
MBf = 0
MfB = 0

M = sp.Matrix([
    [Mpp, MpB, Mpf],
    [MBp, MBB, MfB],
    [Mfp, MBf, Mff],
])

# --- Integrate out phi and B (Schur complement onto psi) ---
# Effective psi symbol = Mpp - [MpB MpB' etc] * inv(2x2 of {B,phi}) * [...]
sub = M[1:,1:]            # {B,phi} block
vecR = M[0,1:].T         # column (MpB, Mpf)
vecL = M[1:,0]           # column (MBp, Mfp)
Meff = sp.simplify(Mpp - (M[0,1:]*sub.inv()*M[1:,0])[0])
Meff = sp.simplify(Meff)
print("Meff (psi effective symbol) =")
sp.pprint(Meff)

# Dispersion: Meff = 0 -> A*omega^2 + G(kpar,kperp) = 0
Meff_poly = sp.expand(Meff)
A = sp.simplify(Meff_poly.coeff(omega,2))
G = sp.simplify(Meff_poly - A*omega**2)     # gradient (omega-independent) part
print("\nA (coeff of omega^2) =", sp.simplify(A))
print("G (gradient part)     =", sp.simplify(G))

# Factor A
print("\nA factored =", sp.factor(A))

# Radial (kperp=0) and transverse (kpar=0) gradient coefficients.
G_rad = sp.simplify(G.subs(kperp,0))
G_tra = sp.simplify(G.subs(kpar,0))
Bpar_grad = sp.simplify(G_rad/kpar**2)    # G_radial = Bpar_grad * kpar^2
Bperp_grad = sp.simplify(G_tra/kperp**2)
print("\nG_radial/kpar^2  =", Bpar_grad)
print("G_transv/kperp^2 =", Bperp_grad)

# Prompt convention: c_s^2 = B/A  with B>0 = stable.  So B_par = -G_radial/kpar^2.
Bpar = sp.simplify(-Bpar_grad)
Bperp = sp.simplify(-Bperp_grad)
print("\n=== PROMPT CONVENTION (c_s^2 = B/A) ===")
print("A     =", sp.factor(A))
print("B_par =", sp.simplify(Bpar), " = 8/fpp - 2 ?", sp.simplify(Bpar - (8/fpp - 2))==0)
print("B_perp=", sp.simplify(Bperp), " = 4/chi - 2 ?", sp.simplify(Bperp - (4/chi - 2))==0)

# ============ HIGH-a SELF-CHECK ============
# high-a: screening off, f->alpha a^2 => fpp->2 alpha, chi->alpha.
print("\n" + "="*60)
print("HIGH-a SELF-CHECK (fpp->2alpha, chi->alpha)")
cs2_target = (2-alpha)*(beta+lam)/(alpha*(1-beta)*(2+beta+3*lam))
# c_s^2 = B/A (isotropic in high-a). Use radial (or transverse -> must agree).
cs2_par_high  = sp.simplify((Bpar /A).subs({fpp:2*alpha, chi:alpha}))
cs2_perp_high = sp.simplify((Bperp/A).subs({fpp:2*alpha, chi:alpha}))
print("c_s,par^2  (high-a) =", cs2_par_high)
print("c_s,perp^2 (high-a) =", cs2_perp_high)
print("target c_s^2        =", sp.simplify(cs2_target))
print("PAR  matches target :", sp.simplify(cs2_par_high - cs2_target)==0)
print("PERP matches target :", sp.simplify(cs2_perp_high - cs2_target)==0)
print("PAR == PERP (isotropic):", sp.simplify(cs2_par_high - cs2_perp_high)==0)

# ============ TENSOR c_T^2 (independent) ============
# TT: (1-beta)(1/4)hdot^2 - (1/4)(grad h)^2 -> (1-beta)omega^2 = k^2 -> c_T^2 = 1/(1-beta)
print("\nc_T^2 = 1/(1-beta)  [tensor sector, (1-beta)K_ijK^ij vs R3]")

# ============ TRACK B_par(y) OVER 0.5<y<2 AT BENCHMARK ============
print("\n" + "="*60)
print("B_par(y) SIGN OVER 0.5<y<2  (benchmark alpha=2e-15,beta=1e-15,lambda=1e-3)")
import math
al = 2e-15
def fpp_y(y):   return 2*al + 2*(2-al)*(1-y)*math.exp(-y)
def chi_y(y):   return al + (2-al)*math.exp(-y)
def Bpar_y(y):  return 8.0/fpp_y(y) - 2.0
def Bperp_y(y): return 4.0/chi_y(y) - 2.0
Aval = float((2*(1-beta)*(2+beta+3*lam)/(beta+lam)).subs({beta:1e-15, lam:1e-3}))
print("A (benchmark) = %.4f  (sign %s)" % (Aval, "positive" if Aval>0 else "negative"))
for y in [0.5,0.7,0.9,0.99,1.0,1.01,1.1,1.3,1.5,2.0]:
    bp = Bpar_y(y); bpe = Bperp_y(y)
    cs2p = bp/Aval; cs2pe = bpe/Aval
    print("y=%.2f  fpp=%+.4e  B_par=%+.4e (cs2par=%+.3e)  B_perp=%+.4e (cs2perp=%+.3e)"
          % (y, fpp_y(y), bp, cs2p, bpe, cs2pe))
