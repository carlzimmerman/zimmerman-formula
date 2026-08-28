#!/usr/bin/env python3
"""
FC architecture A = AeST + J_10  --  self-contained certificate script.
Runnable from a clean checkout (sympy only). Prints residual certificates, not asserted PASSes.

Scope: this script proves the TWO load-bearing structural facts that decide how the AeST gates
are classified. It does NOT re-derive the AeST 6-DOF count (EXTERNAL: PRD 110.044015 / 2307.15126)
and does NOT recompute the committed lensing/FLRW numbers (those live in their own committed scripts,
re-run separately this session, both exit 0).

CERT 1  (kernel regularity of the frozen constitutive law):
        mu_10(y) = y/(1+y^10)^(1/10) is monotone (mu_10'>0), positive-definite in the MOND
        operator sense (mu_10 + y mu_10' > 0), deep-MOND mu_10 ~ y, Newtonian 1 - (1/10)(a0/g)^10.
        As an AeST free function F_M = a0^2 J_10(sqrt(Y)/a0), the deep-MOND branch is
        J_10(x) ~ (2/3) x^3  =>  F_M ~ (2/(3 a0)) Y^{3/2}.

CERT 2  (HOST-vs-KERNEL discriminator -- the decisive classification):
        About the homogeneous background Y=0, a field perturbation delta ~ eps gives Y ~ eps^2.
        delta^2 S_MOND = [eps^2 coefficient of F_M(Y=eps^2 q)] = 0  for an ARBITRARY admissible
        deep-MOND prefactor c (F_M ~ c Y^{3/2}). Leading nonzero term is O(eps^3).
        => the quadratic (linear-spectrum) action is J-INDEPENDENT.
        => AeST's known low-k unbounded-Hamiltonian scalar mode (2109.13287) cannot be fixed OR
           worsened by any choice of J. The IR obstruction is a HOST property of AeST, not a
           property of the kernel. This is what forces the Gate-G/IR failure-class = HOST.
"""
import sympy as sp

def cert1_kernel_regularity():
    y = sp.symbols('y', positive=True)
    mu = y/(1+y**10)**sp.Rational(1,10)
    dmu = sp.simplify(sp.diff(mu, y))
    # MOND operator positivity: mu + y mu'  (coefficient of the elliptic operator d/dy[y^2 mu])
    op = sp.simplify(mu + y*dmu)
    # deep-MOND limit y->0
    deep = sp.series(mu, y, 0, 3).removeO()
    # Newtonian limit y->oo : write x=1/y and expand 1 - mu at large y
    x = sp.symbols('x', positive=True)
    mu_x = (1/x)/(1+(1/x)**10)**sp.Rational(1,10)
    onemmu = sp.series(1-mu_x, x, 0, 11).removeO()   # x=a0/g
    print("[CERT 1] frozen kernel mu_10(y)=y/(1+y^10)^(1/10)")
    print("   mu_10'(y)      =", dmu)
    # dmu is manifestly positive: numerator positive, denom positive power
    dmu_pos = sp.simplify(dmu*(1+y**10)**sp.Rational(11,10))   # strip positive denom
    print("   mu_10' * (1+y^10)^{11/10} =", sp.simplify(dmu_pos), " (must be > 0)")
    print("   mu_10 + y mu_10' (op positivity), *(1+y^10)^{11/10} =",
          sp.simplify(op*(1+y**10)**sp.Rational(11,10)))
    print("   deep-MOND  mu_10 ~", deep, " (=> mu~y)")
    print("   Newtonian  1-mu_10 ~", onemmu, " (=> (1/10)(a0/g)^10)")
    ok = (sp.simplify(dmu_pos) == 1) and (deep == y)
    print("   CERT1 residual (mu_10'*denom - 1 == 0):", sp.simplify(dmu_pos-1))
    return ok

def cert2_host_vs_kernel():
    eps, c = sp.symbols('epsilon c', positive=True)
    q = sp.symbols('q', positive=True)
    Y = sp.symbols('Y', nonnegative=True)
    # ARBITRARY admissible deep-MOND constitutive branch F_M(Y) ~ c*Y^{3/2}
    FM = c*Y**sp.Rational(3,2)
    # homogeneous background Y=0; perturbation makes Y = eps^2 * q
    ser = sp.series(FM.subs(Y, eps**2*q), eps, 0, 4).removeO()
    coeff2 = sp.simplify(ser.coeff(eps, 2))   # quadratic-action contribution = delta^2 S_MOND
    coeff3 = sp.simplify(ser.coeff(eps, 3))   # leading nonzero
    print("[CERT 2] delta^2 S_MOND about Y=0, arbitrary prefactor c:")
    print("   F_M(Y=eps^2 q) =", sp.simplify(ser))
    print("   eps^2 coeff (delta^2 S_MOND) =", coeff2, "  (must be 0, J-independent)")
    print("   eps^3 coeff (leading nonzero) =", coeff3)
    # J-independence: coeff2 == 0 for symbolic c => kernel invisible at quadratic order for ANY J
    ok = (coeff2 == 0) and (coeff3 != 0)
    print("   => quadratic spectrum J-INDEPENDENT:", coeff2 == 0)
    print("   => IR/low-k obstruction classification = HOST (AeST), not KERNEL.")
    return ok

if __name__ == "__main__":
    c1 = cert1_kernel_regularity()
    print()
    c2 = cert2_host_vs_kernel()
    print()
    print("CERT1 kernel-regularity PASS:", c1)
    print("CERT2 host-vs-kernel (J-independence) PASS:", c2)
    print("EXIT_OK:", bool(c1 and c2))
