# CFG121 — Door 3: dipolar dark matter / gravitational polarisation

Criteria frozen and committed before any script: `../CFG121_FROZEN_CRITERIA.md` (e190e0737). Run exactly as frozen; departures are listed below. Two variants: **V_U** (dipoles respond to the total field) and **V_B** (baryon field only). Both use a0 = 9.3603e-11 m/s² unless stated; the second footing (1.1312e-10) was run for T1, B, C, E, S with the same verdicts and slightly different numbers (`*_second.out`).

## Verdict

**A scoped no-go for the missing object.** Fails G1 (extended baryons, any single polarisation law, the committed ν_mono kernel), G1c (medium self-consistency, both variants), G2 (both), G3 reaction and energy (both) and G4 (both). Passes only: the point-mass identity, a nearly tautological Noether check, kernel stability of the matching kernel (P2), and Solar System safety — and the latter holds only through the medium-density cap, which is the same budget that makes G1c fail. Not evidence for or against the framework; nothing here says the theory is closed; κ = ½ stays fitted.

**Binding pincer:** the medium's own budget needs Q²/κ_I ≥ ~140; linear growth tolerates at most 0.16 (V_U) and 1.2 (V_B) — 860× and 115× apart (post-hoc `posthoc_G2_pincer.py`).

## Gate table

| Gate | Result |
|---|---|
| T1.1 identity | PASS (positive control, not evidence): 6.7e-16 analytic; required 4πGχ = sqrt(1+a0/g_b) − 1, i.e. the P2 kernel |
| T1.2 exponential spheres, no refit | FAIL: max dev C_model/C_tgt 1.31 / 1.02 / 0.43 / 0.063 at 1e9/1e10/1e11/1e12; only 1e12 passes |
| T1.3 any single χ | FAIL: best free-form max dev 0.51 (12 knots), 0.52 (6 knots) |
| T1.4 obstruction | FAIL: dD/dr = M_b'(2M_c − a0 r²/G) to 3e-6; profile-degeneracy spread 0.22–0.33 (line 0.10) |
| T1.5 committed ν_mono | FAIL: 1.46 / 1.40 / 1.19 / 0.62 |
| Q1 | FAIL by theorem (bound charge has zero cosmic mean); point (iii) structural, not run |
| G1c (B1–B4) | FAIL both. F_req 0.41–0.97 vs 0.10; Q* = 9.68 (V_B), 138.7 (V_U); max polarised share 0.51–0.70, the rest a real cold fluid needing its own closure |
| G2 (planar solver, N=512) | FAIL both. V_U central +31.2% growth; V_B central +0.76% total but fails on the equilibrium start and the z=1100 screen (0.15); star sets collapse or grow 5–8× |
| G3 E1 reaction | FAIL both (V_B 0.80–0.88, V_U 4.0–4.3 at Q=1; line 0.10) |
| G3 E2 momentum | PASS (near-tautology for a translation-invariant pair potential; said in advance) |
| G3 E3 energy | FAIL: E_int/E_orb 1.22–2.30 (V_B), 11.6–202 (V_U) |
| G4 | FAIL both (Q*, κ_I* needed; a0–Λ tie postulated = PARTIAL as in CFG43) |
| G5 S1 kernel stability | PASS for P2 (+1.3e-9), ν_mono (+3.2e-6); "standard" −0.081 FAIL |
| G5 S2 | V_U PASS; V_B FAIL under the frozen ghost rule applied literally — in the Newtonian action the block has no time derivatives, so it is a ghost only in a relativistic completion (untested) |
| G5 S4 Solar System | uncapped monopole pull 4.68e-11 m/s² (= a0/2 to 4e-5, 468× the 1e-13 line); safe only through the medium-density cap (≤ 1.1e-16 m/s²), i.e. the budget that fails G1c |
| O1 ownership (Gap 1 side test) | twin-state theorem: no ownership from a state functional; literal window test passes for V_B at x = 20.4–30 (τ/t_dyn 1–1.2), but post-hoc the dipole response there is only 0.3–0.5 of equilibrium |

## Controls

sign, kernel (T1, S), nofield, recip: work, exit 1. **MUTATE Q10 (B and C runs) failed as declared and is reported:** B1 flips to PASS but G1c stays FAIL (B3 needs Q²/κ_I ≥ 140, Q = 10 gives 100); the C-run G2 cells are already FAIL from the star sets so they cannot change (magnitudes do).

## Expectations that were wrong (kept, not repaired)

H2 (failure extent larger: to x = 10 at 1e9, 1e11 also fails), H6, H7 (shortfall ~5× at x=1, ~40× at x=10, not 15×/150×), H8 (Q* = 9.7, not 3–5), H10 (V_U central does not pass: +31%; measured pincer 860×/115× not 5000×), H11 (V_U energy estimate used the wrong physics: 12–202× the orbital energy, not ≈2×), H12 (the external-field effect does not touch the a0/2 pull; ν_mono is stable), H13 (a window exists for V_B under the literal O1 test). Held: H1, H3, H4, H5, H5′, H9, H14.

## Departures and disclosures

- CFG44 has no scale-length law; the exponential spheres use CFG50's four (mass, scale-length) points as h(M) = 2 + (log10 M − 9) kpc, fixed before any number was seen.
- G2 is gated on the worst of two dipole starts (cold, equilibrium), declared at phase 2; the frozen file did not fix the dipole start. Initial amplitude read as δ(z=100) = A.
- c_eff² is defined 0 (no gradient term in the polarisation sector) — a definition, not a computed sound speed.
- Two of the agent's own errors were fixed before any C1 number appeared (a wrong integrity reference replaced by the Mészáros analytic; a z=100 zero-span crash).
- A 90 s wall-clock cap gave a few TIMEOUT runs (stiff equilibrium starts) counted as FAIL; an earlier uncapped pass showed the same cases collapsing.
- `posthoc_G2_pincer.py` and `posthoc_C2_by_amplitude.py` are post-hoc and labelled.
- **Not tested:** relativistic completion, lensing slip, non-spherical baryons and the AQUAL/QUMOND curl term, mergers/Bullet offsets (Q1 iii structural only), a Boltzmann-code CMB, k = 1e-3/Mpc at z = 1100 (super-horizon for a sub-horizon solver, UNDECIDED), baryon pressure before recombination, bigravity embeddings.
- Literature (Blanchet 2007; Blanchet–Le Tiec 2008/2009; Blanchet–Heisenberg 2015; the Bruneton et al. criticisms; local DM density 0.01 M☉/pc³) is from memory and unverified; no test depends on it.

## Re-running

`./run_all.sh` (B before C, E, S; the C run takes ~15 min), then `./run_rest.sh` for the second footing and the post-hoc scripts. Path handling: `ZF_REPO`, or an ancestor of `__file__`. The committed outputs are the orchestrator's in-place re-run.

## In-place re-run (orchestrator)

Every main, MUTATE, second-footing and post-hoc script was re-run in this directory (`run_all.out`, `run_rest.out` hold the exit codes; they match the agent's: mains 0, MUTATE sign/kernel/recip/nofield 1, MUTATE Q10 0). All `_results.json` are identical to the agent's. The `.out` files differ only in timing lines and in the C runs, where the 90 s wall-clock cap is machine-load dependent: cases the agent's loaded machine logged as `TIMEOUT(stiff, >90s)` were logged by the re-run as `COLLAPSED` at z ≈ 11–43 (e.g. V_U central collapsed runs 5/24 here, 6/24 there, the sixth being a TIMEOUT counted as FAIL). No verdict, gate cell or table number above depends on this; both counts are FAIL.
