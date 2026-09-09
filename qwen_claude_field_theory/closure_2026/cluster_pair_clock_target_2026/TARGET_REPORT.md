# Exact-law cluster and binary source targets

These are inverse targets for a proposed clock sector, not predictions of an
action, a stable clock construction, or a completed empirical fit. Run against
commit `347950889570a839af41f6bef0c8bcba7531d02a`, with existing unrelated changes
preserved. The exact exponential law is used for clusters; the isolated deep
limit common to that law is used for binaries. Neither old capped-RAR nor
algebraic three-dimensional multipliers enter this calculation.

## Spherical cluster target

Let `M_H(r)` be the published thermal hydrostatic reconstructed mass,
`g_H=G M_H/r²`, `y=g_H/a0`, and `M_b=M_gas+M_star`. If a candidate action actually
derives the additive-source equation

`div[mu(|grad Phi|/a0) grad Phi]=4 pi G (rho_b+rho_clock_eff)`,

then its necessary enclosed effective source is

`M_clock_eff(r) = (1-exp(-y)) M_H(r) - M_b(r)`.

The action must still establish what effective source means in terms of clock
energy, pressure and derivatives. Identifying it with positive rest mass is an
additional assumption. A density-only extra source also extends requirement 1's
literal baryon-only right-hand side and must be reconciled explicitly with the
galactic branch of the specification.

For logarithmic enclosed-mass slopes `alpha_H,alpha_g,alpha_s`,

`dM_clock_eff/dln r = M_H[mu alpha_H + y exp(-y)(alpha_H-2)]
                     - M_g alpha_g - M_s alpha_s`,

and `rho_clock_eff=(dM_clock_eff/dln r)/(4 pi r³)`.
Analytic derivatives are evaluated on the same piecewise log-linear profiles as
the corrected loader, with centered differences independently checked away from
knots. Maximum discrepancy divided by cumulative mass scale is below `4.1e-9`.
An initially overly strict relative-to-nearly-zero derivative check failed;
normalizing by cumulative mass removes cancellation from the diagnostic.

Seven X-COP clusters have stellar FITS files, so this primary run needs no
imputed stellar profile. All seven require positive enclosed extra source over
40–1000 kpc on both footings. Median **total required source / measured baryons**:

| Radius | a0=9.3619e-11 m/s² | a0=1.1279e-10 m/s² |
|---|---:|---:|
| 100 kpc | 8.220 | 7.561 |
| 300 kpc | 7.470 | 6.978 |
| 1000 kpc | 4.066 | 3.573 |

For the three relaxed clusters at 300 kpc on the canonical footing:

| Cluster | Extra enclosed source, Msun | Required local effective density, kg/m³ |
|---|---:|---:|
| A1795 | 7.468e13 | 1.515e-23 |
| A2029 | 1.084e14 | 3.161e-23 |
| A2142 | 8.105e13 | 3.266e-23 |

The cumulative extra source declines in some outer intervals in five of seven
profiles. Canonical first negative-density sampled radii are approximately
680 kpc (A1795), 856 (A2029), 984 (A2319), 671 (A644), and 851 (A85).
A2142 and ZW1215 have no negative-density samples in the tested interval.
The first-to-last negative-radius endpoints in JSON do not assert that every
intervening interpolation segment is negative. This distinction matters:
positive enclosed mass does not suffice for a nonnegative local density.

These signs constrain reproduction of the central reconstructed profiles by a
nonnegative additive source. They do not establish statistically significant
negative matter or eliminate a healthy clock. Derivatives amplify profile
modelling, stellar census, distance and hydrostatic systematics; radial
covariances are unavailable. The published gas-radius normalization uses each
file's own R500, including its inherited model dependence. Nonthermal pressure
and lensing must be handled in a joint inference before imposing these targets
as observational boundary data.

If the effective source were a separately conserved ordinary isotropic fluid,
its static pressure would additionally obey `P'=-rho g_H`. Positive sound speed
for a barotrope would require `dP/drho=-rho g_H/rho'>0` wherever the approximation
applies. Assigning the inverse density by hand supplies neither that equation
of state nor a cosmological origin. A clock with different effective stress
must derive its own relation instead.

## Binary force and population question

Primary source checked 2026-09-08: Mordehai Milgrom, *General virial theorem for
modified-gravity MOND*, arXiv:1311.2579v2, 9 January 2014,
[equations (1)–(2), sections I and III](https://arxiv.org/html/1311.2579v2),
published Phys. Rev. D 89, 024016, DOI 10.1103/PhysRevD.89.024016.
The authenticated author preprint proves the point-mass virial in the isolated,
low-acceleration modified-gravity limit, including nonlinear Poisson MOND.
Its masses are centers of compact bodies; internal velocities do not enter.
No project-local copy matching this identifier was found in the bounded search;
the exact versioned primary HTML was read directly, with no source cache edited.

For two bodies, action-reaction and central symmetry turn that virial into

`F=C/r`,
`C=(2/3) sqrt(G a0) [(m1+m2)^(3/2)-m1^(3/2)-m2^(3/2)]`.

Writing `m_red=m1 m2/(m1+m2)` yields `v_circ,rel²=C/m_red`.
With `f=m1/(m1+m2)`, the mass-ratio correction multiplying
`sqrt(G a0 (m1+m2))` is

`B(f)=(2/3)[1-f^(3/2)-(1-f)^(3/2)]/[f(1-f)]`.

The previous pair script already implemented this correct force. It is not a
test-particle mapping error. Its external-field helper uses another kernel and
an isotropic algebraic approximation; that helper is deliberately not reused.

The relative scalar virial identity derived from this force is

`(1/2) d²(m_red r²)/dt² = m_red v_rel²-C`.

For a bound phase-mixed orbit the averaged left side vanishes, independently of
eccentricity. Thus `<v_rel²>=C/m_red`, and isotropic complete ensemble orientations
give `<Delta v_los²>=C/(3 m_red)`. **An arbitrary eccentricity amplitude is not
needed for this complete stationary ensemble second moment.** Selected projected
separations, nonstationary encounters, incomplete phase coverage and interlopers
can break its direct application to a catalogue likelihood.

For circular orbits at specified `r` and projected `R`, the conditional second
moment is `v_circ² R²/(2r²)`. Under a log-flat prior on true separation and random
orientations, integrating over `r>=R` gives `v_circ²/3`; the corresponding LOS
velocity density is uniform between `-v_circ` and `+v_circ`. The old Gaussian
signal component has the same assigned RMS but a different velocity shape.

## Raw-catalogue refits

`target.py` reconstructs pairs from `real_research/data/2mrs_catalog.csv`, reusing
only the four coordinate/photometric functions from the old script via an
explicit AST whitelist. The selection retains its K-band M/L=0.6, major ratio
below 6, CMB-frame mean velocity 3000–12000 km/s, projected separation 10–1000 kpc,
and |velocity difference|<2000 km/s. Third galaxies within 1000 km/s of the
midpoint are searched to 8 Mpc. Relative isolation means
`d_third>max(F R,300 kpc)`. Because R<1 Mpc and F<=8, the search now covers every
cut. The script rejects any requested isolation threshold beyond its search.

Review found that the first run inherited a 4 Mpc search cap from the earlier
pair script. Encoding no detected neighbour as infinity falsely admitted some
pairs whose required isolation radius exceeded that cap. The affected old
samples had 51 unverified cuts at F=5 and 123 at F=8. Extending the actual search
removes **11 false passes at F=5** (1830 to 1819) and **77 at F=8** (1196 to 1119);
the remaining formerly unverified cuts pass the full search. F=2 is unchanged.
The JSON regenerates the old capped selection and its fits as explicitly marked
legacy diagnostics. It does not label that capped selection fully isolated.
A synthetic 6 Mpc third galaxy is missed by the old search and correctly vetoes
an 8 Mpc cut in the corrected regression check.

Both Gaussian and circular uniform velocity components are convolved with a
40 km/s pair error, mixed with a flat interloper component, and normalized over
the selected velocity window. Six deterministic optimizer starts check each
fit. No curvature errors or sigma exclusions are claimed. Some galaxies appear
in multiple pairs: 10 repeated entries in the F=5 sample, 129 at F=2. These are
not treated as independent evidence for a confidence calculation. The corrected
F=5 sample has 1809 connected components of pairs linked by shared galaxy IDs;
20 pairs belong to ten two-pair components. F=2 has 4166 components, 243 pairs in
shared-galaxy components, and maximum component size three. Any uncertainty
estimate must at least resample these components, while also addressing common
sky/environment systematics. The near/far samples have disjoint galaxy IDs
(checked), but share photometric, selection and gravity assumptions. They are
not independent controlled tests of distance alone: their mass and separation
populations differ. No uncertainty on their amplitude difference or statistical
significance is assigned here.

| Selection | N | Gaussian A, canonical | Circular A, canonical | Circular A, alternate |
|---|---:|---:|---:|---:|
| F=2 | 4294 | 1.753 | 1.443 | 1.377 |
| F=5 | 1819 | 1.891 | 1.626 | 1.552 |
| F=8 | 1119 | 1.928 | 1.671 | 1.595 |
| F=5, nearby 3000–6000 km/s | 521 | 1.678 | 1.414 | 1.350 |
| F=5, distant 9000–12000 km/s | 612 | 2.094 | 1.870 | 1.785 |
| F=5, baryonic gN(R)/a0<0.01 | 854 | 1.553 | 1.395 | 1.331 |

The circular fit has a worse negative log likelihood by 155.5 in the F=5
canonical sample, with the same number of parameters. Its lower source target
therefore does not establish that circular orbits solve the distribution.
It demonstrates the sensitivity of the inferred amplitude to the assumed
velocity shape and associated interloper assignment (16.7% Gaussian versus
25.1% circular at F=5). The near/far change is material and remains compatible
with flux-limit contamination and changing mass populations; it is not an
identified cause from these data alone.

Only under **co-scaling of both compact bodies' total inertial and gravitational
masses, preserving their mass ratio and isolated deep-limit behavior**, the
required total mass multiplier is `A^4`, extra mass `A^4-1` times adopted stellar
mass. For F=5 these totals are 12.78 (Gaussian canonical) and 6.98 (circular
canonical), with circular alternate 5.80. The deep-selected circular totals are
3.79 canonical and 3.14 alternate. Gas is not in the K-band mass estimate.
These are conditional benchmarks, not masses of a diffuse clock halo. A diffuse
clock changes the three-dimensional source and cannot be inverted with `A^4`.
Adding such mass also raises the acceleration and can invalidate the deep-limit
assumption used for the inversion.

## Discriminating next calculation and reproducibility

The immediate constructive calculation is a fixed-mass-ratio, finite-separation
**two-body exact exponential AQUAL boundary-value force table**, measuring the
force by a stress-surface integral while converging body size, box and grid.
Use that table in phase-mixed orbit populations with the actual projected
selection and a deeper, approximately volume-complete isolation catalogue.
A phase-mixed log-potential benchmark must first reproduce the eccentricity-free
virial second moment above. This targets finite-field corrections versus
population/contamination bias without freely assigning an orbital amplitude.
For a pressureful clock, its field equations and common boundary conditions must
predict both the cluster source profile and the pair force; the inverse budgets
alone cannot do so.

Executed scientific command (exit 0):

```text
OPENBLAS_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python -B qwen_claude_field_theory/closure_2026/cluster_pair_clock_target_2026/target.py
```

`results.json` preserves all values and signs. `manifest.json` records actual
runtime, software, commit, dirty state, input SHA256 values and output SHA256.
Checks passed for equal-mass coefficient, mass exchange, mass scaling,
test-body limit, constructed circular-likelihood recovery, and cluster
derivatives. The computation-audit manifest validator with `--root` exited 0,
while explicitly identifying legacy v1 limitations: no enforced resource-cap or
input-freshness guarantee. A first `/usr/bin/python3` dependency probe failed
because Astropy was absent; the existing scientific interpreter above succeeded.
Only this new directory was written; no old data, Fable files or commits changed.
