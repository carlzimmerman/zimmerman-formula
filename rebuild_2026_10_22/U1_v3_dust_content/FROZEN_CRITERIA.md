# U1_v3_dust_content — FROZEN CRITERIA (2026-10-23, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF_E_AUDIT.md`.
κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle: the
cold sector is the Blanchet–Skordis K(Q) dust ("cold energy"). Never "theory closed"; never "the data favour the
framework". Compute: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS, minutes; no downloads; nothing larger than
64³. Inputs and their classes: `ASSUMPTION_LEDGER.md` (committed with this file).

## 0. The question

v3 (literal BS Khronon, J = J_x, K(Q) dust, covector P + γ_L) fails above (satellites +1.33/+1.30 dex, Coma UDGs
+1.12/+1.08 dex: S1; cluster cores ×1.5–1.9: F1; growth: F3, M1) and below (TDGs −0.59/−0.62 dex, DF2/DF4 −1.66/−1.74 ln,
MW K_z,1.1 92/97 vs 66.4: P4). Every tile was scored with the static AQUAL solution, i.e. dust = the AQUAL phantom.
Within v3's own equations: what range of dust content and total gravity can a system have, and is the range fixed by the
field equations or by history?

The PN system (L1 FROZEN_CRITERIA §1; BS24 eqs. 19, 25, 27, 29, 30 via BSK1):
Ξ = Φ − σ̇ + |∇σ|²/2; 4πGρ_τ = −[∇·(J_Y∇Ξ) + μ_K²Ξ], J_Y = μ(x) − 1, μ = x/(1+x), x = |∇Ξ|/a₀; ∇²Φ = 4πG(ρ_b + ρ_τ);
v_τ = −∇σ, ∂_tρ_τ + ∇·(ρ_τv_τ) = 0; dust Dv/Dt = −∇ψ, ψ ≡ Φ − Ξ; baryons Dv/Dt = −∇Φ.
Two readings of the dust are kept apart in every result: **LIT** (literal BS: single-stream, irrotational, σ continuous;
ρ_τ is whatever the hold equation gives, no sign requirement, C4) and **MS** (the posited multi-stream particle dust:
ρ_τ ≥ 0, collisionless, any velocity distribution; the hold equation gives Ξ from ρ_τ; L1's engine reading).

## 1. Derivation checks (sympy unless stated; residual 0 = exact)

- **D1 (ψ equation).** From the PN system: ∇²ψ = 4πGρ_b − ∇·[μ(|∇Ξ|/a₀)∇Ξ] − μ_K²Ξ (3-D, general functions), and the
  single-stream Euler equation is the gradient of the definition of Ξ (Bernoulli identity: ∂_t v + (v·∇)v = −∇ψ for
  v = −∇σ). PASS iff both residuals are 0.
- **D2 (literal statics).** A static single-stream khronon has σ = −Ct, so Ξ = Φ + C and the system reduces to BS24 Eq. 35.
  Checks: (i) the reduction (residual 0); (ii) the AQUAL flux x·μ(x) and the hold flux x·(1−μ(x)) are strictly increasing
  on x > 0 (derivatives > 0, sympy) ⇒ at μ_K = 0 the static solution is unique (monotone-operator argument, stated in the
  README); (iii) with μ_K ≠ 0: the constant C adds a uniform K-dust density −μ_K²C/(4πG) (residual 0) and the linear
  Newtonian-limit operator ∇² + μ_K² has the regular homogeneous solution sin(μ_K r)/r (residual 0) ⇒ the static
  solution is NOT unique (the zero-point freedom S4 scans). PASS iff (i)–(iii) hold.
- **D3 (hold cap).** For J_x the hold flux |(1−μ)∇Ξ| = a₀x/(1+x) < a₀ with limit a₀ (sympy). With μ_K = 0, Gauss on any
  closed surface ∂V gives G M_τ(V) < a₀|∂V|/(4π); a sphere gives GM_τ(<r) < a₀r²; a thin sheet gives Σ_τ < a₀/(2πG).
  The AQUAL phantom obeys GM_ph(<r) = a₀r²·g/(a₀+g) (identity, residual 0) and so sits inside the cap. Spherical total
  gravity is then bounded: g < g_N + a₀. PASS iff the limit, the inequality and the identity check.
- **D4 (spherical dust force).** With n = GM_b(<r)/(a₀r²), m = GM_τ(<r)/(a₀r²) (μ_K = 0): −ψ′ = −a₀[n − m²/(1−m)];
  ψ′ = 0 ⟺ AQUAL (m = m_ph(n) = (−n + √(n²+4n))/2); ∂(g − h)/∂m|_n = 1 − (1−m)⁻² ≤ 0 (held dust is self-repulsive at
  m > 0, exactly neutral at m → 0: the record's D-T). PASS iff residuals 0 and the sign holds on m ∈ (0, 1).
- **D5 (geometry-free virial).** For any dust distribution (any shape), the virial of the dust's own interaction is
  W_self = −∫ρ_τ x·∇(Φ_τ − Ξ) = W_Newton + (1/4πG)∫[3Λ(|∇Ξ|) − A|∇Ξ|²], A = 1−μ, Λ = ∫₀^y A s ds (Derrick identity,
  checked symbolically in spherical symmetry). With Thomson's theorem (∫|∇Φ_τ|² ≤ ∫A²|∇Ξ|²),
  W_self ≥ 0 follows if f(u) = 3(u − ln(1+u)) − u²/(1+u) − u²/(2(1+u)²) ≥ 0 for u ≥ 0.
  PASS iff the Derrick identity has residual 0 and min f ≥ 0 (series at 0 and ∞ by sympy, numeric minimum on
  u ∈ [1e-8, 1e8], 4000 log points, ≥ −1e-12).
- **D6 (linear response in a uniform field, x_e ≥ 0).** Linearising the hold about Ξ_host with |∇Ξ_host| = x_e a₀:
  ψ_k = −4πGρ_b,k/k² + 4πG c_θ(k) δρ_k/k², c_θ = (f_θk² − μ_K²)/((1−f_θ)k² + μ_K²), f_θ = μ_e(1 + L_e cos²θ),
  L_e = dlnμ/dlnx at x_e. Checks: (i) c_θ ≥ 0 for k² ≥ μ_K²/f_θ and every x_e > 0, θ (held dust self-repulsive below the
  scale √f_θ/μ_K); (ii) cold static ⇒ δρ_k = ρ_b,k(1/f_θ − 1) (the EFE phantom; at μ_K = 0); (iii) hot dust with any
  isotropic distribution (linear response ρ̄ χ: δρ = −ρ̄χ δψ, χ > 0) ⇒ δρ_k/δρ_ph,k = k_D²/(k² + k_D²) ∈ [0, 1] at
  μ_K = 0; (iv) cold stream at velocity V ⇒ δρ_k = 4πGρ̄ρ_b,k/(ω_p² − (k·V)²), ω_p² = 4πGρ̄f_θ/(1−f_θ), which equals
  BSK1 M4's k ≫ μ dispersion. PASS iff (i)–(iv) hold symbolically (and (i) on a numeric grid x_e ∈ [1e-4, 1e3]).
- **D7 (T3: held dust is weightless in a static host).** (a) In a static host Ξ_host = Φ_host + C, so ψ_host is constant
  and the host exerts no force on any dust element; (b) the hold force on a localised dust distribution of mass M_τ in a
  uniform host hold field equals M_τ∇Ξ_host (linear anisotropic medium: stress-tensor surface integral on a sphere, sympy;
  nonlinear: check N4); (c) momentum: a bound unit (baryons M_b + its dust M_τ) in a host field g falls at
  a = g·M_b/(M_b + M_τ). PASS iff (a)–(c) hold (residual 0).

## 2. Numerical checks (`u1_v3_dust_content.py`; one line per check; exit 0 iff all PASS)

Systems: S1's satellites (`S1_v3_hosted_small/s1_per_system.csv`, 45 canonical / 46 alt, Plummer, a = r_h) and Coma UDGs
(`s1_coma_per_galaxy.csv`, 9); P4's TDGs (`real_research/data/tidal_dwarfs/lelli2015_tdg.csv`, 6, uniform sphere as P4,
Plummer as variant) and DF2/DF4 (CFG657's constants as P4: Plummer, scale r12/1.30477). All isolated for N1–N3.

- **N0 (reproduce first).** (i) My algebraic isolated law at y_plummer reproduces S1's logG_iso0 per system (E-W:
  log10[g(r12)/g_bar], g_bar = G(M/2)/r12², r12 = 4a/3) to ≤ 1e-3 dex, both footings; (ii) P4's K9 law means
  (TDG −0.6904 / −0.7276; DF2 −1.7091, DF4 −2.1701 canonical) from the raw on-disk inputs to ≤ 1e-3; (iii) my
  central-value median of log_gobs_gbar − logG_emb0 over S1's systems is within 0.10 dex of S1's +1.130 / +1.075
  (S1 used MC + bootstrap; mine is central values). PASS iff (i)–(iii).
- **N1 (T1 verified: isotropic spherical dust, μ_K = 0).** T1 (README): if f = f(E) (any isotropic distribution, or
  f(E, L) with ∂f/∂L ≥ 0) and the baryons' AQUAL phantom density ρ_ph(r) is non-increasing, then M_τ(<r) ≤ M_ph(<r) at
  every r. For every system above (both footings): first check ρ_ph(r) is non-increasing on the system's grid; then solve
  self-consistent dust equilibria (spherical ODE in ψ and M_τ, my own code) for lowered-isothermal (King) and polytropic
  (n = 1.5, 3, 5) distributions on a grid W₀ ∈ {0.3, 1, 3, 6, 10} × 8 central densities (1e-3–1e4 × the system's central
  phantom density, log-spaced) × (King) 6 dispersions (0.03–30 × the baryonic Newtonian σ_N² at r12). Statistic: the
  maximum over all equilibria and radii of M_τ(<r)/M_ph(<r). PASS iff ≤ 1 + 1e-3 (integration tolerance). Configurations
  whose hold equation has no solution (cap reached) are counted and reported, not used.
- **N2 (counterexample search: anisotropy).** Same systems, f = L^{−2β}·g(E) with generalised-polytrope density
  ρ = K r^{−2β} Ψ^n, β ∈ {−1, −0.5, 0.1, 0.25, 0.35, 0.45, 0.49}, n ∈ {0.5, 1.5, 3, 4.5}, 8 central normalisations.
  Reported (not gated): the maximum of M_τ(<r)/M_ph(<r) over all, per β; the maximum gain at r12,
  Δ_an = log10[(M_b(<r12) + M_τ(<r12))/(M_b(<r12) + M_ph(<r12))]; and whether every excess sits where r^{2β}ρ_ph(r)
  increases (T1's generalised condition). Check N2: PASS iff (a) every β ≤ 0 run obeys the T1 bound (≤ 1 + 1e-3) and (b)
  every excess found at β > 0 lies inside the radius where r^{2β}ρ_ph stops increasing (the generalised T1).
- **N3 (counterexample search: time-dependent infall).** Spherical shell code (my own), 3000 shells with angular momentum,
  leapfrog, force −ψ′ = −a₀[n − m²/(1−m)] + j²/r³ from the instantaneous shell ordering (μ_K = 0); cap violations
  (m ≥ 1) recorded. Baryons: Plummer at y = the median S1 satellite y and the median TDG y (canonical). ICs: cold dust at
  rest with M_τ(<r) = λ·M_ph,iso(<r) inside 10 a, λ ∈ {0, 0.5, 1.5, 3} (λ = 0: a uniform cloud of mass M_ph,iso(<10a) to
  20 a), tangential dispersions {0, 0.5} × local v_c. Run 40 deep-MOND dynamical times at r12. Reported: time of first
  shell crossing (end of LIT validity), maximum and late-time (last quarter, time-averaged) M_τ(<r12)/M_ph(<r12).
  Check N3: PASS iff the code conserves energy to ≤ 1e-2 over the run in the λ = 1, cold, MUTATE-free control and the
  λ = 1 cold control stays at its equilibrium (|ratio − 1| ≤ 0.02). The physics readings are §3.
- **N4 (T3 in the nonlinear regime).** 3-D periodic box 64³, nonlinear hold ∇·[(1−μ(|∇Ξ|))∇Ξ] = 4πG(ρ_τ − ρ̄) with a
  uniform imposed gradient |∇Ξ_host| = x_e a₀ (x_e ∈ {0.03, 0.3, 3}), ρ_τ a Plummer blob with internal field from 0.1 to
  10 x_e; fixed point with Anderson mixing, converged to 1e-8. Statistic: the hold self-force |∫ρ_τ∇δΞ|/(M_τ x_e a₀).
  PASS iff ≤ 1e-3 in every case (so the total hold force on the blob is M_τ∇Ξ_host, and with D7(a) the host's net force
  on the blob is zero). Also reported: the fraction of negative mass in the linear-EFE AQUAL phantom of a Plummer
  (forbidden for MS dust, allowed for LIT).
- **N5 (velocity and acceleration: the hosted tiles).** Native, zero-knob criteria (README derivation):
  (A) acceleration (T3 + D4 + shell theorem): dust is held only inside r_h where the isolated law's internal total field
  g_int(r) ≥ x_e a₀ (x_e = S1's / P4's host field), and the bound unit then falls at a = g·M_b/(M_b + M_τ,held);
  (S) streaming (LIT only; D6(iv), BSK1 M6): dust is held only inside r_f where 2GM_b(<r)/r ≥ V², V = record speed
  relative to the host's held khronon (MW satellites: 3-D Galactocentric speed from LVD proper motions, astropy, G2's
  frame; M31 satellites and systems without proper motions: the host law circular speed at d — PROXY; TDGs: host law
  circular speed at D_p — PROXY; DF2/DF4: CFG657's V_coll/2 = 179 km/s, bracket [125, 225]; Coma UDGs: Coma β-model
  circular speed at d_mean — PROXY).
  Branches per system: **B0** dust-free (the branch whose fall acceleration equals the host's: Newton);
  **B1-MS** held dust = isolated phantom inside r_h (upper bound; L★ = 0); **B1-LIT** inside min(r_h, r_f).
  Statistics exactly as the tiles: satellites median over systems of log_gobs_gbar − logG_branch (E-W), bootstrap sd over
  systems (4000, seed 23); Coma ⟨E⟩, se (CFG933), z_stat, σ_sys rerun on each branch (M★ ±0.2 dex, σ ±15 %, D ±5 %),
  z_sys; TDGs r̄ ± se (P4 stats5); DF2/DF4 r = E_obs − E_pred (ln). Check N5: PASS iff every branch is computed for every
  system on both footings and B1 ≥ B0 holds per system (held dust ≥ 0).
- **N6 (MW: the most round hot dust v3 can hold).** McMillan17 baryons (P4's `rho_mcm`, re-implemented): monopole
  M_b(<r), my own ring quadrature for in-plane g_R(R₀) and K_z(R₀, 1.1 kpc) of the baryons. Round dust at the T1 bound
  (M_τ(<r) = M_ph(<r) of the baryon monopole: the most any isotropic round dust can hold): v_c(R₀) and K_z(R₀, 1.1) and
  χ²_Kz over the 43 Bovy–Rix MAPs (P4's errors). Check N6: PASS iff my Newtonian K_z(R₀, 1.1) of the baryons is within
  1 % of P4's ring-quadrature value and v_c, K_z, χ² are computed on both footings.
- **N7 (when μ_K can be dropped).** ε_K(r) = μ_K² r³|Ξ_ref|/(3 G M_ph(<r)) (ratio of the μ_K² flux to the J flux),
  |Ξ_ref| = 3 v_c,host² (generous; host law circular speed) for hosted systems, 3 v_c(r)² isolated; at r12 per system and
  at r = 0.3, 1 Mpc for a 1e14 M☉ cluster, at μ_K = 14.8 h/Mpc (BS cap, h = 0.6856) and BS24's own 0.015637 Mpc⁻¹.
  "Negligible" ⟺ ε_K ≤ 0.01. Also the zero-point offset |ΔΞ| that would make the uniform K-dust equal to a system's
  needed density. Check N7: PASS iff computed for all systems (a reported quantity, not a verdict).
- **N8 (resources).** Peak RSS < 1 GB.

## 3. Readings (frozen)

**Bounds (part a).** For each of LIT, MS-isotropic, MS-anisotropic, flattened, EFE, μ_K, infall: "bound holds",
"bound holds with excess ≤ X dex" (X = N2/N3's maximum), or "bound fails (counterexample: …)". A bound is called a
theorem only if it has a proof in the README and survives N1–N4.

**Velocity (part b).** If the B1 held dust at the record speeds is below 10 % of the static phantom inside r12 for a
tile's median system, the reading is "v3's own dynamics strips that tile's dust"; the reference frame is stated from
D7 (the local khronon flow; inside a held host, the host's held dust).

**Consequence table (part c), per tile and footing.** With D = data and the branch offsets:
- **NATIVE**: the branch v3's own dynamics selects without a history choice (B0 for systems observed to fall with their
  host's baryons — bound satellites, tidal-tail TDGs, trail dwarfs, cluster members) is within 2σ of the data.
- **HISTORY-DEPENDENT**: some branch allowed by v3's equations (static, B0, B1-MS, B1-LIT, the MS hot/anisotropic bound
  maxima, at r ≳ μ_K⁻¹ the self-gravitating K-dust) reaches the data within 2σ, but only for a named history.
- **STRUCTURAL**: the data lie ≥ 3σ outside the whole range [min branch, max branch] on both footings, i.e. no history
  inside v3 fixes it. The README then names which v3 ingredient would have to change (J, μ_K, the dust coupling, or the
  law) and why.
- Between 2σ and 3σ: "TENSION", stated as such.
Cluster cores: this lane computes only N7's ε_K and the bound's domain; the static μ_K solve is S4's (cited, not redone).
The MW tile uses N6 (MS) and P4's static AQUAL (LIT).

## 4. Mutation (`U1_MUTATE=1`; outputs `*_MUTATE.out`, `*_results_MUTATE.json`)

The dust coupling is changed to dust feeling −∇Φ (no hold force on dust; Ξ still from the hold): D4's self-force becomes
attractive, D7(c) gives a = g (no lag), and N1's maximum ratio must exceed 1 (self-gravitating dust can exceed the
phantom). D4, D7 and N1 must FAIL; exit 1. D1–D3, D5, D6, N0 unchanged.

## 5. What a result here cannot say

No verdict on growth (F3/M1/L1), on cluster profiles (S4/F1), or on the MW rotation curve beyond R₀. Nonlinear EFE solves
of the static tiles are S1's/P4's (read-only references, not redone). B1 is an upper bound on held dust (L★ = 0; the
isolated internal field defines r_h). Speeds labelled PROXY are record-derived, not measured.

## AMENDMENT A1 (PRE-RESULT for the production run; written after a smoke run on 2 of 137 N1/N2 cases, 2026-10-23)

The smoke run (scratch copy, not committed) exposed implementation problems. No PASS line, threshold, input or reading
changes. Changes:
1. **N1 grid made harder, not easier.** The frozen King/polytrope grid never came close to the bound (max ratio 0.48–0.58
   in the smoke cases), so it is a weak test of T1. Added (reported separately, same PASS line): near-cold King
   configurations s² ∈ {1e-4, 1e-3, 1e-2} σ_N² with W₀ ∈ {10, 20, 30}, and polytropes n ∈ {2, 2.5} (ρ ∝ r⁻² and r⁻²·⁵ in
   the baryons' Kepler tail, the families that can approach the bound at large r). The N1 check uses the union; the
   frozen-grid maximum is also printed. Also reported (not gated): the maximum over r of the gravity gain
   log10[(M_b + M_τ)/(M_b + M_ph)](<r).
2. **N2 statistic bug.** The reported "max gain at r12" was initialised at 0 and so hid negative values; it now starts at
   −∞. Added (reported): the maximum over all r of the same gain, because N2's excess sits near the centre where both
   masses are small (ratio is a poor measure of gravity there).
3. **N4 Q targeting.** The blob charge Q was set by an approximate formula and overshot the frozen internal-field range
   (one smoke case reached 16.5 x_e, where the self-force was 5.8e-3). Q is now found by bisection so that the internal
   hold-field maximum equals 0.1, 1 and 10 x_e, as frozen. The smoke value at 16.5 x_e is disclosed here; the threshold
   1e-3 is unchanged and a FAIL at 10 x_e will be reported as such (with a reported, ungated resolution test at a
   smoother blob).
4. **N6 sign bug.** The ring formula for g_R returned the outward component (the smoke run crashed on v_c² < 0). Fixed to
   the inward magnitude; the frozen finite-difference sanity check of the formula is kept.
5. **N3/N5 additions (reported, not gated).** N3 prints the dust's binding depth against the baryons' Newtonian well;
   N5 prints, per tile, the median baryonic Newtonian escape speed from the centre (v_esc,N = √(2GM_b/a) for a Plummer)
   next to the observed σ, because D4 implies ψ′ ≤ g_N,b: spherical held dust is bound by at most the baryons' Newtonian
   well.
6. RuntimeWarnings from masked overflow in dead configurations are silenced.

## AMENDMENT A2 (PRE-RESULT, 2026-10-23; coordinator request; written before any number of this part): the field-galaxy frame

**Question.** Part (b) gives: held dust only where 2GM_b(<r)/r ≥ V_rel² (LIT, stationary streaming), and only where the
internal field exceeds the khronon acceleration of the surroundings (T3, any reading). What do these imply for ISOLATED
FIELD GALAXIES (SPARC RAR, BTFR, MeerKAT)? What is V_rel there, and does v3 keep the held phantom?

**Frame (derivation, F1).** The khronon congruence is the dust velocity field; there is no separate cosmic frame locally.
Linearised on FRW (L1 §1 kernels, J_x): baryons feel ∇Φ (all mass), dust feels ∇ψ. The baryon–dust differential
acceleration per comoving mode is ∇Ξ_k = s(k,a)·∇Φ_τ,k with s = k²/(k² + a²μ_K²) (the dust's own potential, times the
kernel). sympy check: residual 0, and limits s → 1 (k ≫ aμ_K: the full dust potential is differential) and
s ≈ (k/aμ_K)² (k ≪ aμ_K: co-flow). Bulk flows enter only through their k > aμ_K part.

**Checks of the new script `u1_a2_field_frame.py` (one line each; exit 0 iff all PASS; `--mutate` via U1_MUTATE=1):**
- **F1** the sympy statements above.
- **F2 (linear relative velocity, z = 0).** Reproduce first: this lane's copy of F3's two-fluid ODE on F3's background A
  gives F3 K4 `bsk2_ai0.001` σ₈ ratio 0.39080 at μ = 14.79771 h/Mpc to ≤ 1e-3 relative. Then, on model B (F3's CLASS
  settings; dust-limit P(k), FRAMEWORK-NATIVE in the dust limit), ICs δ_b = δ_τ = a at a_i = 1e-3, BSK2/J_x kernel:
  rms baryon peculiar velocity σ_b and rms baryon–dust relative velocity σ_rel = rms[H₀(δ_b′ − δ_τ′)/k], with the share
  F(k) = (δ_b′ − δ_τ′)/δ_b′, for μ_K ∈ {BS24 own 0.015637 Mpc⁻¹, cap 14.8 h/Mpc, M1 411 h/Mpc} and k_max ∈ {0.3, 1, 10, 50}
  h/Mpc. Linear theory is not valid beyond k ≈ 0.3 h/Mpc at z = 0 (labelled). Also quoted: the decaying
  post-recombination streaming velocity (EXTERNAL, Tseliakhovich & Hirata 2010: ≈ 30 km/s at z ≈ 1020, ∝ 1/a).
  PASS iff the reproduction holds and all cells are finite.
- **F3 (SPARC hold radii).** All 175 `real_research/data/sparc_data/*_rotmod.dat`, V_bar² = |V_gas|V_gas + Υ_d V_disk² +
  Υ_b V_bul² (Υ_d = 0.5, Υ_b = 0.7, SPS labels; spherical approximation GM_b(<r)/r ≈ V_bar², labelled): per point
  V_hold = √2·V_bar. For V_rel ∈ {1, 3, 10, 30, 100, 300, 600} km/s: fraction of RAR points with V_hold < V_rel (phantom
  not held there, LIT), and the median over galaxies of r_f/R_last. a₀-free (both footings identical). PASS iff 175
  galaxies are read.
- **F4 (acceleration criterion, environment).** For the Chae-matched SPARC galaxies (P4's file and recipe: g_e =
  law(10^primary e_N · GE_CHAE)), the fraction of RAR points with g_obs < g_e, both footings: these are the points whose
  dust cannot follow the galaxy IF the environment's khronon acceleration equals its gravitational field (held
  surroundings); and the same with the field scaled by s at the cap for a source at D = 1 Mpc (unheld, linear). PASS iff
  computed.
- **F5 (a moving-member class: Ursa Major).** SPARC galaxies with distance method 4 (UMa members): V_rel = √3 × the
  dispersion of their cz (RAW, `sparc_a0_environment_table.csv` / `sparc_master_clean.csv`); their points beyond r_f; the
  mean log(g_obs/g_law) of those points against non-UMa points in the same g_bar bins (reported, no gate). If the UMa
  members' outer points sit on the RAR, the held-group branch (members lose their phantom) is contradicted by data.
  PASS iff computed.
- **F6** peak RSS < 1 GB.

**Readings (frozen).**
- "KEPT" for field galaxies if, at the BS cap, every linear σ_rel estimate (k_max ≤ 1 h/Mpc) is below V_hold at ≥ 95 %
  of SPARC points, and F4's held-surroundings fraction is ≤ 5 %.
- "LOST for class X" if a class's V_rel exceeds V_hold at a majority of its RAR points.
- "DEPENDS ON <assumption>" whenever the reading flips between the stated alternatives (held vs unheld surroundings;
  BS24's own μ_K vs the cap; whether held dust is dragged). The favourable alternative is never chosen.
- Board tiles that would change are listed for every LOST or DEPENDS reading.
