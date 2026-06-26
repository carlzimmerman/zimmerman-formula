#!/usr/bin/env python3
"""
agentT4 part 3 — given a value of the precanonical ordering constant lambda,
compute the implied Z_eff = c H_Lambda / a0 and compare to Carl's Z = sqrt(32pi/3).

Carl's framework:
    a0 = (c/2) sqrt(G rho_DE) = c^2 sqrt(Lambda/(32 pi))   (kappa=1/2)
    a0 = c H_Lambda / Z,   Z = sqrt(32 pi/3) = 5.788816...
    H_Lambda := c sqrt(Lambda/3)   (the pure-Lambda 'Hubble' rate)
=>  a0 = c H_Lambda / Z = c * c sqrt(Lambda/3) / sqrt(32pi/3)
        = c^2 sqrt(Lambda/3) * sqrt(3/(32pi)) = c^2 sqrt(Lambda/(32pi))  [consistent].

Kanatchikov framework:
    a* = 8 pi G hbar kappa_UV          (eq 21)
    Lambda = lambda * a*^2             (eq 22, c=1)   => a* = sqrt(Lambda/lambda)
    a0 = 2 a-bar, a-bar = a*/sqrt(2)   (eq 28)        => a0 = sqrt(2) a* = sqrt(2 Lambda/lambda)  (eq 32)
    [Alt 2308.08738 eq 35: a0 = (1/4) sqrt(Lambda)    -> a0 = sqrt(Lambda)/4]

So the Kanatchikov route predicts a relation a0 = f(lambda) * sqrt(Lambda).
We translate that into the Z_eff that Carl's identity a0 = c H_Lambda / Z would
require, i.e. Z_eff := c H_Lambda / a0 with H_Lambda = c sqrt(Lambda/3).
In c=1 units (the paper's), c=1, so:
    H_Lambda = sqrt(Lambda/3)
    Z_eff = H_Lambda / a0 = sqrt(Lambda/3) / a0.
For each candidate a0(lambda) we get Z_eff(lambda); Carl needs Z_eff = 5.7888.
"""
import sympy as sp

Lam = sp.symbols('Lambda', positive=True)
Z_carl = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
print("Z_carl = sqrt(32 pi/3) =", sp.N(Z_carl, 8))
print("a0_carl / sqrt(Lambda) coefficient (a0 = coeff*sqrt(Lambda)):")
# a0 = c^2 sqrt(Lambda/32pi); in c=1 -> a0 = sqrt(Lambda/(32pi))
coeff_carl = sp.sqrt(sp.Rational(1,1)/(32*sp.pi))
print("   coeff_carl = 1/sqrt(32 pi) =", sp.N(coeff_carl,8))

HL = sp.sqrt(Lam/3)   # c=1

def Zeff_from_a0(a0_expr, label):
    z = sp.simplify(HL / a0_expr)
    print(f"  [{label}] a0 = {a0_expr};  Z_eff = H_Lambda/a0 = {sp.simplify(z)} = {sp.N(z,6)}")
    return z

print("\n--- candidate a0(lambda) from Kanatchikov eq 32: a0 = sqrt(2 Lambda/lambda) ---")
for lam in [sp.Rational(3), sp.Rational(3,2), sp.Rational(3,8), sp.Integer(16), sp.Integer(42), sp.Integer(6), sp.Integer(12), sp.Integer(24)]:
    a0 = sp.sqrt(2*Lam/lam)
    Zeff_from_a0(a0, f"eq32, lambda={lam}")

print("\n--- alt a0 from 2308.08738 eq 35: a0 = (1/4) sqrt(Lambda) (lambda-independent) ---")
Zeff_from_a0(sp.sqrt(Lam)/4, "eq35 a0=sqrt(Lam)/4")

print("\n--- what lambda (via eq 32) would be needed to MATCH Carl's Z=5.7888 ? ---")
# Z_eff = sqrt(Lambda/3)/sqrt(2 Lambda/lambda) = sqrt( lambda/(6) ).  Set = Z_carl.
lam_needed = sp.solve(sp.Eq(sp.sqrt(sp.symbols('l')/6), Z_carl), sp.symbols('l'))
print("  From eq32: Z_eff = sqrt(lambda/6).  Z_eff=Z_carl  =>  lambda =", sp.N(lam_needed[0],8),
      " = 6 * Z_carl^2 =", sp.N(6*Z_carl**2,8))
print("  (i.e. would need lambda = 64 pi =", sp.N(64*sp.pi,8), ")")

print("\n--- what lambda matches via the synthesis's stated Z_eff=0.707 (lambda=3)? ---")
# synthesis claim: lambda=3 gives Z_eff = 0.707 = 1/sqrt(2). Check:
z3 = sp.sqrt(sp.Rational(3)/6)
print("  eq32, lambda=3: Z_eff = sqrt(3/6) = sqrt(1/2) =", sp.N(z3,6), " (matches synthesis 0.707) ")

print("\n=================== SUMMARY TABLE Z_eff vs lambda (eq32) ===================")
print("  Z_eff(lambda) = sqrt(lambda/6).   Carl needs Z_eff = sqrt(32pi/3) = 5.7888")
for lam in [3, sp.Rational(3,2), sp.Rational(3,8), 6, 16, 42, 64*sp.pi]:
    z = sp.sqrt(sp.nsimplify(lam)/6)
    ratio = sp.N(z/Z_carl,4)
    print(f"   lambda={str(lam):>10s}:  Z_eff={sp.N(z,5):>8}   Z_eff/Z_carl={ratio}")
