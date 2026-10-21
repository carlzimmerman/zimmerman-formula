# CFG954: clusters and mergers under the source-changing non-local theory (SCT). FROZEN CRITERIA

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-21.
Block CFG950–959 (LEDGER reservation row: "CFG954 SCT clusters and mergers (absorb member phantoms without merger memory; avoid
CFG951's inter-label sourcing failure)"). CFG953 (the SCT construction) runs in parallel; its directory did not exist when this
file was written. This lane therefore declares its own working SCT statement (§1), taken from CFG947's chassis and the owner's brief.
If CFG953's specification later differs on a point used here, a dated, labelled amendment states which result changes; nothing here
is edited.

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Kernel ν_s (CFG695; the
CFG726/916/951 cluster primary) for every SCT law; ν_mono only where a reproduced record result used it (CFG687's stored law in K3,
CFG599's Bullet progenitors, CFG947's T-X); ν_e for the Coma UDGs (CFG933/948's own kernel). "Cold energy" / cold dust throughout;
its mass is still required; no particle species. Framework-native inputs only: no ΛCDM halo, mass function, merger tree,
HMcode/BAHAMAS or standard-MOND yardstick enters any verdict. Not "theory closed". Nothing here says the data favour the framework.

**Machine limit (declared).** One process at a time, one core (OMP_NUM_THREADS=1), nice 10, an in-script RSS guard at 0.9 GB
(exit 3), a vm_stat guard (free+inactive < 8 GB ⇒ exit 75) and a start guard (< 10 GB ⇒ exit 75). Stages split (COMPUTE / K /
MUTATE / MAIN); work arrays go outside the repository (`../_external_data/cfg954_work/` relative to the repository root, not
committed). No download.

## 0. Status: POST HOC; every target was already seen

All targets (CFG687 eRASS1 318 and its T2 slope, CFG686 ACCEPT 8, CFG726 H-MM, CFG949 H-UT, CFG951's LDT numbers, CFG933/948 Coma
UDGs, CFG916's Bullet inputs) were measured and read before this lane. A pass would be an accommodation, not a prediction.

**Hand estimates made while writing (disclosed; from record numbers already published, no script of this lane):**
- **R1 (absorption) absorbs essentially every cluster member.** CFG916's members have median supply edges ≈ 1.0–1.1 Mpc against
  median pericentre King r_J ≈ 178 kpc. The host is then the law of all baryons with the forced edge, which is CFG951's reported
  "supply-capped law": A_MID ≈ 1.89 / 1.73, A_OUTER ≈ 0.95 / 0.86, s ≈ 0.42 / 0.44. Expectation: no merger memory, but the core
  excess (Z_MID ≈ +7) is untouched, and s sits ≈ 2.2 s_err below 0.896.
- **R1 also absorbs the Coma UDGs** (King r_J ~ 10 kpc against edges ~ 20 kpc, deep-regime estimate), so their own phantom is
  recomputed away. Expectation: a Newtonian or EFE prediction far below their observed above-law excess (CFG948's Newton reading is
  excluded at 5.45σ; CFG951's global-phantom bracket at 6.4σ).
- **R2 / R3 (persistence inside r_J)** are CFG951's X-OD bracket with gravitational instead of L2 domains, plus SCT's supply cap.
  Expectation: A_OUTER between X-OD's 0.81 / 0.75 and the capped law; A_MID ≈ 1.5–1.7 (core still in deficit).
- **The CFG949 combination.** The absorbed 𝒮 has zero net mass (zero-sum), so it cannot "become dust". An untethered-like core can
  arise in SCT only through the chassis clip (ρ_s = max(ρ_ph − ρ_c, 0)) when untethered cold dust is denser than the phantom. A
  rough estimate for a NGC 3198-mass galaxy under the same native collapse rule gives native dust ≈ 2–3× the phantom density at
  10 kpc. Expectation: the clip would also switch the law off in galaxy interiors, so the cluster/galaxy split is a CHOICE.
- **Expected overall: FAIL** (through the core, the UDGs or continuity). Stated before any number is computed.

## 1. The SCT working statement (zero new constants)

- **S1 chassis (CFG947 §2).** G_μν = 8πG(T^b + T^c + 𝒮)_μν. Baryons and cold dust are geodesic. The cold dust is untethered: no
  medium, no tether, no χ, no medium tidal tensor.
- **S2 own-domain source.** 𝒮 = Σ_q 𝒮_q. Each 𝒮_q is conserved (2-form current), retarded and sourced by domain q's OWN baryons only;
  nothing cross-sources (no 𝒮_p and no other domain's baryons enter q's law).
  - Static monopole content: inside q's edge the active cold-sector density a_q = ρ_c,q + ρ_s,q equals the ν_s law phantom of q's
    own baryons, with the chassis clip ρ_s,q = max(ρ_ph,q − ρ_c,q, 0) (CFG947 E6).
  - Zero-sum per domain, ∫ρ_s,q = 0 (CFG947 T-Z), forces the edge at the supply root, M_ph,q(<r_e) = S_q, with a_q = 0 beyond it
    (draw q = 1; CFG947 T-E). In cumulative form, A_q(<r) = min(T_law,q(<r), S_q).
- **S3 carried weights (CFG947 T-M).** Between events the 𝒮 weights are constant and carried by matter, so momentum is conserved
  identically. An event that recomputes 𝒮 is a relocation: it conserves momentum iff the 𝒮 dipole D_s and the 𝒮 momentum Ḋ_s = Σ_g Q_g V_g
  (sum over comoving groups g of net 𝒮 charge Q_g) are continuous across it.
- **S4 domains.** Labels are latched at collapse (CFG947 N1). A member's domain is bounded by its bound matter: the gravitational
  King r_J at pericentre (CFG916's solver; irreversible). SCT has no medium tidal tensor, so CFG945/951's L2 is not used. Own-domain
  satellites have no EFE and no hover (CFG947 f1/f2; CFG945).
- **S5 supplies and conservation.**
  - Cluster total S_tot = CFG652 `catchment(M*, M_gas,tot)` (rule "max") = 5.364 × max(M*/0.10, (M* + M_gas)/0.90).
  - Member supply S_i = 53.64 m_i (CFG726 `prog_halo`). When the P2 branch binds, Σ_i S_i = S_tot (checked per cluster, K-S).
  - The total active cold-sector mass of all domains in a cluster never exceeds S_tot. Stripped members' active mass joins the
    host's supply.
- **S6 harness (CFG726 / CFG916 / CFG951 C5, unchanged).**
  - Cluster baryons: CFG687 primary (β = 2/3, r_c = 0.15 R500, cut at 3 Mpc, stars f* = 0.20 co-distributed).
  - Members: N_mem = λ (CFG726's lambda.json), equal masses m_i = M*/N_mem, Hernquist R_e = 15 kpc, own ν_s phantom h(<s) cut at its
    own supply edge r_e,i and r_ta,i, co-distributed with the gas.
  - Orbits: CFG916's isotropic Gauss–Hermite × Gauss–Laguerre nodes at the isotropic-Jeans σ of the gas tracer in the host's current
    total. r_J is CFG916's King r_J.
  - Self-consistency: start from the plain law and iterate the host total (≤ 8 iterations, tol 1e-4 on max |ΔM/M|). Non-converged
    clusters are counted. If the last two iterations give different classes for an item, that item is UNDERDETERMINED.

**Cold-dust placement (SCT does not fix where the untethered dust sits; declared axis).**
- **P-S (primary): the halo is 𝒮-carried.** A member's cold dust inside r_J is negligible against its phantom, so the member group
  carries net 𝒮 charge Q_in = h(<r_J). This is the case in which 𝒮 does SCT's work.
- **P-I (declared bracket): dust-held halos.** A member's bound cold dust sits at its phantom inside its edge (𝒮 ≈ 0 there,
  Q_in = 0). Truncation keeps h(<r_J) as real dust, which the clip leaves Newtonian whatever the host's 𝒮 does.
- **N (reported reading, the CFG949 combination): native dust plus clip.** The cluster's cold dust is CFG949's B0 native debris
  (primary corner: S-cen supply, R930 C = 3000, r_ta boundary at z_i).

## 2. The three rules (declared now; no others)

Definitions per cluster and footing:
- T_law(X)(<r) = X(<r)[ν_s(G X(<r)/(r² a₀)) − 1].
- C_J(<r) = N_mem × the CFG916/951 member convolution of h(<s) with the node-weighted indicator s < r_J(r_p(d, node)). This is
  CFG951's `run_ldt` retention with rule "King".
- C_full: the same with no truncation.
- M*_abs(<r) and M*_str(<r): absorbed and stripped stars, placed at the members' positions (co-distributed with the gas) with
  node-averaged weights. Stripped stars use the Hernquist fraction beyond r_J, 1 − r_J²/(r_J + a)².
- Every min(·, S) is a cumulative cap, so the profile is flat beyond the edge.

**R1, absorption.**
- A member node is absorbed iff r_J(peri) < r_e,i (its domain is tidally truncated below its supply edge; r_e,i = the `prog_halo`
  edge, or r_ta,i if the supply is not reached).
- When absorbed, its stars join the host-domain baryons, its 𝒮_q is folded into the host's 𝒮 and its supply into the host's supply.
  The host's 𝒮 is recomputed (monopole about the host centre) from the host's TOTAL own-domain baryons.
- Unabsorbed members keep their whole 𝒮_q (C_un).
- Profiles:
  - R1 [P-S]: M = M_b + C_un + min(T_law(M_gas + M*_abs), S_tot − C_un,tot).
  - R1 [P-I]: M = M_b + C_J + min(T_law(M_gas + M*_abs), S_tot − C_J,tot). Absorbed members' bound dust stays (C_J includes
    unabsorbed members, for which h(<r_J) = h).

**R2, persistence with own-baryon sourcing only.**
- Members keep 𝒮_q inside r_J. The host's 𝒮 comes from the non-member baryons (the gas; in the harness every star is in a member).
  Nothing cross-sources.
- Profile: M = M_b + C_J + min(T_law(M_gas), S_tot − C_J,tot). This is the same under P-S and P-I.

**R3, hybrid: absorption at the tidal radius, persistence inside it.**
- Per member, the part of 𝒮_q beyond r_J, and the stars beyond r_J, are absorbed into the host. The host's 𝒮 is recomputed from the
  host-domain baryons (gas plus stripped stars) with the merged supply. The part inside r_J persists.
- Profile: M = M_b + C_J + min(T_law(M_gas + M*_str), S_tot − C_J,tot). The profile is the same under P-S and P-I; (f) differs.

**Reading N (reported; the "SCT for galaxies + CFG949 for clusters" test).** On RGRID:
- N-smooth: M = M_b + min(∫₀^r max(ρ_ph[T_law(M_b)], ρ_c,B0) dV, S_B0).
- N+members (graded reading): members' bound dust C_J^N (King r_J at pericentre in the N-smooth host, one pass) is taken out of the
  B0 supply (f_U = 1 − C_J,tot^N / S_B0, floored at 0):
  M = M_b + C_J^N + min(∫₀^r max(ρ_ph[T_law(M_b)], f_U ρ_c,B0) dV, S_B0 − C_J,tot^N).
- S_B0 = B0's total cold (1 − f_b)M_ta. The phantom is per footing; B0 itself has no a₀.

**Declared brackets** (each can move a class to CONDITIONAL): present-epoch r_J instead of pericentre (all rules); the uncut host
law (no forced edge, i.e. drop every min(·, S): the harness convention of CFG687/726/951) (all rules); P-I (R1 and R3).

## 3. Tests (both footings; ν_s)

### (a) eRASS1 merger memory (a1, OUTER 1.2–3 Mpc) and core (a2, MID 0.5–1.2 Mpc)
- **Scoring.** CFG687's per-cluster D/E and CFG951's `score_TR` (30-patch RA jackknife; A = ΣWD/ΣWP; Z = (A − 1)/σ).
- **(a1) per profile.**
  - CONSISTENT iff |Z_OUTER| < 2 on both footings.
  - INCONSISTENT iff |Z_OUTER| ≥ 2 on both footings.
  - CONDITIONAL otherwise, or if any declared bracket gives a different class.
- **(a2):** the same rule with Z_MID.
- Reported (no weight): the absorbed fraction f_abs, median r_J, C_J,tot/M*, C/M_b at 1 Mpc, iterations, and the cap's edge.

### (b) ACCEPT 8 OUTER (reported only)
CFG951's `score_TA` (CFG686 data, bootstrap 1000, seed 1); A and Z for OUTER and MID.

### (c) Outer mass slope
- CFG687 T2 (`score_TR`'s s: the OUTER amplitude against Mgas500 across terciles) vs the observed 0.896 ± 0.209.
- CONSISTENT iff |s − 0.896| < 2 × 0.209 on both footings; INCONSISTENT iff ≥ 3 × 0.209 on both; CONDITIONAL otherwise.
- The binning dependence (CFG688: NOT SETTLED) is disclosed with the result.

### (d) The Bullet (lensing peaks follow the galaxies)
- **Inputs (record only).** CFG599 `Progenitor599` main 1.5e15 / sub 1.5e14 (cool-core cloud), own ν_mono phantoms truncated at rt
  (the sub's edge here is its rt). Present separation 720 kpc. Sub core R_CORE = 200 kpc. CFG915's φ_lin,H. CFG916's King r_J(d)
  of the sub in the main.
- **Relocated core fraction φ(d_p) per rule.** Define φ_J = 1 − M_ph,sub(<min(r_J(d_p), 200))/M_ph,sub(<200).
  - R1 [P-S]: φ = 1 if r_J(d_p) < rt_sub (absorbed; the monopole recompute centres the sub's 𝒮 on the main), otherwise 0.
  - R1 [P-I], R2, R3: φ = φ_J. Bound 𝒮 or dust falls with the galaxies; stripped material joins the main and lags.
  - Reported, no weight, for R1 [P-S]: a non-spherical recompute that keeps the galaxies' own share,
    φ_share = 1 − ph[sub stars only](<200)/ph[all sub baryons](<200).
- **Rule (CFG916's B rule).** CONSISTENT iff φ ≤ φ_lin,H; INCONSISTENT iff φ ≥ 0.9; UNDERDETERMINED otherwise. The pericentre is not
  in the record, so the class is evaluated for every d_p ∈ (0, 720] kpc; if it changes across that range, (d) is UNDERDETERMINED (by
  input), and the thresholds are reported.

### (e) Continuity (merger toy)
- **Set-up (CFG951 (d)).** m₁ = 1e11 M⊙, m₂ = q m₁, q ∈ {1, 1/3, 1/10}, both Hernquist R_e = 15 kpc, z = 0, ν_s, each with its
  `prog_halo` phantom. Quasi-static radial approach d = 1000 → 0.5 kpc (Δ ln d = 0.005), then d = 0. dt = |Δd|/v_c(d) with
  v_c = √(G (M_law,1(<d) + M_law,2(<d))/d).
- **Domains.** r_J,2(d) = CFG916's King r_J of label 2 in label 1's own active profile (M_b,1 + h₁), latched as the running minimum.
  r_J(0) = 0.
- **Label 1's law** is the ν_s law of its own-domain baryons (monopole-enclosed), capped at its own supply. Label 2's content enters
  about centre 1 through CFG951's shell-overlap fraction.
- **Per rule.**
  - R1: label 2 is whole until r_J,2 < r_e,2. Then it is absorbed: its stars join label 1's source and its 𝒮 is recomputed.
    - [P-S]: label 2 keeps nothing.
    - [P-I]: label 2 keeps its dust h₂(<r_J,2), latched.
  - R2: label 2 keeps h₂(<r_J,2). Its stars never source label 1. The stripped active mass joins label 1's supply (outside the
    scored radii).
  - R3: as R2, but label 2's stars beyond r_J,2 join label 1's source.
- **Observables.**
  - About centre 1, R ∈ {20, 50, 100, 200} kpc: E₁ = M_v/M_GP − 1, with M_GP the label-free law of the monopole-enclosed baryons
    (CFG951's).
  - About centre 2, R ∈ {5, 10, 20} kpc: the label-induced change of the secondary's interior,
    E₂ = [M₂,v(<R) − M₂,grav(<R)]/M₂,own(<R). Here M₂,grav = M_b,2(<R) + h₂(<min(R, r_J,2)) is what gravitational truncation alone
    leaves, and M₂,own = M_b,2 + h₂. E₂ ≡ 0 when label 2 keeps its bound phantom or dust.
- **Metric (CFG951's frozen metric).** J = the maximum over observables and over every window of one dynamical time of |ΔE|. The
  dynamical time is R/v_c,rem(R) about centre 1 and R/v_c,2(R) of label 2's own law about centre 2. An instantaneous jump counts in
  full.
- **Rule.** PASS (CONSISTENT) iff J ≤ 0.05 for every q on both footings (primary placement); FAIL (INCONSISTENT) otherwise.
  - The R1 [P-I] row is graded the same way.
  - Reported: the global-recompute bracket's E₂, i.e. the EFE factor of label 2's law in label 1's baryonic field at d.

### (f) Momentum (and mass) of the absorption step
- **T-M identity (S3).** At an event, ΔP_s = Δ(Σ_g Q_g V_g) and ΔD_s = Δ(Σ_g Q_g X_g). The event conserves momentum iff both vanish.
- **Per rule.**
  - **R1 (primary monopole recompute) at its trigger.** The whole member domain is still comoving with zero net charge, and the
    recompute is spherical with zero net charge, so ΔP_s = ΔD_s = 0 identically. This is verified on the discretised member.
    - Bracket (reported, can move the class to CONDITIONAL): a non-spherical "global" recompute keeps a local phantom
      Q_m = [g_law(g_h + g_N,m(r_J)) − g_law(g_h) − g_N,m(r_J)] r_J²/G around the moving member (1-D QUMOND on-axis, CFG947 T-X
      form; g_h = the host's baryonic field at d) while the draw is host-centred. Then ΔP_s/P_m = Q_m/m.
  - **R2.** No event, constant carried weights: ΔP_s = 0 identically.
  - **R3.** The stripped shells are moved into the host's static spherical 𝒮 while the member keeps Q_in. Cumulative
    ΔP_s/P_m = Q_in/(m + M_c,in): P-S gives C_J,tot/M*_bound; P-I gives 0.
- **Quantities.** Computed on the eRASS1 harness (per cluster, medians reported) and for the toy's secondary at its event.
- **Rule.** CONSISTENT iff |ΔP_s|/P_member ≤ 0.01 on both footings (eRASS1 median and every toy case); INCONSISTENT iff > 0.01 on
  both; CONDITIONAL otherwise or if the declared bracket differs.
- **Mass.** The zero-sum and supply bookkeeping (total active ≤ S_tot; the merged supply equals the sum) is checked per cluster to
  ≤ 1e-9 relative and reported.

### (g) Coma UDGs (the 9 admitted, CFG933/948)
- **Inputs.** ⟨E_obs⟩, se, σ_sys and E_ceil = +0.0176 ln from `cfg948_results.json`. The table (L, M/L, R_e, distances) from
  `real_research/data/freundlich2022_coma_udgs.tsv`. The Coma β-model total field and density (L23; CFG948/951).
- **Absorption test (R1).**
  - Each UDG's King r_J at its 3D distance dmean (primary) and dproj (bracket) in the β-model host, with γ = d ln M_host/d ln D. It
    is solved self-consistently with the UDG's own ν_e-law mass (Plummer).
  - The UDG's edge is the supply root of its own phantom with S = 53.64 M*: r_e = r_M/ln(1 + 1/53.64) for ν_e (CFG947 T-E), capped
    at the UDG's own r_ta.
  - The UDG is absorbed iff r_J < r_e.
- **Predictions E (ln g_obs/g_law at r½ = (4/3)R_e).** g_loc = (4π/3) G ρ_host r12 is the host's local density, Newtonian.
  - R1 [P-S] absorbed: E = ln[(g_N + g_loc)/g_law(g_N)] (own phantom recomputed away). Not absorbed: as R2.
  - R1 [P-I], R2, R3: if r_J ≥ r12, E = E_ceil + ln[(g_law(g_N) + g_loc)/g_law(g_N)]; if r_J < r12, the phantom beyond r_J is lost
    (CFG951's E_partial form).
  - Reported: the global-phantom bracket E_ceil + efe (CFG951's M1-inf).
- **z** = (⟨E_obs⟩ − ⟨E_pred⟩)/√(se² + σ_sys²) (CFG948's formula).
- **Class.** INCONSISTENT iff z ≥ 3 on both footings. Otherwise NOT DIAGNOSTIC (CFG948's power failure is inherited: the sample
  cannot certify consistency).
- **Also stated:** whether absorption removes the UDGs' phantom, and whether that is consistent with their above-law excess.

### The CFG949 combination and the selector (reported, with a frozen consequence)
- Reading N is graded on (a1), (a2) and (c) (eRASS1 only; CFG949's B0 has no ACCEPT grade).
- **Selector test.** Under the same native rule (CFG949's R930 copy: f_ret census, C = 3000, r_ta boundary, z = 0), compute
  ρ_c,native/ρ_ph(ν_s, point-mass baryons) at r = 2, 5, 10, 20, 30, 50 kpc for M_b = 1e9, 1e10, 4.72e10 (NGC 3198), 1e11 M⊙. For the
  eRASS1 clusters, compute the fraction of the MID band where ρ_c,B0 > ρ_ph.
- **The clip is a DERIVED cluster/galaxy selector iff** (i) ρ_c,native < ρ_ph at every r ∈ [2, 30] kpc for every galaxy mass and
  both footings, and (ii) ρ_c,B0 > ρ_ph over the whole MID band for the median eRASS1 cluster. Otherwise the split is a **CHOICE**.
- Only if DERIVED does reading N enter the overall, as an R1 row with N's (a1), (a2), (c) and R1 [P-I]'s (d)–(g).

### Classes
- **Per row** (R1 [P-S], R1 [P-I], R2, R3 [P-S], R3 [P-I]):
  - INCONSISTENT if any of (a1), (a2), (c), (e), (f), (g) is INCONSISTENT, or if (d) is INCONSISTENT for every d_p.
  - CONSISTENT iff (a1), (a2), (c), (d), (e), (f) are CONSISTENT and (g) is not INCONSISTENT.
  - CONDITIONAL otherwise.
- **Per rule:** the common class of its rows if they agree, otherwise CONDITIONAL (SCT does not fix the dust placement).
- **Overall.** **SCT CLUSTERS OK** iff at least one rule is CONSISTENT; **CONDITIONAL** iff the best rule is CONDITIONAL; **FAIL**
  iff every rule is INCONSISTENT.

## 4. Controls

**K tests (each must pass, or the item it guards is VOID).**
- **K1 CFG951 persistence failure.**
  - CFG951's stored work arrays for its persistence variant (M3: L2, pericentre, C2) and its X-OD bracket (M3_OD), scored with the
    copied code, reproduce `cfg951_results.json` T_R / T_A: M3 eRASS1 A_OUTER 0.556 ± 0.048 / 0.496 ± 0.043, Z −9.32 / −11.86;
    ACCEPT 0.616 / 0.557. Tolerance ≤ 1e-12.
  - CFG951's `run_ldt` (copied) recomputes M3 for the first 6 eRASS1 clusters and all 8 ACCEPT clusters, both footings, equal to the
    stored arrays to ≤ 1e-10 relative.
- **K2 CFG726 H-MM.** CFG726's stored arrays scored = `cfg726_results.json` T_R / T_A primary (≤ 1e-12). This lane's recomputed H-MM
  arrays = stored (≤ 1e-10 relative).
- **K3 CFG687.**
  - The stored PL (ν_mono canonical) gives A_MID / A_OUTER 1.9102 ± 0.1186 / 1.0118 ± 0.0869 (≤ 1e-9); the alt law recomputed
    reproduces its stored A (≤ 1e-6).
  - This lane's ν_s law arrays equal CFG726's stored law arrays (≤ 1e-10).
- **K4 CFG949 primary corner.** The B0 recompute (CFG951's copy of CFG949's recipe) gives A_MID 1.0109 ± 0.0632, A_OUTER
  1.0469 ± 0.0888 and s 0.6615 (≤ 1e-9).
- **K5 CFG916 King r_J.** The Bullet sub at 720 kpc (303.76 / 305.94 kpc) and its grid (≤ 1e-9); the eRASS1 pericentre median
  178.046 / 178.704 kpc (≤ 1e-6).
- **K6 CFG948.** z_up 1.6334 / 1.4350 from the stored components (≤ 1e-9); β-model g_host(1 Mpc) = 8.806e-11 (≤ 1e-3 relative).
- **K-W.** The matrix convolution equals CFG726's `convolve_members` and CFG916's `convolve_members_w` (≤ 1e-10).
- **K-S.** The supply identity Σ_i S_i = S_tot holds (≤ 1e-12 relative) wherever the P2 branch binds. Every cluster where it does
  not is counted and reported.

**MUTATE (separate `_MUTATE` outputs; exit 0 iff every tooth bites and every control holds).**
- **MU-NA, "never absorb."** Members keep their whole 𝒮_q (no tidal truncation, no absorption), with own-baryon sourcing. It must
  reproduce merger memory:
  - (i) the shared-target form M_b + max(C_full, T_law(M_b)) reproduces CFG726's T-R / T-A primary A (≤ 1e-10) and fails eRASS1
    OUTER (Z ≤ −2, both footings);
  - (ii) SCT's own never-absorb form M_b + C_full + min(T_law(M_gas), max(S_tot − C_full,tot, 0)) also fails eRASS1 OUTER
    (Z ≤ −2, both footings).
  - Bites iff both hold.
- **MU-GS, "a global source."** It must reproduce the EFE:
  - (i) CFG947's `efe_global_dex` on HOSTS882 × {50, 100, 250} kpc × {simple, mono} × footings reproduces the 36 stored T-X values
    (≤ 1e-12), with |EFE| > log₁₀ 1.01 somewhere;
  - (ii) the Coma UDGs under a global source reproduce CFG951's M1-inf prediction and z (≤ 1e-9), with z ≥ 3 on both footings.
  - Bites iff both hold.
- **MU-0 (control).** C ≡ 0 with no cap gives the plain law exactly (≤ 1e-12 relative, every bin, eRASS1 and ACCEPT, both
  footings).

## 5. Disclosure rules
- Any change after this commit is a dated, labelled amendment in its own file, stating whether it was made before or after a result.
  Failed or killed runs are kept with a suffix. Smoke runs write only outside the repository.
- Every load-bearing number comes from the committed `cfg954.py` and its JSON outputs. Margins are quoted from the JSON.
- Nothing in another lane, the LEDGER, any THEORY_CANONICAL file, sol61_push/ or campaign_fresh_gravity_astra/ is edited. CFG953's
  directory is read only, if it appears.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
