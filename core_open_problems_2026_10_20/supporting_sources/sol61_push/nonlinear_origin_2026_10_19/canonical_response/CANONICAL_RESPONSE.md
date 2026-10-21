# A rational compression law from canonical scalar particles

19 October 2026. Parent CE-SHARED-STATE-2026-10-19 / CE-FM092.
This is a conditional daughter-particle state, not a modification of the
original action. The input model and retained matched contact are those in
`../TARGET.json`. Natural units set k_B=1; hbar is displayed.

**Result.** A nondegenerate isothermal gas in a harmonic baryonic core gives
the exact classical response `p(E)=p_sat E/(a+E)` and its logarithmic
connected free energy. The responding operator is a mass second moment,
conjugate to an isotropic gravitational curvature increment. It is not the
total internal mass dipole conjugate to uniform acceleration. Its actual
quantum transition gap is `2 hbar omega`, and its population response is
essential. The shape depends on the thermal protocol, and its normalization
depends on the inventory and core. These distinctions prevent promoting
this positive construction into the requested universal dipole law.

## 1. State and physical source

Consider N prepared daughter particles of mass m in the dilute NR,
Maxwell-Boltzmann regime. A centered, supported baryonic core supplies a
harmonic potential over the occupied cloud. Neglect scalar self-gravity and
contact energy at leading tracer order. Let

\[
 H(E)=\sum_{i=1}^N\left[\frac{p_i^2}{2m}
             +\frac m2(\kappa_0+E/L)r_i^2\right],\quad
 Q=\frac{m}{2L}\sum_i r_i^2,\quad a=\kappa_0 L>0 .       \tag{1}
\]

Here L is a fixed length defining the source amplitude, E has acceleration
units, and E>-a is the stable harmonic domain. This is the physical
curvature source `H(E)=H(0)+E Q`. A uniform core has
`kappa_0=4 pi G rho_b/3`; increasing its overlapping positive density adds
the displayed isotropic curvature. A remote vacuum tide is traceless and
does not provide this source. A uniform acceleration couples instead to
the total center of mass. With the baryon recoil included, its internal
mass-dipole operator vanishes as in the parent packet.

Equation (1) is a tracer reduction about a stated host center, not a proof
that the original action creates or supports this host. Its controlled
window requires `n lambda_T^3 << 1`, `g2 n << T`, scalar self-gravitational
energy per particle much smaller than T, NR velocities, small potentials,
energies below the eliminated-channel detuning, and cloud size well inside
the harmonic core. Recoil, host deformation and anharmonic corrections
must be small or solved in the shared state. Finite baryon support, N,
temperature, a heat receiver and equilibration time are physical inputs.

An ideal quadratic Hamiltonian confines globally; a finite Newtonian core
does not. Its potential tends to a constant at infinity, and the
unrestricted classical canonical partition function then diverges. In a
finite core, (2) describes a spatially confined or conditioned metastable
cloud only to the extent that escape and the outer-tail correction are
controlled. No such boundary, lifetime or tail error has been derived here.
The exact assertion is for (1); the finite-core realization is conditional.

## 2. Exact classical distribution and rational saturation

At fixed T, integrate the actual canonical phase space, including `1/N!`
which cancels in partition-function ratios. Put `s=1+E/a`. Gaussian
integration gives

\[
 \frac{Z(E)}{Z(0)}=s^{-3N/2},\qquad
 \langle Q\rangle_E=\frac{3NT}{2(a+E)},\qquad Q_0=\frac{3NT}{2a}.
                                                               \tag{2}
\]

The induced decrease in width is therefore

\[
 p(E):=Q_0-\langle Q\rangle_E
       =Q_0\frac{E}{a+E},\qquad p_{\rm sat}=Q_0 .          \tag{3}
\]

No distribution of two-level gaps was imposed. In the reference state Q
has the Gamma distribution with shape `nu=3N/2` and scale `theta=T/a`.
The exact Laplace transform `⟨exp(-E Q/T)⟩_0=s^(-nu)` is its origin.
The connected free energy is

\[
 F(E)-F(0)-E Q_0
 =-Q_0\left[E-a\log(1+E/a)\right],\qquad
 -\partial_E F_{\rm conn}=p(E).                            \tag{4}
\]

The linear subtraction defines a connected response. It does not remove
the baseline cloud mass or Q_0 from the complete gravitational source.
In particular it is not permission to add a compensating action term.
The induced observable `Q_0-Q` is bounded above but unbounded below; this
is not a finite bounded dipole. Negative E weakens the confinement and
leads to a pole at -a. Odd continuation as a function of a signed vector
acceleration is neither (1) nor (3). The two-sided rational cusp demanded
of a polarization law is not derived by this construction.

## 3. Heat exchange selects the power

The isothermal oscillator energy is `U_s=3NT`. Quasistatic compression
does work

\[
 W_{\rm on}=\int_0^E\langle Q\rangle_{E'}dE'
            =\frac{3NT}{2}\log s,                         \tag{5}
\]

all of which must leave as heat. The original conservative scalar action
does not by itself justify an infinite fixed-temperature receiver.

For an isolated adiabatic harmonic cloud, action conservation gives
`T(E)=T_0 sqrt(s)` and `p=Q_0[1-s^(-1/2)]`. More generally, suppose the
cloud equilibrates quasistatically with a passive receiver of constant
positive heat capacity C_b. The oscillator heat capacity is C_s=3N.
Conservation of their combined entropy gives

\[
 (C_s+C_b)\log(T/T_0)-\frac{C_s}{2}\log s=0,\quad
 \eta=\frac{C_s}{2(C_s+C_b)},\quad
 p(E)=Q_0[1-s^{-(1-\eta)}].                               \tag{6}
\]

The deficit exponent ranges from one-half at C_b=0 to one only as
`C_b/C_s -> infinity`. Direct differentiation also gives
`dU_tot/dE=⟨Q⟩`, consistent with the first law. Negative-heat-capacity
self-gravitating receivers are outside this positive-C_b model. A large
receiver may approximate the rational shape on a finite window, but
neither its size nor the loading is fixed by the action.

## 4. Actual quantum gaps and occupations

In the nondegenerate quantum oscillator gas, write
`omega=sqrt(kappa_0+E/L)` and `x=hbar omega/(2T)`. Exact single-particle
oscillator traces give the following formulas exactly for N=1, and with
the factor N in the independent Maxwell-Boltzmann trace:

\[
 \langle Q\rangle_E=\frac{3N\hbar}{4L\omega}\coth x,
 \qquad
 \chi_{\rm iso}:=-\frac{d\langle Q\rangle_E}{dE}
 =\frac{3N\hbar}{8L^2\omega^3}
       [\coth x+x\operatorname{csch}^2x].                 \tag{7}
\]

The actual Cartesian level populations are
`P_n=(1-exp(-hbar omega/T)) exp(-n hbar omega/T)` in each direction,
with the fixed-N Maxwell-Boltzmann tensor trace. Exchange corrections
require a Bose trace and change (2). The operator `m x_i^2/(2L)` has
diagonal matrix elements `hbar(2n+1)/(4L omega)` and connects n to n+2
with matrix element `hbar sqrt((n+1)(n+2))/(4L omega)`. Its nonzero
transition line is thus `2 hbar omega`, not an arbitrary occupied
continuum of reduced gaps. The equilibrium susceptibility splits into

\[
 \chi_{\rm off}=\frac{3N\hbar}{8L^2\omega^3}\coth x,
 \qquad
 \chi_{\rm pop}=\frac{3N\hbar}{8L^2\omega^3}
                         x\operatorname{csch}^2x .        \tag{8}
\]

The second term differentiates the populations and needs thermal
relaxation. It is absent from the isolated frozen-population adiabatic
response, and must not be identified with an additional retarded
transition line. In the classical limit the two terms contribute equal
halves to the isothermal susceptibility.

The partial fraction expansion of coth gives
`0 <= x coth(x)-1 <= x^2/3` for x>0. This bounds the relative quantum
correction to the classical width by `x^2/3`. The expansion was checked
against [NIST DLMF 4.36.3](https://dlmf.nist.gov/4.36.E3), accessed
2026-10-19; no local PDF is claimed. For fixed T at sufficiently strong
compression, zero-point motion dominates and the width falls as
`E^(-1/2)`, not `E^(-1)`, in the one-particle harmonic control. For N>1
the nondegenerate approximation can itself fail before this limit, and
contact energy can become important. The control is not an extrapolation
of the many-particle MB state through degeneracy. The exact classical
rational curve therefore holds only in a classical and tracer window,
not to arbitrary field.

## 5. Gravitational normalization remains a state condition

At E=0, `chi_ind=3NT/(2L^2 kappa_0^2)`. Let the cloud occupy reference
volume V, `rho_d=Nm/V`, and
`⟨r^2⟩_0=3T/(m kappa_0)`. In a uniform baryon core,

\[
 4\pi G\frac{\chi_{\rm ind}}{V}
 =\frac32\frac{\rho_d}{\rho_b}
                  \frac{\langle r^2\rangle_0}{L^2}.       \tag{9}
\]

This is dimensionless but depends on inventory, host density, temperature,
source convention and volume. Setting it equal to one is an extra state
condition; it is not a prediction. For example choosing L equal to the
reference rms radius still requires `rho_d/rho_b=2/3`. Further, this is
the susceptibility of an isotropic curvature moment; equating it to the
uniform-acceleration polarization coefficient would mix different
operators. The action has not supplied the needed operator bridge or
normalization selection.

## 6. Evidence and remaining route

`run_001` completed 104 bounded controls: Gamma reweighting and moments;
actual 120-level oscillator sums for the mean, transition response and
population response; finite-temperature derivatives; the coth bound;
finite-receiver entropy and first-law identities; and the separate TF
constants in `STRONG_SOURCE.md`. These checks support the stated exact
formulas and finite examples, not the neglected host dynamics, a
continuum-state error bound, a thermalization rate or a universal law.

The next meaningful extension is a supported, live baryon core and a
finite scalar receiver with a derived heat-exchange rate. Its complete
source must still be varied before comparing to the acceleration law.
The rational width mechanism is a useful positive construction without
closing the original dipole or gravitational-normalization problem.
