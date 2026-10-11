# Baryon-depth identifiability check — freeze alone before execution

Question: do projected gas observables uniquely determine the framework's
round settled target about a specified galaxy centre? This is an exact
translation counterexample plus a numerical size diagnostic, NOT a Bullet
fit, new physical model, observational verdict, or permitted tuning knob.

Take one Gaussian gas component (M=1e14 solar masses, sigma=150 kpc) translated
by d=0,150,450,900 kpc along the line of sight relative to one fixed stellar
Plummer component (M=1e12 solar masses, a=30 kpc). Uniform temperature and
composition, optically thin emission, parallel lines of sight/thin lens.
Gas density translation preserves integrals of rho, rho^2 and rho*T along
each sightline. These observables do not fix gas depth relative to the stars.
Hold host centre/assignment fixed for this conditional example; do not claim
the framework already derives that assignment.

At spherical r=30,100,250,500 kpc compute Mb and the R6 target
Mc=(nu_mono(G Mb/r^2/a0)-1) Mb, using the repaired PM kernel. Two footings
9.36e-11 and 1.13e-10 m/s^2 kept separate (literal owner values; not the
slightly more precise stored engine values). No supply truncation or settling
evolution is inferred. No comparison to observed Bullet masses.

Verify analytic displaced-Gaussian enclosed mass against independent radial
quadrature of angular-averaged density, relative 1e-8 or absolute 1e-12 in
mass fraction. Centre limit, nonnegative density, monotonic enclosed mass,
and total mass limit are required. Projected gas integrals at impact
parameters 0,100,300 kpc must be invariant to relative 1e-9 under translation;
compare analytic projection with independent line-of-sight quadrature.
MUTATE density normalization by 10% must change projected gas and emission
measure; MUTATE ignoring d must miss the computed enclosed mass at d=900,r=250
by more than 1%. A0 affects target only, never baryon observables. Require
finite positive targets and report, rather than preselect, their differences.

Use only exact kernel-defining AST statements extracted from cfg424_pm.py,
not its cosmological transfer/growth code. Pin source hash, code, criteria,
contract, results, Python/numpy/scipy versions. Standard independent constants
G=6.67430e-11 SI, solar mass=1.98847e30 kg, kpc=3.085677581491367e19 m.
One numerical thread, CPU20s/wall30s, expected memory <100MB. Preserve failures.
No claims about actual allowed Bullet depths, novel projection mathematics,
global theory failure/success, action, carrier, or the 32pi coefficient.
