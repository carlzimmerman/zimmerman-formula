import sympy as sp

# ============================================================
# DW2026 mimetic-clock sector: boosted PPN alpha_2 structure.
# Claim A: mimetic constraint (d phi)^2 = -1 linearizes to a FIRST-ORDER
#          slaving d_t(dphi) = -h00/2  -> phi is NOT a propagating mode,
#          carries no O(1) kinetic response (unlike a dynamical aether).
# Claim B: the ONLY unsuppressed metric back-reaction is the dust stress
#          T^mim = rho u_mu u_nu, PROPORTIONAL to rho0 (cosmological).
# ============================================================

t,x,y,z = sp.symbols('t x y z', real=True)
eps = sp.symbols('epsilon', positive=True)   # PPN bookkeeping small param

# --- Metric: eta + h, h from a boosted point source. Signature (-+++), c=1.
# We only need g^{munu} to linear order for the constraint.
h00, h0i, hij = sp.symbols('h00 h0i hij')     # schematic magnitudes ~ O(eps)
# Newtonian: h_00 = 2U, h_ij = 2Phi delta_ij, h_0i = O(w U) gravitomagnetic.

# --- Mimetic scalar phi = t + chi,  chi = O(eps) perturbation ("dphi")
chi = sp.Function('chi')(t,x,y,z)

# Build g^{munu} to linear order. Use explicit small perturbations h_{ab}.
H00 = sp.Function('H00')(t,x,y,z)   # h_{00}(t,x)
H0 = [sp.Function('H0%d'%i)(t,x,y,z) for i in range(1,4)]  # h_{0i}
# inverse metric to linear order:  g^{00}=-1 - h_{00}; g^{0i}= h_{0i}; g^{ij}=delta-h_{ij}
# (indices: h^{00}=h_{00}, h^{0i}=-h_{0i}, using eta to raise)
g_up00 = -1 - H00
g_up0i = [H0[i] for i in range(3)]

# phi = t + chi. Gradients:
dphi_t  = 1 + sp.diff(chi,t)
coords_i = [x,y,z]
dphi_i  = [sp.diff(chi,c) for c in coords_i]

# Constraint C = g^{munu} dphi_mu dphi_nu + 1 = 0, linearize in eps.
C = g_up00*dphi_t**2
for i in range(3):
    C += 2*g_up0i[i]*dphi_t*dphi_i[i]
# g^{ij} dphi_i dphi_j is O(eps^2) (dphi_i ~ eps), drop at linear order.
C = C + 1
# Linearize: treat chi, H00, H0 as O(eps); keep first order.
Clin = C.expand()
# Substitute smallness: keep terms linear in {chi-derivs, H00, H0}
# Do it by series in a dummy scaling lambda:
lam = sp.symbols('lambda')
subs_scale = {chi: lam*chi, H00: lam*H00}
for i in range(3): subs_scale[H0[i]] = lam*H0[i]
Cscaled = C.subs(subs_scale, simultaneous=True)
Cser = sp.series(Cscaled, lam, 0, 2).removeO()
C_order0 = Cser.subs(lam,0)
C_order1 = sp.diff(Cser, lam).subs(lam,0)
print("Constraint O(eps^0):", sp.simplify(C_order0))     # should be 0 (background)
print("Constraint O(eps^1):", sp.simplify(C_order1))     # the slaving equation

# Solve O(eps^1) for d_t chi:
dtchi = sp.diff(chi,t)
sol = sp.solve(sp.Eq(C_order1,0), dtchi)
print("Slaving  d_t(chi) =", sol)   # expect -H00/2

# --- Highest time-derivative present? If only FIRST order in d_t chi,
#     phi is slaved (constrained), NOT a wave (which would carry d_t^2).
has_second_time = C_order1.has(sp.Derivative(chi,(t,2)))
print("Constraint contains d_t^2(chi) (=> propagating wave)?", has_second_time)
