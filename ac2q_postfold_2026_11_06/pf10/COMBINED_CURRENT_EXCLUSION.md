# Full scalar-current exclusion of the matched combined concentration

Candidate derivation for independent audit. The target is the PF09 simultaneous
large-r/boost stress mechanism in a matched, finite-current timelike layer.
No bound on r above or on clock rapidity is imposed.

## Precise layer class

Smooth native full-switch solutions in a regular conformal planar chart converge
outside a shrinking strip around a compact strictly timelike interface to
identified piecewise-regular native outer fields. Metrics converge uniformly
to a continuous nondegenerate metric, with the bounds needed for the limiting
conservation law and regular contractions. Assume r>=r0>0, uniform hold-law cap
separation, bounded potential/derivatives on the relevant clock range, uniform
phi convergence to a continuous clock with common positive regular tangential
trace, and strong uniform same-clock endpoint Pi=exp(2beta)P matching.

Outer A traces are finite, positive, regular and compatible with the polarization
equation. Coordinate total-variation bounds hold for the total Hilbert stress
and for the specific native scalar shift current defined below. Native bulk
stress/current identification and their normal traces are retained. The limiting
stress conservation law has no normal dipole. These are substantive assumptions,
not consequences of signed action finiteness.

## 1. Differential spatial estimates independent of both escapes

Let A=Q/r, Q>=1, mu>=0, mu(Q-1)=0. Exact native equations give
 eA=Wp/r, ePi=exp(2beta)D,
 D=(Ar-1)/gamma-r²-mu.
Clock slices in the regular chart are graphs with |dt/dx|<1; a compact timelike
interface gives crossing proper length O(epsilon), uniformly even as boosts
increase. Bounded Wp and r>=r0 give A variation O(epsilon). Anchored regular
positive outer A therefore yields fixed 0<amin<=A<=amax and common uniform
layer convergence of A. This is not an independent upper-r assumption.

Complete the square to get D_+<=amax²/(4gamma²), up to a harmless tighter
constant. This bound does not require r bounded. Hence positive variation of
Pi on a crossing is O(epsilon). Strong signed endpoint matching makes negative
variation o(1), and Pi lies uniformly between its matching endpoint values up
to o(1). Thus Pi has a common continuous layer limit and
 integral D_- d ell=o(1), integral mu d ell=o(1).
The latter uses mu=-D-r²<=D_- on multiplier support.

Uniform phi convergence gives a bounded clock-label range. The exact coarea
identity dVol_base=r^-1 dphi d ell and r>=r0 transfer these uniform slice
estimates to integral_layer mu dVol=o(1). Bounded beta supplies the transverse
volume factor. No upper boost or invariant-clock bound was used.

## 2. Exact native scalar current, with a fixed representative

Use the auxiliary action BEFORE its topological integration by parts:
 L=E[H-mu(Ar-1)]-A(phi_t Pi_x-phi_x Pi_t),
 E=exp(2alpha+2beta),
 H=r²/2-V-W+(Ar-1-gamma r²)²/(2gamma).
For smooth on-shell native fields, the field-redefinition Euler terms vanish.
The shift-current density representative is
 J^t=E(h-mu A)n^t-A Pi_x,
 J^x=E(h-mu A)n^x+A Pi_t, h=H_r.
It satisfies partial_a J^a=-E(V_phi+W_phi). The source is uniformly bounded
under the potential/cap assumptions. For constant potential it is conserved.

Do not silently replace this current by the after-integration-by-parts current:
the latter differs by curl(A Pi). They have the same divergence on smooth
fields, but finite-measure assumptions must specify the representative.

On shell its clock contraction is exactly
 (J^a partial_a phi)/E=rh-mu Q-QD
     =r²(1-2gamma D_eff)=r²(3-2Ar+2gamma r²),
 D_eff=(Ar-1)/gamma-r²=max(D,-r²).
It contains no mu term. With A bounded it is >=gamma r^4-C uniformly.

## 3. Stress controls the kinetic part of the current

Write J=Jbase-A curl(Pi), Jbase=E(h-mu A)n. In a regular orthonormal frame,
C=n^0>=1, k=rh-mu Q, and
 T00=-H+k C²,
 Jbase^0/E=(k/r)C=(T00+H)/(r C).
The spatial component is no larger in absolute value, up to bounded chart
factors. H has uniformly bounded total mass because Tperp=H+P Wp and cap
separation bounds P Wp. Thus finite total-stress measures control H as well.

Split the shrinking strip into rC>L and rC<=L. On the first part,
 integral|Jbase|<=C/L integral(|T00|+|H|), uniformly. On the second part,
r and C are bounded (using r>=r0), so h is bounded and
 |Jbase|<=C_L(1+mu). The strip volume and multiplier mass tend to zero.
Taking epsilon->0 and then L->infinity proves that Jbase has no surface mass,
in fact its absolute layer mass vanishes. This estimate allows cancellations
inside total stress; it does not assume separate bounds on k n n pieces.

## 4. The finite native current controls derivatives of Pi

Since J and Jbase are finite measures and amin>0, the current formula gives
uniform total-variation bounds on both coordinate derivatives of Pi. Their
weak limits are derivatives of the common continuous Pi limit. With the
identified piecewise-regular outer traces, these derivatives have no surface
measure. Uniform convergence of A to its regular common trace permits
multiplication by A in this measure limit. Therefore J itself has no surface
measure. This step uses the full current equation/representative, not just
constitutive stress algebra; it works also at a zero outer P trace.

## 5. Product identity excludes the large-r concentration

Each smooth native solution obeys
 partial_a(phi J^a)=J^a partial_a phi+phi partial_a J^a.
Uniform phi convergence, finite current measures and bounded identified source
pass the left and last terms to the limit. The limiting current has only the
identified piecewise-regular bulk part. Its scalar equation requires equal
normal traces, [J.N]=0. Continuity of phi then makes the surface coefficient
of partial_a(phi J^a) equal to phi_trace[J.N]=0. This trace argument is needed:
absence of a surface current by itself would not exclude a bulk-flux jump.

Consequently the exact clock contraction has no surface measure. The bound
r²(3-2Ar+2gamma r²)>=gamma r^4-C implies absence of r^4 concentration there.
This contradicts the positive high-r constituent of the PF09 combined tensor.

## 6. No residual surface stress and scope

The base trace is tr_base T=2H-rh+mu. With bounded A,P/cap and no r^4 or mu
surface mass, this trace has no surface measure. Tperp=H+P Wp has none either.
Finite total-stress measures and uniform metric convergence justify taking
trace after the weak limit. Normal no-dipole conservation gives N^a S_ab=0;
for a symmetric longitudinal tensor on a timelike interface this leaves only
S_ab=s T_a T_b. Its trace is -s, hence s=0. Planar symmetry and zero transverse
surface stress give S=0 in every component.

Thus the matched PF09 combined stress mixture cannot satisfy the full native
scalar/polarization equations in this finite-current, finite-stress, regular-
trace class. This closes that simultaneous escape, not every singular class.
It does not rule out loss of current-measure control, polarization trace jumps,
clock degeneration r->0, cap/source concentration, singular metric products,
nonidentified oscillatory bulk limits, or null interfaces. No continuation or
same-data uniqueness theorem follows from this exclusion alone.
