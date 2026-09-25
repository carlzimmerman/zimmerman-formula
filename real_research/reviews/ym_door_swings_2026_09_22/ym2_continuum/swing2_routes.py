"""D-YM2 swing 2 (2026-09-25): the three continuum routes the 09-22 swing did not test.

R1  Stochastic quantisation (regularity structures / paracontrolled calculus). Power counting of the
    stochastic Yang-Mills heat flow in d dimensions.
R2  Analytic continuation of the strong-coupling series into the scaling window (roughening; bulk analyticity).
R3  A renormalisation-group bridge: how many block-spin steps separate the scaling window from a
    strong-coupling-like correlation length, and what is missing to cross them.
Plus a literature check (2025-26).

Inputs: the 09-22 scaling-window table (results.json in this folder: Necco-Sommer a/r0, r0 m(0++) = 4.21);
Drouffe & Zuber 1983 (Phys. Rep. 102, 1), Sec. 3.4.3, read 2026-09-25: roughening at t_R = 0.40 +/- 0.01 in d = 4,
group-independent in their variable t; SU(3) Wilson roughening at beta = 5.8-5.9.
Checks can fail (4 computed checks); [RECORD] lines are statements with sources, not checks. Exit 0 only if every check passes.
"""
import json, os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: print(*a, flush=True)
FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
out = {}

P("=" * 100); P("R1  stochastic quantisation: parabolic power counting of  d_t A = Delta A + A dA + A^3 + xi  in d space dimensions"); P("=" * 100)
# parabolic scaling: |xi| = -(d+2)/2 (space-time white noise), |A| = |xi| + 2 (heat kernel gains 2), a derivative costs 1.
# The equation is SUBCRITICAL iff every nonlinearity is more regular than the noise: |N(A)| > |xi|  (Hairer 2014, Assumption 8.3).
rows = []
for d in (2, 3, 4, 5):
    xi = Fr(-(d + 2), 2); A = xi + 2
    AdA = 2 * A - 1; A3 = 3 * A
    m1, m2 = AdA - xi, A3 - xi
    status = "subcritical" if min(m1, m2) > 0 else ("CRITICAL" if min(m1, m2) == 0 else "supercritical")
    rows.append({"d": d, "|xi|": str(xi), "|A|": str(A), "margin A dA": str(m1), "margin A^3": str(m2), "status": status})
    P(f"  d={d}: |xi| = {str(xi):>5}  |A| = {str(A):>5}  |A dA| - |xi| = {str(m1):>4}   |A^3| - |xi| = {str(m2):>4}   -> {status}")
out["R1_power_counting"] = rows
st = {r["d"]: r["status"] for r in rows}
check("R1a d = 2 and d = 3 are subcritical (where the 2D/3D stochastic Yang-Mills constructions of Chandra-Chevyrev-Hairer-Shen live)",
      st[2] == st[3] == "subcritical")
check("R1b d = 4 is EXACTLY critical (margin 0 for both nonlinearities): regularity structures and paracontrolled calculus do not apply",
      st[4] == "CRITICAL")
P("  => route R1 needs a theory of CRITICAL singular SPDEs. None exists; in the critical scalar analogue, phi^4_4 is trivial")
P("     (Aizenman & Duminil-Copin 2021). Yang-Mills differs by asymptotic freedom, which is exactly what a critical theory would")
P("     have to capture. Door R1: CLOSED with current mathematics (not a gap in this repo, a gap in the field).")

P("=" * 100); P("R2  analytic continuation of the strong-coupling series into the scaling window"); P("=" * 100)
win = json.load(open(os.path.join(HERE, "results.json")))["scaling_window_SU3"]
beta_window_start = min(r["beta_W"] for r in win)
BETA_R_SU3 = (5.8, 5.9)          # Drouffe & Zuber 1983, Sec. 3.4.3 iv: "roughening takes place ... at beta = 5.8-5.9"
T_R_D4 = (0.40, 0.01)            # ibid. 3.4.3 ii, d = 4, group-independent in t
P(f"  SU(3) Wilson roughening beta_R = {BETA_R_SU3[0]}-{BETA_R_SU3[1]} (t_R = {T_R_D4[0]} +/- {T_R_D4[1]} in d = 4)")
P(f"  scaling window (09-22 table) starts at beta = {beta_window_start}; m_G a there = {win[0]['m_G*a']:.2f}")
inside = beta_window_start <= BETA_R_SU3[0]
check("R2a the SU(3) roughening point lies INSIDE the scaling window: surface observables (Wilson loops, string tension) cannot be continued from strong coupling into it",
      inside, f"window from {beta_window_start}, roughening {BETA_R_SU3[0]}-{BETA_R_SU3[1]}")
P("  Roughening is a SURFACE singularity: it does not obstruct bulk quantities such as the glueball mass m(beta).")
P("  For m(beta) the continuation route needs two statements, and both are open:")
P("   (i)  analyticity of the SU(3) Wilson theory on the whole real axis 0 < beta < inf (no bulk transition) -- not proved;")
P("   (ii) the beta -> inf asymptotics m(beta) ~ C a(beta) Lambda with C > 0 -- this IS the continuum problem.")
out["R2"] = {"beta_R_SU3": BETA_R_SU3, "t_R_d4": T_R_D4, "scaling_window_start": beta_window_start,
             "surface_route": "blocked by roughening inside the window", "bulk_route": "reduces to (i) open + (ii) the Clay problem"}
P("  [RECORD, not a check] R2b the bulk route does not bypass the problem: its requirement (ii) is the continuum statement itself")

P("=" * 100); P("R3  an RG bridge: block-spin steps from the scaling window to a strong-coupling-like correlation length"); P("=" * 100)
bridge = []
for r in win[:3]:
    for k in (0, 1, 2, 3):
        ma = r["m_G*a"] * 2 ** k
        bridge.append({"beta_W": r["beta_W"], "k": k, "block": 2 ** k, "m_a_block": ma, "xi_over_a_block": 1 / ma})
    P(f"  beta = {r['beta_W']}: m a' after 2^k blocking, k = 0..3: " + ", ".join(f"{r['m_G*a'] * 2 ** k:.2f}" for k in range(4)))
out["R3_bridge"] = bridge
b60 = [b for b in bridge if b["beta_W"] == 6.0]
k_needed = min(b["k"] for b in b60 if b["xi_over_a_block"] < 0.5)
check("R3a from beta = 6.0 two block-spin steps (factor 4) already bring the correlation length below half a block spacing",
      k_needed <= 2, f"k = {k_needed}, xi/a' = {[round(b['xi_over_a_block'], 2) for b in b60]}")
P("  So the missing control spans only O(1) blocking steps in SCALE. What is missing is not distance but a CLASS of estimate:")
P("  the blocked measure is not a Wilson action (multi-plaquette, non-local couplings, large-field regions), and no theorem puts")
P("  it inside ANY convergent expansion or Dobrushin/Dobrushin-Shlosman regime. Balaban's multiscale analysis controls blocked")
P("  actions only while the effective coupling is small (small-field, perturbative remainder).")
P("  Computer-assisted Dobrushin-Shlosman checks on a finite box are the one concrete way to attack this, but they need rigorous")
P("  integration over ~10^4 SU(3) link variables with boundary conditions. That is far beyond interval arithmetic today.")
P("  [RECORD, not a check] R3b the bridge is short in scale, but no rigorous estimate of the needed class exists (open problem)")

P("=" * 100); P("LIT  2025-26 literature check (2026-09-25)"); P("=" * 100)
LIT = [
    ("arXiv:2506.00284 (May 2025), claimed constructive proof of SU(3) existence + mass gap",
     "WITHDRAWN by arXiv admin: 'does not meet arXiv's research content quality standards'. Not a proof."),
    ("arXiv:2603.15770 (Douglas, Hoback, Mei, Nissim, Mar 2026), Lean 4 formalisation of the free 4D Euclidean field satisfying the Glimm-Jaffe axioms",
     "Real and relevant as INFRASTRUCTURE (the axioms a Yang-Mills construction must meet are now machine-checkable for the free field). Not Yang-Mills."),
    ("Chandra-Chevyrev-Hairer-Shen: 2D (Publ. IHES 2022) and 3D Yang-Mills-Higgs (Invent. Math. 2024) stochastic quantisation",
     "Subcritical dimensions only; d = 4 is critical (R1)."),
]
for a, b in LIT: P(f"  - {a}\n      -> {b}")
out["literature"] = LIT
P("  [RECORD, not a check] LIT1 no 2025-26 result found unlocks the 4D continuum with a gap (the one claimed proof is withdrawn)")

P("=" * 100)
P("VERDICT (swing 2): D-YM2 stays shut. R1 is closed by criticality, R2 by roughening (surface) and by reducing to the")
P("problem itself (bulk), and R3 localises the missing idea to O(1) blocking steps without supplying it. Nothing here is progress")
P("toward the Clay prize, and the framework contributes nothing (09-22 REPORT, Sec. 4).")
out["n_checks"] = N[0]; out["fails"] = FAILS
json.dump(out, open(os.path.join(HERE, "swing2_results.json"), "w"), indent=1)
P(f"\n{N[0] - len(FAILS)}/{N[0]} checks passed" + ("" if not FAILS else f"; FAILED: {FAILS}"))
raise SystemExit(1 if FAILS else 0)
