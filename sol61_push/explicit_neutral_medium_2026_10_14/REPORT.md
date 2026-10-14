# Explicit mediator: the homogeneous coherent neutral branch remains unstable

Parent: db15bdfbe3b755fe634b35431f7c75bcc5f20f9b.
Retaining mediator dynamics removes the invalid weak-mixing elimination at
high density, but does not stabilize the tested homogeneous coherent neutral
state. Its equilibrium composition has negative compressibility, and the
full six-component Bogoliubov matrix independently exhibits growing density
modes. This closes that restricted state proposal as a stable medium within
the stated model. It does not exclude a kinetic/multimode state, other
interactions, or the laboratory few-pair preparation calculation.

## Fixed-number equilibrium without eliminating the mediator

Retain the preceding nonrelativistic rotating-wave model with fields a,b,r,
neutral charge Q=0 and conserved constituent density

    n=|a|^2+|b|^2+2|r|^2.

Use g_plus=gs+gc0=1e-6 eV^-2, h=0.0005 eV^(-1/2) and delta=2e-9 eV.
The mediator kinetic mass is approximated by 2m, with m=1 eV. The detuning
is retained explicitly in the energy. For the phase choice minimizing the
conversion energy, a=b=A is real and r is negative. Define

    f=2|r|^2/n, A^2=n(1-f)/2, r=-sqrt(nf/2).

The energy per constituent, excluding the common rest energy, is

    e(n,f)=delta f/2-h sqrt(n/2) sqrt(f)(1-f)
           +g_plus n(1-f)^2/4.

Solve de/df=0 on 0<f<1. Its second derivative is
h sqrt(n/2)(1+3f)/(4 f^(3/2))+g_plus n/2>0, so there is a unique minimum
in composition at fixed n. This is not a minimum against spatial density
variations. The atomic chemical potential and equilibrium condition are

    mu_chem=g_plus A^2+h r,
    (delta-2 mu_chem)r+h A^2=0.

No vacuum mediator decay is appended to these coherent conversion equations:
the same coupling is already retained dynamically. Quantum damping and other
loss mechanisms would require a consistent extension, not double counting.

## Linearize all three fields

In the rotating frame with chemical potentials (mu_chem,mu_chem,2mu_chem),
the Bogoliubov matrix is [[L,B],[-B,-L]]. For real A and r,

    L_aa=L_bb=(2gs+gc0)A^2-mu_chem+k^2/(2m),
    L_ab=gc0 A^2, L_ar=L_br=h A,
    L_rr=delta-2mu_chem+k^2/(2M),
    B_aa=B_bb=gs A^2, B_ab=gc0 A^2+h r,

with symmetric entries and remaining B entries zero. The matrix is checked
against direct finite differences of the original complex field equations,
not only against an assumed eliminated dispersion relation.

The thermodynamic long-wavelength prediction is

    (hbar omega)^2 approximately [n dmu_chem/dn / m] k^2.

The derivative is negative at all three tested densities. Independently,
the small-k eigenvalue's growth coefficient agrees with
k sqrt(-n dmu_chem/dn / m). The explicit mediator therefore retains the
instability; it was not solely an artifact of applying elimination outside
its regime.

## Results in the assigned homogeneous model

| Constituent density, /m^3 | f, mediator share of constituent number | n dmu/dn, eV | Fastest growing wavelength |
|---|---:|---:|---:|
| 1e6 | 0.0002398 | -4.7953e-13 | 1.266 m |
| 2.08238e9 | 0.15047 | -3.7796e-10 | 4.032 cm |
| 3e14 | 0.33262 | -1.5495e-7 | 1.860 mm |

The final density is the earlier illustrative 0.3 GeV/cm^3 divided by an
approximately 1 eV constituent rest energy. It is not an observed density
for this particle model. f counts two constituents per mediator: it is not
the mediator fraction of the number of all individual excitations.

At that density, mu_chem=-3.09576e-7 eV and energy per constituent is
-2.06273e-7 eV. The computed maximum linear growth rate is 2.78734e8/s.
These are properties of an infinite, zero-temperature coherent background;
the growth rate is not a measured astrophysical collapse time. The search
uses 401 logarithmic wave numbers and a local maximum refinement over the
stated bounded range. It is not a proof of the global spectrum at all k.

The scale h sqrt(n) remains only 7.59e-7 of the 1 eV carrier rest mass at
the largest density, so weak mediator elimination can fail even while the
nonrelativistic energy hierarchy remains small. This hierarchy alone does
not prove the complete mean-field approximation, ultraviolet matching or
omission of all other operators.

At low density the coherent continuum fastest wavelength exceeds the small
laboratory cavity. Neither that continuum prediction nor the large-density
instability can be inserted into the single-pair trapped-state lifetime.
Finite boundaries, sparse occupancy and the actual prepared state differ.

## Consequence for the original cold-energy goal

A homogeneous coherent equal-charge mixture on this minimum-composition
branch is not a stable replacement for the earlier repulsive single-species
cold medium. A substantial mediator population also prevents treating the
high-density system as a weakly perturbed gas of the two carriers alone.
The correct next alternatives are a statistical kinetic/multimode state,
a different conserved-charge population or additional independently motivated
interactions, each with a derived pressure and transport model. The optical
source's global neutrality remains a constraint on any charge-population
proposal.

This is not a universal no-go for every state of the theory. In particular,
finite kinetic stresses may change stability, but adding a guessed positive
pressure to this zero-temperature branch would not derive the required
finite-temperature state. That state must be calculated consistently, and
must still explain the repo's halo selection and dark-energy connection.

Twenty-one numerical checks pass: composition conservation, stationarity,
direct field linearization, chemical-derivative refinement, hydrodynamic
matching and plus/minus eigenvalue symmetry. The bounded-run manifest
validates the record. This is self-reviewed analytic/numerical evidence,
not a new Lean proof or a physical identification. The overall creation
objective remains open; the coherent-medium route now has a concrete
state-specific obstruction instead of an uncontrolled extrapolation.
