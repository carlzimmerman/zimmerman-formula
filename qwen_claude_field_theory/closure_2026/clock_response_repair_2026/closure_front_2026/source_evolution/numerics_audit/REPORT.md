# Independent numerical coordinate audit

Base: `486edc78eaed87647c0b605cdbebccb996a464cf`, with the existing dirty
worktree recorded by the runner. Scope: the new `source_evolution/evolve.py`
and its tests, the literal sourced quadratic action in
`../finite_wavelength/probe.py`, `PROBE.md`, the ADM coefficient definitions,
and the unchanged `nonlinear_evolution_2026/constitutive.py`.

**Verdict:** no equation, forcing-sign, or initial-momentum error found in the
reviewed finite-mode implementation. The original canonical coordinates have
severe avoidable numerical cancellation. An exactly equivalent canonical
shift reduces DOP853 work for the audited case from 28,438 to 166 function
evaluations, with a maximum force-response difference of approximately
`1.67e-13` on the 161 sampled times. This is a bounded floating-point
cross-check, not a global existence or physical viability result.

## Equation and initial-data review

With `M2=1`, the implemented `Theta`, `Sigma`, `C`, `D`, and `E` agree with
the stated sourced ADM action and the documented clock-derivative notation
map. In particular, `D` includes `-2*q*q*P_Xt`, and `E` includes
`-3*H*W_t`; these time derivatives were not frozen. Expanding the square in
the reduced action gives the implemented `A`, `B`, `Ce`, `F`, and `S`, with
both source terms negative as coded.

Setting zeta and its initial derivative to zero requires
`p(0)=a(0)^3*F(0)`, which the implementation uses. Setting canonical momentum
to zero instead would choose a different dynamical initial condition. The
clock and lapse need not vanish on this constrained sourced slice. Source
conservation is consistent with `rho=amplitude/a^3` and a finite initial-time
problem; this is not an abruptly switched source.

The original zeta Euler equation and original momentum relation give
`pdot=2*a^3*r*(zeta+n)` and `p=2*a^3*LapB`. Therefore
`u=-p/(2*a^3*r)`, with `(a^3*r)dot=H*a^3*r`, gives the coded `udot`.
Consequently `Phi=Psi` is an exact identity of this quadratic system. Checking
the two reconstructed values remains useful as an implementation control;
their equality is not an independently fitted slip result.

The existing residual tests mostly share `coefficients()` with the evolution
path. They check elimination and reconstruction well, but do not independently
authenticate the upstream covariant-to-quadratic derivation. That upstream
claim remains supported by the separate existing ADM derivation, not by these
trajectory tests.

## Equivalent coordinates and retained time derivatives

Let `h=2*r/Theta`, `g=-rho/Theta`, and

    w = p - a^3*(h*zeta+g).

This subtracts `d[a^3*(h*zeta^2/2+g*zeta)]/dt` from the time-dependent
Lagrangian. It changes no equation or constitutive coefficient. Set

    Theta_dot = Hdot + 3*gamma*q^2*qdot,
    Bt = J*R*r/den,
    Ft = -J*f/den,
    Ct = 2*r*((Theta-H)/Theta+Theta_dot/Theta^2) + R^2*r^2/den,
    St = S-rho*Theta_dot/Theta^2.

Then

    zetadot = (w/a^3-Bt*zeta-Ft)/A,
    wdot = a^3*(Bt*zetadot+Ct*zeta+St).

The transformed zero-dynamical initial data are `w(0)=a(0)^3*Ft(0)`.
The source is still `amplitude/a^3`; its time derivative is explicitly
included in `St`. Three exact symbolic checks in `audit.py` verify the
velocity, momentum derivative, and the equivalent potential expression

    Phi = ((H-Theta)/Theta)*zeta
          + H*w/(2*a^3*r) - H*rho/(2*r*Theta).

The last expression avoids cancellation of the leading zeta terms in
`-zeta+H*p/(2*a^3*r)`. The audit also reconstructs the original `(zeta,p)`
and evaluates the original `fields()` for comparison. No background jet or
raw coefficient was replaced in these runs, so the coordinate change alone
accounts for the improvement in solver work.

## Bounded run and provenance

The actual audit uses `k=100`, `gamma=1e-6`, `amplitude=1e-7`,
`0<=t<=4`, and 161 common sample times. It also checks the coordinate
transformation on 21 arbitrary small states using NumPy PCG64 seed 803.
Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, and SymPy 1.14.0 were used.

| Integration | Relative tolerance | Function evaluations | Maximum response difference from shifted DOP853 `1e-12` |
| --- | ---: | ---: | ---: |
| Original canonical DOP853 | `1e-10` | 28,438 | `1.67e-13` |
| Shifted DOP853 | `1e-10` | 166 | `9.01e-13` |
| Shifted DOP853 | `1e-12` | 295 | reference |
| Shifted Radau | `1e-10` | 1,373 | `1.23e-14` or less |

The reference final response `-2*r*Phi/rho` is
`1.0000364165923046`, and its initial value is `1.0000735160640626`.
For zeta itself, the looser transformed DOP853 differs from the tighter run
by about `2.45e-8` relative to the maximum zeta amplitude: the scalar amplitude
is much smaller than the source-based absolute tolerance scale. This does
not spoil the potential comparison here, but it cautions against reporting
scalar-state digits based on the nominal relative tolerance alone.

The arbitrary-state floating coordinate comparison reaches relative error
`1.33e-10` when evaluated through the original formulas. The corresponding
symbolic identities vanish exactly, so this sampled discrepancy reflects
floating arithmetic in the ill-conditioned original representation rather
than a different transformed equation.

Durable evidence is `run_002/manifest.json` with the complete numerical JSON
in `run_002/stdout.txt`. The version 2 manifest validates with current input
hashes. The runner enforces a 90-second wall limit and a 1 MiB output limit;
the requested numerical-library thread cap is cooperative. `run_001` is
retained as historical output: its execution succeeded, but root subsequently
updated `evolve.py`, so its input hashes no longer match the current file.

Reproduce from the repository root using the `run_experiment.py` command
recorded in the manifest, selecting a fresh output directory. The direct
computation command is:

    python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/source_evolution/numerics_audit/audit.py

## Remaining gate

The coordinate audit removes a numerical concern about this linear response.
It does not select the physical homogeneous mode: arbitrary source-free
initial perturbations can still be added to the forced solution. The next
meaningful linear check is to quantify that initial-data dependence in the
two physical potentials over a named admissible initial-data family, using
the same fixed action. Merely extending the wavenumber scan would not resolve
that question.

A galaxy claim additionally requires a positive-density localized source,
its conserved evolution, and appropriate spatial boundary data in the fixed
nonlinear action. A linear response is proportional to source amplitude, so
these finite linear trajectories cannot establish a nonlinear MOND mass law.
No constitutive coefficient reconstruction is justified by this audit.

Mathematical self-review covered this report and the displayed coordinate
formulas. No mathematical-token correction or unresolved notation issue was
found. The exact algebra checks and the two solver families supply the
substantive validation described above.
