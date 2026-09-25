"""D-YM2 swing 4 (2026-09-25): the vanishing-margin door in Tomboulis's decimation argument.

Question (from swing 3): does a Tomboulis-type comparison survive a margin eps_m = a/(m + n0), 0 < a <= 1?

Read from the sources (2026-09-25):
  * Tomboulis, arXiv:0707.2179, III.1 / eq. (3.4): the decimation UPPER BOUND holds for every 0 < r <= 1. The margin is
    not needed for the inequality. It is used only in (3.30)-(3.32) to keep the interpolation parameter alpha <= 1 - delta,
    lattice-size independently, which gives the non-degeneracy constants eta1(delta), eta2(delta) > 0. Appendix B,
    eqs. (B.21)-(B.22): delta(eps) = eps*theta/2 with theta > 0 lattice-size independent at each step.
  * Ito & Seiler, arXiv:0803.3019, Sec. 3.3: the tension is "choice 1": for r < 1 the flow reaches strong coupling only if
    r is closer to 1 the larger beta is, and then alpha far from 1 is hard to ensure. Their Problems 1-3 (existence of t_m,
    of t* with alpha = alpha+, and the global extension of the implicit-function branch) are separate.
  * U(1) 4D Wilson transition beta_c = 1.011128(11) (Arnold, Lippert, Neuhaus, Schilling, hep-lat/0011058), first order.

What this script checks:
  M. the margin bookkeeping at fixed n (RECORD from Appendix B; plus the arithmetic min_m eps_m = a/(n + n0) > 0);
  U. the U(1) consistency test: under r_m = 1 - a/(m+n0) the U(1) separatrix beta*_U1(a, n0) must be <= beta_c,
     otherwise the repaired argument would 'prove' U(1) confinement where U(1) is deconfined;
  S. the SU(2) drift at weak coupling (r = 1) must stay bounded away from 0 as beta grows, or the schedule's guarantee
     that SU(2) always turns around is lost; and SU(2) flows under a U(1)-consistent schedule.
Checks can fail. Exit 0 only if every check passes.
"""
import json, os
import numpy as np
from scipy.special import ive
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: print(*a, flush=True)
FAILS = []; NC = [0]
def check(name, ok, detail=""):
    NC[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
out = {}
BETA_C_U1 = 1.011128

# ------------------------------------------------------------ U(1): exact decimation in Fourier space (FFT)
NU = 4096
thU = 2*np.pi*np.arange(NU)/NU
def u1_coeffs_from_logf(logf):
    f = np.exp(logf - logf.max()); F = np.fft.rfft(f).real
    return F/F[0]                                      # c_n, n = 0..NU/2 (f even)
def u1_f_from_c(c):
    full = np.zeros(NU); full[:len(c)] = c; full[NU - len(c) + 1:] = c[1:][::-1]   # c_{-n} = c_n
    return np.fft.ifft(full).real*NU
def u1_step(c, r):
    f = np.clip(u1_f_from_c(c), 1e-300, None)
    cg = np.clip(u1_coeffs_from_logf(4*np.log(f)), 0.0, 1.0)
    return cg**(4*r)
u1_c1_wilson = lambda b: ive(1, b)/ive(0, b)
def u1_beta_eff(c1):
    if c1 <= 1e-14: return 0.0
    if u1_c1_wilson(1e4) < c1: return np.inf
    return brentq(lambda b: u1_c1_wilson(b) - c1, 1e-9, 1e4)
def u1_fate(b0, a, n0, nmax=60000, esc=3.0):
    c = u1_coeffs_from_logf(b0*np.cos(thU))
    for m in range(nmax):
        c = u1_step(c, 1 - a/(m + n0))
        if c[1] < 1e-3: return "strong", m + 1
        if c[1] > u1_c1_wilson(esc): return "escape", m + 1     # beta_eff > 3: U(1) drift < 1e-8 there (check U0), cannot return
    return "undecided", nmax

# ------------------------------------------------------------ SU(2): quadrature in the character basis (as swing 3)
NG = 24000
th = (np.arange(NG) + 0.5)*np.pi/NG
w = (2/np.pi)*np.sin(th)**2*(np.pi/NG)
J = np.arange(0, 600); dj = J + 1
chi = np.sin(np.outer(J + 1, th))/np.sin(th)
def su2_coeffs(logf):
    f = np.exp(logf - logf.max()); raw = (chi*f) @ w
    return raw/(dj*raw[0])
def su2_step(c, r):
    f = np.clip((dj*c) @ chi, 1e-300, None)
    return np.clip(su2_coeffs(4*np.log(f)), 0.0, 1.0)**(4*r)
su2_c1_wilson = lambda b: ive(2, b)/ive(1, b)
def su2_beta_eff(c1):
    if c1 <= 1e-14: return 0.0
    if su2_c1_wilson(1e4) < c1: return np.inf
    return brentq(lambda b: su2_c1_wilson(b) - c1, 1e-9, 1e4)

P("=" * 100); P("0. U(1) FFT decimation agrees with the quadrature decimation of swing 3"); P("=" * 100)
thq = (np.arange(48000) + 0.5)*np.pi/24000 - np.pi; wq = np.full(48000, 1/48000); Jq = np.arange(300)
chiq = np.cos(np.outer(Jq, thq)); multq = np.r_[1.0, 2*np.ones(299)]
def q_step(c, r):
    f = np.clip((multq*c) @ chiq, 1e-300, None); lg = 4*np.log(f); g = np.exp(lg - lg.max())
    raw = (chiq*g) @ wq; return np.clip(raw/raw[0], 0, 1)**(4*r)
err = 0.0
for b0 in (0.8, 3.0):
    cq = ((chiq*np.exp(b0*np.cos(thq) - b0)) @ wq); cq = cq/cq[0]
    cf = u1_coeffs_from_logf(b0*np.cos(thU))
    for k in range(6):
        cq, cf = q_step(cq, 0.95), u1_step(cf, 0.95)
        err = max(err, abs(cq[1] - cf[1]), abs(cq[2] - cf[2]))
check("S0 the FFT and quadrature U(1) decimations agree to 1e-9 over 6 steps", err < 1e-9, f"max |dc| = {err:.1e}")

P("=" * 100); P("M. margin bookkeeping (Tomboulis App. B) at a fixed number of decimations n"); P("=" * 100)
P("  [RECORD] Tomboulis (B.21)-(B.22): at step m, choosing r = 1 - eps_m gives alpha <= 1 - delta_m with delta_m = eps_m theta_m/2,")
P("           theta_m > 0 lattice-size independent; (3.32) then holds at that step with eta1,2(delta_m) > 0.")
P("  [RECORD] His (5.7)-(5.9) use eta > 0 per step to absorb O(1/|Lambda|) mismatches; at fixed n these vanish as |Lambda| -> inf.")
for a, n0 in ((0.5, 10), (1.0, 3)):
    for n in (10, 1000, 10**6):
        P(f"  a = {a}, n0 = {n0}: after n = {n:>7d} steps the smallest margin is eps_min = a/(n+n0) = {a/(n + n0):.3e} > 0")
check("M1 at any finite n every margin is strictly positive: min_m eps_m = a/(n + n0) > 0 (arithmetic; uniformity in n is NOT claimed)",
      all(a/(n + n0) > 0 for a, n0 in ((0.5, 10), (1.0, 3)) for n in (10, 1000, 10**6)))

P("=" * 100); P("U0. the U(1) escape threshold: the r = 1 drift at beta_eff ~ 3 must be negligible"); P("=" * 100)
cU = u1_coeffs_from_logf(3.0*np.cos(thU)); seqU = []
for m in range(60):
    cU = u1_step(cU, 1.0); seqU.append(u1_beta_eff(cU[1]))
dU = (seqU[-1] - seqU[10])/(len(seqU) - 11)
P(f"  U(1), r = 1, from beta = 3: beta_eff settles at {seqU[-1]:.4f}; mean drift per step over steps 10-60 = {dU:+.2e}")
check("U0 U(1)'s own drift at beta_eff ~ 3 is below 1e-8 per step, so a schedule-driven flow past beta_eff = 3 cannot return",
      abs(dU) < 1e-8, f"{dU:+.2e}")
P("  [RECORD] Beyond beta_eff = 3 the schedule adds a*beta/(m+n0) per step, which stays far above 1e-8 over any budget used here,")
P("  and the drift shrinks further as beta grows (exponentially, for the Villain form). So 'escape' at beta_eff = 3 is safe.")

P("=" * 100); P("U. the U(1) consistency test: separatrix beta*_U1(a, n0) versus the U(1) transition beta_c = 1.0111"); P("=" * 100)
def u1_separatrix(a, n0):
    """bracket [lo, hi]: lo = largest beta seen flowing to strong coupling, hi = smallest seen escaping. A flow that stays
    undecided within the step budget (slow schedules, or beta near the separatrix) stops the bisection; the bracket stands."""
    lo, hi = 0.05, 3.0
    if u1_fate(hi, a, n0)[0] != "escape" or u1_fate(lo, a, n0)[0] != "strong": return None
    exact = True
    for _ in range(18):
        mid = 0.5*(lo + hi); f = u1_fate(mid, a, n0)[0]
        if f == "strong": lo = mid
        elif f == "escape": hi = mid
        else: exact = False; break
    return (lo, hi, exact)
grid = {}
for a in (0.25, 0.5, 0.75, 1.0):
    for n0 in (2, 3, 5, 10, 20, 50):
        if n0 <= a: continue
        br = u1_separatrix(a, n0); grid[f"a={a},n0={n0}"] = br
        if br is None: P(f"  a = {a:4.2f}, n0 = {n0:3d}: no bracket (beta=3 does not escape or beta=0.05 does not confine)"); continue
        lo, hi, ex = br
        tag = "consistent (upper end <= beta_c)" if hi <= BETA_C_U1 else "INCONSISTENT (upper end > beta_c)"
        P(f"  a = {a:4.2f}, n0 = {n0:3d}: beta*_U1 in [{lo:.4f}, {hi:.4f}]{'' if ex else '  (bracket; a flow near the separatrix was undecided)'}  {tag}")
out["U_separatrix_U1_bracket"] = grid
fin = {k: v for k, v in grid.items() if v is not None}
consistent = {k: v[1] for k, v in fin.items() if v[1] <= BETA_C_U1}
check("U1 every tested schedule brackets a finite U(1) separatrix: beta = 0.05 confines and beta = 3 escapes (the fixed-r MK failure is gone)",
      len(fin) == len(grid), f"{len(fin)}/{len(grid)} bracketed")
check("U2 (the test) every bracketed schedule keeps U(1)'s separatrix at or below its true transition 1.0111 (no false U(1) confinement)",
      len(fin) > 0 and len(consistent) == len(fin), f"max upper end {max(v[1] for v in fin.values()):.4f}")
check("U3 every schedule with a >= 0.5 is consistent (the family used for SU(2) below)",
      all(v[1] <= BETA_C_U1 for k, v in fin.items() if float(k.split(',')[0].split('=')[1]) >= 0.5))
incons = {k: v for k, v in fin.items() if v[1] > BETA_C_U1}
P(f"  schedules that would 'prove' U(1) confinement in its Coulomb phase: {sorted(incons)}")

P("=" * 100); P("S. SU(2): does the weak-coupling drift stay bounded away from zero, and does SU(2) confine under a consistent schedule?"); P("=" * 100)
drift = []
for b0 in (32.0, 64.0, 128.0, 256.0):
    c = su2_coeffs(b0*np.cos(th)); seq = []
    for m in range(40):
        c = su2_step(c, 1.0); seq.append(su2_beta_eff(c[1]))
    seg = seq[10:]; d = (seg[-1] - seg[0])/(len(seg) - 1)
    drift.append((b0, float(np.mean(seg)), d))
    P(f"  r = 1, start beta = {b0:6.1f}: mean beta_eff over steps 10-40 = {np.mean(seg):7.2f}, drift per step = {d:+.4f}")
out["S_su2_drift"] = drift
ds = [d for _, _, d in drift]
check("S1 the SU(2) weak-coupling drift stays <= -0.2 per step up to beta_eff ~ 250 (no fade: the schedule's guarantee holds)",
      all(d <= -0.2 for d in ds), ", ".join(f"{d:+.3f}" for d in ds))
spread = (max(ds) - min(ds))/abs(np.mean(ds))
check("S2 the drift is flat to within 20% over beta_eff 30-250 (a constant, like a one-loop coefficient)", spread < 0.2, f"spread {spread:.2f}")
best = sorted(consistent.items(), key=lambda kv: -kv[1])[0][0] if consistent else None   # the least conservative consistent schedule
su2_runs = {}
if best:
    a = float(best.split(",")[0].split("=")[1]); n0 = int(best.split("n0=")[1])
    cbar = -float(np.mean(ds))
    for b0 in (2.5, 4.0, 8.0, 16.0):
        c = su2_coeffs(b0*np.cos(th)); b = b0; mstar = None
        for m in range(200000):                      # scalar-model turnaround (for the step budget)
            b = b/(1 - a/(m + n0)) - cbar
            if b < 0.5: mstar = m + 1; break
        budget = int(2.5*mstar) + 100 if mstar else 0; res = "undecided"; peak = b0
        if mstar and budget <= 8000:
            for m in range(budget):
                c = su2_step(c, 1 - a/(m + n0)); be = su2_beta_eff(c[1]); peak = max(peak, be)
                if c[1] < 1e-3: res = f"strong after {m + 1}"; break
        su2_runs[b0] = {"scalar_model_steps": mstar, "result": res, "peak_beta_eff": peak}
        P(f"  schedule {best}: SU(2) beta0 = {b0:5.1f}: {res} (scalar model {mstar}; peak beta_eff {peak:.0f})"
          + ("" if mstar and budget <= 8000 else "  [beyond the numerical budget: scalar model only]"))
out["S_su2_under_consistent_schedule"] = {"schedule": best, "runs": su2_runs}
tested = [v for v in su2_runs.values() if v["result"] != "undecided"]
check("S3 under the U(1)-consistent schedule with the largest beta*_U1, SU(2) reaches strong coupling from every tested beta0 within budget",
      len(tested) >= 2 and all(v["result"].startswith("strong") for v in tested), f"{len(tested)} runs in budget")

P("=" * 100)
P("READING. The margin in Tomboulis's argument is needed only per step (App. B), so a margin shrinking like a/n costs nothing")
P("at any finite number of decimations. Tested here: whether U(1) stays deconfined above its true transition, and whether")
P("the SU(2) drift survives at weak coupling. The door this narrows to: Ito-Seiler Problems 1-3 (existence of t_m, of the")
P("common t* with alpha = alpha+, and the GLOBAL extension of the implicit-function branch). Those are untouched by the margin.")
out["n_checks"] = NC[0]; out["fails"] = FAILS
json.dump(out, open(os.path.join(HERE, "swing4_results.json"), "w"), indent=1, default=str)
P(f"\n{NC[0] - len(FAILS)}/{NC[0]} checks passed" + ("" if not FAILS else f"; FAILED: {FAILS}"))
raise SystemExit(1 if FAILS else 0)
