#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA2 -- SWING 1: THE SCALE-INVARIANT WINDOW THEOREM.  A material-acceleration regularity criterion for 3D NSE,
and why a0 cannot appear in it.

THE UPGRADE
  N05's hypothesis sup|Du/Dt| <= 3.5 a0 is a dimensional ceiling: true for any constant (NSA1 K1) and not invariant
  under the NSE scaling.  The natural theorem puts the material acceleration a := Du/Dt = d_t u + (u.grad)u in a
  scale-invariant (critical) space.

THEOREM (conditional regularity, not Clay).  Let u be a Leray-Hopf weak solution of 3D NSE on R^3 with pressure p.
  (i)  If a in L^s(0,T; L^r(R^3)) with 2/s + 3/r = 3, 1 < r <= 3, then u is smooth on (0,T].
  (ii) If a in L^{s,inf}(0,T; L^{r,inf}(R^3)) with 2/s + 3/r = 3, 1 < r < inf, and that Lorentz norm is below an
       absolute epsilon, then u is smooth on (0,T].
PROOF (three lines).  a = nu Lap u - grad p.  Let Q = I - P be the projection onto gradients (Q^ = xi xi^T/|xi|^2).
  div u = 0 gives Q(Lap u) = 0, and Q(grad p) = grad p, so  grad p = -Q a  EXACTLY.  Q = R (x) R (Riesz transforms)
  is bounded on L^r (1<r<inf) and on L^{r,inf}, so ||grad p|| <= C_r ||a|| in the same space.  Now apply the
  pressure-gradient criterion: grad p in L^s L^r, 2/s+3/r = 3, r > 1 => smooth (Berselli-Galdi 2002 Proc. AMS 130;
  Struwe 2007 JMFM 9; Zhou 2004 Math. Ann. 328 / 2006 Proc. AMS 134), for (ii) Ji-Wang-Wei 2019 arXiv:1909.09960
  Thm 1.1(2).  The r <= 3 cap in (i) is forced by s >= 1.  QED.
Novelty label [B/C]: a corollary of cited criteria through one exact identity.  One literature search found no
  explicit acceleration statement; that is not a priority claim.

WHAT THIS LANE CHECKS
  T1 scaling: a_l = l^3 a(l x, l^2 t), so ||a_l||_{L^s L^r} = l^{3-2/s-3/r} ||a||: critical line 2/s+3/r = 3,
     the same line as grad p (1.5).  N05's (s,r) = (inf,inf) point is off the line (index 0).
  T2 the identity grad p = -Q a in Fourier, symbolically (xi generic, u^ orthogonal to xi).
  T3 the identity on a real flow: pseudo-spectral 3D periodic NSE (N=32, RK4, 2/3 dealiasing); a from a CENTRAL
     TIME DIFFERENCE of the evolved field plus (u.grad)u, grad p from the Poisson solve -Lap p = d_i d_j(u_i u_j).
     The gradient part is dt-independent at rounding level (Q d_t u = d_t Q u = 0 exactly); the solenoidal part
     P a = nu Lap u carries the O(dt^2) error, so the L2 Pythagoras defect ||a||^2 - ||grad p||^2 - nu^2||Lap u||^2
     must fall ~dt^2; measured C_r = ||grad p||_r / ||a||_r at r = 3/2, 2, 3 finite and O(1).
  T4 dimensions: no monomial a0^x nu^y is dimensionless (nullspace empty); a critical norm of a carries units
     nu^{2-1/s}.  The scale-invariant theorem has no slot for a0 -- only nu.
  MUTATE=1 projects with P instead of Q: the identity must fail on the flow and T3 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/ns_audit_2026/NSA2_acceleration_criterion.py
"""
import os, sys, json
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "NSA2_acceleration_criterion"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA2", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


# ============================================================================================ T1
banner("T1  SCALING: THE CRITICAL LINE FOR THE MATERIAL ACCELERATION")
lam, s, r = sp.symbols("lambda s r", positive=True)
# ||f(l x, l^2 t)||_{L^s_t L^r_x} = l^{-2/s - 3/r} ||f||;  a_l = l^3 a(l x, l^2 t)
expo = 3 - 2 / s - 3 / r
crit = sp.solve(sp.Eq(expo, 0), s)[0]
r_rng = (sp.solve(sp.Eq(crit, 1), r)[0], sp.limit(crit, r, 1, "+"))
P(f"    ||a_l|| = l^({expo}) ||a||;  critical: s = {sp.simplify(crit)};  s >= 1 <=> r <= {r_rng[0]};  s -> {r_rng[1]} as r -> 1+")
samples = {sp.Rational(3, 2): crit.subs(r, sp.Rational(3, 2)), 2: crit.subs(r, 2), 3: crit.subs(r, 3)}
P(f"    sample critical pairs (r: s): {samples}")
n05_index = 0   # (s,r) = (inf,inf)
OUT["numbers"]["T1"] = {"exponent": str(expo), "s_of_r": str(sp.simplify(crit)), "r_max": str(r_rng[0]),
                        "samples": {str(k): str(v) for k, v in samples.items()}, "N05_index": n05_index}
check("T1 a scales like grad p (weight 3): critical line 2/s + 3/r = 3, r in (1,3]; N05's L^inf ceiling sits at "
      "index 0, off the line", f"s(r) = {sp.simplify(crit)}; r_max = {r_rng[0]}",
      r_rng[0] == 3 and samples[2] == sp.Rational(4, 3) and samples[sp.Rational(3, 2)] == 2,
      "the critical-space hypothesis is invariant under the NSE symmetry; a dimensional ceiling is not")

# ============================================================================================ T2
banner("T2  THE EXACT IDENTITY grad p = -Q(Du/Dt), SYMBOLICALLY")
x1, x2, x3 = sp.symbols("xi1 xi2 xi3", real=True)
xi = sp.Matrix([x1, x2, x3])
nu_s, ph = sp.symbols("nu phat")
w1, w2 = sp.symbols("w1 w2")
# u^ orthogonal to xi: span of two vectors orthogonal to generic xi
e1 = sp.Matrix([x2, -x1, 0]); e2 = xi.cross(e1)
uh = w1 * e1 + w2 * e2
Qhat = xi * xi.T / (xi.T * xi)[0]
ahat = -nu_s * (xi.T * xi)[0] * uh - sp.I * xi * ph          # (nu Lap u - grad p)^
resid = sp.simplify(Qhat * ahat + sp.I * xi * ph)            # Q a + grad p
div_u = sp.simplify((xi.T * uh)[0])
P(f"    xi . u^ = {div_u};  Q^ a^ + (i xi p^) = {list(resid)}")
check("T2 Q(nu Lap u - grad p) = -grad p identically for divergence-free u (Fourier, generic xi)",
      f"residual {list(resid)}", div_u == 0 and all(c == 0 for c in resid),
      "the pressure gradient IS the gradient part of the material acceleration; the viscous term is its solenoidal part")

# ============================================================================================ T3
banner("T3  THE IDENTITY ON A REAL 3D NSE FLOW (pseudo-spectral, periodic)")
N, NU = 32, 0.05
k1 = np.fft.fftfreq(N, 1.0 / N)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K = np.array([KX, KY, KZ])
K2 = KX ** 2 + KY ** 2 + KZ ** 2
K2i = np.where(K2 == 0, 1.0, K2)
DEAL = (np.abs(KX) < N / 3) & (np.abs(KY) < N / 3) & (np.abs(KZ) < N / 3)


def proj_Q(vh):                       # gradient part
    kd = (K * vh).sum(0)
    return K * kd / K2i


def proj_P(vh):
    return vh - proj_Q(vh)


def adv_hat(uh):                      # ((u.grad)u)^, dealiased
    u = np.real(np.fft.ifftn(uh, axes=(1, 2, 3)))
    out = np.zeros_like(uh)
    for i in range(3):
        gi = np.real(np.fft.ifftn(1j * K * uh[i], axes=(1, 2, 3)))
        out[i] = np.fft.fftn((u * gi).sum(0))
    return out * DEAL


def rhs(uh):
    return -proj_P(adv_hat(uh)) - NU * K2 * uh


def rk4(uh, dt):
    k_1 = rhs(uh); k_2 = rhs(uh + 0.5 * dt * k_1); k_3 = rhs(uh + 0.5 * dt * k_2); k_4 = rhs(uh + dt * k_3)
    return uh + dt / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)


rng = np.random.default_rng(20260922)
uh0 = (rng.standard_normal((3, N, N, N)) + 1j * rng.standard_normal((3, N, N, N)))
uh0 *= (np.sqrt(K2) <= 4) & (K2 > 0)
uh0 = np.fft.fftn(np.real(np.fft.ifftn(uh0, axes=(1, 2, 3))), axes=(1, 2, 3))   # real field
uh0 = proj_P(uh0) * DEAL
urms = np.sqrt(np.mean(np.real(np.fft.ifftn(uh0, axes=(1, 2, 3))) ** 2))
uh0 *= 1.0 / urms


def norm_r(fh, rr):
    f = np.real(np.fft.ifftn(fh, axes=(1, 2, 3)))
    mag = np.sqrt((f ** 2).sum(0))
    return (np.mean(mag ** rr)) ** (1.0 / rr)


def measure(dt, t_star=0.4):
    uh = uh0.copy()
    nsteps = int(round(t_star / dt))
    for _ in range(nsteps - 1):
        uh = rk4(uh, dt)
    um, uc = uh, rk4(uh, dt)
    up = rk4(uc, dt)
    a_h = (up - um) / (2 * dt) + adv_hat(uc)                 # Du/Dt from the evolved field
    # pressure: -Lap p = d_i d_j (u_i u_j)  =>  p^ = -(k_i k_j (u_i u_j)^)/k^2 ; grad p^ = i k p^
    u = np.real(np.fft.ifftn(uc, axes=(1, 2, 3)))
    ph_ = np.zeros((N, N, N), complex)
    for i in range(3):
        for j in range(3):
            ph_ += -K[i] * K[j] * np.fft.fftn(u[i] * u[j]) * DEAL
    ph_ = ph_ / K2i * (K2 > 0)                              # k^2 p^ = -k_i k_j (u_i u_j)^
    gp_h = 1j * K * ph_
    proj = proj_P if MUTATE else proj_Q
    res = np.sqrt((np.abs(proj(a_h) + gp_h) ** 2).sum()) / np.sqrt((np.abs(gp_h) ** 2).sum())
    lap_h = -NU * K2 * uc
    pyth = ((np.abs(a_h) ** 2).sum() - (np.abs(gp_h) ** 2).sum() - (np.abs(lap_h) ** 2).sum()) / (np.abs(a_h) ** 2).sum()
    Cr = {rr: norm_r(gp_h, rr) / norm_r(a_h, rr) for rr in (1.5, 2.0, 3.0)}
    return res, pyth, Cr


res1, pyth1, Cr1 = measure(4e-3)
res2, pyth2, Cr2 = measure(2e-3)
order = np.log2(abs(pyth1) / abs(pyth2))                     # the P-part carries the dt^2 error
P(f"    dt = 4e-3: ||Q a + grad p|| / ||grad p|| = {res1:.3e};  Pythagoras defect {pyth1:+.2e}")
P(f"    dt = 2e-3: ||Q a + grad p|| / ||grad p|| = {res2:.3e};  Pythagoras defect {pyth2:+.2e};  defect order {order:.2f}")
P(f"    C_r = ||grad p||_r / ||a||_r at dt=2e-3: " + ", ".join(f"r={k}: {v:.3f}" for k, v in Cr2.items()))
OUT["numbers"]["T3"] = {"N": N, "nu": NU, "residual_dt4e-3": res1, "residual_dt2e-3": res2, "order": order,
                        "pythagoras_defect": [pyth1, pyth2], "C_r": Cr2}
check("T3 on an evolved 3D NSE flow Q(Du/Dt) = -grad p at rounding level for both dt; the solenoidal remainder "
      "is nu Lap u (Pythagoras defect falls ~dt^2); C_r finite at r = 3/2, 2, 3",
      f"Q-residual {max(res1, res2):.2e}; Pythagoras defect {pyth2:+.2e} (order {order:.2f}); "
      f"C_r {[round(v, 3) for v in Cr2.values()]}",
      max(res1, res2) < 1e-12 and 1.8 < order < 2.2 and abs(pyth2) < 1e-4 and Cr2[2.0] <= 1.0 + 1e-9
      and all(v < 5 for v in Cr2.values()),
      "the identity the proof uses holds on a real flow; the Riesz constants are O(1)")

# ============================================================================================ T4
banner("T4  DIMENSIONS: THE SCALE-INVARIANT THEOREM HAS NO SLOT FOR a0")
# exponents of (m, s): a0 = m s^-2, nu = m^2 s^-1
Mdim = sp.Matrix([[1, 2], [-2, -1]])      # columns a0, nu ; rows m, s
ns = Mdim.nullspace()
sv = sp.symbols("s_", positive=True)
# units of ||a||_{L^s L^r} on the critical line: a * m^{3/r} * s^{1/s}, with 3/r = 3 - 2/s
m_pow = 1 + (3 - 2 / sv); s_pow = -2 + 1 / sv
alpha = sp.solve(sp.Eq(2 * sp.Symbol("al"), m_pow), sp.Symbol("al"))[0]
consistent = sp.simplify(-alpha - s_pow) == 0
lengths = {name: (nuv ** 2 / 9.36e-11) ** (1 / 3) for name, nuv in (("water", 1.0e-6), ("air", 1.5e-5))}
P(f"    nullspace of [a0, nu] dimension matrix: {ns}  (empty => no dimensionless a0-nu combination)")
P(f"    critical norm of a has units nu^{sp.simplify(alpha)}: consistent = {consistent}")
P(f"    a0 with nu only makes a length (nu^2/a0)^(1/3): " + ", ".join(f"{k} {v:.3f} m" for k, v in lengths.items())
  + "  -- moved anywhere by the NSE scaling")
OUT["numbers"]["T4"] = {"nullspace": str(ns), "norm_units_nu_power": str(sp.simplify(alpha)), "lengths_m": lengths}
check("T4 no dimensionless monomial in (a0, nu); the critical acceleration norm is measured in powers of nu alone",
      f"nullspace {ns}; units nu^{sp.simplify(alpha)}", ns == [] and consistent,
      "upgrading N05 to a scale-invariant statement removes a0 entirely: the framework constant was never in the theorem")

# ============================================================================================ verdict
banner("VERDICT")
P("""  Swing 1 lands as a correct conditional theorem, not a Clay result: if the material acceleration of a Leray-Hopf
  solution lies in a critical space L^s L^r (2/s + 3/r = 3, 1 < r <= 3), the solution is smooth.  The proof is one
  exact identity (grad p = -Q Du/Dt, checked symbolically and on an evolved flow) plus the cited pressure-gradient
  criterion.  It strictly generalises N05's hypothesis and, being scale-invariant, contains no a0: the only scale
  it admits is nu.  It does not prove that any solution satisfies the hypothesis -- that a priori bound is the
  Clay problem (NSA3 maps why every route to it stops at the same half-derivative).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
