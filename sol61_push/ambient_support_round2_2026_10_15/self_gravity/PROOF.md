# A weakly self-gravitating exterior exists by a direct contraction

NS-SELF-GRAVITY-001, 15 October 2026. Direct analytic construction and exact
arithmetic checks; self-review with a separate algebra crosscheck. Primary
verdict: **conditional on the specified neutral EOS, density normalization,
fixed spherical central source and exterior inner support**.

This supplies the actual Newtonian Euler--Poisson exterior missing from the
reference power law and from the envelope hypothesis in the stability report.
It is a general exterior robustness result; the round's separate regular-core
construction addresses a different, stronger inner-matching question.

## 1. Model and normalized claim

Let `n>3`, `K>0`, `R0>0`, and `M0>0`. The material is the new neutral support
species of `../action/PROOF.md`, with

\[
 P=K\rho^{1+1/n},\qquad
 \epsilon_{\rm mat}=\rho c^2+nP,\qquad
 z(\rho)=\int_0^\rho\frac{dP(s)}s
         =\mathcal A\rho^{1/n},\quad \mathcal A=(n+1)K.
 \tag{1}
\]

Here `mathcal A` is an EOS constant; it is not the length squared `GM_Q/a0`
used in the action lane's gauge field. `z` is Newtonian chemical enthalpy per
rest mass, with units of speed squared. The exact equations to be solved are

\[
 P'=-\rho\frac{G[M_0+m(r)]}{r^2},\qquad
 m'=4\pi r^2\rho,\qquad m(R_0)=0,\qquad z(\infty)=0.
 \tag{2}
\]

`M0` is the fixed enclosed gravitating mass and `m` counts only the neutral
exterior support. Thus this is an exact Newtonian central-source plus fluid
problem. Gauge-field energy, relativistic pressure gravity, a live central
object and Einstein constraints are not included in this Poisson equation.
The action lane derives why the neutral material has no additional background
constitutive force at `B_U=0`; it does not eliminate those gravitational
closure obligations.

Set

\[
 t=r/R_0,\qquad Z=z/(GM_0/R_0),\qquad
 \rho_R=\left[\frac{GM_0}{\mathcal A R_0}\right]^n,\qquad
 \mu=\frac{4\pi R_0^3\rho_R}{(n-3)M_0}>0.
 \tag{3}
\]

The density is `rho= rho_R Z(t)^n`; the reference atmosphere would have
`Z0=1/t`. We prove that if a number `C>1` satisfies

\[
 \boxed{\quad1+\mu C^n\le C,\qquad q=n\mu C^{n-1}<1,\quad} \tag{4}
\]

then there is a unique solution in the envelope `1/t<=Z<=C/t`, with finite
support mass

\[
 \boxed{\quad \mu M_0\le M_s\le\mu C^nM_0.\quad} \tag{5}
\]

The uniqueness assertion is restricted to this envelope, not every possible
solution of (2).

## 2. The integral operator and its exact norm bound

Let `X` be the real continuous functions on `[1,infinity)` with finite norm
`||Z||_X=sup_{t>=1} t|Z(t)|`. Multiplication by `t` identifies this with the
complete space of bounded continuous functions in its sup norm. The closed
order interval

\[
 \mathcal K_C=\{Z\in X:1/t\le Z(t)\le C/t\}
\]

is complete in that norm. Define

\[
 (TZ)(t)=\frac1t+\mu(n-3)
 \int_t^\infty\frac{ds}{s^2}\int_1^s u^2Z(u)^n\,du.
 \tag{6}
\]

For every `Z` in the interval these integrals converge absolutely, since
`u^2 Z(u)^n<=C^n u^(2-n)` and `n>3`. The exact reference kernel is

\[
 (n-3)\int_t^\infty s^{-2}\int_1^s u^{2-n}du\,ds
 =\frac1t-\frac{t^{2-n}}{n-2}
 =\frac1t\left[1-\frac{t^{3-n}}{n-2}\right].
 \tag{7}
\]

The bracket is positive on `t>=1`, increases to one, and has supremum one.
Thus

\[
 \frac1t\le TZ(t)\le\frac{1+\mu C^n}t\le\frac Ct. \tag{8}
\]

The first condition in (4) is sufficient for the self-map. It is also
necessary for this entire order interval: evaluating `T(C/t)` and taking the
limit of `t T(C/t)` at infinity gives `1+mu C^n<=C`.

If `Z,W` lie in this interval, the ordinary real mean-value bound gives

\[
 |Z(u)^n-W(u)^n|
 \le n(C/u)^{n-1}|Z(u)-W(u)|
 \le n C^{n-1}u^{-n}\|Z-W\|_X.
\]

Substituting in (6) and using (7) yields

\[
 \boxed{\quad\|TZ-TW\|_X\le q\|Z-W\|_X.\quad} \tag{9}
\]

No finite radial grid or cutoff is used in this estimate.

## 3. Construction, first correction and certified error

Starting with `Z0=1/t`, define `Z_(k+1)=T Z_k`. The exact first iterate is

\[
 \boxed{\quad Z_1(t)=\frac{1+\mu}t
                   -\frac{\mu}{n-2}t^{2-n}.\quad} \tag{10}
\]

In the weighted norm, `||Z1-Z0||_X=mu`, with the supremum approached at
infinity. Iterating (9) gives

\[
 \|Z_{k+1}-Z_k\|_X\le\mu q^k,
 \qquad\|Z_*-Z_k\|_X\le\frac{\mu q^k}{1-q}.
 \tag{11}
\]

Indeed, summing the first inequality makes the sequence uniformly Cauchy after
multiplication by `t`; completeness and closedness give `Z_*` in `K_C`.
The Lipschitz estimate then gives `T Z_*=Z_*`. Two fixed points in the same
interval have distance at most `q` times their distance, so they coincide.
This proves the needed contraction conclusion directly. In particular,

\[
 \boxed{\quad\|Z_*-Z_1\|_X\le\frac{q\mu}{1-q}.\quad} \tag{12}
\]

The operator preserves order and `Z1>=Z0`, so the iterates are also monotone.
The geometric error estimate, not an extrapolated numerical trend, controls
their infinite-radius limit.

An explicit certificate needs no free optimization of `C`. Let

\[
 \mu_* =\frac{(n-1)^{n-1}}{n^n},\qquad C_* =\frac n{n-1}.
 \tag{13}
\]

For every `0<mu<mu_*`, choose `C=C_*`. Then (4) holds and `q=mu/mu_*<1`.
Conversely, the largest value of `(C-1)/C^n` on `C>1` is `mu_*`, attained
only at `C_*`: its derivative is

\[
 C^{-n-1}[n-(n-1)C].
\]

Thus simultaneous self-map and strict contraction inequalities admit some
`C>1` **exactly when** `0<mu<mu_*`. At equality the only possible envelope
has `q=1`. This is the sharp range of this certificate, not a nonexistence
threshold for Euler--Poisson equilibria outside it.

## 4. The fixed point solves Euler and Poisson

Write `I(t)=integral_1^t u^2 Z_*(u)^n du`. Since it is continuous and bounded,
differentiating (6) at every finite `t>=1` is legitimate and gives

\[
 -t^2Z_*'(t)=1+\mu(n-3)I(t),\qquad
 -[t^2Z_*'(t)]'=\mu(n-3)t^2 Z_*(t)^n.
 \tag{14}
\]

`Z_*` is positive and is as smooth as the EOS on the occupied domain; the
right derivative at `t=1` is `Z_*'(1)=-1`. Reconstruct

\[
 \rho(r)=\rho_R Z_*(r/R_0)^n,\quad
 m(r)=4\pi\rho_R R_0^3 I(r/R_0),\quad
 \Phi(r)=-z(r)=-\frac{GM_0}{R_0}Z_*(r/R_0).
\]

Equations (3) and (14) give

\[
 z'=-\frac{G[M_0+m(r)]}{r^2},\qquad
 m'=4\pi r^2\rho,\qquad
 \frac1{r^2}(r^2\Phi')'=4\pi G\rho.
\]

Finally, `dP=rho dz` from (1) gives (2). The envelope implies `z->0`,
and `m(R0)=0`; hence the boundary data are satisfied. The source potential
at the inner radius includes the constant potential of the outer fluid shells.
It is the **derivative**, not the value `z(R0)=GM0/R0`, that remains fixed by
the central mass. Substituting the original pure `1/r` profile into Poisson
would have missed this distinction.

The density envelope proves (5), because

\[
 M_s=4\pi\rho_RR_0^3\int_1^\infty t^2 Z_*(t)^n dt,
 \qquad\int_1^\infty t^{2-n}dt=\frac1{n-3}.
\]

In addition `tZ_*(t)->1+M_s/M0` and
`z(r)~G(M0+M_s)/r`, by dominated convergence applied to (6) or integration
of (14). The finite inventory is counted in the gravitational asymptote.

## 5. A sufficient joint self-gravity and causal-gate window

Keep fixed positive enclosed gauge charge `M_Q` and no charged exterior
density. Let `x0=GM_Q/(a0 R0^2) in (0,1)`, so `x=x0/t^2`. The inherited
local principal gate has

\[
 h_{\rm crit}(t)=D_0^2\frac{x_0^3 t^{-6}}{(1-x_0/t^2)^2}.
\]

From the actual EOS, with `eta=GM0/(R0 c^2)`,

\[
 h_{\rm eff}=h_s(1-s^2)
 =\rho c^2\left[1+\frac{n-1}{n}\eta Z_*\right],\qquad
 s^2=\frac{\eta Z_*}{n(1+\eta Z_*)}<1/n.
 \tag{15}
\]

These are the relativistic local EOS quantities; the Newtonian compressibility
used in the fluid stability estimate is instead `dP/d rho=z/n`, with units of
speed squared. The two derivatives must not be confused.

For `3<n<=6`, the lower envelope and the positive pressure term imply

\[
 \frac{h_{\rm eff}(t)}{h_{\rm crit}(t)}
 \ge\frac{\rho_Rc^2}{h_{\rm crit}(1)}t^{6-n}.
\]

Therefore the concrete sufficient normalization

\[
 \boxed{\quad\rho_R c^2>h_{\rm crit}(1)\quad} \tag{16}
\]

passes at every finite exterior radius for the **actual self-gravitating
solution**. This is stronger than the sharp reference-profile normalization;
it is chosen to survive the unknown positive self-gravity correction without
an interior minimization. No enthalpy profile has been assigned by hand.
For `n>6`, the upper envelope gives `h_eff/hcrit->0`, so finite `mu,C` cannot
pass this unchanged gate to infinity.

Equivalently, define

\[
 \mu_{\rm gate}=\frac{4\pi R_0^3h_{\rm crit}(1)}{(n-3)M_0c^2}.
\]

Whenever `3<n<=6` and `mu_gate<mu_*`, the nonempty sufficient window

\[
 \boxed{\quad\mu_{\rm gate}<\mu<\mu_*\quad} \tag{17}
\]

constructs an exterior equilibrium with finite counted support mass and the
local gate. `K` fixes `mu` through (3); the window is a conditional material
normalization, not a predicted abundance. Physical use of this Newtonian
comparison further requires `C eta<<1` and all omitted gravitational sources
to be consistently small or separately included.

## 6. What this closes, and what it leaves open

The immutable stability report `inputs/STABILITY_REPORT.md`, section 4,
assumes an actual equilibrium with `0<z<=C GM0/r`, and obtains the radial
fixed-wall bound `|Q_W|<=q Q_U`, with exactly `q=n mu C^(n-1)`. Equations
(4)--(14) now provide that equilibrium and envelope. Its positive radial
quadratic energy applies to the specified impermeable fixed inner boundary,
mass-preserving/no-flux perturbations and the restricted Newtonian fluid
sector. There is no uniform positive frequency gap on the infinite tail.

The same report's section 5 gives a negative-energy displacement for a moving
inner material surface against constant prescribed pressure. This construction
does not remove that failure: `rho(R0)>0`, `P(R0)>0`, and an actual wall,
inner fluid or regular core must supply the stress and its own dynamics.
The source mass and charge and any interface must be matched. Existence on
the exterior is not boundary-independent stability or a complete isolated
halo. The regular-core lane must be judged on its own matched equations.

The constitutive magnetic response may be chosen on the admitted open gate
domain as in the pinned action/mode analysis. That remains a conditional
finite-density local principal result. This calculation supplies neither a
microscopic neutral species nor off-shell vacuum regularity, nonlinear
well-posedness, coupled gauge/gravity stability, formation, abundance, lensing
or empirical viability.

The dependency graph is: specified neutral action/EOS -> ordinary background
Euler equation; self-map and contraction estimates -> actual finite-mass
Euler--Poisson exterior; its envelope plus sufficient density normalization ->
inherited local causal gate; its same envelope plus the restricted stability
report -> positive fixed-wall radial fluid energy. Matching, carrier identity,
the full metric equations and coupled stability remain independent leaves.

## 7. Evidence and reproducibility

The initial requested base is `283acbcffe1c6c4a5e8f9860f66e43c4e3808ab3`.
The action and stability reports were copied into this lane's `inputs/` and
pinned by its `source_manifest.json`; original round inputs remain under
`../inputs/`. Only `self_gravity/` was edited for this task.

`check_self_gravity.py` checks the kernel primitive, Picard correction, inner
flux, dimensionless Poisson equation, mass integrals and explicit certificate
constants in exact arithmetic. It has no radial cutoff, floating spectrum or
ODE fit. The general estimates above are analytic; bounded arithmetic controls
do not replace them. `computation_contract.json` and `run_exact/manifest.json`
pin code, proof and dependencies. `REPRODUCE.txt` records a bounded replay.
