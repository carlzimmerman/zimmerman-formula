# SALVAGE SYNTHESIS — 2026-07-16

Finishing the VERIFY lanes that died on a spend limit and synthesizing where the day's
compute landed across the fronts touched. Framework: de Sitter–Unruh **modified-inertia**,
a0 = cH_Λ/Z = **9.36e-11** (canonical, ρ_DE) / **1.13e-10** (alt, ρ_total/cH0); own
ν(y)=√(1+1/y); reasoned from its own premises. Both footings noted where they matter.
No result here is claimed as a proof of the framework, and none as a clean kill of it.

All deliverables live in prep_2026 subdirs; the frozen repo was not touched.

---

## 1. The three verified results

### RING — ring-by-ring MI RAR exactness / QUMOND-same-ν discriminant → **UPHELD**
`/Users/carlzimmerman/new_physics/prep_2026/mi_fingerprint/VERIFY_ring.md`

- Reproduction: `ring_by_ring.py` exit 0, 7/7 CHECK PASS, all `canonical|alt` lines
  byte-identical to banked `.out` via diff; `rb1_circular_exactness.py` 15/15 PASS
  (MI ring residual <1e-12, Plummer control 1.34e-5, disk deviation 2.28%); pre-flight
  `rar_framework_a0_mlfit.py` exit 0 → **0.108 dex @ Υ=0.70**, beats reg-MOND 0.122.
- Independent from-scratch code reproduced D̄ for all four footings:
  **+0.0024** (canon/0.5), **−0.0269** (canon/0.7), **+0.0091** (alt/0.5),
  **−0.0194** (alt/0.7), N=114; pooled orthogonal-residual diff reproduced
  (canon/0.5 −0.0393±0.0146 → 2.7σ; canon/0.7 −0.0652 → 4.3σ; alt/0.5 −0.0250 → 1.7σ);
  the equal-galaxy↔precision weighting flip reproduced.
- Central conclusion holds under adversarial scrutiny: **SPARC at fixed Υ cannot decide
  between exact ring-by-ring MI and QUMOND-same-ν.** The MI/MG geometric discriminant
  |D_MI − D_MG| ≈ **0.026 dex** is smaller than every in-hand slider (Υ±0.1 → ∓0.015,
  weighting → −0.023, split → +0.028, footing → +0.007). Neither an MI win nor an MG
  kill is claimable.
- **Two qualifications for the record (neither flips the verdict):**
  (1) the "5–7σ → 1.7–2.6σ" drop is dominantly the conservative galaxy-level bootstrap +
  equal-galaxy null statistic, **not** the framework ν shrinking the offset (pooled
  offset −0.039 is *larger* than Chae's −0.021); RING_RESULTS §4 headline overstates the
  ν/a₀ role though §6 discloses it. (2) The Υ=0.5 MI-consistency sits at a M/L the
  framework's own RAR fit disfavors (0.108 dex @ 0.70 vs 0.145 @ 0.50); at Υ=0.70 the
  same statistic leans MG. Chae 6.9σ / −0.021±0.0045 quoted correctly.

### KERNEL — frequency-universality / kernel closure → **UPHELD (all four claims)**
`/Users/carlzimmerman/new_physics/prep_2026/mi_fingerprint/VERIFY_kernel.md`

- Reproduction: rb1 15/15, rb2 13/13, rb3 19/19, all exit 0, byte-identical to banked
  (rb3 MC seeded default_rng(7)); independent `independent_verify.py` reproduces all.
- (a) Ring-by-ring RAR exactness is **genuinely DERIVED** — first-moment identity
  **u·□_u u = −|a|²** is exact and worldline-general (independently re-derived by hand
  and in a curved Schwarzschild t–r metric on a non-geodesic worldline; ring residual
  ≤3.4e-13).
- (b) Frequency universality robust: figure Δν/ν = **+2.35e-8** (y=1) / +1.71e-8 (y=0.1),
  reactive minimal closure; closure-independent statement is **≪10%** (worst case
  φ ≤ 2.5e-4 rad at all orbital ω → ≤2.5e-4). So **"any O(10%) wide-binary RAR
  deviation must be EFE, not the kernel's ω-dependence" holds regardless of the O(1)
  closure ordering** — the load-bearing conclusion is robust to closure freedom.
- (c) Literal frequency closure correctly dead: |K|=1 ⇒ no MOND (sign-independent);
  secular scale τ = 2c/a0 = **203/168 Gyr**; drift sign appropriately undetermined.
- (d) Dispersion offset −0.011…−0.024 dex (closure B), epicyclic −0.326 ε² dex reproduced.
  The "measure is not free" (Herglotz + RAR ⇒ identity theorem ⇒ unique measure) claim is
  real and pins the operator's frequency response; the distinct O(1) closure freedom is
  **not** under-stated by the scripts.
- **Sole caveat (framing, flips nothing):** the headline "nothing left to tune"
  overreaches — 2.3e-8 is a minimal-closure *bound*, not a corollary of measure-uniqueness
  alone. Open: closure map beyond first moment, s=−1 sign, a0 value.

### LEDGER — CMB-fixed a0 concordance across probes → **UPHELD (3 disclosed caveats)**
`/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger/VERIFY_ledger.md`

- Reproduction: all 7 committed scripts exit 0; independent from-scratch re-derivation
  (no reuse of Carl's constants): anchor c·H0·√Ω_Λ/Z, Z=√(32π/3)=5.78881, H0=67.36±0.54,
  Ω_Λ=0.6847±0.0073 → **a0_canon = 9.3548e-11 ±0.96%**; **a0_alt = 1.1305e-10 ±0.80%**.
- One CMB-fixed a0 threads all three probe bands on both footings:
  **P1** [7.76e-11, 2.00e-10], **P2** [7.23e-11, 3.28e-10] (fit 1.975e-10, χ²/dof 38.9/14),
  **P3** [8.69e-11, 1.55e-10]; joint χ² canon **0.037 < 0.05**.
- All four nulls CONSISTENT: N1 MI-read passes 6.85 orders / MG-read of the *same* a0
  excluded 3.80 orders; N2 3.9 orders; N3 0.65σ; N4 CPT-odd sibling 119×/144× dead.
- ΛCDM NFW is a **fair competitor that WINS raw BIC** (14623 vs 149294), stated honestly —
  the framework's edge is provenance + zero per-object freedom + cross-probe rigidity,
  **not** a χ² win. No g† = 1.2e-10 borrow (framework ν used on real Brouwer2021/SPARC
  data); bands honestly wide; no forbidden language (grep clean).
- **Three disclosed caveats, none flips a row:** (1) N1's 6.8-order MI margin rests on the
  **banked, not-re-derived** `cassini_mi_evasion` computation, and the framework's own
  covariant/AeST realization reading is the *excluded* MG-read; (2) P2 canonical "INSIDE"
  is marginal — canonical inside only via B21's hot-CGM baryon file (legitimate but
  budget-driven; fiducial-budget fit is 2.11× canonical); (3) the anchor docstring's
  correlation wording is inverted (cosmetic; code and 0.96%/1.33% figures correct).

**No verified result was downgraded or refuted.** All three are UPHELD; every load-bearing
number reproduces from an exit-0 script, and the adversarial win/deficit hunts found only
framing overreaches, not number errors.

---

## 2. What the two completions found

### ONELOOP — the finite one-loop correction to ν(y)
`/Users/carlzimmerman/new_physics/prep_2026/oneloop_finite/` — 5 scripts, 37/37 checks
PASS, 3 live negative controls, exit 0.

- **δν(y) is computed and it is PROTECTED, not absorbed away by hand.** Around exact dS the
  renormalized coincident propagator [G(x,x)]_ren is a dS **constant** (dim-reg), so the
  self-energy correction D1 is exactly shape-uniform → **protection theorem: δν(y) ≡ 0 at
  O(du²)** after the Newtonian anchor, for every y*. Three machine-checked legs; flat H→0
  limit reproduces the independent Coleman-Weinberg route.
- On the **quasistatic** background (W(y)≠0) there *is* a genuine shape channel: the
  μ-independent nonanalytic (m⁴/64π²)(1+sW)²ln(1+sW), residual leading (3/2)W². Magnitude
  forks: **Fork P** (proxy-literal ρ_m = m²φ²) gives loop/tree ~2.8e38 — this indicts the
  **proxy** (CC problem routed through the vertex), *not* the framework; **Fork C**
  (physical composite ρ_m) gives ~1e-86 — a real first quantum correction to the MOND
  interpolation that is **structurally unobservable** (>70 dex below deep-MOND, RAR
  curvature, wide binaries). Both footings; anchor-window spread ≤1e-96; nothing flips.
- Scheme-independent where it counts (d³V/dM²³ = 1/(32π²M²) identical in dim-reg MS-bar and
  proper-time hard cutoff). **Honesty flags:** ρ_m = m²φ² is a stated proxy; the δν-shape
  plot uses illustrative W(y)=1/(1+y) (only the magnitude/observability verdict is
  map-independent); c_WW is an unpinned Wilson coefficient; and the "TT-vertex-zero all
  orders n" graviton-loop leg rests on a **hard-coded check(...,True)** at
  `open_doors_2026_07/mi_oneloop_tt_vertex_all_n.py` lines 56,66 (CAS-verified only n=1,2)
  — left out of scope. **Theory NOT closed:** disformal ρ_m variant, finite two-loop parts,
  all-n TT graviton protection, T_μν metric variation remain open; s, a0, Z remain inputs.

### PLANETARY — does the Herglotz kernel force the a0/2 tail suppression at planets?
`/Users/carlzimmerman/new_physics/prep_2026/planetary_doors/` — `laneK_kernel_planets.py`
16/16, independent `vfy_kernel_planets.py` 20/20, exit 0.

**Answer, reported straight as a fork: the published kernel does NOT uniquely force the
a0/2 suppression at the reading that preserves the framework's own galactic physics.**

- **(A) Constitutive / first-moment closure** (the reading the galactic ν-recovery actually
  uses): the kernel **reproduces the a0/2 tail at full strength** (<0.1%): constant sunward
  a0/2 = 4.68e-11 canon / 5.65e-11 alt, **excluded per-planet 1018× (Mercury) to
  33436×/40357× (Mars)**. The kernel does not suppress it here.
- **(B) The DC-absorption rescue is REFUTED.** The fallback that a constant a0/2 is absorbed
  into GM (shared with any ν) fails adversarially: the required fractional GM shift runs
  **613× across planets** (∝ r², not r-independent) and induces a nonzero linear-in-A
  secular perihelion precession = the observable BN11 ruled out. Reading A is simply dead at
  planets with **neither** a kernel **nor** a DC-absorption escape.
- **(C) The only kernel-level suppression is KINEMATIC, on the operator/spectral reading:**
  a bound orbit's u_μ(τ) spans only z≤0, so the tail's argument z=+(a/a0)² is unreachable →
  reactive residual 1e-28…1e-25 m/s² (10–13 orders under bounds). But that same reading
  (i) erases the framework's own RAR (1−ReK ≤ 2e-6) and (ii) carries a newly-computed
  universal secular drift a0/c ~ 1e-11/yr excluded ~**246–297×** (MESSENGER Ġ/G) and
  **47–57σ** (LLR).
- **(D) The only RAR-preserving survivor** is the gated Reading-C (SPEC completion) with a
  **free ~Myr corner**: passes all planetary bounds **iff** ω_c ∈ [~1e-14, ~3.5e-14] rad/s
  (width ×1.7–2.5) — a **conditional, two-sided-open** pass, falsifiable by an ephemeris
  secular refit (×3 closes it) or wide binaries.
- **Q2 scoreboard:** Door A / MG-own-ν Q2 = 2.5–3.3e-26 = **4.8–6.4× the Park+2026
  5.2e-27 ceiling (+13 to +17.5σ — the inherited wall)**; Door C / MI Q2 = 7.4e-34
  (invisible). Everything here discriminates **between the framework's own doors**
  (A vs B vs C), **never framework-vs-ΛCDM** (GR predicts zero anomaly at planetary
  accelerations, healthy MOND-family near-zero). Reading-dependent, closure-free corner,
  soft Ġ/G anchor (orders-robust, exact σ not) all disclosed.

---

## 3. Where the framework's distinctive content stands after today (one paragraph)

After today the framework's genuinely *derived* distinctive content is narrow but real and
survived adversarial re-derivation: the ring-by-ring RAR exactness follows rigorously from
the exact worldline identity u·□_u u = −|a|² (KERNEL-a, independently re-derived in curved
space), and the frequency-response measure is pinned by Herglotz + the RAR calibration
(identity theorem), which together make one load-bearing prediction robust to all remaining
freedom — **any O(10%) wide-binary RAR deviation must be an external-field effect, not the
kernel's frequency dependence**. Against that, the day's honest finding is that the
framework's *edge over its neighbors and over ΛCDM stays undecided on every in-hand front*:
SPARC at fixed Υ cannot separate exact MI from QUMOND-same-ν (discriminant 0.026 dex < every
slider, both footings), the CMB-fixed a0 = 9.355e-11 ±0.96% threads all three probe bands on
both footings but ΛCDM-NFW still wins raw BIC (the framework's advantage is provenance and
zero per-object freedom, not χ²), the one-loop correction to ν(y) is protected to exactly
zero around dS and only ~1e-86 (unobservable) on the quasistatic background, and at planetary
scales the published kernel does not uniquely force the a0/2 evasion — every planetary number
discriminates only *between the framework's own doors*, while Door A's inherited Q2 quadrupole
wall (+13 to +17.5σ) still stands and MI evades it only via the unwritten off-circular
completion. Net: **no manufactured win and no manufactured deficit today** — the derived core
(RAR exactness, frequency universality, CMB-provenance a0, one-loop protection) is intact and
internally consistent, the theory is **not closed** (s, a0, Z remain inputs; disformal variant,
two-loop, all-n TT graviton protection, and the off-circular closure map are open), and the
distinctive-vs-shared boundary is exactly where it was: the clean MI-distinctive discriminators
(aligned-EFE asymmetry, non-adiabatic σ-spread) remain the live but currently underpowered
fronts, not settled ones.

---

## 4. Ranked list of what still needs running (and why)

1. **MI orbit integrator re-run** — `prep_2026/mi_integrator/` (only `EOM_DERIVATION.md`
   + `mi_integrator.py` present; **no banked `.out`, no results JSON, no VERIFY**).
   **Why it matters most:** this is the instrument that turns the off-circular closure
   freedom — the single largest source of "reading-dependent" verdicts today — into a
   *forced, falsifiable* orbital prediction. It is the direct dependency of the KERNEL
   O(1)-closure caveat, the PLANETARY Reading-C ω_c corner, and the wide-binary/σ-spread
   discriminators. Until it runs to exit 0 on both footings, those predictions stay at the
   analytic first-moment level and the planetary "which door" fork cannot be numerically
   closed.

2. **Jeanneau ALT-footing refit** — `prep_2026/highz_tfr_fork/` (Jeanneau high-z BTFR data
   present; the fork confrontation needs the a0 = **1.13e-10** footing run alongside the
   canonical 9.36e-11). **Why:** the both-footings rule is non-negotiable and the high-z
   evolving-BTFR fork is one of the few places the two footings give *different declining-vs-
   rising a0(z)* predictions, so a canonical-only result is an incomplete verdict. Cheap to
   run, directly closes a footing gap on a live front.

3. **WALLABY firing completion** — `prep_2026/wallaby_firing/` (fired **n=25** of **237**
   per-side-capable; QC-pass 50). **Why:** the aligned-EFE asymmetry is a genuinely
   MI-distinctive, MG-hard observable, but at n=25 the achieved sensitivity at AQUAL
   amplitude is ~0.2–0.5σ and **neither pre-registered kill condition can trigger**
   (needs N~1157 canonical / N~1424 alt for 3σ AQUAL-vs-Branch-B separation). Sign-trap and
   hand-verification are already locked (independent-path sign_match true). Completing the
   extraction toward the pre-registered N is what would move this from "exploratory, reported
   straight" to an actual armed discriminator — the current sample cannot decide anything.

---

*Every load-bearing number above traces to an exit-0 script in the named prep_2026 subdir.
No "proves/validates/definitely." Both footings carried where they matter. Frozen repo
untouched.*
