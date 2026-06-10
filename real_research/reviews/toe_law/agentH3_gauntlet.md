# Agent-H3 — the banked kill-test gauntlet run on the superfluid-DM-class hybrid (Berezhiani–Khoury)

*Agent H3 for C. Zimmerman, 2026-06-10. The non-Huygens door closed with a spec sheet for the missing object
(`NONHUYGENS_DOOR_SYNTHESIS.md`): a field-level hybrid — MOND-signed matter sector + a lensing-carrying partner.
The Berezhiani–Khoury superfluid (phonon-mediated MOND force inside a condensate core, CDM-like envelope outside,
lensing from the condensate/halo mass itself) is the most-published object in that class. This file runs the repo's
banked kill-tests on it NUMERICALLY: (1) Cassini Q₂ via the verified Desmond eq (10)–(12) machinery, (2) the agentE
solar-reflex budget, (3) SPARC vs the McGaugh baseline, (4) the ~9σ lensing type split, (5) the WB/DR4 knee.
Scripts: `agentH3_gauntlet.py` (+`.out`), `agentH3_typesplit.py` (+`.out`). No git operations. Every published
number arXiv-pinned. Both ways at full weight — this is a RIVAL hybrid: no strawmanning (its own parameters, its
own most favorable reading run at full weight) and no soft-pedaling.*

## Published pins (every number used below)

| quantity | value | source |
|---|---|---|
| B-K 2015 fiducial | m = 0.6 eV, Λ = 0.2 meV; α^{3/2}Λ = √(a₀M_Pl) ≈ 0.8 meV ⇒ α ≈ 2.51 | arXiv:1507.01019 §3.2 eq (46), §4.1 eq (60) |
| BFK 2018 fiducial | m = 1 eV, Λ = 0.05 meV, α = 5.7, β = 2, σ/m = 0.01 cm²/g | arXiv:1711.05748 §V.2, eq (13), (42) |
| phonon critical acceleration | ā ≡ α³Λ²/M_Pl ≈ 0.87×10⁻¹⁰ m/s² (BFK fiducial) | arXiv:1711.05748 eq (9), (49) |
| phonon MOND limit | a_φ = √(ā a_b), valid for (∇φ)² ≫ 2mμ̂; sourced by BARYONS only | arXiv:1711.05748 eq (8), (34)–(35) |
| condensate EoS / profile | P = ρ³/(12Λ²m⁶); cored, ρ ≈ ρ₀cos^{1/2}(πr/2R) | arXiv:1507.01019 eq (30), (42) |
| MW core / thermalization radius | B-K: R ≈ 158 kpc (M=10¹² M☉); BFK: R_T ≲ 310 kpc (m/eV)^{−8/7}(M/10¹²)^{1/7}(σ/m)^{2/7}; their worked examples 49–82 kpc | arXiv:1507.01019 eq (45); arXiv:1711.05748 near eq (25), eqs (45),(51),(52) |
| local-screening claim | "In the vicinity of individual stars the phonon effective theory breaks down and the correct description is in terms of normal DM particles" — asserted, no radius/criterion published | arXiv:1507.01019 §3.2 |
| lensing statement | photons don't couple to phonons (GW170817); "galaxy-galaxy lensing … closer to the standard cosmological model than … Milgrom's law" | arXiv:1711.05748 §I.2; arXiv:2303.08560 §1, §4 |
| phonon sound speed / Cherenkov | c̄ = 3f̄_β(a_θ/a₀)(√α/m)√(a₀M_Pl), f̄_β = 1/√(3(β−1)(β+3)); "c̄ = 375 km/s·(a_θ/a₀)" at BFK fiducial; exclusion √α/m ∈ [0.34, 3.29] eV⁻¹ (β=2) — BFK fiducial 2.4 eV⁻¹ EXCLUDED | arXiv:2103.16954 §3, eq (10), (17) |
| two-field escape | θ₊/θ₋ split suppresses the radiative matter coupling (τ_E ~ 10¹⁶ yr) while keeping the static MOND force | arXiv:2009.03003 eq (37); arXiv:2103.16954 §4 |
| MOND-limit problem | ε ≡ 2mμ̂/(∇φ)² is O(1) (not ≪1) over much of real galaxies, r ≳ 20 kpc | arXiv:2009.03003 §2.2, Fig 1 |
| SPARC-wide fits | 169 SPARC galaxies: "even the best fits … unsatisfactory"; M/L with "unnatural dependence on size"; best fits live in the NON-MOND regime; forcing the MOND regime → strong-lensing tension | arXiv:2201.07282 |
| lensing RAR confrontation | SfDM vs Brouwer+2021: χ²_red = 15.0/14.9/28.7 (logM_b = 8.5/10.0/11.5 closest-match) vs parameter-free MOND 6.5; "changing the numerical parameter values does not qualitatively affect our conclusions" | arXiv:2303.08560 §4.1, App C |
| Cassini quadrupole | Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² (2026); (3 ± 3)×10⁻²⁷ (2014) | arXiv:2602.17884; Hees+2014 |
| perihelion bounds (repo-pinned) | Mercury 0.0±1.05, Mars −0.020±0.037, Saturn 0.05±0.20 mas/cy | arXiv:1306.3043, 1601.00947 (as pinned in `agentA_f4_eccentric.py`) |
| agentE reflex budget | survival s < (0.34–0.40)a₀ ⇔ quasi-steady anomalous solar response δa ≲ 2.4×10⁻¹⁵ m/s² | `agentE_solar_reflex.out` [9], [2] |
| McGaugh SPARC baseline | 0.1953 dex unweighted (Υ=0.5), 0.2095 (Υ=0.70), framework a₀, pooled 175-galaxy points | `mi_f4_hostile_upsilon.out` |
| lensing split | +0.261 dex early-above-late, 8.8σ baseline, hardened 8.6–9.2σ (u−r), 5.6–6.3σ (Sérsic); per-class med logM_h 12.36 (early) / 11.86 (late) (M13×D08, own catalog) | `lr_battery_results.md`, `agentH_perclass_C.md` |
| WB/DR4 fork | velocity-boost branches: F4 +2–4%, ν_simple +13–16%, McGaugh +11–14%; Newton deep-bin MC medians 0.588/0.639 vs data 0.647±0.02/0.816±0.075 | `mi_f4_widebinary_efe.out` |
| spec-sheet mass band | mc² ∈ [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV (knee window); DR4 knee discriminator ~5×10⁻²⁸ eV | `NONHUYGENS_DOOR_SYNTHESIS.md` item 3 (agentN2) |

**The flagged clash, up front:** the published B-K particle mass is m ~ 0.6–1 **eV** — between **23.8 and 28.9 decades
ABOVE** the spec sheet's ultralight band. The B-K knee (ā = α³Λ²/M_Pl) is set by the symmetry-breaking scale Λ, NOT by m
— so the spec's knee-band logic does not transfer to it, and conversely B-K's a₀ has no Λ_cosmological tie (it is a
fitted coupling; `ESTABLISHED_PATHS_LEDGER.md` banked this). Both the published-mass model and the forced-into-band
variant are run below (T5c).

## PRE-REGISTRATION (locked before any run; outcomes are forks, not predictions)

The decisive physical fork for T1/T2/T5 is the **screening question**: B-K assert (1507.01019 §3.2, one sentence, no
criterion) that the phonon EFT breaks down near stars. The gauntlet computes every standard criterion from the
published parameters (disruption-bubble radius where infall goes supersonic; the Landau/supersonic check for the Sun's
230 km/s; healing length; de Broglie coherence; the radius where the phonon dispersion goes superluminal) and lets the
chain decide which reading each test gets. Both readings are then carried at full weight:
**R1 = face-value** (the published equations extrapolated into the solar system), **R2 = maximally screened**
(phonon force OFF near stars wherever the authors' sentence is invoked).

- **T1 (Cassini Q₂).** (A) R1 violates Cassini/ephemerides by ≥10² → DEAD under R1; R2 verdict then rests on whether
  any computed criterion actually protects the planetary region: if none does, the entry is **"escapes only by
  incompleteness"** (no controlled prediction), not "passes". (B) a computed criterion DOES shut the force off inside
  ≲40 AU while preserving the galactic boost → genuine PASS, and the superfluid hybrid beats AeST/DEW at the Cassini
  wall — report at full weight. (C) marginal (within ×10 of the bound) → data-watch.
- **T2 (solar reflex).** Same fork: (A) R1 anomalous solar response > 2.4×10⁻¹⁵ m/s² by ≥×10 → DEAD under R1;
  (B) R2 → 0 → PASS trivially; record which.
- **T3 (SPARC).** Phonon-only RAR ν_ph(y) = 1 + y^{−1/2} at the PUBLISHED ā (no freedom), pooled dex scatter, Υ ∈
  {0.5, 0.70}, unweighted primary (+ free-ā refit row): (A) within +0.02 dex of the McGaugh baseline → competitive;
  (B) worse by >+0.02 dex at both Υ → disfavored as a one-function RAR; (C) better → report at full weight.
  The published-fit ledger (2 galaxies in BFK; 169-galaxy verdict of 2201.07282) is reported regardless. The task
  brief's premise "BFK 1711.05748 fit SPARC — quote their scatter" is corrected if the pin shows they did not.
- **T4 (type split).** Predicted lensing-RAR early−late offset from the SfDM envelope (lensing = real mass: SHMR+NFW
  at the Brouwer probe radii, own lens catalog, M13×D08 primary, B13×DM14 + Mandelbaum type-dep variants):
  (A) sign matches (+, early above) AND mean magnitude within ×2 of +0.261 dex in ≥1 defensible config → the split is
  CONSISTENT with the SfDM class (locked wording: an exposure-discriminator against type-blind laws, NOT "SfDM
  confirmed" — Brouwer's own MICE/BAHAMAS disagreement rides along); (B) sign mismatch → the phase story fails;
  (C) sign right, magnitude off ×2–5 → partial. The absolute-level lensing-RAR wall (2303.08560) is reported in the
  same breath either way.
- **T5 (WB/DR4 knee).** (A) face-value EFE boost ≥ +10% velocity → SfDM lands on the DR4 detection branch (a clean
  ~3% null kills it; opposite side from F4); (B) screened reading → null branch (Newton-degenerate). The m-band clash
  (published eV vs spec ultralight) is arithmetic, reported regardless; forcing m into the band is checked against the
  EFT's own consistency (c̄ vs c, R_T vs horizon).

Hostility orientation: this is a rival's model — symmetric discipline. Its own fiducials, its authors' own escape
reading (R2), and its best-case configs are all run; so are the kills. Nothing is graded on the framework's a₀
conventions (ā = 0.87×10⁻¹⁰ is the model's own number and is used as such).

---

# RESULTS (filled after the runs; nothing above this line was edited post-run)

## Validation gates (all PASS — `agentH3_gauntlet.out` PART 0/3, `agentH3_typesplit.out` header)
ā = α³Λ²/M_Pl reproduced from scratch: 8.66×10⁻¹¹ (BFK, vs published 0.87×10⁻¹⁰) and 1.19×10⁻¹⁰ (B-K 2015,
their a₀-calibration); c̄(a_θ=ā) = 377 km/s (vs Mistele's 375); the verified q-integral reproduces the banked
anchors exactly (RAR ν: q = −0.2720, Q₂ = +4.654×10⁻²⁶; simple ν: −0.2849, +4.876×10⁻²⁶); precession machinery
agrees three ways (analytic = Gauss integral = 60-orbit two-body LRL to 0.2%); SPARC baselines reproduce
`mi_f4_hostile_upsilon.out` exactly (McGaugh 0.1953 dex @ Υ=0.5, 0.2095 @ Υ=0.70, Υ_bul = 1.4Υ_d); the measured
lensing split reproduces +0.261/+0.185 dex.

## The geography and the screening chain (PARTS 1–2 — the fork-decider)
**The Sun is INSIDE the coherent phase in every published configuration** (R_T = 83–158 kpc vs R₀ = 8.2 kpc;
the MW at M ≲ 10¹²/h is "almost completely condensate"). The phonon force exists at the solar position. The
published escape ("the phonon EFT breaks down near stars", 1507.01019 §3.2 — one sentence, no criterion) was
then computed against every standard candidate criterion, both fiducials:

| criterion | computed value | protects the planets? |
|---|---|---|
| supersonic/Landau (the task's named one) | c̄(local) = 425–602 km/s vs V_☉ = 233 km/s → **Mach 0.39–0.55, SUBSONIC** | **No** — the Sun is ×2 below critical; the naive disruption screen never engages |
| disruption bubble (infall > c̄) | r_dis = 0.005–0.010 AU | No — ×39+ inside Mercury; and the Sun's mass sources phonons in the intact region regardless |
| de Broglie coherence | λ_dB = 1.6–2.7 mm ≫ ℓ = 11–14 μm (ratio 118–232) | No — coherent at planetary radii (B-K's own premise) |
| healing length | ξ = 0.12–0.18 mm | No AU-scale decoherence scale exists |
| **superluminal breakdown** | c̄(r) = c at **r = 10.4–11.5 AU** (Sun-sourced a_θ ∝ 1/r) | **Removes predictivity, not the force**: inside ~10 AU the published dispersion is superluminal — the EFT is out of domain over Mercury–Saturn |
| Cherenkov (published) | √α/m = 2.39 (BFK), 2.64 (B-K15) /eV — both inside the excluded [0.34, 3.29] /eV | Independent **published exclusion of both fiducials** (Mistele 2103.16954 eq 17); the two-field evasion keeps the static force the gauntlet tests |

**Finding:** the task's supersonic criterion, computed from the published parameters, does NOT screen the solar
system — the Sun is subsonic. NO computed criterion shuts the phonon force off at planetary radii. The only
computed breakdown (superluminal dispersion inside ~10 AU) is an EFT-validity hole, not a screen. So the R2
"screened" reading rests on an unquantified sentence with no mechanism behind it under the published EFT.

## T1 — Cassini Q₂ / ephemerides: **R1 DEAD by 6–8 orders; R2 = escapes by incompleteness** (prereg fork A)
- **Direct in-system phonon force** (the dominant channel; all planets sit deep inside r_EFE ≈ 6300 AU, so
  a_φ = √(ā·GM_☉)/r): a_φ/g_N = 4.7×10⁻⁵ (Mercury) → 1.15×10⁻³ (Saturn). Perihelion drifts (analytic =
  Gauss = two-body, validated): **Mercury −1.2×10⁷ mas/cy vs bound 0.0±1.05 → 5.9×10⁶× over (2σ); Mars
  8.6×10⁷× over; Saturn 6.3×10⁶× over.**
- **The EFE quadrupole proper** (the verified Desmond eq (10)–(12) machinery on the phonon interpolation
  function ν_ph(y) = 1 + y^(−1/2), e_N = g_bar,MW/ā set directly): the scale-free phonon function gives
  **q_ph = −3/7 exactly, independent of the external field** (verified at e_N = 0.5–4.0 to 6 digits; vmax-stable
  to 10⁻⁷; a clean analytic byproduct of this run). Hence Q₂ = (9/14)·ā^{3/2}/√(GM_☉) =
  **+4.50×10⁻²⁶ s⁻² (BFK ā) = 24.1σ over Cassini-2026; +7.24×10⁻²⁶ (B-K-2015 ā) = 39.3σ** — worse than
  AeST (3.2×10⁻²⁶) and DEW (2.8×10⁻²⁶), because the phonon force has **no Newtonian-restoration knee at all**
  (the no-knee tail also makes the boost η−1 = 58–87% vs Cassini's ≤2%). AQUAL-vs-QUMOND formulation ~12%
  (repo-measured), immaterial. A scipy roundoff warning on the singular-corner dblquad is noted; the result is
  pinned by the e_N-independence + vmax checks.
- **R2 (screened):** Q₂ = 0 — passes trivially, **but** PART 2 shows no mechanism reaches the planets: under
  the published EFT this is "the solar system is outside the theory's domain", i.e. the model escapes the
  Cassini wall that killed AeST/DEW **only by not making a prediction where they made a fatal one.** Pre-reg
  wording applies: *escapes by incompleteness, not by screening.* (Both fiducials are separately
  Cherenkov-excluded in print; the two-field variant evades Cherenkov but keeps the static force, so T1-R1
  applies to it unchanged.)

## T2 — solar reflex: **R1 over the agentE budget by ×5×10⁴–2×10⁶; R2 zero** (prereg fork A)
SfDM is force-based (not magnitude-keyed inertia), so the reflex channel is the phonon force on the Sun sourced
by Jupiter — r_J-anti-correlated, the same carrier agentE identified. Computed bracket (EFE-suppressed …
isolated-pair): δa_☉ = 1.3×10⁻¹⁰ … 4.3×10⁻⁹ m/s² vs the budget line 2.4×10⁻¹⁵ m/s² (s < 0.34a₀ equivalent):
**×5.4×10⁴ … ×1.8×10⁶ over.** The Jupiter-eccentricity-modulated (unabsorbable) part alone is ×5×10³+ over;
GM_J absorption is Juno-refuted (agentE). Under R2: exactly zero → passes trivially, same incompleteness price.

## T3 — SPARC vs the 0.195-dex McGaugh baseline: **shape-disfavored; the task premise corrected**
**Premise correction (pinned):** BFK 1711.05748 fit **two galaxies** (IC 2574, UGC 2953; their §VII) and quote
**no RAR scatter** — there is no published BFK SPARC-wide fit to quote. The published SPARC-wide confrontation
is Mistele–McGaugh–Hossenfelder 2201.07282 (169 galaxies): *"even the best fits … unsatisfactory"*; M/L with an
*"unnatural dependence on size"*; best fits sit in the **non-MOND regime**; forcing the MOND regime →
strong-lensing tension. This run's numbers (pooled 3389-point RAR, both Υ conventions per the #1 rule):

| model | Υ_d=0.5 unw (wtd) | Υ_d=0.70 unw (wtd) |
|---|---|---|
| McGaugh ν, framework a₀ (baseline) | **0.1953** (0.1122) | **0.2095** (0.1042) |
| McGaugh ν, canonical a₀ | 0.1989 | 0.2245 |
| SfDM phonon-only, published ā=0.87e-10 | 0.2031 (**0.1009**) | 0.2432 (0.1508) |
| SfDM phonon-only, published ā=1.19e-10 (B-K15) | 0.2185 | 0.2677 |
| SfDM phonon-only, FREE ā | 0.1976 (ā=6.2e-11) | 0.2142 (ā=3.6e-11) |

Both ways at full weight: at Υ=0.5 with its own published ā the phonon skeleton is only +0.008 dex behind
McGaugh unweighted and **beats it weighted** (0.1009 vs 0.1122, this-run convention) — *not* SPARC-dead as a
fit. But: (i) at Υ=0.70 it is +0.034 behind; (ii) the **systematic high-acceleration overshoot is the real
shape defect** — the unscreened y^(−1/2) tail leaves a +0.07 dex (Υ=0.5) to +0.21 dex (Υ=0.7) mean excess at
y > 10, exactly where data sit on the 1:1 line; condensate gravity only adds to it; (iii) free-ā rescue pushes
ā down to 3.6–6.2×10⁻¹¹, ~30–60% below the published value. Per the prereg fork: **convention-mixed —
competitive at MOND-default Υ, disfavored at Υ=0.70, with a Υ-independent high-end shape defect**; and the
model does not predict a *single* RAR at all (the condensate term is galaxy-dependent; the published 169-galaxy
verdict stands).

## T4 — the type split: **SIGN MATCHES; measured magnitude sits inside the predicted bracket** (fork A; `agentH3_typesplit.out`)
Predicted early−late lensing-RAR offset at fixed g_bar from the repo's own lens catalog (lensing = real
condensate+NFW mass; the phonon does not lens):

| config | mean Δlog g_obs | 1-halo-safe bins |
|---|---|---|
| M13×D08, type-blind SHMR | **+0.119** | +0.105 |
| B13×DM14, type-blind | +0.113 | +0.111 |
| M13×D08 + Mandelbaum16 type-dep | **+0.401** | +0.327 |
| B13×DM14 + type-dep | +0.402 | +0.354 |
| **MEASURED** | **+0.261 (u−r) / +0.185 (Sérsic)** | — |

Positive (early above) in **all configs and all 15 bins** — the sign the task asked about MATCHES the measured
+0.26 dex. Magnitude: the measurement sits **between** the type-blind (0.46×) and type-dependent-SHMR (1.54×)
predictions — within the prereg ×2 band on the defensible configs. The phase leg is real and quantified: 68%
of early-type lens halos sit above the B-K condensation boundary vs 27% of late (med logM_h 12.36 vs 11.86;
core/r200 fraction 0.39 vs 0.48) → early types have less coherent superfluid (smaller phonon boost,
kinematics) and more normal-phase real mass — the direction chain the task named, confirmed end-to-end.
**Locked wording enforced:** this is the generic real-mass/SHMR effect — it shows the ~9σ split is *consistent
with* (even expected in) the SfDM-class hybrid where it is *fatal to* type-blind universal force laws; it is
NOT "SfDM confirmed" (MICE/BAHAMAS disagree on the split), and the same model **fails the absolute lensing-RAR
shape on the same data** (2303.08560: χ²_red 15–29 vs parameter-free MOND 6.5). Note the structural inversion
vs our walls: SfDM trivially clears the 40.5σ metric-passive wall (lensing from real mass, not baryons only)
and plausibly carries the 9σ split — the two exposures that kill universal-force MOND — while dying in the
solar system, where universal-force MOND was merely wounded.

## T5 — WB/DR4 knee: **face-value lands on the DETECTION branch, opposite F4; the m-band clash quantified**
No published SfDM WB prediction exists (searched). Computed from the published force law: WB separations
(2–30 kAU) sit outside every computed breakdown scale and the EFE-saturated boost applies:
**velocity boost +25.6% … +36.6%** (force boost η−1 = 58–87%) across both fiducials and the g_bar bracket —
the **largest WB signal of any candidate on the board** (banked fork: F4 +2–4%, simple ν +13–16%, McGaugh RAR
+11–14%). DR3 placement: SfDM-shifted deep-bin medians ~0.75/0.82 vs data 0.647±0.02/0.816±0.075 — bin 1 sits
~5σ above (contamination-degeneracy caveat rides). **DR4 fork: a clean ~3% null kills face-value SfDM
decisively; a +10–15% detection that confirms soft MOND also kills it (it predicts +26–37%, not +13%); only a
+25–35% detection selects it.** R2 (maximally screened) → null branch, but now the uncomputed screen must
stretch from 10 AU to >30 kAU with no published mechanism at all.

**The m-band clash (run both, as flagged):** published m = 0.6–1 eV is **23.6–23.8 decades above the spec
sheet's band top** (1.6×10⁻²⁴ eV; bottom 28.9 decades). Forcing m into the band at fixed (ā, α): c̄ ∝ 1/m
goes superluminal already at m ≈ 1.7×10⁻³ eV (at the band top c̄/c ~ 10²¹), and R_T(1.6×10⁻²⁴ eV) ≈ 5×10²⁹ kpc
— 23 decades past the horizon: **the B-K mechanism cannot inhabit the spec's ultralight band; the band belongs
to fuzzy-DM-class physics.** Conversely B-K's knee ā = α³Λ²/M_Pl is Λ-set and m-free: the spec's DR4
knee-position discriminator (~5×10⁻²⁸ eV) cannot probe it — and B-K's a₀ carries **no Λ_cosmological tie**
(banked: "a₀ is a fitted phonon coupling, not cH"). The two hybrid classes are structurally disjoint objects
that happen to share the word "hybrid".

## VERDICT (both ways, full weight)
**The superfluid-DM-class hybrid clears exactly the two walls that kill universal-force MOND — and dies on
exactly the fronts where universal-force MOND survives.**
- **Clears:** the 40.5σ metric-passive lensing wall (by construction: lensing = real mass) and the ~9σ type
  split (sign predicted, magnitude bracketed, phase chain quantified — the first candidate on the board with a
  story for the repo's hardest exposure). Geography is real: the solar system IS inside the coherent phase.
- **Dies (face-value reading R1):** solar system by 6–8 orders (direct phonon force; perihelion drifts 10⁶–10⁸×
  over bounds; Q₂ = 24–39σ over Cassini with the exact universal q_ph = −3/7; solar reflex ×10⁴·⁷–10⁶·³ over
  the agentE budget). The published screening sentence has **no computable mechanism behind it**: the Sun is
  SUBSONIC (the task's named criterion fails), the disruption bubble is 0.005–0.01 AU, and the only real
  breakdown (superluminal phonons inside ~10 AU) removes predictivity, not the force.
- **Survives only as R2:** "no prediction inside ~10 AU" — escaping the Cassini wall by incompleteness where
  AeST/DEW failed it by computation. That escape is *legal but unpaid*: it owes a UV-completion calculation, and
  both published fiducials are independently Cherenkov-excluded in print (the two-field fix keeps the static
  force, so the R1 kills transfer to it intact).
- **SPARC:** competitive-to-disfavored (convention-mixed), with a Υ-independent +0.07–0.21 dex high-end shape
  defect and no single-RAR prediction; the published 169-galaxy verdict is "unsatisfactory".
- **DR4 fork:** face-value SfDM is the most falsifiable object on the board (+26–37% WB velocity signal) and
  sits opposite F4; the 2027 data adjudicate between them in one shot.
- **For the spec sheet:** the B-K object is NOT the missing object of `NONHUYGENS_DOOR_SYNTHESIS.md` — wrong
  mass scale by ≥24 decades (and cannot be moved into the band), no Λ-tie for the knee, and a dead-or-undefined
  solar system. What it DOES demonstrate, quantitatively, is that a hybrid whose lensing partner carries real
  type-dependent mass can absorb the repo's two lensing exposures — the spec-sheet's "lensing partner" line
  now has a worked existence proof of the *phenomenological shape* required, attached to a microphysics that
  fails everywhere else.

*Files: `agentH3_gauntlet.py/.out` (T1, T2, T3, T5 + criteria chain), `agentH3_typesplit.py/.out` (T4).
Machine state: every gate passed; scipy quadrature roundoff warning on the singular-corner q-integral noted and
bounded (e_N-independence to 6 digits, vmax-stability 10⁻⁷). No git operations performed.*
