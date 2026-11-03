# MB1_member_bound_law: frozen criteria, committed alone, before any script or number of this lane

Owner's go, 2026-11-02: swing more like the closest results. **Question:** the closest results are the law on discs plus a second variable that picks out clusters, and the gas-keyed ones put the extra on the gas, where the Bullet kills them. Can the number of bound members be that variable? Each member keeps its own law halo out to its tidal radius, and those halos then add as ordinary mass, so the extra rides with the galaxies.

A description: no action, no field equation, no particle, no fluid. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 reported apart, never pooled. No LCDM input. The cold sector stays retired and nothing here reinstates it; only the owner can. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read first: FG1, NQ1, UX3, UX6, UX7, MG1, GM1, LM1, KS1, BF2, NM1, RQ3's harness and requirements. I know the law's rows and how UX3 fails. **I also did one hand estimate:** for a 1e11 member at 1 Mpc in a 5e14 host, the phantom mass is about 6 times the stars, the bracket with no truncation overshoots the needed acceleration by about 8, and the external-field radius gives extra mass M_star a0/g_c, about 10 too little.

**Expectation on record.** F is short of X-COP by a factor of 2 to 4 at R500 (65 %). K's X-COP fit needs K about 20-30. K fails keys, because galaxies are more concentrated than the deficit LM1 maps (60 %). Bullet's sign comes out right (85 %, nearly by construction, as MG1 said of N2), and its mass fails in F (70 %). Overall RQ3 reads REJECTED in every arm (99 %), since discs, dwarfs, Milky Way and IC 1613 are the law's by construction.

**Prior work this differs from.** NM1 nested member halos inside the retired sector at a fixed fair-share total, which can only redistribute. Here nothing is fixed: the mass is new and set by the law and the tide. UX6's N2 had the Bullet's sign and no carrier; here the carrier is the member. The real law has no such boost: N-body QUMOND's virial relation gives M^(3/2) - sum M_i^(3/2), which is no gain at large N. So this rule **departs from the law's field equation on purpose**, and it needs "a bound member" to be something the field can read. That is a label until someone shows otherwise. Harness tag [LABEL] will fire and stands.

## Rule
Objects add linearly. A one-object system is the law exactly: discs, lenses, planets, dwarfs, Milky Way, any `sample` not listed below.

For `cluster`, `merger`, `group`:

g = law(g_gas) + g_star + G M_x(<r) / r^2

M_x(<r) = integral from 0 to r of R(r') dM_star(r'), where R is the stellar-mass-weighted phantom ratio at r'.

- **Member.** M_i is the member's stellar mass, with nothing else counted. dn/dlog m is NM1's Schechter shape, log M* 10.9, alpha -1.2, log m 8 to 12.5.
- **Phantom.** M_dyn(<d) = d^2 law(G M_i / d^2) / G, and Delta_i = M_dyn(<r_t) - M_i.
- **R(r)** = integral of Delta_i dn / integral of M_i dn.

## Arms, the whole list. No others without an amendment
| Arm | r_t | Numbers | Runs |
|---|---|---|---|
| **F** | tidal radius, self-consistent: r_t^3 = r^3 M_dyn(<r_t) / ((3 - gamma) M_c(<r)), gamma = dln M_c / dln r clipped so 3 - gamma >= 0.5, r_t <= r, M_c the rule's own total, iterated to 0.1 % | none fitted | harness, keys, own Bullet |
| **E** | external-field radius: law(G M_i / r_t^2) = g_c(r), r_t <= r | none | X-COP, groups, Bullet |
| **N** | r_t = r | none | X-COP, groups, Bullet |
| **K** | none: M_x(<r) = K M_star(<r), K per footing, set by X-COP mean = 0 | one, FITTED on X-COP | harness, keys, own Bullet |
| **KG**, control | as K with M_gas in place of M_star: the same amount, on the gas | one | harness, keys, own Bullet |

K is UX3's protocol moved onto the galaxies, and asks only about the shape. X-COP is K's training set and sits out of its joint, as UX3's did. K and KG read keys and Bullet out of sample.

## Inputs, set here
- **Stars, X-COP:** measured `mstar.fits` through the harness's `gs`, integrated per cluster on its radii from M_star = 0 at r = 0.
- **Stars, keys:** the harness's `gs` is a template that follows the gas, so I don't use its shape. M_star(<r500) comes from it; the shape is NFW c_g 2.9 on R200 = 1.5 r500 (NM1's c_g, its R200 mapping replaced, since NM1 records r_ta as too wide), carried out to the grid's end. Both f* of the harness's key cells stay as they are.
- **Groups:** `gg` and `gs` are NaN in the harness. Gas share f 0.5 at all radii, midway on BF2's assumed 0.3-0.85; f 0.3 and 0.85 reported.
- **Bullet:** UX6's `SYS` and `observe`, unedited, through the harness's `bullet_ns`, with extra = gv (m_gas - 1) + R st, where m_gas = law(|gv|)/|gv|, st is the stellar field. R is one number per subcluster, at d 300 kpc with M_c its own model M300, iterated; K and KG use K st and K gv. **This replaces the harness's B28, which can only hand g a magnitude. The harness row is reported as it reads and isn't used.**
- **Sensitivity, reported, moves no label:** alpha -1.0, -1.4; 30 % of stars in intracluster light with no member; base law(g_b) in place of law(g_gas) + g_star.

## Gates and tolerances
RQ3's `acceptance.py` and `tolerances.json`, unedited, set before this lane. Nothing is widened after a result. Own Bullet row: the same PASS rule as the harness's B28.

## Labels, per arm, per footing
- **NO-NUMBER CLUSTERS** (F, E, N only): B23, B24 pass, 15 of 15 keys, Bullet PASS, B1 PASS.
- **GALAXY SHAPE WORKS** (K only): 15 of 15 keys, Bullet PASS, B1 PASS. A shape result, with the amount fitted. Never a pass of a rule.
- **SHORT / OVER** (F, E, N): X-COP B23 fails, model short or over. The factor in M_x needed is reported.
- **FAILS**: anything else, naming the rows.

**Overall:** "hit" means every RQ3 row passes, as the owner's standing rule says. I expect none. A partial label is a requirement, not a law, and adopts nothing.

**The control must bite.** KG must read Bullet FAIL. If KG passes Bullet, the own Bullet row can't see location, and MB1's Bullet reading is void.

## Checks, before any graded number is read
- **K1** a0 tiny: F returns Newton to 1e-6.
- **K2** Non-listed samples return the law to machine precision.
- **K3** F's r_t against the deep-limit closed form, r_t^2 = r^3 sqrt(a0 M_i/G) / ((3 - gamma) M_c), within 2 % where the deep limit applies.
- **K4** Bullet: LAW reproduces harness M300 1.11, 0.73 (canonical, 1e14). UX6's onBCG control PASS, onGas FAIL.
- **K5** X-COP: M_x = 0 on base law(g_b) reproduces the plain law's mean magnitude 0.467, rms 0.476 (DR1).
- **K6** Keys: units confirmed; a cluster's M_b from gb r^2/G within 5 % of the harness's Mb at r500.
- **K7** Rerun byte-identical.
- **MUTATE:** Bullet R st placed on gv, separate outputs, must lose Bullet sign and exit 1.

A failed check gives NO VERDICT for that arm and is reported as such.

## Limits, stated now
Static. Phantoms sit at their member, so r_t isn't smeared; at r near r_t that's wrong. No orbits, no stripping history, no BCG as a separate object. Circular-orbit tide. Bullet is QUMOND-type with PROVISIONAL sigma (UX6). DISPUTED HSE on X-COP, HSC 1.7 on keys (GM1).
