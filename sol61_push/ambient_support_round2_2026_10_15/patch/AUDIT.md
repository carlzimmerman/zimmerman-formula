# Independent algebra audit of the occupied-phase magnetic patch

AS2-PATCH-AUDIT-001, 15 October 2026. Read-only audit of the pinned proof and
code; this file is the only audit edit. The cone algebra and regularity limits
were reconstructed from the proposed definition before reading the completed
proof. A separate read-only algebra subagent also checked the occupied-center
and joint-vacuum limits. This is not an independent audit of the whole theory.

**Normalized claim and primary verdict: proved as written**, with the proof's
explicit conditional occupied-phase and hybrid-gravity scope. The new response
preserves the single-neutral-current all-angle principal cone and positive
quadratic-energy conditions on `h>hcrit`, repairs the magnetic coefficient at
the occupied electric origin, and leaves the pure-electric background first
variation unchanged. It does not repair the joint vacuum limit, establish
magnetic-background health or prove nonlinear evolution. This is a new
constitutive postulate; it is not the unchanged canonical action.

## 1. Exact object and hypotheses

Let `D0>0`, `E=|E_U|`, `t=(1+E/D0)^-1`, `p=t^2`, `x=1-t`, and
`h=h_s(1-s_s^2)>0`, with the inherited material assumptions
`h_s>0`, `0<=s_s^2<1`. The current remains timelike at positive density;
the EOS and `h` are smooth there. The scalar `h` in the cone denominator is
the **effective** inertia, not bare material enthalpy. The background has
`B_U=0`. The frame is varied with the sole neutral current.

Keep `hcrit=E^2 x`, the parent response on the strict gate, the scale
`a^2=D0^2 h/[16(D0^2+h)]`, and the proof's smooth cutoff with `0<=chi<=1`.
The direct definition `beta_new=1/4` on `E^2<=a^2/4` avoids evaluating an
undefined parent expression at `E=0`. These hypotheses are all present in
the audited proof; none needs to be added to it.

## 2. Cone bounds reconstructed directly

On `chi>0`, `E<a`, so

\[
 \frac{E^2}{D_0^2}<\frac{h}{16(D_0^2+h)}<\frac1{16},\qquad
 \frac{E^2}h<\frac{D_0^2}{16(D_0^2+h)}<\frac1{16}.
\]

Consequently `E/D0<=1/4`, `x<=1/5`, `t>=4/5`, `p>=16/25`, and
`hcrit/h<=1/80`. Thus every nonzero-field blend point lies well inside the
parent gate. For the quarter response, `0<t-1/4<1` and the denominator is
at least `h`, giving exactly the stated conservative bound

\[
 f(1/4)=p-\frac14-
 \frac{E^2(t-1/4)^2}{h+E^2(t-1/4)}
 \ge\frac{16}{25}-\frac14-\frac1{16}
 =\frac{131}{400}>0.
\]

Multiplication by the positive denominator gives

\[
 [h+E^2(t-\beta)]f(\beta)
 =h(p-\beta)-E^2(t-\beta)(t-p)=:N(\beta).
\]

The cancellation of both quadratic beta terms is exact. `N` is affine in
`beta`, so

\[
 N(\chi/4+(1-\chi)\beta_P)
 =\chi N(1/4)+(1-\chi)N(\beta_P)>0.
\]

Both endpoints are positive and below `t`, so the same is true of their convex
blend and its denominator. At `chi=0` the parent theorem applies. These facts
supply precisely the old single-current light-cone Schur discriminator and
kinetic assumptions; no angle sampling or frozen-fluid substitution is used.

At exact `E=0`, the electric Hessian is the identity, frame boost mixing is
zero, and the magnetic coefficient is `1/4`. The two transverse gauge speeds
are `1/2` in metric-light-speed units; the fluid sound remains below one and
its vorticity/label zero modes remain. This direct calculation covers the
point at which the parent field-direction notation is undefined.

## 3. Occupied regularity and the sharp limiting obstruction

For every occupied density `n0>0`, continuity and positivity of `a(n)^2`
give a neighborhood of `n0` with a positive lower bound on `a^2`. A sufficiently
small electric-vector ball then has `chi=1` for **all** densities in that
neighborhood. Hence `beta_new=1/4` there jointly in the electric Cartesian
components and density. This repairs nearby states with `E_U=0,B_U!=0` as
well as the exact background point. Away from zero, the electric norm is
smooth and the parent denominators are nonzero on the gate. The cutoff is
smooth and flat at both joins. The magnetic coefficient is therefore smooth
on the occupied gate domain.

The unchanged electric function is

\[
 L_e(\mathbf E)=\tfrac12|\mathbf E|^2
 -\frac{|\mathbf E|^3}{3D_0}+O(|\mathbf E|^4).
\]

It is `C2` with locally Lipschitz Hessian, but not `C3`: on a signed Cartesian
line its cubic term has opposite one-sided third derivatives. With a smooth
occupied current frame, the patched action consequently has a `C2` local
neighborhood at the center; no smoother total action or classical PDE theorem
follows. The original magnetic `|E_U| B_U^2` obstruction is removed there.

The proof's joint-vacuum counterlimit is correct. As `h->0`, along `E=0`
the coefficient stays `1/4`. Along `E=a(h)`, the cutoff is zero and
`hcrit/h=(E^2/h)x->0`, so the parent coefficient tends to one. Both paths
lie in the occupied gate. Thus no continuous joint coefficient extension to
`(h,E)=(0,0)` exists for this patch. This is an actual failure of continuity,
not a missing proof of a limit. The material frame is also undefined at zero
current. The shrinking tail domain and outgoing-radiation obstruction remain.

## 4. Static variation and the joint quadratic energy

At any occupied `B_U=0` point,

\[
 \delta[-\tfrac12\beta_{\rm new}B_U^2]
 =-\tfrac12(\delta\beta_{\rm new})B_U^2
 -\beta_{\rm new}B_U\!\cdot\delta B_U=0.
\]

This includes density, current-frame and metric variations; the volume-element
variation also multiplies a zero background term. The electric action and its
projected first frame variation are unchanged. The pure-electric neutral
Euler equation, static electric Gauss law, background stress and regular-core
fluid equilibrium are therefore unchanged by this magnetic replacement.

At quadratic order, `B_U=O(delta)` and the smooth coefficient variation is
`O(delta)`, so its density/electric derivatives multiply `B_U^2` only at cubic
order. The joint audit's pointwise matrices remain

\[
 M=h_sI+(t-\beta_{\rm new})(\bar E^2I-\bar E\bar E^T),\qquad
 Qb=(t-\beta_{\rm new})(b\times\bar E),
\]

with the same electric Hessian and the same fluid density Hessian. The
constrained Hamiltonian retains its positive-square structure with this new
`M,Q,beta`; spatial coefficient derivatives still enter conservative curls
and the documented flux terms, rather than a new indefinite bulk potential.
The historical parent report's statement `Delta=0` at the center is replaced
by `Delta=3/4` for this candidate. Since `bar E=0`, this still gives
`M=h_s I` and `Q=0` there. Its magnetic quadratic energy and gauge speed do
change; the repair is a substantive new magnetic response.

The positive all-space density-Hessian estimate for the regular core,
`0<f<1/4`, is independent of beta. Therefore the joint quadratic-energy
argument applies to the patch under the **same** fixed external sources,
lab-rest-density Newtonian gravitational truncation, mass/Gauss constraints,
regularity and flux hypotheses. It is not a full Einstein Hessian or a
nonlinear/radiation completion. No inference about health on a
nonzero magnetic background follows from this audit.

## 5. Evidence, provenance and obligations

| Obligation | Result |
|---|---|
| Quarter-response scale and strict cone margin | Passed analytically |
| Parent gate membership throughout blend | Passed; `hcrit/h<=1/80` |
| Convex blend preserves all-angle discriminator | Passed by affine numerator |
| Exact center principal modes | Passed by direct quadratic calculation |
| Smooth occupied magnetic coefficient | Passed locally jointly in field and positive density |
| Pure-electric static first variation | Passed, including current and metric variations |
| Existing joint quadratic-energy structure | Passed under its explicit hybrid-model hypotheses |
| Continuous joint vacuum coefficient | Refuted by two admitted paths |
| Full nonlinear or magnetic-background health | Not established |

The dependency graph is: inherited one-current principal matrices plus the
scale bounds -> safe quarter endpoint; inherited parent endpoint plus affine
numerator -> safe blend; local constant patch plus retained `L_e` -> occupied
`C2` action; magnetic first-variation cancellation plus cubic derivative count
-> unchanged equilibrium and applicable joint quadratic-energy structure.
No external theorem or literature source is a load-bearing leaf here.

The existing run reports 15 exact symbolic identities and 12 illustrative
blend controls. Source inspection confirms that the latter signs are checked
with `evalf(50)` at algebraic input points; they are numerical controls, not
12 exact sign proofs. The uniform analytic margin and affine argument above
do the proof work. No independent new simulation or symbolic run was executed.
The existing version-2 manifest validated against current bytes with:

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/ambient_support_round2_2026_10_15/patch/run_v1/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

| Audited artifact | SHA256 |
|---|---|
| `PROOF.md` | `ce86b05fdb111cd6c9603f826b4424590d41131907002b5564613985064f0b54` |
| `check_patch.py` | `2ac5c82ff2691d42ef9b0de47524b6468af44519a3d843837ef3b573bb3f4528` |
| `run_v1/manifest.json` | `c44f81642375e623b6613f6b6c1844d759a6d38021255a7365b509cc130b8577` |
| `../joint_audit/REPORT.md` | `4743893a336effd9a9de6c1ff3024f4af4631b8fa29803c95f0b5565fa4667f0` |
| `../action/PROOF.md` | `d62484e0a0285b63c7503bcfb57dbe3ffb6337184d52d714fdfc884cc8ea8ad3` |
| `../inputs/MC_MODES_PROOF.md` | `d46b9a2b8adeb7d2692b29d6ac8d8283dfe6054eb619cc9686aa33e747d2b2ac` |

No change to the pinned proof or code is required for the stated claim. The
strongest safe statement is a repaired occupied-center constitutive candidate
with positive local principal cones and the restricted joined quadratic energy.
The next missing physical implication is still a low-density/radiation and
gravitational completion with an identified carrier and counted sources.
