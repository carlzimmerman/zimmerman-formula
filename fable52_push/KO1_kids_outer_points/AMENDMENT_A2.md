# KO1 AMENDMENT A2 (post hoc: written after the main run and the A1 extras, whose numbers have been seen)

Committed alone, before `ko1_shape.py` exists. It changes no frozen statistic, cut, gate, line or label rule: the frozen label
stands as computed (LAW LEVEL HOLDS on both footings). It records two weaknesses of the frozen design that the extras exposed,
and declares, before computing them, the checks that address each.

## 1. The absolute level is a weak statistic here

- The frozen gate compares the host-free outer amplitude with the law at the record's stellar masses (A = 1).
- The extras show the whole stack sits well above that law at every radius: W10 inner window 1.65 +- 0.06, host-free inner
  window 1.81 +- 0.11 (canonical). This is the record's known calibration problem (CFG261: the stellar-mass lever is about
  -1.1 dex per dex), or real extra mass near these lenses; KO1 cannot tell which.
- So "the outer amplitude is at 1" says little: the same lenses are at 1.8 further in.
- The mass-scatter selection factor (1.27) has the same weakness: it rescales every window alike.

**A calibration-free statistic (PH1, post hoc).** R_s = A(outer bins 0-3) / A(inner bins 7-12) for one lens set, with the
delete-one-patch jackknife of the ratio. In the deep regime the law's field of an isolated lens is sqrt(a0 G M(<r)) / r, so
against a fixed-mass model its amplitude is sqrt(M(<r) / M_model), which cannot fall outward: enclosed mass only grows. With
the full interpolating function the statement weakens slightly. The script computes the floor exactly: the enclosed-mass
factor k that reproduces the measured inner amplitude, held constant out to the outer bins, gives the law's smallest allowed
R_s (expected near 0.95). A stellar-mass rescaling, the mass-scatter selection and unseen baryons inside the inner window all
cancel in R_s. PH1 is post hoc and is reported as such; it is not a gate.

## 2. The veto carves a tapered edge (the frozen text's "no hole inside" holds only for point masses)

- The criteria say a uniform absence of projected hosts inside R_h makes no shear inside R_h. That is exact for point masses.
- Hosts have extended mass (a phantom or a cold component, in either reading). The removed surface density is then flat deep
  inside the disc and tapers across the edge, which makes the selected stack's DeltaSigma negative within about one host
  radius of R_h. The outermost bin spans 0.75 to 1 R_h.
- Hand estimate: 0.7 qualifying galaxies inside 2.5 Mpc for a massive lens, each carrying about 3e13 Msun inside 1 Mpc on an
  isothermal profile at 300 km/s, give a mean removed surface density near 1 Msun/pc^2; the edge bias is a fraction of
  that, 0.1 to 0.45 of the law's level in the outermost bin. The host-free profile seen in E1 has its deficit in exactly
  that bin (0.09 +- 0.44 against 0.95, 1.56, 1.24 in the next three), so the deficit cannot be read as physical without a
  test.

**The test (E7, declared before it is computed).** Repeat the frozen cut (Delta 0.3 dex, W 230 Mpc) with the veto radius
widened to 1.3 R_h and to 1.6 R_h (capped at 3.9 and 4.8 Mpc). The lensing sums still end at R_h, so the tapered edge moves
outside the graded range. Report the lens count, the outer-weight share, the four outer bins, A(outer), A(inner) and R_s.
- If the outermost-bin deficit is the edge of the hole, that bin rises to the level of its neighbours as the radius widens.
- If it is physical, it stays.
- Also reported: R_s with the outermost bin left out (bins 1-3 over inner), which is insensitive to the edge at the frozen
  radius.

## 3. A check on tables not yet opened in this window (PH2, declared before it is computed)

B21's published isolated tables with their full covariances: KiDS-bright isolated (photometric isolation) and GAMA isolated
(spectroscopic isolation). Only their four lowest points have been used so far (1.50 +- 0.08 and 0.97 +- 0.28, canonical).
Compute A over bins 7-12 and R_s for each, with the error from the joint covariance.
- If hosts carry the outer points of a photometrically isolated stack, the KiDS-bright table is flat (R_s near or above 1,
  like W10) and the GAMA table falls outward (R_s below 1).
- GAMA's errors are large; the expected power to tell 0.6 from 1 is about 1.3 sigma. It is reported whatever it shows.

## 4. What has been seen since A1 (so nothing above can be called blind, except section 3's inner amplitudes)

Canonical, outer | middle | inner: host-free 1.10 +- 0.15 | 1.82 +- 0.14 | 1.81 +- 0.11; host-free late -0.19 +- 0.39 |
1.53 +- 0.40 | 1.58 +- 0.27; host-free early 1.34 +- 0.18 | 1.90 +- 0.15 | 1.84 +- 0.11; W30 0.94 +- 0.16 | 1.78 +- 0.15 |
1.55 +- 0.10; W30 late 0.53 +- 0.23 | 1.54 +- 0.26 | 0.92 +- 0.16; host-free and W30 0.45 +- 0.26 | 1.64 +- 0.24 |
1.86 +- 0.13; hosted late 1.50 +- 0.16 | 1.12 +- 0.19 | 1.28 +- 0.11; hosted early 2.45 +- 0.13 | 2.48 +- 0.12 | 1.81 +- 0.10;
W10 1.71 +- 0.09 | 1.87 +- 0.09 | 1.65 +- 0.06. Stricter hosts: Delta 0.0 leaves 3,526 lenses (0.01 +- 0.52), Delta -0.3
leaves 1,189 (no power). Hosted minus host-free is 4.98 sigma above the composition level from 200 permutations. Counts: the
isolated lenses have fewer more massive pool objects in range than shuffled positions at almost every separation.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
