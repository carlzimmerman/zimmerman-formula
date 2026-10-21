# CFG932 FROZEN CRITERIA: energy bookkeeping of cold-energy settling (theory spine for H-ELS)

Date: 2026-10-20. Block CFG930–939 (ledger row "CFG930–939 RESERVED", CFG932 = energy bookkeeping of settling). This file is
committed ALONE, before any CFG932 script exists and before any CFG932 number (energy, ratio, window) has been computed. It is
never edited; post-hoc changes go into dated, labelled amendments in the README.

Settings: κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻², never pooled: every number is computed
and classed per footing. "Cold energy" throughout; its mass is required; no particle species. Not "theory closed". Nothing here
may say the data favour the framework. Framework-native inputs only: no ΛCDM simulation fit (no concentration–mass relation, no
abundance matching, no HMcode/halo-model mass function) enters any number that carries a class.

## 0. Disclosure: what was seen before this file was written

- **H-ELS is POST-HOC.** The hypothesis (settling is energy-limited; baryonic feedback pays for unbinding a primordial central
  surplus; energy-starved systems keep it) was formed by the orchestrator after the record's results were seen: CFG42 (NFW debris
  closes UFDs, over-predicts classicals), CFG541/542/544/638 (energy is not conserved by the drift; dark-energy partner), CFG747/
  CFG776 (tethered surplus is expelled by the cubic push), CFG822–CFG928 (the dwarf / early-type / cluster-core excess family and
  the failed mechanisms), CFG650/CFG654 (shear pass, native inputs).
- **Record text read before freezing (read only):** CFG638 README + script; CFG541 EQUATIONS.md (§5: dE_N/dt = ∫ρ_c v_s·∇Φ dV;
  E_sink table; sink options), cfg541.py `Model` (phantom = M_b/expm1(√y); r_analytic); CFG542 README (Pb: Q = ρ_c α τ_ff
  1_B 1_C ∇ψ·∇Φ; K2 energy closes only with the dark-energy partner); CFG544 README (FIX-1 two-sided deficit ψ = Φ_law − Φ; under
  the drift dE/dt is indefinite, positive when overfill is pushed out; overfill NOT HANDLED); CFG747/CFG776 READMEs; CFG889/CFG882
  ledger rows; CFG650 README + FROZEN_CRITERIA + the engine's source routine (Read tool: `forces()` source block, `expel_m3`,
  `_finish_phik`); CFG654 README and its native tables; CFG416 `fret_of`; CFG42 README; the record memory notes; MASTER_COLD_ENERGY_
  EQUATIONS.md (another agent's file, energy sections, read only).
- **Numbers seen before freezing (disclosed):** a scratch prototype (not kept, not in the repo) evaluated the native σ(M) (σ8 0.825
  from the native table) and the concentration rules of §3.2 for six masses (6e5–1.5e15 M☉): c_ta = r_ta/r_s ≈ 45–72 (6e5),
  18–38 (2.6e10), 8–26 (3.8e12), 4–14 (1.5e15) across the rules. No energy, ratio, crossing radius or window was computed.
  Hand estimates (in my head, before this file) suggested: (i) at the central rule a MW-like NFW is not above the law's phantom at
  2 and 10 kpc; (ii) with the record's dwarf supply (M_ta = 64 M_b) a UFD's NFW is far below its own deep-MOND phantom at r_h, and
  even ×100 that supply stays below it for a compact UFD while exceeding it at Boötes-I-like radii; (iii) a cluster NFW exceeds
  the law by ~×1.3 in total mass inside 0.5 Mpc. These estimates are disclosed because they inform what the bracket must cover.

## 1. Questions and classes

- **Q1 (energy accounting of CFG638).** Derive the total-energy equation (cold-energy kinetic + Π + self-gravitating potential +
  baryons) implied by CFG638's kinetic system (CFG541 E3 drift v_s = −α 1_B 1_C τ∇ψ, CFG544 FIX-2 OU relaxation at α/τ to σ_J²,
  ∇²Φ = 4πG(ρ_b + ρ_c), G9), for the one-sided (CFG541 E5), two-sided (CFG544 FIX-1) and gated (CFG639) deficit. Check it on a
  1-D spherical drift-only test (§4).
  **Class rule:** NON-CONSERVING if the derived matter-sector energy equation carries a source term that is not a divergence and
  the 1-D test shows |ΔE_matter|/|W_0| ≥ 1e-3 while the derived identity ΔW = ∫P_drift dt holds to ≤ 2% (relative); the source
  term is then named. CONSERVING if the source vanishes identically. UNDETERMINED if the identity check fails (> 2%) or the test is
  inconclusive. The CFG747 tether dynamics (canonical v2 S2) is reported separately as a reading (its own K2 is on record), not
  part of the Q1 class.
- **Q2 (cost of reaching the law), per system and corner:** ΔE = E(settled law profile + baryons) − E(primordial cusp + baryons)
  inside the declared region (§3.4) = E_bind(primordial) − E_bind(settled). Positive = energy must be supplied. Reported, no class.
- **Q3 (who can pay).** ε_req,i = ΔE_i / E_avail,i (ΔE_i ≤ 0 → ε_req,i = 0; R_i(ε) = ε E_avail,i/ΔE_i). Window for one universal ε:
  W = [ε_lo, ε_hi) with ε_lo = max over rotators of ε_req, ε_hi = min(1, min over the starved set of ε_req); W is NON-EMPTY iff
  ε_lo < ε_hi and ε_lo ≤ 1 (if every starved ε_req > 1, W = [ε_lo, 1]). A starved-set system with ε_req = 0 (no surplus or net
  energy release) makes W empty. **Class over all primary corners (§3.6):** WINDOW EXISTS if W is non-empty in every corner; NO
  WINDOW if empty in every corner; BRACKET-DEPENDENT otherwise. **Robustness downgrade:** if the class on the primary measure (b)
  is WINDOW EXISTS or NO WINDOW but measure (a) or (c) (§3.4) gives a different class, the reported class is BRACKET-DEPENDENT.
  Primary starved set S_A = {UFD-c, UFD-e, Draco-like, cluster core}; rotators = {SPARC-like gas-rich dwarf, MW-like disc}.
  Variant S_B = S_A + Fornax-like (reported; Fornax's own row always reported).
- **Q4 (consistency).** (i) Code reading of the CFG650 engine (M1 per-host supply, M2 condensed source, M3 census gas expulsion):
  does any module carry an energy budget, and is energy-limited settling in conflict with it? (ii) Does the shear pass (CFG650
  T1x/T2x, CFG654 NC1x) assume complete settling: does the engine remove surpluses, fill deficits, and at what resolution?
  (iii) Reported number: E_M3 / E_avail, the energy to expel the census non-retained baryons ((1 − f_ret) f_b M_ta, taken to trace
  the primordial NFW, lifted from circular-orbit energy to rest at r_ta in the primordial potential) against the same E_avail.
  Answered in words with code line references and the number; no class.

## 2. Derivation deliverable

`DERIVATION.md`: the 3-D energy equation of the CFG638 system with self-gravity, the drift power in closed form for the two-sided
deficit (ψ = Φ_law − Φ ⇒ v_s = ατ(g_law − g) ⇒ P_drift = ∫ρ_c v_s·∇Φ dV = α∫ρ_c τ g·(g − g_law) dV), the bath term, the sign
on a central surplus, the dark-energy partner's books (CFG542 Q = −ρ_c v_s·∇Φ), the one-sided / gated cases, and the virial
identity used in Q2 (ΔE = ½ΔW for a mass-conserving rearrangement inside R_x with the outside unchanged).

## 3. Inputs and rules (all declared now)

### 3.1 Constants and supply
- G, M☉, kpc as in CFG541 (6.674e-11, 1.989e30, 3.0857e19). f_b = 0.157126 (record; (1 − f_b)/f_b = 5.364).
- Native background: Ω_m h², h, linear P(k) at z = 0 and growth D(a) from `CFG654_independent_inputs/cfg654_ics_tables_cmb.npz`
  (A1 primary set); Δ_ta(z = 0) = 11.8977 from `cfg654_delta_ta_cmb.json`. These are the record's framework-native early-universe
  inputs (CFG654 principle); disclosed: ω_c, A_s, n_s come from a Planck primary-CMB table.
- Catchment (CFG541 E9): M_ta = L · M_b,now / (f_ret f_b), f_ret = CFG416 `fret_of(log10(M_ta h))` with h = 0.674, solved by fixed
  point; M_cat = (1 − f_b) M_ta; r_ta from M_ta = (4π/3) r_ta³ Δ_ta ρ̄_m (native ρ̄_m). L = 1 is the record rule. **Baryon-loss
  bracket for gas-poor dwarfs (UFD-c, UFD-e, Draco, Fornax): L ∈ {1, 10, 100}.** L = 1 for rotators and the cluster.

### 3.2 Primordial profile (framework-native collapse debris)
- Total primordial matter = NFW truncated at r_ta with M(<r_ta) = M_ta; primordial cold energy ρ_c,prim = (1 − f_b) ρ_NFW (total cold
  mass M_cat). The present baryons are the same in both states.
- Concentration c = r_ta/r_s from the native collapse epoch: the mean density inside r_s equals Δ_vir ρ̄_m(z_s), Δ_vir = 18π²
  (top-hat), where z_s is the epoch at which the extended-Press–Schechter collapsed fraction of M_ta in progenitors above F·M_ta
  equals M(<r_s)/M_ta: erfc[(δ_c/D(z_s) − δ_c)/√(2(σ²(F M_ta) − σ²(M_ta)))] = M(<r_s)/M_ta, δ_c = 1.686, σ(M) top-hat from the native
  P(k) (power-law extension beyond k_max with the last-decade log slope). **Cusp bracket:** EPS F ∈ {0.2, 0.05 (central), 0.01}
  plus PS1 (σ(M(<r_s)) D(z_s) = δ_c, the 1σ-peak epoch; lowest cusp). c is solved in [1, 1e4]; if no root, c = 1 (reported).

### 3.3 Systems (declared representative values, from memory of the literature, not fitted; no downloads; spherical)
| system | role | baryons | M* | other | r_obs |
|---|---|---|---|---|---|
| UFD-c (compact) | starved | Plummer, R_e = 30 pc | 5e3 M☉ | no gas, no BH | 3-D r_h = 1.305 R_e |
| UFD-e (extended, Boötes-I-like) | starved | Plummer, R_e = 240 pc | 3e4 M☉ | no gas, no BH | 1.305 R_e |
| Draco-like | starved | Plummer, R_e = 220 pc | 5e5 M☉ | no gas, no BH | 1.305 R_e |
| Fornax-like | reported / S_B | Plummer, R_e = 710 pc | 4e7 M☉ | no gas, no BH | 1.305 R_e |
| SPARC-like gas-rich dwarf (DDO 154-like) | rotator | stars exp. R_d = 0.6 kpc; gas exp. R_g = 2.0 kpc (sphericalised M(<r) = M[1 − (1 + r/R)e^(−r/R)]) | 2.6e7 M☉ | M_gas = 3.66e8 M☉ | 5 kpc |
| MW-like disc (CFG541's MW-like system) | rotator | Hernquist M_b = 6e10, a = 2.5 kpc | 5e10 M☉ | M_BH 4.3e6 M☉ | 8 kpc |
| cluster core (eRASS1/X-COP-like) | starved | gas β-model r_c = 150 kpc, β = 2/3, M_gas(<1.2 Mpc) = 1e14, truncated at 2.4 Mpc; BCG Hernquist 1.5e12, a = 30 kpc; member+ICL stars 1e13 distributed like the gas | stars inside the region | M_BH bracket {1e9, 5e9, 2e10} | 0.5 Mpc |

- Settled law profile: round-rule phantom (CFG541 E7) M_ph(<r) = M_b(<r)/expm1(√y), y = G M_b(<r)/(r² a0); inside-out fill:
  ρ_c,set = ρ_ph for r ≤ r_*, 0 for r_* < r ≤ r_ta, with M_ph(<r_*) = M_cat (two-sided end state; the CFG541 drift-only edge).
- Retained-excess diagnostic (reported, no class): X_ret = log10{[M_b + M(max(ρ_ph, ρ_c,prim))](<r_obs) / [M_b + M_ph](<r_obs)}, the
  total-mass excess an energy-starved system would show (CFG541's one-sided minimiser, overfill retained).

### 3.4 Region and the three ΔE measures
- Cumulative cold masses M_p(r), M_s(r). **Region R_x** = the outermost radius below r_* at which M_p − M_s changes sign from
  positive to negative (end of the outermost primordial surplus zone). Mass inside R_x is equal in both states, so only the
  rearrangement inside R_x is costed. If M_p − M_s is never positive below r_*: "no surplus", ΔE_core = 0, ε_req = 0.
- **(b) PRIMARY, "in the law's potential":** ΔE_b = ∫_0^{R_x} (ρ_c,set − ρ_c,prim)[Φ_law + ½ v_c,law²] dV, Φ_law and v_c,law of the
  settled (law) total mass (virial energy of the cold mass in the fixed law potential; zero point cancels at equal mass).
- **(a) self-consistent:** ΔE_a = ½[W_set(<R_x) − W_prim(<R_x)], W(<R) = −∫_0^R G M_tot(<r) dM_tot/r (baryons + cold; virial, outside
  unchanged).
- **(c) gross local transport:** ΔE_c = ∫ dm max(0, E_law(r_s(m)) − E_law(r_p(m))) over cold mass coordinates m ≤ M_p(R_x), shells
  ordered (monotone map), E_law = Φ_law + ½ v_c,law²: the cost if inward release cannot pay outward lifts (local drift transport).
- Also reported: the whole-catchment values (R = r_ta) of (a) and (b) (infall included), and M_sur = max_r (M_p − M_s).

### 3.5 Available energy
- E_SN = e_SN M*_formed, e_SN = 1e49 erg per M☉ formed (declared), M*_formed = M*(<region)/0.6 (return fraction 0.4, declared); for
  dwarfs and rotators all stars count; for the cluster the BCG + member/ICL stars inside max(R_x, r_obs).
- E_AGN = 0.1 M_BH c² (declared radiative/mechanical release); dwarfs and the gas-rich dwarf 0; MW 4.3e6 M☉; cluster bracket.
- E_avail = E_SN + E_AGN; ε (unknown coupling) is universal.

### 3.6 Corners
Primary corners = footing {can, alt} × cusp {PS1, EPS 0.2, EPS 0.05, EPS 0.01} × dwarf loss L {1, 10, 100} × cluster M_BH {1e9, 5e9,
2e10} = 72 corners, measure (b), starved set S_A. Central corner: EPS 0.05, L 1, M_BH 5e9 (both footings).

## 4. 1-D drift test (Q1)
Units G = 1. Baryons static Plummer M_b = 1, a = 1; a0 = 0.05 G M_b/a² (deep regime outside the core); cold energy initially NFW
M_c = 30, r_s = 3, truncated at R_C = 30 (catchment = mobility region), at rest (drift-only sub-flow as CFG541/542: element velocities
untouched, no orbits); log grid N = 400 from 1e-3 to 30; donor-cell fluxes; reflecting at both ends; τ = (4πGρ_m)^(−1/2); α = 1;
CFL 0.2; run to t = 200 (G = 1 units) or steady. Two-sided ψ' = G[M_ph(<r) − M_c(<r)]/r²; one-sided with d = max(ρ_ph − ρ_c, 0).
Record ΔW (exact, cold + baryons) and ∫P_drift dt with P_drift = Σ_faces F_face (Φ_{i+1} − Φ_i); split into outward and inward faces.
Pass for the identity: |ΔW − ∫P dt| ≤ 2% of |ΔW|. Also report the one-sided case (central surplus mass change, ΔW sign).

## 5. Controls
- **K1:** numerical W of truncated NFW (c = 10, 30) vs the analytic −(GM²/(2 r_s m(c)²))[1 − 1/(1 + c)² − 2 ln(1 + c)/(1 + c)], and of
  Plummer (to 1e5 a) vs −3πGM²/(32a): relative error < 1e-6 each, with the integrator used in Q2.
- **K2:** reproduce CFG541's MW-like canonical record numbers with its own discretisation (400 log cells, rin = 0.01 a, r_ta from
  its JSON 1249.9941101609163 kpc, max(ρ_ph, ρ_c0)): M_cat/M_b = 53.6432722396066 to 1e-9 and r_analytic = 514.3182020135458 kpc to
  1e-6 (relative); and the continuous phantom M_ph(<r) at that r_* vs the cell sum to ≤ 1e-3.
- **K3:** virial cross-check: ΔE_a (½ΔW) vs a direct isotropic-Jeans W + K evaluation on the central MW and Draco rows: agree to ≤ 1e-2
  of |ΔE_a| or 1e-6 of |W|.
- **MUTATE (separate run, `CFG932_MUTATE=1`, outputs `_MUTATE`):** M1 primordial ≡ settled (ρ_c,prim := ρ_c,set) → every ΔE measure
  must be 0 (|ΔE| ≤ 1e-9 |W|); M2 a0 → 1e-6 a0 (near-Newtonian) → the settled cold mass inside r_obs must change by more than ×10 for
  every system. The MUTATE run exits 1 when both teeth bite (record convention).

## 6. Execution limits (a live 1024³ job runs beside this lane)
One process at a time, OMP_NUM_THREADS=1, nice 10, < 1 GB. Run order: K/MUTATE first, then main (both footings in one run).
Outputs: `cfg932.py` → `cfg932.out`, `cfg932_results.json`; MUTATE → `cfg932_MUTATE.out`, `cfg932_results_MUTATE.json`.
Every quoted number comes from a JSON. κ = ½ FITTED; footings never pooled; not theory closed.
