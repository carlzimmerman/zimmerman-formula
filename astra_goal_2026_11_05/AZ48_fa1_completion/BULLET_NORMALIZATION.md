# Bullet source checked; 3D field still pending

The problem is frozen in FROZEN_BULLET.md, commit7cd8cf3ed7. These are
preparatory identities, not a solved Bullet field. Retired sector, adopts
nothing; kappa=1/2 FITTED; not theory closed.

The inherited signed mass totals2.3916e14Msun. The negative correction
shares its centre with the positive90kpc gas component. Their density ratio
in magnitude is

\[
R(r)=\frac{6.8}{15}\left(\frac{90}{70}\right)^3
\left[\frac{1+r^2/90^2}{1+r^2/70^2}\right]^{5/2}.
\]

The bracket decreases with r because70<90. Thus its global maximum is
R(0)=8262/8575=0.9634985422740525<1. The signed pair is positive at every
finite radius. All other components are positive, so no clipping or removal
is needed. This verifies the source model, not its observational calibration.

Set x=L0*q and pi=L0^2*A*phi in the physical equation. Since pi_ij=A*phi_ij,
choosing A=sqrt(8*pi*G*rho_ref/k) and dividing by8*pi*G*rho_ref yields
epsilon*lap(phi)+(lap(phi))^2-H_ij*H_ij=S, with
epsilon=1/sqrt(8*pi*G*rho_ref*k) and S=rho/rho_ref. No term is dropped.
For the arbitrary unit density1e5Msun/kpc^3, physical epsilon is
0.005074927248848183 canonical and0.00613309157174136 alt. Multiplying
the unit density by4 divides phi and epsilon by2, leaving physical pi and
the normalized Hessian selector unchanged. This is not a fitted parameter.

The rationalized spherical positive root is
phi'=2Q/[epsilon*r^2+sqrt(epsilon^2*r^4+8*r*Q)], with its zero-gradient
origin limit handled explicitly. An independent uniform-density analytic
solution verifies this branch and the spherical equation on both footings.

check_bullet_source.py passes24/24: exact source parsing, signed-pair bound,
paired16384/32768-point Plummer mass integrals, selector identities, physical
normalization and unit rescaling. The s->-s mutation fails the isotropic and
deep-point known answers (22/24, expected exit1). Both scientific outputs
repeat byte-identically.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python check_bullet_source.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python check_bullet_source.py --mutate

Run from this directory with NumPy. No3D discretization, elliptic solve,
boundary test, field convergence pair or Bullet classification has yet been
performed. All production solves remain heavyq-only.
