# Finite-region escape test for the kinetic companion

This is an exact linear response problem, not a new galaxy simulation. It
isolates the outlet in a fixed spherical medium with uniform scalar inertia
A>=1 inside radius R and vacuum inertia1 outside. Spatial gradient coefficient
is1 everywhere, radial measure r^2 dr, c=1. A sharp step is an idealization;
the mobile density, mediator boundary layer and two-state carrier are omitted.
The physical parent may be approximated this way only below its mediator cutoff.

Drive the scalar equation

    A(r) chi_tt-lap chi = -I(t) w(r),
    w=3/R^3 inside R, w=0 outside.

For harmonic I(t)=Re[I_omega exp(-i omega t)], let y=omega R,
x=sqrt(A)y. Regularity and outgoing boundary conditions give

    chi_in = S0/(A omega^2)+a sin(sqrt(A)omega r)/r,
    chi_out = b exp(i omega r)/r,
    S0=3I_omega/R^3,
    a = S0/(A omega^2) (i omega R-1)
                       /[sqrt(A)omega cos x-i omega sin x],
    b/I_omega = 3 exp(-iy) (x cos x-sin x)
                         /[x^2(x cos x-i y sin x)].

Both chi and its radial derivative match at R because only temporal inertia
steps. For A=1 this is exactly -3(sin y-y cos y)/y^3, the established uniform
sphere form factor. At fixed finite A, omega->0 gives b/I->-1. Raising inertia
does not suppress or enhance the leading zero-frequency external monopole.

Let G(omega)=chi_avg/I_omega, chi_avg=integral w chi r^2 dr. The exact average is

    G = [S0/(A omega^2)
         +3a (sin x-x cos x)/(R^3 A omega^2)]/I_omega.

At zero frequency G->-6/(5R), independently of A. Low-frequency evaluation
needs a series or higher precision because the displayed terms cancel.
The outgoing flux and material work obey the exact passivity identity

    -Im G = omega |b/I_omega|^2,
    <P_out> = omega^2 |b|^2/2 = -omega |I_omega|^2 Im G/2 >=0.

Proof: multiply (lap+omega^2 A)chi=S by chi*, integrate by parts over the
interior and a source-free outer shell, and take the imaginary part. The volume
terms are real. The outgoing boundary term has imaginary part omega |b|^2;
the right side is I_omega chi_avg*, whose imaginary part is
-|I_omega|^2 Im G. The factors use the same radial normalization as the CC
records; no hidden4pi conversion is made.

This distinguishes propagating flux from stored near-field energy. At
x=pi/2, |b/I|=3sqrt(A)/x^3. A finite high-inertia body can have cavity
enhancement at selected frequencies, as well as form-factor zeros at
tan x=x. Neither is a universal cooling enhancement. Width, source population,
material backreaction and internal energy change with the same parameters.

For a genuine collective coordinate q with mechanical L=(m qdot^2-K q^2)/2
and Q(q)=Q0+Cq, the interaction Q chi_t produces I=C qdot. Eliminating the
outgoing scalar gives the self-consistent mode equation

    K-omega^2 m+omega^2 C^2 G(omega)=0.

At low frequency G is negative real, so it adds inertia. For a real harmonic
test the absorptive part has the damping sign by the passivity identity.
One must solve this equation (or the full fluid dynamics), rather than assign
an external sinusoidal I and count all its power as free cooling. The finite
body response gives no derived values of m,K,C,R,A for an actual galaxy.

The low-speed fluid branch remains an obstruction to automatic fast cooling.
For c_s^2 small and fixed eta=C_local^2/w, the local lower speed squared is
approximately c_s^2/(1+eta) when A c_s^2 <<1+eta. The kinetic companion repairs
the fast cone without removing this slow-material inertia. The approximation
must not be extrapolated to arbitrarily large A at fixed c_s.

Outcome: finite-region escape is allowed and passive in this idealization;
kinetic completion does not by itself establish an adequate formation rate.
