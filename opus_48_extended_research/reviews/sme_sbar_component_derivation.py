#!/usr/bin/env python3
"""
Component-by-component derivation of the induced SME GRAVITY-SECTOR s_bar^munu
in the Sun-centered celestial-equatorial frame (SCF).

Spurion model (given by the task):
    s_bar^munu = (a0/(2|a|)) * P^munu
    P^munu = u^mu u^nu - (1/4) eta^munu (u.u)      [symmetric, traceless]
    u^mu = gamma*(1, beta*n_hat),  u.u = -1,  mostly-plus eta=diag(-1,1,1,1)

n_hat from CMB dipole apex: RA=167.9 deg, Dec=-6.9 deg (SCF celestial-equatorial).
beta = beta_cmb = 369.82/c (km/s).

We expand every component to O(beta^2), tabulate beta-scaling, numeric magnitude at
|a|=g=9.8 (prefactor a0/2g=4.78e-12), DC-vs-sidereal in a ground lab, and
observability per Bailey-Kostelecky gr-qc/0603030.
"""
import sympy as sp

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
beta, A = sp.symbols('beta A', real=True, positive=True)   # A = a0/(2|a|) prefactor
nx, ny, nz = sp.symbols('n_x n_y n_z', real=True)          # components of n_hat (unit)

# gamma = 1/sqrt(1-beta^2)
gamma = 1/sp.sqrt(1-beta**2)

# u^mu (contravariant), mostly-plus
uT = gamma
uX = gamma*beta*nx
uY = gamma*beta*ny
uZ = gamma*beta*nz
u = sp.Matrix([uT, uX, uY, uZ])

# metric mostly-plus
eta = sp.diag(-1, 1, 1, 1)

# Verify u.u = -1  (u_mu u^mu = eta_munu u^mu u^nu)
u_dot_u = (u.T * eta * u)[0]
u_dot_u = sp.simplify(u_dot_u)
print("CHECK u.u =", u_dot_u, " (should be -1, using n_x^2+n_y^2+n_z^2=1)")
# substitute unit-vector constraint
u_dot_u_unit = sp.simplify(u_dot_u.subs(nx**2, 1-ny**2-nz**2))
print("CHECK u.u (with unit nhat) =", sp.simplify(u_dot_u_unit))

# ---------------------------------------------------------------------------
# P^munu = u^mu u^nu - (1/4) eta^munu (u.u),  with u.u = -1 EXACTLY (unit timelike)
# So P^munu = u^mu u^nu + (1/4) eta^munu
# eta^munu (contravariant) = inverse of eta = diag(-1,1,1,1) (same, mostly-plus)
# ---------------------------------------------------------------------------
eta_inv = sp.diag(-1, 1, 1, 1)   # eta^{munu}
uu = u*u.T                        # u^mu u^nu  (4x4)
P = uu + sp.Rational(1,4)*eta_inv  # since (u.u)=-1 -> -(1/4)*eta*(-1)=+(1/4)*eta

# Trace check: eta_munu P^munu = 0  (lower both indices)
trace_P = sp.simplify((sp.ones(1,1)*0)[0])
tr = 0
for mu in range(4):
    for nu in range(4):
        tr += eta[mu,mu]*eta[nu,nu]*P[mu,nu]  # eta_{mu mu'} eta_{nu nu'} P^{mu' nu'} contracted with eta^{munu}...
# Cleaner: eta_munu P^munu = sum_{mu,nu} eta[mu,nu]*P[mu,nu] (eta diagonal)
trace = 0
for mu in range(4):
    trace += eta[mu,mu]*P[mu,mu]
trace = sp.simplify(trace)
print("\nCHECK trace eta_munu P^munu =", trace, "(should be 0 exactly since u.u=-1)")

# s_bar^munu = A * P^munu
S = A*P

labels = ['T','X','Y','Z']

def comp(mu, nu):
    return sp.simplify(S[mu,nu])

# ---------------------------------------------------------------------------
# Expand each component to O(beta^2)
# ---------------------------------------------------------------------------
print("\n=== s_bar^munu expanded to O(beta^2) (prefactor A = a0/2|a|) ===")
comps = {}
order_beta = {}
for mu in range(4):
    for nu in range(mu, 4):
        name = 's_'+labels[mu]+labels[nu]
        expr = comp(mu,nu)
        ser = sp.series(expr, beta, 0, 3).removeO()
        ser = sp.expand(ser)
        comps[name] = ser
        print(f"{name:6s} = {ser}")

# ---------------------------------------------------------------------------
# Numeric: n_hat from RA=167.9, Dec=-6.9 ; beta_cmb = 369.82/299792.458
# ---------------------------------------------------------------------------
import mpmath as mp
mp.mp.dps = 30
RA  = mp.radians(167.9)
Dec = mp.radians(-6.9)
nhx = mp.cos(Dec)*mp.cos(RA)
nhy = mp.cos(Dec)*mp.sin(RA)
nhz = mp.sin(Dec)
print("\nn_hat =", (float(nhx), float(nhy), float(nhz)),
      " norm=", float(mp.sqrt(nhx**2+nhy**2+nhz**2)))

c_kms = mp.mpf('299792.458')
beta_cmb = mp.mpf('369.82')/c_kms
print("beta_cmb =", float(beta_cmb))

# prefactor at |a|=g: a0/(2g)
a0 = mp.mpf('9.36e-11')
g  = mp.mpf('9.8')
A_g = a0/(2*g)
print("A=a0/2g =", float(A_g))

# numeric P (exact, unit u.u=-1)
gam = 1/mp.sqrt(1-beta_cmb**2)
uvec = [gam, gam*beta_cmb*nhx, gam*beta_cmb*nhy, gam*beta_cmb*nhz]
etam = [[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
Pnum = [[uvec[i]*uvec[j] + mp.mpf('0.25')*etam[i][j] for j in range(4)] for i in range(4)]
# trace check numeric
trn = sum(etam[i][i]*Pnum[i][i] for i in range(4))
print("numeric trace eta_munu P^munu =", float(trn))

print("\n=== Numeric s_bar^munu at |a|=g (value = A_g * P) ===")
for i in range(4):
    for j in range(i,4):
        name='s_'+labels[i]+labels[j]
        val = A_g*Pnum[i][j]
        print(f"{name:6s} = {mp.nstr(val, 6):>14s}   (P={mp.nstr(Pnum[i][j],6)})")

# Off-diagonal SPATIAL differences and the isotropic spatial trace
sXX = A_g*Pnum[1][1]; sYY=A_g*Pnum[2][2]; sZZ=A_g*Pnum[3][3]
print("\n--- spatial structure ---")
print("trace_spatial s^JJ = sXX+sYY+sZZ =", mp.nstr(sXX+sYY+sZZ,6),
      " = A*(beta^2*gamma^2 + 3/4) ~ 3A/4 (the DC isotropic piece)")
iso = (sXX+sYY+sZZ)/3
print("isotropic spatial avg =", mp.nstr(iso,6))
print("anisotropic sXX-iso =", mp.nstr(sXX-iso,6),
      "  sYY-iso=", mp.nstr(sYY-iso,6), "  sZZ-iso=", mp.nstr(sZZ-iso,6))
print("traceless spatial off-diag sXY =", mp.nstr(A_g*Pnum[1][2],6))

# s_TT and the pure-time piece
print("\ns_TT = A*(gamma^2 - 1/4) = 3A/4 + A*beta^2*gamma^2 (DC, isotropic-time)")
print("  s_TT numeric =", mp.nstr(A_g*Pnum[0][0],6))
print("s_TJ = A*gamma^2*beta*n_J  (O(beta), the boost dipole)")
for J,nh in zip(['X','Y','Z'],[nhx,nhy,nhz]):
    print(f"  s_T{J} = {mp.nstr(A_g*gam**2*beta_cmb*nh,6)}")
