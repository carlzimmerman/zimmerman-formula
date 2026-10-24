# TM1_tethered_medium: PAPER49's tethered medium scored on the hardest rows

## Verdict: CRISP FINDING. PAPER49's action is the law side of the split. It does not resolve law versus clumping

PAPER49 v1.2 (DOI 10.5281/zenodo.23533323) is scored with its exact action. That action is
L = −|∇Φ − KP|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|², with K dW_rem/du = u²/(a₀ − u) and ρ_c = ρ̄ + ∇·P.
Where the paper gives a rule and no action, the rule is scored as a POSTULATE:
- T: tether only to condensed baryons, at low relative speed;
- C: catchment supply;
- S: settling;
- U: untethered cold energy in hot-gas systems.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. Cold energy is a medium of real rest mass, not a
particle. Not "theory closed". Nothing here says the data favour the framework.

| row | class | key numbers (canonical / alt) | evidence |
|---|---|---|---|
| 1 Growth on FRW | **FAIL** (healthy, but no growth) | PAPER49 as written: NOT COMPUTABLE (no dynamics). With the forced kinetic term: no ghost, ω² = γρ_c k² ≥ 0, but the medium has **no self-gravity** ⇒ δ ∝ a^**0.610** (EdS). σ₈/σ₈,dust = **0.075 / 0.077** (from a = 1e-3) and **0.041 / 0.043** (from 1e-4) on F3's backgrounds A / B, against the 0.95 line | `.out` L8, L10, L12–L14, L18–L23 |
| 2 Satellites | **FAIL** | No self-binding: in PAPER49's own action the tethered medium's self-gravity cancels exactly (S3). Rest state = Z2's V3S row (S4). Clean excess **+0.900 ± 0.213** (canonical, N 6). Alt clean set is TOO FEW, so alt is scored on C2–C4: **+1.162 ± 0.150**. Host-field slope at fixed M_V: predicted **−0.545 / −0.531**, data **−0.05 ± 0.19** | `.out` L10–L11, L26–L32 |
| 3 Cluster cores (untethered, U0) | **FAIL** | Self-similar collisionless infall with no NFW, supply 5.364 × catchment. Best case ε = 1: all-cluster A_MID **0.87 / 0.91** (h 0.672 / 0.686), but the heavy tercile is overshot in the core (**0.80 ± 0.07**) and undershot outside (A_OUTER **1.30 ± 0.09**). ε = ½ and ⅓ leave the core short (A_MID 1.25–1.64). No ε passes | `.out` L43–L48, L73–L74 |
| 4 Capacity | **CONDITIONAL** (on catchment, C) | Own supply 5.364 M_b fails in **22 % / 34 %** of SPARC galaxies (39 / 60 of 175). The catchment would have to supply up to **3.8 / 4.2 ×** that (95th percentile 1.6 / 1.8 ×). CFG801 already excluded own supply with lensing (Δχ² +197) | `.out` L84–L86 |
| 5 Saddle positivity | **FAIL** | ρ̄ + ∇·P at R = 0.2 d: **−89 ρ̄ / −98 ρ̄** for the MW–M31-like pair and **−33 / −37** for the cluster pair. The minimum is −211 / −232 and −79 / −87. Stiffness cannot fill the pancake: (L★/0.05d)² ≤ 7e-4. The law must fail in the saddle band. The "no saddle dip" test is not possible now (AG7: S/N ≤ 0.87) | `.out` L89–L96 |
| 6 SPARC RAR | **CONDITIONAL** (on settling, S) | Rest state = the n = 1 law. With per-galaxy Υ, rms **0.0541 / 0.0537 dex** and median Υ **0.52 / 0.44**: the line passes on canonical and fails on alt (Υ window). Global Υ gives 0.101 / 0.099. P4's χ² line FAILS for the whole family | `.out` L77–L81 |

**Overall reading (frozen rule §3): it does not resolve the split.**
- **The law side.** PAPER49's action is a clean derivation of the law: an exact rest state with the simple μ (S2), and the
  same static equation as the screened theory (S4).
- **What it costs.** For the same reason it has every cold-sector failure of that side:
  - The tethered medium has no self-gravity. W_rem starts at u³ (S1) and the field term cancels the medium's own pull
    (S3). This is D-T on the paper's own Lagrangian.
  - So growth collapses to a^0.61 (σ₈ at 4–8 % of the dust value).
  - Satellites cannot bind their cold mass. At rest they carry the stiffened-AQUAL EFE that Z2 rejects. In motion the
    medium hovers.
- **Clumping comes only by postulate.** Postulate U (untethered, collisionless cold energy) supplies it in clusters, and
  there it is CDM-like physics. Even then, with a derived profile, it fails the terciles.
- **Postulates used:** T, C, S, U, plus the self-similar initial condition in row 3.
- **Fitted or bounded constants:** κ, L★ (24 pc to about 1 kpc), Ω_c/Ω_b.

## Record check (what this action shares with the record's results)

- **CFG938/941 (D-T).** Confirmed on PAPER49's own Lagrangian, without the χ covariant parent:
  - the 1D force on the medium has d(force)/dP = 0 at P → 0;
  - the 3D longitudinal (∇Φ − KP) = −iKρ_b/k does not depend on P (S3).
  
  The EdS growth exponent is 0.6095, matching CFG938's 0.610. CFG941's 0.694 belongs to the χ parent.
- **Z1 (dipolar, Blanchet–Le Tiec).** **Different on the ghost.** BLT's kinetic matrix [[1,1],[1,0]] has det −1, which
  is a ghost; its gravitating points are geodesic dust (Z1 K3). PAPER49 identifies P with the medium's own displacement,
  so there is one kinetic term per species, diag(ρ_b, ρ_c), and **no ghost** (S5). The price is the reverse of BLT's.
  BLT's linear sector is CDM plus a ghost. PAPER49's is ghost-free with no self-gravity. Neither gives the law together
  with dust growth.
- **WT-02 / CFG961.** CFG938's covariant parent is Hadamard ill-posed on FRW, with c_T not structurally c. That is quoted,
  not re-derived. PAPER49 itself names no covariant parent (L60). The minimal Newtonian completion scored here is healthy.
- **CFG944.** The tether's argument reaches the u = a₀ wall at z ≥ 84. At the wall the medium cannot displace further, so
  this only lowers row 1's growth.
- **CFG945 Theorem S / CFG941 hover; U1 T3; O1 ε = 1.** All the same statement as row 2's. Y1's P-medium binds only
  because its tether is finite, and it loses the law.
- **D6.** Its self-similar K3 failed (interior slope 0.625 against 0.75). Re-solving at 2 × τ_max changes M(λ) by ≤ 2.4 %
  on λ ∈ [0.02, 1] (SSb), and the slope moves 0.625 → 0.642. So the 0.75 asymptote lies deeper than 0.01–0.03, and the
  profile at the radii scored is converged.
- **CFG815.** PAPER49's own hot-gas test also fails: the middle tercile is 1.64 at Z +4.6.
- **CFG949.** It reached A_MID ≈ 1 with native NFW debris. With a derived self-similar profile, no ε fits both the heavy
  tercile's core and its outskirts.

## 1. Growth on FRW

- **PAPER49 as written.** The Lagrangian is static: there is no Ṗ, no background and no metric. That is NOT COMPUTABLE.
  What is missing: the medium's inertia, the FRW state of P (P = 0 by isotropy), the behaviour of u = K|P| in the linear
  universe, and a relativistic completion.
- **Forced minimal completion.** The medium is real rest mass and ∂ₜP = −j, so its kinetic energy ρ_c|ξ̇|²/2 with
  P = −ρ_cξ is forced. Nothing else is added.
  - The linear equations are δ̈_b + 2Hδ̇_b = 4πG(ρ_bδ_b + ρ_cδ_c) and δ̈_c + 2Hδ̇_c = 4πGρ_bδ_b. The medium feels only the
    baryons.
  - Health: kinetic matrix positive (no ghost); medium ω² = γρ_c k² ≥ 0 (no gradient instability).
  - The stiffness sound speed is 0.7–30 m s⁻¹ (L★ = 24 pc to 1 kpc). Its cutoff sits at k ~ 1/L★, far from σ₈ scales,
    and could only lower growth.
- **σ₈.** F3's `growth_ratio` is exec'd from its source text. F3a reproduces F3's committed transfer exactly. The tethered
  kernel is its s → 0 limit. The ratio is scale-free: 0.0747 / 0.0409 (background A, a_i = 1e-3 / 1e-4) and
  0.0773 / 0.0427 (background B). **FAIL**, by a factor of about 12–24 in σ₈.
- **Context.** PAPER49's cosmic-shear claim (L50) used the record's class-A engine. That engine is not the
  non-relativistic limit of any local parent (CFG941 (g), CFG944). CFG963 found that the native pass is carried by gas
  expulsion.

## 2. Satellites with real cold mass

- **Self-binding: no.** PAPER49 says "Its self-gravity cancels against the quadratic part of the field energy" (L34). S3
  makes that exact. The tethered cold mass is real and pulls on baryons, but not on itself or on other tethered medium.
- **The rest state.** The medium's state is set pointwise by the total baryonic Newtonian field (host plus satellite). In
  PAPER49's static equation this is stiffened AQUAL with the host's EFE, identical to D10's form (S4). That is Z2's V3S row,
  at the L★ floor; a larger L★ only screens more.
- **The numbers.** Z2a and Z2b reproduce Z2 from its committed per-system CSV:
  - clean median +0.936 against Z2's bootstrap +0.900;
  - slopes −0.545 / −0.050 against −0.55 / −0.05.
- **Scored.** The excess is +0.900 ± 0.213 canonical and +1.162 ± 0.150 alt (C2–C4). The predicted host-field slope is
  −0.54 / −0.53, against flat data. Both lines fail on both footings.
- **In motion it is worse.** The label-free tether hovers (CFG945 Theorem S; Δa/g_host 1.02–1.11). The stars leave the
  medium in 9–106 Myr, which drives the system toward Z2's dust-free limit (+1.88 dex).

## 3. Cluster cores with untethered cold energy

- **Data.** X2's replay of F1's eRASS1 × KiDS stack (326 clusters), boost convention, catalogue-Mgas500 terciles,
  h 0.672 / 0.686.
- **Model check.** X2a: my law-only model reproduces X2's committed C0 tercile table to 4e-16.
- **The untethered profile.** EdS self-similar collisionless infall: D6's tables (SSa, and SSb at 2 × τ_max), with D6's
  frozen ε bracket.
  - Cold mass inside turnaround = 5.364 × catchment baryons (F1 G0 to 3 Mpc).
  - r_ta comes from the EdS turnaround overdensity on the native mean density (ω_b = 0.0224). The median r_ta is 6.4 Mpc.

| reading | best all-cluster A_MID / A_OUTER | terciles (A_MID / A_OUTER) | class |
|---|---|---|---|
| U0, ε = 1 (h 0.672) | 0.873 ± 0.060 / 1.079 ± 0.098 | T1 0.81 / 0.82, T2 1.03 / 0.91, **T3 0.80 ± 0.07 / 1.30 ± 0.09** | fail |
| U0, ε = ½ | 1.25 / 1.34 | T2 1.44, T3 OUTER 1.59 | fail |
| U0, ε = ⅓ | 1.59 / 1.64 | T2 1.87 | fail |
| U1 (condensed-only tether) | 3.07 / 1.86 (canonical) | the stars' phantom alone is 1.5–1.7 × the supply ⇒ no untethered mass left | FAILS |
| U2 (action as written) | = the law, 1.68 / 0.95 | the law's phantom at r_ta is **3.6–4.0 × the supply**: clusters cannot supply the law | FAILS |

- **Shape problem.** A profile concentrated enough to fill the core (ε = 1) puts too much mass inside 0.5 Mpc in heavy
  clusters and too little at 1.2–3 Mpc. A flatter profile leaves the core short. The frozen class is FAILS for every
  reading, so the row is **FAIL**.

## 4. Capacity in isolated galaxies

- **Inputs.** Per-galaxy Υ from row 6, M_b = Υ L[3.6] + 1.33 M_HI, and the law's phantom M_ph(<R) = (g_law − g_bar)R²/G.
- **Own supply (5.364 M_b): FAIL.**
  - f_gal is 0.223 / 0.343, and f_pts 0.039 / 0.059. The data-side need gives 0.211 / 0.257.
  - In the deep regime own supply ends at r ≈ 5.4 r_M. SPARC's median last radius is 4.0 / 4.6 r_M (95th percentile 7.8 / 8.8).
- **Catchment reading.** The catchment must supply a multiplier m of 0.70 / 0.81 (median), 1.58 / 1.80 (95th percentile)
  and 3.8 / 4.2 (maximum) times own supply. PAPER49 gives no per-galaxy catchment, so this is **CONDITIONAL** on
  postulate C.
- **Lensing.** CFG801 had already excluded own supply (Δχ² +197).
- **The tether's projected cap.** Σ̄ ≤ a₀/πG; AG4c found it NOT DIAGNOSTIC.

## 5. Saddle positivity

- **Reproduction.** AG6C's solver was run as a copy in a temporary directory and reproduces C(0.2 d) = −0.24012 / −0.24041
  (two resolutions).
- **Conversion.** My conversion gives −89.0 ρ̄ (MW–M31-like pair) and −33.4 ρ̄ (cluster pair) on canonical; alt gives
  −97.9 / −36.7.
- **The column a positive medium cannot supply.** 1.94 / 2.14 M☉ pc⁻² (MW–M31-like) and 4.64 / 5.11 M☉ pc⁻² (cluster
  pair), matching the paper.
- **Stiffness does not save it.** The γ term is ≤ (L★/0.05d)² = 6.7e-4 / 1.6e-5 at L★ = 1 kpc.
- **Consequence.** The action's static two-body state cannot be realised by a medium of positive mass, so the law must fail
  in the saddle band. AG6C H6 adds that, read literally with inertia, the medium is also gradient-unstable there. How far
  the medium departs from the law is not computed.
- **Observability.** AG7: box S/N 0.30, optimal strip 0.87; about 12 × more pairs are needed. NOT TESTABLE NOW.

## 6. SPARC RAR

- **Rest state.** The rest state is exactly the simple-μ law (S2), and the static equation equals the screened form (S4).
  P4 showed that the external field and L★ move the rms by < 0.001 dex, so the algebraic isolated law is used.
- **Reproduction.** P4a and P4b reproduce P4 to ≤ 3e-8.
- **Result.** The line passes on canonical (0.0541, Υ 0.52) and fails on alt (Υ 0.44 < 0.50).
- **Settling is a postulate.** CFG939 derived the law state for a spherical single medium only, by phase mixing with 44 %
  of the infall ejected. There is no derivation for discs or with supply. So the row is **CONDITIONAL**.

## Checks, MUTATE, compute, files

- **Main run.** `tm1_tethered_medium.py`: **16/16 PASS**, exit 0, 41 s, 0.24 GB peak, one thread at nice 15.
- **`--mutate`: 10/16, exit 1.**
  - M1 (W_full in place of W_rem) fails S1, S2 and S3 (d(force)/dP = −K).
  - M2 (full self-gravity for the medium) fails S6 (p = 1).
  - M3 (cold mass ×2) moves U0 ε = 1 to A_MID 0.46.
  - M4 (standard μ) fails P4a and P4b.
  - Outputs: `*_MUTATE.out`, `*_results_MUTATE.json`.
- **SSb (AMENDMENT A1, pre-result for rows 3–6).**
  - The frozen 3 × τ_max re-solve reached 9.5 GB through `dense_output` and was killed before any row-3 number.
  - `tm1_selfsim_resolve.py` re-solves at 2 × τ_max with `t_eval` instead (403 / 255 / 346 s, ≤ 0.62 GB). Output:
    `tm1_selfsim_resolve.out`, `tm1_selfsim_resolve_2x.npz`.
  - Rows 1–2 had printed before the amendment (disclosed in A1).
- **ENQUEUE.** None needed. A 3 × τ_max SSb is optional: SSb already passes at 2 ×, and the profile moves ≤ 2.4 %.
- **Inputs.** All read-only:
  - F1, X2, D6, F3 and P4 code is exec'd from source text; AG6C runs as a temporary copy;
  - Z2, X2, F3 and P4 JSON/CSV/npz files are loaded as data;
  - sha256 of every source is in the results JSON. Nothing was downloaded.
- **Commits.** Frozen criteria and ledger alone first (167976b20a), then A1 (9cb49dc712), then this README, the scripts and
  the outputs. Nothing outside this directory was edited.
