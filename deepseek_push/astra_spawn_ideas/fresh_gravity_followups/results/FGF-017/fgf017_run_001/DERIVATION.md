# FGF-017: relative catalogue distance and emissivity closure

Astra agent /root/dynamics_precision, fgf017_run_001; not a DeepSeek execution.
The existing exclusive claim was read, not modified. Derivation written before
numerical code. FGF-012 accepts only the conditional aperture/mass comparison
and its MOND kernels; it explicitly rejects replacing local density by an
integral mass ratio without the uniform-density-shape premise. That premise
remains essential below. No real likelihood or global cluster repair is claimed.

## Define the conversion before varying a distance

Let the eRASS row quote radius Re and enclosed gas mass Me at a fixed angular
aperture theta_e and its own adopted DA_e. Define d=DA_common/DA_e and an
emissivity ratio ell>0. At fixed redshift, angular counts/shape and composition,
the adopted X-ray conversion S_X proportional to n² Lambda DA gives

    r=d Re, n_new/n_e=d^(-1/2) ell^(-1/2),
    m=d^(5/2) ell^(-1/2) Me.                              (R1)

This is a **relative conversion of the eRASS reduction** to a reference physical
radial coordinate. The original X-COP profiles X(r)=Mgas, S(r)=Mstar and H(r)=
M_FORW are held in that reference convention and evaluated at the new radius.
No X-COP mass is multiplied by a power of d. All three radial supports must
contain r; no extrapolation is permitted. Their centres are provisionally
identified only as a conditional comparison, despite the measured offsets.

A common physical distance change would instead rescale both catalogues,
their physical radii and the gas, stellar and hydrostatic conversions at the
same angular shell. For example, fixed X-ray counts, temperature and emissivity
give gas mass proportional to DA^(5/2), fixed stellar flux and M/L give stellar
mass proportional to DA², and fixed angular temperature/shape gives hydrostatic
mass proportional to DA. Those are additional observation-model assumptions,
not the transformation (R1). Nor does d automatically rescale the adopted
vacuum acceleration a; a change of cosmology must propagate its own rho_Lambda
and kappa conventions. This calculation is not that common-distance problem.

## Conditional local force equation and unique root

Let C(r)=G Msun/(r kpc)² so that solar-mass inputs give SI accelerations.
Under a uniform-density normalization relative to the X-COP shape at r,
eta=m/X(r). If p is the thermal pressure-gradient ratio, the transformed
hydrostatic acceleration is p gH/eta, where gH=C H. The required ratio is

    p(d,ell)=eta F(C[eta X+S];a)/(C H).                   (R2)

For fixed admissible d, X,S,H,a are positive and fixed. Define

    h(eta)=eta F(C[eta X+S];a)/(C H).

Its derivative is [F+eta C X F_B]/(C H)>0. For Q and R, h tends to zero as
eta tends to zero and to infinity as eta tends to infinity. Thus h=1 has a
unique positive eta*. For the registered M interpolation, positive tabulated
phantom increments and the explicit B term imply F_B>0 within its declared
range; the computation must supply a sign-changing bracket lying entirely
inside that range before asserting its unique numerical root.

The corresponding exact closure curve is

    ell_crit(d)=[d^(5/2) Me/(eta*(d) X(d Re))]².           (R3)

Since eta decreases strictly with ell, p<1 iff ell>ell_crit and p>1 iff
ell<ell_crit. With unrestricted positive ell there is always a closing value
where the stated bracket exists; distance/emissivity exclusion therefore
requires an independent domain or lower bound, not a redshift-match likelihood.

At any d, p increases with Me and S and decreases with X and H. The earlier
rectangular mass-box ceiling is therefore exactly the favorable corner:
eRASS high gas, X-COP low gas, high stars and low hydro mass. Its ell_crit is
the largest closing emissivity at that d. Error columns retain the inherited
conventions: gas and hydro errors are magnitudes about separately interpolated
central values; stellar errors and eRASS gas errors are endpoints. There is
no independence or joint-coverage interpretation of this box.

For any independently established distance set D, the sharp conditional
emissivity exclusion criterion is

    ell_lower > sup_(d in D, registered branches) ell_crit,favorable(d). (R4)

Pointwise ell_lower(d)>max_branch ell_crit,favorable(d) is the equivalent
functional statement. At ell=1, the first crossing of the favorable envelope
is the smallest relative conversion admitting a fixed-emissivity closure.
Central curves and favorable curves are reported separately. If positivity of
an error-box lower mass fails, that corner is not silently assigned a valid
finite ceiling; its exclusion is explicitly unavailable there.

## Distance derivatives and support-wide controls

On a log-interpolation cell, write sX=d log X/d log r, sS and sH similarly,
f=eta X/(eta X+S), and e=d log F/d log B. At fixed ell, m scales as d^(5/2),
so direct differentiation of (R2) gives

    Dp=d log p/d log d
       =4.5-sX-sH+e[0.5 f+(sS-2)(1-f)].                 (R5)

Also d log p/d log ell=-(1+e f)/2, hence

    d log ell_crit/d log d=2 Dp/(1+e f).                 (R6)

For Q/R, 0<e<=1 follows by differentiation. For M, on each registered
log-B cell its h coefficient is affine in log B; e<=1 follows if the log
slope divided by ln(10) is no greater than the lower-end phantom amplitude.
That finite table property will be checked explicitly, rather than imported
from a different interpolation. F_B>0 is checked separately.

A sum/difference of two log-linear mass curves has logarithmic derivative
(s1 M1 +/- s2 M2)/(M1 +/- M2). On a common cell, M2/M1 is a power law, so its
slope extrema occur at the cell endpoints when the denominator stays positive.
Using those extrema and 0<=f,e<=1 gives conservative bounds

    Dlo=4.5-max(sX)-max(sH)+min(0,min(sS)-2),
    Dhi=4.5-min(sX)-min(sH)+max(0.5,max(sS)-2).           (R7)

If Dlo>0 or Dhi<0 the curve is strictly monotone in that cell. Otherwise a
valid absolute log-slope bound is 2 max(|Dlo|,|Dhi|). Endpoint values and this
bound enclose the curve between cells; ambiguous cells may be subdivided
within the fixed support, without changing the observations or the model.
This permits a support-wide upper envelope and checks for distance-only roots.
The envelope arithmetic remains binary64, not an interval-arithmetic proof;
strict margins and refinement limits must be reported rather than hidden.

## Registered branches, source matching and execution contract

Use both 9.3619e-11 and 1.1279e-10 m/s². The primary branch holds
 a=kappa c sqrt(G rho_Lambda) constant for constant vacuum density. The separate
comparison uses a=a0 sqrt(.315(1+z_XCOP)³+.685), fixed per object during this
calculation. d is not redshift evolution. Q, exponential R and registered M
remain distinct; M is imported from the inspected stage-three implementation
with bytecode disabled and without calling its output-writing main routine.

The sole scientific run will load the two actual eRASS rows and the six
X-COP FITS profiles, inspect their units/supports, recheck the nominal d=ell=1
comparison, then compute (R3) on the union of actual interpolation knots plus
the nominal d=1. One root per fixed distance and branch/corner is solved in
eta, with forward recovery, positivity, monotonicity and M-support checks.
Distance-only crossings and envelope bounds use (R6)-(R7) and finite adaptive
subdivision only where necessary. Scientific processes are capped at 120 s,
100 s CPU, 1 MiB logs and a cooperative one numerical-library thread.
No raw data, caches or imported output directories are overwritten.

FITS/header inspection may authenticate units and quoted row values. It cannot
by itself create a shared cosmology, actual angular aperture, centre correction,
independent emissivity bound, shared-data covariance or error likelihood.
The known A644/ZW1215 centroid offsets and different ZW1215 redshifts remain
explicit limitations. The task stops at conditional closure curves and the
independent bound needed to exclude them.
