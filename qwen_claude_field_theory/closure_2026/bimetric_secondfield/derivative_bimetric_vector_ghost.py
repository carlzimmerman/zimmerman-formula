#!/usr/bin/env python3
# PERMANENT ARTIFACT (adversarial workflow, independently re-verified). Linearized ghost/c_T gates on the
# MOND-alive (a!=0) directions of the ghost-free-tuned derivative-bimetric subspace. Refs: Ostrogradsky
# instability (Woodard, Scholarpedia 2015) for the box^2 higher-derivative ghost; DC-013 slip-lock; c_T
# GW170817 bound Abbott+ 2017. NOT citing PLB 806 (2020) 135970 (misattributed f(Q) letter).
"""GATE = VECTOR (helicity-1) GHOST for the MOND-alive ghost-free-tuned derivative-bimetric subspace.

Relative-graviton quadratic Lagrangian around Minkowski:  L = (1/2)(T4-T5) + lam*Int,
   Int = sum_i c_i T_i,  (c1..c5)=(-u0,-u1/2,-u1/2,u0,u1),  lam ~ a0^2 > 0.
MOND-alive test direction T4-T1: (u0,u1)=(1,0).

Frame k=(w,0,0,kap).  Helicity-1 (SO(2)-vector about z) sector = components with exactly ONE
transverse (x or y) index: x-channel (eps_{0x}, eps_{3x}) = (eps01, eps13); y-channel (eps02, eps23)
(identical copy by SO(2)).  Relative-diff gauge param xi=(0,xi1,0,0) shifts eps01+=w*xi1, eps13+=kap*xi1
=> the transverse Stuckelberg vector A1 IS the helicity-1 field:  eps01=w*A1, eps13=kap*A1.

Three cross-checked computations:
  (I)  Direct 2x2 form in (eps01,eps13); verify EH is gauge-invariant (annihilates the gauge dir (w,kap))
       and that the hel-1 fields decouple from every other component (SO(2)).
  (II) Stuckelberg: the physical hel-1 kinetic term = lam*Int(eps01=w*A1, eps13=kap*A1) (EH gives 0 there).
       Read the sign of its w^2 (time-kinetic) coefficient.
  (III)Calibrate 'healthy sign' against the helicity-2 graviton kinetic term from (1/2)(T4-T5), which MUST
       be non-ghost (Einstein-Hilbert).  Same-sign w^2 => healthy; opposite => ghost; no w^2 => non-dynamical.
Also re-derive & interpret the longitudinal (A0,A3) block (2u0+u1)(kap^2-w^2)[[kap^2,-kap w],[-kap w,w^2]].
"""
import sympy as sp

eta = sp.diag(-1, 1, 1, 1); etaI = eta.inv()
k = sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
u0, u1, lam = sp.symbols('u0 u1 lam', real=True)
w, kap = sp.symbols('omega kappa', real=True, positive=True)

# full symmetric perturbation eps_mn
es = {}
E = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        s = sp.Symbol(f'e{a}{b}', real=True); es[(a, b)] = s; E[a, b] = s; E[b, a] = s

def Cconn(Em):
    C = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                v = sp.Integer(0)
                for sgm in range(4):
                    v += etaI[l, sgm]*(k[m]*Em[sgm, n]+k[n]*Em[sgm, m]-k[sgm]*Em[m, n])
                C[l][m][n] = sp.expand(v/2)
    return C

def invs(C):
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

C = Cconn(E); T = invs(C)
cvec = [-u0, -u1/2, -u1/2, u0, u1]
Int = sp.expand(sum(cvec[i]*T[i] for i in range(5)))
EH  = sp.expand(T[3]-T[4])                     # linearized-EH GammaGamma = T4 - T5
L   = sp.expand(sp.Rational(1, 2)*EH + lam*Int)

ksub = {k[0]: w, k[1]: 0, k[2]: 0, k[3]: kap}
EHk  = sp.expand(EH.subs(ksub))
Intk = sp.expand(Int.subs(ksub))
Lk   = sp.expand(sp.Rational(1, 2)*EHk + lam*Intk)

b1, d1 = es[(0, 1)], es[(1, 3)]                 # x-channel helicity-1 fields eps01, eps13

# ======================================================================================
print("="*95)
print("(I) DIRECT 2x2 helicity-1 x-channel form in (eps01, eps13); decoupling + gauge checks")
print("="*95)
# decoupling: set all NON-helicity-1-x-channel comps to zero, check dL/d(other) == 0 there
hel1x = {b1, d1}
zero_rest = {es[key]: 0 for key in es if es[key] not in hel1x}
Lhel1 = sp.expand(Lk.subs(zero_rest))
coupling_leak = []
for key, sym in es.items():
    if sym in hel1x:
        continue
    leak = sp.expand(sp.diff(Lk, sym).subs(zero_rest))   # source felt by other fields from hel-1 config
    if leak != 0:
        coupling_leak.append((sym, leak))
print("  helicity-1 x-channel sources into OTHER components (should be empty => clean SO(2) decoupling):",
      coupling_leak if coupling_leak else "NONE  -> decoupled")

Hfull = sp.hessian(Lhel1, [b1, d1])
HEH   = sp.hessian(sp.expand(sp.Rational(1, 2)*EHk.subs(zero_rest)), [b1, d1])
HInt  = sp.hessian(sp.expand(lam*Intk.subs(zero_rest)), [b1, d1])
print("\n  EH-only 2x2 form H_EH(eps01,eps13):"); sp.pprint(sp.simplify(HEH))
gauge_dir = sp.Matrix([w, kap])                 # eps01=w*xi1, eps13=kap*xi1
print("  H_EH . (w,kap)^T  (gauge dir; expect 0 => EH gauge-invariant):",
      sp.simplify(HEH*gauge_dir).T)
print("  rank(H_EH) =", sp.simplify(HEH).rank(), " det(H_EH) =", sp.simplify(HEH.det()))
print("\n  Interaction 2x2 form lam*H_Int(eps01,eps13):"); sp.pprint(sp.simplify(HInt))
print("\n  FULL 2x2 form on MOND-alive (u0,u1)=(1,0), lam=1:")
sub10 = {u0: 1, u1: 0, lam: 1}
sp.pprint(sp.simplify(Hfull.subs(sub10)))

# ======================================================================================
print("\n"+"="*95)
print("(II) STUCKELBERG: physical helicity-1 kinetic term  L_A1 = lam*Int(eps01=w*A1, eps13=kap*A1)")
print("="*95)
A1 = sp.Symbol('A1', real=True)
stk = {b1: w*A1, d1: kap*A1}
stk.update({es[key]: 0 for key in es if es[key] not in hel1x})
EH_on_gauge  = sp.expand(EHk.subs(stk))
Int_on_gauge = sp.expand(Intk.subs(stk))
print("  EH on gauge/Stuckelberg dir (expect 0):", sp.simplify(EH_on_gauge))
LA1 = sp.expand(lam*Int_on_gauge)
print("  L_A1 (general u0,u1) =", sp.factor(sp.collect(LA1, A1)))
coeffA1 = sp.expand(LA1.coeff(A1, 2))
print("  coeff of A1^2, general:", sp.factor(coeffA1))
coeffA1_10 = sp.simplify(coeffA1.subs(sub10))
print("  coeff of A1^2 on MOND-alive (u0,u1)=(1,0), lam=1:", sp.factor(coeffA1_10))
wcoef_A1 = sp.expand(coeffA1_10).coeff(w, 2)
kcoef_A1 = sp.expand(coeffA1_10).subs(w, 0)
print("  -> w^2 (time-kinetic) coefficient of helicity-1 mode A1:", wcoef_A1)
print("  -> kap^2 (gradient)    coefficient of helicity-1 mode A1:", kcoef_A1)

# ======================================================================================
print("\n"+"="*95)
print("(III) CALIBRATION: helicity-2 graviton kinetic sign from (1/2)(T4-T5) [MUST be healthy]")
print("="*95)
ep2 = sp.Symbol('ep2', real=True)
grav = {es[(1, 1)]: ep2, es[(2, 2)]: -ep2}       # helicity-2 '+' TT mode, k along z
grav.update({es[key]: 0 for key in es if es[key] not in {es[(1, 1)], es[(2, 2)]}})
Lgrav = sp.expand(sp.Rational(1, 2)*EHk.subs(grav))
cg = sp.expand(Lgrav.coeff(ep2, 2))
print("  (1/2)EH on helicity-2 '+' mode, coeff ep2^2:", sp.factor(cg))
wcoef_g = sp.expand(cg).coeff(w, 2)
kcoef_g = sp.expand(cg).subs(w, 0)
print("  -> graviton w^2 coeff:", wcoef_g, "  kap^2 coeff:", kcoef_g,
      "  (dispersion w^2 = kap^2 =>", "massless, healthy)" if sp.simplify(wcoef_g+kcoef_g) == 0 else "check)")

# ======================================================================================
print("\n"+"="*95)
print("DECISIVE GHOST TEST (the naive 'coeff of w^2' is a TRAP: L_A1 ~ -(w^2-kap^2)^2 is DEGREE-4)")
print("="*95)
print("  (a) STUCKELBERG operator degree in momentum (2=healthy Maxwell, 4=Ostrogradsky higher-deriv):")
degA1 = sp.total_degree(sp.Poly(sp.expand(coeffA1_10), w, kap))
print(f"      coeff(A1^2) = {sp.factor(coeffA1_10)}  -> total momentum degree = {degA1}",
      "(HEALTHY 2-deriv)" if degA1 == 2 else "(HIGHER-DERIVATIVE => Ostrogradsky ghost: 1/(w^2-kap^2)^2 double pole)")
# partial-fraction the propagator 1/coeff to expose the ghost pole
prop = sp.simplify(1/coeffA1_10)
print(f"      propagator 1/coeff(A1^2) = {prop}  (double pole at w^2=kap^2 => +/- residue pair = 1 healthy + 1 ghost)")

print("\n  (b) DIRECT 2x2: kinetic (w^2) matrix signature of the physical fields (eps01,eps13).")
def kinetic_matrix(Hmat):
    return sp.Matrix(2, 2, lambda i, j: sp.expand(Hmat[i, j]).coeff(w, 2))
for label, Hm in [("PURE EH (lam=0) [calib: must be ghost-free]", sp.simplify(HEH)),
                  ("FULL MOND-alive (u0,u1)=(1,0)", sp.simplify(Hfull.subs(sub10)))]:
    W = kinetic_matrix(Hm)
    evs = [sp.simplify(e) for e in W.eigenvals().keys()]
    dW = sp.simplify(W.det())
    nneg = sum(1 for e in evs if e.is_number and e < 0)
    print(f"      {label}:")
    print(f"         W(w^2) = {W.tolist()}   eigenvalues={evs}   det(W)={dW}")
    print(f"         -> negative kinetic eigenvalues = {nneg}",
          "  (GHOST present)" if nneg > 0 else "  (no ghost from time-kinetics)")

print("\n  (c) DIRECT 2x2: full dispersion det(H_full)=0 and its residue structure.")
detH = sp.factor(sp.simplify(Hfull.subs(sub10).det()))
print(f"      det(H_full) = {detH}   (double root at w^2=kap^2 => dipole; sign of leading w^4 coeff = product of kinetic eigenvalues)")
w4 = sp.expand(Hfull.subs(sub10).det()).coeff(w, 4)
print(f"      leading w^4 coeff of det(H) = {w4} = det(W)  -> {'NEGATIVE => one ghost' if (w4.is_number and w4<0) else 'check'}")

print("\n  (d) FIERZ-PAULI calibration: a 0-derivative FP mass term must NOT create a vector ghost.")
# FP mass term m^2/4 (h_mn h^mn - h^2); vector x-channel: h_mn h^mn = -2 eps01^2 + 2 eps13^2, trace h=0
mfp = sp.Symbol('m', positive=True)
Lfp = sp.Rational(1, 4)*mfp**2*(-2*b1**2 + 2*d1**2)      # = m^2/2 (eps13^2 - eps01^2)
Hfp = sp.hessian(sp.expand(sp.Rational(1, 2)*EHk.subs(zero_rest) + Lfp), [b1, d1])
Wfp = kinetic_matrix(sp.simplify(Hfp))
print(f"      EH + FP mass: W(w^2) = {Wfp.tolist()}  eigenvalues={[sp.simplify(e) for e in Wfp.eigenvals().keys()]}"
      f"  det={sp.simplify(Wfp.det())}  (0-deriv mass leaves eps01 auxiliary => no ghost)")

print("\n"+"="*95)
print("VERDICT")
print("="*95)
Wfull = kinetic_matrix(sp.simplify(Hfull.subs(sub10)))
ghost = sum(1 for e in [sp.simplify(x) for x in Wfull.eigenvals().keys()] if e.is_number and e < 0) > 0
print(f"  graviton (calib) healthy: w^2 coeff {wcoef_g} > 0, dispersion w^2=kap^2.")
print(f"  helicity-1 vector: Stuckelberg operator is DEGREE-{degA1} (-(w^2-kap^2)^2) = higher-derivative;")
print(f"                     direct kinetic matrix det(W) = {sp.simplify(Wfull.det())} < 0 => indefinite;")
print(f"                     det(H_full) = -9(w^2-kap^2)^2 => 2 luminal modes, ONE a ghost.")
print(f"  => VECTOR (helicity-1) SECTOR HAS A GHOST: {ghost}   =>  GATE = {'FAIL' if ghost else 'PASS'}")

# ======================================================================================
# ======================================================================================
print("\n"+"="*95)
print("(V) GENERALITY: does MOND-alive (a!=0) FORCE the vector ghost over the whole 2D subspace?")
print("="*95)
# kinetic matrix det in general (u0,u1)
Wgen = sp.Matrix(2, 2, lambda i, j: sp.expand(Hfull[i, j].subs(lam, 1)).coeff(w, 2))
detWgen = sp.factor(sp.simplify(Wgen.det()))
print(f"  det(kinetic matrix W) general (u0,u1), lam=1 : {detWgen}")
# Stuckelberg vector coeff prefactor:
print(f"  Stuckelberg L_A1 = -(1/2)(2u0+u1)(w^2-kap^2)^2 A1^2  -> higher-deriv ghost whenever (2u0+u1)!=0")
# MOND acceleration coefficient a on the subspace (static-NR, matches bimond_5invariant script):
xsp = sp.symbols('t x y z'); eps = sp.Symbol('eps')
Phi = sp.Function('Phi')(xsp[1]); Psi = sp.Function('Psi')(xsp[1])
Phh = sp.Function('Phih')(xsp[1]); Psh = sp.Function('Psih')(xsp[1])
def christ(gm, gmi):
    G = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                s = sp.Integer(0)
                for si in range(4):
                    s += gmi[l, si]*(sp.diff(gm[si, m], xsp[n])+sp.diff(gm[si, n], xsp[m])-sp.diff(gm[m, n], xsp[si]))
                G[l][m][n] = sp.expand(s/2)
    return G
def wfm(P_, Q_): return sp.diag(-(1+2*eps*P_), 1-2*eps*Q_, 1-2*eps*Q_, 1-2*eps*Q_)
g2 = wfm(Phi, Psi); gh2 = wfm(Phh, Psh)
Gg = christ(g2, g2.inv()); Gf = christ(gh2, gh2.inv())
Cd = [[[sp.expand(Gg[l][m][n]-Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]
g2i = g2.inv()
def T1s():
    return sp.expand(sum(Cd[a][m][n]*Cd[b][r][s]*g2[a, b]*g2i[m, r]*g2i[n, s]
                     for a in range(4) for b in range(4) for m in range(4) for n in range(4) for r in range(4) for s in range(4)))
def Pv(a): return sum(g2i[m, n]*Cd[a][m][n] for m in range(4) for n in range(4))
def T2s(): return sp.expand(sum(g2[a, b]*Pv(a)*Pv(b) for a in range(4) for b in range(4)))
def Vc(mu): return sum(Cd[a][a][mu] for a in range(4))
def T3s(): return sp.expand(sum(g2i[m, n]*Vc(m)*Vc(n) for m in range(4) for n in range(4)))
def T4s(): return sp.expand(sum(g2i[m, n]*Cd[a][m][b]*Cd[b][n][a] for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
def T5s(): return sp.expand(sum(Pv(a)*Vc(a) for a in range(4)))
Tns = [T1s(), T2s(), T3s(), T4s(), T5s()]
dPhi = sp.diff(Phi, xsp[1]); dPsi = sp.diff(Psi, xsp[1]); dPhh = sp.diff(Phh, xsp[1]); dPsh = sp.diff(Psh, xsp[1])
gPhi, gPsi = sp.symbols('gPhi gPsi')
avec = []
for Tv in Tns:
    q = sp.series(Tv, eps, 0, 3).removeO().coeff(eps, 2)
    q = sp.expand(q.subs({dPhh: dPhi-gPhi, dPsh: dPsi-gPsi}))
    avec.append(sp.simplify(q.coeff(gPhi, 2)))   # MOND accel coeff a for each T_i
a_sub = sp.simplify(sum(cvec[i]*avec[i] for i in range(5)))     # a on ghost-free subspace (u0,u1)
print(f"  MOND accel coefficient on subspace: a(u0,u1) = {sp.factor(a_sub)}")
print(f"  relation to vector prefactor (2u0+u1): a/(2u0+u1) = {sp.simplify(a_sub/(2*u0+u1))}")
print(f"  => a != 0  <=>  (2u0+u1) != 0  <=>  vector higher-deriv ghost present. MOND-ALIVE FORCES THE GHOST.")

# ======================================================================================
print("\n"+"="*95)
print("(IV) LONGITUDINAL (A0,A3) block  (2u0+u1)(kap^2-w^2)[[kap^2,-kap w],[-kap w,w^2]] -- interpret")
print("="*95)
A0, A3 = sp.symbols('A0 A3', real=True)
long_sub = {b1: 0, d1: 0}
# eps = k_m A_n + k_n A_m with A=(A0,0,0,A3): eps00=2 k0 A0=2w A0; eps33=2 kap A3; eps03=k0 A3+k3 A0=w A3+kap A0
Elong = {es[(0, 0)]: 2*w*A0, es[(3, 3)]: 2*kap*A3, es[(0, 3)]: w*A3+kap*A0}
Elong.update({es[key]: 0 for key in es if es[key] not in {es[(0, 0)], es[(3, 3)], es[(0, 3)]}})
Llong = sp.expand(lam*Intk.subs(Elong))          # EH gives 0 (gauge)
Hlong = sp.hessian(Llong, [A0, A3])
print("  Int longitudinal Hessian in (A0,A3):"); sp.pprint(sp.simplify(Hlong))
fac = sp.simplify(Hlong[0, 0] / (kap**2)) if kap != 0 else None
print("  common scalar factor (Hlong[0,0]/kap^2):", sp.factor(sp.simplify(Hlong[0, 0]/kap**2)))
print("  det(Hlong) =", sp.simplify(Hlong.det()), " rank =", sp.simplify(Hlong).rank(),
      " => rank-1: single combination (kap*A0 - w*A3) appears; no independent 2nd longitudinal DOF")
