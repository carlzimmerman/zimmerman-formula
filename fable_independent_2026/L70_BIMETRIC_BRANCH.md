# L70 — the last open branch: the ghost-free derivative-bimetric MOND subspace

`L70_bimetric_branch.py` + `.out` — **19 checks, 16 PASS, 3 FAIL; every one of the nine controls passes and
every FAIL is the finding.** Runs in ~4 s, exit 0. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt)
on the one dimensional number (§C.4). Independently-written symbolic machinery (its own christoffel /
five-invariant / Stückelberg code).

---

## 0. The answer in one line

> **The Boulware–Deser ghost RETURNS the moment the MOND coupling is switched on.** On the ghost-free
> (lapse-velocity-free) 2-D subspace the transverse vector acquires a fourth-order Ostrogradsky operator
> whose prefactor is `−½(2u₀+u₁)`, and the static-NR MOND acceleration is `a = −2(2u₀+u₁)` — the *same*
> factor — so `a ≠ 0` **is** the ghost. The ghost-free tuning holds only at `a = 0`, exactly the MOND-dead
> point. **The last open branch of L61's foliation theorem is CLOSED at the mode-health gate; the
> exclusive-OR table gains no counterexample.** This independently confirms the lead's WF2 suite of
> 2026-09-09, with no disagreement.

---

## 1. What was open, and what the record already said

L61 (this lane) searched the three branches PAPER9 / L31's foliation theorem leaves permitted and closed two
by gates run there: branch 1 (≥3 Lorentz-invariant modes) at the lensing gate generically, branch 3
(non-minimal coupling) at the tensor-speed gate. It deliberately left **branch 2, two metrics, OPEN**, at
one calculation the record already names as decisive and un-run.

**The record was read first, as the brief requires** (`project_relativistic_mond_closure_2026`,
`qwen_claude_field_theory/closure_2026/bimetric_secondfield/`):

- the single-metric pincer (DC-013 + DC-019) **explicitly does not cover bimetric**;
- **DC-018** (reproduced here at A7): standard ghost-free dRGT / Hassan–Rosen bigravity's helicity-0
  Galileon sector cannot give MOND's `1/r` — `π' ~ r^(1−3/n)`, needing the non-integer `n = 3/2`;
- with the **complete** 5-invariant connection-difference basis (`C = Γ(g) − Γ(ĝ)`, matter on `g` only) the
  background-independent lapse-velocity-free ("ghost-free at `a=0`") subspace is **2-D**,
  `(c₁..c₅) = (−u₀, −u₁/2, −u₁/2, u₀, u₁)`, and contains MOND-alive directions off the f(Q) line;
  **T4−T1** gives static-NR MOND acceleration `a = −4` **and** lensing source `b = −8`, both nonzero;
- health with the MOND coupling ON was recorded **UNDECIDED**, waiting on "the covariant Hamiltonian count on
  the `a ≠ 0` sub-family (7 healthy vs 8 with the BD ghost) plus a coupled two-metric lensing solve that must
  not inherit `α₃ = −1`."

**The lead ran exactly this, in parallel, on 2026-09-09** (WF2 suite). This lane is the independent second
computation the CHARTER requires; it reproduces the result with its own code and reports agreement.

---

## 2. Controls — nine, all PASS

| control | reproduced here | published |
|---|---|---|
| **A1–A4** mode counts | GR **2**, GR+scalar **3**, khronometric **3**, Einstein-aether **5** from `N=(P−2F−S)/2` | L39/L61, PAPER9 |
| **A5** ghost-free bimetric | `P=24, F=4, S=2 → N=7` (2 massless + 5 massive) | Hassan–Rosen 7 |
| **A6** with the BD mode | `P=24, F=4, S=0 → N=8` (sixth mode is the ghost) | the record's 7-vs-8 fork |
| **A7** DC-018 no-MOND | integer `n∈{1,2,3,4}→ r^−2, r^−1/2, r^0, r^1/4`; MOND needs `n=3/2` | galileon_scaling_theorem |
| **A8a** EH ghost-detector | pure-EH TT graviton healthy & luminal (`ω²=κ²`, `+¼` kinetic) | Einstein-Hilbert |
| **A8b** EH ghost-detector | pure-EH transverse vector `W=diag(0,½)` — auxiliary + healthy, **no ghost** | the detector's zero point |

The A8 pair is load-bearing: it fixes the detector's zero point, so the negative eigenvalue found on the
`a ≠ 0` direction is a genuine ghost and not a gauge artefact of the counting scheme.

---

## 3. The crux — does the BD ghost return when `a ≠ 0`? YES. (PART B)

- **B1 PASS** — the lapse-velocity-free subspace, re-derived independently on a *generic* FRW pair (the `cᵢ`
  are action constants, so the tuning must hold background-independently), is **2-D** and equals the recorded
  `(−u₀, −u₁/2, −u₁/2, u₀, u₁)`.
- **B2 PASS** — the static-NR coefficients, independently expanded, are `a = −4u₀−2u₁ = −2(2u₀+u₁)`,
  `b = −8(u₀+u₁)`, `x = 8u₁`; at **T4−T1** `(u₀,u₁)=(1,0)`: `a=−4, b=−8, x=0`, reproducing the record.
- **B3 PASS** — the relative-diffeomorphism Stückelberg transverse vector `ε₀₁=ωA₁, ε₁₃=κA₁` (which the EH
  operator annihilates — pure gauge) picks up
  **`L_A₁ = −½(2u₀+u₁)(ω²−κ²)² A₁²`**, a **degree-4** momentum operator. Its prefactor and the MOND
  acceleration `a` are *both* proportional to `(2u₀+u₁)`: they vanish together.
- **B5 FAIL [CRUX]** — a fourth-order kinetic operator is, by Ostrogradsky, an extra phase-space DOF with a
  Hamiltonian unbounded below: the BD second-class pair that held `N=7` at `a=0` is destroyed (`S: 2→0`) and
  the sixth mode propagates, `N: 7→8`. The direct time-kinetic matrix at T4−T1 is
  **`W = diag(−2, 9/2)`, `det W = −9 < 0`** (one negative eigenvalue), against the pure-EH zero point
  `W = diag(0, ½)`.
- **B6 PASS** — this is not a Minkowski artefact. Expanding T4−T1 around a static MOND background
  `(p=∂Φ, q=∂Ψ)` gives the transverse-vector principal symbol `W = diag(−2M′, 4M′)`,
  **`det W = −8M′² < 0` for every background with `M′ ≠ 0`**; the deep-MOND law `M(T)=(−T)^{3/2}` gives
  `det = −72p²−144q² < 0`. The only escape, `M′=0`, is the degenerate no-MOND point.

> **The ghost-free condition is a tuning of the interaction; switching on the MOND coupling detunes it.**
> `a ≠ 0 ⟺ (2u₀+u₁) ≠ 0 ⟺` the transverse vector is a higher-derivative ghost.

---

## 4. The gates, run anyway (PART C) — a count alone does not close a branch

| gate | verdict | number |
|---|---|---|
| **C1 lensing vs dynamics** | **FAIL** | in the MOND branch `γ = Q′/P′ = u₁/(2(u₀+u₁))`, at T4−T1 `γ=0 → M_dyn/M_lens = 2` (under-lenses 2×), **not ≈1**; `γ=1` requires `u₁=−2u₀`, which gives `a=0` (MOND-dead). Enhancement ⟺ slip is **locked** (DC-013). The EH-dominated far exterior is Newtonian (no MOND at all, DC-018). |
| **C2 tensor speed** | **PASS** | `c_T² = 1` **exactly**, independent of `λ=a₀²`, for both polarisations, positive kinetic — no GW170817 tension despite the massive graviton. The one gate this subspace passes. |
| **C3 preferred frame / α₃** | **PASS (moot)** | the longitudinal block prefactor is `(2u₀+u₁)(κ²−ω²)`: the relative sector propagates luminally (hyperbolic/**retarded**), and with two dynamical metrics and no absolute element `α₃ = 0`. It does **not** inherit the MMG `α₃ = −1` liability. |
| **C4 excess-spent-once** | **PASS (binds)** | L61 PART B's branch-independent theorem follows the second metric: the only new escape is mediating the cold pull through the mass term, a Yukawa `(1+mr)e^{−mr}`; tuning `η(10 kpc)` to the L61 ceiling (0.582 canonical / 0.486 alt) forces Compton wavelength **7.00 / 5.80 kpc** and `η(r_s) = 1.12e−7 / 2.64e−9` — the CMB driving that fixed the abundance is switched off. Wrong range ordering, both footings. |

So even setting the ghost aside, the subspace fails the lensing gate that killed the single-metric branches
(it does **not** deliver `M_dyn/M_lens ≈ 1` in the MOND regime), and the excess-spent-once theorem binds it.
Its only clean pass is the tensor speed.

---

## 5. Verdict

**VERDICT FAIL** — the two-metric branch is **not** a live MOND candidate.

### Three-sentence verdict on whether the last open branch is alive

**It is not alive: the Boulware–Deser sixth mode returns the instant the MOND coupling is switched on,
because on the ghost-free 2-D subspace the transverse vector acquires the fourth-order Ostrogradsky operator
`L_A₁ = −½(2u₀+u₁)(ω²−κ²)²A₁²` whose prefactor is the very factor `(2u₀+u₁)` that carries the MOND
acceleration `a = −2(2u₀+u₁)`, giving a direct kinetic matrix `W=diag(−2,9/2)`, `det=−9<0`, at T4−T1 and
`det W=−8M′²<0` on every MOND background — so the ghost-free tuning holds only at `a=0`, the MOND-dead
point.** **Even granting health, the subspace fails the lensing-versus-dynamics gate that killed the
single-metric branches — its MOND branch gives `M_dyn/M_lens = 2`, not the observed `≈1`, and `γ=1` forces
`a=0` — while it does cleanly pass the tensor-speed gate (`c_T²=1` exactly) and does not inherit the MMG
`α₃=−1`, and the branch-independent excess-spent-once theorem binds it through a wrong-ordered Yukawa.**
**This closes the last open branch of the programme's own foliation theorem: the exclusive-OR table now has
no counterexample, and this lane independently reproduces the lead's 2026-09-09 WF2 suite on every number
with no disagreement.**

---

## 6. Caveats, stated rather than buried

1. **The statement is bounded to the local derivative-bimetric action** — two Einstein–Hilbert terms plus
   the quadratic 5-invariant connection-difference interaction, matter on `g` only. It is **not** a universal
   no-go for all nonlocal or non-connection-difference bimetric theories. A new action that removed the
   vector `□²` term while keeping `a ≠ 0` would have to redo the Hamiltonian, lensing, cosmology and
   stability analysis from scratch (as the lead's report also notes).
2. **The ghost count is done at the level of the quadratic action's kinetic operator** (Stückelberg
   helicity decomposition + principal symbol), calibrated against a pure-EH zero point (A8). The
   Ostrogradsky → extra-DOF step is the standard theorem, invoked, not re-proved from a full covariant
   Dirac–Bergmann algorithm; the nonlinear-background principal symbol (B6) strengthens it beyond a
   Minkowski quadratic test.
3. **C4 imports L61's η-ceiling** (0.582 / 0.486, the ε=0 generous criterion) and reproduces only the Yukawa
   transmission; the full branch-independent theorem is L61 PART B, cited.
4. **Nothing here favours this framework over ΛCDM and nothing constrains ΛCDM.** The cold component, its
   abundance and its galaxy profile are ΛCDM's, imported wholesale; κ remains fitted.
5. **This is a KILL of a branch, verified as hard as a survivor would be.** It is as valuable as finding a
   live candidate: the foliation theorem's exclusive-OR table is now complete.

---

## 7. Reproduction

```
python3 fable_independent_2026/L70_bimetric_branch.py
```

Exit 0, ~4 s. **19 checks: 16 PASS, 3 FAIL.** Nine controls (A1–A8b) rebuild the four published mode counts,
the two-metric 7-vs-8 fork, DC-018's Galileon scaling, and the Einstein–Hilbert ghost-detector zero point.
The three FAILs are the findings: **B5** (the BD ghost returns with `a ≠ 0`), **C1** (the lensing gate,
`M_dyn/M_lens = 2 ≠ 1`, locked to enhancement), and the **VERDICT** (the branch is not alive).
Cross-checked against the lead's `qwen_claude_field_theory/closure_2026/bimetric_secondfield/` WF2 suite;
agreement is complete.
