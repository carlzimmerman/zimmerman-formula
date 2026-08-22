# Morning status — 2026-08-22

## The equation

The frozen action's static field equation (derived, not inserted; the only new object is one
dimensionless constant eps):

    div[ mu(X,Y) grad Phi ] - (c^4/a0^2) d_i d_j [ eps A(X) S_ij ] = 4 pi G rho

    mu = 1 + F_X = x/(1+x) + eps A'(X) Y      x = |grad Phi|/a0
    A(X) = X^2/(1+X)^4                        S_ij = d_i d_j Phi - (1/3) delta_ij lap Phi

Its whole new content condenses to ONE dimensionless coupling per system:

    chi = eps c^4 / (G M a0)        <- scales as 1/M: 6.5e23 (Sun) vs 6.5e12 (10^11 Msun galaxy)

## Tonight's decisive number (linear response, stable solver, validated machinery)

    dq_zz/dchi = +0.304 (Blanchet-Novak eta=1.583)   +0.413 (DHF fiducial eta=1.852)

q_zz(0) is NEGATIVE (-0.226 / -0.259, reproducing published exact-AQUAL to 1.9%), the
derivative is POSITIVE: **the tidal sector suppresses the Solar-System quadrupole**, driving
it through zero at chi ~ 0.63-0.74 — INSIDE the indicative ellipticity cap chi <= 1.73.

Cassini-compatible windows (linear order), DHF fiducial: chi in [0.48, 0.78] at 2 sigma,
[0.58, 0.68] at the central value. Required eps ~ 1.1e-24, i.e. M* ~ 0.6-0.7 Msun.
Galaxies sit at chi ~ 1e-11: RAR/BTFR untouched. Every check: delta-independence 6e-5,
Hessian identity 4e-3, chi=0 limit = validated AQUAL.

## What this is NOT yet

- Linear order only. chi ~ 0.6 is not small; O(chi^2) unknown. The full nonlinear BVP needs
  an implicit fourth-order solver (the naive lagged one is unconditionally unstable - shown).
- Single-potential weak-field equation. The exact ADM variation may split the tidal operator
  into the Psi equation (slip at order eps). The 10-agent first-principles program (exact
  variation, DOF/Hamiltonian, PPN, GW, FLRW, naturalness, adversary) is running now.
- eps ~ 1e-24 is unexplained. M* ~ 0.6 Msun is put in by the value of eps, not derived.
- a0 = 9.3619e-11 is an INPUT of this action. Not derived from Lambda here.

## The free prediction

The same chi ~ 0.6 that fixes the Sun applies to every solar-mass system: WIDE BINARIES
inhabit chi ~ 0.5-1. The theory therefore predicts modified wide-binary dynamics CORRELATED
with the Q2 suppression - directly relevant to the Gaia DR4 preregistration.
