# CFG598 FROZEN CRITERIA: the settling front with the transport-clock correction. Can ONE α give a settled MW, partial settling at 0.2–0.5 r_ta in groups and clusters, and a smaller gravitating-field excess?

Frozen 2026-10-10, before any CFG598 script is written or any CFG598 number is computed. This file is committed alone and is never edited afterwards. Later notes go in the README as dated disclosures.

Standing settings:
- κ = ½ is FITTED. The footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s² are scored separately and never pooled.
- Flat a0, kernel ν_mono = 1/(1 − e^−√y) (CFG541 A1), candidate B, G9 (only real mass gravitates), no EFE.
- The cold energy's MASS is still required. No particle species is added. This is not "theory closed", and nothing here says the data favour the framework.
- Framework-native verdicts: no ΛCDM or standard-MOND yardstick enters a verdict. CFG593's 30–80% requirement used ΛCDM-SHMR masses, so it is reported as context only.
- No knobs: α is O(1) FREE in the theory (CFG541 V5). It is evaluated on the fixed set {0.25, 0.5, 1, 2}, which is the theory's allowed range. It is not fitted.
- Other lanes are used read-only (imported or exec'd, never edited). Nothing in sol61_push/ is edited. No downloads, no PM runs. nice -n 10, ≤ 4 threads, ≤ 8 GB.

## 0. The lead

The transport_clock checkpoint (sol61_push/transport_clock_2026_10_10, check.py re-run 87/87 PASS) derives, from CFG541 E3–E6, the instantaneous rate for a filled core of radius r_i plus a uniform partial fill f outside it:
∂_t f = α V_f √f (1 − f) r_i / r².
Shells at r fill r/r_i times slower than the homogeneous single clock Γ(1 − f), Γ = α√f V_f/r. The checkpoint warns that this formula must not be integrated as a closed one-variable ODE, because uniform f is lost at once. This lane therefore integrates the full radial drift PDE of CFG541 class A. In that PDE the transport-clock geometry is automatic, with infall sources over cosmic time.

## 1. The model (task 1)

**Equations.** CFG541 E3–E6 in spherical symmetry, drift sub-flow only:
- ∂_t ρ_c + ∇·(ρ_c v_s) = s(r, t);
- v_s = −α τ ∂_r ψ, with ∂_r ψ = G D(<r)/r²;
- D(<r) = ∫_0^r 4πr'² max(ρ_ph − ρ_c, 0) dr' on B ∩ C = {r < r_ta(t)};
- τ = (4πG(ρ_b + ρ_c))^−1/2;
- mobility zero for r ≥ r_ta(t).

The numerics are CFG541's donor-cell flux scheme, copied with citation: inward flux at internal faces with the outer cell as donor, CFL 0.4, Γ dt ≤ 0.2, and a trace threshold. A last trace moves whole, so mass is exact. No drift-speed limiter is added: class A as written (CFG541 open item 3). max |v_s|/V_f is reported.

**Phantom target.** Round rule (E7) for the host's own baryons:
- point mass: M_ph(<r) = M_b (ν(y) − 1), with y = G M_b/(r² a0);
- MW: Hernquist M_b(<r) = M_b r²/(r + a)², with M_b = 6e10 Msun and a = 2.5 kpc (CFG541 MW-like).

The baryons grow with the main progenitor: M_b(t) = M_b,0 X_ta(t). Here X_ta(t) is the fraction of M_ta that has turned around by t. M_b,0 = f_ret f_b M_ta, with census f_ret = CFG416 `fret_of(log10 M_ta [Msun/h])`. For the MW, f_ret = 0.10. This is a declared approximation.

**Accretion history: INHERITED and flagged.** CFG557's `cfg557_lib` is imported read-only:
- EPS mean main-progenitor ODE, Neistein+06 form, q = 2.2, recalled, PROVISIONAL;
- spherical-collapse trajectories in the ΛCDM background.

Each shell X = M/M_ta gets a turnaround time t_ta(X), a physical turnaround radius r_ta,sh(X) and a collapse time t_coll(X) = t_ta + (time to reach 0.003 r_ta). The host's mobility edge at time t is r_ta(t) = r_ta,sh of the shell turning around at t. CFG557 used the same history: outside B ∩ C cold energy is cold matter, and R3 conserves the turnaround mass. It is still not derived from the framework alone, so every result carries the tag "accretion history inherited (CFG557)".

**Where the arriving cold energy is put: two placements, both always run.** They are brackets, not knobs.
- **P0, at rest at turnaround.** This is the CFG541 drift-only convention and the transport clock's outer feeding boundary. A shell's cold energy (1 − f_b) M_ta dX is deposited at t_ta(X) into the cell that contains r_ta,sh(X). Only the drift moves it. This is the slow-delivery bracket.
- **P2, after first collapse, radial-orbit average.** At t_coll(X) the shell's cold energy is deposited inside the apocentre R = r_ta,sh(X)/2 (spherical-collapse virial contraction). The weights are the time spent on a radial orbit in the deep-law isothermal potential, with enclosed-mass CDF F(<r) = erfc(√ln(R/r)) for r < R. This is the orbit-assisted bracket.
- Shells with X < 0.02 (CFG557's grid floor) are placed at the start time t_s = t_ta(0.02) as ρ ∝ r^−2 out to the placement radius of the X = 0.02 shell.
- Shells with t_ta (P0) or t_coll (P2) > t0 are not deposited. Their mass is reported as in transit.

**Grid.** N = 300 log cells from r_in to r_ta(t0):
- point-mass hosts: r_in = 0.01 r_M(t0);
- MW: r_in = 0.01 a.

Convergence check: N = 600 at log M_ta = 14, α = 0.5, both placements, canonical. If any reported F_set changes by more than 0.02, that is a dated disclosure.

**Hosts.**
- log M_ta [Msun/h] ∈ {11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15}, point-mass baryons. This grid spans CFG593's host set: CFG556's halo-model masses and the KiDS f30 lens range.
- The MW host as above.
- Every host is run at z = 0 for α ∈ {0, 0.25, 0.5, 1, 2} and α → ∞, both footings, both placements. α = 0 is the reservoir-only reference, reported only.

**α → ∞ (exact, not a large-α run).** After each deposit the state is replaced by the drift's minimiser, the CFG541 V4 inside-out fill:
- cells inside the contiguous filled core are unchanged, including any overfill;
- beyond it, the cells are filled to max(ρ_ph, ρ_c) outward until the mass beyond the core is used up;
- nothing is left beyond that radius.

**Outputs at t0, per host, α, footing, placement.**
- Local fill q(r) = ρ_c/ρ_ph.
- Cumulative settled fraction F_set(<r) = ∫ min(ρ_c, ρ_ph) dV / M_ph(<r), at r/r_ta ∈ {0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0}. r_ta is r_ta(t0).
- Front radius r_f/r_ta: the inner face of the first cell from the centre with q < 0.9 (primary). The q < 0.5 and q < 0.99 fronts are reported.
- Settled mass S(<r) = ∫ min(ρ_c, ρ_ph) dV, and the ratios S_α/S_∞ (finite age, α → ∞) and S_α/S_cen. S_cen is the infinite-age census minimiser with the whole supply (1 − f_b) M_ta, i.e. CFG541's edge r_* = r_M/ln(1 + M_b/M_cat).
- Total cold mass ratio M_c,α(<r)/M_c,cen(<r).
- In-transit mass, max |v_s|/V_f, and the mass-conservation error.

**Supply-based α bound (transport clock §1, evaluated).** α_sup = G S_avail / (T V_f³ · max_f √f(1 − f)), with max_f √f(1 − f) = 2/(3√3), S_avail = (1 − f_b) M_ta, V_f = (G M_b,0 a0)^¼ and T = t0 − t_ta(X = 0.5). T = t0 − t_s is also reported. For α < α_sup the drift current cannot exhaust the catchment within T, so the reservoir stays unexhausted. Exhaustion, i.e. full settling to the supply edge, needs α ≥ α_sup. The PDE decides what actually happens; the bound is reported next to the PDE's delivered fraction.

## 2. Comparisons (task 2)

**(a) CFG593, CONTEXT ONLY (it used ΛCDM-SHMR masses).** The post-hoc requirement was 30–80% of the law's phantom settled, reaching ≈ 0.5 r_ta. It is compared with F_set(<0.5 r_ta) and F_set(<0.2 r_ta) for log M_ta 13–15, and with the shape: a uniform partial fill (CFG593 family) against an inside-out front (this PDE). No verdict uses it.

**(b) Framework-native constraints.**
- **MW (CFG553 sealed predictions inside 30 kpc must stay unchanged).** MW host at t0, per α, footing and placement.
  - SETTLED iff q ≥ 0.99 in every cell with r ≤ 30 kpc.
  - OVERFILLED iff M_c(<30 kpc)/M_ph(<30 kpc) − 1 > 0.01. Class A cannot remove an overfill (CFG541 open item 5).
  - **(i) holds iff SETTLED and not OVERFILLED.** Whether an overfill is α-independent (present at α = 0) is reported.
- **Groups (CFG543 P2).** `cfg543_group_supply` is imported read-only and `sigma_log` is copied with ONE change: the law's cold mass min(M_ph(<r), M_sup) is multiplied by R(r) = M_c,α(<r/r_ta, t0)/M_c,cen(<r/r_ta).
  - R is interpolated in log M_ta between the grid hosts, and in r/r_ta. Each group's M_ta [Msun/h] = M_bar h/(0.10 f_b) (P2 containment), and r_ta = r_ta(t0) of the host model at that mass, interpolated in log M_ta.
  - PASS iff |Z| < 2, per footing, with CFG543's statistic.
  - Control G0: R ≡ 1 reproduces CFG543's P2 mean to ≤ 1e-6.
  - Declared approximation: the ratio comes from point-mass hosts and is applied to CFG543's Hernquist groups.
- **Growth / excess (CFG555 machinery).** The CFG555 512³ caches are used: 425_R3_can_512 (canonical) and 439_A_alt_512 (alt), with P_part, P_grav, P_src and s8_*.
  - Scale the settled source by a scalar λ: P(λ) = P_p + λ(P_g − P_p − P_s) + λ² P_s, and σ8(λ)² the same way in squares.
  - Score with CFG555's `stat` against the matched S0 JSON.
  - λ = mean over log M_ta ∈ {13, 13.5, 14, 14.5, 15} of S_α(<0.5 r_ta)/S_cen(<0.5 r_ta), per α, footing and placement. The min and max over those hosts are reported as a bracket.
  - Controls: λ = 1 reproduces CFG555's gravitating max|P − 1| and σ8 ratio (0.163 / 0.193) to ≤ 1e-6; λ = 0 reproduces the particle values.
  - **Declared approximation:** one global amplitude. It is not per host, and the radial redistribution inside each host is ignored. The unsettled part stays in the particle field as ordinary cold matter.
  - **(iii) levels:**
    - PASS iff max|P − 1| (k ≤ 1) ≤ 0.10 AND |σ8 ratio − 1| ≤ 0.05 (the CFG361 GROWTH OK bar), on both footings;
    - REDUCED iff max|P − 1| is ≥ 25% below CFG555's value on both footings but not PASS;
    - otherwise NOT REDUCED.

## 3. Verdict (task 3)

Per placement, and per α ∈ {0.25, 0.5, 1, 2}, on both footings:
- (i) MW as in §2(b);
- (ii) partial settling at 0.2–0.5 r_ta in groups and clusters. For every host log M_ta ∈ {13, 13.5, 14, 14.5, 15}: F_set(<0.2 r_ta) ≤ 0.8, AND 0.3 ≤ F_set(<0.5 r_ta) ≤ 0.8, AND S_α/S_∞(<0.5 r_ta) ≤ 0.9. The last condition means the partial fill is rate-limited, not merely CFG557's finite-age supply edge;
- (iii) as in §2(b).

Labels per placement:
- **ONE-α PARTIAL SETTLING WORKS (α = …)**: some single α satisfies (i), (ii) and (iii) = PASS on both footings, AND CFG543 groups PASS on both footings at that α.
- **PARTIAL**: some single α satisfies (i) and at least one of {(ii), (iii) ≥ REDUCED}. Also PARTIAL if all three hold but groups fail.
- **DOES NOT**: otherwise.

Overall: if P0 and P2 give the same label, that label stands. If they differ, the WEAKER label stands (DOES NOT < PARTIAL < WORKS), tagged PLACEMENT-SENSITIVE, with both reported.

## 4. Controls and MUTATE

**Controls (main run).**
- K1: t0 and Δ_ta from cfg557_lib agree with CFG557 (13.820 Gyr; 11.806) to 1e-3.
- K2: mass conservation |M_grid + M_transit − M_deposited-total|/M ≤ 1e-10 in every run.
- K3: the transport_clock benchmark. On the grid, set a filled core at r_i and a uniform f = 0.2, 0.5 or 0.8 outside it, then evaluate one instantaneous step of the PDE flux divergence. It must reproduce ∂_t f = α V_f √f (1 − f) r_i/r² to ≤ 2% at r/r_i ∈ {2, 5, 10}.
- K4: no run hits the step cap. If one does, it is a dated disclosure and that cell is NOT EVALUATED.

**MUTATE (CFG598_MUTATE=1; writes *_MUTATE.out and *_MUTATE.json; exits 1 iff every tooth bites).**
- M1, α → ∞. The PDE at α = 64 (log M_ta = 14, canonical, both placements) must reproduce the exact α → ∞ trajectory: |ΔF_set(<r)| ≤ 0.03 at every reported r/r_ta, and |S(<r_ta) ratio − 1| ≤ 0.03.
- M1b. The α → ∞ minimiser with the whole supply present and infinite age reproduces CFG541's point-mass edge r_M/ln(1 + M_b/M_cat) to ≤ 1% (log M_ta = 12 and 14, both footings).
- M2, no transport-clock correction. The single-clock code path replaces the flux divergence by per-cell homogeneous relaxation df/dt = α√f(1 − f) V_f/r. It must reproduce the analytic u = tanh(α V_f t/(2r) + atanh u0), f = u², to ≤ 1e-3. On the K3 benchmark it must differ from the PDE rate by the factor r/r_i to ≤ 2%, so the correction is a tooth.
- Reported: f_set at t0 under the single clock against the PDE, per host, at α = 0.5 and 1.

## 5. Pre-freeze hand estimate (2026-10-10, for honesty about expectations)

- α_sup ≈ 0.5–0.9 across log M_ta 12–15. The current a host can carry is J_max ≈ 0.385 α V_f³/G, against a cold accretion rate of about S/T.
- So for α ≳ 1 the hosts are expected to exhaust their supply: settled to the supply edge, with no rate-limited partial state. Partial settling, if any, is expected at α ≈ 0.25–0.5, where the MW interior must still fill.
- The inside-out front fills the inner radii first. That is the opposite of the reduced inner mass (0.05–0.2 r_ta) that CFG593's uniform-f family asks for. A NOT REDUCED or REDUCED (not PASS) outcome for (iii) would not be surprising.
