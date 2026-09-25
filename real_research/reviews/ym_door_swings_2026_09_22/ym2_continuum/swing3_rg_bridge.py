"""D-YM2 swing 3 (2026-09-25): the RG-bridge door, via Migdal-Kadanoff-type decimations (Tomboulis's route).

Tomboulis (arXiv:0707.2179) tried to bridge weak and strong coupling in 4D SU(2) by comparing the lattice theory with the
'MKT' decimation: raise the plaquette weight to the power 2^(D-2) = 4 (bond moving), then raise each character
coefficient to the power 4r (decimation), r = 1 - eps. Ito & Seiler (arXiv:0803.3019; PoS Confinement8:034, arXiv:0901.4246)
found three problems:
  (a) with r < 1 the flow goes to the WEAK-coupling fixed point above a bifurcation (they report beta = 4.79 -> weak,
      4.80 -> strong at r = 0.9);
  (b) the existence argument for the interpolation parameter alpha* is only local (implicit-function theorem);
  (c) FUNDAMENTAL: at r = 1 the 4D MK flow drives U(1) to strong coupling exactly like SU(2) (Ito 1985), but 4D U(1)
      provably deconfines at weak coupling (Guth 1980; Froehlich-Spencer 1982), so any comparison that ignores the
      nonabelian structure must fail.
This script builds the decimation exactly (it is exact on the corresponding hierarchical lattice), reproduces (a) and (c),
and then tests a step-dependent r_n = 1 - a/(n + n0). (Credit: Ito-Seiler report that Tomboulis hinted orally at an
n-dependent r without saying how; the concrete schedule, the 0 < a <= 1 criterion and the test are this script's.) With a vanishing margin the decimation might
be driven to strong coupling by SU(2)'s O(1)-per-step asymptotic-freedom drift while U(1), whose drift fades at weak
coupling, escapes to the weak-coupling fixed point. That would be a hierarchical decimation that knows the difference.
NOTE: r_n -> 1 violates Tomboulis's own requirement that r stay away from 1, so even a positive result here does NOT repair
the rigorous route; it only sharpens what the missing inequality would have to allow.
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

# ---------------------------------------------------------------- groups as class functions on a theta grid
NG = 24000
class SU2:
    name = "SU(2)"
    th = np.linspace(0, np.pi, NG + 1)[1:-1] if False else (np.arange(NG) + 0.5)*np.pi/NG      # midpoint grid
    w = (2/np.pi)*np.sin(th)**2*(np.pi/NG)                                                   # Haar (normalised)
    J = np.arange(0, 400)                                                                    # 2j = 0..399
    d = J + 1                                                                                 # dimension 2j+1
    mult = J + 1                                                                              # f = sum (2j+1) c_j chi_j
    chi = np.sin(np.outer(J + 1, th))/np.sin(th)                                             # chi_j(theta)
    @staticmethod
    def wilson(beta): return beta*np.cos(SU2.th)                   # log f, f = exp((beta/2) tr U), beta = 4/g^2
    @staticmethod
    def c_fund_wilson(beta): return ive(2, beta)/ive(1, beta)      # c_{1/2} of the Wilson action
class U1:
    name = "U(1)"
    th = (np.arange(2*NG) + 0.5)*np.pi/NG - np.pi
    w = np.full(2*NG, 1/(2*NG))
    J = np.arange(0, 400)
    d = np.ones(400)                                                # c_n = int f cos(n th) / int f
    mult = np.r_[1.0, 2*np.ones(399)]                               # f = c_0 + 2 sum_{n>=1} c_n cos(n th)  (n and -n)
    chi = np.cos(np.outer(J, th))                                   # real part suffices for even class functions
    @staticmethod
    def wilson(beta): return beta*np.cos(U1.th)                    # f = exp(beta cos theta), beta = 1/g^2
    @staticmethod
    def c_fund_wilson(beta): return ive(1, beta)/ive(0, beta)

def coeffs(G, logf):
    """normalised character coefficients c_j (c_0 = 1) of f = exp(logf), computed stably."""
    f = np.exp(logf - logf.max())
    raw = (G.chi*f) @ G.w
    return raw/(G.d*raw[0])

def step(G, c, r):
    """one MKT step from coefficients c: f = sum d_j c_j chi_j; g = f^4 (normalised); c' = c_g^(4r)."""
    f = (G.mult*c) @ G.chi
    f = np.clip(f, 1e-300, None)
    cg = coeffs(G, 4*np.log(f))
    cg = np.clip(cg, 0.0, 1.0)
    return cg**(4*r)

def beta_eff(G, c1):
    """effective Wilson coupling with the same fundamental coefficient (a coordinate on the flow, not an approximation)."""
    if c1 <= 1e-12: return 0.0
    hi = 4000.0
    if G.c_fund_wilson(hi) < c1: return np.inf
    return brentq(lambda b: G.c_fund_wilson(b) - c1, 1e-9, hi)

def flow(G, beta0, rs, nmax, strong=1e-3, weak_beta=2000.0):
    c = coeffs(G, G.wilson(beta0)); traj = [beta_eff(G, c[1])]
    for n in range(nmax):
        r = rs(n) if callable(rs) else rs
        c = step(G, c, r)
        be = beta_eff(G, c[1]); traj.append(be)
        if c[1] < strong: return "strong", n + 1, traj
        if be > weak_beta: return "weak", n + 1, traj
    return "undecided", nmax, traj

out = {}
P("=" * 100); P("0. sanity: the coefficient machinery reproduces the Wilson action's Bessel-function coefficients"); P("=" * 100)
for G, b in ((SU2, 2.3), (SU2, 10.0), (U1, 1.0), (U1, 10.0)):
    c = coeffs(G, G.wilson(b)); P(f"  {G.name} beta={b}: c_1 numeric {c[1]:.10f}  exact {G.c_fund_wilson(b):.10f}")
err = max(abs(coeffs(G, G.wilson(b))[1] - G.c_fund_wilson(b)) for G, b in ((SU2, 2.3), (SU2, 10.0), (U1, 1.0), (U1, 10.0)))
check("S0 quadrature reproduces the exact fundamental coefficients to 1e-8", err < 1e-8, f"max err {err:.1e}")

P("=" * 100); P("A. Ito-Seiler (a): MKT with r = 0.9 has a bifurcation in beta (SU(2))"); P("=" * 100)
def fate(G, b, r, nmax=400): return flow(G, b, r, nmax)[0]
lo, hi = 2.0, 40.0
assert fate(SU2, lo, 0.9) == "strong" and fate(SU2, hi, 0.9) == "weak", (fate(SU2, lo, 0.9), fate(SU2, hi, 0.9))
for _ in range(25):
    mid = 0.5*(lo + hi)
    if fate(SU2, mid, 0.9) == "strong": lo = mid
    else: hi = mid
bstar = 0.5*(lo + hi)
P(f"  separatrix at beta_std = 4/g^2 = {bstar:.4f}   (= {bstar/2:.4f} in beta = 2/g^2)")
P(f"  Ito-Seiler report the split between beta = 4.79 and 4.80 (their normalisation stated as beta = 2/g^2)")
out["A_r09_separatrix_beta_std"] = bstar
check("A1 a separatrix exists at r = 0.9 (flow to the WEAK fixed point above it): Ito-Seiler's point (a) reproduced qualitatively",
      np.isfinite(bstar) and 2 < bstar < 40, f"beta_std* = {bstar:.3f}")
ratio = 4.795/bstar
P(f"  published midpoint 4.795 / this separatrix = {ratio:.4f}")
P("  RECORD: the location agrees with Ito-Seiler up to an exact factor 2, consistent with a factor-2 difference in how the")
P("  coupling is normalised (their talk states beta = 2/g^2 but not the action's normalisation). Their text also has the")
P("  flow directions the other way round (4.79 -> weak, 4.80 -> strong); here larger beta goes to the weak fixed point, as")
P("  their own Gaussian argument requires. Unresolved, recorded, not fitted.")
out["A_ratio_to_published"] = ratio
check("A2 (POST HOC, formulated after seeing 2.399) the separatrix equals the published 4.79-4.80 up to a factor 2.00 +/- 0.01 (normalisation)",
      abs(ratio - 2.0) < 0.01, f"ratio {ratio:.4f}")

P("=" * 100); P("B. Ito-Seiler (c): r = 1, SU(2) versus U(1)"); P("=" * 100)
def drift_along(G, b0, r, n_skip=10, n_run=400):
    res, n, tr = flow(G, b0, r, n_skip + n_run)
    tr = [x for x in tr if np.isfinite(x)]
    if len(tr) < n_skip + 5: return res, n, tr, float("nan")
    seg = tr[n_skip:]
    return res, n, tr, (seg[-1] - seg[0])/(len(seg) - 1)
fB = {}
for G, betas in ((SU2, (4.0, 8.0, 16.0, 32.0)), (U1, (2.0, 4.0, 8.0, 16.0))):
    for b0 in betas:
        res, n, tr, dr = drift_along(G, b0, 1.0)
        fB[f"{G.name} beta={b0}"] = {"fate_within_410": res, "steps": n, "mean_drift_per_step": dr, "beta_after_10": tr[10] if len(tr) > 10 else None}
        P(f"  {G.name:6s} beta0 = {b0:5.1f}: mean d beta_eff/step after transients = {dr:+.5f}   ({res} within {n} steps)")
out["B_r1"] = fB
su = [v["mean_drift_per_step"] for k, v in fB.items() if k.startswith("SU(2)")]
u1 = [v["mean_drift_per_step"] for k, v in fB.items() if k.startswith("U(1)")]
check("B1 SU(2) at r = 1: an O(1) drift toward strong coupling at every tested beta (the decimation's shadow of asymptotic freedom)",
      all(np.isfinite(x) and x < -0.1 for x in su), ", ".join(f"{x:+.3f}" for x in su))
check("B2 U(1) at r = 1: the drift is at least 100x smaller than SU(2)'s for beta0 >= 4 (near-marginal: for the Villain form it is exponentially small)",
      all(np.isfinite(x) for x in u1) and max(abs(x) for x in u1[1:]) < min(abs(x) for x in su)/100,
      ", ".join(f"{x:+.2e}" for x in u1))
P("  [RECORD] its SIGN is below numerical resolution here; Ito (1985) proves the r = 1 flow still reaches strong coupling.")
P("  That is the published obstruction: at r = 1 the decimation confines U(1), which the real 4D U(1) theory does not.")
cSU = float(np.mean([abs(x) for x in su]))

P("=" * 100); P("D. the one new idea tested: a vanishing-margin schedule r_n = 1 - a/(n + n0), 0 < a < 1"); P("=" * 100)
P("  Scalar model: beta_{n+1} = beta_n/r_n - c. With u_n = beta_n * prod_k r_k, u_{n+1} = u_n - c prod_k r_k, and for a < 1")
P("  sum_n prod_k r_k diverges: ANY drift c > 0 wins eventually. SU(2) (c = O(1)) must turn around from every beta0;")
P("  U(1) (c exponentially small at weak coupling) must follow the drift-free growth beta0 / prod_k r_k.")
def model_turnaround(b0, a_, n0, c, nmax=200000):
    b = b0
    for n in range(nmax):
        b = b/(1 - a_/(n + n0)) - c
        if b <= 0.5: return n + 1
    return None
sched = {}
N0 = 10
for a_, betas in ((0.5, (4.0, 16.0, 64.0)), (0.75, (4.0, 16.0))):
    rs = (lambda n, a_=a_: 1 - a_/(n + N0))
    for b0 in betas:
        npred = model_turnaround(b0, a_, N0, cSU)
        res, n, tr = flow(SU2, b0, rs, int(3*npred) + 50, weak_beta=3000.0)
        sched[f"SU(2) a={a_} beta0={b0}"] = {"fate": res, "steps": n, "scalar_model_steps": npred, "peak_beta_eff": float(np.nanmax([x for x in tr if np.isfinite(x)]))}
        P(f"  SU(2) a = {a_:4.2f} beta0 = {b0:5.1f}: {res:9s} after {n:5d} steps (scalar model with c = {cSU:.3f}: {npred}); peak beta_eff {sched[f'SU(2) a={a_} beta0={b0}']['peak_beta_eff']:.0f}")
for b0 in (2.0, 8.0, 32.0):
    a_ = 0.5; rs = (lambda n: 1 - 0.5/(n + N0)); nrun = 2500
    res, n, tr = flow(U1, b0, rs, nrun, weak_beta=1e9)
    free = b0*np.prod([1/(1 - a_/(k + N0)) for k in range(n)])
    ratio = tr[-1]/free
    sched[f"U(1) a={a_} beta0={b0}"] = {"fate": res, "steps": n, "beta_final": tr[-1], "drift_free_prediction": free, "ratio": ratio}
    P(f"  U(1)  a = {a_:4.2f} beta0 = {b0:5.1f}: after {n} steps beta_eff = {tr[-1]:.1f} vs drift-free {free:.1f} (ratio {ratio:.4f}); {res}")
out["D_schedule"] = sched
su_ok = [v for k, v in sched.items() if k.startswith("SU(2)")]
u1_ok = [v for k, v in sched.items() if k.startswith("U(1)")]
check("D1 SU(2): every tested flow reaches strong coupling, within a factor 2 of the scalar-model step count",
      all(v["fate"] == "strong" and 0.5 <= v["steps"]/v["scalar_model_steps"] <= 2 for v in su_ok),
      ", ".join(f"{v['steps']}/{v['scalar_model_steps']}" for v in su_ok))
check("D2 U(1): from beta0 >= 8 the flow tracks the drift-free growth to within 1% and does not turn around within 2500 steps (the scalar model says it never does)",
      all(v["ratio"] > 0.99 and v["fate"] != "strong" for k, v in sched.items() if k.startswith("U(1)") and not k.endswith("beta0=2.0")),
      ", ".join(f"{v['ratio']:.4f}" for v in u1_ok))
P("  => in the hierarchical model a vanishing margin r_n = 1 - a/n (0 < a < 1) separates SU(2) (confines from every tested")
P("     coupling) from U(1) (keeps growing at weak coupling), the separation Ito-Seiler showed fixed-r decimations lack.")
P("     (For a > 1, sum_n prod_k r_k converges and SU(2) escapes at large beta too: the window is 0 < a <= 1.)")
P("  [RECORD] It does NOT repair the rigorous bridge: Tomboulis's comparison inequality needs r bounded away from 1, and the")
P("     interpolation parameter alpha* (Ito-Seiler (b)) is still unproved. The sharpened open question: does a Tomboulis-type")
P("     inequality survive a margin eps_n = a/n? Even a yes gives confinement (\'t Hooft string tension) at every lattice")
P("     coupling for SU(2), which is NOT the continuum mass gap the Clay problem asks for.")

P("=" * 100)
P("READING. Parts A-B reproduce the published obstruction; part D finds that a vanishing margin separates the groups in the")
P("hierarchical model. No rigorous bridge follows (see the RECORD lines). D-YM2 stays shut.")
out["n_checks"] = NC[0]; out["fails"] = FAILS
json.dump(out, open(os.path.join(HERE, "swing3_results.json"), "w"), indent=1, default=str)
P(f"\n{NC[0] - len(FAILS)}/{NC[0]} checks passed" + ("" if not FAILS else f"; FAILED: {FAILS}"))
raise SystemExit(1 if FAILS else 0)
