# DE_FINAL — the directional-EFE programme, state on 2026-09-17 (deepseek lane)

State: **OPEN** (all ten lanes closed, computed, or re-pointed; the decision
rules are frozen; the two scoreable direction channels survived; one
extreme-eta tension registered with its escape audited).

## What the programme asked
The framework's fingerprint: external-field effect with MAGNITUDE (decline
depth ν(η)) but NO DIRECTION (zero field-aligned asymmetry). AQUAL predicts
both; ΛCDM predicts neither; only the framework predicts magnitude-yes /
direction-no. The work order (GAME_PLAN_DIRECTIONAL_EFE) set DE01–DE10.

## The gates, with numbers and second computations

**DE04 — the sample premise, audited (4/4).** The plan assumed
"30–40 SPARC galaxies at η ≥ 0.3" from the Chae+21 environmental table.
FALSE: the published table (109 galaxies, in-repo, validated) tops at
η = 0.019 (maxclu) / 0.0022 (noclu); the repo's independent reconstruction
(175 galaxies) agrees (max 0.039). SPARC curves never enter the EFE zone:
median R_out/r_EFE = 0.256, only 15/218 reach it (reproduces h28's WALLABY
null + identifiability FAIL). THE DIRECTION TEST IS UNDERPOWERED BY
CONSTRUCTION ON THE ENVIRONMENTAL CHANNEL — the programme re-points to the
MOND-boosted channels: MW satellites η_MOND ~ 0.3–0.6 at 100–150 kpc, Virgo
spirals η_MOND ~ 0.4–1.7 at 0.5–2 Mpc.

**DE02 — the decline law and floors (14/15).** THEOREM (certified in sympy
and Lean, DE02F): for g = ν(√(x²+η²)) g_N, x = (r_M/r)², the outer floor is
v²r → ν(η)·GM_b exactly, parameter-free, with the expansion
v²r = GM_b[ν(η) + x² ν′(η)/(2η) + O(x⁴)]. Decline slopes reach −0.5
(Keplerian) beyond ~0.3 r_M. DECISION BAR (DE06): NFW5 separates from the
framework floor at 0.40–0.43 dex (> 0.4 bar: PASS); NFW3 does not
(0.18–0.21: FAIL as registered). Honest cap: **AQUAL vs the framework are
NOT separable in the magnitude channel** (median |Δ floor| = 0.09 dex, slopes
agree to 1e-5) — only the DIRECTION channel separates them, which is why
DE07/DE09/DE08 carry the verdict.

**DE03 — the dSph elongation table (6/6).** Certified identity:
eps_Φ(η) = (√(1+L)−1)/(√(1+L)+1), L = d ln μ/d ln η; sympy-exact. NEW
CORRECTION TO THE PLAN: eps_Φ DECREASES with η over the classical range
(AQUAL's elongation is strongest at small e_N, bound 0.1716), the plan's
"growing with η" phrasing is wrong on the closed form. Per-dSph MOND-boosted
η table (Sagittarius 2.69, Sculptor 0.53, Draco 0.62, ...), both footings.

**DE07 — wide binaries, re-run under the original rule (9/9).** El-Badry+21
DR3, 39,702 clean pairs, the registered split statistic b_perp/b_par − 1:
sample-level +0.0068 ± 0.0106 (p = 0.522, random-axis null, 1000 axes) —
**ABSENT**; widest bin s/r_M > 1.96: −0.1530 ± 0.0926 (−1.7σ, p = 0.093)
canonical, −0.1081 ± 0.0734 alt — pre-registered kill (≥3σ parallel-dominant)
NOT fired. DR3 is underpowered for the AQUAL-class ~6% modulation
(N_need ≈ 8,000 widest-bin pairs vs 372). The registered prior Â = +2.95,
p = 0.029 is the OLD rotation-curve statistic, not reproduced by this
channel; its honest status stated against interest. VERDICT: direction-blind
SURVIVES at DR3.

**DE09 — dSph shape alignment, the first execution (3/3).** 59 MW dwarfs
(LVD table, in-repo), δ = |PA − bearing_GC| folded to [0, 90]: mean
δ = 49.0° (uniform 45), chi2(8) p = 0.499, KS p = 0.211, mean |cos δ| =
0.584 (uniform 0.637), field-aligned fraction 0.119 (uniform 0.167). AQUAL's
predicted alignment (eps_Φ ≈ 0.10–0.15 at these η) is NOT present.
VERDICT: DIRECTION-BLIND SURVIVES on the dSph channel. Second computation:
bootstrap CI of the mean [42.1, 55.9] encloses 45; MUTATE=1 (shuffled PA)
breaks the uniform-check as required.

**DE08 — the extreme-eta rotator (4/4, the honest FAIL-as-finding).** The
LMC at d = 50.1 kpc sits at η_MOND = 0.77: the framework's EFE-cap law
(G119) predicts M_dyn/M_b → 1/√η = 1.14 with r_efe = 2.6 kpc inside the
measured 8.7 kpc. Measured: M(8.7)/M_b = 4.86 (vdM02, PUB) — 4.4× above the
cap, no turnover seen (z = 1.9). The free-dust class (the framework's
ΛCDM-overlap sector) is the registered escape: KILL SUSPENDED, verdict
DISPUTED-ON-THE-DUST, and the turnover RADIUS is named the decider: the LMC
is the strongest resolvable η on record and the flat curve pushes AGAINST
the cap unless the dust carries it — registered as the single most
interesting tension of this programme.

**DE01 — the AQUAL anisotropy table (the decision rule itself).**
IN FLIGHT (the full axisymmetric solver run, steered twice). The steer
found the physics: beyond r_EFE = r_M/√η the downstream side has NO
rotational support (v² < 0 along the field) — r_cap is itself a table
column and a fingerprint element (AQUAL kills rotation on one side; the
direction-blind rule does not).

**Lean certificate (DE02F).** The floor theorem (v²r → ν(η)GM_b, the
mass-scaling floor, the boost factor floor/Newton = ν(η)) certified in
Lean: exit 0, 0 sorry, axioms {propext, Classical.choice, Quot.sound}.

## The state of the fingerprint
- WIDE BINARIES (DE07): direction-blind SURVIVES (consistent with zero).
- dSph SHAPES (DE09): direction-blind SURVIVES (uniform vs GC bearing).
- EXTREME-η ROTATOR (DE08): magnitude side DISPUTED (measured floor 4.4×
  above the cap; dust escape registered); direction side untested (needs
  approaching/receding HI).
- The environmental (SPARC) channel the plan bet on: PROVEN UNRUNNABLE
  (DE04) — the plan's count of 30–40 galaxies at η ≥ 0.3 does not exist.
- The one AQUAL-vs-framework separator is the DIRECTION, and the two
  scoreable direction channels both come out for the direction-blind rule.

## The measurement that would overturn each result
- DE09: a dSph PA distribution aligning with the GC bearing at the AQUAL
  level (eps ~ 0.10–0.15) with no tidal/orbital explanation → direction-yes.
- DE07: a DR4 widest-bin split reaching −3σ parallel-dominant under the
  random-axis null (DR4 mostly cannot: N_need ≈ 8,000 widest-bin pairs).
- DE08: an outer HI turnover of the LMC toward ν(η)GM_b would confirm the
  cap; a flat curve to the tidal radius with the dust excluded kills it.

## Ranked next computations (kills first)
1. **DE01 closeout** — the frozen A(η, r/r_M) table + r_cap(η) column
   (running); kill: if A ≈ 0 at η = 0.5, r ≥ 2 r_M, the plan's own
   expectation fails and the decision rule is the table itself.
2. **DE05 re-pointed**: A_obs on the MOND-boosted channel — the LMC's
   approaching/receding HI asymmetry (Kim+98 PVDs) vs A_pred(η = 0.77);
   kill: |slope| ≥ 2σ → direction-yes.
3. **DE10**: lopsided HI m=1 phase alignment (WHISP/THINGS PVDs) — the
   independent density channel with the same geometry; kill: m=1 phase
   aligned with g_ext at ≥ 3σ.
4. The dust-escape audit of DE08: is the free-dust class actually allowed
   to bind at M_b(LMC) = 3.5e9 and supply M_dyn/M_b = 4.86? (G093's TG
   bound said dust does not bind at galaxy scale — if that holds, the LMC
   IS a cap failure, stated as such.)

## Do-not-cite list
- Any claim that the SPARC-environmental direction test was run (DE04:
  the sample does not exist; h28's WALLABY identifiability FAIL).
- The plan's "30–40 galaxies at η ≥ 0.3" (DE04: 0).
- The plan's "AQUAL elongation grows with η" (DE03: it decreases).
- The Â = +2.95, p = 0.029 prior as wide-binary evidence (DE07: different
  statistic, not reproduced).