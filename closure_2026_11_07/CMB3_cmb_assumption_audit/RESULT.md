# CMB3: assumption audit of "the CMB acoustic peaks require a cold component of ~5.4 x the baryons at z ~ 1100"

CMB3 RESULT (criteria e46081b7a9): A1 law inert at z 1100: frozen line BREAKS POSSIBLE / BREAKS POSSIBLE (the
baryons-only potential gradients sit in the law's deep regime), and by CMB2 D4 (cd1c7c35a3, cited) the law's response
FOLLOWS the fluid and leaves H3/H2 at the baryons-only value at a0(z) = a0, so the inference HOLDS / HOLDS; open corner
a0(z 1100) >= 30 x today. A2 lensing: HOLDS / HOLDS (unlensed theory: survival S 0.993 / 0.993, R +1.9 / +1.5 %;
fixed cold lensing template x A_phi free in [0, 15]: S 0.877 / 0.862, R +0.0 / +0.0 %). A3 recombination, N_eff, YHe: HOLDS
/ HOLDS (S 0.892 / 0.871, R -2.2 / -2.2 %); no framework-native change of the photon-baryon coupling (CMB2 D3). A4 initial
conditions (n_s to 2.5, running free): HOLDS / HOLDS (S 0.901 / 0.895, R +0.4 / +0.3 %). A5 "the stuff that sits still at
z 1100 is the stuff that flattens rotation curves": BREAKS / BREAKS (reading; the record's own F2 data). A6 nuisance block
widened, priors off: HOLDS / HOLDS (S 0.751 / 0.736) but nuisance-sensitive (DeltaMB -25 / -26 %, more than a few
percent). KA all to 0, MUTATE M1 and M2 bite on both footings. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

Footings graded separately, never pooled (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2; values read canonical / alt).
Background: F1A's B2 footing rule; no LCDM parameter as a premise. Cold dark energy, the cold component; no particle.

## Files

- FROZEN_CRITERIA.md (local 93abdeff84, origin e46081b7a9), committed and pushed alone, before any script or number.
- cmb3.py: imports F1A's likelihood classes, footing rule and CAMB call (f1a.py, read only); nothing from QX3/QX10/QX15.
- run_all.sh: every step in sequence, one process at a time. Peak RSS 0.71 GB. Nothing downloaded.
- cmb3_grade.py writes cmb3.json / cmb3.out and cmb3_MUTATE.json / cmb3_MUTATE.out. parts/ holds every fit.
- cmb3_aphi_check.py: a post-run check of the A2-T cold fits (reported, not graded).

## Known answers and MUTATE (all PASS)

| control | canonical | alt |
|---|---|---|
| KA-1: PA chi2 at F1A's four stored best fits, d vs stored (cold, MB) | -8e-9, -1e-8 | -5e-6, -3e-9 |
| KA-1: DeltaMB replay | +172,915.6 | +166,674.4 |
| KA-2: 60 NM evaluations from the cold best fit: dchi2, dR | 0.0, 0.0 (R 5.410) | 0.0, 0.0 (R 5.412) |
| KA-3: lensing path, own C_L^phiphi x 1 vs F1A | -4e-8 | -5e-6 |
| KA-4: N_eff/YHe, running and nuisance-box code switched off | 0.0 each | 0.0 each |
| M1: omega_b doubled on the MB fit: d(H1/H2) | +0.207 | +0.220 |
| M1: H3/H2 (mutant / MB / cold) | 0.632 / 0.629 / 0.982 | 0.686 / 0.672 / 0.982 |
| M1: chi2 vs cold | +188,261 | +181,784 |
| M2: dchi2 at the cold fit, A_phi 3 / N_eff 5 / running +0.10 | +2,595 / +45,192 / +350 | +2,630 / +45,189 / +348 |

- M1 means: doubling the baryons moves the odd/even ratio by 21-22 %. It does not restore the third peak: H3/H2 stays
  0.63-0.69 against the cold model's 0.98. So the baryon density alone cannot do the cold component's job.
- M2 means: every switch the audit uses reaches the likelihood.

## The assumptions, one by one

Survival S = DeltaMB under the relaxed assumption / F1A's DeltaMB. R = omega_d / omega_b at the relaxed cold fit.
Labels per the frozen lines:
- HOLDS: S >= 0.5 and |dR| <= 10 %.
- BENDS: S < 0.5, or |dR| in (10, 25] %.
- BREAKS: DeltaMB <= 25, or |dR| > 25 %.

### A1. The a0 law is inert at z ~ 1100 (GR linear theory governs the acoustic era)

| | canonical | alt |
|---|---|---|
| background c H(z 1100) / a0 | 1.65e5 | 1.37e5 |
| y = g / a0 per ln k, cold fit, k 0.02 / 0.05 / 0.1 / 0.2 / 0.3 | 12.1 / 11.0 / 9.9 / 7.5 / 6.1 | 10.1 / 9.1 / 8.2 / 6.2 / 5.1 |
| nu - 1 there (simple form) | 0.08-0.14 | 0.09-0.17 |
| y per ln k, baryons-only fit | 1.12 / 0.44 / 0.13 / 0.008 / 2e-4 | 0.96 / 0.38 / 0.11 / 0.004 / 1e-5 |
| largest nu - 1, baryons-only | 72 | 324 |
| needed to stand in for the cold component: nu >= 1 + R, i.e. y <= | 0.0288 | 0.0288 |
| frozen line | **BREAKS POSSIBLE** | **BREAKS POSSIBLE** |
| reported: total rms gradient y_rms, cold / baryons-only | 20.6 / 3.3 | 17.1 / 2.9 |
| reported: nu - 1 at y_rms, cold / baryons-only | 0.046 / 0.25 | 0.055 / 0.27 |

- The Weyl gradient comes from CAMB's z 1100 transfer. The large-scale check reads |Phi_W| = 0.62 per unit curvature
  (expected about 3/5).
- The frozen text rounded the needed y to 0.027; the exact value is 1/(n(n-1)) = 0.0288. No label depends on the
  difference.

**What the law does there (CMB2 D4, cited, not redone).** In a baryons-only universe the potential gradients at
recombination are inside the law's range, so "the law is inert" is not something the framework can assume. But the
size of the response is not the question; its timing is.
- D4's phantom correlates with the acoustic potential at r 0.992-0.997. It FOLLOWS the fluid.
- Its still part is at most 0.05 of the dust's at k 0.1, and at most 0.28 / 0.30 at k 0.03 (at x 100).
- At a0(z) = a0, as the record's constant rho_DE gives, the law's peak ratio H3/H2 is 1.008. Baryons-only gives 1.006,
  and the dust gives 1.447.
- So the law does not replace the cold component, and the inference HOLDS.

My total-gradient reading points the same way. It is reported, not graded, and was added after the freeze.
- The law's argument is the total gradient, and that gradient is set by long modes: half of g^2 comes from k < 0.010.
- Against that outside field of about 3 a0, the short modes see nu - 1 of about 0.25, not 72-324.

**Open corner (CMB2's, restated).** At a0(z 1100) >= 30 x today, the following phantom raises the odd peaks: H3/H2 is
1.08 at x 30 and 1.30 / 1.36 at x 100. It also moves the first peak away from the data. This needs rho_DE 900-1e4 x
today's at z 1100, and no history in the record gives that.

**A question the record should put to itself.** Even the fitted cold model is not law-inert at recombination: nu - 1
is 0.05 at its total gradient and 0.08-0.17 per band. F1A's fit sets nu = 1. If the law acts on linear perturbations at
all, the cold fit omits a few-percent following boost of the potential. That boost would shift R at the few-percent
level, not remove the requirement. It is named here and not computed.

### A2. The theory is lensed with the model's own late-time lensing potential

| | canonical | alt |
|---|---|---|
| A2-U unlensed theory: chi2 cold / MB | 5,051.2 / 176,736.9 | 5,050.6 / 170,503.7 |
| DeltaMB, S, R (dR) | +171,685.7, 0.993, 5.511 (+1.9 %) | +165,453.1, 0.993, 5.495 (+1.5 %) |
| A2-T fixed cold template x A_phi: chi2 cold / MB | 3,740.16 / 155,311.4 | 3,740.30 / 147,326.0 |
| A_phi at best fit, cold / MB | 1.00 / 9.50 | 1.00 / 9.45 |
| DeltaMB, S, R (dR) | +151,571.2, 0.877, 5.410 (0.0 %) | +143,585.7, 0.862, 5.412 (0.0 %) |
| label | **HOLDS** | **HOLDS** |

- **The data need lensing.** Unlensed theory costs the cold fit +1,311 chi2. With the template free, the data pick
  A_phi = 1.00: the post-run scan gives +2.8 / +2.4 at 0.95 / 1.05, and +11 / +10 at 0.9 / 1.1. So the smoothing in
  PR4 + ACT is the amount a universe with the cold component predicts, to about 3 %.
- **Lensing cannot make up the peaks.** Baryons-only takes A_phi about 9.5 (inside WG2's 0.31-14 range for the law on
  the web), and recovers only 12-14 % of the deficit.
- **The amount does not move.** Removing lensing moves R by under 2 %; freeing it moves R by 0.
- **Not on disk.** A delensed data vector: CamSpec NPIPE and ACT DR6 CMB-only are lensed.

### A3. Standard recombination, Thomson coupling, N_eff

| | canonical | alt |
|---|---|---|
| N_eff [1, 6] and YHe [0.10, 0.40] free: chi2 cold / MB | 3,728.41 / 158,043.8 | 3,728.53 / 148,867.8 |
| cold fit N_eff, YHe | 2.93, 0.226 | 2.96, 0.226 |
| MB fit N_eff, YHe | 1.00 (edge), 0.349 | 1.00 (edge), 0.283 |
| DeltaMB, S, R (dR) | +154,315.4, 0.892, 5.290 (-2.2 %) | +145,139.3, 0.871, 5.295 (-2.2 %) |
| label | **HOLDS** | **HOLDS** |

- **Photon-baryon coupling: no framework-native change exists** (CMB2 D3, cd1c7c35a3).
  - The matter action has no khronon field.
  - Tight coupling gives c_s^2 = 1/(3(1+R)) exactly.
  - r_s changes only through H(z), which is already in B2.
  - The only slip is |Phi - Psi| / Psi <= 7e-4.
- **NOT TESTABLE in this apparatus:** varying alpha or m_e, or extra ionising photons. Each needs a recombination-code
  change, and the action has no source for any of them.

### A4. Adiabatic, Gaussian, nearly scale-invariant initial conditions

| | canonical | alt |
|---|---|---|
| n_s [0.5, 2.5], running [-0.5, 0.5], ln A_s [0, 5]: chi2 cold / MB | 3,736.63 / 159,469.1 | 3,736.50 / 152,944.1 |
| cold n_s, running | 0.967, +0.014 | 0.967, +0.014 |
| MB n_s, running | 1.387, -0.50 (edge) | 1.469, -0.50 (edge) |
| DeltaMB, S, R (dR) | +155,732.5, 0.901, 5.429 (+0.4 %) | +149,207.6, 0.895, 5.428 (+0.3 %) |
| label | **HOLDS** | **HOLDS** |

**Degeneracy direction** (chi2 Hessian at the A4 cold fit; nuisances profiled):
- sigma_R is 0.022 / 0.017 (0.3-0.4 %).
- corr(omega_d, running) is -0.25 / -0.34, and dR / d(running) is +1.37 / +1.24, consistent across footings. A running
  of +0.08 would move R by 10 %; the data allow about +-0.01.
- corr(omega_d, n_s) is -0.11 / -0.19.
- dR / dn_s is not robust: -0.02 / +1.17, disagreeing in sign between footings. The ln A_s-tau block is ill-conditioned
  without L < 30 data (canonical sigma_tau 0.09 vs alt 0.014), so it is not quoted as a direction.
- From F1A, with no new fit: n_s fixed at 0.95 (B1, which also fixes H0 and omega_b) gives R 5.83 (+8 %).
- **NOT TESTABLE here:** isocurvature or non-Gaussian initial conditions.

### A5. The identification "the component that sits still at z 1100 is the stuff that makes rotation curves flat"

**BREAKS / BREAKS, by the record's own data (reading; no run).** F1 says that a cold, pressureless component with
omega_d / omega_b = 5.41 sat in the potential wells at z 1100. It says nothing about where that component is today.
The record's measurements say it is not in galaxies:
- **SPARC** allows f <= 0.33 / 0.19 of the baryons on the exact field (DEDUCTION F2).
- **KiDS isolated lenses**, with kSZ-measured gas (KX1, e9c7e42786): the posterior excess of data over the law is
  -0.21 / +0.02 / +0.01 / +0.05 dex canonical and -0.25 / -0.02 / -0.03 / +0.01 alt across its bins, against the 5.4x
  that a cosmic share would add.
- **Cluster members vs field early types** (NC3, 774ead884f): no member residue (D +0.011 / +0.012 dex).
- **Bound hosts** together hold 0.9 % / 0.8 % of the component (NC4 capacity C 0.0091 / 0.0078). Even if every
  baryon sat in a host, the bound would be <= 75 % / 68 %.

The standard picture's step "the CMB's cold component = the galaxy halo mass" is therefore not an inference from the
CMB. It is an extra identification, and it is the one the record's data contradict (F2 against F1).

### A6. Foreground / calibration templates and priors

| | canonical | alt |
|---|---|---|
| Step 1, wide box at F1A's fits: dchi2 cold / MB | -0.9 / -34,384 | -0.9 / -35,439 |
| Step 2, MB refit with the wide box: chi2 MB | 133,583.9 | 126,450.5 |
| DeltaMB (cold at its step-1 value), S | +129,844.7, 0.751 | +122,711.1, 0.736 |
| nuisance sensitivity | -25 % | -26 % |
| label | **HOLDS** (S >= 0.5), nuisance-sensitive | **HOLDS**, nuisance-sensitive |

- **The cold fit does not care:** -0.9 chi2.
- **Baryons-only is helped by about 25 %, through unphysical nuisances.** Its Planck TT foreground amplitudes go to the
  1000 muK^2 edge (the cold fit uses 6-19), EE calibration to the 1.5 edge, and ACT P_act to 1.31. A still wider box
  would help it more. This bends the size of DeltaMB, not its sign, and needs foregrounds 50-100x the cold fit's.

## Disclosed

- **Fits.** ONE warm Nelder-Mead start each (250 evaluations cold, 300 MB), against F1A's two starts.
  - Each Delta is an upper bound for its fit.
  - The baryons-only fits sit on bracket edges (n_s 1.3; running -0.5; N_eff 1.0; omega_b 0.0215 or 0.0230; tau; the
    A6 nuisances).
  - Wider brackets could lower chi2_MB further. The smallest DeltaMB under any single relaxation is +122,711 (A6 alt),
    about 5e3 times the 25 line.
- **The relaxations were fitted one at a time, not jointly.** A non-rigorous sum of the separate reductions (canonical:
  0.7 + 12.3 + 10.8 + 9.9 + 24.9 %) is about 59 %, which would still leave about 7e4. No joint fit was frozen, and this
  sum is not graded.
- **A2-T cold fits.** Neither cold fit moved off the F1A point in 250 evaluations. The post-run A_phi scan (+2-3 chi2
  at +-5 %) confirms that point is the minimum.
- **A4 alt cold fit.** It took 19,574 s of wall time because the machine was under load (same 250 evaluations, RSS
  0.59 GB).
- **A1** uses the simple-form nu and the rms gradient per ln k, from one CAMB transfer (no realisation). The still /
  follows sign is CMB2's.
- **A6 cold** is not refit, as frozen; its refit gain is bounded by the step-1 -0.9.
- **Siblings, cited, not redone.**
  - CMB1 (ee9150ee36): lane NO VERDICT by its own M1 rule; its block C reads CLUSTERING PINNED on both footings
    (neither equality alone nor baryon density alone stands in).
  - CMB2 (cd1c7c35a3): NO on both footings; its F1A G4 starting-state finding (-25.14 / -90.28 vs -26.8 / -108.1)
    leaves F1A's no-go standing.

## Plain answer to the owner's question

**Solid.** The inference "the acoustic peaks need a cold, pressureless component of about 5.4 x the baryons at
z 1100" survives every assumption the record can test:
- GR on the acoustic era. The law is not inert in a baryons-only universe, but its response follows the fluid and
  leaves the peak ratios at the baryons-only values, unless a0 was at least 30x larger at z 1100.
- Lensing. The data ask for exactly the smoothing a cold-component universe gives. Lensing freedom recovers at most
  14 %.
- Recombination, N_eff and helium. The action has no route to the photon-baryon coupling.
- Initial-spectrum shape. Tilt and running recover 10 %, and move R by 0.4 %.
- The foreground and calibration block. It recovers 25 %, only with unphysical foregrounds.

In every case baryons-only stays more than 1.2e5 chi2 worse, and the amount moves by at most 2.2 %.

**The record's own to question.**
- The fitted cold model itself sets nu = 1 at recombination, although its own gradients sit at y 6-20, where the law
  would add a few percent. That is a consistency debt of the framework, at the few-percent level in R, not a hole in
  the requirement.
- The a0(z 1100) >= 30 corner, which no record history reaches.

**Wrong by the record's numbers: only A5.** That is the identification of the CMB's cold component with the mass that
flattens rotation curves. The CMB measures how much cold, pressureless stuff gravitated at z 1100. The record's SPARC,
KiDS, NC3 and NC4 numbers say that today it is not in galaxies and that bound hosts hold about 1 % of it. So the
peak-ratio inference holds, and the only broken assumption is A5.

Kappa = 1/2 FITTED; not theory closed.
