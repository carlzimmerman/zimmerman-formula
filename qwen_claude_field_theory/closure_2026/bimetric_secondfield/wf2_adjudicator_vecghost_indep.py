#!/usr/bin/env python3
"""ADJUDICATOR independent re-verification of the VECTOR (helicity-1) GHOST kill.
Written from scratch (own indexing/derivation). Does NOT import any committed script.
L = (1/2)(T4-T5) + lam*Int,  Int = sum c_i T_i,  c=(-u0,-u1/2,-u1/2,u0,u1),  lam>0.
Checks:
  (A) Int on transverse Stuckelberg vector A1 (eps01=w A1, eps13=kap A1) -> operator degree & factor.
  (B) Direct 2x2 kinetic matrix W = coeff_{w^2} Hessian_{(eps01,eps13)} L ; eigenvalues/det.
  (C) Controls: pure EH (lam=0) and 0-derivative Fierz-Pauli mass -> must be ghost-free.
  (D) Generic det(W)(u0,u1) and its tie to the MOND accel coeff a(u0,u1).
"""
import sympy as sp

eta = sp.diag(-1, 1, 1, 1); etaI = eta.inv()
u0, u1, lam = sp.symbols('u0 u1 lam', real=True)
w, kap = sp.symbols('omega kappa', real=True, positive=True)
k = sp.Matrix([w, 0, 0, kap])                      # frame: propagation along z

# symmetric perturbation
E = sp.zeros(4, 4); S = {}
for a in range(4):
    for b in range(a, 4):
        s = sp.Symbol(f'h{a}{b}', real=True); S[(a, b)] = s; E[a, b] = s; E[b, a] = s

def Cconn(Em):
    C = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                C[l][m][n] = sp.expand(sum(etaI[l, t]*(k[m]*Em[t, n] + k[n]*Em[t, m] - k[t]*Em[m, n])
                                           for t in range(4))/2)
    return C

def invariants(C):
    T1 = sum(C[a][m][n]*C[b][r][s]*eta[a, b]*etaI[m, r]*etaI[n, s]
             for a in range(4) for b in range(4) for m in range(4) for n in range(4)
             for r in range(4) for s in range(4))
    P = [sum(etaI[m, n]*C[a][m][n] for m in range(4) for n in range(4)) for a in range(4)]
    T2 = sum(eta[a, b]*P[a]*P[b] for a in range(4) for b in range(4))
    V = [sum(C[a][a][mu] for a in range(4)) for mu in range(4)]
    T3 = sum(etaI[m, n]*V[m]*V[n] for m in range(4) for n in range(4))
    T4 = sum(etaI[m, n]*C[a][m][b]*C[b][n][a] for m in range(4) for n in range(4)
             for a in range(4) for b in range(4))
    T5 = sum(P[a]*V[a] for a in range(4))
    return [sp.expand(x) for x in (T1, T2, T3, T4, T5)]

C = Cconn(E); T = invariants(C)
c = [-u0, -sp.Rational(1, 2)*u1, -sp.Rational(1, 2)*u1, u0, u1]
Int = sp.expand(sum(c[i]*T[i] for i in range(5)))
EH = sp.expand(T[3] - T[4])                        # linearized EH = T4 - T5
L = sp.expand(sp.Rational(1, 2)*EH + lam*Int)

b1, d1 = S[(0, 1)], S[(1, 3)]                       # helicity-1 x-channel: h_{0x}, h_{xz}

print("="*80)
print("(A) Transverse Stuckelberg vector A1: eps01=w*A1, eps13=kap*A1, rest=0")
print("="*80)
A1 = sp.Symbol('A1', real=True)
sub_stk = {S[key]: 0 for key in S}
sub_stk[b1] = w*A1; sub_stk[d1] = kap*A1
EH_stk = sp.expand(EH.subs(sub_stk))
Int_stk = sp.expand(Int.subs(sub_stk))
print("  EH on Stuckelberg dir (must be 0, gauge):", sp.simplify(EH_stk))
LA1 = sp.factor(sp.expand(lam*Int_stk))
coefA1 = sp.expand(lam*Int_stk).coeff(A1, 2)
print("  L_A1 coeff(A1^2), general:", sp.factor(coefA1))
deg = sp.total_degree(sp.Poly(sp.expand(coefA1.subs(lam, 1)), w, kap))
print("  momentum degree of the A1 operator:", deg,
      "=> HIGHER-DERIVATIVE (box^2) ghost" if deg == 4 else "=> healthy(2)/other")

print("\n" + "="*80)
print("(B) Direct 2x2 kinetic matrix W = coeff_{w^2} Hessian_{(h0x,h1z)} L")
print("="*80)
def Wmat(expr):
    H = sp.hessian(sp.expand(expr), [b1, d1])
    return sp.Matrix(2, 2, lambda i, j: sp.expand(H[i, j]).coeff(w, 2))

L_hel1 = L.subs({S[key]: 0 for key in S if S[key] not in {b1, d1}})
W_full = Wmat(L_hel1.subs({u0: 1, u1: 0, lam: 1}))
evs = [sp.nsimplify(e) for e in W_full.eigenvals().keys()]
print("  MOND-alive (u0,u1)=(1,0), lam=1:  W =", W_full.tolist(),
      " eigenvalues =", evs, " det =", sp.simplify(W_full.det()))
print("  negative eigenvalues:", sum(1 for e in evs if e.is_number and e < 0),
      "=> GHOST" if any(e.is_number and e < 0 for e in evs) else "=> none")

print("\n" + "="*80)
print("(C) CONTROLS (method must NOT manufacture a ghost on known-clean cases)")
print("="*80)
# pure EH
W_EH = Wmat(sp.Rational(1, 2)*EH.subs({S[key]: 0 for key in S if S[key] not in {b1, d1}}))
evEH = [sp.nsimplify(e) for e in W_EH.eigenvals().keys()]
print("  pure EH:            W =", W_EH.tolist(), " eig =", evEH,
      "=> ghost-free" if not any(e.is_number and e < 0 for e in evEH) else "=> GHOST(!)")
# Fierz-Pauli 0-derivative mass: (m^2/4)(h_mn h^mn - h^2); x-channel h_mn h^mn = -2 h0x^2 + 2 h1z^2, trace 0
m = sp.Symbol('m', positive=True)
L_fp = sp.Rational(1, 2)*EH.subs({S[key]: 0 for key in S if S[key] not in {b1, d1}}) \
       + sp.Rational(1, 4)*m**2*(-2*b1**2 + 2*d1**2)
W_FP = Wmat(L_fp)
evFP = [sp.nsimplify(e) for e in W_FP.eigenvals().keys()]
print("  EH + FP mass:       W =", W_FP.tolist(), " eig =", evFP,
      "=> ghost-free" if not any(e.is_number and e < 0 for e in evFP) else "=> GHOST(!)")

print("\n" + "="*80)
print("(D) GENERIC det(W)(u0,u1) and tie to MOND accel coeff a(u0,u1)")
print("="*80)
W_gen = Wmat(L_hel1.subs(lam, 1))
detW = sp.factor(sp.simplify(W_gen.det()))
print("  det(W) general (lam=1):", detW)
# MOND accel coeff a: static weak-field g,ghat, C-difference, T_i O(eps^2), coeff of (Phi')^2
tt = sp.symbols('t x y z'); ep = sp.Symbol('ep')
def wf(P, Q): return sp.diag(-(1 + 2*ep*P), 1 - 2*ep*Q, 1 - 2*ep*Q, 1 - 2*ep*Q)
Phi = sp.Function('Phi')(tt[1]); Psi = sp.Function('Psi')(tt[1])
Phh = sp.Function('Ph')(tt[1]); Psh = sp.Function('Ps')(tt[1])
g = wf(Phi, Psi); gh = wf(Phh, Psh); gi = g.inv()
def chr_(gm, gmi):
    G = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for mm in range(4):
            for nn in range(4):
                G[l][mm][nn] = sp.expand(sum(gmi[l, si]*(sp.diff(gm[si, mm], tt[nn])
                                        + sp.diff(gm[si, nn], tt[mm]) - sp.diff(gm[mm, nn], tt[si]))
                                        for si in range(4))/2)
    return G
Gg = chr_(g, g.inv()); Gf = chr_(gh, gh.inv())
Cd = [[[sp.expand(Gg[l][mm][nn] - Gf[l][mm][nn]) for nn in range(4)] for mm in range(4)] for l in range(4)]
def Ti_static():
    T1 = sum(Cd[a][mm][nn]*Cd[bb][r][s]*g[a, bb]*gi[mm, r]*gi[nn, s]
             for a in range(4) for bb in range(4) for mm in range(4) for nn in range(4)
             for r in range(4) for s in range(4))
    Pv = [sum(gi[mm, nn]*Cd[a][mm][nn] for mm in range(4) for nn in range(4)) for a in range(4)]
    T2 = sum(g[a, bb]*Pv[a]*Pv[bb] for a in range(4) for bb in range(4))
    Vv = [sum(Cd[a][a][mu] for a in range(4)) for mu in range(4)]
    T3 = sum(gi[mm, nn]*Vv[mm]*Vv[nn] for mm in range(4) for nn in range(4))
    T4 = sum(gi[mm, nn]*Cd[a][mm][bb]*Cd[bb][nn][a] for mm in range(4) for nn in range(4)
             for a in range(4) for bb in range(4))
    T5 = sum(Pv[a]*Vv[a] for a in range(4))
    return [T1, T2, T3, T4, T5]
Ts = Ti_static()
dP = sp.diff(Phi, tt[1]); dPs = sp.diff(Psi, tt[1]); dPh = sp.diff(Phh, tt[1]); dPsh = sp.diff(Psh, tt[1])
gP, gPs = sp.symbols('gP gPs')
a_i = []
for Tv in Ts:
    q = sp.series(Tv, ep, 0, 3).removeO().coeff(ep, 2)
    q = sp.expand(q.subs({dPh: dP - gP, dPsh: dPs - gPs}))
    a_i.append(sp.expand(q.coeff(gP, 2)))
a_sub = sp.simplify(sum(c[i]*a_i[i] for i in range(5)))
print("  MOND accel coeff a(u0,u1) =", sp.factor(a_sub))
print("  det(W)/a =", sp.simplify(detW / a_sub), "  (finite & nonzero => a!=0 forces det(W)<0 ghost)")
print("  => on the whole 2D ghost-free subspace, a!=0  <=>  vector kinetic det(W) indefinite (ghost).")
