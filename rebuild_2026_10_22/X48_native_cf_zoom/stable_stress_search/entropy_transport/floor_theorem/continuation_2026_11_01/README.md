# Uniform startup: nonlinear closure still open

**The requested bound has not been proved.** This continuation derives new
all-mesh estimates for the unchanged law, but supplies no common T for the
actual cold collapse. The all-time central entropy-floor theorem remains
conditional on uniform seeding. The exact quantified target is
[TARGET.md](TARGET.md).

Three routes were executed rather than repeating the earlier finite grids:

| Route | New result | Remaining limitation |
| --- | --- | --- |
| [Actual moving graph](all_mesh_certificate.md) | Exact actual-graph Duhamel formula removes the moving-conductance commutator; uniform capacity/form bounds, weighted scalar energy, and a ceiling-correct boundary barrier | Barrier assumes a compression-amplitude envelope; nonlinear constitutive/heat bound (AC) and that envelope are unproved |
| [Effective viscous flux](effective_flux.md) | Exact primitive F=(W^2-9/4)/4 and nonlinear Green/Volterra equation absorb density-dependent old viscosity; integrated memory and thermal corrections are O(s^6) under the stated envelope | Bounds on a smoothed stress potential do not recover instantaneous cell compression uniformly in N |
| [Entropy and coupled energy](entropy_energy.md) | Full heat edge variation, positive reduced density stiffness, actual-geometry conductance comparison, dissipative leading density-gradient energy, uniform Nash inequality and leading-model pointwise smoothing | Nonlinear coefficient/time-weight/cutoff terms and the actual boundary forcing remain unbounded by the new energy |

These are analytical results, with [independent review](INDEPENDENT_AUDIT.md).
Their stated hypotheses matter. No physical parameter, source, entropy floor,
accepted state, or earlier result file was changed.

## Exact remaining estimate

Let x=-theta be signed compression, x_d the homogeneous reference, S the
actual full stress, and nu_d,S_d its reference coefficients. Put

\[
 w=x_d-x,\qquad \delta S=S-(S_d-\nu_dw).
\]

Using the propagator P_r of nu_d L_r on the actual moving graph gives the
exact formula

\[
 w(s)=b(s)+\int_0^sP_r(s,v)(R_d-R)\,dv
            -\int_0^sP_r(s,v)L_r(v)\delta S(v)\,dv.
\]

The geometric/gravity reaction satisfies R>=0. The scalar boundary term b
has a uniform central-quarter bound under the explicit amplitude envelope.
What is still missing is a pointwise estimate of the last integral for the
full constitutive evolution, together with a proof of the envelope. Deleting
delta S, freezing its density dependence, or bounding its amplitude without
controlling its effect through L_r would omit this step.

The new density-memory model is stable and has a proved smoothing estimate

\[
 \|w(s)\|_\infty\le C s^{-9/4}\|w(0)\|_{L^2(V)},
\]

uniformly in N for compatible regular initial data on a fixed homogeneous
graph. Its proof uses a radial resistance estimate, a uniform Nash inequality,
and an elementary beta-integral representation. The actual activation
coefficient satisfies the required exact inequality C_a>16/3. This theorem
does not cover arbitrary forcing, the nonlinear moving coefficients, or the
surface layer of the actual collapse. Replacing those terms by the regular
initial-data multiplier would be unjustified.

## Why an energy bound alone cannot finish

On the homogeneous graph, a unit first-cell spike satisfies

\[
 \|f\|_{L^2(V)}^2=O(N^{-1}),\qquad
 \mathscr D(f)=O(N^{-1/3}),\qquad \|f\|_\infty=1.
\]

Thus even one controlled graph derivative does not provide a uniform
pointwise central bound. The radial geometry has three-dimensional scaling.
The leading-model smoothing theorem addresses this issue in that model;
the actual nonlinear forcing estimate remains a separate proof obligation.
The example is an inference obstruction, not a trajectory counterexample.

The surviving task is a localized nonlinear energy/regularity estimate that
controls the explicit heat commutator, state-dependent time weights and
cutoff work, then closes the actual compression envelope. These continuations
remain open; no impossibility or specified-data counterexample is claimed.
See [STATUS.md](STATUS.md) for the precise handoff and
[PROVENANCE.md](PROVENANCE.md) for review and source checks.
