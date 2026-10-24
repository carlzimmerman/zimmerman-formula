# TM1_tethered_medium: frozen criteria (committed alone, with the assumption ledger, before any script or number)

Owner request: score PAPER49's tethered medium (its exact action) as a flavor on the hardest rows, with frozen criteria
and verified pipelines. κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Cold energy
is a medium of real rest mass, never a particle. Not "theory closed". Nothing here may say the data favour the framework.

**Blindness disclosure.** Not blind. Before freezing I read the record numbers of Z2 (satellites), P4 (SPARC), F1/X2
(cluster stack and terciles), AG6C/AG7 (saddle), CFG938/939/941/944/945/946/949/959/815/801 (ledger rows), D6 (self-similar
tables, including its K3 FAIL) and F3 (growth machinery). Rows 2, 5 and 6 are re-scorings of verified pipelines whose
numbers I have seen. Row 1's growth exponent was anticipated from CFG938 (a^0.61). Rows 3 and 4 are new computations whose
numbers I have not seen.

## 0. The flavor, exactly

PAPER49 v1.2 (DOI 10.5281/zenodo.23533323; `qwen_claude_field_theory/papers_2026/PAPER49_why_cold_energy_settles_2026.tex`
L30–L37):

    L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|²,   K = 4πG, u = K|P|,
    K dW_rem/du = u²/(a₀ − u)   (W_rem = W_full − u²/2K, K dW_full/du = a₀u/(a₀ − u)),   γ = K L★²/2,
    ρ_c = ρ̄ + ∇·P,   ∂ₜP = −j   (L27).

Rules PAPER49 states without an action, each scored as a **POSTULATE**: T (tether only to condensed baryons, only at low
relative speed; L57 says "the action as written responds to all baryons"), C (catchment supply, L50), S (settling: the
rest state is reached, L44), U (hot-gas systems keep cold energy untethered and collisionless, L52).

## 1. Checks (the script exits 0 only if all pass; each is an implementation or reproduction check, not a verdict)

| id | check | line |
|---|---|---|
| S1 | sympy: W_rem from K W_rem′ = u²/(a₀−u), W_rem(0) = 0, has Taylor series u³/(3a₀K) + O(u⁴) (no quadratic term) | exact |
| S2 | sympy: varying Φ and P gives ∇²Φ = K(ρ_b + ∇·P) and (∇Φ − KP) − R(u)P̂ + γ∇²P = 0; the rest state of the γ = 0 limit is g_N = g²/(g + a₀) | exact |
| S3 | sympy (1D/planar and linear 3D): the P-equation's dependence on P through Φ cancels exactly (self-gravity of the tethered medium = 0; D-T at the level of PAPER49's own action) | exact |
| S4 | sympy: for curl-free P, PAPER49's static P-equation in a₀ units equals D10's stiffened equation ∇Φ + (Λ²/2)∇(∇·p) = p/(1−\|p\|) with Λ = L★ (so Z2's V3S and P4's T1 rows are this action's rest state) | exact |
| S5 | sympy: minimal kinetic completion (below) gives a positive-definite kinetic matrix; BLT's [[1,1],[1,0]] has det −1 (Z1 K1 reproduced) | exact |
| S6 | sympy: EdS growing exponent of the completed linear system with f_b = 1/6.364 | reproduces CFG938's 0.610 to 0.005 |
| F3a | F3's `growth_ratio` (exec'd read-only from its source text) reproduces F3's committed `T_at_k` for K4 BSK2_floor_1100, bsk2, a_i = 1e-3 | max \|Δ\| ≤ 1e-4 |
| Z2a | from Z2's committed per-system CSV: clean-subset (C1–C4) median of Delta_V3S, canonical | within 0.05 of Z2's +0.900 |
| Z2b | from the same CSV: OLS slope of the V3S prediction and of the data on log x_e with M_V controlled (45 systems, canonical) | within 0.05 of Z2's −0.55 and −0.05 |
| X2a | my cluster model with no cold component reproduces X2's committed C0 tercile A_MID and A_OUTER (boost convention, all four footing × h cells) | max \|Δ\| ≤ 0.005 |
| SSa | the D6 self-similar tables (read-only) give r_sp/r_ta = 0.364 ± 0.01 for ε = 1 and M(λ = 1) = 1 ± 1e-4 | as stated |
| SSb | re-solving D6's self-similar iteration (its function, exec'd read-only) at 3 × τ_max changes M(λ) by ≤ 5 % for λ ∈ [0.02, 1] (ε = 1, ½, ⅓) | ≤ 5 %; if it fails, the re-solved table is used and the failure is reported; if the re-solve does not converge (last max\|ΔlnM\| > 0.02), row 3 is NOT COMPUTABLE |
| P4a | my SPARC loader + algebraic simple law, per-galaxy Υ (P4's grid and rms rule), reproduces P4's iso_perUps rms on both footings | ≤ 2e-4 |
| P4b | the same with one global Υ reproduces CFG695 S2 (0.10091 @ 0.60 / 0.09943 @ 0.55) | ≤ 1e-4, Υ equal |
| AGa | AG6C's saddle script (run as a read-only copy in a scratch directory) gives mid-plane C(R = 0.2 d) = −0.240 ± 0.01 at both resolutions | as stated |
| AGb | my conversion of C(0.2) to units of ρ̄_c gives −89 ± 5 (MW–M31-like, 8e10 M☉ each, 0.77 Mpc) and −33 ± 2 (cluster pair, 2e13 M☉ each, 5 Mpc), canonical | as stated |

`--mutate` plants: M1 W_rem with a quadratic term (W_full instead of W_rem in the P-equation) → S1, S3 must fail;
M2 the medium given full self-gravity in the growth system → S6 must fail; M3 the cluster cold mass doubled → X2a passes
(no cold), but the row-3 numbers move (reported); M4 the SPARC law swapped to the standard μ = x/√(1+x²) → P4a must fail.
MUTATE must exit non-zero.

## 2. Rows and frozen class rules

Every row is scored on both footings where a₀ enters; a row's class is the worse of the two unless stated.
Classes: PASS / CONDITIONAL (passes only under a named postulate or on one footing) / FAIL / NOT COMPUTABLE.

### Row 1. Growth on FRW
- (a) **Does PAPER49 supply cosmological dynamics?** It gives a static Lagrangian (no time derivative of P or of the
  medium). If it does not, row 1 for PAPER49-as-written is NOT COMPUTABLE, with the missing ingredients named.
- (b) **Forced minimal completion** (scored): the medium is real rest mass and P is its displacement (∂ₜP = −j), so its
  kinetic energy ρ̄|ξ̇|²/2 with P = −ρ̄ξ (linear) is forced, not chosen; Newtonian cosmology on FRW, sub-horizon, the
  baryons a second pressureless fluid. No other term is added.
- (c) **The record's covariant parent** (CFG938; WT-02/CFG961 Hadamard ill-posed on FRW; CFG941 growth a^0.694): reported
  from the record, not re-derived.
- Health: ghost-free iff the kinetic matrix is positive definite; gradient-stable iff the medium's ω² ≥ 0 at large k.
- If healthy: σ₈/σ₈,dust with F3's `growth_ratio` on F3's backgrounds A and B, a_i = 1e-3 and 1e-4.
- **Rule:** PASS iff healthy AND σ₈/σ₈,dust ≥ 0.95 on every background and a_i (the F3/Y1 line). FAIL if a ghost, a
  gradient instability or σ₈/σ₈,dust < 0.95. The row class is that of (b); (a) and (c) are stated beside it.

### Row 2. Satellites with real cold mass
- Question: under the tether postulate T, does a satellite's own cold mass self-bind inside the MW host? Answered from S3
  (self-gravity of the tethered medium) and the record's hover results (CFG941, CFG945 Theorem S), contrasted with U1 T3 and
  O1 ε = 1.
- Rest-state score: by S4 the rest state is Z2's V3S row (stiffened AQUAL with the host field at the L★ floor; larger L★
  only screens more). Scored numbers: Z2's committed clean-subset excess and the host-field slope at fixed M_V
  (`Z2_satellite_systematics/README.md` L19–L28, L100–L103), after Z2a/Z2b reproduce them.
- **Rule:** PASS iff the clean-subset excess is within 2 sd of 0 AND the predicted host-field slope is within 2 sd of the
  data's (−0.05 ± 0.19). FAIL otherwise. If the clean subset is TOO FEW on a footing, that footing is scored on Z2's
  C2–C4-only subset (N 19) and this is stated.

### Row 3. Cluster cores with untethered mass (postulate U)
- Data and statistic: X2's replay of F1's eRASS1 × KiDS stack (`x2_replay_percluster.npz`, 326 clusters), F1's bands
  (MID bins 3–5, OUTER 6–7), A = ΣW·D/ΣW·P, 30-patch jackknife, boost convention (F1 A1), catalogue-Mgas500 terciles
  (X2). Cells h = 0.672 and 0.686 (native).
- Baryons: F1's G0 gas (β = 2/3, cut at 3 Mpc, pipeline-distance rescale) × 1.20 for stars, miscentring offset as X2.
- **Untethered cold profile (derived under a stated initial condition):** collisionless self-similar secondary infall
  (EdS, radial orbits; Bertschinger 1985 for ε = 1, Fillmore–Goldreich ε = ½, ⅓), from D6's tables. The bracket
  ε ∈ {1, ½, ⅓} is D6's frozen bracket, not a knob. No NFW.
  - Supply (postulate C): cold mass inside turnaround = 5.364 × the catchment baryons, taken as the F1 G0 baryons inside
    3 Mpc (M_ta = 6.364 M_b,3).
  - r_ta from M_ta = (4π/3)(3π/4)² ρ̄_m(z) r_ta³, ρ̄_m(z) = 6.364 × ω_b ρ_crit,100 (1+z)³, ω_b = 0.0224 (BBN, as AG6C).
  - M_cold(<r) = 5.364 M_b,3 · ℳ_ε(r/r_ta), truncated at r_ta (D6's convention).
- Readings (each scored; none is chosen after the numbers):
  - **U0 (primary; PAPER49 L52 read literally):** all cold energy untethered; g = G(M_b + M_cold)/r². Footing-independent.
  - **U1 (postulate T, condensed-only tether):** the stars (the 0.20 share) carry the law, g = ν(g_N,⋆/a₀) g_N,⋆ +
    G(M_gas + M_cold,unt)/r², with M_cold,unt = max(0, 5.364 M_b,3 − M_ph,⋆(<r_ta)) distributed as ℳ_ε.
  - **U2 (the action as written: all baryons tether):** g = ν(g_N,b/a₀) g_N,b + G M_cold,unt/r², M_cold,unt =
    max(0, 5.364 M_b,3 − M_ph,b(<r_ta)) as ℳ_ε.
  ν is the spherical AQUAL μ = x/(1+x) (F1's `g_aqual_sph`).
- **Cell rule:** a (reading, ε, footing, h) cell PASSES iff, on all 326 clusters, |A_MID − 1| ≤ 2 s_jk and
  |A_OUTER − 1| ≤ 2 s_jk, AND in each of the three terciles |A_MID − 1| ≤ 2 s_jk and |A_OUTER − 1| ≤ 2 s_jk.
- **Reading class:** EXPLAINS if every ε passes on both h cells; CONDITIONAL(ε) if some do; FAILS if none.
- **Row rule:** the row class is U0's (PAPER49's own prediction); since U0 rests on postulates U and C, an EXPLAINS gives
  CONDITIONAL, never PASS. FAILS gives FAIL. U1 and U2 are reported with their own classes. PAPER49's own scored test
  (CFG815) is quoted beside it.

### Row 4. Capacity in isolated galaxies
- Data: SPARC (175 galaxies, P4's loader), per-galaxy Υ from row 6's fit, M_b = Υ L[3.6] + 1.33 M_HI (SPARC table).
- Need: the rest state's phantom M_ph(<R) = (g_law − g_bar) R²/G at each measured radius (primary); the data's
  (g_obs − g_bar) R²/G reported.
- Supply (own reading, the brief's default): 5.364 M_b.
- f_gal = fraction of galaxies with M_ph(<R) > 5.364 M_b at any measured radius; f_pts likewise for radii.
- **Rule (own reading):** PASS if f_gal ≤ 0.05 on both footings; FAIL if f_gal > 0.20 on either; CONDITIONAL otherwise.
  CFG801 (own-supply edge excluded by isolated-galaxy lensing, Δχ² +197) is quoted beside it.
- **Catchment reading (postulate C):** report, per galaxy, the catchment multiplier m = max_R M_ph(<R)/(5.364 M_b) that the
  catchment must supply. PAPER49 gives no per-galaxy catchment, so this reading is CONDITIONAL by construction.
- **Row class:** the own reading's class if it is PASS; otherwise CONDITIONAL (on postulate C) and the own-reading class
  is stated beside it.

### Row 5. Saddle positivity
- Reproduce AGa, AGb. The γ = 0 limit is AG6C's; the stiffness's effect is bounded by (L★/ℓ)² with ℓ the negative
  pancake's half-thickness 0.05 d, at L★ = 1 kpc (the largest allowed).
- **Rule:** PASS iff ρ̄ + ∇·P ≥ 0 everywhere in the action's static two-body solution; FAIL otherwise (the action's rest
  state cannot be realised by a positive medium there, so the law must fail in the saddle band). Observability is quoted
  from AG7 (S/N, pairs needed); it does not change the class.

### Row 6. SPARC RAR
- The rest state is the n = 1 law (S2). Statistic: P4's T1 line (rms ≤ 0.110 dex AND median Υ in [0.50, 0.80]), per-galaxy
  Υ, algebraic isolated simple law (P4: the external field and L★ move the rms by < 0.001 dex). Global-Υ rms reported.
- **Rule:** a footing PASSES the line or not. Because the rest state is reached only under postulate S (CFG939 derived it
  for a spherical single medium by phase mixing; no derivation for discs or with supply), the row is at best CONDITIONAL:
  CONDITIONAL if the line passes on at least one footing, FAIL if it fails on both. P4's χ² line (family-generic FAIL) is
  quoted.

## 3. Overall reading (frozen form)
"Resolves the law-versus-clumping split" iff rows 1 and 2 both PASS and row 6 is not FAIL. Otherwise: does not resolve.
Postulates are counted by name (T, C, S, U, plus the self-similar initial condition in row 3). Fitted / bounded constants
(κ, L★, Ω_c/Ω_b) are listed.

## 4. Compute and commits
Single thread, `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes. No downloads. Inputs read-only; AG6C's script is run as
a copy in a scratch directory. Commits by explicit pathspec, lane directory only. Never pushed. Amendments fix-forward
in this file, dated, marked pre- or post-result.
