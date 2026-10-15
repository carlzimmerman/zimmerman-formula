# Exact finite-stock binding energy and the formation energy budget

AR4-ENERGY-001. This closes a quantitative energy question in the previously
proved Newtonian, fixed-point-baryon, critical-charge, zero-stiffness reduction.
It does not supply a physical cooling interaction, actual finite-stiffness
galaxy profile, or a cosmological catchment. Both that scope and the point
baryon's singular origin are retained.

Let `s=Mc/Mb>0`, `rM=sqrt(G Mb/a0)`, `r=rM*y`, and measure energies in
`E0=Mb*a0*rM`. The spherical potential with the fixed baryon self-energy
excluded is exactly

\[
 V[m]=\int_0^\infty\left\{y^2F(m(y)/y^2)-m(y)/y^2\right\}dy,
 \quad F(x)=-x-\log(1-x)-x^2/2,\quad0\le x<1.
\]

Here m is enclosed cold mass in units Mb; the term linear in m is the
baryon interaction. Critical self-gravity has already been canceled against
the Maxwell part of the electric Hamiltonian, exactly once. The remaining
F term is positive. The pinned dynamical-lift proof establishes the unique
fixed-stock global constrained energetic minimum

\[
 m_*(y)=\min\{(\sqrt{1+4y^2}-1)/2,s\},\quad
 Y=R/rM=\sqrt{s(s+1)}.
\]

It controls nonradial admissible changes in that same mechanical functional;
the calculations below only evaluate its spherical representative.

## Closed binding-energy formula

The profile is independent of s inside its edge. Since its enclosed mass is
continuous at Y, differentiating its finite energy with respect to s leaves
only the exterior integral. On any compact positive s interval the derivative
is dominated and integrable, including the moving edge. Thus

\[
 V_*'(s)=\int_Y^\infty\left\{
 {s^2\over y^2(y^2-s)}-{1\over y^2}\right\}dy
 =-\sqrt{(s+1)/s}+\sqrt{s}\,\operatorname{arsinh}(s^{-1/2}).
\]

For example, decompose the first rational integrand as
`-s/y²+s/(y²-s)`, integrate to infinity and use
`atanh(1/sqrt(s+1))=asinh(1/sqrt(s))`. The s-to-zero limit of the
minimum energy is zero: its inner scaled contribution and its baryon energy
both vanish as its support shrinks, and its exterior tail does likewise.
Integration consequently gives the exact universal formula

\[
 \boxed{V_*(s)={2\over3}\left[
 s^{3/2}\operatorname{arsinh}(s^{-1/2})
 -\sqrt{s(s+1)}-2\operatorname{arsinh}\sqrt{s}\right].}
\]

Differentiation and the zero-stock limit independently fix the integration
constant. This is a mathematical identity for every s>0 in the specified
reduction, not a finite-grid extrapolation or predicted abundance.

## Actual finite uniform starts and an explicit remainder bound

An initially resting uniform sphere of radius L*rM and total cold stock s*Mb
has m(y)=s(y/L)^3 inside L and m=s outside. It is admissible when
`a=s/L²<1`. Its baryon interaction is exactly `-3s/(2L)`. Expanding the
positive F series and integrating term by term gives

\[
 V_{\rm unif}(s,L)=-{3s\over2L}
 +L^3\sum_{n=3}^\infty a^n\left[
 {1\over n(n+3)}+{1\over n(2n-3)}\right].
\]

Every term is positive, so monotone integration justifies this equality.
After terms through n=N>=3 the omitted positive electric energy is at most

\[
 {2L^3a^{N+1}\over(N+1)^2(1-a)},
\]

because both bracket terms are bounded by 1/n². This gives an explicit
truncation certificate rather than relying only on numerical quadrature.

Strict constrained minimality implies
`Delta=V_unif-V_*>0` for every admissible uniform start distinct from the
minimum. Uniform and minimum enclosed profiles cannot coincide for s>0:
their central powers are y³ and y². The statement is therefore strict for
all such s,L, independently of the bounded examples.

## What formation must do with this energy

The known current Hamiltonian is `K+E0*V`, K>=0. Separate conservation of
rest mass also conserves charge `sqrt(4piG)*Mc`. If a regular closed solution
starts at rest in this uniform state, reaching the exact resting minimum
requires **E0*Delta** to reside in additional heat, velocity dispersion,
remnants or outgoing channels. If all final material and fields are claimed
to be exactly the resting minimum, that amount must leave the modeled cold
system. Closed strong convergence in the same conserved-energy topology is
impossible at positive Delta. Weak phase mixing or coarse observables are
different claims and are not excluded by this argument.

The associated fraction of cold rest energy is

\[
 {E_{\rm excess}\over Mc\,c^2}
 ={a0\,rM\over c^2}{\Delta\over s}.
\]

Bounded examples take s=5.364*N with assigned N=3,6,10 and L/Y=1.5,2,4.
They probe supply and start-size dependence; they are not dynamically derived
initial conditions or new data fits. The physical scale uses the declared
canonical a0 and one assigned Mb=10^10.5 solar masses. An energy capacity
does not derive a rate, reciprocal coupling, no-recapture rule or basin of
attraction. No radiation equation has been added to the instantaneous model.

## Source units and existing ownership

CFG416's actual declared retention thresholds are in **Msun/h**, and its
function is called on a mass in those units. With physical Mta the faithful
translation is `f(log10(h*Mta))`, not `f(log10(Mta))`. This is a resolution of
the local mathematical dictionary; the empirical calibration and component
meaning of that census remain external inputs. The legacy physical-Msun
interpretation is retained as a secondary comparison in this round's lensing
calculation, without selecting the branch by its fit.

The existing T1x M1 already assigns numerical host ownership by smallest
distance/r_ON, with tie rules and per-host zero-sum source construction.
Its pinned criteria are a concrete numerical ownership prescription. The
remaining implication is its physical source/current/transport interpretation
and an ownership-consistent lens–matter correlation, rather than the absence
of any partition algorithm. The energy result here does not derive that
interpretation or duplicate the newly registered CFG806 SN/cooling census
route, which concerns a different baryon feedback budget.
