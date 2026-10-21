# CFG958 FROZEN CRITERIA: one energy channel, cold energy ↔ dark energy, for SCT's body energy (C-E), CFG935's settling sink and CFG955's relaxation reservoir

Block 950–959 (LEDGER reservation b1ce41cf3f). Date 2026-10-21. Agent lane. Committed ALONE, before any script, run or number.
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² never pooled. Cold energy is the framework's own component: its mass is
required, no particle species. Framework-native inputs only. Not "theory closed". Nothing here can say the data favour the framework.

## 0. Not blind: what was read before freezing, and the hand estimates

Read in full or in the relevant sections before writing this file: CFG953 (README, DERIVATION, criteria R6, `cfg953.py` S-En and toy
code, `cfg953_results.json` S-En and toy energies), CFG954 (LEDGER row), CFG955 (README, DERIVATION §1, §8 L7, §10), CFG935 (README,
DERIVATION), CFG930 (README), CFG932 (README), CFG630 (README, `cfg630.out`, `native_anchored` JSON block), CFG542 (README), CFG131 and
CFG195 (LEDGER rows), the pure-vacuum local-reaction report `sol61_push/local_sink_reaction_2026_10_11/REPORT.md` (read only),
CFG689 (README, `cfg689.json` header; Read tool only), CFG956 (criteria, A1, `cfg956_K.out`; no result yet), THEORY_CANONICAL
2026-10-18, LEDGER rows CFG770 (Cassini Q2 ceiling 5.2e-27 s⁻²) and CFG832 (L* window).

Hand estimates written before freezing (disclosed; they set no line):
- **E1** the cosmic deposit is ≲ 1e-5 of ρ_DE (all cold energy at the cluster value of S-En) and ~1e-7–1e-6 at native settled
  fractions, so far inside CFG689's band.
- **E2** a deposit held locally inside an NGC 3198-like body gives δV/V̄ ~ 1e-5 (uniform in r_e) or ~1e-3 (∝ body density, at
  30 kpc). If a₀ reads the LOCAL vacuum this moves the law by ~3e-6 or ~2e-4, above the 1e-6 line. If a₀ reads the cosmic mean, the
  only local effect is the deposit's own dust-like gravity, ≲ E_int/(M_c c²) ~ 2e-7.
- **E3** SCT's events relabel dust without changing its distribution function, so they produce no entropy and need a work-type
  (zero-entropy) reservoir; a finite-temperature heat bath would be violated by the merger draw. CFG955's K-T and CFG935's bath
  need entropy absorption and cannot use a coherent dark energy.
- **E4** a w = −1 interacting vacuum has no propagating degree of freedom, so no ghost and no gradient instability; the record's
  canonical receiver (CFG542) is singular at w = −1 and anti-damped on energy draws.
- **E5** expected class: CONDITIONAL.

**Coordinator message received before freezing (2026-10-21, after CFG955 landed at 115054648):** test whether CFG955's Clausius
argument (a coherent, zero-entropy dark-energy partner cannot absorb entropy on the cooling branch) also applies to SCT's E_int
bookkeeping. That question is test **T-S** below. It is part of the frozen text, not an amendment, because nothing had been computed.

## 1. The hypothesis and the channel (declared)

The reservoir that SCT (C-E), CFG935 (settling sink) and CFG955 (relaxation reservoir) each need is dark energy itself, through a
covariant exchange that is active only where the cold sector reorganises (body formation, mergers, reshaping/relaxation).

**Primary receiver: the interacting vacuum (IV).** Signature (−,+,+,+), V an energy density, x⁰ = ct:

    T_V^{μν} = −V g^{μν}            (intrinsic w = −1 exactly, at every point and time)
    Q^ν ≡ ∇_μ T_V^{μν} = −∇^ν V      (the exchange current is fixed by V's gradient: CFG131, CFG195, sol61 report)
    ∇_μ (T_c + 𝒮′)^{μν} = −Q^ν = +∇^ν V,   ∇_μ T_b^{μν} = 0   (baryons untouched)
    ⇒ ∇_μ (T_b + T_c + 𝒮′ + T_V)^{μν} = 0   (total stress-energy conserved)

𝒮′ = Σ_q Σ′_q − T_c,lab is CFG953's source with each body's internal energy removed (E_int ≡ 0 in Σ′_q). Every increment CFG953 books
into E_int,q (conversion, merge, reshape: R4, R6, R7) is booked instead as vacuum energy: ∫ΔV d³x = ΔE_int,q.

**Deposit variants.**
- **CH-L (local, primary).** V = V̄(t) + Σ_q δV_q(|x − X_q|), δV_q = E_q w_q, ∫w_q d³x = 1, supported in r ≤ r_e,q, carried with body q
  (spherical about its centroid; retarded updates as CFG953 R8). Per-owner rule: the reaction +∇δV_q acts on body q's 𝒮 only and is
  held by body q's stress (p_hold = δV_q − δV_q(r_e)). Profiles: **P-σ** w ∝ σ_q (the deposit sits where the body's mass is) and
  **P-U** w uniform inside r_e (most spread out that a body can hold).
- **CH-G (global).** V = V̄(t) only, homogeneous in the cosmic frame; the deposit is carried from the body to the cosmic mean by a
  radial relocation current in 𝒮 propagating at c. This is a new non-local rule, not in CFG953's R0–R9 (named condition **C-G**).

**a₀ readings** (a₀ = ½ c √(G ρ_DE), ρ_DE = V/c²): **a0-cos** — a₀ reads the cosmic-mean vacuum V̄ (the volume average, lumps
included); **a0-loc** — a₀(x) reads the local V(x). Neither is primary: the record states a₀(z) only for the background.

**Other receivers, for T4 only (reported):** **R-φ** CFG542's canonical scalar φ̈ + 3Hφ̇ − c²∇²φ + V′(φ) = Q/φ̇; **R-F** a minimal
dark-energy fluid with constant w, rest-frame c_s² = 1, exchange along the cold 4-velocity, Q^μ = Q u_c^μ.

## 2. Tests (every line fixed here; both footings scored separately; simple kernel primary, ν_mono reported)

### T1 exchange: exact absorption, conservation, momentum (sympy + CFG953 toy)
- **T1a** ∇_μ(−V g^{μν}) = −∇^ν V on Minkowski and on flat FRW (sympy, all components).
- **T1b** event algebra: for a conversion, a merge and a reshape step, the CFG953 increments booked as ∫ΔV give Δ(K + W + E_V) = 0
  identically (sympy), with E_V ≡ ∫(V − V̄₀) d³x over the bodies' lumps.
- **T1c** momentum: T_V^{0i} = 0 in every inertial frame (sympy boost), so the vacuum carries no momentum; ∫Q^i d³x = 0 for a compact
  spherical δV_q; with the reaction added to body q's balance under the per-owner rule, CFG953's relocation term
  R = D̈_s − ∫ρ_s g stays identically 0 (sympy, CFG953's two-blob construction plus the vacuum force term).
- **T1d** composite identity: T_V + T_hold with p_hold = δV equals δV u u/c² (pure dust), and a rigidly translating lump is
  conserved (sympy).
- **T1e** toy: CFG953's toys E (dt 2e-3, t_end 40) and M (dt 2e-3, t_end 30), code copied verbatim, with E_V booked in place of E_int:
  |Δ(K + W + E_V)|/|E₀| ≤ 1e-3 and equal to CFG953's E_int-booked residual to ≤ 1e-9; dP/P_scale, dL/L_scale ≤ 1e-13.
- **T1 PASS** iff T1a–e all pass. Reported: locality class of Q (pointwise identity vs non-local deposit rule).

### T2a cosmic size
- Hard ceiling, no mass function: Δρ_DE/ρ_DE(z) ≤ ε_max ω_c (1+z)³ / ω_DE(z), with ε_max = max over CFG953's S-En grid (both footings)
  of E_rel/(M_c c²), ω_c and ω_DE(z) from CFG689's primary best fit (`cfg689.json`, nodes interpolated linearly in z). Then
  |Δ ln a₀(z) − Δ ln a₀(0)| ≤ ½ max(ceiling(z), ceiling(0)).
- Line: at each CFG689 node z = 1.0, 1.2, 1.5, 2.33 the ceiling on |Δa₀/a₀| must be < 0.1 × CFG689's 68% half-width there.
- Reported: (i) native PM-anchored bracket F_sw(z) × (ω_c/ω_DE) × ε(M_b) at the PM resolution mass and at M_b = 1e14, with F_sw from
  CFG630's K6 (CFG424 switch-on mass fractions, N512); (ii) CFG630's own native-anchored ledger (JSON) rescaled by SCT's E_rel/(M_c V_f²)
  over CFG630's c_W; (iii) CFG956's wave bound if its result exists when the main stage runs; (iv) sign of the shift.
- **T2a PASS** iff the ceiling passes at all four nodes on both footings.

### T2b local size (CH-L P-σ, CH-L P-U, CH-G; each under a0-cos and a0-loc; both footings)
- E_int of NGC 3198 = CFG953's S-En recipe at its own M_b (Υ 0.61, spherical-equivalent) on its census domain (point-mass baryons, as
  S-En). ε ≡ E_int/(M_c c²).
- **NGC 3198:** max over the 43 radii of |g_chan/g_law(ḡ; a₀ footing) − 1| < 1e-6. g_chan includes the deposit's dust-like gravity
  G δM_V(<r)/r² (T1d) and, under a0-loc, the body built pointwise with a₀(r) = a₀ √(1 + δV(r)/V̄). P-σ: δV(r) = E_int σ(r)/M_c with σ
  from the 43-radius M_σ (finite differences); P-U: δV = E_int/((4π/3) r_e³). CH-G: δV ≡ 0 locally; its in-transit 𝒮 energy density
  P/(4πr²c), P = E_int/t_P, t_P ∈ {1, 10} Gyr, gravitates; it does not change V.
- **Slip:** s = CFG953's worst (1.3548e-5, alt cluster) + s_chan ≤ 1.9e-5, s_chan = anisotropic stress of T_V + T_hold over ρc² (T1d).
- **EFE:** under a0-loc, CFG953's satellites H1–H3 (CFG882 Plummer dwarfs) at 50/100/250 kpc inside the 6e10 M☉ host's lump:
  |Δ log₁₀ g_law| at each satellite's Plummer radius ≤ 0.082 dex (δ_c). Under a0-cos it is 0 by construction (own-body lumps).
- **Cassini:** traceless tidal tensor of the MW-like (6e10 M☉) lump at 8 kpc ≤ 5.2e-27 s⁻² (Park+2026 via CFG770); under a0-loc,
  CFG770's |Q2|/ceiling 3.5e-6 × (1 + δa₀/a₀)³ < 1 (exponent 3 declared generous).
- **Headroom (graded under a0-loc only):** V̄ + δV > 0 at all NGC 3198 radii including a merger draw of 0.207 |E| (CFG953 toy fraction)
  with the same profile. Reported for UFD, Draco-, Fornax-, SPARC-dwarf-, MW- and cluster-class bodies at declared radii.
- **T2b PASS for (variant, reading)** iff NGC 3198, slip, EFE, Cassini (and headroom under a0-loc) all pass on both footings.

### T3 sign and ordering
- Sign: E_V(t) − E_V(0) = −Δ(K + W) (state function); formation releases (S-En > 0 for every M_b), mergers draw. Report the sign of
  the cosmic Δρ_DE and of a₀(z)/a₀(0) − 1.
- Ordering (CFG930/932): capacity ratio C(M) = V̄ (4π/3) r_e³ / E_rel per class (UFD-c, UFD-e, Draco-like, Fornax-like, SPARC dwarf
  1e9, MW-like 6e10, group 1e12, cluster 1e14), the analogue of CFG930's E_SN/ΔE. **AVOIDS** if min C ≥ 10 (the channel is never
  energy-limited, so it imposes no mass ordering); **REPRODUCES** if C < 1 somewhere with the faint systems best supplied.
- **T3 PASS** iff AVOIDS (both footings). Reported: the channel then gives no handle on the excess family.

### T4 stability (graded on the primary IV)
- IV: no time-derivative of δV in T_V or in the exchange (no kinetic term ⇒ no ghost, no gradient instability; δV is slaved to the
  events); the composite perturbs as dust (T1d); |1 + w_eff| = |Q|/(3H V̄) from the T2a ceiling deposit rate ≤ 1e-4.
- Reported (and MU3): R-φ perturbation friction 3H + Q/φ̇² with φ̇² = (1 + w)V̄, its sign on draws; R-F velocity response
  ∝ Q/((1 + w)ρ_DE c²) and its w → −1 divergence; whether CFG689's best-fit nodes cross w = −1.
- **T4 PASS** iff the IV items all hold.

### T-S entropy (coordinator question)
- **S1 conversion:** the event changes labels only, so the total dust distribution f (labelled + unlabelled) is unchanged and
  −∫f ln f is unchanged; bodies and vacuum carry zero entropy ⇒ ΔS_tot = 0 with a zero-entropy dark energy (sympy). Reported: the
  labelled sector's gravitating energy is identically 0, i.e. it is an entropy store at zero temperature.
- **S2 merger draw D > 0:** zero-entropy dark energy ΔS = 0; a heat bath at any finite T_R gives ΔS_tot = −D/T_R < 0 (sympy).
- **S3 reshape:** deterministic and reversible (work), ΔS = 0.
- **S4** (contrast, = K6) CFG955 K-T: on the cooling branch the reservoir must absorb entropy ≥ −Q/T_J > 0.
- **S5** CFG935: the drift's work to a coherent partner (CFG542 Pb) is admissible; the bath (relaxation to σ_J²) is S4's case.
- **T-S PASS (SCT)** iff S1–S3 hold with a zero-entropy dark energy.
- **V2 (one channel for all three):** YES (all parts of SCT, CFG935 and CFG955 admissible) / **ONLY WHERE NO ENTROPY IS EXCHANGED**
  (SCT and the class-A drift admissible; CFG955 K-T and the CFG935 bath not) / NO (SCT not admissible).

### T5 verdict on C-E
- **DERIVED:** some variant passes T1, T2a, T2b, T3, T4 and T-S on BOTH a₀ readings with no posit beyond the hypothesis (a variable
  vacuum exchanging with 𝒮) and SCT's inherited conditions (C-c, C-MR, C-DF).
- **CONVERTED:** T1 and T-S pass and some variant passes T2–T4, but only under a named reading (a0-cos) or a named extra structure
  (C-G); total energy is then conserved exactly, with the conditions named.
- **NOT CLOSED:** T1 or T-S fails, or every variant fails T2a, T2b, T3 or T4 on every reading.

## 3. Classes
- **CHANNEL CLOSES THE BOOKS** iff T5 = DERIVED and V2 = YES.
- **CONDITIONAL** iff T5 ∈ {DERIVED, CONVERTED} and not CLOSES. The class line names every condition and V2.
- **FAILS (where)** iff T5 = NOT CLOSED, naming the failing test(s).

## 4. Controls
**K (exit 0 required):**
- K1 CFG953's S-En table (E_rel/|W_f| and E_rel/(M_c c²), 13 masses × 2 footings) recomputed with CFG953's functions copied verbatim:
  relative difference ≤ 1e-9 against `cfg953_results.json`.
- K2 (main stage) CFG953's toy E_int: conversion −0.22681, reshape −4.74e-5 (E) and merge −0.20693, reshape −0.00924 (M), and dE,
  dE_mech, reproduced to ≤ 1e-9 in units of |E₀|.
- K3 CFG689 band nodes from `cfg689.json` equal 0.913 [0.762, 1.027], 0.925 [0.762, 1.048], 0.942 [0.706, 1.115], 0.909 [0.325, 1.212]
  at z 1.0 / 1.2 / 1.5 / 2.33 to ≤ 5e-4.
- K4 CFG953's NGC 3198 law with no channel: max deviation ≤ 1e-12; r_e 453.9 / 412.9 kpc to ≤ 0.1 kpc.
- K5 the sol61 report's numbers: reaction/reference ηF = 0.63212 at t = τ; deposited/rest 2.8133e-7 (200 km/s) and 7.0333e-6
  (1000 km/s), to 5 significant figures.
- K6 CFG955 L7 identity dS_d/dt − Q/T_J = (3/2)(ρ/τ)(T_J − T)²/(T T_J) (sympy).

**MUTATE (separate `_MUTATE` outputs; exit 1 when every tooth bites):**
- MU1 exchange off (no E_V booking): the toy energy error returns, |ΔE|/|E₀| ≥ 0.2 for E and M (CFG953 Mu5: 0.249 / 0.217).
- MU2 wrong-sign exchange (the vacuum receives −ΔE_int): toy |ΔE_tot|/|E₀| ≥ 100 × the channel-on residual (conservation broken).
- MU3 wrong sign / draw branch with the record's canonical receiver R-φ: perturbation growth rate |Q|/φ̇² − 3H > H₀ for NGC 3198- and
  cluster-class deposits at 1 + w ∈ {0.01, 0.1} (stability violated).
- MU4 reaction not held (per-owner holding removed; the vacuum gradient acts as an unbalanced force density on the body's mass):
  |∇δV|/(σ g) at NGC 3198 ≥ 0.1 for P-σ (the sol61 O(1) reaction returns).
- Reported, no tooth: the IV wrong-sign mutation's effect on stability and ordering; a shared (not per-owner) reaction on satellites.

## 5. Compute, outputs, wording
- One process at a time, one core (`OMP_NUM_THREADS=1 nice -n 10`), in-script 1 GB RSS guard. Nothing downloaded. Other lanes'
  files are read only (CFG689 through its committed JSON, as CFG956 does). No LEDGER, THEORY_CANONICAL or other-lane edit.
- Stages: `CFG958_STAGE=K` → `cfg958_K.out/json`; `CFG958_MUTATE=1` → `cfg958_MUTATE.out/json`; main → `cfg958.out/json`.
- κ = ½ FITTED; footings never pooled; no particle species; never "theory closed"; never "the data favour the framework"; a FAIL is
  reported as plainly as a pass.
