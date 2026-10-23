#!/usr/bin/env python3
"""Q7_bs25_cosmology step S (FROZEN_CRITERIA section 4): the Blanchet-Skordis cosmological sector as transcribed by
WebFetch (BS24 = arXiv:2404.06584v2, BS25 = arXiv:2507.00912v1; PROVISIONAL, not on disk) checked for internal
consistency with sympy, and compared term by term with the linear khronon equations used by Q6/F3/M1.

Equation labels are those of today's fetch of the BS24 v2 HTML (the DBI block was Eq. 96/97 in a June fetch); the
checks use the equation CONTENT. c = 1 throughout; G only through 8 pi G rho combinations.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_source.py   (Q7_MUTATE=1: Q6's sound speed with j1 = +1 -> S7, S8d FAIL)
"""
import json
import os
import sys
import time

import sympy as sp

T0 = time.time()
MUT = os.environ.get("Q7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, f"q7_source{TAG}.out"), "w")
RES = {"mutate": MUT, "checks": {}, "source": "BS24 v2 / BS25 v1 arXiv HTML via WebFetch 2026-10-23 (PROVISIONAL)"}
NP = NC = 0


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, thr):
    global NP, NC
    NC += 1
    NP += bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")
    RES["checks"][name] = {"pass": bool(ok), "value": str(value), "threshold": thr}


def zero(e):
    return sp.simplify(sp.together(sp.expand(e))) == 0


Q, mu, lam, a, I0, k, Z = sp.symbols("Q mu lambda_D a I_0 k Z", positive=True)
q = sp.symbols("q", positive=True)
J1 = sp.Integer(+1) if MUT else sp.Integer(-1)          # Q6's j1 = J'(0); MUTATE flips it
P(f"== Q7 step S: BS24/BS25 cosmological sector (WebFetch, PROVISIONAL){' [MUTATE: Q6 j1 = +1]' if MUT else ''}")

# ------------------------------------------------------------------ S1 the DBI K (BS25 Eq. 6 = BS24 Eq. 87)
u = Q - 1
K_dbi = 2 * mu**2 / lam * (1 - sp.sqrt(1 - lam * u**2))
K_quad = mu**2 * u**2
lim0 = sp.limit(K_dbi, lam, 0)
d = [sp.simplify(sp.diff(K_dbi, Q, n).subs(Q, 1)) for n in range(5)]
ok1 = zero(lim0 - K_quad) and d[0] == 0 and d[1] == 0 and zero(d[2] - 2 * mu**2) and d[3] == 0 and zero(d[4] - 6 * mu**2 * lam)
check("S1_DBI_shape", ok1, f"lim_(lambda->0) = {lim0}; K^(n)(1) n=0..4: {d}", "= mu^2(Q-1)^2; 0, 0, 2mu^2, 0, 6 mu^2 lambda_D")

# ------------------------------------------------------------------ S2 background solution (BS24 Eq. 88) and coded forms
Kp = sp.diff(K_dbi, Q)
Kpp = sp.diff(K_dbi, Q, 2)
x = 2 * mu**2 * a**3 / I0
Qbar88 = 1 + 1 / sp.sqrt(lam + x**2)
res_root = sp.simplify(Kp.subs(Q, Qbar88) - I0 / a**3)
# coded (cancellation-free) forms in Z = I0/(2 mu^2 a^3), r = sqrt(1 + lambda Z^2)
r = sp.sqrt(1 + lam * Z**2)
Zof = I0 / (2 * mu**2 * a**3)
Qc = 1 + Z / r
Kc = 2 * mu**2 * Z**2 / (r * (r + 1))
Kppc = 2 * mu**2 * r**3
ca2c = Z / (r**2 * (r + Z))
subsZ = {I0: 2 * mu**2 * a**3 * Z}
ok2a = zero(res_root)
ok2b = zero((Qbar88 - Qc).subs(subsZ))
ok2c = zero(K_dbi.subs(Q, Qc) - Kc) and zero(Kpp.subs(Q, Qc) - Kppc)
bound = sp.simplify(1 - lam * (Qc - 1)**2)             # > 0  <=>  Qbar < 1 + lambda^-1/2
ok2d = zero(bound - 1 / (1 + lam * Z**2))
check("S2_background_Eq88", ok2a and ok2b and ok2c and ok2d,
      f"K'(Qbar88) - I0/a^3 = {res_root}; Eq.88 = coded 1+Z/r: {ok2b}; K, K'' coded: {ok2c}; 1 - lambda(Qbar-1)^2 = {bound}",
      "residuals 0; 1 - lambda q^2 = 1/(1+lambda Z^2) > 0 (1 <= Qbar < 1 + lambda^-1/2)")

# ------------------------------------------------------------------ S3 rho, p (Eqs. 89a/b) and conservation
rho89 = I0 / a**3 + 2 * mu**2 / lam * (-1 + sp.sqrt(1 + lam * Zof**2))           # 8 pi G rho
p89 = 2 * mu**2 / lam * (1 - 1 / sp.sqrt(1 + lam * Zof**2))                      # 8 pi G p
rho44 = (Q * Kp - K_dbi).subs(Q, Qbar88)
p44 = K_dbi.subs(Q, Qbar88)
ok3a = zero(sp.simplify(rho89 - rho44)) and zero(sp.simplify(p89 - p44))
cons = sp.simplify(sp.diff(rho89, a) + 3 * (rho89 + p89) / a)
ok3b = zero(cons)
check("S3_rho_p_Eq89_conservation", ok3a and ok3b, f"89a/b = (QK'-K, K) on Eq.88: {ok3a}; d rho/da + 3(rho+p)/a = {cons}",
      "residuals 0")

# ------------------------------------------------------------------ S4 w, c_ad^2 (Eqs. 92-94) vs Eqs. 45/46
s_ = sp.sqrt(1 - lam * q**2)
w92 = (lam * q**2 + (1 + q) * s_ - 1) / (2 + (1 + lam) * q)
c93 = q * (1 - lam * q**2) / (1 + q)
Kq = K_dbi.subs(Q, 1 + q)
Kpq = Kp.subs(Q, 1 + q)
Kppq = Kpp.subs(Q, 1 + q)
w45 = Kq / ((1 + q) * Kpq - Kq)
c46 = Kpq / ((1 + q) * Kppq)
w94 = Z / (1 + lam * Z**2 + (1 + Z) * sp.sqrt(1 + lam * Z**2))
c94 = Z / ((1 + lam * Z**2) * (sp.sqrt(1 + lam * Z**2) + Z))
qZ = Z / r
ok4 = (zero(sp.simplify(w92 - w45)) and zero(sp.simplify(c93 - c46))
       and zero(sp.simplify(w45.subs(q, qZ) - w94)) and zero(sp.simplify(c46.subs(q, qZ) - c94))
       and zero(sp.simplify(c94 - ca2c)))
if not ok4:                                           # numeric fallback when simplify stalls
    import random
    random.seed(1)
    mx = 0.0
    for _ in range(40):
        vals = {lam: sp.Float(10 ** random.uniform(-3, 3)), Z: sp.Float(10 ** random.uniform(-3, 3)), mu: 1}
        qv = (qZ.subs(vals))
        for e1, e2 in ((w92.subs(q, qv), w45.subs(q, qv)), (c93.subs(q, qv), c46.subs(q, qv)), (w45.subs(q, qv), w94),
                       (c46.subs(q, qv), c94), (c94, ca2c)):
            v1, v2 = complex(e1.subs(vals).evalf(30)), complex(e2.subs(vals).evalf(30))
            mx = max(mx, abs(v1 - v2) / max(abs(v2), 1e-300))
    ok4 = mx < 1e-25
    RES["S4_numeric_fallback_maxrel"] = mx
check("S4_w_cad2_Eqs92_94", ok4, "Eq.92/93 (q) = Eq.45/46; Eq.94a/b (Z) = Eq.45/46 on q = Z/r; coded c_ad^2 = 94b",
      "residuals 0 (or < 1e-25 at 40 random points)")

# ------------------------------------------------------------------ S5 limits (Eqs. 90, 95)
w_late = sp.limit(w94 / (Z / 2), Z, 0)
c_late = sp.limit(c94 / Z, Z, 0)
w_early = sp.limit(w94 / (1 / (Z * sp.sqrt(lam) * (1 + sp.sqrt(lam)))), Z, sp.oo)
c_early = sp.limit(c94 / (1 / (lam * Z**2 * (1 + sp.sqrt(lam)))), Z, sp.oo)
rhoZ = rho89.subs(I0, 2 * mu**2 * a**3 * Z)
r_late = sp.limit(sp.simplify(rhoZ / (2 * mu**2 * Z)), Z, 0)
r_early = sp.limit(sp.simplify(rhoZ / (2 * mu**2 * Z)), Z, sp.oo)
ok5 = all(zero(v - 1) for v in (w_late, c_late, w_early, c_early, r_late)) and zero(r_early - (1 + 1 / sp.sqrt(lam)))
check("S5_limits_Eqs90_95", ok5, f"w/(Z/2)->{w_late}, cad2/Z->{c_late} (late); w, cad2 / Eq.95b -> {w_early}, {c_early} (early); "
      f"rho/(I0/a^3): late {r_late}, early {r_early}", "1, 1, 1, 1, 1, 1 + lambda^-1/2")
# the early DBI era is dust-like: w -> 0 and rho a^3 -> const (no a^-6 partner)
RES["early_dust_factor"] = str(r_early)

# ------------------------------------------------------------------ S6 the quadratic limit of 89a = Q6 step B's background
lim_rho = sp.limit(rho89, lam, 0)
ok6 = zero(lim_rho - (I0 / a**3 + I0**2 / (4 * mu**2 * a**6)))
check("S6_quadratic_limit", ok6, f"lim_(lambda->0) 8piG rho = {sp.simplify(lim_rho)}", "= I0/a^3 + I0^2/(4 mu^2 a^6) (Q6 step B)")

# ------------------------------------------------------------------ S7 BS24 Eq. 71 vs Q6's rest-frame sound speed (general K)
Qb, K1, K2 = sp.symbols("Qbar Kp Kpp", positive=True)
cad2 = K1 / (Qb * K2)                                  # Eq. 46
fourpiG_rho_1pw = Qb * K1 / 2                          # 4 pi G (rho + p) = Q K'/2 (Eq. 44a + 44b)
cs2_BS = cad2 / (1 + cad2 * k**2 / (a**2 * fourpiG_rho_1pw))
cs2_Q6 = Qb * K1 / (Qb**2 * K2 - 2 * J1 * k**2 / a**2)
res7 = sp.simplify(cs2_BS - cs2_Q6)
check("S7_BS_Eq71_equals_Q6_cs2", zero(res7), f"c_s^2(BS Eq.71) - c_s^2(Q6, j1 = {J1}) = {res7}",
      "0 for general K: BS's own perturbations contain the J'(0) = -1 hold")

# ------------------------------------------------------------------ S8 the Upsilon constraint, the kernel, Upsilon = Xi, Eq. 66a = Q6's delta rho
Ups, Dlt, w_ = sp.symbols("Upsilon Delta w")
A_ = a**2 * Qb * K1 / 2 / (1 + w_)                      # 4 pi G rho a^2
sol = sp.solve(sp.Eq(-k**2 * Ups, A_ * ((1 + w_) * Ups / cad2 + Dlt)), Ups)[0]
M2 = Qb**2 * K2 / 2
ok8a = zero(sp.simplify(sol + A_ * Dlt / (k**2 + a**2 * M2)))
s_BS = sp.simplify(1 - cs2_BS * k**2 / (a**2 * fourpiG_rho_1pw))
ok8b1 = zero(sp.simplify(s_BS - a**2 * M2 / (k**2 + a**2 * M2)))
ok8b2 = zero(sp.simplify(s_BS.subs({Qb: 1, K2: 2 * mu**2}) - a**2 * mu**2 / (k**2 + a**2 * mu**2)))
# (c) Upsilon (cosmic time, BS) = Xi (conformal, Q6)
t = sp.symbols("t")
af, Qf, piB, phi, Hf, cf = (sp.Function(n)(t) for n in ("a", "Qbar", "pi_BS", "phi", "H", "c_ad2"))
sigma = Qf * piB                                         # theta_K = sigma/Qbar = pi_BS (Eq. 66b)
dQ_rule = {sp.Derivative(Qf, t): -3 * Hf * cf * Qf}      # Eq. 48
Ups62 = phi - (sp.diff(sigma, t).subs(dQ_rule) + 3 * Hf * cf * sigma) / Qf
piC = piB / af                                           # conformal time shift
dconf = lambda f: af * sp.diff(f, t)                     # ' = a d/dt
Xi = phi - dconf(piC) - af * Hf * piC                    # Psi = phi, curly-H = a H; H = a_dot/a
Xi = Xi.subs(sp.Derivative(af, t), af * Hf)
ok8c = zero(sp.simplify(Ups62 - Xi))
# (d) Eq. 66a delta_K (times rho) vs Q6's 8 pi G delta rho = Q K'' dQ + 2 j1 (k/a)^2 Xi, dQ = -Q Xi + Q_dot pi (cosmic time)
Xs, pis, pid, phis, Hs, cs = sp.symbols("Xi pi pidot phi H c_ad2_s")
wq = sp.symbols("w_q")
eightpiGrho = Qb * K1 / (1 + wq)
K2_of = K1 / (Qb * cs)                                   # K'' from c_ad^2 = K'/(Q K'')
sig_dot_over_Q = pid - 3 * Hs * cs * pis                 # sigma_dot / Qbar with sigma = Q pi
ups_s = phis - pid                                       # Upsilon = phi - pi_dot (S8c)
delta66a = (1 + wq) / cs * (sig_dot_over_Q - phis) + (-k**2 * ups_s) / (a**2 * eightpiGrho / 2)
dQ = -Qb * ups_s + (-3 * Hs * cs * Qb) * pis
delta_Q6 = (Qb * K2_of * dQ + 2 * J1 * k**2 / a**2 * ups_s) / eightpiGrho
res8d = sp.simplify(delta66a - delta_Q6)
ok8d = zero(res8d)
check("S8_kernel_Upsilon_Xi_Eq66a", ok8a and ok8b1 and ok8b2 and ok8c and ok8d,
      f"(a) Upsilon = -4piG rho a^2 Delta/(k^2 + a^2 M^2), M^2 = Q^2K''/2: {ok8a}; (b) s = a^2M^2/(k^2+a^2M^2): {ok8b1}, "
      f"Q->1, K''=2mu^2 -> F3/BSK2 kernel: {ok8b2}; (c) Upsilon(Eq.62) = Xi(Q6): {ok8c}; (d) Eq.66a = Q6 delta rho "
      f"(j1 = {J1}): residual {res8d}", "all exact")

# ------------------------------------------------------------------ S9 BS24's quoted bounds from the transcribed formulas
H0c = 70.0 / 299792.458 / 1000.0                         # kpc^-1
OmK = 0.26
w0max = 0.0164 * (10 ** -4.5) ** 3 / (1 - 0.0164)
mu_inv_max = (4 * w0max / (3 * H0c**2 * OmK)) ** 0.5
w0_100 = 3 * H0c**2 * OmK / (4 * (1 / 100.0) ** 2)
q9 = {"wtilde0_max": (w0max, 5.3e-16), "mu_inv_max_kpc": (mu_inv_max, 0.22), "wtilde0_at_100kpc": (w0_100, 1.06e-10)}
ok9 = all(abs(v / ref - 1) <= 0.03 for v, ref in q9.values())
check("S9_BS24_bounds_reproduce", ok9, "; ".join(f"{n} {v:.4g} (quoted {ref:g})" for n, (v, ref) in q9.items()),
      "each within 3 % (Eqs. 76-80)")
RES["S9"] = {n: v for n, (v, _) in q9.items()}

# ------------------------------------------------------------------ S10 BS25 = BS24 (J at Y -> 0, background, quadratic)
Y, a0, Lam = sp.symbols("Y a_0 Lambda", positive=True)
J4b = Lam - Y + sp.Rational(2, 3) / a0 * Y**sp.Rational(3, 2)
ok10a = zero(J4b.subs(Y, 0) - Lam) and zero(sp.diff(J4b, Y).subs(Y, 0) + 1) and (a0 not in (Lam - Y).free_symbols)
ok10b = zero(sp.diff(J4b, Y) + 1 - sp.sqrt(Y) / a0)       # deep MOND: 1 + J_Y = y = sqrt(Y)/a0
Qq = 1 + I0 / (2 * mu**2 * a**3)                          # BS24 Eq. 53
w0t = I0 / (4 * mu**2)
ok10c = (zero(sp.simplify((Qq - 1) / (Qq + 1) - w0t / (w0t + a**3)))
         and zero(sp.simplify((Q * sp.diff(K_quad, Q) - K_quad).subs(Q, Qq) - I0 / a**3 * (1 + w0t / a**3))))
ok10d = zero(sp.diff(K_quad, Q).subs(Q, Qq) - I0 / a**3)
check("S10_BS25_equals_BS24", ok10a and ok10b and ok10c and ok10d,
      f"Eq.4b: J(0)=Lambda, J'(0)=-1, a0 first at Y^3/2: {ok10a}; 1+J_Y = sqrt(Y)/a0 (deep MOND): {ok10b}; "
      f"BS25 Eq.17 = BS24 Eqs.54/57 on Eq.53: {ok10c}; Eq.16/47 K_Q = I0/a^3: {ok10d}; BS25 Eq.6 = BS24 Eq.87 (same text)",
      "all exact")

# ------------------------------------------------------------------ S11 BS25 Eq. 11 (static, linear) = Q6's delta rho; Eqs. 10a+11 -> Eq. 13
JY = sp.symbols("J_Y")
fourpiG_rho_tau_11 = -(JY * (-k**2) * Xs + mu**2 * Xs)   # Fourier: grad^2 -> -k^2
eightpiG_drho_Q6 = 2 * mu**2 * (-Xs) + 2 * J1 * k**2 * Xs
ok11a = zero(sp.expand(2 * fourpiG_rho_tau_11.subs(JY, -1) - eightpiG_drho_Q6))
rho_m = sp.symbols("rho_m")
phiF = sp.symbols("phiF")
eq10a = sp.Eq(-k**2 * phiF, 4 * sp.pi * sp.Symbol("G") * rho_m + fourpiG_rho_tau_11.subs(Xs, phiF))
eq13 = sp.Eq(-(1 + JY) * k**2 * phiF + mu**2 * phiF, 4 * sp.pi * sp.Symbol("G") * rho_m)
ok11b = zero(sp.solve(eq10a, phiF)[0] - sp.solve(eq13, phiF)[0])
check("S11_BS25_Eq11_equals_Q6", ok11a and ok11b,
      f"2x Eq.11 (J_Y = -1, static) = Q6 8piG drho (j1 = {J1}): {ok11a}; Eq.10a + Eq.11 at Xi = phi -> Eq.13 (any J_Y): {ok11b}",
      "exact")

# ------------------------------------------------------------------ exports for the patch / native steps
RES["coded_forms"] = {"Z": "K'/(2 mu^2)", "r": "sqrt(1 + lambda_D Z^2)", "Qbar": "1 + Z/r", "K": "2 mu^2 Z^2/(r(r+1))",
                      "Kpp": "2 mu^2 r^3", "ca2": "Z/(r^2 (r + Z))", "8piG_rho": "2 mu^2 Z + 2 mu^2 Z^2/(r+1)",
                      "cs2_rest": "Qbar K'/(Qbar^2 K'' - 2 j1 k^2/a^2), j1 = -1", "M2_kernel": "Qbar^2 K''/2"}
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"q7_source_results{TAG}.json"), "w"), indent=1)
P(f"Q7_SOURCE COMPLETE: {NP}/{NC} checks PASS. ({RES['elapsed_s']} s)")
OUT.close()
sys.exit(0 if NP == NC else 1)
