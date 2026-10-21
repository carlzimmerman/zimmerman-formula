# CFG953 FROZEN CRITERIA: the minimal source-changing non-local theory (SCT), constructed and tested

Committed alone, before any CFG953 script, derivation output or number exists. Date 2026-10-21. Block CFG950–959 (LEDGER
reservation row: "CFG953 source-changing non-local theory (SCT) construction and theory tests"). Clusters and mergers are tested
in detail by the parallel lane CFG954, which froze its own working SCT statement before this file existed; here they get a
first-order statement only.

**Settings.** κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², scored separately, never pooled. Cold
energy is the framework's own component: its mass is required, and no particle species is added. Framework-native inputs only;
no ΛCDM yardstick enters a verdict. Not "theory closed" whatever the outcome; nothing here can say the data favour the framework.
Any change after this commit is a dated, labelled amendment.

## 0. What is being built, and why this form

The owner's brief: build the non-local theory that changes the SOURCE of gravity (CFG947's only open door). The record fixes the
frame:
- a response that holds cold matter on the law (a tether) cancels its self-gravity and makes satellites hover (CFG941 D-T,
  CFG945 S, CFG946 D-T′);
- a local field that supplies the deep law carries an EFE, so the law's extra mass must be the cold energy itself (CFG946 T-O2);
- a conserved, retarded, non-local source sector 𝒮 has no hover, a¹ growth, forced zero-sum and a forced edge (CFG947), but the
  class-A relocation rule is not conservable (T-M), RMIN switches the law off (T-R), and a global phantom carries the EFE (T-X);
- a labelled tether (LDT) sources the host's law from the members' media (CFG951) and its energy closes only with a label energy
  (CFG950).

SCT therefore keeps cold energy as ordinary, untethered, self-gravitating dust, and puts the law's extra gravity in 𝒮, sourced by
each collapsed system's own baryons only. The new step is how 𝒮 is made conservable: at collapse the system's cold dust is
**converted** into a "phantom body" whose shape is fixed by the law of its own baryons and whose centroid, momentum, spin and
internal energy are dynamical charges that absorb every conversion and merge inelastically.

## 1. SCT specification (frozen)

**R0 chassis.** G_μν = (8πG/c⁴)(T^b + T^c + 𝒮)_μν. Baryons and all cold dust are geodesic. The dust is CFG938's matter sector
without W, χ, λ or stiffness (no tether). The Bianchi identity then forces ∇_μ𝒮^{μν} = 0 separately.

**R1 domains and labels.**
- A domain q is born when a region turns around from the Hubble flow (E3's criterion, enclosed mean ≥ Δ_ta(z) ρ̄_m about a peak of
  the matter density smoothed at L* = 24 pc; no RMIN) and the region contains baryons. A baryon-free collapse is not a domain.
- At birth every unlabelled matter element inside the turnaround region takes label q (latched: rule β). Unlabelled matter that
  later enters q's turnaround region joins q.
- Labels are never reassigned except by the merge rule R7. In particular a satellite keeps its label and its whole body.
- A self-bound system that forms inside an already collapsed domain (stars, star clusters, binaries, tidal dwarfs, collisional
  debris: "in situ") is not a new domain. Its matter keeps the parent's label, and it finds no unlabelled cold dust to convert.

**R2 conversion: the source.** 𝒮^{μν} = Σ_q Σ_q^{μν} − T^{μν}_{c,lab}, where T_{c,lab} is the full stress-energy of labelled dust and
Σ_q that of domain q's phantom body. Non-relativistic (NR) limit:
- ρ_s = Σ_q σ_q − ρ_{c,lab}; the gravitating density is ρ_b + ρ_{c,unl} + Σ_q σ_q;
- labelled dust still moves geodesically but sources nothing (it is gravitationally inert; its rest mass, momentum, kinetic energy
  and stress are all cancelled from the source by 𝒮's −T_{c,lab} part).

**R3 the body's shape.**
- **SCT-M (primary): monopole body.** σ_q is spherically symmetric about its own centroid X_q, with enclosed mass
  M_σ,q(<r) = min{ r²[g_law(ḡ_q) − ḡ_q]/G , M_c,q }, ḡ_q(r) = G M_b,q(<r)/r²,
  where M_b,q(<r) is q's own (labelled) baryon mass within r of X_q and M_c,q is q's labelled cold mass. g_law is the S2 simple
  kernel (primary) or ν_mono (secondary). The edge r_e,q is the kernel's own supply root, M_ph,q(<r_e) = M_c,q. The body has no mass
  beyond r_e.
- **SCT-Q (declared variant): pointwise body.** σ_q is the pointwise QUMOND phantom of q's own baryon field,
  −∇·[(ν(|g_N,q|/a₀) − 1) g_N,q]/(4πG), truncated where its enclosed mass about X_q reaches M_c,q, translated with X_q, its
  orientation slaved to the baryons, with the spin charge S_q absorbing the torque.
- Both variants share every other rule. They coincide for spherical systems, so they differ only where sub-structure or geometry
  matters ((g), (h), the a3 report).

**R4 the body's dynamics (momentum).**
- Between events, P_q = M_c,q V_q obeys dP_q/dt = ∫σ_q g dV (g = −∇Φ, total and retarded). Reshaping at fixed centroid carries no
  net momentum (internal current; the compact stress Π_σ exists iff this centroid law holds).
- **Conversion event** (a dust element m at x, v joins q): M_c → M_c + m; X → (M_c X + m x)/(M_c + m); P → P + m v; the element's
  angular momentum about the new centroid in the new centroid frame goes into S_q; its kinetic energy in that frame, plus the change
  of W caused by moving its active mass into the body, goes into E_int,q.
- **Birth** is a sequence of conversion events ramped over τ_conv = the free-fall time at turnaround.
- Baryon accretion, loss or internal motion changes the body's shape only (through M_b,q(<r)), never its centroid.

**R5 angular momentum.** A spherical body feels no torque about its own centre. Its spin S_q is a bookkeeping charge, carried by the
magnetic part of 𝒬 (j_s ⊃ ∇×M), with no NR gravitational effect. It changes only at events (and, in SCT-Q, by the baryon–body torque).

**R6 energy.**
- Each body carries an internal energy E_int,q: a declared, non-dynamical reservoir that gravitates at 1/c².
- dE_int,q/dt = −P_σ,q, where P_σ,q = ∫Φ ∂_t σ_q dV (shape change in the centroid frame), plus the event terms of R4 and R7.
- Then E = K_b + K_{c,unl} + Σ ½ M_c V² + W[ρ_b + ρ_{c,unl} + Σσ] + Σ E_int is conserved. This reservoir is SCT's version of
  CFG935's "energy sink outside matter"; its size is computed, not assumed small.

**R7 merges (M-R_SCT).**
- Domains p (smaller) and q merge when p's baryons are no longer self-bound (bound fraction < ½; CFG947 M-R) or when the two baryon
  centroids coalesce (separation ≤ the larger domain's baryonic half-mass radius; CFG951's trigger).
- At a merge, mass, centroid and momentum add; S absorbs the relative orbital angular momentum; E_int absorbs the relative kinetic
  energy and −ΔW. The blend runs over τ_m = the remnant's dynamical time.
- Mergers and clusters are CFG954's subject.

**R8 causality.**
- Own-baryon fields are retarded (□_ret).
- σ's shape at a point uses the retarded angle average (the past light cone of that point).
- Body signals and relocation currents propagate at c_u = c (declared). The rigid centroid law is the NR (c_u → ∞) limit, valid
  for r_e/c ≪ t_dyn.
- Labels evolve along matter worldlines.

**R9 no action principle (declared cost).** These are retarded non-local equations, which are not Euler–Lagrange equations of any
action; the time-symmetric action form is acausal (CFG947 Mu2).

## 2. Tests (a)–(h) and pass lines

Common inputs:
- CFG4_common (footings, ν_mono, SPARC loader);
- NGC 3198 rotmod at Υ = 0.61 with the spherical-equivalent m_N = r² g_bar/G (the record convention of CFG938/941/947);
- CFG947's census for supply, N = M_c/M_b = (1 − f_b)/(f_r f_b), with the engine's f_ret table and CFG654's native Δ_ta(0)
  (inherited, flagged);
- CFG882's satellites H1–H3 at 50/100/250 kpc from CFG938's 6e10 M⊙ host on its law;
- CFG847's five systems.

### (a) Static law, one domain
- **a1.** NGC 3198, edge at the kernel's own supply root. max |g/g_law − 1| ≤ 1e-6 at the 43 radii, both footings, both kernels,
  under the dust profiles P-S (dust in a shell beyond r_e), P-I (dust = ρ_ph inside r_e) and P-X (dust = 2ρ_ph). Labelled dust is
  inert, so all three must agree. Every radius must lie inside r_e.
- **a2.** Deep points y = g_N/a₀ ∈ {1e-2, 1e-3}, inside r_e: ≤ 1e-6, and V⁴/(G M_b a₀) equal to the law's value there.
  - Reported: y_e, the deepest y inside the edge; V⁴/(G M_b a₀) at y_e; the law's own asymptote at y = 1e-14 (must → 1 within
    1e-6); the Keplerian fall beyond r_e.
- **a3 (reported, no class weight).**
  - SCT-M against the pointwise law for a thin exponential disc with y(R_d) = 10, 1, 0.1: max |Δ| in dex over 0.5–10 R_d.
  - The supply N against CFG803's N_min (3 / 4 in the primary range; 16 / 24 at all radii).
- **(a) PASS iff a1 and a2.**

### (b) FRW and growth
- 𝒮 ≡ 0 on exact FRW (no domain at δ = 0: Δ_ta(z) > 1; labels unset), so T_total is dust with w = 0, isotropic (sympy).
- Linear-regime dust exponent |n − 1| ≤ 1e-12 (CFG941's Lagrangian machinery with no tether).
- Top-hat: no domain is born before turnaround (9π²/16).
- Large-scale growth after domains exist: bodies are free-falling centres of mass, so the coarse-grained source obeys dust
  continuity and Euler at linear order (stated with a sympy check of the body-gas moment equations).
- **(b) PASS iff all hold.**

### (c) No hover and no satellite EFE (SCT-M and SCT-Q)
- **c1.** Δa/g_host = |⟨g_ext⟩_σ,sat − ⟨g_ext⟩_b,sat|/g_host. ⟨⟩ is the mass-weighted mean over the satellite's body and over its
  Plummer baryons, in the host's total field (point baryons plus the host's spherical body). This is the tidal-order differential
  free fall, plus CFG947's retardation bound. Grid: H1–H3 × 50/100/250 kpc × both footings.
  - PASS iff max ≤ ε_B (0.344 canonical / 0.317 alt; CFG945).
- **c2.** EFE on the satellite's own law: 0 dex by construction (own baryons only), plus the effect at the Plummer radius of the
  equilibrium baryon–body offset δ_eq = Δa / [K_bσ (1/M_b + 1/M_c)], K_bσ = (4πG/3)∫ρ_b σ dV.
  - PASS iff |factor| ≤ δ_c = 0.082 dex everywhere (CFG874 via CFG945).
  - Reported: the host tidal term; δ_eq/a.
- **(c) PASS iff c1 and c2.**

### (d) Slip
- The body's isotropic stress completion p(r) = ∫_r^{r_e} σ g dr′, zero at r_e. Labelled dust stress is cancelled (R2).
- s_grad = 4πG r|p|/(c² g) and s_847 = 8πG r² |p|/(c² v_c²), on CFG847's five systems and NGC 3198, both footings.
- **(d) PASS iff worst ≤ 1.9e-5.**

### (e) Conservation
- **e1 (sympy).**
  - Under R4, a conversion event leaves the 𝒮 dipole D_s and the 𝒮 momentum Ḋ_s continuous.
  - Between events, D̈_s = −∫ρ_s∇Φ_m.
  - CFG947's two-blob toy redone under R4 gives relocation term R ≡ 0 for every ε, against E8's −ε(M̈_e X + 2Ṁ_e Ẋ).
  - A spherical body feels no torque about its centre.
- **e2 (N-body toy, §4).** Formation (ramped conversion), anisotropic accretion with angular momentum, satellite infall and a
  head-on merger.
  - Momentum: |ΔP|/P_scale ≤ 1e-10.
  - Angular momentum: |ΔL|/L_scale ≤ 1e-10.
  - Energy: E = K + W + ΣE_int conserved to integrator precision, |ΔE|/|E| ≤ 1e-3, and smaller at dt/2.
  - Reported: ΔE_int per event class relative to |E|.
- **e3.** The force between two overlapping spherical bodies (shell quadrature) is equal and opposite to ≤ 1e-6 relative, computed
  both ways.
- **Grades.**
  - Momentum and angular momentum: PASS iff e1, e2 (P, L) and e3 hold.
  - Energy: PASS if it closes with E_int ≡ 0; CONDITIONAL if it closes only through E_int (a declared reservoir, as CFG950's R-E);
    FAIL if it does not close.
  - **(e) = the worse of the two.**

### (f) Dwarfs: the law with no RMIN
- Every collapsed system with baryons has a domain, whatever its mass.
- For CFG939's classes (UFD-c 5e3 M⊙ / 30 pc, UFD-e 3e4 / 240 pc, Draco-like 5e5 / 220 pc, Fornax-like 4e7 / 710 pc; Plummer)
  and H1–H3:
  - σ ≥ 0;
  - the law holds to 1e-6 inside r_e;
  - the edge moves the isotropic-Jeans aperture σ²_los(<R_e) by ≤ 0.082 dex against the untruncated law.
- Also checked: the CFG939 SPARC dwarf's rotation point lies inside its edge, and the mass grid 1e3–1e15 M⊙ has a domain with
  σ ≥ 0.
- **(f) PASS iff all hold.**
- Excess family (reported, no class weight, stated plainly): SCT's prediction for every dwarf is the EFE-free law of its own
  baryons. Any handle must be shown by a computation, otherwise "no handle".

### (g) Below-law systems
Data, statistic and class rule are CFG936's (per-object values read from its committed results JSON, read-only): class T = the six
Lelli+15 TDGs (dex); class U = DF2 and DF4 (ln σ²).
- **SCT-M.** In-situ systems (R1) have no own body, and the parent's monopole body has no local structure, so the prediction is
  Newton (f = 0).
- **SCT-Q.** In-situ systems are inside the parent's pointwise phantom, so the prediction carries the host EFE: CFG936 route (iii),
  FM12 eq. 60 (a declared approximation).
- Also stated: consistency with CFG939's no-capture criterion, and CFG948's Coma UDGs (reported).
- **Grades.**
  - PASS: T and U both EXPLAINS on both footings, with no extra premise.
  - CONDITIONAL: U needs the premise that DF2/DF4 are in-situ debris (the record's reading).
  - FAIL: T or U FAILS on either footing.

### (h) CFG678 scorecard (reported, no class weight)
- SCT has no action. Gates produced by the action-less 𝒮 sector cannot PASS: they are CONDITIONAL with the premise named, or
  UNTESTED. A gate fully set by the variational sector (GR + matter) is scored normally.
- C1 (Cassini) and the wide binaries are evaluated for both variants from the R1/R3 rules, citing G01/G02 and CFG653.

### Clusters (first-order statement only; CFG954 decides)
Members keep their whole bodies until R7, and the host's body is the law of the host's own baryons. The cluster therefore lies
between CFG951's "plain law" row (all merged) and its X-OD row (members kept, there truncated at L2). This is stated from the
record, not computed.

## 3. Structural statements (each counts only with its check)

| id | statement | check / falsifier |
|---|---|---|
| S-P | total momentum Σ_{b,unl} m v + Σ_q M_c V_q is exactly conserved | sympy event algebra + toy; falsified if any event or step changes it beyond round-off |
| S-L | total angular momentum including S_q is exactly conserved | sympy (no torque on a sphere about its centre) + toy |
| S-TM | R4 escapes CFG947's T-M: relocation term R ≡ 0. The price is that the body's centroid is the converted dust's centroid, so the baryons sit off it by δ until mutual gravity re-centres them | falsified if R ≠ 0 under R4 |
| S-Z | zero-sum per domain, ∫ρ_s = M_c − M_c,lab = 0, exactly | identity |
| S-+ | σ ≥ 0 ⟺ M_ph(<r) non-decreasing. This holds whenever M_b(<r) is non-decreasing, for kernels with dg_law/dg_N ≥ 1 | sympy (simple kernel) + numeric (ν_mono); NGC 3198's m_N profile checked |
| S-E | the edge is forced inside turnaround, r_e < r_ON, for M_b 1e3–1e15 | CFG947 T-E with the kernel's own root |
| S-C | every kernel retarded; the response vanishes before r/c | sympy |
| S-En | building a body releases energy E_rel = −ΔW (dust uniform within r_ON at turnaround → body inside r_e, baryons fixed) | table over M_b, both footings, in units of \|W\| and M_c c² |

## 4. Declared toys

**N-body toy (e2).** Code units G = a₀ = 1, simple kernel, 3-D. Baryon–baryon and baryon/dust–dust forces are Plummer-softened
Newtonian (ε = 0.05). The body–particle force is G m M_σ(<r)/r² (r floored at ε), pairwise. The body–body force uses shell
quadrature. Leapfrog KDK.
- **Run E (events).** Host A: 200 Plummer baryons, a = 1, M_b = 1.
  - Formation: a uniform dust sphere (200 particles, R = 10, mass 20, at rest) is converted in random order over τ_conv = 5 from
    t = 0.5.
  - Accretion: a cold dust stream (60 particles, mass 2, cylinder of radius 1 and length 10) starting at x = 30 with velocity −0.8 x̂
    and impact offset 3 ŷ. It is converted on entering r_lab = 25 of X_A.
  - Satellite B: 60 Plummer baryons, a = 0.1, M_b = 0.02, existing body M_c = 0.4, starting at (0, 12, 0) with velocity (0.6, 0, 0).
  - Baryon velocities: isotropic, 1-D dispersion 0.5 v_c(r) of the final law potential. Seeds fixed in code.
  - t ∈ [0, 40], dt = 2e-3, rerun at dt = 1e-3 for the energy check.
- **Run M (merger).** Two equal domains (150 Plummer baryons each, a = 1, M_b = 1, M_c = 20) start at rest at separation 8. They merge
  under R7 at baryon-centroid separation ≤ 1.305 (the Plummer half-mass radius), with no blend in the primary run. Run to t = 30.
  - Reported: ΔE_int at the merge, and the T-L field jump (g at r = 5 just before and just after).
- **Reported diagnostics.** The baryon–body offset |X_b − X_q| over time; satellite B's offset against its a.

**Two-blob toy (e1).** CFG947's E8 toy (core plus two blobs at ±X with dipole fraction ε, M_e/M_dom = ½, growth time = dynamical time),
with the draw replaced by R4 conversion.

## 5. Controls and MUTATE

**K controls** (VOID rule: if any K fails, the classes are VOID, reported but not graded).

| id | target | line |
|---|---|---|
| K1 | CFG938's reduced EL law on NGC 3198 | ≤ 1e-6 both footings (record 2.2e-16) |
| K2 | CFG947's no-hover retardation bound 1.2114e-6; CFG941's tethered hover 1.017–1.107 and EFE −0.73…−0.10 dex | bound within 1%; ends within 0.005 / 0.01 |
| K3 | CFG941 exponents 0.60954 / 0.69433 and dust n = 1 | 1e-4; 1e-12 |
| K4 | CFG947 slip: worst 1.6324e-5 (P-I, the dust's own pressure) and the 𝒮 P-S stress 1.2955e-5 (alt cluster) | each within 1% |
| K5 | CFG4 SPARC local law 0.1003 @ Υ 0.61 / 0.0991 @ 0.57 | rms within 1.5e-4, Υ exact |
| K6 | CFG947 T-M for E8: R/(M_dom g_ref) = π²ε/4 → 0.024674 / 0.246740 / 0.740220 | 1e-6 |
| K7 | CFG936 route (i) class T (r̄ +0.054634, χ² 1.1680) and route (iii) class T canonical (r̄ −0.381410, χ² 14.8547), recomputed from the stored per-object values | 1e-6 |
| K8 | CFG947 T-E minimum M_law(<r_ON)/M_ta = 1.847 and the T-R threshold M_b = 4.815e10 M⊙ | 1e-3 relative |

**MUTATE.** Separate outputs (`*_MUTATE`); exit 1 when every tooth bites, 2 if any does not.

| tooth | change | bites if |
|---|---|---|
| Mu1 | global source (body from the global baryon field) | \|EFE\| ≥ 0.05 dex somewhere on the H1–H3 grid (CFG947 T-X) |
| Mu2 | tether instead of source | Δa/g_host ≥ 0.5, n differs from 1 by ≥ 1e-3, and the linear C₁C₂ coefficient is 0 (theorem D-T) |
| Mu3 | body glued to its baryon centroid (no inelastic absorption) | toy momentum drift ≥ 1e-3 P_scale, and two-blob R ≠ 0 |
| Mu4 | no cancellation (labelled dust gravitates on top of the body; P-I) | NGC 3198 dev ≥ 1e-3 |
| Mu5 | no E_int (reshaping and event work not booked) | toy \|ΔE_mech\|/\|E\| ≥ 1e-3 and ≥ 10 × the integrator error |
| Mu6 | time-symmetric kernel | a nonzero precursor before switch-on |
| Mu7 | no supply edge (untruncated law phantom) | created 𝒮 mass at r_ON > 1e-6 M_b |

## 6. Classes

Graded tests are (a)–(g). (h) and the cluster statement are reported only.

**Per variant (SCT-M, SCT-Q).**

| class | condition |
|---|---|
| SCT CONSISTENT | every graded test PASSES. A PASS may rest on declared costs (the action-less 𝒮, retarded non-local kernels, latched labels, rigid bodies, E_int, S_q), never on an unproved condition. The costs are listed |
| SCT CONDITIONAL | no graded FAIL, and at least one graded test is CONDITIONAL. Each condition is named |
| SCT INCONSISTENT | at least one graded FAIL, with the obstruction shown: a computed violation beyond the line that no declared rule removes |

**Overall.** The class of SCT-M, the primary. SCT-Q is reported with its own class.

**Conditions named in advance** (each makes the class CONDITIONAL wherever it is needed for a PASS):
- C-MR: real galaxies are single-domain only if R7 has acted (T-L non-additivity otherwise; CFG954 tests R7);
- C-E: energy closes through E_int;
- C-DF: DF2/DF4 are in-situ debris;
- C-c: a finite-c_u body exists whose NR limit is R4.

## 7. Design-stage disclosures (not blind)

**Read before freezing:**
- README, DERIVATION, criteria and code of CFG947;
- READMEs of CFG935, 936, 938, 939, 941, 944, 945, 946, 950, 951 and 952;
- LEDGER rows CFG801, 803, 748, 940–952;
- CFG678's criteria; CFG936's results JSON (structure and route values); CFG951's X-OD definition;
- CFG954's frozen criteria (read only, after it landed; it uses CFG947's clip-and-carried-weights statement, which differs from R2–R4
  here).

**The choice of SCT-M as primary was made with CFG936's TDG result in view.** A pointwise own-baryon phantom gives in-situ systems the
host EFE (route iii), which CFG936 found FAILS for the TDGs. SCT-Q is kept as a scored variant so that the choice and its cost are
visible.

**Expectations (paper estimates, no script run):**

| # | expected result |
|---|---|
| X1 | (a) exact to round-off for any dust profile |
| X2 | (b) passes by construction |
| X3 | Δa/g_host ~ 1e-5 – 4e-3 (≤ ε_B); δ_eq/a ~ 1e-2 for H3; EFE ≪ 0.082 dex |
| X4 | slip ~ 1.2–1.5e-5 |
| X5 | toy P and L to round-off; Mu3 leaks O(accreted momentum) |
| X6 | E_int at formation O(1) of the binding energy (~1e-7 – 1e-6 of M_c c²); merger O(0.1–1) |
| X7 | SCT-M TDGs and DF2/DF4 EXPLAIN; SCT-Q TDGs FAIL |
| X8 | SCT-M CONDITIONAL (C-MR, C-E, C-DF, C-c); SCT-Q INCONSISTENT |
| X9 | no handle on the excess family |

## 8. Compute

- One process at a time; OMP_NUM_THREADS=1; nice -n 10; in-script RSS guard at 1 GB; sympy, numpy and scipy only.
- No downloads. No other lane's files edited.
- Read-only inputs: CFG4_common, the record's SPARC files, CFG654's Δ_ta JSON, CFG936's results JSON.
- Stages K, MUTATE and main, in that order, with separate outputs.
