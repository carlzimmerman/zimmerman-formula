# agentLL — THE GENERATOR QUESTION: scoping the index-1/3 source

**STATUS: CLOSED — DIRECTION-NARROWED. Bare b-family caustic KILLED as a cubic source (machine: its
normal form is Watson/power-law, all variants non-cubic); the fingerprint class proven UNIQUE to a
one-sided OSCILLATORY k=1/2 essential density (√3 = tan(π/3) fingerprints the cubic class exactly);
the b-family survives only DRESSED — a fourth-root (q=1/4) oscillatory edge measure, which the
Deser–Levin map κ ∝ x^(−1/2) converts to index 1/3 with √3 + π/3 automatic. One named confirming
calculation defined. All claims machine-backed in `agentLL_generator_scoping.{py,out}`.**

Date: 2026-06-12 (relaunch, compute-first). Repo: zimmerman-formula. Hardware: local (sympy/mpmath, dps≥30).
Task: work the mathematical fingerprint of the locked pump profile BACKWARD — what de Sitter
horizon/bath mechanism OUTPUTS an index-1/3 (cubic-saddle / Airy-class) locked spectral structure?

**The fingerprint (banked, agentHH):**

    F_req(w) ∝ (c_χ w)^(−5/3) · exp(−c̃ (c_χ w)^(1/3)) · cos(√3 c̃ (c_χ w)^(1/3) + φ̃ + π/3),
    c̃ = (3/4)·2^(2/3)·ζ̃^(2/3)

Theorem HH-1 (banked): scale-invariant pumping cannot COMPOSE the locked Gevrey-3 pair — it must be
HANDED ζ̃^(2/3) c_χ^(1/3), the 1/√3 lock, and the phase. So the generator is whatever does the handing.

**DISCIPLINE (absolute):**
- ζ̃ and the (16π/3)^(1/4) quarantine stand. NO Z claims. Any pure number reported raw + quarantined.
- Hostility to wishful steps; every claimed structure verified symbolically/numerically in
  `agentLL_generator_scoping.py` → `.out`.
- FIREWALL: the INPUT side (agentV: σ_req) is ω^(1/4)-class (fourth-root essential singularity);
  the RESPONSE fingerprint is ω^(1/3)-class. Kept distinct throughout — no cross-contamination.
  (§5.7 states a *requirement-match* between the two classes; it is flagged as such, not an identification.)

---

## 0. VERDICT

**DIRECTION-NARROWED** (no generator-candidate fully found; no scoping obstruction).

1. **The fingerprint class is a theorem-grade signature** (LL-1/LL-2/LL-3, all machine-verified):
   it is EXACTLY the Laplace image of a **one-sided density with an oscillatory k=1/2 essential
   point** (canonically: a negative-argument Airy-type density). The √3 ratio is tan(π/3) from the
   admissible cube-root saddle pair at action phases ±π/3 — UNIVERSAL for the cubic class,
   independent of every constant; the ratio tan(π/(2(k+1))) is strictly monotone in k, so
   **√3 ⟺ index 1/3 is unique**. The π/3 in the fingerprint phase is the Airy connection-formula
   quantum (one unit of the exactly-derived π/3-per-t-power phase law).
2. **Candidate (d), bare, is KILLED.** On EE's banked b-family pullback (with κ(b) reconstructed
   from the universal UV normalization — flagged), the family-edge pole CANCELS exactly in the
   response; the surviving edge exponent vanishes like √(c_χ−b); the local normal form at the
   coalescence is **LINEAR in the unfolded variable at an endpoint (Watson class) ⇒ pure power
   law** — not cubic, not Airy, not even pole–saddle exponential. Machine: slope test pinned at
   2.000001. The fixed-κ and uncancelled-pole variants land thermal (index 1) and power×log — all non-cubic.
3. **Candidate (d), dressed, is the surviving primary direction.** Conversion theorem (sympy,
   §5.6): an edge measure e^(−γ x^(−q)) on x = c_χ−b outputs transform index 2q/(2q+1) through the
   Deser–Levin map; **index 1/3 ⟺ q = 1/4 uniquely**. The map κ ∝ x^(−1/2) converts a FOURTH-ROOT
   oscillatory essential edge measure into the LL-1 k=1/2 class exactly, and then √3 + π/3 + the
   prefactor family all follow automatically (end-to-end numeric: §5.7, ratio→1 monotone).
   This is also exactly the agentV input-side index class — stated as a requirement-match only.
4. **Candidate (b) bare is killed** (dS QNMs: pure-imaginary equally-spaced ladder ⇒ Gevrey-1/
   thermal, LL-3(iii)); it survives only REBORN as the Airy-spectral-edge of the family fluctuation
   operator — the same normal-form criterion as (d)-dressed, so it folds into (d). Candidates (a)
   and (c) are graded plausible-secondary with named calculations (§6, §8).
5. **The named confirming calculation** (decides (d)-dressed): derive the pump's family measure
   ρ(b) near b = c_χ from the worldline construction on EE's banked forms.
   **PASS ⟺ ρ has an oscillatory fourth-root essential singularity cos(γ(c_χ−b)^(−1/4)+φ₀)·(powers)
   with γ = γ_req (§9). FAIL ⟹ (d)-dressed dies and the σ-hook with it.**
   No >1h computation is needed anywhere — this is an analytic derivation on banked closed forms,
   so NO agentLL_overnight.py is issued.

## 1. The fingerprint restated; what is locked vs free

Conventions: transform variable w ≥ 0; below ω ≡ c_χw where convenient. LOCKED by HH: the index 1/3;
the ratio √3 between oscillation and decay rates; the explicit +π/3 phase offset; c̃ = (3/4)2^(2/3)ζ̃^(2/3)
(ζ̃ quarantined). FREE: φ̃; overall amplitude; the −5/3 prefactor power is locked by HH but sits in the
freely-shiftable family (§3.3: t-weight law) — its value pins the density's edge weight, not the class.

## 2. LEMMA LL-1 — the Stokes geometry of a cubic saddle (the √3 lock + 2π/3 phases, derived)

Machine record: `.out` sections LL-1a–LL-1e.

- **Setup.** For a one-sided density with oscillatory essential point, f(w) = ∫₀^∞ e^(−wt) cos(β t^(−1/2)) dt;
  t = s² maps the t^(−1/2) point to the SPLIT CUBIC exponent Φ(s) = w s² ∓ iβ/s.
- **Saddle triad (sympy, exact).** Φ′=0 ⇔ s³ = −iβ/(2w): cube roots at arg s* = {−π/6, π/2, −5π/6};
  on-shell Φ(s*) = 3ws*², so Φ(s*)/(w^(1/3)β^(2/3)) = 3·2^(−2/3)·{e^(−iπ/3), −1, e^(+iπ/3)} — the
  saddle actions land at RELATIVE PHASE 2π/3 (the cube-root triad). Descent sectors of the pure
  cubic: boundaries cos3θ=0 at ±π/6, ±π/2, ±5π/6; centers {0, ±2π/3} — the Stokes triad (LL-1b).
- **The √3 lock (sympy, exact).** The admissible pair (Re Φ > 0; decay demanded of any Laplace
  transform of a locally-integrable one-sided density) sits at action phases ±π/3:
  **Im/Re = ∓√3 EXACTLY**, with β and w dropping out. The third root (phase π) is the growing
  e^(+c w^(1/3)) member — Stokes-excluded by one-sidedness (§4). So
  decay rate = (3/2)2^(−2/3)β^(2/3)w^(1/3), osc rate = √3 × decay rate, UNIVERSALLY.
- **Index 1/3 from the cubic alone (LL-1c).** u → W^(−1/3)v gives I(W) = W^(−1/3)·C₃ exactly;
  constant pinned by Ai(0) = 3^(−2/3)/Γ(2/3) (30 digits).
- **Fluctuation (sympy, exact).** Φ″(s*) = 6w exactly (β-independent) — hands the w^(−5/6)-type
  prefactor and, through the s₀ = |s₀|e^(−iπ/6) prefactor, the π/6 HALF-quantum phase
  (the "π/3 fluctuation half-phase" of the skeleton).
- **Machine quadrature vs saddle formula (LL-1d).** Rotated-contour mpmath quadrature
  (s = e^(−iπ/6)σ, both ends exponentially flat; contour passes through the saddle) against the
  two-saddle formula incl. prefactor: ratio = 1.0086 (w=10³), 1.0035 (10⁴), 1.0022 (10⁵) → 1. ✓
- **Universality table (LL-1e, sympy).** For density singularity e^(±iβt^(−k)):
  ratio = tan(π/(2(k+1))), index = k/(k+1):

  | k   | index | osc/decay ratio |
  |-----|-------|-----------------|
  | 1/3 | 1/4   | 1+√2            |
  | 1/2 | **1/3** | **√3**        |
  | 1   | 1/2   | 1               |
  | 2   | 2/3   | 1/√3            |
  | 3   | 3/4   | √2−1            |

  Strictly monotone ⇒ **√3 ⟺ k=1/2 ⟺ index 1/3, UNIQUE in the whole one-sided oscillatory-essential family.**

## 3. LEMMA LL-2 — the inverse transform of the fingerprint class is an Airy-type density

Machine record: `.out` LL-2a–LL-2d.

1. **Canonical pure-decay pair (verified to 1e-31).** Q(W) ≡ ∫₀^∞ Ai(v) e^(−W/v³) dv = (1/3)e^(−(3W)^(1/3))
   over W ∈ [0.1, 100] ⇒ **L[3^(−1/3) t^(−4/3) Ai(3^(−1/3) t^(−1/3))](w) = e^(−w^(1/3)) EXACTLY** —
   the one-sided stable-1/3 density in Airy form (known closed-form family; here verified
   independently by quadrature, no literature needed), normalization ∫g = 1 exact (A/B = 1).
2. **Oscillatory member = the fingerprint class (EXACT, not asymptotic).**
   **L[t^(−4/3) Ai(−3^(−1/3) t^(−1/3))](w) = 2·3^(1/3) e^(−w^(1/3)/2) cos((√3/2) w^(1/3))** —
   the Airy connection formula Ai(−z) = e^(iπ/3)Ai(e^(iπ/3)z) + c.c. rotates the pure-decay pair onto
   the ±π/3 saddle pair of LL-1: the √3 lock and the π/3 machinery ARE the connection formula.
   Verified at w ∈ {8,27,64,125} to ~1e-6 with the residual PROVEN to be quadrature tail truncation
   (cutoff test: 8.5e-7 → 6.8e-7), plus the exact w→0 limit 2·3^(1/3) ✓.
   *Honesty note:* the first run carried a hand-normalization slip (2/3^(2/3), exactly 3× small);
   the quadrature caught it (rel err 2.00 flat) and the closed form was corrected — the machine
   record, not the longhand, is authoritative, per discipline.
3. **The π/3 phase quantum and the (2/3) prefactor quantum (sympy, exact).** One t-power in the
   density ⟺ prefactor × (1/3)w^(−2/3) AND phase shift EXACTLY −π/3 (simplify ≡ 0). So phase
   offsets are quantized in π/3 per (2/3)-step of prefactor power (Δφ/Δp = π/2 per unit power);
   the fingerprint's explicit +π/3 is one quantum (the connection-formula unit); φ̃ absorbs the
   rest and stays free. The −5/3 prefactor power then pins the density's edge weight
   (t^(5/4)-class amplitude in the μ-law of LL-1's fluctuation), not the class.
4. **Conclusion:** the spectral density behind the fingerprint is a **NEGATIVE-ARGUMENT AIRY-TYPE
   density, one-sided, with the oscillatory k=1/2 essential point at t→0⁺**; the pure-decay
   member corresponds to positive-argument Airy (stable-1/3).

## 4. LEMMA LL-3 — the orientation theorem: what the √3 lock + one-sidedness kills

The √3 lock is a CLASS detector (LL-1e table), and the one-sidedness is an orientation detector. Kills:

- **Any quadratic saddle / index-1/2 class** (k=1 image: e^(−β/t)-type densities, diffusive/heat-kernel
  image class): predicts ratio tan(π/4) = **1 ≠ √3** (sympy one-liner). No 2π/3 triad exists for a
  quadratic exponent — its Stokes rays come in π-separated pairs.
- **Any pure power-law density** t^α: L = Γ(α+1)w^(−α−1) (sympy): NO essential factor at all —
  killed by the existence of e^(−c̃w^(1/3)) itself, before the ratio is even consulted.
- **Any KMS-thermal-only structure**: the exact sinh⁻² worldline transform (§5.1, verified 1e-25)
  is the Planck factor with Boltzmann tail e^(−2πw/κ): index 1, oscillation ratio 0. Killed twice
  (wrong index AND no locked oscillation).
- **Two-sided / non-causal spectral support**: the transform of the fingerprint class decays in
  Re w > 0; Paley–Wiener-style, that certifies ONE-SIDED density support. Two-sided support
  injects the third (growing, phase-π) cube-root member, which the fingerprint's decay excludes.
  The Stokes exclusion of the growing root is exactly the one-sidedness clause.

## 5. CANDIDATE (d) — the b-family caustic at b → c_χ [worked first and hardest]

Machine record: `.out` S4a–S4i. EE banked input (per skeleton summary): dilatation orbits =
Deser–Levin family; free pullback G_b(τ) = −H²/[16π² c_χ (c_χ²−b²) sinh²(κτ/2)], pole at b = c_χ.

1. **Exact single-orbit frequency transform (S4a).** R(w,κ) = ∫ e^(−iwτ) dτ / sinh²(κ(τ−iε)/2)
   = −(8πw/κ²)/(e^(2πw/κ)−1), verified numerically to 1e-25 (shifted-line sech² method).
   Single orbit = thermal: Boltzmann tail, Gevrey-1. (Feeds LL-3(iii).)
2. **κ(b) reconstruction (S4b — FLAGGED).** The skeleton's quote left κ unspecified. Imposing the
   universal short-distance normalization G_b → −1/(4π²τ²) forces
   **κ(b) = H/√(c_χ(c_χ²−b²))** (sympy, both roots checked). κ diverges at the family edge —
   the orbit acceleration diverges approaching the horizon, consistent with Deser–Levin
   2πT = √(a² + H²·) [CQG 14, L163 (1997); see pins, §11]. This is a RECONSTRUCTION, not a read
   of EE's banked κ; if EE's κ(b) differs, §5.4–5.5 must be re-run (the conclusion is robust for
   the fixed-κ alternative too — see 5.5).
3. **The pole CANCELS (S4c, exact).** (c_χ²−b²)^(−1) κ(b)^(−2) = c_χ/H². The family-edge pole of
   the pullback prefactor cancels exactly in the response. The naive "the pole drives the
   asymptotics" intuition dies immediately. Surviving superposition:
   F(w) ∝ w ∫db ρ(b) exp(−(2πw/H)√(c_χ(c_χ²−b²))).
4. **Bare edge and interior (S4d, S4e).** Edge: E(b=c_χ(1−x)) = √2·c_χ^(3/2)√x + O(x^(3/2)) —
   square-root VANISHING (not divergence) of the exponent at the edge:
   ∫x^σ e^(−Aw√x) dx = 2Γ(2σ+2)/(Aw)^(2σ+2) — PURE POWER LAW (sympy exact); numeric slope test
   pinned: 2.000203 → 2.000013 → 2.000001 (constant ⇒ power law, no essential factor).
   Interior: E″(0) = −1/√c_χ ≠ 0, E‴(0) = 0 (parity): ordinary quadratic saddle, and subdominant.
5. **LOCAL NORMAL FORM AT THE COALESCENCE (the prompt's question, answered).** Unfolding the edge
   with y = √x: exponent Φ_local = −(2πw/H)√(2c_χ³)·y, measure 2y dy — **LINEAR exponent × smooth
   measure at an ENDPOINT: Watson-lemma class ⇒ F_bare(w) = Σ cₙ w^(−2(n+1)), a pure power series.
   NOT CUBIC** (no Airy), and not even pole–saddle (Bessel/error, index-1/2) exponential — weaker.
   Variants: uncancelled-pole normalization → pinch gives power×log; fixed (b-independent) κ →
   pure thermal e^(−2πw/κ) (index 1). **All readings non-cubic ⇒ the BARE b-family caustic is
   killed as the generator**, robustly against the κ(b) uncertainty of 5.2.
6. **THE CONVERSION THEOREM (S4g — the salvage, sympy exact).** Dress the family with an edge
   measure e^(−γx^(−q)): the saddle of −γx^(−q) − wu₀√x gives output index 2q/(2q+1)
   (w·d ln(action)/dw computed symbolically). Table: q = {1/8, 1/6, 1/4, 1/2, 1} → index
   {1/5, 1/4, **1/3**, 1/2, 2/3}; monotone ⇒ **index 1/3 ⟺ q = 1/4 UNIQUE**. Mechanism: in
   u ≡ 2π/κ = u₀√x the fourth-root singularity x^(−1/4) becomes u^(−1/2) — the LL-1 k=1/2 class
   EXACTLY; the Deser–Levin square-root map is the 1/4 → 1/3 index converter. The √3 lock and the
   π/3 quanta then follow from LL-1/LL-2 **iff the edge measure is the oscillatory member
   cos(γx^(−1/4)+φ₀)** (pure-decay member gives the no-cos class — excluded by the fingerprint).
7. **End-to-end machine check (S4h).** F_d(w) = ∫₀^∞ cos(γx^(−1/4)) e^(−w√x) dx evaluated by
   rotated-contour quadrature vs the cubic-saddle formula: ratio 1.2522 → 1.1093 → 1.0617 → 1.0499
   (w = 10³…10⁶), monotone → 1 with O(w^(−1/3))-scale drift: **the dressed family emits the
   COMPLETE fingerprint class** — index 1/3, decay (3/2)2^(−2/3)γ^(2/3)w^(1/3), oscillation √3×,
   phase offsets in π/3 quanta, power-law prefactor family.
8. **Structural hook (firewall-respecting).** q = 1/4 is the same index class as the banked INPUT
   side (agentV σ_req, ω^(1/4) fourth-root essential). Stated strictly as a REQUIREMENT-MATCH:
   IF the pump's family measure inherits a fourth-root oscillatory structure at the edge, the
   output is FORCED to the fingerprint class through the Deser–Levin map. Whether it does is
   exactly the named calculation (§10). No identification claimed.

## 6. CANDIDATE (a) — heat-kernel / worldline proper time near a horizon turning point [scoping grade]

A linear turning point hands Airy only as a LOCAL uniform approximation; horizon transmission
(greybody) tails are thermal e^(−w/T_H) — index 1, killed by LL-3 as a global structure. For (a) to
generate the fingerprint, the cubic must sit in the TRANSFORM variable globally: i.e. the worldline
proper-time kernel's complex-s singularity nearest s=0, on the family of horizon-grazing
trajectories, must be a CUBIC branch point (then its Borel image is the LL-2 Airy density). Generic
geodesic singularities are e^(−L²/4s) (k=1 ⇒ index 1/2 — killed); a cubic requires a DEGENERATE
(fold) grazing family. Named calculation: compute the dS worldline heat kernel on the
horizon-grazing geodesic family and classify the nearest complex-s singularity (cubic vs quadratic
branch). Grade: plausible-secondary — nothing forces the fold, but nothing kills it.

## 7. CANDIDATE (b) — QNM ladder resurgence [scoping grade; bare form killed, folds into (d)]

Pure-dS static-patch QNMs are PURELY IMAGINARY and EQUALLY SPACED, ω_n = −i(2n+j+…)/ℓ-type
(López-Ortega-class results; see pins §11). An equally-spaced imaginary ladder resums to the
thermal/Gevrey-1 class (Boltzmann tail, ratio 0): **bare (b) is killed by LL-3(iii)**. The salvage
is spectral: the fingerprint's LL-2 density is the AIRY density — the universal SPECTRAL-EDGE
density. If the locked kernel's fluctuation operator on the b-family has edge normal form
−d²/dx̃² + (linear ramp) at x = c_χ−b (band edge meeting the dilatation ramp), its resolvent/heat
structure hands the Airy density and hence the full class — the SAME criterion as (d)-dressed, so
(b) folds into (d). Named calculation: derive the fluctuation operator's edge normal form on the
family (is it canonical Airy?). Grade: folded-into-(d); not independent.

## 8. CANDIDATE (c) — cigar / Euclidean conical heat kernel [scoping grade]

Cigar (Euclidean horizon) heat traces are governed by closed/winding geodesics: singularities
e^(−L²/4t) ⇒ k=1 ⇒ index 1/2 in the conjugate variable — NOT the fingerprint (killed for the
generic tip). The only cubic route: the winding-geodesic family near the smoothed tip develops a
FOCAL CAUSTIC; if the length function degenerates as a FOLD (L″=0, L‴≠0) at a critical winding,
the heat-trace singularity is Airy-class and the conjugate transform lands at index 1/3. Named
calculation: compute the geodesic length function L(winding; tip smoothing) on the capped cigar
and test the fold conditions at the critical winding angle. Grade: plausible-secondary.

## 9. The constant check — does any surviving candidate FIX c̃ = (3/4)2^(2/3) ζ̃^(2/3)?

**No candidate fixes c̃ yet.** Exact dictionaries banked (all raw, QUARANTINED, no Z claims):

- LL-2d (sympy exact): the fingerprint's c̃ ⟺ density essential-singularity strength **β = ζ̃/2**
  in c_χ units (solve of 3·2^(−2/3)β^(2/3) = (3/4)2^(2/3)ζ̃^(2/3)).
- S4i (sympy exact, under the §5.2 reconstruction): dressed-family rate
  c̃_d = 3·2^(5/6)π^(1/3)√c_χ·γ^(2/3)/(2H^(1/3)); matching c̃(c_χ)^(1/3) requires
  **γ_req = 2^(1/4)√H·ζ̃/(4√π·c_χ^(1/4))** — γ is NOT derived; fixing it (hence ζ̃) requires the
  family-measure derivation. QUARANTINE ABSOLUTE.

## 10. Verdict + the defined confirming calculation

**DIRECTION-NARROWED.** Survivors and their named calculations:

1. **(d)-dressed [PRIMARY]:** derive ρ(b) near b = c_χ from the pump construction on EE's banked
   forms. PASS ⟺ oscillatory fourth-root essential edge singularity, cos(γ(c_χ−b)^(−1/4)+φ₀) ×
   (power weights), with γ = γ_req of §9. FAIL ⟹ (d) dies entirely (bare form already killed) and
   the §5.8 σ-hook with it. Also verify EE's actual κ(b) against the §5.2 reconstruction.
2. **(b)-as-Airy-edge [folds into 1]:** edge normal form of the family fluctuation operator —
   canonical −d² + x ⇒ Airy density ⇒ fingerprint automatic.
3. **(a) [secondary]:** classify the nearest complex-proper-time singularity of the dS worldline
   kernel on horizon-grazing geodesics (cubic vs quadratic branch).
4. **(c) [secondary]:** fold test (L″=0, L‴≠0) of the winding-geodesic caustic on the capped cigar.

KILLED at this gate: the bare b-family caustic (Watson/power-law normal form — the prompt's
coalescence question answered: NOT cubic, and not pole–saddle exponential either); quadratic/index-1/2
classes (ratio 1 ≠ √3); pure power-law densities; KMS-thermal-only structures; two-sided spectral
support; bare QNM-ladder resurgence (thermal class). No computation here exceeded minutes —
**no agentLL_overnight.py is needed or issued.**

## 11. Files / repro / pins

- `agentLL_generator_scoping.py` → `agentLL_generator_scoping.out` (the machine record; rerun:
  `python3 agentLL_generator_scoping.py`; sympy + mpmath, dps 30–50, runtime ~1 min).
- Sources (per relaunch protocol, summarized in the original skeleton — not re-read):
  `agentHH_pump_profile.md` (fingerprint + Theorem HH-1), `agentEE_sigma_khronon.md` (b-family
  pullback, STEPs 2–4), `agentV_kernel_inversion.md` (input-side ω^(1/4) class, firewalled).
- Literature pins (2 fetches of the allotted 4; remaining pins not load-bearing, skipped):
  - Deser & Levin, *Accelerated detectors and temperature in (anti-) de Sitter spaces*,
    [CQG 14, L163 (1997)](https://ui.adsabs.harvard.edu/abs/1997CQGra..14L.163D/abstract) — GEMS
    temperature 2πT = √(a²+R⁻²); supports §5.2's diverging-κ edge (see also
    [Jacobson's comment, gr-qc/9709048](https://arxiv.org/abs/gr-qc/9709048)).
  - dS static-patch QNMs purely imaginary, equally spaced:
    [Quasinormal modes and dual resonant states on de Sitter space](https://www.researchgate.net/publication/354591364_Quasinormal_modes_and_dual_resonant_states_on_de_Sitter_space);
    [On the quasinormal modes of the de Sitter spacetime](https://www.researchgate.net/publication/230569775_On_the_quasinormal_modes_of_the_de_Sitter_spacetime);
    spacing derivation [PRD 69, 064033](https://dx.doi.org/10.1103/PhysRevD.69.064033) — feeds §7's bare-(b) kill.
