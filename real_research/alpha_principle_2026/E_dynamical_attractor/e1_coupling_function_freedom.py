#!/usr/bin/env python3
"""Lane E, script E1: what the Damour-Polyakov attractor / runaway / Lambda-minimum do and do not fix.
Pre-registered in E_PREREGISTRATION.md (+ Amendment 1). Usage: python3 e1_coupling_function_freedom.py [MUTATE]
Exit 0 iff every declared expectation holds (the expectations are that the route does NOT fix a value).
In MUTATE mode two false assertions are added (M1, M2); they must trip, so the exit code must be 1.
"""
import sys
import sympy as sp

MUTATE = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []


def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        fails.append(name)


phi = sp.symbols("phi", real=True)
mu, nu, Ls = sp.symbols("mu nu Lambda_s", positive=True)
B = sp.Function("B")

# ---------------- C1: stationary condition of the mass function ----------------
Bphi = B(phi)
m = mu * Bphi ** sp.Rational(-1, 2) * sp.exp(-8 * sp.pi ** 2 * nu * Bphi) * Ls
dlnm = sp.simplify(sp.diff(m, phi) / m)
expected = -sp.diff(Bphi, phi) * (1 / (2 * Bphi) + 8 * sp.pi ** 2 * nu)
check("C1a d ln m/dphi = -B' [1/(2B) + 8 pi^2 nu]", sp.simplify(dlnm - expected) == 0)
Bs = sp.symbols("Bs", positive=True)
bracket = 1 / (2 * Bs) + 8 * sp.pi ** 2 * nu
check("C1b bracket > 0 for B > 0, nu > 0 (zero set of d ln m/dphi is exactly B' = 0)",
      sp.simplify(bracket).is_positive is True)
rhoL, kappa_prog = sp.symbols("rho_Lambda kappa_prog", positive=True)
check("C1c stationary condition contains neither rho_Lambda nor the programme's kappa",
      not (dlnm.free_symbols & {rhoL, kappa_prog}))

# ---------------- C2: three-term vs four-term string-loop truncation ----------------
Ph = sp.symbols("Phi", real=True)
c0, c1, c2 = sp.symbols("c0 c1 c2", real=True)
B3 = sp.exp(-2 * Ph) + c0 + c1 * sp.exp(2 * Ph)
y = sp.symbols("y", positive=True)  # y = exp(2 Phi_m)
dB3 = sp.diff(B3, Ph)
# extremum: exp(4 Phi) = 1/c1  (c1 > 0)
c1p = sp.symbols("c1p", positive=True)
B3p = B3.subs(c1, c1p)
ymp = 1 / sp.sqrt(c1p)  # y_m
sol_ok = sp.simplify(sp.diff(B3p, Ph).subs(sp.exp(2 * Ph), ymp).subs(sp.exp(-2 * Ph), 1 / ymp)) == 0
check("C2a three-term: B'=0 at exp(2 Phi_m) = c1^-1/2", sol_ok)
d2B3 = (4 * sp.exp(-2 * Ph) + 4 * c1p * sp.exp(2 * Ph)).subs({sp.exp(2 * Ph): ymp, sp.exp(-2 * Ph): 1 / ymp})
d2B3 = sp.simplify(d2B3)
check("C2b three-term: B''(Phi_m) = 8 sqrt(c1) > 0 -> extremum is a MINIMUM of B (max of masses): NOT an attractor",
      sp.simplify(d2B3).is_positive is True, f"(B'' = {d2B3})")
Bm3 = sp.simplify(B3p.subs({sp.exp(2 * Ph): ymp, sp.exp(-2 * Ph): 1 / ymp}))
check("C2c three-term value B_m = c0 + 2 sqrt(c1)", sp.simplify(Bm3 - (c0 + 2 * sp.sqrt(c1p))) == 0)

B4 = sp.exp(-2 * Ph) + c0 + c1 * sp.exp(2 * Ph) + c2 * sp.exp(4 * Ph)
c2sol = (1 - c1 * y ** 2) / (2 * y ** 3)
dB4 = sp.diff(B4, Ph).subs({sp.exp(-2 * Ph): 1 / y, sp.exp(2 * Ph): y, sp.exp(4 * Ph): y ** 2})
check("C2d four-term: B'=0 fixes c2 = (1 - c1 y^2)/(2 y^3)", sp.simplify(dB4.subs(c2, c2sol)) == 0)
d2B4 = sp.diff(B4, Ph, 2).subs({sp.exp(-2 * Ph): 1 / y, sp.exp(2 * Ph): y, sp.exp(4 * Ph): y ** 2}).subs(c2, c2sol)
check("C2e four-term: y*B'' = 12 - 4 c1 y^2  (attractor B''<0 iff c1 y^2 > 3)",
      sp.simplify(y * d2B4 - (12 - 4 * c1 * y ** 2)) == 0)
Bm4 = sp.simplify(B4.subs({sp.exp(-2 * Ph): 1 / y, sp.exp(2 * Ph): y, sp.exp(4 * Ph): y ** 2}).subs(c2, c2sol))
check("C2f four-term value B_m = 3/(2y) + c0 + c1 y/2", sp.simplify(Bm4 - (3 / (2 * y) + c0 + c1 * y / 2)) == 0)

# ---------------- C3: surjectivity ----------------
targets = [sp.Integer(1), sp.Integer(25), sp.Rational(137035999177, 10 ** 9), sp.Integer(1000)]
k = sp.Integer(1)  # declared free constant, fixed at 1
combos = [(sp.Integer(1), sp.Integer(4)), (sp.Integer(2), sp.Integer(1)), (sp.Rational(1, 2), sp.Integer(20))]
ok_all = True
for (yy, cc1) in combos:
    assert cc1 * yy ** 2 > 3
    for T in targets:
        c0s = sp.solve(sp.Eq(k * Bm4.subs({y: yy, c1: cc1}), T), c0)
        good = len(c0s) == 1
        if good:
            c0v = c0s[0]
            c2v = c2sol.subs({y: yy, c1: cc1})
            Bfun = B4.subs({c0: c0v, c1: cc1, c2: c2v})
            Phim = sp.log(yy) / 2
            good = (sp.simplify(sp.diff(Bfun, Ph).subs(Ph, Phim)) == 0
                    and sp.simplify(sp.diff(Bfun, Ph, 2).subs(Ph, Phim)) < 0
                    and sp.simplify(k * Bfun.subs(Ph, Phim) - T) == 0)
        ok_all &= bool(good)
        print(f"    (y_m={yy}, c1={cc1}) target 1/alpha={float(T):.9g}: c0 = {float(c0s[0]) if c0s else None:.9g}, attractor + value OK = {good}")
check("C3a every declared target (4) reachable with an attractor for every declared (y_m, c1) (3): 12/12", ok_all)
dBm_dc0 = sp.diff(Bm4, c0)
check("C3b dB_m/dc0 = 1 (the principle never fixes B_m)", sp.simplify(dBm_dc0 - 1) == 0)
print("    REPORT-ONLY: c0 = 0 would need (y=1) c1 = 2(target - 3/2) = %.6f ; not an outcome of the principle." % (2 * (137.035999177 - 1.5)))

# ---------------- C4: Lambda-minimum (de Sitter attractor) ----------------
rL, xi, phiL, kk, zF, zF2, m_rho, zm = sp.symbols("rho_Lambda xi phi_L k zeta_F zeta_F2 rho_m zeta_m", real=True)
V = rL * (1 + xi / 2 * (phi - phiL) ** 2)
phistar = sp.solve(sp.diff(V, phi), phi)
check("C4a de Sitter minimum at phi = phi_L", phistar == [phiL])
BF = 1 + zF * (phi - phiL) + zF2 * (phi - phiL) ** 2 / 2
alpha_min = 1 / (kk * BF.subs(phi, phistar[0]))
check("C4b alpha_min = 1/(k B_F(phi_L)): d/d rho_Lambda = 0 and d/d xi = 0",
      sp.simplify(sp.diff(alpha_min, rL)) == 0 and sp.simplify(sp.diff(alpha_min, xi)) == 0)
# with a non-universal matter coupling the stationary point tracks rho_m / rho_Lambda
phi_star_m = sp.solve(sp.diff(V, phi) + m_rho * zm, phi)[0]
check("C4c non-universal matter coupling: phi* = phi_L - rho_m zeta_m/(rho_Lambda xi) depends on rho_m/rho_Lambda (time-dependent -> alpha drifts)",
      sp.simplify(phi_star_m - (phiL - m_rho * zm / (rL * xi))) == 0 and sp.diff(phi_star_m, m_rho) != 0)

# ---------------- C5: runaway dilaton ----------------
C, b, phi0, kc = sp.symbols("C b phi_0 k", positive=True)
Bfun = C + b * sp.exp(-phi)
alpha_inf_inv = sp.limit(kc * Bfun, phi, sp.oo)
check("C5a alpha_infinity^-1 = k C_F", sp.simplify(alpha_inf_inv - kc * C) == 0)
check("C5b present offset k b e^-phi_0 is a second free number; alpha^-1(phi_0) = k(C + b e^-phi_0) has 2 free parameters for 1 datum",
      len((kc * (C + b * sp.exp(-phi0))).free_symbols & {C, b, phi0}) == 3)
target = sp.Rational(137035999177, 10**9)
Csol = sp.solve(sp.Eq(kc * (C + b * sp.exp(-phi0)), target), C)
check("C5c for any b, phi_0, k a C_F reproduces the target (surjective)", len(Csol) == 1)

# ---------------- C6: ledger ----------------
print("""
    C6 PARAMETER LEDGER (what the attractor principle leaves free)
      quantity                                         status under DP least-coupling / runaway / Lambda-minimum
      gauge kinetic function B_F(phi) (whole function)  FREE (only its extremum LOCATION is pinned)
      value B_F(phi_m)  -> alpha^-1 = k B_F(phi_m)      FREE (c0 above; C_F for runaway)
      normalisation / KM level / RG constant k          FREE (declared constant)
      potential / B_Lambda(phi)                         FREE (only its minimum location enters)
      phi_initial                                       REMOVED by the attractor (this is what the principle buys)
      rho_Lambda, kappa                                 do not enter the value at all (C1c, C4b)
    data: 1 (alpha).  free numbers needed to hit it: >= 1 (c0) -> under-determined by construction.""")

# ---------------- MUTATE controls (false assertions; must trip) ----------------
if MUTATE:
    check("M1 (FALSE) three-term extremum is an attractor (B'' < 0)", sp.simplify(d2B3).is_negative is True)
    check("M2 (FALSE) dB_m/dc0 = 0 (principle fixes the value)", sp.simplify(dBm_dc0) == 0)

print("\nSUMMARY:", "ALL DECLARED EXPECTATIONS HOLD" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
