# Which part of the shared example is fixed by the scalar benchmark?

This is a dimensional control, not an astrophysical candidate or a formation
calculation. The scalar coefficients use the declared original benchmark
m=1 MeV/c^2 and lambda_rep=0.00587528017. The baryon closure is the ideal
nonrelativistic fermion model with spin degeneracy two in EQUILIBRIUM.md,
with a declared
constituent mass 1.67492749804e-27 kg. The scalar action does not select that
baryon EOS or composition. Ordinary matter's electromagnetic, nuclear,
chemical and weak-interaction behavior is outside this ideal mechanical
closure; no stable free-neutron object is proposed by this unit map.

Write physical K=lambda_rep hbar^3/(4m^4c), and
K_b=hbar^2(6pi^2/g_b)^(2/3)/(5m_b^(8/3)). To map the mixed TF example's
dimensionless G'=1/(4pi), K'=1/2, K_b'=2/5 to SI, the length, mass and time
units are fixed—not free fitting constants:

    L0^2=K G'/(G K'),
    M0=[K_b G'/(G L0 K_b')]^3,
    T0^2=G' L0^3/(G M0),
    tau'=hbar^2 T0^2/(2m^2 L0^4).                           (1)

The bounded script checks the three unit conversions independently and gives

    L0=3.68347e7 m, M0=8.25319e16 kg, T0=2.68700e7 s,
    rho0=M0/L0^3=1.65139e-6 kg/m^3,
    tau'=6.86261e-25.

For the formal common-cutoff TF state with central enthalpy one,
x1=2.36924317416 and radial masses N_d=1.26043509806,N_b=.841802494120,
the scale map is

    R=x1 L0=8.72704e7 m,
    M_d=4pi N_d M0=1.30723e18 kg,
    M_b=4pi N_b M0=8.73056e17 kg.                            (2)

These TF branch numbers are not asserted to identify the global minimum at
those two masses or the exact finite-GP solution. The existence proof gives
a minimizing state; the common-cutoff TF stationary control is distinct.
The very small tau' is far below the .2,.05,.0125 values used in the finite-
GP numerical controls. It would be incorrect to label those moderate-tau
profiles as numerical realizations of (2). No new stiff tiny-tau BVP was run.
The variational TF limit controls the limiting set of minima without a
specific finite-tau surface or mode-error rate.

At the formal TF center the declared microphysical regime ratios are

    G(M_d+M_b)/(R c^2)=1.85529e-17,
    p_F/(m_b c)=6.46672e-9,
    n_d a_s^3=9.09298e-26,
    (scalar contact energy)/(M_X-2m)=5.22784e-14,

using a_s=lambda_rep hbar/(8pi m c) and the declared source u_star=.02.
These show compatibility with the scalar NR/dilute/source-eliminated
hierarchies for this ideal TF scale comparison. They do not establish the
baryon closure's material realism, condensation, cooling, chemical stability,
production, or a halo abundance. Substituting a physically justified different
baryon EOS changes the state problem and its scale map.

`run_calibration_001` completed with twelve finite checks under 30-second
wall, 20-second CPU, one-thread and 65536-byte log limits. The additional
checks compare the exact target mass moment in MODE_MASS_DICTIONARY.md with
independent quadrature at cutoffs 1,2,10,100. The inputs are declared numerical
values rather than a new precision measurement or an uncertainty budget.
