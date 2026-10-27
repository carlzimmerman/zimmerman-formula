# Repo-derived lead: condensate-assisted optical emission

2026-10-13. **Conditional candidate, not an established breakthrough.** A specific occupied final state can enhance the proposed radiative transition while repulsive interaction energy lowers its available photon energy. Their competition produces a finite emission window. The elementary weak-mixing projection agrees with the actual homogeneous coupled-field gapped mode at the tested point. Formation, confinement, competing decay, photon transport and empirical identification remain open; no laboratory gravity device is demonstrated.

## What the repository search contributed

This was a targeted search across the fresh-gravity campaign, independent-field-theory summaries, and carrier/framework-certification files; it was not an exhaustive audit of every repository line.

- `cold_production_2026_10_11/BOSE_REACTION_CLOCK.md` distinguishes gross stimulated decay from net forward-minus-inverse relaxation. A large occupation factor cannot be substituted for a cooling rate.
- `framework_certification_2026_10_12/resolved_q3/DERIVATION.txt` derives exact Fock ladder factors and retains interaction energy in finite quantum evolution.
- `framework_certification_2026_10_12/local_interaction/RESULT.txt` explicitly keeps the quartic detuning in conversion and distinguishes conditional quantization from empirical validation.
- The broader CFG384 Bose-relaxation estimate concerns elastic scattering and carries astrophysical/model assumptions; its multiplier is not a photon-emission calculation. The separate C2 gravity/interface work has an unclosed metric/perturbation contract and cannot be attached as a certified gravity law here.

The first three inputs are copied and hash-pinned in this package. Their exact occupation and interaction-energy bookkeeping motivates the calculation below. Their stated limitations are retained.

## Occupied final state and finite-volume bookkeeping

Take a uniform daughter condensate in volume \(V\), occupation \(N\), density \(n=N/V\), and repulsive Hamiltonian \(H_{\rm int}=\kappa a^{\dagger2}a^2/V\). An added source excitation can deposit two daughters in that same condensate mode while emitting opposite-momentum photons. This is a particular final-state channel, not the total in-medium decay rate.

The exact creation factor is

\[
|\langle N+2|a^{\dagger2}|N\rangle|^2=(N+1)(N+2).
\]

The condensate pair density factor tends to \(n^2\), since
\((N+1)(N+2)/V^2\to n^2\) at fixed density. It does not give an unrestricted \(N^2\) macroscopic luminosity at fixed density.

The interaction energy needed for the pair is

\[
\Delta E_{\rm int}=\frac{\kappa}{V}[(N+2)(N+1)-N(N-1)]
=\frac{\kappa}{V}(4N+2)\to4\kappa n.
\]

Ignoring mixing initially, the photon-pair energy is
\(\Delta_c=\delta-4\kappa n\), with \(\delta=M-2m\). This channel requires \(\Delta_c>0\). The large occupation cannot overcome an energy-forbidden final state. Other final states need separate analysis.

## Conditional photon partial width

Keep the previously declared, hypothetical interaction

\[
-\frac{\zeta}{4\Lambda^3}(\chi^*\phi^2+\chi\phi^{*2})F_{\mu\nu}F^{\mu\nu}.
\]

In the occupied final-state matrix element, \(\phi^{*2}\) contributes \(n/(2m)\) at leading order. The effective linear photon vertex for a source excitation is therefore \(g_{\chi\gamma\gamma}=\zeta n/(2m\Lambda^3)\). With source normalization \(1/(2M)\), identical-photon symmetry factor, and two-body photon phase space, the leading projection gives

\[
\boxed{\Gamma_{\gamma,c}
=\frac{\zeta^2 n^2\Delta_c^4}{256\pi M m^2\Lambda^6}},
\qquad E_\gamma=\Delta_c/2.
\]

The fourth power, rather than a vacuum scalar's usual third-power expression, retains the heavy source normalization while only the gap energy is released. The formula assumes a homogeneous rest condensate, a weakly mixed source excitation, the vacuum photon density of states, near-unit Maxwell normalization, weak perturbative coupling and negligible recoil. Finite-size momentum spread, depletion and nonuniform chemical potentials broaden the ideal photon line. The portal is not established by the repo's dark action or by experiment.

At fixed \(\kappa,\delta\), define \(x=4\kappa n/\delta\). The rate depends on \(x^2(1-x)^4\), maximized at \(x=1/3\). Radiated power per excited source depends on \(x^2(1-x)^5\), maximized at \(x=2/7\). In particular,

\[
0\le x\le1\quad\Longrightarrow\quad x^2(1-x)^4\le16/729.
\]

These are leading weak-mixing extrema, not universal physical optima over all microscopic parameters or source preparations.

## Check against the actual coupled homogeneous fields

A pure daughter condensate with exactly zero source background is not a stationary solution when \(c_3\ne0\). Retain the required background:

\[
\psi=\sqrt n\,e^{-i\mu t},\quad b=B e^{-2i\mu t},\quad
B=-\frac{c_3n}{\delta-2\mu},\quad
\mu=2\kappa n+2c_3B.
\]

With \(\epsilon=c_3^2/(\kappa\delta)<1\) and \(u=2\mu/\delta\), the branch connected to the daughter condensate is

\[
u=\frac{1+x-\sqrt{(1-x)^2+4\epsilon x}}2,
\qquad \Delta_c=\delta(1-u).
\]

The coherent background source charge relative to daughter charge is \(\epsilon x/[2(1-u)^2]\). This background is stationary; counting \(|B|^2\) as a supply of independently decaying source particles would falsely predict light from the ground state.

In units of \(\delta\), the zero-momentum Bogoliubov matrix for \((a,b,a^*,b^*)\) is

\[
L=\begin{pmatrix}
x-u/2&\sqrt{\epsilon x}&u/2&0\\
\sqrt{\epsilon x}&1-u&0&0\\
-u/2&0&-x+u/2&-\sqrt{\epsilon x}\\
0&0&-\sqrt{\epsilon x}&-1+u
\end{pmatrix}.
\]

Besides the zero-frequency phase sector, its gapped frequency satisfies

\[
(\omega_g/\delta)^2=(1-u)^2+x(x-u)+2\epsilon x.
\]

For a symplectically normalized eigenvector \((u_a,u_b,v_a,v_b)\), the photon-operator matrix element relative to the bare source is
\(u_b+v_b+2(B/\sqrt n)(u_a+v_a)\).
The script independently diagonalizes the matrix and projects this vertex.

At \(\epsilon=10^{-4},x=2/7\), \(\omega_g/\delta=0.7143737073\), while the bare-background gap is 0.7143257120. Vertex and frequency corrections together multiply the projected rate by **1.000089575**. Thus the leading example survives this homogeneous mixing check. This is not a full spectral-function, finite-momentum stability, damping or escape calculation.

## Parameter scan and admission failures

Use \(m=1\) MeV, \(\delta=5\) eV, \(\Lambda=10M\), \(\zeta=1\), \(\epsilon=10^{-4}\), and \(x=2/7\). Set \(\kappa=\lambda_{\rm tot}/(4m^2)\). The table uses the weak-mixing background gap; the mode correction above is below 0.01% in rate. Its ideal photon wavelength is about 694.3 nm. The wavelength follows these chosen parameters, not measured data.

| \(\lambda_{\rm tot}\) | Condensate density, kg/m³ | Radiative partial width, s⁻¹ | Initial power per source-equivalent kg, W |
|---:|---:|---:|---:|
| 1 | 331.45 | \(4.9011\times10^{-24}\) | \(7.8663\times10^{-13}\) |
| \(10^{-3}\) | \(3.3145\times10^5\) | \(4.9011\times10^{-18}\) | \(7.8663\times10^{-7}\) |
| \(10^{-6}\) | \(3.3145\times10^8\) | \(4.9011\times10^{-12}\) | 0.78663 |

“Source-equivalent kg” means \(M N_s\) for a prepared excited population, not the total condensate mass and not newly created gravitational mass. Excitations need preparation and energy. No source fraction, replenishment mechanism, steady luminosity or visual-safety claim is supplied.

The baseline ordinary *vacuum* source width at \(\lambda_{\rm tot}=10^{-6}\) is about 135 s⁻¹, vastly larger than the quoted radiative partial width. That vacuum number is a diagnostic, not the dressed competing rate. It shows why a radiative partial width alone cannot predict total yield or a steady glow. Weakening \(c_3\) can change competition, but also changes source formation; the earlier recycling bottleneck must be revisited in the dressed state.

More extreme densities were explicitly screened rather than promoted. At \(\lambda_{\rm tot}=10^{-9}\), the daughter field amplitude exceeds \(\Lambda\); without a symmetry or UV completion suppressing further operators, the isolated portal truncation is uncontrolled. At \(10^{-12}\), the chosen positive \(\zeta\) even gives a negative background Maxwell kinetic coefficient:

\[
I=1+\frac{2Bn}{2m\sqrt{2M}\Lambda^3}\simeq-398.27.
\]

That row is rejected, not a high-brightness prediction. The accepted small-field example at \(10^{-6}\) has \(I\simeq0.99999960\) and daughter amplitude about 0.0423 of \(\Lambda\); these are necessary consistency checks, not an empirical admission of the model. Near \(I=0\), canonical photon normalization and strong coupling invalidate the uncorrected rate well before any inferred divergence can be trusted.

## Confinement and ordinary gravity

Large density does not establish a compact, controllable object. The leading contact-fluid sound speed in the example is about \(2.53\times10^5\) m/s, giving a one-centimeter sound-crossing time near \(4\times10^{-8}\) s in the absence of confinement. No trap or container interaction has been derived.

For a separate Newtonian, Thomas–Fermi self-gravity comparison, use \(P=K\rho^2\). The interior hydrostatic profile and its radius/mass are

\[
\rho(r)=\rho_c\frac{\sin(\pi r/R)}{\pi r/R},\qquad
R=\sqrt{\frac{\pi K}{2G}},\qquad
M_{\rm cloud}=\frac{4\rho_cR^3}{\pi}.
\]

The mass integral is independently checked. These are standard contact-condensate/Thomas–Fermi relations, not a new gravitational law; [Chavanis, arXiv:1103.2050](https://arxiv.org/abs/1103.2050) studies the Newtonian repulsive-condensate mass–radius problem. Quantum-pressure edge structure and the full coupled source state require further treatment.

At \(\lambda_{\rm tot}=10^{-6}\) and the tabulated density taken as central density, this comparison gives **\(R\simeq1.51\times10^6\) m** and **\(M_{\rm cloud}\simeq1.45\times10^{27}\) kg**. Ordinary self-gravity could be significant for such a stipulated inventory, but it is a planetary-scale model, not a tabletop force source. The optical calculation is local and has not been integrated through this nonuniform cloud. No condensation or assembly process has produced that inventory in the calculation.

## Evidence and next discriminator

The baseline script checks exact finite Fock factors, thermodynamic volume scaling, stationary background identities and the hydrostatic mass integral. The extended run includes eight independent Bogoliubov eigenvalue comparisons: 24 numerical checks total, plus four exact SymPy identities. Three Lean statements certify the pair-energy algebra and polynomial rate-window bound; they do not certify the photon width or the existence of a physical condensate.

The first Lean audit rejected an unused-hypothesis warning despite successful theorem compilation. The original source is retained as `CondensateWindow_initial.lean` with its logs in `lean_run/`; the unnecessary hypothesis was removed and the clean audit is `lean_run_v2/`. Two deliberately damaged mathematical controls are checked there. Successful manifests, contracts and scripts preserve actual execution inputs and results. This work is self-reviewed, without independent agent review.

The new lead is **occupied-state radiative emission limited by repulsive detuning**, supported by a homogeneous coupled-mode check. The next load-bearing calculation is the dressed nonradiative width and radiative branching ratio of that same mode, followed by photon propagation through a finite condensate. Source preparation and confinement remain separately required. The repo inputs opened this route; they did not already contain a certified glow-plus-gravity mechanism.
