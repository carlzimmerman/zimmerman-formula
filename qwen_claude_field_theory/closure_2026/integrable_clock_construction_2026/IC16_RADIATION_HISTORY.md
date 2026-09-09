# IC16: remove the artificial radiation ceiling, then test the new history

2026-09-08. **Constructive finite FLRW history, not full-theory closure.**
This calculation follows Carl's request to do the mathematics before
recombination. The density bound belongs to the old switch, not to all MOND
theories. The repair below changes that switch in the action itself.

## Explicit action revision

Retain the full covariant first-order action, fields, coefficient definitions
and boundary conditions of [IC5](IC5_ACTION.md), [IC10](IC10_LOCAL_CLOCK.md)
and [IC11](IC11_CLOCK_PRESSURE.md). Replace **every** occurrence of their
compact-window activation by

    E(v)=exp(-1/v) for v>0, and 0 otherwise,
    eta_up(r)=E(r²-1/2)/[E(r²-1/2)+E(3/4-r²)],
    r=-Np/(3mh0).

The denominator is everywhere positive; the function is smooth and even.
It is zero for r²<=1/2 and one for r²>=3/4. In particular it no longer
switches off the Einstein-clock branch just because the expansion is fast.

The full definition is

    H16=H10[eta -> eta_up]
        -eta_up exp(-4w) f(exp(2w) Xphysical),
    f(x)=(5mh0²/64)(2x)^16,
    S16=integral sqrt(-g) [2P:Q-H16] + Srad[g,theta],
    Srad=integral sqrt(-g) c_rad Zg²,
    Zg=-g^{mu nu} theta_mu theta_nu/2, c_rad>0.

The radiation model is an isentropic relativistic fluid with timelike
gradient, not a complete photon/baryon Boltzmann system. The new scalar is
ordinary radiation-fluid matter, not an uncounted gravitational auxiliary.
All numerical constants other than the switch retain the IC11 values.
This action is NOT IC14's reconstructed square plus IC13's repairs.

At static p=0 the switch is identically zero on an open neighborhood, so
the new switch and pressure terms have zero variations there. The existing
static exponential constitutive equation is retained with its existing
source, boundary and physical-potential caveats. This does not establish
cosmology-to-galaxy matching or baryon-only AQUAL by itself.

## Varying the sourced expanding restriction

On eta_up=1, varying both momentum components is exactly the stationary
Legendre elimination in IC10, because the switch derivatives vanish. With
g=z gtilde, z=exp(2w), X=-gtilde^{mu nu} T_mu T_nu/2=exp(-2S)/2,

    S16|plateau=integral sqrt(-gtilde)
      [mstar Rtilde/2 + P0(X,w)+f(X) + c_rad Z²],
    Z=-gtilde^{mu nu} theta_mu theta_nu/2,
    mstar=m exp(-1/6).

The equality of the radiation terms follows from z² c_rad(Z/z)²=c_rad Z².
Thus the independently varied equations are

    P0_w=0,
    nabla_tilde_mu(F_X nabla_tilde^mu T)=0,
    nabla_tilde_mu(2 c_rad Z nabla_tilde^mu theta)=0,
    mstar Gtilde_mu nu = F_X T_mu T_nu + F gtilde_mu nu
                         +2c_rad Z theta_mu theta_nu+c_rad Z² gtilde_mu nu,

where F=P0(X,w0(X))+f(X). Radiation leaves the algebraic vacuum root
unchanged; it does NOT leave the Hubble rate unchanged. Its pressure,
energy, kinetic coefficient and sound speed are respectively

    p_rad=c_rad Z², rho_rad=3c_rad Z²,
    Q_rad=6c_rad Z, c_rad,sound²=1/3.

The clock coefficients remain F_X and Q=F_X+2X F_XX. On this conformally
invariant restriction the frozen principal scalar blocks have no direct
clock-radiation derivative mixing. Einstein metric constraints and finite
wavelength gravitational effects are not a full CMB transfer calculation.

In flat FLRW, using Einstein proper time tau and scale factor Atilde,

    3mstar Htilde²=rho_F+rho_rad,
    rho_F=2X F_X-F,
    Atilde³ F_X sqrt(2X)=constant,
    rho_rad Atilde^4=constant,
    dS/dtau=3Htilde c_clock²,
    Hphysical=exp(-w) Htilde[1+3 c_clock² w_S].

The physical radiation density is rho_rad/z² and Aphysical=sqrt(z)Atilde.
The script checks its physical-frame continuity identity, not merely a
combined effective stress conservation statement.

## The old compact switch's exact bound

In m=h0=1 units the actual sourced activation is

    r²=exp(2S-1/6)(rho_F+rho_rad)/(3z0²).

For the OLD switch its upper plateau edge r²<=5/4 implies

    rho_rad <= (15/4)exp(1/6-2S)z0²-rho_F,
    rho_rad/(rho_F+rho_rad) <= 1-(4/5)r_vac².

If S is also in the old vacuum plateau, r_vac²>=3/4, giving the exact
conditional upper bound 2/5. Thus radiation cannot dominate there.
This premise must not be silently extended to other S or other actions.

On the previously identified vacuum component the numerical minimum of
r_vac² occurs at S=.085125275116295745. Its resulting fraction ceiling is
.129710273658402 and its radiation-density cap .431102328266416. This is
a located numerical extremum, not an interval-certified global maximum.

## A genuine finite history after changing the action

Choose S_initial=.03 and rho_rad,initial=10^16 in the stated normalized
units. These are selected initial data, not an empirical fit. Solve the
clock charge equation at 65 equally spaced Einstein-frame e-folds from
0 to 8. Radiation is evolved by its independent charge, not set to a
desired fraction at each point. At 60-digit precision:

| Result | Computed value |
| --- | ---: |
| physical e-folds | 7.88929066972590 |
| final S | .519622213300811 |
| minimum sampled radiation fraction | .989437651450873 |
| minimum sampled clock sound speed squared | 3.51608301716e-11 |
| final physical H / h0 | 8.02200905779 |
| final r² | 166.439567773 |
| largest relative clock-charge residual | 1.58e-43 |
| largest physical-radiation conservation residual | 2.49e-60 |

All 65 samples are expanding, inside eta_up=1, and satisfy the stated
clock linear health tests. The actual auxiliary block is computed from
P0+f at fixed canonical momentum, not fixed X; its singular-value rank is
computed, not supplied as input. Radiation adds no w derivative to it.
Independent quadrature checks a shorter charge-derived history.

The large span approaches the located F_X=0 endpoint
S*=.519622213335972. That endpoint is NOT certified: the clock sound speed
tends to zero, and the strong-coupling scale still needs calculation.
There is another concrete failure: S=.001 with rho_rad=10^16 is now
inside eta_up=1 but has negative clock kinetic coefficient. Opening the
switch exposes this ghost. IC16 is not globally healthy and is not the
final theory. A new pressure must remove this defect without merely
hiding it outside a diagnostic flag.

## Scope and reproducibility

Eight new unit tests and eight symbolic checks exercise the action weights,
Friedmann change, true density cap, switch, charge inversion and physical
conservation, including the exposed ghost as a negative control and an
independent finite-difference Raychaudhuri check.

    python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p test_ic16_radiation_history.py
    python3 -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic16_radiation_history.py --require-full-closure

The strict report exits 2. No new transition closure, strong-coupling cutoff,
all-background two-tensor count, full dust perturbations, physical Phi/Psi,
PPN, empirical recombination spectrum or global novelty has been established.
