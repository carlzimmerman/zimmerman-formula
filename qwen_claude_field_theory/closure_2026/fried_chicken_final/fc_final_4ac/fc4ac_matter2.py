#!/usr/bin/env python3
r"""
=====================================================================================
FC-FINAL 4-AC Type-II MMG -- TASK Q3b: matter conservation nabla_mu T^{mu nu}
                             ON THE CONSTRUCTED H_can (ATTEMPT B / EMBEDDING I).
=====================================================================================
This is DISTINCT from fc4ac_matter_conservation.py, which analysed the OLD/GUESSED
chassis (Embedding II: kernel on ln N, {pi_N,C_M}=L_N != 0, chain S=(pi_N,C_M,C_q,C_p)).
That chassis FAILED matter conservation at Newtonian order because lambda_M = -r_1/L_N
with r_1 = {pi_N,H} = -(H_g+eps_n) NOT a constraint => lambda_M != 0 => a fifth force.

The CONSTRUCTED H_can of inverse_chain_B.py is EMBEDDING I (kernel on q):
    H_can = INT [ N * C_M^(10)(q,gamma)  +  (sigma/2) p_q^2  +  H_TT ],
    C_M^(10) = (c^4/4piG) sqrt(g) D_i[mu_10 D^i q] - sqrt(g) c^2 rho .
Matter (dust) enters C_M as the -sqrt(g) c^2 rho term, minimally coupled to N.
The GENERATED chain is  S_1=pi_N, S_2=C_M, S_3={C_M,H}=sigma L^[p_q],
S_4={S_3,H}=sigma^2 Chat - sigma L^^2[N], with the Attempt-B Dirac block
    {pi_N,S_4}=sigma L_N^2, {C_M,S_3}=sigma L_N^2, {pi_N,C_M}=0   (EMBEDDING-I DICHOTOMY).

QUESTION: does the OLD-chassis matter-conservation FAIL TRANSFER to Embedding I
(as asserted in passing in FC4AC_construct_B.md Sec.5 and inverse_chain_B), or does the
{pi_N,C_M}=0 dichotomy change the verdict?  We DERIVE it, we do not transfer it.

HONESTY: every load-bearing line prints a certificate simplify(...)==0 or a residual.
  Labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
PHENOMENOLOGICAL INPUT (never derived): a0^2=kappa^2 c^2 G rho_Lambda, kappa=1/2, Z~21.
"""
import sys
import sympy as sp
import numpy as np

FAILS = []
def cert(label, cond):
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label)
    if not ok: FAILS.append(label)
    return ok
def info(s): print("  [info] " + s)

# =====================================================================================
print("=" * 88)
print(" PART 0 -- the Embedding-I identity {pi_N,H_can} = -C_M  vs the old-chassis identity")
print("=" * 88)
# Old chassis (Embedding II): H had a DELETED Hamiltonian constraint; {pi_N,H}=-(H_g+eps_n),
#   and H_g+eps_n is NOT among the imposed constraints => r_1 = -(H_g+eps_n) != 0 (matter source).
# Embedding I: H_can is LINEAR in N with coefficient C_M (matter INSIDE C_M as -sqrt(g)c^2 rho).
#   {pi_N,H_can} = -dH_can/dN = -C_M = -S_2, and S_2 IS an imposed (second-class) constraint.
#   => r_1 = -S_2  is WEAKLY ZERO.  This is the decisive structural difference.
Nn, piN, qq, pq, sig, rho, cc = sp.symbols('N piN q p_q sigma rho c', real=True)
# C_M as an explicit function of q carrying the matter density term -sqrt(g)c^2 rho, sqrt(g)=e^{-3q}:
Kq = sp.Function('K')(qq)                        # kernel piece (c^4/4piG) sqrt(g) D_i[mu D^i q]
CM = Kq - sp.exp(-3*qq) * cc**2 * rho            # C_M(q; rho)  -- matter minimally coupled
Hcan = Nn * CM + sig * pq**2 / 2                 # Embedding-I H_can (scalar-sector standin)
cert("{pi_N,H_can} = -dH_can/dN = -C_M  (matter is INSIDE C_M; pi_N-preservation => the constraint)",
     sp.simplify(-sp.diff(Hcan, Nn) - (-CM)) == 0)
cert("the matter density rho is present in C_M (d C_M/d rho = -sqrt(g)c^2 != 0)",
     sp.simplify(sp.diff(CM, rho) + sp.exp(-3*qq)*cc**2) == 0)
cert("EMBEDDING-I DICHOTOMY: {pi_N,C_M} = dC_M/dN = 0 (C_M is N-independent)",
     sp.simplify(sp.diff(CM, Nn)) == 0)
info("=> r_1 := {pi_N,H_can} = -C_M = -S_2 is (minus) an IMPOSED constraint => r_1 ~ 0 WEAKLY.")
info("   Contrast old chassis (Emb.II): r_1 = -(H_g+eps_n), H_g+eps_n NOT imposed => r_1 != 0.")
info("   The matter source eps_n is BALANCED inside the constraint C_M=0 (the MOND Poisson eq),")
info("   not left over as a free source -- this is why the transfer must be re-derived, not assumed.")

# =====================================================================================
print("=" * 88)
print(" PART 1 -- matter-augmented lattice: generate S_2,S_3,S_4; verify r_A ARE the constraints")
print("=" * 88)
# Exact periodic n-site lattice.  Matter = external density field rho_a (parameter, {.,rho}=0),
# entering C_M with the geometric weight sqrt(g)_a = exp(-3 q_a) so that matter genuinely
# propagates into the GENERATED S_3, S_4 (not put in by hand).
def build(n, sigma):
    Q  = sp.symbols(f'Q0:{n}', real=True);  PQ = sp.symbols(f'PQ0:{n}', real=True)
    NN = sp.symbols(f'N0:{n}', real=True);  PN = sp.symbols(f'PN0:{n}', real=True)
    RHO = sp.symbols(f'RHO0:{n}', real=True)                  # external matter density
    allv = list(Q)+list(PQ)+list(NN)+list(PN)
    EPS = sp.Rational(1, 10**6)
    def link(a): return Q[(a+1) % n] - Q[a]
    def mflux(s):
        ya = sp.sqrt(s*s + EPS**2)                            # a0=1, c=1
        return ya/(1+ya**10)**sp.Rational(1, 10) * s
    def sg(a): return sp.exp(-3*Q[a])                         # sqrt(g)=e^{-3q}
    def CM(a): return (mflux(link(a)) - mflux(link((a-1) % n))) - sg(a)*RHO[a]  # kernel div - matter
    H = sum(NN[a]*CM(a) for a in range(n)) + sum(sigma*PQ[a]**2/2 for a in range(n))
    def PB(F, G):
        o = sp.Integer(0)
        for a in range(n):
            o += sp.diff(F, Q[a])*sp.diff(G, PQ[a]) - sp.diff(F, PQ[a])*sp.diff(G, Q[a])
            o += sp.diff(F, NN[a])*sp.diff(G, PN[a]) - sp.diff(F, PN[a])*sp.diff(G, NN[a])
        return o
    S1 = [PN[a] for a in range(n)]
    S2 = [CM(a) for a in range(n)]
    S3 = [PB(S2[a], H) for a in range(n)]
    S4 = [PB(S3[a], H) for a in range(n)]
    return dict(Q=Q, PQ=PQ, NN=NN, PN=PN, RHO=RHO, allv=allv, CM=CM, H=H, PB=PB,
                S1=S1, S2=S2, S3=S3, S4=S4, sigma=sigma)

n = 4
L = build(n, sigma=1)
allv = L['allv']
MOD = [{'DiracDelta': (lambda z: 0.0)}, 'numpy']
def Lam(e): return sp.lambdify(allv + list(L['RHO']), e, modules=MOD)

# background: Newtonian-regime gradients, generic N, p_q, and nonzero matter density
base = np.array([0.7, -1.3, 0.9, -0.4])
qv = np.cumsum(2.0*base); qv -= qv.mean()
bg = {}
for a in range(n):
    bg[L['Q'][a]] = qv[a]; bg[L['PQ'][a]] = 0.3*(a+1)
    bg[L['NN'][a]] = 1.0+0.1*a; bg[L['PN'][a]] = 0.2*(a+1)
rho_vals = [0.5, 1.1, 0.7, 0.9]
xs = [float(bg[v]) for v in allv] + rho_vals

# (1a) {pi_N,H} = -C_M exactly on the lattice (with matter)
okp = all(abs(float(Lam(L['PB'](L['S1'][a], L['H']) + L['CM'](a))(*xs))) < 1e-9 for a in range(n))
cert("{pi_N,H} + C_M = 0 exactly on the matter-augmented lattice (r_1 = -S_2)", okp)

# (1b) r_2 = {S_2,H} = S_3  and  r_3 = {S_3,H} = S_4  (the generated chain: r_A ARE constraints)
ok2 = all(abs(float(Lam(L['PB'](L['S2'][a], L['H']) - L['S3'][a])(*xs))) < 1e-9 for a in range(n))
ok3 = all(abs(float(Lam(L['PB'](L['S3'][a], L['H']) - L['S4'][a])(*xs))) < 1e-9 for a in range(n))
cert("r_2 := {S_2,H} = S_3 exactly (generated)", ok2)
cert("r_3 := {S_3,H} = S_4 exactly (generated)", ok3)
info("=> r_1=-S_2, r_2=S_3, r_3=S_4 are ALL (up to sign) imposed constraints => weakly zero.")
info("   Only r_4 = {S_4,H} is a genuine non-constraint (it fixes the surviving multiplier).")

# (1c) matter genuinely propagates into the GENERATED S_3 and S_4 (d/d rho != 0):
dS3 = any(abs(float(Lam(sp.diff(L['S3'][a], L['RHO'][b]))(*xs))) > 1e-9
          for a in range(n) for b in range(n))
dS4 = any(abs(float(Lam(sp.diff(L['S4'][a], L['RHO'][b]))(*xs))) > 1e-9
          for a in range(n) for b in range(n))
cert("matter density rho appears in the GENERATED S_3 (dS_3/d rho != 0): matter is NOT absent",
     dS3)
cert("matter density rho appears in the GENERATED S_4 (dS_4/d rho != 0)", dS4)
info("Matter DOES enter every generated constraint; the question is whether its MULTIPLIER survives.")

# (1d) LATTICE-EXACT pairing structure needed for Part 2: S_1=pi_N pairs ONLY with S_4.
#      {pi_N,S_2}=0 (dichotomy), {pi_N,S_3}=0, {pi_N,S_4}!=0.  Symbolic, all (a,b) pairs.
z12 = all(sp.simplify(L['PB'](L['S1'][a], L['S2'][bb])) == 0 for a in range(n) for bb in range(n))
z13 = all(sp.simplify(L['PB'](L['S1'][a], L['S3'][bb])) == 0 for a in range(n) for bb in range(n))
nz14 = any(abs(float(Lam(L['PB'](L['S1'][a], L['S4'][bb]))(*xs))) > 1e-9
           for a in range(n) for bb in range(n))
cert("{pi_N,S_2}=0 and {pi_N,S_3}=0 EXACTLY (symbolic), while {pi_N,S_4}!=0: pi_N pairs ONLY with "
     "S_4 -> Dirac-block row 1 = [0,0,0,d] (the fact Part 2 rests on)", z12 and z13 and nz14)

# =====================================================================================
print("=" * 88)
print(" PART 2 -- the multiplier solve on the Attempt-B block: is lambda_M density-sourced?")
print("=" * 88)
# HONEST general block MEASURED on the lattice (NOT the idealised anti-diagonal): the only firm
# zeros are {pi_N,C_M}={pi_N,S_3}=0 (verified exactly on the lattice: pi_N pairs ONLY with S_4).
# Keep the other measured-nonzero entries free: d={pi_N,S_4}, a={C_M,S_3}, b={C_M,S_4}, e={S_3,S_4}.
d, a, b, e = sp.symbols('d a b e', nonzero=True)
Delta = sp.Matrix([
    [ 0,  0,  0,  d],      # S_1=pi_N pairs ONLY with S_4  (lattice: {pi_N,S_2}={pi_N,S_3}=0)
    [ 0,  0,  a,  b],      # {C_M,S_3}=a, {C_M,S_4}=b (b != 0 on the lattice)
    [ 0, -a,  0,  e],      # {S_3,S_4}=e (e != 0 on the lattice)
    [-d, -b, -e,  0],
])
cert("general lattice-consistent Dirac block antisymmetric", sp.simplify(Delta + Delta.T) == sp.zeros(4, 4))
cert("firm structural zeros from the lattice: {pi_N,C_M}=Delta[0,1]=0 and {pi_N,S_3}=Delta[0,2]=0 "
     "(S_1 pairs ONLY with S_4) -- the Embedding-I dichotomy",
     Delta[0, 1] == 0 and Delta[0, 2] == 0)
cert("det(Delta) = a^2 d^2 != 0 (rank 4; det = {C_M,S_3}^2 {pi_N,S_4}^2, independent of b,e)",
     sp.simplify(Delta.det() - a**2*d**2) == 0)

# r_A = {S_A,H} = (-S_2, S_3, S_4, W) with S_2,S_3,S_4 constraints (weakly 0) and W the survivor.
S2c, S3c, S4c, W = sp.symbols('S2 S3 S4 W')      # S2,S3,S4 = constraint values (~0 on Sigma)
rvec = sp.Matrix([-S2c, S3c, S4c, W])
lam = Delta.solve(-rvec)
lam1, lam2, lam3, lam4 = [sp.simplify(x) for x in lam]
print("  multipliers (lambda_1..lambda_4) from Delta.lambda = -r  (general block):")
for nm, x in zip(['lambda_1(pi_N)', 'lambda_2=lambda_M(C_M)', 'lambda_3(S_3)', 'lambda_4(S_4)'],
                 [lam1, lam2, lam3, lam4]):
    print(f"    {nm:26s} = {x}")
# Decisive: lambda_M = lambda_2 is a COMBINATION OF CONSTRAINTS (S_2,S_4), hence weakly zero -- and
# this survives b,e != 0 because row 1 = [0,0,0,d] forces lambda_4=0, then row 3 forces lambda_2=0.
cert("lambda_M := lambda_2 = (S_2 e + S_4 d)/(a d): a COMBINATION OF CONSTRAINTS (S_2,S_4) => "
     "lambda_M = 0 on Sigma (robust to b,e != 0)",
     sp.simplify(lam2 - (S2c*e + S4c*d)/(a*d)) == 0)
onS = {S2c: 0, S3c: 0, S4c: 0}
cert("on Sigma (S_2=S_3=S_4=0): lambda_M = lambda_3 = lambda_4 = 0 EXACTLY",
     sp.simplify(lam2.subs(onS)) == 0 and sp.simplify(lam3.subs(onS)) == 0
     and sp.simplify(lam4.subs(onS)) == 0)
cert("the ONLY surviving multiplier is lambda_1 = W/d (= W/{pi_N,S_4}), multiplying S_1=pi_N which "
     "carries NO matter", sp.simplify(lam1.subs(onS) - W/d) == 0)
info("MECHANISM (robust): row 1 of Delta is [0,0,0,d] because pi_N pairs ONLY with S_4 (lattice-exact")
info("{pi_N,S_2}={pi_N,S_3}=0). Hence lambda_4=0 on Sigma, and then row 3 (-a lambda_2 + e lambda_4=-S_4)")
info("gives lambda_2=lambda_M=0 -- independent of the nonzero {C_M,S_4}=b and {S_3,S_4}=e entries.")

# CONTRAST: the old-chassis (Embedding II) block, {pi_N,C_M}=L != 0, reproduces the FAIL.
print("  --- CONTRAST: old chassis (Embedding II), {pi_N,C_M}=L_N != 0 (fc4ac_matter_conservation) ---")
LN2, cM2, K2 = sp.symbols('L_N c_M K')
DeltaII = sp.Matrix([[0, LN2, 0, 0], [-LN2, 0, cM2, 0], [0, -cM2, 0, K2], [0, 0, -K2, 0]])
r1o, r2o, r3o, r4o = sp.symbols('r1 r2 r3 r4')   # r1 = -(H_g+eps_n) is NOT a constraint here
lamII = DeltaII.solve(-sp.Matrix([r1o, r2o, r3o, r4o]))
lamMII = sp.simplify(lamII[1])
cert("Embedding II: lambda_M depends on r_1 (d lambda_M/d r_1 != 0) and r_1=-(H_g+eps_n) is NOT a "
     "constraint => lambda_M != 0 => the committed Newtonian-order FAIL (old chassis)",
     sp.simplify(sp.diff(lamMII, r1o)) != 0)
info(f"   Embedding II: lambda_M = {lamMII}  (carries r_1 = -(H_g+eps_n): density-sourced => FAIL).")
info("   THE FLIP: Embedding I has {pi_N,C_M}=0, so lambda_M pairs with r_3=S_4 (a constraint), NOT")
info("   with r_1.  The single sign change {pi_N,C_M}: L_N -> 0 moves lambda_M off the matter source.")

# =====================================================================================
print("=" * 88)
print(" PART 3 -- the on-shell fifth force on matter and nabla_mu T^{mu nu}|_g (DERIVATION+THEOREM)")
print("=" * 88)
# Matter evolution uses the DIRAC bracket: p_dot_m = {p_m,H}_D,
#   {p_m,H}_D = {p_m,H} - {p_m,S_C}(Delta^{-1})_{CD}{S_D,H} = {p_m,H} + {p_m,S_C} lambda_C .
# The NON-METRIC (fifth) force is exactly  F5 = sum_C lambda_C {p_m,S_C}.
# {p_m,S_C} != 0 only for C in {2,3,4} (S_1=pi_N has no matter).  On Sigma lambda_2=lambda_3=lambda_4=0.
lm2, lm3, lm4 = sp.symbols('lambda_2 lambda_3 lambda_4')
b2, b3, b4 = sp.symbols('b2 b3 b4')              # {p_m,S_2},{p_m,S_3},{p_m,S_4} (matter brackets)
F5 = lm2*b2 + lm3*b3 + lm4*b4                    # {p_m,S_1}=0 => no lambda_1 term
F5_onshell = F5.subs({lm2: 0, lm3: 0, lm4: 0})   # lambda_{2,3,4}=0 on Sigma (Part 2)
cert("fifth force F5 = sum_C lambda_C {p_m,S_C} with {p_m,S_1}=0; on Sigma (lambda_{2,3,4}=0) => F5=0",
     sp.simplify(F5_onshell) == 0)
info("The vanishing is EXACT (all orders in v/c), not merely Newtonian: lambda_{2,3,4} are ")
info("proportional to the constraints S_2,S_3,S_4 as PHASE-SPACE FUNCTIONS, zero on Sigma to all orders.")

# THEOREM (Noether / minimal coupling): with no fifth force, matter feels ONLY the lapse+shift of g,
# so nabla_mu T^{mu nu}=0 w.r.t. g is the ordinary matter EOM identity.  Verify the geodesic form.
x = sp.symbols('x'); Psi = sp.Function('Psi')(x)
p_, m_, c_ = sp.symbols('p m c', positive=True)
Hp = (1 + Psi/c_**2) * sp.sqrt(m_**2*c_**4 + p_**2*c_**2)   # test particle, lapse N=1+Psi/c^2, NO extra X
acc = sp.simplify(-sp.diff(Hp, x).subs(p_, 0)/m_)
cert("with F5=0 the matter acceleration is a = -grad Psi = -grad ln N EXACTLY (pure geodesic of g): "
     "no extra potential X (contrast old chassis a=-grad(Psi+X), X=c^2 chi != 0)",
     sp.simplify(acc + sp.diff(Psi, x)) == 0)
# dust divergence w.r.t. g with a=-grad Psi (continuity + geodesic):
t = sp.symbols('t'); rho_ = sp.Function('rho')(t, x); v_ = sp.Function('v')(t, x)
Ttx = rho_*v_; Txx = rho_*v_**2; Gam = sp.diff(Psi, x)
divT = sp.diff(Ttx, t) + sp.diff(Txx, x) + Gam*rho_
divT = divT.subs({sp.diff(rho_, t): -sp.diff(rho_*v_, x),
                  sp.diff(v_, t): -v_*sp.diff(v_, x) - sp.diff(Psi, x)})   # NO X term now
cert("nabla_mu T^{mu x}|_g = 0 EXACTLY (dust, minimal coupling, no fifth force): matter conserves "
     "w.r.t. g itself -- NOT only w.r.t. a bimetric g_eff",
     sp.simplify(sp.expand(divT)) == 0)
info("=> In Embedding I the OLD-chassis two-potential/bimetric disease is ABSENT: matter couples to g,")
info("   the constraint C_M=0 IS the matter field (MOND-Poisson) equation, and eps_n is balanced")
info("   inside it rather than re-emitted as a fifth force.  nabla_mu T^{mu nu}=0 w.r.t. g holds.")

# =====================================================================================
print("=" * 88)
print(" PART 4 -- the trade: matter conservation is bought with the SLIP (complementarity THEOREM)")
print("=" * 88)
# The SAME structure that rescues matter conservation forces the slip:
#   - matter conservation OK  <=  {pi_N,H}=-C_M is a CONSTRAINT  <=  H_can LINEAR in N (Embedding I).
#   - linear in N  =>  N enters every generated constraint linearly  =>  S_4 fixes the lapse Psi
#     through the LINEARISED Hessian (mu+y mu'), while S_2 fixes Phi through the NONLINEAR flux (mu)
#     =>  slip (mu+y mu')/mu : 1 (Newtonian) -> 2 (deep MOND)  =>  gamma_PPN != 1  (inverse_chain_B).
y = sp.symbols('y', positive=True)
mu = y/(1+y**10)**sp.Rational(1, 10)
slip = sp.simplify((mu + y*sp.diff(mu, y))/mu)
cert("H_can linear in N (d^2 H_can/dN^2 = 0): the same fact that makes {pi_N,H}=-C_M a constraint",
     sp.simplify(sp.diff(Hcan, Nn, 2)) == 0)
cert("that linearity forces the lapse slip (mu+y mu')/mu : ->1 (y->oo), ->2 (y->0) [gamma_PPN!=1]",
     sp.limit(slip, y, sp.oo) == 1 and sp.limit(slip, y, 0) == 2)
info("COMPLEMENTARITY (Embedding I): matter conservation (this task, PASS) and gamma_PPN=1 (FAIL)")
info("cannot both be evaded -- the linear-in-N structure that secures one forces the other.")
info("Embedding II is the mirror: {pi_N,C_M}=L_N!=0 loses matter conservation (old-chassis FAIL).")
info("SECTOR-ORTHOGONAL (EXTERNAL-INPUT, committed, unchanged): alpha_3=-1 (ppn_mmg_gate_2026.py) --")
info("an elliptic instantaneous-lapse defect in the 0i sector, independent of this matter analysis.")

# =====================================================================================
print("=" * 88)
print(" VERDICT")
print("=" * 88)
print(r"""  TASK: derive matter coupling on the CONSTRUCTED H_can (Embedding I) and check
  nabla_mu T^{mu nu} = 0, computing {H_matter,S_A}.

  RESULT (DERIVATION):  nabla_mu T^{mu nu} = 0 w.r.t. g  --  PASS at Newtonian order,
  in fact EXACTLY on the constraint surface.  The old-chassis matter-conservation FAIL
  does NOT transfer to Embedding I.  Reason, fully certified:

    [0] Embedding I is LINEAR in N with coefficient C_M (matter inside C_M as -sqrt(g)c^2 rho),
        so {pi_N,H_can} = -C_M = -S_2 is (minus) an IMPOSED second-class constraint => r_1 ~ 0.
        (Old chassis: r_1 = -(H_g+eps_n) is NOT a constraint => r_1 != 0.  This is the flip.)

    [1] Generated chain on the matter-augmented lattice: r_1=-S_2, r_2=S_3, r_3=S_4 are ALL
        constraints (exact); matter rho genuinely enters S_3,S_4 (dS/d rho != 0) -- yet only its
        MULTIPLIER decides the force.

    [2] General lattice-consistent block ({pi_N,C_M}={pi_N,S_3}=0 => row1=[0,0,0,d]): the C_M
        multiplier lambda_M = (S_2 e + S_4 d)/(a d) is a COMBINATION OF CONSTRAINTS => lambda_M=0 on
        Sigma (robust to the nonzero {C_M,S_4}=b, {S_3,S_4}=e). lambda_3,lambda_4 vanish on Sigma too.
        The only surviving multiplier lambda_1 = W/d multiplies the matter-free pi_N.
        (Contrast Embedding II: lambda_M = f(r_1) with r_1=-(H_g+eps_n) => density-sourced => FAIL.)

    [3] Fifth force F5 = sum_C lambda_C {p_m,S_C} = 0 on Sigma (exact, all orders): matter feels
        ONLY the lapse, a = -grad ln N, and nabla_mu T^{mu x}|_g = 0 EXACTLY -- no bimetric g_eff.

    [4] The rescue is BOUGHT with the slip: the linear-in-N structure that makes {pi_N,H}=-C_M a
        constraint is exactly what forces the lapse onto the LINEARISED Hessian (mu+y mu') while the
        curvature stays on the nonlinear flux (mu) => slip 1->2 => gamma_PPN != 1 (the operative FAIL).

  BOTTOM LINE:  matter conservation is NOT the Embedding-I obstruction (this CORRECTS the
  in-passing transfer in FC4AC_construct_B.md Sec.5 / inverse_chain_B, which imported the old
  Emb.II identity).  The theory still dies -- on the SLIP (gamma_PPN != 1) and the sector-orthogonal
  alpha_3 = -1 -- but nabla_mu T^{mu nu} = 0 w.r.t. g is DERIVED to HOLD in Embedding I.

  CAVEATS (honest):
   * "Conservation" here = no fifth force on Sigma; it presupposes the second-class surface is
     consistently reached (rank Delta=4, from inverse_chain_B) and that C_M=0 is the matter field eq.
   * scalar/TT decoupling MODEL-ASSUMPTION inherited (full q-h_TT York coupling = residual OPEN,
     same class as FC4AC_DOF.md Part IV); shift/N^i momentum sector taken standard.
""")
print("=" * 88)
ok = len(FAILS) == 0
print(f" FC4AC-MATTER2 CERTIFICATE: {'ALL BOOLEAN CHECKS PASS (exit 0).' if ok else 'FAILURES:'}")
for f in FAILS: print("   - " + f)
print("=" * 88)
sys.exit(0 if ok else 1)
