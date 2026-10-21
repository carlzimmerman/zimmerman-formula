# CFG955 FROZEN CRITERIA: is the class-A engine the coarse-grained limit of a kinetic theory of relaxing cold dust?

Committed alone, before any CFG955 script, derivation output or number. Block 950–959 (LEDGER reservation row, 3b5aa10ca:
"CFG955 relaxing-cold-dust kinetic parent"). κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², scored
separately and never pooled. Cold energy is the framework's own component: its mass is required and no particle species is added.
Framework-native inputs only; no ΛCDM yardstick enters a verdict. Not "theory closed" whatever the outcome, and nothing here can
say the data favour the framework. Any change after this commit is a dated, labelled amendment.

## 0. The hypothesis as given (H-K), and the two readings it admits

**H-K (verbatim content of the brief).** Cold energy is collisionless dust with phase-space density f(x, v, t) obeying

  ∂ₜf + v·∇f − ∇Φ·∂ᵥf = −(f − f_eq)/τ   inside each host's own domain; no relaxation outside domains;

with ∇²Φ = 4πG(ρ_b + ρ_d) (plain Poisson: no phantom field, no source S). f_eq is the maximum-entropy (isothermal) distribution
"whose density is the own-domain law phantom" of the host's condensed baryons (M2), truncated at the supply edge where the phantom
exhausts the host's own catchment dust (M1, zero-sum). The relaxation "conserves mass and momentum locally" (f_eq carries the local
dust mean velocity u) and does not conserve dust kinetic energy; the energy goes to or comes from a reservoir outside matter.

**Common chassis (both readings).**
- **Domains.** A domain is born at first turnaround from the Hubble flow (E3's criterion, no RMIN) and its identity is latched. A
  system formed inside a collapsed domain (stars, binaries, tidal dwarfs, debris) is not a domain (CFG953 R1, the SCT-M in-situ
  rule). Cells are assigned among domains by M1 (smallest d/r_ON). Dust is relaxed by position: dust in a cell of domain D relaxes
  to D's target.
- **Own-domain phantom.** The MONOPOLE law phantom of the domain's own condensed baryons, spherical about the domain's
  condensed-baryon centroid X_b,D: M_ph(<r) = r²[g_law(ḡ) − ḡ]/G with ḡ = G M_b,own(<r)/r². It is not the pointwise phantom
  (CFG953: the pointwise own-baryon phantom, SCT-Q, carries the host EFE into in-situ systems and fails the tidal dwarfs).
- **Edge.** r_e,D is the supply root M_ph(<r_e) = M_d,D, with M_d,D the dust mass of the domain (for an isolated host, the
  catchment supply). Relaxation acts at r < r_e only; the domain shell r_e < r < r_ON is collisionless.
- **Jeans temperature.** T_J(r) = (1/ρ_ph(r)) ∫_r^{r_e} ρ_ph(r′) g_law(r′) dr′: the isotropic Jeans temperature of the phantom in
  the law field, with zero pressure at r_e.

**Reading K-ρ (density target).** f_eq = ρ_eq(x) M[u, T_J](v), with ρ_eq = ρ_ph inside r_e and (1 − q)ρ_d in the shell
(the engine's E6–E8 written as a target) and u the local dust mean velocity. This is the literal "density = phantom" target. Its
collision term has ∫(f − f_eq) dv = ρ_d − ρ_eq ≠ 0.

**Reading K-T (temperature target; primary).** f_eq = M[ρ_d(x), u(x), T_J(x)], the local Maxwellian with the local dust density,
the local dust mean velocity and the temperature T_J. Its collision invariants are 1 and v, so mass and momentum are conserved at
every point, as H-K requires. In K-T "the density of f_eq is the phantom" holds for the stationary state, not pointwise.

**Reservoir R.** Per unit volume, R receives −Q, the energy moment of the collision term (K-T: Q = (3/2)ρ_d(T_J − T)/τ, with T the
local dust temperature): ∂ₜe_R = −Q. R lies outside matter. It is to be identified against CFG935's channels (a dynamical
dark-energy partner; a heat reservoir at the local Jeans temperature).

## 1. Structural statements (each counts only with a sympy or numeric check)

| id | statement | check; what falsifies it |
|---|---|---|
| H0 | K-T's collision term has zero mass and momentum moments and energy moment (3/2)ρ(T_J − T)/τ; K-ρ's has mass moment −(ρ − ρ_eq)/τ, so its continuity equation has a source and the O(c²) part of ∇_μT^{μ0} = 0 fails unless a separate conserved sector carries the mass (then CFG947's T-M applies) | sympy moments of both operators |
| L1 | Fast-relaxation limit. K-T as τ → 0 is Euler flow with p = ρT_J(x) (Chapman–Enskog zeroth order; first order: η = ρT_Jτ, heat flux). E8 (instant relocation of active mass) is not in that family: gravitating mass moves only by continuity. K-ρ as τ → 0 is E6–E8 minus the clip, with real mass relocated | sympy moments; spherical toy (§2 a3): from IC-I at the fast probe τ = 0.1 τ_π, the L1 distance ‖ρ_d − ρ_ph‖₁/M_c over r < r_* (40 bins) against t/t_e. **LIMIT** iff it falls below 0.1 by t = 0.1 t_e; otherwise not a τ → 0 limit |
| L2 | Momentum (T-M). K-T conserves total momentum exactly (pairwise gravity + per-cell momentum-preserving relaxation), so R ≡ 0. K-ρ breaks the centre-of-mass theorem in an asymmetric domain | 1-D planar sheet toy (§2 e): K-T \|ΔP\|/(M v_ref) ≤ 1e-10; K-ρ centre-of-mass slip \|X_cm − X_cm(0) − P t/M\|/x_e ≥ 1e-3 |
| L3 | RMIN (T-R). K-T has no RMIN: every collapsed system with baryons has a domain, and the relaxed state is the local law inside r_e. In a PM implementation the floor is resolution: r_e ≥ 2 dx (dx = 100/1024 Mpc/h comoving, z = 0) | computed M_b,res (both footings) vs CFG952's 2.19e11; SPARC rms with every galaxy relaxed in its own domain (CFG947's own-domain predictor) and the count of points beyond an edge, reported |
| L4 | No EFE, no hover. With linear Poisson Φ, a uniform external field drops out of Vlasov + BGK in the freely falling frame, because f_eq uses the local u and a T_J that moves with its own baryons. So Δa/g_host = 0 and the EFE is 0 dex at monopole order | sympy (uniform-acceleration covariance of the equation); planar toy (§2 b1) |
| L5 | Selection (O2d2's gap, CFG946). With T_J prescribed and the domain's dust mass fixed, the hydrostatic + Poisson system has a one-parameter family of solutions (central normalisation C). **UNIQUE** iff M_d(<r_e; C) = M_c has one root on C/C_law ∈ [1e-2, 1e2] (401 log points plus bisection), at C_law to 1e-6 | NGC 3198 (both footings, both kernels) and the spherical toy |
| L6 | Multi-stream. Relaxation to the local mean velocity removes the relative velocity of interpenetrating streams at rate 1/τ, d(u₁ − u₂)/dt = −(u₁ − u₂)/τ, and sends their relative kinetic energy to R. As τ → 0, dust in a domain becomes one fluid (no collisionless interpenetration). A domain with no own dust cannot capture a stream: the stream's mean velocity is a collision invariant | sympy (two-stream moments); used in (b3) and the Bullet report |
| L7 | Second law. The bath must behave as a heat reservoir at T_J: dS_d/dt − Q/T_J = (3/2)(ρ/τ)(T_J − T)²/(T T_J) ≥ 0, and on the cooling branch (T > T_J) the dust's entropy falls, so R must absorb entropy ≥ −Q/T_J. A zero-entropy (coherent) reservoir, as CFG542 Pb requires of the dark-energy partner, cannot take the cooling branch | sympy (local-Maxwellian moments); cooling and heating flows booked in the toy |
| T-EX | Excess unreachable. K-T's relaxed state is the law inside r_e, and its unrelaxed state is native dust. CFG930 D4 found native cold mass inside every dwarf aperture below the settled phantom (Q_ap medians 0.15 / 0.32 / 0.28 / 0.30 / 0.26 for U / C / M31 Collins / M31 LVD / I; frac > 1 = 0 except M 32). Every mixture then lies at or below the law, so no τ gives the dSph excess | read CFG930's stored D4 (both footings): T-EX holds iff max over classes of the median Q_ap < 1 |

## 2. Tests (a)–(f), both footings

### (a) The law for isolated relaxed hosts
- **a1 (NGC 3198 stationary state).** Inputs: the record's rotmod file, Υ = 0.61, spherical-equivalent m_N(r) = r²g_bar/G at the
  43 radii, interpolated by PCHIP in (ln r, m_N); m_N ∝ r³ below the first radius; point mass beyond the last radius. Kernels: S2
  simple law (primary) and ν_mono (secondary). Domain: CFG947's `domain()` (census, native Δ_ta(0), E7 edge). T_J from the exact
  phantom on a fine grid; the hydrostatic + Poisson ODE integrated from 0.1 kpc with C = C_law. Line: max |g/g_law − 1| ≤ 1e-6 at
  the 43 radii. **If dM_ph/dr < 0 anywhere inside r_e on the grid** (a negative phantom density), no non-negative dust can be the
  law there: a1 FAILS for that kernel/footing, and the minimum ρ_ph/⟨ρ_ph⟩ and the deviation of the best non-negative profile
  (M_d = running maximum of M_ph) are reported.
- **a2 (BTFR).** Deep points y = g_N/a₀ ∈ {1e-2, 1e-3} inside r_e: |g/g_law − 1| ≤ 1e-6; V⁴/(G M_b a₀) reported (the law's own
  1.105 / 1.032).
- **a3 (selection by the dynamics).** Spherical shell toy (below). K-T at τ = T1 (§3) from IC-L, IC-I, IC-S. A run is ON THE LAW
  iff CFG935's gate holds: D = median over SEDGES' 16 bins in r = 1–9 of log₁₀(ρ̄_d/ρ_ph), |D(W2)| ≤ 0.1 and |D(W2) − D(W1)| ≤ 0.05,
  windows W1 = [0.5, 0.75] and W2 = [0.75, 1] of t_end. a3 passes iff IC-L and IC-I are ON THE LAW; IC-S is reported. X_m at
  r = 2, 5, 8, f_esc and ε_E are reported.
- **Grade.** PASS iff a1, a2, a3 pass and L5 is UNIQUE. CONDITIONAL iff a1 and a2 pass and either a3 passes for IC-L only, or L5 is
  not unique while a3 passes. FAIL otherwise.
- **Toy (declared).** G = a₀ = M_b = 1; static Plummer baryons, a = 1; simple kernel; domain edge r_* = 10, so M_c = M_ph(<10);
  R_C = 30; N = 10000 shells (r, v_r, L); softening ε = 0.02 (CFG935 A2); reflecting r_min = 1e-3; DTMAX 0.02; CA 0.03; CFG935's
  41 radial bins (EDGES); seed 955; ICs as CFG935 (IC-L Jeans-supported law; IC-I cold uniform sphere of radius 15, L = 0.05 r v_c;
  IC-S cold, enclosed dust 1.5 M_ph); t_end 350 (IC-L) and 650 (IC-I, IC-S), as CFG935 A0. Relaxation (K-T) in each bin inside
  r_*: each particle is resampled with probability 1 − exp(−dt/τ_bin); the resampled subset keeps its own mean radial velocity
  exactly (zero-mean deviates), with T = T_J at the subset's mass-weighted mean radius; tangential speeds come from the 2-D
  Maxwellian at the same T. ΔK is booked to E_R. T_J is the phantom's Jeans σ² truncated at r_* (CFG935's `law_jeans_sigma2`
  form).

### (b) Satellites: no hover, no EFE, and the multi-stream drag
- **b1 hover.** Monopole order from L4 (sympy). Numeric, planar toy: a satellite (baryons + its relaxed own dust) in a uniform field
  g_ext for t = 50. The fitted ε = 2|ΔX_dust − ΔX_bary|/(g_ext t²) must be ≤ 1e-2.
- **b2 EFE.** 0 dex at monopole order (own-domain monopole T_J; L4). The M1 radius of a satellite's own domain at each host distance,
  s_M1 = (d/r_ON,host) r_ON,sat, is reported against the Plummer radius a and the satellite's own r_e.
- **b3 drag (L6).** CFG882's dwarfs H1–H3 (Plummer 1e4 M⊙ / 30 pc, 3e5 / 200 pc, 2e7 / 700 pc) at 50 / 100 / 250 kpc from a
  6e10 M⊙ host on its law (simple kernel; point-mass host). Host dust density ρ_h = the host's phantom density at d; satellite dust
  ρ_s(r) = the satellite's own monopole phantom density; V = v_c,host(d); g_host = g_law,host(d). ε_drag(r) = [ρ_h/(ρ_s + ρ_h)]·V/(τ·g_host).
  **Line:** ε_drag(a) ≤ ε_B = 0.344 (canonical) / 0.317 (alt) (CFG945) in all 18 cases per footing. The strip radius r_s, where
  [ρ_h/(ρ_s + ρ_h)]V/τ = g_int,s(r) (the satellite's own law field), is computed. If r_s < a, the enclosed-mass deficit at a,
  log₁₀[(M_b(<a) + M_ph(<r_s))/(M_b(<a) + M_ph(<a))], must satisfy |δ| ≤ δ_c = 0.082 dex (CFG945). ε_drag(2a) and the
  dust-mass-weighted mean inside 2a are reported.
- **b4 Bullet (reported, no grade).** The fraction of the sub's dust relative momentum removed in one core crossing,
  1 − exp(−t_x ρ_main/((ρ_main + ρ_sub) τ)), with t_x = 2 × 250 kpc / 2666.7 km/s (CFG623's v₀), ρ_main and ρ_sub the relaxed
  phantom densities of a 1.5e14 M⊙ main (CFG847's cluster) at 250 kpc and of a 1.5e13 M⊙ sub at its own 50 kpc, for each τ.
- **Grade (per τ candidate).** PASS iff b1 and b2 pass and b3 passes. The reading's (b) is PASS iff it passes for at least one τ
  candidate that passes τ-P (§3); CONDITIONAL iff it passes only for candidates failing τ-P; FAIL if b3 fails for every candidate
  (or b1/b2 fail).

### (c) Slip
Measures as CFG938 S4 on CFG847's five systems (point masses; dwarf, MW disc, MW outer, group, cluster), both footings, simple kernel:
s_grad = 4πG r|p|/(c² g) and s_847 = 8πG r² |p|/(c² v_c²), with the isotropic dust pressure p = ρ_ph T_J of each system's relaxed
state (exact T_J, each system's own E7 edge). **PASS** iff the worst value is ≤ 1.9e-5.

### (d) Growth
- Outside domains there is no relaxation, so the dust exponent is n = 1 (CFG941's Lagrangian machinery with c₂ = 0): |n − 1| ≤ 1e-12.
- The collision term vanishes identically for a cold single stream with T_J = 0 (sympy): relaxation cannot act before condensed
  baryons exist (M2: f_d = 0 before collapse).
- No domain before turnaround (top-hat: mean density reaches 9π²/16 at δ_lin = 1.0624, CFG947's check reused).
- **PASS** iff all three hold.

### (e) Conservation
- Planar toy (declared). G = 1; sheets with exact pairwise gravity, a_i = 2πG Σ_j m_j sign(x_j − x_i) from ranks; leapfrog, dt = 0.01,
  t_end = 50; cells of width 0.25 on [−60, 60]. A host is 2000 baryon sheets (Gaussian, σ = 1, mass 1) plus 10000 dust sheets of
  mass 5.364. Toy target T_J(x) = T₀ max(0, 1 − (x − X_b)²/x_e²), with x_e = 5 and T₀ = πG M_tot x_e/2, centred on the domain's
  baryon centroid. τ = 1 (code units). Relaxation as in (a) per cell (the subset's own mean velocity kept exactly).
- Runs: **E-R**, an asymmetric host (dust offset +1, bulk velocity +0.3); **E-S**, a satellite of 1/10 the host's mass starting at
  x = 20 with velocity −1; **E-M**, two equal hosts at ±15 approaching at ±0.5, with M1 switching cells between them as they
  overlap.
- **Lines** in all three runs: mass exact (integer counts); |ΔP|/(M_tot v_ref) ≤ 1e-10 with v_ref = √T₀; booked energy:
  |Δ(E_kin + W + E_R)| ≤ 2 × the same run's integrator error with relaxation off + 1e-10 |E|.
- Reported: E-M's largest change of the gravitating density per dynamical time (CFG954-style J) and the jump of T_J at M1 switches.
- **PASS** iff every line holds in all three runs.

### (f) Causality
- **f1.** The kinetic operator is local in x, its characteristic speed is |v| ≪ c (sympy), and τ is finite.
- **f2.** The target T_J is a functional of the domain's condensed baryons and dust mass (a non-local, domain-wide functional). It is
  causal only if built from retarded own-domain fields (CFG947 N1 / N2-B construction, □_ret): condition **C-ret**.
- **f3.** The relaxation is dissipative (an H-theorem against R), so the theory has no action principle (CFG678's one-action rule
  cannot be met). This is a declared cost, not a grade.
- **Grade.** PASS iff f1 holds and T_J is retarded by construction. CONDITIONAL iff f1 holds and causality needs C-ret (the
  engine-faithful instantaneous target). FAIL iff f1 fails.

## 3. What sets τ (candidates declared now; record quantities only; no scan)

| id | rate law | source |
|---|---|---|
| T1 | τ = τ_π = τ_ff/(2α), τ_ff = (4πGρ_m)^{−1/2} (local ρ_m), α = 1 | CFG638's pressure-relaxation time (CFG935's α = 1; α ≤ 1.186, CFG542). SIS: τ_ff = r/V |
| T2 | τ = k t_orb, t_orb = 2πr/V, k ∈ {0.46 can / 0.52 alt, 1.20} (both bracket ends) | CFG764's orbital clock |
| T3 | τ ∈ {0.72 can / 0.83 alt, 3.47} Gyr (both bracket ends) | CFG763's universal clock |
| T4 | dust is a continuum: τ_2b = ∞; with stars as scatterers, Spitzer τ_2b = 0.34σ³/(G² m_* ρ_* lnΛ), m_* = 1 M⊙, lnΛ = 10 | two-body estimate |
| T5 | T1's rate applied only to dust with \|v − u_b\| < V_esc,b (a per-element reading of CFG939's capture criterion) | CFG939 / CFG948 |

Violent relaxation acts on t_dyn but conserves energy (Vlasov) and has no T_J target, so it is not a BGK-to-T_J channel. This is
stated with its argument; it carries no class weight.

**Class rows.** CFG939's N5 rows (r½, M_b(<r½), g_N/a₀, ρ_ph, T_c, age; both footings): UFD-c, UFD-e, Draco-like, Fornax-like,
SPARC dwarf, MW-like, cluster core, six tidal dwarfs, DF2/DF4. Local ρ_m = ρ_b + ρ_ph at r½, with ρ_b from CFG939's own profiles
(code copied with attribution). Rotators are also checked at CFG764's slowest SPARC last-point orbit, 2.91 Gyr, age 8 Gyr (CFG764's
k_max rule).

**Relaxed fraction.** R = 1 − exp(−age/τ). ON LAW if R ≥ 0.9; NATIVE if R ≤ 0.1; MIXED otherwise. T5 is evaluated as the fraction
of the relaxed law-state Maxwellian with speed below V_esc,b at r½ (the law cannot be self-maintained where that fraction is < 0.5).

**Facts.**
- Rotators (SPARC dwarf, MW-like, and the slowest SPARC orbit): ON LAW.
- Cluster cores: NATIVE (CFG949 B0; CFG954).
- Below-law systems (TDGs, DF2/DF4): Newtonian, via no own domain (in situ) or no capture (L6).
- dSph/UFD excess (+0.37 dex stars-only, CFG860; CFG873) and the Coma UDGs (+0.76 / +0.67 ln, CFG948): scored through T-EX, for
  all τ at once.

**τ classes (per candidate).**
- **τ-P (parenthood):** rotators and the engine-resolved hosts at the 1024³ threshold (MW-like, cluster core) are ON LAW.
- **τ-F (facts):** rotators ON LAW, cluster cores NATIVE, and below-law systems Newtonian.
- **Ordering check (any proportionality constant).** For a local clock τ = c·t(r), a constant exists that gives τ-F iff
  min_rotators(age/t) / max_clusters(age/t) ≥ ln(10)/ln(10/9) = 21.85. Computed for t = τ_ff and t = t_orb.
- **Verdict.** "A derived selector for CFG949" iff some candidate passes τ-F; otherwise **"no record-derived τ works"**, stated
  plainly.
- **Cluster amplitudes (reported, approximate).** For each candidate's cluster R: A_band(R) = 1/[R/A_law + (1 − R)/A_B0], using
  CFG687's law and CFG949's B0 stored band amplitudes (MID, OUTER; per footing). This assumes shapes are similar within a band.

## 4. Energy
- **E1.** The net energy each host's relaxation exchanges equals E_start − E_end, with E_end the Jeans-supported truncated law. That is
  the same end state as CFG935's N-type law. Hence K-T's per-host net exchange equals CFG935's E_x table (primordial debris → law,
  whole catchment; read from its PHYS.json). Sign: dust → R for native-debris starts. The toy books E_R for IC-I and IC-S (sign
  reported). Power per host E_x/τ is reported for T1–T3 (MW-like, cluster core).
- **E2.** Gross versus net exchange: cooling (dust → R) and heating (R → dust) flows in the toy, and their meaning under L7.
- **E3 (CFG930/932 ordering).** K-T's exchange is with R, not with baryonic feedback, so CFG930's SN-energy ordering (E_SN/ΔE ≈ 600 /
  22 / 0.5) is **NOT APPLICABLE** unless R's capacity is tied to baryonic energy. T-EX is graded separately. The task-4 class is
  KILLS iff K-T's settling would require an energy budget with CFG930's inverted ordering; otherwise DOES NOT KILL (with T-EX stated).

## 5. Shear-run design (not run)
A separate file `FROZEN_CRITERIA_KT1024_DRAFT.md` (DRAFT; explicitly NOT frozen; not criteria for this lane). It must contain:
- the PM engine variant: own-domain monopole T_J relaxation of particles with per-bin momentum conservation; no E4, no E6–E8; RMIN
  only at resolution (r_e ≥ 2 dx); M3 unchanged; M2 as in NC1x;
- the statistic, control and classes (CFG654's native scorer, NCS0, as CFG952's draft);
- validation gates;
- the cost from CFG952's NC1x baseline model (16.27 h; 44.33 GB; t_pass 105 s);
- owner approvals.

No heavy job is started.

## 6. Controls and MUTATE

**K controls.** VOID rule: any K failure makes the main classes VOID (reported, not graded).

| id | target | line |
|---|---|---|
| K1 | CFG947 T-M: the identity D̈ − Σ s ẍ = Σ(s̈x + 2ṡẋ); E8 two-blob R = −ε(M̈_e X + 2Ṁ_e Ẋ); max\|R\|/(M_dom g_ref) = π²ε/4 = 0.025 / 0.247 / 0.740 at ε 0.01 / 0.1 / 0.3 | sympy exact; numbers to 1e-3 |
| K2 | CFG947 T-R: M_b,thr 4.815e10 M⊙; NGC 3198 not resolved; 128 of 175 SPARC below | 1e-3 relative; counts exact |
| K3 | CFG947 T-X: 36 E4 EFE factors, range −0.730 … −0.102 dex | each end within 0.001 |
| K4 | CFG938's NGC 3198 law (reduced EL) | ≤ 1e-6 both footings (CFG938 2.2e-16) |
| K5 | CFG952's effective RMIN: node 1.0471 Mpc/h on E3's 14-point grid at 1024³, M_b,ret ≥ 2.19e11 M⊙ | within 1% |
| K6 | CFG941 growth exponents 0.60954 / 0.69433 / 1 | first two within 1e-4; third within 1e-12 |
| K7 | CFG935: PHYS E_x table read (exact); this lane's toy T_J against CFG935's `law_jeans_sigma2` on the toy | ≤ 1e-3 relative inside r = 0.1–9 |
| K8 | CFG947 SPARC local law 0.1003 @ 0.61 / 0.0991 @ 0.57; Newton 0.2755 | rms within 1.5e-4, Υ exact; Newton within 1e-3 |

**MUTATE.** Separate outputs (`*_MUTATE`). Exit 1 when every tooth bites, 2 otherwise.

| tooth | change | bites if |
|---|---|---|
| Mu1 | a tether instead of relaxation (CFG941's c₂ = 1 with the χ̄ gradient) | n = 0.69433 within 1e-4 (D-T), against K-T's 1 |
| Mu2 | a global phantom (host + satellite baryons) instead of the own-domain monopole | the satellite EFE returns: max \|factor\| ≥ 0.05 dex, and CFG947's range is reproduced within 0.001 |
| Mu3 | K-ρ relocation in the planar toy | centre-of-mass slip ≥ 1e-3 x_e or \|ΔP\|/(M v_ref) ≥ 1e-3 |
| Mu4 | a self-consistent target (CFG554: T from the current dust density, no phantom) in the spherical toy from IC-I | NOT ON THE LAW |
| Mu5 | relaxation off (τ = ∞) in the spherical toy from IC-I | NOT ON THE LAW |

## 7. Classes

**Per reading.**
- **NOT CONSERVATIVE:** H0 or L2 fails (no local mass or momentum conservation).
- **Engine relation** (E6–E8 / M1 / M2 / M3 against the reading):
  - LIMIT: E6–E8 is the τ → 0 limit in L1 of the gravitating density at fixed time (L1's line), up to named differences, each
    bounded at ≤ 1% by a computation here;
  - ATTRACTOR: E6–E8's source equals the reading's late-time stationary state for isolated relaxed hosts (a3 ON THE LAW), but not
    at fixed time. Named differences: the clip (the engine keeps native surplus; K-T relaxes it), E4's global phantom, RMIN, and
    multi-stream collisionality (L6);
  - NONE: neither.

**Overall.**

| class | condition |
|---|---|
| **ENGINE HAS A KINETIC PARENT** | a conservative reading with (a)–(e) PASS, (f) PASS or CONDITIONAL on C-ret only, engine relation LIMIT, and a τ candidate passing τ-P. Costs listed |
| **CONDITIONAL** | a conservative reading with no FAIL among (a)–(f) and engine relation LIMIT or ATTRACTOR, not meeting the row above. Every condition is listed (R's identity, τ, C-ret, the attractor differences, shear transfer by run) |
| **NO KINETIC PARENT** | no reading is conservative; or every conservative reading has a FAIL among (a)–(f) or relation NONE, and a structural statement (H0, L1, L2, L5, L6, L7 or T-EX) that passes its check shows the failure is generic |

**Transfer.** The T1x / T2x / NC1x shear passes transfer to the kinetic theory only on LIMIT. On ATTRACTOR the transfer is "not
established; needs the 1024³ KT run".

## 8. Design-stage disclosures (not blind)

**Read before freezing:**
- the CFG650 README;
- CFG947 (README, criteria, derivation, script);
- CFG941, 944, 945, 946, 948, 949, 952 (README, draft, design cost section), 953 (README; result 8d27793af, read after the
  coordinator's message, before this commit) and 954;
- CFG930, 932, 935 (README, script);
- CFG923, 638, 639, 623 (README heads), 763, 764 (README heads);
- CFG939's N5 code and JSON keys;
- the stored CFG930 D4 and CFG935 PHYS numbers (record values, not this lane's).

**From the coordinator's message, adopted here before the commit:**
- the target is the monopole own-centroid phantom (not the pointwise one);
- in-situ systems are not domains (SCT-M R1).

**Expectations formed while reading** (mental estimates; no script run):
1. K-ρ is not conservative (H0).
2. K-T conserves mass and momentum exactly.
3. E8 is not K-T's τ → 0 limit, only its late-time attractor (expected relation ATTRACTOR).
4. No record clock separates clusters from rotators: the slowest SPARC orbit, 2.91 Gyr, is about a cluster core's t_orb.
5. T-EX holds, since CFG930's Q_ap are all < 1.
6. R must be a heat bath at T_J (CFG935's reservoir ii). No drift partner is needed, because K-T has no drift; a zero-entropy
   partner fails the cooling branch.
7. (a) is uncertain: L5, the toy dynamics and the positivity of NGC 3198's phantom density are unknown.
8. Hand estimate of T1's drag in the deep SIS limit: ε_drag(a) ≈ 2Va/(v_s d) ≈ 0.04–0.22, largest for H3 at 50 kpc.
9. The likely overall class is CONDITIONAL.

## 9. Compute
- One process at a time; OMP_NUM_THREADS=1; nice -n 10; in-script RSS guard at 1 GB; small sympy and numpy only.
- No downloads. Read-only inputs: CFG4_common, the record's SPARC files, CFG654's Δ_ta JSON, and the CFG930 / 935 / 939 / 949 / 687
  JSONs.
- No other lane's file is edited.
- Stages K, MUTATE, main, in that order, with separate outputs.
