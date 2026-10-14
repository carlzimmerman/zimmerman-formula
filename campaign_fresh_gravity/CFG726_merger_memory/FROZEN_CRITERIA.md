# CFG726: MERGER MEMORY (H-MM). FROZEN CRITERIA

Committed alone, before any script of this lane exists and before any target comparison is computed. Date 2026-10-13.
Lane number: CFG726 is free (no directory, no commit, no LEDGER row carried it), in the owner chat's reserved block CFG720–729.

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Kernels: CFG695's
ν_s(y) = ½ + √(¼ + 1/y) PRIMARY, ν_mono (CFG4_common) bracket, never pooled. "Cold energy" throughout; its mass is still required;
no particle species. Not "theory closed". No ΛCDM halo, mass function, merger tree or standard-MOND yardstick enters any verdict.

**Machine limit (declared).** A 1024³ PM job shares the machine. This lane runs as ONE process, nice 10, ≤ 0.8 GB RSS, no PM run,
no Method A infall run (CFG637 `derive` is not called). vm_stat is checked before each stage; a stage is aborted if free+inactive
< 10 GB.

## 0. Status: POST-HOC mechanism test, every target already seen

All targets (CFG669 T2, CFG687, CFG652, CFG686, SPARC) were measured and read before this lane. A pass is an accommodation, not a
prediction. Hand estimates made while writing (disclosed, from the deep-regime formula below, not from any script): for KiDS early
types concentric equal pieces give a law-relative lift at 50–100 kpc of roughly +0.13 / +0.21 / +0.27 / +0.31 dex for
N = 2 / 3 / 4 / 5, i.e. predictions ≈ +0.10 / +0.18 / +0.24 / +0.28 after CFG658's −0.027. So N = 2 is expected to sit near the
2σ line; this is disclosed before freezing N.

## 1. The derivation (zero new constants)

**Inputs inherited, unchanged.** Law phantom of a source M_src(<r): M_ph(<r) = M_src(<r)[ν(G M_src(<r)/r² a₀) − 1] (running max),
cut at the supply edge (where it reaches the supply) and confined to the turnaround radius r_ta: `cfg637_lib.phantom_trunc`.
Supply = 5.364 × catchment; catchment = max(M_cond/0.10, M_b/0.90) (CFG652 `catchment`); r_ta from `cfg637_lib.r_ta_single`
(M_ta = catchment/f_b) at the system's redshift.

**H-MM statement.** Cold energy is conserved and collisionless (CFG722/723). A bound progenitor i (baryons m_i, its own profile)
carries its tethered cold energy T_i(<s) = its own law phantom cut at its own supply edge (supply 5.364 × m_i/0.10, condensed
progenitor) and its own r_ta. Smooth (diffuse) accretion brings baryons but no tethered halo of its own (diffuse matter has no
bound phantom). After assembly the progenitor halos are superposed (concentric for merged progenitors; around the member positions
for unmerged cluster members). The remnant's law profile T_rem(<r) is the plain law of ALL remnant baryons (each harness's own
convention, below). Cold energy cannot be destroyed, so where the superposed progenitor cold energy exceeds the remnant's law it
persists as free memory mass; where the law exceeds it, the law holds:

  **M_HMM(<r) = M_b(<r) + max[ C(<r), T_rem(<r) ]**,  C(<r) = Σ_i T_i(<r) (superposed; for members, convolved over positions).

The excess over the plain law is E(<r) = max(0, C − T_rem). Its total free mass is F = max_r E(<r).

**Closed forms (deep regime, every progenitor edge beyond r, concentric):** C(<r) = Σ_i √(G m_i a₀) r / G, so
E(<r) = (Σ_i √f_i − 1) × T_rem(<r) with f_i = m_i/M (mass fractions of bound progenitors) and smooth accretion entering only M.
Equal pieces: E = (√N − 1) T_rem. Two pieces of mass ratio q: Σ√f = (1 + √q)/√(1 + q). With finite edges, piece i contributes
min(√(G m_i a₀) r/G, S_i), so F = S_tot(1 − 1/√N) for N equal pieces (peaking at the progenitor edge r_e,i), and pieces whose edge
lies inside r contribute linearly (their whole supply). The additive limit (phantom ∝ source) gives E ≡ 0; N = 1 gives E ≡ 0.

**Placement.** PRIMARY P1 "memory placement": the superposed progenitor distribution is kept as it is (phase mixing of already
virialised collisionless halos preserves the coarse-grained radial distribution, Jeans theorem); M_HMM above. REPORTED bracket P2
(no verdict weight): the free mass F re-placed as CFG637 Method B (`maxent_reservoir`, Woolley F(E) in the total potential, bounded
at r_ta), with energy target E = Σ dM_free [Φ(r) + ¾ v_c(r)²] evaluated on the P1 free distribution (isothermal equipartition,
declared approximation); lensing = M_b + T_rem + F_P2 (KiDS and eRASS1, canonical, ν_s only).

## 2. N assignment per target (declared before any target number)

- **T-K KiDS early types:** PRIMARY N = 2 equal concentric pieces (one equal-mass major merger, the maximally sub-additive single
  merger). PROVISIONAL context from memory, unverified: pair-fraction studies give ~1 major merger since z ~ 2–3 for log M* ~ 11.
  REPORTED bracket N = 1, 2, 3, 4, 5 (equal pieces) and the q = 1/3 two-piece case. **Late types N = 1.** Progenitors have the
  remnant's baryon shape scaled in mass (so the additive MUTATE is exact). Baryons: CFG721 T-K late-type profile
  (M652.profiles(M_b, 0, R_X(M_b))) for both types, ladder M_b = 10^10, 10^10.5, 10^11, 10^11.5, R = 50, 70.71, 100 kpc, z = 0.
- **T-R eRASS1 / T-A ACCEPT clusters:** progenitors = unmerged member galaxies holding the condensed baryons (stars, f* = 0.20 of the
  gas, CFG687 primary), distributed like the stars (co-distributed with the gas β-model, CFG687 primary); hot gas = smooth (no own
  halo). PRIMARY: N_mem equal-mass members, each a Hernquist with R_e = 15 kpc (CFG652's RE_BCG, inherited), N_mem = redMaPPer λ
  where CFG688's 76-cluster match exists, else λ from a log-log least-squares relation λ(M_gas(<1 Mpc)) fitted on those 76 matched
  clusters (a measured scaling, not an H-MM parameter); ACCEPT uses the same relation on its own M_gas(<1 Mpc). REPORTED brackets:
  N_mem × 0.5 and × 2; "stripped" limit (member halos tidally stripped, cold energy distributed exactly like the members:
  C(<r) = Σ S_i-weighted member profile); "BCG half" (half the stars in one concentric BCG with its own halo, half in N_mem − 1
  members).
- **T-E eFEDS:** progenitors = BCG (M_bcg, concentric, R_e 15 kpc) + max(1, round(N_mem)) equal members sharing M_cond − M_bcg,
  distributed as CFG652's satellite profile (Hernquist R_e = 0.5 R_X); M_cond, M_bcg, N_mem are CFG652's staged inputs; hot gas smooth.
- **T-S SPARC:** discs are not major-merger remnants: N = 1 ⇒ H-MM is the plain law identically.

## 3. Targets, statistics and pass rules (per kernel × footing)

- **T-K** (CFG669 T2 Ks, +0.280 ± 0.083): prediction = −0.027 (CFG658's law value) + Δ_MM, Δ_MM = mean over the ladder and the three
  radii of log10[ΔΣ_HMM,early/ΔΣ_law,early] (late Δ ≡ 0 since N = 1). ΔΣ via M652.delta_sigma, truncated at r_ta, T_rem = uncut law
  of all baryons to r_ta (CFG721 T-K convention). **PASS** iff |pred − 0.280| < 2 × 0.083 at the PRIMARY N = 2.
- **T-R** (CFG687, 318 clusters): CFG687's per-cluster D, E, W, bands, 30-patch RA jackknife; T_rem = CFG687's uncut law (stored PL
  for ν_mono canonical; recomputed with CFG721's `law_M`/`dsig_from_M` otherwise). A = ΣWD/ΣWP. **PASS** iff |A_MID − 1| < 2σ AND
  |A_OUTER − 1| < 2σ. **T-R2 (reported):** tercile slope s of the H-MM predictions; "explains 0.90 ± 0.21" iff |0.90 − s| < 2 × 0.21
  AND s − s_law ≥ 0.21.
- **T-A** (CFG686, 8 ACCEPT): CFG686's measured ΔΣ/errors and gas construction (as copied in CFG721), bootstrap 1000 seed 1.
  **PASS** iff |A_MID − 1| < 2σ AND |A_OUTER − 1| < 2σ.
- **T-E** (CFG652, 131 groups): CFG652's staged stack and score code (as in CFG721: 30-patch jackknife, Hartlap, 8 bins 53–783 kpc,
  outer band 248–783 kpc). T_rem = candidate B as the analytic cut law (phantom_trunc of all baryons, confined to r_ta) — the
  harness's own baseline, CFG652 (b). **PASS** iff χ² p ≥ 0.01 AND |A_out| < 2σ_A.
- **T-X X-COP and T-B Bullet cores: NOT RUN** in this lane (no member inventory on disk for X-COP; Bullet needs CFG637's
  B1 machinery, which is a Method A run excluded by the machine limit). A not-run cell blocks a PASS.
- **T-S SPARC:** PASS iff the RAR rms is unchanged (0.100 dex); with N = 1 for discs this holds identically (stated as an identity,
  checked by the N = 1 MUTATE). **T-S2 (reported, not in the verdict, a declared vulnerability):** if minor accretion counts as
  progenitors, the disc changes. Reported: E/T_rem at r = 10, 30, 100 kpc for discs M_b = 10^10 and 10^11 carrying an accreted
  fraction f_acc ∈ {0.01, 0.03, 0.10} in pieces of 1% of M_b (concentric memory).

**Verdict per kernel (both footings required):** H-MM PASSES iff T-K, T-R, T-A, T-E, T-S pass on both footings AND T-X, T-B are run
and pass. Since T-X and T-B are not run, the best attainable label is "PASSES THE RUN TARGETS (T-X, T-B NOT RUN)"; any failing run
target gives "H-MM FAILS" with the failing targets listed.

## 4. MUTATE and controls (each must hold or the lane is void)

- **M-N1:** N = 1 everywhere (KiDS early N = 1; clusters and groups: a single concentric progenitor holding all condensed baryons
  with their actual profile) must reproduce the plain-law predictions exactly: max |E|/T_rem ≤ 1e-12 and ΔΣ identical to the
  baseline to ≤ 1e-12 relative, every target, kernel, footing.
- **M-ADD:** additive law (ν_add(y) ≡ 2, phantom = source) must give zero excess (E ≡ 0 to ≤ 1e-12 relative) in every target.
- **M0 harness fidelity:** the ν_mono canonical uncut law must reproduce CFG687's stored PL (median per bin ≤ 1%, band A ≤ 0.01) and
  CFG686's stored canonical/alt primary predictions (≤ 1%); the eFEDS analytic candidate B with CFG652's own kernel (C540.nu) must
  reproduce cfg652_models.npz canonical x1 (b) to ≤ 2% every group and bin (Method A's drawn settling vs the analytic cut, disclosed
  benchmark max 1.4% on three groups while writing); eFEDS score code must reproduce CFG652's χ² 22.8958 (a, canonical x1).
- **C-CONS:** in P1, max_r[max(C, T_rem)] ≤ max(S_tot, max T_rem) (no cold energy created beyond the larger of the supply and the
  law's own baseline).

## 5. What would change the reading

Nothing here is a prediction. A pass would need a forward test (e.g. pre-registered early types split by a measured merger
indicator at fixed M_b). A fail is scoped by target and by the N rule; the T-S2 vulnerability (minor accretion) is reported either
way.

κ fitted; cold energy mass required; not theory closed.
