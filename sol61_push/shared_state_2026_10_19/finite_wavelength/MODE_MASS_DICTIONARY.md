# Actual size–gap scaling in a shared-state family

The exactly solvable common-profile TF state has a fixed R at fixed K_d,K_b,
but a free mass amplitude M. Use the odd finite-wavelength source
D_k=integral rho sin(kz)/k in the COM frame. For fixed probe kR
and a fixed **source-carrying total-density internal mode** nu, rescaling the
linear fluid equations and the mass-metric normalization gives

    omega_nu^2 = c_nu GM/R^3,
    chi_nu(k)=A_nu(kR) R^3/G,
    |<1_nu|D_k|0>|^2=d_nu^2= (hbar/2) chi_nu omega_nu.      (1)

The shape constants c_nu>0,A_nu>=0 depend on the actual eigenmode and source.
Compensated composition modes have A_nu=0 and cannot supply these dipoles.
Both the mode lane and the root finite-k calculation derive those source
factors rather than using an inventory of independent hosts.

For A_nu>0, the *reduced* gap relevant to a proposed two-level comparison is

    Delta_nu=hbar omega_nu/(2d_nu),
    d_nu=chi_nu Delta_nu,
    M=4 chi_nu^2 R^3 Delta_nu^4/(hbar^2 c_nu G).             (2)

Thus d_nu is proportional to M^(1/4), Delta_nu to M^(1/4), and the
source-conjugate zero-point displacement scale d_nu/M to M^(-3/4).
The bulk geometric R does not equal that matrix-element displacement.
This derives a concrete joint size–gap relation for the conditional shared
state. It is not the arbitrary d proportional to Delta^(-1/3) family that
passed the parent packet's abstract integrability test.

The mode remains a harmonic many-level oscillator. Using only its first
transition does not prove that it saturates as a two-level object. The
following test is therefore conditional on a proposed one-mode-per-object
saturating identification, rather than a claim that such sites were derived.

Suppose a population of these self-similar objects is proposed, with each
counted once in that fixed mode, and with n(Delta)dDelta objects per volume.
The source-magnitude inventory w=n d then fixes—not independently frees—
the object number and total mass:

    N_objects = (1/chi_nu) integral w(Delta)/Delta dDelta,
    rho_objects = [4 chi_nu R^3/(hbar^2 c_nu G)]
                        integral Delta^3 w(Delta)dDelta.   (3)

For the target w=p_sat a Delta/(a^2+Delta^2)^(3/2), the object number is finite,
p_sat/(chi_nu a). The mass integral diverges quadratically in the UV. At a
finite reduced-gap cutoff L its exact moment is

    integral_0^L Delta^3 w dDelta
      =p_sat a [L sqrt(L^2+a^2)/2 + a^2 L/sqrt(L^2+a^2)
                    -(3a^2/2) asinh(L/a)]
      ~ (p_sat a/2)L^2.                                   (4)

Equivalently a target distribution over actual object mass would require
n_M(M) proportional to M^(-3/4) at its formal soft end and M^(-3/2) at its
formal hard end. The latter has infinite mean mass. This is a new
state-specific obstruction, obtained using the actual source-mode relation
(2); it is stronger than assuming a fixed dipole by hand. A finite mass
cutoff makes the integral finite and permits only a stated interpolation
window. Low masses eventually leave the TF regime, and high masses leave
the Newtonian/source-eliminated regime; (2) is not extrapolated as a physical
law past either cutoff.

One cannot evade (3) by treating every transition of the same many-level
object as an independent full-mass host. That would double count its mass
and source strength. Multiple actual modes instead use their shared
Hamiltonian, source matrix elements and occupations in OCCUPATIONS.md.
Nor does (3) exclude all multimode, dense, non-TF or correlated phases.

Finally even before matching the distribution, the target static
normalization would require nu_objects chi_nu=1/(4piG), i.e.

    nu_objects R^3=1/[4pi A_nu(kR)].                        (5)

For this odd long-wavelength source A_nu is suppressed as (kR)^4;
even/tidal source channels can have a different leading power.
Separated objects cannot supply the required packing; the complete mode
sum in FINITE_WAVELENGTH.md gives 4piG chi_eff=3C f(kR)^4.
Choosing a free object number to impose (5) is not a normalization prediction.
This calculation supplies an explicit conditional size/gap/abundance
dictionary and a finite-mass test. The original action still needs a
formation-selected state and genuine nonlinear saturation.
