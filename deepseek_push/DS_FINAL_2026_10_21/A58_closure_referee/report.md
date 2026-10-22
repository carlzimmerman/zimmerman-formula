# A58 — THE CLOSURE REFEREE

Lane A58. `a58_checks.py` (36 checks, 36/36 PASS, exit 0, 0.4 s), `a58.out`,
`a58_results.json` (checks + 50-claim ledger + every quoted number), `MUTATE.md`
(3 mutations, 4/3/1 checks broken). No commit. SI.

**Provenance — what had landed.** No A5x lane had a `report.md` at referee time. Where a
script existed I ran it (read-only, output captured in this lane) and attacked its printed
claims; where nothing existed I attacked the answer where it is actually written, in
`THEORY.md` §3.2–3.6 and the originating lanes.

| lane | on disk at 23:10 | verdict I could attack |
|---|---|---|
| A50_horizon_thermo | empty directory | **none** |
| A51_kappa_measured | checks only; run >180 s, `a51.out` empty | script: lensing carries zero κ information (K8) |
| A52_the_number | report + 17/17 + out + 4 mutations | 11.5776 not special; κ_meas = 0.417 ± 0.095 |
| A53_medium_candidates | empty directory | **none** |
| A54_four_gates | checks + run0/run1; no report; run0 traceback | G8: galactic α₁ = 0.073–5.194 |
| A55_lensing_prediction | `_scratch` only | **none** |
| A56_Lstar_origin | report + 25/25 + 5 mutations | L* unique in a grammar; "the medium has no velocity scale" |
| A57_uv_completion | report + 20/20 + Lean certificate | no joint (κ, L*); misses 7.4 dex; 1 excess input |

Finding #0: **three of eight lanes produced the report the brief requires; two produced only
a script (A51, A54) and three nothing (A50, A53, A55).** The closure cannot be written as
"A50–A57 say so". That is the referee's first duty here, independent of every number below.

## Claim

The four answers compute cleanly (34/50 ledger claims BACKED; every re-derivable number
agrees with its lane) and **fail as closure**: three are status upgrades of a result their
own lane labels CONDITIONAL, NO-GO or OPEN. Defect density is 16/50 = 32.0 % against A31's
document-wide 24.6 % (ratio 1.30) — the four answers are where upgrade pressure concentrates.
Two of my first-pass findings were wrong; A52/A56 correct them below, and that is recorded.

## 0. Verdict

| # | answer | grade | defects | load-bearing claim | verdict | deciding number |
|---|---|---|---|---|---|---|
| Q1 | κ = 1/2 from the horizon | **C** | 3/13 | `a0/(cH_Λ) = 1/Z` is a horizon fact that fixes κ | **WRONG** (as derivation) | 0.4944 = gap from g=Z to 2π |
| Q2 | the medium + discriminator | **C** | 5/14 | the law is the stationary state of a single-scale gate lattice | **OVERSTATED** | +17.05 < 25 (pre-registered) |
| Q3 | the four gates | **B−** | 4/12 | four independent gates pass | **OVERSTATED** | 2 premises / 4 gates |
| Q4 | the origin of L* | **C** | 4/11 | σ_c = 8.33 km/s (10⁴ K) is L*'s origin | **OVERSTATED** | 6.84 dex joint miss |

**Total: 16 defects in 50 claims (32.0 %).** Referee's rubric: A = exact + load-bearing claim
BACKED; B = exact with one overstated corollary; C = status right, framing or one number
wrong; D = load-bearing claim wrong; F = answer wrong.

## 1. The four answers, and the strongest objection to each

### 1.1 κ = 1/2 from the horizon — grade C, load-bearing verdict WRONG

**The objection.** The horizon argument is a normalisation: one equation in two unknowns.
With `a0 = κc√(Gρ_Λ)` and `H_Λ² = Λc²/3`, `a0/(cH_Λ) = κ√(3/8π) = 2κ/Z`,
`Z = 2√(8π/3) = 5.788810`. Setting that to `1/Z` *is* κ = 1/2; it cannot be evidence for it.
Every horizon count produces `g ∈ {2^a π^b}` and `κ = (Z/2)/g`; κ = 1/2 needs `g = Z`, not a
count. The nearest ladder member is `Z/4π = 0.460659`, 7.868 % away; the specified strain
principle gives `4√(π/3) = 4.093307`, 8.1866× away; the class theorem (κ² ∈ ℚ·π^odd)
excludes 1/2 for every integer-π count. The sentence has the arrow backwards.

**A52 ran the number down, and it is worse than "not derived".** In a declared grammar of
430461 expressions (119108 distinct), **401 expressions hit the target at the 1 % level**,
against a random-target mean of 401.05 (z = −0.003): 11.5776 sits at the **54th percentile**.
The pool's best hit is `π(π + e/5)` at 5.9e-6 — 6137× closer than the best physical
candidate. So the number is not merely underived; it is *unremarkable*. And the one
independent measurement is `κ = 0.417 ± 0.095` (A52, CFG493 via A15): 1/2 is 0.874σ away,
the 1/12 reading 0.688σ, the alt footing 1.971σ. **The data cannot separate 1/2 from 1/12
(0.185σ apart); a 3σ separation needs σ_κ ≈ 0.0059, a 16.2× improvement** (A52 K11 quotes
22.5× — the difference is the N↔κ Jacobian; neither closes the gap).

**Independent re-derivation.** `Z = 5.788810036` ✓; `2Z = 11.577620073` ✓;
`1/Z = 0.1727470747` ✓; `a0 = c²√(Λ/32π) = 9.354173e-11` ✓; `κ = Z/12 = 0.482400836`,
deviation **3.520 %** ✓ — "1/12 of the horizon" read literally is 3.52 % low in κ and
3.648 % low in `g = 2cH/a0`. The BRIEF's two vacuum constants disagree: `a0` from
`ρ_Λ = 5.831e-27` is `9.351151e-11`, **3.2e-4** below the Λ value; the quoted `9.36e-11` is
**6.2e-4** above it. Neither moves a conclusion; both should be labelled.

**Correct statement.** *κ = 1/2 is a choice, exactly equivalent to `L_MOND = 2ℓ₁` and to
`a0 = c²√(Λ/32π)`; the horizon supplies `a0/(cH_Λ) = 2κ/Z`, not the integer n = 1/κ = 2.
No current measurement separates the candidates.* `THEORY.md` §3.6 says this; the failure
mode is the section title and the "1/12" folklore.

### 1.2 The medium and its discriminator — grade C, load-bearing verdict OVERSTATED

**The objection.** The lattice is a representation, not a derivation. The grand-canonical
potential is chosen as `μ(g) = k_BT ln(g/a0) − ε` so that `x = g/a0` — the drive is defined to
reproduce the answer. A2 concedes the general point: any monotone response is
`A(g) = ∫ g/(g+s) dμ(s)`, μ ≥ 0, so "the medium is a lattice" has no content unless `N_s` is
predicted, and A2 says it is not. The real theorem is negative: no positive mixture gives
n = 2, because the n=2 response has branch points at `g = ±i a0/2`, off the negative real
axis where every Stieltjes function lives. A57 independently confirms the algebra (q = 2
only, `C = s` exactly, K10–K11) and its parameter count is 3 inputs for 2 targets, excess 1.

**The discriminator fails three ways.** (i) A25's `Δχ²(Q−L) = +157.96` is the *fixed-footing*
number; profiled in `(A, a0)` it is **+17.05**, inside the pre-registered ±25 no-decision band
(collapse 9.265×). (ii) The occupancy-noise shape at SPARC's median 2.4 kpc beam has
`N_s = 9.97e5` and `σ(a0) = 2.9e-4 dex`, **103× below** the 0.03 dex assumed, so the test
needs ~10⁴× more galaxies or 100× better resolution. (iii) The direct fit gives
`z = +0.745 / −1.209`. A53, the lane that was to settle the medium, is an **empty directory**.

**Independent re-derivation.** Langmuir residual **0** ✓; `C = s` → 0, `C = a0/2` → 1/2 ✓;
branch points `±i a0/2` ✓; max separation **15.47005 %** (g) / **7.45699 %** (v) ✓; noise
**22.3422**, slope **−1.4999** ✓.

**Correct statement.** *Within a single-scale mass-action lattice with one occupant per site
and capacity = affinity = a0, n = 1 is the unique member; the capacity is matched to the
observed deep limit, not derived; n = 2 is excluded as a positive mixture. No dataset on
disk separates the laws at 3σ (N ≈ 1330–1980).*

### 1.3 The four gates — grade B−, load-bearing verdict OVERSTATED

**The objection.** They are not four gates. Lensing = dynamics, `c_T² = 1` (speed),
`α₁ = α₂ = 0` and stability all follow from P2's structure — one O(ε) lapse source, no
P–curvature coupling, `η = γ`, convex `W(u)`. The only independent input is the P5 posit
`y_t = 66.30`. So the four gates carry **two premises**; one failure of P2 fails all four.
None is testable now: the lensing slip is 2.64e-7 (5.6 decades below a 10 % measurement); the
mode mass is 3.76e-25 eV, **46.8× below** the 1.76e-23 eV bound; `α₁ = 0` holds only for
`r ≪ 17 pc`, and the galactic α₁ is not computed; stability is a consistency condition.

**The α₁ defect.** `α₁ = −8(c₃² + c₁c₄)/(2c₁ − c₁² + c₃²)` is 0/0 at `c₁ = c₃ = c₄ = 0`, the
theory's point, and the limit is path-dependent: along `c₃ = √c₁` it is **−8/3 = −2.6667**.
The code's `if den == 0: alpha1 = 0` is an assertion dressed as a check (A31 §4). With
`c₃ = 0` exactly the physical point is 0, but that is a point value at a discontinuity. A54's
G8 measures the same structure at galactic radii: **α₁ = 0.073–5.194**, O(1), not zero.

**Independent re-derivation.** slip `= (154 km/s/c)² = 2.6388e-7` ✓; `605.96/66.2999 = 9.1397`
✓; `a0/B_E = 2557.377`, `(a0/2)/B_E = 1278.689` ✓ — the BRIEF's 1279 and THEORY's 2557 are
the same quantity for two different laws (factor 1.9995). THEORY §3.5 quotes 2557 with no
note that 1279 is the quadrature's; a reader cannot reconcile them without A4.

**Correct statement.** *One structural premise passes four consistency checks; the
Solar-System check requires the fitted posit y_t = 66.30, which is 46.01 on the alt footing.
`α₁ = α₂ = 0`, `β = 1` are near-source statements (`r ≪ 17 pc`); the galactic α₁ is open.*

### 1.4 The origin of L* — grade C, load-bearing verdict OVERSTATED

**The objection is A56's own.** Its K9 states: *"the medium has no velocity scale: sigma_c is
not its parameter."* Its K20: *"to get 24 pc you must import L* itself."* So the medium
answer and the L* answer are disjoint by the L* lane's own admission. What A56 does establish
is weaker: among the parameter-free combinations it enumerated (6 vacuum lengths, 29 density
lengths, 34 Compton lengths, 1 from `{G,c,ρ_c}`), exactly one lands in [24, 90] pc —
`σ_c²/a0 = 24.025 pc` (K12) — which is the identity inverted. **Uniqueness within a declared
grammar is not an origin.** A57 then tries the joint dynamics and misses by **6.84 dex** on its
printed `L*(κ=0.5) = 1.6584e8 pc` (its report says 7.4 dex; `κ(L*=24 pc) = 0.00259`).

**A correction to my own first pass.** I first read A56 K22's alt ratio 1.112 as an 11.2 %
failure; A56 is right that 9.153 km/s is the **μ = 1.00** thermal width (9.085 km/s) to 0.7 %.
The hit survives both footings — but only by selecting μ = 1.22 (canonical) or 1.00 (alt), a
discrete dial rather than a prediction. And 10⁴ K is the *warm* phase; the cold phase (50–100 K)
gives `L* = 0.12–0.24 pc`, 100–200× smaller. The number is also convention-dependent by √2:
with `K = 8πG`, `L*(K) = 16.988 pc = λ_P`.

**Independent re-derivation.** `L* = 24.025 pc` ✓; `R_core = 53.37 pc` ✓;
`L*/L_MOND = 7.7206e-10` (log −9.1124) ✓; window 180 pc at `f_c = 0.25` ✓; alt footing
19.900 pc (−17.2 %) ✓.

**Correct statement.** *L* is a free stiffness scale, measured through γ and bounded to
[24, 180] pc; `L* = σ_c²/a0` is the unique parameter-free combination inside the window, not
an origin; the 10⁴ K agreement is a coincidence consistent with, not evidence for, a thermal
origin.*

## 2. Cross-lane consistency (A51/A53/A54 have scripts, no report; A50/A55 nothing)

**Four of six pairs carry a quantified conflict**; two are unobservable.

| pair | verdict | size of the conflict |
|---|---|---|
| A50 horizon ↔ A51 κ | **CIRCULAR + BLIND** | 20.8 % spread; 0.185σ resolution |
| A53 medium ↔ A56 L* | **DISJOINT** | 6.84 dex joint miss |
| A51 κ ↔ A54 gates | **CONFLICT — misattributed, see erratum** | 30.6 % (y_t 66.30 → 46.01) — but 46.01 is κ = 0.604's image, i.e. the **Ω_Λ = 1 footing**, NOT A51's measured κ = 0.371 |

> **ERRATUM (2026-10-22, coordinator): the "A51 κ ↔ A54 gates" row is misattributed.** The row's own
> magnitude — `y_t` 66.30 → 46.01 — is A4's *alternative footing* (a₀ = 1.132×10⁻¹⁰, κ = 0.605), not
> A51's measured κ = 0.371. Fed through `I(y_t) = 8π/κ²`: κ = 0.371 gives **y_t = 118.97**, which is
> **INSIDE** [60,140]; κ = 0.605 gives 45.82, which is outside. The section body below states this
> correctly ("on its own alt footing"); only this summary row conflates the two. So the falsifier fires
> on the `Ω_Λ = 1` footing — which A51's measurement disfavours at 1.97σ — and **not** on the measured κ.
> The band [60,140] on y_t maps exactly to κ ∈ [0.3415, 0.5265]; the measurement's central value sits
> inside it and only its lower 1σ tail (κ = 0.252, y_t = 255) leaves the band.
| A51 κ ↔ A56 L* | **CONFLICT** | 17.2 % (24.03 → 19.90 pc) |
| A54 gates ↔ A56 L* | unobservable | 0.17σ |
| A53 medium ↔ A54 gates | unobservable | 103× below beam |

**(a) Horizon → κ.** The horizon normalisation assumes κ = 1/2, and the one measurement that
could break the circle is too coarse: `0.417 ± 0.095` puts 1/2 at 0.874σ and the alt footing at
1.971σ, and separates 1/2 from 1/12 by **0.185σ**. The 20.8 % footing spread the theory
carries is therefore invisible to data — the pair is consistent *and* uninformative.

**(b) Medium → L*.** A56 K9 says the medium has no velocity scale, so σ_c cannot be its
parameter; A57's joint construction gives `L* = 1.6584e8 pc` at κ = 1/2, **6.84 dex** from
24 pc. The medium does not produce L*; the two answers are independent postulates that happen
to share `a0`.

**(c) κ → gates.** `y_t` is the image of κ under `I(y_t) = 8π/κ²`: 66.30 at κ = 0.5, 45.98 at
κ = 0.604 (A4's exact integral 46.0148), **−30.6 %**. The Solar margin is insensitive
(planets sit at `y ~ 10⁷`), but `THEORY.md` §5 makes "turn-off outside [60, 140]" a falsifier —
and **46.01 is outside [60, 140]**. The theory's own falsifier fires on its own alt footing.

**(d) κ → L*.** `L* ∝ 1/a0`, so the alt footing moves 24.03 → 19.90 pc (−17.2 %) at fixed σ_c;
THEORY quotes "24 pc" while carrying two footings.

## 3. Load-bearing checks

| answer | the one claim that decides it | test | result | number |
|---|---|---|---|---|
| Q1 | the horizon *fixes* κ, rather than restating it | solve for κ with the horizon's own count | **WRONG** | g = 5.788810 vs 2π = 6.283185 (gap 0.4944) |
| Q2 | the law is the stationary state of a real lattice | is the drive independent of the answer? | **OVERSTATED** | μ(g) chosen; +17.05 < 25 |
| Q3 | four gates are four independent passes | count premises | **OVERSTATED** | 2 premises / 4 gates; 0/4 testable |
| Q4 | σ_c = 8.33 km/s is L*'s origin | does any joint dynamics produce both? | **OVERSTATED** | 6.84 dex miss; μ = 1.22 vs 1.00 |

Only Q1 is outright **WRONG**; Q2–Q4 state conditional or matching results as closures — the
A31 pattern, surviving into the four answers.

## 4. Verdict, and what the correct statements are

| answer | grade | may be written as | may **not** be written as |
|---|---|---|---|
| κ from the horizon | **C** | `NO-GO`: κ = 1/2 is a choice; `a0/(cH_Λ) = 2κ/Z` | "the horizon derives κ = 1/2" / "1/12 exactly" |
| medium + discriminator | **C** | `CONDITIONAL(single-scale lattice)`; n=2 excluded as a mixture | "the medium is derived" / "SPARC decides n" |
| four gates | **B−** | four consistency checks of one premise, one with a fitted posit | "four independent gates pass" / "α₁ = α₂ = 0 exactly" |
| L* origin | **C** | `OPEN`: unique parameter-free combination in [24, 180] pc | "L* = σ_c²/a0 is derived from the 10⁴ K medium" |

**The one wrong answer, corrected.** *κ = 1/2 is not derived from the horizon. The exact
content is `a0/(cH_Λ) = 2κ/Z` with `Z = 2√(8π/3)`; setting it to `1/Z` is the definition of
κ = 1/2, and `L_MOND = 2ℓ₁` is the same definition. No integer-π horizon count produces
n = 2, and the one measurement (0.417 ± 0.095) cannot separate 1/2 from the 1/12 reading.*

## 5. Checks

`a58_checks.py`, 36/36 PASS, exit 0, 0.4 s, stdlib + numpy + sympy, deterministic, no network.
Groups: K1–K11 κ/horizon, K12–K19 medium, K20–K25 gates, K26–K31 L*, K32–K34 ledger/cross-lane,
K35–K36 A52/A57. For defect checks PASS means the defect is confirmed (the `name` field says
which). Mutations `z`/`r32`/`kappa` break 4/3/1 checks.

Self-inflicted lesson: K14 first passed with **0 roots** — `sympy.solve` returns `[]` for
`g²+a²=0` with `g` positive, and `all(...)` over an empty list is vacuously true. It now uses
`sp.roots` and asserts two roots with Re = 0, |Im| = a. A check that cannot fail is no check.

## 6. What this does not do

1. **It does not certify A50–A57** — three of eight had a report; A50, A53, A55 had nothing.
2. **The 50-claim ledger is my selection**, not a census; 32.0 % is indicative, using A31's method.
3. **It does not re-fit SPARC.** A7/A25 are taken as reported; their conflict is internal.
4. **The α₁ test is a counterexample to the limit**, not a computation at `c₃ ≠ 0`; and it does
   not decide whether κ = 1/2 is true, only that the horizon does not derive it.

## 7. Next

1. **Do not write the four answers in.** A50, A53 and A55 have nothing; A51 and A54 have no
   report. The brief's bar (CLOSED-DERIVED / CLOSED-NO-GO / DECIDABLE) is met by none of them.
2. Freeze what is earned: Q1 `NO-GO`, Q2 `CONDITIONAL`, Q3 `B−` with the y_t posit named, Q4 `OPEN`.
3. Make the turn-off falsifier footing-relative (`y_t/y_t(κ) ∈ [0.9, 1.1]`), or the theory
   falsifies itself at 46.01.
4. Replace "1/12" in BRIEF §1 with `2Z = 11.5776`, or mark 12 as a 3.52 % approximation.
5. State `K` once and propagate: the choice moves L* by √2 and makes the `8πG` value `λ_P`.