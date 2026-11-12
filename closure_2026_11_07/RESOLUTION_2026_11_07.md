# Resolving the contradiction, 2026-11-07 15:xx: the kicked collisionless carrier re-graded at today's needs

Owner: "OK help me resolve the contradiction then" and "have the other lanes on subagents on everything you come up
with". Analysis from the record; no new number here. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

## 1. The record fact that reopens one cell

DEDUCTION_2026_11_07.md closed Cell A (escape by a late kick) on the September lanes L365-L390 (XR13 README, lines
123-138): a cold, kernel-invisible carrier shed from galaxy halos at virialisation with v_k = 575-650 km/s PASSED
S8, the forest, galaxy clearing (intact progenitor v_esc 107-421 km/s, below every kick), cosmic shear, KiDS and
Harvey's merger constraint, and FAILED X-COP and the groups. But the X-COP and group FAILS were graded against
September's requirements, not today's:

| | September rule (XR13) | L388 carrier gives | Today's need (KD1 / SE2 / UA1, current law) |
|---|---|---|---|
| X-COP (every cluster in L388's top bin, M(<1 Mpc/h) 5.0-8.7e14) | retained fraction >= 0.868-1.405 of a LCDM-like halo ("two-sided 20 % rule", "without the phantom") | 0.79-0.85 at 575-650 km/s; linear extrapolation reaches 0.868 at ~546 km/s (not run) | f = 4.2 / 3.8 of M_b = 0.78 / 0.70 of the cosmic 5.4 |
| groups (20 Lovisari) | carrier 0.78-1.08 of the LCDM-like halo | lowest bin retains 0.17-0.34 | f = 1.2-3.5 / 0.9-2.9 of M_b = 0.17-0.65 of 5.4; UA1 step +0.26 / +0.22 dex, fragile |
| galaxies, SPARC, KiDS | cleared | cleared at every kick | f <= 0.33 / 0.19; KiDS firm (KX1) |

At today's needs the top bin's 0.79-0.85 covers X-COP's 0.78 / 0.70, and the lowest bin's 0.17-0.34 sits inside the
groups' 0.17-0.65. Nothing in the September numbers fails today's rows. This is the only cell in the record whose
label rests on a superseded requirement.

Why this is not CE2's fluid: CE2 modelled the late-heated sector as a pressure-supported fluid, which evaporates from
clusters (inner bin +0.48) and is ram-stripped in the Bullet (Mach 1.7-1.9). L388's daughters are collisionless,
produced inside the well at v_k below the cluster escape speed, so they stay bound and pass through the Bullet
(L370: Harvey beta_excess 0.000 with an intact carrier). The record's own numbers separate the two.

## 2. What would make it the resolution, and what still kills it

F1 (cold at z 1100): the parent is cold; passes by construction, CMB lensing kernel at z < 1 to be graded.
F2 (none in galaxies): cleared at every kick >= 450 km/s; KiDS passed in L388; SPARC passes.
F3 (clusters, collisionless, gas-to-stars profile): retention covers X-COP at today's need; the PROFILE against
NA2's band and the per-cluster X-COP rows on the current law (v3s + adopted blend) have never been graded for the
kicked carrier. The Bullet passes (L370).
Groups: retention 0.17-0.34 vs need 0.17-0.65, with a predicted rise of f with group mass: a prediction to grade on
the 20 groups against UA1's posteriors.
The owner's 09-26 rule: the kick must come out of the action (energy the scalar sector releases when the gate
switches on), not be scanned. v_k ~ 550-600 km/s is the measured requirement; whether the adopted action releases
(5.5-6e5 m/s)^2 per unit carrier mass at the switch is a derivation from the certified field equations (QX17D).

## 3. Lanes (all today; frozen criteria first; both footings; MUTATE bites; adopt nothing; subagents inside each)

CK1 (closure coordinator): re-grade the L388 collisionless carrier at v_k in {500, 525, 550, 575, 600, 650} km/s
on GB1 G1-G9 with today's needs (KD1 f-table; SE2/UA1 residue rows; NA2 X-COP per-bin profile band), on the
current law with the adopted blend. Reuse L365-L390's machinery (real_research/) read-only; the trigger is L388's
(shed at halo virialisation). Labels per gate; CANDIDATE only if every gate passes at one v_k on both footings.
MUTATE: v_k = 0 must give KD1 capture; v_k = 2000 must empty X-COP. KA: L388's retention numbers to 0.

CK2 (Field equations session): derive the release speed. From the certified v3s + blend equations (QX17D) and AC2q's
charge switch (EP1/EP2 backgrounds), compute the energy per unit carrier mass released when the switch changes branch
at halo virialisation / the acceleration crossover; report v_k = sqrt(2 E/m) with its uncertainty and whether it
lands in 500-650 km/s. No knob: if the action gives no such term, say so, and the carrier stays phenomenological.

CK3 (Repository session): groups under the kick: predicted retained f versus group sigma for the 20 Lovisari
groups (L388's bins interpolated, both footings) against UA1's joint posteriors; the f-sigma slope is the
prediction. Label PASS / FAIL / NO POWER.

CK4 (KD1 session): cosmology under the kick: daughters produced at halo virialisation (z ~ 1-3) with v_k 550-600,
graded on PR4 CMB-lensing shape (chi^2 <= 18.5 at L <= 400), DESI fsigma8 at z < 1, the forest at z >= 2, and EB1's
early-black-hole timing with the cold parent. Same gates CE2 passed, for the collisionless kick.

KX/CE/RS/UA labels stand. If CK1-CK4 all pass, the contradiction is resolved by a cold carrier that galaxies shed
and clusters keep, and the derivation (CK2) decides whether it is the action's or a new postulate. If any fails,
section 7 of the deduction stands as written.

## DISCLOSURES (added ~16:50 after the paper session's sourcing pass, f68fe972ee; they qualify section 1's table)

D1. L388's retention is eps = M_c,model / M_c,LCDM, a ratio to a LCDM run; its boxes start from CLASS with
    omega_cdm 0.12 (L362 -> L366 -> L377). Under the raw-data / framework-native rule those numbers are NOT evidence
    and NOT a KA for CK1; CK1 must re-measure retention against a framework-native reference.
D2. L388 ran on old footings (a0 9.3619e-11 / 1.1279e-10) and canonical only; only its shear gate was scored on both.
D3. L388's retention is inside 1 Mpc/h, not r500; its top bin holds n = 7 halos; XR13's requirement was computed
    "without the phantom" against retention measured "with the cluster phantoms on". The bins are not X-COP's.
D4. The Bullet's "beta_excess 0.000" is L370's MUTATE (kernel off, nu = 1, LCDM physics); the main run reads
    +0.001 to +0.072 intact. The Bullet row is therefore OPEN for the kicked carrier, not PASS.
D5. "Cosmic 5.4" is not a literal: QX15 states omega_b 0.02236, omega_d 0.1209 and no ratio; QX12 states R = 5.562.
D6. v_k was hand-set in L388 (575, 600, 625, 650) with "the trigger posited (no action)"; CK2 has since found NO
    RELEASE TERM, so the owner's 09-26 rule applies in full.
D7. KX1's frozen label is NO VERDICT on both footings; "kill holds" is the record's reading, not the label.
Corrections: v_esc 107-421 km/s is XR16's, not XR13's; UA1's group medians are +0.259 / +0.221.

Consequence: the sentence "Nothing in the September numbers fails today's rows" is true only of numbers that are
themselves inadmissible as evidence under the record's rules. The candidate stands or falls on CK1's own
framework-native retention and profile, not on L388.

## POST-RESULT (CK1 8e171a71a8, ~15:00): the candidate FAILS on framework-native ground

In the law's own field the escape speed at the release radius is 740-1480 km/s for the massive spirals (v_flat >= 250)
and 4800-6300 km/s for the clusters, not the 107-421 km/s the September lanes quoted. So every kick that a cluster
survives is kept by the big discs too: 9-10 of 10 keep f 1.5-3.9 against the cap 0.33 / 0.19, in every bracket
cell, at every v_k from 500 to 650. The window is closed from both ends. The carrier that clusters keep traces the
gas, not the gas-to-stars profile NA2 requires. CK2 had already found no release term; CK3's group slope was too
steep; CK4's forest ceiling sat at 560. Postulate P3 is dead, and with it this candidate. The deduction's section 7
stands as written, now with Cell A closed on the framework's own numbers rather than on September's.
