# Independent proof audit — 2026-10-28

**Normalized claim.** For positive `a0,G,r0,r`, a spherical Burkert halo with `rho0*r0=a0/(2*pi*G)` cannot supply the simple-mu law's required acceleration excess when `gN/a0` exceeds the stated cap-inversion threshold. Separately, a spherical isolated simple-mu model has the displayed circular-speed-to-enclosed-baryonic-mass inverse, conditional on the adopted IC 1613 inputs.

**Primary verdict: proved as written**, for those mathematical necessary conditions under their displayed hypotheses. No proof error requiring correction was found. The sharp decimal threshold is an ordinary numerical evaluation of an exact implicit bound, not a certified decimal enclosure. The fully analytic weaker exclusion at `gN/a0>=1/6` needs no numerical root. The IC 1613 interpretation remains conditional on the named source model and the transferred half-mass convention; it is not an empirical significance calculation or a universal gravity exclusion.

Reviewer: delegated foundations reviewer, separate from the author of `RESULT.md`. The raw density, law and equations were reconstructed rather than inferred from the output's pass flags. The author supplied the proof and program and asked for adversarial review; this was not a blind audit. No original source or result was changed. Agent independence is provenance, not proof.

## Exact revision reviewed

Repository requested base: `44fd23a71c9888d9ea204c0ee832805829f9c090`; the audited proof is new workspace content. FD1 evidence is later than that base. Exact content hashes at review:

| Artifact | SHA-256 |
|---|---|
| `RESULT.md` | `7b58bd3017ee311fc38c9d597925bdab6278ec7431dc3fc51b32d18983b7cd8a` |
| `check_conditions.py` | `8f620a61b14167a011e99414b9b038f604f4e42bb58e1fb8d919a12577fe5062` |
| `SOURCES.json` | `1c1ae93a2c934cb87f04d6c6932d29c75d09596214e0d6713c10c579ebaa832f` |
| `run/manifest.json` | `d9b732a4097bb95853523da327bcd14d0a45f928c28f46856ae15bc8a4c9c40d` |
| FD1 `fd1_field_dwarf_audit_results.json` | `95b52ca23d3919023d3b9f849e2d089fc0b3ce27b12f3a5184226a97881162ad` |

## 1. Burkert maximum: independent reconstruction

Set `D=(1+x)(1+x²)`. Starting from the density, the mass integral is

\[
M_h=4\pi\rho_0r_0^3\int_0^x\frac{t^2}{(1+t)(1+t^2)}\,dt.
\]

Differentiating the proposed `B` gives `B'=4*x²/D`, and `B(0)=0`, proving the mass normalization and `q=B/(2*x²)` exactly. The analytic `q<1/3` proof is correct: `x²/6-B/4` vanishes at zero and has strictly positive derivative `x*((1-x)²+x³)/(3*D)` for every `x>0`.

For the maximum, `q'=H/(2*x³)` with `H=x*B'-2*B`. Independent differentiation gives

\[
H'=\frac{4x^2(1-x^2-2x^3)}{D^2}.
\]

The polynomial `p(x)=1-x²-2*x³` has derivative `-2*x-6*x²<0` on the whole domain, with `p(0)=1` and `p(infinity)=-infinity`. It has exactly one positive zero `x_c`. Since `H(0)=0`, `H` is strictly positive through its increasing segment and reaches a positive maximum at `x_c`. For large `x`, `B=4*log(x)-pi+o(1)` and `x*B'->4`, hence `H->-infinity`. It therefore has exactly one positive zero on its decreasing segment. Thus `q` has exactly one global maximum, without a numerical-grid assumption. Both endpoint values of `q` are zero.

This supplies the small omitted asymptotic details in the author's argument; it does not change its premises or conclusion. The root bracket and numerical value agree with the correct analytic object. The program's finite grid is appropriately labelled a regression only.

## 2. Cap inversion and scope

Writing the required extra acceleration as `h=(sqrt(y²+4*y)-y)/2`, the defining identity is

\[
h^2+yh-y=0,\qquad y=\frac{h^2}{1-h},\quad 0<h<1.
\]

The inverse increases strictly, since its derivative is `h*(2-h)/(1-h)²>0`. Consequently `h<=qmax` implies `y<=qmax²/(1-qmax)`. In particular, `h(1/6)=1/3`, whereas the halo has the strict bound `q<1/3`; the analytic exclusion correctly includes equality `y=1/6`.

The equality at the numerical threshold would require the halo to be evaluated precisely at its acceleration maximum. Thus the result is a necessary pointwise condition; satisfying it does not establish an all-radius profile match. The proof fixes the baryonic field. Refitting stellar mass is outside this theorem, as the author states.

The restriction to a halo **exactly on** the floor is crucial: `Sigma=max(Sigma_floor,eta*Sigma_coll)` is not globally bounded above by `Sigma_floor`. The author's exclusion of above-floor halos and additional force components is therefore necessary and correct.

Optional strengthening: if the baryonic and spherical-halo vectors are not parallel, the triangle inequality still gives `|g_b+g_h|<=gN+gh`. The same magnitude cap is therefore a necessary condition even without alignment. The current alignment restriction is conservative and does not make the statement false. Changing the full gravity theory or halo shape is a different matter and remains outside scope.

## 3. IC 1613 inversion and the input rectangle

Starting directly with `g=v²/r`, the spherical simple-mu law yields `gN=g²/(g+a0)` and `M_b=gN*r²/G`, hence

\[
M_b(v,r)=\frac{v^4r}{G(a_0r+v^2)}.
\]

The dimensions are mass. There is no extra factor of radius missing. The program's calculation and the report's alternative expression are algebraically identical.

The stated rectangle's extrema really do lie at its corners:

\[
\partial_rM_b=\frac{v^6}{G(a_0r+v^2)^2}>0,
\qquad
\partial_vM_b=\frac{2rv^3(2a_0r+v^2)}{G(a_0r+v^2)^2}>0.
\]

Independent evaluation of the direct `v^4` formula gives `3,922,434.2803` and `3,266,813.3745` solar masses at `v=15 km/s,r=2 kpc`, matching the recorded numbers. The stars-only lower circular speeds use the correct monotonic simple-law map. Positive enclosed gas increases that acceleration under the same isolated spherical assumptions.

The FD1 “M only” row actually contains `logMb=7.848151250383644` and `used=['M']`; halving its mass gives `35,246,926.6482` solar masses, as reported. This is a conditional carried-over stellar-mass convention, not a source-verified radial stellar-mass profile at the new radius. The report states that restriction and does not substitute the new radius into the frozen FD1 grade.

The exact-version [Taibi et al. v2 primary text](https://arxiv.org/html/2402.01631v2) was checked independently: Table 1 gives `Re=1.50±0.02 kpc`; section 6.2 gives `vcirc(rhalf)=15±2 km/s` and inclination `32±11 degrees`. The source derives these using asymmetric-drift and tracer assumptions, takes `rhalf≈(4/3)Re`, and calls for a future joint dynamical study. The report's conditional use is faithful. Its error rectangle is correctly distinguished from a joint confidence region; correlations and systematics are not propagated here.

## 4. Dependency and obligation matrix

Density + spherical Newtonian gravity → mass normalization → shape `q` → unique global maximum → simple-law excess inverse → pointwise necessary threshold.

Source's model-dependent `v,r` + isolated spherical simple-mu assumption → enclosed baryonic mass requirement. FD1 half-mass transfer → conditional stars-only minimum speed. There is no arrow from these alone to an empirical significance or a universal falsification.

| Obligation | Finding |
|---|---|
| Mass integration and `2*pi` normalization | **Passed**, from density |
| Formula for `H'` | **Passed**, independent differentiation |
| Unique maximum and endpoints | **Passed**, sign proof and asymptotics |
| Inverse threshold and strict conservative endpoint | **Passed**, monotonic inverse |
| Sharp decimal root as rigorous decimal enclosure | **Not claimed**; ordinary floating-point estimate |
| IC mass inversion and physical dimensions | **Passed**, direct reconstruction |
| Rectangle covers its declared input domain | **Passed**, positive partial derivatives |
| Published source numbers and modelling qualifications | **Passed**, exact-version primary text |
| Same stellar mass within revised radius | **Conditional**, explicitly retained FD1 convention |
| Universal observational theory exclusion | **Out of scope**, correctly disclaimed |

## 5. Computation checks and residual gaps

The script was inspected without importing its pipeline. Its X43 AST extraction includes only the pure `B` function, and the density quadrature is independently defined. The eight advertised checks are present. The small-`x` formula has cancellation, but the lowest tested value is `0.01` and the recorded density-integral discrepancy is safely below the declared tolerance; no limiting proof depends on it.

Independent short SymPy calculations returned zero residuals for `B'`, `H'`, and the conservative-bound derivative, returned `H(infinity)=-infinity`, and recovered the positive mass derivatives above. Direct SI arithmetic independently reproduced the two required masses. These are supplementary checks on the handwritten derivations, not stand-alone empirical evidence. The full author script was not rerun in this audit.

`validate_manifest.py .../necessary_conditions/run/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula` returned **valid evidence record, run status completed**. This verifies stored provenance, not the theorem by itself.

**Remaining implication:** a common radial baryon/tracer model and the candidate theory's actual field equation must map the published kinematics into a gravity test. The report does not yet supply that map and does not claim to. The strongest safe result is the exact floor-to-simple-law obstruction plus the conditional IC 1613 mass target. The cheapest discriminating next check is resolved enclosed stellar/gas mass with a common inclination and asymmetric-drift model, not another manipulation of the aggregate dispersion estimator.
