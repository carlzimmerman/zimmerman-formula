# Which inner-orbit requirement belongs to which kernel?

Pinned source base: `19d8c776494f0995d5b6b9330dd3ca5065025f5e`.

The exponential inner hollow is a consequence of the chosen interpolation, not of the user's separate scale relation `a0 = kappa c sqrt(G rho_DE)`. The repository already contains a repaired interpolation with a positive inner cusp. This note derives its local density and high-binding isotropic distribution asymptotic. It does not establish a complete halo, a formation mechanism, a microscopic carrier, or kappa = 1/2.

## Exact continuous splice and the actual implementations

Write `y = g_b/a0`, `h(y) = y[nu(y)-1]`, and

\[
h_R(y)=\frac{y}{e^{\sqrt y}-1},\qquad
h_R'(y)=\frac{2(e^{\sqrt y}-1)-\sqrt y\,e^{\sqrt y}}
 {2(e^{\sqrt y}-1)^2}.
\]

Define `y_p` by `h_R'(y_p)=0`, `h_p=h_R(y_p)`, `b=0.05 h_p`, and the earlier switch `y_s` by `h_R'(y_s)=b/(y_s+y_p)`. The continuous repair is

\[
h(y)=\begin{cases}
h_R(y),&y\leq y_s,\\
h_R(y_s)+b\log\dfrac{y+y_p}{y_s+y_p},&y>y_s,
\end{cases}
\qquad \nu(y)=1+\frac{h(y)}y.
\]

Independent evaluation of these scalar root equations gives:

| Quantity | Value |
|---|---:|
| `y_p` | 2.5396382821881684 |
| `h_p` | 0.6476102378919150 |
| `b` | 0.03238051189459575 |
| `y_s` | 2.337412405266330 |
| `h_R(y_s)` | 0.6469603693249751 |
| `r_s/r_M = 1/sqrt(y_s)` for a point source | 0.6540821957169259 |

The analytic implementation is [CFG233_common.py, lines 92–113](../../campaign_fresh_gravity/CFG233_rc100_referee/CFG233_common.py). The switch is **not** `y_p`; summaries saying the repaired kernel equals the exponential all the way to `y_p` are approximate descriptions. The floor starts earlier.

The PM implementation [cfg424_pm.py, lines 96–108](../../campaign_fresh_gravity/CFG424_turnaround_catchment/cfg424_pm.py) instead integrates `max(h_R', b/(y+y_p))` on a log grid, then interpolates. Its grid ends at `y=10^12`; other copies end at `10^14`. `np.interp` clamps `h` beyond the last grid point, so the literal far-tail extrapolation becomes constant `h`, not the logarithm above. The following logarithmic asymptotics concern the intended continuous splice. The clamped extension instead has a `1/r` point-source cusp. Neither has the exponential hollow.

## Positive real cold density

For spherical baryons with enclosed mass `M_b(r)`, use `y=G M_b(r)/(a0 r^2)` and `g_c=a0 h(y)`. Gauss's law gives

\[
\rho_c=h'(y)\rho_b+
\frac{a_0}{2\pi G r}\,[h(y)-yh'(y)].
\]

Both coefficients are positive. Below the splice, `h_R'>0` and

\[
h_R-yh_R'=\frac{y^{3/2}e^{\sqrt y}}
 {2(e^{\sqrt y}-1)^2}>0.
\]

Above it, put `B(y)=h(y)-by/(y+y_p)`. Then `B'(y)=by/(y+y_p)^2>0`, and `B(y_s)=0.6314414389218127>0`. Therefore any nonnegative spherical baryon density produces nonnegative effective cold density under this spherical algebraic law. This is not a claim about arbitrary nonspherical QUMOND phantom densities.

Outside compact baryons define `mu=G M_b`, `r_M=sqrt(mu/a0)`, `V_f^2=mu/r_M`, and

\[
c_h=h_R(y_s)-b\log(y_s+y_p)=0.5956521313178601.
\]

The point-source inner expansion is

\[
\rho_c(r)=\frac{a_0}{2\pi G r}
\left[2b\log\frac{r_M}{r}+c_h-b
 +O\!\left(\frac{r^2}{r_M^2}\right)\right].
\]

It rises inward. On the repaired branch this follows directly from `rho_c proportional to sqrt(y) B(y)` and `B,B'>0`. The exponential branch is used only at `sqrt(y)<=1.529`, before its density maximum at `sqrt(y)=3.8300`. Thus the point-source profile has no inner outward-rising hollow. For finite-sized baryons, this point-source asymptote applies only outside their extent; it does not describe the centre of a resolved baryonic core.

## Local high-binding isotropic distribution

Assume a Newtonian point source and an outer completion with finite central contribution to the cold potential. The logarithmic cold acceleration is integrable at the centre, so relative potential `Psi=Phi_boundary-Phi` satisfies `Psi=mu/r+O(1)`. Hence, with `E0=V_f^2` and `D=a0/(2 pi G mu)`,

\[
\rho_c(\Psi)=A\Psi\log\frac{\Psi}{E_0}+C\Psi+O(\log\Psi),
\qquad A=2bD>0,\quad C=(c_h-b)D.
\]

For an isotropic mass distribution `f(E)` with binding energy `E=Psi-v^2/2`, the velocity integral is

\[
\rho(\Psi)=4\pi\sqrt2\int_0^\Psi
 f(\mathcal E)\sqrt{\Psi-\mathcal E}\,d\mathcal E.
\]

Its high-binding inverse is

\[
f(\mathcal E)=\frac{
 A\log(\mathcal E/E_0)+C+A(1+\log4)+o(1)}
 {\sqrt8\,\pi^2\sqrt{\mathcal E}}
\quad (\mathcal E\to\infty).
\]

This asymptotic uses the smooth derivative expansion inherited from the displayed density and potential. It is eventually positive because `A>0`. The coefficient and constant follow by inserting the displayed leading form into the velocity integral and using

\[
\int_0^1t^{-1/2}(1-t)^{1/2}\,dt=\frac\pi2,\qquad
\int_0^1t^{-1/2}(1-t)^{1/2}\log t\,dt
=-\frac\pi2(1+\log4).
\]

An independent quadrature of this Abel pair, with illustrative `A=1,C=2,E0=1` and `Psi=0.1,1,10,100`, reproduced `A Psi log(Psi/E0)+C Psi` to absolute error at most `1.2e-13`. This check verifies normalization, not positivity of that illustrative all-energy extension or existence of a global physical halo.

Crucially, the local positive asymptotic draws on arbitrarily high binding energies near the mathematical point source. It therefore does **not** contradict a stream result assuming a fixed bounded energy range. No full-halo Eddington inversion has been performed. Positivity at intermediate energies, a physical outer edge, stability, formation and finite-sized central baryons remain separate obligations. In particular, a sharp cut with nonzero density just inside the edge is not supplied by this local isotropic result.

## What changes, and what does not

The repaired cusp removes the **essential exponential** suppression demanded by the exponential interpolation. A residual constraint remains: `4 pi r^2 rho_c v_escape` scales as `sqrt(r) log(r_M/r)` and tends to zero in the Newtonian point-source limit. A nonzero fixed purely radial crossing flux with bounded energies instead gives an `r^(-3/2)` density. Thus this repair weakens the orbit-selection requirement to a power-law one; it does not allow arbitrary centre-crossing traffic.

- Kernel and scale are separate inputs in [THEORY_v1, A1–A2](../../campaign_fresh_gravity/THEORY_v1_2026-10-09.md). The repair preserves `a0=kappa c sqrt(G rho_DE)` algebraically, without deriving kappa.
- The repair is already the baseline of [CFG468, table and lines 46–49](../../campaign_fresh_gravity/CFG468_kernel_family/README.md). Exponential improves independent-point SPARC chi-squared by 30.15 relative to repaired; that audit quotes about 1.7 after its clustering deflation. The T-free fitted `kappa_Lambda` changes from 0.474 (repaired) to 0.464 (exponential), so empirical scale calibration remains kernel-dependent. No fit was rerun here.
- Its slow high-acceleration tail creates an unacceptable planetary anomaly **if the Sun owns its own settled target**. The host-only reading passes that particular repository test; ownership/capture is still required. See [CFG484, N1d](../../campaign_fresh_gravity/CFG484_alternative_chassis_search/README.md), lines 65–66. This is a physical cost of the alternative, not a global solar-system clearance.
- [CFG620's definition](../../campaign_fresh_gravity/CFG620_anisotropic_velocity_target/README.md), lines 54–58, constructs a stationary anisotropic target conditional on the **exponential** density. Its positivity/support result does not decide the repaired profile's global isotropic distribution or formation.

The useful next fork is an explicit comparison of the two already-committed kernels' orbital requirements. No baseline, manuscript, frozen criterion or simulation was changed by this note.
