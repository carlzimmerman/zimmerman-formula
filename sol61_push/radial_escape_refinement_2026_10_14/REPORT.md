# Radial escape refinement through 320 shell modes

The previous forty-mode calculation did not resolve the radial escape sum,
especially for the small cavity. This extends the SAME conditional mechanical
and particle model to 320 radial modes for each geometry. It does not add new
physical evidence or new interactions. It is a convergence investigation of a
specific outstanding loss contribution.

## Scope and verification changes

The two shells remain a/b=0.2/2.2 m and 0.02/0.52 m. All couplings, assigned
elastic constants, temperature, initial reference orbitals and continuum energy
normalization are unchanged from ../radial_phonon_escape_2026_10_14/REPORT.md.
The elastic root scan extends to kb=1200, with independent spacings 0.08 and 0.04.
Both identify the same first 320 positive roots to the recorded tolerance.
Neither scan is a certified complete root enumeration.

Gauss integration is increased to 1536 and 3072 points. Nodes are cached for
reuse. Every retained elastic mode is checked using its Rayleigh quotient,
free-surface stress and bulk-plus-surface coupling identity. Every open
particle transition is checked using interface matching, quadrature refinement,
and agreement of the two forms of the perturbation matrix element. The low-mode
mass orthogonality checks are retained. The first forty escape contributions are
also compared against the independently recorded predecessor results.

## Results: still small, but the forty-mode result needed correction

| Candidate | 40 modes, /s | 80 modes, /s | 160 modes, /s | 320 modes, /s |
|---|---:|---:|---:|---:|
| Large | 3.65684e-28 | 3.78931e-28 | 4.45156e-28 | 4.47371e-28 |
| Small | 1.61076e-23 | 1.81081e-23 | 1.83609e-23 | 1.83713e-23 |

The final partial rate is about 22.3% above the forty-mode large-cavity result,
and about 14.1% above the forty-mode small-cavity result. The 160-to-320 additions
are about 0.50% and 0.056%, respectively. These are observed partial-sum changes,
not mathematical remainder bounds. In particular, the earlier small increase
between forty and eighty LARGE-cavity modes would have underestimated the
subsequent contribution. No asymptotic extrapolation is used to replace omitted
modes by a claimed total.

The large-cavity absorption contribution remains the whole resolved rate, since
emission is energetically closed. The seven open small-cavity emission channels
sum to 4.79039e-36/s and are negligible within this conditional calculation.
The resolved 320-mode rates divided by the assigned drive frequencies are
2.33538e-22 and 1.14126e-17; divided by tunneling rates they are 2.39630e-22 and
1.32301e-16. These ratios do not bound other loss mechanisms.

## What this settles, and what it does not

The numerical radial loss estimate is more stable under increasing the retained
mode count, and still very small in the specified model. This supports continuing
the theoretical candidate instead of rejecting it because of these computed
radial channels. It does not establish a physical storage lifetime.

The angular selection rule that limited diagonal phase noise to l=0 does not
limit inelastic loss: a mechanical multipole can excite the corresponding final
particle partial wave. All nonradial mechanical modes are absent here. Also
absent are a certified high-frequency tail bound, finite phonon linewidth
integration, supports, structural damping, defects and a measured material
response. The initial state remains an approximation to a narrow finite-shell
resonance. The proposed optical field and its detection are not validated by
this mode refinement.

The next discriminating calculation should address the angularly allowed loss
channels, rather than claim an all-mode result from this radial calculation.
The broader creation objective, especially identification with the repo's
cosmological cold component, remains open.

The bounded run stores both modes.json and results.json, along with hashes,
resource caps, versions and logs. The explicit check counts and predecessor
comparisons are in those files. No new Lean certification is claimed.
