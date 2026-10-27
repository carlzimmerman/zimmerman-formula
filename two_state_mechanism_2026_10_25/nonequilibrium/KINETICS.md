# Finite assertion: radiative nonequilibrium molecular assembly

This extends the same Coulomb parent, not a new fitted force. M/mC=100 is retained,
not derived. The fine-structure coupling and constituent mass remain hypotheses.
Electronic energies use the leading clamped-nuclei mass convention B_A=1/2;
atomic radiative reduced mass is likewise 1. Nuclear motion uses mu=50 and
A+X translation uses mu=100*101/201. Neglected finite-electron-mass corrections
are O(1/M); these are not an exact finite-mass Coulomb calculation.

The g radial Hamiltonian is -d²/(2 mu dR²)+U_g+1/2+J(J+1)/(2 mu R²).
Keep each (v,J) level independently, with weight 2J+1 (no nuclear-spin/exchange
projection). Solve the u continuum at specified positive energies by Numerov,
matching to energy-normalized free spherical Bessel solutions at large R.
The normalization is sqrt(2 mu/(pi k)); bound waves have integral |u|² dR=1.
Electronic dipole d_gu is computed from the same electronic eigenvectors.
Absorption angular strengths from J are (J+1)/(2J+1) to J+1 and J/(2J+1) to J-1.
The resulting S_b(E) is squared dipole per unit continuum energy.

The low-order electronic basis breaks down at R=120. Do not use it there.
Use curves only through R=40 (alternate join 32). Thereafter the Coulomb
hydrogen ground-state polarization coefficient fixes -9/(4R^4); a R^-6
coefficient is set by continuity, separately for g and u. This is an asymptotic
approximation; join variation is tested. Dipole tends to R/2 with a matched
R^-2 correction. No environmental parameter sets either tail.

For omega=E+D_b:
 sigma_PI,b/(alpha a_D²)=(4pi²/3) omega S_b(E).
 k_b/alpha³=(4/3)g_b(2pi/mu_AX)^1.5 T^-1.5
             integral omega³ S_b(E) exp(-E/T) dE.
This is spontaneous recombination, obtained from the same matrix elements and
Milne reciprocity. For a Planck bath, replace exp(-E/T) by
exp(-E/T)/(1-exp(-omega/T)); then k_b/Γ_b equals the inverse Saha constant.
The mean incident energy uses an additional E in the same integral.
No independently adjustable forward/reverse rates or formation energy.

Restricted isolated parcel: X+C -> A+photon, A+X -> T_b+photon.
Initially x=c=1, a=t_b=0, thermal energy K=3 Ti per initial X,C pair.
x=1-a-2sum(t_b), c=1-a-sum(t_b). Temperature T=K/[1.5(1+x)].
Emission rates per pair are r_A=N k_A x c and r_b=N k_b a x.
Kdot=-<E>_A r_A-sum(<E>_b r_b); escaped radiation
Qdot=(B_A+<E>_A)r_A+sum((D_b+<E>_b)r_b).
Then K-B_A*a-sum((B_A+D_b)*t_b)+Q is constant identically;
x+2sum(t_b)+a=1, c+a+sum(t_b)=1, x+sum(t_b)-c=0.
Atomic cross section is the hydrogenic ground-state photoelectric formula;
its Milne inverse fixes atomic recombination. All radiation is outgoing in
this optically thin submodel. No external thermostat or arbitrary cooling rate.

IMPORTANT LIMITS: This is a radiative subnetwork and a homogeneous, fixed-density
parcel, not live gravity or rotating disk formation. No blackbody equilibrium is
imposed. Escaped photons cause no reverse reaction; this boundary condition must
be gated by computed optical depth. Independent thermal-bath reciprocity tests
exercise the reverse coefficient but do not replace radiation transport.
Collisional dissociation, dissociative recombination T+C -> 2A, u bound states,
other molecular species, spin statistics, line trapping, hydrodynamic work and
spatial transport are not included. A positive outcome cannot establish a
surviving charged phase; a negative outcome is restricted to this assembly path.

All four input environments use the same microphysics and initial ionized state.
Only baryonic mass/radius set density and virial temperature. These names label
proxies, not code branches or a predicted morphology. Keep the previous weak
coupling, classical dilution, low-temperature and nonrelativistic gates.
