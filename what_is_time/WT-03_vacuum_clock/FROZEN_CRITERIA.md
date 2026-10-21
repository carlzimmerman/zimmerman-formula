# WT-03 — the vacuum clock: FROZEN CRITERIA

Written and committed alone, before any script or computed number of this lane. Post-freeze changes go in appended amendments;
this text is never edited.

**Standing wording.** κ = ½ is FITTED. Z ≡ cH_Λ/a0 = √(32π/3) = 5.7888 (κ = ½ restated). Footings 9.3603e-11 (canonical) and
1.1312e-10 (alt) m s⁻², scored separately, never pooled. Cold energy is real gravitating mass; no particle. Framework-native
inputs only. Nothing here closes the theory or says the data favour the framework over ΛCDM.

## 1. Question

Owner: "what is time, based on my framework?" This lane: **which way and how fast does a0 run in cosmic time, and what does
that demand of dark energy?** The law is a0 = κ c √(G X), X the dark-energy quantity. Three readings are in use on the record
(CFG911 README, 36a18db2e): **ε** (energy density, canonical S1), **−p** (stage 17), **V** (potential, R16; defined only for a
scalar).

- (a) the CFG689 primary band, with exact JSON keys;
- (b) sympy: what d ln a0/dt > 0 and < 0 require under ε, −p and V (V for a minimally coupled canonical scalar, Klein–Gordon);
- (c) per z interval and reading: the fraction of the band that needs NEC violation (ρ + p < 0) or a ghost; whether any reading
  allows a rising a0 with healthy minimal dark energy;
- (d) arrow: is a0 monotone in t; turnaround; does the framework carry a vacuum-set arrow;
- (e) the rate today per reading (per Gyr, per yr; median, 68%), propagated to v_flat, r_M and an outer-disc period; the rival
  a0 ∝ H(z) (d ln a0/dt = Ḣ/H) from the same background; reachability by any local time-domain measurement;
- (f) the de Sitter horizon entropy written through a0, labelled IDENTITY, no verdict weight.

## 2. Record check (git grep on tracked *.md / *.py, 2026-10-21)

Already on the record (not redone, only linked):
- **CFG911 K17** (36a18db2e): ε portal d ln a0/d ln a = −(3/2)(1 + w) exactly; "a0 grows with cosmic time only while the dark
  energy is phantom". Today's running under the three DESI DR2 **CPL** fits, in H0 units: ε −0.37/−0.24/−0.50, V −0.62/−0.41/
  −0.83, −p −0.94/−0.61/−1.32 (DESY5/Pantheon+/Union3); "a few × 10⁻¹¹ per year, cannot be measured directly". CFG911 also
  states a canonical scalar cannot cross w = −1 (kinetic portal).
- **book ch. 25 / DOI 10.5281/zenodo.21110936**: under DESI CPL, a0 (ε) peaks at the phantom-divide crossing, z ≈ 0.4.
- **CFG254 / CFG6 / CFG176 / CFG195**: the w = −1 crossing carries 99.8–100% of the DESI CPL weight at median z 0.36–0.44;
  CFG176's accumulation a0 ∝ t (phantom at every z) excluded at 27–36σ.
- **RETRACTIONS.md** (508a12052): the row "ȧ0/a0 ≈ −3×10⁻¹¹/yr, DERIVED" is retracted (different construction, wrong sign).
  It is NOT used or cited here.

New in this lane: the **native** (CFG689, no CPL) version, segment by segment; the −p and V requirements for a canonical scalar
and their convexity conditions; the arrow/turnaround; today's native drift for each reading against the rival; its propagation to
galaxy observables; reachability.

DO-NOT-CITE checked: "a0(3) = 0.74 ELT target" (CPL law, dead), the retracted ȧ0 row above, and CFG666's κ = ½-from-de-Sitter×age
coincidence are not used.

## 3. Inputs (read only; nothing in CFG689's folder is run, edited or staged)

- `campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json` (result commit **6c064b83a**; mode "primary": curvature free,
  DESI DR2 BAO + Pantheon+, native r_d, no CPL, no late CMB fit). Keys used:
  - `cfg.nodes` = [0, 0.4, 0.7, 1.0, 1.5, 2.33]; the script's percentile list Q = [2.5, 16, 50, 84, 97.5]
    (`cfg689_native_ruler.py`, **fb8d4bba4**, line `Q = [...]`).
  - `BAO+SN.P1.<z>.sqrtX_q` for z = 1.0, 1.2, 1.5, 2.33 — the tracking band √X = a0(z)/a0(0) (percentiles Q); `BAO+SN.P1.<z>.E_q`.
  - `BAO+SN.P3.a0_node_q.<z>` for the six nodes (a0 at κ = ½, percentiles Q); `BAO+SN.P3.H0_q`; `BAO+SN.P3.P_w_le0`.
  - `BAO+SN.posterior.node_mean`, `.node_std` (w_k = ρ_DE(z_k)/ρ_crit,100 at the six nodes), `.omega_b`, `.omega_c`, `.omega_k`
    ([mean, std]).
  - `BAO+SN.P2` (context only: Δχ² 11.11/5, 1.97σ, CONSISTENT WITH CONSTANT).
- CFG689's parametrisation (its script, fb8d4bba4, `bg()`): ρ_DE(z) = ρ_crit,100 · w(z), **w(z) linear in z between nodes**
  (np.interp), ρ_m ∝ (1+z)³ (CFG253), E² = ω_m(1+z)³ + ω_r(1+z)⁴ + ω_k(1+z)² + w(z) over h². Constants copied: G = 6.67430e-11,
  c = 2.99792458e8, ρ_crit,100 = 1.87847e-26 kg m⁻³, ω_γ = 2.4728e-5, N_eff 3.044 (m_ν = 0 in primary) ⇒ ω_r = ω_γ(1 + 0.2271·3.044).
- Canon context: `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-21_DRAFT.md` §3.8 (9470c0433) — primary rows only; θ* rows are
  not used (K9 failed as frozen).

## 4. Declared approximation (posterior samples are NOT stored)

cfg689.json stores percentiles and the per-node posterior mean and standard deviation, not samples or the node covariance.
Therefore:
- **APPROX-G:** node values w_k are drawn as Gaussians with the stored `node_mean`/`node_std`; the only correlations are between
  **adjacent** nodes, ρ_adj ∈ {−0.5, 0, +0.5} (**primary ρ_adj = 0**; ±0.5 is the bracket). Non-adjacent correlations are 0.
- N = 400 000 draws per bracket value, numpy default_rng seed 3031.
- **Background for time conversion:** fixed at the posterior means (nodes, ω_b, ω_c, ω_k) — not sampled, because independent
  draws would ignore the strong w0–ω_k anticorrelation that fixes H0. K1 checks this background against the stored H0 and E(z).
- **Net intervals [0, z]** at z = 1.0, 1.2, 1.5, 2.33 are judged from the stored `sqrtX_q` directly (no approximation).
- Anything that rests on APPROX-G carries the suffix (CORRELATION-SENSITIVE) when the class at ρ_adj = ±0.5 differs from ρ_adj = 0.

## 5. Theory to derive (sympy, `wt03.py` §S)

All in an FRW background, H > 0, dark energy minimally coupled and separately conserved (true by construction in CFG689: ρ_m ∝
(1+z)³ is imposed, so ρ_DE obeys its own continuity equation). With ' = d/dz and d/dt = −(1+z)H d/dz:
- **S1 (ε):** ρ̇ = −3H(ρ + p) ⇒ d ln a0/dt = −(3/2)H(1 + w); in z, d ln a0/dt = −½(1+z)H ρ'/ρ. Rising ⇔ w < −1 ⇔ ρ' < 0 ⇔ NEC
  violated. Falling ⇔ w > −1. (Reproduce CFG911 K17.)
- **S2 (−p):** p = (1+z)ρ'/3 − ρ, so −p = ρ − (1+z)ρ'/3 and d(−p)/dz = (2/3)ρ' − (1+z)ρ''/3. Fluid form: d ln(−p)/dt =
  3H c_a² (1 + w)/(−w), c_a² = ṗ/ρ̇. Canonical scalar: d(−p)/dt = 2V'φ̇ + 3Hφ̇². Rising with NEC (ρ' ≥ 0) ⇔ ρ'' > 2ρ'/(1+z)
  (c_a² > 0). State the < 0 conditions too.
- **S3 (V, canonical scalar, Klein–Gordon φ̈ + 3Hφ̇ + V' = 0):** V̇ = V'φ̇; rising ⇔ the field climbs (V'φ̇ > 0), which forces
  d(φ̇²)/dt = −6Hφ̇² − 2V'φ̇ < 0 (decelerating; transient); ρ̇ = −3Hφ̇² ≤ 0 throughout. In z: K = (1+z)ρ'/6 (≥ 0 ⇔ no ghost),
  V = ρ − (1+z)ρ'/6, V' = (5/6)ρ' − (1+z)ρ''/6; rising V with no ghost ⇔ ρ' ≥ 0 and ρ'' > 5ρ'/(1+z). ρ' < 0 needs K < 0: a ghost
  (or a non-canonical / coupled sector, outside this lane).
- **S4 (parametrisation identity, flagged TRUE BY CONSTRUCTION):** inside a CFG689 segment ρ'' = 0, so the drift signs of all
  three readings equal −sign(ρ') there. The readings can differ only through ρ'', which the node band does not measure.
- **S5 (IDENTITY, no verdict weight):** de Sitter horizon entropy of the DE patch, S = π k_B c⁵/(G ħ H_Λ²) with H_Λ = Z a0/c ⇒
  S = 3 k_B c⁷/(32 G ħ a0²) at κ = ½; d ln S/dt = −2 d ln a0/dt. Numbers for both footings.

## 6. Definitions

- Segments s_k = [z_k, z_{k+1}], k = 1..5, over the six nodes. Δw_k = w_{k+1} − w_k, m_k = Δw_k/(z_{k+1} − z_k).
- **Literal reconstruction (PRIMARY):** CFG689's own piecewise-linear w(z). Inside s_k: F_ε = w, F_−p = w − (1+z)m_k/3,
  F_V = w − (1+z)m_k/6. a0 for reading R "rises across s_k" ⇔ F_R(z_{k+1}) < F_R(z_k) (larger at lower z ⇒ grew with time).
  A draw is **UNDEFINED** for R on s_k if F_R ≤ 0 at either end (a0 not real); undefined fractions are reported.
- **Smooth reconstruction (SECONDARY, sensitivity only, no verdict weight):** scipy CubicSpline (not-a-knot) through the six
  node values per draw; F_R evaluated at the nodes with the spline's ρ' and ρ''; rising across s_k as above.
- p_rise(R, s) = P(rises across s | defined); p_fall(R, s) = P(F_R(z_{k+1}) > F_R(z_k) | defined). A difference with
  |ΔF| ≤ 1e-12·|F(z_k)| counts as neither (flat). f_NEC(s) = P(Δw_k < 0) over all draws: by the mean value theorem, Δw_k < 0 forces
  ρ' < 0 (NEC violated) somewhere in s_k for ANY interpolant, so f_NEC is reading-independent and interpolation-free. Under V it
  is the fraction needing a ghost.
- Thresholds: **t68 = 0.8413**, **t95 = 0.9750** (one-sided Φ(1), Φ(1.96)).
  - RISE_L(R, s): p_rise ≥ t_L. FALL_L(R, s): p_fall ≥ t_L. Otherwise FLAT_L.
  - D_s(L) (band demands NEC violation on s at level L): f_NEC(s) ≥ t_L.
  - Net interval [0, z] (ε only, stored quantiles): rising at 68% ⇔ sqrtX_q[84] < 1; at 95% ⇔ sqrtX_q[97.5] < 1; falling at
    68% ⇔ sqrtX_q[16] > 1; at 95% ⇔ sqrtX_q[2.5] > 1. A net rise at L ⇒ NEC violated somewhere in (0, z) at L (mean value theorem).

## 7. Verdict rules (per reading R, per level L ∈ {68%, 95%}; ordered, first match wins)

1. **PHANTOM-REQUIRED:** ∃ s with RISE_L(R, s) and D_s(L); or, for ε, a net interval rising at L.
2. **HEALTHY:** ∃ s with RISE_L(R, s) and not D_s(L). (Impossible for ε by S1, and impossible for −p and V in the literal
   reconstruction by S4 — both flagged as by construction. It can occur only in the secondary spline rows.)
3. **FALLING** (class added by this lane; declared): no rise at L, and ∃ s with FALL_L(R, s) (or, for ε, a net interval falling
   at L). a0 fell with time there; w > −1 (healthy) suffices; no rise is demanded.
4. **NOT DIAGNOSTIC:** everything FLAT_L (the band is consistent with a flat a0 at L).
- Suffix (CORRELATION-SENSITIVE) per §4.
- A separate **THEOREM-LEVEL** line per reading answers "can a rising a0 come from healthy minimal dark energy at all?" (from S1–S3:
  ε NO; −p YES iff convex enough; V YES iff the scalar climbs, transient) and "does the CFG689 band measure the needed ρ''?"
  (expected NO: nodes are 0.3–0.83 apart and the parametrisation sets ρ'' = 0 inside segments).

**Arrow / turnaround (d), per L, on the literal reconstruction (identical for the three readings inside segments by S4):**
- Definite set = segments with RISE_L or FALL_L, plus net intervals definite at L.
- **TURNAROUND:** a RISE_L segment lies at higher z than a FALL_L segment (a0 rose, then fell) or the reverse. Location = the
  nodes between the closest opposite pair, with lookback times. Verdict: **NO GLOBAL VACUUM ARROW** (a0 is not monotone; its
  direction flips where w crosses −1 under ε).
- **RISING-ONLY / FALLING-ONLY:** definite set non-empty and of one sign. Verdict: **DIRECTION SEEN, MONOTONICITY NOT
  ESTABLISHED.**
- **FLAT:** definite set empty. Verdict: **NO VACUUM CLOCK MEASURED** at L.
- Always stated (by construction): a0 depends on t only through ρ_DE(a(t)); any direction it has is the expansion's direction read
  through dark energy, not an independent arrow.
- Descriptive only: P(the a0 maximum over the nodes sits at node k) and P(monotone in t over all five segments) per draw. A
  non-monotone draw fraction is NOT a turnaround test (noise alone makes most draws non-monotone).

**Rate today (e).** r_R ≡ d ln a0/dt at z = 0:
- literal: r_ε = −½H0 m_1/w0; r_−p = −½H0 (2/3)m_1/(w0 − m_1/3); r_V = −½H0 (5/6)m_1/(w0 − m_1/6) (m_1 = secant over [0, 0.4]:
  a segment average, flagged);
- spline: r_ε = −½H0 ρ'/ρ; r_−p = −½H0 [(2/3)ρ' − ρ''/3]/(ρ − ρ'/3); r_V = −½H0 [(5/6)ρ' − ρ''/6]/(ρ − ρ'/6), at z = 0;
- rival: r_H = Ḣ/H|0 = −H0 E'(0), E'(0) = (3ω_m + 4ω_r + 2ω_k + ρ'(0))/(2h²), ρ'(0) = m_1 per draw, ω's at their means.
- Reported: median, 16–84%, 2.5–97.5%, per Gyr and per yr. H0 in Gyr⁻¹ = H0[km/s/Mpc]/977.792.
- Observables, per footing, a0(z=0) = footing value, reference galaxy M_b = 6e10 M☉ (CFG911's MW-like row), deep-MOND flat curve:
  v_flat = (G M_b a0)^{1/4}; r_M = √(G M_b/a0); outer orbit at r = 3 r_M, P = 2πr/v_flat. Rates: d ln v_flat/dt = r/4,
  d ln r_M/dt = −r/2, d ln P/dt = −r/4 at fixed r and −r/2 for an adiabatic orbit (fixed angular momentum). Accumulated over 100 yr:
  Δv (m/s), Δr_M (AU), ΔP (s). Absolute ȧ0 = a0·r (m s⁻² yr⁻¹) per footing.
- **REACHABLE / NOT REACHABLE** (framework per reading, rival separately): REACHABLE iff T_req = δ_rec/|r|_68 ≤ 100 yr, where
  |r|_68 = max(|q16|, |q84|) of the rate and δ_rec = the relative 68% half-width of a0(z=0) in cfg689.json
  (`BAO+SN.P3.a0_node_q["0.0"]`: (q84 − q16)/(2 q50)), the only a0 precision among this lane's committed inputs. A stress line
  with δ = 1e-6 (hypothetical, not a quoted precision; no verdict weight) is also reported. No external precision is quoted.

## 8. Controls

- **K1 (hard; reproduces committed CFG689 numbers):** from the posterior means and CFG689's constants: (a) H0 = 67.6955
  (`P3.H0_q[2]`) within 0.05 km s⁻¹ Mpc⁻¹; (b) a0(z = 0) = ½ c √(G ρ_crit,100 w0_mean) vs `P3.a0_node_q["0.0"][2]` = 9.3523e-11
  within 0.5%; (c) E(z) vs `P1.<z>.E_q[2]` within 0.5% at the four z.
- **K1b (approximation diagnostic; reported, flags only):** APPROX-G at ρ_adj = 0 reproduces `sqrtX_q` at percentiles 16/50/84
  within 0.03 (absolute) and `P_w_le0` within 0.01 at the four z. A miss flags "APPROXIMATION OFF at z" in the README.
- **K2 (identity, flagged TRUE BY CONSTRUCTION):** constant dark energy (all nodes = w0 per draw) ⇒ every reading, literal and
  spline: every segment FLAT in every draw (|ΔF| within the 1e-12 tolerance) and |r_R| ≤ 1e-12 H0 today.
- **K3 (logic plants, noiseless; std × 1e-9):** constant w = −1.2 (ρ ∝ (1+z)^{−0.6}) ⇒ ε returns RISE_95 in all five segments and
  PHANTOM-REQUIRED at both levels; w = −0.8 ⇒ FALL_95 in all five and FALLING. Rate sign correct, and the literal rate equals the
  analytic secant −½H0[(1.4)^{3(1+w)} − 1]/0.4 to 1e-10 relative. The ratio of that secant rate to the instantaneous
  −(3/2)(1+w)H0 is reported, not graded (it measures how much the [0, 0.4] segment average differs from the z = 0 value).
- **K4 (sympy):** S1–S5 simplify to zero; CFG911's K17 form reproduced.
- **K5 (integrator):** flat matter + Λ age vs the closed form (2/(3H0√Ω_Λ)) asinh(√(Ω_Λ/Ω_m)) within 1e-6 relative.
- **MUTATE (`WT03_MUTATE=1`):** X → H²(z) per draw (the rival a0 ∝ H(z), from the same background). PASS iff (i) all five segments
  FALL_95 under the ε classifier; (ii) class FALLING at 68% and 95%; (iii) arrow FALLING-ONLY at both levels; (iv) the mutated ε
  rate today equals the rival secant rate −½H0 [E²(0.4) − 1]/0.4 to 1e-10 relative. **Bite:** the mutated ε class at 68% must
  differ from the unmutated one; if the unmutated class is also FALLING, report NO BITE.
- The script exits 1 if K1, K2, K3, K4 or K5 fails (outputs still written).

## 9. Files and compute

`wt03.py` → `wt03.out`, `wt03_results.json`; `WT03_MUTATE=1` → `wt03_MUTATE.out`, `wt03_results_MUTATE.json`; `README.md` with
the verdict. Left uncommitted for orchestrator review. One process, `OMP_NUM_THREADS=1 nice -n 10`, `/usr/bin/time -l`, peak RSS
< 1 GB, minutes. sympy/numpy/scipy only. No downloads; no WebFetch.

## 10. Blindness disclosure and frozen hand expectations

Not blind. Before freezing I was told the band is ≈ 0.91–0.94 out to z 2.33, and I read cfg689.json: the stored `sqrtX_q`, `E_q`,
`a0_node_q`, `H0_q`, `P_w_le0`, `P2`, and `posterior` (node_mean 0.310/0.322/0.391/0.258/0.276/0.256, node_std
0.023/0.039/0.063/0.089/0.131/0.227). I also read CFG911's CPL running table and the RETRACTIONS row. Hand expectations (frozen,
not computed by code):
- The stored 84th percentiles of √X at z 1.0/1.2/1.5/2.33 are 1.027/1.048/1.115/1.212, all > 1 ⇒ no net interval is rising at 68%.
- Under independence, segment 0.7→1.0 has Δw ≈ −0.13 at ≈ 1.2σ (p_rise ≈ 0.89 ⇒ RISE_68, so ε PHANTOM-REQUIRED at 68%), likely
  CORRELATION-SENSITIVE (ρ_adj = −0.5 brings it to ≈ 0.84); 0.4→0.7 falls at ≈ 0.9σ (p ≈ 0.82, FLAT_68 at ρ_adj = 0, FALL_68 at
  +0.5); 0→0.4 ≈ 0.25σ (flat). Expected at 95%: NOT DIAGNOSTIC for all readings. Arrow at 68%: RISING-ONLY at ρ_adj = 0, TURNAROUND
  at z ≈ 0.7 at +0.5 (CORRELATION-SENSITIVE); at 95% FLAT.
- Today: r_ε ≈ −0.05 H0 (≈ −3e-3 Gyr⁻¹), 68% spread ≈ ±0.2 H0; rival r_H ≈ −0.47 H0 (≈ −3.3e-2 Gyr⁻¹, ≈ −3e-11 yr⁻¹).
  Both NOT REACHABLE (T_req ~ 10⁹ yr at δ_rec ≈ 4%).
- −p and V: same segment classes as ε (S4); spline rows NOT DIAGNOSTIC (ρ'' is noise).
These are expectations, not results; the code decides.
