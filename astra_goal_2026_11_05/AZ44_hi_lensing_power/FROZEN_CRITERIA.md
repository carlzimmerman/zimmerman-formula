# AZ44 — HI-selected lensing stage0, lane10

Freeze before counts/forecast, under FN4e criteria c03a803b3b. Metadata
only inspected: named inputs exist; KiDS row width833 bytes and DESI
row width808 bytes. DESI's local table has no stellar-mass column. The
FN4c reader's LambdaCDM distance object cannot be used under this run's
native-input rule. Kappa=1/2 FITTED; not theory closed. No downloads.

## Target and decision order

Determine whether the gas-selected sample can reach sigma(log10 a0)<=.05
dex on both footings, retaining FN4e's sample/gate. Before requiring an
exact cosmological distance law and mass-complete neighbour catalogue,
compute an explicitly optimistic upper bound on Fisher information.
If even that bound fails the .05dex gate on either footing, stage1
cannot qualify under the stated forecast assumptions. Label STOP:
NOT ENOUGH POWER, reporting a lower bound on sigma, not an exact forecast.
If the bound can pass, report NOT EVALUABLE pending the missing exact
distance/isolation inputs; do not call the optimistic bound a stage0 pass.
No stage1 measurement is authorized by an upper-bound pass.

## Input and sample rules

Use the files named in FN4e, read-only. Match ALFALFA AGCNr to Durbala
AGC; use finite logMstarTaylor and the HI catalogue's logMH and distance.
This is an SPS stellar-mass assumption, not a raw stellar-mass measurement.
FASHI may use stellar masses only through the supplied ALFALFA match;
deduplicate matched systems by AGC, giving ALFALFA precedence. No
unmatched FASHI stellar mass is invented. Log missing/multiple matches.
Require positive finite distance, mass and physical coordinates, and
fgas=1.33MHI/(1.33MHI+Mstar)>.6. Stellar-mass and distance calibrations
remain explicit survey assumptions, not predictions of the framework.

Build the nside512 footprint from the KiDS catalogue's finite positions;
forecast sources require finite positions,Z_B,e1,e2 and weight>0. Count
the masks separately. Source cut Z_B>z_l+.2; ALFALFA z_l=Vhelio/c,
FASHI uses z_opt. Use each HI catalogue's supplied distance for the
proper angular annulus .03–1Mpc (local-distance convention). Do not
substitute a LambdaCDM distance or infer an expansion history from a0.
Report the area/count effect of using all positions versus usable sources.

Stream DESI BGS positions/redshift/quality into a footprint and report
candidate-lens overlap. Coverage from observed rows is not a complete
selection function and cannot certify isolation. No Mstar-threshold
isolation claim is possible without a stated mass estimator/catalogue.
The information bound includes every eligible gas-rich lens, including
unisolated/unknown-coverage lenses, so removing them cannot defeat the
triangle bound below. The exact isolated-lens count remains unavailable.

## Fisher upper bound, derive before use

Let vM²=sqrt(G M_b a0). For the point-baryon law-S acceleration
g=GM/(2r²)+sqrt[(GM/(2r²))²+GM a0/r²], derive

  0 <= d DeltaSigma/d ln a0 <= vM²/(8 G R).

Use the projection integral
DeltaSigma=R²/(2*pi*G) int_0^infinity [g/r³-g'/r²] dz,
r²=R²+z². For ordinary positive lensing geometry D_ls/D_s<=1,
Sigma_crit^-1<=4*pi*G*D_l/c². Thus for a source at angular separation
theta in the annulus,

 |d gamma/d log10 a0| <= ln(10)*pi*vM²/(2*c²*theta).

Sum these positive bounds over all eligible lenses for each source,
then square and sum over sources divided by sigma_e². This triangle
bound retains possible shared-source coherence; summing independent
lens-pair Fisher terms is not generally an upper bound. It also bounds
any isolated subset. The lower error bound is1/sqrt(F_upper).
Report both footings separately, with exact F_upper proportional to a0
as a known scaling check. These claims assume the point-source law and
the frozen constant shape-noise forecast; they are not an unconditional
bound on every extended-galaxy/shear/noise model.

Estimate sigma_e² per component from the catalogue's weighted centred
e1/e2 spread, averaging the two. The optimistic forecast neglects
additional measurement noise, calibration/systematic errors and sample
selection losses. Report weighted means and spreads; do not use measured
tangential shear as a power forecast. No significance for a measured
law discrepancy is inferred from this calculation. A gap of.09dex is
reported as gap/error_upper-SNR only, alongside the two-footing separation.

## Controls, numerical validation and scope

K1: alpha.100 has31502 rows, retaining FN4e's frozen expectation. A miss
is preserved and investigated, never silently changed. K2: measured
footprint area within5% of777deg², provisional; a miss is reported and
the measured area is used as FN4e specified. K3:100 nonoverlapping SIS
lenses with sigma_v=100km/s, beta_geometry=1, shape dispersion.3 and
source density10/arcmin², annulus corresponding to Dl=100Mpc, recover
analytic SNR²=N_lens*2*pi*n_source*(2*pi*sigma_v²/c²)²*
log(theta_max/theta_min)/sigma_e² within10% on deterministic noise-only
mock positions. Analytic quadrature128/256 agreement<=1e-8.

MUTATE rotates lens RA by180deg, before footprint selection. The
in-footprint count must fall by>50% and the original-count preservation
check must fail (exit1); report if the frozen mutation does not bite.
Keep original and rotated catalogues/results separate. Also verify the
triangle inequality on a two-lens spin-2 fixture and the exact deep-MOND
and Newtonian projection limits symbolically. The upper-bound algebra
must be valid before any gate interpretation.

Read FITS headers only with astropy, then raw row chunks (FN4c method),
never materialize the17.7GB or5.19GB structured tables. Chunk sizes10000
and20000 form the convergence pair for counts, footprint and Fisher;
counts/pixels exact, relative floating summaries<=1e-10. Same-size rerun
must reproduce the deterministic scientific JSON; exclude runtime and
RSS from that comparison. One thread, target RSS<1GB. Checkpoint source
chunks and write outputs atomically with input metadata/hashes. Any
missing mass/geometry input required after the optimistic bound goes
to NEEDS_OWNER, without a download. No existing seals/files are edited.
