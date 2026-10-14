# B. Can the condensed-vs-hot tether source be derived? (theory push, 2026-10-14)

Status: reading + hand algebra only (no runs; a 1024^3 job is live). Nothing here is a verdict. κ = ½ is FITTED; the
cold energy's amount is an input; not "theory closed". Numbers marked (hand) are one-line arithmetic, not committed scripts.

## 0. The problem in one equation

Spherical, zero-stiffness, carrier at rest (astra cold_baryon_selection route G; CFG722 Q2):

    carrier force balance:  b_cond + b_hot + b_free + u  (inward)  =  u + R(u)  (outward),   R(u) = u²/(a0 − u)
    ⇒  R(u) = b_cond + b_hot + b_free.

The empirical rule (CFG640/650 T12, KiDS Δχ² +68.7 → +14.0 → +2.03) wants R(u) = b_cond (stars + HI/H2), with hot gas
still gravitating. The action is density-only, so any selector needs either (i) a matter-state variable in a new vertex,
or (ii) a carrier-state (kinematic/history) variable, or (iii) a non-static support term (astra's warm tether:
d(ρσ_r²)/dr + 2βρσ_r²/r = −ρ h). Constraints carried in from the record:
- CFG749: tethered carrier has its self-gravity cancelled by the critical term ⇒ bound ONLY by baryons; carrier moving at
  ≳ 0.3 V_flat is unbound from the tether. The working carrier must be nearly at rest in the basin frame (CFG722 anchor).
- CFG744 / CFG760–762: no dissipation/capture channel (cold-medium waves too slow; P radiation closed, one c_P ×170–182).
- CFG747: radial cold infall relaxes onto the law without dissipation (inner ≤ 5 r_M); CFG776: surplus tethered cold
  energy is expelled (overshoot into deficit).
- CFG659: P follows baryons adiabatically (radiated fraction ≤ 1e-195).
- astra route S: a weighted source ρ_eff = η ρ_b obeys ∂_t ρ_eff + ∇·(ρ_eff v_b) = ρ_b D_t η ⇒ a state-transition term
  and its work must be accounted for in any phase rule.

Scale used below: r_M = √(G M_b/a0) = 1.08 / 10.8 / 108 / 341 kpc for M_b = 1e9 / 1e11 / 1e13 / 1e14 M☉ (hand, a0 = 1.2e-10).

## (a) Timescale / adiabaticity — FAILS as a phase selector; reduces to a density cut

Adiabaticity parameter for any source component X: ε_X = t_resp · |d ln M_X(<r)/dt|. The carrier response time is a
crossing time in the held potential, t_resp ≈ N · t_dyn, t_dyn = (G ρ̄)^-1/2, with N read from the record's own
collisionless runs: N ∈ [5, 100] (CFG747 lands within a few crossings; CFG776 expels surplus in 50–100 t0).

Hot gas: shocked once at ~R_vir on one crossing, but the *source* is only its mass distribution. After the shock the hot
atmosphere is hydrostatic and changes on the cooling/accretion time ~ t_H. So ε_hot ~ t_dyn/t_H ~ 0.05–0.1. Condensed
discs: the same accretion rate sets d ln M/dt ~ 1/t_H ⇒ ε_cond ~ 0.05–0.1. Cold-mode and hot-mode accretion deliver mass
at comparable rates; shock heating changes the gas's entropy, not its gravitational source. **No separation of the
phases (ε ratio ~ 1).** Turbulent potential fluctuations in hot gas: stochastic heating of a carrier at rest,
dσ²/dt ~ δg² τ with δg ~ 𝓜 g_gas, τ ~ r/(3 𝓜 c_s), gives t_heat/t_dyn ~ 6 c_s/(𝓜 V_b) ≈ 45–90 for 𝓜 = 0.2,
c_s/V_b = 1.5–3 (hand): longer than a Hubble time in clusters (t_dyn ~ 1 Gyr), and discs (spiral δ ~ 0.1–0.3) are
comparable. No phase separation from heating either (and astra route K already closes direct thermal contact).

What the route *does* produce is a mean-density cut: settled iff N t_dyn < t_age ⇔ ρ̄ > N²/(G t_age²)
= 8.6 N² ρ_crit (hand, Ht_age = 0.99): 215 / 860 / 2.1e4 / 8.6e4 ρ_crit for N = 5 / 10 / 50 / 100.
- Kill: DDO154's outermost HI (8 kpc, V = 47 km/s) sits at ρ̄ = 1.4e4 ρ_crit (hand). astra's SPARC comparison shows the
  gas there MUST source the tether (9/21 gas-dominated discs, Δχ² ≥ 25). N ≳ 41 excludes it ⇒ the record-native upper
  half of the N bracket is killed by gas-rich dwarfs; N ≤ 40 keeps cluster cores (≳ 1e4 ρ_crit at 100 kpc) tethered, so
  hot-gas-dominated cores (X-COP: hot/stars 1.03–4.0 at 100 kpc, astra) still source. It is a radius/density selector,
  not a phase selector. It mimics the condensed rule in a KiDS stack only through the mass trend of f_cond.
- Also: CFG763 formation clock (τ ≤ 3.47 Gyr) already says every old system fills; adding an adiabatic criterion does not
  separate an old hot atmosphere from an old disc. **Verdict (a): FAIL (no phase number; density cut killed by dwarfs
  for N > 40, inert for N < 40).**

## (b) Co-motion / velocity — FAILS, wrong sign

Static tether ⇒ the carrier is at rest in the basin frame (CFG749). If the tether required its sources to share the
carrier's mean flow, the selection quantity would be the source's mean velocity in that frame:
- hot atmosphere: ⟨v⟩ ≈ 0 (pressure supported; hot-halo rotation ≲ 0.1–0.3 V_c) ⇒ co-moving ⇒ SELECTED;
- rotating cold disc: ⟨v_φ⟩ ≈ V_c ⇒ NOT co-moving ⇒ excluded;
- early-type stars: ⟨v⟩ ≈ 0, σ ≈ V_c/√2 ⇒ selected like hot gas.
This is the opposite of the needed rule. Swapping to "requires dispersion-free sources" excludes early-type stars, which
the T12 condensed rule counts; it would lower early types' lensing, against KiDS's measured early-type excess
+0.280 ± 0.083 at 50–100 kpc. And the action has no baryon-velocity vertex (only ρ_b enters Poisson; dP/dt = −j is the
CARRIER current), so any velocity selector is a new coupling. **Verdict (b): KILLED (wrong sign + no operator).**

## (c) Argon's two-population picture, made consistent — the best route, but it selects by CARRIER history, not baryon phase

**Why one medium cannot do it.** dP/dt = −j defines P for any carrier distribution, phase-mixed or not; continuity gives
∇·P = ρ_t − ρ̄ exactly. A concentrated phase-mixed core therefore carries P ≠ 0, so W_rem acts on it (Claude's review
stands). In the single-medium dynamics the critical term cancels self-gravity of ALL carrier, so phase-mixed carrier with
v > v_esc,b is not "free in the core"; it leaves the basin (CFG749). That predicts merged systems DEFICIENT in cold
energy, against the cluster-core ×1.8 and early-type +0.28 excesses. **Single medium: killed.**

**Minimal two-population action (one structural postulate, zero constants).** Lagrangian carrier particles with a binary
label s ∈ {t, f}; ξ_i = displacement of tethered particle i from its Lagrangian site:

    L = −|∇Φ|²/8πG − (ρ_b + ρ_t + ρ_f) Φ + P_t·∇Φ − W_full(4πG|P_t|) + Σ_i ½ m v_i²,
    P_t(x) ≡ −Σ_{i∈t} m ξ_i δ(x − q_i) (coarse-grained),   ∇·P_t = ρ_t − ρ̄_t   (single-stream identity),

ρ_f enters Poisson only. Postulate: W reads only the coherent displacement field P_t (Argon's P_DC). The identity holds
for the tethered part only, so it is consistent; it is not derived from the one-medium action.

**Membership rule derived from the record (no constant).** A tethered particle sits in an effective well whose depth is
set by baryons alone (CFG749). Define its tether-frame energy E_b = ½v² + Φ_b(r) + Φ_T(r) (Φ_T the tether residual,
zero at the law's static minimum). E_b > 0 ⇒ the tether cannot hold it. Relabel t → f irreversibly. Irreversibility is
not put in by hand: capture back needs dissipation, and the record has none (CFG744 a, CFG760–762). Liouville forbids
collisionless capture in a static well. Free particles feel full gravity (incl. their own), so they stay bound in the
TOTAL potential and pool like collisionless matter. That is the free component CFG721/776 said is needed.

**The transfer: violent relaxation.** A major merger mixes the carrier on ~t_dyn to ⟨v²⟩ = α V_c² with α ∈ [0.5, 1.5]
(1.5 = isotropic isothermal 3σ²). Point-mass baryon escape: v_esc,b² = 2 G M_b/r = 2 V_c²/ν_s. Tetherable iff
α V_c² < 2 V_c²/ν_s ⇔ ν_s < 2/α ⇔ y = g_N/a0 > y_crit:

    y_crit = 1 / [(2/α − ½)² − ¼]  =  0.083 / **0.50** / 2.25   for α = 0.5 / **1** / 1.5   (hand).

So after a major merger the tether survives only where g_N ≳ a0/2 (Newton-dominated cores). Everything outside goes free
(an extended Φ_b raises v_esc and lowers y_crit somewhat; the bracket covers it). Quiescent discs whose carrier was never
virialized keep the full law to their supply edge. That covers ALL their baryons, including any hot CGM.

**Predictions (sign/structure; amplitudes need a run):**
- Groups/clusters (assembled by mergers): y at 100 kpc ≈ 0.35 / 1.2 for M_b(<100 kpc) = 3e12 / 1e13 M☉ (hand) ⇒
  tether confined to ≲ 100 kpc cores; outskirts free. That cuts the extended law-shaped cold mass at 0.3–1 Mpc that drives
  the KiDS k ≈ 0.3–1 boost (CFG646: 76% of +68.7 from k < 1). Same direction as the condensed rule.
- Early types (merger remnants, baryon-dominated inside R_e, y > 1): tethered core plus free carrier pooling ⇒ a core
  EXCESS over the law at 50–100 kpc. That is the sign of the KiDS +0.280 ± 0.083. The condensed rule has no mechanism for
  this sign; CFG776 needed "an untethered component" and this supplies one.
- Gas-rich dwarfs and late-type discs: all baryons source (HI participates; astra's 9/21 satisfied trivially).
- **Distinguishing prediction vs the condensed rule:** at fixed M* and HI, a QUIESCENT massive spiral with a large hot CGM
  (no major merger since z ~ 1) has its hot gas SOURCING the tether. Under the condensed rule it does not. Conversely a
  gas-poor merger remnant with little hot gas still has a free outskirt. The selector is merger history plus baryon
  dominance of the potential; hot-gas fraction is only a correlated proxy.
- Possible bonus (post-hoc, no weight): CFG776's expelled surplus would partly cross E_b = 0 and relabel free, staying
  bound in the total potential. That could turn CFG776's deficit into retention. Needs a rerun of CFG776 with relabeling.

**What kills (c):**
1. Tidal dwarf galaxies. TDG baryons are born moving at ~V_host through carrier at rest in the host frame; relative speed ≫
   their v_esc ⇒ no capture ⇒ (c) predicts Newtonian young TDGs. CFG763 reads young TDGs as 25–75% filled (window
   τ ≥ 0.72 Gyr). If TDGs carry the law's discrepancy, (c) needs a supply at rest that the record does not have. This
   problem is shared with any at-rest carrier (CFG763), but (c) makes it sharper. **Highest-risk point.**
2. Energy ledger. Relabeling removes the particle's share of W_full. ΔW must go into its kinetic energy (route S
   state-work term). Not yet shown to keep E_b > 0 after transfer; it could also create a relabel/re-tether chatter.
3. It does not derive the condensed rule. If T1x/T12 succeed only because of the phase label, and a merger-history PM
   (framework-native stream/energy tags on the 1024³ particles, NO ΛCDM merger trees) gives Δχ² ≫ +2, (c) is excluded
   as the F1 explanation.
4. Bullet: the free carrier is collisionless and passes through, like the lensing peaks. The tethered core (y > ½) holds
   to its baryons' basin, which in the Bullet is gas-dominated. Needs CFG623-style scoring; open.
5. Still a two-population POSTULATE (W reads P_t only). Argon's idea becomes consistent; it is not derived from one medium.

## (d) Other routes examined

**(d1) Geodesic-source / support-ratio weight.** Weight each baryon element by the fraction of its radial support that is
inertial (free fall, EP-flavoured, CFG693): w = 1 − s_r, s_r = (−ρ⁻¹ ∂_r p)/g. Stars: s_r = 0 (collisionless, so
early-type stars count). Cold HI: s_r ≈ (σ/V)² |d ln ρ/d ln r| ≈ 0.03–0.1 (DDO154: (8/47)² × 2–3 ≈ 0.06–0.09).
Hot gas: s_r ≈ 0.8–1. This is the sharpest phase number found (a factor ≳ 10 gap) and reproduces the T12 labels
element by element with no constant. **But no operator realizes it.** The local covariant candidate
L ⊃ −P·∇p/ρ_b (dimensionally clean, coefficient 1) makes the tether read ∇Φ + ∇p/ρ = −a_b. In a volume-filling
hydrostatic atmosphere that vanishes, so the tether is cancelled for ALL sources there, condensed ones included: the BCG
in a cluster, and every galaxy in its own hydrostatic CGM out to 100 kpc–1 Mpc. That is exactly where the lensing RAR is
measured. The non-local weighted-source version is a phase label again (astra: density-only/linear filters cannot recover
it), and it inherits astra's force problem: the at-rest carrier still feels the hot gas's gravity (R = b_cond needs warm
stress or a one-way cancellation, which breaks reciprocity). **Verdict: KILLED as a local coupling; survives only as a
label.**

**(d2) Capacity Σ ≤ a0/πG.** CFG721: the law's tethered phantom never reaches the cap. It cannot bind. **Closed.**

**(d3) Thermal/evaporation selector.** If the carrier is thermally coupled, eV carriers (CFG723 window 16–143 eV) are
evaporated by 8000 K HI (σ ~ 0.2c) as well as by keV gas (astra route K). That removes the tether everywhere. A carrier
that is heated only to the warm-tether stress σ² ≈ G M_hot/r needs m ≈ μ m_p/f_hot,grav ~ 5 GeV (hand), outside the
condensate window. **Closed.**

## Bottom line

No route derives the selection of hot vs condensed BARYONS from the action. (a) gives no phase separation, only a density
cut that is either inert or killed by gas-rich dwarfs. (b) has the wrong sign. (d1) gives a clean number (s_r ≲ 0.1 vs
≳ 0.8) but no operator: its only local realization deletes the tether inside every hydrostatic CGM. The one route that
yields a sharp, constant-free criterion with record-derived irreversibility is (c′): the selector is the CARRIER's
kinematic history. A tether-frame energy E_b > 0 (CFG749 binding) plus no capture channel (CFG744/762) makes merger-mixed
carrier permanently free, with y_crit ≈ ½ (bracket 0.08–2.25). This turns the T12 phase rule into a proxy. It predicts the
right sign for the early-type and cluster-core excesses, and it rests on one structural postulate (W reads coherent P_t
only). Its biggest exposure is young tidal dwarfs.

## Proposed frozen criteria (route c′; to commit ALONE before any script; runs only after T1x/T12 and the live 1024³ job)

- **H-C′ (rule):** carrier particles labelled t/f. W_full reads P_t only. At each census refresh a tethered particle with
  E_b = ½|v − v_basin|² + Φ_b + Φ_T > 0 (basin = CFG693 own free-fall basin, Φ_b from ALL baryons, no phase label) is
  relabelled f irreversibly. ΔW_full is added to its kinetic energy (energy ledger closed per step; |ΔE_tot|/E ≤ 1e-3 or
  VOID). No other constants; κ = ½ fitted (both footings, never pooled); supply 5.364 × catchment (CFG647).
- **Inputs:** framework-native PM (CFG650 chassis), no ΛCDM mass functions/merger trees/HMcode. Merger history comes
  only from the run's own particles.
- **T1 (F1, primary):** raw KiDS cosmic shear, CFG650 T12 pipeline unchanged except the source rule. PASS iff
  Δχ² ≤ +4.0 canonical AND ≤ +6.0 alt. FAIL iff Δχ² ≥ +9. Between = INCONCLUSIVE. The T12 condensed result (+2.03) is a
  comparison row, not a target.
- **T2 (sign):** KiDS early- vs late-type stacks at matched g_bar, 50–100 kpc. PASS iff the predicted early-type excess is
  > 0 and within 2σ of +0.280 ± 0.083. A predicted value ≤ 0 = FAIL.
- **T3 (guard):** SPARC, all baryons as source for systems with no major merger in the run's history analogue. Use the
  canonical rms guard (CFG695: ≤ 0.110). The 21 gas-dominated discs must keep gas participation (astra's Δχ² ≥ 25 rows
  reproduced).
- **T4 (discriminator, data-gated):** at fixed M* + M_HI, quiescent hot-CGM-rich spirals vs gas-poor merger remnants.
  (c′) predicts lensing ratio > 1 at 100–300 kpc, the condensed rule ≈ 1. Declare the sample before looking.
- **K-kill:** if young TDGs (CFG441 Tier B, ages at −1σ) show ≥ 25% of the law's dark mass at ≥ 2σ, (c′) is EXCLUDED
  unless a declared at-rest supply exists. Write that outcome down now.
- **MUTATE:** M1 threshold E_b > 0 → E_b > −∞ (everything free) must fail T3. M2 no relabel (everything tethered) must
  reproduce CFG596's +68.7 (bit-for-bit chassis check). If either mutation does not bite, the test is VOID.
- **Hand estimate before running:** T1 direction right; amplitude unknown (could under-shoot if outskirts were mostly
  never virialized). T2 sign right. The TDG kill risk is high. κ fitted; not theory closed.
