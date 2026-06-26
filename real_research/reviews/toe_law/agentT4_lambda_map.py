#!/usr/bin/env python3
"""
agentT4 part 2 — MAP every convention chain to the resulting lambda, and locate
which chain reproduces 3 (2311.05525 eq 23), which reproduces 16 = (1/4)*4^3,
and which reproduces 42 (2308.08738 sec 3.3). Goal: decide forced vs ambiguous.

The c-number in eq (23) is built from a Clifford SCALAR  C := contraction of
gamma^{IJ} gamma^{KL} with the pair-delta from [d_omega, omega], times:
  - a prefactor P (paper: -1/16),
  - possibly a mu-sum factor M (sum_mu delta_mu^mu = 4) OR not (if the mu in
    eq 23 is a single fixed/free index, not summed),
  - a metric vs flat choice in the (IJ)<->(KL) contraction,
  - a sum range: all-16 (full Einstein I,J,K,L=0..3) vs ordered-6 (I<J,K<L),
  - Euclidean (all +) vs Lorentzian (+---) signature for the trace value.

We tabulate lambda = P * M * C for the cross product of all these and read off
which equals 3, 16, 42, and whether ANY single 'natural' choice is singled out.
"""
import sympy as sp
import itertools

def gammas(signature):
    i = sp.I
    I2 = sp.eye(2); Z2 = sp.zeros(2)
    sx = sp.Matrix([[0,1],[1,0]]); sy = sp.Matrix([[0,-i],[i,0]]); sz = sp.Matrix([[1,0],[0,-1]])
    def B(A,Bb,C,D): return sp.Matrix(sp.BlockMatrix([[A,Bb],[C,D]]))
    if signature == "lorentz":   # +---  gamma^0 timelike, gamma^k spacelike (gamma^k anti-herm)
        g0=B(I2,Z2,Z2,-I2); g1=B(Z2,sx,-sx,Z2); g2=B(Z2,sy,-sy,Z2); g3=B(Z2,sz,-sz,Z2)
        eta=sp.diag(1,-1,-1,-1)
    else:                        # euclidean ++++  (use hermitian gamma^k = [[0,s],[s,0]])
        g0=B(I2,Z2,Z2,-I2); g1=B(Z2,sx,sx,Z2); g2=B(Z2,sy,sy,Z2); g3=B(Z2,sz,sz,Z2)
        eta=sp.diag(1,1,1,1)
    return [g0,g1,g2,g3], eta

def build(signature):
    g, eta = gammas(signature)
    # verify clifford
    for a in range(4):
        for b in range(4):
            assert sp.simplify(g[a]*g[b]+g[b]*g[a] - 2*eta[a,b]*sp.eye(4))==sp.zeros(4), signature
    def gIJ(a,b): return (g[a]*g[b]-g[b]*g[a])/2
    return g, eta, gIJ

def scalar(M):
    M=sp.simplify(M)
    return sp.nsimplify(sp.trace(M)/4)

def delta_anti(a,b,c,d):
    return (1 if (a==c and b==d) else 0) - (1 if (a==d and b==c) else 0)

results = []
for sig in ("lorentz","euclidean"):
    g, eta, gIJ = build(sig)
    pairs = [(a,b) for a in range(4) for b in range(4) if a<b]
    # contraction matrix C = sum gamma^{IJ} gamma^{KL} * weight(IJ,KL)
    # FLAT: weight = delta_anti (pure Kronecker pairing, no metric)
    # METRIC: weight = eta_{IK}eta_{JL}-eta_{IL}eta_{JK}  (lower the KL pair)
    def metric_weight(a,b,c,d):
        return eta[a,c]*eta[b,d]-eta[a,d]*eta[b,c]
    for rng_name, rng in (("all16", list(itertools.product(range(4),repeat=2))),
                          ("ord6",  pairs)):
        for wname, wfun in (("flat", delta_anti), ("metric", metric_weight)):
            C = sp.zeros(4)
            for (a,b) in rng:
                for (c,d) in rng:
                    w = wfun(a,b,c,d)
                    if w!=0:
                        C += w*(gIJ(a,b)*gIJ(c,d))
            Csc = scalar(C)
            results.append((sig, rng_name, wname, Csc))

print(f"{'sig':10s} {'range':6s} {'weight':7s}  C=Tr/4   "
      f"| -1/16*C  | -1/16*C*4(mu) | -1/64*C*4^3(=*256/64) examples")
for (sig,rng,w,C) in results:
    l_base = sp.nsimplify(sp.Rational(-1,16)*C)
    l_mu   = sp.nsimplify(sp.Rational(-1,16)*C*4)
    print(f"{sig:10s} {rng:6s} {w:7s}  {str(C):>6s}  | {str(l_base):>7s}  | {str(l_mu):>9s}")

# Now specifically hunt for the chains that give 3, 16, 42.
print("\n=== chains that hit target lambda values ===")
targets = {3:"2311.05525 eq23", 16:"(1/4)*4^3 = 2308 'order 1/4 4^3'", 42:"2308 sec3.3 numeric"}
for (sig,rng,w,C) in results:
    for P,Pn in [(sp.Rational(-1,16),"-1/16"),(sp.Rational(1,16),"1/16"),
                 (sp.Rational(-1,8),"-1/8"),(sp.Rational(-1,4),"-1/4"),
                 (sp.Rational(-1,32),"-1/32"),(sp.Rational(-1,2),"-1/2")]:
        for M,Mn in [(1,"noMu"),(4,"mu=4"),(6,"=6pairs"),(16,"=16")]:
            val = sp.nsimplify(P*C*M)
            if val in (3,16,42, sp.Integer(3), sp.Integer(16), sp.Integer(42)):
                print(f"  lambda={val}: sig={sig} range={rng} weight={w} "
                      f"C={C} prefactor={Pn} mufac={Mn}   [{targets[int(val)]}]")
