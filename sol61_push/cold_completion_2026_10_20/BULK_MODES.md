# Full common-action homogeneous modes

**Status: the corrected coexistence background passes this finite linear-mode check.** This is the explicit alternative three-field matter action in `common_action.py`, not the unchanged ARGON action. No merger, cooling flux, finite-fragment stability, galaxy profile, or full-theory completion is established here.

The completed evidence is `bulk_run_001/repaired_run/`, with 35 passing checks, 0.260 seconds runtime, and measured peak RSS 30,294,016 bytes. Both its manifest and the preserved failed first-launch manifest validate. The first launch failed on the Python token `else0.`; `bulk_modes.py`, `bulk_contract.json`, and that failed record remain unchanged. `bulk_run_001/corrected_source.py` repairs that whitespace and adjusts its base path for the nested placement; the matrix and declared thresholds are unchanged.

## Pinned input and scope

The background is the **corrected** `run_003/results.json`, produced by `liquid_phase_v2.py`; the failed old grand-potential calculation is not used. The parameters are read from `run_001/results.json`, and the action source is pinned without executing its stationary solver. Hashes are SHA-256:

| Input | Hash |
|---|---|
| `common_action.py` | `a700b211d45f339400feebab83db878dfa243cb99c26e22a2a249a2220e1e208` |
| `run_001/results.json` | `0f8fcb2cf8d3bfb057c213ff87abc1728257cca3e119c5d2c0905036ee2c9eac` |
| `liquid_phase_v2.py` | `527d3a3fa019b785e68d4c1bc45f55d555e3b564ab975303289656b72cc484de` |
| `run_003/results.json` | `eab33af45db4b068bd5cc64c92da136b6e8ca5013802aa00db01461ff88ef9af` |
| `bulk_run_001/corrected_source.py` | `d8242369750801b93250412f5e1b8b55527a478f0ce6e2eac1b5d9ef4a3768e8` |
| `bulk_run_001/repaired_run/results.json` | `ca86c840924d7bd3f2e1ce384569b2408fd24b0cc0f01acf457f0e3fd7c7ffb5` |

The execution manifest records repository commit `e7962101328fd7447eb2175829b6018adb22b85c` with a dirty worktree; the exact file hashes, rather than that commit alone, identify the tested action and background. No PDE, 3D evolution, live Claude experiment, frozen criterion, or publication was changed.

## Exact linearization and normalization

The complex fields have the usual kinetic normalization, the real field has kinetic coefficient one half, and

\[
 V=|\Psi|^2+M_X^2|X|^2+g(X^*\Psi^2+X\Psi^{*2})
   +\lambda|\Psi|^4+a\chi|\Psi|^2+U(\chi),
 \qquad U(h)=\frac{M^2h^2}{2}-\frac{Mh^3}{8}+\frac{h^4}{4}.
\]

Here \(M=100\), \(a=200\), \(g=0.002168\), \(M_X^2=4.0016\), and \(\lambda=1.99+g^2/M_X^2\). With \(I=f^2\), use

\[
 \Psi=e^{i\omega t}(f+u+iv),\qquad
 X=e^{2i\omega t}(b+s+it_X),\qquad \chi=h+\xi.
\]

The script calls the real imaginary-part perturbation \(t_X\) simply `t`; time derivatives below use a dot. The homogeneous equations are

\[
 1-\omega^2+2\lambda I+ah+2gb=0,\quad
 Db+gI=0,\quad U'(h)+aI=0,\quad D=M_X^2-4\omega^2.
\]

Define

\[
 V_u=1-\omega^2+6\lambda I+ah+2gb=4\lambda I,\quad
 V_v=1-\omega^2+2\lambda I+ah-2gb=-4gb,\quad
 B=U''(h)=M^2-\frac{3Mh}{4}+3h^2.
\]

For a spatial Fourier mode of magnitude \(k\), direct variation gives

\[
\begin{aligned}
 \ddot u-2\omega\dot v&=-(k^2+V_u)u-2gf\,s-af\,\xi,\\
 \ddot v+2\omega\dot u&=-(k^2+V_v)v-2gf\,t_X,\\
 \ddot s-4\omega\dot t_X&=-(k^2+D)s-2gf\,u,\\
 \ddot t_X+4\omega\dot s&=-(k^2+D)t_X-2gf\,v,\\
 \ddot\xi&=-(k^2+B)\xi-2af\,u.
\end{aligned}
\]

The neutral couplings are asymmetric in these coordinates because the real and complex kinetic coefficients differ. Rescale to
\(z=(\sqrt2u,\sqrt2v,\sqrt2s,\sqrt2t_X,\xi)^T\). Then

\[
 \ddot z+G\dot z+W(k)z=0,\qquad W(k)=W_0+k^2\mathbf1,
\]

\[
W_0=\begin{pmatrix}
 V_u&0&2gf&0&\sqrt2af\\
 0&V_v&0&2gf&0\\
 2gf&0&D&0&0\\
 0&2gf&0&D&0\\
 \sqrt2af&0&0&0&B
\end{pmatrix},\qquad
G=\begin{pmatrix}
 0&-2\omega&0&0&0\\
 2\omega&0&0&0&0\\
 0&0&0&-4\omega&0\\
 0&0&4\omega&0&0\\
 0&0&0&0&0
\end{pmatrix}.
\]

The tested 10 by 10 generator for \(y=(z,\dot z)^T\) is
\(L(k)=\left(\begin{smallmatrix}0&\mathbf1\\-W(k)&-G\end{smallmatrix}\right)\).
The symmetry phase vector is
\(p=(0,\sqrt2f,0,2\sqrt2b,0)^T\), with \(W_0p=0\).

## Finite evidence

The corrected coexistence values are
\(I=49.00650744444027\), \(h=-0.976461506496568\),
\(b=-0.10747017781677803\), and \(\omega=0.8678983025671659\).
All nonzero tested eigenvalues form imaginary pairs within the declared absolute tolerance \(10^{-8}\):

| \(k\) | Largest \(|\Re\lambda|\) outside the declared zero cluster | Smallest positive frequency |
|---:|---:|---:|
| 0 | \(4.40\times10^{-15}\) | 0.2653436138 |
| 0.001 | \(8.94\times10^{-15}\) | 0.0004979188270 |
| 0.01 | \(6.10\times10^{-15}\) | 0.004979330429 |
| 0.1 | \(8.69\times10^{-15}\) | 0.049934599995 |
| 1 | \(3.54\times10^{-15}\) | 0.4998763964 |
| 10 | \(1.25\times10^{-15}\) | 8.462317800 |
| 100 | \(1.11\times10^{-14}\) | 98.28420937 |

At \(k=0\), the expected double zero prints as a tiny real pair \(\pm6.23799\times10^{-8}\), inside the **predeclared** \(2\times10^{-5}\) zero cluster. This floating point splitting is preserved in the raw record; the computed matrix is not claimed to have an exactly imaginary zero pair. The independent field-equation residual and exact symmetry/positivity identities provide the interpretation of that pair. A zero-frequency phase drift can have a secular generalized mode, which differs from exponential growth.

At \(k=0.001\), the Goldstone pair gives

\[
 \frac{\Omega^2}{k^2}=0.24792315829624437,
 \qquad c_{s,\mathrm{thermo}}^2
 =\frac{q}{\omega\,dq/d\omega}=0.24792301922176127.
\]

The relative discrepancy is \(5.61\times10^{-7}\), below the declared \(10^{-4}\). The lower-frequency-pair ratios at larger \(k\) are dispersive values; they are not all thermodynamic sound speeds or a tracked mode identity through potential crossings.

## Conditional all-wavenumber statement

This is an algebraic sufficient condition, separate from the finite numerical eigenvalue check. For an **exact** stationary background with \(I>0\), \(D>0\), \(B>0\), and

\[
 S=4\lambda I-\frac{4g^2I}{D}-\frac{2a^2I}{B}
   =2I\left[2\left(\lambda-\frac{g^2}{D}\right)-\frac{a^2}{B}\right]>0,
\]

the amplitude block in coordinates \((\sqrt2u,\sqrt2s,\xi)\) is positive definite by its Schur complement. The phase block in \((\sqrt2v,\sqrt2t_X)\) has positive trace and zero determinant because \(b=-gI/D\), so it is positive semidefinite with the U(1) null direction. Thus \(W_0\succeq0\) and \(W(k)\succ0\) for every \(k>0\).

With \(G^T=-G\),

\[
 \mathcal E_2=\tfrac12|\dot z|^2+\tfrac12z^TW(k)z,
 \qquad \dot{\mathcal E}_2=0,
 \qquad L^T\operatorname{diag}(W,\mathbf1)
       +\operatorname{diag}(W,\mathbf1)L=0.
\]

For \(k>0\), the positive energy metric makes \(L\) similar to a real skew-symmetric matrix, hence its eigenvalues are imaginary. At \(k=0\), positive semidefiniteness excludes nonzero exponentially growing eigenmodes by the same energy identity; the neutral symmetry sector needs the separate zero-mode treatment above.

The numerical background has \(D=0.9886101456\), \(B=10076.0950442\), and \(S=0.9998296930\). The amplitude eigenvalues are approximately \((0.943767673,1.008392816,10465.223523)\); the phase eigenvalues are approximately \((-1.57\times10^{-14},0.989542127)\). These satisfy the sufficient conditions with a substantial amplitude margin, up to the displayed floating point phase roundoff. They are not an interval-certified enclosure of an exact coexistence solution.

## Consequence and remaining obligation

The **same proposed action** passes this homogeneous linear stability check at its corrected coexistence point, with its full charged-X and neutral dynamics retained and a sound mode matching thermodynamics. It does not make that sound mode an escaping vacuum radiation channel. The vacuum gaps and charge constraints in `ASYMPTOTIC_FLUX_AUDIT.md` still apply.

The next discriminating calculation remains an outgoing-boundary fluctuation or small radial perturbation calculation around the finite three-field fragment. It must resolve which bulk/surface disturbances reach real outgoing \(\Psi\), \(X\), \(\chi\), or bound-fragment channels, and measure their energy and charge. Angular-momentum transfer additionally requires nonradial modes or an independently derived torque calculation. Stable bulk waves and a positive stationary merger gap alone do not determine that efficiency or the four-dwarf mass allocation.

## Reproduction and review

The executed command is recorded verbatim in `bulk_run_001/repaired_run/manifest.json`. Reproduction must use a **fresh output directory** and preserve both completed and failed evidence. Source reading independently checked the five equations, both rotation factors, the neutral kinetic normalization, phase null vector, Schur complement, and energy identity. Mathematical self-proofreading covered this report's displays, variables, table, provenance paths, and interpretation limits. The sole mathematical-token edit was renaming the displayed imaginary-part amplitude from \(t\) to \(t_X\) to distinguish it from time, consistently throughout the report; no coefficient, sign, operator, or result changed. No unresolved notation issues remained.
