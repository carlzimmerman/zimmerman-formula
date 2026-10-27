# Radiating collapse: bulk inventory survives; a universal remnant is not selected

RC-20261022, continuing dynamical_arrest_2026_10_22 from revision 08daade3f873ad4fa6dfbf31b9be950a833d9072. **The requested common remnant mass and joint observational/growth pass were not obtained.** Actual finite-time collapse experiments now replace the earlier static-radius and prescribed-source diagnostics. They find measurable phase-field export at stronger coupling, but retain the initial mass dependence and substantial internal oscillations. A separate energy-budget argument obstructs one canonical endpoint for several heavier seeds. Precise inner profiles remain numerically unresolved, and that failed convergence check is retained explicitly.

These are conditional radial projections of the reduced action, not full three-dimensional formation simulations. All review is self-review. The parameters below are exploratory choices, not values derived or fitted by the theory.

## 1. What was evolved

In units ell0=.440422 kpc, a0=9.3603e-11 m/s², time sqrt(ell0/a0)=12.0743 Myr, and mass M0=a0 ell0²/G, use radial material shells coupled to dynamical polarization w and phase z=chi/chi0. The canonical fitted mass is Mstar=.0840813 M0, approximately 1.095e7 solar masses.

The discrete Hamiltonian is a projection of

    E = K_radial + sum_i L_i²/(2I_i) + U_gravity
        + integral r² dr [eps w_dot²/2 + W(w) + e²/(2z)
          + b z_dot²/2 + d z_r²/2 + a(z-1)²/2],
    W(w)=-|w|-ln(1-|w|), e=rho-div w, h=e/z.

Radial matter and both fields receive forces by differentiating the same discrete energy. Material is neither damped nor deleted. Shells may cross or travel outward. Each shell has fixed axial angular momentum and constrained spherical shape, with I_i=2m_i r_i²/3 before regularization. This is a restricted rotating-shell model: it excludes angular deformation, torques between shells, fragmentation and nonradial instabilities. It is not a single-stream smooth fluid after crossings. No baryons or X background are imposed; the experiment isolates the existing passive phase-radiation channel. It therefore does not demonstrate negligible baryonic heating.

The field equations use a staggered finite-volume divergence and its energy-adjoint gradient. Shell mass uses TSC deposition and the derivative of that same deposition for reciprocal force. Gravity and rotational inertia are explicitly softened at one cell width; softening is reduced during refinement. This is a numerical regulator, not a new physical core size. Any inner result sensitive to it is withheld.

Only field momenta in the exterior absorber are damped; removed kinetic energy is accumulated exactly. Independently, the net flux through r=6 is measured:

    F_P = r² h w_dot,
    F_chi = -d r² z_dot z_r.

The total Hamiltonian plus absorbed energy must remain constant to numerical tolerance. Net flux at a finite radius may include reversible near-field redistribution, so absorber loss and finite-radius flux are not blindly equated with asymptotic radiation.

Initial material is a smooth Gaussian radial distribution, with scale .6(M/Mstar)^(1/3), at rest radially. This holds initial characteristic density fixed while varying inventory. Fields start at their discrete static minimum. Twelve baseline seeds cover M/Mstar=.5,1,2,4 and initial spin energies 0,2%,5% of gravitational binding magnitude. The baseline uses eps=.005, lambda=1, phase gap=.5 and phase speed=1, with a=1/(2lambda), b=a/gap² and d=b. Stronger phase tests use lambda=10,100 and gaps .5,.2. These choices keep positive kinetic and gradient terms; no friction coefficient is fitted to object class.

## 2. Bulk collapse does not approach a common mass in the tested family

The baseline runs extend to 30 time units, or .362 Gyr. All retain their material near the collapsed system; none meets the declared far-outward positive-energy ejecta criterion. The longer, stronger-radiation runs extend to 120 units, or 1.449 Gyr, at 2% initial spin energy, lambda=100 and gap=.2:

| initial mass / Mstar | mass inside .881 kpc / Mstar | absorbed field energy / initial binding magnitude |
|---:|---:|---:|
| .5 | .500 | .000785% |
| 1 | .992 | .01996% |
| 2 | 1.922 | .3171% |
| 4 | 3.719 | 1.1615% |

The larger-mass runs thus radiate more strongly but do not converge to one core inventory. A refined heavy run gives 3.750 Mstar inside the same radius and about 1.05% energy absorption. There are no declared far-unbound ejecta in these runs. Some material lies outside the chosen inner aperture; it is not assumed to have escaped.

These are **finite central masses**, not asymptotic remnant masses. The mass inside .440 kpc still varies substantially during the last fifth of the long runs: its peak-to-peak variation is approximately .063, .227, .141 and .234 of the total inventory, respectively. The system has not become the static fitted core simply because a substantial fraction of its material is central.

The test family spans an eightfold initial mass range; even restricting to seeds at or above Mstar, the final central-mass spread is 123% of their mean, failing the declared 10% common-mass diagnostic. This is a result for the stated finite family and coefficients. It does not prove that no other initial conditions, nonlinear field regime, or three-dimensional fragmentation process could select a scale.

### Numerical reliability: a useful result and an important failure

Energy-force directional derivatives agree for material, polarization and phase variables. Material mass is conserved by deposition. Across the reported runs the largest sampled relative energy-balance error is about 2.2e-5; the finest baseline run reaches 2.8e-8. Initial static-source ringing is separately controlled: holding matter fixed yields only 2.3e-13 absorbed energy in the baseline test.

At r=6, changing the outer box while holding cell size fixed changes the baseline net flux by less than 1%. Absorber losses themselves differ because the absorption surfaces have different travel distances. This distinction prevents a false radiation-convergence claim. Baseline radiation is extremely weak; finite-radius total flux can be negative because near-field energy returns inward. It is not interpreted as clean irreversible cooling.

For the heavy long run, the positive phase flux is about .000298 energy units; refinement gives .000263, a 13.1% difference. The signal is large relative to energy-balance error. Its accompanying material mass inside .881 kpc changes by only .78% of initial inventory. These support the bulk retention and measurable-export conclusions within this radial model.

**The instantaneous inner density profile is not converged.** The maximum empirical enclosed-mass difference is .219 of total mass between the 256- and 512-cell repeats, and .152 between 512 and 1024 cells. Both exceed the declared .05 gate. Last-third time-averaged enclosed masses improve: the two finest runs differ by at most .0283 of total mass at the recorded apertures. That does not establish a stationary profile or justify a precision dwarf fit. The failed profile gate remains failed in postcheck_run/result.json.

## 3. Why radiation does not automatically select material mass

The action conserves the cold current separately. Phase and polarization waves carry energy, but they do not carry that conserved material charge. Therefore

    M_initial = M_central + M_bound_outer + M_escaped.

Cooling alone cannot reduce the cold inventory. A selected central mass requires actual material redistribution, ejection, fragmentation or continuing supply. The simulations allow outward material motion; their near-total retention is an outcome, not an imposed fixed-core-mass constraint. However, spherical shape constraints exclude fragmentation, so this is not a test of that alternative.

There is also a sharper endpoint constraint. For one specified core plus mutually separated, nonnegative-total-energy escaped matter and outgoing waves,

    E_initial = E_core + E_escaped + E_radiated,
    E_initial >= E_core,min.

Here E_core,min is the minimum field energy at the specified cold density profile, plus its gravitational energy and zero-spin material energy. At fixed density the field functional is convex: e²/z is a convex quadratic-over-positive-variable perspective, W is convex, and the remaining phase/gradient terms are positive quadratics. Numerical minimization therefore has a well-defined discrete target. This is not a lower bound over *all possible cold density profiles*.

I sampled the previously fitted canonical cold profile, re-minimized its fields with the collapse model's finite-chi coefficients, and repeated at two resolutions. Its endpoint energy is about -.002370 in model units; the two-grid change is 1.44%. At 2% initial spin:

| seed inventory | initial energy | canonical-endpoint energy minus initial energy |
|---:|---:|---:|
| Mstar | -.001919 | -.000451 |
| 2 Mstar | -.006875 | +.004505 |
| 4 Mstar | -.024154 | +.021784 |

The positive deficits in the last two rows mean those seeds cannot become that one canonical density profile plus nonnegative-energy debris by radiating away energy. Radiation lowers the retained energy further. The conclusion is insensitive to the measured endpoint discretization change. The same obstruction holds for all three tested seed spins at those higher inventories.

Possible escapes are explicitly outside this endpoint statement: a more tightly bound core with a different density profile; additional bound material; multiple self-bound fragments; external work; or a different action. Self-bound escaped fragments can carry negative internal energy and are not the nonnegative-energy debris assumed in the inequality. A bound envelope can also store negative energy, but its mass and gravity must then be included in dwarf/cluster predictions. A half-Mstar isolated seed cannot make an Mstar core for the separate, simpler reason of mass conservation.

For the Mstar seed, the canonical endpoint is energetically allowed, but would require export of roughly 23.5% of its initial binding magnitude if it ended exactly in that state with no other retained component. The baseline run exports vastly less over its tested interval. This is an energy budget, not an extrapolated cooling time.

## 4. A linear fragmentation check supplies no missing preferred wavelength

To avoid simply replacing “one remnant” by an untested fragmentation claim, linearize the original unpumped homogeneous cold branch in a static local patch with background gravity subtracted. Let rho0>0, eps>0 and y=gamma² for a growing longitudinal mode. Eliminating polarization gives

    eps y² + A(k)y-rho0=0,
    A(k)=1+k²-eps rho0(1-k²),
    y=2rho0/[A+sqrt(A²+4eps rho0)].

Since A increases strictly with k>0, gamma² decreases strictly with k. The fastest mode is at the largest available scale, not a finite nonzero wavelength selected by this branch. The phase source is quadratic around e=X=0, so adding its radiation dynamics does not change this linear conclusion. Nine inertia/density combinations and 300 wave numbers each check the branch against the original equations.

This is not a nonlinear fragmentation theorem, and excludes neither an imposed initial spectrum nor rotating/shearing, warm, driven or expanding backgrounds. It does rule out citing this particular cold linear instability as an already-derived universal fragment mass. A new formation-scale claim must supply the missing ingredient rather than borrow it from a different scalar-field theory.

## 5. Dwarf fits, rotation curves and growth

I passed the instantaneous collapse mass profiles through the inherited empirical-law-plus-cold-mass diagnostic, without refitting the 10 MW,17 M31/field,21 UFD and56 rotating SPARC samples. For the long 2%-spin runs:

| profile | MW RMS ln dispersion residual | UFD mean ln dispersion residual | SPARC mean dex residual |
|---|---:|---:|---:|
| canonical static reference | .216 | .092 | .0267 |
| .5 Mstar seed | .402 | .543 | .0294 |
| 1 Mstar seed | .358 | .518 | .0272 |
| 2 Mstar seed | .310 | .482 | .0232 |
| 4 Mstar seed | .344 | .248 | .0150 |

These are diagnostic snapshots, **not validated fits**: the inner profiles fail instantaneous convergence, remain time-dependent, and the baryons have not been dynamically evolved. The changing dwarf residuals show why merely retaining the right total mass is insufficient. The rotating sample's coarse mean is comparatively insensitive, but that does not establish preservation of full rotation curves or their scatter. No observed dwarf exclusion is inferred from an unconverged snapshot.

The homogeneous e=P=X=0, chi=chi0 linear background is unchanged by these quadratic phase sources. Thus the new channel does not introduce a linear phase source there, but it also does not repair the inherited compliance suppression. With the same ell0, the previous quasistatic EdS diagnostic retained about .99950 at k=.1/Mpc and .95565 at k=1/Mpc. Finite-inertia expansion, radiation energy from an actual cosmological population, a covariant stress tensor and formation abundance remain uncomputed. There is no new full cosmological-growth pass.

Likewise, no cluster spatial distribution follows from these isolated radial collapses. Their mass dependence and remaining bound outer material must enter a population assembly calculation; neither can be silently replaced by the earlier fitted cluster profile.

## 6. What this checkpoint establishes

Localized phase radiation is a real energy outlet in the tested action projection. It does not, in the tested regime, erase initial inventory or produce a settled universal core. The stronger evidence is the combination of bulk-retention repeats, independently checked field flux, the endpoint energy budget, and the absence of a fastest finite wavelength in the unpumped linear branch—not a claim that every collapse route has failed.

The remaining physically distinct route is nonradial fragmentation/angular-momentum transport or an independently specified supply mechanism. Before using it, the model needs a continuum/kinetic closure through crossings and a mechanism selecting the fragment scale. The current instantaneous-profile convergence failure prohibits promoting these radial outputs into a population fit. Full baryonic response and cosmology remain joint requirements.

All ordinary run checks are recorded separately from interpretation gates. The common finite-time mass gate and instantaneous-profile convergence gate fail. An earlier endpoint run failed only while serializing a NumPy boolean; its original source/log are preserved, and the corrected run changes no equations. See AUDIT.md, HANDOFF.md, and the reproducible contracts/manifests.
