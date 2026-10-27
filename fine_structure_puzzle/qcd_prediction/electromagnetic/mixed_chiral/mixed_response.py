"""Mixed chiral mass-shape relation from vacuum and baryon pion loops.

No empirical alpha or fitted coefficient is used. This is a finite symbolic
audit of the stated chiral kernels, operator mass powers and matching rules.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    M, F, Z, g, scale, uvscale = s.symbols(
        "M F Z g scale uvscale", positive=True
    )
    q = s.symbols("e2", nonnegative=True)
    K, Lp = s.symbols("K Lp", real=True)
    checks = []

    def check(name, actual, expected):
        residue = s.simplify(actual-expected)
        if residue != 0:
            raise AssertionError((name, residue))
        checks.append({"name": name, "verified": True,
                       "value": s.sstr(s.simplify(actual))})

    def mass_log_derivative(expr):
        return M/s.Integer(2)*s.diff(expr, M)

    def vacuum_filter(expr):
        return mass_log_derivative(expr)-mass_log_derivative(
            mass_log_derivative(expr)
        )

    def proton_filter(expr):
        return s.diff(expr, M)-M*s.diff(expr, M, 2)

    # Actual leading charged-pion vacuum determinant and HB baryon kernel.
    Delta = 2*q*F**2*Z
    vacuum_kernel = -((M**2+Delta)*s.log((M**2+Delta)/scale**2)
                      -M**2*s.log(M**2/scale**2))/(16*s.pi**2*F**2)
    proton_kernel = q*Lp-g**2/(16*s.pi*F**2)*(
        (M**2+Delta)**s.Rational(3, 2)-M**3
    )
    V = K+s.diff(vacuum_kernel, q).subs(q, 0)
    Bp = s.diff(proton_kernel, q).subs(q, 0)
    A = Z/(8*s.pi**2)
    d = 3*g**2*Z/(16*s.pi)
    check("vacuum charge coefficient from determinant", V,
          K-A*(1+s.log(M**2/scale**2)))
    check("proton charge coefficient from pion kernel", Bp, Lp-d*M)
    Dchi = mass_log_derivative(V)
    Dp = s.diff(Bp, M)
    check("vacuum logarithmic mass shape", Dchi, -A)
    check("proton linear mass shape", Dp, -d)
    check("normalized cross-sector shape relation", 2*Dp/(3*s.pi*g**2*Dchi), 1)
    check("vacuum local e2 p2 counterterms removed", s.diff(Dchi, K), 0)
    check("baryon local e2 counterterms removed", s.diff(Dp, Lp), 0)
    check("F cancels from vacuum shape", s.diff(Dchi, F), 0)
    check("F cancels from proton shape", s.diff(Dp, F), 0)
    check("Z cancels from normalized relation",
          s.diff(2*Dp/(3*s.pi*g**2*Dchi), Z), 0)

    # The alternative infrared order is a genuinely different operation.
    A_finite = mass_log_derivative(s.diff(vacuum_kernel, q))
    B_finite = s.diff(s.diff(proton_kernel, q), M)
    check("finite-charge vacuum shape", A_finite, -A*M**2/(M**2+Delta))
    check("finite-charge proton shape", B_finite, -d*M/s.sqrt(M**2+Delta))
    check("nonuniform finite-charge shape ratio",
          2*B_finite/(3*s.pi*g**2*A_finite),
          s.sqrt(M**2+Delta)/M)
    check("zero-charge-first shape ratio",
          (2*B_finite/(3*s.pi*g**2*A_finite)).subs(q, 0), 1)

    # Chiral RG: choosing scale=M moves the log into K(M); it cannot delete it.
    K0 = s.symbols("K0", real=True)
    K_running = K0-A*s.log(scale**2/uvscale**2)
    V_running = V.subs(K, K_running)
    check("chiral scale independence", scale*s.diff(V_running, scale), 0)
    check("running-LEC scale=M gives same shape",
          mass_log_derivative(V_running.subs(scale, M)), -A)

    # Local finite subtraction changes a mass-independent constant at this order.
    c = s.symbols("c", real=True)
    check("finite-subtraction shift killed", mass_log_derivative(
        (2*c-1)*Z/(16*s.pi**2)), 0)

    # Exact mass-convention chain rule on the leading chiral susceptibility.
    mu, md, t, r, B, au, ad = s.symbols(
        "mu md t r B au ad", positive=True
    )
    chi0 = F**2*B*mu*md/(mu+md)
    convention_shift = -(au*mu*s.diff(chi0, mu)+ad*md*s.diff(chi0, md))/chi0
    fixed_ratio_shift = s.simplify(convention_shift.subs({mu:r*t, md:t}))
    check("mass-independent matching shift is constant at fixed ratio",
          t*s.diff(fixed_ratio_shift, t), 0)
    check("mass-independent matching shift exact value", fixed_ratio_shift,
          -(au+ad*r)/(1+r))
    a_ir = s.symbols("a_ir", real=True)
    check("IR-dependent matching changes leading vacuum shape",
          mass_log_derivative(-a_ir*s.log(M**2/scale**2)), -a_ir)

    # Next local EFT mass terms are M^2, not M or log M. These are the mass
    # powers of operators, not guessed numerical matching coefficients.
    cchi, cp = s.symbols("cchi cp", real=True)
    check("ordinary vacuum shape retains next analytic counterterm",
          mass_log_derivative(cchi*M**2), cchi*M**2)
    check("ordinary proton shape retains next analytic counterterm",
          s.diff(cp*M**2, M), 2*cp*M)
    check("improved vacuum shape preserves leading loop", vacuum_filter(V), -A)
    check("improved proton shape preserves leading loop", proton_filter(Bp), -d)
    check("improved normalized relation",
          2*proton_filter(Bp)/(3*s.pi*g**2*vacuum_filter(V)), 1)
    check("improved vacuum kills next analytic counterterm",
          vacuum_filter(cchi*M**2), 0)
    check("improved proton kills next analytic counterterm",
          proton_filter(cp*M**2), 0)
    check("improved vacuum single-log contamination",
          vacuum_filter(cchi*M**2*s.log(M**2/scale**2)), -cchi*M**2)
    check("improved proton single-log contamination",
          proton_filter(cp*M**2*s.log(M**2/scale**2)), -4*cp*M)

    # Controlled finite list of the first allowed mass dependences: all such
    # corrections vanish in the sequential chiral limit. This does not assert
    # uniform all-order remainder bounds for nonperturbative QCD.
    for power in (0, 1, 2):
        term = M**2*s.log(M**2/scale**2)**power
        check("vacuum next-order mass-shape limit, log power "+str(power),
              s.limit(mass_log_derivative(term), M, 0, dir="+"), 0)
    for power in (0, 1):
        term = M**2*s.log(M**2/scale**2)**power
        check("proton next-order mass-shape limit, log power "+str(power),
              s.limit(s.diff(term, M), M, 0, dir="+"), 0)
        check("proton improved next-order limit, log power "+str(power),
              s.limit(proton_filter(term), M, 0, dir="+"), 0)

    # Converting a canonically normalized e=0 pion pole mass changes the mass
    # derivative only by a factor tending to one.
    aM, bM = s.symbols("aM bM", real=True)
    physical_mass = M*(1+aM*M**2+bM*M**2*s.log(M**2/scale**2))
    check("canonical e0 mass-coordinate Jacobian tends to one",
          s.limit(s.diff(physical_mass, M), M, 0, dir="+"), 1)
    check("canonical e0 log-coordinate Jacobian tends to one",
          s.limit((physical_mass/M)/s.diff(physical_mass, M),
                  M, 0, dir="+"), 1)

    result = {
        "checks_passed": len(checks), "checks": checks,
        "normalized_relation": "2 Dp / (3 pi g_A0^2 Dchi) = 1 at retained chiral orders",
        "order_of_limits": "charge derivative at e2=0 with M>0; then shape derivatives; then M->0+",
        "no_alpha_target_used": True,
        "non_claims": [
            "No finite-mass all-orders identity",
            "No exact nonperturbative QCD theorem or all-order remainder bound",
            "No c_H, fixed-proton cosmological path, or alpha prediction",
            "No invariance under an arbitrary IR-dependent redefinition of held mass inputs",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"checks_passed":len(checks),"alpha_target_used":False}))


if __name__ == "__main__":
    main()
