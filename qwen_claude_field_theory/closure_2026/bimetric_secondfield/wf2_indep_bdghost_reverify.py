"""
INDEPENDENT re-verification (from scratch, NO import of committed scripts) of the
helicity-0 / Boulware-Deser ghost result on the ghost-free-tuned derivative-bimetric
subspace.

Relative-graviton perturbation dh_mn -> polarization eps_mn (plane wave).
Connection difference:
    C^l_mn = (1/2) eta^{ls} (k_m eps_sn + k_n eps_sm - k_s eps_mn)
Five quadratic invariants (match the committed convention):
    P^a  = eta^{mn} C^a_mn
    V_m  = C^a_am
    T1 = eta_ab eta^{mr} eta^{ns} C^a_mn C^b_rs
    T2 = eta_ab P^a P^b
    T3 = eta^{mn} V_m V_n
    T4 = eta^{mn} C^a_mb C^b_na
    T5 = P^a V_a
    Int = c1 T1 + c2 T2 + c3 T3 + c4 T4 + c5 T5
Ghost-free 2D subspace: (c1..c5) = (-u0, -u1/2, -u1/2, u0, u1).  Sum c_i = 0 identically.
MOND-alive (a!=0) directions: generic (u0,u1); concrete T4-T1 = (u0,u1)=(1,0).

GATE (a): Int on pure longitudinal eps_mn = k_m k_n pi  =  (Sum c_i)(k^2)^3 * (1/4) pi^2  -> 0.
GATE (b): full Stuckelberg eps_mn = k_m A_n + k_n A_m + k_m k_n pi ; build Hessian in
          (A0,A1,A2,A3,pi); is the pi row/col identically zero (=> pi NON-dynamical, no BD ghost)?
          Confirm across the MOND-alive family (symbolic u0,u1 AND explicit u0=1,u1=0 and u0=1,u1=1).
"""
import sympy as sp

# ---------- metric (mostly plus): eta_{mn} = eta^{mn} = diag(-1,1,1,1) ----------
eta = sp.diag(-1, 1, 1, 1)

def build_C(eps, k):
    """C^l_mn = (1/2) eta^{ls}(k_m eps_sn + k_n eps_sm - k_s eps_mn)."""
    C = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                s_sum = 0
                for s in range(4):
                    s_sum += eta[l, s]*(k[m]*eps[s, n] + k[n]*eps[s, m] - k[s]*eps[m, n])
                C[l][m][n] = sp.Rational(1, 2)*s_sum
    return C

def invariants(C):
    """Return (T1..T5)."""
    # P^a = eta^{mn} C^a_mn
    P = [sum(eta[m, n]*C[a][m][n] for m in range(4) for n in range(4)) for a in range(4)]
    # V_m = C^a_am
    V = [sum(C[a][a][m] for a in range(4)) for m in range(4)]
    # T1 = eta_ab eta^{mr} eta^{ns} C^a_mn C^b_rs
    T1 = 0
    for a in range(4):
        for b in range(4):
            for m in range(4):
                for n in range(4):
                    for r in range(4):
                        for s in range(4):
                            T1 += eta[a, b]*eta[m, r]*eta[n, s]*C[a][m][n]*C[b][r][s]
    # T2 = eta_ab P^a P^b
    T2 = sum(eta[a, b]*P[a]*P[b] for a in range(4) for b in range(4))
    # T3 = eta^{mn} V_m V_n
    T3 = sum(eta[m, n]*V[m]*V[n] for m in range(4) for n in range(4))
    # T4 = eta^{mn} C^a_mb C^b_na
    T4 = 0
    for m in range(4):
        for n in range(4):
            for a in range(4):
                for b in range(4):
                    T4 += eta[m, n]*C[a][m][b]*C[b][n][a]
    # T5 = P^a V_a
    T5 = sum(P[a]*V[a] for a in range(4))
    return T1, T2, T3, T4, T5

# ghost-free subspace coefficients
u0, u1 = sp.symbols('u0 u1', real=True)
def coeffs(U0, U1):
    return [-U0, -U1/sp.Integer(2), -U1/sp.Integer(2), U0, U1]

def Int_of(Ts, c):
    return sum(c[i]*Ts[i] for i in range(5))

print("="*80)
print("GATE (a): pure longitudinal eps_mn = k_m k_n pi")
print("="*80)
k = sp.symbols('k0 k1 k2 k3', real=True)
pi = sp.symbols('pi', real=True)
eps_long = sp.Matrix(4, 4, lambda i, j: k[i]*k[j]*pi)
C_long = build_C(eps_long, k)
Ts_long = [sp.expand(t) for t in invariants(C_long)]

# generic (untuned) c_i to expose the mechanism
c1, c2, c3, c4, c5 = sp.symbols('c1 c2 c3 c4 c5', real=True)
Int_generic = sp.expand(c1*Ts_long[0] + c2*Ts_long[1] + c3*Ts_long[2]
                        + c4*Ts_long[3] + c5*Ts_long[4])
k2 = sum(eta[i, j]*k[i]*k[j] for i in range(4) for j in range(4))  # k^2 = eta^{mn}k_m k_n
target = sp.Rational(1, 4)*(c1+c2+c3+c4+c5)*k2**3*pi**2
print("each T_i on longitudinal (should all equal (1/4)(k^2)^3 pi^2):")
for i, t in enumerate(Ts_long):
    print(f"   T{i+1} - (1/4)(k^2)^3 pi^2  simplify =",
          sp.simplify(t - sp.Rational(1,4)*k2**3*pi**2))
print("Int(generic c) - (1/4)(Sum c_i)(k^2)^3 pi^2  simplify =",
      sp.simplify(Int_generic - target))

# now on the ghost-free subspace
c_sub = coeffs(u0, u1)
Int_long_sub = sp.simplify(Int_of(Ts_long, c_sub))
print("Sum c_i on ghost-free subspace =", sp.simplify(sum(c_sub)))
print("Int_longitudinal on ghost-free subspace (symbolic u0,u1) =", Int_long_sub)

print()
print("="*80)
print("GATE (b): full Stuckelberg eps_mn = k_m A_n + k_n A_m + k_m k_n pi")
print("          frame k^mu = (w, 0, 0, kap)")
print("="*80)
w, kap = sp.symbols('w kap', real=True)
kk = [w, 0, 0, kap]               # k_m (lower). k^2 = -w^2 + kap^2
A = list(sp.symbols('A0 A1 A2 A3', real=True))
Pi = sp.symbols('Pi', real=True)
eps_st = sp.Matrix(4, 4, lambda i, j: kk[i]*A[j] + kk[j]*A[i] + kk[i]*kk[j]*Pi)
C_st = build_C(eps_st, kk)
Ts_st = invariants(C_st)

fields = A + [Pi]      # order: A0,A1,A2,A3,Pi
labels = ['A0', 'A1', 'A2', 'A3', 'Pi']

def hessian_of(expr):
    expr = sp.expand(expr)
    H = sp.zeros(5, 5)
    for i in range(5):
        for j in range(5):
            H[i, j] = sp.expand(sp.diff(expr, fields[i], fields[j]))
    return H

def kinetic_EH(eps, k):
    """(T4 - T5) evaluated on eps -- linearized Einstein-Hilbert relative graviton."""
    C = build_C(eps, k)
    T1, T2, T3, T4, T5 = invariants(C)
    return sp.expand(T4 - T5)

# sanity: linearized-EH kinetic term is a pure gauge => vanishes on Stuckelberg polarization
EH_st = kinetic_EH(eps_st, kk)
print("linearized-EH (T4-T5) on the pure-Stuckelberg polarization =",
      sp.simplify(EH_st), " (expect 0: EH is diff-invariant, contributes nothing to Stuckelberg sector)")

# Int on ghost-free subspace, symbolic u0,u1
Int_st_sub = Int_of(Ts_st, coeffs(u0, u1))
H = hessian_of(Int_st_sub)
print()
print("Hessian of Int in (A0,A1,A2,A3,Pi), ghost-free subspace, symbolic (u0,u1):")
for i in range(5):
    row = [sp.factor(H[i, j]) for j in range(5)]
    print(f"  {labels[i]:>2}: ", row)

pi_row = [sp.simplify(H[4, j]) for j in range(5)]
pi_col = [sp.simplify(H[j, 4]) for j in range(5)]
print()
print("Pi ROW  (H[Pi,*]) =", pi_row)
print("Pi COL  (H[*,Pi]) =", pi_col)
pi_decoupled = all(e == 0 for e in pi_row) and all(e == 0 for e in pi_col)
print("=> Pi row & col identically zero for symbolic (u0,u1)?", pi_decoupled)
# does Pi appear ANYWHERE in Int at all?
print("Int depends on Pi at all? (diff wrt Pi) =", sp.simplify(sp.diff(sp.expand(Int_st_sub), Pi)))

# (A0,A3) longitudinal 2x2 block
idx = [0, 3]
block = sp.Matrix(2, 2, lambda a, b: sp.factor(H[idx[a], idx[b]]))
print()
print("(A0,A3) 2x2 longitudinal block (factored):")
sp.pprint(block)
print("  det of (A0,A3) block =", sp.factor(block.det()), " (rank<=1 iff det=0)")
print("  rank of (A0,A3) block =", block.rank())

# explicit MOND-alive test points
print()
print("-"*80)
print("Explicit MOND-alive directions (confirm a!=0 => Pi still non-dynamical):")
for (U0, U1, name) in [(1, 0, 'T4-T1  (u0=1,u1=0)'),
                       (1, 1, 'u0=1,u1=1'),
                       (2, sp.Rational(-1), 'u0=2,u1=-1'),
                       (sp.Rational(3,2), sp.Rational(1,2), 'u0=3/2,u1=1/2')]:
    Hn = hessian_of(Int_of(Ts_st, coeffs(sp.Integer(U0), sp.Integer(U1) if not isinstance(U1, sp.Rational) else U1)))
    prow = [sp.simplify(Hn[4, j]) for j in range(5)]
    pcol = [sp.simplify(Hn[j, 4]) for j in range(5)]
    dec = all(e == 0 for e in prow) and all(e == 0 for e in pcol)
    # MOND-alive amplitude proxy: (A0,A3) block prefactor 2u0+u1
    amp = 2*sp.Integer(U0) + (U1 if isinstance(U1, sp.Rational) else sp.Integer(U1))
    print(f"  {name:22s}: 2u0+u1={amp}, Pi row/col zero? {dec}, Pi row={prow}")

print()
print("="*80)
print("VERDICT LOGIC")
print("="*80)
print("(a) longitudinal Int = (1/4)(Sum c_i)(k^2)^3 pi^2, Sum c_i=0 on subspace => 0. ",
      "MATCH:", Int_long_sub == 0)
print("(b) Pi non-dynamical (row/col=0) for generic symbolic (u0,u1):", pi_decoupled)
print("    a!=0 (MOND-alive) does NOT switch on the Pi kinetic term.")
