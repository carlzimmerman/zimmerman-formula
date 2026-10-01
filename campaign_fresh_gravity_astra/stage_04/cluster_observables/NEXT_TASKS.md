# Narrow follow-up task cards for the coordinator

These are proposed tasks, not assignments or completed results. No shared queue
was modified. Each task should receive its own write lane and pinned manifest.

## 1. Bound the missing aperture/distance convention

**Inputs:** this lane's `run_002/gas_comparison.csv`, matched eRASS1 entries in
`real_research/data/erass1cl_primary_v3.2.fits`, and the A644/ZW1215 gas, stellar
and M_FORW FITS profiles. Read the current comparison's restrictions first.

**Equation:** introduce the relative distance conversion d=DA_common/DA_eRASS
and emissivity ratio ell. Translating the SAME eRASS angular aperture under
fixed counts/shape gives `r'=d R_e` and
`Me'=d^(5/2) ell^(-1/2) Me`. Compare with original X-COP profiles evaluated at
r', not each catalogue's separate R500. Then

    eta = Me'/Mx(r'),
    p_required = eta F(G[Me'+Ms(r')]/r'^2;a)/gH(r').

**Controls:** distinguish a relative catalogue-distance conversion from a
physical change in all cluster distances and a0. Permit only d for which all
three X-COP radial supports contain r'; no extrapolation or invented distance
prior. Keep both normalizations, vacuum/H and Q/R/M distinct. Do not infer a
distance likelihood from the redshift agreement alone.

**Acceptance:** return p=1 root curves in (d,ell), or a certified no-root result
within the declared support, plus the smallest independently required distance
or emissivity bound that would preserve this stage's conditional exclusion.
If catalogue metadata cannot identify the actual angular convention, retain
that explicit gap rather than interpreting the curves as observed corrections.

## 2. Stress-test the continuity sign against the supplied profile error columns

**Inputs:** all seven measured-star X-COP FITS triplets; stage-three
`run_003/shell_constraints.csv` and `continuity_intervals.csv`; stage-four error
column conventions. No extra thermodynamic data are required for this bounded
conditional test.

**Equations:** on adjacent gas-mass knots, let Li and Ui be a declared lower
and upper enclosed-mass box. A sufficient interval lower bound on slope is

    s_min = ln(L2/U1)/ln(r2/r1).

At each interior shell, independently bound

    Delta_min = G Mh_low/r² - F(G[Mgas_high+Mstar_high]/r²;a).

If s_min>1 and Delta_min>0 at even one shell, the stage-three steady,
source-free spherical-flow sign contradiction survives every point in that
box. If either condition fails, the box test is inconclusive; it does not
construct an admissible steady flow.

**Controls:** MGAS_LO/HI magnitudes versus MSTAR_LO/HI endpoints must remain
distinct. Preserve positivity and monotonic mass, make interpolation/error
conventions explicit, and do not assign a confidence level to the box or
assume neighboring errors independent. Global profile constraints can only
tighten the admissible box and should be reported separately.

**Acceptance:** a list of shells whose sign contradiction survives all allowed
box perturbations, or an explicit admissible perturbation removing the local
sign certificate, with no claim that such a perturbation solves all equations.

## 3. Determine what local pressure information is identifiable in the cached SZ map

**Inputs:** `deepseek_push/Z06_data/ilc_actplanck_ymap.fits`, the matched mask,
`ilc_beam.txt`, source coordinates in `run_002/catalogue_matches.csv`, and
ZW1215's X-COP radial supports. ZW1215 is the only eRASS-matched target with an
unmasked map center in the current inventory. A644 center mask=0 is a hard
warning against treating geometric coverage as usable pressure data.

**Equation:** derive the spherical line-of-sight pressure projection
`y(theta)=constant integral P_e(sqrt[(DA theta)^2+l^2]) dl`, followed by the
cached beam and explicit angular binning/mask. Keep pressure-gradient target,
outer pressure profile, background modes and distance conversion explicit.

**Controls:** inspect masks over entire annuli, not only the center. Do not
invent noise covariance, use aperture scatter as independent instrument noise,
or count ACT+Planck and PSZ2 as independent Planck observations. Do not identify
integrated Y or a fitted SZ mass proxy with a local pressure gradient. The
original hydrostatic pipeline's shared Planck inputs require a separate
cross-covariance audit before an independence claim.

**Acceptance:** demonstrate that the desired gradient functional is identifiable
in a stated finite projection/outer-boundary model, or exhibit an explicit
projection null mode that changes it. If identifiable, return a deterministic
estimate with its required missing covariance/response inputs; do not turn it
into a confidence bound until those inputs exist. This settles whether the
current map can supply the next constraint, rather than assuming that more
angular bins create independent information.
