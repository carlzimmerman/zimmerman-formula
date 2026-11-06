# Coupled temperature and abundance feedback

Base b101d584e9. Target: stable abundance and temperature with outer flat curves,
v^4 proportional to Mb, and the normalization c sqrt(G rho_DE)/2 predicted.
Only this investigation directory is writable. No adopted-action changes.

Test local optically thin fixed-flux feedback, with linear cooling as in the
preceding result: T_dot=a F-b n T, positive constants. Particle source/sink
R=K F^s T^u n^v-D T^w n^z. Define d=z-v>0, h=u-w. Derive the steady conditions,
linearized eigenvalue determinant, and requirements for a constant-temperature
1/r^2 outer density over a radial interval and a family of luminosities. Keep
global gravity, transport, and non-power-law chemistry outside the local claim.
Account for possible number-change thermal coupling via -eta(T/n)n_dot;
show explicitly which conclusions are unchanged. This is a parameterized
kinetic model, not a newly derived microscopic reaction.

Concrete tests at dimensionless F=1, a=b=1:
A: n_dot=1-n, T_dot=1-nT (joint stable equilibrium).
B: n_dot=n(1-nT), T_dot=1-nT (candidate preserving the pressure relation).
Use initial (n,T)=(0.2,0.5),(2,0.5),(0.5,2),(3,2), integrate to t=60 with
DOP853 rtol1e-10 atol1e-12, max step0.1. A must approach (1,1) within1e-7.
For B test nT approaches1 within1e-7 and ln(n)-T is conserved within1e-7;
different invariants must not be reported as convergence to one state.
Compare final states to roots ln(n)-1/n=initial invariant.

Symbolic check of general Jacobian determinant with eta retained. Negative
control omits h in d+h and must fail the determinant and neutral-mode checks.
60 seconds, one thread. No empirical target, full halo stability proof,
microscopic production/cooling rate derivation, or automatic phase-pressure
selection is claimed. Numerical convergence is finite evidence; general
scope follows from the algebra, not the number of runs.

Pre-execution constructive extension C: a global homologous-halo feedback
X_dot=gamma(Theta-X), Theta_dot=epsilon(S-X Theta), where X=v_h^2,
Theta=2 kB T/m, S=B L, B=2 G kB sigma_abs/Lambda_1. The first equation is
an explicitly postulated global abundance feedback, not a derived microscopic
rate. Test whether it can stabilize both variables without fixing B. In units
X*=Theta*=sqrt(S), take rates1 and the same four initial states and time bound.
Check convergence to(1,1) and the exact Lyapunov identity for
V=(x-1)^2/2+(y-1)^2/2: V_dot=-(x-1)^2-x(y-1)^2. Distinguish this constructive
phenomenological attractor from deriving its material source, transport,
energy budget, boundary or the coefficient. No 1/2 used as an input.
