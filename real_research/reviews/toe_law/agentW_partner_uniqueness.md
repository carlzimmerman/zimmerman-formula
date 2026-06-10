# agentW — the partner pincer made rigorous: the DOUBLE-COUNTING THEOREM (real-mass partner + MI dynamics dead at 8.7–21σ, every convention) and the unique survivor, LENS-ONLY METRIC SLIP, scoped with its four named gates

*agentW, 2026-06-10. Files: `agentW_partner_uniqueness.py` → `.out` (every number below is machine-printed there;
gates against the banked pipelines pass in-run before anything else executes). Inputs: the SPARC pipeline at the
locked conventions of `mi_f4_sparc_shape_test.py` (175 galaxies, unweighted-dex primary, Υ_bul = 1.4Υ_d, best-Υ on
[0.3,1.2]×46), the Brouwer+2021 released isolated lensing RAR + full covariance (the `f4_lensing_wall.out` data,
re-derived exactly: 1658.9/15 → 40.5σ, 206.8/15 → 12.5σ, deep-5 ratio 229.7×, conversion G = 4.301×10⁻³ pc M☉⁻¹(km/s)²
identified and gated). Both a₀ footings, both weightings, all four banked ν shapes, per-galaxy (conservative) and
per-point (charitable) statistics throughout, per the working rule. No git. Both ways at full weight.*

**Context (the pincer as banked):** agentI item 3a named the fork for Link 7's partner: (i) a partner with real
stress-energy arranged MOND-like "pulls stars too — double-counts" (asserted, never computed); (ii) a lens-only slip
sector "has no published field-level realization". agentM fixed the matter sector (Milgrom-22 MI + exponential tail:
dynamics with NO real phantom mass); `f4_lensing_wall.out` proved the partner necessary at 40.5σ; agentH3 proved the
real-mass *phenomenology* can carry the lensing exposures (B-K existence proof). This memo computes jaw (i) and
scopes jaw (ii).

---

## PART 1 — THE DOUBLE-COUNTING THEOREM

### 1.0 Pre-registration (locked in the .py header before the runs; adjudicated in §1.5)
Class: (a) dynamics = MI (circular orbits: μ(a/a₀)a = g_N exactly, monotone xμ(x)); (b) lensing = real partner mass
with the phantom-equivalent profile g_p = [ν(y)−1]g_bar (what the Brouwer amplitude demands of a metric-passive
matter sector). Expectation: ordering B (force-side: g_dyn = ν(y)g_bar + g_p) overshoots deep by → exactly 2×
(0.301 dex); ordering A (self-consistent MI on the total field — the "partial cancellation" escape) by ν(ν(y)y) →
y^(−1/4), i.e. MORE, unbounded. Thresholds: theorem HOLDS if both orderings show deep (g_bar < 10⁻¹¹) excess
≥ 0.2 dex at ≥ 5σ in every shape/footing cell with best-Υ granted; ESCAPE-SURVIVES if either ordering sits within 2σ.

### 1.1 The exact lemma (the theorem's spine — not statistics)
For monotone xμ(x) (the same condition Milgrom-22 imposes for uniqueness), the MI response to a total real Newtonian
field g_N is the **unique** a = ν(g_N/a₀)g_N. If rotation curves satisfy the observed RAR a = ν(g_bar/a₀)g_bar, then
**g_N = g_bar exactly — the real partner density is forced to ZERO everywhere kinematics probes.** The lensing data
demand g_p = [ν−1]g_bar ≠ 0 (its absence is the 40.5σ wall, re-derived in-run). The class cannot satisfy both: one
horn or the other fails, and the only question is by how much. (WEP premise stated: real stress-energy sources the
metric for stars and photons alike; exempting matter from the partner's pull is by definition jaw (ii), Part 2.)

### 1.2 The overshoot, computed on SPARC (λ = 1, the lensing-demanded partner; best-Υ granted per model)
Deep-regime factors first (exact, McGaugh ν, framework a₀): A overshoots ×6.0/×3.6/×2.2 at g_bar = 10⁻¹³/10⁻¹²/10⁻¹¹
(0.78/0.55/0.34 dex); B ×1.97/×1.90/×1.72 (0.29/0.28/0.24 dex). **The pre-registered expectation was right in sign
and size for B and right that A inverts the escape: keying the inertia to the TOTAL field (partial cancellation of
the boost) overshoots MORE, not less, everywhere below y = 1/16 — the escape reading is anti-helpful.**

SPARC (146 galaxies with deep points, 1549 deep points; kill statistic = deep-bin excess offset over the SAME-shape
λ=0 baseline, per-galaxy SEM — galaxy-level independence, data noise in the denominator; charitable per-point
√Δχ² with σ_int calibrated so the baseline gives χ²/N = 1):

| a₀ | shape | ordering A: deep offset, excess t, √Δχ² | ordering B: deep offset, excess t, √Δχ² |
|---|---|---|---|
| framework | McGaugh RAR | −0.350 dex, **17.8σ**, 84.6 | −0.200 dex, **9.9σ**, 48.9 |
| framework | fw √(1+1/y) | −0.278, 14.5σ, 65.9 | −0.165, **8.7σ** (weakest cell), 41.0 |
| framework | simple | −0.354, 18.4σ, 84.5 | −0.201, 10.4σ, 47.2 |
| framework | F4 standard | −0.283, 14.2σ, 62.2 | −0.185, 9.4σ, 41.5 |
| canonical | McGaugh RAR | −0.421, 20.5σ, 101.2 | −0.253, 11.8σ, 59.6 |
| canonical | (other three) | −0.338…−0.425, 15.4–21.1σ | −0.215…−0.254, 9.5–12.2σ |
| canonical, **Υ fixed 0.5** (MOND-default row) | McGaugh | −0.486, **21.6σ** | −0.327, **13.8σ** |

- **Convention-robustness, both directions (the working rule, applied):** the kill survives both a₀ footings, all
  four ν shapes, both weightings, and the MOND-default fixed-Υ row. The *most charitable* convention is the best-Υ
  grant: the fit slams the **Υ_d = 0.30 grid floor in every λ=1 cell** (vs 0.44–0.64 at baseline), soaking ~0.1 dex
  of overshoot at a disk M/L far below SPS priors (~0.5 at 3.6 μm) — and the weakest cell is still 8.7σ. Deep-cut
  robustness (g_bar < 3×10⁻¹²; 69 galaxies): excess grows to −0.16/−0.28 dex (B) and −0.38/−0.41 (A) with t = 4.7σ
  (B, framework — the single sub-5σ entry anywhere, a statistics-starved subset, not a vanishing effect: the offset
  *grows*) to 11.6σ. Scatter: every λ=1 model degrades the locked unweighted scatter from 0.195 to 0.236–0.372 dex.
- **Adjudication against the pre-registered bars, honestly:** the ≥5σ bar clears in **all 16 primary cells**
  (weakest 8.7σ). The ≥0.2 dex magnitude bar clears in all A cells; in B cells the *excess* lands 0.15–0.21 dex
  under the Υ-floor charity (raw deep offsets 0.165–0.254 dex; at fixed Υ=0.5 the excess is 0.256 dex — above the
  bar). Reported as measured: the magnitude bar is met everywhere except where the Υ-floor grant buys ~0.05 dex,
  and the significance bar is met everywhere regardless.

### 1.3 The ordering escape, CLOSED (not merely characterized)
Free the MI scale a₀_MI (the partner stays lensing-fixed at a₀); where does the dynamics fit want it?
**a₀_MI → 0 in both orderings** (scatter minimum 0.1950 at exactly 0 — because λ=1, a₀_MI=0 is g_dyn = ν(y)g_bar:
Newtonian inertia + a real phantom-profile halo = the observed RAR by construction = **particle dark matter with
extra steps**). The scatter rises monotonically to the MI-class point (0.247 B / 0.326 A at a₀_MI = a₀). The
"operator ordering" ambiguity therefore contains no refuge: ordering A makes the deep overshoot *worse*; freeing
the MI scale only re-derives dark matter by deleting premise (a). **The only consistent member of the class is the
one with no MI in it.**

### 1.4 The pincer dial (partner fraction λ, jointly against both datasets)
σ_lens(λ) (Brouwer bins, full covariance) vs t_dyn(λ) (per-galaxy deep excess, McGaugh ν, framework a₀, best-Υ per λ):
λ=0 → (40.5σ lens, 0σ dyn); λ=1 → (12.0σ lens, 17.8σ A / 9.9σ B dyn). **min over λ of max(σ_lens, t_dyn) = 16.6σ
(A, λ=0.9) / 12.0σ (B, λ=1)** — and the 12.0σ floor at λ=1 is the *published absolute lensing-RAR shape tension*
(§2c) that even parameter-free MOND lensing carries on these bins; the dynamics horn alone is still 9.9σ there.
No partner fraction opens a live window.

### 1.5 PART 1 VERDICT
**THE THEOREM HOLDS.** A pure-mass partner reproducing the lensing-demanded phantom profile + MI dynamics is
internally inconsistent: the rotation curves overshoot the observed RAR by 0.165–0.49 dex in the deep regime,
**8.7–21.6σ** on the conservative per-galaxy statistic (41–102 on the charitable per-point √Δχ²), under every
convention combination tried, with the exact lemma (§1.1) underneath: dynamics forces g_p ≡ 0, lensing forces
g_p ≠ 0 at 40.5σ. The partial-cancellation ordering makes it worse (deep overshoot unbounded, y^(−1/4)); the
a₀_MI freedom only re-derives dark matter. **Scope note (both ways):** this kills the *MI-dynamics + real-partner*
assembly — i.e., exactly the Link 6 (Milgrom-22) + Link 7 (real mass) combination. It does NOT touch the B-K-class
hybrids, whose dynamics is force-side with the condensate mass shared between both channels (they die in the solar
system instead, agentH3); and it would be voided only if the SPARC deep amplitudes were coherently biased high by
~0.2 dex across 146 galaxies or the Brouwer amplitude were wrong by ~200× — neither is on any table.

---

## PART 2 — LENS-ONLY SLIP, SCOPED (the unique surviving partner structure)

### 2.1 What field structure gives slip with NO fifth force on matter
Non-relativistic matter responds to the time-time potential Φ only; lensing to (Φ+Ψ)/2. A sector sourcing **only the
spatial-curvature potential Ψ** is therefore lens-only *automatically* — no force on stars, no Cassini Q₂ quadrupole,
no solar reflex, no vertical-Jeans load: **the entire solar-system battery that killed AeST, DEW and face-value B-K
evaporates by construction.** Required amplitude (gated against agentI item 3a): Ψ′/Φ′ = 2ν−1 = **61.2 / 19.4 / 6.2**
at g_bar = 10⁻¹³/10⁻¹²/10⁻¹¹. In the standard (μ,Σ) parametrization this is (μ,Σ) = (1, ν): photons see the MOND
amplitude, matter sees Newton.

**GW170817, verified precisely — the bound is two bounds, and they cut differently:**
- *The speed bound* (1710.05834: |Δc|/c ≲ 10⁻¹⁵) constrains the photon and graviton **propagation cones**, not static
  potentials. A static Ψ ≠ Φ sourced through the field equations leaves both species on the same null cones:
  **evaded, verified.**
- *The differential-Shapiro test from the same event* (Boran–Desai–Kahya–**Woodard** 1710.06168, PRD 97, 041501 —
  author corrected from the tasking's "Sarkar"): if photons and GWs propagate on **different metrics** — photons
  seeing the dark/phantom potential, GWs not — the accumulated Shapiro delay differs by **~1000 days vs the observed
  1.7 s**: kills that whole class by ~7 orders. This executes the **photon-sector realizations**: nonminimal photon
  couplings, photon-disformal couplings, kinetic-mixing/refractive-index dark sectors (1706.04455-class — which also
  fail achromaticity: gravitational deflection is dispersionless, a medium's generally is not). **Surviving
  realization, uniquely: the slip must live in the metric itself** — a real Ψ-channel source — shared by photons
  and gravitons.
- *What can source metric Ψ−Φ:* anisotropic stress — and the Saltas–Sawicki–Amendola–Kunz theorem (1406.7139,
  PRL 113, 191101; extended in 1612.02002 "non-standard GWs imply gravitational slip") makes the converse sharp:
  across Horndeski, Einstein-aether and bimetric classes, **slip ⇔ modified tensor-sector propagation.** Two branches:
  - **(i) Real stress-energy with large anisotropic stress: CLOSED by causality + Part 1.** For any medium with
    stable subluminal transverse modes, c_s² = μ_shear/(ρ+p) ≤ 1 and elastic strain ≲ 1 force |π| ≲ ρ+p
    (elastic-dark-energy relations, Battye–Moss class). Sourcing Ψ at 6–61× the baryonic gradient then demands
    ρ_s of at least that order — which gravitates on stars and re-imports Part 1's overshoot **amplified ×~2**
    (the required source scales as 2ν−2, twice the phantom profile's ν−1). An energy-condition-violating
    "pure-π, ρ≈0" source is the only loophole, and nothing stable/causal in print supplies it.
  - **(ii) Modified-gravity slip (no local stress-energy): the OPEN branch.** Post-GW170817 c_T = 1 classes with
    beyond-Horndeski/DHOST α_H-type operators (or nonlocal terms) generate Φ ≠ Ψ without α_T; the Saltas theorem
    then prices it in tensor-sector modification (damping/friction-type at minimum — bounded at O(0.1–1)
    cosmologically, unprobed at halo scales). **No published member produces an a₀-keyed, MOND-phantom-amplitude
    static slip at galactic scales** (§2.4). This is the unique surviving partner structure.

### 2.2 The B-K Φ=Ψ template (1602.05961 §6) and the minimal decoupling
Khoury's construction uses the medium 4-velocity u^μ to make the scalar source Φ and Ψ **equally** — *enforced
equality WITH a matter force*: it presupposes a metric MOND force, re-importing the AQUAL static limit and the
Cassini-Q₂ kill (banked, agentI/agentH1). The minimal modification that decouples the two: keep the u^μ-projected
structure but move the scalar's metric source entirely into the **traceless/anisotropic channel** (δρ → 0, π ≠ 0),
so it feeds Ψ−Φ and nothing else. That lands exactly on branch (i)'s causality wall if the source is honest
stress-energy, or on branch (ii) if the projection is done in the gravitational operator (the u^μ machinery is then
building an effective α_H-type term). Either way the matter force is gone and the solar system goes quiet by
construction — the template's *architecture* survives the port; its *budget* must come from branch (ii).

### 2.3 The kill-gates a slip sector faces immediately (computed)
1. **Solar light bending / Shapiro (Cassini γ): PASS, automatic.** γ_eff − 1 = 2[ν(y)−1] at the Cassini conjunction
   (b = 1.6 R☉, y = 1.1×10¹²): **1.8×10⁻¹² for the power-law (simple-ν) tail — ×1.3×10⁷ inside the 2.3×10⁻⁵ bound;
   e^(−1,069,734) for the exponential tail** (the tasking's e^(−√2000) ≈ 4×10⁻²⁰ is reached out at ~178 AU; at
   Saturn the exponential slip is ~e^(−831)). An a₀-keyed slip profile clears the solar system without a screening
   mechanism — for BOTH μ-tail families. (Computed at framework a₀; canonical moves nothing.)
2. **Clusters: RE-FAILS, by construction, at the MOND factor.** A slip keyed to ν(g_bar/a₀) predicts the MOND
   lensing amplitude — short of observed cluster lensing by **×1.97** at the canonical M_bar(<1 Mpc) = 7×10¹³,
   M_lens = 5×10¹⁴ benchmark (the known ~2× residual, re-derived). The partner spec must either carry the same
   second variable the type split demands (below) with cluster-scale amplitude, or concede clusters to a separate
   component — it does not get them for free.
3. **The type split: the slip CANNOT be a function of g_bar alone.** A universal slip(g_bar) predicts exactly zero
   early−late offset at fixed g_bar — facing the measured **+0.261 dex (8.6–9.2σ hardened, own catalog)** with no
   real-mass/SHMR escape (that escape belongs to the real-mass class, H3-T4; a lens-only hybrid has no extra real
   mass). **Spec item, sharpened by agentJ:** the slip amplitude must carry a second variable, smooth in halo mass
   (sharp condensation staircase refuted at 7.3σ; the surviving signal is the smooth 1-halo-safe mass trend
   +0.122 ± 0.062 dex/dex with the contamination control inverted — the trend lives in the *clean* bins). The
   constructive reading, both ways: one smooth mass/depth-keyed modulation could in principle carry the type split
   AND the cluster amplitude — that is a falsifiable structural prediction (slip grows with halo mass at fixed
   g_bar), already consistent in sign with agentJ's 2.0σ trend.
4. **The absolute lensing-RAR shape rides along:** any exactly-ν-keyed slip inherits the published tension on the
   Brouwer bins — **12.0–12.5σ (framework a₀) / 8.6–8.9σ (canonical)** across all four shapes (computed, full
   covariance). The partner spec should target the measured profile, not assume ν; this is a *shape* requirement,
   not an amplitude wall (the amplitude is the 230× the partner exists to supply).

### 2.4 Literature (searched 2026-06-10; queries in the run log)
**No published model realizes lens-only slip at galactic scales.** The near misses, each disqualified for a named
reason: dark-matter emulators / TeVeS-class (photons on the DM-mimicking metric, GWs not — killed by 1710.06168);
1602.05961 §6 (slip-free by design, WITH a matter force — Cassini-class kill re-imported); elastic/solid dark energy
(Battye–Moss/Battye–Pearson: real anisotropic stress, built for cosmological perturbations, never a₀-keyed or
galactic, and capped by |π| ≲ ρ+p); refractive/kinetic-mixing dark sectors (1706.04455-class: photon-metric class →
Shapiro-killed, plus chromaticity); Mistele 2408.02725 (QUMOND phantom-halo lensing — the force acts on matter too,
checked directly). The (μ,Σ) parametrization literature measures Σ ≠ μ as a *cosmological* possibility; no
field-level galactic construction with (μ,Σ) = (1,ν) exists in print.

---

## VERDICT (both ways, full weight): **UNIQUE-AND-SCOPED**

- **Part 1 (the first jaw): THEOREM.** MI dynamics + a real-mass partner carrying the lensing-demanded phantom
  profile is internally inconsistent at **8.7–21.6σ** (conservative statistic, weakest cell, maximal charity:
  best-Υ slammed to the 0.30 floor) — the pre-registered ~2× (0.3 dex) deep overshoot confirmed for ordering B
  (2 − 1/ν → 2 exactly) and *exceeded* by the "escape" ordering A (ν(ν(y)y) → y^(−1/4), unbounded). The ordering
  ambiguity is closed: A is worse, and the only continuous escape (a₀_MI → 0) is particle dark matter with the MI
  deleted. The joint compromise over partner fractions never gets below **12σ**.
- **Part 2 (the second jaw): the survivor is scoped, not dead.** The unique structure left for Link 7 is a
  **metric-level, Ψ-channel (lens-only) slip sector**: static (GW-speed-bound-evading, verified), shared by photons
  and gravitons (differential-Shapiro-evading — the gate that executes every photon-sector realization), sourced in
  the modified-gravity branch (the real-stress branch is closed by the causal-medium bound |π| ≲ ρ+p, which
  re-imports Part 1 amplified ×~2), solar-system-silent automatically (×10⁷ inside Cassini γ even for power-law
  tails), and obligated to four named gates: the cluster ×2, the type-split second variable (smooth in mass, agentJ),
  the absolute Brouwer shape (8.6–12.5σ if naively ν-keyed), and the Saltas-theorem price (tensor-sector modification
  — the falsifiable handle: GW damping/propagation through halos). **No published realization exists** — the partner
  slot is now as sharply specified as the matter sector was after agentM, and as empty.
- **For Link 7 / DERIVATION_CHAIN.md:** the wording "every published covariant carrier fails a gate" stands and
  sharpens: *real-mass carriers are now excluded as a CLASS for the MI matter sector (this memo's theorem), not
  instance-by-instance; the lens-only slip carrier is the unique remaining class, with its gates named and its
  literature empty.* The B-K existence proof (H3) remains exactly what it was — proof that real-mass phenomenology
  can carry the lensing exposures — but Part 1 proves that phenomenology cannot be *attached to the MI matter sector
  the program has selected*: the hybrid's two halves are now known to require different physics than any published
  pairing supplies.

## Pin table

| id | role |
|---|---|
| 2106.11677 | Brouwer+2021 lensing RAR (released profiles + covariance used directly; SIS C=4 eq. 7) |
| 2406.09685 | flat lensing V_c to ~1 Mpc (the amplitude's reach) |
| 1710.05834 | GW170817/GRB speed bound (cones, not statics — evaded by metric slip) |
| 1710.06168 | Boran–Desai–Kahya–Woodard PRD 97, 041501: ~1000-day differential Shapiro kills photon-sector slip |
| 1406.7139 / 1612.02002 | Saltas+ slip ⇔ modified GW propagation (the branch-(ii) price) |
| 1602.05961 | Khoury §6: u^μ-enforced Φ=Ψ WITH force (the template ported in §2.2) |
| 1706.04455 | refractive dark sector (photon-metric class, named near-miss) |
| 2408.02725 | Mistele QUMOND lensing halos (checked: force on matter too) |
| Battye–Moss / Battye–Pearson (e.g. astro-ph/0703744, 1301.5042) | elastic DE anisotropic stress; c_s² = μ/(ρ+p) ≤ 1 bound |
| 2208.07073 | Milgrom-22 MI (the matter sector whose monotonicity condition powers the §1.1 lemma) |
| repo | `mi_f4_sparc_shape_test.py/.out` (conventions + G1 gate), `f4_lensing_wall.out` (G2 gate, reproduced exactly), `agentI_fraction_amplitude.md` (item 3a, slip 61/19/6 gate), `agentH3_gauntlet.md` (real-mass existence proof, scope note), `agentJ_massbin_phase.md` (7.3σ staircase kill; +0.122±0.062 smooth trend), `agentM_milgrom2022_gauntlet.md` (Link 6), `DERIVATION_CHAIN.md` Link 7 |

*Machine state: G1 reproduced all eight banked SPARC cells to ±0.0002 dex; G2 reproduced χ² to 0.1 and the 229.7×
ratio exactly. Bug log: (i) first-pass "excess t" used a paired model-vs-model difference whose variance collapses at
fixed Υ (printed a meaningless 392σ) — replaced with the data-noise per-galaxy SEM statistic before any number was
banked; (ii) a garbled f-string in the 2b footer fixed. The single sub-5σ entry anywhere (4.7σ, ordering B, deeper
3×10⁻¹² cut, 69 galaxies) is reported in §1.2 rather than hidden. No git operations performed.*
