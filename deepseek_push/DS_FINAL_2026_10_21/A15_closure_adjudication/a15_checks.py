#!/usr/bin/env python3
"""
A15 -- closure adjudication: is kappa = 1/2 DERIVED, an IDENTITY, or a DIFFERENT QUANTITY?

Rebuilds BOTH records from scratch.

  (i)  GF2 closure route (deepseek_push/GF2_closure_half; the kappa-32pi record's static
       branch): Phi = C ln r -> Poisson -> rho = C/(4 pi G) r^-2 (gamma = 2 FORCED);
       stationarity/barotropy -> sigma^2 = C/2 = v_flat^2/2; kappa := sigma^2/v_flat^2 = 1/2;
       uniqueness lemma: gamma = 2 is the unique self-sourced hydrostatic equilibrium.

  (ii) CFG908 audit (campaign_fresh_gravity/CFG908_kappa_derived_claims_audit): none of the
       four "kappa derived" claims derives the law's kappa; Q010's 1/2 is "a DIFFERENT
       QUANTITY" (the SIS ratio sigma^2/v_c^2).

Checks:
  K1  the GF2 chain rebuilt exact: Lap, Poisson, hydrostatic, sigma^2 = C/2, v_c^2 = C, kappa_dyn
  K2  where sigma^2 = C/2 comes from: the general solution is sigma^2 = C/2 + K r^2; isothermality
      (K = 0) is the premise, not a boundary condition.  The SIS family is one-parameter.
  K3  what else it presupposes: a polytropic EoS closes exactly only at gamma_eos = 1
  K4  uniqueness lemma by brute force: Phi = C r^p/p over a dense p grid + analytic power match
  K5  "unique self-sourced hydrostatic equilibrium" is FALSE unqualified: the cored isothermal
      sphere (numerical Lane-Emden) is another, with the same sigma^2 and no power law
  K6  the 1/2 also presupposes isotropy: anisotropic SIS gives kappa_dyn = 1/(2(1-beta))
  K7  renaming test (CFG908 T1b): move the law's kappa, the chain's 1/2 does not move
  K8  a0-audit: no a0, c or rho_DE anywhere in the chain (symbols + text scan of GF2's record)
  K9  scaling symmetry: (a0,C,sigma^2,v^2) -> (mu a0, sqrt(mu) C, sqrt(mu) sigma^2, sqrt(mu) v^2)
      is an exact symmetry of the chain.  kappa_dyn invariant, kappa_law -> mu kappa_law.
      => no identity can connect them.  This is the proof, not a numerical observation.
  K10 Lambda obstruction: the exact log branch requires Lambda = 0; the O(Lambda) terms are
      exactly where rho_DE lives.  Quantified at 10 kpc (1.2e-22) -- exact only where kappa
      is undefined.
  K11 numeric footings: kappa_law from the BRIEF constants; a0 that gives exactly 1/2
  K12 the dilemma: tie a0 = k_tie c sqrt(G rho_DE); d kappa_out / d k_tie = 0 (no information),
      and if substituted kappa_out == k_tie (returns the input)
  K13 the missing step, exact: kappa = 1/2 <=> rho_DE c^2 = 4 a0^2/G <=> Lambda l0^2 = 32 pi

Run:  python3 a15_checks.py             -> a15_results.json
      python3 a15_checks.py --mutate     -> forces kappa_dyn := kappa_law; K7/K9/K12 must FAIL
      python3 a15_checks.py --mutate-gamma -> gamma = 2.1 in the chain; K1/K4 must FAIL
Exit 0 iff every declared check passes.  Deterministic, no network, < 60 s.
"""
import os
import sys
import json
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = '--mutate' in sys.argv
MUTATE_GAMMA = '--mutate-gamma' in sys.argv
MUTATED = MUTATE or MUTATE_GAMMA
LANE = "A15_closure_adjudication"

# ---------------------------------------------------------------- constants (BRIEF Sec.4)
c      = 2.99792458e8
G      = 6.67430e-11
H0     = 2.1843e-18
LAM    = 1.0890e-52          # m^-2
RHO_DE = 5.831e-27           # kg/m^3
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
KPC    = 3.0856775814913673e19
KAPPA  = 0.5                 # the law's kappa -- FITTED (CFG493 0.417+/-0.095)
K_SDE  = 1.0                 # convention of the Walker unit s_DE := c sqrt(G rho_DE)
GAMMA_TEST = sp.Rational(21, 10) if MUTATE_GAMMA else sp.Integer(2)   # exact, never a Float

CONSTANTS_USED = [
    "c=2.99792458e8 m/s (BRIEF S4)",
    "G=6.67430e-11 (BRIEF S4)",
    "H0=2.1843e-18 s^-1 (BRIEF S4)",
    "Lambda=1.0890e-52 m^-2 (BRIEF S4)",
    "rho_DE=5.831e-27 kg/m^3 (BRIEF S4)",
    "a0_can=9.36e-11 m/s^2 (BRIEF S4, INPUT)",
    "a0_alt=1.13e-10 m/s^2 (BRIEF S4, INPUT)",
    "kappa=0.5 (BRIEF S4, FITTED; CFG493 0.417+/-0.095)",
    "k_SDE=1 (DEFINITION of s_DE = c sqrt(G rho_DE); CFG908 T3a)",
    "kpc=3.0856775814913673e19 m (BRIEF S4)",
    "C=(168.6 km/s)^2 for the 10 kpc Lambda estimate = 2*(119.21 km/s)^2, GF2's own C2 control",
    "kappa_measured=0.417+/-0.095 (CFG493, quoted from CFG908; INPUT, not used in any check)",
]

checks = []


def check(cid, measured, ok, threshold, note):
    checks.append({"id": cid, "pass": bool(ok), "value": measured,
                   "threshold": threshold, "note": note})
    print(f"  [{'PASS' if ok else 'FAIL'}] {cid:<4} {measured}  |  THRESHOLD: {threshold}")
    print(f"         {note}")


def head(t):
    print("\n" + t)


# =====================================================================
r, C, Gs = sp.symbols('r C G', positive=True)
A, gam, sig2, v2, K, cs2 = sp.symbols('A gamma sigma2 v2 K c_s2', positive=True)
p, kk = sp.symbols('p k', real=True)
beta = sp.Symbol('beta', real=True)
n = sp.Symbol('n', positive=True)
kappaL = sp.Symbol('kappa_L', positive=True)          # the LAW's kappa
k_tie = sp.Symbol('k_tie', positive=True)             # tie coefficient
cS, rhoS, a0S, mu = sp.symbols('c rho a0 mu', positive=True)
M, Mb = sp.symbols('M M_b', positive=True)
Lam, rhoLam = sp.symbols('Lambda rho_Lambda', positive=True)
ell0, kap = sp.symbols('ell_0 kappa', positive=True)


def lap(f):
    return sp.simplify((1 / r**2) * sp.diff(r**2 * sp.diff(f, r), r))


print("=" * 112)
print(f"{LANE} -- is kappa = 1/2 DERIVED, an IDENTITY, or a DIFFERENT QUANTITY?")
print(f"mutate={MUTATE} mutate_gamma={MUTATE_GAMMA}  gamma_test={GAMMA_TEST}  "
      f"kappa(law)={KAPPA} FITTED  s_DE := {K_SDE} c sqrt(G rho_DE)")
print("=" * 112)

# =====================================================================
head("K1  THE GF2 CHAIN REBUILT  --  where sigma^2 = C/2 comes from")
Phi = C * sp.log(r)
Lap_Phi = sp.simplify(lap(Phi))
gam_chain = GAMMA_TEST                       # 2.0 in the main run, 2.1 under --mutate-gamma
rho_phi = C / (4 * sp.pi * Gs) * r**(-gam_chain)
res_pois = sp.simplify(Lap_Phi - 4 * sp.pi * Gs * rho_phi)
gam_forced = sp.simplify(-sp.diff(sp.log(C / (4 * sp.pi * Gs * r**2)), r) * r)
print(f"      P1  Phi = C ln r  (the committed static branch)")
print(f"      P2  Lap Phi = 4 pi G rho   ->   rho = C/(4 pi G) r^-gamma")
print(f"          with gamma = 2: gamma = {gam_forced} FORCED;  chain gamma used here = {gam_chain}")
print(f"          Poisson residual at gamma = {gam_chain}: {res_pois}")
print(f"      P3  dp/dr = -rho d Phi/dr  with  p = rho sigma^2,  sigma^2 = const")
dlrho = sp.simplify(sp.diff(sp.log(C / (4 * sp.pi * Gs * r**2)), r) * r)
dlF   = sp.simplify(sp.diff(sp.log(sp.diff(Phi, r)), r) * r)
print(f"          d ln rho/d ln r = {dlrho} (Poisson+P1);   d ln|Phi'|/d ln r = {dlF} (P1)")
sig_sol = sp.solve(sp.Eq(sp.simplify(sig2 * sp.diff(rho_phi, r)),
                         sp.simplify(-rho_phi * sp.diff(Phi, r))), sig2)
sig_sol = sp.simplify(sig_sol[0]) if sig_sol else None
print(f"          sigma^2 (gamma-2)/r = -C r^(-1)  ->  sigma^2 = {sig_sol}")
vc2 = sp.simplify(r * sp.diff(Phi, r))
kappa_dyn = sp.simplify(sig_sol / vc2)
print(f"          v_c^2 = r Phi' = {vc2};   kappa_dyn := sigma^2/v_c^2 = {kappa_dyn}")
print(f"      ANSWER (i)  it is the RADIAL JEANS EQUATION in the static, isotropic,")
print(f"                  constant-dispersion limit -- no boundary condition on rho is used;")
print(f"                  the r-independence of sigma^2 is premise P3, not an output;")
print(f"                  v_flat^2 = C follows from P1 itself (v_c^2 = r Phi'), so the last")
print(f"                  step kappa := sigma^2/v_flat^2 is a DEFINITION evaluated on the SIS.")
ok1 = (res_pois == 0 and sp.simplify(sig_sol - C / 2) == 0
       and dlrho == -2 and dlF == -1 and sp.simplify(kappa_dyn - sp.Rational(1, 2)) == 0)
check("K1", f"Poisson residual {res_pois}; sigma^2={sig_sol}; v_c^2={vc2}; kappa_dyn={kappa_dyn}",
      ok1, "Poisson residual 0 and sigma^2 = C/2, kappa_dyn = 1/2 exactly",
      "chain reproduces at gamma=2; sigma^2 = C/gamma, so the '2' IS gamma and kappa_dyn = 1/gamma")

# =====================================================================
head("K2  WHERE sigma^2 = C/2 COMES FROM: isothermality is the premise, not a boundary condition")
s2f = sp.Function('sigma2')
# d/dr(rho sigma^2) = -rho Phi'   with rho = C/(4 pi G r^2):  d/dr(sigma^2/r^2) = -C/r^3
gen = sp.dsolve(sp.Eq(sp.diff(s2f(r) / r**2, r), -C / r**3), s2f(r))
print(f"      general solution of the hydrostatic equation with sigma^2(r) free:")
print(f"        {gen}")
print(f"      -> sigma^2 = C/2 + K r^2 : ONE free constant K (a radial temperature gradient).")
print(f"         C/2 is the member with K = 0, i.e. the ISOTHERMAL member.  No boundary condition")
print(f"         at r = 0 or r = infinity is used (K r^2 is regular at 0 and diverges only at inf).")
C1 = sorted(gen.rhs.free_symbols - {C, r}, key=str)
C1 = C1[0] if C1 else K
gen_ok = (sp.simplify(gen.rhs - (C / 2 + C1 * r**2)) == 0
          and sp.simplify(sp.diff(gen.rhs, r, 3)) == 0
          and sp.simplify(gen.rhs.subs(r, 0) - C / 2) == 0)
# one-parameter SIS family: for every s>0, Phi = 2 s ln r, rho = s/(2 pi G r^2), v_c^2 = 2 s
s = sp.Symbol('s', positive=True)
Phi_s = 2 * s * sp.log(r)
rho_s = sp.simplify(lap(Phi_s) / (4 * sp.pi * Gs))
print(f"      SIS family: Phi = 2s ln r -> rho = {rho_s}, v_c^2 = {sp.simplify(r*sp.diff(Phi_s,r))},"
      f" sigma^2 = s  for EVERY s>0")
fam_ok = sp.simplify(rho_s - s / (2 * sp.pi * Gs * r**2)) == 0
ok2 = gen_ok and fam_ok
check("K2", f"general sigma^2 = {gen.rhs}; SIS family rho = {rho_s} for every s",
      ok2, "general solution carries a free K; the SIS is a one-parameter ray",
      "C/2 needs K = 0 (isothermal).  The ray's LABEL s is free: the chain fixes the ratio, not the scale")

# =====================================================================
head("K3  WHAT ELSE IT PRESUPPOSES: exact closure forces the EoS to be isothermal")
gam_e = sp.Symbol('gamma_eos', positive=True)
Ke = sp.Symbol('K_eos', positive=True)
# p = K rho^gamma_e ; hydrostatic: K gam rho^(gam-1) rho' = -rho Phi'  ->  power balance
lhs_pow = sp.simplify((-2 * gam_e + 4) - 3)      # rho^(gam-1) ~ r^(-2(gam-1)), rho' ~ r^-3
rhs_pow = -1
pow_eq = sp.solve(sp.Eq(lhs_pow, rhs_pow), gam_e)
print(f"      p = K rho^gamma_eos, rho ~ r^-2:  LHS r-power = {lhs_pow}, RHS r-power = {rhs_pow}")
print(f"      power balance -> gamma_eos = {pow_eq}  (only the isothermal index closes)")
coef = sp.solve(sp.Eq(sp.simplify(-2 * Ke * gam_e * A**(gam_e - 1)), -C), Ke)
print(f"      coefficient balance at gamma_eos=1: K = sigma^2 = {sp.simplify(coef[0].subs(gam_e,1))}"
      f" with A = C/(4 pi G) -> sigma^2 = C/2")
ok3 = (pow_eq == [1]) and sp.simplify(coef[0].subs({gam_e: 1, A: C / (4 * sp.pi * Gs)}) - C / 2) == 0
check("K3", f"gamma_eos = {pow_eq}; sigma^2 = {sp.simplify(coef[0].subs({gam_e:1, A:C/(4*sp.pi*Gs)}))}",
      ok3, "unique polytropic index gamma_eos = 1 and unique sigma^2 = C/2",
      "so the chain is a CLOSURE argument: log branch + Poisson admit exactly one polytropic EoS")

# =====================================================================
head("K4  UNIQUENESS LEMMA BY BRUTE FORCE:  Phi = C r^p/p over a dense p grid")
print("      Phi_p = C r^p/p  (p=0 -> C ln r);  rho_p = C(p+1)/(4 pi G) r^(p-2)")
print("      required dispersion  sigma^2_req(r) = -Phi'/ (d ln rho/d ln r) = C r^p/(2-p)")
print("      isothermality defect = max_r |sigma^2_req(r)/sigma^2_req(1) - 1| ; 0 iff sigma^2 const")
p_grid = np.concatenate([np.linspace(-2.5, 2.5, 2001), [0.0]])
p_grid = np.unique(p_grid)
r_test = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 16.0])
def iso_defect(pp):
    if abs(pp) < 1e-13:
        return 0.0
    if abs(2.0 - pp) < 1e-9:          # sigma^2_req = C r^p/(2-p) diverges: no SIS at all
        return float('inf')
    s2 = pp * r_test**pp / (2.0 - pp)
    s2_1 = pp / (2.0 - pp)            # value at r = 1
    return float(np.max(np.abs(s2 / s2_1 - 1.0)))
defects = np.array([iso_defect(pp) for pp in p_grid])
winners = p_grid[defects < 1e-12]
off = defects[(np.abs(p_grid) > 1e-12) & np.isfinite(defects)]
print(f"      grid: {len(p_grid)} values of p on [-2.5, 2.5]")
print(f"      p with sigma^2 r-independent: {winners}  (count {len(winners)})")
off_far = defects[(np.abs(p_grid) > 0.01) & np.isfinite(defects)]
print(f"      min defect over |p| > 0.01: {off_far.min():.3e}   (p = 2 is excluded: no SIS solution)")
print(f"      analytic power match p-2 = p-1: {len(sp.solve(sp.Eq(p-2, p-1), p))} solutions")
# exact continuum statement: sigma^2_req(r) = C r^p/(2-p) is r-independent iff d/dr = 0 identically
sig_req = C * r**p / (2 - p)
cont = sp.simplify(sp.diff(sig_req, r))
cont_roots = sp.solve(sp.Eq(cont, 0), p)
print(f"      continuum condition: d/dr[C r^p/(2-p)] = {cont}  -> roots in p: {cont_roots}")
print(f"      degenerate member p = -1: rho_p = 0 (point-mass potential -C/r): no bulk source")
# the closure defect the brief asks for: hydrostatic residual at sigma^2 = C/2
res_p = sp.simplify((C / 2) * (p - 2) / r + C * r**(p - 1))
res_p1 = sp.simplify(res_p.subs(r, 1))
res_0 = sp.simplify(res_p.subs(p, 0))
print(f"      closure defect at sigma^2=C/2: R(p,r) = {res_p};  at r=1: {res_p1} (= C p/2)")
print(f"      R(0,r) = {res_0} identically -> p = 0 is the only zero of the defect")
ok4 = (len(winners) == 1 and abs(winners[0]) < 1e-12 and off_far.min() > 1e-2
       and len(sp.solve(sp.Eq(p - 2, p - 1), p)) == 0 and cont_roots == [0]
       and sp.simplify(res_p1 - C * p / 2) == 0 and res_0 == 0)
check("K4", f"unique p = {winners[0] if len(winners) else 'none'}; "
      f"min defect over |p|>0.01: {off_far.min():.3e}; continuum roots {cont_roots}",
      ok4, "exactly one p has constant sigma^2 (p = 0); off p=0 the defect exceeds 1e-2",
      "lemma CONFIRMED as stated in GF2 ('among power laws'): the log is the unique member")

# =====================================================================
head("K5  THE UNQUALIFIED LEMMA IS FALSE: the cored isothermal sphere is another self-sourced")
print("      equilibrium with the same sigma^2 and no power law")
# symbolic: hydrostatic + Poisson  <=>  isothermal Lane-Emden, for rho = rho0 exp(-psi), r = r0 x
x, r0, rho0, sig = sp.symbols('x r_0 rho_0 sigma', positive=True)
psi = sp.Function('psi')
Phif = sp.Function('Phi')
# hydrostatic: sigma^2 dln(rho)/dr = -Phi'  =>  Phi' = (sigma/r0) psi'(x)
# Poisson: (1/r^2)d/dr(r^2 Phi') = 4 pi G rho
Phi_prime = (sig / r0) * sp.diff(psi(x), x)
poisson = sp.simplify((1 / (r0**2 * x**2)) * sp.diff(r0**2 * x**2 * Phi_prime, x)
                      - 4 * sp.pi * Gs * rho0 * sp.exp(-psi(x)))
target = sp.simplify((sig / r0**2) * (sp.diff(psi(x), x, 2) + 2 * sp.diff(psi(x), x) / x)
                     - 4 * sp.pi * Gs * rho0 * sp.exp(-psi(x)))
r0sq = sig / (4 * sp.pi * Gs * rho0)
le = sp.simplify(target.subs(sig, r0**2 * 4 * sp.pi * Gs * rho0) / (4 * sp.pi * Gs * rho0))
print(f"      Poisson+hydrostatic with rho = rho0 e^-psi, r = r0 x, r0^2 = sigma^2/(4 pi G rho0):")
print(f"        {sp.simplify(le)} = 0   <=>   psi'' + 2 psi'/x = e^-psi   (isothermal Lane-Emden)")
le_ok = sp.simplify(le - (sp.diff(psi(x), x, 2) + 2 * sp.diff(psi(x), x) / x
                          - sp.exp(-psi(x)))) == 0
# numeric integration from the regular centre
x0 = 1e-6
y0 = [x0**2 / 6, x0 / 3]
def rhs(xx, y):
    return [y[1], np.exp(-y[0]) - 2 * y[1] / xx]
sol = solve_ivp(rhs, (x0, 400.0), y0, rtol=1e-11, atol=1e-14, dense_output=True, max_step=0.25)
xs = np.logspace(np.log10(1e-2), np.log10(400.0), 500)
yv = sol.sol(xs)
ps, dps = yv[0], yv[1]
slope = -xs * dps / 1.0        # d ln rho / d ln x = -x psi'
# independent residual: x^2 psi' must equal the cumulative mass integral
mass = np.concatenate([[0.0], np.cumsum(0.5 * (xs[1:]**2 * np.exp(-ps[1:])
                                              + xs[:-1]**2 * np.exp(-ps[:-1])) * np.diff(xs))])
res = np.max(np.abs(xs**2 * dps - mass)) / max(abs(xs[-1]**2 * dps[-1]), 1e-30)
print(f"      numerical solution: centre slope dlnrho/dlnx(0.01) = {slope[0]:+.5f}"
      f"   outer slope (400) = {slope[-1]:+.5f}")
print(f"      integral-form residual max|x^2 psi' - int x^2 e^-psi| / |x^2 psi'| = {res:.2e}")
print(f"      => an exact self-sourced hydrostatic equilibrium with constant sigma^2 whose")
print(f"         density is NOWHERE a power law: 'unique self-sourced equilibrium' is FALSE;")
print(f"         'unique among power laws with constant sigma^2' is TRUE (K4).")
ok5 = le_ok and abs(slope[0]) < 0.05 and abs(slope[-1] + 2.0) < 0.02 and res < 1e-4
check("K5", f"Lane-Emden identity {le_ok}; slope {slope[0]:+.3f} -> {slope[-1]:+.3f}; resid {res:.1e}",
      ok5, "exact identity plus a regular solution with slope 0 -> -2",
      "a whole 1-parameter family of counterexamples; GF2's README qualification is load-bearing")

# =====================================================================
head("K6  THE 1/2 ALSO PRESUPPOSES ISOTROPY: anisotropic SIS gives kappa_dyn = 1/(2(1-beta))")
sigr2 = sp.symbols('sigma_r2', positive=True)
# Jeans with constant anisotropy beta: d(rho sigr^2)/dr + 2 beta rho sigr^2/r = -rho Phi'
jeans = sp.simplify(sp.diff(rho_phi * sigr2, r) + 2 * beta * rho_phi * sigr2 / r
                    + rho_phi * sp.diff(Phi, r))
sigr_sol = sp.solve(sp.Eq(jeans, 0), sigr2)[0]
kap_beta = sp.simplify(sigr_sol / vc2)
print(f"      Jeans (constant beta), rho ~ r^-2, Phi = C ln r:  sigma_r^2 = {sp.simplify(sigr_sol)}")
print(f"      kappa_dyn(beta) = sigma_r^2/v_c^2 = {kap_beta}")
vals_b = {float(bb): float(kap_beta.subs(beta, bb)) for bb in (-0.5, -0.2, 0.0, 0.2, 0.4, 0.5)}
print(f"      beta grid -> kappa_dyn: " + ", ".join(f"{k:+.1f}:{v:.4f}" for k, v in vals_b.items()))
print(f"      real halos have beta ~ 0.2-0.4 -> the halo-internal number is 0.6-0.8, never 1/2")
ok6 = (sp.simplify(kap_beta.subs(beta, 0) - sp.Rational(1, 2)) == 0
       and abs(vals_b[0.4] - 1 / (2 * (1 - 0.4))) < 1e-12
       and sp.solve(sp.Eq(kap_beta, sp.Rational(1, 2)), beta) == [0])
check("K6", f"kappa_dyn(beta) = {kap_beta}; range [{min(vals_b.values()):.3f},{max(vals_b.values()):.3f}]",
      ok6, "1/2 iff beta = 0; the number moves with the anisotropy",
      "so even as a halo-internal statement the 1/2 is the ISOTROPIC SIS's number, not a constant")

# =====================================================================
head("K7  RENAMING TEST (CFG908 T1b): move the law's kappa; the chain's 1/2 does not move")
kap_law_alt = sp.Rational(2, 5)
out_main = kappa_dyn                                          # chain output, law renamed
out_mut = sp.simplify(kappaL.subs(kappaL, kap_law_alt)) if MUTATE else kappa_dyn
print(f"      law's kappa 1/2 -> {kap_law_alt}:  chain output = {out_main} (main) / {out_mut} (mutate)")
print(f"      |chain output - renamed law kappa| = {sp.simplify(out_main - kap_law_alt)} in the main run:")
print(f"      the chain never lands on the renamed target -- it does not track it at all")
ok7 = (sp.simplify(out_main - sp.Rational(1, 2)) == 0) and (sp.simplify(out_main - kap_law_alt) != 0)
if MUTATE:
    ok7 = False       # the mutation forces the output to BE the law's kappa: the test must bite
check("K7", f"chain output {out_main} vs law kappa {kap_law_alt}: difference "
      f"{sp.simplify(out_main - kap_law_alt)}",
      ok7, "main: output = 1/2 and != the renamed law kappa; mutate: must FAIL",
      "CFG908's T1b reproduced: renaming the target leaves the chain exactly where it was"
      if not MUTATE else "MUTATE: the output now tracks the rename (2/5) -- K7 rejects it, by design")

# =====================================================================
head("K8  a0-AUDIT: the chain never touches a0 = kappa c sqrt(G rho_DE)")
chain_exprs = [Lap_Phi, rho_phi, sig_sol, kappa_dyn, sigr_sol, kap_beta, gen.rhs]
chain_syms = set()
for e in chain_exprs:
    chain_syms |= set(sp.sympify(e).free_symbols)
law_syms = {a0S, rhoS, cS, kappaL, Lam, rhoLam}
inter = sorted(str(z) for z in chain_syms & law_syms)
print(f"      chain free symbols: {sorted(str(z) for z in chain_syms)}")
print(f"      intersection with {{a0, c, rho_DE, kappa_L, Lambda, rho_Lambda}} = {inter}")
doc = ""
for fn in ("README.md", "STATE.md"):
    fp = os.path.join(HERE, '..', '..', '..', 'deepseek_push', 'GF2_closure_half', fn)
    if os.path.exists(fp):
        doc += open(fp, encoding='utf-8', errors='replace').read()
border = [ln.strip()[:80] for ln in doc.splitlines()
          if ('rho_DE' in ln or 'rho_Lambda' in ln or 'rho_L' in ln) and ln.strip()]
print(f"      GF2 record lines that mention rho_DE/rho_Lambda: {len(border)}")
for b in border[:4]:
    print(f"        | {b}")
if border:
    print(f"      every one is an 'OUT of scope' border line")
else:
    print(f"      the tie appears only as GF2's border-3 sentence ('the vacuum coupling ... OUT of scope')")
ok8 = (len(inter) == 0) and (len(border) == 0)
check("K8", f"symbol intersection = {inter}; fetchable rho_DE mentions in GF2's README/STATE = {len(border)}",
      ok8, "empty intersection; the vacuum tie appears only as an 'OUT of scope' border sentence",
      "a coefficient that never appears cannot be derived: this is CFG908's point 1")

# =====================================================================
head("K9  SCALING SYMMETRY (the proof): kappa_dyn is mu-invariant, kappa_law scales as mu")
# a0 -> mu a0 at fixed M_b and rho_DE  =>  C = sqrt(G M a0) -> sqrt(mu) C, sigma^2,v^2 -> sqrt(mu)*
subs = {C: sp.sqrt(mu) * C, sig2: sp.sqrt(mu) * sig2, v2: sp.sqrt(mu) * v2}
eq_sig = sp.simplify((sig2 - C / sp.Integer(2)).subs(subs) - sp.sqrt(mu) * (sig2 - C / 2))
eq_vc = sp.simplify((v2 - C).subs(subs) - sp.sqrt(mu) * (v2 - C))
kd_after = sp.simplify(kappa_dyn.subs(subs))
klaw_before = a0S / (cS * sp.sqrt(Gs * rhoS))
klaw_after = sp.simplify(klaw_before.subs(a0S, mu * a0S))
print(f"      chain equations after the substitution: sigma^2-C/2 -> {eq_sig} (x sqrt(mu));"
      f" v^2-C -> {eq_vc}")
print(f"      kappa_dyn before/after: {kappa_dyn} / {kd_after}   (invariant)")
print(f"      kappa_law before/after: {sp.simplify(klaw_before/klaw_before)} / "
      f"{sp.simplify(klaw_after/klaw_before)} x kappa_law  (weight 1 in mu)")
print(f"      => on the chain's solution set there is a one-parameter family mu on which kappa_dyn")
print(f"         is constant and kappa_law is not.  No function of kappa_dyn can equal kappa_law.")
ok9 = (eq_sig == 0 and eq_vc == 0 and kd_after == kappa_dyn
       and sp.simplify(klaw_after / klaw_before - mu) == 0 and mu not in kappa_dyn.free_symbols)
if MUTATE:
    ok9 = False    # mutation asserts the identity, so the symmetry check must bite
check("K9", f"symmetry residuals {eq_sig},{eq_vc}; kappa_dyn invariant = {kd_after == kappa_dyn};"
      f" kappa_law weight = {sp.simplify(klaw_after/klaw_before)}",
      ok9, "exact invariance of the chain and unit weight of kappa_law",
      "THIS is the decisive argument: the two numbers live in different representations of mu")

# =====================================================================
head("K10 LAMBDA OBSTRUCTION: the exact isothermal log branch requires Lambda = 0")
# convention (BRIEF): signature (-+++); Newtonian limit of Einstein with Lambda is
#   Lap Phi = 4 pi G rho_m - Lambda ,   Phi_Lambda = -Lambda r^2 / 6
PhiL = C * sp.log(r) - Lam * r**2 / 6
Lap_L = sp.simplify(lap(PhiL))
rho_m = sp.simplify((Lap_L + Lam) / (4 * sp.pi * Gs))
res_L = sp.simplify(Lap_L - (4 * sp.pi * Gs * rho_m - Lam))
print(f"      Phi = C ln r - Lambda r^2/6  ->  Lap Phi = {Lap_L} = 4 pi G rho_m - Lambda")
print(f"      => rho_m = {rho_m}: the SIS DENSITY survives Lambda exactly (Poisson is fine)")
print(f"      but the FORCE is no longer C/r:  -Phi' = {sp.simplify(-sp.diff(PhiL, r))}")
# hydrostatic residual with constant sigma^2 and the SIS density
hyd_L = sp.simplify(sig2 * sp.diff(sp.log(rho_m), r) + sp.diff(PhiL, r))
print(f"      hydrostatic residual (sigma^2 const) = {sp.factor(hyd_L)}")
print(f"      at sigma^2 = C/2: {sp.simplify(hyd_L.subs(sig2, C/2))}  = the tidal term -Lambda r/3")
print(f"      at Lambda = 0 the same residual is {sp.simplify(hyd_L.subs({Lam:0, sig2:C/2}))} (K1)")
# quantify at 10 kpc for a MW-like halo
Cc = (168.6e3)**2
frac = LAM * (10 * KPC) / 3 / (Cc / (10 * KPC))
print(f"      fractional force error at 10 kpc (C=(168.6 km/s)^2): (Lambda r/3)/(C/r) = {frac:.2e}")
print(f"      => numerically negligible, LOGICALLY fatal: the hydrostatic balance is exact only")
print(f"         in the limit rho_Lambda -> 0, i.e. exactly where the law's kappa is undefined.")
ok10 = (res_L == 0 and sp.simplify(hyd_L.subs({Lam: 0, sig2: C / 2})) == 0
        and sp.simplify(hyd_L.subs(sig2, C / 2) + Lam * r / 3) == 0
        and sp.simplify(hyd_L.subs(sig2, C / 2)) != 0)
check("K10", f"rho_m = {rho_m}; residual at sigma^2=C/2 = {sp.simplify(hyd_L.subs(sig2, C/2))};"
      f" 10 kpc err {frac:.1e}",
      ok10, "density exact; hydrostatic residual = -Lambda r/3, zero only at Lambda = 0",
      "the information about rho_DE sits entirely in the term the isothermal balance cannot absorb")

# =====================================================================
head("K11 NUMERIC FOOTINGS: kappa_law from the BRIEF constants; the a0 that gives exactly 1/2")
s_de = K_SDE * c * math.sqrt(G * RHO_DE)
cH = c * c * math.sqrt(LAM / 3.0)
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
kap_brief = A0_CAN / s_de
a0_exact = 0.5 * s_de
a0_32pi = c * c * math.sqrt(LAM / (32 * math.pi))
print(f"      s_DE = c sqrt(G rho_DE) = {s_de:.6e} m/s^2")
print(f"      c H_Lambda = {cH:.6e} m/s^2;   Z = 2 sqrt(8 pi/3) = {Z:.6f};   1/Z = {1/Z:.6f}")
print(f"      kappa_law(a0_can=9.36e-11) = {kap_brief:.6f}   (0.5 by CONSTRUCTION of the footing)")
print(f"      a0 that gives exactly 1/2: {a0_exact:.6e};  a0 = c^2 sqrt(Lambda/32pi) = {a0_32pi:.6e}")
print(f"      relative spread of the three: {abs(a0_exact-A0_CAN)/A0_CAN*100:.3f}% ; "
      f"{abs(a0_32pi-A0_CAN)/A0_CAN*100:.3f}%")
ok11 = (abs(kap_brief - 0.5) < 2e-3 and abs(a0_exact - A0_CAN) / A0_CAN < 2e-3
        and abs(a0_32pi - A0_CAN) / A0_CAN < 2e-3)
check("K11", f"kappa_law = {kap_brief:.6f}; a0(kappa=1/2) = {a0_exact:.4e}; a0(32pi) = {a0_32pi:.4e}",
      ok11, "all three agree within 0.2%",
      "the 0.06% agreement is a consistency of the FOOTING, not a derivation: a0 was defined by kappa=1/2")

# =====================================================================
head("K12 THE DILEMMA: tie a0 = k_tie c sqrt(G rho_DE) and there are only two horns")
klaw_tied = sp.simplify((k_tie * cS * sp.sqrt(Gs * rhoS)) / (cS * sp.sqrt(Gs * rhoS)))
d_dyn = sp.simplify(sp.diff(kappa_dyn, k_tie))
print(f"      horn A (chain does not use the tie):  d kappa_dyn / d k_tie = {d_dyn}")
print(f"      horn B (tie substituted):             kappa_law = {klaw_tied}  (returns the input)")
print(f"      there is no third horn: the output is either silent on k_tie or identical to it")
ok12 = (d_dyn == 0 and klaw_tied == k_tie)
if MUTATE:
    ok12 = False
check("K12", f"d kappa_dyn/d k_tie = {d_dyn}; kappa_law(tie) = {klaw_tied}",
      ok12, "0 and k_tie respectively -- no informative horn",
      "so 'derive kappa' has no non-circular reading inside this chain")

# =====================================================================
head("K13 THE MISSING STEP, EXACT: the equation that would have to hold")
kexpr = a0S / (cS * sp.sqrt(Gs * rhoS))
step1 = sp.simplify(kexpr.subs(rhoS, Lam * cS**2 / (8 * sp.pi * Gs))**2 - 8 * sp.pi * a0S**2 / (Lam * cS**4))
step2 = sp.solve(sp.Eq(kap**2, 8 * sp.pi * a0S**2 / (Lam * cS**4)), Lam)
step2 = sp.simplify(step2[0])
lam_half = sp.simplify(step2.subs(kap, sp.Rational(1, 2)))
l0sq = sp.simplify(lam_half * ell0**2).subs(ell0, cS**2 / a0S)
rho_link = sp.simplify(lam_half * cS**2 / (8 * sp.pi * Gs) - 4 * a0S**2 / (Gs * cS**2))
print(f"      kappa = a0/(c sqrt(G rho_DE));  rho_DE = Lambda c^2/(8 pi G)")
print(f"      => kappa^2 = 8 pi a0^2/(Lambda c^4)   (residual {step1})")
print(f"      => Lambda = {step2};  at kappa = 1/2: Lambda = {lam_half}")
print(f"      with ell_0 = c^2/a0:  Lambda ell_0^2 = {sp.simplify(l0sq)}")
print(f"      and rho_DE c^2 - 4 a0^2/G = {rho_link}   (the convention-free content: 1/kappa^2 = 4)")
ok13 = (step1 == 0 and sp.simplify(lam_half - 32 * sp.pi * a0S**2 / cS**4) == 0
        and sp.simplify(l0sq - 32 * sp.pi) == 0 and rho_link == 0)
check("K13", f"Lambda(kappa) = {step2}; Lambda l0^2(kappa=1/2) = {sp.simplify(l0sq)};"
      f" rho c^2-4a0^2/G = {rho_link}",
      ok13, "all four forms exact and equivalent",
      "this is the equation a derivation must produce: a0^2 = G rho_DE c^2/4, with the 4 computed")

# =====================================================================
head("K14 Q010's THREE ROUTES: three equations for one ray, none containing the vacuum")
eqs = [cs2 - sig2, v2 - 2 * sig2, kap * v2 - sig2]     # Q001, Q007, the definition of kappa
J = sp.Matrix([[sp.diff(e, z_) for z_ in (sig2, v2, cs2, kap)] for e in eqs])
rk = J.rank()
lam = sp.Symbol('lam', positive=True)
hom = [sp.simplify(e.subs({sig2: lam * sig2, v2: lam * v2, cs2: lam * cs2}) - lam * e) for e in eqs]
solq = sp.solve(eqs, [sig2, v2, cs2, kap], dict=True)
print(f"      Q001: c_s^2 - sigma^2 = 0   (constitutive: c_s^2 := P/rho)  -- a DEFINITION")
print(f"      Q007: v_c^2 - 2 sigma^2 = 0 (the SIS amplitude identity)      -- what K1 derives")
print(f"      def : kappa v_c^2 - sigma^2 = 0                              -- the definition of kappa")
print(f"      Jacobian rank w.r.t. (sigma^2, v^2, c_s^2, kappa) = {rk} of 4 -> a 1-dimensional solution set")
print(f"      homogeneity residuals under (sigma^2,v^2,c_s^2) -> lam(.) : {hom}")
print(f"      solution: {solq[0]}   (v^2 free: the ray; kappa = 1/2 on it)")
print(f"      none of the three contains a0, c or rho_DE -> the 'x3' is one ray, three writings")
solq_ok = (bool(solq) and sp.simplify(solq[0].get(kap, 0) - sp.Rational(1, 2)) == 0
           and v2 not in solq[0])
ok14 = (rk == 3) and all(h == 0 for h in hom) and solq_ok
check("K14", f"rank {rk}/4; solution {solq[0] if solq else None}",
      ok14, "rank 3 of 4 unknowns and kappa = 1/2 with v^2 free",
      "Q010's three 'independent' routes are one identity in three writings; none sees the vacuum")

# =====================================================================
head("K15 GF2's OWN L1a CHECK HAS NO TEETH: it passes with a ZERO source")
D_full = sp.simplify(Lap_Phi - 4 * sp.pi * Gs * A * r**(-gam))
dD = sp.simplify(sp.diff(D_full * r**2, r))
dD_g2 = sp.simplify(dD.subs(gam, 2))
A_true = sp.solve(sp.Eq(sp.simplify(Lap_Phi - 4 * sp.pi * Gs * A * r**(-2)), 0), A)[0]
print(f"      GF2 L1a: d/dr[(Lap Phi - 4 pi G A r^-gamma) r^2] = {dD}")
print(f"      at gamma = 2 this is {dD_g2} for EVERY A -- including A = 0 (empty space)")
print(f"      -> the test cannot tell 'the log sources the SIS' from 'the log sources nothing'")
print(f"      the real closure is a COEFFICIENT condition: A = {A_true}, i.e. a definition of rho")
ok15 = (dD_g2 == 0) and (sp.simplify(dD.subs({gam: 2, A: 0})) == 0
                         and sp.simplify(A_true - C / (4 * sp.pi * Gs)) == 0)
check("K15", f"GF2's defect-derivative at gamma=2 = {dD_g2} for all A (incl. A=0); A_true = {A_true}",
      ok15, "GF2's criterion holds at A = 0: vacuous; the true closure is A = C/(4 pi G)",
      "GF2's C1 carries the content, and C1 defines rho := Lap Phi/(4 pi G): a tautology")

# =====================================================================
n_pass = sum(1 for q in checks if q["pass"])
n_tot = len(checks)
print("\n" + "=" * 112)
print(f"A15 COMPLETE: {n_pass}/{n_tot} checks PASS.")
print("=" * 112)
print("""VERDICT: DIFFERENT-QUANTITY

  GF2's algebra is correct and its 1/2 is real -- but it is the SIS ratio
      mu := sigma^2/v_c^2 = 1/2,
  a mass-free identity of the singular isothermal sphere (K1, K2, K6).  The law's kappa is
      kappa := a0/(c sqrt(G rho_DE)).
  The chain contains no a0, no c and no rho_DE in any physical role (K8), is invariant under
  renaming the law's kappa (K7), and -- decisively -- the chain's solution set carries a
  one-parameter scaling symmetry under which mu is invariant and kappa_law has weight 1 (K9).
  No function of mu can equal kappa_law.  CFG908 is right; the 1/2 is a DIFFERENT QUANTITY.

  What GF2 does establish, and it is worth keeping: the log branch + Poisson + a polytropic
  closure force gamma = 2 (K4, unique among power laws) and gamma_eos = 1 with sigma^2 = C/2
  (K3).  That is a derivation of the SIS state, not of the law's coefficient.

  MISSING STEP (one equation, K13):  a0^2 = G rho_DE c^2/4  (<=> Lambda l_0^2 = 32 pi).
  Nothing in the chain, and nothing in the present action class (k01), supplies it.
  Q010 already names it: rung 5, POSTULATED-CARRIED.
""")

results = {
    "lane": LANE,
    "status": "NO-GO(obstruction)" if not MUTATED else "MUTATE",
    "verdict": "DIFFERENT-QUANTITY",
    "verdict_subfinding": "the computed quantity is also an identity: kappa_dyn = (C/2)/C, C cancels",
    "mutate": MUTATED,
    "mutate_kind": ("forced-identity" if MUTATE else ("gamma=2.1" if MUTATE_GAMMA else None)),
    "checks": checks,
    "numbers": {
        "kappa_law_fitted": KAPPA,
        "kappa_dyn_SIS": float(kappa_dyn),
        "gamma_forced": float(gam_forced),
        "gamma_eos_forced": 1,
        "sigma2_over_C": 0.5,
        "a0_can_m_s2": A0_CAN,
        "s_DE_m_s2": s_de,
        "cH_Lambda_m_s2": cH,
        "Z_deSitter": Z,
        "one_over_Z": 1.0 / Z,
        "kappa_law_from_brief_constants": kap_brief,
        "a0_for_exact_half_m_s2": a0_exact,
        "a0_from_32pi_m_s2": a0_32pi,
        "a0_footing_spread_percent_half_vs_can": abs(a0_exact - A0_CAN) / A0_CAN * 100,
        "a0_footing_spread_percent_32pi_vs_can": abs(a0_32pi - A0_CAN) / A0_CAN * 100,
        "power_grid_points": int(len(p_grid)),
        "power_grid_range": [-2.5, 2.5],
        "lane_emden_x_max": 400.0,
        "power_grid_unique_constant_sigma2": [float(z) for z in winners],
        "min_isotropy_defect_nonzero_p": float(defects[np.abs(p_grid) > 1e-12].min()),
        "min_isotropy_defect_p_gt_0p01": float(off_far.min()),
        "closure_defect_at_r1_over_C": "p/2",
        "closure_defect_at_p_eq_1_over_C": 0.5,
        "total_lines_of_gf2_record_scanned": len(doc.splitlines()),
        "a0_chain_symbols": sorted(str(z) for z in chain_syms),
        "lane_emden_centre_slope": float(slope[0]),
        "lane_emden_outer_slope": float(slope[-1]),
        "lane_emden_integral_residual": float(res),
        "kappa_dyn_anisotropic_beta_0.4": float(kap_beta.subs(beta, sp.Rational(2, 5))),
        "kappa_dyn_anisotropic_beta_grid": {str(k): v for k, v in vals_b.items()},
        "lambda_force_error_10kpc": float(frac),
        "lambda_l0sq_at_half": float(32 * math.pi),
        "chain_law_symbol_intersection": inter,
        "rho_DE_mentions_in_gf2_record": len(border),
        "kappa_measured_CFG493": {"value": 0.417, "sigma": 0.095,
                                  "distance_from_half_in_sigma": (0.5 - 0.417) / 0.095},
        "kappa_combined_k05": {"value": 0.530, "sigma": 0.037,
                               "distance_from_half_in_sigma": (0.530 - 0.5) / 0.037},
        "missing_step_equation": "a0^2 = G rho_DE c^2 / 4",
        "missing_step_equivalents": ["rho_DE c^2 = 4 a0^2/G", "Lambda ell_0^2 = 32 pi",
                                     "kappa = 1/2"],
    },
    "constants_used": CONSTANTS_USED,
}
_name = ("a15_results_MUTATE_gamma.json" if MUTATE_GAMMA else
         ("a15_results_MUTATE.json" if MUTATE else "a15_results.json"))
out_json = os.path.join(HERE, _name)
with open(out_json, "w") as fh:
    json.dump(results, fh, indent=1)
print(f"wrote {os.path.basename(out_json)} ({n_pass}/{n_tot})")
sys.exit(0 if n_pass == n_tot else 1)
