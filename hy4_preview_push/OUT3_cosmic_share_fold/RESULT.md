# OUT-3 (COSMIC-SHARE FOLD) RESULT — where 5.41 M_b sits, and one construction attempted

2026-11-12. Lane: **derive the footing AMOUNT**. Criteria `PREREGISTER.md` written and committed to
disk **before** any script ran. Test lane, quarantined: adopts nothing, relabels nothing, registers
nothing. Footings graded separately, NEVER pooled. **kappa = 1/2 FITTED; not theory closed.**

## Label

**AMOUNT NOT DERIVED (UNAVAILABLE).**

The construction was attempted, it is well posed, and it returns a number. The number is wrong by
18.5 band-widths, it drifts 1.81 dex with galaxy mass and 1.82 dex with epoch, and the physical
reading of the brief is not even available: the charge the fold front can deliver is 0.196 of the
share the condition demands. Both pre-registered readings fail.

---

# PART A — where 5.41 M_b sits in the record

Read from `closure_2026_11_10/R541_why_the_cold_share/NOTE.md`,
`argon_push/ARGON01_modulus_kappa_2026-10-15/REPORT.md`,
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/` and
`fable_independent_2026/kappa_slot_2026/`.

**Answer: 5.41 is FITTED FREE. Nothing outside form B pins it.**

1. **It is a CMB fit, not a consequence.** `R = Omega_d/Omega_b = 5.410 (canonical) / 5.412 (alt)` is
   the best fit of `closure_2026_11_07/F1A_primary_cmb_audit/RESULT.md:22` on Planck PR4 + ACT DR6
   spectra. R541 §1: no posterior on R is stated anywhere in the record; the 0.065 width used
   everywhere is a **Planck 2018 fallback**, not F1A's own error. The standard value refitted on the
   framework's background is 5.364 ± 0.065 — 5.41 is 0.9 % above it, 0.7 of that width.
2. **In the action it is an integration constant.** R541 §2: in action (A) with P = 0 the stiffness
   term and W(0) both vanish, the shift symmetry `tau -> tau + const` gives the first integral
   `a^3 mu_K^2 (Q-1)/K = C`, and on shell `R = C/rho_b0`. "No equation of the action sets it."
   `a_0` enters only through W and `kappa` only through `a_0`, and W ≡ 0 in the background — so the
   amount and the law have **no parameter in common**.
3. **ARGON01 closes the structural escape, and the same obstruction is what makes the amount free.**
   `argon_push/ARGON01_modulus_kappa_2026-10-15/REPORT.md` N1: in the extended action the primitive's
   constant enters no Euler–Lagrange equation except as `C'(λ)`, so `C_0` is a free integration
   constant of every solution — "the C zero-mode is structural, not a parameter choice." Only a
   global/sequestering (k02-class) structure can reduce the observables' rank, and ARGON01's k02
   scale check is 65× to 1.6e7× short of the vacuum offset the framework needs. This is a κ-side
   theorem, but it is the same zero-mode that leaves the amount free.
4. **The κ campaign never touched it.** The 848-row
   `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/` ledger contains **no row mentioning 5.41,
   the cold share, or the amount** (grepped). `KAPPA_CLOSURE_2026-11-03.md` §1: "no derivation of ½
   on record." The κ campaign and the amount campaign are disjoint; nothing in CFG894 pins the
   amount. `fable_independent_2026/kappa_slot_2026/KS00_INDEX.md` records the single live slot as
   SLOT-NOT-LIVE, with three κ candidates inside 2σ and no amount statement at all.
5. **Five mechanism lanes were already run and all failed.** R541 §8: R541A (clock–matter coupling),
   R541C (made in inflation), R541D (baryon-current cogenesis), R541E (B−L variant) are **EXCLUDED**
   on both footings; R541B (early symmetry breaking) is **TRADES** — it moves the number into a
   potential's height and needs two or three new constants plus two initial conditions. "Nothing
   tested fixes 5.41."
6. **Nothing outside the framework pins it either.** R541 §5: in Skordis–Zlosnik, Blanchet–Skordis,
   mimetic dust and Mukohyama the dust amount is a free integration constant; the nearest mechanism
   (Chamseddine–Mukhanov, arXiv:2601.05931) still rests on a chosen coupling with no link to
   baryons; the one particle model that reproduces 5.36 needs an axion, which the framework's rules
   exclude. R541 §4: a 1,084 + 2,856 + 615-value formula hunt over the framework's own constants
   finds **chance-level** counts (p 0.52–0.90) — the nearest hits (4+√2 = 5.414, π√3 = 5.441) are
   produced by nothing in the framework.
7. **The one independent anchor is a measurement, not a pin.** X-COP clusters, Newtonian:
   `M_dark/M_bar = 5.73 ± 0.68` (R541 §6; HIS1's edge 4.94 [4.30, 6.11]). It is **reported and never
   pooled**. It shows the same number in a second place; it does not explain or fix it.
8. **And the amount is now under independent pressure.** AMT1 §4: ONE1's brackets **reject**
   `X = 5.41` for the halo at **+4.85 / +4.93 sigma** while accepting 53.64 and 59.5. Form B's halo
   needs 59.5 M_b at the KiDS windows — 11.0× the entire cosmic budget — and LFS1 closes the exit
   that it could be assembled later.

**Part A bottom line: 5.41 is a fitted initial condition of the field, refitted on the framework's
own background, and pinned by no equation inside or outside form B. The framework has two fitted
numbers, 1/2 and 5.41.**

---

# PART B — the construction

## The condition, as pre-registered

**(S)** At the fold front, where the law's static halo is first established, the halo it becomes must
enclose exactly the **cosmic share of the enclosed baryons**:

    M_c(<R_fold(t))  =  R_cosmic * M_b ,     R_cosmic = Omega_d/Omega_b = 5.410 / 5.412

with the record's own exact halo `M_c(<r) = M_b X(x)`, `X = (sqrt(1+4x^2) − 1)/2`, `x = r/r_M`,
`r_M = sqrt(G M_b/a_0)`. Exact inversion (G0, sympy, and independently certified in
`FINAL-14_lean_amount`'s `x_b(R)^2 = R(1+R)`): `X = R ⟺ x^2 = R(1+R)`, so with **no** deep-regime
approximation

    a_0^S = G M_b R_cosmic (1 + R_cosmic) / R_fold^2 ,      kappa_S = a_0^S / (c sqrt(G rho_Lambda)).

`R_fold` is FLD1's measured front (committed runs, origin bce6d61451, N = 2400, z_i = 10, law on),
so (S) is one equation in one unknown.

## The number

log M_b = 10.45, z = 0, both footings:

| footing | R_fold(0) measured | R_cosmic | a_0^S | kappa_S | a_0^S / a_0(footing) |
|---|---|---|---|---|---|
| canonical | 139.305 kpc | 5.410 | 7.020e-12 m/s^2 | **3.752e-02** | 0.0750 |
| alt | 139.288 kpc | 5.412 | 7.026e-12 m/s^2 | **3.756e-02** | 0.0621 |

**kappa_S = 3.75e-02, i.e. 13.3× below the fitted 1/2 — a miss of 1.125 dex.**

This reproduces FINAL18's mutation arm MU2 (`kappa_M = 0.0375`, REJECTED) to three digits. That is
the expected outcome of a declared replication and is recorded as a cross-check, not as a finding.

**What the condition physically asks for:** it wants the fold front at **38.15 kpc** where FLD1
measures 139.3 kpc (AMT1 §3: 38.15 kpc is where the canonical halo has spent the whole cosmic
budget). Since `a_0^S ∝ R_fold^{-2}`, that factor 3.65 in radius is the factor 13.3 in `a_0`.

## The error bar (G4, pre-registered budget, computed)

    kappa_S = 3.752e-02   (+0.174 / -0.174 dex)   ->   [2.51e-02, 5.60e-02]

| term | shift (dex) |
|---|---|
| `R_cosmic ± 0.065` (Planck 2018 fallback, R541 part E) | 0.0096 |
| `R_fold` at-rest vs Hubble flow, measured ratio **1.2210** from FLD1's own `rest_*` runs | **0.1734** |
| `R_fold` start redshift 20/30 (+1.4 %) | 0.0121 |
| `R_fold` shell N 1200 → 4800 (+0.07 %) | 0.0006 |
| `rho_Lambda ± 1.5 %` (Planck) | 0.0032 |
| **total (quadrature on the log)** | **0.174** |

The bar is dominated by one thing: whether the front is read at rest or in the Hubble flow, a
convention in FLD1's own output worth a factor 1.22 in `R_fold` and hence 1.49 in `a_0`.

**The bar does not rescue the number.** The miss is 1.125 dex against a 0.174 dex bar: **6.5
bar-widths**, and the top of the bar (5.60e-02) is still 8.9× below 0.5.

## The gates

| gate | result | the number |
|---|---|---|
| **G0** exact inversion | **PASS** | `X(1+X) − x^2 → 0`; `4R(1+R)+1 = (2R+1)^2`; `X(sqrt(R(1+R))) − R → 0` |
| **G1** `abs(kappa_S − 1/2) <= 0.025` | **FAIL** | miss 0.4625 (can) / 0.4624 (alt) = **18.5× the band** |
| **G2** mass span `<= 0.0411 dex` | **FAIL** | **1.811 dex** canonical, 1.812 alt (44.1×); `kappa_S` = 1.90e-03 at log M_b 6.5 → 1.23e-01 at 12 |
| **G3** epoch drift `<= 0.0411 dex` | **FAIL** | **1.820 dex** canonical, 1.823 alt (z = 0 → 4); `kappa_S` 3.75e-02 → 2.48e+00 |
| **G4** error bar | reported | ± 0.174 dex; 6.5 bar-widths short |
| **G5** can the front deliver `R_cosmic`? | **FAIL** | delivered 1.059 M_b (turned) / 0.555 (crossed) vs 5.410 demanded → **0.196** at every mass, both footings |

**G2's shape is the structural kill.** `R_fold ∝ M_b^{1/3}` (FLD1) while the demanded share is a
constant, so `kappa_S ∝ M_b^{1/3}` exactly. No single `a_0` satisfies (S) for two galaxies of
different mass, let alone one galaxy at two epochs. This is a spread of *different numbers*, not an
uncertainty on one number, so by the pre-registered §3 rule it is a falsification and no error bar
can absorb it.

**G5 is the deeper kill, and it is why the label is UNAVAILABLE rather than merely FALSIFIED.**
Under reading (i) of the brief (the halo's own enclosed charge equals the cosmic share) the
condition is *falsified* — G1/G2/G3. Under reading (ii) (the charge the clock **carries across** the
front equals the cosmic share) it is not available at all: FINAL3's (H) says settling rearranges cold
charge and does not create it, and FLD1 delivers 1.059 M_b. The condition demands 5.410 M_b cross a
front that can carry 0.196 of it. (S) then cannot be posed, not merely gotten wrong.

## MUTATE — three false twins, all REJECTED

| arm | claim | verdict |
|---|---|---|
| MU1 | the cosmic-share settle-down derives kappa = 1/2 | **REJECTED** by G1: band miss 0.4625 vs 0.025 (18.5×) |
| MU2 | the miss is inside the error bar | **REJECTED** by the §3 rule: bar 0.174 dex, miss 1.125 dex, and G2's 1.811 dex is a spread of different numbers |
| MU3 | use the X-COP value 5.73 ± 0.68 instead | **REJECTED**: `kappa_S = 4.17e-02`, still 18.3× the band; X-COP is reported and never pooled (R541 §6) |

---

## Disclosures (all adverse)

1. **Order disclosure (the big one).** The pre-registration was written **after** reading FINAL18,
   R541, AMT1 and the two neighbouring OUT-3 lanes, so the expected number (0.0375) was known
   beforehand. This lane is a **replication with an added error bar and an added conservation gate**,
   not a blind test. Its new content is G4 and G5 only.
2. **The pre-registered error-bar expectation was wrong, and I correct it here.** `PREREGISTER.md` §4
   predicted ± 0.10 dex. Measured: ± 0.174 dex. Cause: I inherited OUT3 arm A's sensitivity, where
   `kappa ∝ R_fold^{-4}`; in this lane `kappa_S ∝ R_fold^{-2}`, and I measured the at-rest/Hubble
   ratio directly from FLD1's committed `rest_*` runs (1.2210) instead of assuming OUT3's +22.3 %.
   The gates do not rest on the bar; the reported value is 0.174 dex.
3. **The label ordering is my own and is arguable.** G5's failure takes the label to UNAVAILABLE.
   Under reading (i) the same run is FALSIFIED (G1/G2/G3). Both are true; the stricter one is
   reported because the pre-registered rule puts the G5 case in its own branch.
4. **The fold inputs are FLD1's physics**: baryons as a softened point mass ramped on over 1 Gyr,
   radial shells, no discs, no mergers, no feedback, law-dominated limit. Non-spherical infall could
   reach further; by how much is not computed. `R_fold` is a model quantity, not a measurement, and
   its 22 % at-rest/Hubble-flow convention is the single largest term in the bar.
5. **`R_cosmic` has no F1A posterior.** The 0.065 is a Planck 2018 fallback (R541 part E). It
   contributes only 0.0096 dex, so this does not affect any verdict.
6. **`rho_Lambda` differs slightly from the neighbouring lanes** (Omega_L = 0.6847 here vs 0.685 in
   OUT3), giving `kappa` at the canonical footing = 0.500299 rather than 0.499889. Inside the
   footing's own tolerance; touches nothing.
7. **Not `OUT3_scale_free_boundary`** (that lane matched formation normalisations to vacuum values in
   three unit slots and recorded share-vs-cosmic-share as INADMISSIBLE unit-mismatched; it imposed
   no radius condition) and **not `OUT-3_kappa_equality_fixed`** (its settle-down is
   `rho_c(r_sd) = rho_Lambda`, a cosmic-vacuum boundary, and it found K ∈ [3/2, 3], so 1/2 is out of
   range). This lane's boundary is the **baryon** share at FLD1's fold.

## What this adds

- 5.41 is **fitted free and pinned by nothing outside form B** — now stated with the κ campaign's
  silence (0 of 848 ledger rows) and ARGON01's structural zero-mode added to R541's five failed
  lanes and its chance-level formula hunt.
- The one remaining formation door named in the brief — *the settle-down at the fold front where the
  enclosed cold charge equals the cosmic share* — is **closed on both readings**: falsified as an
  equation for `a_0` (18.5× the band, 1.81 dex of mass drift, 1.82 dex of epoch drift) and
  unavailable as a physical statement (the front carries 0.196 of the share it is asked to carry).
- The number it forces, for the record: **`a_0 = 7.02e-12 m/s^2` (canonical), `kappa = 3.75e-02`,
  +0.174/−0.174 dex** — 13.3× below the footing, 6.5 bar-widths outside the band.

**Standing: kappa = 1/2 FITTED; 5.41 FITTED; not theory closed. This lane adopts nothing.**

## Files

`PREREGISTER.md`, `out3csf.py`, `out3csf.out`, `out3csf.json`, `RESULT.md` (this file).
