# X54_cold_de_exchange: can cold dark energy and dark energy exchange energy?

**The owner's framing.** The cold component is "cold dark energy, paired with dark energy". Cold dark energy is the
gravitating w ≈ 0 clumping field component. It is not matter and not a particle. Do the CMB, DESI DR2 BAO and supernova
data allow, or prefer, an energy exchange Q between cold dark energy (ρ_c) and dark energy (ρ_DE)? And if a₀ tracks
ρ_DE (a₀(z) = κ c √(G ρ_DE(z)), κ = ½ FITTED), does the implied a₀(z) match CFG689's native a₀(z)?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (04200bb449, committed alone first). κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework. ΛCDM is only the name of the external rival. **The cosmological fit contains no a₀.** Footings enter only
the secondary a₀ grade, as absolute a₀ = footing × √X. Every number below comes from `x54_cold_de_exchange.out` /
`_results.json` (refits and per-point χ² in `x54_cold_de_exchange_run1_fits.out` and the JSON `profiles` block).

## Verdict (primary: Q = ξHρ_c, DES-SN5YR): **EXCHANGE EXCLUDED BEYOND ξ ∈ [−0.0035, +0.0011] (95 %)**

Sign convention: ξ > 0 means energy flows DE → cold.

| model × SN set | ξ̂ | Δχ²(ξ = 0 vs ξ̂) | 95 % interval | frozen class | a₀ grade (z 2.33) |
|---|---|---|---|---|---|
| **M-C Q = ξHρ_c, DES-SN5YR** | −0.00122 | 1.08 | [−0.00349, +0.00110] | **EXCLUDED BEYOND** | **CONSISTENT** |
| M-C, Pantheon+ | −0.00133 | 1.25 | [−0.00363, +0.00102] | EXCLUDED BEYOND | CONSISTENT |
| M-C, Union3 | −0.00141 | 1.39 | [−0.00370, +0.00095] | EXCLUDED BEYOND | CONSISTENT |
| M-D Q = ξHρ_DE, DES-SN5YR | +0.110 | 2.76 | [−0.020, > +0.20] | UNDECIDED (not closed) | TENSION |
| M-D, Pantheon+ | +0.099 | 1.94 | [−0.041, > +0.20] | UNDECIDED (not closed) | TENSION |
| M-D, Union3 | +0.117 | 1.86 | [−0.052, > +0.20] | UNDECIDED (not closed) | TENSION |

Post-hoc S1 (reported only; adds ξ = 0.3, seeded from the ξ = 0.2 refit) closes M-D's upper side:
- DES-SN5YR [−0.020, +0.240];
- Pantheon+ [−0.041, +0.236];
- Union3 [−0.052, +0.279].

Read by the frozen rule, all three would be EXCHANGE ALLOWED, but those classes are not credited.

**In words.**
- **Q ∝ ρ_c is pinned to within a few tenths of a percent of zero by every SN set.** No exchange is preferred:
  Δχ² ≤ 1.4, about 1.2σ, with a mild lean to cold → DE.
  - The bound is set by the CMB and BAO jointly. The CMB fixes the cold density at recombination, while BAO + SN fix Ω_m
    today, and ρ_c a³ ∝ a^ξ links the two.
  - At ξ = +0.002 the refit pays +5.2 in the CMB and +2.1 in BAO. At ξ = −0.004 it pays +3.7 and −1.5 (DES-SN5YR rows of
    `run1_fits.out`).
- **Q ∝ ρ_DE leans DE → cold** by Δχ² 1.9–2.8 (1.4–1.7σ), under the 2σ line.
  - Its DE then has a constant intrinsic w = −1 + ξ/3 ≈ −0.963 (DES-SN5YR best). This is the SN sets' known pull toward
    w > −1, and DES-SN5YR pulls hardest.
  - The upper side is not closed on the frozen grid. At ξ = 0.4, CLASS's θ_s shooting fails ("root must be bracketed")
    for all three SN sets. The ξ = 0.6 frozen point was started from ξ = 0 and did not converge. See "Disclosures".

## The produced cold dark energy fraction, against CFG253

F_made = the fraction of today's cold dark energy made by exchange since z = 1090. A negative value means cold dark energy
was lost to DE.

| | best | 95 % ends |
|---|---|---|
| M-C DES-SN5YR | −0.86 % | **−2.47 % / +0.77 %** |
| M-C Pantheon+ | −0.94 % | −2.57 % / +0.71 % |
| M-C Union3 | −0.99 % | −2.62 % / +0.66 % |
| M-D DES-SN5YR | +9.0 % | −1.9 % / ≥ +15.0 % on the frozen grid (S1: +17.4 %) |
| M-D Pantheon+ / Union3 | +8.2 % / +9.6 % | −4.0 % / ≥ +15.0 % (S1 +17.1 %); −5.2 % / ≥ +15.0 % (S1 +19.4 %) |

**What changes relative to CFG253 when a₀ tracks ρ_DE.**
- CFG253's 3 % was a declared convention (its G1), not a likelihood. Its a₀ already tracked ρ_DE.
- The flat-a₀ ingredient in that record is CFG131's 1 % line (|a₀(z)/a₀(0) − 1| < 0.01 for z ≤ 5). That line allowed
  0.5–1.6 % made after recombination. It is a flat-a₀ cap, and it is not used here.
- With a₀ tracking ρ_DE and no flat-a₀ cap, the data alone (CMB + BAO + SN, ω_c and ξ free) give:
  - **Q ∝ ρ_c: at most +0.7 to +0.8 % made (DE → cold), or at most 2.5–2.6 % lost (cold → DE).** This is tighter than
    CFG253's convention on the side the owner's idea needs (DE → cold), by a factor of about 4.
  - **Q ∝ ρ_DE: up to about 15–19 % made.** That is looser than CFG253's 3 %, because this form barely acts before z ≈ 1.
- Neither form makes the bulk of the cold mass. CFG253's reading (A) conclusion stands, now as a likelihood statement.

## a₀(z) against CFG689 (secondary verdict)

√X(z) = a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0) is footing-independent.

| | √X(2.33): best [95 % range] | √X(5) best | a₀(2.33) best, canonical / alt (m/s²) | CFG689 68 % band, flat + θ* (curvature-free) | grade |
|---|---|---|---|---|---|
| M-C DES-SN5YR | 0.9974 [0.9926, 1.0024] | 0.984 | 9.336e-11 / 1.1282e-10 | [0.68, 1.04] ([0.34, 1.21]) | CONSISTENT |
| M-C Pantheon+ | 0.9971 [0.9924, 1.0022] | 0.983 | 9.334e-11 / 1.1280e-10 | [0.68, 1.05] ([0.32, 1.21]) | CONSISTENT |
| M-C Union3 | 0.9970 [0.9922, 1.0021] | 0.982 | 9.332e-11 / 1.1278e-10 | [0.69, 1.07] ([0.42, 1.26]) | CONSISTENT |
| M-D DES-SN5YR | 1.0685 [0.988, 1.128] | 1.104 | 1.0001e-10 / 1.2086e-10 | [0.68, 1.04] | TENSION |
| M-D Pantheon+ | 1.0615 [0.976, 1.128] | 1.093 | 9.936e-11 / 1.2007e-10 | [0.68, 1.05] | TENSION |
| M-D Union3 | 1.0732 [0.969, 1.128] | 1.111 | 1.0045e-10 / 1.2140e-10 | [0.69, 1.07] | TENSION |

- **The CONSISTENT grade for Q ∝ ρ_c is consistency by flatness.** The allowed exchange moves a₀(2.33) by at most 0.8 %.
  It cannot produce CFG689's median shape: √X(2.33) = 0.909 ("a₀(2.33) ≈ 0.91–0.94 of local") is reached by no ξ in any
  95 % interval. The record's mild a₀ decline, if real, needs DE evolution beyond this exchange.
- **For Q ∝ ρ_DE, the preferred direction (DE → cold) makes a₀ rise with z**, by +7 % at z 2.33. That is the opposite sign
  to CFG689's mild decline, and it lies just above the flat + θ* 68 % band. The cold → DE end of the interval gives
  0.97–0.99, inside the band, but still not 0.909.
- **Caveat (frozen).** CFG689's band assumed ρ_m ∝ (1+z)³ (CFG253 ±3 %; brackets B4m/B4p). The grade is a placement,
  not a joint fit.

## w_eff(z) against DESI's w0wa preference

DESI DR2 chains (CMB + BAO + SN; means recomputed in S0-3):
- DES-SN5YR w0 −0.752, wa −0.861;
- Pantheon+ −0.838, −0.617;
- Union3 −0.667, −1.085.

**M-C (DES-SN5YR best ξ = −0.00122).**
- Intrinsic w_DE = −1.0001 / −1.0005 / −1.0012 / −1.0040 at z 0 / 0.5 / 1 / 2: very slightly phantom, as cold → DE
  requires.
- The apparent w that an uncoupled fit would infer is −1.0000 / −0.9994 / −0.9976 / −0.9871, with CPL (w0, wa) =
  (−1.004, +0.018).
- At the 95 % ends the CPL fit is (−1.012, +0.051) and (−0.996, −0.017).
- **Q ∝ ρ_c cannot produce DESI's w0 ≈ −0.75, wa ≈ −0.86.** It stays within about 0.01 of w = −1.

**M-D (DES-SN5YR best ξ = +0.110).**
- Intrinsic w_DE = −1 + ξ/3 = −0.963 at all z.
- The apparent w is −1.0003 / −1.093 / −1.323 at z 0 / 0.5 / 1, and it diverges by z ≈ 2. The apparent fluid
  ρ_c + ρ_DE − ρ_c0 a⁻³ runs to zero there, because cold dark energy made late is "missing" at high z.
- The CPL fit (w0, wa) = (−0.56, −2.23) is dominated by that divergence and is not a fair comparison. Pantheon+ gives
  (−0.61, −1.95) and Union3 (−0.53, −2.43).
- So the sign of wa matches DESI, but the apparent w near z = 0 stays at −1. This exchange does not reproduce DESI's
  w0 > −1 today.

## S8 = σ₈ √(Ω_m/0.3)

| | ξ = 0 | best | 95 % ends |
|---|---|---|---|
| M-C DES-SN5YR | 0.8229 | 0.8313 | 0.8474 (cold → DE end) / 0.8158 |
| M-C Pantheon+ / Union3 | 0.8227 / 0.8223 | 0.8316 / 0.8315 | 0.8474 / 0.8158; 0.8472 / 0.8159 |
| M-D DES-SN5YR | 0.8229 | 0.7976 | 0.8286 / ≤ 0.7797 (S1 end 0.7726) |
| M-D Pantheon+ / Union3 | 0.8227 / 0.8223 | 0.7997 / 0.7966 | 0.8341 / ≤ 0.7799; 0.8364 / ≤ 0.7811 |

- M-C's best fit (cold → DE) raises S8, away from the weak-lensing values.
- M-D's preferred DE → cold direction lowers S8 by about 0.025: Ω_m rises to 0.33, but σ₈ falls more (0.759).
- Reported only. No lensing likelihood is included.

ξ = 0 refits (no ΛCDM prior, ω_c free; DES-SN5YR / Pantheon+ / Union3):
- H₀ 68.47 / 68.50 / 68.52;
- ω_c 0.11859 / 0.11852 / 0.11849;
- Ω_m 0.3009 / 0.3004 / 0.3002;
- χ² 2652.142 / 2406.417 / 1045.311 (CMB part 1004.5–1004.8).

## Step 0 and checks (normal run: 7/7 have their required outcome)

| id | result | line |
|---|---|---|
| S0-1 C7 ΛCDM χ² | 1003.475 (plik 582.40, lowTT 24.31, lowEE 396.72) | 1003.475 ± 2 |
| S0-2 CFG681 BAO / BAO + Pantheon+ | 10.5515, Ω_m 0.29703 / 1400.143, 0.30390 | (10.5515, 0.2970), (1400.143, 0.3039) |
| S0-3 DESI DES-SN5YR chain | w −0.7521, wa −0.8611 (burn-in 0.3) | margestats −0.752, −0.86 |
| K1 background identity + sign | rate error 1.9e-7 (M-C ξ 0.01), 2.3e-10 (M-D ξ 0.3); total-conservation error 1.2e-3 / 1.2e-4 | ≤ 2e-3 |
| K2 ξ = 0 vs vanilla | max \|ΔC_ℓ/C_ℓ\| 0.0, σ₈ identical | ≤ 1e-4 |
| K3 δ_c growth z 10 → 0 (k 0.0338 /Mpc, ξ 0.05) vs independent ODE | 8.54284 vs 8.54321 (4.3e-5); ξ = 0: 3.9e-5; dilution term's own effect 7.4 % | ≤ 3e-3; ≥ 1 % |
| K4 CLASS D_M, H vs analytic background | 2.6e-9 | ≤ 1e-4 |

**MUTATE** (`X54_MUTATE=1`). The exchange sign is flipped in the background and the dilution term is dropped
(δQ = Qδ_c).
- Exit 0 with 6/6 required outcomes.
- **K1 FAILS**, with rate error 2.00, i.e. the energy flows the wrong way.
- **K3 FAILS**, with CLASS growth 8.300 vs ODE 7.347 (13 %).
- S0-1 to S0-3 and K2 still pass, because the bug is inert at ξ = 0.

## Model and implementation

- **Background:** flat GR with photons, N_eff 3.044 massless neutrinos, baryons, cold dark energy and a w = −1 vacuum.
  - dρ_c/dt + 3Hρ_c = +Q, dρ_DE/dt = −Q.
  - Analytic solutions (FROZEN §1) are coded in CLASS's background, written so that ξ = 0 is bit-identical to vanilla.
- **Perturbations:** Q^μ = Q u_c^μ, i.e. zero momentum transfer in the cold dark energy rest frame. δQ = 0 on cold-comoving
  slices, so the vacuum has no perturbation in that frame. Synchronous gauge:
  δ_c' = −h'/2 − (aQ/ρ_c ℋ)ℋδ_c, with θ_c = 0.
- **Code:** `x54_make_patch.py` builds the patch from the pristine CLASS v3.3.4 tree on disk, outside the repository;
  `x54_exchange.patch` is the diff. All committed runs (run 1, the reanalysis and MUTATE) used binary debac461… and patch
  d66bbc98… (see each `.out`). There were no downloads.
- **Likelihood:**
  - C2's plik-lite + low-ℓ TT + low-ℓ EE + A_planck prior;
  - DESI DR2 BAO (CFG689's table), with r_d and distances from the same CLASS run;
  - SN with M marginalised analytically;
  - three SN sets, never pooled.
- **Refits:** X34's Gauss–Newton/Broyden steering on plik + priors + BAO + SN, with a 6 + 1 parameter refit at every ξ.
  - The graded χ² adds low-ℓ TT/EE.
  - Grid: M-C ±{0.002, 0.004, 0.008, 0.012} (DES-SN5YR) and ±{0.002, 0.004} (others). M-D ±{0.1, 0.2, 0.4, 0.6}
    (DES-SN5YR) and ±{0.1, 0.2} + 0.4 (others).
  - 582 CLASS runs, about 50 min, one thread, nice 15. Peak child RSS is under 0.3 GB.

**No ΛCDM-derived inputs (coordinator/owner rule).**
- No Planck ω_c/ω_b ratio and no ΛCDM background prior. ω_c, ξ, ω_b, θ_s, A_s, n_s, τ and A_planck are fitted.
- C7's ΛCDM refit is used only as the start point.
- Still inherited, and disclosed in the ledger (A6–A11):
  - HyRec recombination;
  - BBN Y_He from CLASS's table;
  - massless N_eff 3.044;
  - power-law adiabatic initial conditions;
  - linear lensing;
  - plik-lite's foreground model;
  - C2's τ steering prior (steering only);
  - DESI's BAO template;
  - each SN collaboration's standardisation.

## Disclosures (implementation changes made before any graded number; none alters a frozen line)

1. **K2.** The first build differed from vanilla by 1.6e-3 at ℓ ≈ 2500 at ξ = 0, from floating-point reordering. The
   background was rewritten as factors on CLASS's own expressions, which made ξ = 0 bit-identical. The threshold is
   unchanged.
2. **has_cdm/has_lambda guard.** This check ran before CLASS set those flags. It was moved after `background_indices`.
3. **M-D for b = ξρ_DE0/((3−ξ)ρ_c0) > 1.** This case only arises at θ_s-shooting trial points with h > ~1.4. There the
   a⁻³ term is dropped (ρ_c = B a^{−ξ}). Every accepted fit has b < 1 (`b_D` in the JSON; max 0.150).
4. **K3's "dilution term's own effect".** This was first coded as the total ξ effect against ξ = 0 (0.47 %, because the
   background partly compensates). It was recoded to match the frozen text: ODE with the term vs without it, on the same
   background (7.4 %). The ODE first used CLASS's Newtonian-gauge k-output. That output is now converted back to
   synchronous gauge exactly as CLASS converts it (perturbations.c L8429–8450).
5. **Refit robustness.** A Broyden Jacobian reused from the neighbouring ξ is rebuilt by finite differences when a line
   search fails or the fall is < 0.05. One restart was made before any profile point was graded.
6. **Converged points only (frozen §3).** Run 1's analysis included the unconverged M-D ξ = 0.6 point (χ² 3651, started
   from ξ = 0 after ξ = 0.4 failed) in the spline. That produced a spurious "EXCHANGE PREFERRED (DE → cold), Δχ² 4.32"
   for M-D DES-SN5YR, visible in `run1_fits.out`.
   - The code was corrected to the frozen rule. The analysis was rerun on run 1's refits (`X54_REANALYSE`, no new fits),
     and Step 0 and the checks were rerun.
   - The grid's own Δχ² for M-D DES-SN5YR is 2652.142 − 2649.408 = 2.73 at ξ = 0.1, below 4.
   - M-C is unaffected: all its points converged.
7. **S1 is post hoc** (`X54_SUPP=1`): M-D at ξ = 0.3 converged for all SN sets, and ξ = 0.4 failed again in θ_s
   shooting. Its intervals are reported, not graded.

## Reading for the owner

- Pairing cold dark energy with dark energy through an exchange is **allowed only as a small perturbation**.
- In the Q ∝ ρ_c form the data cap the exchange at roughly a percent of the cold amount since recombination, and slightly
  prefer no flow or a weak cold → DE flow.
- In the Q ∝ ρ_DE form, a DE → cold flow making about 9 % of today's cold dark energy is mildly preferred (≈ 1.7σ, DES-SN5YR).
  It lowers S8 by about 0.025, but it makes a₀ rise with z, against CFG689's mildly declining native a₀(z).
- Neither form makes the cold mass, and neither turns a₀(z) into CFG689's 0.91 at z 2.33.
- κ = ½ remains FITTED.
