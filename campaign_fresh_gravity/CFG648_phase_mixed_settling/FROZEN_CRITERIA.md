# CFG648 FROZEN CRITERIA: phase-mixed settling (hypothesis H-SP)

Date 2026-10-12. Committed ALONE, before any CFG648 code or any H-SP number exists.

Settings: κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻² (the CFG543 group path keeps its own
9.36e-11 / 1.13e-10), never pooled; every test reported per footing. "Cold energy" throughout; its mass is required; no
particle species. Both sources reported separately: all-baryon (candidate B) and condensed-only (H-CB). No ΛCDM or
standard-MOND yardstick enters any verdict; the T6 halo model and any EPS accretion history are ΛCDM-built and are labelled
CONTEXT ONLY wherever they appear. Not "theory closed". No PM run (no grid ≥ 256³), no download. 1 process, ≤ 1.5 GB,
nice -n 10. cfg636_pm.py, the cfg640 waiter, the cfg625 driver and other agents' jobs are not touched.

## 0. Hypothesis

**H-SP:** cold energy settles into the law's round phantom (R1, R6) only inside the system's SPLASHBACK radius r_sp, the
outermost first apocentre of shells that have passed their first pericentre (the boundary between phase-mixed orbiting
material and first-infall material). Candidate B's switch 1_B lets cold energy settle anywhere inside turnaround; H-SP
narrows the settling region to the phase-mixed part. Settling into a STEADY profile is only meaningful where the material
is phase-mixed. Supply (A6, 5.364 × catchment baryons), R2 (supply edge), R5 (never drawn back), R7 (no EFE) and G9 (only real
mass gravitates) are kept. **Zero new constants:** r_sp is read off the framework's own infall dynamics, not set by hand.

Structural statement **S1** (to be verified numerically): H-SP can only move the SETTLED edge inward,
r_set = min(r_edge, r_sp). It cannot place settled cold energy beyond B's supply edge. The supply it frees stays as
collisionless (unsettled) cold energy in the catchment, located by its own orbits (CFG637 Method A).

How H-SP differs from CFG598 (finite-age partial settling, which did not fix growth): CFG598 changes WHEN the law's profile
fills (inside-out front, timing); every region still settles eventually, and the outer settled shell at 0.2–0.5 r_ta is the last
to go but is reached. H-SP removes WHERE: material outside r_sp never settles while it is on first infall, however old the
system. Whether this removes the 0.2–0.5 r_ta settled mass that CFG556/CFG596 flag is decided by r_sp/r_ta, computed here.

## 1. Derivation of r_sp (framework dynamics; library cfg648_lib.py)

Engine: CFG637's committed self-similar secondary-infall solver (`cfg637_lib.Infall`, imported read-only) in the framework's
own flat background, G9 potential (baryons + settled cold energy + reservoir + not-yet-turned shells + Λ term), seed slope ε and
angular-momentum bracket q as CFG637 (INHERITED context: ε = 1 primary, q = 0.1). One subclass adds only:
- **Tracking:** a shell has passed pericentre when, after turnaround, its radial velocity changes sign from < 0 to ≥ 0; its first
  apocentre is the next sign change > 0 → ≤ 0 (radius and time recorded).
- **r_sp(t) (PRIMARY):** the outermost caustic = the largest current radius among shells that have passed pericentre.
  Settled cold energy is never taken back (R5), so the settling cut uses the running maximum r_sp,eff(t) = max_{t'≤t} r_sp(t').
  **Bracket "apo":** the median first-apocentre radius of shells whose first apocentre occurred within the last Δln a = 0.1
  (latest apocentre if none in the window).
- **Settling (H-SP):** the settled target is the law's phantom of the source baryons truncated at min(supply edge, r_sp,eff),
  confined to r_ta, applied LIVE inside the run (the potential the shells feel includes it, so r_sp is self-consistent).
- **Draw (PRIMARY):** the settled increment is drawn outer-first from the cold weight of shells that have passed pericentre (the
  continuous limit of R5 with the edge at r_sp: only phase-mixed material settles). **Bracket "R5lit":** CFG637's draw rule with the
  edge replaced by min(edge, r_sp) (draws from any turned-around shell beyond the cut, including first-infall material).
- **Read-out (PRIMARY, H-SP):** phase-mixed reservoir shells are orbit-averaged in the final potential (CFG637's routine);
  first-infall shells (turned, not yet at pericentre) are placed at their current radius. With H-SP OFF the solver runs
  CFG637's code path unchanged (MUTATE M-ta).
- **Accretion rate:** Γ = Δln M_ta / Δln a over the last Δln a = 0.4 before a_obs, measured in the run from the turned-around
  mass history (M_ta is the turnaround mass, declared).

**D1 (r_sp/r_ta vs Γ and mass).** Representative systems as CFG637: galaxy (M_b 6e10, Hernquist a 3 kpc, f_ret 0.10), group
(CFG637's median Tian group), cluster (A1795, X-COP audit profile, f_ret 0.90); ε ∈ {0.3, 0.5, 0.75, 1, 1.5, 2.5}; both
footings; both sources. Reported: Γ, s = r_sp/r_ta (primary and apo), x_edge = r_edge/r_ta (B's), x_set = r_set/r_ta, settled
mass / B's settled mass, reservoir / supply, settled and reservoir mass inside 0.2–0.5 r_ta. Labels per mass:
- **TREND** if the Spearman ρ(s, Γ) over the ε grid is < 0 at that mass on both footings (prediction (a): faster accretion → smaller
  r_sp/r_ta); **NO TREND** otherwise.
- **BINDS** at ε = 1 if s < x_edge (both footings), **DOES NOT BIND** otherwise.
- Mass dependence of s at fixed ε reported (the potential differs between scales: f_ret, core concentration, settled mass).

**D2 (Γ per system).** PRIMARY: the framework's own run (ε = 1, flat background) gives each system's Γ_fw and s. CONTEXT:
the seed profile δ_L(M/M_ta) from CFG557's EPS mean main-progenitor history (`cfg557_lib.Epoch.mah`, ΛCDM-background,
PROVISIONAL) replaces the power law (shape only; normalisation calibrated as in CFG637). For observed systems the measured
proxies on disk are colour-at-fixed-mass (KiDS early types, CFG585/700: OLD = redder third). No SPS model is on disk, so
colour → Γ is not converted; T5 reports the H-SP amplitude over the full Γ range the solver spans (an upper bound) and its sign.

## 2. Tests (light; reuse committed code; per footing; both sources)

Per-system solver runs (ε = 1, N = 1600) for: SPARC (each galaxy, rotmod baryons, point mass inside the first data point and
constant beyond the last, f_ret 0.10; B source = H-CB for SPARC, CFG634 T1), the 63 Tian+26 groups, the 12 X-COP clusters, Bullet
progenitors BASE/B1/B2/B3 (a_obs 1/1.296), KiDS lens masses at the 5/50/95 percentiles (point-mass baryons; B = H-CB, the lens
source is stars + cold gas), the CFG556 halo masses (T6). Gate inputs, supply conventions and statistics are CFG634's/CFG637's,
executed from their committed source text with ONE patch per function: the settled phantom is cut at the system's r_sp (held
at M_ph(r_sp) beyond it) and the derived reservoir M_res(<r) (gate units, CFG637 scaling supply_gate/supply_A) is added.

| test | label rule (both footings unless stated) |
|---|---|
| **T1 SPARC** (CFG487 harness as CFG645 T1 runs it) | PASS if rms ≤ 0.12 and \|Δrms vs B\| ≤ 0.005; FAIL if rms > 0.15; else TENSION |
| **T2 Tian+26 groups** (CFG634 `sigma_hcb`, res = RD-SP) | CFG543 stats label; PASS = CLOSES |
| **T3 X-COP** (CFG634 `cl_model`/`t3_cell`/`t3_label`) | t3_label on the headline η AND on the inner band 200–420 kpc, both reported |
| **T4 Bullet** (CFG634 `dark_components`/`t4_cell`) | t4_cell label for B1 (static aperture contrast); core M(<250)/P16 reported (PROVISIONAL). Merger statement: H-SP's own phase-mixing time (pericentre → first apocentre of the shells at r_sp in the B1 main run) vs the Bullet's time since pericentre; if longer, H-SP predicts NO settling during the passage (α_eff = 0, the only value CFG623 allows) |
| **T5 KiDS isolated lenses** | δ_in, δ_9 = ESD_HSP/ESD_B − 1 in the K-in (bins 12–14) and K9 (bins 6–14) bands of CFG700 (radii from the gbar edges at each lens mass), from the solver's final total mass profile (excess over the mean density, projected). Record (CFG529): f30 inner-bin DEFICIT. Label: HELPS if δ_in ≥ +0.05, WORSENS if δ_in ≤ −0.05, else UNCHANGED (= record FAIL). **Age split:** H-SP predicts OLD (low Γ, more phase-mixed) ≥ YOUNG; A_HSP,max = log10[ESD_K9(lowest Γ)/ESD_K9(highest Γ)] over the D1 ε grid at the median lens mass. Observed (CFG700) A = +0.166, σ ≈ 0.071. Labels: SIGN (matches if A_HSP,max > 0); SIZE: CANNOT PRODUCE if A_HSP,max < 0.024 (observed − 2σ), CAN REACH if ≥ 0.166, else PARTIAL |
| **T6 growth proxy (CONTEXT ONLY)** (CFG556 halo model executed from source) | settled edge re → min(re, s(M) r_ta) with s(M) interpolated in log M from the T6 solver runs; mass inside r_ta conserved. PRIMARY placement: CFG556's own (the unsettled remainder in the shell beyond the edge, ML shape). Bracket: remainder with the solver's derived reservoir shape. Labels as CFG645: REMOVES if R(k=1) − 1 ≤ 0.10 and R(k=1) ≥ 0.90; REDUCES if the k = 1 excess falls by ≥ 25%; DEFICIT if R(k=1) < 0.90; else UNCHANGED |

**Inertness tolerance** (vs candidate B / CFG637 RD): ≤ 0.005 dex (T1, T2), ≤ 0.01 in η (T3), ≤ 0.1 in z (T4), ≤ 1% of the excess (T6).

## 3. Checks and MUTATE (`CFG648_MUTATE=1`, separate outputs)

- **C1** supply = drawn + reservoir (1e-9); the gravitating settled mass equals the drawn mass (max (drawn − target)/target over
  the run ≤ 1e-3, reported).
- **C2** N 1600 vs 3200: s changes by ≤ 5% (galaxy, group, cluster; ε = 1; reported, precision-limiting if not).
- **C3** (reported) no-core benchmark (ε 1, q 0.02, Λ background): s and the reservoir slope.
- **S1** settled M_set,HSP(<r) ≤ M_set,B(<r) at every r, every run (1e-9 relative).
- **M-ta** (must hold): r_sp → r_ta (H-SP off) reproduces CFG637's lib output for the three D1 systems (M_res(<r) arrays and
  summaries, to 0) and CFG637's gate JSON for B and H-CB RD|P|phase (T2, T3 headline + inner, T4 all variants; 1e-9) using
  CFG637's own profiles; and reproduces candidate B's T1 rms (CFG624) and CFG556's primary R(k) (1e-9).
- **M-Γ** (must hold): the EPS seed profiles are permuted across the D1/T6 masses (reversed order); the regression slope of s
  on each mass's OWN (unshuffled) Γ must change sign or fall below 50% of the unshuffled slope, while s vs the Γ actually used
  keeps the sign of D1's trend. If the unshuffled EPS route shows no trend, M-Γ is reported as not applicable.

## 4. Verdict rule (per source, both footings)

- **H-SP KNOB-FREE PASS** if T1 PASS, T2 CLOSES, T3 headline PASS, T4b B1 PASS, T5 not WORSENS, and T6 (context) REMOVES or
  REDUCES without DEFICIT.
- **INERT** (≡ candidate B; inherits CFG596 / CFG637 fails) if every gate statistic is within the inertness tolerance.
- Otherwise **FAILS** with the failing gates listed; the T6 reading and the age-split SIGN/SIZE are reported separately.
- The EPS (context) route is reported; it can add the label "ACCRETION-HISTORY-DEPENDENT" if it flips any gate label, but it
  cannot turn a FAIL into a PASS.
- A native PM specification (how a PM run tags phase-mixed vs first-infall particles per catchment, e.g. particles that have
  passed pericentre about their host) is written, not run.

## 5. Disclosure before any number (reasoning only; no script run)

Hand estimates made while reading: (i) for a self-similar infall with Γ ≈ 1 the outermost caustic sits near 0.35 r_ta, while
B's supply edge is 0.32–0.42 r_ta in galaxies and X-COP clusters and 0.49–0.99 r_ta in groups (CFG637). So at ε = 1 H-SP is
expected to bind strongly in groups and only marginally in galaxies and clusters; faster accretion should make it bind more.
(ii) By S1 H-SP cannot move a settled edge outward, so prediction (b) as phrased (settled mass farther out in isolated lenses)
cannot come from the settled phantom; any outward mass must come from the freed reservoir. (iii) The KiDS K9 band reaches about
0.35 r_ta for log M* 10.8, so the age amplitude from an r_sp shift is expected to be small. (iv) CFG637's derived reservoirs are
core-concentrated, so freed supply may ADD inner mass (relevant to T1, T3 inner band and T5). These expectations are written so
the computation can contradict them.
