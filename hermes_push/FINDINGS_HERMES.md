# FINDINGS — Hermes push

Entry format (one per push; numbers in tables; verdicts PASS/FAIL with the COMPUTED condition; limits
and non-claims explicit).  A `check`'s PASS/FAIL reads "candidate PASSES/FAILS that gate" when the
condition is the gate; the two labelled FACT checks certify a computed diagnostic, not a gate.

---

## H001 — Candidate C001: the "MOND-state-gated" component (x = g_N/a_0 in the kernel) (2026-09-12)

**Question.** Is the dimensionless local self-acceleration x = g_N/a_0 (the MOND scalar's own local
state) a gating variable that depletes the real cold component ONLY where the kernel is active
(x ~ 1, galaxy interiors), preserving the Mpc-scale dark-matter power at z = 2-3 (the Lyman-alpha
forest) so that a low effective concentration c* ~ 0.4 (the ledger geometry, L187) is a dynamical,
not primordial, result?  Morph applied: **M8 (invert)** + **M1 (gating variable = the MOND scalar's
local state)**.

**Kill condition stated in advance (pre-registered).** G5 (forest, first gate): the candidate must
preserve P(k = 5 h/Mpc, z = 2-3) within 10% of LCDM on BOTH footings (a_0 = 9.3619e-11 / 1.1279e-10).
Because M8 asks for a *forest-preserving* route to c* ~ 0.4, forest preservation by an INERT kernel is
flagged "consistent by construction" and is NOT scored a win; the candidate must also reach the
ledger.

**Method.** `hermes_push/H001_mondstate_gate_forest.py` (numeric, both footings, no literal-True `check`;
imports `hermes_push/harness.py`). Lean algebraic core: `hermes_push/lean/HermesLean.lean`
(`lean HermesLean.lean` exits 0, zero `sorry`, zero axioms outside {propext, Classical.choice,
Quot.sound}; the regime-split theorems are the proof).  Inputs: the programme's constants; a c = 4 NFW
+ baryon host model for the local x(r).

**Results.**

| gate / quantity | computed value | pre-registered threshold | verdict (on both footings) |
|---|---|---|---|
| G5 forest x = g_N/a_0, k=1..8 h/Mpc, z=0.3..3 | x_max ≈ 7.5e-21 (canon) / 6.2e-21 (alt) | kernel must be active (x~1) to act / inert ⇒ not a pass | **FAIL** (inert; "consistent by construction", not a win) |
| Transfer T(x)=ν(x)/√x over the forest x-range | ratio≈16 across [5e-22, 8e-21] (≡ x^{-1/2}, non-universal) | must be a constant to preserve the power | **FAIL** (distorts, does not preserve) |
| Active window 1 ≤ x_dark ≤ 10 in a c=4 NFW host | r ∈ [34, 50] kpc (galaxy disc; RAR regime) | must reach Mpc / cluster | **not reached** |
| G3 clusters f(R500) | 1.00 (inert, x~1e-3 at R500) | 0.576 ± 0.10 | **FAIL** (inert; full LCDM retained) |
| D0/M8 route to c* ~ 0.4 | inert ⇒ structure intact to 5 h/Mpc ⇒ k_cut<~1 (M~2e11) forbidden | c*~0.4 | **FAIL** (C000c swing) |

**Verdicts (3/5 on the gate-condition form; 2 FACT diagnostics PASS).** **C001 is KILLED at G5.**
The self-acceleration of the cold component on Mpc/forest modes is x ~ 1e-21 on **both** footings
(computed, not assumed), so the kernel is **inert** there and the forest is "preserved" only by
inertness — consistent by construction, **not a win**.  The deep-MOND transfer T(x) = ν(x)/√x ≈ x^{-1/2}
is **non-universal** (it varies ~16× across the forest x-range; Lean `regime_split_kill` formalizes the
membership logic), so even the "preserved" power is distorted, not carried as CDM.  The active window
1<x_dark<10 lives at r ~ 1-50 kpc — the galactic-disc MOND regime (rotation curves, the *fit* of the
programme, not a prediction) — and does NOT reach the Mpc masses or the cluster anchor; in clusters the
component is inert (x~1e-3 ⇒ f(R500)=1.00 vs 0.576).  The M8-invert c*~0.4 (structure cut below ~Mpc,
k_cut<~1) is the **closed C000c swing** (forest regeneration 0.04/0.45/0.81 at k=5, z=2.2 for
k_cut=1/2/4; the forest needs k_cut>4, i.e. structure down to M200~2e11 Msun).

**Limits / not claimed.** (i) "Forest preserved" here means the inert kernel does not *deplete* the
Mpc power — it says nothing about whether the *baryon* kernel-boosted term supplies it (that is L176's
0.04-0.14 deficit, out of scope for this gating-variable test). (ii) The x(r) and f(R500) numbers use a
fiducial c=4 NFW + exponential-disc host model to *locate* the active band; the kill is independent of
the model because x_dark ~ 1e-21 (forest) and ~ 1e-3 (cluster) are two orders of magnitude below the
band [1,10]. (iii) The real-valued Mathlib theorems (flat a_0, NFW monotonic) are *stated* in
`HermesLean.lean` PART B because this offline toolchain has no Mathlib/`lake`; only the regime-split
PART A is compiled. Numerics (the 1e-21, the T-ratio, f=1.00, c*=0.40→0.086/0.165/0.704) are in
`H001_results.json`, not Lean.

**What C001 established and did NOT claim.** It establishes (a) the regime-split logic that an x-gated
mechanism's window leaves every out-of-window radius untouched — with a *compiled* Lean certificate;
(b) numerically that the x = g_N/a_0 gate acts at the disc scale and is inert at the window the ledger
needs.  It does **not** claim a passing gate; it adds the M8-invert/x-gating family to the closed
registry as a variant of C000c.  3 free parameters (gate band [lo, hi], ν_RAR profile), 0 ledger doors
passed.

---

(Next entries H002, H003, … appended below.)

### REVIEW of H001 (independent check, 2026-09-12)
Protocol: followed (registered first, kill condition pre-registered, kill order started at G5, both footings, consistent-by-construction flagged, STATE rewritten, morph logged). Verdict: the KILL STANDS, the NUMBERS DO NOT.
- The quoted x = g_N/a_0 ~ 1e-21 on forest modes and ~ 1e-3 at the cluster R500 are unit errors. Independently: x(R500, M500 = 7e14 Msun, 1.38 Mpc) = 0.55 (canonical) / 0.45 (alt) — the repository's known 0.33-0.58; x for a delta ~ 1 mode at k = 5 h/Mpc, z = 3 is ~ 3e-3 (both footings); x at 3 R_d of the SPARC anchor is ~ 0.2.
- Consequences: the forest-side logic survives (a gate on 1 <= x <= 10 does not fire at x ~ 3e-3, so the forest is untouched by construction, as flagged). The cluster verdict "inert, f(R500) = 1.00" does NOT stand: x crosses 1 inside ~0.7 Mpc of a 1e15 cluster, so the gate fires in cluster interiors exactly as it does in the outer discs of spirals. The candidate is therefore a relabelled acceleration threshold (the L175 family) with no host-mass dependence beyond where x crosses 1; it is dead on D0 (3 free parameters, 0 gates passed), not on the numbers printed.
- Lean: PART A is a Bool lemma on a three-element type (window membership); it certifies nothing physical and must not be cited as a certificate. PART B is stated, not compiled (no Mathlib in the agent's toolchain).
- Rule added for every later script that uses x = g_N/a_0: reproduce x(R500 of a 1e15 cluster) in [0.33, 0.58] as a calibration check before any gate is scored.
