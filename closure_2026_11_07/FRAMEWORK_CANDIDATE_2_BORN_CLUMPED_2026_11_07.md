# Framework candidate 2, 2026-11-07 ~15:30: born-clumped cold dark energy (the owner's "anisotropy" idea)

Owner: "what if the cold dark energy has anisotropies that would explain clusters but where there aren't they work
like galaxies" and "cherry pick stuff together to get an answer that is consistent". This assembles the record's
PASSES into the one picture that is consistent with all of them, states what it adds, and freezes what kills it.
It is a CANDIDATE: nothing here is graded yet. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

## 1. Why the first candidate died and this one is different

Candidate 1 (FRAMEWORK_CANDIDATE_2026_11_07.md) kept a uniform cold component and REMOVED it from galaxies after
capture. Every removal mechanism is dead: fixed temperature (wall 2), hot relic (wall 3), shock heating (wall 4),
late heating as a fluid (CE2), a kick (CK1: the law's own field keeps a 500-650 km/s carrier in the massive spirals),
and the action supplies no release (CK2). The record's exhaustion theorem (DEDUCTION section 7) is about mechanisms
that act AFTER the component is in place.

Candidate 2 never puts it there. The cold component is BORN inhomogeneous on a few-Mpc scale: concentrated at the
sites that become clusters and groups, absent from the regions that become field galaxies. Nothing has to be
removed from a galaxy, because the galaxy formed where the component was not. The only thing added is an initial
condition, not a force, a temperature or a kick.

## 2. The pieces of the record it is built from (every one a recorded PASS or measured number)

| Piece | Record |
|---|---|
| The law + v3s action with the adopted blend, certified | PAPER70 v1.0; QX17, QX17D |
| Field galaxies: law alone, no halo | SPARC exact field (QX8); KiDS with kSZ gas (KX1); dwarfs (SE2); wide binaries Newton (CQ2) |
| A cold component exists at the CMB's amount | QX15 primary CMB (cold component needed, baryons-only FAIL); native R = 5.562 (QX12) |
| Clusters hold it at ~0.78 / 0.70 of that ratio, concentrated between gas and stars, collisionless | X-COP f 4.2 / 3.8 (KD1, SE2); NA2 profile band; Bullet (DB1); CLASH lensing-only missing mass z 0.19-0.70 (QX33: no hydrostatics involved) |
| Groups hold part of it, with a fragile step | UA1 +0.259 / +0.221; KD1 f 1.2-3.5 / 0.9-2.9 |
| Early structure and growth need it cold early | CK4 early-BH row; QX3 iter3 member found with the corrected kernel (GL1); growth (QX3) |
| Large-scale isocurvature is forbidden | R19: Planck CDI bound; the light-spectator origin failed it by 2e8-6e8 (X1_seedfree) |

## 3. What the picture requires (and therefore predicts)

R1. The component's inhomogeneity lives only at k >~ 0.5 Mpc^-1 (clump scale <~ 10 Mpc comoving): the primary CMB
    (ell <= 2500) and CMB lensing (L <= 400) see only its MEAN, which is the adiabatic cold component QX15 fits.
    Below that scale the Planck CDI bound (R19) does not reach; the mu-distortion bound bites only at k > 50.
R2. The clumps' large-scale distribution must trace the adiabatic mode with bias ~1 at recombination, or the
    peak heights move; a biased component is a kill unless the fit survives.
R3. Every clump gathers its cosmic baryon share and becomes a cluster or group: no baryon-free clumps (dark lenses),
    and the clump mass spectrum must reproduce the X-COP / eRASS1 / Lovisari abundances by mass with no LCDM input.
R4. Field galaxies form outside clumps: f = 0 by construction; KiDS isolated lenses (field by selection) see nothing.
R5. Galaxies that formed INSIDE clumps (cluster members, group centrals) formed in a component-rich region: they
    either carry halos or had them stripped. The cluster-vs-field split of early-type dynamics at fixed mass is the
    sharpest galaxy-scale test, and the record has not graded it.
R6. The forest at z 2-5 traces baryons: outside clumps it is a baryons + law forest; inside, rare dense proto-cluster
    absorbers. The 1D flux power at k 0.01-0.1 s/km must not show the clumps' extra small-scale power beyond its
    errors.
R7. Groups: f rises with group mass (the clump-to-baryon ratio grows toward the cluster scale), the same trend CK3's
    data allowed at +0.21 per dex and CK1's kick could not give.
R8. No evolution of the cluster ratio with redshift at fixed mass (the clumps are primordial): CLASH's lensing-only
    lookback (QX33, 20 clusters, z 0.19-0.70) is the only time series on disk and has no power; CHEX-MATE has no
    per-cluster gas masses (CFG436 NOT POSSIBLE). A prediction, not a test today.

## 4. Kill lines, frozen before any number

K1. R2 fails: the primary CMB under the footing background does not tolerate the clumped component's large-scale
    bias at the level the clump spectrum implies.
K2. R6 fails: the forest 1D power at z 2-4 excludes the small-scale power of a clumped component at the CMB's mean
    abundance (the strongest expected kill; grade with the record's forest machinery, both footings).
K3. R3 fails: no clump spectrum reproduces the cluster and group abundance by mass while giving f 4.2 / 3.8 in
    X-COP and 0.9-3.5 in groups.
K4. R5 fails the wrong way: cluster-member early types at fixed mass show the SAME residue as field early types
    (zero after IMF) AND no stripping budget explains it.
K5. The NA2 profile: a primordial clump's concentration must sit in the gas-to-stars band at X-COP's radii.

## 5. Lanes (frozen first, both footings, MUTATE bites, subagents inside, adopt nothing)

NC1 (closure coordinator): the clump spectrum. Build the component's clump mass function that gives f = 4.2 / 3.8 in
    X-COP and 0.9-3.5 in groups with cosmic baryon share, compare to the X-COP / eRASS1 / Lovisari abundances by mass
    on disk (no LCDM mass function), and grade R3, R7 and K5 (profile vs NA2's band for an early-collapsed clump).
NC2 (KD1 session): cosmology. Primary CMB (QX15 grader) with the clumped component's large-scale bias as a parameter
    forced by NC1's spectrum (R2 / K1); CMB lensing L <= 400 with the corrected kernel; the forest 1D power at z 2-4
    with Mpc-scale clumps at the mean abundance (R6 / K2); mu-distortion check at the clump scale.
NC3 (EV1 session): galaxy scale. Cluster-member versus field early-type dynamics at fixed stellar mass from what is
    on disk (SLUGGS, MaNGA red galaxies, the 7 X-ray ellipticals with environment tags; SR1 / U1 / X64 lanes hold
    loaders), with a stripping budget stated first (R5 / K4); the KiDS isolated-lens selection as the field-by-
    construction control; CLASH's lensing-only concentration slope (QX33 s) read as the profile check at z 0.2-0.7.

## 6. One paragraph

The law and its action are right wherever the universe is cold and isolated. The cold component the CMB demands is
real, but it was never spread evenly: it was born in few-Mpc clumps at the sites that became clusters and groups, so
clusters hold it concentrated and collisionless, groups hold it in proportion to their mass, and the field galaxies
that formed between the clumps hold none and obey the law alone. Nothing is removed, heated or kicked; one initial
condition replaces every dead mechanism. It lives or dies on the forest, the CMB's tolerance of a clumped
component, the clump spectrum against cluster counts, and the cluster-member galaxies. Kappa = 1/2 FITTED; not
theory closed.

## Post-result NC3 (39940c070e): members are clean too, so the clumps are smooth below galaxy scales

Cluster-member early types show no residue at r_half (D +0.011 / +0.012 dex, upper edge 0.065; at most ~16 % extra
mass there), and the pre-stated stripping budget cannot hide one. K4 does not fire by the frozen rule, but the only
reading that survives is R9: inside a clump the component is smooth on scales below a galaxy's half-light radius; it
has a minimum clustering scale of order 0.1 Mpc or more, even inside clusters. That sharpens the other kills: K5 must
be met by a clump that is concentrated at X-COP's radii (0.1-1 Mpc) yet smooth below ~20 kpc; and K2 (forest) now
concerns a component whose small-scale power is cut off near that scale, which the forest machinery must model as
such. CLASH's concentration slope carries the sign an early clump gives (-0.08 to -0.13) with no power. R4 holds
(KiDS field control clean).

## Post-result NC2 (47c50d2827): candidate 2 is CLOSED

The primary CMB tolerates a large-scale bias of the cold component between 0.9967 and 1.0014; a component born in
few-Mpc clumps at the future nodes is a peaks population with bias 45 to 1866 at recombination, and even b = 1.2
costs Delta 4e4. The forest at z 2.2-4.4 tolerates only 0.13-0.28 % of the component in clumps on both footings, at
every clump mass and with NC3's 0.1 Mpc cutoff. The clumps' Poisson power also fails CMB lensing at and above 1e14.
This is the same physics that closed the PBH door (PB1-PB4): a cold component cannot be born clumped at the CMB's
mean abundance without the CMB and the forest seeing the clumping. K1 and K2 both fire; NC4's profile and abundance
rows are now record rows, not a candidate's gates. One initial condition cannot replace the dead mechanisms either.
