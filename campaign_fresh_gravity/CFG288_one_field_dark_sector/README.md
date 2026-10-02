# CFG288: one field for the dark sector (background = dark energy, clumps = the cold component), and seeding at recombination

The owner asked two things. Can ONE field do both jobs, with its smooth background as the dark energy (w = -1, density rho_Lambda, the same rho_Lambda that sets a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED) and its clumps as the cold component (Omega_c h^2 = 0.120)? And could the cold component be "seeded" as a byproduct of recombination (z ~ 1100)?

The criteria were frozen first, in `FROZEN_CRITERIA.md` (commit 140c8542d, sha256 ed0e1442...; every output prints it). Paths are relative to the repository root. **The cold mass is still required.** No dark-matter particle species is added. The best construction is a classical field whose quanta would be light bosons: the dark-energy field doing a second job. kappa = 1/2 is FITTED.

## Bottom line

- **Behaviour: yes, on the wave-field road.** Take a linear complex field with V = rho_Lambda + m^2 |Phi|^2 and m >= 2e-20 eV (declared). It passes every behaviour gate: background, dust-like perturbations, onset, stream crossing, small-scale power, mergers, stability and gravitational waves. Its vacuum value is the dark energy and its oscillation is the cold component. This is FL1's order parameter with V_min identified with rho_Lambda; it is not new physics.
- **The amount: no.** Neither road fixes Omega_c h^2.
  - Theorem A1: dust present before z_eq needs a potential height of at least 1.5e10 rho_Lambda. At m = 2e-20 eV it needs about 1e22 rho_Lambda, and a misalignment amplitude phi_i = 0.0147 Mbar_Pl (3.6e16 GeV).
  - So the field needs a second, independent scale. The dark energy is then a residual at the minimum, tuned to <= 6.6e-11 of the height.
  - rho_Lambda never enters the dust's dynamics (dV'/d rho_Lambda = 0; rho_Lambda / rho_total = 3.5e-27 at onset).
  - "One field" is therefore a shared label, not a tie between the two halves.
- **Seeding at recombination: excluded, twice.**
  - **Energy.** No reservoir at z = 1100 can supply rho_c(1100) = 5.4 rho_b. Hydrogen binding falls short by about 5e8, all the CMB photons by 4.4x, all radiation by 2.6x, and the FIRAS-allowed photon energy by 7e4.
  - **CMB (CAMB).** Dark energy converting to dust at z = 1100 changes the lensed TT spectrum by ~300% over the first three peaks, raises the H1/H3 peak ratio by 21%, and moves the BAO sound horizon by +21%.
  - Seeding must happen at z >~ 1e5. On the frozen rule, z <= 1e4 is EXCLUDED and 1e5 and 1e6 are UNDECIDED. A labelled post-hoc differential comparison finds 1e6 indistinguishable from LambdaCDM.

## Per-gate table (`cfg288_construction_gates.py`)

| gate | Road W: linear complex wave field (quanta = light bosons) | Road S: seeded shift charge (ghost-condensate P(X)) |
|---|---|---|
| G-BG | PASS: w = -1 exactly (0.9 sigma from -1.028 +- 0.031); a0 tie -0.057% (canonical) / -0.059% (alt) | PASS: same tie, P(X0) = -rho_Lambda |
| G-DUST | PASS-CONDITIONAL (m >= 2e-20 eV declared): c_s^2(1100, 0.3/Mpc) = 2.8e-15, forest c_s = 1.3e-3 km/s, \|w(1100)\| <= 4.3e-18, c_vis^2 = 0 | PASS-CONDITIONAL: needs M >= 4.24 eV. The single-scale tie (M^4 <= 1e3 rho_Lambda) FAILS: c_s^2(1100) = 1.3e5 |
| G-ONSET | PASS (timing): z_on = 3.8e7 >= 1e7; \|w(3400)\| <= 1.9e-16 | PASS-CONDITIONAL: needs M >= 3.3 keV to stay dust-like back to z = 1e7 |
| G-AMOUNT | **AMOUNT FREE**: needs phi_i = 1.47e-2 Mbar_Pl at 2e-20 eV, plus m itself | **AMOUNT FREE**: needs the charge C, i.e. the amount itself. Seeding needs a reservoir >= 3.9e14 rho_Lambda at z_s = 1e5 |
| G-STREAM | PASS: wave L1 = 0.0008 / 0.0024 vs the fluid control's 1.03 / 1.35. The self-gravitating version is INHERITED from L374 | **FAIL**: the single-valued gradient flow is this road's dust limit (L1 = 1.03 / 1.35). L374: the EFT breaks at the first crossing |
| G-PK | PASS-CONDITIONAL: HBG gives 1 - T^2(0.2 h/Mpc) = 2e-16 and T^2(10 h/Mpc) = 1.000 at 2e-20 eV. L383's 2-5e-19 eV floor reported | PASS-CONDITIONAL: k_J(1100) = 2.2 h/Mpc at M = 4.24 eV; needs M >= 4.04 eV |
| G-MERGER | PASS: c_q(200 kpc) = 1.5e-3 km/s; superposes; lambda = 0 | **FAIL**: a single-valued flow cannot pass through itself |
| G-STAB/GW | PASS: no ghost (Hamiltonian eigenvalues 1, m^2); c_s^2 >= 0; c_T = 1 derived (tensor equation with the field present). Kernel invisibility INHERITED (L353, MS1, FL1, FL2 all clean). Solar-system dark mass 4e-15 Msun | PASS-CONDITIONAL: needs C > 0 and the declared k^4 term; c_T = 1 ((box phi)^2 adds no h_t^2 / h_z^2 term) |

Main run: 21/25 checks pass. The 4 load-bearing failures are findings: both G-AMOUNT rows, and road S's G-STREAM and G-MERGER. In MUTATE1 (hbar/m = 0.02) the wave match fails (L1 = 0.43 / 0.67), so rc = 1 as required.

## The seeding table (`cfg288_seeding_camb.py`; CAMB 1.6.6, reference = Planck-2018 best-fit LambdaCDM)

S_TT is the maximum of |dC_l/C_l| over the lensed TT spectrum, 30 <= l <= 1000. Comparison (a) holds H0 fixed; (b) matches theta*. Per the frozen rule, (b) decides.

| z_seed | pre-seed vacuum fraction | S_TT (a) | S_TT (b) | H0 (b) | H1/H3 change | z_eq | verdict |
|---|---|---|---|---|---|---|---|
| 1100 (recombination) | 0.62 | 2.99 | no theta*-match in [40, 120] | -- | +21.2% | 1133 | **EXCLUDED** (decided on (a)) |
| 3400 | 0.41 | 1.32 | 1.11 | 53.95 | -32.7% | 3187 | **EXCLUDED** |
| 1e4 | 0.21 | 0.214 | 0.217 | 65.10 | -12.5% | 3402.5 | **EXCLUDED** |
| 1e5 | 0.026 | 1.09e-3 | 1.10e-3 | 67.361 | -0.11% | 3402.5 | UNDECIDED |
| 1e6 | 2.7e-3 | 8.7e-4 | 8.7e-4 | 67.361 | -0.08% | 3402.5 | UNDECIDED (INDISTINGUISHABLE blocked: controls failed) |
| 1e7 (control) | 2.7e-4 | 8.8e-4 | 8.7e-4 | 67.361 | -0.08% | 3402.5 | control FAILED (see disclosure 1) |

- Energy is conserved, so before seeding the fluid holds the vacuum energy rho_c(a_s) = 0.386 (1+z_s)^3 rho_Lambda. At z_s = 1100 that is 5e8 rho_Lambda: a separate vacuum, not the rho_Lambda that sets a0.
- Cosmic-variance proxy Delta chi^2_CV (reported, approximate): 3.2e5, 2.8e5, 6.6e4, 1.4 and 1.05 for the five main rows.
- The reported rows (transition widths 0.02 and 0.2, w_e = -0.99, unlensed spectra) change no reading.
- Main run: 4/9 checks pass. The load-bearing failures are C-FLUID, C-EARLY and SEED-1100 (a finding). In MUTATE1 the control is seeded at 1100 and C-EARLY fails, as required.

**Post-hoc instrument check (`cfg288_seeding_posthoc_instrument.py`, outputs `_POSTHOC`, written after the controls failed; no frozen verdict changed).**
- The differential statistics are: unlensed seeded spectra vs CDM, and lensed seeded spectra vs the fluid baseline.
- Readings: 1e5 is UNDECIDED (1.11e-3 / 1.19e-3: a real effect, from the 2.6% pre-seed vacuum fraction); 1e6 is INDISTINGUISHABLE (5.6e-4 / 1.3e-5); 1e7 is INDISTINGUISHABLE (5.6e-4 / 1.7e-7).
- The post-hoc z_req analogue is 1e6. 3/3 checks pass.

**BAO row (POST-FREEZE, added at the coordinator's relay of the owner's "what about BAO"; no frozen verdict depends on it).**
- Reference r_d = 147.10 Mpc. Shifts Delta r_d / r_d: +20.8% (seeding at 1100), +4.11% (3400), +0.645% (1e4), -1.9e-6 (1e5, 1e6, 1e7).
- At fixed late-time expansion, D_M/r_d and D_H/r_d at z = 0.5, 1.0 and 2.3 move by -17.2%, -3.95%, -0.64% and about 0 (the late-time distances change by <= 3e-9).
- Against the declared precision scales (Planck r_d ~0.2%; DESI DR2 ~0.3-1% per bin), BAO alone also exclude seeding at z <= 1e4 and allow z >= 1e5.
- BAO do not give closure. They confirm that the cold component must be in place before z ~ 1e5, and they measure its amount; they do not derive it from rho_Lambda.
- The framework's own law under an evolving dark energy, a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)), using the DESI DR2 CPL triples committed in `campaign_fresh_gravity/CFG6_a0z_branches.py`:

| fit | z = 0.4 | z = 1 | z = 2 |
|---|---|---|---|
| DESY5 | 1.062 | 1.009 | 0.862 |
| Pantheon+ | 1.035 | 0.989 | 0.874 |
| Union3 | 1.089 | 1.031 | 0.854 |

  The one-field construction here has w = -1, so its a0 is flat. An evolving dark energy would need a rolling field in place of the vacuum term, which is outside this lane.

## Stage A theorems (`cfg288_stageA_theorems.py`)

- **A1 (potential road): PROVED.**
  - For a healthy kinetic term, d rho/dt = -3H phidot^2 exactly, and a |phi|^(2n) minimum averages to <w> = (n-1)/(n+1). So rho_0 <= Delta V a_d^3.
  - The minimum Delta V / rho_Lambda: 5.2e8 (dust from z = 1100), 1.5e10 (3400), 3.9e11, 3.9e14, 3.9e17 and 3.9e20 (1e4 to 1e7). The exact radiation-era value at m = 2e-20 eV is 1.0e22 (Delta V^(1/4) = 711 eV).
  - So a potential with one scale tied to rho_Lambda cannot supply the dust: a second scale is needed, and the dark energy is a tuned residual.
  - Control: the Bessel solution matches to 2e-12. MUTATE1 (a ghost) breaks monotonicity (d rho/dt = +3H phidot^2; rho grows by 6e21), so only a ghost escapes A1, and G-STAB forbids it.
- **A2 (shift-charge road): PROVED.**
  - The charge is an integration constant: d(a^3 P_X phidot)/dt = 0, and a solution exists for every C > 0. rho_d = sqrt(2 X0) C a^-3 is independent of rho_Lambda and M^4.
  - c_s^2 = rho_d / (4 M^4) and w = c_s^2/2. Coldness needs M >= 4.24 eV (from z = 1100) or 9.9 eV (from 3400). The single-scale tie fails: c_s^2(1100) = 1.3e5 at M^4 = 1e3 rho_Lambda, and 1.3e8 at M^4 = rho_Lambda.
  - A seeding event must break the shift symmetry and inject >= rho_c(z_s). At recombination every reservoir fails (numbers above).
- **A3 (mass scale): NOT derived.**
  - The window is [2e-20 eV, 37 eV] (21 decades).
  - Inside it: m_q = Mbar_Pl^(1-q) (hbar H_Lambda)^q for q = 1/2 (1.7e-3 eV), 2/3 (1.5e-13 eV) and 3/4 (1.4e-18 eV), and rho_Lambda^(1/4) (2.2 meV). These are non-unique numerology.
  - The framework's distinctive scale misses: hbar H_Lambda by 13.2 decades, and hbar a0 / c^3 by 14.0 decades (canonical) and 13.9 decades (alt).
- Main run: 8/15 checks pass. The 7 load-bearing failures are all findings: A2.4, five A2.5 reservoirs, and A3.

## Disclosures (read before citing)

1. **The frozen lensed-spectrum controls FAILED.** CAMB's DarkEnergyFluid carrying Lambda + dust (cs2 = 0) differs from real CDM by 0.40% (TT) and 0.56% (EE) over 2 <= l <= 2500.
   - The cause is located post hoc. The unlensed spectra agree to 5.6e-4 (TT) and 6e-5 (EE), but the fluid under-clusters at late times: C_L^phiphi is 8% low at L = 500 with AccuracyBoost 2, and 17% low with boost 1. It is a numerical limitation of the instrument, not seeding physics.
   - Consequence under the frozen rule: no row can be INDISTINGUISHABLE, and the frozen z_req is undefined. G-ONSET (ii) is therefore scored against 1e7, the largest value the frozen definition can return.
   - The EXCLUDED rows are robust: their deviations of 22-300% exceed the 0.4-0.6% instrument error by 40x or more, in both the lensed and the unlensed statistics.
2. The BAO and a0(z) block was added to `cfg288_seeding_camb.py` after the freeze, at the coordinator's request. Re-running left the frozen part of the output byte-identical (checked).
3. Stage A's quartic row (reported only) first averaged over 2.5 cycles (<w> = 0.307). It now averages over complete cycles (0.332). Separately, the ghost MUTATE integrates only to x = 30, because the ghost overflows beyond that.
4. Stage B's W2 control first used a fixed-window average. That cannot resolve an O(1/x^2) <w>, because amplitude drift leaks in at O(1/x). It was replaced by the exact EOM identity plus a least-squares fit; the fitted coefficient matches theory to 1.0000. A label in the road-S G-PK verdict was also corrected (text only).
5. The misalignment amplitudes ignore g*(T) evolution (declared). They serve only to quote "needs X".
6. No Planck binned data are on disk. The 1% / 0.1% scale and Delta chi^2_CV are declared and approximate; this is not a likelihood fit.
7. The construction script also prints the post-hoc z_req analogue, read from the `_POSTHOC` json, for display only. The run order is stage A, seeding, post-hoc, construction.
8. Hand estimates (section 11 of the criteria): HE1-HE3 and HE5-HE9 held. HE4 held on every row except the control, which I expected to pass and which failed (disclosure 1).

## What this lane cannot say

- Nothing about the galaxy-scale double count, Gap 1/2 ownership, satellites or cluster cores.
- The wave road at linear order is CDM (the GDM theorem), so its behaviour passes are not a new prediction.
- The CAMB model is a uniform, energy-conserving conversion; other seeding microphysics is not covered.
- No closure claim, no claim that the data prefer the framework, and kappa stays FITTED.

## Files and runs (each script ends with "N/M checks pass")

- `cfg288_stageA_theorems.py` (2 s) and `MUTATE=1` -> `cfg288_stageA_theorems[_MUTATE1].out` / `_results.json`
- `cfg288_seeding_camb.py` (55 s) and `MUTATE=1` -> `cfg288_seeding_camb[_MUTATE1].out` / `_results.json`
- `cfg288_seeding_posthoc_instrument.py` (105 s) -> `cfg288_seeding_posthoc_instrument_POSTHOC.out` / `_results.json`
- `cfg288_construction_gates.py` (4 s) and `MUTATE=1` -> `cfg288_construction_gates[_MUTATE1].out` / `_results.json`

Run from the repository root: `python3 campaign_fresh_gravity/CFG288_one_field_dark_sector/<script>`, with `MUTATE=1` for the controls. Main runs exit with rc 1 because their load-bearing findings fail, as listed above (house convention, as in CFG286).
