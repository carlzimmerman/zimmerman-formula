# CFG916 FROZEN CRITERIA: lock-and-release (H-LR) against the galaxy, cluster, Bullet and dwarf constraints

Date 2026-10-20. Block 910–919 (LEDGER.md:662 reserves CFG916 for lock-and-release, owner request). Committed alone, before
any script of this lane exists and before any number of this lane is computed.

**Kind of lane: HYPOTHESIS TEST** (constructive, from CFG915). Every choice below is declared here. No knob is scanned. A clean
CONTRADICTED is a valid result.

**Settings.** κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s², never pooled; every class is given per
footing. Cold energy is real gravitating mass; no particle species is added. Not "theory closed". Nothing here says the data
favour the framework. Raw data and framework-native models only (no HMcode, BAHAMAS, ΛCDM mass function or "within X% of ΛCDM"
in any verdict). No downloads. One core (`OMP_NUM_THREADS=1 nice -n 10`), one process at a time, each < 1 GB; no PDE beyond the
record's 1-D drift model; no merger or 3-D run (a test that would need one is UNDERDETERMINED and its run is specified, §8).
Inputs are read only; no other lane is edited.

## 0. Why (record context)

- CFG913: no single local mobility law satisfies mergers (α ≈ 0), galaxy settling (α ≳ 0.5) and retained dwarf clumps (α ≲ 1e-2).
- CFG914: no common density threshold orders the open excesses.
- CFG915 (H-POP): rule LC (latch f → t on exact settling) passes the MW settling test only by latching the overfill, and then
  carries CFG726's merger memory (H-MM), which fails eRASS1/ACCEPT outer cluster profiles (Z −3.63/−4.05, −4.83/−5.19).
- CFG915's README ends with the untested constructive lead, quoted verbatim: "latching plus a release of t when it is stripped
  from its host. That would have to leave satellites' inner clumps intact (CFG838 found no tidal signal), keep Bullet-type cores
  immobile, and remove member-halo memory in clusters."

## 1. Naming (as CFG915 §1)

**t** = latched cold energy (α_t = 0, collisionless; dynamically the record's untethered class). **f** = mobile cold energy
(α_f ∈ {0.5, 1.0}; the record's settling class). Both gravitate and count toward the law's target.

## 2. H-LR, frozen (all new posits are listed in §2.6)

### 2.1 Latching rule: two readings, both graded
- **LR-x (primary, as posed).** CFG915's LC exactly: in every cell inside the owner's bound region that is settled
  (m_t + m_f ≥ m_ph(1 − 1e-12)) and has no deficit inside, all f becomes t (overfill included).
- **LR-c (declared variant).** Capped capture: the same cells, but a cell's t is raised only up to its phantom,
  Δm_t = min(m_f, max(m_ph − m_t, 0)). Capture never latches overfill. Overfill t exists only where already-latched t later
  exceeds a falling phantom (baryon loss, sub-additive superposition of latched pieces).
- **Why two (argued before any number, §9):** under exact capture, released cold energy that lands in a settled, deficit-free
  host region is latched again at once by the host. So under LR-x release cannot remove cluster memory. LR-c is the smallest
  change to the latching rule under which release can act. Two readings means two chances; this is disclosed.
  **Overall H-LR = the best class over LR-x and LR-c** (CONSISTENT > UNDERDETERMINED > CONTRADICTED).

### 2.2 Ownership and the member's bound region (new posit)
t belongs to the structure in whose bound region it was latched. While a structure orbits inside a host's field, its bound
region is its Jacobi sphere r < r_J. The host's bound region is r < r_ta (CFG598) outside the members' Jacobi spheres. Capture
inside a member's r_J latches to the member; capture elsewhere in the host latches to the host.

### 2.3 Release rule (new rule)
Member-owned t at member-centric radius r > r_J (at the epoch, §2.5) becomes f, mobile at α_f. Released f is ordinary f, subject
to the reading's capture rule (LR-x: re-latched in place wherever the host is settled with no deficit inside; LR-c: re-latched only
up to the host's phantom, so released surplus stays f). Release is irreversible: once released, cold energy is not returned to
the member. Host-owned t is never released by a member's r_J.

### 2.4 r_J convention (no new constant)
King/Jacobi tidal radius at member–host separation d:

  r_J³ / m(<r_J) = d³ / [(3 − γ(d)) M(<d)],   γ = d ln M / d ln r of the host at d,

i.e. r_J³ = G m(<r_J)/(Ω² − Φ''). If 3 − γ ≤ 0 (no tidal stretching), r_J = ∞. Solved by inverting the monotone function
r³/m(<r) on the member's grid. Masses are the law's effective (baryons + cold energy) masses:
- **member m(<r)** = its baryons + its own cold energy: the law phantom of its baryons, running maximum, cut at its own supply edge
  (5.364 × catchment; catchment = M_cond/0.10 for condensed baryons, i.e. 53.64 m) and confined to its own r_ta (CFG726
  `prog_halo` convention: `cfg637_lib.phantom_trunc`, `r_ta_single`);
- **host M(<r)** = the law's effective mass as each source lane builds it: clusters, the uncut law of all baryons (CFG687/686
  harness via CFG726); MW and M31, point-mass baryons 6.0e10 / 1.0e11 M_⊙ (CFG821/838/839 values) under the law; Bullet main,
  the record's CFG599 `Progenitor599` total mass (case L).
- Kernel: ν_s(y) = ½ + √(¼ + 1/y) (g_N = g²/(g + a0), CFG695) for r_J everywhere, except inside a source model that fixes its own
  kernel (the CFG598 MW drift model and the CFG599 Bullet progenitors keep their ν_e, unchanged, so the K identities hold).

### 2.5 Epoch convention
**Primary: pericentre** (the minimum r_J along the current orbit; release there is irreversible). **One alternative: present
position.** Each test states its pericentre source below. A member is assumed to have passed at least one pericentre on its
current orbit (steady state); where no pericentre has occurred (MW–M31 first approach), both conventions use the present position.
The class of each test is the primary epoch's class; the alternative's class is reported beside it, not combined.

### 2.6 Posits table (new unless marked)
| item | status |
|---|---|
| α_t = 0 | carried from CFG915 (posit against the record's universal push) |
| α_f ∈ {0.5, 1.0} | not new (the record's O(1) coefficient) |
| LR-x latching = CFG915 LC | not new here (new in CFG915) |
| LR-c capped capture | **new rule** (no constant) |
| ownership; member bound region = Jacobi sphere | **new posit** |
| release of member-owned t beyond r_J; irreversible | **new rule** (no constant) |
| r_J = King formula with the law's effective masses | **convention** (no constant) |
| pericentre epoch (alternative: present) | **convention** |
| cluster-member orbits: isotropic Gaussian velocities at the isotropic-Jeans σ of the member tracer in the host's law potential | **declared approximation** |
| released surplus relaxes to the host law by t_obs (transport-unlimited, M only) | **declared approximation** (§3 M) |
| member halos fully latched at infall (LR-c, M) | **worst case for H-LR** (less latching only lowers retained memory) |

## 3. Graded tests, data and grading

### G: CFG598's MW test (P0 drift model; CFG915's two-population code copied)
- Model: CFG915 `Run2` (copied, read-only reuse; CFG598 `cfg598_lib` imported), MW host, N = 300, both footings, α_f 0.5 and 1.0,
  α_t = 0, with (a) the reading's capture rule and (b) release: after every capture call, cells whose centre lies beyond r_J,MW get
  m_f += m_t, m_t = 0.
- r_J,MW: the MW as a member of the MW–M31 pair in M31's field (M31 the host; 1.0e11 M_⊙ point mass, law, ν_s; MW m(<r) = Hernquist
  6.0e10 M_⊙, a = 2.5 kpc + its own phantom per §2.4). No MW–M31 pericentre has occurred, so the epoch is the present position.
  d = |x_M31| with M31's Galactocentric position fitted by least squares to the LVD `distance_m31` of every LVD dwarf row (MW, M31 and
  local-field files) with finite distance (positions from LVD ra, dec, distance in astropy's default Galactocentric frame).
- **Grade (CFG598 (i)):** min q ≥ 0.99 for r ≤ 30 kpc AND M_c/M_ph(<30) − 1 ≤ 0.01. Per footing: CONSISTENT iff (i) holds at
  α_f 0.5 or 1.0; CONTRADICTED otherwise. CFG915's joint rule (both footings at the same α_f) is reported.

### M: cluster outer profiles (CFG726 machinery, ν_s primary kernel, memory placement P1, CFG726's member model and N_mem rule)
- Samples: T-R eRASS1 318 (CFG687 per-cluster ΔΣ, 30-patch RA jackknife) and T-A ACCEPT 8 (CFG686 ΔΣ, bootstrap 1000, seed 1),
  scored exactly as CFG726: A = ΣWD/ΣWP per band; Z_band = (A − 1)/σ.
- **LR-x:** released member t lands in the settled, deficit-free host (CFG915 C1's footing: hosts settled to their supply edge) and
  is re-latched in place, so the mass placement is unchanged: M(LR-x) ≡ release-none ≡ CFG726 primary (identity by argument; the
  numbers used are the release-none arrays).
- **LR-c:** each member's latched halo T_i is truncated at its r_J: retained C_J(<R) = Σ members' T_i(<min(s, r_J)) convolved over
  member positions (CFG726 `convolve_members` with a per-position truncation weight). Released cold energy is not re-latched beyond
  the host law and relaxes (two-sided drift, CFG638 form): M_LR(<r) = M_b(<r) + max[C_J(<r), T_rem(<r)].
  - Pericentre (primary): members co-distributed with the gas (CFG726 primary); host potential from the law mass M_b + T_rem;
    isotropic-Jeans σ_r(d) of that tracer (tracer truncated where the harness gas is truncated, 3 Mpc); Gaussian velocities with
    4 Gauss–Hermite nodes in |v_r| and 8 Gauss–Laguerre nodes in v_t²/(2σ²); r_p = the root of 2(E − Φ(r)) − L²/r² below d, floored
    at the harness grid's 1 kpc; r_J at r_p; the retention weight at each member position is the node-weighted fraction with r_J > s.
  - Present (alternative): r_J at d.
- **Graded statistic: Z_OUTER on eRASS1 and on ACCEPT.** MID is reported, not graded. (The plain law already fails eRASS1 MID,
  A 1.91 ± 0.12, CFG687/726. That open core excess is not addressed here; M asks only whether release removes the outer memory.)
- **Class per footing (LR-c graded at the static, transport-unlimited release limit):**
  - CONTRADICTED iff |Z_OUTER| ≥ 2 with A_OUTER < 1 (overshoot) in eRASS1 or ACCEPT (finite α_f leaves more released mass in place,
    so only more overshoot);
  - CONSISTENT (static) iff |Z_OUTER| < 2 in both;
  - UNDERDETERMINED otherwise (an undershoot, or missing inputs).
- Reported only:
  - eFEDS (T-E, CFG652 staging and score code as CFG726), with the BCG as the host's central (never released). CFG726's T-E fails at
    the law's own level, so it cannot grade memory removal;
  - ν_mono (CFG726's bracket kernel) is not run (CFG726: within 0.01 of ν_s everywhere);
  - the released-surplus transport clock Γ⁻¹ = (4πG ρ_c τ α_f)⁻¹ at r = 1.5 Mpc (law densities, median eRASS1 cluster), α_f 0.5 and 1;
  - median member r_J at pericentre and present; retained memory fraction.

### B: Bullet-type subcluster core (record inputs only)
- Sub label split: the CFG598 grid host log M_ta = 14 (CFG915 §4(c)'s sub analogue; point-mass baryons, inherited EPS history,
  flagged), P0, both footings, α_f 0.5 and 1.0, run with the reading's capture rule. φ_f = f share of the cold mass inside
  R_core = 200 kpc at t0 (CFG623's window scale; the record has no measured lensing core radius).
- r_J of the sub in the main's field: CFG599 `Progenitor599` main 1.5e15 M_⊙ (no cloud) and sub 1.5e14 M_⊙ (with its cool-core
  cloud), case L, total masses, footing a0 (record model, its ν_e).
- Mobile fraction: LR-x: φ_mob = φ_f (released t lies inside the main's overfilled, settled core and is re-latched at once; CFG915:
  log-15 cores M_c/M_ph(<200) 1.36–1.54). LR-c: φ_mob = φ_f + [t at r_J < r ≤ 200 kpc] / [cold mass inside 200 kpc].
- **Class (CFG915's mapping rules, per footing, at a G-passing α_f; if G passes at neither, both α_f are reported and the larger
  φ_mob is used):** CONSISTENT (first order) iff φ_mob ≤ φ_lin,H (CFG915: 0.0390 / 0.0411) at some G-passing α_f; CONTRADICTED iff
  φ_mob ≥ 0.9 at every G-passing α_f (maps onto CFG623's single-α nodes α ≥ 0.3, EXCLUDED on both footings; CFG915 §8's rule;
  disclosed: CFG623's α = 1 node is UNSCORABLE, not excluded); UNDERDETERMINED otherwise (CFG915 §9's merger run decides).
- **Pericentre (primary):** the record has no measured Bullet pericentre distance. CFG597 M-6 is head-on by declaration; the minimum
  sampled galaxy separation in CFG623's α = 0 run is reported only. So B(peri) is UNDERDETERMINED, unless φ_mob at zero release
  already meets a threshold: ≥ 0.9 gives CONTRADICTED at any pericentre, since release only adds mobile mass. Reported condition
  (a mapping over d, not a scan of a fitted knob): d* below which φ_mob ≥ 0.9.
- **Present (alternative):** d = 720 kpc (the record's BCG–BCG separation, CFG597 O-4) → computed class.

### D: satellite dwarfs and field dwarfs
- **D-sat, primary (pericentre):** the 12 MW satellites of CFG839, orbits recomputed by CFG839's method (LVD phase space, astropy
  default Galactocentric frame, turning points from E and L) in the law's MW field (ν_s, 6.0e10 M_⊙ point mass) per footing.
  **Alternative (present position):** CFG838's 24 MW + M31 satellites at their LVD host distance (M31 1.0e11 M_⊙).
  - Satellite m(<r) = Plummer stars (scale a = r_h from LVD; M_* = Υ_SFH L_V as CFG838/839) + its own law phantom (§2.4).
    r½ = (4/3) r_h (CFG838/839).
  - Exposed iff r_J < r½. Reference Δ = median Δ (CFG828 rows, ν_e, same footing) of the intact satellites in the same sample if ≥ 3
    are intact, else 0 (the law).
  - Per footing: CONSISTENT iff no exposed satellite has Δ above the reference; UNDERDETERMINED iff exactly one does; CONTRADICTED iff
    ≥ 2 do. With no exposed satellite, H-LR predicts no tidal modulation of any inner clump, which matches CFG838/839's NO SIGNAL.
    For any reading, cold energy outside r_J is unbound: it is released (H-LR) or stripped collisionlessly (release-none). So the
    exposure set is the same for both readings.
- **D-field:** field dwarfs (no host) have r_J = ∞ and keep their clumps. H-LR predicts satellites ≤ field (equality if no satellite
  is exposed), and a non-negative slope of Δ with host distance. Per footing, CONTRADICTED iff any of these lies ≤ −2 se (excess
  significantly higher in or near hosts):
  - CFG873 primary D (field − satellites at matched g_bar);
  - CFG874 primary c (isolated − satellites);
  - CFG875 primary k (Δ slope per dex of host distance).
  Otherwise CONSISTENT.
- **Carried from CFG915 and stated:** α_t = 0; route D-i, formation-epoch baryon loss with loss factor median ×4.3 (16–84%
  1.2–17.8) from CFG827's 28 out-of-sample dwarfs. **LR-c adds a history condition:** a dwarf's t must have been latched (exact
  settling, growth halted) before the loss, because capped capture never latches overfill f.
- **D class** = CONSISTENT (conditional on the above) iff D-sat and D-field are CONSISTENT; CONTRADICTED if either is; else UNDERDETERMINED.

## 4. Classes

Per reading (LR-x, LR-c): CONTRADICTED if any graded test is CONTRADICTED on either footing (every failing item listed); else
UNDERDETERMINED if any is UNDERDETERMINED; else CONSISTENT WITH ALL FOUR, with its posits and conditions listed. Overall H-LR =
best over the two readings (§2.1).

## 5. K identity tests (a failed K is reported FAIL and not loosened)

- **K-G-NONE:** LR-x with r_J = ∞ reproduces CFG915's cached LC MW runs (min q, max q, M_c/M_ph(<30), f share(<30), t share) at α_f
  0.5 and 1, both footings, to ≤ 1e-12 relative.
- **K-G-ALL:** release-all (r_J = 0) with exact capture reproduces CFG915's cached REF runs (= CFG598 MW P0) to ≤ 1e-12, and
  `cfg598_results.json` MW P0 (min q, max q, M_c/M_ph) to ≤ 1e-9. LR-c release-all reproduces REF to ≤ 1e-9.
- **K-H14:** LR-x log-14 host runs reproduce CFG915's cached φ_f(<200) and t share to ≤ 1e-12.
- **K-M-NONE:** release-none per-cluster ΔΣ equals CFG726's stored arrays (`erass.npy`, `accept.npy`: hmm|s|foot|primary) to
  ≤ 1e-10 relative; T-R/T-A A and Z_OUTER equal `cfg726_results.json` (Z to 0.001).
- **K-M-ALL:** release-all equals CFG726's stored law arrays (law|s|foot) to ≤ 1e-10 relative and its A_law.
- **K-M-W:** the truncated convolution with weight ≡ 1 equals CFG726's `convolve_members` to ≤ 1e-10 relative (code-path check).
- **K-ORB:** for the median eRASS1 cluster (canonical), a direct leapfrog orbit from one quadrature node reaches the solver's r_p to
  ≤ 1%; every node has r_p ≤ d.
- **K-SAT:** with CFG839's own settings (ν_e, 9.3603e-11, 6.0e10), the recomputed r_peri of its 12 satellites equal its JSON to
  ≤ 1e-6 relative.
- **K-R (record numbers used):**
  - CFG915 φ_lin,B/H 0.1346/0.1338, 0.0390/0.0411 (±1e-4), LC log-14 φ_f(<200) 0.864/0.882;
  - CFG726 T-R/T-A s primary Z_OUTER −3.63/−4.05, −4.83/−5.19 (±0.01), law eRASS1 A MID 1.91, OUTER 1.01 (±0.01);
  - CFG873 D −0.150 ± 0.097, CFG874 c −0.100 ± 0.091, CFG875 k −0.190 ± 0.150 (canonical; alt read from the same JSONs);
  - CFG827 loss factor median 4.3 (recomputed as in CFG915);
  - CFG838 class NO TIDAL SIGNAL, CFG839 class NO SIGNAL.

## 6. MUTATE (separate outputs `cfg916_MUTATE.out`, `cfg916_results_MUTATE.json`; exit 1 iff every required arm bites)

Two arms, each re-graded for both readings:
- **release-all** (r_J → 0):
  - G: all MW t released every step;
  - M: C_J = 0 (the plain law);
  - B: LR-c φ_mob = 1; LR-x φ_mob = φ_f (re-latched by the main);
  - D: every satellite's t released. LR-c: the released clump is overfill, never re-latched, so it drifts at α_f ≫ α_c and is lost;
    every satellite is exposed. LR-x: re-latched only where the MW is exactly settled with no deficit inside at the satellite's
    present radius. r_cap = the largest radius inside which every cell of the LR-x MW run is settled at t0 (per α_f, footing);
    satellites beyond r_cap are exposed, satellites inside are retained.
- **release-none** (r_J → ∞ = CFG915 LC):
  - G = CFG915 LC;
  - M = H-MM (CFG726 primary);
  - B: φ_mob = φ_f;
  - D-sat unchanged (stripping beyond r_J is collisionless anyway).

**Bite per arm and reading:** at least one test changes class on either footing, OR a score moves by a pre-declared margin:
|ΔZ_OUTER| ≥ 1.0 (M, either sample), |Δφ_mob| ≥ 0.05 (B), |Δ min q| ≥ 1e-3 (G).
**Required arms:** both arms for LR-c, and release-all for LR-x. LR-x release-none is expected to be an identity (§9). It is
reported as frozen, and its non-bite is a finding, not a failure.

## 7. Outputs, runs, disclosures

- Script `cfg916.py`. Three sequential single-core runs in the task's order:
  1. `CFG916_MODE=K`: computes and caches all runs (every arm's raw numbers come from these computations) and runs the K tests →
     `cfg916_K.out`;
  2. `CFG916_MUTATE=1` → the MUTATE files;
  3. the default main run → `cfg916.out`, `cfg916_results.json`.
  Caches stay in the lane dir (small JSON, scores and diagnostics only).
- **Read before writing this file (not blind):**
  - READMEs and criteria of CFG915 (and its code, JSONs and cache keys), CFG726 (and its code), CFG598 (and `cfg598_lib`), CFG838
    and CFG839 (code and JSON: per-satellite pericentres, log T, Δ; Sagittarius Δ +0.00 at log T_p +0.33), CFG913, CFG914, CFG827,
    CFG873, CFG874, CFG875, CFG623, CFG625;
  - CFG597/599 progenitor code and criteria;
  - THEORY_CANONICAL_2026-10-18 with all addenda and caveats;
  - the LEDGER rows 662–668;
  - CFG828/827 row structures.
- **Pre-freeze hand estimates** (disclosed, not verdict inputs):
  - Draco r_J ≈ 1.4 kpc vs r½ ≈ 0.3 kpc (intact); Sagittarius r_J ≈ 1.1 kpc vs r½ ≈ 3.5 kpc (exposed, Δ ≈ 0);
  - cluster members r_J ~ 20–60 kpc vs their halo edges 200–900 kpc (retained memory ~5–10%);
  - MW in M31's field r_J ~ 500 kpc.
- **Expectations:** LR-x M CONTRADICTED by identity; LR-c M likely CONSISTENT (static); LR-x B UNDERDETERMINED (φ_f 0.86–0.88);
  LR-c B unknown (the capped split may leave φ_f ≥ 0.9); LR-x G identical to LC if no t lies beyond r_J,MW; LR-c G unknown.

## 8. Heavy runs (specified, NOT run here; queue only after the 1024³ chain, ≥ 16 GB free, ≤ 4 processes)

- **(a) Finite-α_f release in clusters.** A 1-D two-population, two-sided (CFG638) drift of the released surplus around the host law,
  with members' retained halos as fixed t. One median cluster per eRASS1 mass tercile; α_f 0.5 and 1; both footings. Run from
  release at the first pericentre to t_obs, with the time since release taken from the same orbit model. Scored on OUTER as in §3 M.
  It replaces the static limit.
- **(b) CFG915 §9's two-population merger stopwatch** with the reading's label split, plus release at the sub's pericentre. It needs a
  non-head-on Bullet geometry taken from data.

## 9. Pre-freeze argument: why the release is inert under exact capture

CFG915 C1 rests on the argument that a remnant of settled pieces is overfilled by H-MM's sub-additive excess with no deficit inside it,
so LC latches that excess at once. The latching is by the remnant or host itself, whatever the pieces' labels, on the footing that
hosts are settled to their supply edge. Under the same footing:
- a member's released f lands in host cells that are settled (the host's own settled profile alone has q ≥ 1) and have no inner deficit;
- exact capture re-latches it in place, so the cluster's mass placement is unchanged (LR-x M ≡ H-MM);
- the same holds for a Bullet sub's released core inside the main's overfilled core (LR-x B ≡ LC);
- and for the MW, if no MW t lies beyond r_J,MW (LR-x G ≡ LC).
For release to remove memory, the host must not latch released surplus. That is LR-c.

## 10. Not claimed

That H-LR is derived; any measured α_f, r_J or pericentre beyond the record's; κ derived; "theory closed"; that the data favour the
framework. A CONSISTENT M under LR-c would hold only in the static, transport-unlimited limit and would leave the law's own eRASS1 MID
failure untouched.
