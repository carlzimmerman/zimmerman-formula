# CT2_local_gravity: review of local gravity for the galaxy law (2026-11-04)

Review lane under `../README.md`. Nothing is re-run; the only new computation is a seconds-long sympy reading (`ct2_stiffness_scaling.py`, `.out`), labelled as a reading, not a frozen gate. κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. No particle; the cold sector stays retired. Not theory closed. Nothing here says the data favour the framework. Literature values are those already in the record (`prep_2026/planetary_doors/BOUNDS.md`, AX1); anything else is marked PROVISIONAL (memory).

## Bottom line

1. **Local gravity is not the open problem; the length is.** The record has one mechanism that passes every local test on both footings: v3s's aether divergence stiffness γ_L(D·P)² with a fixed L★ ≥ 21.7 / 22.9 pc. Cassini Q2 ≤ 2.1e-8 of Hees and ≤ 3.6e-8 of Park (C6, made clean by C6P). The worst planet is Mars at 0.173 of its bound. γ − 1 and β − 1 remainders are ≤ 1.3e-13 and ≤ 1.1e-12 (V3W W1). c_T = c with |Δv/c| ≤ 5.1e-32 (W4a). α1 = α2 = 0 (X15). The only local item still open is W4b, solar-background health: UNDECIDED, with no instability found (V3X). L★ is put in by hand.
2. **The KT17 target (ξ ∝ r_M) is not a local-gravity requirement, and its action form is dead.** Cassini needs only a screen of at least about 0.5 r_M ≈ 0.02 pc at the Sun. A fixed length of 24 pc passes by 1e9 (FN1b, C6). r_M scaling was a Milky Way device. Its variational (reciprocal) form has no joint window: the MW needs ε ≤ 0.313 / 0.465 and Cassini needs ε ≥ 0.516 / 0.593 (KT33/KT34).
3. **No local field-equation key reproduces "screen within ~r_M of each mass" healthily.** Each key was tried and failed:
   - k-mouflage is AQUAL;
   - Vainshtein has the wrong mass exponent and runs inward;
   - potential and density keys fail (screening squeeze, M1 R2b);
   - Weyl and Hessian keys have an Ostrogradsky ghost or a wrong-sign MW force (M1 R2b4, KT40/KT42);
   - the local ratio and tidal rules fail Cassini at the saddle or the MW K_z (CZ5, KT32).

   One new reading (below): a power-law or log divergence stiffness F(D·P) gives L ∝ M^{1/2} only in the logarithmic limit, which is concave (unhealthy) on the physical branch.
4. **For CT1:** within healthy AeST/A33 laws that match SPARC, the planet tail is ≥ 0.96 a0 (theorem T2, M1). That is 1.0e4–7.7e4× the planet bounds, and only γ_L-type stiffness removes it. Any AeST, khronon or aether action CT1 proposes must carry a v3s-type stiffness or an equivalent new length. A k-essence MOND scalar with the law's μ fails Q2 by 2.44–5.19× Hees, whatever kinetic function is chosen within the family that keeps SPARC (D7c, M1 R2c).

## Step 1. Every screening idea on record

| idea | lane (commit where given) | best number | where it failed |
|---|---|---|---|
| Unscreened AQUAL, law's μ | E2 / PAPER58 (021ee82abb / 474050bcd8) | Q2 2.44–4.59× / 2.85–5.19× Hees | Cassini; planet tail 1.3e4 / 1.6e4× at Saturn |
| Unscreened QUMOND, law's ν | D7b | Q2 1.70–3.70× / 1.91–4.03× Hees; simple ν at Park ceiling 7.88× / 9.05× (KT16) | Cassini |
| High-g turn-off (y > 60) | D7b (c6a0b6f3c7 / 9542a09f54) | removes the monopole; Q2 moves ≤ 0.052σ | fixes planets and the LLR tail, not Q2 |
| Sharper μ (β ≥ 2.5, QUMOND) | D7c (e9e5349368 / 26b5db080f) | 0.61–0.95× Hees, canonical | alt E0 1.19–1.23×; not the law |
| Relativistic classes | AX1 (677c5c79a3 and per-class commits) | AeST 2.44–5.15×; BIMOND alt 1.19×; TeVeS, Einstein-aether | GW170817 (TeVeS, E-aether MOND); Q2 (AeST, khronon); DEW static open |
| k-mouflage / capped W (R2c) | M1_trilemma (3298c74815) | least-tense member 1.41× | it *is* AQUAL |
| Galileons L3/L4 of the AeST scalar (R2a) | M1; Galileon no-go scripts (CFG230 Amd 2) | planets need r3 ≥ 900 / 1090 Gpc or r4 ≥ 0.67 / 0.81 Mpc | SPARC −0.68 / −0.54 dex; the mass exponent is M^{1/3}, not M^{1/2} |
| Potential-keyed (chameleon, symmetron) (R2b1) | M1; STANDING screening squeeze | Sun Φ/c² 2.1e-6 is deeper than every galaxy; Pal 14 is 120× shallower | both monotone orders fail |
| Body density, HNS (R2b2) | M1 | star-dominated SPARC −0.17 / −0.18 dex | screens disc stars |
| Ambient density (R2b3) | M1 | needs HI thickness h_z > 371 pc | NO-GO (CONDITIONAL) |
| Weyl / curvature key (R2b4) | M1 | contrast 4.5e-17 vs 8.6e-31 s⁻² would screen | fourth order: Ostrogradsky ghost |
| Hessian generalized QUMOND (ℓ = 3 kpc, p = 9/8) | KT40, KT42 | Cassini passes at fixed ℓ | outward MW force at R12 (156/156); Draco virial < 0; curvature smoothing crosses the ceiling at a ≈ 0.55 / 0.52 pc |
| Fixed-length filter, action form R | FN1b (e6e031a163) | Cassini ≤ 7.4e-10×, planets pass at every L | no length passes: MW 0 cells below 2 kpc; dwarfs need L ≤ 0.1 kpc |
| ξ = ε r_M filter (KT16/17/25) | KT16 (72a296bf17), KT17 (3d4dba837a), KT25 | ε ≥ 0.45 / 0.50 (as published) | KT16's integral dropped an origin surface term: physical 3.69 / 5.91× at ε = ½ (KT33); with the Newtonian host field ε = ½ gives 1.18 / 2.97× (CZ1, CZ2) |
| ξ = ε r_M, reciprocal (action) form | KT33, KT34 | ε = ½: 1.09 / 1.62× Park | no MW–Cassini window (gaps 0.20 / 0.13 in ε) |
| Local rule ξ = \|g\|²/(\|∇\|g\|\| g*) | KT26/27, CZ2–CZ5 (c805085c2f) | 1D 0.004 / 0.02× | 3D: 13.3 / 18.1× at the saddle, 0.75–0.85 r_M sunward |
| Tidal rule ξ_tid (uniform field drops out) | KT28 (c8b2586bb1), CZ2–CZ4, KT29–KT32 (c8248fa630) | Cassini 0.21 / 0.44×; planets 1e-7 | MW K_z: 0 cells once ξ varies in (R, z) (lowest K 84.5–86 vs 66.4 ± 4.4) |
| Bound-region switch (khronon R⁽³⁾) | L342–L352 (STANDING) | Solar System untouched (x ≥ 600) | GW170817 for the R⁽³⁾ form (≈14 h early for the MW; repaired by a shear term); Gauss cancellation; closed |
| v3s stiffness L★ | C6 (1b2ced55a4 / ae428dc252), C6P, V3W, V3X | ≤ 3.6e-8 Park; Mars 0.173 | **passes all local tests**; L★ by hand; W4b UNDECIDED |

## Step 2. The requirement, as numbers

Sun: GM = 1.32712e20 m³ s⁻². Galactic field at the Sun 2.32e-10 m/s² total. With the law inverted, its Newtonian part is g_N,e = 1.653e-10 (y_e 1.766, canonical) and 1.560e-10 (y_e 1.379, alt), as in CZ1.

| quantity | canonical | alt |
|---|---|---|
| r_M = √(GM/a0) | 1.191e15 m = 7959 AU = 0.0386 pc | 1.083e15 m = 7240 AU = 0.0351 pc |
| saddle r_e = √(GM/g_N,e) | 5989 AU = 0.752 r_M | 6166 AU = 0.852 r_M |
| natural Q2 scale a0/r_M | 7.86e-26 s⁻² | 1.04e-25 s⁻² |
| **Q2 allowed (Park 2026, 2σ 5.2e-27)** | **≤ 0.066 a0/r_M** | **≤ 0.050 a0/r_M** |
| Q2 allowed (Hees 2014, 2σ 9.0e-27) | ≤ 0.114 a0/r_M | ≤ 0.086 a0/r_M |
| anomalous radial δg, Saturn (perihelion, 1σ) | ≤ 7.0e-15 m/s² (unscreened tail a0 is 1.34e4×) | 1.62e4× |
| anomalous radial δg, Mars | ≤ 1.4e-15 m/s² (tail 6.7e4×) | 8.1e4× |
| Q2 at the ceiling × Saturn's orbit | 7.4e-15 m/s² (the two bounds are of the same size) | same |
| Moon: Sun's Q2 at the ceiling across the Earth–Moon distance | 2.0e-18 m/s², range ≈ 3.3e-4 mm: **LLR is blind to Q2** | same |
| Moon: mm range ↔ δa ≈ n_syn² × 1 mm | ≈ 7e-15 m/s² (order of magnitude, this lane's arithmetic) | same |
| Moon: equivalence principle (Biskupek+ 2021, Δ(m_g/m_i) 2.4e-14, 1σ) | Earth–Moon differential ≤ 1.4e-16 m/s². If a tail saturates Earth's 8.7e-15 bound, Earth and Moon screening must agree to 1.6 % | same |
| PPN | γ − 1 ∈ [−2.5e-5, 6.7e-5]; \|β − 1\| ≤ 1e-4 (V3W lines) | same |
| GW170817 | c_T/c − 1 ∈ [−3e-15, 7e-16] | same |
| Earth's own r_M | 13.8 AU (the Moon sits at y ≈ 3e7) | 12.6 AU |

**What a screen must do between 1 AU and r_M:**
- **Inside ~30 AU:** cut the monopole tail from a0 to below 1.4e-15 m/s². That is a suppression of ≥ 6.7e4 / 8.1e4. A y > 60 turn-off does it for free in QUMOND, but healthy AeST/A33 laws cannot do it (T2).
- **At 0.3–3 r_M (≈ 2000–24000 AU), where g ≈ g_e ≈ a0:** cut the anisotropic part of the phantom so that the tidal field at the Sun is ≤ 6.6 % / 5.0 % of a0/r_M. Plain QUMOND gives 7.9 / 9.1× that (KT16).
- **Do it on the 3D vector field.** The total field has a zero at the saddle (CZ5).
- **Leave the EFE intact for dwarfs.** CZ1 E1 gives 18/24 with the Newtonian host field.
- **Galaxy side-effects:** the screen must stay below about 0.1 kpc in dwarfs (FN1b R form) or 22–90 pc (v3s L★, X27).

**The plain law with the Galactic field, from the record:**
- **Planets:** FAIL by 1.3e4–8.1e4. With the y > 60 turn-off, PASS.
- **Cassini Q2:** FAIL. QUMOND 1.70–4.03× Hees; AQUAL 2.44–5.19× Hees; 7.9 / 9.1× Park (KT16, MOND-field convention). A plain number at CZ1's Newtonian convention is not on record. CZ1 moved the filtered forms up by about 2.5×.
- **LLR:** the Q2 part PASSES by about 1e3. The tails FAIL without the turn-off. The Sun's tail differential is 2.4 / 2.9e-13 m/s², of order 4–5 cm. Earth's own tail is a0 at the Moon, of order 1e4× the mm scale. Both are estimates, not lane results. Both vanish with the turn-off.
- **GW speed:** not defined (the law is non-relativistic).
- **γ:** not defined.

## Step 3. Mechanisms that come from a field equation (5, checked against the record)

| # | mechanism | why r_M would emerge | Cassini | c_T | status / first kill test | CT1 class |
|---|---|---|---|---|---|---|
| 1 | k-mouflage P(X) keyed on \|∇φ\| vs g* = c√(Gρ_DE) = a0/κ | exactly: r_K = √(GM/g*) = √κ r_M = 0.707 r_M | AQUAL: 2.44–5.19× Hees | = c (conformal), but then no extra lensing (G3) | **CLOSED** (D7c, M1 R2c, DHF 2024 8.7σ). The screen is the MOND transition itself, so it can't hide the EFE quadrupole made there | k-essence: this is the warning |
| 2 | Vainshtein / Galileon | no: r_V = (2 r_M² c²/a0)^{1/3} ∝ M^{1/3}. With Λ tied to a0: Sun 453 / 399 pc = 1.2e4 r_M; MW (6e10) 1.8 / 1.6 Mpc = 190 r_M; 1e8 dwarf 540 r_M | passes (screens everything) | cubic = c; quartic/quintic fail GW170817 | **CLOSED** (M1 R2a: planets need r3 ≥ 900 Gpc, SPARC −0.68 dex; no-go scripts: runs inward) | Horndeski add-on to AeST |
| 3 | Nonlocal kernel with ξ = ε r_M | put in by hand through "system mass". Local proxies fail (LOC at the saddle, TID at MW K_z) | reciprocal form at ε = ½: 1.09 / 1.62× Park; passes for ε ≥ 0.516 / 0.593 | no relativistic form | **CLOSED** for the record's baryon family (KT34 gap 0.20 / 0.13). A ρ_DE-set ε (κ = 0.5 or √κ = 0.707) sits outside the MW band | none |
| 4 | Aether / khronon divergence stiffness (v3s γ_L(D·P)²) | does not: L★ is fixed (≥ 21.7 / 22.9 pc). System-scaled variant, this lane's reading: with F(D) = λ\|D\|^n/n in C6's balance F'(D) = GM/r, the screen ends at L ∝ M^{−1/(n−2)}. Exponent ½ needs n → 0, i.e. F = k a0² ln D, which gives L = 2 r_M/√k but F'' = −λ/D² < 0 (concave) on the D > 0 branch. Every convex n > 1 gives exponent > 1 or < 0 | ≤ 3.6e-8 Park (fixed L★) | = c, ≤ 5.1e-32 | **OPEN, the only local survivor.** First kill test: W4b health at the β = η = 0 point (l ≥ 1 ladder within 5 %; tensor roots within 1e-10) at higher precision. Then derive L★: from (G, c, a0) alone the only length is c²/a0 = 31 / 26 Gpc | AeST, khronon, aether: native |
| 5 | Tidal / Weyl key (Galilean-symmetric, so a uniform field drops out and "which mass" is answered by the system's own tide) | ξ_tid = r_M/2 deep in an isolated system (KT28's 4/√3) | 0.21 / 0.44× (TID); curvature smoothing 7.2 / 8.3× at 1 pc (KT42) | not built | **CLOSED**: fourth order gives a ghost (M1 R2b4); the generalized-QUMOND form gives the wrong-sign MW force (KT40/42); MW K_z fails (KT32). Its healthy first-order relative in aether language is #4 | aether (via #4 only) |

**About #4's reading:** it is scoped to power-law and log F of D·P in the static C6 equation, with the screen edge set at |p| = a0. The control (n = 2) gives C6's constant-|p| hedgehog (dp/dr = 0). The physical branch is D > 0, which v3s's max(D, 0) keeps. The convex-looking λ < 0 branch needs D < 0: an inward hedgehog, unbounded below at large |D|. It is not a graded theorem.

## Step 4. Gated sequence for any candidate action (numbers frozen here; stop at the first FAIL)

- **G0. Record gate (no compute).**
  - Write the static weak-field limit.
  - If it is AQUAL or QUMOND with the law's μ and no new length: **FAIL** by the record (Q2 1.70–5.19× Hees; tail 1.3e4×).
  - If it is a healthy AeST/A33 law without stiffness: **FAIL** by T2 (tail ≥ 0.96 a0).
- **G1. Cassini Q2 (seconds).** Point Sun in a uniform Galactic field, on the 3D vector field.
  - **PASS** iff Q2 ≤ 5.2e-27 s⁻² at both host-field conventions: Newtonian g_N,e 1.653e-10 / 1.560e-10 (primary) and the MOND convention (beside).
  - Hees 9.0e-27 is reported beside.
  - Use the physical Hessian, with no dropped origin surface term (KT33).
  - Known answers: plain simple-ν QUMOND gives 7.88 / 9.05× Park (KT16, to 1e-4); C6 at L★ 24 pc gives ≤ 3.6e-8.
- **G2. Planets and the Moon.**
  - Anomalous radial δg ≤ 1.4e-15 (Mars) and ≤ 7.0e-15 m/s² (Saturn), or Z ≤ 2 on the AZ12 precession gate.
  - Earth-centred anomalous acceleration at the Moon ≤ 7e-15 m/s² (order-of-magnitude line; replace it with a published LLR bound before grading).
  - Earth–Moon screening difference ≤ 1.4e-16 m/s².
- **G3. PPN.** γ − 1 ∈ [−2.5e-5, 6.7e-5]; |β − 1| + the non-PPN remainder at Mercury ≤ 1e-4; α1 = α2 = 0, or within published bounds (look-up owed, PROVISIONAL).
- **G4. GW and health.**
  - c_T/c − 1 ∈ [−3e-15, 7e-16], derived on three backgrounds: FRW, a galactic one with |∇φ| ≈ a0, and the solar one.
  - Every ω² > 0, with no ghost, on the screened solar background.
- **G5. Galaxy side-effects (hand to CT4).**
  - Dwarfs E1 ≥ 15/24 (plain 18/24).
  - SPARC on KT19's frozen line.
  - MW ≥ 1 in-prior cell on KT17's lines.

The order is cheapest and most discriminating first. A v3s-family action already holds G1–G3 and G4 c_T, so for it the sequence starts at G4 health (W4b) and at deriving L★.

## What is genuinely untried
- A derivation of L★, or of any 22–90 pc constant, from the action. No (G, c, a0, ρ_DE) combination gives one.
- A plain-QUMOND Q2 at CZ1's Newtonian host-field convention.
- A real LLR grade of the tails. Only order-of-magnitude estimates exist (this lane; BOUNDS.md §1.5).
- DEW's static non-spherical limit (AX1 Unfinished).
