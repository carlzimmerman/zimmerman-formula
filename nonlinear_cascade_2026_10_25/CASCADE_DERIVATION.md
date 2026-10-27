# Derived transfer, cubic vertices, and reciprocal escape

This is an internal derivation. No external theorem, novelty claim, or new
microscopic derivation of the optional CC operator is used.

## Exact transfer in the actual radial action

Write the positive material-gradient matrix as K=U diag(lambda) U^T and let
c_s=U^T a_s. The full inherited dynamics is

    i sigma a_t=K a+N_gravity+N_Fpressure+N_response+N_alignment+N_inertia.

For any fixed set B of kinetic eigenvectors, its positive gradient energy obeys

    dE_B/dt=(2/sigma) Im sum_s,k in B lambda_k c_s,k* (U^T N_s)_k.

Every N is the actual Hamiltonian force, including carrier-inertia density
backreaction and reciprocal chi. No density history or pump is supplied.
The midpoint implementation has the corresponding exact quadratic work
identity. These are kinetic bands, not full Hamiltonian normal modes. Their
spatial support and actual conversion-source time spectrum must be checked
separately before inferring a fast escaping population.

The scalar far-field continuum response of a radial integrated source S_i is

    chi_omega(r)=-exp(i omega r/c)/(c²r)
                sum_i S_i,omega sinc(omega r_i/c).

A finite tapered source gives a windowed spectral estimate, not an exact
spectral accounting of the measured finite-window500kpc flux.

## Local angular route: explicit additional continuation assumption

The radial nonlocal response energy has not previously specified arbitrary
angular density variations. For a local WKB calculation only, choose the
rotationally covariant continuation

    E=integral [rho |grad S|²/2+kappa |grad rho|²/(8rho)
                +W(|g0+delta g|)-|delta g|²/2] dV,
    div(delta g)=delta rho, curl(delta g)=0,
    W(u)=-log(1-u)-u.

The uniform background g0=u e_z is held on the patch scale. Linear terms are
subtracted. This is a stated3D continuation of the pure-T radial sector, not
a uniquely derived nonspherical theory or a full interface model. The pure-T
sector has no F pressure, alignment conversion or moving interface, so it
cannot alone establish the requested joint galaxy conditions.

For Fourier k, delta g_k=-i k delta rho_k/k². With rho0>0 and u>0,

    omega_k²=rho0[(a_perp-1)+(a_parallel-a_perp)cos²(theta)]
                 +kappa k^4/4,
    a_parallel=1/(1-u)², a_perp=1/(1-u).

Set A_k=sqrt(rho0 k²/(2omega_k)), B_k=1/(2A_k), and
rho_k=A_k(b_k+b_-k*), S_k=-i B_k(b_k-b_-k*).
For k3=k1+k2, the resonant cubic Hamiltonian is

    H3=V123 b1 b2 b3*+conjugate,
    V123=(V_velocity+V_quantum+V_response)/sqrt(volume),
    V_velocity=A1 B2 B3 k2.k3+A2 B1 B3 k1.k3+A3 B1 B2 k1.k2,
    V_quantum=-kappa A1 A2 A3/(4rho0²)
                         [k2.k3+k1.k3-k1.k2],
    V_response=-i A1 A2 A3 C[k1,k2,k3]/(k1²k2²k3²).

The third derivative tensor of W is

    C_ijk=[(3u-1)/(1-u)³] e_i e_j e_k
           +[1/(1-u)²](e_i delta_jk+e_j delta_ik+e_k delta_ij).

All three terms matter. Omitting the quantum-pressure cubic vertex produces
spurious scattering even for the exactly linear free Schrödinger field.

For equal transverse parents |k1|=|k2|=q, define Delta²=rho0(a_perp-1).
Resonance determines d=1+cos(angle)=sqrt(1+3Delta²/(kappa q^4)). It exists
only if q^4>=Delta²/kappa. Here V_response=0 and the exact combined vertex is

    V123=V_velocity Delta²/omega_q²,
    V_velocity=q² sqrt(d)(d+1)/(4A_q sqrt(volume)).

This cancellation is structural. At Delta=0 the on-shell vertex vanishes,
as required by free Schrödinger evolution. At large q the interaction weakens,
rather than growing like the individual large gradient terms.

## Depleted pump and field backreaction

For a single resonant triad, i b1_t=V* b2* b3, i b2_t=V* b1* b3,
i b3_t=V b1 b2. With real positive V and b1=b2=sqrt(N0), b3=0 initially,

    b1=b2=sqrt(N0) sech(V sqrt(N0)t),
    b3=-i sqrt(N0) tanh(V sqrt(N0)t).

Thus the pump depletes and the Manley-Rowe invariants hold. A prescribed
undiminished pump is not used. Initial modal amplitudes in the local test
are declared weak standing-wave perturbations, not asserted to equal actual
infall occupations. NC1 supplies actual infall evidence separately.

For opposing modes +/-k, the compact monopole part of the CC charge is

    Q=2g2 sum_k A_k²[N_k+N_-k+2Re(b_k b_-k)].

For modes of a common omega, define O=sum_k A_k² b_k b_-k. The oscillatory
charge amplitude is4g2|O| and the emitted scalar power to leading compact
order is128g2² omega^4 |O|²/c³ times the source form factor squared.
The uniform spherical patch has F(x)=3(sin x-x cos x)/x³, x=2omega R/c,
and static self-kernel D=6/(5R). Its reciprocal leading envelope terms are

    H_reactive=-16g2² omega² D |O|²/c²,
    b_k,t|loss=-(32g2² omega³/c³)|F|² A_k² b_-k* O.

The conjugate partner has the reciprocal term. Collective interference is
retained for degenerate parent pairs. These terms remove the same resonant
wave energy that appears in the outgoing-flux ledger; the reactive frequency
shift can detune a weak triad and must not be dropped. They are a compact,
weak-coupling, rotating-wave reduction, not the full field equations.
Check frequency shift/omega, compactness and source amplitude before use.
The tests record secular wave energy plus outgoing energy; they do not claim
an exact all-orders energy ledger for the omitted nonresonant Hamiltonian.

## Material mesh is part of the cascade test

On a locally uniform material mesh, the positive Schrödinger gradient has

    lambda(k)=2 kappa sin²(k h/2)/h².

Coarsening h decreases its entire propagating band. A high-frequency packet
can reflect from a coarse tail while discrete mass and energy are conserved.
Consequently conserved energy and a scalar-grid refinement alone cannot
certify that material sound or waves reach the free outer reservoir. The
new packet controls and refined full initial-value runs address this distinct
obstruction. They do not retroactively certify an untested continuum limit.
