# Open observational doors (2026) — the three live tests in decisive forecast-ready form + a fresh-scan for a NEW distinctive test

*C. Zimmerman / session 1b2404fe, 2026-06-27. PURE framework-internal (no comparison to other theories as
the subject — the framework is the subject throughout). Footing locked: **a₀ = 9.36×10⁻¹¹ m/s²** (the
framework's OWN pure-Λ dS–Unruh value, used only as INPUT — every front INDUCES from it, none derives it),
the framework's OWN interpolation μ_fw(x) with the inverse relation μ/(1−μ²)=a/a₀ (golden check μ_fw(1)=1/φ=
0.61803, verified) and the dS–Unruh kernel θ(0)=√2. **McGaugh's ν is NEVER used.** All numbers independently
re-derived this session with mpmath (dps=30) + numpy and cross-checked against the banked source files.
Both-ways, anti-overclaim: most observational doors are future-gated or below-floor — the genuine ones are
named, and where a door is shut or decoupled I say so straight. LOCAL — do NOT git-push.*

Scratchpad verification scripts: `/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/{verify_all.py, verify_front2.py, verify_dwarf2.py, match_v2.py, verify_dipole.py}` (all run clean).
Grounding (all absolute): `opus_48_extended_research/reviews/{CASSINI_STX_REVERIFY_2026-06-21.md, FRONT_CASSINI_STX_2026-06-20.md, FRONT_A0Z_DESI_2026-06-20.md, SIGMA_SPREAD_MI_TEST_2026-06-19.md}`, `real_research/{DWARF_ECC_SIGMA_PILOT_2026-06.md, THETA_KERNEL_TOWARD_FORCED_2026-06.md}`, memory `reference_published_papers_live_frontier`, `project_sme_lorentz_bridge`, `project_a0z_muse_confrontation`.

---

## PART 1 — THE DECISIVE NEAR-TERM PROGRAM (ordered by when the verdict arrives)

| # | Test | What it touches | Verdict arrives | Confirm / kill threshold |
|---|---|---|---|---|
| 1 | **Dwarf σ y-contrast** | MI-vs-MG (history-dependent inertia) | **Gaia DR4, Dec 2026** (axis) → ~2028-32 (σ) | carrier-vs-control σ sign-split around y=1 |
| 2 | **a₀(z) / BTFR-sign** | evolving dark-energy ↔ a₀ | **DESI DR3, 2026-27** (gate) → ALMA/ELT 2030s | z≥2 BTFR zero-point BELOW local |
| 3 | **s^TX SME boost-dipole** | preferred-frame / Lorentz violation | **~2028-32** (analysis-limited) | global SME-in-loop refit ≳5× → ±8.7e-10 |

### TEST 1 — the dwarf orbital-history σ y-contrast (the nearest axis; Gaia DR4, Dec 2026)

**The prediction, SHARPENED on this session's resolved kernel (DOI 20963226 v2, 2026-06-27).** The framework's
inertia is a nonlocal-in-time response to the de Sitter horizon bath, which carries exactly ONE clock H_Λ. A
member's effective inertia argument is A = a_in + θ(y)·a_ex with y ≡ ω_ext/ω_in. The memory kernel is now
bath-derived, not free: **θ(y)=θ₀/(1+(θ₀−1)y²), θ₀=√2** (selected on the framework's own excess-heat /
amplitude coupling — it already rejects the T²−T_Λ² energy branch to get the right deep-MOND law; the Luo
additive-acceleration construction confirms unit-weight first-moment), Lorentzian form + y⁻² tail forced by
the dS Wightman 1/sinh²→exponential memory. The **σ boost ≈ θ(y)^(1/2)−1** (reproduced this session; matches
the published headline to the digit):

| y = ω_ext/ω_in | θ(y) | σ boost vs the y=1 reference |
|---|---|---|
| 0.35 | 1.346 | **+13–16%** (preferred +12–14%) |
| 0.50 | 1.282 | **+13%** |
| 1.00 | 1.000 | **EXACTLY 0** (forced zero-crossing) |
| 1.30 | 0.832 | −9% |
| 1.50 | 0.732 | −14% |
| 2.00 | 0.532 | −27% |

**The robust, MG-impossible core (theorems, kernel-independent):** (i) **SIGN** — hotter for y<1, colder for
y>1; (ii) **EXACT zero-crossing at y=1** (ω_ext=ω_in); (iii) **monotone decrease**. Modified gravity (AQUAL/
QUMOND/AeST) has an instantaneous EFE depending only on the momentary a_ex (Milgrom 2022, verbatim) → θ≡1
identically → **exactly zero** infall-phase σ dependence for any a₀. CDM also has no inertia channel. So a
nonzero, sign-changing, y=1-crossing σ contrast is **MG-AND-CDM-impossible** and **non-a₀-degenerate**.

**⚠️ CRITICAL RECONCILIATION I am flagging straight (v1→v2, against the loose framing).** The banked v1
"carriers run HOTTER" framing named **Crater II (y=3.28)** and **Antlia II (y=2.55)** as the carriers — but on
the resolved v2 kernel those sit on the **y>1 SUPPRESSED (COLDER) side**, not the hotter side. The +12–14%
HOTTER signal lives at **y=0.35–0.50** (the sub-unity plunging band). So the correct v2 statement is NOT
"plungers are hot" but **"σ splits around y=1: hotter below, exactly zero at y=1, colder above."** This is
sharper and more falsifiable than the v1 framing (a SIGN-CHANGE across a known axis value is far harder to
fake than a one-sided excess), and it means a dwarf sample must be **binned across y=1**, with Crater II /
Antlia II expected on the COLD side. The earlier "carriers hotter" reading was the v1 single-band
approximation; do NOT carry it forward.

**Decisive analysis.** Measure resolved internal σ for a diffuse-dwarf sample with Gaia-measured per-object
y (built from ω_ext at pericenter / ω_in from σ,r_half), bin **across y=1**, and test the σ(y) sign-change at
matched pericenter+mass with explicit tidal modeling. Carriers below y=1 (hotter) and above y=1 (colder) +
the zero-crossing = the framework signature; flat σ(y) = the MG/CDM null.

**Timeline + threshold.** **Gaia DR4 (Dec 2026)** delivers the sharpened per-object orbits + a larger
diffuse-dwarf set — this is the **nearest** thing that moves (the axis). The σ side needs resolved profiles
to ~2–3 km/s → a dedicated MUSE/KCWI campaign **~2028–32** for a marginal ~3σ; ELT-HARMONI resolved-star σ
**~2032+** for a definitive 3–5σ. **Magnitude is θ₀-hostage** (factor ~2: the θ₀=2 double-pole envelope
roughly doubles every number to +24–30% at the band edge) — quote the **+12–14% preferred / +12–30% envelope**
range, never a point value. The pre-registered 24-dwarf pilot (Pace+2022 / Gaia EDR3) was an honest NULL at
no power (partial Spearman ρ=−0.196, p=0.40, tidal-robust) — **only 2 dwarfs reach |y|≳1 and the σ errors are
comparable to the signal**; existing data cannot yet test it, and I say so straight.

### TEST 2 — a₀(z) and the z≥2 BTFR sign (the DESI DR3 gate, 2026-27)

**The prediction (the framework's OWN declining √ρ_DE branch; κ, c, Z, interpolation ALL cancel — sympy-proven
— only w(z) enters).** Under DESI DR2+DESY5 (w₀=−0.752, wₐ=−0.86), a₀(z)/a₀(0)=√(ρ_DE(z)/ρ_DE(0)) is
**non-monotonic** (DESI's w crosses −1 at z=0.405, so ρ_DE — hence a₀ — peaks there, then declines). Verified
this session to dps=30:

| z | a₀(z)/a₀(0) | deep-MOND BTFR V offset (dlogV = ¼ dlog a₀) |
|---|---|---|
| 0.405 | 1.0615 | +0.0065 dex (+1.5% V) — the **+6.15% a₀ bump**, LOCKED to the phantom crossing |
| 1 | 1.0087 | +0.002 dex |
| 2 | 0.862 | −0.016 dex |
| **3** | **0.737** | **−0.033 dex (−7.34% V) BELOW local** |

**The OUTPUT discriminator is the SIGN of the z≥2 BTFR zero-point offset.** Three-way at z=3 (framework
footing): framework declining = **−0.033 dex BELOW** local; constant-a₀ MOND (the NULL) = **ON** the local
zero-point; rising rival cH∝E(z) = **+0.164 dex ABOVE** (already excluded by Milgrom 2017 / clusters / RC100).
**The framework is the ONLY hypothesis predicting V BELOW the local BTFR.**

**NON-diagnostic NOW (quarantine-honest, both ways).** DESI supplies ρ_DE as the **INPUT**; the framework
merely outputs a₀(z)=√ρ_DE. "DESI confirms a₀(z)" is **forbidden** — it confirms the input. The only genuine
OUTPUT test is the z≥2 BTFR sign. The √ρ_DE shape is **Limbach-Psaltis-Özel 2008** (not novel); the
framework's fresh pieces are the value c²√(Λ/32π), the DESI-w₀wₐ evaluation, and the z~0.4 bump.

**The one direct datum is in real tension — reported straight.** MUSE-DARK III (Ciocan 2026, A&A 709 L16)
measures a₀ **RISING** ~2× by z~1; the amplitude-marginalized SHAPE test puts the framework's **declining
branch as the WORST-fitting of the three (~17σ raw, WRONG SIGN)**, softening to **~3–5σ** only via genuinely-
shared ΛCDM systematics (the Magneticum assembly drift gives apparent a₀ rising ×3 with NO fundamental a₀, ≈
50% of MUSE's slope; MUSE is steeper than every forward-model including the rising rival). This is the
**strongest live pressure on the framework's distinctive content** — NOT a referee-proof kill (shared
systematic + MUSE-too-steep-for-all), but I do not dress it as anything softer than a real tension.

**Timeline + threshold.** **GATE 1 = DESI DR3 (2026-27):** w(z) stays evolving (currently 3.1–4.2σ) → the
hostage is FREED, declining branch live; reverts to w=−1 → a₀=const → the distinctive content **dissolves** to
plain constant-a₀ MOND (dissolution, NOT a kill — constant-Λ is the safe core; w=−1 does NOT rescue the MUSE
tension, it flattens the branch to exactly flat). **GATE 2 = z≥2 clean gas-traced BTFR sign:** ALMA [CII]/
[OIII] rotating discs ~2028-30 (needs M_b systematic ≲0.04 dex), ELT-HARMONI definitive early-mid 2030s.
**The z=3 decline sign is conditional on large |wₐ|** (flips positive under low-|wₐ| ACT variants) — flag it.

### TEST 3 — the s^TX SME boost-dipole (analysis-limited, ~2028-32)

**The exact prediction (ephemeris-analyst-ready; re-derived this session to dps=30).** The framework is a
forced preferred-frame (Lorentz-violating) modified-inertia theory → it induces a gravity-sector spurion
s̄^μν = (a₀/2|a|)(uᵘuᵛ)_traceless about the CMB rest frame. Three rows (trace=0 exact): (i) **s^TT = ¾(a₀/2|a|)**
O(1) isotropic, fully **ABSORBABLE** (Bailey-Kostelecký) — tests nothing; (ii) **s^TJ = (a₀/2|a|)·β_cmb·n_J**
the O(β) boost dipole — the leading **OBSERVABLE**; (iii) s^<JK> O(β²) quadrupole — 20–123× under its bound,
not binding. Inputs: β_cmb=369.82 km/s/c = **1.2336×10⁻³**; CMB apex RA=167.94°, Dec=−6.94° →
n=(−0.9708, +0.2074, −0.1208), |n|=1.000. **Sign: s^TX NEGATIVE** (n_X<0). **LOCKED ratios (the joint
fingerprint):** s^TY/s^TX=−0.214, s^TZ/s^TX=+0.124.

**Per-body 1/|a| ladder** (|s^TX|=(a₀/2|a|)·β·|n_X|, |a|=GM☉/r²):

| body | \|a\| (m/s²) | \|s^TX\| | a₀/a |
|---|---|---|---|
| Mercury | 0.0396 | 1.42e-12 | 2.4e-6 |
| Earth/Moon (LLR) | 0.00593 | 9.45e-12 | 1.6e-8 |
| Mars | 0.00255 | 2.19e-11 | 3.7e-6 |
| Jupiter | 2.19e-4 | 2.56e-10 | 4.3e-7 |
| **Saturn / Cassini** | **6.46e-5** | **8.68×10⁻¹⁰** | **1.45e-6** |

Saturn is the **binding body** (lowest-a well-tracked point, so A=a₀/2\|a\| is largest there — NOT because it
is near a₀: a₀/a_Saturn=1.45×10⁻⁶, deeply Newtonian).

**Decisive analysis.** A single global **SME-in-loop ephemeris refit** that fits all 8 orbital s̄ components
simultaneously to EXISTING data (Cassini Grand-Finale Saturn ranging + INPOP/EPM planetary postfit + LLR +
VLBI) with the framework's **CMB-apex direction and locked s^TY:s^TX:s^TZ ratios imposed as a one-template
prior** — collapsing 8 free coefficients to 1 amplitude, beating the marginalized covariance. The prospective
tightening path confirmed in the 2026 scan: the **Gaia DR3/DR4 Solar-System-Object asteroid covariance fit**
(Hees et al. arXiv:1509.06868; ~360,000 wide, decorrelating sub-mas asteroids) forecasts s̄^μν below today's
best — **the data already exist; the test is purely analysis-limited**.

**Timeline + threshold (sharpened — corrects the loose banked "3–10×").** Today's tightest published bound is
the **combined fit s̄^TX=(−0.2±1.3)×10⁻⁹** (Kostelecký-Russell Data Tables v19, Jan/Feb 2026, Table D50, ref
Hees 2016). The Saturn-a prediction 8.68×10⁻¹⁰ sits at **0.67σ INSIDE** (margin 1.50×, predicted NEGATIVE
sign consistent with the −0.2e-9 central value — within the bar, NOT a detection, NOT wrong-signed). Refit
factor → decisiveness (verified): **3× → only 2.0σ (STILL INDECISIVE); 4.5× → exactly 3.0σ; 5× → 3.3σ
(DECISIVE); 10× → 6.7σ.** So the honest decisive bar is **~5×, not 3×.** **Timeline ~2028-32, analysis-
limited** (no new spacecraft; the Gaia SSO fit / extended INPOP-EPM full-SME / Cassini residuals carry it).
The r-varying refinement (s̄∝r², +r² aphelion weighting) tightens Saturn by only +0.5%; the convention-free
bracket [1.34×, 1.68×] stays >1 → **no flip to excluded without a real refit; the ~1.5× margin is ROBUST.**

**Both-ways caveats the analyst MUST carry.** (1) s^TX is the **preferred-frame / LV** discriminator, **MOND-
family-SHARED** — any preferred-frame MG host (AeST, khronometric, Hořava) induces a comparable s^TX, so a
detection confirms preferred-frame inertia but does **not** separate MI from MG. The genuinely MI-vs-MG-
distinctive Cassini content is the **separate a₀/2≈4.7×10⁻¹¹ channel** (excluded ~3.7 orders as MG via
Kepler-III; evades ~3 orders as MI), already in hand. (2) The planetary s^TX tests only the β-suppressed
projection (~0.12% of the O(1) effect), NOT the framework-unique content. (3) Quarantine held: a₀ is INPUT.
(4) The CPT-even-only theorem holds and BITES — the natural CPT-odd scale ħH₀=**1.49×10⁻⁴² GeV is 149× ABOVE**
the photon CFJ bound (~1e-44 GeV), so a CPT-odd realization at the framework's own scale would already be
excluded; the framework predicts k_AF=a_μ=b_μ=0 exactly and survives by **structure, not tuning**. (5) **NO
2024-26 result tightens it** (Dong-Wang-Shao 2024 pulsar |s^TX|<2.9e-9, LLR (−0.9±1.0)e-8, INPOP-only
(−2.9±8.3)e-9 — all LOOSER; **there is NO INPOP21a/EPM2021/BepiColombo s^TX fit** — those test graviton
mass/dilaton/PPN/Ġ, the WRONG channel; **BepiColombo does NOT bind s^TX**). DO NOT cite the banked "9.6×"
(superseded INPOP-only bound) — the live margin is ~1.5× worst-corner.

---

## PART 2 — THE FRESH SCAN: is there a genuinely-NEW framework-distinctive above-floor test?

### The headline candidate — the COSMIC DIPOLE TENSION — is DECOUPLED (named straight)

The prompt's sharpest fresh-scan question: the cosmic number-count dipole anomaly **escalated to 5–6.4σ in
2026** (the same significance tier as the Hubble tension) — radio/QSO source counts (Secrest+2021; Quaia/
CatWISE 2025-26) give a dipole **2–5× the CMB-kinematic 0.12%**, implying a ~1700 km/s "velocity" along
**the same CMB apex** the framework's preferred frame points at. Does the framework's preferred-frame / MI
content touch it?

**Verdict: NO — DECOUPLED. This is the honest both-ways result, credited and stated straight.** Three
independent reasons, verified this session:

1. **Channel mismatch.** The cosmic dipole is a **source-count / large-scale-structure clustering** signal in
   QSOs/radio galaxies at **z~1-2 in the HIGH-acceleration (Newtonian) regime** (g ≫ a₀). The framework's
   preferred-frame inertia anisotropy is a **galaxy-kinematics / weak-lensing** effect that exists **ONLY at
   a≲a₀** (it switches OFF above a₀). The framework induces **no number-count dipole** — these are orthogonal
   observables.
2. **Amplitude.** The framework's deep-MOND inertia dipole observable is **0.062%** (=½·β_cmb, slope-weighted;
   verified) — **~8× BELOW** the ~0.5% cosmic-dipole excess. Even if the channels overlapped, the framework
   cannot source the anomaly.
3. **The 2026 literature is attacking it through a DIFFERENT door.** The brand-new Moffat 2026 paper
   (arXiv:2601.07487) explains the excess via **STVG-MOG's scale-selective GIGAPARSEC enhancement of the
   matter dipole** — a large-scale clustering / modified-Friedmann channel. The framework has **no such
   cosmological-perturbation enhancement**; its modification is a local-acceleration inertia law, silent on
   gigaparsec structure growth. So even the MG family that DOES touch the cosmic dipole does it via a mechanism
   the framework structurally lacks.

This is a clean "say-so-straight" result: a tempting same-apex coincidence that, examined on the framework's
own premises, is a **decoupled channel** — the framework neither explains nor is constrained by the cosmic
dipole anomaly.

### The nearest framework-distinctive above-floor signature (named, but below-floor this decade)

The framework's genuinely-UNIQUE preferred-frame content is the **CMB-apex-locked inertia-anisotropy DIPOLE
at a≲a₀** — a **dipole (ℓ=1), exactly cos(ψ)**, locked to the FIXED CMB apex (galactic ℓ=264.0, b=+48.3),
**NEGATIVE-signed**, saturating at −½β_cmb=**−0.062%** in deep MOND and **switching OFF above a₀**. No
isotropic ΛCDM/MOND can fake a fixed-apex dipole. The sharpest probe is the **weak-lensing RAR dipole**
(KiDS→Euclid/Rubin N~10⁹; the only probe that reaches deep-MOND saturation and is immune to kinematic
systematics). **Honest verdict: BELOW-EVERY-FLOOR this decade — but SYSTEMATIC-limited, not statistics-
limited** (Euclid N~10⁹ beats 0.062% statistically by ~56×; the killer is the sky-correlated M/L +
circumgalactic-gas zero-point dipole ~100–400× the target, which does NOT average down with N). The existing
search (Zhou+2017/2018 SPARC RAR dipole) is null/non-diagnostic (spurious direction ~103° off apex). It IS
better-posed than the a₀(z) +2% bump (the apex is fixed + known to <1° → a one-parameter targeted template),
but reachable only mid-late 2030s at earliest, possibly never at 0.062%.

### Other candidates scanned — all below-floor / future / shared (no new near-term door)

- **Inverted-BH strong-field null** (DOI 20947913): framework forces exactly-GR shadow/ISCO/ringdown,
  falsifying metric-MOND (AeST/MOG) — extends Cassini's MI-vs-MG axis to strong field, but ngEHT 2030s /
  LISA 2035+ (far-future).
- **Cluster relational σ-spread** (SIGMA_SPREAD_MI_TEST): genuine MG-impossible MI signature, but CONFOUND-
  LIMITED (tidal-shock heating fakes a same-signed correlation; deployable only as the joint amplitude+
  radial-trend signature), carrier UDGs only (~0–45/cluster), and ~2028-32 marginal at best. Same physics
  family as Test 1, harder.
- **Floor temperature T₀=2.20×10⁻³⁰ K** (capstone theory, DOI 20965016): ~34 orders below atomic — no lab
  effect, not a test.

**No NEW above-floor near-term distinctive test emerged from the 2026 scan.** The three live tests in Part 1
remain the genuine frontier; the cosmic dipole — the single most tempting 2026 candidate — is decoupled. I am
not manufacturing a fourth door.

---

## THE HONEST NEAR-TERM CALENDAR

**Could move in 2026-27:**
- **Gaia DR4 — December 2026.** Sharpens per-object dwarf orbits (the y-axis) → enables the carrier-vs-control
  σ y-contrast (Test 1) as a designed measurement. The nearest thing that moves; it delivers the AXIS, not yet
  the σ verdict.
- **DESI DR3 — 2026-27.** The a₀(z) make-or-break (Test 2). Evolving DE survives → hostage freed; w→−1 →
  distinctive content dissolves to constant-a₀ MOND (NOT a kill). Currently favored at 3.1–4.2σ.

**Later (2028+):**
- **s^TX ephemeris refit — ~2028-32** (Test 3). Analysis-limited on existing data; needs a ~5× SME-in-loop
  refit to put the Saturn-a prediction at 3σ.
- **ALMA z≥2 BTFR sign — ~2028-30**; **ELT-HARMONI** clean a₀(z) tracking + dwarf σ + cluster σ-spread +
  weak-lensing apex dipole — **early-mid 2030s**.

---

## WHAT TO TELL CARL (straight)

You have three genuinely-live observational doors, and the nearest one moves first. **Gaia DR4 in December
2026** sharpens the dwarf orbital axis for your horizon-bath σ prediction — and this session's resolved kernel
(θ(0)=√2, the v2 dwarf paper) makes that prediction SHARPER and more falsifiable than the old framing: σ does
not just "run hot for plungers," it **splits around y=1 — hotter below, exactly zero AT y=1, colder above** —
a sign-change across a known axis value that modified gravity and CDM both forbid (their inertia is
instantaneous → exactly flat). One correction you should carry: your named carriers Crater II and Antlia II
are y>1, so on the new kernel they sit on the COLD side; the +12–14% hot signal is at y=0.35–0.50. Bin across
y=1, not above it.

**DESI DR3 (2026-27)** is the a₀(z) gate. If evolving dark energy holds, your declining √ρ_DE branch stays
live and predicts galaxies at z≥2 sitting ~7% BELOW the local baryonic-Tully-Fisher line — the one thing no
constant-a₀ MOND and no rising rival predicts. Straight talk on the one direct datum: the MUSE/Ciocan
measurement has a₀ RISING, which puts your declining branch as the worst-fitting of the three branches at face
value (softening to ~3–5σ only through a ΛCDM systematic shared by everyone). It is real pressure, not a kill,
and I am not softening it past that.

**s^TX (~2028-32)** is the ephemeris test, and I've sharpened the threshold: it needs a ~5× SME-in-loop refit
of existing Cassini+LLR+VLBI data to become decisive (a 3× refit leaves it indecisive at 2σ) — the data exist,
it's purely analysis-limited, and your Saturn prediction (8.7×10⁻¹⁰, negative, CMB-apex-locked, with the
locked s^TY:s^TX:s^TZ ratios) sits 0.67σ inside today's bound: live, neither safe nor excluded.

On the fresh scan: the 2026 cosmic-dipole anomaly (now 5–6.4σ, same tier as the Hubble tension, pointing at
YOUR CMB apex) was the tempting candidate — and the honest answer is that **your framework is decoupled from
it.** It's a source-count signal at high acceleration; your preferred-frame inertia only bites at a≲a₀, is ~8×
too small, and induces no number-count dipole. Moffat's brand-new 2026 paper explains the dipole through a
gigaparsec structure-growth enhancement your local-inertia law structurally lacks. So I won't sell you a
fourth door there. Your genuinely-unique signature — the fixed-apex −0.062% lensing dipole at a≲a₀ — stays
below the sky-systematic floor this decade (systematic-limited, not statistics-limited). The frontier is the
three doors above, and the calendar is real.

**This door stays open** — never "no doors." The nearest verdicts are 6–18 months out (Gaia DR4, DESI DR3).

### Sources
Kostelecký-Russell Data Tables v19 (arXiv:0801.0287, Jan/Feb 2026, Table D50; s̄^TX=(−0.2±1.3)e-9, Hees 2016);
Hees et al. Gaia SSO (arXiv:1509.06868); Bailey-Kostelecký (gr-qc/0603030); Dong-Wang-Shao 2024 (PRD 109
084024). DESI DR2 (arXiv:2503.14738); Limbach-Psaltis-Özel 2008 (arXiv:0809.2790); MUSE-DARK III Ciocan 2026
(A&A 709 L16, arXiv:2604.22613); Magneticum Mayer+2023 (arXiv:2206.04333). Cosmic dipole: Colloquium
(arXiv:2505.23526), Quaia/CatWISE (arXiv:2511.00822), Moffat STVG-MOG 2026 (arXiv:2601.07487).
Framework records: a₀(z) DOI 10.5281/zenodo.20737162; dwarf σ v2 DOI 10.5281/zenodo.20963226; capstone theory
DOI 10.5281/zenodo.20965016; inverted-BH DOI 10.5281/zenodo.20947913.
