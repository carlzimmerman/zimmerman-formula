# Restricted feasibility follow-up, after the broad spectrum test

The original spectrum criterion failed: no length up to 300 kpc stabilized
the *artificially rotation-dominated cluster-size profile* as well as all the
galactic-size profiles. That stronger mass-independent selection claim is
not made. The 30 kpc, beta=20 point stabilized the three smaller profiles
when strongly rotating, while all four low-streaming profiles were unstable.

Test that one common parameter pair nonlinearly, without changing equations
between objects. Every profile is crossed with f=.3,.95,.99 and an initially
free f=.99 control. The rotating cluster counterexample is retained as an
endpoint-stability failure, not hidden or changed into a success. This is a
post-hoc candidate to address the requested dwarf/disk/cluster pattern; the
parameters are not independently derived or observationally calibrated.

Use a uniform radial grid for this stiff calculation, N=64 then N=128/256.
It avoids assigning almost empty inner cells extraordinarily short relaxation
times on the four-decade logarithmic grid. Compare grid refinement explicitly.
The underlying mass profile and physical length are unchanged. Retain all
old failed runs. Negative-eigenvalue high-streaming cases already fail the
protection test and need not undergo a further unstable trajectory.

The earlier explicit and implicit local-only scans encountered phase-coordinate
excursions after an initially protected cell became unstable at a later time.
The polynomial h is inadmissible outside [0,1]; those trajectories are rejected,
not interpreted as physical conversion. The constrained domain is still checked
strictly in every new trajectory. Any numerical failure remains a failure to
establish that case. No clamping or artificial noise is used to force a result.

The first uniform-grid nonlinear run with purely local drag was interrupted
before its first completed case because the very stiff small-system phase
relaxation was not progressing efficiently. It produced no valid manifest or
accepted trajectory. The follow-up specifies *gradient damping* as well as
gradient energy: the positive Rayleigh dissipation is
R=(dot x^T D dot x + dot x^T L dot x)/2, where D is the recorded positive
local drag and L is the phase-gradient matrix. Hence (D+L)dot x=-grad E and
receiver heating is dot x^T(D+L)dot x>=0. This is an added, explicitly assumed
dissipative completion; it changes relaxation paths/times, not equilibria or
their stability signs. It is not disguised as a mere solver optimization.
Absolute transport/damping coefficients remain undetermined. Its physical
continuum form includes a positive |grad dot x|^2 dissipation term.
