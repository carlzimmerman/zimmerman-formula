# Conditional isentropic endpoint from mass and energy

The calculation in [isentropic_limit.py](isentropic_limit.py) predicts a
regular, baryon-free, isolated hydrostatic sphere after spatial
isentropization. It retains the full mass and conserved energy, with a
pressure-free material surface at density `rho_q`. The material scales and
the gated equation of state are fixed. No measured final entropy or positive
entropy floor is an input. Global branch uniqueness, preservation of entropy
ordering, and global dynamical convergence remain unproved.

For the virgin initial sphere, `K=0`, mass `M=pi/3`, radius `R_i=1`, velocity
`v=H_i r` with `H_i=-0.25`, and `G=rho_q=Kstar=1`, the continuum energy is

\[
 E_i=\frac{3}{10}H_i^2MR_i^2-\frac{3GM^2}{5R_i}
     =-0.6383386726543542.
\]

The [recorded prediction](isentropic_prediction/result.json), with its
[execution manifest](isentropic_prediction/manifest.json) and
[declared contract](isentropic_prediction_contract.json), gives these numerical
values:

| Quantity | Prediction |
| --- | ---: |
| Constant `K` | 0.3496240637094284 |
| Central density `rho_c/rho_q` | 2.455533676765764 |
| Material surface radius | 0.5379206218348132 |
| Half-mass radius | 0.404769306556221 |
| Total entropy `S=M(K/Kstar)^(1/3)` | 0.7377270763911522 |
| Internal energy `U` | 0.6383204705672295 |
| Gravitational energy `Omega` | -1.2766591432169432 |

These are floating-point predictions, rather than exact constants. The
computed energy mismatch is `4.63e-12`; the direct and virial energy integrals
differ by `1.10e-14`. These residuals check internal consistency and do not
bound every numerical error.

## Stationary mass and energy selection

Write `d=rho/rho_q`, `w=W/rho_q`, and let `h(d)` be the fixed activation gate.
The material law is

\[
 e=KW(\rho),\qquad P=K\rho^2h(d),\qquad
 W(\rho_q)=\frac32\rho_q.
\]

For each regular dimensionless central density `d_c>1`, the hydrostatic shape
has dimensionless mass `m_s` and radius `x_s`. The dimensional scales are

\[
 L=\sqrt{\frac{K}{4\pi G}},\qquad
 M_s=4\pi\rho_qL^3,\qquad E_s=K\rho_qM_s.
\]

Fixing the physical mass selects

\[
 K=\left(\frac{M\sqrt{4\pi}\,G^{3/2}}{\rho_qm_s}\right)^{2/3}.
\]

The remaining scalar solve matches `E_i` to `E_eq=U+Omega`. Independently,
hydrostatic virial balance gives `Omega=-3 int P dV`, so the same energy is

\[
 E_{\rm eq}=K\int\left[W(\rho)-3\rho h(d)\right]dm.
\]

The latent specific energy `3 K rho_q/2` at the free surface is included;
subtracting it would change the mass/energy prediction.

Along a differentiable fixed-mass stationary branch whose parameter
derivatives are admissible free-surface displacements, the stationary
envelope identity is

\[
 \frac{dE_{\rm eq}}{dK}=\int W\,dm=\frac UK>0.
\]

Indeed, in mass coordinates `1/rho=4 pi r^2 r_m`, the variation in shape
vanishes by hydrostatic balance. Its boundary term is
`-[4 pi r^2 P delta r]_0^M=0`. A moving surface adds no pressure work, while
the latent energy remains in the integral.

The formal endpoint limits are a dense `n=1` polytrope as `K->0`, with
`R~sqrt(pi K/(2G))` and `E~-GM^2/(2R)->-infinity`, and a sphere of density
`rho_q` as `K->infinity`, with `E~3 K rho_q M/2->+infinity`. Strict increase
along a differentiable branch does not by itself prove that the branch is
globally single or covers every `K>0`. An argument excluding mass turning
points using the positive adiabatic radial gap must also establish that the
branch derivative satisfies the physical free-traction condition. That
global uniqueness argument is not supplied here.

## Why retained adverse ordering would force constant entropy at rest

For `sigma=(K/Kstar)^(1/3)`, the temperature is
`T=3 Kstar^(1/3) K^(2/3) W`. On the active interior, define

\[
 \Gamma=\left.\frac{\partial\log P}{\partial\log\rho}\right|_K
       =2+\frac{d\,h'(d)}{h(d)}\ge2,\qquad
 \beta=\frac{\rho h(d)}{W(\rho)}\in(0,1].
\]

Here `h'(d)` denotes the derivative with respect to `d`. Consequently

\[
 \left.\frac{\partial T}{\partial P}\right|_K>0,\qquad
 \left.\frac{\partial\log T}{\partial\log K}\right|_P
       =\frac23-\frac{\beta}{\Gamma}\ge\frac16>0.
\]

Hydrostatic balance gives `P'<0` away from the center. If the ordering
`K'<=0` is retained, these two inequalities force `T'<0`. For the outward
instability-gated closure, a strictly negative `K'` then activates a positive
outward heat flux wherever the material is active and diffusivity is
positive. In an isolated stationary connected active region, the heaters
vanish and the luminosity is constant; regularity at the center and closed
boundaries make it zero. Thus zero flux and retained `K'<=0` require `K'=0`
throughout the active interior.

This is a conditional characterization of a stationary state. The transport
equations have not been shown to preserve `K'<=0`, approach such a regular
state, or produce a positive entropy bound uniform in mesh resolution and
time. The positive selected `K` therefore supplies a stationary benchmark,
not a dynamical entropy-floor theorem.
