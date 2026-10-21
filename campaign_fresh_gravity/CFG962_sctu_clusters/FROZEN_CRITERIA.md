# CFG962: SCT-U clusters (SCT-M + kinematic retention u = f_P + partial body stripping). FROZEN CRITERIA

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-21.
Block CFG960–969 (LEDGER reservation row "CFG960–969", entry "CFG962 (10-21): SCT-U clusters, i.e. CFG953 SCT-M + CFG959 retention
(dispersion-supported domains keep native dust unconverted, u = f_P) + partial body stripping beyond r_J (stripped body mass reverts
to dust); does it fix CFG954's core and merger-memory failures without breaking galaxies?").

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², scored separately, never pooled. Kernel ν_s
(CFG695; CFG726/916/951/954 cluster primary) for every SCT body in clusters, members and the merger toy; each reused record estimator
keeps its own kernel (CFG959's SPARC ν_simple = ν_s; its UDG/lens/dwarf estimators ν_e; CFG953's satellites law_simple). "Cold energy"
/ cold dust throughout; its mass is still required; no particle species. Raw data and framework-native inputs only: no ΛCDM halo, mass
function, merger tree, HMcode/BAHAMAS or standard-MOND yardstick enters any verdict. Not "theory closed". Nothing here says the data
favour the framework. A FAIL is reported as plainly as an OK.

**Machine limit (declared; a 1024³ CFG960 job is running).** One process at a time, one core (OMP_NUM_THREADS=1), nice 10. In-script
RSS guard at 0.95 GB (exit 3). Start guard: free+inactive+speculative < 8 GB ⇒ exit 75. Run guard: if it drops below 3 GB the script
pauses (re-checks every 60 s for up to 30 min, then exit 75). Stages split (COMPUTE / K / MUTATE / MAIN). Every file write outside this
lane's directory is refused by a guard on `open`. No download. CFG960's directory, processes and outputs are not touched.

## 0. Status: POST HOC; every target was already seen

All targets (CFG687 eRASS1 318 and its T2 slope 0.896 ± 0.209, CFG686 ACCEPT 8, CFG949 B0, CFG954 R1–R3 / never-absorb / reading N,
CFG959 H-UNR items, CFG933/948 Coma UDGs, CFG916/599 Bullet inputs, CFG953 satellites) were measured and read before this lane. A pass
would be an accommodation, not a prediction. SCT-U was chosen with CFG954's and CFG959's results in view.

**Hand estimates made while writing (disclosed; from record numbers already published, no script of this lane):**
- **Core (MID).** u = f_P = 1 for clusters (no ordered rotation) means the cluster domain converts nothing. Its dust stays native, so
  the host is CFG949's B0 (A_MID 1.011 ± 0.063). Members add co-distributed mass and take it out of B0's supply. Reading N's members
  held C_J/S_B0 ≈ 0.15 (median) with r_J ≈ 97 kpc in a B0-like host. Expectation: A_MID ≈ 0.95–1.10, i.e. the core failure goes away.
- **Memory (OUTER).** Members (red sequence, u = 0.80) keep body(<r_J) + their own native debris(<r_J): a hand estimate gives ≈ 8 m_i
  per member at r_J ≈ 100 kpc (a 2.7e11 M⊙ member: body ≈ 4 m_i, debris ≈ 4 m_i), i.e. ≈ 0.2 of S_B0. Expectation: A_OUTER ≈ 0.85–0.95,
  between B0 (1.047) and never-absorb (0.771). Whether it clears Z = −2 on the alt footing is not known.
- **Merger toy continuity (J).** Every own-domain rule in CFG954 failed J ≤ 0.05 (R2 0.385 at q = 1), because two own-domain laws
  differ from the law of the combined baryons by O(√2 − 1) in the deep regime. Partial stripping does not remove that. Expectation:
  (b-J) FAILS (J ≳ 0.2 at q = 1) and with it the overall class under the inherited rule.
- **Coma UDGs.** u = 1 (dispersion-supported): no body; native debris only. CFG959 found them below the law (resid +1.18 ln, z +4.5).
  CFG954 found r_J/r½ ≥ 4.45 with law masses, so partial stripping should not reach r½. Expectation: (c1) no stripping side effect;
  (c2) CONTRADICTED, as CFG959.
- **SPARC** = CFG959 (a) (0.1013 / 0.1002 PASS), because SCT-U on one isolated domain is H-UNR's reading R-C. **dSphs** at u = 1 =
  CFG959 (b): −0.57 dex predicted against +0.37 observed, worse than SCT-M's law (0 dex).
- **Bullet:** UNDERDETERMINED by input (no pericentre in the record). **Momentum through stripping:** exact by construction.
  **Satellites:** no hover, no EFE (inherited, tidal order).
- **Expected overall: SCT-U CLUSTERS FAIL through (b-J),** with the cluster-profile sub-class FIXED or PARTIAL. Stated before any
  number is computed.

## 1. The SCT-U statement (zero new constants)

- **U0 chassis = CFG953 SCT-M, R0–R9, unchanged** except U1–U2. G = 8πG(T_b + T_c + 𝒮); 𝒮 = Σ_q σ_q − T_c,lab (labelled dust inert);
  σ_q spherical about its centroid, M_σ,q(<r) = min{r²[g_law(ḡ) − ḡ]/G, M_c,q}, ḡ from the domain's OWN baryons (monopole); edge at
  the supply root; R4 centroid momentum; R5 spin; R6 E_int; R7 merges (bound fraction < ½, or coalescence; inelastic); R8 retarded;
  R9 no action. Own-baryon sourcing, no cross-sourcing, no EFE, no tether.
- **U1 partial conversion (CFG959's derivation).** At conversion a domain converts only the fraction (1 − u) of its dust. u = f_P =
  3σ²/(v² + 3σ²), measured from the domain's own kinematics (random motions exert no secular torque; virial share). The converted part
  is the SCT-M body with supply (1 − u)S: M_σ(<r) = min{phantom of own baryons, (1 − u)S}. The unconverted part u·S stays real,
  gravitating, unlabelled native dust in the CFG930 R930 NFW (C 3000, r_ta boundary, native EPS z_c). For one isolated domain this is
  exactly CFG959's reading R-C: g = g_N + G[min(M_ph, (1 − u)M_c) + u M_cNFW]/r².
  - Capture: unlabelled dust that becomes bound to an existing domain is converted at that domain's (1 − u) (CFG953's inelastic capture
    with U1's fraction). A u = 1 domain therefore never converts.
- **U2 partial stripping.** When a member body's tidal radius r_J (CFG916 King r_J at pericentre, latched as the running minimum) falls
  inside its edge, the body mass beyond r_J reverts to unlabelled dust; the part inside r_J persists unchanged (no reshaping).
  - **D-REV (the reversion event, defined).** The reverted dust is created with exactly the stripped shells' mass distribution, centroid
    and velocity (the body's V_q), and the domain's labelled-dust ledger T_c,lab is debited by the same 4-current. Then 𝒮 changes by
    −σ_strip + T_rev = 0 at the instant: mass, momentum, dipole, angular momentum and the gravitating density are continuous, and
    ∇·𝒮 = 0 is kept (T_rev is geodesic dust afterwards). This is gentler than CFG954's R1 (whole-body absorption) and differs from R3
    (which relocated the stripped 𝒮 into a static host body and kept the host's own dust converted).
  - A member's own unconverted native debris is real dust: beyond r_J it is tidally stripped as ordinary dust; inside r_J it stays bound.
- **U3 everything else as CFG953** (labels latched at turnaround; in-situ systems are not domains and stay Newtonian; R7 merges on the
  baryonic bound fraction < ½ or centroid coalescence, inelastic). R7's bound fraction is the member's baryonic (Hernquist) fraction
  inside r_J, as CFG951 used it.
- **U4 energy bookkeeping (CFG958, CONDITIONAL there).** A D-REV event changes no field at the instant (ΔW = 0, ΔK = 0); R7 merges and
  reshaping still need E_int, which CFG958 converts into its interacting-vacuum channel (C-E CONVERTED, not derived). Reported, not
  graded here.

## 2. u per class (declared from data already in the record; no fitting)

| system | u used | from |
|---|---|---|
| cluster domains (eRASS1 318, ACCEPT 8, Bullet main and sub) | **1** | f_P with v = 0: the record's cluster inputs carry no ordered rotation; σ = the isotropic-Jeans σ of the gas tracer (CFG916 harness) |
| cluster members (CFG726 λ from CFG688's redMaPPer match: red-sequence galaxies) | **0.80** | CFG919 / CFG959 early-type class value (n > 2 Sérsic proxy) |
| SPARC discs | 3σ²/(V_flat² + 3σ²), σ = 10 km/s | CFG959 (a) (median ≈ 0.029, max ≈ 0.49) |
| merger-toy galaxies (1e11 L* progenitors) | the SPARC median f_P (CFG959, σ 10 km/s) | disc progenitors |
| dSphs (CFG880 83), Coma UDGs (CFG933 9), satellite dwarfs H1–H3 | **1** | dispersion-supported, no rotation data on disk (CFG959 class value) |
| TDGs, DF2/DF4 | not domains (in situ) | CFG953 R1 |
| red / blue lenses, McQuinn rotators (carried, reported) | 0.80 / 0.20 / f_P(V_rot, 10 km/s) | CFG959 |

Declared brackets (each can move a class to CONDITIONAL where §4 says so): members u = 0.20 (the n < 2 class); toy u = 0.80. Reported only
(no class weight): members u = 0 and u = 1; UDGs and satellites u = 0. The u "at conversion" is the present-day class value (the record has
nothing earlier); disclosed.

## 3. Cluster profiles (eRASS1 and ACCEPT; per cluster, per footing)

**Inputs.**
- Host baryons and native dust: CFG949's B0 primary corner, built by CFG949's own code (its script slice exec'd read-only, as CFG959
  did): baryons M_b = 1.20 × CFG922 gas_beta (eRASS1) or gas_accept (ACCEPT); native dust M_c,B0 = (1 − f_b,N) M_ta NFW with S-cen
  supply (census f_ret), R930 C 3000, r_ta(z_i), each cluster's own z. Total cold S_B0 = M_c,B0(∞).
- Members: CFG954's harness (its code exec'd read-only): N_mem = λ (CFG726), equal masses m_i = M*/N_mem, Hernquist R_e 15 kpc,
  co-distributed with the gas (erass_gas / accept_inputs), CFG916 isotropic Gauss–Hermite × Gauss–Laguerre orbit nodes, King r_J at
  pericentre in the host's current total.
- Member supply S_i = 53.64 m_i (CFG726 prog_halo, the harness's condensed-floor convention). Member body = `phantom_trunc` with supply
  (1 − u_m)S_i (at u_m = 0 identical to CFG954's h). Member debris = u_m S_i × NFW shape of prof930(M_ta = S_i/(1 − f_b,N), z_cluster,
  3000, r_ta). Member own mass for r_J: m_i·hern + body + debris.

**Primary profile (SCT-U, u_cl = 1, u_m = 0.80, R7 on, pericentre, stripped cold joins the host's native dust: placement P-NFW).**

    M(<r) = M_b(<r) + C_J(<r) + min{T_law(src)(<r), M_rem} + f_U · M_c,B0(<r),    f_U = (S_B0 − C_J,tot − M_rem) / S_B0

- C_J = N_mem × (member body + debris inside r_J), convolved over kept (non-merged) nodes (CFG951's matrix convolution).
- R7: a node with Hernquist fraction inside r_J < ½ merges; its body inside r_J (M_rem, summed) becomes the merged host-domain body,
  the law of the host-domain baryons src (gas + stripped stars of kept nodes + all stars of merged nodes, CFG954 R3's placement) capped
  at M_rem; its debris inside r_J joins the host's dust. With u_cl = 1 the host converts nothing else.
- Everything stripped (body beyond r_J by D-REV, debris beyond r_J) is unlabelled dust of a u = 1 domain: never reconverted, and placed
  in B0's native NFW shape (it phase-mixes into the host's collapse debris), mass conserved through f_U.
- Self-consistency: start from B0 (M_b + M_c,B0); iterate the host total for r_J (≤ 8 iterations, tol 1e-4 on max |ΔM/M|; the CFG954
  convention). Non-converged clusters are counted. If the last two iterations give different classes for an item, it is UNDERDETERMINED.
- Mass bookkeeping: C_J,tot + M_rem + f_U S_B0 = S_B0 per cluster (≤ 1e-9 relative). If f_U < 0 would be needed, f_U is floored at 0
  and the cluster is counted as a bookkeeping violation (the members then hold more cold than B0's census supply).
- ΔΣ: CFG949's `dsig_newton`; eRASS1 scored with CFG949's `STE.band` (CFG687's 30-patch RA jackknife) and `s_model` (CFG687 T2);
  ACCEPT with CFG949's ACCEPT `Stack` ("boot"). Both equal CFG954/CFG687 scoring on the law (K).

**Declared brackets** (each can move (a)/(b-ACC) classes to CONDITIONAL):
- B1 present-epoch r_J (instead of pericentre);
- B2 placement P-ORB: stripped cold follows the members' orbital distribution (gas-co-distributed, CFG954's convention for stripped
  stars) instead of joining B0's NFW;
- B3 members u_m = 0.20;
- B4 R7 off (no merges);
- B5 members keep only their body inside r_J; their own native debris is part of the host's native NFW (the "cluster NFW already
  contains substructure" convention).
Reported only: u_m = 0 (SCT-M bodies, stripped, in a native host) and u_m = 1 (members fully native).

## 4. Tests (both footings)

**(a) eRASS1 318.** A_MID (0.5–1.2 Mpc), A_OUTER (1.2–3 Mpc), Z = (A − 1)/σ_jk; outer mass slope s vs 0.896 ± 0.209.
- (a-MID) core and (a-OUTER) memory: CONSISTENT iff |Z| < 2 on both footings; INCONSISTENT iff |Z| ≥ 2 on both; else CONDITIONAL. A
  bracket B1–B5 with a different class makes the item CONDITIONAL.
- (a-s): CONSISTENT iff |s − 0.896| < 2 × 0.209 on both footings; INCONSISTENT iff ≥ 3 × 0.209 on both; else CONDITIONAL; brackets as
  above. CFG688's binning dependence (NOT SETTLED) is disclosed with the result.
- Reported: f_U, C_J,tot/M*, C_J,tot/S_B0, median r_J, merged fraction, iterations, bookkeeping residuals, terciles.

**(b) Merger memory.**
- (b-ACC) ACCEPT 8 OUTER (and MID reported): the (a) rule on Z_OUTER, brackets as above. Because B0 alone already sits at ACCEPT OUTER
  0.71 ± 0.17 (Z −1.7; CFG949 gave ACCEPT no class weight), an INCONSISTENT (b-ACC) caps the overall at CONDITIONAL; it does not by
  itself FAIL the lane.
- (b-J) merger-toy continuity (CFG954 (e) set-up: m₁ = 1e11, q = 1, 1/3, 1/10, Hernquist R_e 15 kpc, z = 0, ν_s, quasi-static radial
  approach d = 1000 → 0.5 kpc (Δ ln d = 0.005), then 0; CFG951's frozen J metric: the maximum over observables and over every window of
  one dynamical time of |ΔE|, an instantaneous jump counts in full). SCT-U rules in the toy:
  - label i content: M_b,i + body_i (law phantom of own baryons capped at (1 − u)S_i) + debris_i (u S_i NFW), S_i = 53.64 m_i;
  - label 2 truncated at r_J,2 = King r_J in label 1's own content (latched running minimum); its stripped cold is unlabelled dust bound to
    label 1: captured and converted at (1 − u₁) into label 1's body supply (centred on label 1; the cap is checked and reported), the
    remaining u₁ fraction stays comoving with centre 2;
  - label 2's stars never source label 1 until R7; R7 fires when label 2's Hernquist fraction inside r_J,2 < ½ or at d = 0: label 2's
    kept body merges into one body about centre 1, the law of the combined monopole-enclosed baryons capped at the summed body mass
    (CFG954's R1 convention); label 2's kept debris stays comoving dust;
  - E₁ = M_v/M_GP − 1 at R = 20, 50, 100, 200 kpc about centre 1 (M_GP the label-free law of the monopole-enclosed baryons); E₂ =
    [M₂,v − M₂,grav]/M₂,own at R = 5, 10, 20 kpc about centre 2, with M₂,own = M_b,2 + body₂ + debris₂ and M₂,grav = M_b,2 + (body₂ +
    debris₂)(<min(R, r_J,2)); dynamical times from the label-free remnant law (centre 1) and label 2's own content (centre 2).
  - Rule: CONSISTENT iff J ≤ 0.05 for every q on both footings at the primary toy u; INCONSISTENT otherwise. The u = 0.80 bracket is
    graded the same way and a different class makes it CONDITIONAL. Reported: J without R7.

**(c) Coma UDGs (9 admitted).**
- (c1) cluster-rule side effect: each UDG's King r_J in the Coma β-model host (CFG948/954 L23 inputs), solved self-consistently with
  its SCT-U mass (Plummer baryons from the CFG954 table + u = 1 native debris), at its 3D distance dmean (primary) and dproj (reported).
  CONSISTENT iff r_J ≥ r½ for all 9 on both footings at dmean (stripping leaves the aperture untouched); otherwise CONDITIONAL, with the
  truncated prediction reported. Reported: r_J/r½, and the u = 0 bracket's r_J ("do they keep enough body inside r_J").
- (c2) where they land against the observed excess: CFG959's estimator (CFG933 membership) at u = 1, z = residual/se; CONTRADICTED iff
  z ≥ 3 on both footings. Also the CFG948-style z with σ_sys (CFG954's convention) and the u = 0 bracket (the whole body kept: the law).
  (c2) is graded but enters the galaxy-scale / excess-family statement, not the cluster class: SCT-U is not expected to fix it.

**(d) SPARC rotators stay on the law.** CFG959's SPARC engine (CFG695 S2 recipe, Υ refit 0.30–1.20) with R-C at u = f_P (σ 10 km/s):
PASS iff rms ≤ 0.110 with Υ in [0.50, 0.80] on both footings; reported Δ against the law's 0.10091 / 0.09943. The monopole-vs-pointwise
body difference (≤ 0.054 dex for LSB discs, CFG953) is inherited, as CFG953's C2 did.

**(e) TDGs and DF2/DF4 Newtonian (inherited).** CFG936 route (i) via CFG959's `f_items`: CONSISTENT iff both are |z| < 2 on both
footings. SCT-U does not change in-situ systems (not domains).

**(f) Momentum and mass through stripping events.**
- (f1) event algebra on a discretised member (body shells + debris shells, cluster-median member and the toy secondary): ΔM, ΔP, ΔD
  (dipole), ΔL and the gravitating density across one D-REV event.
- (f2) dynamical toy: a host (1e12 M⊙, softened point, ε 30 kpc) and a satellite (Hernquist baryons 1e10 M⊙, R_e 3 kpc, softened
  ε 3 kpc; its body + bound debris as rigid shells about its centroid, u = SPARC median and u = 0.80, ν_s, both footings) on an
  eccentric orbit (start 300 kpc, tangential speed 0.5 v_circ), leapfrog for 4 Gyr. At every pericentre the King r_J (point host) is
  latched and the shells beyond it become dust particles by D-REV (antipodal pairs on each shell, the satellite's velocity). All pair
  forces are antisymmetric (point–point softened; shell–point by the shell theorem); dust–dust pairs are omitted, which keeps total
  momentum exact.
- Contrast (reported): the same events with the stripped mass relocated into the host at the host's velocity (CFG954 R3 [P-S]-type).
- eRASS1 bookkeeping identity (§3).
- Rule: CONSISTENT iff |ΔP|/P_member ≤ 0.01 at every event and every (f1) case, the run's total-momentum drift ≤ 1e-9 of the satellite's
  momentum scale, mass exact, and the eRASS1 identity ≤ 1e-9 in every unfloored cluster; INCONSISTENT iff the event momentum test
  exceeds 0.01; CONDITIONAL otherwise. Energy changes at events are reported and booked per U4 (no grade).

**(g) Bullet (CFG599 progenitors; the pericentre is not in the record).** Both main and sub are clusters: u = 1, so their cold is native
dust (no body). Sub and main: CFG599's baryons (Progenitor599 M200 1.5e15 / 1.5e14, cool-core cloud on the sub) + native NFW
(mta_fixed of their baryons, prof930 C 3000 r_ta, z 0.296). King r_J(d_p) of the sub in the main (CFG916 solver). φ_J(d_p) = 1 −
M_c,sub(<min(r_J, 200 kpc))/M_c,sub(<200 kpc) counts dust stripped from the sub's core as relocated (conservative). CFG916's B rule:
CONSISTENT iff φ ≤ φ_lin,H (CFG915: 0.0390 / 0.0411), INCONSISTENT iff φ ≥ 0.9, else UNDERDETERMINED; evaluated for every
d_p ∈ (0, 720] kpc; if the class changes across that range, (g) is UNDERDETERMINED (by input). Reported: under D-REV / collisionless
dust the stripped core dust keeps the sub's velocity, so no 𝒮 is relocated (φ_reloc = 0).

**(h) Satellites: no hover, no EFE (CFG945's bound).** CFG953's (c) machinery (copied; HOSTS882 H1–H3 at 50 / 100 / 250 kpc in the
6e10 host, law_simple host field): Δa/g_host between the satellite's cold and its baryons (+ CFG953's stored retardation term) against
ε_B 0.344 / 0.317, and the EFE against δ_c 0.082 dex. Primary u = 1 (native debris truncated at the Jacobi radius; EFE 0: no body);
bracket u = 0 (body truncated at the Jacobi radius by U2). PASS iff both hold for every satellite, radius and footing, in the primary
and the bracket.

**(i) dSph excess (carried from CFG959 at u = 1; reported with a grade).** CFG959's dwarf estimator (83 CFG880 dSphs): the SCT-U residual
against SCT-M's (the law, u = 0). Graded WORSE iff |residual(SCT-U)| > |residual(SCT-M)| on both footings.

## 5. Classes

- **Cluster-profile sub-class** (what the lane set out to fix): **FIXED** iff (a-MID), (a-OUTER), (a-s) are CONSISTENT and (b-ACC) is
  not INCONSISTENT; **NOT FIXED** iff (a-MID) or (a-OUTER) is INCONSISTENT; **PARTIAL** otherwise.
- **SCT-U CLUSTERS** (overall):
  - **FAIL** iff any of (a-MID), (a-OUTER), (a-s), (b-J), (f) is INCONSISTENT, (c1) is INCONSISTENT, or (g) is INCONSISTENT for every
    d_p;
  - **OK** iff (a-MID), (a-OUTER), (a-s), (b-ACC), (b-J), (c1), (f), (g) are all CONSISTENT;
  - **CONDITIONAL** otherwise (including an INCONSISTENT (b-ACC), an UNDERDETERMINED Bullet, or bracket-driven CONDITIONAL items).
- **Galaxy scale:** CFG953's class is carried (**CONDITIONAL**: C-E, C-DF) iff (d) PASS, (e) CONSISTENT and (h) PASS; FAIL if any of them
  fails. Stated alongside, never folded away: (c2) and (i). If (i) is WORSE, the galaxy-scale label is "CONDITIONAL (rotators, in-situ,
  satellites) + DWARF EXCESS WORSE than SCT-M".

## 6. Controls

**K (each must pass, or the item it guards is VOID).**
- **K1 CFG954 numbers.** CFG954's stored work arrays (R1PS, R2, R3, law, never-absorb `na_sct`, H-MM) scored with CFG954's own scorers
  reproduce `cfg954_results.json` T_R / T_A and `cfg954_results_MUTATE.json` MU-NA (≤ 1e-12): R1 [P-S] OUTER 0.950 / 0.863, R2 0.868 /
  0.793, never-absorb 0.771 / 0.762, R3 MID 1.710 / 1.563.
- **K2 CFG954's runner (exec'd)** recomputes R2 and R3 for the first 6 eRASS1 clusters, both footings, equal to the stored arrays
  (≤ 1e-10 relative).
- **K3 CFG949 B0.** eRASS1 A_MID 1.0109 ± 0.0632, A_OUTER 1.0469 ± 0.0888, s 0.6615 and ACCEPT 8 B0 bands (MID 0.657 ± 0.149,
  OUTER 0.710 ± 0.169) from `cfg949_results.json` (≤ 1e-9).
- **K4 CFG959 numbers.** Through CFG959's exec'd slice: its (d) clusters (= B0), (a) SPARC rms/Υ, (b) dSph E/se, (c) Coma mean
  residual/se, (e) red lenses and (f) TDG/DF items at the primary setting equal `cfg959_results.json` (≤ 1e-9).
- **K5 CFG954 reading N.** Its stored N+members arrays scored with CFG949's STE reproduce `cfg954_results.json` reading_N (≤ 1e-12).
- **K6 toy.** CFG954's exec'd `toy_sct` reproduces its stored J for every rule, q and footing (≤ 1e-12); this lane's SCT-U toy at u = 0,
  R7 off, equals CFG954's R2 row (J and E₁ finals, ≤ 1e-10).
- **K7 CFG916 King r_J.** Bullet sub at 720 kpc (303.76 / 305.94 kpc, ≤ 1e-9); eRASS1 pericentre median 178.046 / 178.704 kpc from the
  stored CFG954 diagnostics (≤ 1e-6).
- **K8 CFG953 satellites.** The copied `sat_c` reproduces CFG953's stored (c) values for all 18 cases (≤ 1e-12).
- **K9 member profile.** This lane's member body at u_m = 0 equals CFG954's h (`prog_halo`) exactly for every eRASS1 cluster; the host
  baryons B0 M_b and CFG954's ctx M_b agree (max relative difference reported; ≤ 1e-6 required, else the host uses B0's).
- **K10 scorers.** CFG949's `STE.band` and CFG954's `score_TR` give the same A on CFG954's stored law arrays (≤ 1e-9).

**MUTATE (separate `_MUTATE` outputs; exit 0 iff every tooth bites and the control holds).**
- **MU-U0 (u ≡ 0 everywhere).** (i) This lane's runner with u ≡ 0, CFG954's supply S_tot, CFG954's baryons, R7 off and the plain-law
  start reproduces CFG954's stored R3 arrays (eRASS1 and ACCEPT, both footings, ≤ 1e-10) and fails the core: Z_MID ≥ +2 on both
  footings. (ii) u ≡ 0 with the primary's B0 baryons and supply S_B0, R7 on: Z_MID ≥ +2 on both footings. Bites iff both.
- **MU-NS (no stripping).** (i) u ≡ 0, no stripping, S_tot reproduces CFG954's never-absorb `na_sct` arrays (≤ 1e-10) and fails OUTER
  (Z_OUTER ≤ −2 on both footings). (ii) the primary u's (1 / 0.80) with no stripping (supply S_tot, where Σ S_i = S_tot): Z_OUTER ≤ −2 on
  both footings. Bites iff both.
- **MU-0 (control).** No members (C ≡ 0, M_rem = 0) through the SCT-U runner gives B0 exactly (≤ 1e-12 relative, every bin, eRASS1 and
  ACCEPT, both footings).

## 7. Disclosure rules
- Any change after this commit is a dated, labelled amendment in its own file, stating whether it was made before or after a result.
  Failed or killed runs are kept with a suffix.
- Every load-bearing number comes from the committed `cfg962.py` and its outputs; margins are quoted from the JSON.
- Nothing in another lane, the LEDGER, any THEORY_CANONICAL file, sol61_push/ or campaign_fresh_gravity_astra/ is edited; CFG949, 953,
  954, 959 and the rest are read or exec'd read-only; CFG960 is not touched.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
