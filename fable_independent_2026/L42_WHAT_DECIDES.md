# L42 — what actually decides between this framework and ΛCDM?

`L42_what_decides.py` + `L42_what_decides.out` — **22 checks, 13 PASS, 9 FAIL. All seven controls
PASS.** Every FAIL is an obstruction established, not a defect of the script.

Four lanes tonight each removed a source of discriminating power (L28 rotation curves, L24 cluster
lensing as a separate probe, L21 the external-field branch of pairs, L32 the coefficient). This lane
asks what is left, forecasts each survivor honestly against real instruments and real sample sizes,
names the systematic that will decide each one, and ranks them.

**The honest headline: very little discriminates, and what does mostly already has.** Three tests are
already decisive at ≥3σ with data in hand and all three point against the framework. Exactly **one**
undecided test is decisive at 3σ with an existing, scheduled facility — Gaia DR4's Arm A — and
confirming it would confirm the arm that fails the Cassini quadrupole by 4–5×. Nine of the fourteen
registered tests never reach 3σ at their best reachable precision, and four of those cannot at **any**
precision from **any** facility.

---

## 0 · The organising principle this lane found first

A test has discriminating power against ΛCDM only if **ΛCDM predicts something different**. Six of
the ledger's flagged strengths and future tests predict *exactly* what ΛCDM + GR predicts:

| ledger row | prediction | ΛCDM/GR |
|---|---|---|
| **D1** α_M = 0, c_T = 1 from LISA/ET standard sirens — *"the strongest prediction in the corpus"* | 0, 1 exactly | 0, 1 exactly |
| A6 GW speed, GW170817 | c_T = 1 | c_T = 1 |
| A4 γ_PPN | 1 | 1 |
| A3 CMB power spectrum at 0.01σ | matched | matched by construction |
| A7 / D3 no Solar-System MOND signal | none | none |
| D2 binary-pulsar decay | GR quadrupole | GR quadrupole |

These separate this framework from **other modified-gravity theories**, which is real and worth
saying. Against ΛCDM their power is **exactly zero at any precision from any facility**, and
`EMPIRICAL_TESTS.md` does not carry that flag. **Check S1 FAILS on this.**

---

## 1 · The ranked table

Ordered by discriminating power per unit of effort. **power** = separation in σ achievable at the
best reachable precision, capped by the binding systematic (and, for T7, by the least favourable
admissible modelling assumption). **effort**: 0 = data in hand · 1 = data scheduled or public, no new
observations · 2 = no new hardware, needs an external team · 3 = large approved-facility programme ·
4 = a sample nobody has · 5 = a facility nobody is building. **score** = power / (1 + effort).

| # | test | framework predicts | ΛCDM predicts | 3σ needs | achieved | power | effort | score | status | binding systematic (size) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **T9** structure formation with no cold dark matter — P(k), σ₈ | σ₈ ≤ 0.648, rms \|log R\| ≥ 0.94 dex over 0.1–1 h/Mpc at **any** \|K₂\| | σ₈ = 0.810, R(k) = 1 | σ ≤ 0.054 | 0.010 | **16.2** | 0 | 16.2 | **(a)** | none observational — a **missing calculation**: the nonlinear top-down fragmentation loophole is uncomputed, not excluded, and the linear result was for the separately-dead thermal-relic sector. ⚠️ decisive against every *computed* variant, not yet against the class |
| 2 | **T5** cluster residual vs the cosmic dark-to-baryon share | M_resid/M_bar = 0 after its own kernel | Ω_dm/Ω_b = 5.43, fixed by CMB + BBN, universal to 12% | σ ≤ 1.03 M_b | 0.21 | **15.0** | 0 | 15.0 | **(a)** | hydrostatic mass bias *b*. L18 measured it: the Newtonian ratio moves 5.73 → 9.04 over b ∈ [0, 0.33], i.e. the systematic **strengthens** the residual. It cannot rescue |
| 3 | **T4** cluster weak-lensing ΔΣ log-slope (L24's new quantity) | +0.531 ± 0.058 (can) / +0.536 (alt) **shallower** — the phantom is a near-uniform sheet | the measured NFW/Einasto slope | σ ≤ 0.177 | 0.058 | **9.2** | 0 | 9.2 | **(a)** | 5 clusters, per-cluster mass errors 20–60%, miscentering. **Not binding**: control C10 recovers the measured ΔΣ from the measured X-ray profile to a median 1.11, so a 3× error inflation still leaves 3.1σ. Caveat: a lensing-sector slip below ~15% is untested. Not novel — the counterpart of Natarajan & Zhao 2008 |
| 4 | **T1** Gaia DR4 wide binaries, **Arm A** | γ_v ∈ 1.1614–1.1814 (can) / 1.1917–1.2267 (alt) | 1.0000 exactly | σ_tot ≤ 0.0538 | 0.028 | **6.8** | 1 | 3.4 | (b) | σ_sys = 0.020, irreducible in the frozen model (undetected hierarchical/triple companions, the eccentricity law) = 12% of the signal. **Not binding** — the floor-only ceiling is 8.1σ / 9.6σ |
| 5 | **T6** binary galaxies, **isolated branch** | isolated deep-MOND A = 1.802 ± 0.041 (can) / 1.731 (alt); σ_los = 0.60679 (G m a₀)^¼ = 107.7 / 112.9 km/s at any separation | abundance-matched halo A = 0.967 ± 0.024 | σ ≤ 0.278 | 0.048 | **3.5** | 1 | 1.7 | (b) | **isolation depth**, and it is the whole story: 2MRS sees companions only above ~23% of the pair's mass and the amplitude falls 1.99 → 1.51 as isolation deepens — a **0.48 swing against a 0.835 separation, 57% of the signal**. Every published A is an upper limit |
| 6 | **T11** directional external-field effect | AQUAL-class directional signal; kill switch fired once, Â = +2.95, p = 0.029 | exactly zero (as does pure MI) | σ ≤ 0.98 | 1.35 | 2.2 | 1 | 1.1 | (b) | the same contamination/isolation systematics as T1 and T6, and they are **unquantified on this axis** — the 2.2σ hint has no systematic budget at all |
| 7 | **T2** Gaia DR4 wide binaries, **Arm B** (the covariant candidate) | 1.000 < γ_v ≤ 1.0450 (can) / ≤ 1.0300 (alt) — **ceilings** | 1.0000 exactly | σ_tot ≤ 0.015 | 0.028 | 1.6 | 1 | 0.8 | **(c)** | the same σ_sys = 0.020 floor, which **alone** caps the separation from Newton at **2.25σ (can) / 1.50σ (alt) at infinite N**. No sample size suffices |
| 8 | **T7** Coma ultra-diffuse galaxies | EFE prediction; measured dispersions +1.159 dex (can) / +1.112 (alt) above it — factor 14.4 | no prediction violated | σ ≤ 0.386 dex | 0.235 | 2.7 | 3 | 0.7 | (b) | stellar **M/L + IMF at 0.148 dex**, unpropagated by the source paper, inside a 0.227 dex coherent floor that does not average down over eleven galaxies. **And** the dynamical-state assumption, worth 2.2 of the 4.9σ by itself — hence the 2.7σ cap |
| 9 | **T10** a₀(z) from the Rubin/LSST SN stream | R(z=3) = 0.775 on the DESI DR2 posterior; 1.000 if Λ is constant | R = 1.000 | σ ≤ 0.075 | 0.113 | 2.0 | 2 | 0.7 | **(c)** | **the test is not about a₀.** The programme's own preregistration warns z = 3 is a lever arm, not a redshift where calibrated SNe exist. What is measured is whether w = −1 — and a null makes the framework *exactly degenerate* with constant-a₀ MOND and with flat |
| 10 | **T3** deep-MOND BTFR zero point at z ≈ 2.5 | **0.00 dex** on the ρ_Λ tie (−0.09 with DESI w0wa); **−0.576 dex** on the Hubble-horizon tie — ⚠️ see §3 | +0.33 dex (DM14), +0.45 (Duffy08), ~+0.50 (Magneticum) | σ ≤ 0.109 dex | 0.13 registered | 2.5 | 3 | 0.6 | (b) | the **apparent-a₀ drift nuisance**: Magneticum calibrates p = 0.92 and MSA-3D *measures* an apparent p = 1.22 in a real JWST sample, worth **+0.50 to +0.67 dex at z = 2.5 — larger than the 0.33 dex signal**. It is neutralised only by a genuinely deep-MOND, rotation-dominated, lens-controlled target, so the binding item is **target discovery, not telescope time**. Second: lens magnification (two refereed models of the best current object disagree by 2.3× = 0.36 dex) |
| 11 | **T8** s^TX SME boost dipole | \|s^TX\| = 8.68e-10 (can) / 1.048e-9 (alt), sign locked negative | 0 exactly | σ ≤ 2.89e-10 | 1.3e-9 | 0.8 | 2 | 0.3 | (b) | **absorption into the ephemeris global fit** — 94.3% of the template is absorbed at the preregistration's own conservative level, and a real INPOP/DE refit absorbs more, so every quoted sensitivity is an upper limit. Plus the interpretation guard: any preferred-frame MG host gives a comparable s^TX |
| 12 | **T14** SPARC rotation-curve tightness | 0.142 dex at zero parameters/galaxy | **0.085 dex** from a fitted NFW halo carrying ΛCDM's *own* population width; shape channel tied 0.070 vs 0.072 | — no gap | — | **0.0** | 4 | 0.0 | **(c)** | the halo **population width**. Removed as a discriminant by L28; what survives is parsimony and held-out prediction |
| 13 | **T12** α_M, c_T from LISA / Einstein Telescope | 0 and 1 exactly | 0 and 1 exactly | — no gap | — | **0.0** | 5 | 0.0 | **(c)** | not a systematic — a **degeneracy**. Zero power against ΛCDM at any precision from any facility |
| 14 | **T13** the coefficient κ | κ = ½ (fitted; underivable by the candidate action) | ΛCDM has no κ | — no rival | 8.0% total | **0.0** | 5 | 0.0 | **(c)** | the H₀-convention systematic (3.8% on a 7.1% statistical error). Nothing in [0.40, 0.66] rejectable at 3σ; **27 simple candidates already inside the band** |

**Status letters.** (a) already achieved · (b) achievable with an existing or approved facility and a
stated sample size · (c) not achievable. Both a₀ footings carried throughout (9.3619e-11 / 1.1279e-10
m s⁻²); the alt footing is quoted in the .out for every row.

**Facilities and sample sizes, stated.** T1: Gaia DR4, ESA release ~Dec 2026, frozen N = 30,000 (3σ
would need only 4,342). T3: JWST NIRSpec IFU G235H/F170LP (1.66–3.17 µm; Hα + [O III] in one setting
for 2.32 < z < 3.83) then ALMA Band 3 CO(3–2) (84–116 GHz ⇒ 1.98 < z < 3.12) — **both instruments
exist and operate, and the committed 21-object ledger contains no object that passes the gates**.
T6: no new observations — DESI DR1 (~13 million public extragalactic redshifts) against 2MRS
(~45,000, K < 11.75). T7: ~10 objects × ~30 hr of 8–10 m spectroscopy (DF44 alone took 33.3 hr of
Keck/KCWI) plus imaging for tidal state. T8: no new hardware, but a factor 4.5 on the published
combined multi-planet fit (−0.2 ± 1.3)e-9 (Hees et al. 2016) — and it requires an **external
ephemeris team** to run the frozen template.

---

## 2 · The DR4 crux — the sharpest thing in this lane

The two registered arms are not on the same footing with respect to the Solar System. **Arm A** is
the kernel taken as strict AQUAL modified gravity with no coherence length, and gate G01 (two
independent solvers agreeing to 0.05%) has it **failing the Cassini quadrupole by 4–5×**. **Arm B**
passes the static Solar-System gates precisely *because* it carries a coherence length at or above the
Cassini floor — and that same length is what lowers the boost from A's band to B's ceiling.

So the question is not which arm wins. It is: **is there any γ_v that both kills Newton at 3σ and is
consistent with a version of the framework the Solar System permits?**

| footing | Newton dead at | Arm B still alive up to | window | P(landing there \| truth **at** Arm B's ceiling, its best case) |
|---|---|---|---|---|
| canonical | γ_v ≥ 1.0840 | γ_v ≤ 1.1290 | 0.045 = 1.61 σ_tot | **8.0%** |
| alt | γ_v ≥ 1.0840 | γ_v ≤ 1.1140 | 0.030 = 1.07 σ_tot | **2.6%** |

- **X2 FAILS.** Arm B cannot be separated from Newton at 3σ at **any** sample size: σ_sys = 0.020
  caps it at 2.25σ (can) / 1.50σ (alt) at infinite N.
- **X3 FAILS, and it is a correctable arithmetic slip in the registered document.** Amendment 11(e)
  says confirming Arm B at 3σ_tot "needs σ_tot ≤ 0.015 (about four times the frozen N at unchanged
  systematics, or DR5)". Four times the frozen N gives σ_fit = 0.0095 and **σ_tot = 0.0221 — 1.5×
  the stated requirement**, because σ_tot ≥ σ_sys = 0.020 by construction. **No N reaches 0.015.**
  The systematic itself must be reduced, and the amendment does not say so. *(Reported here only —
  the preregistration is append-only and frozen; an amendment needs the owner's explicit go.)*
- **X4 FAILS, by design and stated against interest in the amendment itself.** A Newtonian DR4 result
  falsifies Arm A at ≥5.8σ_tot and leaves Arm B — the arm the Solar System permits — untouched.
- **X1 PASSES.** The window is narrow and unlikely.

**Consequence, and it is the deliverable's core:** DR4 cannot return a result that both confirms the
framework and is consistent with Cassini, except in an ~8% (canonical) / ~3% (alt) corner.

---

## 3 · Registered predictions that are conditional — ⚠️ read before quoting

### ⚠️ P1 FAILS — PAPER7's Δ_BTFR = 0.00 dex is conditional on an unstated posit

`PAPER7_a0z_decisive_measurement_2026.tex` registers the framework's z = 2.5 prediction as **0.00 dex**
(−0.09 with DESI dark energy), from a₀ ∝ √ρ_Λ. The repository's own
`prep_2026/a0z_crossscale/desitter_unruh_horizon_fork_2026.py` states **verbatim that which horizon
sources a₀ "is a POSIT"** and carries a second reading — a₀(z)/a₀(0) = H(z)/H₀, the Hubble/apparent
horizon, credited to McCulloch — which at z = 2.5 gives **Δ log a₀ = +0.576 dex**, a BTFR zero point
displaced 0.576 dex the *other* way from ΛCDM's +0.33. **PAPER7 never names that reading.**

- 0.576 dex is **4.4×** PAPER7's own required total uncertainty (0.13 dex) and **1.76×** the ΛCDM
  separation the measurement is designed to resolve.
- **The serious part.** PAPER7's scoring rule says a result inconsistent with both 0.00 and +0.33
  "counts against both". A measurement at −0.58 dex would therefore be scored as **falsifying the
  framework when it is exactly what the framework's other horizon reading predicts**.
- The corpus is internally inconsistent about whether that branch is closed: `STANDING.md` §4 lists
  "a rising a₀ ∝ H(z) with no dark field" among doors shut, while L32's N7 and the fork script both
  still carry it as live. **That inconsistency is precisely why the paper must state the assumption.**
- **Recommended (owner's call, not this lane's):** an append-only note to the PAPER7 record stating
  which horizon the registered 0.00 dex assumes, and that the alternative reading predicts −0.576 dex.

### ⚠️ P2 FAILS — which *G* enters a₀ = κ c √(G ρ_Λ) is unsettled

L29 found that L9's own late-time closure drives ω_Λ down by a factor 0.38–0.54, moving a₀ by
**−38% to −27%** if the G in the law is the local one and **−17% to −5%** if it is the cosmological
F·G₀. Both readings are carried. That is a 27–38% ambiguity in the framework's central formula,
against a 9.47% BTFR floor on κ and DR4's 21% reach. It does not touch a *ratio* like Δ_BTFR, so the
a₀(z) registration is unaffected — but **any registered prediction quoted in absolute a₀ inherits it.**

### ✅ P3 PASSES — and Amendment 11 deserves the credit

Amendment 11 registers Arm B for **both** candidate kernels (ν_RAR 1.0450/1.0300 in force; the
superseded exponential 1.0375/1.0275 for the record, a 0.27 σ_tot spread) and says which is in force.
That is good preregistration practice. **Flagged, not scored:** Arm A's band carries no such dual
number, while L28 independently found the two carriers differ by up to 0.073 dex on SPARC and move
its own margin from 1.20× to 1.06×. A documentation gap of comparable size on the comparable arm.

### One further gap, smaller

PAPER7 registers a **total** 0.13 dex and does not decompose it into the part that averages down over
several objects and the part that does not. That decides whether a second qualifying object helps,
and the paper does not say. This lane's own estimate (0.07 dex coherent: frozen local C₀ plus the
shared M/L and α_CO prescriptions) is **this lane's, not the paper's**, and is flagged as such.

---

## 4 · Verdicts

| check | result |
|---|---|
| D1 — any live test already decisive with data in hand | **PASS** — T4 (9.2σ), T5 (15.0σ), T9 (16.2σ). All three point **against** the framework |
| D2 — any live test decisive with an existing or approved facility | **PASS** — T1 (6.8σ), T6 (3.5σ) |
| D3 — any **undecided** test decisive with an existing or approved facility | **PASS** — T1 only |
| D4 — every test reaches 3σ at some precision | **FAIL** — 9 of 14 do not; **4 cannot at any precision from any facility** (T12, T13, T14, T2) |
| V1 — the framework is falsifiable in practice within five years | **PASS** — Gaia DR4 Arm A, ~Dec 2026, 6.8σ |
| V2 — the version that **passes the Solar System** is falsifiable within five years | **FAIL** — excluding the arm that fails Cassini by 4–5×, no undecided test at effort ≤ 2 reaches 3σ; Arm B is capped at 2.25σ at infinite N |
| V3 — the framework can be **confirmed** at 3σ within five years by a test ΛCDM cannot pass | **FAIL** — the only candidate is Arm A, whose confirmation is internally inconsistent with gate G01 |

**Read plainly: the framework is falsifiable but not confirmable on the current five-year horizon,
and the part of it that survives the Solar System is neither.**

---

## 5 · What to bet on — three sentences

**Bet on Gaia DR4 Arm A, and bet on it now**: 0.1614 against Newton at σ_tot = 0.028 is 5.8σ canonical
/ 6.8σ alt, on a scheduled date with a hash-frozen pipeline and a systematic floor that is not
binding — it is the only forward test in the register that is decisive, cheap and dated, and the whole
programme should be ready to score it the week the data land. **Spend the cheap second bet on
re-cutting the binary-galaxy isolation with DESI's public redshifts**, because the data already exist,
no new observations are needed, and isolation depth — not sample size — is the systematic that
currently caps 57% of that test's discriminating power. **Spend nothing further on the coefficient,
the Rubin a₀(z) stream, standard sirens or the SPARC tightness claim as a discriminant**: four of them
cannot reach 3σ at any precision from any facility, and knowing that is the most useful thing this
lane can hand over.

---

## 6 · For the orchestrator — proposed additions elsewhere (this lane edits nothing)

1. **`EMPIRICAL_TESTS.md`** — add a "shared with ΛCDM" column. Six rows, including D1 ("the strongest
   prediction in the corpus"), predict exactly what ΛCDM + GR predicts and carry zero power in that
   comparison. Recording them as strengths without that flag overstates the ledger.
2. **`FINDINGS.md`** — a short L42 section carrying: the ranked table; the DR4 crux (8.0% / 2.6%
   window); the P1 conditionality flag on PAPER7; and the D4/V2/V3 verdicts.
3. **PAPER7 record (owner's call)** — an append-only note naming the horizon posit and the −0.576 dex
   alternative, so the paper's own "counts against both" rule cannot misfire.
4. **`PREREGISTRATION_DR4.md` (owner's explicit go required)** — Amendment 11(e)'s route to
   σ_tot ≤ 0.015 is arithmetically unreachable at unchanged systematics. Nothing else in the
   preregistration is affected; no registered number moves.
