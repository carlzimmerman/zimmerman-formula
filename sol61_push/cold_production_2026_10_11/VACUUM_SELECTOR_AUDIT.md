# The production mechanism still needs a vacuum selector

Status: direct local cosmological-constant gravity and a simple optional
Ricci-scalar mass portal were audited. Neither calculation supplies the
repo's halo normalization. This is a scope-specific negative result, not a
no-go theorem for cosmological formation or all possible interactions.

## The requirement being tested

The authoritative microscopic-carrier report requires

    V_f^4=G M_b a0,    a0=kappa c sqrt(G rho_Lambda),    kappa=1/2,

as a derived behavior, together with the requested halo profile. rho_Lambda
here is vacuum mass density; its energy density is rho_Lambda c^2. The
charged production action and repulsive extension contain no such local
coupling. A constant term in their potential has zero field derivative.
It changes gravity but does not directly change the local conversion vertex.

The preceding production and halo-response calculations therefore establish
possible carrier dynamics, not this normalization. Increasing their numerical
resolution alone cannot add a missing interaction or determine kappa.

## Direct vacuum gravity: sign, magnitude and scaling

In the weak-field spherical vacuum exterior,

    Phi=-G M/r-H_Lambda^2 r^2/2,
    H_Lambda^2=Lambda c^2/3=8 pi G rho_Lambda/3,
    a_r=-G M/r^2+H_Lambda^2 r.

The vacuum contribution is outward. Its equality with inward point-mass
gravity gives r_t=(G M/H_Lambda^2)^(1/3). This is the spherical maximum
turnaround scale, not a dark-matter confinement pressure. The primary
source checked was Pavlidou and Tomaras, arXiv:1310.1920v3, section 3.1:
https://arxiv.org/pdf/1310.1920 . Their result supports the turnaround
formula; the target-law comparisons below are this project's calculation.

For comparison only, define r_M=sqrt(G M_b/a0) and assign a test baryonic
mass using the target V_f^4=G M_b a0. This assignment is not a derivation.
Eliminating M_b and rho_Lambda gives

    a_Lambda(r_M)/a0 = [8 pi/(3 kappa^2)] (V_f/c)^2.

The suppression is independent of the illustrative vacuum density used to
quote lengths. For kappa=1/2:

| Target comparison speed | a_Lambda(r_M)/a0 |
|---|---:|
| 50 km/s | 9.3213e-7 |
| 100 km/s | 3.7285e-6 |
| 200 km/s | 1.4914e-5 |
| 300 km/s | 3.3557e-5 |

With declared rho_Lambda=6e-27 kg/m^3, not a cosmological fit,
a0=9.48570e-11 m/s^2. The 200-km/s comparison has r_M=13.666 kpc and
baryonic point-mass r_t=555.189 kpc. A real total-mass turnaround estimate
would include the dark mass; these numbers deliberately compare the
baryonic mass appearing in the target law.

A family placed at r=f r_t, with the same fixed 0<f<1, has

    v_c^2=(G M)^(2/3) H_Lambda^(2/3) (1/f-f^2),
    v_c^4 proportional to M^(4/3) rho_Lambda^(2/3).

At r_t itself the net circular-speed-squared is zero, so GM/r_t must not
be called the actual circular speed there. For a fixed total-to-baryonic
mass ratio and fixed f, the family has the wrong baryonic mass exponent
for the required linear V_f^4 law. Mass-dependent f or dark-to-baryonic
ratio could change that conclusion, but must be derived independently.

This rejects direct vacuum acceleration and a fixed-fraction turnaround
construction as the missing local selector. It does not exclude a small
cosmological term influencing formation history or a nonlinear instability;
that would need an explicit evolution and selection calculation.

## A possible Ricci mass portal is additional physics

To quantify one extension, define its local quadratic mass shifts by

    m_eff^2=m^2+xi_phi (hbar c)^2 R,
    M_eff^2=M^2+xi_chi (hbar c)^2 R,
    Delta_eff=M_eff^2-4m_eff^2
             =Delta+(xi_chi-4xi_phi)(hbar c)^2 R.

The equations specify the sign convention for the optional coupling. In
vacuum de Sitter space, R=4Lambda, so

    (hbar c)^2 R=32 pi G rho_Lambda hbar^2.

For the declared density this is 1.74417e-65 eV^2. The production model has
m=1e-12 eV and Delta=4m^2 u^2=4e-30 eV^2 with u=0.001. Thus:

- An order-one xi_phi changes m^2 by only 1.74417e-41 fractionally.
- An order-Delta vacuum shift requires xi_chi-4xi_phi about 2.29336e35.
- An order-m^2 vacuum shift requires xi_phi about 5.73339e40.

Large coefficients alone are not an inconsistency proof. No radiative
stability, gravitational mixing, cutoff or positivity calculation for this
new action has been performed. In particular, changing the masses does not
automatically retune the existing quartic g^2/Delta to g^2/Delta_eff;
previous positive-square and low-energy matching results cannot simply
be transferred to the modified theory.

There is a further selectivity problem. In minimally coupled Einstein
gravity the trace equation for nonrelativistic matter gives approximately

    R=(8 pi G/c^2)(rho_matter+4rho_Lambda).

As a test-field estimate on the original halo background, rho_matter=1e-21
kg/m^3 gives a matter/vacuum Ricci contribution ratio of about 41,667. A
portal amplified to respond to vacuum curvature therefore also responds
strongly to local matter curvature. Once nonminimal backreaction matters,
this background estimate must be replaced by the modified field equations;
it is a diagnostic, not their solution. Choosing xi_chi=4xi_phi cancels
the direct Ricci shift of the mass-squared gap for both contributions,
so that cancellation does not isolate the vacuum contribution.

The portal preserves the charge symmetry at the level of these quadratic
terms, but no halo law or coefficient kappa follows. A useful next extension
must specify how the medium senses the relevant background, derive its
stress and exchange terms from one action, and retain the established
production and stability conditions. Merely defining a coupling using the
desired a0 would encode the requested law rather than explain it.

## Verification and research decision

vacuum_selector.py checks force-ratio elimination, force cancellation at
turnaround, circular speeds including vacuum repulsion, the mass exponent,
and the Ricci energy scale. All 13 checks pass; the manifest validates
provenance. The interpretation is self-reviewed. The external search scope
was the spherical Lambda turnaround result and its primary paper; no global
literature or novelty claim is made.

The previous turn made progress by identifying the stimulated unbound tail.
This turn identifies a separate missing component that an open-boundary
halo simulation cannot supply on its own. The production route remains a
conditional carrier construction. The full cold-energy goal still requires
a justified selector, abundance, stable halo evolution and the repo's
specific profile and acceleration law.
