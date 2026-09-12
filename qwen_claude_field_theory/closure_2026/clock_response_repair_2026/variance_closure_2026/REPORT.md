# Same-action variance dynamics and the first nonlinear vertices

**Full gravity theory: OPEN.** This checkpoint derives an actual missing
equation and computes the first omitted nonlinear interactions. It does not
certify a cosmological attractor, CMB viability, or all the gravity gates.
No coefficient functions were reconstructed and no particle species added.

Base `48ab93de3` (PAPER20), following `d2301db52`. Concurrent commit
`08281ae25` (L195) was also inspected. Input hashes, not arrival order, reconcile
the parallel runs; no imported scientific source changed during them.

## 1. The variance equation actually implied at leading order

For the unchanged action

\[
S=\int\sqrt{-g}\,[M^2(R-2\Lambda)/2+P(X,\tau)-V(\tau)
                   +sW(Y,\tau)+\gamma X\Box\chi]+S_m,
\]

the physical clock-frame gradient begins at second perturbative order:

\[
Y^{[2]}=a^{-2}|\nabla(\sigma-Q\delta\tau/s)|^2.
\]

This is derived with arbitrary first- and second-order metric perturbations,
not assigned from a coordinate gradient. In unitary clock gauge, let
\(u_k=(\sigma,\delta Q,r,\delta Q_r,\theta,\delta\rho_b)\),
\(\dot u_k=A_k(t)u_k\), \(\delta N=\ell_k u_k\),
and \(C_k=\langle u_ku_k^\dagger\rangle\). For RMS-normalized modes,
\(p_k=k^2/a^2\), with any fixed spectral weights included in the sum:

\[
\boxed{\dot C_k=A_kC_k+C_kA_k^\dagger,\qquad
\dot{\mathcal Y}=-2H\mathcal Y+
2\sum_kp_k\operatorname{Re}\left[C_{10,k}
                         +Q\sum_j\ell_{j,k}C_{j0,k}\right].}
\]

These equations retain the original action's expansion, coefficient rates,
matter response and constrained lapse. An unnormalized real cosine instead
has spatial mean \(p_k\langle\sigma_{\rm amp}^2\rangle/2\); this factor
is explicit and is not a change to any physical coupling.

**Restricted theorem.** On a regular reduced branch with the displayed
cross-coupling nonzero, no universal exact law
\(\dot{\mathcal Y}=f(t,k,\mathcal Y)\) describes every admissible linear
initial ensemble. Same variance can have different field-velocity or
matter-density correlations. `geometry/DERIVATION.md` constructs positive
semidefinite witnesses using the actual constraint matrix. In particular,
if its scalar/lapse minor is \(\Delta=A_cL-ED\), then
\(A_{0,5}=-QA_c/(2M^2\Delta)\); this is computed, not an assumed rank.

`VarianceClosure.lean` proves the exact two-coordinate algebraic criterion:
for \(p>0\), the rate of \(px^2\) under
\(\dot x=ax+by\) factors through \(px^2\) for every \((x,y)\) iff
\(b=0\). The covariant/action-to-state map is a separate symbolic audit,
not silently included in the Lean certificate. This theorem does **not**
exclude a nonlinear attractor on a restricted basin.

## 2. Actual constrained evolution, including inertia

The unchanged sourced history is tested over proper time \([0,0.02]\) in
its dimensionless units, with \(k=0.3,3,30\). At each k, three small,
constraint-compatible ensembles have \(\mathcal Y_0=10^{-12}\) but
\(\dot{\mathcal Y}_0/\mathcal Y_0=-2,0,+2\).

The initially zero-rate ensembles immediately depart from balance:

| k | \(\ddot{\mathcal Y}_0/\mathcal Y_0\) | \(\mathcal Y(0.02)/\mathcal Y_0\) |
|---:|---:|---:|
| 0.3 | -0.84352413 | 0.9998327920 |
| 3 | -1.05325329 | 0.9997923561 |
| 30 | 1.54430648 | 1.0003006835 |

Even fixing both \(\mathcal Y\) and \(\dot{\mathcal Y}\) does not close
the dynamics for all ensembles: adding independent velocity variance keeps
both unchanged but changes \(\ddot{\mathcal Y}\). Exact stationarity needs
the additional correlation condition

\[
\langle\dot\sigma^2\rangle+\langle\sigma\ddot\sigma\rangle
=(2H^2+\dot H)\langle\sigma^2\rangle.
\]

Lean proves this necessary condition, including its coherent-mode reduction
\(\ddot\sigma=(H^2+\dot H)\sigma\). The physical acceleration is computed
from \((\dot A+A^2)u\), not a guessed friction coefficient. Time stencils
are refined and independently checked against the evolved variance.

Independent covariance integration agrees with fundamental-matrix transport
to a maximum scaled difference \(3.10\times10^{-12}\). Original eight-Euler
residuals, including selected initial ensembles, are below
\(1.93\times10^{-7}\) with the source's documented scaling. These are
bounded floating-point checks, not interval bounds or a nonlinear simulation.
The k=0 gradient vanishes; its separate homogeneous constraints are not
computed by substituting into the singular finite-k reduction.

## 3. New nonlinear calculation: the actual bare quartic vertex

To go beyond linear covariance, expand the unchanged scalar action at fixed
metric and clock, with
\(\chi=\bar\chi+\epsilon A\cos kx\). Holding the geometry fixed isolates
vertices; it is **not** a solved finite-amplitude gravitational background.
For the zero perturbation-velocity spatial vertex,

\[
\boxed{\langle L_4\rangle=
\frac{3k^4A^4}{16a}(P_{XX}+sW_{YY}).}
\]

The script also derives every bare quartic term involving the perturbation
velocity and \(P_{XXX},P_{XXXX}\), by expansion rather than inserting this
boxed answer. The constant-gamma cubic term has degree at most three in
\(\chi\) on fixed geometry, but still contributes interactions and exchange
when the metric/clock are dynamical.

Independent variation of the static spatial sector gives the cubic source

\[
E^{[3]}_{P+sW,\mathrm{spatial}}=
\frac{3(P_{XX}+sW_{YY})A^3k^4}{2a^4}
[\cos kx-\cos3kx].
\]

A single harmonic is therefore not closed within this nonlinear sector.
At the actual first sourced state, \(Q=0.9078321505772312\),
\(P_{XX}=0.6301409907160642\),
\(sW_{YY}=-0.06242275469149993\), so their sum is
\(0.5677182360245643\). Including P reverses the isolated W contribution's
sign. **This is not a sign theorem for the full reduced Hamiltonian.**
Metric/clock exchange, the time part of the scalar equation, and the other
harmonics must still be included before deciding nonlinear stabilization.

The exact constitutive flux's third harmonic converges to this coefficient
as amplitude decreases: relative errors are 0.00138265, 0.000124561 and
0.0000138413 at amplitudes 0.01, 0.003 and 0.001. Quadrature refinement and a
linear no-third-harmonic control are checked independently.
The same harmonic has
\(\langle Y^2\rangle=3\langle Y\rangle^2/2\), so
\(\langle W(Y)\rangle-W(\langle Y\rangle)
=W_{YY}\langle Y\rangle^2/4+O(\epsilon^6)\)
in this fixed-geometry calculation. Averaging and evaluating at the variance
already differ at the first nonlinear feedback order.

## 4. What PAPER20 and L195 do and do not change

Their local claims are independently reviewed in `review/PAPER20_AUDIT.md`.
The L194 ODE attractor is not denied; its identification with a same-action
nonlinear state remains unproved. The new covariance system is also not
presented as a saturation model: it is homogeneous and linear in C.

L195's CLASS comparisons prescribe a positive effective-fluid sound speed,
where the L194 equilibrium is negative, and use separate constant values for
the CMB and late-time runs. They do not derive that fluid, its abundance, or
its transfer history from this action. A successful comparison for those
inputs cannot close this theory's CMB gate. No external observational bound
or publication status is independently authenticated here.

## Next unavoidable calculation

Construct the **constraint-reduced cubic and quartic action** on this same
sourced history. Retain the induced homogeneous and 2k geometry/clock/matter
responses and the 3k scalar mode; preserve constraints and include the
higher-order physical-volume definition of Y. Test whether the resulting
nonlinear equations actually admit a regular attracting state with a real,
positive physical scalar characteristic. Only then derive its full stress
and run one common cosmological transfer history. No new coefficient fit is
required or justified by this checkpoint.

The action's previously found unstable homogeneous samples remain unstable;
this does not rule out every nonlinear statistical state. Exact MOND, the
full Dirac count, PPN, galaxies/clusters and CMB viability are not newly
certified. See `COMMANDS.md` and the four version-2 manifests for executable
evidence; see `FILES.md` for the exact new paths.
