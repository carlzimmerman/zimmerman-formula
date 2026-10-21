# CFG947 FROZEN CRITERIA: option 3, a non-local (causal) parent whose non-relativistic limit is the class-A engine

Committed alone, before any CFG947 script, derivation output or number. Block 940–949 (LEDGER reservation row CFG940–949).
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², scored separately, never pooled. Cold energy (its
mass is required; no particle species is added). Framework-native inputs only; no ΛCDM yardstick enters a verdict. Not
"theory closed" whatever the outcome; nothing here can say the data favour the framework. Any change after this commit is a
dated, labelled amendment.

## 0. The target: the class-A engine's non-relativistic equations

Read with the Read tool only: the CFG650 engine (forces(), cover_peaks(), cover_balls(), x_supply(), expel_m3(); modules
M1, M2, M3 = the T1x / T2x combination), CFG654 (the same engine with native inputs; NC1x), and the lineage CFG518 → 524 →
527 → 596. Production settings (run_650.py): 1024³, L = 100 Mpc/h, RMIN_PHYS = 0.78125 Mpc/h comoving.

| id | engine equation (continuum reading of the code) |
|---|---|
| E1 | every particle (one species, baryons and cold energy in fixed proportion) feels −∇Φ, with ∇²Φ sourced by δ + S (code: φ_k = −(3/2)(Ω_m/a) δ_k/k² − S_k/k²); universal coupling |
| E2 | S = e − comp, nonzero only on catchment cells |
| E3 | catchment = union of balls of radius r_ON around resolved peaks. Peak = local maximum of δ (3-cell filter) with δ ≥ 3(τ − ε), τ = (Δ_ta(z) − 1)/3. r_ON = largest R on a 14-point grid [dx, 8 Mpc/h] with mean enclosed (1 + δ) ≥ Δ_ta(z). Resolved iff r_ON ≥ RMIN_PHYS |
| E4 | phantom s_ph = −∇·[(ν_mono(\|g_b\|/a₀) − 1) g_b], g_b = f_b × the PM field of the retained-baryon density (tab[code](1 + δ); with M2 the condensed per-particle deposit), mean removed (k = 0), over the whole box |
| E5 | tidal switch f_sw = clip(½ + (λ₂ − τ)/(2ε), 0, 1), λ₂ the middle eigenvalue of δ's tidal tensor |
| E6 | deficit e = f_sw · 1_edge · max(s_ph − s_c, 0) · 1_catch, s_c = (1 − f_b)(1 + δ) |
| E7 | edge = union of balls of radius x·r_ON, x = min(r_M / ln(1 + f_r f_b/(1 − f_b)) / r_ON, 1), r_M = √(G M_b,ret/a₀), M_b,ret = f_r f_b M_ta |
| E8 | zero-sum: comp = q_C s_c on the shell (catchment minus edge), q_C = Σ_C e / Σ_shell s_c, capped at 1 (e scaled by 1/q_C when capped). C = connected component, or with M1 the own host (each cell goes to the resolved peak with the smallest d/r_ON) |
| E9 | census f_r = fret_of(log₁₀ M_ta[M⊙/h]): 0.10 below 12.5, linear to 0.55 at 13.5, then to at most 0.90. M2: per-particle condensed fraction f_d, irreversible, raised at census refreshes (a latched label) |
| E10 | M3: census non-retained baryons removed from the source and re-placed Gaussian-smoothed (σ = r_ON of the class); mass conserved |
| E11 | the census and catchment state is refreshed every 10th force call (time discretisation) |

**Disclosed before any number.** E4 is the pointwise QUMOND phantom of the *global* retained-baryon field. It therefore
contains the baryonic external-field effect of every neighbour, inside and outside the catchment. The wording "own-baryon
phantom per collapsed structure" (CFG941 §4 and this lane's brief) is the record's galaxy-scale round rule (CFG888 Q1, the
material reading of CFG478), not the engine's formula. Both are scored: the engine's formula in (g), the no-EFE rule in (f).

## 1. Common chassis (every candidate)

  G_μν = (8πG/c⁴)(T^b + T^c + 𝒮)_μν,

with these pieces:
- S_GR, baryons, and cold dust. The dust is CFG938's matter sector (comoving labels, F = −mc²n) *without* W, the τ-stiffness, χ
  or λ: there is no tether.
- **(i) Geodesic matter.** Baryons and cold dust are geodesic (E1).
- **(ii) Conservation by construction.** The 𝒮 mass current is J_s^μ = ∇_ν𝒬^{μν}, with 𝒬 antisymmetric and supported on the
  domains. In the NR limit:
  - ρ_s = −∇·𝒫 (𝒫 the electric part, compact per domain);
  - j_s = ∂ₜ𝒫 + ∇×M.

  The stress Π_s is the completion that solves ∂ₜj_s + ∇·Π_s = −ρ_s∇Φ. For (e) the isotropic choice is declared, vanishing
  at the domain boundary.
- **(iii) Causality.** Every inverse operator is the retarded one (□_ret⁻¹). Labels and latches evolve by first-order ODEs
  along matter worldlines.
- **(iv) Declared, not hidden: no action principle.** Retarded non-local equations are not the Euler–Lagrange equations of
  any action, because varying a non-local action gives the time-symmetric kernel. Each parent is therefore a set of causal
  effective field equations, with conservation imposed by (ii). This is a cost; it is not scored as a failure. MUTATE Mu2
  shows what the action (time-symmetric) version does.

## 2. Candidates (declared before computing)

**N1: labelled domains (Lagrangian, historical).**
- **Labels.** Peaks are maxima of the cold medium's density smoothed at L* (24 pc primary, 1 kpc bracket: CFG820's window, an
  existing record length). The turnaround criterion is E3's, with no RMIN. A matter element receives, fractionally, the label
  of the first turned-around ball it lies in. Labels are never reassigned (rule β).
- **Phantom.** Each domain's phantom comes from its *own* retained baryons:
  - □_ret Φ_D = 4πG f_r ρ_b,D;
  - F_D = (ν(\|∇Φ_D\|/a₀) − 1)∇Φ_D.
- **Domain rules.** Deficit, edge and zero-sum draw follow E6–E8, with the domain's own M_b,ret and M_ta. The draw acts on the
  domain's labelled cold, with q ≤ 1.
- **Merge rule M-R (a declared cost, scored with and without).** A sub-domain's label merges into its host's when the
  sub-domain's baryons are no longer self-bound (bound fraction < ½).

**N2: constraint-field domains (Eulerian; the instantaneous switch made dynamical).**
- **Turnaround potential.** A retarded ψ with □_ret ψ = 4πG(ρ_m − Δ_ta(z)ρ̄_m).
- **Domains.** A domain is the region about a minimum of ψ where the enclosed mean is ≥ Δ_ta (E3's criterion written as a
  field statement).
- **Per-domain fields.** A constraint field χ_D with □_ret χ_D = 4πG f_r ρ_b 1_D, and a multiplier μ_D enforcing zero-sum
  per domain (E8).

Two realisations:
- **N2-E (engine-verbatim).**
  - Domains are balls of radius r_ON about ψ minima, resolved iff r_ON ≥ RMIN_PHYS (declared a constant of the theory).
  - M1 partition; phantom from the global retained field (E4); E5–E10 verbatim.
- **N2-B (basins).**
  - Domains are watershed basins of ψ smoothed at L* (24 pc; 1 kpc bracket); no RMIN.
  - Phantom from the domain's own retained baryons, unsmoothed; E5–E8 otherwise.

**N3: domain-free, Deser–Woodard type.** No labels, no partitions, no per-domain integrals.
- 𝒫 = s · [F_ph − F_c]/(4πG), where:
  - F_ph = (ν(\|g_b\|/a₀) − 1)g_b from the global retained field, mean removed;
  - F_c = −∇Φ_c, the cold's own Newtonian field;
  - s is a smooth gate of local values of retarded scalars (the turnaround overdensity field and λ₂).
- Then ρ_s = −∇·𝒫 = s(ρ_ph − δρ_c) − (F_ph − F_c)·∇s/(4πG).
- Zero-sum is automatic: the source is a divergence and s → 0 outside the gate. There is no clip and no edge.

## 3. Tests and pass lines

### (a) Static law

**Inputs.**
- NGC 3198: the record's rotmod file, Υ = 0.61, spherical-equivalent m_N = r²g_bar/G (as CFG938/941).
- Kernels: the S2 simple law (g_N = g²/(g + a₀)) as primary, ν_mono as secondary.
- The domain is the isolated galaxy's catchment:
  - M_ta from the census fixed point M_b,ret = f_r f_b M_ta, with f_r = fret_of and M_b,ret = M_b(< last radius);
  - r_ON from the engine's own M_ta(R, Δ) formula with Δ_ta(0) = 11.83 (CFG654's native table; the engine's 0.315 inside
    M_ta is an inherited constant, flagged);
  - r_e from E7.

**Cold profiles (declared).**
- P-S, the settled limit: ρ_c = 0 inside r_e; the catchment's cold lies in the shell ∝ r⁻² between r_e and r_ON. Primary.
- P-I, the isothermal identity: ρ_c = ρ_ph inside r_e. Secondary.
- P-X: ρ_c = 2ρ_ph. A diagnostic of condition C-ρ (ρ_c ≤ ρ_ph).

**Pass lines.**
- **a1.** max \|g/g_law − 1\| ≤ 1e-6 at the 43 radii, both footings, under P-S and P-I, both kernels.
- **a2.** \|g/g_law − 1\| ≤ 1e-6 at deep points y = g_N/a₀ ∈ {1e-2, 1e-3} lying inside r_e. NGC 3198's baryons are treated
  as a point mass beyond the last radius. Points outside r_e are reported.
- **a3 (reported, no class weight).**
  - The asymptotic V⁴/(G M_b a₀) beyond r_e.
  - The forced-edge test T-E (§4).
  - The supply N = M_c,catch/M_b against CFG803's N_min (3 canonical / 4 alt in the primary range; 16 / 24 at all radii).

**By construction, stated now so that a PASS is not over-read.** Inside r_e with ρ_c ≤ ρ_ph, a class-A source *is* the law's
deficit. So a1 and a2 check the implementation, the cap and the edge placement. Their physical content lies elsewhere:
- the edge location;
- condition C-ρ;
- N1's label heterogeneity, computed for co-spatial label fractions f ∈ {0.01, 0.1, 0.3, 0.5} and N ∈ {2, 10, 100} equal
  labels, without M-R;
- N2-E's RMIN;
- N3's gate.

### (b) FRW background
- **Line.** 𝒮 ≡ 0 on exact FRW for each candidate:
  - domain criteria are unmet at δ = 0;
  - labels are unset;
  - per-domain fields are unsourced;
  - N3's mean-removed field is zero.
- **Consequence.** T_total = dust, with w = 0 and isotropy checked symbolically (sympy, as CFG941 K2).
- **PASS** if all hold exactly.

### (c) Growth
- **Line.** EdS, Ω_c/Ω_b = 5.364, baryons free: \|n − 1\| ≤ 1e-6, using CFG941's Lagrangian growth machinery at the
  candidate's linear coefficient.
- **Plus a top-hat check.** The gate, label or domain criterion is unmet for every perturbation before turnaround.
- **PASS** if both hold.

### (d) Causality and well-posedness
- **d1. Every kernel retarded.** Sympy support of the retarded Green's function lies on the future light cone. The response to
  a source switched on at t₀ is identically zero for t < t₀ + r/c.
- **d2. No ghost.**
  - 𝒮 has no independent initial data (count of initial-data functions = 0 per candidate).
  - The linear response of matter perturbations inside edges and in shells has positive kinetic coefficients.
  - ω² is bounded below by a Jeans term with the effective G; there is no ω² ∝ −k² at large k.
- **d3. Total-source positivity.** ρ_b + ρ_c + ρ_s ≥ 0 everywhere in each candidate's static domain configuration (P-S), for
  NGC 3198 and CFG847's five systems, both footings.
- **d4. Hadamard continuity in a declared toy.**
  - Toy: two equal point masses in a uniform background with Δ_ta(0) = 11.83, separation varied by ±1% across the
    domain-topology change.
  - PASS if the source (domain mass, r_ON, pooled q) changes by ≤ 1%; otherwise FAIL for that domain rule.
- **d5. Conservation.**
  - The 2-form identity ∂_μ∂_ν𝒬^{μν} ≡ 0 (sympy).
  - ∫ρ_s = 0 per domain.
  - The momentum-consistency condition D̈_s = −F_ms (§4 T-M) derived symbolically and evaluated on the declared toy.
- **Class rule for (d).**

  | grade | condition |
  |---|---|
  | PASS | d1–d5 all pass |
  | CONDITIONAL | d1, d2, d3 and d5 pass; d4 fails for the literal rule, with a continuous variant declared |
  | FAIL | any of d1, d2, d3 or d5 fails |

  d5 fails for a candidate whose NR limit, as declared, contains a relocation rule that violates T-M.

### (e) Slip
- **Measures** (as CFG938 S4), on CFG847's five systems, both footings:
  - s_grad = 4πG r\|p_r\|/(c² g);
  - s_847 = 8πG r² max(\|p_r\|, \|p_t\|)/(c² v_c²).
- **Stress.** 𝒮's isotropic stress completion p(r) = ∫_r^{r_ON} ρ_s g dr′, in the P-S configuration. In P-I, 𝒮 = 0 and the
  cold's own pressure ρσ² with σ² = v_c²/2 is used.
- **PASS** if the worst value is ≤ 1.9e-5.

### (f) Satellites

**Setup** (CFG941's): CFG882's dwarfs H1–H3 (Plummer 1e4 M⊙/30 pc, 3e5/200 pc, 2e7/700 pc) at 50/100/250 kpc from a 6e10 M⊙
host on its law, both footings.

- **f1.** Δa/g_host between the satellite's stars and its cold matter and phantom.
  - PASS if ≤ 1e-2 (CFG941's tethered value is ≈ 1).
  - Monopole order from the equations. Retardation corrections are bounded by max(Φ_sat/c², v²/c², g_host r_h/c²).
- **f2.** Host EFE on the satellite's phantom.
  - Own-domain candidates have none by construction (factor 0 dex).
  - Global-QUMOND candidates: the static on-axis factor [g(g_bh + g_bs) − g(g_bh)]/g(g_bs) at the Plummer scale radius
    (CFG941's formula; CFG925's E2 1-D QUMOND form).
  - PASS if \|factor\| ≤ 0.01 dex in every case.
  - The line is the record's EFE-free satellite reading: CFG925 R3, and CFG478 (isolated phantom χ² 0.7/5;
    force-with-EFE 61–107/5 EXCLUDED).
  - N2-B's basin supply cap (a satellite basin truncated near its Jacobi radius) is reported, with no class weight.
- **(f) PASS** iff f1 and f2 pass.

### (g) Class-A limit, equation by equation (E1–E11)
- **Per candidate.** Each Ek is REPRODUCED (continuum limit of the engine's discrete form) or DIFFERS (stated how).
- **Grades.**

  | grade | condition |
  |---|---|
  | PASS | all reproduced (E11's cadence and the mesh are discretisation) |
  | CONDITIONAL | only named differences, each bounded at ≤ 1% of the engine's source by a computation in this lane |
  | FAIL | otherwise |

- **Meaning of FAIL.** An unquantified difference is a FAIL of (g). It means "transfer not established", not a shear failure.
- **Transfer.** The T1x / T2x / NC1x shear results are said to transfer only on PASS, or on CONDITIONAL with the bound.

### (h) CFG653's constraints
- **h1. SPARC**, CFG4 statistic:
  - ν_mono, Υ_bul = 1.4Υ, one global Υ on 0.30–1.20 (coarse 0.05, then 0.01);
  - weights (V/eV)², eV floored at 1 km/s.

  PASS if rms ≤ local + 0.005 dex with Υ in 0.50–0.80 (CFG653 gate a), both footings. Treatment:
  - Each galaxy is isolated with its own census domain, as in (a); points beyond its r_e use the edge-truncated field.
  - N2-E galaxies with r_ON < RMIN get no source: the law is OFF (Newtonian baryons). The cold-particle halo is not modelled;
    no ΛCDM halo model is used.
  - N1 is also scored with co-spatial label heterogeneity f = 0.1 and no M-R.
- **h2. Wide binaries.** Injected γ against the DR3 builder value 1.0750 ± 0.0550 (canonical) / 1.0775 ± 0.0512 (alt):
  z ≤ 2 PASS; 2–5 TENSION; > 5 FAIL.
  - A binary inside a host domain whose phantom is QUMOND (global or own-domain) carries the host EFE. CFG653's recovered
    local-EFE values are cited: 1.179 (+1.3σ) / 1.244 (+2.3σ), comparable to its L → ∞ column.
  - An EFE-free own phantom for each binary (a star as its own domain) is CFG447's exclusion (7.7σ / 8.3σ).
  - No new pipeline run.
- **h3. Satellites (R7).** Mapped from f2 onto CFG478.
- **h4. Static causality** (CFG653 c4). The support radius of every kernel is ≤ l_dS = c/H_Λ.
- **(h) PASS** iff h1 passes, h2 passes or is in TENSION, h3 passes and h4 passes.

## 4. Structural statements to test

Each counts only with a sympy or numeric check.

| id | statement | test, and what falsifies it |
|---|---|---|
| T-Z (zero-sum forced) | For geodesic matter and G = 8πG(T + 𝒮) with 𝒮 ≡ 0 on FRW, ∇_μ𝒮^{μν} = 0 forces ∫ρ_s d³x = 0 for all time. Per-domain zero-sum ⟺ no 𝒮 current crosses a domain boundary | falsified if a conserved 𝒮 with ∫ρ_s ≠ 0 arises from zero |
| T-M (momentum) | Total Newtonian momentum P_m + ∫j_s is conserved with ∫j_s = Ḋ_s (D_s = ∫xρ_s). Hence a prescribed source is conservable only if D̈_s = −F_ms, F_ms = ∫ρ_s∇Φ_m the force of 𝒮 on matter | declared toy: a core plus a two-blob cold shell with dipole fraction ε ∈ {0, 0.01, 0.1, 0.3}, under E6–E8's relocation; F_ms and the mismatch are computed. Falsified if F_ms = 0 for ε > 0 |
| T-E (forced edge) | For every M_b in 1e7–1e15 M⊙ (both footings, both kernels, native Δ_ta(0), census f_r), the law's enclosed mass at r_ON exceeds the catchment's particle mass: M_law(< r_ON) > M_ta. A zero-sum source with ρ_tot ≥ 0 must then end the law at some r_e < r_ON | falsified if M_law(< r_ON) ≤ M_ta for any M_b |
| T-F (free fall) | Geodesic matter plus a conserved 𝒮 carried by freely falling matter gives Δa/g_host = 0 at monopole order (no hover) | Mu1 (a local always-on tether) must restore CFG941's ≈ 1 |
| T-R (RMIN) | With RMIN_PHYS fixed, the engine's continuum limit has no source for isolated systems with r_ON < RMIN. The threshold M_b,thr is computed from E3, E7 and E9 (both footings) | falsified if NGC 3198 and the majority of SPARC galaxies lie above it |
| T-X (EFE fork) | E4 gives a satellite inside a host domain the host EFE; any own-domain rule differs from E4 wherever two domains' baryonic fields are comparable | falsified if the difference is ≤ 1% on the H1–H3 grid |
| T-L (labels) | The own-label phantom is non-additive: for co-spatial labels the deep factor is √(1 − f) + √f | computed on NGC 3198 |
| T-N3 (domains forced) | With the gate at r_ON (N3), the transition shell's total density is negative (d3) for every system | computed |

## 5. Controls and MUTATE

**K controls.**

| id | target | line |
|---|---|---|
| K1 | CFG938's reduced EL (W_full) solved at NGC 3198's 43 radii, against the closed law | ≤ 1e-6, both footings (CFG938: 2.2e-16) |
| K2 | CFG941 growth exponents: n(c₂ = 1, no χ̄ gradient) = 0.60954; n(c₂ = 1, with the gradient) = 0.69433; n(c₂ = 0) = 1 | first two within 1e-4; third within 1e-12 |
| K3 | CFG653 / CFG4 local law (ν_mono): rms 0.1003 @ Υ 0.61 (canonical) / 0.0991 @ 0.57 (alt); Newton rms 0.2755 | rms within 1.5e-4 with Υ exact; Newton within 1e-3 |
| K4 | CFG938 slip for the local parent: worst s_847 = 1.5398e-5 | within 2% |
| K5 | CFG941 hover and EFE for the tethered parent over H1–H3 × 3 radii × 2 footings: Δa/g_host in [1.017, 1.107]; EFE factors −0.73 to −0.10 dex | each end within 0.005; each EFE end within 0.01 |

**VOID rule.** If any K fails, the main classes are VOID (reported, not graded).

**MUTATE.** Separate outputs (`*_MUTATE`); exit 1 when every tooth bites, 2 if any does not.

| tooth | change | bites if |
|---|---|---|
| Mu1 | a local always-on tether (CFG938/941 P0) replaces the non-local 𝒮. D-T should return: n = 0.69433, Δa/g_host ≥ 0.5, and the linear-regime C₁C₂ mutual coefficient (1 − c₂) = 0. The non-local candidates give 1, ≈ 0 and 1 | all three hold |
| Mu2 | the time-symmetric kernel ½(G_ret + G_adv), which an action gives | a nonzero response appears before switch-on (precursor) |
| Mu3 | zero-sum removed (no shell draw) | ∫ρ_s ≠ 0 is created at switch-on, so the 𝒮 continuity equation has no solution: created mass > 1e-6 M_b |
| Mu4 | own-domain replaced by the global-QUMOND field for a satellite | \|EFE factor\| ≥ 0.05 dex somewhere on the H1–H3 grid |
| Mu5 | the q cap removed (q > 1 allowed) | min ρ_tot < 0 in the shell |

## 6. Classes

**Per candidate.**

| class | condition |
|---|---|
| VIABLE | (a)–(h) all PASS; no new constant; no unproved condition |
| VIABLE-WITH-COST | (a)–(f) and (h) PASS or CONDITIONAL, each condition named; (g) PASS or CONDITIONAL; costs listed (non-variational elements, extra rules, background subtraction, record constants) |
| NOT VIABLE | any of (a)–(h) FAIL |

A candidate failing only (g) is additionally labelled "a non-local theory, not class A's parent". No shear result is credited
to it.

**Overall.**

| class | condition |
|---|---|
| NON-LOCAL PARENT FOUND | at least one VIABLE candidate |
| CONDITIONAL | none VIABLE; at least one VIABLE-WITH-COST |
| NO-GO | every candidate NOT VIABLE, *and* a §4 statement that passes its check shows the failing combination is generic to every parent whose NR limit is exactly the class-A engine (not only to the three candidates) |
| NO CANDIDATE PASSES | every candidate NOT VIABLE, with no such generic statement (not a no-go) |

A NO-GO in this sense concerns exact parenthood. Whether an approximate parent (one differing from the engine by a computed,
small amount) exists is reported separately, as established or not established.

## 7. Design-stage disclosures (not blind)

**Read before freezing:**
- CFG938, CFG941 and CFG653 (README, criteria, code);
- CFG925, CFG678 (criteria, scorecard), CFG478 (README lines);
- the CFG801 / 803 / 748 LEDGER rows;
- the engine code listed in §0, run_650.py's settings, and CFG654's Δ_ta table.

**Expectations formed while reading.** These are mental estimates; no script was run. They are written down so that results
can be checked against them; the class follows only the rules above.
1. The (f)/(g) fork: E4 carries an EFE.
2. RMIN switches the law off for isolated galaxies below a few × 1e10 M⊙ in baryons, probably including NGC 3198.
3. The engine's prescribed relocation does not conserve momentum for asymmetric draws (T-M).
4. N3 cannot place the supply edge without a domain integral (positivity).
5. N1 needs a label-merge rule (√ non-additivity).
6. (a), (b), (c) and f1 pass by construction for class-A-type sources.
7. The overall class may be NO-GO for exact parenthood.

## 8. Compute

- One process at a time; OMP_NUM_THREADS=1; nice -n 10; an in-script RSS guard at 1 GB; small sympy and numpy only.
- No downloads. No other lane's files are touched. Inputs are read-only: CFG4_common, the record's SPARC files, CFG654's
  Δ_ta JSON.
- Stages K, MUTATE, main, in that order, with separate outputs.
