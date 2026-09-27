# Independent review of the expansion/pressure reconstruction

Date: 2026-09-26. Science files were read only; this file is the review record.
**Verdict: conditional on the named field-equation and conservation inputs.**
No mathematical gap was found in the displayed inverse formulas once those
inputs and their stated domains are retained. The actual microscopic
field-to-stress interpretation is deliberately outside their conclusion.

Reviewed versions:

- `../reconstruction/RESULT.md`, SHA256
  `9c45f1da2c1ba47785211a24bbffe6124175cf6817a872bd941c588d8b94526e`
- `../reconstruction/check.py`, SHA256
  `9c10d252e6e73470aa023880d12c453f34cfae9b9f3218b2c261c3ab3f09157d`
- Development Lean source at review time, SHA256
  `944418e8b5fb6ac9fb878b0ffd29f2661987283f18d81a77502ef9212ead3127`;
  this version's second attempt was not accepted, as explained below.
- Final reconstruction report checked during synthesis review, SHA256
  `0289761bf2a9924306dd7ef9d7060deeb61e795f12232d18b0cb2141ee37a766`.
  The symbolic check source still has the hash above.

## Mathematical checks

1. With energy density and pressure both in J/m3,
   `a0^2=kappa^2 G_N epsilon` and `a0^2=kappa^2 G_N(-p)` have acceleration-squared
   units. Neither requires an additional c2; converting mass density does.

2. Separate conservation gives
   `(a^3 epsilon)'=3a^2 Pi`, `Pi=-p`, on the stated monotone expanding interval.
   Its integral contains a genuine density boundary constant. Constant
   positive Pi gives `epsilon=Pi0+D/a^3`, so a common pressure magnitude does
   not identify a unique energy density or equation of state. `D>=0` ensures
   positivity, and only `D=0` makes this family pure vacuum. The action still
   has to decide whether an integration constant is allowed clock data; the
   report does not infer a particle species from it.

3. The density-promotion inverse
   `w=-1-(2/3)d ln a0/d ln a` follows only for the stated constant couplings
   and conserved sector. Pressure promotion instead gives
   `d ln Pi/d ln a=(1/w)dw/d ln a-3(1+w)` and retains a boundary value.
   The report explicitly restricts this logarithmic pressure form to `w<0`
   and positive density; division through `w=0` is not claimed.

4. The curved Einstein-form effective stress has the correct factors and
   signs:
   `epsilon_tot=3c^2(H^2+K)/(8pi G_cosm)` and
   `p_tot=-c^2(2Hdot+3H^2+K)/(8pi G_cosm)`, with `K=k c^2/a^2`.
   Differentiation reproduces effective continuity for fixed `G_cosm`.
   Subtracting separately conserved dust leaves its pressure unchanged.
   In modified gravity this construction defines an effective stress unless
   the action independently identifies a material source; the report says so.

5. For flat space with negligible ordinary pressure,
   `Q=2Hdot+3H^2=3H^2-(1+z)d(H^2)/dz=H^2(1-2q_dec)` is correct.
   The pressure promotion implies
   `a0^2=kappa^2 c^2 Q/(8pi g)` and the normalized ratio equals one.
   The stated nonzero baseline and positive-Q domain matter. Constant g and
   kappa cancel algebraically; this does not cancel measurement covariance
   or distance-model dependence. The ordinary-pressure correction has the
   correct **plus** sign in
   `Pi_X=c^2(Q+K)/(8pi G_cosm)+p_ordinary`.

6. The pressure operator annihilates `D_H/a^3` in `H^2`. Its inverse therefore
   has exactly the stated free `C_H` term. Constant a0 leads to
   `H^2=B a0^2/3+D_H/a^3`; resemblance to a vacuum-plus-dust background does
   not identify a microscopic source. The code locally reuses `Pi0` for a
   constant a0-squared placeholder and explicitly comments on that change;
   the report uses the dimensionally unambiguous `a0^2` notation.

7. In the isolated spherical unfiltered algebraic controls, with
   `r=g_bar/g_obs` in `(0,1)` and `L=-ln(1-r)`, the two distinct inverses are
   `a0_RAR=g_bar/L^2` and `a0_AQUALexp=g_obs/L`. Their ratio is `L/r`.
   At fixed g_bar, differentiating r as `d r/d ln g_obs=-r` gives the reported
   condition numbers `2r/[(1-r)L]` and `1+r/[(1-r)L]`. Both tend to two in
   the deep limit and diverge near r=1. No positive finite inverse exists
   at r>=1. The report correctly does not apply these formulas pointwise
   to the operative filtered/gated nu_mono source problem.

8. The synthetic CPL history uses `w0=-0.8,wa=-0.4` consistently:
   `epsilon/epsilon0=a^0.6 exp[-1.2(a-1)]`. The normalized pressure promotion
   differs from the density promotion by `sqrt[-w(a)/0.8]` and satisfies the
   proposed ratio exactly. This is a chosen illustration, not observational
   evidence for either promotion; the report labels it correctly.

These checks do not require importing an external paper's equation as a
premise. The campaign's literature/source-check document is separate evidence;
this review does not claim to have independently authenticated its citations.

## Computation and Lean status

`../reconstruction/run1/manifest.json` passed the installed mathbox validator
with `--root`, including current input/result hashes. The implementation
checks exact symbolic identities and independent forward/inverse numerical
controls within declared domains; it contains no empirical data fit.

At the reviewed Lean hash, `lean_attempt2_record.json` has exit 1 and its log
contains `sorryAx` for the failed integrating-factor proof. The error comes
from a generated instance-equality goal in `convert hh using 1`, not from a
counterexample to the derivative identity. That attempt remains excluded
from accepted evidence, and its failed source/record are retained.

**Compiler resolution, 2026-09-26:** the final source SHA256 is
`70cb19253890254b06eb8bbe74f59bfeee3c816012cb45d0f2094b5202fe31f3`,
matching `../reconstruction/lean_attempt3_record.json`. The recorded command
is `lake env lean -j 1` on that source; exit code is 0 and elapsed time is
75.87397289276123 seconds. Direct inspection of `lean_attempt3.log` confirms
six declarations: the integrating-factor derivative, constant-pressure dust
family, fixing its constant by one density boundary value, pressure/density
identification cost, dust-pressure cancellation and normalized pressure null.
Their printed axioms are only `propext`, `Classical.choice` and `Quot.sound`.
There are three harmless linter warnings (two sequencing suggestions and an
unused variable), no errors and no `sorryAx`. This successful attempt is
accepted at the stated algebraic/differential scope; it does not formalize
the whole FLRW action, integral inversion or empirical reconstruction.

Checked record SHA256:
`90c869ee49a579e450e0c73eb4327a9d9488331f06c23eb5aee1f1120c70469e`.
Checked log SHA256:
`e7bd2ff223963995f261ccf0c08b6b47d51eeef3bdb84709e07fbc2f1bef5ac0`.

The reconstruction report's kernel and causality scope is current: it keeps
filtered nu_mono/criterion B operative and uses the unfiltered kernels only
as explicit controls. No recipe or science source was edited by this review.
The subsequent campaign README and CD26-3 recipe amendment are independently
reviewed in [SYNTHESIS_REVIEW.md](SYNTHESIS_REVIEW.md).
