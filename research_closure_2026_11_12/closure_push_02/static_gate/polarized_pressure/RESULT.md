# Polarization-subtracted pressure and a coefficient ceiling

Two different statements are established here. The explicit minimum-moment finite-band repair fails the **quiet constitutive annulus** even at mu_K=198.25/Mpc, once its pressure is included in the polarization-subtracted Einstein equation. A separate, weaker but more general pressure bound limits mu_K to about 435–446/Mpc on the same clock/force target, without assuming that P retains its AQUAL reference relation. Neither is an unrestricted theorem about all possible theories or all correlated Q–Pi state domains.

## 1. Pressure enters the full static equation before taking a weak-field limit

Write H for the repaired clock term including its Q-Gamma compensator, but not QX17's original one-sided stiffness. Let `p_H=H-Pi H_Pi`, `rho_H=QH_Q-H`, and let `P W_P` use the magnitude P. Fixed-J variation, with `J^i=sqrt(h)P^i`, and the static polarization equation give

\[
\rho=\Pi+\rho_H+W+\gamma\Pi_+^2/2,
\]
\[
3\bar p=3p_H+2P W_P-3W+3\gamma\Pi_+^2/2.
\]

Thus the exact static lapse identity is

\[
\frac{D^2N}{N}
=K[\Pi+\rho_H+3p_H+2(PW_P-W)+2\gamma\Pi_+^2]-\Lambda. \tag{1}
\]

The anisotropic W stress has been included through its trace; no pressureless scalar Poisson equation has been substituted. This follows from `R_nn=K(rho+3 mean(p))-Lambda` for a static zero-shift geometry.

Subtracting the polarization divergence using `Pi=D_iP^i` gives the exact identity

\[
\boxed{D_i(D^iN-KNP^i)=N\{K[\rho_H+3p_H
+2(PW_P-W)+2\gamma\Pi_+^2-P\cdot A]-\Lambda\}.} \tag{2}
\]

In a nearly flat spherical region, its boundary flux divided by 4pi is `r²(N'-KNP)`. The term `-P.A` is required by differentiating NP and is retained in the computation. Since `PW_P-W>=0`, `K|P|<a=a0/c²`, and rho_H>=0 on the stated positive-Q branch, a conservative local lower bound is `3K p_H-a|A|-Lambda`. The full executed calculation uses every term in (2), rather than that coarse bound.

Spatial curvature is not assumed absent from the exact identity. Only its evaluation on the specified weak-field target uses nearly flat spatial geometry. The normal-energy constraint independently reconstructs a spatial potential of order 2.3e-6 in that target, as reported below. Ordinary weak spatial metric corrections cannot absorb an order-ten baryon-mass residual while retaining the same regular target geometry and boundary force.

## 2. The minimum-moment finite-band compensator keeps the quiet force relation

Use the perspective B and the finite rectangular Q band from the independent repair audit. Define

\[
M=\sup_{1\le Q\le Q_{\max}}B(Q)/Q,\quad u_0=(2/3)^{1/3},
\]
\[
\Gamma_{uu}=M\max(S''(u),0),\quad
\Gamma(0)=\Gamma_u(0)=0.
\]

For u>=u0,

\[
\Gamma=M[S(u)-S(u_0)-S'(u_0)(u-u_0)],
\quad \lambda=-MS'(u_0)/\Pi_c,
\quad J=3Me^{-2/3}.
\]

The full leaf equation can be written exactly as

\[
D[N(1+\gamma\Pi_+-H_\Pi)]=N W_P.
\]

With the static clock normalization NQ=1, the constant lambda drops out as the exact Q-Pi boundary term. The remaining scalar whose gradient perturbs the force is

\[
T=N\gamma\Pi_+
+N(QM-B)S'/\Pi_c,
\qquad DN+DT=N W_P. \tag{3}
\]

The second term, not the large removable constant slope, is what must be bounded. It is not assumed zero merely because a gate is called suppressed.

The target is the accepted canonical annular solve `Mb=1e11 Msun`, `Lstar=22 pc`, `x=r/rM in[1,60]`, `rM=.01220427284 Mpc`, outer reference u=4. The baseline coupled solve is rerun at tolerance 5e-7. For this new substitution take `N=exp(phi)`, `Q=exp(-phi)` consistently; the earlier scalar cap below uses its separately stated linear weak-potential target. The difference is of weak-field order and is not silently pooled.

Set mu_K=198.25 and choose L² just above the exact energy-suppression lower bound. The actual minimum u is 4.000916. The executed checks give:

- maximum residual gate potential: `3.77e-27`;
- maximum gate-gradient force shift: `3.16e-18` of A;
- maximum complete repaired constitutive residual: `2.40e-11` of A;
- original-stiffness force correction: at most `1.62e-6` of A;
- energy suppression fraction: at most `2.54433098927e-5`, below delta=`2.54433099202e-5`.

Thus the supplied fields nearly satisfy the repaired constitutive equation, with all finite gate and stiffness terms evaluated. This is a controlled quiet-branch substitution; it is **not** a newly solved deformed repaired-action halo.

## 3. The low-mu quiet annulus fails the polarization-subtracted Einstein equation

Normalize the flux in (2) by `a rM²=GM_b/c²`. Its target change across the annulus is `1.82289e-6` baryon masses. The source terms instead require:

| source contribution | baryon-mass units |
|---|---:|
| pressure term 3 p_H | 12.2136511 |
| residual clock normal energy rho_H | 1.0005157 |
| W, original stiffness and -P.A combined | 0.000000531 |
| total for Lambda=0 | 13.2141674 |

The reconstructed spatial potential from the normal-energy constraint has maximum magnitude `2.23415e-6`. Pressure and W anisotropy were retained through the exact stress trace in (1), not omitted on the ground that the metric is weak.

The Lambda dependence is explicit:

| Lambda / Mpc^-2 | required flux change / M_b | target flux change / M_b |
|---:|---:|---:|
| 0 | 13.2141674 | 0.000001823 |
| 1e-7 | 10.4799055 | 0.000001823 |
| 1.1e-7 | 10.2064793 | 0.000001823 |

A constant Lambda of `4.83281e-7/Mpc²` would cancel this **integrated** residual in this substitution. That is a numerical cancellation threshold, not a new cosmological solution: the local equations, fixed cosmological background, normal energy and endpoint conditions would still need to be satisfied. The listed Lambda values are explicit benchmarks, not an empirical determination.

This resolves why the raw lapse-flux ratio of about .207 at low mu did not by itself diagnose this quiet branch. Most of the reference lapse source is already supplied by polarization. Subtracting it reveals the large extra active source. The result closes the tested quiet constitutive construction, with its actual off-gate u and tiny force correction.

**Scope limit:** changing Pi so that u is nearer the gate transition can change T in (3), rearrange P and invalidate the assumption that the polarization flux remains the reference one. This calculation does not exclude all such deformed low-mu configurations. That wider question must use the next bound or a new field solution; it cannot inherit the quiet-branch label.

## 4. A necessary coefficient ceiling that permits P to deform

The raw lapse bound from the independent perspective audit uses only positive normal energy, the on-shell mean-pressure lower bound, and the same Q/force target. It does not use the AQUAL P relation or the reference Pi density. Concavity is required only on the finite rectangular Q band `[1,Qmax]`, with `Qmax=1+2.21794508245e-6`, and Gamma has its FRW endpoint conditions.

For the supplied pointwise energy ceiling `delta=1/mu_K²` in the specified Mpc units, define

\[
T_\delta=-\log(1-\delta),\quad
I_\delta=3e^{-2/3}-(1-3\log\delta)\delta.
\]

Energy suppression implies S<=delta and hence the finite pressure moment bound. The necessary mean-pressure floor is

\[
\boxed{K\bar p\ge
\frac{x_{\max}^2}{2Q_{\max}T_\delta}I_\delta
\equiv P_{\min}(\mu_K).} \tag{4}
\]

For mu_K>exp(1/3), this expression is strictly increasing: as mu grows, delta decreases, T_delta decreases, and I_delta increases. Both factors in (4) are positive. It tends to infinity with mu². Therefore a unique scalar root of the required/allowed lapse flux ratio equal to one supplies a necessary upper bound, rather than merely a sampled crossing.

Using the target lapse flux `2.81853380e-7 Mpc`, `N_min=1/Qmax`, and nearly flat spatial volume, the inequality is

\[
[P_{\min}(\mu_K)-\Lambda/3]N_{\min}(R^3-r_1^3)
\lesssim R^2N'(R)-r_1^2N'(r_1). \tag{5}
\]

At the roots the bracket is positive, so the N_min bound has the stated sign. A nonzero Lambda is carried explicitly, and no unknown negative-active stress is assumed to cancel the floor.

The executed scalar roots give:

| Lambda / Mpc^-2 | necessary mu_K upper bound / Mpc^-1 |
|---:|---:|
| 0 | 435.3270994 |
| 1e-7 | 445.3183487 |
| 1.1e-7 | 446.3051717 |

These ceilings allow polarization to deform, provided the repaired action remains in its stated rectangular concavity domain, the clock energy meets the supplied ceiling, the specified weak Q/force target is retained, and normal energy is nonnegative. They are target- and action-class bounds, not universal observational upper limits.

An independently established lower bound from the unchanged FRW history can now be compared directly with these ceilings. This lane does not infer such a cosmological bound from a withdrawn historical CMB proxy; that derivation belongs to the separate background audit.

## Evidence and remaining boundary

`run01/manifest.json` records the executed BVP benchmark, source integrals, constitutive residuals and three scalar roots. Inputs, package versions, limits and hashes are pinned. The new action is evaluated on a controlled target, not mislabeled a new nonlinear solution. The complete exact static stress is used before the weak spatial metric approximation. Λ and possible additional negative-active stresses remain explicit hypotheses.

The next permitted conclusion is a class-specific lack of overlap if a verified unchanged-background lower coefficient bound exceeds the ceilings in section 4. A different action, another early-time history, or a rigorously derived correlated state-domain restriction remains outside this result.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
