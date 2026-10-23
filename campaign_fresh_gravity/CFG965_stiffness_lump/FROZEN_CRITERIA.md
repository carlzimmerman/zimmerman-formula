# CFG965 FROZEN CRITERIA: the stiffness-bound cold lump (NEW_ANGLES_SCOUT NA-3)

Block CFG960–969 (LEDGER row "CFG960–969 RESERVED": CFG965 = NA-3). Written and committed alone, before any lane script
exists and before any lane number is computed. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled.
Cold energy is real gravitating mass, not a particle species. Not "theory closed". Nothing here can say the data favour the
framework. Field equation: the action's own AQUAL μ = x/(1+x); no QUMOND and no additive-EFE recipe anywhere in this lane.

## 0. The question

NA-3 premise: if cold mass that **self-gravitates** (its linear self-gravity is not cancelled) also carries the record's
stiffness pressure p = (γ/2)ρ² = πG L*² ρ², γ = 2πG L*², then an isolated cold lump is an n = 1 polytrope,
ρ ∝ sin(kr)/(kr), k = √2/L*, with edge R = πL*/√2 ≈ 2.22 L* whatever its mass. Read against CFG870's core (104 pc) or
CFG877's edge (≈ 199 pc) this would give a second, independent L*.

**Part A (derivation).** Does any formulation on the record give that structure? Primary target, per the coordinator
(2026-10-23): the screened theory v3 (`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1: Khronon τ, spatial covector P,
J_x so that the static limit is AQUAL μ = x/(1+x), BS24 K(Q) dust of mass μ_K, stiffness −(γ_L/2)(D·P)², γ_L = K L*²/2,
K = 4πG). Also checked, each with a row in the output: canonical S2 + S3 (ID) + S4 (THEORY_CANONICAL 10-14, 10-16, 10-18,
10-21 draft); CFG938's covariant parent (adopted χ-tidal stiffness (3γ/4K²)τ_μντ^μν, and its rejected local form
ε_int = (γ/2)ρ²); CFG939's single medium; CFG941's repairs R1, R2, R3n, R3θ, R3ℓ; class A (CFG541/638, CFG882);
CFG848's two-population functional; SCT (CFG953); v4 (AeST + γ_L), whose spherical statics S4 shows equal v3's with μ_K → μ.

**Part B (fit).** Runs only if Part A passes (§3). It is frozen here in full so that it cannot be shaped after Part A.

The lane does **not** address the lump's **mass** (supply: CFG823/930/959, E3, P1). Whatever the class, that stays open.

## 1. Definitions (frozen)

- **NA-3 structure.** In some regime that contains kL* ~ 1, the cold mass obeys the linear (WKB) dispersion
  ω² = ρ(γk² − 4πG) up to corrections that move the marginal wavenumber by < 10 %, and the isolated static lump obeys
  γ∇ρ = −∇Φ_self, so its edge is R = πL*/√2 with L* the record's stiffness length **alone** (no other constant).
- **Untethered / self-gravitating.** The −4πGρ Jeans term survives at kL* ~ 1: no tether or hold term cancels it.
- **Live formulation.** An action or equation set on the record whose static limit is the framework's law (AQUAL
  μ = x/(1+x), equivalently S2's g_N = g²/(g+a₀)) and which its own lane has not marked rejected, excluded, NOT REPAIRABLE,
  or a MUTATE control. Rejected variants and controls get a row and a number, but cannot pass Part A.
- **Allowed range of a second constant.** For v3's μ_K: BS24's admissibility cap μ_K ≤ 14.8 h/Mpc (THEORY_V3_DRAFT line 48),
  the only theory-internal bound on the record. The growth requirement μ_K ≥ 411 h/Mpc (M1, line 75) and the literal-K BBN
  line μ_K ≥ 1.84e8 h/Mpc (Q6, line 79) are reported alongside, with no verdict weight. Conversion to Mpc⁻¹ uses h = 0.674,
  with the bracket h ∈ [0.55, 0.73] reported; it cannot move a ratio to the cap by more than 25 %.

## 2. Part A computations (script `cfg965.py`, sympy + small numpy/scipy)

Reproductions (K, all must pass in the main run):
- **K1** NA-3 hand numbers (scout appendix A3): θ = sin ξ/ξ solves Lane–Emden n = 1 (sympy); R/L* = π/√2 = 2.2214;
  half-density radius 1.3403 L*; M = 4π²α³ρ_c, α = L*/√2; L* = 77.6 pc from 104 pc (half-density) and 90.0 pc from
  200 pc (edge); M = 3.9e6 / 6.1e6 M☉ at ρ_c = 0.6 M☉ pc⁻³. Tolerance 1 % on the hand numbers, 1e-9 on identities.
- **K2** the NA-3 hydrostatic equation from E[M] = ∫[−GM²/2r² + γ(M′)²/(8πr²)] dr (sympy Euler–Lagrange):
  γρ′ = −GM/r² ⇒ ∇²ρ + (2/L*²)ρ = 0.
- **K3** H4's v3 dispersion from H4's linear PN system (Poisson, hold Hessian M_θ, stiffness, continuity, Bernoulli,
  ρ_τ = ∇·P − μ_K²Ξ/K): ω² = ρ_τ[k²/χ − K], χ = k²/(KM_θ + γ_L k²) + μ_K²/K; μ_K = 0 form Kρ_τ(M_θ − 1 + L*²k²/2).
  Residual exactly 0.
- **K4** H4 at μ_K = 0 equals CFG938 S5a, ω² = γρk² + Kρ[R′cos²θ + (R/u)sin²θ], via M_L − 1 = R′ and M_T − 1 = R/u with
  u = a₀x/(1+x). Residual exactly 0.
- **K5** CFG888 S4: (γ/2)|∇P_L|² = πG L*² ρ² for longitudinal P (sympy). **K6** CFG888 S1: the on-shell single-mode
  Lagrangian under ID has no C² (self-gravity) term.

Derivations (D):
- **D1 v3 exact nonlinear statics, μ_K = 0, spherical.** From the static v3 equations (Ξ = φ + C, Poisson, P equation with
  the full hold a₀u/(a₀ − u), u = K|P|), derive γ_L D′ = u²/(a₀ − u) − g_N,b, D = ∇·P (sympy). Integrate a baryon-free lump
  outward from D(0) = D_c, D′(0) = 0 for central fields such that max u/a₀ ∈ {1e-3, 0.05, 0.2, 0.5}; record whether D ever
  falls (an edge) or rises monotonically (no lump). Confirm that with baryons it is the screened law R(u) = g_N + γρ′.
- **D2 v3 with μ_K, linear statics.** The marginal (ω = 0) condition of K3 gives the static wavenumber k_s(μ_K, L*, M_θ)
  and the regular bounded profile D ∝ sin(k_s r)/(k_s r) (check that ρ_τ ∝ D). Report: (i) the limits μ_K L* ≫ 1 and ≪ 1;
  (ii) the value s* of μ_K L* at which k_s = √2/L* (the NA-3 radius), at M_θ = 1; (iii) the μ_K needed for the dwarf
  targets R_edge = π/k_s = 199 pc (CFG877 r_t, read from its JSON) and R_half = 1.8955/k_s = 104 pc (CFG870 r_c, from its
  JSON), at L* ∈ {D10 central 21.68 / 22.85 pc, E4 native 28.85 / 29.12 pc (both from D10's JSON), 90 pc, 2.04 kpc} and
  M_θ ∈ {1, 1 + x_cl, (1 + x_cl)²}, x_cl = G M_cl/(r_t² a₀) from CFG877's JSON, per footing; (iv) the elasticity
  d ln R / d ln L* at that point; (v) the lump scale at the BS cap. All in h/Mpc and as ratios to 14.8 and 411 h/Mpc.
- **D3 CFG941 R1 (rejected repair, W_full → W_rem).** Euler–Lagrange of E[M] with W_rem and the stiffness:
  γρ′ = −u + u²/(a₀ − u). Integrate isolated lumps to ρ = 0; report R/L* against central u/a₀; it must tend to π/√2.
- **D4 CFG938 local-EOS form + tether off.** ε_int = (γ/2)ρ² gives p = (γ/2)ρ²; with Newtonian self-gravity this is NA-3
  exactly (sympy). Report as rejected variant (CFG938 §3.3(a): BBN-excluded if the medium exists then) plus an unwritten
  switch (CFG938 B1 UNTESTED; THEORY_CANONICAL 10-18 note: S4 not derivable).
- **D5 formulation table.** One row per formulation in §0: carries the stiffness on its own density? linear self-gravity?
  isolated-lump equation; lump exists? live? Each row cites file:line, and the script checks that every cited string is
  present in its file (targeted files only, no repo-wide search).

## 3. Part A outcome rule (frozen)

- **A-PASS**: a live formulation has the NA-3 structure. Part B runs.
- **A-PARTIAL**: a live formulation gives a self-gravitating, stiffness-bound lump whose scale needs L* **and** one more
  constant, and the value that constant needs for the dwarf targets lies inside its allowed range (§1). Part B then runs
  with that scale and reports the second constant, not an independent L*.
- **NO FORMULATION**: otherwise, including (a) the structure appears only in rejected variants or controls, (b) it needs an
  unwritten term or switch, or (c) a second constant is needed outside its allowed range. **Part B is then not run**
  (report only), and the lane class is NO FORMULATION.

## 4. Part B (only if Part A is A-PASS or A-PARTIAL)

- Data and likelihood: CFG880's 83 LVD dwarfs, Υ_V = 2, gas counted, split-normal errors, CFG880's code paths.
  σ_pred² = σ_law² + G M_lump(<r12)/(3 r12), M_lump(<r) = M_i [sin kr − kr cos kr]/π for r < π/k, M_i for r ≥ π/k.
- Free: one global L* (or the A-PARTIAL constant), and M_i per dwarf as CFG880/877 treat σ_x: hierarchical ln M_i with a
  fitted mean and intrinsic scatter. Both footings, separately.
- Compared by ΔBIC (k counted honestly) with CFG880's universal-σ (s_int = 0) and hierarchical fits and CFG877's finite clump.
- Checks: compact (r12 < 312 pc) vs large (r12 ≥ 312 pc, CFG876's set) L* fitted separately, z of the difference; Sextans'
  extended mass to ~1.7 kpc (CFG884, PROVISIONAL); the globular floor (D10 21.68 / 22.85 pc; E4 28.85 / 29.12; CFG820 record
  23.64 / 24.48).
- K: reproduce CFG880's stored ŝ_int (0.380 / 0.380) and scatter Λ (277.5 / 304.2), and CFG877's stored group E values,
  to 1 %. MUTATE: plant n = 1 lumps with L* = 60 pc in mock dwarfs (CFG880's errors) and recover L* within its 95 % interval;
  outputs `*_MUTATE.*`.
- **Kills:** L*'s 95 % interval outside [24 pc, 2 kpc]; ΔBIC > +10 against the best existing fit; compact vs large z > 3.
  Class DERIVES THE CLUMP SIZE iff none fires; PARTIAL iff only the compact/large split is 2 < z ≤ 3; FAILS otherwise.

## 5. Controls for Part A (frozen)

- **MUTATE** (`CFG965_MUTATE=1`, outputs `cfg965_MUTATE.out`, `cfg965_results_MUTATE.json`): remove the critical quadratic
  of the hold/tether (v3 hold a₀u/(a₀−u) → u²/(a₀−u), i.e. M_θ → M_θ − 1, the c₂ = 0 case of CFG941 theorem D-T). The
  detector must then find the NA-3 structure in v3 (D1 lump edge → πL*/√2 at small u, to 1 %), K3/K4 must FAIL (the record's
  dispersions are no longer reproduced), and the outcome rule must flip away from NO FORMULATION. Exit 1 by design.
- Main run exits 0 iff K1–K6 and the D-stage internal checks (sympy residuals exactly 0; ODE tolerances ≤ 1e-8 relative)
  pass.
- Compute: one process, `OMP_NUM_THREADS=1 nice -n 10`, an in-script RSS guard aborting above 1 GB, minutes. No downloads.

## 6. Disclosure (before freezing)

Read before writing this file: the scout's NA-3 section and "already tried" list; doors_push E1, E2, E3, E4, D8, D10;
THEORY_V3_DRAFT; rebuild H4 and U1; CFG888 (S1, S4, S5); CFG938 (§3.2–3.4, §6–7); CFG941; CFG939's stiffness rows;
CFG953's rules; CFG848's header; CFG638; THEORY_CANONICAL 10-14 S2–S4, 10-16 S4, 10-18 note, 10-21 draft rows.
From that reading the record already says that the tethered/held cold sector has no linear self-gravity (CFG888 S1,
CFG938 S5a, CFG941 D-T, U1 D4, H4 at μ_K = 0). Hand sketches made before freezing, with no script and no number: the D1
equation γ_L D′ = u²/(a₀ − u) − g_N,b, the D2 quadratic for k_s², and the D3 equation for R1. So the expected Part A outcome
is NO FORMULATION; the lane's new content is the script-checked derivation, the v3 μ_K-dependence and the numbers in D2.
