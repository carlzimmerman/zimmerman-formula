# SS1 AMENDMENT A2: variants B-G (outside rounds 4-10), frozen once, committed alone before any B-G number

Criteria b5adc7a90b, A1 9aeeb48503. Variant A was graded and recorded at b8569ef94a (FAIL / FAIL). Nothing in A changes.

The orchestrator relayed six further constructions from the outside source, plus a G addendum. Each is frozen here once, as
given, in the lane's words. The outside text itself is not in the lane and nothing from it is committed. **G is the
primary variant and is finished first.** Each variant is labelled separately on each footing. TEST lane, quarantined;
adopts nothing; no particle adopted. kappa = 1/2 FITTED; not theory closed. Footings as in A, never pooled.

## 1. What every variant shares (unless its section says otherwise)

- **Pre-conversion component.** Cold dust of amount R omega_b before onset.
- **Pre-conversion halos.** As in A:
  - primary: KD1 P3 capture amount (f_cap 0.76 R M_b), SIS truncated at R200 at the variant's z_dec;
  - bracket B1: NFW with Duffy 2008;
  - bracket B2: Moster 2013 abundance matching for galaxy-scale systems;
  - new bracket B3 ("observed M500"), for v_vir-keyed gates only: v_vir from the record's measured M500 / R500 where the
    record has them (Lovisari 2015 table `real_research/data/lovisari2015_groups.tsv`; X-COP R500 from its FITS headers
    with M500 = 500 rho_c(z) 4 pi R500^3 / 3).
- **System descriptors.**
  - v_vir = sqrt(G M500_pre / R500_pre).
  - A virialized pre-conversion halo has Delta_sys = 500 and R_sys = R500_pre.
- **Retention.** f is the root of -ln f + (x0^4 / 4)(1 - f^4) = alpha. It applies uniformly to the whole pre-conversion
  component of the system. B's radial factor and the G-local bracket are the exceptions.
- **Members** (Coma UDGs inside Coma; UMa members inside UMa): C, D, E use x = sqrt(x_own^2 + x_host^2); B uses its bath
  rule (f of the host); F, G use max(x_own, x_host). A member's own pre-conversion halo is its primary halo.
- **Where conversion happens.**
  - C-G (two-body): only inside collapsed halos (Press-Schechter collapsed fraction at z_dec above 1e6 Msun, as A; bracket
    M_min = 1e10 reported). The uncollapsed web stays cold.
  - B: the field converts too (field retention e^-alpha).
- **The converted daughter's mass is kept** (B loses 2e-4 of it). So the background matter density is unchanged, with a
  bare Lambda and a0 fixed. Its fate by variant:
  - B: warm, streaming at 355 km/s; leaves every system (as given).
  - C: kick 220 km/s; the evicted mass sits in a shell around its system, Gaussian in r with mean 1.2 Mpc and sigma
    0.3 Mpc (the source's 0.6-1.8 Mpc shelf, as given).
  - D, E, F, G: kick 4 v_stiff (about 1150 km/s); the daughter is unbound and removed from the system. Where a system's
    central escape speed exceeds the kick, the daughter is retained instead; the count is reported.
- **Subhalo multiplicity f_sub,eff (B-E), off-record.** The record has no subhalo masses for its groups, X-COP or KiDS
  lenses, so these use a disclosed bracket, and a label resting on it says "(on the subhalo bracket)":
  - The Jiang & van den Bosch 2016 unevolved subhalo mass function, dN/dln mu = 0.22 mu^-0.91 exp(-6 mu^3), mu from 1e-4
    to 1.
  - f_sub,eff = sqrt(integral of mu^2 dN) + 0.012.
  - KiDS isolated lenses: mu <= 0.25 (satellites up to 10 % of the stellar mass; halo-mass ratio about 0.25).
  - E: f_slosh = (integral of mu^2 dN) / mu1 + 0.008, with the central's share mu1 = 1 - (integral of mu dN).
  - The source's own assumed values are reported beside.
- **Subhalo multiplicity, record-native** (used where it exists):
  - Bullet main: the subcluster-to-main baryon ratio (DB1);
  - UMa: SPARC members' primary halos, the largest member as i = 1;
  - MW: LMC halo ratio 0.1 (literature value, disclosed).
- **F's central share f_cen** (a baryon key, recorded as such): not on disk per group or cluster. Disclosed bracket: 0.3 and
  0.6 for groups and clusters; 1.0 for isolated galaxies.
- **UMa geometry** (C-E use R_sys and Delta_sys): the source's R_sys 1.5 Mpc; Delta_sys computed from the members' summed
  primary halos inside it (disclosed). The bound-group reading (Delta 500) is reported beside.

## 2. The variants (frozen once)

- **B:** z_dec 0.55, Gamma0 0.693/Gyr, alpha 3.80.
  - Gate: x0 = (f_sub,eff / 0.0350)(R500_pre / 250 kpc).
  - Radial factor: x0(r) = x0 for r <= 0.25 R500 and x0 (r / 0.25 R500)^(ln 0.72 / ln 4) beyond (0.72 at R500, as given).
  - Bath: members take the host's f.
  - Daughter: warm 355 km/s, free-streaming length 5 Mpc.
  - Constants: 0.035, 250 kpc, 0.012, Hill 4, the 0.72 profile, alpha.
- **C:** z_dec 0.55, alpha 3.80.
  - Gate: x0 = (f_sub,eff / 0.035)(R_sys / 250 kpc)(Delta_sys / 500)^(3/2).
  - Daughter: two-body, kick 220 km/s, shelf as in section 1.
  - Reported beside: the UMa exponent-1 reading (orchestrator: x0 0.87).
- **D:** as C, but kick 1150 km/s and unbound daughters.
- **E:** as D, but the gate is x0 = W_mach(v_vir) [ (f_slosh / 0.120)(R_sys / 250 kpc) + max(0, v_vir - 410) / 95 ]
  (Delta_sys / 500)^(3/2), with W_mach = max(0, 1 - (260 / v_vir)^2), velocities in km/s.
  - Constant count recorded: 260, 410, 95, 0.120, 0.008 and the exponent 3/2 (six).
- **F:** z_dec derived from q = 0, i.e. 1 + z = (2 Omega_DE / Omega_m)^(1/3), per footing.
  - v_stiff = (a0 c L*)^(1/3) per footing, with L* 21.68 / 22.85 pc. Kick 4 v_stiff.
  - Gamma0 = 4 pi H0 sqrt(Omega_DE) per footing; alpha = Gamma0 times the time from z_dec to 0. Graded at the footing's
    alpha (about 4.39); alpha 3.80 is the source's bracket.
  - Gate: x0 = 3.40 max(0, (v_vir / v_stiff)^2 - 1)(1 - 0.75 f_cen), times Theta(Delta - 200).
  - Members: max(x_own, x_host). Bracket: v_vir from kT (B3-like).
  - Constant count: 2 fitted (3.40, 0.75) plus the baryon key f_cen.
- **G (PRIMARY):** z_dec, Gamma0, alpha, v_stiff and the kick as F.
  - Gate: x0 = 3 max(0, (v_vir / v_stiff)^2 - 1), with x0 = 0 if Delta < 500. Members: max(x_own, x_host).
  - Form choices recorded beside the label: 4 pi, the factor 4 in the kick, the factor 3, the cube-root combination.
  - **G-local bracket** (named added assumptions; never grades): v_loc(r) = v_vir (1 + (r / 0.35 R500)^2)^(-1/4) applied
    shell by shell, plus the 18 % "AGN adiabatic expansion" of the retained profile. A local dispersion gate is close to
    the dead dispersion keys HX1 / SK1.

## 3. Gates and lines

Gates 1-10 are A's, with A's lines and A's gate 7(b) rule. Additions:

- **Gate 5b, Ursa Major (record-native, graded for B-G).**
  - Data: EV1 W1, the 26 GB1-sample UMa spirals against the field, measured d = -0.024 +- 0.064.
  - Delta_pred = (mean over members of the pointwise log10(g_with_component / g_law) at fixed Upsilon, QX8 median U) minus
    (the same over the field galaxies, each with its own retention).
  - PASS iff |Delta_pred + 0.024| <= 0.128.
- **Gate 6.** Mass is kept, so the background equals the reference. Graded with A's integrator at S_bg = 1 - 2e-4 (1 - S)
  for B and S_bg = 1 for C-G; PASS iff Delta chi^2 <= 4.
- **Gate 8 growth.**
  - The daughters are a non-clustering fraction at k above 1 / lambda: fc(k, a) = F_conv(a) (1 - 1 / (1 + (k lambda)^2)).
  - F_conv(a) is the cosmic converted share of the component from the Press-Schechter mass nodes. Each node's y(tau) comes
    from the closed form.
  - lambda is the comoving streaming length of a daughter produced at onset, with v proportional to 1/a (B: the source's
    5 Mpc).
  - The record's two-fluid growth ODE (k-dependent, WD1 form), the CE2 fsigma8 rule (graded), and the forest (graded; z
    above onset, so unchanged).
  - sigma8 and S8 reported beside KiDS-1000 S8 0.759 (+0.024 / -0.021), a literature number not graded.
  - CMB lensing: reading only (NO VERDICT, as A: no validated method).
- **Lens-redshift split.** None is on disk: the KiDS-bright catalogue has lens redshifts but no shear profiles. So the F and
  G lens-redshift steps are recorded as frozen predictions, not graded.
- **High-z kinematics (D, E claims).** NOT EVALUATED: AT2's on-disk high-z samples are blocked. Reported.

**Label per variant and footing.** PASS iff gates 1, 2, 3, 5, 5b, 6, 7(b), 8, 9 and 10 all pass. Otherwise FAIL, naming the
first failing gate in that order, with the full table. A label resting on a gate graded on the subhalo bracket says so.

## 4. Known answers (a FAIL is printed; nothing is stopped unless it is the lane's own closed form or ODE)

- **K0 (graded):** the closed form against a numerical integration of dy/dtau = -y/(1 + (x0 y)^4) at x0 0.5, 1.5, 1.95,
  2.4, 3.2 and alpha 3.80 / 4.39, to 1e-6.
- **K-B (reproduction):** the source's x0 1.95 / 2.10 / 2.40 -> 25.0 / 66.7 / 85.2 % at alpha 3.80, and KiDS x0 0.18-0.64 ->
  2.2-2.3 %. Hand estimate before any number: the closed form gives about 57 / 73 / 86.5 %, so the 25 % does not solve the
  source's own closed form.
- **K-D:** x_crit = ((64/15)(alpha - ln 2))^(1/4) = 1.908 at 3.80 and 1.99 at 4.39.
- **K-F:** the orchestrator's F checks: kT 0.8 keV group v_vir 361.5 -> x0 1.27 -> f 0.043 / 0.024; 1.8e13 -> 0.94;
  3e13 -> 0.99. Reproduced at v_stiff 286 and f_cen as the orchestrator took it, reported.
- **K-G:** z 0.05, 500 rho_c, v_stiff 286, alpha 4.39. M500 3e12 / 5e12 / 7e12 / 1e13 / 1.35e13 / 2e13 / 3e13 -> v_vir
  242 / 287 / 321 / 361 / 399 / 455 / 521 km/s (within 1 %) and f 0.012 / 0.012 / 0.014 / 0.161 / 0.927 / 0.990 / 0.998
  (within 0.005). Every Lovisari group retains >= 0.992 on its table M500 / R500.
- **K-C:** the source's own shelf numbers for M* 10^11.3 (+0.28 dex at 1 Mpc, +0.31 at 1.5 Mpc). Replayed, reported.
- **A's KAs** (law-only replay, Bullet K1, baselines) are rerun in each variant's pass.

## 5. MUTATE (G only, separate outputs)

- **MG1, MG2:** v_stiff x 1.25 and / 1.25. The group / KiDS thresholds and at least one status must move; otherwise NO
  BITE, disclosed.
- **MG3:** alpha -> 0 (no conversion). KiDS or SPARC must FAIL (every halo keeps its share).
- **MG4:** x0 = 0 everywhere (everything collapsed converts). Groups and X-COP must FAIL.

## 6. Hand estimates (before any number)

- **G, primary halos:**
  - Groups: M200_pre about 5 M_b gives v_vir about 360-450, near or above the 369 threshold. Retention about 0.2-1 by group:
    bimodal and sensitive.
  - X-COP keeps everything (4.1 M_b, SIS); the inner bin is over-filled as in A or worse: X-COP FAILS.
  - KiDS, SPARC and the MW sit below threshold and PASS.
  - Bullet keeps 4.1 M_b on the galaxies: may pass.
  - Converted share about 0.6-0.75 of the component (PS down to 1e6), more than the source's 22 %. lambda about 3-5 Mpc. Small
    effect on fsigma8 at k about 0.1; sigma8 down a few %.
- **B, C, D:** the subhalo-bracket f_sub is self-similar (about 0.25 + 0.012), so x0 scales as R500, as in A. With 0.035 and
  250 kpc, groups and clusters sit far above threshold and isolated lenses (mu <= 0.25) near it. C's shelf FAILS KiDS (K-C).
- **E:** groups with v_vir < 410 depend on f_slosh (about 0.25 / 0.8 + 0.008, so x0 about 2.5 x R500/250 x W_mach).
- **F:** small groups FAIL at the M500-based v_vir (K-F).
- **UMa:** below threshold in C-G at the source's geometry, so 5b PASSES. B with record-native f_sub: unknown.

## 7. Operational

As A. New script `ss1v.py` (variant engine), reusing ss1.py / ss1_cosmo.py functions read-only and the DB1 child through
ss1_bullet.py. Lean additions in `ss1_lean/SS1_variants.lean`. Results go in `RESULT_B_G.md`, `ss1v.json` / `.out` and
`ss1v_MUTATE.json` / `.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
