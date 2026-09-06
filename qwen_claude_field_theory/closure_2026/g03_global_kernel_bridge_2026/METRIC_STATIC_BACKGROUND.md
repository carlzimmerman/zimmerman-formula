# Solved backgrounds and a physical initial-curvature obstruction

2026-09-06. Same bulk Hamiltonian as `METRIC_CONSTRAINT.md` and
`METRIC_CAUSAL_SYMBOL.md`; no interpolation replacement or empirical data.

**Result:** regular nonlinear static backgrounds exist on a regulated finite
slab. On two such backgrounds, a computed positive-energy matter experiment
has a nonzero initial curvature difference outside the support of the matter
initial-data difference. The calculation includes background derivatives,
boundary conditions, and the homogeneous trace mode. It no longer relies on
the previous spacetime tangent-inverse hypothesis or an arbitrary imposed
source history. It remains a perturbative, numerically verified obstruction,
conditional on smooth coupled solvability and the stated boundary problem.
It is not a completed theory or an unconditional theorem about all MOND.

## 1. Vary the background before fixing coordinates

The Hamiltonian is

\[
H=\int_\Sigma [N\mathcal H_{GR}+N^i\mathcal H_i
-2N\sqrt h a_0^2F(a^2/a_0^2)
+\lambda(\pi-\sqrt h\bar\pi)]d^3x+H_m,
\qquad F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}].
\]

Here \(a_i=D_i\ln N\), \(\bar\pi=\int\pi/\int\sqrt h\), and c=1.
The common gravitational normalization is suppressed. Matter fields below
can be rescaled by \(\sqrt{16\pi G}\) to use this normalization.

For \(ds^2=-N(z)^2dt^2+B(z)^2dz^2+A(z)^2(dx^2+dy^2)\), static
\(\pi^{ij}=0\), zero shift and homogeneous lambda, the trace-multiplier
term and its first variation vanish. The script computes the spatial Ricci
scalar from its connection and integrates the EH density by parts, obtaining

\[
L={2NA'^2+4AA'N'\over B}-2\Lambda NBA^2
+2NBA^2a_0^2 F\!\left({N'^2\over N^2B^2a_0^2}\right).
\]

All three fields are varied while B is still free. Define
\(D=B^{-1}\partial_z\), \(u=D\ln N>0\), \(b=D\ln A\),
\(y=u/a_0\), \(E=e^{-y}\), and \(\chi=(1-y)E\). The equations are

\[
\mathcal N=2Db+2\chi Du+3b^2+\Lambda-a_0^2F+2u^2E+4buE=0,
\]
\[
\mathcal A=Db+Du+b^2+bu+u^2+\Lambda-a_0^2F=0,
\qquad C=b^2+2bu+\Lambda-a_0^2F+2u^2E=0.
\]

The actual variational derivatives are
\(E_N=-2BA^2\mathcal N\), \(E_A=-4NBA\mathcal A\),
\(E_B=-2NA^2C\). Exact differentiation verifies

\[
N'E_N+A'E_A-BE_B'=0,
\qquad DC+(u+2b)C=u\mathcal N+2b\mathcal A.
\]

Thus the radial constraint propagates; it is not imposed after integration.
The **computed** highest-derivative Hessian determinant is

\[
\det L_{(N',A')(N',A')}=-{16A^2\over B^2}
\underbrace{[1+(y-1)e^{-y}]}_{\mu_\parallel}<0
\quad(y>0).
\]

Its nonvanishing, rather than its sign, establishes that the static equations
can be solved for the two second derivatives. This is a *spatial* Hessian,
not a ghost or canonical-DOF count. On N,A,y>0 the resulting ODE is smooth
and locally Lipschitz. A sufficiently short integral-equation interval is a
contraction, giving a genuine local solution through any real constrained
seed. The determinant vanishes at y=0; that point is explicitly excluded.

After B=1, a seed is obtained by solving the varied constraint:

\[
b_0=-u_0+\sqrt{u_0^2-\Lambda+a_0^2F(y_0^2)-2u_0^2e^{-y_0}}.
\]

Two independent integrators check all three equations on each patch. The
background audit uses (y0,Lambda/a0^2)=(1,0) and (20,32 pi); maximum absolute
constraint drifts are 6.51e-16 and 1.56e-13. The later response calculation
also solves its own backgrounds at (0.5,0) and (10.5,32 pi).

## 2. Make the spatial average legitimate; do not invent a global vacuum

Use \(\Sigma=[-L,L]\times T^2\), with fixed induced N,A at the walls,
zero shift, and the standard Dirichlet gravitational boundary completion.
The EH integration-by-parts boundary contribution is
\([-4NAA'/B]_{-L}^{L}\); its cancelling boundary action removes the
unfixed normal-derivative variation. The script checks that cancellation
including the B variation. The auxiliary boundary term vanishes with delta N.
The volume is finite, \(\bar\pi=0\) exactly, and homogeneous lambda equals
its average. This supplies a regulated-domain background of the same bulk
Hamiltonian, not a closed-leaf cosmological completion.

There is a separate exact obstruction to the latter *static vacuum* claim.
Full spatial conformal variation and lapse variation give

\[
D_i[(1-F_z)D^iN]=N[a_0^2(F-zF_z)-\Lambda],
\qquad F-zF_z=2-(y^2+2y+2)e^{-y}<2.
\]

For a smooth positive lapse on a compact boundaryless static vacuum leaf,
the integrated left side is zero and the right side is strictly negative
when Lambda>=2a0^2. No such solution exists. Wall flux resolves this on the
slab. This does **not** exclude expanding FLRW, horizons, matter-supported
solutions or local static regions; the analogous GR positive-Lambda caveat
is important. No novelty is claimed for this integral argument.

The optional framework input Lambda=32 pi a0^2 satisfies this inequality.
It is imposed, not derived. The dimensionless calculation applies on both
the canonical a0=9.3619e-11 and alternate a0=1.1279e-10 m/s^2 footings;
physical lengths are obtained from z_dimensionless=a0*z_physical/c^2.

## 3. Use actual positive-energy matter on the curved background

Take three minimally coupled canonical KG fields with squared masses 1,4,9
in the chosen dimensionless units. Their action is
\(-\frac12\int\sqrt{-g}\sum_i[(\partial\phi_i)^2+m_i^2\phi_i^2]\).
Set the initial values and normal velocities of the two states to

\[
\phi_i(0)=\varepsilon(1,\tfrac12,\tfrac13)_i,\qquad
N^{-1}\dot\phi_i(0)=\varepsilon[(1,1,1)_i
\mathbin\pm(1,-2,1)_i\sigma(z)].
\]

Sigma is smooth and supported strictly inside the slab; use identical
compatible matter boundary data. Both initial energy densities are the
derived positive expression \(3\varepsilon^2(1+\sigma^2)\).
Let delta T be half their stress difference with the overall epsilon^2
removed. Solve KG in coordinate-time jets using the **curved** wave operator

\[
\ddot\phi=N^2[\phi''+(u+2b)\phi'-m^2\phi].
\]

The computed jets give

\[
\delta T(0)=\delta\dot T(0)=0,\quad
\delta\ddot\rho(0)=0,\quad
\boxed{\delta\ddot S(0)=-24N^2\sigma},\quad S=h_{ij}T^{ij}.
\]

The script also evaluates the covariant divergence with the connection
terms, obtaining six zero coefficients through time degree 2. More
generally the canonical matter action gives
\(\nabla_\mu T^{\mu\nu}=\sum_i(\Box\phi_i-m_i^2\phi_i)\nabla^\nu\phi_i\).
The two sources are therefore physically specified, not arbitrary signed
forcing. Gravity affects this test-matter stress only at order epsilon^4;
its leading backreaction is order epsilon^2. These are three explicitly
counted ordinary matter species, not hidden auxiliary gravitational modes.

## 4. Compute the first gravitational response, including the zero mode

Work at order epsilon^2 about the static vacuum solution. The experiment
seeks common gravitational initial data; equal stress removes the immediate
source mismatch but does not itself construct those common data. In zero-shift gauge,
the difference initially has delta h=delta pi=delta N=0. The vanishing
first source jets give a homogeneous first-derivative constraint problem.
Its uniqueness is tested by the same boundary matrix used below.

Write the nontrivial second metric/lapse jets as

\[
\delta\ddot h_{ij}=2w h_{ij},\quad
\delta\ddot N=Nv,\qquad
w={\delta\dot\lambda-\delta\dot{\bar\lambda}\over2}.
\]

Twice differentiating the lapse constraint and the preservation of the
mean-subtracted trace constraint gives

\[
\delta E_{\rm lapse}[w,v]=0,\qquad
\delta E_{\rm trace}[w,v]=24N^2\sigma+{2c\over N},
\quad c=\delta\bar\pi''',\qquad \int A^2w\,dz=0.
\]

Here \(E_{\rm lapse}=E_N/(A^2B)\) and
\(E_{\rm trace}=(AE_A+BE_B)/(NA^2B)\). The script differentiates the
full background equations with delta A=Aw, delta B=Bw and delta N=Nv
**before** B=1. All lower-derivative background terms are retained. The
complete coefficient matrix is saved. Neither c=0 nor a local pi=0
replacement is assumed. Impose w=v=0 at both walls.

Three integrated homogeneous response columns determine a 3x3 boundary
matching matrix, including the volume integral. Its rank is computed,
not preset: both examples give rank 3, condition numbers 22.7 and 21.4.
The smallest singular values are 0.133 and 0.578. Thus no numerical
homogeneous kernel was found; an interval-certified statement is still owed.

The observable is an exact initial-slice Ricci contraction, **not** the lapse:

\[
\boxed{\delta R_{\mu\nu}n^\mu n^\nu(0,z)=-{3w(z)\over N(z)^2}.}
\]

It follows from \(\delta R_{00}=-h^{ij}\delta\ddot h_{ij}/2\);
the lapse second derivative cancels. With identical initial metric and
observer, this difference is not removed by a coordinate relabeling. In the
analytic GR Rindler control the computed lapse equation is -4w''=0, so Dirichlet data force
w=0: no corresponding curvature tail. Positive-Lambda GR requires a
separate no-resonance check, which is not assumed here.

Use \(\sigma=\exp[1-1/(1-(z/(0.35L))^2)]\) inside |z|<0.35L and zero
elsewhere. Results compare RK45 with DOP853 and independently check the ODE,
wall values and weighted mean:

| y0, Lambda/a0^2 | L | peak exterior / peak total curvature | relative integration difference |
|---|---:|---:|---:|
| 0.5, 0 | 0.02 | 0.5240 | 4.73e-8 |
| 10.5, 32 pi | 0.002 | 0.5302 | 9.23e-8 |

“Exterior” means |z|>0.5L, where the matter initial-state difference vanishes.
Maximum independent ODE residuals are below 9e-9, relative weighted-mean
residuals below 4e-14. This ratio is **not an observational prediction**:
it describes this normalized test experiment, with overall epsilon^2 removed.

## 5. What is now ruled out, and what is still owed

For this regulated Hamiltonian and these matter states, the computed smooth
perturbative response does not have a local domain of dependence: a local
initial matter change produces a curvature difference outside its support
on the initial slice. Fixed identical wall data do not make that a causal
signal sent from the walls. The spatially averaged constraint is part of the
model and is included, not a removable numerical artifact.

This is stronger than the earlier principal-symbol obstruction: a solved
background, actual canonical matter, and the full spatial operator replace
the earlier arbitrary-source and tangent-inverse assumptions. It is still
**conditional on constructing the pair's common gravitational initial data,
higher constraint/boundary compatibility, and smooth coupled solutions**.
A failure of that existence premise would expose a
different admissibility/regularity problem, not automatically prove the
same causal theorem. Floating-point integration is not interval certification.

**Status:** causal initial-jet gate **DEAD in the tested perturbative boundary
problem**; complete nonlinear candidate **OPEN, with a strengthened
conditional obstruction**; full relativistic MOND objective **OPEN**.
No full nonlinear Dirac count, PPN certificate, empirical success, or global
novelty claim is supplied by this calculation.

**Next unavoidable calculation:** construct the common constraint-satisfying
initial data, interval-certify the boundary inverse, and establish (or refute)
a smooth coupled initial-boundary solution for this
specific positive-energy pair. That closes the remaining implication; another
kernel fit does not. A new viable candidate must change the leading
kinetic/constraint architecture if this response persists.

## 6. Exact artifacts, commands and verification

New files in this directory:

- `metric_static_background.py`, `test_metric_static_background.py`
- `metric_static_background_results.json`
- `metric_initial_response.py`, `test_metric_initial_response.py`
- `metric_initial_response_results.json`
- this report, `metric_static_background_manifest.json`

No prior research artifact was modified. Existing unrelated working-tree
changes were preserved. No commit or push was performed. Inspected HEAD:
5e31f01667a34d0602bf5bf5365a0dd2b969abed, unchanged during this work.

Exact research/test commands, run from the repository root:

```bash
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_static_background.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_static_background_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_initial_response.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_initial_response_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_static_background.py --require-causal-principal-response
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_initial_response.py --require-local-initial-curvature
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_static_background.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_initial_response.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_static_background_manifest.json
git status --short
git log -5 --oneline
git rev-parse HEAD
git diff --check
```

Successful audits exit 0; both strict causal gates exit **2**, reporting the
failed physics requirement. The final regression run passes **62 tests**,
including the existing closure/source/Dirac/zero-mode tests in this audit
directory. This is not a run of every independent experiment in the repo.
The manifest records test-first failures and the corrected volume-factor bug.
Passing software tests validate the reproducibility of the adverse result,
not the theory's viability.
