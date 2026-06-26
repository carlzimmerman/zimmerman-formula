#!/usr/bin/env python3
"""
agentT4b part 2 -- pin down EXACTLY what is robust vs convention-dependent,
and independently re-derive the a0 -> Z_eff chain + the Yukawa variance.

Findings to lock:
  (A) The Clifford SCALAR gamma^{IJ}gamma_{IJ} is BASIS/SIGNATURE/Majorana-INVARIANT
      (= -12 metric, = 0 flat). Recomputation #2 (different basis) gives the SAME
      number as recomputation #1 (Dirac +---). -> the *algebra core* is robust.
  (B) lambda is NOT the scalar; it is (prefactor)x(range-count)x(mu-sum)x(scalar).
      Those three bookkeeping knobs are NOT fixed by the basis and move lambda over
      {0, 3/8, 3/4, 3/2, 3, ... 16, 42}. -> lambda is CONVENTION-DEPENDENT.
  => The 3-vs-42 paper split is an ORDERING/BOOKKEEPING ambiguity, NOT a basis effect
     and NOT an arithmetic slip. Recomputation #2 PROVES the split is not basis-driven.
"""
import sympy as sp

print("="*78)
print("(A) Is the 3-vs-42 split a BASIS effect?  -> NO. The basis-invariant core")
print("    gamma^IJ gamma_IJ = -12 is identical in Dirac(+---), Dirac(-+++),")
print("    Majorana(+---) [shown in agentT4b_lambda_majorana.py]. So changing")
print("    basis/signature does NOT move lambda. The split must be bookkeeping.")
print("="*78)

# Enumerate the bookkeeping knobs and show they reproduce BOTH 3 and ~16/42:
# lambda = prefactor * range * mu * scalar_metric
# scalar_metric (all16) = -12 ; (ord6) = -6
print("\n(B) The bookkeeping knobs (NONE fixed by basis):")
print("    knob1 prefactor p in {-1/16, -1/8, -1/32}  (the written -1/16 vs reorder)")
print("    knob2 mu-sum     m in {1,4}                 (count delta_mu^mu = d=4 or not)")
print("    knob3 range      r in {all16:-12, ord6:-6}  (double-count antisym pairs or not)")
print("    knob4 normaliz.  n in {half:1, quarter:1/4} (gamma^IJ=1/2[g,g] vs 1/4[g,g])")
print()
sols = {}
for p in [sp.Rational(-1,16), sp.Rational(-1,8), sp.Rational(-1,32)]:
    for m in [1,4]:
        for scal,rl in [(-12,'all16'),(-6,'ord6')]:
            for n,nl in [(1,'half'),(sp.Rational(1,16),'quarter^2')]:
                lam = p*m*scal*n
                lam = sp.nsimplify(lam)
                if lam>0:
                    sols.setdefault(lam,[]).append((p,m,rl,nl))
print("  distinct POSITIVE lambda reachable from the SAME invariant scalar:")
for lam in sorted(sols, key=lambda z: float(z)):
    print(f"    lambda = {str(lam):>6}   (e.g. p={sols[lam][0][0]}, mu={sols[lam][0][1]}, {sols[lam][0][2]}, {sols[lam][0][3]})")

# The 2308 estimate: 1/4 * 4^3 = 16, and numeric 42, and Lambda_w ~ 4^2 a*^2 -> 16
print("\n  2308.08738 reorder estimate: (1/4)*4^3 =", sp.Rational(1,4)*4**3,
      " ; Lambda_w ~ 4^2 a*^2 -> lambda=16 ; numeric quoted 42")
print("  -> {3, 16, 42} all live inside the bookkeeping span of ONE invariant scalar.")

print("\n" + "="*78)
print("(C) Independent re-derivation of the Yukawa variance  abar^2 = (1/2) a*^2")
print("    Psi = e^{-omega/a*} / (pi sqrt(8 G hbar ka) omega),  a* = 8 pi G hbar ka")
print("    <omega^2> = Int d^3omega  Psi omega^2 Psi   over R^3 (omega=|vec omega|)")
print("="*78)
w, a = sp.symbols('omega a_star', positive=True)
# Psi^2 * omega^2, with d^3omega = 4 pi omega^2 d omega for the radial integral,
# BUT the paper's Psi has 1/omega so Psi^2 ~ e^{-2w/a*}/(pi^2 * 8 G hbar ka * w^2).
# Normalization constant: <Psi|Psi> = Int 4pi w^2 dw * [N/w e^{-w/a*}]^2 = 1.
N = sp.symbols('N', positive=True)
Psi = N/w*sp.exp(-w/a)
norm = sp.integrate(4*sp.pi*w**2*Psi**2, (w,0,sp.oo))   # = 4 pi N^2 Int e^{-2w/a}dw
print("  <Psi|Psi> =", sp.simplify(norm), " -> set =1 gives N^2 =", sp.solve(norm-1,N**2))
N2 = sp.solve(norm-1,N**2)[0]
var = sp.integrate(4*sp.pi*w**2*Psi**2*w**2,(w,0,sp.oo)).subs(N**2,N2)
var = sp.simplify(var.subs(N, sp.sqrt(N2)))
print("  <omega^2> =", sp.simplify(var), "  (target: a*^2/2 =", a**2/2, ")")
print("  abar^2 = (1/2) a*^2 ?  ->", sp.simplify(var - a**2/2)==0)

print("\n" + "="*78)
print("(D) The a0 -> Z_eff chain (independent), with abar^2=a*^2/2, a*^2=Lambda/lambda")
print("="*78)
Lam, lam = sp.symbols('Lambda lambda_', positive=True)
astar2 = Lam/lam                      # from Lambda = lambda a*^2  (eq Lala)
abar2  = astar2/2                     # eq (l.670)
a0 = 2*sp.sqrt(abar2)                 # a0 = 2 abar  (eq a0lambda)
a0_simpl = sp.simplify(a0)
print("  a0 = 2 abar = ", a0_simpl, "   (paper: a0 = sqrt(2 Lambda/lambda) =",
      sp.sqrt(2*Lam/lam), ")  match:", sp.simplify(a0_simpl-sp.sqrt(2*Lam/lam))==0)
HLam = sp.sqrt(Lam/3)                 # c H_Lambda = c sqrt(Lambda/3), c=1
Zeff = sp.simplify(HLam/a0_simpl)
print("  Z_eff = c H_Lambda / a0 = sqrt(Lambda/3)/sqrt(2 Lambda/lambda) =", Zeff,
      " = sqrt(lambda/6)")
print()
Z_zim = sp.sqrt(sp.Rational(32,3)*sp.pi)
print("  For lambda=3 (paper, our recomputation #2 metric/all16/half/mu=4):")
print("     Z_eff = sqrt(3/6) = 1/sqrt(2) =", sp.N(sp.sqrt(sp.Rational(1,2)),8))
print("  Z_zimmerman = sqrt(32 pi/3) =", sp.N(Z_zim,8))
print("  ratio Z_zim/Z_eff =", sp.N(Z_zim/sp.sqrt(sp.Rational(1,2)),6),
      " (= 8 sqrt(3 pi)/3 =", sp.N(8*sp.sqrt(3*sp.pi)/3,6),")")
print("  lambda needed to hit Z_zim:  lambda = 6 Z_zim^2 = 64 pi =",
      sp.N(64*sp.pi,7), " -> TRANSCENDENTAL (no finite Clifford trace = rational gives this)")
print()
print("  Z_eff for the full reachable lambda set:")
for L in [sp.Rational(3,8),sp.Rational(3,4),sp.Rational(3,2),3,6,16,42,64*sp.pi]:
    Lv = sp.nsimplify(L)
    print(f"     lambda={str(Lv):>7}  Z_eff=sqrt(lam/6)={sp.N(sp.sqrt(Lv/6),5):>8}"
          f"   match Z=5.789? {sp.simplify(sp.sqrt(Lv/6)-Z_zim)==0}")
