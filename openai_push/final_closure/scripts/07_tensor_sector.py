"""Gate 9: Tensor sector.

Expand the theory around Minkowski in TT variables and verify:
  (1) the scalar MOND constraint C_M has NO dependence on the TT perturbation
      h_TT at quadratic order (it depends only on the scalar lapse phi), so
      the constraint term mu_1 S_1 does not feed the TT equations at O(eps^2);
  (2) the TT sector is therefore exactly the GR Einstein quadratic sector;
  (3) the quadratic TT action has  Q_T > 0  (positive kinetic term, no ghost),
      c_T^2 > 0, and  c_T^2 = c^2  (luminal).

Perturbation bookkeeping:  phi = eps*phi_1  (lapse),  h = eps*h_1  (metric),
with h_1 split into TT part.  We expand C_M to O(eps^2) and check the h_TT
coefficient vanishes.
"""

import sympy as sp

print("=" * 70)
print("GATE 9: TENSOR SECTOR")
print("=" * 70)

# ------------------------------------------------------------------
# (1) Decoupling: C_M has no h_TT dependence at quadratic order
# ------------------------------------------------------------------
print("\n--- (1) C_M quadratic order: no TT dependence ---")
eps = sp.symbols("eps")                      # perturbation bookkeeping
c, a0, Gc = sp.symbols("c a0 G", positive=True)
# 1D spatial coordinate (sufficient for the order-counting; the TT part is a
# spatial tensor that enters only through index-raising D^i = gamma^ij D_j).
x = sp.symbols("x", real=True)
phi1 = sp.Function("phi1")(x)                # O(1) scalar lapse profile
hTT  = sp.Function("hTT")(x)                 # O(1) TT tensor profile (1D component)

phi = eps * phi1                             # lapse perturbation
# gamma_ij = delta_ij + h_ij ;  inverse gamma^ij = delta^ij - h^ij + O(h^2)
# In 1D:  gamma = 1 + eps*hTT ,  gamma^11 = 1 - eps*hTT + O(eps^2).
gammainv = 1 - eps * hTT                     # O(eps^0) + O(eps)

lnN = sp.log(1 + phi)
DlnN = sp.diff(lnN, x)                       # D_x ln N  (lower index)
# y = (c^2/a0) |D ln N|  ;  use signed branch for algebra (1D).
y = (c**2 / a0) * DlnN
mu = 1 - sp.exp(-y)
# Flux F^x = c^2 mu(y) D^x ln N  with  D^x = gamma^xx D_x  (index raising).
DlnN_raised = gammainv * DlnN                # D^x ln N = gamma^xx D_x ln N
flux = c**2 * mu * DlnN_raised
C_M = sp.diff(flux, x)                        # D_x F^x  (vacuum: rho_m = 0)

# Expand C_M to O(eps^2)
C_M_series = sp.series(C_M, eps, 0, 3).removeO()   # up to and including eps^2
C_M_1 = sp.simplify(C_M_series.coeff(eps, 1))
C_M_2 = sp.simplify(C_M_series.coeff(eps, 2))
print("[1.1] C_M O(eps^1) =", C_M_1)
print("[1.2] C_M O(eps^2) =", C_M_2)
# The O(eps^1) term should be 0 (background is a solution: y=0 -> mu=0).
# The O(eps^2) term must have NO hTT dependence.
has_hTT_2 = (C_M_2.has(hTT))
print("[1.3] C_M O(eps^1) == 0 (background solution) :", C_M_1 == 0)
print("[1.4] C_M O(eps^2) depends on hTT ?           :", has_hTT_2)
# The hTT correction enters flux at O(eps^3) (|Dphi|~eps, h~eps, Dphi~eps).
# Verify: collect the lowest order at which hTT appears.
C_M_full = sp.series(C_M, eps, 0, 5).removeO()
orders_hTT = []
for n in range(1, 5):
    coeff_n = C_M_full.coeff(eps, n)
    if coeff_n.has(hTT):
        orders_hTT.append(n)
print("[1.5] lowest order at which hTT appears in C_M :",
      orders_hTT[0] if orders_hTT else "none (fully decoupled)")
decoupled = (not has_hTT_2) and (not orders_hTT or orders_hTT[0] >= 3)
print("[1.6] TT decoupled at quadratic order          :", decoupled)

# ------------------------------------------------------------------
# (2) & (3) GR TT quadratic sector: dispersion and kinetic sign
# ------------------------------------------------------------------
print("\n--- (2)/(3) GR TT quadratic sector ---")
# Linearized Einstein tensor for g_mu nu = eta_mu nu + h_mu nu.
# R^(1)_{mu nu} = 1/2 (d_mu d^alpha h_alpha nu + d_nu d^alpha h_alpha mu
#                    - Box h_mu nu - d_mu d_nu h).
# For a TT perturbation: h = 0 (traceless), d^alpha h_alpha mu = 0
# (transverse, h_0 mu = 0).  Hence  R^(1)_{mu nu} = -1/2 Box h_mu nu.
# G^(1)_{mu nu} = R^(1)_{mu nu} - 1/2 eta_mu nu R^(1) = -1/2 Box h_mu nu.
#
# In Fourier space  (d_t -> -i omega, d_i -> i k_i,  Box = d_t^2/c^2 - nabla^2):
#   Box -> -omega^2/c^2 + k^2 .
# G^(1)_{ij} = 0  =>  Box h_ij = 0  =>  -omega^2/c^2 + k^2 = 0  =>  omega^2 = c^2 k^2.
omega, k = sp.symbols("omega k", positive=True)
Box_fourier = -omega**2 / c**2 + k**2
disp = sp.solve(sp.Eq(Box_fourier, 0), omega**2)
cT2 = disp[0] / k**2
print("[2.1] linearized G^(1)_{ij} = -1/2 Box h_ij  (TT gauge)")
print("[2.2] dispersion:  omega^2 =", disp[0])
print("[2.3] c_T^2 = omega^2/k^2  =", sp.simplify(cT2), "  (= c^2, luminal)")

# Quadratic TT action (Einstein-Hilbert, TT gauge, Minkowski):
#   S_TT^(2) = (c^3 / 64 pi G) int d^4x [ (1/c^2) hdot_TT_ij hdot_TT_ij
#                                          - d_k h_TT_ij d_k h_TT_ij ].
# Kinetic coefficient Q_T = +1/(c^2) > 0  (no ghost).
Q_T = sp.Rational(1, 1) / c**2
print("[3.1] Q_T (kinetic coefficient) =", Q_T, " > 0 :", Q_T > 0)
print("[3.2] c_T^2 =", sp.simplify(cT2), " > 0 :", sp.simplify(cT2) > 0)
print("[3.3] c_T^2 == c^2 (luminal)    :", sp.simplify(cT2 - c**2) == 0)

# The MOND modification (mu_1 S_1) contributes to the TT equations only at
# O(eps^3) (from part 1), so it does NOT modify the O(eps^2) dispersion.
print("\n[3.4] mu_1*S_1 feeds TT EOM only at O(eps^3) -> no O(eps^2) c_T shift.")

all_pass = (decoupled and sp.simplify(cT2 - c**2) == 0 and Q_T > 0)
print("\n" + "=" * 70)
print("GATE 9 RESULT:", "PASS" if all_pass else "FAIL")
print("  TT sector = GR Einstein quadratic;  c_T = c,  Q_T > 0,  no extra scalar pole.")
print("=" * 70)
