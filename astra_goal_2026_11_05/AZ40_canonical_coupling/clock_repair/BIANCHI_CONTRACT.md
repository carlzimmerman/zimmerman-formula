# Nonlinear bounded-expansion discriminator

Before running: test the exact vacuum Bianchi-I sector of EH plus Fcap(Theta),
P=0, mu_K=0, Theta_star=0, with positive cap parameters b,T. This isolates the
new operator; it is not the full rolling-sinh scalar/dust candidate background.
Use proper time and volume V=product of three directional scale factors,
shear invariant sigma^2=S0/V^2. Reconstruct the lapse constraint from the
minisuperspace action before solving it. Test whether a finite contracting
solution exists beyond the unregulated Kasner volume zero and whether it
hits the cap at finite time. A positive dispersion alone is insufficient.

Algebra: prove monotonicity of the lapse constraint as a function of
r=-log(sqrt(1-Theta^2/T^2)); prove finite-time lower bound V>=V0 exp(-Tt)
and finite anisotropy/auxiliary momentum on every finite interval. Retain
possible asymptotic singularity at t=infinity and the inhomogeneous gaps.

Numerics: V0=1,T=1,b=.1,1,10,S0=1/3,3 (six cases). Evolve w=-log V to
5 times the corresponding unregulated tc=1/sqrt(3 S0). Solve the algebraic
constraint in r with brentq xtol=1e-13,rtol=1e-14; use DOP853 tolerances
(1e-9,1e-11) and (1e-11,1e-13), compare on501 fixed times. Volume discrepancy
normalized by1+fine V must be<1e-8; relative constraint residual<1e-10.
Record cap gap, minimum volume, auxiliary lambda and curvature/shear proxies.
No claim of a uniform continuum PDE estimate follows from these six ODEs.
Known answers: S0=0 gives Theta=0 and constant V; removing cap gives
V=1-sqrt(3 S0)t and its finite crossing. Those controls must distinguish the
mechanism. No threshold tuning, no new observations, one thread,60second cap.
