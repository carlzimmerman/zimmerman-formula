# Independent test of the fixed radial variance conjecture

Status: numerical counterexample supported by an independent implementation;
an analytic inequality and novelty remain to be established.

The model is a central source in a unit conservative unpolarized Thomson
sphere, with D=T-x_exit dot u_exit. Fix epsilon=1/8, d=4 and
A=8/log(65); kappa(r)=A/(epsilon^2+r^2). The known first-moment identity gives
E[D]=4 without fitting. The conjectured extension of the uniform-model bound
would require Var(D)>=6.4 for this radial cloud.

Qwen b81f7acf0ec2433f8c89e7e91f685624 contains a real optical-depth inversion
simulation. Both original 8,000-photon runs reproduce exactly. They gave
B=D^2-22.4 residuals -5.904 and -5.090 approximate MC SE, so they FAIL the
predeclared six-SE predicate. Neither is retrospectively relabeled a pass.
Qwen printed the theoretical exp(-tau_rad) as an “unscattered fraction”;
that was not a measured fraction. It also broadly clamps geometry arguments.

The independent audit freezes 32,000 photons per case and seeds 9810001,
9820001,9830001 before its results. It uses full 3D position/direction and
homogeneous-majorant null collisions, rather than reduced coordinates or
optical-depth inversion. Thus it does not reuse the candidate's flight formula.
For radial opacity the majorant is A/epsilon^2, and real collisions occur with
probability epsilon^2/(epsilon^2+r^2). Rejected null events advance position and
time without scattering. All photons finish; no forced exits or dropped paths.
Initial +z directions are equivalent to isotropic central emission for these
rotation-invariant observables in a spherical medium.

| Independent case | mean D | sample Var(D) | mean B / SE(B) |
| --- | ---: | ---: | ---: |
| Radial, seed 9810001 | 3.99583 | 4.68226 | -12.4325 |
| Radial, seed 9820001 | 3.98949 | 4.75722 | -12.1782 |
| Uniform k=8, seed 9830001 | 3.99560 | 8.89675 | +10.0962 |

Both radial runs pass the SAME six-SE counterexample predicate with mean-delay
calibration; the uniform negative fixture fails it as required. All 18 audit
checks pass, including the symbolic optical-depth derivative, original replay,
geometry and Thomson angular second moment. Independent radial paths have
maximum 982/919 real collisions, well below the 10,000 cap. Actual unscattered
counts are 0/0 for radial (expected fraction 2.339e-10), and 13 for uniform
(expected fraction exp(-8)). Approximate standard errors do not constitute
rigorous probability bounds. The manifest validates against current inputs.

Earlier cap failures are often a parameter bug: writing
log((1+epsilon*epsilon)/epsilon*epsilon) evaluates log(1+epsilon^2), giving
A about 516, instead of A about 1.916. Raising caps does not fix that physical
model change. The runner correctly rejected these executions; no runner fix
is indicated. Preserve the source leaf with correctly parenthesized A.

This limits the uniform theorem's profile applicability; it does not refute
the uniform theorem or establish a new physical law. The next useful task is
an analytic supersolution bounding the second moment for the SAME profile,
not repeated sampling or parameter selection. See SOURCES.md for known overlap.
