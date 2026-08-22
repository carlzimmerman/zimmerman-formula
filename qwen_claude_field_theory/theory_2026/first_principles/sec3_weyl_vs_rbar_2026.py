#!/usr/bin/env python3
"""
SECTION 3: exact relation between Rbar_munu (trace-free spatial Ricci of h_ij)
and the electric Weyl tensor E_ij, at linear order in the static weak-field
metric with INDEPENDENT potentials:

    ds^2 = -(1+2 Phi/c^2) c^2 dt^2 + (1-2 Psi/c^2) dx^2

Everything below is DERIVED by sympy from the metric; nothing is imported
except the standard 4D Weyl decomposition formula (textbook identity, exact).

Targets (to CHECK, not assume):
  (T1)  E_ij  = (1/c^2) S_ij[(Phi+Psi)/2]     with S_ij[f] = d_i d_j f - (1/3) delta_ij lap f
  (T2)  Rbar_ij = (1/c^2) S_ij[Psi]
  (T3)  Rbar ~ E  iff  S_ij[Phi - Psi] = 0  (i.e. Phi = Psi up to a quadratic;
        with decay at infinity, Phi = Psi + const)
  (T4)  a_i (khronon acceleration) = d_i Phi / c^2 at linear order
        => X is built from the LAPSE potential Phi, Y from the SPATIAL potential Psi.

Run:  python3 sec3_weyl_vs_rbar_2026.py   -> prints PASS/FAIL per check.
"""

import sympy as sp

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
t, x, y, z = sp.symbols('t x y z', real=True)
c = sp.symbols('c', positive=True)
ep = sp.symbols('epsilon', positive=True)   # linearization bookkeeping parameter

Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

coords = [t, x, y, z]
n = 4

# metric: static weak field, independent potentials
g = sp.diag(-(1 + 2*ep*Phi/c**2)*c**2,
            (1 - 2*ep*Psi/c**2),
            (1 - 2*ep*Psi/c**2),
            (1 - 2*ep*Psi/c**2))
ginv = g.inv()   # diagonal => exact inverse trivial

def lin(expr):
    """Truncate to first order in ep."""
    return sp.expand(sp.series(sp.expand(expr), ep, 0, 2).removeO())

# ----------------------------------------------------------------------
# Christoffels, Riemann, Ricci (exact, then truncated at O(ep))
# ----------------------------------------------------------------------
print("computing Christoffels...")
Gamma = [[[sp.simplify(sum(ginv[a, d]*(sp.diff(g[d, b], coords[cc])
                                        + sp.diff(g[d, cc], coords[b])
                                        - sp.diff(g[b, cc], coords[d]))
                            for d in range(n))/2)
           for cc in range(n)] for b in range(n)] for a in range(n)]

print("computing Riemann (linear order)...")
# R^a_{bcd} = d_c G^a_{db} - d_d G^a_{cb} + G^a_{ce} G^e_{db} - G^a_{de} G^e_{cb}
Riem_up = [[[[lin(sp.diff(Gamma[a][d][b], coords[cc]) - sp.diff(Gamma[a][cc][b], coords[d])
              + sum(Gamma[a][cc][e]*Gamma[e][d][b] - Gamma[a][d][e]*Gamma[e][cc][b]
                    for e in range(n)))
              for d in range(n)] for cc in range(n)] for b in range(n)] for a in range(n)]

# lower first index: R_{abcd} = g_{ae} R^e_{bcd}
Riem = [[[[lin(sum(g[a, e]*Riem_up[e][b][cc][d] for e in range(n)))
           for d in range(n)] for cc in range(n)] for b in range(n)] for a in range(n)]

# Ricci R_{bd} = R^a_{bad}, scalar R = g^{bd} R_{bd}
Ric = [[lin(sum(Riem_up[a][b][a][d] for a in range(n))) for d in range(n)] for b in range(n)]
Rsc = lin(sum(ginv[b, d]*Ric[b][d] for b in range(n) for d in range(n)))

# ----------------------------------------------------------------------
# Weyl tensor (4D decomposition; textbook identity, exact in D=4):
# C_abcd = R_abcd - (1/2)(g_ac R_bd - g_ad R_bc - g_bc R_ad + g_bd R_ac)
#          + (R/6)(g_ac g_bd - g_ad g_bc)
# ----------------------------------------------------------------------
print("computing Weyl...")
def Weyl(a, b, cc, d):
    expr = (Riem[a][b][cc][d]
            - sp.Rational(1, 2)*(g[a, cc]*Ric[b][d] - g[a, d]*Ric[b][cc]
                                 - g[b, cc]*Ric[a][d] + g[b, d]*Ric[a][cc])
            + Rsc/6*(g[a, cc]*g[b, d] - g[a, d]*g[b, cc]))
    return lin(expr)

# ----------------------------------------------------------------------
# Khronon 4-velocity u_mu = -d_mu T / sqrt(-g^{ab} d_a T d_b T), T = t
# ----------------------------------------------------------------------
norm = sp.sqrt(-ginv[0, 0])                      # = 1/(c sqrt(1+2 ep Phi/c^2))
u_lo = [-1/norm, 0, 0, 0]                        # u_t = -c sqrt(1+2 ep Phi/c^2)
u_up = [lin(ginv[0, 0]*u_lo[0]), 0, 0, 0]        # u^t

# check normalization exactly
unorm = sp.simplify(sum(g[a, b]*sp.simplify(ginv[0, 0]*u_lo[0])*sp.simplify(ginv[0, 0]*u_lo[0])
                        if (a == 0 and b == 0) else 0 for a in range(n) for b in range(n)))
unorm = sp.simplify(g[0, 0]*(ginv[0, 0]*u_lo[0])**2)
check_norm = sp.simplify(unorm + 1)

# ----------------------------------------------------------------------
# Electric Weyl E_ij = C_{i a j b} u^a u^b  (only a=b=t survives)
# ----------------------------------------------------------------------
print("computing E_ij...")
E = sp.zeros(3, 3)
for i in range(1, 4):
    for j in range(1, 4):
        E[i-1, j-1] = lin(Weyl(i, 0, j, 0)*u_up[0]*u_up[0])

# ----------------------------------------------------------------------
# Trace-free spatial Ricci of h_ij = g_ij (induced metric on t=const;
# for the static hypersurface-orthogonal khronon these coincide, K_ij = 0)
# ----------------------------------------------------------------------
print("computing 3-Ricci of h_ij...")
sp3 = [x, y, z]
h = sp.diag(1 - 2*ep*Psi/c**2, 1 - 2*ep*Psi/c**2, 1 - 2*ep*Psi/c**2)
hinv = h.inv()
G3 = [[[sp.simplify(sum(hinv[a, d]*(sp.diff(h[d, b], sp3[cc])
                                     + sp.diff(h[d, cc], sp3[b])
                                     - sp.diff(h[b, cc], sp3[d])) for d in range(3))/2)
        for cc in range(3)] for b in range(3)] for a in range(3)]
Ric3 = [[lin(sum(sp.diff(G3[a][b][d], sp3[a]) - sp.diff(G3[a][a][b], sp3[d])
                 + sum(G3[a][a][e]*G3[e][d][b] - G3[a][d][e]*G3[e][a][b] for e in range(3))
                 for a in range(3)))
         for d in range(3)] for b in range(3)]
R3 = lin(sum(hinv[b, d]*Ric3[b][d] for b in range(3) for d in range(3)))
Rbar = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Rbar[i, j] = lin(Ric3[i][j] - sp.Rational(1, 3)*h[i, j]*R3)

# ----------------------------------------------------------------------
# Khronon acceleration a_mu = u^a grad_a u_mu (static => a_i = d_i ln N)
# ----------------------------------------------------------------------
print("computing a_i...")
acc = []
for m in range(n):
    expr = sum(u_up[a]*(sp.diff(u_lo[m], coords[a])
                        - sum(Gamma[e][a][m]*u_lo[e] for e in range(n)))
               for a in range(n))
    acc.append(lin(expr))

# ----------------------------------------------------------------------
# Reference operators
# ----------------------------------------------------------------------
def lap(f):
    return sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)

def S(f):
    """Trace-free Hessian S_ij[f]."""
    M = sp.zeros(3, 3)
    for i, xi in enumerate(sp3):
        for j, xj in enumerate(sp3):
            M[i, j] = sp.diff(f, xi, xj) - (sp.KroneckerDelta(i, j) if False else 0)
    for i in range(3):
        M[i, i] -= sp.Rational(1, 3)*lap(f)
    return M

S_weyl = S((Phi + Psi)/2)   # target for E
S_psi  = S(Psi)             # target for Rbar
S_phi  = S(Phi)

# ----------------------------------------------------------------------
# CHECKS
# ----------------------------------------------------------------------
results = []

def check(name, mat_diff):
    ok = all(sp.simplify(mat_diff[i, j]) == 0 for i in range(3) for j in range(3))
    results.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(sp.simplify(mat_diff))
    return ok

print("\n================ CHECKS ================")

# C0: u normalization
ok0 = sp.simplify(check_norm) == 0
results.append(("C0 u.u = -1 exactly", ok0))
print(f"[{'PASS' if ok0 else 'FAIL'}] C0 u.u = -1 exactly")

# C1: E_ij = (ep/c^2) S_ij[(Phi+Psi)/2]
check("C1 E_ij == (1/c^2) S_ij[(Phi+Psi)/2]",
      sp.Matrix(3, 3, lambda i, j: E[i, j] - ep/c**2*S_weyl[i, j]))

# C2: E is trace-free (Weyl property, consistency)
trE = sp.simplify(E[0, 0] + E[1, 1] + E[2, 2])
ok2 = trE == 0
results.append(("C2 tr E = 0", ok2))
print(f"[{'PASS' if ok2 else 'FAIL'}] C2 tr E = 0   (got {trE})")

# C3: Rbar_ij = (ep/c^2) S_ij[Psi]
check("C3 Rbar_ij == (1/c^2) S_ij[Psi]",
      sp.Matrix(3, 3, lambda i, j: Rbar[i, j] - ep/c**2*S_psi[i, j]))

# C4: full 3-Ricci for reference: Ric3_ij = (ep/c^2)(d_i d_j Psi + delta_ij lap Psi)
check("C4 Ric3_ij == (1/c^2)(d_i d_j Psi + delta_ij lap Psi)",
      sp.Matrix(3, 3, lambda i, j: Ric3[i][j]
                - ep/c**2*(sp.diff(Psi, sp3[i], sp3[j])
                           + (1 if i == j else 0)*lap(Psi))))

# C5: Rbar - E = (ep/(2 c^2)) S_ij[Psi - Phi]   (exact difference law)
check("C5 Rbar_ij - E_ij == (1/(2c^2)) S_ij[Psi - Phi]",
      sp.Matrix(3, 3, lambda i, j: (Rbar[i, j] - E[i, j])
                - ep/(2*c**2)*(S_psi[i, j] - S_phi[i, j])))

# C6: at Phi = Psi, Rbar_ij == E_ij exactly (proportionality constant 1)
subs_eq = {Phi: Psi}
ok6 = all(sp.simplify((Rbar[i, j] - E[i, j]).subs(Phi, Psi).doit()) == 0
          for i in range(3) for j in range(3))
results.append(("C6 Phi=Psi => Rbar_ij = E_ij (constant exactly 1)", ok6))
print(f"[{'PASS' if ok6 else 'FAIL'}] C6 Phi=Psi => Rbar_ij = E_ij (constant exactly 1)")

# C7: khronon acceleration a_i = ep d_i Phi / c^2 (lapse-built; no Psi anywhere)
ok7 = (sp.simplify(acc[0]) == 0 and
       all(sp.simplify(acc[i] - ep*sp.diff(Phi, sp3[i-1])/c**2) == 0 for i in range(1, 4)))
results.append(("C7 a_i = d_i Phi / c^2 (X is LAPSE-built, Psi-free)", ok7))
print(f"[{'PASS' if ok7 else 'FAIL'}] C7 a_i = d_i Phi / c^2 (X is LAPSE-built, Psi-free)")

# C8: Y invariant at leading order: Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi]  (O(ep^2))
a0 = sp.symbols('a0', positive=True)
Ycontr = sp.expand(sum(Rbar[i, j]*Rbar[i, j] for i in range(3) for j in range(3)))
# raise indices with h^ij ~ delta + O(ep): corrections are O(ep^3), drop
Ytarget = sp.expand(ep**2/c**4*sum(S_psi[i, j]**2 for i in range(3) for j in range(3)))
ok8 = sp.simplify(sp.expand(Ycontr - Ytarget)) == 0
results.append(("C8 Rbar.Rbar = (1/c^4) S[Psi]:S[Psi] + O(ep^3)  => Y = (c^4/a0^4) S[Psi]:S[Psi]", ok8))
print(f"[{'PASS' if ok8 else 'FAIL'}] C8 Rbar.Rbar = (1/c^4) S[Psi]:S[Psi]  => Y = (c^4/a0^4) S[Psi]:S[Psi]")

print("\n================ SUMMARY ================")
npass = sum(1 for _, ok in results if ok)
print(f"{npass}/{len(results)} checks passed")
for name, ok in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
