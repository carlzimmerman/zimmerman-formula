# PAR1 AMENDMENT A2 (POST HOC, committed alone, after the result landed; before the known-answer check below is run)

Criteria 51522963e0; A1 427bc818f6; result c8d1463e35 (origin 6be0bf30d1). The coordinating session asked for one more
input after the result landed: `closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md` (origin c39b1272f1). It is a design
note, not a lane: no criteria, no label. This amendment adds its cited theorems to the spec as conditions, each with its
source lane. It adds one known answer, recomputed independently in SI, and states how each condition bears on PAR1's
branches. Nothing is re-derived. Everything in sections 1 and 3 was written from the cited statements before the check
in section 2 was run.

## 1. New spec conditions (cited, not re-derived)

| # | condition, as its source states it | source (read) |
|---|---|---|
| C16 | **M5.** The two premises exclude each other for a local, momentum-conserving medium that couples to the baryons only through gravity: "the law is the medium's equilibrium for every baryon distribution" and "the medium self-gravitates normally, with no hold". (S1, S2) Exactly one local stress makes the law the equilibrium: Pi_ij = [chi d_iPhi d_jPhi - K(s) delta_ij]/(4 pi G), with chi = 1 - mu. It cannot depend on rho_c. (S4, R2) As the medium's dynamics it is Hadamard ill-posed; with stiffness, the equilibrium is not an attractor (ln A median 59 / 67 on SPARC). (S5) In the deep regime it cancels the medium's nonlinear self-gravity: top-hat delta_c 13.6 against 1.686 | `rebuild_2026_10_22/M5_equilibrium_law/README.md` |
| C17 | **Z1 family 6, every local selector closed:** Theorem G (gates in theta and u; CFG944: "for any local L(theta,u), ghost freedom + the static law + a tether off in the linear universe force a static vacuum offset B >= W(u*) = 0.71 / 0.62 a0^2/K, 15-25x what slip allows"); Theorem S (CFG945: any label-free tether hovers at leading order); D-T' (CFG946: any local holding force cancels the felt self-gravity, for any source multiplicity); the mu-pincer (pressure cannot keep the cold mass out of galaxies; STANDING.md:296); J1 (potential depth); V1 (density) | `rebuild_2026_10_22/Z1_successor_design/FAMILY_SCORES.md` lines 49-50 and its sources: `campaign_fresh_gravity/LEDGER.md` lines 705, 707, 709 and STANDING.md:296. J1 and V1 are quoted from Z1 only; Z1 sources them as TD:96 and TD:114, not re-read |
| C18 | **T-O2 (CFG946).** Assume dust cold energy, local second-order universal sectors, a profile-independent deep BTFR and no EFE. Then the deep extra force must be the dust's own mass: cold energy IS the phantom. Holding that dust then cancels its self-gravity. Lemmas: L-G (any field that supplies the deep law has an EFE) and N-L (a field-supplied deep law has no linear regime about FRW) | `campaign_fresh_gravity/LEDGER.md` line 707 |
| C19 | **AKD1.** Dust stiffness keyed on the clock's acceleration: BREAKS AT A1 (a ghost on FRW for z > 11.6; any decreasing M_2(Y) fails in wells) | already in C12; `closure_2026_11_10/AKD1_acceleration_keyed_dust/RESULT.md` |
| C20 | **MEDIUM_DESIGN section 3.** A cold medium in thermal contact with baryons where their acceleration exceeds a0 needs opacity pi G/a0 per unit baryon mass, and then: (1) it is dragged by the plasma at recombination (drag rate 0.73 / 0.61 of the expansion rate at z 1100 for 30 km/s); (2) a cluster's gas column (0.1 to 0.7 optical depths) drags it, against the Bullet. A hand check, not a lane | `closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md` section 3 |

## 2. Known answer (frozen here; run after this commit)

KA-MD: recompute section 3's SI numbers with an independent script (`par1_medium_ka.py`; the note's own script is not
run or imported). The inputs are the note's: G, a0 per footing, h 0.674, Omega_b 0.0493, Omega_m 0.3147, Omega_r
9.15e-5. Lines:
- opacity pi G/a0 = 22.4 / 18.5 cm^2/g, to 0.5 %;
- mean free path at z 1100 = 25.8 / 31.1 pc, to 1 %;
- drag rate at 30 km/s and z 1100 = 0.73 / 0.61 of H, to 0.01.

PASS iff all three hold on both footings. MUTATE MU5: opacity G/a0 (pi dropped). It must miss the opacity line on both
footings.

## 3. How the new conditions bear on PAR1's branches (reading fixed here, before the check)

Rule: a cited theorem moves a branch to EMPTY only if its stated hypotheses cover every member of the branch. Otherwise
it is listed as a condition the branch's members must evade, with the reason the coverage is not established.

| branch (A1 label) | C16 M5 | C17 Z1 family 6 | C18 T-O2 | C20 contact | effect |
|---|---|---|---|---|---|
| B0 (EMPTY) | - | - | **covers**: a law from a separate sector with dust kept double-counts, so cold energy must be the phantom (an independent second closure of B0, and of WV1's V2) | - | none (already EMPTY) |
| B-L (EMPTY) | - | - | - | - | none |
| B-Ts (EMPTY) | consistent: (A)'s clock is M5's row (b) once relaxed | consistent: Theorem G, the mu-pincer, J1 and V1 close the gated and keyed versions | - | - | none |
| B-Tm-fine (OPEN) | **not established.** M5's S2 assumes a stress Pi(rho_c, grad Phi). In B-Tm-fine the hold acts through the wave's own phase-frame acceleration, which is zero in free fall, so M5's equilibrium stress applies only once relaxed. R2 and S5 become conditions to evade: the static state must be reached and held despite M5's non-attractor row | **not established.** Theorem G assumes a tether off in the linear universe built from (theta, u). The wave's phase frame needs no gate: it is geodesic at linear order (A = 0), so whether G's hypothesis is met is not settled here | consistent (counted once is assumed by Pi3) | outside Pi1 (contact coupling) | none; conditions listed |
| B-Tm-smooth (OPEN) | **not established**, same reason: the hold switches on only where the coarse-grained mean frame is static | **not established**: the alignment coupling is ungated, and the law switches off on the web because the aligned frame is geodesic at linear order. A member must still show it evades Theorem G's vacuum-offset bound and D-T' (a local hold cancels the felt self-gravity inside halos) | consistent | outside Pi1 | none; conditions listed |

Labels: no branch label changes under A2, so the lane label stays NO VERDICT / NO VERDICT, unless KA-MD fails. If it
fails, C20 is recorded as not reproduced, and still no label changes, since C20 bears only on a class outside Pi1.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
