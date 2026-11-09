# SS5 (baryon-component segregation, the outside source's variant L): FROZEN CRITERIA, committed alone before any SS5 script or number

TEST lane, quarantined; registered RUNNING by the orchestrator. Adopts nothing; no particle adopted. kappa = 1/2 FITTED; not
theory closed. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. SS1 machinery (ss1_cosmo.py prefix:
CLASS reference, background) is used read-only.

## 1. Construction L, frozen once (as relayed)

- **Matter content.** No conversion and no pressure. The component (R omega_b, pressureless at all z) feels only the Newtonian
  field g_N, sourced by component + baryons.
- **Baryons** feel the law, g = nu(|g_N| / a0) g_N, with nu(y) = 1/2 + sqrt(1/4 + 1/y) (the record's law).
- **The law acts on the peculiar field.** The background expansion is the GR background (the record's convention: SV5 / CFG,
  "the law on the web"). So the baryons' peculiar acceleration is nu(|delta g_N| / a0) delta g_N, with delta g_N the
  perturbation's own Newtonian field.
- **Claimed mechanism:** a relative drift of about v_stiff (265.8 / 288.1 km/s) leaves isolated galaxies R_seg = v_stiff /
  H(z_turn 1.2) = 3.45 / 3.74 Mpc from their intact component clumps; groups and clusters capture
  f_cap = (1/sqrt 3) exp(-u^4 (1 + u^2)), with u = v_stiff / v_vir.
- **Form choices beside the label:** the 1/sqrt(3) cap (SS1 found it did no work in I), the u^4 (1 + u^2) capture law,
  R_seg's formula, z_turn = 1.2.

## 2. The decisive tests (dynamics, not bookkeeping)

**D1, linear two-fluid growth from recombination.**
- The equations (ln a as time, the footing's CLASS reference background):
  - delta_chi'' + (2 + dlnH) delta_chi' = (3/2)(Omega_chi delta_chi + Omega_b delta_b);
  - delta_b'' + (2 + dlnH) delta_b' = (3/2) nu(k, z)(Omega_chi delta_chi + Omega_b delta_b).
- **Baryons** start at z 1090 with delta_b = 0 (released from the photons), the component in the growing mode.
- **nu(k, z):** nu(y) with y = |delta g_N| / a0 at the scale. delta g_N = (3/2) H0^2 Omega_m delta_rms(k, z) / (a^2 k)
  (k comoving), and delta_rms = sqrt(k^3 P_lin(k, z) / 2 pi^2) from the CLASS reference.
  - This is a prescribed coefficient (the record's convention for the law on linear scales), disclosed.
  - Bracket D1-N: nu = 1 (Newtonian baryons), as the null.
- **Reported** at k = 0.1, 0.3, 1, 3 h/Mpc and z = 3, 1.2, 0:
  - delta_b / delta_chi;
  - the cross-correlation coefficient r(k, z) = <delta_b delta_chi> / sqrt(<delta_b^2><delta_chi^2>). Both species are linear
    functionals of the same initial field, so r = 1 identically unless a decaying mode differs; the run prints it.
  - the relative velocity theta_b - theta_chi, as a drift in km/s.

**D2, collapse with both species.**
- **(a) Spherical.** 200 shells of each species, physical coordinates.
  - Equation: r'' = -G M_bg(<r) / r^2 + H0^2 Omega_Lambda r - F_s G delta M(<r) / r^2, with F_s = 1 for the component and
    nu(G |delta M| / (r^2 a0)) for baryons; softening 1 kpc.
  - Initial state: z 200, a Gaussian overdensity of total mass 1e12 Msun (component 84 %). Its amplitude is set so the
    Newtonian top-hat would collapse at z 1. Both species start co-located in the growing mode (bracket: delta_b,i = 0).
  - Reported at z 3, 1.2, 0: each species' half-mass radius (inside the turnaround region), and the baryon mass fraction
    inside the component's half-mass radius.
  - In spherical symmetry the two centres cannot separate, so (a) tells only the radial direction: do baryons end up more
    or less concentrated?
- **(b) 1D plane-parallel N-sheet** (the only way a centre can move).
  - A periodic comoving box of 20 Mpc, 2000 sheets per species.
  - Initial state: two offset Gaussian peaks of different amplitude and width, the same for both species, at z 200. The
    larger peak's linear Newtonian amplitude reaches collapse at z about 1.
  - Equation: comoving x'' + 2 H x' = g / a, with the 1D plane field for g_N (periodic, mean removed); baryons get
    nu(|g_N| / a0) g_N.
  - Reported: the density-peak position of each species (smoothed 0.1 Mpc) at z 3, 1.2, 0, and the peak offset in comoving
    Mpc. This is the record's best available proxy for "R_seg" (stated as a proxy).

**Label rule (mechanism).**
- **D-FAIL:** "FAIL at the mechanism" iff all of the following hold:
  - D1 gives r >= 0.99 at every (k, z) graded, and delta_b / delta_chi >= 1 at z <= 1.2 (baryons trace or exceed the
    component on the same peaks);
  - D2(a) gives the baryon half-mass radius <= the component's at z 0;
  - D2(b) gives a peak offset < 0.35 Mpc (one tenth of the claimed R_seg) on both footings.
- **D-SEP:** if separation appears (D1 r < 0.99, or D2(b) offset >= 0.35 Mpc, or baryons less concentrated than the
  component), D3 is run as relayed (KiDS via option (c), groups, X-COP, P(k), cross-correlation / bias, forest, Bullet,
  Coma UDGs) with SS1-SS4's lines. The label is then the gate table's.
- **NO VERDICT** if a known answer fails.

## 3. Known answers

- **KA-L1:** D1 with nu = 1 gives delta_b -> delta_chi (r = 1, ratio -> 1 by z 0 to 1e-2): the baryon catch-up.
- **KA-L2:** D2(a) with nu = 1 for both reproduces the Newtonian top-hat collapse redshift of the frozen amplitude
  (z_coll 1 +- 0.1).
- **KA-L3:** D2(b) with nu = 1 gives peak offset < 0.02 Mpc (identical dynamics).
- **KA-L4:** the background of the ss1_cosmo reference: h and z* as SS1.

## 4. MUTATE

- **ML1:** a planted relative velocity of v_stiff (265.8 / 288.1 km/s) between the species at z 1.2 in D2(b). The offset
  must then grow to >= 0.35 Mpc (the test can see segregation when it is put in); otherwise the D2(b) test has no power and
  the label is NO VERDICT.
- **ML2:** baryons Newtonian (nu = 1) in D2(b): offset 0 (as KA-L3).

## 5. Hand estimates (before any number)

- **D1:** on linear scales y = |delta g_N| / a0 is about 1e-3 to 1e-1, so nu is about 3-30. Baryons fall about nu times harder
  into the same wells, and delta_b / delta_chi >> 1 (the law on the web, SV5). r = 1.
- **D2(a):** the baryons collapse earlier and end more concentrated than the component (the orchestrator's expected sign).
- **D2(b):** both species' peaks sit at the same place (offset at resolution). The drift points along the same gradient, so
  it is not a displacement. Expect "FAIL at the mechanism".
- **ML1:** a 266 km/s planted drift from z 1.2 moves sheets about 2-3 Mpc comoving before gravity re-binds them. This shows
  the test has power.

## 6. Operational

- One thread, RSS < 1 GB (CLASS once per footing), outputs small (no particle dumps; peak positions and radii only).
- Explicit-path commits via a sparse temporary worktree.
- Files: ss5.py, ss5_grade.py, ss5.json / .out, ss5_MUTATE.json / .out, RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
