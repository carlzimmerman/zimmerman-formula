# CT1_action: review of requirement 12 (an action that sets a0 = kappa c sqrt(G rho_DE) dynamically)

Review lane under `complete_theory_2026_11_04/README.md`. Nothing was rerun. The only arithmetic here is the three kill-test numbers in Step 3, worked by hand in one python line each. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. Not theory closed. Nothing here says the data favour the framework. No particle, and the retired cold sector is not reinstated. Literature entries are PROVISIONAL: abstract-page search snippets from 2026-11-04, or memory. Nothing was downloaded.

**Bottom line.** The record suggests the answer is probably no. Every class on record fails in one of three places: an unscreened Solar System, a broken cosmology, or a0 put in by hand. Tying a0 to rho_DE with slope 1/2 is easy, and the record has done it many times (four-form, Henneaux-Teitelboim, the CFG911 portals). Each time it is a TRADE: kappa^2 equals a free coupling, and the open piece stays xi = 1. No action on record contains a tie, a screen and c_T = 1 together. I found two classes not on record. Neither is expected to supply kappa = 1/2.

## Step 1. Every action class on record

| class | what it achieved | where it failed (number) | lane / commit |
|---|---|---|---|
| AQUAL / QUMOND / RAQUAL | static law exact | Cassini Q2 2.44-4.55x Hees (AQUAL) and 1.69-3.68x (QUMOND); planets 1.3e4-1.6e4x; a conformal scalar gives no extra lensing | AX1 AUDIT 677c5c79a3 |
| BIMOND | law with a sharper beta >= 2.5 on canonical only | alt E0 1.19-1.20x Hees; canonical G4 (GW) [PROVISIONAL] | AX1 fd417eea04 / ffd6f71b2a |
| TeVeS | law | GW170817 | AX1 |
| AeST (SZ21) | law plus CMB-capable dust | Q2 2.44-5.15x; alpha_1 = -22/5 (static branch; AS3 shows it is an artefact for moving sources); H1: no F(Y,Q) family member passes (health at Y = 0 against the MOND limit); H2 cannot supply the cluster excess; AN1 and AN2 NO VERDICT | AX1 7b7d1a7811/360bf66de8; H1 1654b84f78; H2 385f61a14c; AN1 a3ce1814c5; AN2 f04da07be4 |
| khronon (Blanchet-Marsat) | law | Q2 as AeST; G2c open | AX1 6b618b184d/6d20d2bbc9 |
| Einstein-aether MOND (Zlosnik-Ferreira-Starkman) | law | GW speed depends on the potential; \|c13\| <= 1e-15 | AX1 |
| superfluid (effective field) | different law | sqrt(a0 g_N) at Saturn 1.1e7 / 1.2e7 x the bound | AX1 |
| nonlocal metric MOND (DEW) | open on canonical only | alt E0 1.19-1.47x | AX1 cd18cad5dd/04cbb9ddb5 |
| **v3s (Khronon + P, switched stiffness, L* >= 24 pc)** | G1-G4 reading PASS; Cassini clean PASS (Q2 >= 4.85e7 inside Hees); c_T = c; 3 DOF | clusters 1.5-1.7x the law; sigma8/sigma8,dust 0.003-0.005; BBN needs mu_K >= 1.84e8 h/Mpc; hosted dwarfs (Antlia II 24 sigma); MW K_z 92-97 vs 66.4; caustics; carries its own dust; **a0 by hand** | V3S verdict; C1-C8; C6P 8c5703da06; V3X ee4210e959 |
| khronon + scalar with (D^2 chi)^2 (v3's scalar pair) | Q2 margin 2.8e7 / 4.0e7 | FRW growth: sigma8 ratio 0.0757 / 0.0817 against 0.95 | AS3 6770f2d8ad |
| AS2 enumeration (8668 templates) | | Tier A 0 of 717; a screen plus a dust is over budget | AS2 102c3e16bf |
| smoothed QUMOND with one fixed length | static Cassini passes at every L | no universal length passes on either footing: MW needs about 2 kpc, dwarfs <= 0.1 kpc | FN1b e6e031a163 / 22f8e50070 |
| curvature- and tidal-filtered generalized QUMOND (KT37-KT42) | MW four cuts plus Cassini at p = 9/8, ell = 3 kpc | dwarfs 12/24 against 19/24 plain; outward force in the MW; negative virials (KT40) | KT35-KT42, **uncommitted, another session** |
| VCDM + f(a^2) (trace-constrained, CMC-like) | | negative matter kinetic coefficient on FLRW at f_s(0) = 1 | `qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/FLRW_OBSTRUCTION.md` |
| cuscuton bridge | | no rolling de Sitter with a constant vacuum; linking a0 to it moves H and a0 together | `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/cuscuton/` |
| one aether function F(c2 K^2 - c1 a^2) | healthy de Sitter branch | the static MOND branch and the vacuum branch are separate; a deformation moves the vacuum and leaves a0 fixed (non-selection) | W4-08 `unified_invariant/SINGLE_FUNCTION.md` |
| chi portal / mu_n action | an exact action for mu_n; explains the 2 | kappa = 1/(2b), with b = premise A; KT3 needs DU = 8 pi; KT5 c_E = 1 is an input; KT6 w > 0; KT7 no-go in its class | KT2 3004271e49; KT3-KT7 |
| four-form / HT / unimodular ties | a0 proportional to sqrt(rho_DE), slope exactly 1/2 if C0 = 0 | TRADE: kappa^2 = 2 beta^2/Z free; C0 = 0 has no name; AS652 "a0 environmental" | K208 2fb80ca12, K617/K618, K594 a075ad7f7, CFG187 7be5e8637 (1/2 written in), p63 5df0e1cd84 (C1 INCONSISTENT, C3 FREE) |
| CFG911 portals S ⊃ lambda[a0^2 - xi G F(T_DE)] | tie for every stress F; running law d ln a0/d ln a = -(3/2)(1+w); N6 canonical quintessence locally silent (<= 4e-11) | TRADE: kappa^2 = xi | CFG911 1ff4510ee |
| sequestering / self-tuning | | TRADE or condition (K206 five orders short; K279; self-tuning B(X), B(Theta): h stays an action scale) | `reviews/self_tuning_selector_2026_10_24` |
| stiffness-term vacuum as DE (door D1) | | wrong sign; behaves as H^2; 1e-19 to 1e-15 of critical; kappa >= 1e7 | CFG897 4c7a17d27 |
| k-essence / P(X) / deep-MOND attractor; Berezhiani-Khoury seesaw | | free multiplier; kappa^2 = 8 pi/q; kappa^2 = alpha^6 TRADE | K102, K339, K643 |
| horizon entropy, Verlinde | 0.482 at the data level | SPARC shape fails (p34 Delta chi^2 +1389; CFG117 G1 0/16) | K038, K489 and others |

## Step 2. The gap

These are the properties no action on record has together:

- **P1, the tie by a field equation.** Ties exist (four-form, HT, CFG911), but never inside a screened host.
- **P2, xi = 1.** No route supplies it. The kappa closure (K840, K843) reduces every route to it. The four walls are: c is required; a0-and-H-only routes give kappa^2 in Q·pi^odd; a0 carries no hbar; the vacuum zero mode is free.
- **P3, screening.** Only v3s's L* passes the Solar System, and L* is a second scale put in by hand. A fixed Gaussian length fails (FN1b).
- **P4, c_T = 1.** This is easy in the khronon and four-form classes; aether, TeVeS and BIMOND lose it.

**Which of these constrain each other:**
- **P1 and P2.** Any tie gives kappa^2 = coupling. The tie is cheap; ½ needs a pi-free normalisation that no GR equation provides.
- **P1 and P3.** A tie through a constraint field (four-form, HT, CMC multiplier) responds algebraically to the local MOND energy, so a0 becomes environmental. A tie through a propagating, Planck-stiff field is silent (CFG911 N6), but its normalisation is still free.
- **P3 and cosmology.** A healthy screen plus the dust the CMB needs goes over the AS2 budget. In v3s the screening field and the dust field are the same (alpha ≡ 1), and that is the root of the 10-24 failures.
- **P4** constrains nothing else, as long as the host is a khronon or a scalar.

## Step 3. Classes not on record (checked with grep)

Excluded as already on record: unified k-essence or superfluid (K102, K339, K643, AX1). It also fails w ≈ -1, because the DE branch has to sit where P_X ≈ 0, which leaves its perturbations strongly coupled, while the MOND branch needs P_X ≠ 0. Also excluded: AeST with a0 as a function of Q (H1, K353, CFG187), horizon entropy (Verlinde rows), sequestering (K206, K279, K303), and cuscuton or VCDM (see Step 1).

**A. v3s-T: a four-form tie inside the screened Khronon + P action** (a recombination; never graded jointly)
- **Action sketch.** S = S_v3s with a0^2 -> xi G q^2/c^2, plus ∫ [-Z q^2/2] with q = *F4, where q's energy is rho_DE.
- **Why a0 ∝ sqrt(rho_DE).** rho_DE = Z q^2/2 if C0 = 0.
- **kappa.** kappa^2 = 2 xi/Z: a TRADE. It does not supply xi = 1.
- **First kill test.** The q equation fixes ∂L/∂q to its cosmic value, so q shifts by the local MOND-sector energy. That energy is about a0^2/(8 pi G), which is kappa^2/(8 pi) ≈ 0.0099 of rho_DE c^2. The expected |δ ln a0| is O(0.01) between void, field and cluster. It must stay under the record's environment slope, -0.010 ± 0.015 (CFG911), i.e. ≤ 0.015 dex.
- **What it avoids and what it still faces.** It removes "a0 by hand" in exchange for xi. It inherits all of v3s's failures: clusters, growth, BBN, hosted dwarfs, the MW disc, and v3s's dust term.

**B. Lambda-projector khronon** (not found by grep in an action): the MOND scale is built from the foliation's own expansion.
- **Action sketch.** The MOND function's scale is a0^2 = xi c^2 Q, with Q = K^2/3 + (2/3) L_n K. On FRW this equals Lambda - 8 pi G p/c^2 exactly, so pressureless matter cancels.
- **Why a0 ∝ sqrt(rho_DE).** For w = -1 it gives a0 ∝ sqrt(Lambda), with no separate DE field. It is the record's pressure link (CD26-3) made geometric.
- **kappa.** kappa = sqrt(8 pi xi): a TRADE.
- **Kill test 1, Ostrogradsky.** L_n K carries K-dot, so the DOF count in unitary gauge must be degenerate, or the class dies.
- **Kill test 2, local constancy.** It needs |δQ/Q| ≤ 0.05 at r ≤ 30 kpc. With matter-comoving leaves, (v/r)^2 / (Lambda c^2) ≈ 4.3e4 at 200 km/s and 10 kpc. So it needs CMC-locked leaves, which X15's lambda-term gives, and then it must face the VCDM FLRW obstruction.
- **Kill test 3, radiation era.** Q < 0 for z > 11.3, where (1+z)^4 = 3 Omega_L/Omega_r. a0^2 turns negative before z ≈ 11, which CT3 must accept or reject.

**C. CFG911 N6 inside v3s** (Planck-stiff quintessence with a potential portal; a recombination)
- **What it does.** It is locally silent (≤ 4e-11), so Cassini and the environment slope are untouched. It predicts the running d ln a0/d ln a = -(3/2)(1+w) under DESI's w(z).
- **What it leaves.** kappa^2 = xi, and every v3s failure.
- **Kill test.** a0(z) at z ≈ 2.5 to 0.10 dex (CFG689 P6, AT1's rule). It is the cheapest to grade because the local sector is unchanged.

## Step 4. Gated plan (freeze before computing; ordered by how fast each candidate dies)

| order | gate | line | B | A | C |
|---|---|---|---|---|---|
| 0 | DOF / Ostrogradsky count in unitary gauge | no ghost, no 4th DOF with negative kinetic sign | first | trivial (q is non-propagating) | trivial |
| 1 | weak-field limit is the law (both footings) | max deviation ≤ 0.01 dex over y in [1e-3, 1e3] | yes | yes | yes |
| 2 | local constancy of a0 | \|δ log a0\| ≤ 0.015 dex for void / field / cluster at 30 kpc | 4.3e4x unless CMC | expected ≈ 0.004-0.01 dex: the deciding gate | ≤ 4e-11 |
| 3 | a0 ∝ rho_DE^s with s = 0.5 | \|s - 0.5\| ≤ 0.01 on an analytic w(z) | yes if w = -1 | needs C0 = 0, named | yes (potential portal) |
| 4 | Cassini Q2 below Hees (9.0e-27 canonical), planets | Q2 / Hees ≤ 1 at L* ≥ 24 pc | open | inherit C6P only if gate 2 holds | inherits C6P |
| 5 | c_T = 1 | \|c_T - 1\| ≤ 1e-15 | the K^2 term is OK; check L_n K | yes | yes |
| 6 | cosmology | handed to CT3 | z > 11 sign flip | v3s's failures | v3s's failures |

- **Expected outcomes.** C passes 1-5 and changes nothing physical: it renames "a0 by hand" as "xi by hand". A is decided at gate 2. B most likely dies at gate 0 or 2.
- **What none of them can do.** No candidate here can pass P2. kappa = 1/2 stays FITTED unless a pi-free portal appears (KAPPA_CLOSURE section 5).
- **What this means for requirement 12.** A could not close it. C would only restate v3s; so would A even if it passed. Requirement 12 as a whole theory is blocked by v3s's alpha ≡ 1 cosmology, not by the tie.

## Sources
- Record: the files and commits named in the tables above.
- Web (PROVISIONAL, abstract pages only): [1110.2580](https://ar5iv.labs.arxiv.org/html/1110.2580) (a scaling relation, not an action); [2203.05606](https://arxiv.org/abs/2203.05606); [astro-ph/0505266](https://arxiv.org/pdf/astro-ph/0505266) (I read only its search snippet; I did not open the PDF). None of them gives a covariant action that derives a0 from rho_DE.
