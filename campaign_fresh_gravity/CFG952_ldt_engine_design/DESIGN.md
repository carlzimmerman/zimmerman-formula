# CFG952 DESIGN: the labelled-domain-theory (LDT) change-set for the class-A PM engine

**Status.** A design, not an implementation.
- Nothing here edits or imports CFG650 / CFG654 code.
- The smoke tests behind it are in `cfg952_ldt_proto.py` (a separate 64³ toy); the results are in `README.md`.
- Every number below comes from that script's JSON outputs.
- κ = ½ FITTED. Footings never pooled. Not "theory closed".

## 0. What is changed, and which LDT

**Target.** The CFG654 engine (CFG650 modules M1 + M2 + M3, native_cmb inputs; the NC1x / NC2x configuration).

**How to implement it.** Copy the engine into a new lane with one master switch `LDT` (default off). With every LDT switch off,
the copy must reproduce the CFG654 engine bit for bit at 256³ (gate V-R, §5). The CFG650 / CFG654 files stay untouched.

**Formulation.** The brief and the class-A chassis point to formulation **(B)**: CFG947 N1, i.e. untethered geodesic dust plus a
conserved per-domain source. CFG950 declares the per-label tether **(A)** primary. §8 maps (A) onto the same machinery and says
why the smoke tests favour it for the engine.

## 1. Switches (all default off ⇒ CFG654 bit for bit)

| switch | values (primary first) | meaning |
|---|---|---|
| `LDT` | 0 / 1 | master |
| `LDT_LATCH` | `catch` / `theta` | label birth from the engine's resolved turnaround balls + M1 partition (toy-tested), or CFG950's θ-latch (needs the mesh velocity divergence) |
| `LDT_RDOM` | `mass` / `latched` / `node` | domain radius: from the label's current mass, r_ON = R_ta(M_ℓ, Δ_ta(a)) (continuous); latched at birth (the toy); or the engine's 14-node grid (jumps of 40% per node; not recommended) |
| `LDT_OWN` | `exact3d` / `hybrid` / `mask` | own-domain phantom: an isolated sub-box solve per label; spherical own-phantom for small labels and 3-D for large; or the global field minus each label's baryon-weighted mean external field |
| `LDT_SC` | `own` / `total` | cold compared with the phantom in the deficit: the label's own labelled cold, or the engine's s_c = (1 − f_b)(1 + δ) |
| `LDT_DRAW` | `e8` / `dipfree` / `dipslave` | per-label uniform draw (class A's M1 rule per label); dipole-free tilt; momentum-slaved tilt (§3 iii: infeasible under positivity in the toy) |
| `LDT_XH` | 1.0 / < 1 | edge factor on E7's supply root (1.0 = the engine; < 1 gives the draw headroom) |
| `LDT_MERGE_TRIG` | `tc` / `rd0` / `ov` | CFG951 T_c (r_dom ≤ r_½,b, equivalent to CFG947 M-R's bound fraction < ½); CFG950 (ii) whole-label tidal ball r_dom = 0; centroid overlap (the toy; fires on flybys, §3 iv) |
| `LDT_MERGE_MODE` | `blend` / `instant` / `persist` | CFG951 M2 (blend over one dynamical time); M1 (instant relabel); M3 (labels persist until tidal disruption) |
| `LDT_RMIN` | `r0` / `r2` | inherit the engine's RMIN; or subgrid point domains for peaks with dx ≤ r_ON < RMIN (§3 v) |

## 2. Data structures

**Per-particle label `lab` (int32).**
- Disk-backed, like the engine's `DField`: pread / pwrite by Lagrangian chunk, with F_NOCACHE. That is 4.29 GB on disk and 0 GB of
  RSS.
- Read once per labelled pass, sequentially (≈ 2–4 s per step).
- Added to `_ck_arrays` as a spilled file; checkpoint meta also stores the label table and the alias map.

**Label table LT** (numpy structured arrays, ≤ 1e5 rows, < 50 MB). Per row:
- id, alive, birth a, parents, alias;
- latched M_ta and f_ret class; r_ON, r_e;
- X (float64, periodic) and its reference;
- M_b,own, M_c,own;
- the last M_ph(< r_e), Σe, Σcomp, q, capped;
- β, Newton iterations and convergence flag, headroom;
- strays (labelled baryons outside the label's sub-box).

**Sector table.** D_t(3), P_s(3), A_s(3), plus the ramp (t_m, τ_m, A, B, C, w).

**Ragged sub-box buffers** for each batch of labels (≤ 1.5 GB per batch), float32:
- RB_b: retained-baryon weight FB · f_d (the M2 condensed fraction), as the engine's `deposit_cond`;
- RB_c: cold share (1 − FB).

**S_ℓ.** Spilled ragged storage of each label's source, for the F′ gathers.

**Kernel caches** per sub-box size class: one class per r_ON node, or binned sizes under `LDT_RDOM=mass`. The largest class,
r_ON = 8 Mpc/h, has n = 169 and padded P = 343. Its three vector kernels plus one potential kernel take ≈ 0.65 GB in complex64;
for that class only, compute them on the fly.

## 3. Ingredient → engine change (function names are the CFG654 engine's)

### (i) Label assignment with causal persistence

**Where.** In `forces()`, inside the census-refresh block (`refresh = ... _INC["calls"] % 10 == 0`), after
`peaks = cover_peaks(mesh, delta, D)`. Call `own_host_labels(mesh, peaks)` even when M1 is off.

```
def ldt_latch(mesh, P, hostD, hostC, hostR, D, a):              # once per census refresh (E11 cadence)
    counts = sparse {}                                           # (host h, effective label l) -> labelled mass
    for (i0, i1) in P.chunks:                                    # pass 1
        g  = NGP cells of P.positions(i0, i1)
        h  = _gather_window(mesh, hostD, g, i0)                  # M1 partition (smallest d / r_ON)
        l  = alias[lab.read(i0, i1)]
        counts += unique((h, l) for labelled particles with h >= 0)
    for each host h:
        cont[h] = argmax_l counts[h, l]  if max >= 1/2 of the labelled mass in h  else NEW
    for (i0, i1) in P.chunks:                                    # pass 2 (latch rule beta)
        un = (lab == 0) & (h >= 0)
        lab[un] = cont[h[un]], creating labels where cont == NEW: latch M_ta = M_ta(hostR[h], D), f_ret, birth a
    newborn: X = centroid of own baryons; sectors D_t = P_s = 0
```

- Labelled particles are never rewritten, except at a merge (alias, rewritten once at the end of the blend) and by an optional
  L2 re-latch.
- Domain radius under `LDT_RDOM=mass`: r_ON,ℓ(a) = (3 M_ℓ/(4π Δ_ta(a) Ω_m 2.775e11))^{1/3}, with M_ℓ the label's current particle
  mass (the inverse of the engine's `M_ta`). r_e,ℓ = XH · x_supply(r_ON,ℓ, Δ_ta(a), a, branch, foot) · r_ON,ℓ. Both are
  continuous between refreshes, so there are no 40% node jumps.
- The θ-latch alternative (CFG950 rule i) latches a particle when the physical divergence of the mesh velocity at its cell
  first becomes ≤ 0. It costs three extra momentum deposits per refresh.
- **Toy check (a0, a2): PASS.** The satellite and host get distinct labels at t = 0, and both keep purity 1.00000 through the
  infall to d = 5 (41 snapshots).

### (ii) Own-domain phantom (no EFE)

**Where.** It replaces the `f_mond` block of `forces()`: `deposit_cond` → `phb` → `gb_comp` ×3 → `ysq` (a full float32 field
in RAM) → `Dw` → `divk` → `s_ph`. A new routine fills the same `divk` buffer with the summed source, so `_finish_phik` (and
M3's `expel_m3`) run unchanged.

```
def ldt_source(mesh, P, Dd, Dfsw, a, branch, foot):
    for batch of labels (ragged bytes <= 1.5 GB):
        one labelled pass over P.chunks -> windowed bincount of FB*f_d (RB_b) and (1-FB) (RB_c) into each label's sub-box
        for each label l (thread pool; sizes bucketed):
            g_l  = FB * isolated solve of RB_b                   # zero-padded (Hockney) convolution, code units:
                                                                 #   lap phi = (1.5 Om / a) n,  so G = -(1.5 Om / a) / (4 pi r)
            s_ph = -div[ (nu_mono(|g_l| / (a a0_code)) - 1) g_l ]    # as the engine, own baryons only
            e    = f_sw * max(s_ph - cs * n_c,l, 0)  on |x - X_l| < r_e,l     # cs = 1.5 Om (1 - FB) / a; f_sw from Dfsw
            comp = draw on the shell r_e <= |x - X_l| < r_ON,l from the label's own cold (iii)
            S_l  = e - comp ; scatter-add S_l into divk's real view ; spill S_l (for F')
```

**Cost of the three schemes** (§4 for numbers):

| scheme | how | cost and accuracy |
|---|---|---|
| exact3d | 4 transforms of (2n)³ per label | it removes E4's 11 full-box transform-equivalents and adds Σ_ℓ of small transforms; at N_L ≤ 5000 it is net cheaper than `mask` |
| hybrid | spherical own phantom from radially binned RB_b for labels with r_ON below a declared node; 3-D above | cheapest at large N_L; error = the non-spherical part of small labels |
| mask | keeps E4's global solve and subtracts each label's baryon-weighted mean g (uniform external field) on its cells | it needs an extra interpolation pass of g to the labelled baryons; tidal residual |

**Toy check (a1): PASS by construction**, and no leakage: the satellite's own phantom with every particle present equals the
label-only computation exactly (0.0 at all three snapshots).

**The engine's E4 (Mu1) carries a real EFE in the PM:**

| d | 12.0 | 7.97 | 5.01 |
|---|---|---|---|
| E4 EFE (dex) | −0.009 | −0.025 | −0.114 |
| MASK residual (dex) | −0.003 | −0.001 | −0.014 |

So `mask` is a usable approximation, within CFG945's δ_c = 0.082 dex in this toy.

**Discretisation.** The sub-box phantom differs from the periodic spectral one by −0.03 to −0.05 dex when the edge radius is 2.6
cells. At 1024³ the smallest labels have edges of a few cells, so this systematic needs measuring (V-LDT).

### (iii) Dipole-preserving draw (fixing CFG947's T-M), and why it fails as specified

**Rule tested.** For the positive exponential tilt, comp = ρ_c min(1, e^{λ + β·d}) is solved by Newton on the convex dual
(per-label λ, per-sector β). The sector's realised source dipole is enforced to a target D_t. D_t and P_s are integrated on the
particles' leapfrog with D̈_t = A_s = Σ_cells S_ℓ g_tot dV.

**Engine hooks.**
- In `accel_pass`, after each component's real-space g_c, gather it at each label's sub-box cells and accumulate
  A_s += Σ S_ℓ g_c dV.
- With the same `quad` kick coefficients as `P.kick`: P_s += A_s · cc.
- In `P.drift`'s coefficient: D_t += P_s · d.
- Book: Σ P.mom (float64 per chunk) + Σ P_s, against the realised dipoles.

**Toy result.**
- **(a) Gentle infall.** The book closes (B/I 2.85e-9).
- **(b) Asymmetric host** (cold offset 1.5, edge 3.4, catchment 9.6). The slaved target becomes infeasible at t = 2.56: no
  positive draw ≤ ρ_c can realise it. Over the run B/I = 81 (frozen), or 6.5 with the post-hoc zero-sum-exact fallback.
- **(c) Major merger.** B/I = 71 (frozen) / 2.3 (post hoc).

The paper estimate (A1.4, README) explains it. The slaved dipole oscillates about an equilibrium of order Σe · R · g_c/g(R). That
needs a draw displacement of about 2 Σe · R, while the shell can supply at most about Σe · R once g_c ~ g(R).

**Design consequence.** In formulation (B), momentum conservation through the 𝒮 dipole is capacity-limited by positivity of
the active cold mass. The options:
- **O1. A labelled class-A step.** Use the per-label `e8` draw (or `dipfree`) and report the momentum non-closure as a
  diagnostic. The engine already violates momentum at this level (CFG947 T-M; toy E8 B/I 0.82). This tests only the EFE fix
  plus labels.
- **O2.** A larger supply region (draw beyond r_ON: CFG748 / 801's infall catchment N ≥ 3–4).
- **O3. Formulation (A)** (CFG950 primary). The phantom is the medium's own mass moving under internal forces, so momentum holds
  by construction (§8).
- **O4.** Allow negative active cold. **Rejected** (d3 positivity).

Do not launch a (B) 1024³ run with `dipslave`.

### (iv) Merge rule

**Trigger.** One of `tc` (CFG951 T_c ≡ CFG947 M-R written with L2), `rd0` (CFG950 ii) or `ov` (toy).

**Transition `blend`** (CFG951 M2): S = (1 − w)(S_A + S_B) + w S_C over τ_m = r_e,C/(G M_b,C a₀)^{1/4}. During the blend:
- three sub-box solves (A, B and C = A ∪ B through the alias, without rewriting `lab`);
- one β common to the three draws (if a tilt is used);
- D_t,C = D_t,A + D_t,B, and likewise for P_s.

At the end of the blend, one pass rewrites `lab` from A, B to C.

**Toy results.**
- **The blend keeps the source continuous at the trigger.** J_Φ there is 0.025 under RAMP, against 2.77 under INSTANT (a 110×
  jump).
- **Its peak per-step J during the blend is 0.053**, which is (π/2) × J_instant/N_steps plus motion. That exceeds the frozen 0.03
  line, so c1 FAILS as frozen. The NONE run (no merge) reaches 0.053 from motion alone.
- **CFG947's M-R (MR1, bound fraction < ½) never fires in an equal-mass merger.** Bound fractions are 0.998 / 0.999 at first
  passage and 0.98 at t = 30. So equal-mass mergers need T_c / r_dom or a pair-boundness trigger.
- **A pure overlap trigger is unsafe.** It fired at first passage. Without merging, the same pair separates (end separation 16.7);
  with the merge it stays bound (1.3 / 0.6). The merge rule itself changes the orbit, so a trigger must not fire on an unbound
  passage: test the pair energy, or wait for coalescence (T_c).
- **Without merging**, the two labels' phantoms over-count the union by ×1.35 inside r_e,C (T-L; Mu5).

### (v) RMIN

**Finding.** The engine's r_ON takes only the values geomspace(dx, 8, 14).
- At 1024³ (L = 100) the first node ≥ RMIN = 0.78125 is **1.0471 Mpc/h**, so the effective threshold is M_ta ≥ 4.97e12 M⊙/h, i.e.
  **M_b,ret ≥ 2.19e11 M⊙**.
  - This is 4.5× CFG947's continuous 4.82e10, which is reproduced as a control.
  - With native_cmb inputs it is 2.13e11.
- At 256³ the node is 0.7841 (4.79e10). The 256³ validation therefore does not reproduce the 1024³ threshold.

**Options.**
- **`r0`.** Keep it, for comparability with NC1x / NC2x. The run then tests the law only for M_b,ret ≳ 2e11 M⊙.
- **`r2` subgrid.** Every peak with dx ≤ r_ON < RMIN becomes a latched point-domain label. Its own phantom is the spherical
  profile from its labelled baryons (the `hybrid` machinery), with the edge from E7 and the draw on its own cold. Its sources sit
  within a few cells, i.e. at k ≳ 2π/r_ON ≳ 6 h/Mpc, next to the scorer's support limit πN/(4L) ≈ 8 h/Mpc. Their effect on the
  shear statistic must be measured at 256³ (V-RMIN) before choosing.

Systems below one cell are not peaks at all. The box cannot test them.

### (vi) Untethered cold

No change. The engine's particles are geodesic, self-gravitating dust (baryons and cold in fixed proportion). LDT changes only
the active source. The S0 control is the same particles with S ≡ 0, so NCS0 (native_cmb, seed 359) serves unchanged: S0 reads
neither the footing nor the source.

### (vii) Diagnostics to write

**Per census refresh** (npz): the LT snapshot (id, alive, X, r_ON, r_e, M_b,own, M_c,own, M_ph(< r_e), Σe, Σcomp, q, capped, β,
Newton status, headroom, D_t, P_s, A_s, strays), and label counts by mass.

**Per step:**
- P_m (3, float64), ΣP_s, Σ realised dipoles;
- the max per-label zero-sum residual; the max dipole miss;
- the counts of labels, capped labels and infeasible solves;
- J_Φ of the source;
- the summed own-phantom mass.

**Merger log.** Step, a, A, B → C, trigger metric, separation, τ_m, MR1 bound fractions, J_Φ at the trigger, phantom before and
after.

**Memory and timing by stage**, as the engine's MEMST, plus the physical footprint.

## 4. Memory and runtime at 1024³ (EST stage; estimates, not results)

**Baseline (NC1x run JSON).**
- 16.27 h of compute: per step, deposit 105 s, forces 193 s, accel 63 s.
- Peak RSS 44.33 GB (getrusage; the watcher's ps peak was 42.4 GB).
- Host peaks: 32 399 / 56 162 / 63 140 at z = 0 / 0.5 / 1.

**Model.**
- One particle pass t_pass = 105 s. One full 1024³ transform t_FFT ≈ 2 s, bracket 1.5–3 s. Small transforms are taken as 2×
  less efficient.
- The smallest label's sub-box (node 1.047) has n = 27 and P = 54.
- The labelled ragged deposit replaces `deposit_cond`: +0.3 pass, plus one pass per extra 1.5 GB batch.
- Label refresh +0.1 pass per step; F′ gathers +0.05 pass per step.

| N_L (alive labels) | scheme | ragged (GB) | Δ per step (s, t_FFT lo/mid/hi) | wall per run (h) |
|---|---|---|---|---|
| 1 000 | exact3d | 0.16 | +32 / +27 / +16 | 17.0–17.6 |
| 5 000 | exact3d | 0.79 | +36 / +32 / +24 | 17.3–17.8 |
| 5 000 | hybrid | 0.79 | +31 / +26 / +15 | 16.9–17.6 |
| 20 000 | exact3d | 3.15 (3 batches) | +261 / +262 / +265 | 27.2–27.3 |
| 63 140 (every peak a label: no latching benefit) | exact3d | 9.94 (7 batches) | +725 / +741 / +772 | 46.5–48.5 |
| any | mask | — | +47 | 18.2 |

**Memory.** With labels on disk, the peak RSS is 42.8–47.1 GB. The low end assumes `f_mond` was the peak stage, since E4's
in-RAM `ysq` (4.3 GB) goes. The high end assumes the census refresh stage was the peak and adds batch and solve buffers
(≈ 2.8 GB). With labels in RAM the worst case is 51.4 GB, against the frozen 52 GB abort line: **rejected**.

**Recommended scheme.**
- Labels on disk; `exact3d` (or `hybrid` if N_L > 5000); ragged batches ≤ 1.5 GB.
- Peak ≤ 47 GB, so the frozen start rule (free + inactive ≥ 48 GB) and abort rule (52 GB) are kept.
- About 17–18 h per footing if N_L ≲ 5000. The label count is the dominant unknown: count it at 256³ (V-LDT) and log it from the
  first 1024³ refresh. An abort rule on ragged batches > 3 is advised.

**Disk.**
- +4.3 GB labels file;
- +4.3 GB per checkpoint copy (two copies transiently);
- ≤ 1–10 GB S_ℓ spill.

So raise the disk start rule from 18 GB to ≥ 30 GB.

## 5. Validation ladder before any 1024³ (each one process, nice 10)

| gate | size | what |
|---|---|---|
| V-R | 256³, LDT off | the copy equals the CFG654 engine bit for bit (CFG654 V-R form) |
| V-LDT | 256³, LDT on | books, zero-sum ≤ 1e-10, dipole miss, label count and size distribution, strays, own-vs-E4 discretisation, timing and RSS scaling; the 64³ smoke tests rerun through the engine path |
| V-RMIN | 256³ | `r0` vs `r2` on P_grav at k ≤ 8 h/Mpc (note the 256³ effective RMIN differs, §3 v) |
| V-MEM | 1024³, MAXSTEPS = 3 | memory probe; this is itself a heavy job and needs the owner's approval |

## 6. What the 64³ toy established (README for every number)

- **Established.**
  - Labels from the catchment machinery persist through infall (a0, a2).
  - The own-domain phantom has no EFE while the engine's global E4 carries −0.11 dex (a1, Mu1).
  - A blended merge removes the 110× instant jump at the trigger.
  - The PM is momentum-exact without a source (K1).
- **Not established.**
  - A momentum-conserving positive draw in asymmetric domains or mergers (b1, c2): capacity-limited.
  - Per-step continuity ≤ 0.03 during a one-dynamical-time blend (c1: 0.053).

## 7. CFG950 / CFG951 candidates (their criteria are frozen; their results were not available)

| lane | candidate | engine switch |
|---|---|---|
| CFG951 | merge variants M1 / M2 / M3 | `instant` / `blend` / `persist` |
| CFG951 | coalescence trigger T_c | `tc` |
| CFG950 | rule (ii) whole-label tidal ball | `rd0` |
| CFG950 | rule (i) θ-latch | `theta` |
| CFG950 | rule (iv) L2 one-way re-latch | an optional pass at refresh: a labelled particle outside its label's ball moves to the largest-mass label whose ball contains it |

## 8. Formulation (A) (CFG950 primary) on the same machinery

The same labels, sub-boxes and isolated solves serve. What changes is what each per-label solve produces:
- **The source is the label's medium itself.** Labelled cold particles carry the phantom as their own mass. The engine's
  deficit / draw relocation disappears; the medium moves under its own forces.
- **Forces.**
  - On labelled cold particles: the tether force from the label's χ_ℓ, a nonlinear (QUMOND-type) per-label solve from the
    label's own medium mass, with D-T removing within-label self-gravity.
  - On baryons, other labels and unlabelled dust: ordinary Newtonian gravity of every mass.
- **New per-step costs.**
  - One nonlinear per-label solve (iterated, say 3–5 sub-box solves).
  - A per-label force interpolation onto that label's particles.
  - CFG950's internal viscosity (rule iii), e.g. a Galilean-invariant velocity-relaxation term on labelled particles within a
    label, which needs a per-label mesh velocity.
- **Momentum.** Conserved by construction (internal forces and translation-invariant dissipation), which removes §3 (iii)'s
  capacity problem.
- **Memory.** As (B), plus one ragged velocity buffer per batch.

This is the design to build if CFG950's (A) holds. A 1024³ shear test of (B) with `e8` (O1) tests only the EFE fix plus labels.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
