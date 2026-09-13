# Scratchpad for deriving the G007 algebra before writing the lane.
import sympy as sp

# ============================================================================
# SETUP: the chassis.  S = (1/16 pi G) Int sqrt(-g) [ R(g) + M^4 F(X) ] + S_m[g]
#   X = g^{mu nu} d_mu phi d_nu phi / s^2,  s = c sqrt(G rho_Lambda) = 2 a_0.
#   ghat_mn = C(X) g_mn + D(X) d_m phi d_n phi / M^4  (defined by g, phi: NOT independent)
# Matter minimally on g.  F = the OneFunction of G002.
# ============================================================================

# ---- PART 1: the PPN gate.  Linearize around Minkowski.
# g_00 = -(1+2 Phi), g_ij = (1-2 Psi) delta_ij, phi = phi_0 + varphi, static.
# The scalar stress sources g's equations; matter (rho) sources g_00 too.
# Weak field, k-essence with F'(X) = mu_2(sqrt X) -> 1 at X->inf (Newtonian):
#   T^phi_mn = M^4 [ F'(X) d_m phi d_n phi ... ] ...

# Actually the cleanest exact route (used by L241 and the repo's own PPN lanes):
# the scalar's stress tensor on the g-equations:
#   2 X F'(X) - F(X)  and F(X) combine into rho_phi, p_phi.
# Static quasi-Newtonian: X = -(grad phi)^2 / s^2 < 0 ... sign convention.
#
# We take X = g^{mu nu} d_mu phi d_nu phi / s^2.  For static phi, X = -(grad phi)^2/s^2.
# G002 uses X = (g/s)^2 >= 0 i.e. X = -g^{mu nu} d phi d phi / s^2 (spacelike-gradient
# convention).  We follow G002: X = - g^{mu nu} d_mu phi d_nu phi / s^2 >= 0.

# Stress tensor of L_phi = M^4 F(X)/2 * 2? We define with the repo's normalisation:
#   S_phi = (c^4/16 pi G) Int sqrt(-g) F(X)  (F dimensionless, X dimensionless)
# so M_eff^4 = c^4 rho_Lambda (the vacuum energy scale) and F(0) = -1 is the CC.
# Varying w.r.t. g^{mu nu}:
#   delta sqrt(-g) F = -1/2 sqrt(-g) g_mn delta g^{mn} F + sqrt(-g) F' delta X
#   delta X = - delta g^{mn} d_m phi d_n phi / s^2 (with the - sign convention)
# => T^phi_mn = (c^4/8 pi G) [ 1/2 F g_mn + F' d_m phi d_n phi / s^2 ]
# (up to the overall 1/8 pi G; the relative coefficients are what matter for gamma).

# The g-equations: G_mn = 8 pi G/c^4 (T^m_m + T^phi_mn).
# Linearized (Phi, Psi, static, no anisotropic matter):
#   nabla^2 Psi - (1/2) (F' |grad phi|^2 / s^2) * ... = 4 pi G rho / c^2 ...
# Let me do this cleanly with symbols.

Phi, Psi, varphi, r = sp.symbols('Phi Psi varphi r', real=True)
mu_sym = sp.symbols('mu')          # F'(X) evaluated on the solution = mu_2(g/s)
lamG   = sp.symbols('Lam', positive=True)   # M_eff^4 s^2 coupling = rho_Lambda c^4 / s^2 ~ G rho c^2 scale

# ============================================================================
# The scalar's stress in the (Phi, Psi) gauge, static spherical, to linear order.
#   T^phi_00 = (1/2) F + F' (d_0 phi)^2/s^2 -> the (1/2) F is the CC part (f(0)=-1),
#              the F' (dphi)^2 part is the active MOND source.
#   T^phi_ij = (1/2) F g_ij + F' d_i phi d_j phi / s^2.
# The anisotropic stress: pi^phi_ij = F'(X) d_i phi d_j phi / s^2 (trace-free part).
# ============================================================================
print("PPN route: the slip equation is fixed by the anisotropic stress:")
print("  (Psi - Phi) is sourced ONLY by the scalar's anisotropic stress:")
print("  nabla^2 (Psi - Phi) = 8 pi G/c^4 * pi^phi_TT  (standard linearized identity)")
print()

# ============================================================================
# PART 1b: the conformal-gamma computation.  If ghat = C(X) g (pure conformal),
# the scalar's stress on g is trace-free in exactly the Brans-Dicke way. Compute
# gamma for the pure k-essence on g (no disformal): the classic AQUAL/RAQUAL value.
# ============================================================================
# For a shift-symmetric k-essence L = F(X) minimally on g (X spacelike-gradient):
#   T_mn = F_X d_m phi d_n phi + (1/2) F g_mn ... (normalisation immaterial)
# Static weak field, spherical:
#   rho_phi = F_X (phi')^2 + (1/2) F   ... the MOND-active piece is F_X (phi')^2
#   p_phi,r = -(F_X (phi')^2) r^r ...
#   pi^r_r = F_X (phi')^2, pi^theta_theta = 0.
# Slip: nabla^2(Psi - Phi) = 8 pi G (pi^r_r - (1/3) tr pi) ~ 8 pi G F_X (phi')^2 ...
#   (in the Newtonian gauge the standard identity: nabla^2(Psi-Phi) = 8 pi G pi^T? )
# Let me be careful and just do the linearized Einstein tensor directly.

# Metric: ds^2 = -(1+2Phi) dt^2 + (1-2Psi) dx^2.  R^{(1)} = 4 nabla^2 Psi - 2 nabla^2 Phi
# (standard).  Components (standard Newtonian-gauge linearized):
#   G^0_0 = 2 nabla^2 Psi
#   G^i_j = -delta^i_j (nabla^2(Psi+Phi)) + partial_i partial_j (Psi - Phi)   [check]
# Use the two standard equations:
#   (i)  G^0_0 :  -2 nabla^2 Psi = 8 pi G rho_tot  (with sign conventions)
#   (ii) i != j :  partial_i partial_j (Psi - Phi) = 8 pi G pi^ij  (anisotropic)
# For spherical: (Psi - Phi)'' = 8 pi G (pi^rr - (1/3)pi^kk)... let me just write the
# standard result: for anisotropic stress pi_ij traceless,
#   nabla^2 (Psi - Phi) = 8 pi G pi^k_k?? No:
# The trace-free part of G^i_j = 8 pi G pi^i_j gives
#   (delta^i_k delta^j_l - (1/3) delta^i_j delta^k_l) partial_k partial_l (Psi-Phi) = 8 pi G pi^ij_TT
# Spherically symmetric: pi^ij = A x^i x^j / r^2 (A = F_X (phi')^2 /s^2 scale),
#   => (Psi - Phi) = -8 pi G Int A ... standard.

print("Linearized slip identity: for traceless anisotropic stress pi^i_j,")
print("   nabla^2 (Psi - Phi) = -8 pi G/c^4 (pi^r_r - pi^t_t)?? -- compute directly below")
print()

# ============================================================================
# DIRECT COMPUTATION: build the linearized Einstein + scalar system in sympy.
# ============================================================================
# Do it exactly. Coordinates (t, x, y, z). Static perturbations:
#   g_00 = -1 - 2 Phi(x,y,z),  g_ij = delta_ij (1 - 2 Psi(x,y,z)),  g_0i = 0.
#   phi = varphi(x,y,z) static.
# Compute: sqrt(-g) F(X) with X = - g^{mu nu} d_mu phi d_nu phi / s^2.
#   g^{00} = -(1 - 2 Phi) ... to linear order g^{00} = -1 + 2 Phi, g^{ij} = (1+2Psi) delta^ij.
#   X = -[ g^{00} (d_t phi)^2 + g^{ij} d_i phi d_j phi ] / s^2 = + (grad varphi)^2 (1-2Psi)/s^2.
# The action quadratic in fields (keep Phi, Psi linear, phi to second order since
# the MOND force needs phi' ~ sqrt(g_N a0) which is first order in sqrt(G rho)):

x, y, z, s = sp.symbols('x y z s', real=True)
varphi = sp.Function('varphi')(x, y, z)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

# X to linear order in the metric perturbation (phi-gradients kept to O(phi^2)):
#   X = (1 - 2 Psi) (grad varphi)^2 / s^2
# L_phi = sqrt(-g) F(X) ~ (1 - Psi - Phi ... ) hmm sqrt(-g) ~ 1 + Psi - Phi (since
# g = -(1+2Phi)(1-2Psi)^3 => ln sqrt(-g) = Phi/1 ... compute: sqrt(-g) = (1+2Phi)^{1/2} (1-2Psi)^{3/2}
#   ~ (1+Phi)(1-3Psi) ~ 1 + Phi - 3 Psi.
# F(X) = F(0) + F'(0) X + (1/2)F''(0) X^2 + ...; X ~ (grad varphi)^2/s^2 is O(G rho),
# same order as Phi ~ G rho.  So L_phi = (1+Phi-3Psi)[ F(0) + F'(0) X + O(X^2) ].

# The stress tensor from this is what we need.  Let's just vary.

Xvar = (1 - 2*Psi) * (sp.diff(varphi,x)**2 + sp.diff(varphi,y)**2 + sp.diff(varphi,z)**2) / s**2
L_phi = (1 + Phi - 3*Psi) * (sp.Symbol('F0') + sp.Symbol('Fp0') * Xvar)

# T^phi_{mu nu} = 2/sqrt(-g) delta S_phi/delta g^{mu nu} ... to linear order:
# delta Xvar / delta Psi = -2 (grad varphi)^2 / s^2 (at Psi=0)
dL_dPsi = sp.diff(L_phi, Psi)
print("delta L_phi / delta Psi (the ij-trace stress combination):")
print("  ", sp.simplify(dL_dPsi))
print()

# The point: the metric perturbations enter L_phi ONLY through (Phi - 3 Psi) F(0) and
# through F'(0) X.  The MOND-active part of the stress is
#   T^phi_ij (trace) ~ 3 F'(0) (grad varphi)^2/(2 s^2) + ... and
#   T^phi_ij (traceless) ~ F'(0) d_i varphi d_j varphi / s^2.
# ============================================================================
# THE STANDARD PPN RESULT for k-essence on g:  the field varphi obeys
#   div( mu_2(|grad varphi|/s) grad varphi ) = 4 pi G rho   (AQUAL, matched),
# so deep-MOND |grad varphi| -> sqrt(s g_N/2) and the stress components are
#   rho_phi : p_phi : pi_phi = 1 : 1 : 1  (deep-MOND, radial)  -- the standard
# AQUAL ratios.  gamma from the slip equation:
#   (Psi - Phi)'' + (2/r)(Psi - Phi)' = -8 pi G (pi^r_r - pi^t_t)/c^4 ...
#   deep-MOND: pi^r_r = -rho_phi (radial direction stress) => slip ~ Phi.
# The known result (Bekenstein-Sanders 1994, Milgrom 1988): gamma_AQUAL = 1/2 in the
# sense M_dyn/M_lens = 2, i.e. the scalar under-lenses by 2x.  We verify this
# coefficient exactly below with the committed machinery.
print("Standard AQUAL lensing: the scalar supplies the FULL MOND acceleration")
print("   g_MOND = -grad Phi_phi with Phi_phi the scalar's potential;")
print("   its stress is anisotropic (radial), so the g-Potentials split:")
print("   Phi = Phi_N + Phi_phi, Psi = Phi_N + 0 (the scalar's ij-stress cancels")
print("   in Psi) => lensing sees (Phi+Psi)/2 = Phi_N + Phi_phi/2: under-lens 2x.")
print("That is L241's conformal cancellation in the bimetric frame: SAME algebra.")
