# A nonzero leading capture witness in an existing Coulomb host

This is a comparison calculation within the original heavy-host Newtonian
potential. It supplies an explicit positive *leading Born kernel*, rather
than inferring capture from an energy inequality. It is not an exact
Coulomb-distorted continuum or full regulated scattering theorem.

Use natural units for momentum, mass and length, retaining `hbar` only in
the energy-to-time conversion. Let the host's existing mass be `M_h`,
`alpha=G M_h m`, and use its hydrogenic daughter ground state

\[
 a={1\over m\alpha},\qquad E_b={m\alpha^2\over2},\qquad
 \phi_b(x)={e^{-|x|/a}\over\sqrt{\pi a^3}}.
\]

Its Fourier transform is obtained by elementary radial integration:

\[
 \widetilde\phi_b(Q)
 ={8\sqrt\pi a^{3/2}\over(1+a^2Q^2)^2}>0.
 \tag{1}
\]

Replace the exact continuum waves by box-normalized plane waves solely in
the leading comparison matrix. Equation (5) of `RESULT.md` then gives

\[
 M^{\rm Born}_{bk;pq}
 ={2g_2\over V^{3/2}}\widetilde\phi_b(p+q-k).
 \tag{2}
\]

On the capture energy shell,

\[
 k_0^2=p^2+q^2+2mE_b.
\]

For example take equal incoming momentum magnitudes `p=q=m v` with
`alpha<<v<<u_*`, and choose their angle such that
`p dot q=m E_b`. The outgoing vector `k=p+q` then has magnitude `k_0`
and gives the strictly positive maximal overlap `Q=0` in (1)-(2).
The chosen angle exists because `cos angle=alpha^2/(2v^2)<1`.
All incoming/outgoing kinetic energies can simultaneously satisfy the
low-energy contact regime because `v<<u_*` and `alpha<<v`.
No source resonance or additional microscopic coupling is used in this
comparison. The particular host and scattering state are constructed
initial data, not inherited empirical predictions.

There is a whole outgoing energy shell, not just one measure-zero vector.
For a normalized distinct incoming pair, integrate that shell using the
same continuum normalization. Let `P=|p+q|` and `k_0>0`. The golden-rule
capture width in this leading approximation is

\[
 W^{\rm Born}_{pq\to b+C}
 ={g_2^2m k_0\over\pi^2\hbar V^2}
       \int d\Omega_k\,|\widetilde\phi_b(P-k_0\hat k)|^2.
 \tag{3}
\]

The elementary angular integral is, for `A>B>0`,

\[
 \int {d\Omega\over(A-B\cos\vartheta)^4}
 ={2\pi\over3B}\big[(A-B)^{-3}-(A+B)^{-3}\big].
\]

Applying it with `A=1+a^2(P^2+k_0^2)` and `B=2a^2Pk_0` gives

\[
 \boxed{W^{\rm Born}
 ={64g_2^2m a\over3\hbar V^2P}
 \left[{1\over(1+a^2(P-k_0)^2)^3}
       -{1\over(1+a^2(P+k_0)^2)^3}\right]>0,\quad P>0.}
 \tag{4}
\]

At `P=0` its continuous limit is

\[
 W^{\rm Born}={256g_2^2m k_0a^3\over
                  \hbar V^2(1+a^2k_0^2)^4}>0.
\]

Thus the leading approximation exhibits a nonzero-measure positive capture
kernel and a physical outgoing energy carrier. The factor `V^-2` is for
one normalized incoming pair; summing an actual incoming particle
distribution supplies the corresponding volume/density factors. It is
not an independent phenomenological attempt rate.

Two qualifications are load bearing. First, plane waves are not exact
continuum eigenstates of the Coulomb host and are not exactly orthogonal
to `phi_b`. Orthogonalizing them changes the kernel; merely writing
`alpha/v<<1` is not a bound on that change or on the full Coulomb distortion.
At the displayed phase-matched point each one-wave bound-projection
subtraction has a relative factor of order `(a p)^-8`, from the known
bound wave and density Fourier transforms, but that observation alone
does not control every exact-continuum correction. Second, the spatial
contact and host must use a common admitted finite regulator before
transferring continuum hydrogen formulas to an exact field Hamiltonian.

A positive Born expression therefore establishes a concrete candidate
channel and its coefficient in that approximation. A rigorous nonzero
exact capture probability in the full specified host requires its
distorted continuum overlaps or a controlled remainder estimate, plus
the scattering/asymptotic escape construction. Those are not supplied
by (4). No deterministic writer, actual inherited capture probability,
or complete S4 memory is claimed.

All integrals and factors were calculated analytically. No numerical
simulation, symbolic package or fit was run. This is author self-review.
