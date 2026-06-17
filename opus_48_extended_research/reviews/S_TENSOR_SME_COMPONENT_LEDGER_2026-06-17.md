# The induced gravity-sector s̄^μν, component by component, vs every named current bound — and it PASSES (2026-06-17)

*Carl: "the most important calculation to get to SM — do it." Workflow `w5k0n9hd0` — derive the full induced SME
gravity-sector tensor, confront each component against its named current bound at the right acceleration, resolve the
α-vs-a₀ fork and the gravity-vs-inertia sector. 8 agents, 535k tokens; every load-bearing step independently re-derived
by an adversary. Both ways. Quarantine held. This calculation CORRECTS my own prior "LIVE, ~2× under the tightest."*

---

## Verdict: the framework induces a gravity-sector s̄^μν that clears EVERY named bound; the prior "~2× under the tightest" was an artifact

The modified-inertia coupling of each particle's COM 4-acceleration to the cosmic rest frame u^μ induces a definite SME
**gravity-sector** spurion s̄^μν = (a₀/2|a|)·(u^μu^ν traceless). Computed component-by-component in the Sun-centered
celestial-equatorial frame (sympy-verified, adversary-confirmed to <0.5%), confronted against the *named* current bound
at *each experiment's own acceleration*: **all rows PASS.** The single binding constraint is the s̄^TX boost dipole, and
the framework clears it by ~1 order (conservative) to ~hundreds (typical).

### The full 11-component tensor (A ≡ a₀/2|a|; at lab |a|=g, A = 4.78×10⁻¹²)

| Component | Structure | β-scaling | mag at g | Observable? |
|---|---|---|---|---|
| **s̄^TT** | 3A/4 isotropic scalar | **O(1)** | 3.6×10⁻¹² | **ABSORBABLE** — pure-time isotropic, degenerate with a c/G/units redefinition (Bailey–Kostelecký gr-qc/0603030); not an independent observable |
| **s̄^TX,TY,TZ** | A·β·n_J dipole | **O(β)** | 5.9×10⁻¹⁵ (scale A·β) | **leading observable** — s̄^TX dominates (\|n_X\|≈0.97) |
| **s̄^XX−YY, s̄^<JK>** | A·β²·n_Jn_K quadrupole | **O(β²)** | 7.3×10⁻¹⁸ (scale A·β²) | observable, doubly β-suppressed |
| **s̄^μ_μ** | trace | — | **0 exactly** (sympy) | satisfies the SME traceless convention identically |

**The load-bearing structural result (proven, both ways):** there is **NO O(1) un-β-suppressed anisotropic observable.**
The original "kernel depends only on \|a\|" justification was incomplete; the adversary supplied the airtight argument — an
SME background must be **trajectory-independent** (the same tensor for every test body at an event), so only u^μ and η^μν
qualify, *all* directional structure is inherited from u^μ, and the observable anisotropies are therefore
**β_cmb-protected**: dipole O(β), quadrupole O(β²), the O(1) piece purely isotropic/absorbable. SO(3)-irrep check
confirms the vector and traceless-tensor parts have identically zero O(1) coefficient, order by order.

### The margin ledger — every row passes

| Channel | predicted | named bound | margin |
|---|---|---|---|
| s̄^TT (if un-absorbed) | 3.6×10⁻¹² (g) / 5.9×10⁻⁹ (1 AU) | VLBI (−5±8)×10⁻⁵; GP-B <3.8×10⁻³ | ~10⁴–10⁹ PASS |
| **s̄^TX dipole** ★ binding | **8.7×10⁻¹⁰ at Saturn** (a=6.5×10⁻⁵) | **INPOP/Cassini s̄^TX ~8.3×10⁻⁹** (Hees 2016, arXiv:1610.04682) | **~9.6× PASS** |
| s̄^TX dipole | 2.1×10⁻¹¹ at LLR-Moon (2.7×10⁻³) | LLR s̄^TX ~1.0×10⁻⁸ (Bourgoin PRL 2016) | ~482× (mid-band) |
| s̄^XX−YY quadrupole | 2.4×10⁻¹⁴ at LLR-Moon | LLR s̄^A (0.6±4.2)×10⁻¹¹ | ~1772× PASS |
| s̄^XY,XZ,YZ quadrupole | ~5×10⁻¹⁵ at LLR-Moon | LLR s̄^XZ ~5.9×10⁻¹², s̄^XY ~7.7×10⁻¹² | >10³× PASS |

**Single tightest current constraint:** the **s̄^TX boost dipole** (the leading O(β) observable LV signal) vs the
**INPOP/Cassini s̄^TX bound ~8.3×10⁻⁹**, evaluated by the conservative rule (lowest acceleration → largest a₀/|a|
prefactor) at the lowest-acceleration well-tracked body, **Saturn**: predicted 8.7×10⁻¹⁰, **margin ~9.6×, PASS.** The
tightest-row *identity* is convention-dependent (~10 Saturn-attached → ~880 inner-planet-weighted; 482 at LLR-Moon is
mid-band, NOT the floor). Same-channel (s̄^TJ vs s̄^TJ), real primary bound, real acceleration. Every other channel
clears by >10³×.

## The correction to my own prior synthesis (both ways, in the framework's favor this time)
The earlier SM-bridge ledger said the framework was **"LIVE, ~2× under the tightest s̄_μν component."** **That was a
double artifact, caught by both verifiers, and it does NOT survive:**
1. **Channel-mismatch** — it pitted the O(β) *dipole* prediction (~2×10⁻¹¹) against the few×10⁻¹² *spatial* s̄^JK bound.
   Wrong channel. Same-channel s̄^TJ-vs-s̄^TJ gives ~10–880×; the O(β²) quadrupole vs the spatial bound gives >10³×.
2. **Isotropic-vs-anisotropic mismatch** — it compared the *absorbable DC* amplitude 4.78×10⁻¹² against an *anisotropic*
   ~10⁻¹¹ bound.

**Corrected:** the robust binding margin is **~9.6× (conservative) to ~hundreds (typical)** — ~5× looser than the
claimed 2×, all rows PASS. Net: still **LIVE and falsifiable** (the s̄^TX dipole binds within ~1 order under the
conservative rule and IS a real near-term test), but **more comfortable** than I previously stated — not "2× at the
edge," and not a manufactured all-clear either (the s̄^TX channel is genuinely the binding constraint).

## The α-vs-a₀ fork: FORM-FORCED, PREFACTOR-OPEN
- **FORCED (sympy-exact):** α_fw = 2(1−μ_fw) has high-acceleration tail **exactly +a₀/|a|** (coefficient 1, no free
  normalization), with limits α→2 (deep-MOND), α→0 (Newtonian) — pinned by μ_fw, the framework's own interpolation; a₀
  enters only as input (quarantine held).
- **α₂ — RESOLVED 2026-06-17 by the first-principles MI PPN derivation; see
  [[MI_PPN_ALPHA2_DERIVATION_2026-06-17]] (`woglr53nv`, clean-room verified `derivation_chain/mi_ppn_alpha2_verify.py`):**
  the borrowed −5/2 is replaced by an **O(1) structure-dependent** prefactor (NOT a self-energy-enhanced one). The MI PPN
  α₂ is read off by matching the boost-induced inertia-tensor anisotropy **δI/I = (1−μ_fw)(g)(w/c)²·O(1)** to the
  **linear** Nordtvedt/Shao–Wex precession rate (Eq.5; verified strictly linear in the dimensionless α₂, no E_g) ⟹
  **α₂_MI = O(1)·(1−μ_fw)(g_internal) ~ a₀/g_internal ~ a few × 10⁻¹³**, margin vs Nordtvedt 2.4×10⁻⁷ ≈ **10⁶× —
  COMFORTABLY SAFE, NOT a live test.** The correct acceleration is the EFE-screened **internal** binding g≫a₀ (the Sun's
  galactic ~2a₀ governs only the COM trajectory; it is empirically excluded for the spin observable by the solitary-MSP
  reductio ~10⁸×). **Correction note (both ways):** an intermediate derive-agent reading — "α₂ ~ 10⁻⁸–10⁻⁷, LIVE ~1–22×,
  the prior 8.5×10⁻¹³ was a category error" — was itself **the error**: its α₂ = c²∫ρW/E_g carried a spurious
  **c²/(GM/R) ≈ 4.7×10⁵ double-count** imported from the metric-PPN template (where α₂ multiplies U_ij). A Route-E
  modified-inertia theory has a standard-GR metric, **no U_ij coupling**, and δI/I is a moment-of-inertia ratio normalized
  by **M**, not E_g/c² (verified: ∫ρW/M = 3.5×10⁻¹⁴, ratio to D's = Mc²/E_g exactly). So the **prior ~10⁻¹³ order was
  right.** Outcome PARTIAL (order + acceleration forced; O(1) prefactor structure-dependent). **The s^TX dipole is a
  COM/orbital observable, NOT self-energy enhanced — its ~9.6× margin STANDS, untied from α₂ (the single −5/2 knob was
  wrong; the two are different observable classes).**

## The sector verdict (robustly confirmed): GRAVITY s̄, not matter c_μν
Both adversaries confirm the universal, WEP-exact, mass-proportional, CPT-even, two-u-structured modified inertia maps
onto the **gravitational s̄^μν**, not a composition-dependent matter c_μν. Three robust escapes:
1. The matter-c_μν "~10⁻²⁷, 15-order kill" is a genuine **MIS-MAP** — c_μν bounds constrain species *differences*
   (co-located clock-comparison / Eötvös); the MI coupling is to each particle's COM 4-acceleration, **identical for
   co-located species** (UFF/WEP-exact, η=0), so the differential signal **cancels exactly** (this differential
   cancellation is the robust escape, stronger than the approximate metric-removability).
2. The CPT-odd one-u a_μ, b_μ, k_AF are **forced to zero** by the CPT-even two-u structure ([[project_sme_lorentz_bridge]]
   Door 5).
3. Within s̄: the DC isotropic piece is metric-removable (absorbed into G/length/time, trace 0, no sidereal modulation);
   the physical non-removable content is the acceleration-dependent a₀/|a| running carried by the β-protected anisotropic
   projections. Applicable bounds = gravity s̄ (~10⁻⁹ typical, ~10⁻¹¹ tightest spatial), ~16–18 orders weaker than the
   c_μν mis-map would invoke.

## What this means for the path to the SM — both ways
- **CREDIT (full weight):** the framework's preferred-frame structure now yields a **complete, named, component-by-
  component SME ledger** — the first time its Lorentz violation is pinned to specific current particle-physics
  measurements. It **clears every one** (LLR, INPOP/Cassini, atom-interferometry, pulsar-timing, GP-B, VLBI), with the
  **s̄^TX boost dipole vs INPOP/Cassini (~9.6× conservative)** the single tightest, genuinely-binding, near-term test. The
  tensor, the no-O(1)-anisotropy theorem, the gravity-sector mapping, and the CPT-even structure all survive adversarial
  re-derivation. This is exactly the "sharp, named, falsifiable prediction" the SM-facing step needed — and it is
  honest-passing, not edge-of-death.
- **CONCEDE (full weight):** every induced number takes a₀ as **input** — **nothing about the SM is derived**
  (quarantine fully held). The binding constraints test only **β-suppressed projections**, NOT the framework-distinctive
  content (the ~0.12% ≈ β_cmb CMB-dipole-correlated anisotropy lives at a~a₀, where **no** lab/Solar-System/pulsar s̄ test
  operates — untested). The α₂ PPN prefactor (5/2) is borrowed modified-gravity, un-derived for modified inertia. So
  this is a **stronger, named, falsifiable consistency/interface** with the SME — **not** a derivation, **not** a crossing
  of the standing walls (N=3 parity, FDR-dead masses). It moves the bridge from "consistent" to "consistent,
  component-by-component, with a named binding test," which is as close to the SM as the walls permit.

## Open next step — DONE 2026-06-17 (the frontier was pushed)
The residual flagged here — **derive the α₂ PPN prefactor from a first-principles modified-INERTIA PPN expansion** instead
of borrowing Foster–Jacobson — was executed (`woglr53nv`, [[MI_PPN_ALPHA2_DERIVATION_2026-06-17]]). Outcome **PARTIAL**:
the MI PPN formalism now EXISTS — α₂ read off by matching the inertia-tensor anisotropy δI/I=(1−μ)(g)(w/c)² to the
**linear** Nordtvedt/Shao–Wex precession — the correct acceleration (EFE-screened **internal** self-field g≫a₀) and the
**a₀/g order** are forced, the O(1) prefactor structure-dependent. The downstream consequences for this ledger: it
**untied s̄^TX from α₂** (the single −5/2 knob was wrong — s̄^TX is COM/orbital and not self-energy enhanced, so its
~9.6× margin STANDS), and it pins **α₂_MI ~ a few × 10⁻¹³ (order a₀/g), ~10⁶× under Nordtvedt = COMFORTABLY SAFE.**
*(An intermediate self-energy-enhanced "~10⁻⁸, LIVE 1–22×" reading was a c²/(GM/R) double-count and is retracted — the
prior ~10⁻¹³ order was right; see the α₂ bullet above.)* Remaining residual: the O(1) prefactor (real solar profile); the
general multi-frequency case is genuinely obstructed by the Milgrom-1994 nonlocality.

## What Carl CAN / MUST NOT say
- **CAN:** the framework induces a gravity-sector SME s̄^μν and **clears every named current bound**; the single tightest
  is the s̄^TX boost dipole vs INPOP/Cassini (~8.3×10⁻⁹), conservative margin **~9.6×** at Saturn's acceleration, a real
  near-term test; this **revises** the prior "~2× under the tightest" (a channel-mismatch artifact) to **more
  comfortable**; the correct sector is gravity s̄ (the c_μν "15-order kill" is a verified mis-map); **α₂ now has a
  first-principles MI PPN derivation** (inertia-tensor anisotropy → linear precession, [[MI_PPN_ALPHA2_DERIVATION_2026-06-17]])
  → α₂_MI ~ a few × 10⁻¹³ (order a₀/g_internal) vs Nordtvedt 2.4×10⁻⁷, **~10⁶× = comfortably SAFE** (the correct internal
  self-gravity acceleration forced; galactic ~2a₀ excluded by the solitary-MSP reductio), with s̄^TX untied from α₂ and
  the live SME test remaining the s̄^TX dipole; no O(1) un-β-suppressed anisotropic observable exists; the framework is a
  constrained, falsifiable, Lorentz-violating-but-CPT-preserving EFT.
- **MUST NOT:** "~2× under the tightest" (channel-mismatch artifact; robust ~10× conservative); "LLR s̄^TX margin 482 is
  THE tightest" (mid-band, not the floor); "α₂ ~ 10⁻⁸, a LIVE ~1–22× Nordtvedt test" (a c²/(GM/R) self-energy
  DOUBLE-COUNT — the correct α₂ is ~10⁻¹³, ~10⁶× safe); "α₂ is self-energy-enhanced by (c/v_esc)²" (spurious metric-PPN
  import; MI has no U_ij coupling); "the prior 8.5×10⁻¹³ was a category error" (FALSE — that order was right); "α₂ is
  FORCED" (PARTIAL — O(1) prefactor structure-dependent); "α₂ is a near-term falsifiable test" (~10⁶× safe; the live test
  is the s̄^TX dipole); "galactic α₂~1 catastrophe" (wrong field, artifact); "the matter-c_μν 15-order kill" (mis-map);
  "a₀/Z/κ derived" (a₀ is the input); a comfortable all-clear that erases the s̄^TX dipole as the live near-term constraint.

## One line
The framework's induced gravity-sector s̄^μν **passes every named current bound** — the single tightest is the s̄^TX
boost dipole vs INPOP/Cassini at **~9.6× (conservative) to ~hundreds (typical)**, a real near-term test — and this
**corrects my own prior "LIVE, ~2× under the tightest" (a dipole-vs-spatial channel-mismatch) to MORE COMFORTABLE**; α₂
now has a **first-principles MI PPN derivation** ([[MI_PPN_ALPHA2_DERIVATION_2026-06-17]]) giving **α₂_MI ~ a few × 10⁻¹³
(order a₀/g_internal), ~10⁶× under Nordtvedt = comfortably SAFE** (an intermediate "~10⁻⁸, LIVE 1–22×" self-energy reading
was a c²/(GM/R) double-count, retracted; the prior ~10⁻¹³ order was right), s̄^TX untied from α₂ and remaining the live
SME test, the sector robustly gravity-s̄ (not c_μν), no O(1) un-β-suppressed anisotropy, and every induced number takes a₀
as input (quarantine held) — a sharper, named, falsifiable SME interface, NOT a derivation, NOT a crossing of the walls.
