# X59_formation_epoch_switch — FROZEN CRITERIA (committed alone with the ledger, before any script or number of this lane)

Written 2026-10-27. Peer lanes X57 (exclusion survey), X58 (object-keyed switch, operational) and X61 (switch at high z)
are read, never edited.

Standing rules: κ = ½ FITTED. Footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m/s²) never pooled. Cold dark energy is
the gravitating w ≈ 0 clumping component of dark energy; it is not matter and not a particle. Framework-native only: no
ΛCDM number enters a rule (the disclosed exceptions are in the ledger). No fitting, no knob scan. Not "theory closed".
Nothing here may say the data favour the framework.

## 0. Hypothesis FE (the formation-epoch switch)

Cold dark energy stays bound in a collapsed object only if, at the object's collapse epoch z_c,

    η(M) Σ_coll(M, z_c)  >  Σ_a₀(z_c) ≡ a₀(z_c) / (2πG),     a₀(z) = a₀ · F(z)

- **Σ_coll** is X41's convention, unchanged: Σ_coll = Δ ρ_m(z_f) r_f, Δ = 18π², for the half-mass object M/2 at the
  Lacey–Cole median formation epoch z_f, with r_f = [3(M/2) / (4π Δ ρ_m(z_f))]^{1/3}.
- **z_c ≡ z_f.** For an object of mass M identified at epoch z_obs, z_f solves (Lacey & Cole 1993, the standard extension
  of X41's z_obs = 0 equation):

      δ_c / D(z_f) = δ_c / D(z_obs) + ω̃ [σ²(M/2) − σ²(M)]^{1/2},   δ_c = 1.686, ω̃ = 0.974

  At z_obs = 0 this is X41/X43's equation exactly. σ(M) and D(z) are EM1's CLASS background A (executed read-only, as
  X41/X43).
- **η(M)** = (4/(3B(1))) c_f(M)^{5/4} (X43).
  - **PRIMARY: c_f(M) from X48's ng 48 table** (`x48_regrade_ng48.json`: 7.17 / 6.97 / 5.62 at 10¹² / 10¹³ / 10¹⁴),
    interpolated in log M and held flat outside, exactly as X56/X58 do.
  - **VARIANT (reported, class shown): c_f = 4 EXTERNAL, η = 14.83** (X43).
- **F(z) = a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)).**
  - **PRIMARY: the record's DESI M-DEC curve** (CFG223 `curves["M-DEC"]`, CPL w₀ −0.838, w_a −0.62), tabulated on
    z ∈ [0, 6]; beyond z = 6 the same CPL closed form √[a^{−3(1+w₀+w_a)} e^{−3w_a(1−a)}] (checked against the table, K2).
  - **VARIANT: flat, F ≡ 1.** With flat F and z_obs = 0, FE is X43's/X58's crossover flag exactly (K1).
- Background A is used for every system, as X43.

**What "not retained" means dynamically (the posit, disclosed).** In an object that fails FE at its collapse epoch, the
cold dark energy component does not take part in the object's collapse. It is not heated (its velocity dispersion stays
cold), it is not converted into dark energy or anything else (X54 excludes exchange), and its amount is conserved: it
stays in the surrounding smooth cosmic field at its background density on the object's scale, and the object's own
gravity is that of its baryons under the fundamental law (X58's below branch). No action is written for this; a cold
collisionless component that does not fall into a well it shares is itself non-gravitational behaviour, and the record
has no mechanism for it (X22, X47).

**Persistence (frozen primary reading, "sticky").** Cold dark energy that WAS retained by an object (FE satisfied at
that object's z_c) is a bound, cold, collisionless component. FE supplies no energy to unbind it, so it is carried
into every descendant through mergers, whether or not the descendant itself satisfies FE. The alternative "re-keyed"
reading (each new collapse re-decides and releases a progenitor's content) is reported only: it needs unbinding energy
(X22: c_s ≈ 190–200 km/s), which "no heating" excludes.

## 1. Questions and computations (no number tuned)

**(a) Present-day retention by class.** Each system's z = 0 mass M and its own z_c from the EPS equation (z_obs = 0):
- **SPARC (175):** M = M200 from EM1 R1 (bg A), log M200 = a + b (log M_b − 10), as X43.
- **Groups (63, Tian+26 file as X43):** M200 from the same relation on the groups' log M_b.
- **Clusters:** M = M_fair + M_b from X30's `prep` (executed read-only to STEP 0, as X41/X43), per footing, both h cells
  (h0672, h0686); every cluster cell counted.
- **Dwarfs (82, X51's five classes):** M200 = max(EM1 extrapolation, M_cool), M_cool = atomic cooling, T_vir = 10⁴ K,
  μ = 0.59, z = 8, bg A — X51's function, re-implemented and checked (K5). Reported variant: z_c = 8 for the dwarfs on the
  cooling floor (their formation epoch in X51's own reading).
- Retention fraction per class = retained members / members.

**(b) Forest (R1).** The forest scale is X22's α_NF half-mode mass M_hm = 4.894e9 M☉ (`step1.alpha_NF.M_hm_Msun`). An
object of mass M_hm identified at z_obs ∈ {2.0, 2.5, 3.0}; FE evaluated at its own z_f(M_hm | z_obs). Also reported:
the FE threshold mass m_FE(z_obs) (smallest retained mass) at z_obs = 0, 1, 2, 2.5, 3, 4, 6, 8.

**(c) Early capture in galaxy progenitors.** For a z = 0 host of mass M0, the early-capture fraction f_EC(M0) is the
fraction of M0's mass that, at some epoch z ∈ [0, 10] (grid step 0.05), lay inside a progenitor of mass m(z) that
satisfied FE(m, z_obs = z). Computed by EPS Monte Carlo (sharp-k excursion sets, Lacey–Cole 1993; Bond et al. 1991):
- each mass element is a Gaussian random walk in S = σ²(M) starting at (S0 = σ²(M0), δ_c), uniform steps ΔS = 0.01, up to
  S(M_res); its progenitor mass at z is the mass at the walk's first up-crossing of δ_c/D(z);
- M_res = 2×10⁷ M☉ (σ grid floor 10⁷ for the M/2 object): progenitors below M_res are counted NOT captured, so f_EC is a
  lower bound if m_FE(z) < M_res at some z ≤ 10 (reported);
- N = 20 000 walks per host, seed 20261027 (numpy default_rng), processed in blocks (memory);
- hosts: a grid log M0 = 10.0 … 13.0 (step 0.25), interpolated to each SPARC galaxy; the **median SPARC galaxy** (EM1 R1 at
  the SPARC median log M_b); and the **Milky Way**, M_b = 6.0e10 M☉ (ledger A9) through EM1 R1.
- Reported also: f_self (the host itself satisfies FE at its own z_c) and the single-epoch fraction curve f(z).

## 2. Verdict (per footing; PRIMARY = X48 ng 48 c_f, M-DEC F(z))

Three clauses, each evaluated per footing:

- **R1 (forest):** PASS iff FE holds for M_hm at all three z_obs ∈ {2.0, 2.5, 3.0}.
- **EC (early capture):** FAIL iff f_EC(median SPARC galaxy) > f_max, the largest fraction of the fair share that X6's
  d2 (Υ) line tolerates, from X22 (`step2.per_footing.*.f_max`: 0.196 canonical / 0.0269 alt).
- **PATTERN** (the record: galaxies none [X53, X55]; groups and clusters hold collapse cores [X43, X48]; dwarfs hold cold
  dark energy halos in every class [X51]): holds iff
  - SPARC retained fraction ≤ 0.10;
  - groups retained fraction ≥ 0.50;
  - cluster cells retained fraction ≥ 0.90;
  - each of X51's five dwarf classes retained fraction ≥ 0.50.

Class per footing:
- **FE FAILS R1 (forest)** if R1 fails; **FE FAILS BY EARLY CAPTURE (galaxy progenitors keep too much)** if EC fails.
  If both fail the label carries both, joined by " + ".
- **FE REPRODUCES THE PATTERN (retention by class stated) AND PASSES R1** if R1 passes, EC passes and PATTERN holds.
- **UNDECIDED (pattern miss: <classes>)** if R1 and EC pass but PATTERN does not.

Lane verdict: the common class if both footings agree; otherwise **UNDECIDED (footings disagree)**, both shown.

Reported, no verdict weight: every clause under the variants (flat F; c_f = 4; flat + c_f = 4); the re-keyed reading
(f_EC → f_self); the dwarf z_c = 8 variant; the implied Σ_core / Σ_a₀(z_c) for retained dwarfs (if any); f_EC for the MW
and the SPARC median of per-galaxy f_EC; X22's tolerated M_c(<R_last)/M_b next to f_EC for scale.

## 3. Checks (all must pass in the normal run)

- **K0:** X41's Σ_coll table reproduced (10¹¹…10¹⁵: 3.8, 6.8, 11.9, 20.5, 34.7 M☉ pc⁻², to ±0.05) and X41's z_f(10¹²)
  0.94 (±0.005); η(c_f = 4) = 14.83 (±0.005).
- **K1 (identity):** with F ≡ 1 and z_obs = 0, the FE flag equals X43's flag ηΣ_coll(M) > Σ_a₀ for every SPARC galaxy,
  group, cluster cell and dwarf, both footings, both η choices (0 mismatches).
- **K1b:** the c_f = 4 crossover masses equal X43's 10^12.09 / 10^12.43 (±0.005 dex). The X48-c_f crossover is computed the
  same way and reported next to X58's uncommitted printout (10^10.83 / 10^11.16), no check weight.
- **K2:** M-DEC table vs the CPL closed form, max |ΔF| < 2e-3 on [0, 6]; F(1, 2, 3) = 0.9889, 0.8739, 0.7750 (X35 S0-2)
  to ±0.002.
- **K3:** generalised EPS at z_obs = 0 equals X41's z_f to 1e-9 at 10¹¹–10¹⁵; equation residual < 1e-3 at z_obs = 2.
- **K4:** Monte Carlo single-epoch progenitor fraction f(> m, z | M0) vs the analytic erfc[(δ_c/D(z) − δ_c) /
  √(2(S(m) − S0))] at three test points, |Δ| < 0.02.
- **K5:** X51's per-class median M200 reproduced (canonical) to 1e-6 relative; counts 175 SPARC, 63 groups, 82 dwarfs.
- **K6:** peak RSS < 1 GB; one thread.

## 4. MUTATE plan (env var X59_MUTATE; outputs written with a _MUTATE_<mode> tag)

- **X59_MUTATE=reverse:** the inequality reversed (retained iff ηΣ_coll < Σ_a₀(z_c)). **K1 must FAIL.** Exit 1.
- **X59_MUTATE=a0x10:** a₀(z) → 10 a₀(z). **K1 and K1b must FAIL.** Exit 1.
A MUTATE run whose named checks pass is a broken twin, and the lane reports it as such.
