# CFG939 FROZEN CRITERIA: P as the exact Lagrangian displacement of a collisionless medium; shell crossing as the untether criterion?

Committed alone, before any derivation file, script or number of this lane. 2026-10-20. Block CFG930–939 (reserved in the LEDGER
row for 930–939: "CFG939 P as the exact Lagrangian displacement of a collisionless medium (multi-stream; shell crossing as the
untether criterion S4, derived not posited)"). Agent lane. κ = ½ FITTED. Footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt)
m/s², never pooled. Framework-native inputs only; no ΛCDM template enters any verdict.

## 0. The question and the hypothesis under test

The canonical statement (THEORY_CANONICAL_2026-10-14.md S2–S4; L* window [24 pc, ≳ 1 kpc] from CFG820 as carried in the 10-16/10-18
revisions) has
- S2: L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|², K = 4πG, u = K|P|, K W_rem′(u) = u²/(a0 − u), γ = K L*²/2 = 2πG L*²;
- S3: cold energy is a collisionless rest-mass medium whose displacement is P, ∇·P = ρ − ρ̄, ∂ₜP = −j;
- S4 (postulate): cold energy whose tether-frame binding becomes positive is permanently free, stays as collisionless mass bound by
  ordinary gravity, never re-tethers.

**H-SC.** ∇·P = ρ − ρ̄ is only the linear, single-stream form of the medium's kinematics. Tethered cold energy = the single-stream
regime of the Lagrangian map x(q, t) = q + Ψ(q, t); free cold energy (S4) = the multi-stream regime after shell crossing
(det ∂x/∂q → 0). If so, S4's untether criterion should be derivable.

## 1. Tasks and what each must produce

**T1. Exact Lagrangian form.**
- Write the S2 + S3 action in Lagrangian coordinates for a collisionless medium (kinetic term ½ρ̄|∂ₜx|² per unit Lagrangian volume),
  with the Jacobian density ρ = ρ̄ Σ_streams 1/|det ∂x/∂q| and the W_rem and stiffness terms in Lagrangian form, exactly where the
  geometry allows it (1-D plane and spherical symmetry, where P is fixed by the instantaneous map) and with the 3-D transverse
  part stated as open if it is not fixed.
- Resolve the sign: is P = −ρ̄Ψ at first order (given ∇·Ψ = −δ at first order)?
- State whether ∇·P = ρ − ρ̄ is linear-only or exact (with P = −∫ j dt, total current), and what happens to P after shell crossing.
- Derive the equations of motion; state what is FORCED by the identification and what is CHOSEN.

**T2. Shell crossing.** Derive the condition det(∂x/∂q) = 0 for 1-D and spherical collapse under (a) the Newtonian control (tether
off, γ = 0), (b) the S2 + S3 dynamics with the canonical tether, γ = 0, (c) with stiffness γ > 0. Give a stiffness criterion
(whether it delays/prevents crossing, and below which scale). Compare with S4's "tether-frame binding becomes positive" and with
CFG782's photo-evaporation selector (V_init < √2 c_s; DEAD as a selector, CFG782).

**T3. Consequences.** For UFDs, classical dSphs, SPARC rotators, MW-like galaxies, cluster cores, tidal dwarfs, NGC 1052-DF2/DF4,
at the order of magnitude the record supports and with the record's own numbers: is the cold medium multi-stream inside r½?
Grade H-SC's mapping against the record's observed sides (§4).

**T4. Energy bookkeeping.** Is the Lagrangian-map dynamics energy-conserving? Relate to CFG932 Q1 (the record's class-A settling is
non-conserving). Read sol61_push/cold_completion_2026_10_20/ (read only; do not duplicate it).

## 2. Inputs (read only)

- THEORY_CANONICAL_2026-10-14.md S2–S4; THEORY_CANONICAL_2026-10-16.md / -10-18.md (S4 revisions, open list).
- CFG747 (radial-shell tether dynamics, `cfg747.py` force formula), CFG748, CFG749 (cold energy bound only by baryons), CFG776
  (surplus expelled), CFG782 (selector, DEAD), CFG888 (self-gravity cancellation; law source = baryons only), CFG932 (Q1; its
  representative systems in `cfg932.py` `systems()`), CFG936 (TDG table `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`),
  CFG933 (DF2/DF4: M* 2.0e8 / 1.5e8 M☉, R_e 2.0 / 1.6 kpc).
- SPARC NGC 3198 (`real_research/data/sparc_data/NGC3198_rotmod.dat`), V_bar² = V_gas|V_gas| + 0.5 V_disk|V_disk| + 0.7 V_bul|V_bul|
  (the record's convention, e.g. CFG881); spherical M_b(<R) = V_bar² R/G (the record's convention).
- sol61_push/cold_completion_2026_10_20/ (astra's GRAVITY_ACTION_AUDIT.md, MASS_LEDGER_REPAIR.md, LATEST_ADDENDUM.md): read only,
  cited, not duplicated.
- Record baryon-loss factor for dwarfs: median ×4.3 (CFG915/CFG920) — used only in the T3 sudden-loss column.

## 3. Checks (K) — all must PASS before any class is read

- **K1 (sympy, linear limit).** With x = q + Ψ (3-D, generic functions), ρ = ρ̄/det(I + ∂Ψ/∂q): δ = −∇·Ψ + O(Ψ²); with P = −ρ̄Ψ:
  ∇·P − (ρ − ρ̄) = O(Ψ²) and ∂ₜP + j = O(Ψ²). Symbolic zero required.
- **K1b (sympy, exact single-stream).** 1-D: P(x(q)) = ρ̄(q − x(q)) satisfies ∂ₓP = ρ − ρ̄ and ∂ₜP|ₓ = −ρv exactly. Spherical:
  P_r = ρ̄(q³ − r³)/(3r²) satisfies Gauss and continuity exactly; its series in Ψ = r − q starts −ρ̄Ψ. Symbolic zero required.
- **K1c (numeric, multi-stream 1-D).** For a folded 1-D map, P_E(x) = (cumulative mass) − ρ̄x equals −ρ̄ Σ_s sign(J_s) Ψ_s(x) and
  ∂ₓP_E = ρ − ρ̄ with ρ = ρ̄ Σ 1/|J_s|; relative agreement ≤ 1e-6 on a grid away from caustics.
- **K2 (sympy).** The Euler–Lagrange equation of the 1-D Lagrangian action equals the Eulerian force −Φ_b′ + R(K|P|) sgn P − γ∂ₓρ
  (single stream), including the stiffness identity and the tether-off limit (W_rem → −u²/2K gives Newtonian self-gravity).
- **K3 (Zel'dovich, Newtonian control).** 1-D static background, tether off, γ = 0, no baryons, from rest with Ψ₀ = −(A/k) sin kq:
  t_sc = arccosh(1/A)/√(Kρ̄). The sheet code's first crossing time must agree within 0.5%.
- **K4 (record galaxy).** NGC 3198: the static single-stream solution of the Lagrangian force balance (shells at rest) reproduces
  g = ν_s(g_N/a0) g_N, ν_s(y) = ½ + √(¼ + 1/y), at every rotmod radius to ≤ 1e-10 relative, both footings. V_pred vs V_obs is INFO.
- **K5 (energy).** Spherical shell code: law control at rest |ΔE/E| ≤ 1e-10 and |force| ≤ 1e-10 g_N; runs with crossings |ΔE/E| ≤ 1e-3.
- **K6 (single-stream energy theorem).** In a spherical run before its first crossing, every shell's E_q = ½ṙ² + Φ_b + Π_q (own
  enclosed mass) is conserved to ≤ 1e-6 relative (max over shells).
- **K7 (record identity).** With the deep cubic kernel, this lane's discrete tether force equals CFG747's
  (m_out³ − m_in³)/(3 dm r⁴) to ≤ 1e-12 on a random configuration (formula re-implemented from its source, read only).
- **K8 (closed forms).** The tether potential Π(r) = ∫_r^∞ R(Gm/r′²) dr′ and any closed-form unbinding threshold agree with direct
  quadrature / root finding to ≤ 1e-8.

## 4. Classes (frozen rules)

**S4 class** (from the exact S2 + S3 dynamics as written, ∂ₜP = −j with j the TOTAL current):
- C1 (spherical cold infall, N3): **TETHERED AFTER CROSSING** if ≥ 90% of the mass inside 5 r_M has crossed by the end and the
  time-averaged m/m_law at r = 2 and 5 r_M lies within ±0.05 of 1; otherwise UNTETHERED. A Newtonian (tether-off) control from the
  same start must NOT satisfy the ±0.05 condition (else C1 cannot discriminate and is NOT DIAGNOSTIC).
- C2 (coincidence with S4's trigger): (a) "crossing ⇒ positive tether-frame binding": among crossed mass, fraction with
  E_tf > 0 (or escaped) ≥ 0.9; (b) "positive binding ⇒ crossing": among mass that reaches E_tf > 0, fraction that crossed before it
  did ≥ 0.9, in BOTH the infall run (N3) and the sudden-loss runs (N4). E_tf = ½v² + Φ_b + ∫_r^∞ R(G M(<r′)/r′²) dr′ in the frozen
  current configuration.
- C3 (analytic): does the force on an element depend on its stream membership in the action as written?
- **S4 DERIVED** iff C1 = UNTETHERED and C2(a) holds.
- **S4 MODIFIED** iff the action yields a long-lived (≥ 10 local cold-oscillation periods) bound population that feels no tether
  under a criterion other than S4's; the criterion must be stated as an equation.
- **S4 NOT DERIVABLE** iff C1 = TETHERED AFTER CROSSING and no such population appears in N3/N4 (mass that reaches E_tf > 0 leaves:
  ≤ 10% of it still within the box after 10 periods).
- Alternative lifts of S2 to multi-stream states that change S3 (per-element "identity" tether; a tether on a "coherent" current
  only) are analysed and reported as CHOSEN, not forced; they carry no class weight unless they keep S3 exactly.

**Alignment class** (H-SC's mapping, T3). Predicted side per class: medium absent (no capture) → BELOW (Newtonian); medium present
and single-stream inside r½ → ON LAW (tethered); multi-stream inside r½ → FREE (counts as the excess side). Multi-stream inside r½
iff medium present AND N_osc = age/T_c(r½) ≥ 1 AND the stiffness Mach number at r½, M = v_in/c_s ≥ 1 (v_in = baryonic escape speed
at r½, the maximum infall speed of a medium bound only by baryons; c_s² = 2πG L*² ρ_ph(r½), the stiffness sound speed on the law).
Medium absent iff the system's baryons move through the ambient settled medium faster than their own baryonic escape speed
(debris: declared v_rel ≥ 100 km/s, sensitivity ×0.5). Record observed sides (frozen): UFDs EXCESS (CFG930/934 +0.33 dex);
classical dSphs EXCESS (CFG827 +0.38 ln σ, 25/28; CFG828); SPARC rotators ON LAW (CFG828, CFG919); MW-like ON LAW (rotator family,
CFG919); cluster cores EXCESS (CFG922 ×1.8); tidal dwarfs BELOW (CFG936 −0.69 dex); DF2/DF4 BELOW (CFG933/936). INFO only: Coma
UDGs EXCESS (CFG933), isolated LG dwarfs E +0.19 (CFG874, UNDECIDED).
- **ALIGNS:** 7/7 match. **PARTIAL:** ≥ 5/7 match AND both rotator classes match. **MISALIGNS:** otherwise.
- Graded per footing × L* ∈ {24, 100, 300, 1000} pc. Overall = the common class if all cells agree, else L*-DEPENDENT (listed).
- The derived reading (multi-stream matter tethered, if C1 says so) is graded by the same rule and reported as a second row.

## 5. Main numerics (one process at a time; dimensionless where stated)

- N1 1-D S2 + S3, γ = 0, no baryons: exact single-stream solution (independent per-element ODEs on a q-grid) vs the sheet code;
  first crossing times must agree within 2% (else the derivation of the 1-D crossing condition is not confirmed).
- N2 1-D stiffness: Lagrangian-fluid runs at λ/L* ∈ {2, 4, 8, 16} (Newtonian+stiffness Jeans length λ_J = √2 π L* predicted),
  tether off and canonical tether; J_min(t) and a gradient-catastrophe detector.
- N3 spherical cold infall (S2 + S3, full kernel, point baryon mass, inner reflecting boundary with the law's core): C1, C2, energy
  budget, Newtonian control.
- N4 sudden baryon loss from the law at rest, f ∈ {0.5, 0.6, 0.7, 0.8, 0.9}: unbound fraction vs f; C2(b).
- N5 consequences table, both footings, L* ∈ {24, 100, 300, 1000} pc.

## 6. MUTATE (separate `_MUTATE_<name>` outputs; each must bite)

- **M1 γ → 0:** an N2 run at λ < λ_J (tether off) must change from "no crossing" (J_min ≥ 0.1) to crossing at the Zel'dovich time
  (within 1%).
- **M2 tether off (W_full → 0):** the N1 start must change from tether oscillation to Newtonian collapse at the K3 time (0.5%).
- **M3 literal a0 → 0 (a0 × 1e-6 in R(u) = u²/(a0 − u)): REPORT ONLY.** Hand expectation: NOT Newtonian collapse (the capacity wall
  u < a0 pins the medium); the non-commuting limit is disclosed, not a failure of code.
- **M4 sudden-loss tooth:** f = f_crit ± 0.05 must flip deep shells bound ↔ unbound.
- **M5 grading tooth:** a hand-made criterion "excess iff pressure-supported and medium present" must return ALIGNS or PARTIAL under
  §4's rules (shows the grader can return a non-MISALIGNS class).

## 7. Hand expectation (disclosed; written before any script)

- The record's own CFG747/748 radial-shell dynamics computes the tether from the SORTED enclosed mass, i.e. the total current, and
  settles onto the law by collisionless phase mixing, which requires shell crossing. CFG888 shows the critical quadratic cancels the
  carrier's self-gravity. A hand analysis before freezing gives: P = −ρ̄Ψ at first order (sign resolved), exact in 1-D single
  stream; ∇·P = ρ − ρ̄ with P = −∫ j dt holds exactly through crossing (P stays single-valued); in single-stream 1-D each element is an
  independent anharmonic oscillator tethered to its Lagrangian position; after crossing the anchor is the mass rank; the stiffness
  becomes (γρ̄²/2)(1 − J)²/J per unit Lagrangian length (a barrier at J → 0); per-shell energy is conserved in single stream with
  static baryons, so unbinding needs crossing, a changing baryon potential, or stiffness work; for sudden baryon loss from the deep
  law at rest (point-mass baryons) a shell unbinds iff the lost fraction f > 2/3.
- Expected classes: **S4 NOT DERIVABLE** (multi-stream matter stays tethered; unbound matter escapes; S4's "stays bound, never
  re-tethers" needs a coupling switch the action lacks) and **alignment MISALIGNS** (crossing is universal among collapsed systems,
  rotators included; large L* would make the smallest systems single-stream, the inverse of the excess pattern).
- These expectations are not results; the scripts decide.

## 8. Machine and wording

- One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, in-script RSS guard ≤ 0.95 GB, 1-D/spherical numerics only;
  NC2x (1024³) runs beside this lane. No downloads; no other lane edited; LEDGER/THEORY_CANONICAL/sol61_push untouched.
- Any post-hoc change is a dated, labelled amendment committed before the affected number is read.
- κ = ½ FITTED; footings never pooled; framework-native only; never "theory closed"; never "the data favour the framework";
  NOT DERIVABLE / MISALIGNS reported as plainly as success.
