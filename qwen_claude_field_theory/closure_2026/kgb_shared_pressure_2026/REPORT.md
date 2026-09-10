# Action-derived pressure repair and a regular clock chart

2026-09-10. Base: `17f869d48ec64d54e8a5321a85775dc720aa2500`.
Full gravity target: **OPEN**. No dark-matter particles are added. The clock is
an explicit physical field carrying stress-energy, not a concealed auxiliary.

## What changed

The preceding zero-pressure inverse failed the exponential transition.
This package derives a pressure-enabled inverse, finds and independently
checks a healthy local completion, and integrates the kinetic functions instead
of assigning their derivatives independently at each radius. A singular
P_X-based reconstruction chart was replaced by one regular through P_X=0.

The complete universal theory is NOT obtained: the tested continuations either
leave the timelike chart or lose the available causal window; some develop
large pressure or negative density. Last solver evaluations are not accepted
endpoints or proofs of nonexistence. The surviving result is constructive local
action freedom plus an exact criterion that guides the missing global solve.

The action remains

\[
 S=\int\sqrt{-g}\,[mR/2+P(X)-G(X)\Box\phi]+S_m[g,\psi],
 \quad X=-\tfrac12(\nabla\phi)^2,
 \quad m=(8\pi G_b)^{-1}>0.
\]

G_b is bare; measured Newton G has not been derived. No Lambda extension,
first-principles kappa, new empirical fit or global novelty claim is made.
Credit: Carl Zimmerman supplied the clock direction and exponential-law target.
KGB is established prior work; see the version-pinned
[source record](../ticking_kgb_inverse_2026/SOURCES.md). The covariant action,
stress and scalar principal expression are imported from the preceding
locally varied calculation, not from a different gravity model.

## 1. Pressure inverse from the same equations

Let ds²=-A dt²+B dr²+r²dOmega², phi=q t+psi(r), p=psi',
g=A'/(2A), U=q²/A-2X=p²/B, T=1+2rg, Z=U/X-rg.
Primes in this report denote r derivatives unless a subscript X is given.
The zero-flux ticking branch has J^r=0 and p_r=P(X). Einstein's radial equation
therefore fixes

\[
 B={T\over1+r^2P/m},\qquad
 \rho+P=E_0-{rP_X\over T}X',
\]

where E_0 is the same expression evaluated holding P fixed when differentiating
B. Explicitly, with B_r|P the partial radial derivative,

\[
 E_0=m[(1-1/B)/r^2+(B_r|_P)/(B^2r)]+P.
\]

The current and density equations then give

\[
 X'={ZE_0\over rP_X(1+Z/T)},\qquad
 G_X={P_X\,p\,r\over2XZ}.
\]

Both residuals are checked, as are the radial Einstein equation and the
Schwarzschild zero-density control. Exclude the displayed zero denominators;
the P_X=Z=0 case is handled below, not silently dropped.

For the target profile use mu=1-exp(-y), r=epsilon/sqrt(y mu),
epsilon=sqrt(G_b M a0)/c² and dimensionless a0=m=|q|=1. The prescribed temporal
metric has g=y/(1-2ry). Thus its weak-field acceleration follows the exact
exponential spherical law. B is now determined by pressure, not fixed to its
old zero-pressure value. Lensing must consequently be checked again; retaining
the temporal force law does not assign Psi or gamma_PPN.

The first scan uses one shared P(X)=k(X-1/2), k={10^4,10^6,10^8}, two mass
parameters epsilon={10^-6,2*10^-6}, and three initial radial-gradient ratios
{0.25,0.75,1.25}. The 18 outward integrations start at y=20 and aim at y=0.02.
None reaches the entire interval in that scan. Additional exploratory k=1,100
integrations can reach it, but do not remain healthy throughout; these are not
universal-G tests. No best-fit parameter or observational claim is inferred.

## 2. The exact local freedom, and its invariant

Let C be the coupled scalar principal matrix after eliminating Ricci using
Einstein's equations, with canonical positive time coefficient C00. It is
computed by differentiating the scalar Euler–Lagrange equation, not assigned.
At fixed background, P and P_X, varying P_XX consistently in the inverse varies
G_XX by (G_X/P_X) delta P_XX. Actual symbolic differentiation gives

\[
 {dC\over dP_{XX}}={E\over P_X}
    \operatorname{diag}(1,0,\beta,\beta),\qquad
 E=\rho+P,\quad\beta={p^2\over2BX}>0.
\]

The cross/time-radial and radial entries do not change. In particular,

\[
 \boxed{\mathcal I=C_{00}-{C_{22}\over\beta}
 \quad\hbox{is independent of the free kinetic curvature}.}
\]

Positive time kinetic sign and negative angular coefficient require I>0.
For I<=0, no choice of this free second derivative repairs both signs at the
specified background. For I>0 and E!=0 there is a constructive family:

\[
 C_{00}=K,\quad C_{22}=C_{33}=\beta(K-\mathcal I),\quad 0<K<\mathcal I,
\]

while C01 and C11 stay fixed. This is an accessibility statement for a local
action jet, not a claim that arbitrary K(r) defines integrable functions.

The radial discriminant additionally requires C01²-K C11>0. Strictly inside
the physical light cone requires K>|C01| and

\[
 K>\max_{0\le t\le1}
 {\beta\mathcal I-(C_{11}+\beta\mathcal I)t^2+2|C_{01}|t
       \over1+\beta-\beta t^2}.
\]

The maximum is calculated from endpoints and the actual quadratic equation
for its stationary points, not a hard-coded speed or rank. Together these
inequalities give an interval for K; an empty interval rejects that local jet.
The solver chooses an interior K, translates it back into action derivatives,
and reevaluates the original principal expression independently.

Among 60 local jet probes, 34 have a nonempty numerical interval. These are
NOT 34 complete theories. A concrete repair at epsilon=10^-6, y=20, u=0,
z=0.5, P=0, P_X=1 has a 60-digit independently recomputed principal matrix with
C00 about 1.50333*10^7, C22 about -15.0286 and positive radial discriminant about
9.30483*10^6. Direct Einstein/stress residual is below 10^-53. Here
u=log(A)/epsilon and z=(1/2-AX)/epsilon. This establishes a healthy local jet
where the earlier restricted construction failed, not a full profile.

The high-precision control also reproduced an unhealthy scan point. Ordinary
floating evaluation of the very small Newtonian-end residual density loses
digits by subtraction; it must not be interpreted as a field-equation defect.

## 3. Integrability and the regular chart

`steered_profile.py` evolves P and P_X together with the metric/clock profile:
dP/dr=P_X X', dP_X/dr=P_XX X'. Its first continuations encounter P_X->0 and
Z->0 together, with finite reconstructed G_X. The solver floor there was NOT
evidence of a physical singularity.

Set L=G_X/p. The same equations become

\[
 P_X={2XLZ\over r},\quad
 X'={E_0\over2XL(1+Z/T)},\quad G_X=pL.
\]

These equations never divide by P_X or Z. With R=L_X as the new free curvature,

\[
 G_{XX}={p'L\over X'}+pR,\quad
 P_{XX}={2LZ\over r}+{2XL\over r}
       \left({Z'\over X'}-{Z\over rX'}\right)+{2XZ\over r}R.
\]

Recomputing the principal derivative in this chart gives
dC/dR=(E/L) diag(1,0,beta,beta), including at Z=0. The symbolic residuals vanish
without a division by P_X. L!=0, X!=0, p!=0, X'!=0 and regular metric are still
required; this does not certify every degeneracy.

`regular_clock.py` evolves P'=P_X X' and L'=R X' and does cross P_X=0 in the
tested trajectories. The seven runs use window fractions 0.01,0.1,0.5,0.9,0.99,
two masses and both signs of the initial L. None completes y=20 to 0.02 with
the present selection rule. The midpoint negative-L examples approach X=0
and can develop unacceptable pressure/density; the positive-L example loses
the causal window. Fractions near the lower bound extend farther but still
leave the chart. These are limitations of the tested continuation policies,
not a no-go for every pressure function or boundary condition.

## 4. What Lean certifies

`PressureWindowFormal.lean` checks five explicit conditional statements:
invariance under the allowed coefficient shift; necessary positive invariant;
nonrepairability when it is nonpositive; a constructive hyperbolic choice when
the radial coefficient is negative; and the algebraic zero-current crossing.
It does NOT yet formalize the variation-to-principal-symbol bridge, the ODE
solution, the full causal-interval optimization, or the entire gravity theory.
Only standard Lean axioms are printed; there is no `sorryAx`.

## Next unavoidable calculation

Use the regular chart in a constrained, joint inverse for P(X),G(X) across
different masses. A healthy local choice cannot independently be selected
at each radius/mass: both functions and their derivatives must agree on every
shared X interval. Simultaneously enforce positive desired density, the
pressure/slip bounds and the causal interval, not just a positive kinetic sign.
Do not infer complete viability from another successful local patch.

Full Dirac closure, separately counted healthy clock, tensor/vector sector,
all PPN parameters, measured G, cosmological matching, zero-field regularity
and empirical validation remain missing. No dark-matter particles or
photons/gravitons with different physical metrics have been introduced.

## Reproduction

From this directory run `python3 -B run_suite.py`. The bounded run under
`run_001/` records exact nested argv, working directories, exits, versions,
raw logs and input/output hashes. `audit_contract.json` records ranges and
non-claims. The suite runs all new scripts, nine new tests, five Lean theorems,
and the previous 49 regression tests. Execution success is not physics closure.
