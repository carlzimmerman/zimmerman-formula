# HOSTILE REGRADE of Route E (null_steelman): does the dS-Unruh FOUNDATION license a local-density a0? — VERDICT (2026-06-14)

**Regrade: CONFIRMED NULL (CLOSED FALSIFIER). Route E's closed-falsifier verdict is UPHELD — and made
sharper.** The dS-Unruh foundation forces NO derived, in-window (~300–450 kpc), SPARC-safe local-density
scale. Every claim was independently re-derived; the arithmetic checks; the conclusion is airtight. One
minor non-load-bearing code inconsistency flagged; one honest over-statement in the prose corrected (the
foundation DOES license a local-POTENTIAL dependence — the Tolman redshift — but it is derived-but-1e-5,
not absent). This is the front's sixth/seventh banked null and the deepest: it is a STRUCTURAL TRAP, not
a scan miss.

This is NOT a derived cure and NOT a partial. It is a confirmed, falsifiable NULL the framework does not own.

---

## (a) Is the derivation real, or was a tuned input smuggled? — REAL, no smuggle.

Re-ran `route_E_foundational_scale_enumeration.py` (clean) and re-derived every framework-native length
independently. All values reproduce:

| scale | derived value | vs 300–450 kpc window | status |
|---|---|---|---|
| r_AH = c/H_local | 199 Mpc @ R500, 3.4 Gpc cosmic | **442× too big** | DERIVED, cosmological |
| 1/μ (AeST Compton) | 1 Mpc, CMB-pinned | 2.2–3.3× too big | tuned/fixed, banked NULL |
| r_DE level-set | self-normalizes to 2 ρ_DE | √2 nudge, **zero differential boost** | DERIVED, self-defeating |
| r_M = √(GM/a0) | 9 kpc gal / 863 kpc clu | tracks system → kills RAR | DERIVED, dead |
| Z-modulus 32π/3 | dimensionless | no length | n/a |
| ~6–10 Mpc fixed ell (would thread) | — | the only in-window threading scale | **TUNED** (horizon derives to Gpc) |

The verdict smuggles NO tuned input: its content is precisely that no derived in-window scale exists. The
one scale that WOULD thread (~6–10 Mpc fixed ell, η 1.16–1.47, RAR-safe ≤0.001 dex) is tuned — the
dS-Unruh apparent horizon derives to Gpc, not 6–10 Mpc. **Derivation real.**

## (b) Is the a0_local arithmetic right? — RIGHT (one minor non-load-bearing code bug).

Independently recomputed a0_local = (c/2)√(G·ρ_local), all verified to 3 figures:
- galaxy disk (1e5 ρ_DE): **316×** [√1e5] — would kill RAR ✓
- cluster core (730 ρ_DE): **27×** [√730] — right magnitude for Tian 2020's ~17× ✓
- cluster Mpc-ambient (30 ρ_DE): **5.6×** [√30] ✓
- cosmic mean: verdict prose says **1.21×** (= (c/2)√(G·ρ_crit) = 1.13e-10, the ρ_total footing) — **CORRECT**.

**MINOR BUG (flagged, non-load-bearing):** the code's `(rho+rho_DE)` in sections (1)/(5) double-counts DE at
the cosmic mean, printing **1.57×** there instead of 1.21×. The verdict TABLE/prose (1.21×, 1.13e-10) is the
correct figure. This does NOT touch the conclusion: (i) at cluster-core/disk densities ρ≫ρ_DE so the +ρ_DE
term is negligible (27× and 316× are identical either way); (ii) 1.21× and 1.57× are both UNIFORM multipliers —
neither differentially boosts clusters. Arithmetic sound.

## (c) Does it REALLY thread (boost clusters AND keep SPARC tight)? — NO. New independent confirmation.

Every derived scale fails to thread: r_AH/cosmic washes to a uniform a0 (no boost), r_DE self-normalizes
(no boost), local-clumpy density kills the RAR (316× on disks). **New independent check (not in Route E):**
the mean-interior-density (isotropic/tidal-curvature) reading — the ONLY covariantly-legitimate way local
curvature could enter the isotropic floor — gives galaxy inners 10–500× DENSER than cluster cores
(MW <8 kpc: 2.7e5 ρ_DE vs cluster core <300 kpc: 1.0e4 ρ_DE). So **any density- or curvature-monotone
floor boosts GALAXIES MORE than clusters → WRONG DIFFERENTIAL.**

This is the STRUCTURAL TRAP underlying all five+ banked nulls: cluster cores are LESS dense than galaxy
inners but LARGER and more MASSIVE. The only axes on which clusters exceed galaxies are absolute LENGTH
(→ a fixed external ~Mpc scale, tuned) and absolute MASS (→ r_M, system-tracking, kills RAR). No DENSITY/
CURVATURE-monotone scale can separate them. **Fails to thread — provably, not just empirically.**

## (d) Is the sign right? — RIGHT but inadmissible.

Two right-signed channels: (i) local-clumpy density (overdensity → larger floor → larger a0; 27× core ~ Tian
17×); (ii) Tolman floor redshift (deep well → blueshifted dS bath → larger a0). Both right-signed for the
cluster fix. BUT (i) is the inadmissible local reading the 10.5σ SPARC null excludes, and (ii) is ~1e-5
(c² scale). The foundation-licensed readings (cosmic-mean 1.21×, Tolman 1e-5) are uniform or negligible.
**Sign right only in the inadmissible/negligible readings — verified.**

## (e) Is the closed-falsifier conclusion airtight, or did it miss a route? — AIRTIGHT; no route missed.

Checked the candidate misses:
- **Tolman redshift of the floor** (a LOCAL-POTENTIAL, not density, route — banked DSUNRUH_TOLMAN): the
  foundation DOES license it (right sign, zero new input), but the scale is c² → ~1e-5 in any bound system
  (cluster needs 2–25×, gets 1.000025×). DERIVED-but-4–5-dex-too-small. Not a miss.
- **Mean-interior tidal/isotropic curvature:** WRONG differential (boosts galaxies more, §c). Not a miss.
- **Luo 2026 (arXiv:2602.14515)** re-fetched: the "quantum equivalence principle" framing REINFORCES the EP
  obstruction; a_bg = c²√(Λ/48) **verified = 1.355e-10**, uniform, Λ-set, no feedback from local mass. Every
  literature floor is c²√(Λ/N) — a single Λ-fixed number, identical for galaxy and cluster.

**One honest correction to Route E's prose:** "the foundation licenses NO local dependence" is slightly too
strong — it licenses a local-POTENTIAL dependence (Tolman), but a derived-but-1e-5 one. The precise, airtight
claim is: **no DERIVED, in-window (~300–450 kpc), SPARC-safe local scale exists.** That stands.

## Empirical nail — re-verified at source.

`A0_COSMICWEB_ENVIRONMENT_2026-06.md` (real 175 SPARC × external 2MRS/2M++/Tully): d log a0/d log(1+δ) =
**+0.052 ± 0.043** → **10.5σ from the density-a0 prediction +0.5** (correctly = d log a0/d log ρ for a0∝√ρ).
Injection-recovery: a +0.5 fork would be recovered at ~12σ (100% detection) — it would have been seen.
Hostile-verifier-audited, seven independent density axes agree. The per-galaxy coupling is dead on data,
independent of the foundational argument.

## REGRADE VERDICT — CONFIRMED NULL (CLOSED FALSIFIER), upheld and sharpened.

Route E's grade is correct. Density-a0 is a real, distinctive, falsifiable, right-signed-in-magnitude
signature (a0_cluster > a0_field, 27× core ~ Tian 17×, zero-parameter raw-deficit flattening) that the
framework's OWN dS-Unruh foundation does NOT deliver and the SPARC data (10.5σ) already disfavors. The new
structural finding (the mean-interior/tidal reading has the WRONG differential — galaxies denser than cluster
cores) elevates this from "every derived scale happens to miss" to "no density/curvature-monotone scale CAN
thread; only a tuned absolute length or RAR-killing absolute mass separates clusters from galaxies."

Both ways: the distinctive zero-parameter cluster lever and right-signed magnitude credited at full weight;
the EP obstruction, the wrong-differential trap, the scale gap, and the 10.5σ null reported at full weight.
No manufactured cure; no high-priest dismissal. **Quarantine held: a0/Z never asserted derived; the Tolman
local-potential dependence flagged DERIVED-but-1e-5; no in-window scale asserted to exist.**

*Verification code: `/tmp/regrade_check.py`, `/tmp/footing_check.py`, `/tmp/tidal_differential.py`,
`/tmp/luo_abg.py`, `/tmp/final_regrade_summary.py`. Sources: Milgrom 1999 (astro-ph/9805346); Luo 2026
(arXiv:2602.14515, a_bg=c²√(Λ/48)=1.355e-10 verified); banked ELL_DESITTER_UNRUH_HORIZON,
DENSITY_A0_RDE_CROSSOVER, DENSITY_A0_ELL_1MPC, DSUNRUH_TOLMAN_FLOOR_A0LOCAL, ROUTE_C_APPARENT_HORIZON,
A0_COSMICWEB_ENVIRONMENT (10.5σ).*
