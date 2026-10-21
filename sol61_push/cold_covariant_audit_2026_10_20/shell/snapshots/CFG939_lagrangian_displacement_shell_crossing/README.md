# CFG939: P as the exact Lagrangian displacement of a collisionless medium. Does shell crossing derive S4? No.

**Bottom line.** The record's identity ∇·P = ρ − ρ̄ is not a linear approximation. With P = −∫ j dt (S3's total current) it holds
exactly through shell crossing, and P stays single-valued. In 1-D and spherical symmetry the S2 + S3 force on every element of cold
energy is the same before and after crossing: −∇Φ_b + R(K|P|)P̂ − γ∇ρ_c. After crossing, the tether anchors to the element's mass
rank instead of its birth position.

So the multi-stream regime is **tethered**. The record's own settled law state is reached by collisionless phase mixing (CFG747/748
and N3 here: 100% crossed, on the law at 2 r_M). S4's free population (bound by ordinary gravity, never re-tethered) is not a regime
of the single medium. It needs a coupling switch the action does not contain: matter that gravitates but sits outside ∇·P (CFG888's
unwritten coupling).

H-SC's mapping (tethered = single stream, free = multi-stream) also **MISALIGNS** with the data:
- every collapsed class has crossed inside r½, rotators included;
- large L* would make the smallest systems single-stream, which inverts the excess pattern.

**Classes**
- **S4: unassigned by the frozen rules at the primary run (C1 borderline); never DERIVED; NOT DERIVABLE on the analytic test C3 and
  on C1 in 4 of 5 runs.**
  - The C1 gate needs m/m_law within ±0.05 at 5 r_M. The primary run gives 0.949, which misses by 0.001. The first run gave 0.966.
    The A2 report-only runs give 0.958 and 0.956, and 0.994 at t = 6000.
  - The shortfall is a still-filling deficit, opposite in sign to the 3.9 × pile-up of the tether-off control.
  - C2(a) (crossing ⇒ positive binding) is 0.43–0.52 against a 0.9 bar in every run.
- **Alignment (H-SC): MISALIGNS** in all 16 cells (2 footings × L* 24/100/300/1000 pc × v_rel 100/50 km/s), 2–4 of 7 classes right.
  The derived reading (multi-stream matter tethered) also MISALIGNS: 3–4 of 7 right. Rotators and below-law systems come out right;
  UFDs, dSphs and cluster cores come out on the law instead of in excess.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Framework-native inputs only. Not "theory closed". Nothing
here says the data favour the framework.

## What is derived (equations; details in DERIVATION.md)

| # | result | where |
|---|---|---|
| 1 | **P = −ρ̄Ψ** to first order (∇·Ψ = −δ). Exact in 1-D single stream: P(x(q)) = ρ̄(q − x(q)). Spherical: P_r = ρ̄(q³ − r³)/(3r²) = −ρ̄Ψ + ρ̄Ψ²/r − ρ̄Ψ³/(3r²) | K1, K1b (sympy) |
| 2 | Multi-stream 1-D: P = −ρ̄ Σ_s sign(J_s) Ψ_s, with ∂ₓP = ρ̄Σ1/\|J_s\| − ρ̄ (error 9e-16 / 1.5e-9) | K1c |
| 3 | Lagrangian action (1-D): ℒ = ½ρ̄Ψ̇² − ρ̄Φ_b(q+Ψ) − J·W_rem(Kρ̄\|Ψ\|) − (γρ̄²/2)(J−1)²/J. Kinetic term FORCED ⇒ inertia I = 1/ρ̄ for P; velocity dispersion is invisible to P | K2 |
| 4 | Single-stream invariant E_q = ½ṙ² + Φ_b + √(G m_q a0)[artanh√(u/a0) − √(u/a0)], conserved to 9e-9 ⇒ positive binding needs crossing, a changing Φ_b, or stiffness work | K6, K8 |
| 5 | **Sudden baryon loss unbinds a medium at rest on the law iff f > f_crit(x) = 1 − (1−x)(artanh√x − √x)/x^(3/2)**, x = u/a0; f_crit = 2/3 in the deep regime (0.673–0.691 at dwarf r½, 0.774 for MW-like) | K8c–e, N4, M4 |
| 6 | Flat frozen potential of the law state: μ = −(2/3)GM_b/R_e (deep, edge R_e; numerically −0.01339 vs −0.01333) ⇒ cold energy moving faster than √(4GM_b/3R_e) is unbound (CFG749, derived) | A1, K8h |
| 7 | Stiffness: (γρ̄²/2)(1−J)²/J is a barrier at J → 0. The cold fluid (p = πG L*²ρ_c²) breaks by a gradient catastrophe at finite density instead (N2), and S2 does not define what follows. Newtonian control λ_J = √2πL*. Crossing is suppressed inside **r_sub = L*²/(4 r_M)** (M² = 4 r_M r/L*², deep, point mass) | D1, N2 |
| 8 | W_rem promotes crossing: elements are independent anharmonic oscillators (no self-gravity, no linear restoring force), so they dephase and cross in 1.64 periods in N1. Literal a0 → 0 does NOT give Newtonian collapse (J − 1 = O(a0)) | N1, M2, M3 |
| 9 | No capture iff the system moves through the settled medium faster than its own baryonic escape speed (TDGs 21–53 km/s, DF2/DF4 22–23 km/s vs v_rel ≥ 100 km/s) ⇒ Newtonian | N5 |

## Consequences per class (canonical; alt within a few %)

T_c is the cold medium's radial period at r½ in the S2 + S3 dynamics (ω² = 4πGρ_b + (2g_N/r)a0/(a0 − u)). Mach is the baryonic
escape speed over the stiffness sound speed.

| class (record row) | r½ (kpc) | T_c (Gyr) | age/T_c | Mach @ L* 24 pc / 1 kpc | H-SC side (24 pc / 1 kpc) | derived side | observed |
|---|---|---|---|---|---|---|---|
| UFD-c / UFD-e | 0.039 / 0.31 | 0.26 / 2.4 | 51 / 5.4 | 0.74, 3.3 / 0.02, 0.08 | MIXED / ON LAW | ON LAW | EXCESS |
| Draco / Fornax-like | 0.29 / 0.93 | 0.51 / 0.31 | 24 / 38 | 6.3, 35 / 0.15, 0.84 | EXCESS / ON LAW | ON LAW | EXCESS |
| SPARC dwarf | 5.0 | 1.14 | 8.8 | 149 / 3.6 | EXCESS / EXCESS | ON LAW | ON LAW |
| MW-like | 8.0 | 0.16 | 64 | 724 / 17 | EXCESS / EXCESS | ON LAW | ON LAW |
| cluster core | 500 | 2.7 | 2.3 | 4e4 / 1e3 | EXCESS / EXCESS | ON LAW | EXCESS |
| tidal dwarfs (6) | 2.6–7.7 | 0.48–1.46 | 0.4–1.1 | medium absent | BELOW | BELOW | BELOW |
| DF2 / DF4 | 2.6 / 2.1 | 0.67 / 0.56 | 13 / 16 | medium absent | BELOW | BELOW | BELOW |

**Reading.**
- Shell crossing has happened inside r½ in every collapsed class: 2–64 cold periods per age.
- Only the stiffness can stop it. It does so in the *faintest* systems (r_sub ∝ L*²/r_M), which is backwards for H-SC.
- The record's sudden-loss route for UFDs (×4.3 baryon loss, f = 0.77 > f_crit ≈ 0.67) unbinds the tethered medium. In S2 + S3 that
  medium then leaves, which gives a deficit, not the +0.33 dex excess.

## Energy (T4)

The map dynamics conserves energy:
- law control: dE/E 1.3e-15;
- cold infall with full crossing: 1.3e-4 (1.7e-5 at the finest step).

Settling runs by phase mixing plus ejection: 44% of the infall mass (21.4 of 48.9 M_b) leaves on unbound orbits, carrying kinetic
energy 0.54 against 0.20 in the bound part (units M_b V_f²). So CFG932 Q1's non-conservation belongs to the class-A drift law
(CFG638), not to S2 + S3. The conservative channel supplies an explicit escaping receiver, which is astra's continuation 2 in
MASS_LEDGER_REPAIR.md. Like CFG776, it settles by expelling cold energy and never holds a surplus, so the excess family stays
unexplained.

## Checks

- **sym (`cfg939_sym.py`): 30/30 PASS** (K1 linear limit + sign tooth, K1b exact 1-D and spherical forms, K2 Euler–Lagrange ↔ S2
  force, stiffness, tether-off ⇒ Newton, I = 1/ρ̄, D1 λ_J, K8 closed forms).
- **main (`cfg939.py`): K 11/11 PASS**:
  - K1c multi-stream identity;
  - K3 Zel'dovich 1.87390 vs 1.87382;
  - K4 NGC 3198 law to 3e-16 on both footings (INFO: V_pred/V_obs at 44 kpc 159/149 and 166/149 km/s);
  - K5a law control (force 4.7e-13);
  - K5b–d energy with crossings 1.3e-4 / 1.8e-4 / 6.0e-5;
  - K6 9e-9;
  - K7 CFG747 force identity 1.1e-13;
  - A1 force identity 7.8e-13 a0.
- **MUTATE: all bite (exit 1 by design).**
  - M1 γ → 0: with stiffness, no J → 0 up to the gradient catastrophe at t 1.79 (J ≥ 0.70, where γ = 0 has J = 0.073); γ = 0
    crosses at 1.87385 vs 1.87382.
  - M2 tether off: Newtonian crossing at the K3 time; with the tether it crosses at 17.7.
  - M3 literal a0 → 0 (report only): no crossing by t = 2000 (1 − J_min = 1.1e-4) vs Newtonian 15.7.
  - M4: f = 0.617 / 0.717 flips deep shells 0% → 100% unbound.
  - M5: the grader returns ALIGNS for the hand-made "pressure-supported + medium present" rule.

## Disclosures

- **A1 (7dace0a16, pre-result).** The flat-potential identity makes the frozen E_tf a test-particle quantity, so C2 is printed with
  three definitions. The frozen NOT DERIVABLE proxy clause is ILL-POSED: 97.7% of the ever-E_tf>0 mass stays in the box while
  tethered. It was replaced by C3 plus a force identity.
- **A2 (92e2f0627, post hoc).**
  - First main run (dt 0.005): K5c failed (control dE/E 1.04e-3) and C1 printed TETHERED. Kept as `cfg939_firstrun_dt0005.*`.
  - Second run (dt 0.00125): K5c failed again, and C1 printed UNTETHERED by 0.001. Kept as `cfg939_secondrun_dt00125.*`.
  - Diagnosis: a random walk from ~3e5 reflections at r_min in the Newtonian control. Fix: the control runs at dt/4. The final run
    passes every K and its C1 numbers are unchanged.
  - Three report-only runs (`cfg939_A2.*`) show C1 is step-sensitive at t = 2000 and that 5 r_M fills to 0.994 by t = 6000.
- **Scratch debugging runs (not committed):**
  - a resolution study of the gradient catastrophe, t_b = 1.822 / 1.794 / 1.782 / 1.773 at N = 256–2048 (the main script repeats
    the 512 vs 2048 check);
  - a dt study of the energy errors.
- The N2 γ = 0 tether run at λ = 2 trips the grid-jump detector at J_min 0.024, which is the onset of crossing. The detector has no
  meaning without pressure.
- The N3 header prints a literal "dt {DT_SPH}" (an f-string slip). The step used is 0.00125 for the tether run and 0.0003125 for the
  control.
- The MUTATE outputs were produced before the A2 patch. The patch touches only the main-run control and the A2 mode, not the MUTATE
  paths.
- Ages in N5 are declared nominal values. The class needs only age ≥ T_c, which holds for every collapsed row by a factor of 2–64.
- Open (not tested): the 3-D transverse part P_T. Static S2 demands one, while S3 makes it history-dependent.

## Files and commands (one core, < 100 MB, nothing downloaded, no other lane touched)

- `FROZEN_CRITERIA.md` (3524438b2), `AMENDMENT_A1_pre_result.md` (7dace0a16), `AMENDMENT_A2_post_hoc.md` (92e2f0627), `DERIVATION.md`.
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg939_sym.py` → `cfg939_sym.out`, `cfg939_sym_results.json` (exit 0).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg939.py` → `cfg939.out`, `cfg939_results.json` (exit 0; about 8.5 min).
- `CFG939_MUTATE=<tetheroff|gamma0|a0zero|losstooth|gradetooth> ... python3 cfg939.py` → `cfg939_MUTATE_<name>.out/.json` (exit 1).
- `CFG939_A2=1 ... python3 cfg939.py` → `cfg939_A2.out`, `cfg939_results_A2.json` (report only).

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
