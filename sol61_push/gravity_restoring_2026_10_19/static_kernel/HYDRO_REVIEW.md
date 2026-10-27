# Independent focused review of the one-fluid limit

Target: `../collective_response/HYDRODYNAMIC_LIMIT.md`, SHA-256
`9ea6fa9dc4bb05ee8a41f9ff29d69b8a786ea67ac01147967f864085379bb8a6`.
19 October 2026. Reviewer: root coordinator, a different derivation from
the author's, with shared research context. This is an in-session focused
proof review, not an external referee report or a blind review.

**Claim:** at a fixed positive-density, finite-chemical-potential state of
a homogeneous local zero-temperature one-current fluid, with stable sound
`0<cs²<=1`, the physical acoustic energy susceptibility tends to
`(epsilon+p)/cs²`, not zero as `k²`. Its inverse therefore cannot be a
positive `K_g/k²` static material kernel. **Verdict: proved as written**
within those explicitly named fluid and source assumptions.

Independent reconstruction uses `epsilon'(n)=mu`,
`P(mu)=mu n-epsilon`, `kappa=P''=dn/dmu`, hence
`dp/dn=n/kappa` and `cs²=n/(mu kappa)`. Thus `w=mu n`,
`mu²kappa=w/cs²`. This uses the exact equation of state, with no mean-field
coefficient substituted. The causal sound bound gives `mu²kappa>=w>0`.
Finite `n,mu` and a fixed state are essential; the vacuum and a state varying
with the probe momentum are not counterexamples to the normalized claim.

The lapse calculation was reconstructed independently. In
`N P(sqrt[(mu+pidot)²/N²-|grad pi|²])`, with `N=1+Phi`, expand the argument:

\[
 X=\mu+\dot\pi-\mu\Phi+\mu\Phi^2
 -\dot\pi\Phi-{|\nabla\pi|^2\over2\mu}+O(3).
\]

Multiplying by `N` cancels both extra terms proportional to
`n mu Phi²` and `n Phi pidot`. The result is

\[
 L=P-\varepsilon\Phi+n\dot\pi
 +\frac\kappa2(\dot\pi-\mu\Phi)^2
 -\frac n{2\mu}|\nabla\pi|^2+O(3).
\]

The explicit metric contact and phase exchange yield
`chi_EE=w k²/[cs²k²-(omega+i0)²]`. This checks the response sign, source
normalization and order of limits independently of the author's Euler
derivation. At static nonzero momentum the contact survives; at fixed
nonzero frequency the conserved-density response is `O(k²)`.

I separately checked the three operators. A source coupled to number has
`chi_NN=kappa`. A source coupled to reference density `rho0=m n` has
self-response `m²kappa`. An actual lapse has cross-response
`chi_rho0,E=m mu kappa` and energy self-response `mu²kappa`. Inverting the
cross-response would not give the reference-density self-energy. The note
keeps these quantities distinct and uses the full chemical potential,
rather than only a rotating-frame detuning.

The spectral check also passes: the acoustic residue is proportional to
`k²`, so its equal-time weight is proportional to `k`, while its static
susceptibility has the additional inverse phonon energy and tends to a
nonzero constant. Equal-time hyperuniformity does not supply the asserted
static incompressibility. A gapped signed/optical charge can be a different
projection from positive acoustic energy; the proof does not identify them.

| Obligation | Review outcome |
|---|---|
| Exact EOS and sound identities | Passed by differentiation |
| Complete lapse measure/contact terms | Passed by independent expansion |
| Reference versus energy source dictionary | Passed |
| Retarded/static order of limits | Passed at leading controlled hydrodynamic order |
| Fixed-state positive lower bound | Passed conditional on the stated causal-fluid hypotheses |
| Original neutral bath reaches that fluid | Not established and not claimed |
| All phases, finite temperature, solids, full metric constraints | Outside scope |

No scientific numerical run was required. The primary Son attribution was
not independently re-authenticated by this reviewer; the internal pressure,
thermodynamic and source algebra suffices for the conditional claim, while
the author's exact-version source record remains separately identified.
This theorem narrows a named loophole and does not certify a microscopic
gravitational law or exclude every nonlocal/inhomogeneous phase.
