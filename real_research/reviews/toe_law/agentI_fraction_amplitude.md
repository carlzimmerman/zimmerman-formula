# Agent I — the fraction–amplitude GO/NO-GO: an f ≲ 1–3% ultralight carrier CANNOT carry the MOND amplitude. NO-GO, every decade, every route, convention-immune (gaps 4.2–38 dex)

*agentI, 2026-06-10. Task: the go/no-go question agentH4 §7 named decisive for the entire hybrid build —
can an ultralight field limited to the H4 fraction ledger (f ≲ 1–3% across the knee band
[1.3×10⁻²⁹, 1.6×10⁻²⁴] eV, f ≲ 0.2–0.3 in the top two decades) produce the FULL MOND-amplitude effect,
g_obs = √(g_bar·a₀) at a₀ = 9.36×10⁻¹¹ — an order-unity modification of baryon dynamics at the RAR knee?
Artifacts: `agentI_fraction_amplitude.py` + `.out` (all numbers quoted below are machine-printed there;
raw numbers before comparisons; both a₀ conventions; charity dials resolved toward the framework and
labelled). Every external number arXiv-pinned. No coefficient claims. No git.*

---

## 0. Setup (pinned)

MW halo per tasking: **M200 = 10¹² M☉, NFW, c200 = 10** (1402.7073; MW-mass cross-pin 1912.02599) →
R200 = 211.7 kpc, Rs = 21.2 kpc. Baryons M_bar = 6.1×10¹⁰ M☉, Rd = 2.6 kpc (1602.07702). Cosmology
Planck-2018 (1807.06209): ρ_DM,cosmic = 1.26×10⁻⁶ GeV/cm³ = 9.72×10⁻¹² eV⁴; ρ_DM,local = 0.3 GeV/cm³
(2306.16228; charity edge 0.4, 1404.1938/2012.11477). RAR ν-function (1609.05917) at a₀ = 9.36×10⁻¹¹;
baseline a₀ = 1.2×10⁻¹⁰ also run (changes M_phantom by 13% — nothing turns on it). Universal-coupling
ceiling β ≤ 3.39×10⁻³ (Cassini |γ−1| ≤ 2.3×10⁻⁵ via 1403.7377 — agentN3's convention, kept).
λ_dB = ħ/(mv), v = 200 km/s (H4's convention; reproduces its 19 Mpc at 5×10⁻²⁸ eV). Regime split:
halo-bound iff λ_dB ≤ R200 → **bound decades m ≳ 5×10⁻²⁶ eV (top ~1.5 decades only); everything at and
below 10⁻²⁶ eV is a quasi-homogeneous cosmic background at the f-bounded cosmic mean** — including the
DR4 discriminator mass 5×10⁻²⁸ eV. Knee-band sanity: m/H_Λ ∈ [1.1×10⁴, 1.3×10⁹] — **m ≫ H everywhere**
(N2 §4, principal series); this fact does double duty below (§2c).

---

## 1. Item 1 — the sourcing route (superfluid template: carrier gravitationally supplies the phantom)

M_phantom(R) = g_obs R²/G − M_bar(R). Raw values (a₀ = 9.36×10⁻¹¹): 2.9×10¹¹ M☉ at 50 kpc,
6.1×10¹¹ at 100 kpc, 1.25×10¹² at 200 kpc, **6.37×10¹² at 1 Mpc** (deep-MOND M_eff grows ∝ R; the
lensing RAR is measured MOND-amplitude to ~Mpc — 2106.11677, 2406.09685, banked 40.5σ wall).

| supply mode | f_req (50 kpc) | f_req (300 kpc) | f_req (1 Mpc) | ledger f | gap |
|---|---|---|---|---|---|
| clustered f·M_NFW (bound decades, m ≳ 5×10⁻²⁶) | **0.85** | **1.58** | **3.27** | 0.1–0.3 | ×2.8–8.5 (best radius) |
| homogeneous f·(4π/3)R³ρ_cosmic (m ≲ 10⁻²⁶) | **1.7×10⁴** | 5.0×10² | 45.7 | 0.01–0.05 | ≥9×10² (best radius); **3×10⁵–3×10⁷ at the kinematic radii** |

- **At f = 0.01/0.03 the clustered carrier is ×84–99 / ×28–33 short inside R200 and ×327/×109 short at
  1 Mpc.** The homogeneous decades are short by 10⁵–10⁷ where rotation curves live — and that is the
  "even if it could all be piled up inside R" reading: a quasi-homogeneous field's true differential
  pull is (4π/3)Gρ_f r, i.e. effectively zero.
- **Structural kill independent of the ledger:** even at f = 1, M_phantom(1 Mpc)/M_NFW(1 Mpc) = 3.27 —
  sourcing the measured Mpc-scale lensing amplitude needs ~3.3× more mass than the entire pinned halo
  carries there. (Both ways: a ~3× heavier outer halo is the ΛCDM-accommodation question, outside
  scope; at f ≤ 0.03 the gap is ×109 regardless.) This is the 2303.08560 SFDM lensing kill re-derived
  as a mass budget. And at f < 1 the remaining (1−f) of the dark sector gravitates too — crediting the
  carrier with the whole phantom while a CDM-like partner sits in the same potential double-counts;
  the table is generous to the route.

**Item-1 answer: sourcing requires f ≈ 0.85–1.3 (bound decades, sub-Mpc), f > 1 at Mpc, f ~ 10⁴–10⁵
(homogeneous decades). No decade of the band comes within ×2.8 of its ledger ceiling; most are 10²–10⁷
away. The superfluid-template route is dead pre-assembly.**

## 2. Item 2 — the mediator route (the spec's actual structure): amplitude per energy density

The carrier mediates the N2/N3 inertia channel; its energy budget caps only the coherent amplitude:
ρ_f = ½m²φ² ⇒ **φ_max = √(2ρ_f)/m**, and a linear coupling m_p(φ) = m_p(1 + βφ/M_Pl,red) gives

> **ε = β φ_max/M_Pl = β √(2 f ρ_DM) / (m M_Pl,red) ∝ β √f / m** — the amplitude-per-energy-density
> DOES improve as 1/m at fixed ρ, exactly as the route was built to exploit. Derived, verified, and
> exploited to its limit below — it is still not enough.

ε ≥ O(1) is a *necessary* condition (generous: the DC inertia shift from an oscillating linear term is
second order in ε_lin, so ε_lin ~ 1 is the charitable floor). Raw table in `.out`; the spine:

| m (eV) | regime | ε(β_Cassini, ledger f) | ε(β=1, ledger f) | β_req for ε=1 | f_req at β=1 |
|---|---|---|---|---|---|
| 1.3×10⁻²⁹ (floor) | homogeneous | **1.1×10⁻⁷** | 3.1×10⁻⁵ | 3.2×10⁴ | 5.2×10⁷ |
| 5×10⁻²⁸ (DR4) | homogeneous | 2.7×10⁻⁹ | 8.1×10⁻⁷ | 1.2×10⁶ | 7.6×10¹⁰ |
| 5×10⁻²⁶ (lowest bound) | marginal/local | 1.9×10⁻⁸ | 5.6×10⁻⁶ | 1.8×10⁵ | 3.2×10⁹ |
| 1.6×10⁻²⁴ (top) | bound | 1.0×10⁻⁹ | 3.0×10⁻⁷ | 3.3×10⁶ | 3.3×10¹² |

- **Best decade in the whole band is the floor** (1/m wins faster than √ρ loses): ε = 1.1×10⁻⁷ at the
  Cassini coupling — **7.0 dex short**. At β = 1 (gravitational strength, ALL fifth-force bounds
  ignored): 4.5 dex short.
- **Maximum-charity stack** (f = 0.1 contested S8 window 2301.08361, ρ_local = 0.4 GeV/cm³, ×100
  soliton overdensity extrapolated far beyond its f=1 validity 1407.7762, β = 1): **ε = 6.4×10⁻⁵ —
  still 4.2 dex short of order-unity. NO DECADE PASSES.** β_req ≥ 1.6×10⁴ everywhere = a fifth force
  ≥ 2.6×10⁸ × gravity on an unscreened pc–Mpc-wavelength carrier — excluded by Cassini by ~4×10¹³ in
  force; chameleon screening self-defeats in-band (N3 Wall 1, unchanged).
- **(2c) The two sub-routes, also closed:** (i) *vacuum-correlator amplitude* (the field's
  state-independent retarded tail instead of the condensate): the dressing improves on N3's dS-bath
  wall only by √(1.85·m/H) ≤ 5×10⁴ → β_req ≥ 4.4×10³⁵, **≥38 orders above Cassini** — and the SIGN is
  wrong: N3's machine-verified dressing is MOND-signed only for m² < 2H², while the knee window forces
  m ≫ H (N2 §4) — **the sign and the knee cannot come from the same field's vacuum tail**; structural
  kill independent of amplitude. (ii) *Quadratic coupling* φ²/M²: ε = 1 forces M = φ_max, at which the
  matter-induced mass √(2ρ_b)/M exceeds the bare mass in every decade (×6 at the top to ×7100 at the
  floor; midplane ρ_b from 1509.05334) — the knee becomes a local-baryon-density dial, destroying the
  universal acceleration-keyed knee (spec items 2+3) and re-creating exactly the environment-keyed
  RAR-scatter structure N5 killed at 5.2σ. (iii) *Derivative/P(X) couplings*: ε = 1 needs a universal
  matter coupling at M ~ 0.015 eV — the meV scale is the BK superfluid structure (Λ ~ 0.2 meV,
  1507.01019): that exit leads INTO agentH4's fully mapped Wall-A, not out.

**Item-2 answer: the 1/m scaling is real and large — the condensate brings N3's β_req = 2.2×10⁴⁰ down
to 1.6×10⁴, a ~36-order improvement — and the route still misses order-unity by ≥4.2 dex with
fifth-force bounds ignored and ≥6.7 dex with Cassini enforced, in every decade. The make-or-break
breaks.**

## 3. Item 3 — the crossfire (run on the empty passing set: the hypothetical best decade + DR4 mass)

- **(a) Lensing wall (the partner, named explicitly).** A mediator does not lens; with dynamics on the
  inertia channel the metric stays baryonic, so the partner must source the lensing potential ALONE:
  ∇Ψ = 2g_MOND − g_bar ⇒ required gravitational slip Ψ′/Φ′ = 2ν−1 = **61 at g_bar = 10⁻¹³, 19 at
  10⁻¹², 6 at 10⁻¹¹** (the banked wall: 40.5σ, deep-bin amplitude ratio 229.7×, `f4_lensing_wall.out`).
  The carrier's own convergence covers 1.9% of the job at 300 kpc (f = 0.03) and zero in the
  homogeneous decades. The partner requirement: source Ψ at 10–60× the baryonic Φ-gradient at
  0.1–1 Mpc while staying inside Cassini Q₂ ∈ [−2.0, +5.2]×10⁻²⁷ s⁻² (2602.17884) and the MW
  vertical-Jeans budget (1812.08169/1911.12365). **The pincer:** real stress-energy arranged MOND-like
  pulls stars too (double-counts the mediator → DM with extra steps); a lens-only slip sector has no
  published field-level realization — the one Φ=Ψ template (1602.05961 §6) presupposes a metric MOND
  force and re-imports the AQUAL static limit, i.e. the Cassini-Q₂ kill that took AeST and DEW;
  photon-disformal versions are squeezed by GW170817's |Δc|/c ≲ 10⁻¹⁵ (1710.05834) through the very
  halo medium that must lens.
- **(b) Cherenkov gate (2103.16954-class).** The free massive carrier's relativistic branch has
  v_phase > c at all k — true Cherenkov kinematically forbidden. The gapless collective branch
  (ω = k²/2m) has modes slower than 220 km/s at every in-band mass (λ > π·λ_dB(v_orb): 17 kpc at the
  band top; > system size in the homogeneous decades, where the gate has no purchase even in
  principle). At β ≤ β_C, f ≤ 0.03 the exposure sits ≥3×10⁶ below the killed BK point — a trivial
  pass — but **the gate and the amplitude are one dial**: at β_req ~ 2×10⁴ the exposure rises ~10⁷
  over the killed point (its ≲10 Gyr stellar lifetimes scale toward kyr). Any coupling big enough to
  do MOND re-arms the gate in the bound decades; any coupling small enough to pass it cannot do MOND.
- **(c) DR4 knee discriminator (5×10⁻²⁸ eV, the hardest ledger pinch f ≤ 0.013, eROSITA 2502.03353;
  λ_dB = 19 Mpc → homogeneous).** ε = 1.4×10⁻⁹ (Cassini, **8.9 dex short**) / 4.1×10⁻⁷ (β = 1,
  6.4 dex). H4 §7's fork — (i) works at f ≤ 3% → band open, DR4 discriminates; (ii) needs f > 3% →
  knee forced to the top decades — **has no live branch**: the top decades are the WORST in the band
  (ε ~ 10⁻⁹ at Cassini), the floor is best and still 7.0 dex short. The band does not narrow. It
  closes.

---

## 4. VERDICT (both ways, full weight)

**NO-GO.** The f-limited ultralight carrier cannot produce the full MOND-amplitude effect by any of its
three channels, in any decade of [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV, under every convention checked:

| route | best-case gap | binding wall |
|---|---|---|
| A — sourcing (superfluid template) | ×2.8 (top decades, best radius) → ×10⁵–10⁷ (homogeneous, kinematic radii); **f > 1 needed at Mpc even before the ledger** | H4 fraction ledger + the Mpc lensing continuation (2106.11677/2406.09685) |
| B — mediator (condensate amplitude) | **4.2 dex at β = 1, maximum charity; 6.7 dex at Cassini; 8.9 dex at the DR4 mass** | ε = β√(2fρ)/(mM_Pl) vs the f-ledger and β ≤ 3.39×10⁻³ (1403.7377) |
| C — mediator (vacuum correlator) | 38 orders; **anti-MOND sign for m² > 2H² = the whole band** | N3 coupling wall (banked) + the sign–knee incompatibility (new) |

- **Convention immunity, checked not asserted:** a₀ footing (9.36×10⁻¹¹ vs 1.2×10⁻¹⁰) moves M_phantom
  13%; ρ_local 0.3→0.4, ledger hard→charitable edges, ×100 soliton charity, hostile vs framework band
  ceiling — none moves any gap by more than ~1 dex against shortfalls of 4.2–38 dex. The kill is not a
  baseline artifact in either direction; nothing here is a default-convention verdict on the equation.
- **The framework-favorable facts, at full weight:** (1) the 1/m amplitude scaling is real — this
  calculation moved the coupling wall from N3's 10⁴⁰ to 10⁴, a 36-order improvement, the single largest
  step any bath-side channel has taken; the door closed from ~85 orders of impossibility to ~4–7. It is
  still closed. (2) The sign–knee incompatibility (2c-i) is a clean structural discovery: the spec's
  item 1 (MOND sign needs m² < 2H²) and item 3 (knee needs m ≫ H) cannot both be supplied by one
  field's vacuum tail — the spec sheet itself is now known to require *two distinct functions even
  within the carrier sector*. (3) The Cherenkov gate genuinely passes at allowed couplings — recorded
  as a pass, with the honest reason (the coupling is too small to do anything).
- **What this does NOT kill (named):** the carrier as pure KNEE-SETTER with the amplitude paid
  elsewhere. But every published "elsewhere" lands on a banked kill: the dS bath (N3, 10⁸⁵), a metric
  MOND sector (AeST-class — Cassini Q₂, repo-banked; DEW — agentD 8.8–14.6σ), meV-scale derivative
  couplings (BK-class — H4 Wall-A). The crossfire adds the partner pincer: lens-only slip (no
  realization; GW170817 squeeze) vs metric-MOND (Q₂ kill). **The hybrid build as specced — a
  fraction-limited carrier supplying the MOND amplitude — dies pre-assembly.** What survives of Door II
  must find an order-unity amplitude source outside the carrier's energy budget, and as of 2026-06-10
  no published structure supplies one.
- **What would reopen it (bounded, named):** a worldline coupling with no static-limit fifth force
  whose in-band amplitude is not paid from ρ_f (none exists in print; derivative variants exit into
  Wall-A); or the fraction ledger collapsing by ≥4 orders (CMB+BOSS+eROSITA+Lyα would all have to be
  wrong together — not on the table); or abandoning order-unity amplitude (i.e. abandoning MOND as the
  target — outside the spec).

**Status line for the registry:** H4 §7's decisive calculation is done and decides NEGATIVE at full
weight. The DR4 wide-binary fork remains a real measurement, but it no longer discriminates FOR this
build — the build it was to discriminate for does not survive to assembly.

---

## Pin table (all arXiv; repo artifacts named inline)

| id | role |
|---|---|
| 1807.06209 | Planck 2018: H0, Ω_c h², Ω_Λ (footings; ρ_crit, cosmic DM density) |
| 1402.7073 | NFW c(M): c200 = 10 at 10¹² M☉ |
| 1912.02599 | MW mass review (M200 ≈ 1.2×10¹² cross-pin) |
| 1602.07702 | MW baryons: M* = 5×10¹⁰, gas 1.1×10¹⁰, Rd = 2.6 kpc |
| 1609.05917 | RAR ν-function (McGaugh interpolation) |
| 2306.16228 | EPTA: ρ_DM,local = 0.3 GeV/cm³ convention; top-sliver fraction bound |
| 1404.1938 / 2012.11477 | local DM density range (0.4 charity edge) |
| 1509.05334 | midplane baryon density 0.084 M☉/pc³ (quadratic-coupling matter mass) |
| 1403.7377 | Cassini |γ−1| ≤ 2.3×10⁻⁵ → β ≤ 3.39×10⁻³ (agentN3 convention) |
| 2209.15487 | MICROSCOPE final (binds composition-dependent variants harder) |
| 2502.03353 / 1410.2896 / 2104.07802 / 1708.00015 / 2301.08361 | the H4 §B2 fraction ledger (f ceilings per decade) |
| 1407.7762 | soliton–halo relation (×100 charity dial, flagged as beyond validity) |
| 2106.11677 / 2406.09685 | Brouwer lensing RAR to ~Mpc; flat lensing V_c (the wall's data) |
| 2303.08560 | SFDM lensing incompatibility (item-1 budget kill matches it) |
| 2103.16954 / 2208.14308 | Cherenkov gate (killed BK point; two-field evasion) |
| 1507.01019 | BK superfluid: Λ ~ 0.2 meV (where the derivative-coupling hatch exits) |
| 1602.05961 | the only Φ=Ψ partner template (presupposes metric MOND force) |
| 2602.17884 | Cassini Q₂ window [−2.0, +5.2]×10⁻²⁷ s⁻² (partner constraint) |
| 1812.08169 / 1911.12365 | MW vertical-Jeans budget (partner constraint) |
| 1710.05834 | GW170817/GRB: |Δc|/c ≲ 10⁻¹⁵ (photon-disformal squeeze) |
| repo | `agentH4_hostile_walls.md` (ledger, §7 task), `agentN2_memory_langevin.md` (knee window, m ≫ H), `agentN3_tail_scale.md` (coupling wall 2.2×10⁴⁰, sign flip at m² = 2H²), `agentN5` (5.2σ environment-keying kill), `f4_lensing_wall.out` (40.5σ, 229.7×), `agentD_dew_quadrupole.md` (DEW Q₂), `agentH1_candidate_matrix.md` (templates, imported gates) |
