# KT40 external-field test: the KT39 survivor loses dwarf binding

The fixed p=9/8, ell=3 kpc curvature response has a serious external-field
failure in the prescribed Plummer models. **Every one of 2,624 nonzero-field
configurations has a lower scalar virial than its isolated counterpart.**
Of the 2,952 configurations including zero field, **1,805 have negative total
binding virial**, despite including ordinary Newtonian gravity. Such a fixed
centered density cannot satisfy stationary scalar virial balance 2K=W with
nonnegative kinetic energy, in the stated uniform-field, gravity-only setting.
This conclusion does not require isotropic velocities.

The tested external acceleration is the *auxiliary Newtonian* gradient
eta=e/a0. It is not the physical MOND acceleration. The latter is nu(eta)e
for a uniform background. The lower eta bracket below was added after the
initial results because eta=.1–3 alone would be too large for many satellite
auxiliary environments. No actual satellite field or orbit was fitted.

## What was computed

All original profiles, masses, observations, Upsilon samples and two a0
footings remain fixed. The four objects are Draco, Sculptor, Leo II and
Fornax. The initial eta values were [0,.1,.3,1,3], followed by the explicitly
adaptive [.001,.003,.01,.03], with all 41 Upsilon values on [1,3].
Each configuration was evaluated on three radial/angular/domain grids.

The table shows the trace-averaged dispersion at the most massive sampled
Upsilon=3, canonical/alternate in km/s. A dash means **negative total virial**,
not zero dispersion or a missing integration.

| Object | Isolated | eta=.003 | eta=.01 | eta=.03 |
|---|---:|---:|---:|---:|
| Draco | 2.638 / 2.763 | 1.271 / 0.646 | — / — | — / — |
| Sculptor | 4.999 / 5.194 | 4.752 / 4.871 | 3.977 / 3.819 | — / — |
| Leo II | 3.296 / 3.420 | 2.981 / 3.002 | 1.739 / 1.025 | — / — |
| Fornax | 10.233 / 10.676 | 9.996 / 10.373 | 9.401 / 9.602 | 7.372 / 6.884 |

At eta=.001 and .003, Fornax still retains sampled orientation-averaged
passes; at eta=.01 it loses them on both footings. The other three objects
are not rescued at any sampled external value. At eta=.01 every Draco mass
has negative total virial. At eta=.03 every Draco, Sculptor and Leo II mass
has negative total virial. At all initial nonzero values eta=.1,.3,1,3,
**all 1,312 configurations have negative total virial**.

These dispersion comparisons are a scalar trace screen. A nonzero external
field breaks spherical force symmetry; an arbitrary observed line of sight
requires the tensor velocity distribution. Positive trace variance does not
establish an anisotropic equilibrium. Negative trace binding, however, is a
stronger necessary-condition failure for the fixed gravity-only profile.

## Equations and physical reason

With the full action coefficients A=[R−1+xR']g and
B=p ell² s^(p−1)xR'H, the exact centered homology virial is

    W_ph=(1/(4piG)) integral [(A−A_ext).(2g_self+r.grad g_self)
                                  +B:(3H_self+r.grad H_self)] d³r.

The external gradient is held fixed. Constant-background and linear energy
tangents are subtracted. Uniform physical external acceleration contributes
no centered scalar virial. For a spherical Plummer self field this reduces
to an ordinary radial/angular integral, retaining every Hessian term.
[Full derivation](DERIVATION_v2.md) · [Wording clarification](ERRATA.md)

An independent route uses the angular-averaged physical radial force:

    <g_ph,r>=<A_r>−d_r<D g'>−2<D(g'−g/r)>/r,
    D=p ell²s^(p−1)xR'.

The full analytic D derivative includes the external-field term in
x'=2(g+e mu)g'/a0². Integrating this force against the mass profile reproduces
the energy-homology virial throughout both parameter brackets.

The mechanism is explicit in an external-dominated, curvature-weak expansion:

    U_H=−e²R'(eta²)ell^(2p)/(8piG a0^(2p)) integral(H:H)^p d³r > 0,
    W_H=−(6p−3)U_H < 0.

R'<0 for the original simple-Q primitive. Thus the external gradient
activates a positive compression energy and an outward virial stress. At
these fixed dwarf sizes that stress can overwhelm Newtonian plus ordinary
MOND attraction. For canonical Draco at Upsilon2 and eta=.01, the exact
variance contributions in (km/s)² are

    Newton: +1.08196, A: +5.54923, B: −25.96949,
    total: −19.33829.

The leading Plummer curvature term scales as

    sigma_H²=(p−1/2)J_p a0 a eta²R'(eta²)
                             (ell/a)^(2p) [GM/(a²a0)]^(2p−1),
    J_(9/8)=0.4322655081522538.

The large size ratio ell/a has power9/4. This explains why an asymptotic
weak-source limit alone did not protect these finite dwarf systems.
[Expansion, assumptions and coefficient](MECHANISM.md)

## The deficit is local, not an infinite-field energy artifact

The separate density-weighted force integral locates the actual scalar
virial inside the dwarf. For canonical Draco, Upsilon2, eta=.01, the total
W/(3M) is−19.3383 (km/s)²; inside3a it is already−17.4498 and inside5a
−19.6368. For canonical Fornax, Upsilon2, eta=.1, the total is−89.2525;
inside2a it is−93.4329 and inside3a−96.3984. The small outer contribution
partly offsets, rather than causes, the failure. These are physical
mass-weighted virial integrals, not cumulative field-energy densities.
[Localization data](localize_001/results.json)

## Validation and scope

Five bounded computation manifests are complete. The checks include:

- Exact Newtonian mutation and independent Newtonian Plummer virial.
- Zero-external reproduction of KT39 to9.8e−9 km/s.
- Fourteen direct40-digit actual-energy homology derivatives, independent of
  the coded A/B integrand, with the original1e−5 relative acceptance gate.
- Three radial/angular/domain settings; signs of all total virials agree.
- Independent full-force monopole virials for every configuration, with
  the declared1e−4 relative comparison gate.
- Independent sign/boundary review by the dynamics worker in
  [EFE_REVIEW.md](../dynamics/EFE_REVIEW.md).

The sigma convergence gate alone is not meaningful for negative variances;
therefore the independent signed-variance comparison and three-grid variance
margins are separately recorded in VERIFICATION.json. Numerical acceptance
means the failure was computed consistently, not that the model passed.
Run `python3 rebuild_2026_10_22/KT40_mechanism/efe/verify.py` from the repository
root to validate the manifests, regrade signs and finite observational screens,
and regenerate the checkpoint. No historical source was edited.

This is a finite constant-external-field test of four fixed Plummer systems,
not an exclusion of all density shapes, tidal fields, external accelerations,
or gravity theories. Actual satellite fields, their gradients, anisotropic
line-of-sight predictions and full evolution remain uncomputed here. The
result supplies a concrete additional condition for any proposed replacement:
it must avoid this dominant external-field curvature stress while retaining
its intended Solar and Milky Way behavior.
