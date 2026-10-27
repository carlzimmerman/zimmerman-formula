#!/usr/bin/env python3
# ROUTE 3 AUDIT -- PART 1: re-derive "dynamics sees rho+3p, lensing sees rho+p" FROM SCRATCH.
# No formula taken on trust.  Explicit static isotropic metric -> Einstein tensor -> linearise.
import sympy as sp

t, r, th, ph = sp.symbols("t r theta varphi", real=True)
X = [t, r, th, ph]
Phi = sp.Function("Phi")(r)
Psi = sp.Function("Psi")(r)
eps = sp.Symbol("varepsilon", positive=True)     # bookkeeping order parameter
G, pi = sp.symbols("G pi", positive=True)

# isotropic-coordinate static metric
g = sp.diag(-(1 + 2*eps*Phi), (1 - 2*eps*Psi), (1 - 2*eps*Psi)*r**2,
            (1 - 2*eps*Psi)*r**2*sp.sin(th)**2)
ginv = g.inv()

def christoffel(g, ginv, X):
    n = len(X)
    Ga = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b])
                                     - sp.diff(g[b, c], X[d]))
                Ga[a][b][c] = sp.simplify(s/2)
    return Ga

Ga = christoffel(g, ginv, X)

def ricci(Ga, X):
    n = len(X)
    R = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Ga[a][b][c], X[a]) - sp.diff(Ga[a][b][a], X[c])
                for d in range(n):
                    s += Ga[a][a][d]*Ga[d][b][c] - Ga[a][c][d]*Ga[d][b][a]
            R[b, c] = s
    return R

Ric = ricci(Ga, X)
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(4) for j in range(4)))
Ein = sp.Matrix(4, 4, lambda i, j: Ric[i, j] - Rs*g[i, j]/2)

def lin(e):
    return sp.simplify(sp.series(sp.simplify(e), eps, 0, 2).removeO().coeff(eps, 1))

lap = lambda F: sp.diff(F, r, 2) + 2*sp.diff(F, r)/r   # flat 3-Laplacian, spherical

# ---- G_tt  ->  rho ;  spatial trace  ->  p
G_tt = lin(Ein[0, 0])
G_rr = lin(Ein[1, 1])
G_thth = lin(Ein[2, 2]/r**2)
print("linearised G_tt      =", sp.simplify(G_tt))
print("linearised G_rr      =", sp.simplify(G_rr))
print("linearised G_thth/r^2=", sp.simplify(G_thth))

# Einstein eq: G_mu_nu = 8 pi G T_mu_nu, T = diag(rho, p_r, p_t, p_t) in the ORTHONORMAL frame.
# G_tt component with g_tt = -(1+2 eps Phi):  T_tt = rho*(1+2 eps Phi) -> at O(eps): T_tt = rho
rho, p_r, p_t = sp.symbols("rho p_r p_t", real=True)
eq_tt = sp.Eq(G_tt, 8*pi*G*rho)
sol_Psi = sp.solve(eq_tt, lap(Psi))
print("\n[A] from G_tt:  Laplacian(Psi) =", sp.simplify(sol_Psi[0]) if sol_Psi else "??")

# spatial trace: g^ij G_ij = 8 pi G (p_r + 2 p_t) at O(eps)
sp_trace = sp.simplify(G_rr + 2*G_thth)
eq_sp = sp.Eq(sp_trace, 8*pi*G*(p_r + 2*p_t))
print("[B] spatial-trace equation:", sp.simplify(sp_trace), "= 8 pi G (p_r+2p_t)")

# solve the pair for Laplacian(Phi), Laplacian(Psi)
LP, LS = sp.symbols("LapPhi LapPsi")
subsmap = {lap(Phi): LP, lap(Psi): LS}
e1 = sp.expand(G_tt - 8*pi*G*rho)
e2 = sp.expand(sp_trace - 8*pi*G*(p_r + 2*p_t))
# express in terms of the two Laplacians by matching derivative structure
e1 = e1.subs({sp.diff(Psi, r, 2): LS - 2*sp.diff(Psi, r)/r})
e2 = e2.subs({sp.diff(Phi, r, 2): LP - 2*sp.diff(Phi, r)/r,
              sp.diff(Psi, r, 2): LS - 2*sp.diff(Psi, r)/r})
sol = sp.solve([sp.simplify(e1), sp.simplify(e2)], [LP, LS], dict=True)
print("\n[C] SOLVED:")
for s in sol:
    print("    Laplacian(Phi) =", sp.simplify(s[LP]))
    print("    Laplacian(Psi) =", sp.simplify(s[LS]))
    lens = sp.simplify((s[LP] + s[LS])/2)
    print("    Laplacian((Phi+Psi)/2) =", sp.simplify(lens))
    print("    => DYNAMICS source /(4 pi G) =", sp.simplify(s[LP]/(4*pi*G)))
    print("    => LENSING  source /(4 pi G) =", sp.simplify(lens/(4*pi*G)))
