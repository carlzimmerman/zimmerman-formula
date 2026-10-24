# X23_late_heated_cold: FROZEN CRITERIA (committed alone, before any script or number of this lane)

κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. The cold component ("cold energy",
Ω_c/Ω_b = 5.364) is gravitating field mass, never a particle. No fitted knob. Never "theory closed". Never "the data favour
the framework". Theory frozen as v3s (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8).

## 0. Hypothesis and scope

LHC (late-heated cold energy): the cold sector is cold until z ≈ 2–3, then warms universally to an isothermal sound speed
c_s(z = 0) = c_s,need, **read from X22's JSON** (`step2.per_footing.<f>.cs_need_kms`; 190.0 / 201.3 km/s), never fitted.

**ID collision and overlap (disclosed).** A peer lane `rebuild_2026_10_22/X23_late_heating_graded` (criteria 6ec6b89807,
result 9c54fae62e) already grades X22's window on every X19 class with X22's flat-well profile: hosted dwarfs, clusters by
MGAS500 tercile, groups, SPARC and the MW disc. Before freezing, I re-ran its committed script read-only from a scratch copy
(only its input root patched): `.out` identical line for line and `_results.json` identical apart from timing. Per the
brief's rule ("if an equivalent test exists, reproduce it and say so"), this lane does **not** re-grade those rows. It
adds only what the peer lane does not cover:
1. clusters keyed on **KT** (X21's 106 clusters, terciles and slope), with the cold component in the **real C\* potential**
   (law + baryons + EFE, X2's model) and **mass-conserving fair-share normalisation** at turnaround (not X22's flat-well cap);
2. the forest / σ₈ / CMB lines, read from X22's committed p-scan (p band 3, 4, 5; p = 5 lies between X22's graded 4 and 6).
Hosted dwarfs, groups, SPARC, the MW disc, the heating energy budget and the Bullet sign are reported only.

**Seen before freezing.** X22, X21, X2, X20 (both lanes), X19 READMEs/criteria and the scripts' model sections; X21's KT
tercile values and V1 slope (README and JSON); the peer lane's README and `.out` (its cluster rows: T1/T2/T3 +0.85/+1.01/+1.18
dex canonical at X22's cap). No number of this lane's model exists.

## 1. Step 0 (stop rule; all must pass, else UNDECIDED with no graded number)

- **K0.** With X2's functions exec'd read-only (as X21 does) and X7's committed per-cluster npz, recompute X21's C\* MID sums
  (n_i, d_i) and reproduce, in all 4 cells (2 footings × h 0.672 / 0.686): X21's KT tercile A (`binned.V1.terciles.cells`)
  and the V1 linear slope point estimate b (`tests.V1.cells.<cell>.b`) to ≤ 1e-9 absolute, KT terciles cut at X21's edges.
- **K1.** c_s used equals X22's JSON `cs_need_kms` per footing exactly; X22's p-scan forest classes and R_σ₈ (p = 3, 4, 6)
  are read and printed from X22's JSON.

## 2. The cluster model (derived, not posited)

For each of the 106 KT clusters, each cell, inside the C\* model:
- External field: g(r) = the C\* acceleration of the baryons (X2's `model` recipe: gas shape P, Mb = 1.2 Mg, AQUAL + noclu EFE).
- Isothermal hydrostatic equilibrium, c_s² d ln ρ_c/dr = −g(r) ⇒ ρ_c(r) = ρ_n exp[−∫_{r_ta}^{r} g dr′ / c_s²]
  (test fluid in the law + baryon potential; cold self-gravity left out of the potential, as the brief states, reported below).
- r_ta (physical) = X22's r_ta(M_b) / (1 + z) with M_b = the model's total baryons, and X22's constants (δ_ta 5.55, CFG946).
- **Normalisation (mass-conserving fair share):** M_c(< r_ta) = 5.364 M_b. Profile set to 0 beyond r_ta.
- The cold mass sources AQUAL with the baryons (X6 X-D5) and lenses: the cluster model is X2's `model` with
  M_src = M_b + M_c(<r), everything else unchanged; P_LHC on X2's bins; d_i^LHC = Σ_MID W_ij P_LHC,ij.

## 3. Graded tests (per cell)

- Predicted tercile A_pred(S) = Σ_S d^LHC / Σ_S d (the A the C\* stack would show if LHC were true).
  Z_t = (A_meas − A_pred)/s_meas with X21's tercile A and s (`binned.V1.terciles`).
- Predicted slope b_pred = the noiseless fit of d^LHC = (a + b x) d, x = log10(KT/median) (X21's wls with unit weights);
  Z_slope = (b_meas − b_pred)/s_b with X21's b and s_b (`tests.V1.cells`).
- Amplitude factor F = (A_pred,all − 1)/(A_meas,all − 1) over the 106, A_meas,all = X21 `tests.V1.cells.<cell>.A_sub`.

**Cell class:** PASS iff all |Z_t| ≤ 2 and |Z_slope| ≤ 2. Else WRONG AMPLITUDE iff some |Z_t| > 2 and A_meas − A_pred has
the same sign in all three terciles (state F). Else WRONG KT DEPENDENCE iff |Z_slope| > 2. Else UNDECIDED.
**Lane verdict (frozen classes):** LHC PASSES THE CLUSTER TEST WITH c_s FIXED BY GALAXIES / WRONG AMPLITUDE (factor) /
WRONG KT DEPENDENCE iff all 4 cells share that class; FAILS GALAXIES OR GROUPS iff the peer lane's reproduced output grades
groups or the X22 SPARC line as failing at c_s,need; otherwise UNDECIDED. Each sub-grade is reported.

## 4. Reported only

- Bracket: c_s,eff = σ_KT = (kT/μ m_p)^½, μ = 0.6 (a shock-heated reading), same normalisation.
- Fraction of M_c inside 0.15 Mpc; uncapped cosmic-mean normalisation (ρ_c(r_ta) = Ω_c ρ_crit(z)) as a mass ratio to the fair
  share; cold-to-baryon acceleration ratio at R500 (self-gravity size).
- Forest/σ₈/CMB: X22's p = 3, 4, 6 rows; c_s(z = 1100) = c_s,need a^{p−½} and k_J = aH/c_s there.
- Hosted dwarfs (peer lane + both X20 lanes: `X20_hosted_dwarf_requirement`, `X20_hosted_dwarf_disequilibrium`); a
  prediction of no extra is reported as a **conflict with a measured requirement**.
- Bullet Cluster offset sign (qualitative: a single perfect fluid with c_s ≪ collision speed shocks with the gas).
- Heating energy: (3/2) ρ̄_c c_s² as a fraction of ρ_Λc², and per baryon vs a PROVISIONAL from-memory supernova/AGN
  feedback scale; record action status (X6, X19 step 2, CFG944 Theorem G, CFG741, CFG643) — "no action" if none.

## 5. Checks and MUTATE

- K2: solver — for a Newtonian point mass, the numerical ln ρ equals GM/c_s² (1/r − 1/r_ta) to ≤ 1e-6; with c_s = 1e6 km/s
  the profile is uniform to ≤ 1e-6.
- K3: peak RSS < 1 GB.
- MUTATE (`X23_MUTATE=1`, outputs `*_MUTATE.*`, exit 1): m1 c_s := σ_KT per cluster; m2 KT labels shuffled; m3 hydrostatic
  sign flipped. **K0, K1, K2 must FAIL.**

## 6. Compute

One thread, `nice -n 15`, `PYTHONHASHSEED=0`, < 1 GB, minutes. No download, no `compute_queue/`. README numbers only from
the committed `.out` / `_results.json`.
