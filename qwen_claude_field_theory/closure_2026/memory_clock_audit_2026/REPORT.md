# Timelike memory clock audit — 2026-09-09

## Claim tested

The causal-memory route can use a timelike mimetic clock as a **non-propagating
auxiliary** while retaining the nonzero FLRW dust density needed by the route.

The calculation audits the explicit multiplier action

\[
 S_c=-\frac12\int d^4x\sqrt{-g}\,\lambda
       (g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi+1)
\]

on a flat-FLRW Fourier mode.  It is a reduced clock-sector calculation; it is
not presented as the full gravity-plus-clock functional constraint algebra.

## Reproduction

```text
python3 qwen_claude_field_theory/closure_2026/memory_clock_audit_2026/mimetic_clock_dirac.py
```

Exit status: **0**.  The script writes
`mimetic_clock_dirac_results.json` beside itself.

## Action-derived Dirac result

With \(A=a^3\) and \(K=1+k^2\phi^2/a^2\),

\[
 L_c=\frac{A\lambda}{2}\left(\frac{\dot\phi^2}{N}-NK\right),
 \qquad p_\phi=\frac{A\lambda\dot\phi}{N},
 \qquad p_\lambda\simeq0.
\]

The secondary constraint obtained by preserving \(p_\lambda\) is

\[
 C_2=\frac{A K}{2}-\frac{p_\phi^2}{2A\lambda^2}\simeq0.
\]

The computed constraint matrix on \((C_1,C_2)=(p_\lambda,C_2)\) is

\[
 \{C_A,C_B\}=\begin{pmatrix}
 0&-p_\phi^2/(A\lambda^3)\\
 p_\phi^2/(A\lambda^3)&0
 \end{pmatrix}.
\]

It has computed generic rank 2 in both sectors:

| sector | computed rank | reduced phase dimension | reduced clock configuration DOF |
|---|---:|---:|---:|
| \(k=0\) | 2 | 2 | 1 |
| \(k\ne0\) | 2 | 2 | 1 |

Preservation of \(C_2\) fixes the primary multiplier through the nonzero
\(\{C_2,C_1\}=p_\phi^2/(A\lambda^3)\); it does not generate a new independent
constraint on the generic branch.  The zero-density locus \(\lambda=0\) is
rank-degenerate and cannot represent the dust branch used by the memory
proposal.

## FLRW consequence

The homogeneous equations give

\[
 \frac{\dot\phi}{N}=1,\qquad
 \rho_c=\lambda,\qquad p_c=0,
 \qquad a^3\lambda=\text{constant}.
\]

Thus an expanding solution with \(H\ne0\) can carry \(\rho_c\propto a^{-3}),
but exactly that nonzero density is the branch on which the reduced clock has
one remaining canonical configuration DOF.  Its background adiabatic sound
speed is \(c_s^2=dp_c/d\rho_c=0\), so the scalar is dust-like rather than a
strictly auxiliary algebraic variable.  This is a warning about zero-gradient
strong coupling, not a claim of a ghost.

## Preferred-frame pricing

The mimetic multiplier has no Einstein-aether \(c_i\) kinetic block, so an
exact standard PPN \(\alpha_1,\alpha_2\) value does **not** follow from the
clock constraint alone.  As a contrast, the script symbolically specializes
the standard Einstein-aether expressions to \(c_{13}=0,c_4=0\):

\[
 \alpha_1=-4c_1,
 \qquad
 \alpha_2=-\frac{c_1(2c_1c_2+c_1-c_2)}{c_2(c_1-2)},
 \qquad
 \alpha_2=0\Longleftrightarrow c_2=\frac{c_1}{1-2c_1}.
\]

For the illustrative \(c_1=10^{-5},c_2=0.1\), the computed values are
\(\alpha_1=-4.0\times10^{-5}\) and
\(\alpha_2=-4.9994\times10^{-6}\).  These numbers apply only after adding a
dynamical aether/khronon kinetic sector; they are **not** a certification of
the mimetic memory model.  Adding that sector reintroduces its own scalar mode
and requires a separate full PPN/Dirac audit.

## Relation to L65

`fable_independent_2026/L65_memory_kernel.py` was rerun (exit 0; 28 PASS and
9 explicitly marked gate FAIL).  Its causal doubled-field construction is
variational, but its hidden response/bath data are not removed by the
retarded-state prescription.  This audit closes a narrower attempted escape:
the mimetic clock can avoid an aether kinetic pole only by retaining a
dust-like scalar canonical pair on the nonzero-density FLRW branch.

## Safe verdict

**The nonzero-density mimetic-clock localization is not a zero-DOF auxiliary
in the audited action.** The causal memory route therefore remains **OPEN as
a global program**, but this proposed no-hidden-clock implementation is
**not a pass**.  A full covariant gravity-plus-clock Dirac algebra and a
boosted PPN solve remain necessary before any universal no-go statement.
