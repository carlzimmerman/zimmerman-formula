# What Tacconi+2013 says about the radius of `Vrot` (record only; no radius chosen)

Source: arXiv:1211.5743 (ApJ 768, 74), read from a local copy of the PDF
(`~/new_physics/_external_data/papers/tacconi2013_arXiv1211.5743.pdf`, 4,052,671 bytes,
sha256 `0d33e7a3c4bdfa4a88990890962eece4c06cd45be28a127efdf0854378b2fc30`, 63 pages, not in the repo). Section 2.5
(page 14) and Table 2 were read as text and, for the formulas, as a page image. This note records what the paper
states and where it is silent. It picks no radius for any galaxy. The CFG54 question was at what radius `Vrot`
was measured; the answer below is that the paper defines none.

## What the paper states
1. **`Vrot` is a characteristic circular velocity from a formula, not a velocity read off a curve at a radius.**
   Section 2.5 gives two cases:
   - if no velocity gradient is detected (an unresolved galaxy): the isotropic virial estimate
     v_c = sqrt(3 / (8 ln 2)) x Δv_FWHM, the CO line width;
   - if a gradient indicative of rotation is detected: v_c = 1.3 x Δv_blue-red / (2 sin i), with i "estimated from the
     morphological aspect ratio on the HST/Hα images". The factor 1.3 is called "an empirical calibration"
     determined from disk models with source sizes, rotation velocities and resolutions comparable to the data
     (Förster Schreiber et al. 2009).
   Neither case names a radius. Δv_blue-red is the velocity difference between blue and red CO centroids across
   the source.
2. **Resolution scale, as stated:** the sub-arcsecond CO data have beams of 0.3 to 1 arcsec FWHM (page 10); the paper
   describes its CO maps as having "~4-8 kpc linear resolution" (in the velocity-dispersion discussion, page 21).
3. **How gradients were found:** in all 9 sets with sub-arcsecond CO data, and in the compact-configuration data of 21
   other galaxies, by measuring centroids at different velocities more accurately than the beam (page 14).
4. **Table 2 footnote for `vrot`:** "rotation velocity, typical uncertainty 20-30%". No radius, no method flag, no
   inclination in the table.
5. **Half-light radii** (`R1/2opt`, `R1/2CO`) are separate columns, from HST I-band fitting for AEGIS, Hα for the BX
   sample and CO 3-2 for the CO column (footnote 3, uncertainty about 25%). The paper does not say `Vrot` is
   evaluated at any of them.
6. **Quality classes** (section 3.1): quality A = disk-like HST morphology plus a significant resolved CO gradient;
   quality B = disk-like morphology but no detected gradient.

## Where the paper is silent
- **A radius for `Vrot`**, per galaxy or as a rule. The formulas are set by the whole-source velocity difference or
  the line width, calibrated on models; no r/R_e is given.
- **Which of the two formulas was used for which galaxy.** Table 2 carries a `Type` label but no method column.
  By the paper's own definitions a quality-B disk has no detected gradient, so the gradient formula cannot have
  applied to it; the paper does not say the virial formula was used for those rows in Table 2 (my inference from
  the definitions, not a statement in the paper).
- **The source of `Vrot` for the z~2.2 galaxies that also have Hα kinematics.** The paper lists SINFONI and Keck
  Hα kinematics for 10 of the z~2.2 galaxies and names nine BX/MD galaxies with spatially resolved Hα data (in the
  sample description before page 10, and section 3.1 on page 17), but does not state that Table 2's `vrot` for those comes from Hα rather than CO.
- **The inclination** used for each galaxy, and the velocities for the Daddi BzK, PEP and lensed rows: the paper
  points to the original papers (Daddi et al. 2010; Magnelli et al. 2012; Baker 2004, Coppin 2007, Swinbank 2010)
  for those objects and does not restate their method here.

## What the joined table shows (`phibss13_joined.csv`, from CDS)
73 rows; 65 have `Vrot`. Exact `Type` counts among those 65 (as printed in the table): Disk(A) 35; Disk(B) 6;
Disk(A/B) 1; Merger 2; Late merger 1; Merger/Disk 1; Int. disk 1; Int. disks 1; Inter.Disk 1; Amorph 2; Amor.Comp 2;
Amor.Clump 1; Compact 1; Comp. Disk? 1; Disp.Dominated 1; blank 8 (35+6+1+2+1+1+1+1+1+2+2+1+1+1+1+8 = 65). This is
the paper's own classification and not a per-galaxy method flag.

## Consequence for a radius-dependent test
A test that needs the velocity at a stated radius (for example where g_bar < a0) cannot take that radius from this
paper for any of the 65 galaxies. It would have to be assumed and declared, which means any g_bar(r) built from
`R1/2opt`, `R1/2CO` or a multiple of them is a modelling choice and not a statement of the source.
