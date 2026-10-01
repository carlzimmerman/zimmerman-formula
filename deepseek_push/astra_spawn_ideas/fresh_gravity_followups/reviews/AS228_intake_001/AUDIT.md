# AS228 independent scoped audit

Claim: the reported static weak-field MONO torus lapse and slip fields follow from independent variations of the pinned common action, including its metric-dependent gate/filter/projector, and the reported negative control validates the sourced slip channel.

**Primary verdict: refuted, with the smallest valid counterexample.** The implemented first variation is not the derivative of its own displayed gate density; its purported full four-curvature also fails a flat-spatial-metric lapse test. This refutes the implementation-to-action evidence implication. It does not prove the proposed action has no solutions or rule out physical slip. No AS228 action-derived slip or metric closure is promoted.

## Evidence ancestry and scope

Independent review by `/root/metric_intake`, 2026-09-30, of frozen AS228 intake; no source artifacts altered. Exact input hashes are in `audit_result.json`. The coordinator's INTAKE receipt records fourteen matching declared source/artifact hashes. The `framework_cell` prose embeds *different* action/spec hash strings from the verified `input_sha256` dictionary; this is an internal provenance inconsistency, not evidence that all checked source bytes failed. The frozen report remains unreviewed in its primary location. No upstream AS245 result or Lean theorem is accepted by inheritance.

The dependency graph is: pinned common action -> independent lapse/spatial Euler–Lagrange equations -> the proposed source formula -> a torus solution -> independent variation/control. Code instead starts with the proposed sources and constructs their Poisson solutions. The last independent-variation edge fails the controls below. The scope is finite, synthetic, static MONO; the two SI a0 footings are conversion roundtrips, not two full dynamics runs, and distinct vacuum/H(z) branches are not tested. No source mass/discrepancy or observational constraint is calculated in this audit.

## Decisive checks

1. **Gate chain rule fails.** `onshell_dLdeps` (lines 488–516 in the frozen script) defines `df` as the directional derivative of `f=G'`, then uses `df*dY`. For the displayed action the derivative is `f*dY`. The implementation is approximately `G''(Y)*(dY)^2`, which is not linear in the variation. On the active branch, normalize delta=1, choose Y=2 and dY=1. `G(Y)=Y-1/2`: its central directional difference is 1.0000000000287557; the code's term is zero. This is already a counterexample without a metric solve.

2. **Kernel chain rule is off by two.** The pinned definition is J=2 a0² q(|p|²/a0²), q'=nu−1. Thus δJ=2(nu−1) δ|p|², with δ|p|²=Aij pi pj+2p·δp. The integral used in `kernel_J`, 4a0²∫s(nu(s)−1)ds, agrees with this derivative. Line 486 instead uses 4(nu−1) δ|p|². The correct vector derivative J_p=4(nu−1)p in FINAL_ACTION is consistent with the factor 2 scalar derivative and does not justify the code factor 4.

3. **Four-curvature fails on flat spatial metric.** For ds²=−N(x)²dt²+dx²+dy²+dz², direct Christoffel contraction gives Γ⁰₀i=N_i/N, Γⁱ₀₀=N N_i, R00=N ΔN, Rij=−N_ij/N, hence R=−2ΔN/N. `ricci_scalar4_static` constructs `Gam0=N*grad(Phi)` where Phi=(N²−1)/2, adding an extra N, and its Rij loop includes only spatial Christoffels. With N=1+epsilon cos(kx), epsilon=1e−4, grid Ngrid=L=16 (so the grid-spacing issue below is absent), at x=0 the correct R is 3.0839429810423195e−5. The extracted code returns 1.5421256876927346e−5, ratio 0.5000500000073033. Its continuum formula at this point is epsilon k²=1.542125687670212e−5. The reference asserted in the report is itself incorrect. No appeal to an omitted traceless metric component fixes this test with exactly flat h.

4. **The refinement changes the differential operator.** Coordinates are spaced L/N, but `Torus3.__init__` uses `fftfreq(N,d=1.0)`. A fundamental sine has derivative amplitude 2pi/N rather than 2pi/L. A 16³, L=8 isolated check gives 0.3926990816987247 instead of 0.7853981633974483. The original L=16,N=48 cell has derivative scale 1/3 of its stated coordinate derivative; N=72 has scale 2/9. The heat filter likewise changes its physical smoothing length. The reported factor 2.26 change in slip amplitude cannot be interpreted as a fixed-domain convergence test or attributed exclusively to gate threshold sampling.

5. **Substitution checks solve their own asserted equations and remove the mean.** `solve_fields` sets Phi=P(4piG rho+src), Psi=P(4piG rho+src+4piG rho_slip), with P the implemented mean-subtracting inverse. Necessarily ΔP(s)=s−mean(s). Thus R_lapse=−4piG mean(rho), and R_slip=−4piG mean(rho_slip), modulo discretization/roundoff. These constants are compatibility projections, not independently derived action residuals. A tiny check with s=2+cos returns residual from −2.0000000000000027 to −1.999999999999997. The projected torus equations can be valid surrogate equations; unprojected equations with positive net rho cannot hold on the torus. Residuals divided by potential amplitudes also do not provide dimensionless equation errors without a specified length scale.

6. **The stationarity statistic is not an Euler–Lagrange residual.** The code returns pointwise δ(sqrt(−g)R) under a spatially varying strain and takes its RMS/max before spatial integration or integration by parts. This density can include total divergences even on shell. For compact torus stationarity the test is the integrated first variation (or an independently derived EL residual contracted with arbitrary test strains). Consequently the quoted 0.19 cannot presently be identified as gauge content, a missing traceless mode, or physical failure of the action. Incorrect curvature and gate derivatives make that interpretation still less justified. Subtracting two nonstationary, incorrectly differentiated densities and comparing with FD epsilon noise does not cure these defects.

Additional failures: differentiating Δu_b=s at fixed s gives δu_b=−P(δΔ u_b) on nonzero modes (and the mean projection/normalization must also be treated); the code takes the positive sign. The response evaluates the filter on u_b, although the solved U differs from u_b for ell nonzero. The report's f=0 zero-limit assertion is not algebraically general: g2−g4 at f=G=0 is c_N ell(2 gradPhi·gradW+ΔW), not identically zero. Its numerical `gate_idle` has f_max=1, so it is not a gate-everywhere-inactive control. These observations do not require importing any new mechanism.

## Obligation matrix and strongest safe statement

| Obligation | Status |
|---|---|
| Frozen artifact hashes versus declared dictionary | Passed for coordinator's fourteen checks; prose-hash inconsistency preserved |
| MONO Poisson construction using asserted slip source | Computational construction only; mean projection explicit |
| Independent variation of pinned common action | Failed: gate/kernel/curvature controls |
| Fixed-domain refinement | Failed: FFT spacing |
| Negative control as a test of action stationarity | Failed: derivative defects and density-versus-action statistic |
| Universal force/lensing conclusion or observed evidence | Not addressed |

The strongest safe statement is that the script constructs a finite surrogate MONO-dependent pair of projected torus Poisson fields with nonzero difference and a coupling-dependent source. Its saved numbers are not accepted as predictions of the pinned action. Failure of this run is not failure of the user's entire framework.

## Reproducible computation record

Only four inspected definitions (`Torus3`, `gate_f`, `gate_G`, `ricci_scalar4_static`) were extracted through Python AST and executed in an isolated namespace with numpy, DELTA_GATE=1 and B_HEAT=0.125. No module import, global initialization, worker, subprocess, external command, or primary file write was executed. The four 16³ controls completed in about 0.20 s. These are finite binary64 counterchecks corroborating the explicit algebra, not comprehensive validation. The reproduction code and outputs are recorded in `audit_result.json`.

## Specific executable child target (proposal only)

A **variational-foundation repair audit**, before any full ten-component solve: define one fixed L periodic grid; validate the sine derivative at N=16,32 using d=L/N; validate flat-h and flat-lapse curvature reductions independently from Christoffels; compare integrated G(J+ellΔW−theta) directional differences with independently coded analytic first variations for active, transition, inactive gates and signed strains. Require signed-linearity and convergence with epsilon; include mandatory mutants `df*dY`, doubled δJ, wrong inverse-response sign and old spacing, each of which must fail. Then derive the projected scalar metric equations from this corrected action and compare them with the proposed g1+g2−g4 formula. Pin all input bytes and record residual normalization and zero-mode constraints. This is distinct from AS228.c1 (a ten-component solve assuming the current variation harness) and should be prerequisite to interpreting its 0.19 statistic. It is not dispatched by this review.

## Reproduction listing and observed output

Environment: Python 3.9.6, numpy 1.26.2, executable `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`. The following was executed with `python3 -c` (20-second outer timeout); exit 0. This ad hoc review has no experiment-runner manifest.

```python
import ast, numpy as np
from pathlib import Path
p=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/AS228_intake_001/as228_slip.py')
t=ast.parse(p.read_text())
names={'Torus3','gate_f','gate_G','ricci_scalar4_static'}
body=[n for n in t.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
assert len(body)==4
s={'np':np,'DELTA_GATE':1.,'B_HEAT':.125}
exec(compile(ast.Module(body=body,type_ignores=[]),'<reviewed definitions>','exec'),s)
T=s['Torus3'](16,8.); f=np.sin(2*np.pi*T.X/8)
print('Fourier amplitude',np.max(T.D(0,f)), 'expected',2*np.pi/8)
rhs=2+np.cos(2*np.pi*T.X/8); r=T.lap(T.poisson(rhs))-rhs
print('Projection residual',r.min(),r.max())
Y=np.array([2.]); dy=np.array([1.]); e=1e-6
print('Gate true FD',(s['gate_G'](Y+e*dy)-s['gate_G'](Y-e*dy))/(2*e))
print('Gate implemented',(s['gate_f'](Y+e*dy)-s['gate_f'](Y-e*dy))/(2*e)*dy)
T=s['Torus3'](16,16.); e=1e-4; k=2*np.pi/16; N=1+e*np.cos(k*T.X)
R=s['ricci_scalar4_static'](T,(N*N-1)/2,np.zeros_like(N))
print('Curvature at x0',R[0,0,0],'expected',2*e*k*k/(1+e))

```

```text
Fourier amplitude 0.3926990816987247 expected 0.7853981633974483
Projection residual -2.0000000000000027 -1.999999999999997
Gate true FD [1.]
Gate implemented [0.]
Curvature at x0 1.5421256876927346e-05 expected 3.0839429810423195e-05
```
