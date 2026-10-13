# CFG723 FROZEN CRITERIA: "the carrier's mass is not what we think"

Committed ALONE, 2026-10-13, before any CFG723 script or number. Block CFG720–729 (owner chat reservation, LEDGER L484).
κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 m s⁻² never pooled; "cold energy"; not "theory closed"; no ΛCDM or
standard-MOND yardstick in any verdict. Light compute: analytic + one small script (`cfg723.py`, sympy/numpy, one process,
< 1 GB, `nice -n 10`). No downloads. Literature numbers (abstract-level) are marked PROVISIONAL and never decide a
framework verdict alone.

## Question
CFG722 showed the P-field bound charge has zero net mass and no inertia, so CFG624's required cold mass needs a collisionless
carrier. The owner suspects the carrier's mass is "not the mass the way we think". Can cold energy's gravitating, inertial,
collisionless mass arise WITHOUT ordinary rest mass of quanta? Candidates A–D below, each judged against the same
requirements, which are derived from the data first (owner addition, incorporated before freezing).

## 0. What the evidence says cold energy is (data first; only raw-data / committed lanes)
- E1 **Amount.** Ω_c/Ω_b = 5.364 at recombination (CMB pair; native 5.376; BBN bracket 5.48). Measured, not derived
  (THEORY_v3 §2; CFG642, CFG360: no derivation / baryon-tie no-go).
- E2 **Collisionless and inertial.** In the Bullet the lensing mass follows the galaxies, not the stripped gas; an
  instant-response, inertia-free phantom is excluded (CFG624 G3 Z_B +7.9; CFG621/623).
- E3 **Gravitates where the law alone is short.** X-COP clusters miss 3.09 / 2.75 M_b at 0.8 R500 without it (CFG624 G2);
  cluster cores need ×1.8 inside ~1 Mpc (CFG687); Local Group timing (CFG624 G4a); cosmic shear / web (CFG624 G5).
- E4 **Follows the law around galaxies.** Inside galaxies the settled cold energy IS the law's phantom inside the census
  edge; SPARC rms 0.100 / 0.101 dex is identical with or without it (CFG624 G1 identity).
- E5 **Settled-only in bound systems; amount per system bounded.** Capacity Σ̄_c ≤ a₀/πG; the tethered profile is the law's
  (CFG722 B8, CFG695 S4). Extra mass in massive cores is open (CFG713–715 early types; CFG720 overflow).
- E6 **No non-gravitational signal.** The framework adds no coupling to light or matter (CFG659: P has no visible signature;
  every matter channel below threshold). No detector signal is on the record; the literature null results are PROVISIONAL
  context only (no lane).
- E7 **Not the P bound charge** (CFG722 Q1: net mass 2.7e-12 of M_c; no ballistic transport).

## Requirements (operational; each candidate scored on each)
- **R1 amount (E1).** The candidate's mass density at 1+z = 1100 must reach ρ_c,req = 5.364 ρ_b(z), with
  ρ_b = (Ω_b/Ω_DE) ρ_DE, ρ_DE = a₀²/(κ²c²G) (framework-native; per footing), Ω_b = 0.0493, Ω_DE = 0.686 (CFG624's declared
  values), and be pressureless there (c_s² ≤ 1e-6, CFG635 G2). PASS iff ratio ≥ 0.5; FAIL if < 0.5 or not pressureless.
- **R2 collisionless + inertial (E2).** Inertial mass density (ρ+p)/c² > 0 and ≈ gravitating density; ballistic transport
  (a translating lump exists); multistream (not a single-valued potential flow, CFG288 / L374); Bullet optical depth
  τ = (σ/m) Σ_x < 1, with Σ_x = 0.1–0.3 g cm⁻² (PROVISIONAL bracket, abstract-level).
- **R3 cluster budget (E3, E5).** Available mass density at the cluster scale (M_b = 1e14 M☉, r = 1 Mpc) and around galaxies
  (the law's phantom density at r = r_M = √(GM_b/a₀), M_b ∈ {1e9, 1e10, 1e11, 1e12} M☉) ≥ 0.5 × required. The ×1.8 core
  overflow is the open CFG720 question: a candidate that defers to it gets CONDITIONAL, not PASS.
- **R4 clusters like matter on large scales (E3).** w ≈ 0 after equality, multistream, and for wave-like carriers a quantum
  mass ≥ 2e-20 eV (CFG635 K1 record threshold); a comoving Jeans length below galaxy scale.
- **R5 equivalence principle.** Gravitational = inertial mass: couples only through the metric, T^{μν} dust-like (p/ρc²
  ≤ 1e-3 in halos); Eötvös-level only where the candidate couples to baryons non-gravitationally.
- **R6 constants.** Count every new constant beyond κ, ρ_DE, Ω_c/Ω_b (already inputs), γ / L*, I (already in the action).

## Candidates and the numbers each must produce (formulas fixed now)
- **(A) Field energy of P as the mass.** W(u) = (a₀/4πG)[−u − a₀ ln(1 − u/a₀)] (CFG695 S1) at the law's u = a₀g/(a₀ + g),
  g = ν_s(g_N/a₀) g_N; gradient term (γ/2)|∇P|² with γ = 2πG L*² (bounded by W (L*/r)²); total field energy bound
  g²/8πG. Report:
  A1 = W(u)/(ρ_ph c²) at r ∈ {0.1, 1, 10} r_M for the four masses and the cluster point (ρ_ph = the law's phantom density);
  A2 = ∫(W + g²/8πG) dV / (M_ph c²) inside r; A3 = cosmic: e_max = W(u = a₀/2) (a generous everywhere-saturated bound)
  vs ρ_c,req c² at z = 0 and 1+z = 1100; A4 equation of state of static field energy (sympy: p for a static gradient field).
- **(B) Condensate / superfluid medium with P as its displacement/phonon field.** B0 (sympy): with P ≡ −∫ j dt, continuity
  gives ∇·P = ρ − ρ̄ exactly, i.e. CFG722's ID identification is the kinematic identity of any medium. B1 degeneracy bound
  m ≤ m_deg = [ρ (2πħ)³ / v³]^{1/4} at r_M (ρ = ρ_ph, v = V_f = (G M_b a₀)^{1/4}). B2 thermalisation (needed for a
  condensate) σ/m ≥ 1/(ρ v t), t = 13.8 Gyr declared. B3 Bullet σ/m ≤ 1/Σ_x. B4 window exists iff B2 < B3. B5 Landau: the
  coherent sound speed vs the merger speed 4700 km/s (PROVISIONAL): superfluidity broken in the collision? B6 is ρ = m n
  (mass shell)? → decides "particle in disguise".
- **(C) Vacuum-displaced energy.** C1 = ρ_c,req(1+z = 1100)/ρ_DE0 (how much vacuum energy must have been given up by
  recombination); C2 late-conversion cap = 0.02 ρ_DE0 / ρ_c,req(0) (a₀ flat < 1% for z ≤ 5 ⇒ ρ_DE flat < 2%; a₀(z) law,
  PAPER7 v3); C3 (sympy) inertial density (ρ+p)/c² of vacuum = 0; C4 local reaction (astra local_sink_reaction identity
  δV/(ρ_c c²) = ηF(v/c)², |a_react|/g_ref = ηF): the η needed to deposit one rest mass at v = 200 and 1000 km/s, hence the
  force ratio.
- **(D) Other non-particle origins, only if R5-respecting.** D1 gravitating-without-inertia (the phantom): cite CFG624 G3 /
  CFG722 B2. D2 coherent oscillation energy of P itself: quantum ħω₀ with ω₀ = 2π/t_resp, t_resp from CFG722 B3
  (5e-5 – 0.28 Gyr, and the c_P = c corner), vs 2e-20 eV and its Jeans length; amplitude counted as a constant. D3 baryon
  binding energy: E_bind/(M c²) ~ (V_f/c)². D4 irrotational geometric dust (mimetic-type): single-valued flow (CFG288 / L374).
  D5 vacuum-induced rest mass m(ρ_DE): mass shell present; R5 only as homogeneous ρ_DE (flat to 2%).

## Verdict rule (per candidate)
- **VIABLE**: R1, R2, R4, R5 PASS; R3 PASS or CONDITIONAL; constants counted.
- **VIABLE-AS-PARTICLE-IN-DISGUISE**: as VIABLE, but the passing object has a mass shell, ρ = m n with quanta of mass m > 0
  (B6). Labelled honestly; "only a particle-like carrier works" is an allowed outcome.
- **FAILS**: any of R1, R2, R4, R5 FAILS (name it, with the number).
- A **general statement** is tested in the script (sympy): a cold (p ≪ ρc²), collisionless, multistream kinetic component
  obeys a Vlasov equation on a mass shell p² = −m²c²; with m = 0 every quantum moves at c (hot). If it holds, any candidate
  that passes R1+R2+R4 has a mass shell.

## Detection / interaction channels (owner addition; for every surviving candidate)
For each survivor list NEW framework-specific channels beyond plain gravity, with an order-of-magnitude size vs
current / near-term sensitivity, labelled **OBSERVABLE** (within current data), **FUTURE** (named near-term data), or
**BELOW THRESHOLD**. At least: finite supply / census edge in galaxy lensing; double-pulsar extra decay / c_P floor
(CFG659); Gaia DR4 vertical force (sealed pre-reg); Bullet-like merger lag (CFG720, t_resp); a lab / Solar-System channel
(honest: the law is off at Earth's g, fractional deviation ~ a₀/g_N); any coupling a condensate implies (self-interaction
σ/m, Landau velocity). Sizes come from committed lanes where they exist (cited) or from this script. Labels carry no
pass/fail weight.

## Controls / MUTATE
- K1: A1 recomputed with ρ_ph from the law must give M_ph(<r) = M_b(ν_s − 1) consistently (integral check ≤ 1e-6).
- K2: B0 identity holds to machine precision on a random 1-D flow.
- `CFG723_MUTATE=1` writes `_MUTATE` outputs: (M1) multiply A's field energy by (c/V_f)² (pretend field energy counted
  at rest-mass weight at the virial scale): A1 must rise to order one, showing A's failure is the (V/c)² factor (bites);
  (M2) give the vacuum w = 0 (ρ+p = ρ): C3's inertia must become non-zero (bites); (M3) set m = 0 in the mass-shell
  statement: the cold condition must fail (bites). MUTATE exits 0 iff every tooth bites (control PASS), else 1.

## Disclosure
Before freezing, back-of-envelope orders were held in mind for A (field energy ~ (V/c)² of rest mass) and C (needed vacuum
energy at recombination ≫ ρ_DE0). No script was run and no number was written into the record before this commit.
