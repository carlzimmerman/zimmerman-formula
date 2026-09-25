# -*- coding: utf-8 -*-
"""
lanes.py -- the deepseek_push lanes re-run by D02, in dependency order, and the MINIMAL sandbox patches that let their own code
run on corrected inputs.  Every patch changes how an input is LOOKED UP, never the physics:

  O04b_joint_update.py, P02_power_audit.py  read the SPARC-deep entry of N05_results.json by VALUE RANGE
      (find_first(n05, "Delta", lambda v: -1e-21 < v < 0), "a0eff_a0" in (0.5, 1.5), "z_clustered" < 0, ...) -- the deficit is
      written into the lookup, so a corrected (positive) SPARC value is not found, and a range-filtered "a0eff_a0 > 1.5" could
      return the SPARC entry instead of MIGHTEE's.  Patched to read n05["deep_sparc_L06"][...] and n05["mightee_deep"][...] by key.
  G183_n_family.py  asserts the SPARC ring count 641 (and MIGHTEE 80, HI 26) and builds its sample-label array with a literal 641;
      the err/V < 10% quality cut changes the SPARC count only, so the assertion clause and the label array use len(sN).  The
      lane's own count check C1 is left as written and fails in the cut variants (reported, not hidden).
  ZD08_velocity_domain_a0star.py, ZD11_highz_dark_fraction.py  hard-code a0* = 6.407e-11 / 6.4e-11, the G183 SPARC-deep value;
      they are given the G183 value re-computed in the same sandbox.
  N05_deep_bar.py  stores the SPARC-deep a0_eff as 1 - |Delta|/a0E (a deficit assumed; its own MIGHTEE block uses 1 + Delta/a0E).
      Patched to the signed 1 + Delta/a0E, which is IDENTICAL for the committed (negative) Delta and correct for either sign.
  Q02_deep_onset.py, R03_offset_robust.py  open the corpus through a hard-coded absolute path into the working tree, so in a
      sandbox they would silently read the UNCORRECTED corpus.  Patched (by pattern, so no machine path is written here) to open
      the sandbox corpus relative to their own directory.
"""
LANES = ["G071_sparc_fullcurve.py", "g03d_efe_refit.py", "g03e_equipartition.py", "G119_break_factor.py", "G208_deep_staircase.py",
         "L06_rar_moment.py", "N01_density_locality.py", "N05_deep_bar.py", "Q02_deep_onset.py", "R03_offset_robust.py", "S01_running_a0.py",
         "G158_n_discriminator.py", "G183_n_family.py", "G199_deep_universality.py", "O04b_joint_update.py", "P02_power_audit.py",
         "S02_mightee_mirror.py", "T03_mightee_subpop.py", "U01_deep_structure.py", "U02_arbitration_refresh.py", "U03_digitization_audit.py",
         "W03_wallaby_card.py", "S02_a0z_plane.py", "ZD08_velocity_domain_a0star.py", "ZD11_highz_dark_fraction.py"]

STATIC_PATCHES = {
    "O04b_joint_update.py": [
        ('delta  = find_first(n05, "Delta",     lambda v: -1e-21 < v < 0)', 'delta  = n05["deep_sparc_L06"]["Delta"]'),
        ('secl   = find_first(n05, "se_clustered", lambda v: 1e-24 < v < 1e-21)', 'secl   = n05["deep_sparc_L06"]["se_clustered"]'),
        ('frac   = find_first(n05, "fraction_a0E", lambda v: 0.1 < v < 0.5)', 'frac   = n05["deep_sparc_L06"]["fraction_a0E"]'),
        ('x_sparc = find_first(n05, "a0eff_a0", lambda v: 0.5 < v < 1.5)', 'x_sparc = n05["deep_sparc_L06"]["a0eff_a0"]'),
        ('z_sparc = find_first(n05, "z_clustered", lambda v: -10 < v < 0)', 'z_sparc = n05["deep_sparc_L06"]["z_clustered"]'),
        ('"mightee_excluded": {"a0eff_a0": find_first(n05, "a0eff_a0", lambda v: v > 1.5),', '"mightee_excluded": {"a0eff_a0": n05["mightee_deep"]["a0eff_a0"],'),
        ('"z": find_first(n05, "z", lambda v: v > 5),', '"z": n05["mightee_deep"]["z"],'),
    ],
    "P02_power_audit.py": [
        ('delta = abs(find_first(n05, "Delta", lambda v: -1e-21 < v < 0))', 'delta = abs(n05["deep_sparc_L06"]["Delta"])'),
        ('frac  = find_first(n05, "fraction_a0E", lambda v: 0.1 < v < 0.5)', 'frac  = abs(n05["deep_sparc_L06"]["fraction_a0E"])'),
        ('s = noise = find_first(n05, "per_ring_noise_a0E", lambda v: 1 < v < 10) or noise', 's = noise = n05["n_requirement"]["per_ring_noise_a0E"]'),
    ],
    "N05_deep_bar.py": [
        ('fraction_a0E=f0, a0eff_a0=1.0 - f0,', 'fraction_a0E=f0, a0eff_a0=1.0 + Delta_d / a0E_d,'),
    ],
    "Q02_deep_onset.py": [
        ("re", r"open\('[^']*glm53_push/data/rotation_curve_corpus_v7\.json'\)",
         "open(os.path.join(os.path.dirname(BASE), 'glm53_push', 'data', 'rotation_curve_corpus_v7.json'))"),
    ],
    "R03_offset_robust.py": [
        ("re", r"open\('[^']*glm53_push/data/rotation_curve_corpus_v7\.json'\)",
         "open(os.path.join(os.path.dirname(BASE), 'glm53_push', 'data', 'rotation_curve_corpus_v7.json'))"),
    ],
    "G183_n_family.py": [
        ('assert len(sN) == 641 and len(mN) == 80 and len(hN) == 26, "sample counts drifted"',
         'assert len(sN) > 0 and len(mN) == 80 and len(hN) == 26, "sample counts drifted"'),
        ('allsamp = np.array(["SPARC"] * 641 + ["MIGHTEE"] * 80 + ["HI"] * 26)',
         'allsamp = np.array(["SPARC"] * len(sN) + ["MIGHTEE"] * 80 + ["HI"] * 26)'),
    ],
}

def a0star_patch(lane, a0star):
    if lane.startswith("ZD08"):
        return [("A0_STAR_REG = 6.407e-11", f"A0_STAR_REG = {a0star:.4e}")]
    if lane.startswith("ZD11"):
        return [("A0_STAR = 6.4e-11", f"A0_STAR = {a0star:.4e}")]
    return []
