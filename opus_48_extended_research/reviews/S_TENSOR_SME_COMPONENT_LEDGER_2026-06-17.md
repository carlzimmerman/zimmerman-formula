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
- **OPEN:** the PPN dictionary factor α₂ = −(5/2)α is the borrowed **Foster–Jacobson Einstein-aether/khronometric
  MODIFIED-GRAVITY** map, whose kinetic coefficients a modified-INERTIA theory does not possess. The gravity-vs-inertia
  translation is un-derived, so the prefactor is an O(1)-to-zero knob. (This softens the construct's flat "FORCED.")
- **α₂ severity (both ways):** the earlier "~6× LIVE vs Nordtvedt" used the *orbital* field (5.9×10⁻³) — an arbitrary
  middle choice. The Nordtvedt solar-spin test is a **self-gravity** effect, so the physically-correct field is the Sun's
  internal binding (g≫a₀): α₂ ~ 8.5×10⁻¹³ = **~2.8×10⁵× SAFE.** The deep-MOND "galactic α₂~1, 4×10⁶× over" is the **wrong
  field** for a self-energy effect (samples internal g≫a₀ — Sanders camouflage) — an **artifact, not a tension.** No
  robust α₂ deficit. Residual genuine uncertainty: which acceleration governs the self-gravity precession in an MI
  realization — unresolved (no first-principles MI PPN derivation exists).

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

## Open next step (if pushed further)
The one genuine residual: **derive the α₂ PPN prefactor (and the s̄^μν normalization) from a first-principles modified-
INERTIA PPN expansion**, rather than borrowing the Foster–Jacobson modified-gravity dictionary — that is the only way the
α₂ prediction becomes a forced number rather than form-forced/prefactor-open, and the only way the binding s̄^TX margin
becomes a sharp prediction rather than a conservative band. No MI PPN formalism currently exists; building it is the
honest frontier.

## What Carl CAN / MUST NOT say
- **CAN:** the framework induces a gravity-sector SME s̄^μν and **clears every named current bound**; the single tightest
  is the s̄^TX boost dipole vs INPOP/Cassini (~8.3×10⁻⁹), conservative margin **~9.6×** at Saturn's acceleration, a real
  near-term test; this **revises** the prior "~2× under the tightest" (a channel-mismatch artifact) to **more
  comfortable**; the correct sector is gravity s̄ (the c_μν "15-order kill" is a verified mis-map); α₂ is FORM-forced
  (a₀/|a| tail, coeff 1) but PREFACTOR-OPEN, and SAFE (~2.8×10⁵× at the self-field) on the directly-applicable
  solar-spin test; no O(1) un-β-suppressed anisotropic observable exists; the framework is a constrained, falsifiable,
  Lorentz-violating-but-CPT-preserving EFT.
- **MUST NOT:** "~2× under the tightest" (channel-mismatch artifact; robust ~10× conservative); "LLR s̄^TX margin 482 is
  THE tightest" (mid-band, not the floor); "α₂ is FORCED" (form-forced, prefactor-open); "α₂ is 6× at the edge of
  Nordtvedt" (orbital-field choice; self-field ~2.8×10⁵× safe); "galactic α₂~1 catastrophe" (wrong field, artifact);
  "the matter-c_μν 15-order kill" (mis-map); "a₀/Z/κ derived" (a₀ is the input); a comfortable all-clear that erases the
  s̄^TX dipole as a live test.

## One line
The framework's induced gravity-sector s̄^μν **passes every named current bound** — the single tightest is the s̄^TX
boost dipole vs INPOP/Cassini at **~9.6× (conservative) to ~hundreds (typical)**, a real near-term test — and this
**corrects my own prior "LIVE, ~2× under the tightest" (a dipole-vs-spatial channel-mismatch) to MORE COMFORTABLE**; α₂
is FORM-forced/prefactor-open and SAFE (~2.8×10⁵× at the self-field, not a 6× edge), the sector is robustly gravity-s̄
(not c_μν), no O(1) un-β-suppressed anisotropy exists, and every induced number takes a₀ as input (quarantine held) — a
sharper, named, falsifiable SME interface, NOT a derivation, NOT a crossing of the walls.
