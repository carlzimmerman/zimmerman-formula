# Collision-dependent adiabatic action

Let x be a homogeneous scalar with constant kinetic coefficient K, and let
f_i be occupations in fixed comoving momentum bins (the phase-space weights
are absorbed into f_i). At a fixed scale factor a, write

    E = K xdot^2/2 + U(x,f,a),
    U = V(x) + sum_i f_i epsilon_i(x,a),
    I(E,f,a) = 2 integral_x-^x+ sqrt(2K[E-U]) dx.

I is the action per physical volume; the canonical comoving action is a^3 I.
The period is P=I_E. For every slow parameter lambda,

    I_lambda = -P <U_lambda>_orbit.

For reactions without coherent field recoil, the instantaneous total energy
loss is sum epsilon_i C_i, where fdot_i=C_i(x,f,a). Therefore the leading
averaged collision contribution is

    Idot_coll/P = sum_i [<epsilon_i C_i>
                                - <epsilon_i><C_i>].

It does **not** generally vanish: an on-shell resonance selects both momentum
and field phase. Setting Idot_coll=0 requires a separately justified zero
covariance, for example phase-independent C_i. Particle energy removed from
U must be deposited once into tracked daughters/radiation. A number-only
equation does not determine this energy or the action drift.

With physical occupations diluted by expansion, fixed comoving momenta, and
the scalar's 3H friction, differentiating the Hamiltonian gives

    Idot = -3 H I + P sum_i Cov_orbit(epsilon_i,C_i),

where C_i is the physical collision contribution, with the a^-3 measure
included consistently. The explicit a derivative of epsilon cancels between
E and I at fixed slow parameters. This result assumes slow H and collision
evolution per orbit, a closed bound orbit, and no separatrix crossing. It
does not justify averaging through disappearance of the trapping well.

## Independent analytic control

Take K=1, U=k x^2/2+n[m0+alpha x^2/2], and
ndot=-gamma n(1+beta x^2). At fixed n the orbit is harmonic,
omega^2=k+alpha n, x=A cos(omega t), I=pi omega A^2. Since
Var(x^2)=A^4/8,

    Idot_coll/P = -gamma n alpha beta A^4/16.

For beta>0 the sink cools the action; for a nonnegative sink weighted toward
the inner turning region (beta<0 in its admitted range) it heats the action.
At beta=0 the covariance vanishes. action_control.py compares this averaged
identity with direct microscopic dynamics and checks total energy including
the emitted radiation. This is a derivation/control of the averaging law,
not a calculation of the SU5 collision operator.
