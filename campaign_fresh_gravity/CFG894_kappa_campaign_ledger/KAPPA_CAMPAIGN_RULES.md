# Rules for the κ campaign (CFG894, 2026-10-20)

These rules apply to every new attempt to derive or select κ in a₀ = κ c √(G ρ_DE). They exist because the record holds
about 440 earlier attempts. In about one attempt in seven, ½ was put in by insertion, posit, tuning, naming, circularity or
error, and the determinate values land in the data window at the rate chance predicts (`KAPPA_ATTEMPTS_LEDGER.md`,
`kappa_campaign_lee.out`). A new attempt counts only if it can be told apart from that history.

## 0. Standing facts every attempt restates

- **κ = ½ is FITTED.** Quote the measurement as CFG493: κ_Λ = 0.417 ± 0.095 (ρ_DE footing) and κ_crit = 0.345 ± 0.078
  (ρ_crit footing). ½ sits at 0.8σ and 1.6σ.
  - Never quote 0.551 ± 0.043 or 0.465 ± 0.076 (use 0.450 ± 0.073, MNRAS R1).
  - Never quote SPARC 1.0766e-10 or the p48 pool.
- **The two footings are never pooled.** 9.3603e-11 and 1.1312e-10 m/s² are both κ = ½ statements, on ρ_DE and on ρ_crit.
- **Z ≡ κ.** Z = cH_Λ/a₀ = √(8π/3)/κ = 5.7888 at κ = ½, never ~21. Z² = 32π/3 holds for any ρ and H that obey Friedmann, so
  "matching" it via Friedmann is a tautology.
- **½ versus 0.461 cannot be separated today.** 0.461 is Z = 2π, i.e. Λ = 12π² a₀²/c⁴. A 3σ call needs a₀ to ≤ 2.8%
  (k03), against a 9.3% shared floor.
- **Do not cite dS–Unruh arguments for κ = ½.** They force a₀ = 2cH_Λ, the temperature root, off by exactly Z.
- **GF2's "κ derived" is the SIS ratio σ²/v² = ½, not the law's κ** (AUDIT_GF2, a755b66ca). Q010's "DERIVED" does not engage
  that audit and must not be cited.
- Never manufacture a derivation. No knob scans. Check identities by construction. Never write "theory closed".

## 1. Register before computing

Commit `FROZEN_CRITERIA.md` alone, before any script exists. It must contain:

1. **Mechanism and assumptions.** The physical principle, every equation taken from the record (with file path), and every
   added hypothesis, each named.
2. **Inputs, with provenance.** G, c, ρ_DE (symbolic), ħ if used, and pure numbers forced by the mechanism. See §2 for what is
   forbidden.
3. **Footing.** Declare ρ_DE or ρ_crit in advance.
4. **Option space Ω.** The full list of values the route could output under its own admissible variants (conventions,
   identifications, branches, normalisations), with weights (equal unless argued). If the variants cannot be listed, declare a
   class:
   - `odd`: a-and-H-only, κ² ∈ ℚ·π^odd;
   - `any`: a density route, κ² ∈ ℚ·π^k;
   - `cont`: a transcendental root, log-uniform on [0.05, 5].
5. **π-parity and ħ declarations.** Does the route use only a₀ and H (or a dS-invariant vacuum)? Then exact ½ is impossible
   (CFG263, L4) and the frozen file must say so. Does ħ enter? Then show in advance how it cancels.
6. **Kill conditions and hit classes,** as in §7.
7. **The mutation control** you will run, with the expected direction of the change (§5).
8. **The second prediction** (§3, S4): what else the same mechanism fixes, and the data that test it.

## 2. Forbidden inputs (any one voids the attempt)

- **Any measured or footing value of the result**, used anywhere upstream of the result:
  - a₀ values 9.36e-11, 9.3603e-11, 1.13e-10, 1.1312e-10 and 1.2e-10;
  - measured κ (0.417, 0.45, 0.465, 0.53, 0.55, …);
  - Z = 5.7888, √(32π/3), 0.1727 = a₀/cH_Λ, cH_Λ/Z, and A₀ = c√(Gρ)/2 (GF1's circular input).
- **The target used as a premise:** Λ = 32π a₀²/c⁴, G ρ_Λ = 4a₀², W_v = 4, ε_tot = 1/(32π), J = Gρr²/c² = 1, or "the MOND
  sector couples through G, not 8πG" (premise A) — unless that premise is itself what the attempt derives.
- **Measured ratios:**
  - Ω_m/Ω_Λ, Ω_c/Ω_b = 5.364, f_ret, H₀, measured w₀/w_a;
  - kernel measures calibrated on the RAR.
  Measured H₀ and Ω_Λ may convert a finished prediction into an a₀ at the very end, on both footings.
- **Fitted or bounded record constants** that the result then depends on (L*, α, β, σ_clump, γ, y_t, a cutoff). If κ
  depends on one of them, the attempt is a TRADE, not a derivation. An attempt may use a constant's *independent* bound to test
  a predicted range, as long as it says so.

## 3. Entry screen (all must pass before computing)

- **S1. c is required (CFG893, 131bedf33).**
  - {a₀, G, ρ} have no dimensionless group.
  - The c-free cold-energy system (drift, gate, deficit Poisson equation, phantom, supply, catchment, bath, stiffened action)
    is invariant under S_λ: x → λx, M → λ³M, a₀ → λa₀.
  - So any c-free balance either makes a₀ ∝ Gρ̄^{2/3}M_b^{1/3} (galaxy-mass dependent) or holds for every a₀.
  - **Doors without c are excluded.** c must enter through relativistic or cosmological physics: a horizon, the background
    expansion, a relativistic completion of the action, lensing, or causal propagation.
- **S2. Counterfactual.** The principle must give a different number if κ were different. A condition that every κ satisfies
  is an identity (EXT02 screen Q1).
- **S3. Dimension.** State the route in general spacetime dimension d before setting d = 4 (Q2). A route that is ½ only
  because d = 3 or d = 4 was built in is void (agent F; FRONTIER1).
- **S4. A second prediction (Q3), mandatory.** The look-elsewhere budget is already spent (§8), so the same mechanism must fix
  a second quantity that can be measured independently.
- **S5. Not a reparametrisation.** A monotone one-parameter map (W_n ∝ κⁿ) is a probe, never a derivation (RT-12).
- **S6. The vacuum constant must be fixed by something named.** In a local classical action a constant can be added, so the
  route must name the symmetry, quantisation or dynamics that fixes it (k01, AS067, ARGON01, the sol61 non-selection Lean).
- **S7. Not inside an excluded class:**
  - the unstiffened QUMOND/BIMOND vacuum class (Cassini, p58);
  - κ = 1/(channel or polarisation count) (H061);
  - SIS or virial ratios (AUDIT_GF2);
  - the free-fall surface gravity with a posited J = 1;
  - energy-density matching at g = a₀ with a chosen convention (the W_v / ε_tot slot);
  - global averages without the halo filling factor (k02 is five orders short).
- **S8. a₀(z).** The condition must read ρ_DE locally at each epoch. Real horizons drift with H(z) and give the rival a₀ ∝ H(z)
  law.

## 4. Determinacy

A route predicts a number only if every admissible variant declared in §1 gives the same κ, or their spread is smaller than
the hit window. Otherwise it is a **MENU** and never a hit. A menu that happens to contain ½ counts as a spurious ½ (as for
p02, KS02 and QC2).

## 5. Mutation control (required; a separate run that writes separate `_MUTATE` outputs)

Change at least one input the mechanism says is load-bearing, and state the expected effect in advance:
- the Einstein coupling 8πG → 4πG;
- the vacuum equation of state w = −1 → −0.9;
- the dimension d = 4 → 5;
- the reduced versus the non-reduced Planck mass;
- the identification or branch.

The output must move as stated. An output that stays at ½ under a mutation that should move it is hard-coded, and the attempt
is void. The scorer must exit non-zero when a control bites (chain6 convention).

## 6. Identity-by-construction checks (I1–I8, all reported in the .out)

- **I1. Grep the script** for the §2 constants and fail on any hit.
- **I2. Compute κ symbolically** (sympy, with G, c, ρ_DE and ħ as symbols). Print its dependence on every free constant; a
  non-zero dependence makes the attempt a TRADE.
- **I3. Scaling.** G → λG, ρ → μρ, c → νc must give a₀ → ν√(λμ) a₀ with κ invariant.
- **I4. Rename test (the GF2 lesson).** Set the law's κ to 0.4 in the code.
  - A derivation's output must not move, so its comparison with 0.4 now fails.
  - If the output follows the law's κ, it is a consistency relation.
  - If the output stays ½ whatever the law says, check it is the law's κ and not another quantity.
- **I5. No Friedmann tautology** (Z² = 32π/3 for any ρ).
- **I6. Declared footing only;** never pooled.
- **I7. ħ bookkeeping.** The Bekenstein–Hawking ¼ cannot appear un-ratioed (RT-18).
- **I8. π-parity.** Print the π-weight of κ² and confirm it matches the class declared in §1.

## 7. Outcome classes (frozen)

- **EXACT CANDIDATE.**
  - The route is determinate, κ = ½ exactly (symbolic) on the declared footing, and S1–S8, §5 and I1–I8 all pass.
  - It becomes an **EXACT HIT** only when the campaign-level significance in §8 is ≤ 0.0027 *including* the second prediction,
    and an independent audit lane has reproduced it.
- **CONSISTENT (not significant).** The route is determinate, κ lies inside W_data and the checks pass.
  - W_data is [κ − 2σ, κ + 2σ] of the current primary measurement: today [0.227, 0.607] on ρ_DE and [0.189, 0.501] on ρ_crit.
  - With today's window any O(1) route lands inside about 21–28% of the time, so this class can never be called a detection.
- **MISS.** The route is determinate and lands outside W_data.
- **MENU** (see §4).
- **TRADE / CONDITION / BOUND / CLOSURE.** The route gives no number: κ is swapped for another constant, the condition equals
  the target, the result is an inequality, or the route is shown not to work.
- **VOID.** The route used a forbidden input, failed an identity check or the mutation control, or an algebra error was found.

## 8. Look-elsewhere: the rule and the running numbers

For attempt i with option space Ω_i:
- p_i^data = the mass of Ω_i inside W_data;
- p_i^exact = the mass of Ω_i at κ = ½ exactly.

If Ω_i is declared as a class, `kappa_campaign_lee.py` takes these masses from the reference generator κ² = (p/q)π^k
(1 ≤ p, q ≤ 16, k ∈ {−2…2}, 0.05 ≤ κ ≤ 5), weighted either flat or by simplicity 1/(pq(1+|k|)). Simplicity weighting is the
conservative choice because it favours ¼.

**Campaign statistic.** P_LEE = 1 − ∏(1 − p_i) over every determinate trial so far, including the new one. That is the chance
that the campaign produces at least one hit if no route knows κ. Menus are never hits under §4. A naive figure that includes
them is printed alongside for comparison.

**Significance of an exact candidate.** The candidate's combined chance probability is P_LEE(exact, simple, including it) ×
p_second, where p_second is the chance that its second prediction matches its own measurement (from its own option space and
data window). It is an EXACT HIT only if that product is ≤ 0.0027 (≈ 3σ).

**State at registration** (`kappa_campaign_lee.out`; rerun after every new row):
- 51 determinate trials, 63 menus.
- P_LEE(exact, simple weighting) = 0.20 (0.03 flat).
- P_LEE(data) = 1.00. 17 of the 51 determinate values lie in W_data, where the null expects about 14.
- 64 of 439 derivation attempts output ½ by a flawed route.

Two consequences:
1. **No exact ½ can be significant on its own today.** It needs the second prediction.
2. **A "consistent" landing carries no evidential weight** until W_data shrinks below the ½ / 0.461 separation (σ(a₀) ≤ 2.8%).

The data-side unlock (a stellar M/L zero point and an absolute gas scale at the few-percent level) is not a derivation route,
but it is what makes any future hit testable.

## 9. Running count and register

- Every attempt appends one row to `kappa_attempts_register.csv` (append-only), and failures get a row too.
- Ids are sequential: K595, K596, …
- Columns: kid, src (lane id), family, path, mechanism, kappa (if determinate), options (if menu), cls
  (odd/any/cont/menu/free/pend/obs/audit/lean/nk), half (1 if the route output exactly ½), verdict, commit.
- Then rerun `kappa_campaign_lee.py` and commit the CSV, the regenerated `KAPPA_ATTEMPTS_LEDGER.md`, the `.out` and the `.json`
  together with the lane's own result.
- Never edit another lane's row. Corrections go in as new rows that reference the old id.

## 10. Reporting language

- **Until an EXACT HIT exists:** "κ = ½ is FITTED; route X gives κ = … (class …, P_LEE …)."
- **Allowed:** "route X lands at 0.461, inside today's window, not significant."
- **Forbidden:**
  - "κ derived", "the 32π explained", or "the ½ comes from de Sitter";
  - "data favour ½ over 1/2π" without naming the footing and kernel;
  - "κ = 1/2 by polarisation count";
  - citing GF2 or Q010 as a derivation.

## 11. Coordination and resources

- Read `KAPPA_ATTEMPTS_LEDGER.md` and `KAPPA_DOORS.md` before proposing anything.
- Run the registered-but-unrun lanes (p62, p63-C1/C1b/C2/C3, KAPPA_LOGIC) before any lane that overlaps them.
- Take CFG ids only from a reserved block, after checking LEDGER.md and `ls campaign_fresh_gravity | grep CFG…`.
- Do not duplicate the 32π chat (measured-κ provenance; the logic/Lean argument).
- **While a 1024³ run is live:** light single-core scripts only (`nice -n 10`, `OMP_NUM_THREADS=1`, under about 1 GB, seconds).
- **Searches:** text files only.
  - Use `rg -t md -t py -t txt -t json --max-filesize 2M`, or `git grep` on tracked files.
  - Exclude _external_data, *.npz, *.npy, *.bin, *.fits, *.dat, *.hdf5 and checkpoint directories.
  - Never `git grep --untracked`. (Orchestrator rule of 2026-10-20, after a repo-wide grep over binaries caused the swap spike
    that killed the 00:32 run.)
- No downloads. No personal names or home paths in committed files. Commit only your own paths; never rebase, amend or force.
