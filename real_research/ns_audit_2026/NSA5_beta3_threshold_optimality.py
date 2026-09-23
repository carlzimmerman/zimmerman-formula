#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA5 -- SWINGING THE beta = 3 DOOR BELOW 4 c nu = 1: the standard H^1 closure cannot go lower, even with every term
the literature drops.  (Follow-up to NSA3 W3/W4.)

THE DOOR
  d_t u - nu Lap u + (u.grad)u + c|u|^2 u + grad p = 0 on T^3 (critical damping, the convective Brinkman-Forchheimer
  equations with r = 3).  Global regularity is known for 4 c nu >= 1 (Hajduk-Robinson 2017, JDE 263:7141; also
  Zhang-Wu-Lu 2011, Kim-Li 2017).  Mohan 2024 (arXiv:2412.20940) records monotonicity at 2 c nu >= 1 and no
  regularity result below 4 c nu = 1; a second, harder search found none either, so NSA3 W3/W4 stand.  This door
  sits strictly between the known theory and Clay: c nu is the only dimensionless parameter and the damping is
  scale-critical.

THE SWING
  Test with -Lap u.  Two things the standard proof leaves on the table:
    (a) the damping dissipates c int (|u|^2 |A|^2 + 2 |A^T u|^2), A = grad u (A_ij = d_j u_i), including the
        (c/2)||grad|u|^2||^2 = 2c||A^T u||^2 term usually dropped;
    (b) GAUGE FREEDOM: int (A^T u).Lap u = int grad(|u|^2/2).Lap u = 0 because Lap u is divergence-free, so
        int (u.grad)u . Lap u = int ((A + lam A^T) u) . Lap u for EVERY real lam (lam = -1 is the vorticity form
        -(u x omega)).
  Pointwise Cauchy-Schwarz + Young then close the estimate iff 4 c nu >= M(lam),
        M(lam) = sup over (u, traceless A) of |(A + lam A^T) u|^2 / (|u|^2 |A|^2 + 2 |A^T u|^2).
  G1 the gauge identity on a random smooth solenoidal field, lam in {-1, 0.5, 2}.
  G2 the damping dissipation density 2|A^T u|^2 = (1/2)|grad|u|^2|^2 (pointwise, numerically).
  G3 M(0) = 1: |A u| <= |A||u| gives M(0) <= 1; 2e5 random (u, traceless A) never exceed it.
  G4 THE WITNESS: A = a b^T with a perpendicular to u, b parallel to u (traceless, A^T u = 0) gives ratio exactly 1
     for every lam (symbolic).  Hence min over lam of M(lam) = 1: the best threshold in this family is exactly
     4 c nu >= 1.  Going below needs a non-pointwise (nonlocal) estimate -- the witness is realisable at any
     single point (u(x) = u0 + A(x - x0) is divergence-free), so no pointwise inequality can exclude it.
  Label [C]: an optimality statement about a METHOD, not about the PDE.  The PDE question below 1/4 stays open.
  MUTATE=1 replaces Lap u by Lap u + grad phi (not solenoidal) in G1: the gauge freedom must break and G1 must FAIL.

Run from the repository root:  python3 real_research/ns_audit_2026/NSA5_beta3_threshold_optimality.py
"""
import os, sys, json
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "NSA5_beta3_threshold_optimality"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA5", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


# ------------------------------------------------------------------ a random smooth solenoidal field on T^3
N = 32
k1 = np.fft.fftfreq(N, 1.0 / N)
K = np.array(np.meshgrid(k1, k1, k1, indexing="ij"))
K2 = (K ** 2).sum(0)
K2i = np.where(K2 == 0, 1.0, K2)
rng = np.random.default_rng(11)
uh = (rng.standard_normal((3, N, N, N)) + 1j * rng.standard_normal((3, N, N, N))) * ((np.sqrt(K2) <= 3) & (K2 > 0))
uh = uh - K * (K * uh).sum(0) / K2i                                   # Leray projection
u = np.real(np.fft.ifftn(uh, axes=(1, 2, 3)))
u /= np.sqrt(np.mean(u ** 2))
uh = np.fft.fftn(u, axes=(1, 2, 3))
A = np.real(np.array([[np.fft.ifftn(1j * K[j] * uh[i]) for j in range(3)] for i in range(3)]))   # A[i][j] = d_j u_i
lap = np.real(np.fft.ifftn(-K2 * uh, axes=(1, 2, 3)))
Au = np.einsum("ij...,j...->i...", A, u)                             # (u.grad)u
ATu = np.einsum("ji...,j...->i...", A, u)                            # grad(|u|^2/2)
div_u = np.max(np.abs(np.real(np.fft.ifftn((1j * K * uh).sum(0)))))

# ============================================================================================ G1
banner("G1  GAUGE FREEDOM: int (u.grad)u . Lap u = int ((A + lam A^T) u) . Lap u FOR EVERY lam")
target = lap.copy()
if MUTATE:
    phi_h = np.fft.fftn(np.sin(np.linspace(0, 2 * np.pi, N, endpoint=False))[:, None, None] * np.ones((N, N, N)))
    target = lap + np.real(np.fft.ifftn(1j * K * phi_h, axes=(1, 2, 3)))  # add a gradient: no longer solenoidal
base = np.mean((Au * target).sum(0))
rows = {}
for lam in (-1.0, 0.5, 2.0):
    val = np.mean(((Au + lam * ATu) * target).sum(0))
    rows[lam] = val
    P(f"    lam = {lam:+.1f}: int ((A + lam A^T)u).Lap u = {val:+.12e}   (lam = 0: {base:+.12e})")
rel = max(abs(v - base) for v in rows.values()) / abs(base)
OUT["numbers"]["G1"] = {"lam0": base, "by_lam": rows, "rel_spread": rel, "max_div_u": div_u}
check("G1 the trilinear term is independent of lam (grad(|u|^2/2) is L2-orthogonal to the solenoidal Lap u)",
      f"relative spread over lam in {{-1, 0.5, 2}}: {rel:.1e}; max|div u| {div_u:.1e}", rel < 1e-10,
      "one free parameter in how the nonlinearity is split before Cauchy-Schwarz")

# ============================================================================================ G2
banner("G2  THE FULL DAMPING DISSIPATION DENSITY")
s2 = (u ** 2).sum(0)
g_s2 = np.real(np.array([np.fft.ifftn(1j * K[j] * np.fft.fftn(s2)) for j in range(3)]))
lhs = np.mean((g_s2 ** 2).sum(0)) / 2
rhs = 2 * np.mean((ATu ** 2).sum(0))
lhs_full = np.mean(s2 * (u * (-lap)).sum(0))
rhs_full = np.mean(s2 * (A ** 2).sum((0, 1))) + 2 * np.mean((ATu ** 2).sum(0))
r2, r2f = abs(lhs - rhs) / abs(rhs), abs(lhs_full - rhs_full) / abs(rhs_full)
P(f"    (1/2) int |grad|u|^2|^2 = {lhs:.10e};  2 int |A^T u|^2 = {rhs:.10e};  rel {r2:.1e}")
P(f"    int |u|^2 u.(-Lap u) = {lhs_full:.10e};  int (|u|^2|A|^2 + 2|A^T u|^2) = {rhs_full:.10e};  rel {r2f:.1e}")
OUT["numbers"]["G2"] = {"rel_density": r2, "rel_full": r2f}
check("G2 the damping dissipates c int (|u|^2 |A|^2 + 2 |A^T u|^2): the usually dropped term is 2c||A^T u||^2",
      f"rel {r2:.1e}, {r2f:.1e}", r2 < 1e-10 and r2f < 1e-10, "the denominator of M(lam) is the whole dissipation")

# ============================================================================================ G3
banner("G3  M(0) = 1: NO RANDOM (u, traceless A) EXCEEDS IT")
S = 200000
uu = rng.standard_normal((S, 3))
AA = rng.standard_normal((S, 3, 3))
AA -= np.einsum("s,ij->sij", np.trace(AA, axis1=1, axis2=2) / 3, np.eye(3))       # traceless (div-free)
AAu = np.einsum("sij,sj->si", AA, uu)
AATu = np.einsum("sji,sj->si", AA, uu)
den = (uu ** 2).sum(1) * (AA ** 2).sum((1, 2)) + 2 * (AATu ** 2).sum(1)
ratio0 = (AAu ** 2).sum(1) / den
Mlam = {lam: float(np.max(((AAu + lam * AATu) ** 2).sum(1) / den)) for lam in (-1.0, -0.5, 0.0, 0.5, 1.0)}
P(f"    sampled max ratio at lam = 0: {ratio0.max():.6f} (bound 1);  sampled max by lam: "
  + ", ".join(f"{k:+.1f}: {v:.4f}" for k, v in Mlam.items()))
OUT["numbers"]["G3"] = {"max_ratio_lam0": float(ratio0.max()), "sampled_max_by_lam": Mlam}
check("G3 |A u|^2 <= |A|^2 |u|^2 <= denominator, so M(0) <= 1; sampling never exceeds 1",
      f"max sampled ratio {ratio0.max():.6f}", ratio0.max() <= 1 + 1e-12,
      "random sampling alone does not find the worst case (see G4); the upper bound is the inequality itself")

# ============================================================================================ G4
banner("G4  THE WITNESS: RATIO EXACTLY 1 FOR EVERY lam  =>  min_lam M(lam) = 1")
lam, al, be = sp.symbols("lambda alpha beta", real=True)
uv = sp.Matrix([1, 0, 0])
a_vec = sp.Matrix([0, al, 0])          # a perpendicular to u
b_vec = sp.Matrix([be, 0, 0])          # b parallel to u
Aw = a_vec * b_vec.T
trace_w = Aw.trace()
ATu_w = Aw.T * uv
num = ((Aw + lam * Aw.T) * uv).dot((Aw + lam * Aw.T) * uv)
denw = uv.dot(uv) * sum(x ** 2 for x in Aw) + 2 * ATu_w.dot(ATu_w)
ratio_w = sp.simplify(num / denw)
P(f"    A = a b^T, a = (0, alpha, 0), b = (beta, 0, 0), u = e1:  tr A = {trace_w};  A^T u = {list(ATu_w)};  "
  f"ratio = {ratio_w}")
OUT["numbers"]["G4"] = {"trace": str(trace_w), "ATu": str(list(ATu_w)), "ratio": str(ratio_w)}
check("G4 a traceless A with A^T u = 0 and |A u| = |A||u| gives ratio 1 for every lam: the pointwise H^1 closure "
      "needs 4 c nu >= 1 exactly, whatever gauge is used and with the full damping dissipation",
      f"tr A = {trace_w}; A^T u = {list(ATu_w)}; ratio(lam) = {ratio_w}",
      trace_w == 0 and all(x == 0 for x in ATu_w) and ratio_w == 1,
      "the 4 c nu = 1 wall of the literature is the optimum of this method, not a lost constant")

# ============================================================================================ verdict
banner("VERDICT")
P("""  The beta = 3 door below 4 c nu = 1 is swung and does not open with the standard tools.  Keeping the whole
  damping dissipation and using the gauge freedom in splitting (u.grad)u, the pointwise H^1 closure still needs
  4 c nu >= 1 exactly; the extremal configuration (A^T u = 0, |A u| = |A||u|) is realisable at any point by a
  divergence-free field, so only a genuinely nonlocal estimate could go lower.  The PDE question for 4 c nu < 1
  remains open; it is a critical problem, a small critical perturbation of Navier-Stokes itself.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
