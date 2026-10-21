# CFG951: mergers and clusters under the labelled-domain theory (LDT). FROZEN CRITERIA

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-20.
Block CFG950–959 (LEDGER reservation row: "CFG951 mergers and clusters under LDT"). CFG950 (the formal LDT specification) runs in
parallel; its directory did not exist when this file was frozen. This lane therefore declares its own working LDT statement (§1),
taken from CFG945 (H1, per-label tether, L2 re-latch) and CFG947 (labelled domains, merge rule M-R, own-domain phantom). If CFG950's
specification later differs on a point used here, a dated, labelled amendment states which result changes; nothing here is edited.

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Kernel ν_s (CFG695;
CFG726/CFG916 primary) for the cluster law and the member halos; ν_mono only where a reproduced record result used it (CFG687's
stored law in K2; CFG597/599's Bullet progenitors; CFG947's T-X). "Cold energy" throughout; its mass is still required; no particle
species. Framework-native inputs only: no ΛCDM halo, mass function, merger tree, HMcode/BAHAMAS or standard-MOND yardstick enters any
verdict. Not "theory closed". Nothing here says the data favour the framework.

**Machine limit (declared).** A 1024³ job shares the machine. One process at a time, one core (OMP_NUM_THREADS=1), nice 10, an
in-script RSS guard at 0.9 GB (exit 3) and a vm_stat guard (free+inactive < 8 GB ⇒ exit 75). Stages are split (K / MUTATE / MAIN);
work arrays go to `../_external_data/cfg951_work/` (not committed). No download.

## 0. Status: POST HOC; every target was already seen

All targets (CFG687 eRASS1 318, CFG686 ACCEPT 8, CFG726 H-MM, CFG916 LR-c, CFG949 H-UT, CFG933/CFG948 Coma UDGs, CFG916's Bullet
inputs) were measured and read before this lane. A pass would be an accommodation, not a prediction.

**Hand estimate made while writing (disclosed, from the deep-regime formula only, no script).** Members retained inside tidal
domains of ~150–250 kpc each hold ~10–15× their stars in medium, so a co-distributed member population carries C/M_b ~ 1–2. If C is a
Newtonian source for the host label's law (§1 C2), the outer lensing mass rises by ≈ √(1 + C/M_b) ≈ 1.4–1.7, i.e. A_OUTER ≈ 0.6–0.7
(an overshoot of H-MM's kind), while MID/OUTER changes little. This expectation is stated before any number is computed.

## 1. The LDT working statement (zero new constants)

**LDT core (common to every variant).**
- **C1 labels.** Every collapsed object carries one label q. Its medium n_q is tethered to its own potential χ_q only:
  S ⊃ −s(θ) Σ_q W_full(|Dχ_q|) + Σ_q λ_q(D²χ_q − K m n_q) (CFG945 H1, its collapse gate s(θ) included).
- **C2 label equilibrium (primary coupling, "X-H1").** Static, in the label's free-fall frame: R(u_q) = |g_N + Σ_{p≠q} g_p + g_free|
  (CFG945 [H1_two_label_equilibrium] and (e); CFG941 R2). Every mass that is not in label q (all baryons, other labels' media, free
  cold matter) is a Newtonian source of label q's law; uniform external fields cancel (no EFE); a single label is the law exactly.
  Monopole form about the label's centre: M_tot(<r) = S(<r) ν(G S(<r)/(r² a₀)), with S = everything except label q's own medium.
  - **Bracket X-OD (CFG947 own-domain phantom).** Label q's phantom is the law of its own-domain baryons only, and other labels'
    media are not sources: M = M_b + Σ_p C_p + T_law(host-domain baryons).
- **C3 L2 re-latch (CFG945; "L2 required" there).** A medium element takes the label whose medium tidal tensor
  |τ_q| = (√6/3)|u_q′ − u_q/r| dominates at its position, with u_q = G M_med,q(<r)/r² from each label's own medium. For a member at
  host-centric distance d, its domain is r_dom(d) = the outermost s with |τ_m(s)| ≥ |τ_h(d)| (CFG945's implementation; here capped
  only at the member's own r_ta). Re-latching is irreversible, so the retained domain is the one at pericentre (primary) or at the
  present position (bracket).
- **C4 static relaxation (as CFG916 LR-c).** Re-latched medium joins the host label; the host medium settles to its C2 target by
  t_obs (transport-unlimited); any excess over the target is expelled beyond the scored radii.
- **C5 harness conventions (CFG726 / CFG916, unchanged).** Cluster baryons: CFG687 primary (β = 2/3, r_c = 0.15 R500, cut at 3 Mpc,
  stars f* = 0.20 co-distributed). Members: N_mem = redMaPPer λ (CFG688 match) or CFG726's λ(M_gas(<1 Mpc)) relation; equal masses
  m_i = M*/N_mem; Hernquist R_e = 15 kpc; each with its own ν_s law phantom cut at its own supply edge (53.64 m_i) and its own r_ta
  (CFG726 `prog_halo`); positions co-distributed with the gas. Orbits: CFG916's isotropic Gaussian velocities at the isotropic-Jeans
  σ of the gas tracer in the host's total potential, pericentre by CFG916's solver. Host law uncut (the harness convention of
  CFG687/726/916).
- **Self-consistency.** τ_h and the orbit potential use the host's current total. Start from the plain law, recompute with the C2
  host, iterate (≤ 8 iterations) until max |ΔM_tot/M_tot| over the grid ≤ 1e-4 per cluster. Non-converged clusters are counted and
  reported; if the last two iterations give different classes, the item is UNDERDETERMINED.
- **Coalescence trigger T_c (used by M1/M2).** A secondary is coalesced when its domain shrinks inside its baryonic half-mass radius
  (r_dom ≤ r_½,b; for the member Hernquist r_½,b = (1 + √2) a with a = R_e/1.8153, computed in code), i.e. fewer than half its
  baryons remain inside its own domain: CFG947 M-R's "bound fraction < ½" written with L2.

## 2. Merge-rule variants (three; declared now)

- **M1, instant relabel.** At T_c the secondary's whole remaining label becomes the primary's at once; the primary's medium settles
  to the C2 target of the merged baryons (plus any other remaining labels).
- **M2, blend over one dynamical time.** From T_c the secondary's label fraction falls linearly to 0 over t_dyn = r/v_c(r) of the
  remnant (r = the remnant's baryonic half-mass radius). During the blend the remnant is flagged unsettled and is not graded on the
  law, so the two-label non-additivity (√f + √(1 − f), CFG947; R(u₁) = g_N + u₂, CFG945) never acts on a settled galaxy. For static
  cluster scoring (t_obs − t_c ≫ t_dyn, declared), M2 ≡ M1.
- **M3, labels persist until tidal disruption.** No merge rule beyond C3: the secondary keeps the medium inside r_dom until r_dom → 0.
- **Bracket M1-inf (reported, no class weight).** Trigger at infall (entry inside the host's r_ta) instead of T_c: members and
  satellites lose their labels at infall, which is the global phantom (the MU-GP arm).

Progenitor groups that coalesced into a cluster carry no memory in any variant (M1 at once, M2 after t_dyn, M3 at disruption; argued,
not computed: the harness has no progenitor-group inventory). What is computed is member memory: the surviving members' retained
media and their effect on the host.

## 3. Tests per variant (both footings, ν_s)

### (a) Merger memory (clusters)
- **Profile.** M_v(<r) = (M_b + C_v)(<r) ν(G (M_b + C_v)(<r)/(r² a₀)). C_v = N_mem × the CFG726 member convolution of h_i(<s) with a
  per-position retention weight w_v(d, s): the node-weighted indicator s < r_dom(r_p(d, node)) (M3); for M1/M2 additionally
  multiplied by [r_dom ≥ r_½,b].
- **Scoring.** CFG726/CFG916's T-R (eRASS1 318, CFG687 per-cluster D/E, 30-patch RA jackknife) and T-A (ACCEPT 8, CFG686 data,
  bootstrap 1000, seed 1); A = ΣWD/ΣWP; Z = (A − 1)/σ.
- **Class (a) per variant.**
  - CONSISTENT iff |Z_OUTER| < 2 on eRASS1 AND ACCEPT on both footings.
  - INCONSISTENT iff, on both footings, Z_OUTER ≤ −2 (overshoot = memory) on eRASS1 or ACCEPT, or Z_OUTER ≥ +2 on eRASS1.
  - CONDITIONAL otherwise, or if any declared bracket gives a different class from the primary.
- **Declared brackets (can move the class to CONDITIONAL):** present epoch instead of pericentre; CFG916's King r_J instead of L2;
  ICM-sourced member halos (each member's medium = the ν_s law phantom of its stars plus the local gas monopole (4π/3)s³ρ_gas(d),
  cut at its own supply edge; L2 recomputed with it); the X-OD coupling.
- **Reported only (no class weight):** a supply-capped bracket (total cold medium ≤ 5.364 × catchment, CFG652 `catchment`), applied
  to the law and to every variant; the fraction of members coalesced; median r_dom; C/M_b at 1 Mpc; iterations used.

### (b) Cluster core
- **Reading T (LDT as declared).** One tethered host label with nested member labels and C2 sourcing: A_MID (0.5–1.2 Mpc) from (a)'s
  profile.
- **Reading U (CFG949 H-UT).** Untethered host: CFG949's B0 primary corner (R930 C3000 r_ta, S-cen; baryons + native NFW, Newtonian).
  Members keep their labels; with no host label L2 is undefined, so they are truncated at CFG916's King r_J at pericentre
  (gravitational tides), and their retained media are taken out of the H-UT supply (conservation). Bracket: members at full halos.
- **Which reading LDT implies (argued and fixed now).** LDT seeds a label at every collapse and gates its tether on where the medium
  is settled (θ = 0). A relaxed cluster's medium is settled, so it is tethered: **reading T**. Reading U needs an untethered-cluster
  selector that LDT does not contain (CFG939: S4 not derivable). U is reported as "LDT + selector" and cannot by itself give LDT a
  pass.
- **Class (b) per variant (reading T).** CONSISTENT iff |Z_MID| < 2 on eRASS1 on both footings; INCONSISTENT iff |Z_MID| ≥ 2 on both;
  CONDITIONAL otherwise or if a declared bracket of (a) changes the class. ACCEPT MID reported.

### (c) The Bullet
- **Inputs (record only).** CFG599 `Progenitor599` main 1.5e15 / sub 1.5e14 (cool-core cloud) per footing (their own ν_mono phantoms,
  truncated at r_t); present separation 720 kpc; sub core R_CORE = 200 kpc (CFG916); CFG915's φ_lin,H; the head-on model's minimum
  separation from CFG623's α = 0 run (report only, as CFG916 PH4).
- **Computed.** The sub's L2 domain r_dom(d) on d ∈ [5, 720] kpc, with |τ| from each progenitor's own medium (M_ph).
  - M3: the re-latched core fraction is φ_rel(d_p) = 1 − M_ph,sub(<min(r_dom, 200))/M_ph,sub(<200).
  - M1: φ_rel = 1 if r_dom(d_p) ≤ r_½,b(sub), otherwise as M3.
  - M2: as M3 below the trigger; above it, φ_rel lies between M3's value and 1, set by (t_obs − t_p)/t_dyn, which is not in the
    record (bracket [M3, M1]).
- **Physical reading (declared).** Re-latched medium is main-labelled and is pulled toward the main's equilibrium, so it lags the
  sub's galaxies. Retained medium is tethered to χ_sub and falls freely with the galaxies.
- **Rule (CFG916's B rule).** CONSISTENT iff φ_rel ≤ φ_lin,H; INCONSISTENT iff φ_rel ≥ 0.9; UNDERDETERMINED otherwise.
  - The pericentre d_p is not in the record, so the class is evaluated for every d_p ∈ (0, 720] kpc. If it differs across that
    range, (c) is UNDERDETERMINED (by input), and the thresholds d*(φ_lin,H), d*(0.9) and d*(T_c) are reported.
  - The present-position (d = 720 kpc) value is reported.

### (d) Continuity (merger toy)
- **Set-up.** Two Hernquist objects, m₁ = 1e11 M⊙ and m₂ = q m₁ with q ∈ {1, 1/3, 1/10}, both R_e = 15 kpc, z = 0, ν_s, both
  footings, each with its isolated law medium cut at its supply edge (CFG726 `prog_halo`).
- **Approach.** Quasi-static radial approach d = 1000 → 0.5 kpc (Δ ln d = 0.005), then d = 0. Time along it: dt = |Δd|/v_c(d) with
  v_c(d) = √(G M_GP(<d)/d) about centre 1 (declared infall speed).
- **Domains.** Label 2's domain is r_dom(d) (C3), with τ₁ from label 1's C2 medium (iterated) and τ₂ from label 2's own medium.
- **Observables.** M_tot(<R) about centre 1 for R ∈ {20, 50, 100, 200} kpc, in C2's monopole form; label 2's baryons and retained
  medium are enclosed via the shell-overlap fraction.
  - Reference GP: the label-free law of the monopole-enclosed baryons.
  - Label-induced part: E_v(t; R) = M_v/M_GP − 1.
- **Metric.** J_v = the maximum, over R and over every window of one remnant dynamical time t_dyn(R) = R/v_c,rem(R), of |ΔE_v|
  (an instantaneous jump counts in full).
- **Rule.** PASS (CONSISTENT) iff J_v ≤ 0.05 for every q on both footings; FAIL (INCONSISTENT) otherwise.

### (e) Satellites accreted onto clusters (the 9 admitted Coma UDGs of CFG933/CFG948)
- **Inputs.** ⟨E_obs⟩, se, σ_sys and E_ceil = +0.0176 ln from `cfg948_results.json` (read only). The table (L, M/L, R_e, distances)
  from `real_research/data/freundlich2022_coma_udgs.tsv`. The Coma total field and density from the L23 β-model used by CFG948
  (hydrostatic total: an upper bound on all host matter).
- **(i) Label retention.** Each UDG's L2 domain at its 3D distance dmean (primary) and at dproj (bracket; smaller, so harsher), with
  τ_h from the β-model total field (an upper bound on the host medium's τ).
  - Medium inside r12 = (4/3)R_e is lost if r_dom < r12 (M3).
  - The whole label is lost if r_dom ≤ r_½,b (M1/M2), which pushes that UDG to Newton.
- **(ii) Inter-label sourcing (C2).** The UDG's law is the law of its baryons plus the monopole of all other mass inside r12:
  M_loc = (4π/3) r12³ ρ_host(D).
  - ΔE = ln[g_law(g_N + g_loc)/g_law(g_N)] at r12, with g_N = G(M*/2)/r12² and M* = L × M/L.
  - LDT ceiling = E_ceil + ⟨ΔE⟩ (an upper bound).
  - z_LDT = (⟨E_obs⟩ − ⟨E_pred⟩)/√(se² + σ_sys²) (CFG948's formula). ⟨E_pred⟩ is the LDT ceiling, with relabelled UDGs at their
    Newtonian E_N = −ln ν_e(g_N/a₀).
- **Class (e) per variant.** INCONSISTENT iff z_LDT ≥ 3 (with systematics) on both footings. Otherwise NOT DIAGNOSTIC (CFG948's power
  failure is inherited: the sample cannot certify consistency). Reported: "LDT raises the ceiling by ⟨ΔE⟩", and the M1-inf bracket's
  global-phantom EFE in Coma.

### Classes
- **Per variant.**
  - INCONSISTENT if any of (a), (b), (d), (e) is INCONSISTENT, or if (c) is INCONSISTENT for every d_p.
  - CONSISTENT iff (a), (b), (c), (d) are CONSISTENT and (e) is not INCONSISTENT.
  - CONDITIONAL otherwise.
- **Overall.**
  - **LDT MERGERS OK** iff at least one variant is CONSISTENT.
  - **CONDITIONAL** iff the best variant is CONDITIONAL.
  - **FAIL** iff every variant is INCONSISTENT.
- The "LDT + untethered-cluster selector" reading (U) is graded the same way with (a) and (b) from U, and reported. It does not
  enter the overall, because LDT does not contain the selector.

## 4. Controls

**K tests (each must pass, or the item it guards is VOID).**
- **K1 CFG726 H-MM.**
  - (i) CFG726's stored per-cluster arrays, scored with the copied score code, reproduce `cfg726_results.json` T_R and T_A primary
    (ν_s, both footings: A and σ for MID / OUTER, and Z) to ≤ 1e-12.
  - (ii) The H-MM arrays recomputed with the copied cluster code equal the stored arrays to ≤ 1e-10 relative.
- **K2 CFG687.**
  - (i) The stored PL (ν_mono canonical) gives A_MID / A_OUTER 1.91 ± 0.12 / 1.01 ± 0.09, equal to `cfg687_results.json` to ≤ 1e-9.
    The alt law recomputed reproduces its stored A to ≤ 1e-6.
  - (ii) The ν_s law arrays recomputed here equal CFG726's stored law arrays to ≤ 1e-10. ν_s A_MID is 1.9068 / 1.7510 to ≤ 1e-4.
- **K3 CFG949 primary corner.** The recomputed B0 primary (copied R930 code, and CFG949's exec recipe for the CFG686 / CFG922 engines;
  CFG949's own script is never executed) reproduces A_MID 1.011 ± 0.063, A_OUTER 1.047 ± 0.089 and s 0.6615 of
  `cfg949_results.json` to ≤ 1e-9.
- **K4 CFG945 L2.** This lane's L2 radius function reproduces CFG945's 18 stored r_dom (H1 (b), HOSTS882 × 50/100/250 kpc, both
  footings) to ≤ 1e-6 relative.
- **K5 CFG916.** King r_J of the Bullet sub at 720 kpc, and its r_J grid, equal `cfg916_cache.json` to ≤ 1e-9. The eRASS1 King
  pericentre median r_J (178.05 / 178.70 kpc) is reproduced to ≤ 1e-6 relative.
- **K6 CFG948.** z_up 1.633 / 1.433 recomputed from its stored components to ≤ 1e-9. The β-model g_host(1 Mpc) = 8.806e-11 to ≤ 1e-3
  relative.

**MUTATE (separate `_MUTATE` outputs; exit 0 iff every tooth bites and every control holds).**
- **MU-NM, "labels never merge"** (members keep whole halos: no L2 truncation, no merge).
  - Under the shared-target convention this is H-MM exactly. It must reproduce CFG726's T-R / T-A primary A to ≤ 1e-10 and fail
    OUTER (Z ≤ −2 on eRASS1 and ACCEPT, both footings).
  - Under C2 (LDT-native never-merge) it must also fail OUTER.
  - Bites iff both hold: merger memory is reproduced.
- **MU-GP, "the global phantom."**
  - (i) CFG947's `efe_global_dex` on HOSTS882 × {50, 100, 250} kpc × {simple, mono} × footings reproduces `cfg947_results.json`
    T-X (all 36 values to ≤ 1e-12), with |EFE| > log₁₀ 1.01 somewhere: the class-A EFE is present.
  - (ii) For clusters, the global phantom (no member labels) equals the plain ν_s law to ≤ 1e-12.
  - Bites iff both hold.
- **MU-0 (control).** C ≡ 0 in the C2 formula gives the plain law exactly (≤ 1e-12 relative, every bin).

## 5. Disclosure rules
- Any change after this commit is a dated, labelled amendment in its own file, stating whether it was made before or after a result.
  Failed or killed runs are kept with a suffix.
- Every load-bearing number comes from the committed `cfg951.py` and its JSON outputs. Margins are quoted from the JSON.
- Nothing in another lane, the LEDGER, any THEORY_CANONICAL file, sol61_push/ or campaign_fresh_gravity_astra/ is edited.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
