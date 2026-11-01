# DR7_fragments: FROZEN CRITERIA (committed alone, before any script or number on this rule)

**Question.** Door 7, from an outside text that reached us as fragments: a Lynden-Bell / Liouville cap on ρ_f/σ_f³ limiting the contraction. PS1 and PS2 capped the **initial core** of the rule with the floor; neither touched the response. UR1, UR2, NR3, LC1, OP3 contract with no phase-space bound. RM1 names "phase-space cap" as one proposal behind its envelope, but grades a fitted f, not this rule. So the exact case is untested: on the response path, does the cap, with no new number, change what UR1's rule gets?

## Rule (derived; no fitted number)
Collisionless cold dark energy conserves fine-grained f, and coarse-graining can only lower its maximum. Use the pseudo-density Q = ρ/σ³, isotropic Jeans, as PS1/PS2 do. **Q is a proxy for f, not f: a bound on f_max is a theorem, this bound on Q is not.** Stated, not derived away.

Start state is UR1's own: cold M₀(r) at core rule N, baryons tracing it, so M_tot,i = M₀(1 + F), `contract`'s own F. End state: measured M_b and the responded cold mass M.

    P(r) = ∫_r^edge ρ G M_tot / s² ds,  σ² = P/ρ,  Q = ρ/σ³ = ρ^(5/2) / P^(3/2)
    Q₀ = max Q_i(r), on r ≤ r_s, r_s = the radius of the minimum of Q_i (beyond it, Q_i rises only from the truncated edge, P → 0)

Q ≤ Q₀ is the same statement as ρ ≤ ρ_lim(r) = Q₀^(2/5) P_f(r)^(3/5). G cancels. Saturated matter is a γ = 5/3 polytrope, which is the Lynden-Bell / Thomas-Fermi form, here with no particle mass and no degeneracy number: Q₀ comes from the path's start.

M_c = Blumenthal, X39's `contract`, unmodified. Then, outward from the centre on r ≤ r_s, with P_f from M itself and fixed-point iteration (12 damped steps):

    M(r + dr) = min( M_c(r + dr), M(r) + ρ_lim dV )

M ≤ M_c, monotonic, rejoins M_c outside the capped core, so held-back mass sits just outside it. Beyond r_s, M = M_c. Applied by wrapping `contract`, so every call site gets it: SPARC, clusters, groups, X-COP, LITTLE THINGS.

Choices fixed now: global Q₀ (theorem-strength, as PS2, because PS1 showed mean-Q is contradicted); isotropy (PS2: anisotropy cancels when shared); core shape by hand, so Q₀ inherits the hand-chosen Burkert and η. A true adiabatic response of an isotropic core keeps Q about fixed (Young 1980, from memory, provisional), while Blumenthal's circular orbits overshoot it; that is the reason the case is worth computing.

## Disclosed. Not blind.
UR1, UR2, NR3, LC1, OP3, PS1, PS2 read. Baseline, NR3 MEDIAN, EM1 + Blumenthal: Υ 0.35/0.36, rms 0.0670, tilt +0.17, 14 keys, groups +1.50, X-COP −0.097, 0.146, LT +0.116. Off: Υ 0.75/0.76, tilt +0.59.

**RM1 read before this freeze** (its reader's verdict isn't committed; I evaluated its five gates on its result files, read only, NR1 PRIMARY's η): 0 of 180 cells clear; best cells fail one gate, Υ at f 1, tilt at f 0.3–0.4. At δ 0: I0.00 Υ 0.59, tilt +0.64; I0.25 0.51, +0.42; I0.50 0.46, +0.30; I0.75 0.40, +0.22; G0.5 0.50, +0.26. The cap only weakens the response, and inward, so it should land near family I. This run can't be a surprise upward unless it differs from those forms. Its value is that it has no free strength: it gives the f the physics claims.

**Expectation on record, mine.** Binds in the inner disc only (Blumenthal on a core is cusped by construction), so Υ rises a little, to 0.36–0.45, tilt worsens or holds, line fails. Label **BITES, FAILS** or **CAP INERT**. Clusters expand, so the cap is inert there, unless the BCG makes it bind.

## Runs (UR1's path, read only, own cache dir), canonical, f★ 0.034, both backgrounds, EM1 at δ 0
1. **PRIMARY:** EM1, Blumenthal, cap on, NR2 MEDIAN (ρ 1.241, 1.147; η(10¹²) 21.53).
2. EM1, Blumenthal, cap on, NR2 LOW and HIGH, SPARC side (clusters don't read these inputs, as NR3).
3. Reported: FAIRTA + cap at MEDIAN (UR1's primary). Reported: Q₀ cold-only, M_tot,i = M₀, the weaker cap. Reported: M/M₀ at r₀ by V_flat, against Blumenthal's.

No scan. No Gnedin row: LC1's f_Q is a different test and isn't a phase-space statement.

## Pass lines (the record's)
SPARC rms ≤ 0.110 and Υ 0.50–0.80, both backgrounds; |tilt| ≤ 0.15; groups |Z| ≤ 2 CONSISTENT; X-COP |mean| ≤ 0.05, rms ≤ 0.10; LITTLE THINGS |median E| ≤ 0.10; 15 keys |Z| ≤ 2. **The keys on this path run on UR1's gas inputs, without GS4's +0.005 factor, which lives only in ZN1's grader. Stated now:** if the primary row reaches 15 of 15 and every other gate, the label is CLEARS, KEYS NOT ON MEASURED GAS, and no more until regraded. KiDS, Local Group, MW not run, so no PASS label is available here.

## Labels, PRIMARY
- **CLEARS SPARC SIDE:** line, tilt, groups, LT all pass; then read keys, X-COP. Never a pass.
- **BITES, FAILS:** Υ moves ≥ 0.02 from the baseline on either background and a gate fails. Name it.
- **CAP INERT:** Υ moves < 0.02 on both. A gate fails. The bound doesn't reach what the fit reads.
- **[NOISE-LIMITED]** if the label or the line differs at LOW or HIGH.

## Checks (failed check: no verdict)
K1 cap off in this path reproduces NR3 MEDIAN's EM1|blum: Υ, rms, cluster preds, |d| ≤ 10⁻⁶. K2 test case, Hernquist baryons in a Burkert core: independent Q (`np.gradient`, direct Jeans quadrature) ≤ Q₀ × 1.05 on the capped range, and Blumenthal uncapped exceeds it. K3 identity, M_b = F M₀: no contraction, cap doesn't bind, |M/M₀ − 1| ≤ 10⁻³. K4 grid × 2 on K2's case: M at the half-baryon radius moves ≤ 1 %. K5 all calls in PRIMARY: M ≤ M_c, monotonic, M_edge = M_c,edge within 10⁻⁶ wherever M_c reaches the edge, fixed point ≤ 10⁻³ (worst reported). **MUTATE:** ρ_lim × 0.1, separate output: Υ moves ≥ 0.02 from PRIMARY. Rerun of the reader byte-identical.

Under 1 GB, one thread, nice 15; checkpoint per row. κ = ½ FITTED, unused here; no a₀ in the cold sector, owner's 10-31 rule kept. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
