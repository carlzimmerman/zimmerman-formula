# Handoff to astra, 2026-11-04 (companion): the complete-theory lanes CT1 to CT18

**Correction, read first (CT14, landed after this was written):** C'' FAILS G0. With the khronon's velocity kept in the static weak-field perturbations, its tie gives a UV instability (growth ∝ k) for g above 2.7e-9 to 1.9e-7 m/s^2, reached in inner galaxies, for any realistic w; only exact Lambda escapes. CT13's pass came from treating the khronon as a static constraint. So the 'result worth taking forward' below is overturned: a healthy dynamical rho_DE tie in v3s is NOT established, and lane 1 becomes 'find a coupling that keeps the rest-frame tie stable with the khronon velocity included, or prove none exists'. See complete_theory_2026_11_04/CT14_Cpp_health/README.md and CT18_CPP_FINAL_VERDICT.md.

Written at the owner's request ("please push up this work and lanes for astra to pick up and continue"). It complements `ASTRA_HANDOFF_2026-11-04_FROM_CLAUDE.md`, the main handoff (read that first; it records the later 11-04 owner decision adopting v3s as the a0 law's action, scoped to isolated galaxies, the Solar System, galaxy lensing and GWs). This brief is not a result: every claim points to a lane README or .out, which is the record. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.

## What was done

All in `complete_theory_2026_11_04/`. Start with `CT0_ROADMAP.md`, `CT9_GRADING_VERDICT.md` (with its addendum) and `CT18_CPP_FINAL_VERDICT.md`.

- **CT1 to CT4, fresh-look reviews** of the action, local gravity, cosmology, and lensing/clusters/data, each with a record table.
- **Owner decision D1** (`OWNER_DECISION_2026-11-04_D1.md`): "Yes, grade it". A field with a linear dust phase may be graded; that is a go to grade, not an adoption, and the 11-01 retirement stays on record.
- **CT5 to CT8:**
  - three tie candidates inside v3s (four-form A, Lambda-projector B, stiff portal C);
  - a dust phase tied to rho_DE.
  - A and B fail health, C misses the slope, and no dust amount can be tied to rho_DE.
- **CT10 to CT13:**
  - the no-go theorem is partial.
  - CT10 found **C''**, an independent review (CT13) re-derived it, and it passes G0 (conditional) to G4.
  - The one-reservoir route (CT11) and the leaf-global tie (CT12) fail.
- **CT14 to CT17**, the remaining gates for C'':
  - CMB fails (CT15);
  - disc depletion not passed (CT16);
  - clusters fail (CT17).
  - CT14 (full health) was still running when this was written; its files will land in `CT14_Cpp_health/`.

## The result worth taking forward

**C'' gives v3s a healthy rho_DE tie** (CT10, CT13). In the v3s action, replace the hand-set a0 by a0^2 = kappa^2 G rho_phi, where rho_phi = 2 X P_X - P is the covariant rest-frame energy of a canonical dark-energy scalar phi, and remove J's Lambda. Then:

| Property | Result | Source |
|---|---|---|
| a0^2 ∝ rho_DE on FRW | exact: slope 0.5 in every background a canonical field can realise | CT10, CT13 |
| local a0 | constant to ≤ 1.0e-10 dex in clusters and 7e-23 at the Sun | CT13 `ct13_review.out` |
| health | gradient coefficient 1 + eps h, cannot flip | CT10, CT13 |

The khronon-frame energy T_nn, used in CT7 and CT12, is what produces the instability. This bears directly on the main handoff's **A3 (a0 from the v3s action)**: the tie can be made dynamical, but kappa^2 = xi stays a free coupling. kappa = 1/2 is not derived.

C'' is not a complete theory. Its dust is v3s's khronon, and three gates fail because of it:

| Gate | What fails | Source |
|---|---|---|
| CMB | radiation-like until z 35-78 at allowed mu_K; H3/H2 0.53-0.57 for any amount, against 0.979 | CT15 |
| Discs | the dust folds in 3.6-724 Myr | CT16 |
| Clusters | too weak in cluster wells: X-COP +0.43 to +0.46 dex short, Bullet wrong sign, KiDS +0.09 to +0.12 dex short | CT17 |

These sit outside the adopted scope, as in v3s.

## Open lanes, best first (use your AZ prefix)

1. **C'' into the adopted scoped v3s.** Small to medium.
   - Wait for CT14 to land (full mixing with the curvature mode, P and the dust; W4b; the tracker branch), then decide whether C'' should replace v3s's hand-set a0 inside the adopted scope.
   - Conditions to state: the dark energy is phi alone (Lambda removed by hand), w never crosses -1, a thawing potential, kappa^2 hand-set.
   - Adoption is the owner's call.
2. **kappa inside C''.** Is there a term or symmetry in the v3s + phi action that fixes xi (kappa^2 = xi)? This is the main handoff's A3 restated for C''. Check `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md` (every route on record reduces to xi = 1) before starting, and its reopen conditions.
3. **C'''s falsifiable prediction.** C'' predicts a0(z) = kappa c sqrt(G rho_phi(z)) exactly, and is excluded by a confirmed w = -1 crossing (DESI DR3, Euclid). Write it as a frozen pre-registration against the AT1 a0(z) rule. Ask the owner before any download.
4. **The disc-fold variant.** Only if the owner wants the out-of-scope gates pursued.
   - CT16: deciding disc depletion needs C'' plus X14's beta K^2 term (beta 2e-6 to 1e-5), which is a new candidate.
   - It needs an axisymmetric (R, z) run of about 40-80 CPU h, plus about 8x more for the convergence pair, at RSS 0.2-0.5 GB.
   - Heavy compute must be preemptible.
5. **The cosmology and cluster wall.** No lane. CT3, CT8, CT11 and CT15 show the CMB needs linear cold dust (omega_x/omega_b 4.9-5.4 by z ≥ 3e4) that no tested field supplies natively. A separate dust component is the retired sector by another name. Reopening that is the owner's decision alone.

## Record corrections flagged, not edited (owner's call)

- **CFG689.** Its a0(z) band uses r_d 147 Mpc from the retired sector's omega_c; with baryons alone r_d is 201 Mpc. The band is therefore conditional on that sector (CT3).
- **L295.** The baryons-only CMB failure stands, but its direction was wrong: H3/H2 is 0.527, too low, not too high (CT3).
- **CT1.** Its running law for the portal misses the -w'/(2(1-w)) term (CT7).
- **KT17's r_M-scaled filter** has no window in its action-consistent form (KT33/KT34, CT2), so it is not a live lead.

## Rules

- Check the record before proposing anything (grep the repo, git log, STANDING.md, the ledgers).
- Freeze gates before computing, derive rather than tune, and record failures as hard as passes.
- No dark matter particle. The cold sector stays retired unless the owner says otherwise.
- Ask the owner before downloads, deposits and sending.
- Never write "theory closed".

kappa = 1/2 FITTED; not theory closed.
