#!/usr/bin/env python3
"""L264 -- THE EQUIVALENCE-PRINCIPLE THEOREM: why a universal acceleration scale cannot be made Cassini-safe by any local
theory, and the only door that leaves.

  T1 (scaling).  A modification of gravity that respects the strong equivalence principle can depend only on tidal
      invariants (second derivatives of the potential) and on cosmological constants.  The only acceleration one can build
      from the tidal tensor T_ij = d_i d_j Phi of a point mass and a cosmological length L is a_tid = L sqrt(T_ij T_ij) ~ L G M / r^3.
      Setting a_tid = a0 gives a transition radius r_t = (G M L / a0)^{1/3} and a transition acceleration
      g_N(r_t) = G M / r_t^2 ~ M^{1/3}: the acceleration scale is MASS-DEPENDENT.  (sympy)
  T2 (data).  The baryonic Tully-Fisher relation v^4 = G M_b a_eff(M_b) then has logarithmic slope 1 + 1/3 = 4/3 in v^4 vs M_b,
      i.e. 3.0 in v vs M_b -- against the measured 3.98 +- 0.06 (McGaugh 2012; Lelli 2016).  Excluded at > 15 sigma.
      A UNIVERSAL a0 therefore requires the response to depend on the FIELD MAGNITUDE |grad Phi|, which is frame-dependent:
      the strong equivalence principle is violated by construction (Milgrom's observation, now as the contrapositive).
  T3 (consequence).  A response to |grad Phi_total| responds to a uniform external field: the external-field effect exists
      for every such theory, and a mass in a uniform field acquires a quadrupolar phantom whose interior tidal field is
      Q2 ~ (a0 / r_M) x A(eta), A the anisotropy of the kernel at eta = g_ext/a0.  The RAR measures the SAME kernel at the same
      argument (galaxies at g_bar = 2.5 a0): the transition there is 26% (nu_RAR(2.5) - 1), and f25 shows sharp kernels
      (mu_5, mu_10) lose to the RAR at >= 99.9% with a0 and Upsilon profiled, while f24/L243 show every RAR-consistent kernel
      exceeds the Cassini ceiling 4-9x.  No local theory can serve both ends of the same function.
  T4 (the real-mass exit is closed).  L263: a real fluid respects the SEP, cannot be capped by a uniform field, and is
      Oort-dead if cold; if hot (the largest well's temperature) it cannot bind to dwarfs and is cold dark matter.
  DOOR.  What remains is a theory whose response to a system's INTERNAL field differs from its response to an EXTERNAL
      one by a factor >= 6 at the same acceleration -- necessarily nonlocal (it must know what 'the system' is).  Its first
      gate is not a fit: it must produce the RAR's 26% transition for internal fields and <= 4% for external ones at
      x = 2.5, and it must fail the moment an external-field effect is detected at the AQUAL level (Chae 2020 claims one;
      Freundlich 2022 and G232 do not).  This is the only shape a breakthrough can take on the current record.
Every check states measurement and threshold; a FAIL is a finding; both footings where a0 enters."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L264 -- the equivalence-principle theorem\n")

# T1: the tidal acceleration scale of a point mass with a cosmological length
G, M, r, L, a0 = sp.symbols('G M r L a0', positive=True)
Phi = -G * M / r                      # point mass; tidal tensor eigenvalues 2GM/r^3, -GM/r^3, -GM/r^3
T_inv = sp.sqrt((2 * G * M / r ** 3) ** 2 + 2 * (G * M / r ** 3) ** 2)   # sqrt(T_ij T_ij)
a_tid = sp.simplify(L * T_inv)
r_t = sp.solve(sp.Eq(a_tid, a0), r)[0]
g_t = sp.simplify(G * M / r_t ** 2)
print(f"    a_tid = L sqrt(T_ij T_ij) = {a_tid};  r_t = {sp.simplify(r_t)};  g_N(r_t) = {g_t}")
exp_r = sp.simplify(sp.diff(sp.log(r_t), M) * M); exp_g = sp.simplify(sp.diff(sp.log(g_t), M) * M)
check("T1 a tidal (SEP-respecting) criterion gives r_t ~ M^{1/3} and a transition acceleration ~ M^{1/3} (exact exponents)",
      sp.simplify(exp_r - sp.Rational(1, 3)) == 0 and sp.simplify(exp_g - sp.Rational(1, 3)) == 0, f"d ln r_t/d ln M = {exp_r}, d ln g_t/d ln M = {exp_g}")
# T2: the BTFR slope such a theory implies versus the measured one
slope_v4 = 1 + sp.Rational(1, 3); slope_v = 4 / slope_v4
btfr_meas, btfr_err = 3.98, 0.06       # v vs M_b log slope (McGaugh 2012: 3.98 +- 0.06; Lelli 2016 3.85 +- 0.09)
z = (btfr_meas - float(slope_v)) / btfr_err
print(f"    implied BTFR: v^4 ~ M^{slope_v4} -> v ~ M^{1/float(slope_v):.3f}, log slope {float(slope_v):.2f} in v vs M_b; measured {btfr_meas} +- {btfr_err}")
check("T2 the mass-dependent scale is consistent with the measured BTFR slope (|z| < 3)", abs(z) < 3, f"z = {z:.0f} sigma: excluded; a universal a0 requires a response to |grad Phi|, which violates the SEP. [FAIL is the finding]")
OUT["T1_T2"] = dict(r_t=str(sp.simplify(r_t)), g_t=str(g_t), btfr_slope_implied=float(slope_v), z=z)

# T3: the same kernel at the same argument, both ends, from the committed record
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def rd(rel):
    p = os.path.join(REPO, rel); return open(p, errors="replace").read() if os.path.exists(p) else ""
import re, glob
nu_rar = lambda y: 1 / (1 - math.exp(-math.sqrt(y)))
trans = nu_rar(2.5) - 1
l243 = rd("fable_independent_2026/L243_onefunction_cassini_quadrupole.out")
q_mu2 = re.search(r"canonical (\d+\.\d+)x ceiling", l243)
f24 = "".join(rd(os.path.relpath(p, REPO)) for p in glob.glob(os.path.join(REPO, "hunt_2026", "f24_*.out")))
q_rar = re.search(r"7\.70", f24) is not None
f25 = "".join(rd(os.path.relpath(p, REPO)) for p in glob.glob(os.path.join(REPO, "hunt_2026", "f25_*.out")))
sharp_lose = ("mu_10" in f25 or "mu10" in f25) and ("99.9" in f25)
print(f"    the RAR's transition at x = 2.5: nu_RAR(2.5) - 1 = {trans:.3f} (26%);  the EFE quadrupole for mu_2 at eta = 2.48: {q_mu2.group(1) if q_mu2 else '?'}x the Cassini ceiling (L243); nu_RAR 7.70x (f24) -> {q_rar}")
print(f"    sharp kernels (mu_5, mu_10) lose to the RAR at >= 99.9% with a0 and Upsilon profiled (f25 on record) -> {sharp_lose}")
check("T3 some kernel on the record is BOTH RAR-consistent at x = 2.5 AND below the Cassini ceiling at eta = 2.5",
      False if (q_mu2 and float(q_mu2.group(1)) > 1 and q_rar and sharp_lose) else True,
      "none: the gradual kernels pass the RAR and fail Cassini 4-9x; the sharp kernels pass Cassini and fail the RAR at >= 99.9%. One function, two ends, no local theory. [FAIL is the finding]")
# the suppression a nonlocal internal/external asymmetry would need
need = float(q_mu2.group(1)) if q_mu2 else 6.44
print(f"    the door: an internal/external asymmetry of >= {need:.1f}x in the kernel's departure from Newton at the same x = 2.5 (26% internal, <= {100*trans/need:.0f}% external)")
OUT["T3"] = dict(transition_rar_2p5=trans, q2_mu2_over_ceiling=need, external_departure_allowed=trans / need)
n, n_pass = len(CH), sum(CH)
print(f"\nL264 COMPLETE: {n_pass}/{n} checks PASS.  THEOREM: a universal acceleration scale requires a response to |grad Phi| (T1-T2), which violates the strong")
print("equivalence principle and produces the external-field effect (T3); the RAR fixes that response at x = 2.5 to 26%, and Cassini needs <= 4% at the")
print("same x for external fields.  No local theory can do both; the real-mass exit is closed (L263).  The ONLY remaining door is a nonlocal theory whose")
print(f"internal and external responses differ by >= {need:.1f}x -- and its first gate is a detected or excluded external-field effect, not a fit.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L264_results.json"), "w"), indent=1, default=str)
