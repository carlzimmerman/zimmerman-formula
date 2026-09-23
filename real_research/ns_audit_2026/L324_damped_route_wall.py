#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L324 -- SWING 2: THE DAMPED ROUTE TO CLAY, CARRIED TO THE WALL.  d_t u - nu Lap u + (u.grad)u + c|u|^(b-1)u + grad p
= 0 with c -> 0 (the campaign's ZNS family, N03/N03b), step by step, until a step fails.

THE ROUTE
  Prove the damped system smooth at fixed c > 0, then pass c -> 0 with c-uniform bounds to reach NSE.

WHAT THIS LANE SHOWS
  W1 THE c-UNIFORM INFORMATION IS LERAY-HOPF.  The energy identity  ||u(t)||^2 + 2 nu int||grad u||^2 +
     2c int int |u|^(b+1) = ||u0||^2  bounds L^inf L^2 and L^2 H^1 independently of c.  Every interpolant has Serrin
     index 2/q + 3/p = 3/2 (symbolic), against the regularity threshold 1: a gap of exactly 1/2.
  W2 THE DAMPING'S OWN BOUND DEGENERATES.  c ||u||^(b+1)_{L^(b+1)_{t,x}} <= ||u0||^2/2: index 5/(b+1), Serrin-class
     iff b >= 4, and the constant ||u0||^2/(2c) diverges as c -> 0.  At b = 3 the index is 5/4: gap 1/4, c-dependent.
  W3 THE CRITICAL MEMBER b = 3 CLOSES ONLY FOR 4 c nu >= 1.  Testing with -Lap u:
        1/2 d_t||grad u||^2 + nu||Lap u||^2 + c|| |u||grad u| ||^2 + (c/2)||grad|u|^2||^2 = int (u.grad)u . Lap u
                                                                                        <= X Y,
     X = || |u||grad u| ||, Y = ||Lap u||; the estimate closes iff nu Y^2 + c X^2 - X Y >= 0 for all X, Y >= 0,
     i.e. iff 4 c nu >= 1 (symbolic).  The integration-by-parts identity is checked numerically on a random smooth
     periodic field.  Every b = 3 result found carries a c*nu threshold: Zhang-Wu-Lu 2011 (JMAA 377, uniqueness,
     4 c nu >= 1); Kim-Li 2017 (EJDE 2017/244, strong solutions, c nu > 1/4, as summarised in arXiv:2410.00457);
     Liu-Gao (arXiv:1608.07996, stochastic, alpha >= 1/2 at b = 3).  Zhou 2012 (AML 25:1822) states "b >= 3" in its
     abstract; its coefficient normalisation could not be read here (publisher 403) -- recorded, not assumed.
     No result for 4 c nu < 1 was found.  c*nu is the ONLY dimensionless parameter at b = 3 (scale-critical).
  W4 THE FRAMEWORK'S c SITS FAR BELOW THE THRESHOLD.  N03b's survival bound c_3 <= 6.55e-30 s/m^2 needs
     nu >= 1/(4 c_3) = 3.8e28 m^2/s for the certified regime; water, air and even a generous 1e24 m^2/s give
     c_3 nu <= 7e-6.  N03b's "b = 3 globally smooth at every fixed kappa > 0" is therefore NOT covered by the
     literature it cites at the framework's own coupling; N03b's Galerkin evidence run (c = 0.3, nu = 5e-3,
     c nu = 1.5e-3) is also outside the certified regime (evidence, not certificate).
  W5 EVERY DOOR HITS THE SAME HALF.  For each quantity X the energy class gives a space; excess over critical,
     per power of u, is 1/2 for u, grad u, p, grad p and the gradient part of Du/Dt (L323's route).  Symbolic table.
  W6 THE PASSAGE c -> 0 IS THE CLAY ESTIMATE.  The b = 3 closure needs c >= 1/(4 nu); the b >= 4 bound diverges
     ~ c^(-1/(b+1)); what survives c -> 0 is W1's Leray-Hopf class with gap 1/2.  Crossing it requires a c-uniform
     critical bound, i.e. an a priori estimate for NSE itself.  Tao 2016 (JAMS 29:601) builds an averaged NSE that
     keeps the energy identity and the harmonic-analysis bounds used in W1-W5 and still blows up: closing the gap
     needs the exact structure of (u.grad)u (documentary).
  MUTATE=1 replaces the +1/2 in the integration-by-parts identity by -1/2: the numerical check must fail and W3 must
  FAIL (rc = 1).

Run from the repository root:  python3 real_research/ns_audit_2026/L324_damped_route_wall.py
"""
import os, sys, json
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L324_damped_route_wall"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L324", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


th, b, c, nu, X, Y = sp.symbols("theta beta c nu X Y", positive=True)

# ============================================================================================ W1
banner("W1  THE c-UNIFORM INFORMATION IS LERAY-HOPF: SERRIN INDEX 3/2 FOR EVERY INTERPOLANT")
# u in L^inf_t L^2_x  and  u in L^2_t L^6_x (Sobolev from L^2 H^1); interpolate with weight theta
inv_q = th / 2                              # 1/q between 1/inf = 0 and 1/2
inv_p = (1 - th) / 2 + th / 6               # 1/p between 1/2 and 1/6
index = sp.simplify(2 * inv_q + 3 * inv_p)
gap_uniform = sp.simplify(index - 1)
P(f"    interpolant L^q L^p: 2/q + 3/p = {index} for every theta in [0,1]; Serrin threshold 1; gap = {gap_uniform}")
OUT["numbers"]["W1"] = {"index": str(index), "gap": str(gap_uniform)}
check("W1 every c-uniform (energy-class) bound sits at Serrin index 3/2: gap 1/2 above the regularity threshold",
      f"index {index}, gap {gap_uniform}", index == sp.Rational(3, 2),
      "the damping adds nothing that survives c -> 0 beyond the Leray-Hopf class")

# ============================================================================================ W2
banner("W2  THE DAMPING'S OWN BOUND: L^(b+1)_{t,x}, INDEX 5/(b+1), CONSTANT ~ 1/c")
idx_b = 5 / (b + 1)
b_serrin = sp.solve(sp.Eq(idx_b, 1), b)[0]
bound = 1 / (2 * c)                         # ||u||^(b+1) <= ||u0||^2/(2c), ||u0|| = 1
lim_c0 = sp.limit(bound ** (1 / (b + 1)), c, 0, "+")
tab = {bv: idx_b.subs(b, bv) for bv in (2, 3, 4, 5)}
P(f"    index(b) = {idx_b}: " + ", ".join(f"b={k}: {v}" for k, v in tab.items()) + f";  Serrin iff b >= {b_serrin}")
P(f"    ||u||_(L^(b+1)) <= (1/(2c))^(1/(b+1)) -> {lim_c0} as c -> 0")
OUT["numbers"]["W2"] = {"index_of_b": str(idx_b), "b_serrin": str(b_serrin), "table": {str(k): str(v) for k, v in tab.items()},
                        "limit_c0": str(lim_c0)}
check("W2 the damping bound is Serrin-class iff b >= 4 and its constant diverges as c -> 0; at b = 3 the index is "
      "5/4 (gap 1/4, c-dependent)", f"b_serrin = {b_serrin}; b=3 index {tab[3]}; c->0 limit {lim_c0}",
      b_serrin == 4 and tab[3] == sp.Rational(5, 4) and lim_c0 == sp.oo,
      "the better-than-Leray-Hopf information is paid for with 1/c")

# ============================================================================================ W3
banner("W3  b = 3: THE H^1 ESTIMATE CLOSES IFF 4 c nu >= 1")
# closes iff q(X,Y) = nu Y^2 + c X^2 - X Y >= 0 on the quadrant  <=>  PSD of [[c, -1/2], [-1/2, nu]]
Mq = sp.Matrix([[c, -sp.Rational(1, 2)], [-sp.Rational(1, 2), nu]])
det = sp.factor(Mq.det())
thr = sp.solve(sp.Eq(det, 0), c)[0]
P(f"    form matrix det = {det}  =>  closes iff c >= {thr}  (i.e. 4 c nu >= 1)")
# numeric integration-by-parts identity on a random smooth periodic field
N = 32
k1 = np.fft.fftfreq(N, 1.0 / N)
K = np.array(np.meshgrid(k1, k1, k1, indexing="ij"))
K2 = (K ** 2).sum(0)
rng = np.random.default_rng(3)
uh = (rng.standard_normal((3, N, N, N)) + 1j * rng.standard_normal((3, N, N, N))) * (np.sqrt(K2) <= 3)
u = np.real(np.fft.ifftn(uh, axes=(1, 2, 3)))
u /= np.sqrt(np.mean(u ** 2))                                  # O(1) amplitude
uh = np.fft.fftn(u, axes=(1, 2, 3))
du = np.real(np.array([[np.fft.ifftn(1j * K[j] * uh[i]) for j in range(3)] for i in range(3)]))   # du[i][j] = d_j u_i
lap = np.real(np.fft.ifftn(-K2 * uh, axes=(1, 2, 3)))
s2 = (u ** 2).sum(0)
s2h = np.fft.fftn(s2)
gs2 = np.real(np.array([np.fft.ifftn(1j * K[j] * s2h) for j in range(3)]))
lhs = np.mean(s2 * (u * (-lap)).sum(0))
coef = -0.5 if MUTATE else 0.5
rhs_ = np.mean(s2 * (du ** 2).sum((0, 1))) + coef * np.mean((gs2 ** 2).sum(0))
rel = abs(lhs - rhs_) / abs(lhs)
P(f"    int |u|^2 u.(-Lap u) = {lhs:.10e};  int |u|^2|grad u|^2 + ({coef:+}) int |grad|u|^2|^2 = {rhs_:.10e};  rel {rel:.1e}")
# confirm the closure boundary numerically: min over the quadrant of q on the unit circle
def qmin(cv, nv):
    ang = np.linspace(0, np.pi / 2, 20001)
    return float(np.min(nv * np.sin(ang) ** 2 + cv * np.cos(ang) ** 2 - np.sin(ang) * np.cos(ang)))
probe = {(0.26, 1.0): qmin(0.26, 1.0), (0.24, 1.0): qmin(0.24, 1.0)}
P(f"    min of the form on the quadrant: c nu = 0.26 -> {probe[(0.26, 1.0)]:+.2e};  c nu = 0.24 -> {probe[(0.24, 1.0)]:+.2e}")
OUT["numbers"]["W3"] = {"det": str(det), "threshold_c": str(thr), "ibp_rel_err": rel, "probe": {str(k): v for k, v in probe.items()},
                        "literature": ["Zhang-Wu-Lu 2011 JMAA 377:414 (b=3 uniqueness, 4 c nu >= 1)",
                                       "Kim-Li 2017 EJDE 2017/244 (b=3 strong, c nu > 1/4; via arXiv:2410.00457)",
                                       "Liu-Gao arXiv:1608.07996 (stochastic, b=3 alpha >= 1/2)",
                                       "Zhou 2012 AML 25:1822 (abstract: b >= 3; normalisation unread)"]}
check("W3 at b = 3 the standard H^1 estimate closes iff 4 c nu >= 1 (symbolic + quadrant probe); the "
      "integration-by-parts identity holds on a random smooth field",
      f"threshold c = {thr}; IBP rel err {rel:.1e}; probe {probe}",
      thr == 1 / (4 * nu) and rel < 1e-10 and probe[(0.26, 1.0)] >= 0 > probe[(0.24, 1.0)],
      "the critical member is certified only above c nu = 1/4; below it no closure is known")

# ============================================================================================ W4
banner("W4  THE FRAMEWORK'S OWN COUPLING vs THE CERTIFIED REGIME")
C3 = 6.54712558141094e-30            # s/m^2, N03b_beta_family_results.json 'c3_survival'
nu_needed = 1 / (4 * C3)
fluids = {"water": 1.0e-6, "air": 1.5e-5, "generous_1e24": 1.0e24}
cnu = {k: C3 * v for k, v in fluids.items()}
galerkin_cnu = 0.3 * 5e-3
P(f"    c_3 <= {C3:.3e} s/m^2 (N03b survival)  =>  certified regime needs nu >= {nu_needed:.2e} m^2/s")
for k, v in cnu.items():
    P(f"    {k:14s} nu = {fluids[k]:.1e} m^2/s  ->  c_3 nu = {v:.2e}  (threshold 0.25)")
P(f"    N03b Galerkin evidence run: c nu = 0.3 * 5e-3 = {galerkin_cnu:.1e}")
OUT["numbers"]["W4"] = {"c3": C3, "nu_needed": nu_needed, "c3_nu": cnu, "galerkin_cnu": galerkin_cnu}
check("W4 at the framework's survival coupling every plausible fluid has c_3 nu << 1/4: N03b's 'b = 3 at every "
      "kappa > 0' is outside the certified regime, and so is its Galerkin evidence run",
      f"nu_needed {nu_needed:.1e} m^2/s; max c_3 nu {max(cnu.values()):.1e}; Galerkin {galerkin_cnu:.1e}",
      nu_needed > 1e28 and max(cnu.values()) < 1e-5 and galerkin_cnu < 0.25,
      "a second b-overreach in N03b (after the b = 2 one it already amended)")

# ============================================================================================ W5
banner("W5  EVERY DOOR HITS THE SAME HALF-DERIVATIVE")
# (quantity, scaling weight, degree in u, energy-class space L^q_t L^p_x as (q, p))
R = sp.Rational
rows = [("u", 1, 1, (R(10, 3), R(10, 3))),
        ("grad u (and vorticity)", 2, 1, (2, 2)),
        ("p = RR(u u)", 2, 2, (R(5, 3), R(5, 3))),
        ("grad p = -Q(Du/Dt)  [L323 route]", 3, 2, (R(5, 4), R(5, 4)))]
table = {}
for name, wgt, deg, (q, p) in rows:
    idx = 2 / sp.S(q) + 3 / sp.S(p)
    table[name] = {"index": str(idx), "critical": wgt, "excess_per_u": str((idx - wgt) / deg)}
    P(f"    {name:34s} energy class L^{q}_t L^{p}_x: index {idx}, critical {wgt}, excess per power of u {(idx - wgt) / deg}")
OUT["numbers"]["W5"] = table
check("W5 u, grad u, p, grad p (= the gradient part of Du/Dt) all sit exactly 1/2 per power of u above critical",
      {k: v["excess_per_u"] for k, v in table.items()}, all(v["excess_per_u"] == "1/2" for v in table.values()),
      "the pressure, acceleration and vorticity doors are the same wall in different currencies")

# ============================================================================================ W6
banner("W6  THE PASSAGE c -> 0")
need_c = thr.subs(nu, 1)
lim_b3 = sp.limit(c - need_c, c, 0, "+")
P(f"    b = 3 closure needs c >= 1/(4 nu); at nu = 1: c - 1/4 -> {lim_b3} < 0 as c -> 0 (closure lost)")
P(f"    b >= 4: constant (1/(2c))^(1/(b+1)) -> oo;  surviving c-uniform class: Leray-Hopf, gap {gap_uniform}")
check("W6 as c -> 0 the b = 3 closure is lost and the b >= 4 constants diverge; only the gap-1/2 class survives, "
      "so the route needs an NSE a priori estimate (the Clay problem) to finish",
      f"c - 1/(4 nu) -> {lim_b3}; W2 limit {lim_c0}; gap {gap_uniform}",
      lim_b3 < 0 and lim_c0 == sp.oo and gap_uniform == sp.Rational(1, 2),
      "the break point, named: a c-uniform critical bound; Tao 2016 says it must use the exact form of (u.grad)u")

# ============================================================================================ verdict
banner("VERDICT")
P("""  Swing 2 breaks at a named step.  Damping at b >= 4 (any c) and b = 3 with 4 c nu >= 1 give smooth solutions,
  but every closing constant degenerates as c -> 0; what survives is the Leray-Hopf class, a half-derivative
  short of regularity, and the pressure, acceleration and vorticity routes sit on the same half (W5).  The
  framework's own survival coupling puts c_3 nu below 1e-5, outside even the certified b = 3 regime, so N03b's
  'b = 3 at every kappa > 0' needs amending.  Finishing the route requires a c-uniform critical estimate: that
  estimate is the Clay problem, and Tao's averaged-NSE blowup says it must use the exact structure of (u.grad)u.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
