# AG6A: can a "capacity of the vacuum" set the switch-on scale, i.e. derive κ = ½? (frozen criteria, committed alone)

Written 2026-10-20, before any AG6A script, run or number. κ = ½ FITTED; Z ≡ κ, Z = 2√(8π/3) = 5.7888 (never ≈ 21);
both footings (9.3603e-11 canonical / 1.1312e-10 alt), never pooled; no dark-matter particle species; not theory closed.
Small jobs only (OMP_NUM_THREADS=1, nice -n 10, < 1 GB, minutes) beside the live 1024³ run.

**Division of labour.** AG6B (dbcaeba9e) owns the *shape* question: which microscopic medium saturates at u → a₀/n and
whether physics picks n (Langevin, Brillouin, Landau, Born–Infeld, Langmuir, Deser–Levin, ...). AG6A owns only the *scale*:
does any capacity principle fix the capacity u_sat (equivalently a₀ = n·u_sat, κ) from the vacuum, with no inserted constant?
AG6A does not re-score shapes or SPARC.

**Disclosure.** The candidate list was drawn up after hand algebra during planning. In particular I expect, but have not
computed: the causal horizon of a uniformly accelerated observer in dS₄ has area 4πL² for every acceleration; the Einstein
heat-capacity function is ≤ 1; (ρ + p) = 0 for Λ; the DESI DR2 rows cross w = −1 below z ≈ 0.6. Every one of these is a
check in the script, with a MUTATE that must flip it. No number below the "targets" block has been computed by a script.

## 1. Targets (identities, not results)
- Capacity family (AG4, AG6B): u² + n g_N u = a₀ g_N; capacity u_sat = a₀/n; half-saturation s = a₀/n²; a₀ = u_sat²/s.
- In de Sitter units (c = 1): a₀ = κ√(Gρ_Λ), H_Λ = √(8π/3)·√(Gρ_Λ). So a₀/H_Λ = κ/√(8π/3); κ = ½ ⇔ a₀ = H_Λ/Z.
- Milgrom 1999 (dS–Unruh ΔT): F(a) = √(a² + H²) − H: n = 2, u_sat = H, a₀ = 2H ⇔ κ = 2√(8π/3) (numerically = Z).
  Ratio Milgrom/framework a₀ = 2Z (both n = 2); ratio of capacities = Z for the action's own n = 1 law (AG4).
- Data band for κ (quoted, not re-fitted): CFG493 κ_Λ = 0.417 ± 0.095 (primary); MNRAS v3.1 route A 0.450 ± 0.073.

## 2. Candidate mechanisms (frozen)
**M1. Horizon-information capacity (QFT in curved space / holography).** The vacuum's resistance is the share of the
observer's horizon capacity (Bekenstein–Hawking entropy of its causal horizon) that its acceleration consumes; it switches
on where that share becomes O(1).
- M1.1: build dS₄ ⊂ R^{1,4}; the uniformly accelerated orbit X⁰ = R sinh(τ/R), X¹ = R cosh(τ/R), (X²,X³,X⁴) fixed with
  |X⊥|² = L² − R²; 5D acceleration A = 1/R; 4D proper acceleration a = √(A² − 1/L²) (sympy).
- M1.2: the causal horizon of the full orbit = boundary of its causal past = {X⁰ = X¹} ∩ dS₄; compute its induced area A_h(a).
- M1.3 (control): Euclidean period of the orbit's Killing flow ⇒ T = A/2π = √(a² + H²)/2π (Deser–Levin, record WW/agentYY).
- M1.4 (control): flat limit L → ∞ gives the Rindler horizon plane at proper distance 1/a.
- **Line:** if A_h is symbolically independent of a, no capacity is consumed by acceleration and M1 sets NO scale
  (M1 = SCOPED NO-GO, geometric). If A_h depends on a, compute the half-consumption acceleration and κ.

**M1b. Thermal (KMS/Tolman) capacity: the bath's heat capacity sets the switch-on.** Inertia from the bath energy seen
along the orbit, F(a) = f(A) − f(H), f = the mean energy per degree of freedom at T = A/2π in acceleration units,
normalised so that f′(∞) = 1 (Newtonian limit).
- B.1 slope theorem (sympy series): deep law F ≈ f′(H) a²/(2H) ⇒ a₀ = 2H/f′(H) ⇒ κ = 2√(8π/3)/f′(H).
- B.2 required slope for κ = ½: f′(T_GH) = 2Z = 4√(8π/3); temperature windows δ₁ = √(1 + 3/(32π)) − 1 (a = a₀) and
  δ₂ = √(1 + 3/(128π)) − 1 (a = a₀/2, the n = 2 rest scale).
- B.3 equipartition bound: for a bath of harmonic modes, f′(T) = C(T)/C_classical = Einstein function x²eˣ/(eˣ−1)² (one mode)
  or the Debye function (1D, 3D) — check ≤ 1 everywhere (analytic limit + dense grid). If it holds: a₀ ≥ 2H, κ ≥ 2√(8π/3) in
  this class, i.e. the framework sits a factor 2Z below the class floor.
- B.4 power family F_k = (A^k − H^k)^{1/k}, k = 1, 2, 3, 4: deep exponent 2/k; MOND (exponent 2) iff k = 1 (Milgrom).
- B.5 escapes (reported, not tuned): a Schottky (two-level) peak, max C/k = 0.4392 per level; a phase transition at T_c.
  Count the free constants each needs to reach f′(T_GH) = 2Z.
- **Line:** DERIVATION-grade only if a member with no inserted constant gives f′(T_GH) = 2Z and exponent 2. Otherwise
  SCOPED NO-GO with the bound as the reason.

**M2. Holographic / Bekenstein polarization capacity.** The vacuum's saturation polarization P_sat (mass per area,
u_sat = 4πG P_sat) is the capacity of the horizon's degrees of freedom. Pre-declared menu (ħ must cancel in each):
- (i) P_sat = [1/(4ℓ_P²)] × kT_GH/c² (BH entropy density × one thermal quantum per cell);
- (ii) Padmanabhan surface DOF 1/ℓ_P² × ½kT_GH/c²;
- (iii) CKN/Schwarzschild-saturated vacuum ball (2GM_vac(R)/c² = R): its surface gravity c²/2R;
- (iv) Bekenstein bound saturated by the static-patch vacuum (S = 2πER/ħc = A/4ℓ_P²): E/R → acceleration GE/(c²R²);
- (v) thermal Compton dipole crossover g_c = kT_GH/(m·ħ/mc) (scale only; its shape belongs to AG6B).
For each: u_sat/H_Λ (or a_c/H_Λ), a₀ for n = 1 and n = 2, κ, and the π-grade of κ² (rational × π^k).
- **Line:** DERIVATION-grade only if an entry gives κ = ½ exactly with no choice. The fraction of entries inside the CFG493
  1σ band is reported as a base rate, never as evidence.

**M3. Enthalpy (inertial-density) capacity of the dark-energy medium (fluids / cosmology).** A medium resists
displacement through its inertial mass density (ρ + p/c²); the vacuum's capacity is u_sat = q c √(G(ρ + p/c²)).
- C.1 Λ: (ρ + p/c²) = 0 ⇒ u_sat = 0 for every q and every length (exact).
- C.2 DESI DR2 flat w0waCDM rows as recorded in sonnet55_push/puzzle_32pi/p13b_desi_dr2_a0z.py (37b55b149; Table 5 of
  arXiv:2503.14738 read from the HTML table, not re-read here): κ_eff(0) = q√(1 + w0) for q ∈ {1, √(4π/3), √(8π/3), √(4π)}
  (bare G, ball, Friedmann, Jeans), error from w0's marginal σ only.
- C.3 dataset independence (q = 1): χ² of the four κ_eff(0) about ½ and their spread.
- C.4 second prediction: a₀(z)/a₀(0) = √[(1 + w(z)) ρ_DE(z) / ((1 + w0) ρ_DE0)] (CPL); the crossing z_× where 1 + w = 0;
  values at z = 0.2 and 0.3.
- **Line ("forced"):** q = 1 fixed a priori AND all four κ_eff(0) within 1σ of ½ AND z_× > 2.5 for all four (a₀ real at every
  redshift the record uses). Any failure ⇒ M3 = SCOPED NO-GO, naming which. In-repo a₀ at z ≈ 0.2–0.5 is not calibrated
  (CFG260/281; CFG255 lens-z split not possible), so the z-collapse is reported as NOT DIAGNOSTIC against data.

## 3. Gates for every mechanism
- **G-forced:** no free or tuned constant; a constant picked from a menu after the target is known counts as free.
- **G-identity:** the equality must not hold by construction (e.g. Z = cH/a₀ = √(32π/3) for any ρ with H² = 8πGρ/3).
- **G-κ:** κ computed exactly. DERIVATION requires κ = ½ as an exact symbolic result. κ in the data band but ≠ ½ is reported
  as a data-compatible alternative, not as a derivation of ½.
- **G-second:** a second prediction independent of the a₀ value (a₀(z), the capacity u_sat, or n), testable.
- **G-record (controls, must reproduce):** CFG47 κ_match = √(8π/3)/n; F1 / equation book Milgrom a₀ = 2cH_Λ (factor 2Z);
  X2 (ρ + p) = 0; k03 κ = √(8π/3)/(2π) = 0.461.

## 4. Verdict rule
- **DERIVATION:** one mechanism passes G-forced, G-identity, G-κ (exact ½) and G-second.
- **CANDIDATE:** κ = ½ (or the band) with exactly one free choice or a post-hoc selection.
- **SCOPED NO-GO:** every mechanism fails for a stated structural reason.
- **NOT DIAGNOSTIC:** the computation cannot decide.

## 5. Script, outputs, controls
- `ag6a.py` (sympy + numpy, seconds): sections M1, M1b, M2, M3, each check written as `check(name, measured, ok, reading)`;
  outputs `ag6a.out`, `ag6a_results.json`; exit 0 iff every check holds.
- `AG6A_MUTATE=1` → `ag6a_MUTATE.out`, `ag6a_results_MUTATE.json`; must exit 1 (bites). Mutations:
  - Mu1 (M1): horizon replaced by the sphere of radius 1/A ⇒ the a-independence check must fail.
  - Mu2 (M1b): f(A) = A + (1 − 2Z)H²/A (inserted transcendental) ⇒ the "no natural member reaches 2Z" check and the
    "equipartition bound holds" check must both fail.
  - Mu3 (M2): add entry u_sat = H/(2Z) by hand ⇒ the "no exact ½" check must fail.
  - Mu4 (M3): all four rows set to w0 = −0.75, wa = 0 ⇒ the dataset-spread and crossing checks must fail.
- README.md with the verdict, numbers, what is new against the record, caveats. Results are NOT committed by this lane.

κ = ½ FITTED; not theory closed.
