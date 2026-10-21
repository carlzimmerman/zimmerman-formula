# Origin of the stiffness length: bounded checkpoint

**The origin of \(L_*\) remains open.** Three specified mechanisms were tested. Finite-range alignment supplies a gradient coefficient but introduces an interaction range and strength; contact-interaction pressure supplies the longitudinal coefficient but leaves a microscopic mass/coupling ratio free; quantum pressure has the wrong derivative order to supply the canonical coefficient directly. A useful exact result is that \(L_*\) is **not a universal response or correlation length** of the frozen action.

Base: `431f22bd6fe998759b843d13113762d73356aec6`; local date 2026-10-20. Scope and criteria were recorded in [contract.md](contract.md) before the new computations. No other current lane report was read. Evidence is a self-reviewed analytic derivation plus **40/40 finite checks**, not an independently reviewed proof of a microscopic theory. No products of constants, exponent searches, or fits of particle parameters to the window were used.

## 1. What the constraint actually says

The requested 24 pc–1 kpc interval is a useful benchmark, not an established joint confidence interval. CFG820 gives the primary globular lower limit 24.0 pc canonical / 24.7 pc alternate. CFG821's nominal upper limit 22 pc comes from a model that already fits the unscreened dwarfs badly; it is conditional on their missing-mass treatment. PARAMRED C_LSTAR (CFG832) identifies the old 1 kpc endpoint as a scan edge and gives soft upper edges **2042 / 2138 pc** under point-source screening and a campaign rms threshold. This report neither recomputes these likelihoods nor upgrades their status.

Nearest relevant prior results were read before selecting routes: PARAMRED C_LSTAR's dimensional obstruction and free inertia; CFG694's critical quadratic cancellation; CFG699's cosmic-mean inertia timescale and its nonlinear-density caveat; CFG807's uniform-vacuum freedom; CFG858's failure to obtain an extra dwarf speed from stiffness; CFG897's unsuccessful FRW stiffness-vacuum matching; CFG938's longitudinal pressure dictionary, shear limitation, and early-universe problem for an unmodified quadratic-density energy. Their exact input hashes are in [results/manifest.json](results/manifest.json). The older O6 inventory supplies historical context only. In particular, neither a horizon matching argument nor the previously failed extra-speed coincidence is repeated as a new mechanism.

## 2. Exact response operator and structural freedom

Use the specified S2 action, with \(K=4\pi G\), \(u=K|P|\), and \(\gamma=KL_*^2/2\). Up to an additive constant,

\[
 W_{\rm rem}(u)=\frac{a_0^2}{K}w(s),\qquad
 w(s)=-\frac{s^2}{2}-s-\log(1-s),\qquad s=u/a_0\in[0,1).
\]

About a homogeneous background \(P_0\ne0\), write \(e=P_0/|P_0|\). The local Hessian is

\[
 H_W=K\{B I+(A-B)ee^T\},\quad
 B=\frac{s}{1-s},\quad A=\frac{s(2-s)}{(1-s)^2}.
\]

The homogeneous background can be held by an external source; only its local linear response is being studied. For a nonzero Fourier mode, eliminate the potential perturbation using its own field equation, with baryon perturbation held fixed at zero. The quadratic form \(|\nabla\delta\Phi-Kp|^2/(2K)\) then leaves \(K|p_T|^2/2\). Thus

\[
 \boxed{\mathcal H(k)=K\{\Pi_T(\hat k)+B I+(A-B)ee^T\}
                 +\gamma k^2 I.}
\]

This is a static susceptibility kernel. S2 alone contains no inertia or stochastic ensemble, so it does not define a dynamical propagation length or a thermal correlation function.

For a fixed direction of \(k\), an eigenvalue \(KC\) of the zero-gradient kernel has crossover/pole scale

\[
 \xi_C=\sqrt{\gamma/(KC)}=L_*/\sqrt{2C}.
\]

For \(k\parallel e\), the longitudinal eigenvalue has \(C=A\), while both transverse ones have \(C=1+B\). For \(k\perp e\), the longitudinal mode has \(C=B\); the two transverse modes have \(C=1+A,1+B\). In general the gravitational projector makes the response angular and nonlocal; the directional scales are not a proof of a single exponential real-space correlation function.

| Background \(s\) | \(\xi/L_*\), longitudinal \(k\parallel e\) | \(\xi/L_*\), longitudinal \(k\perp e\) |
|---|---:|---:|
| 0.0001 | 49.996 | 70.707 |
| 0.01 | 4.962 | 7.036 |
| 0.1 | 1.460 | 2.121 |
| 0.9 | 0.0711 | 0.2357 |

At \(s=0\), \(A=B=0\): the **coupled longitudinal vacuum mode is gapless**, with no finite mass-defined correlation length. The transverse static scale is \(L_*/\sqrt2\). If instead \(\Phi\) is externally clamped, the kernel is \(KI+H_W+\gamma k^2 I\), giving radial \(\xi=L_*(1-s)/\sqrt2\). These are different physical response problems. If the medium is constrained to be purely longitudinal, project onto that subspace rather than importing the unrestricted vector's mixed eigenmodes.

There is a simple freedom result within the stated effective theory: for every positive \(\lambda\), replacing \(\gamma\) by \(\lambda\gamma\) leaves \(W\), the coupling, homogeneous solutions, and positivity of these static modes unchanged, while multiplying \(L_*\) and each finite \(\xi_C\) by \(\sqrt\lambda\). Hence these properties cannot select \(\gamma\). This does not prohibit an additional microscopic theory from selecting it.

## 3. Route A — finite-range alignment

**Mechanism.** Specify a positive bond energy between polarization elements,

\[
 F_{\rm bond}=\frac{\eta K}{4}\int d^3x\,d^3r\,w_\ell(r)
       |P(x+r)-P(x)|^2,
\quad w_\ell(r)=\frac{e^{-r^2/(2\ell^2)}}{(2\pi\ell^2)^{3/2}},\quad\eta>0.
\]

Its exact Fourier Hessian is \(\eta K[1-e^{-\ell^2k^2/2}]I\). Expansion at small \(k\ell\) gives

\[
 \gamma=\eta K\ell^2/2,\qquad \boxed{L_*^2=\eta\ell^2}.
\]

For any normalized isotropic positive kernel with finite second moment, this becomes \(L_*^2=\eta\langle r^2\rangle/3\). No uniform-field measurement of \(W\) determines this second moment. The explicit Gaussian is a specified toy bond free energy, not a demonstrated particle completion of S2.

**Executed discriminator.** The gradient approximation's relative error is 0.25% at \(k\ell=0.1\), 27.1% at 1, and grows without bound at high \(k\); the exact kernel saturates. Its 1% validity boundary is \(k\ell=0.1996686\). Therefore identifying an interaction range of tens of parsecs with \(L_*\) at order-one \(\eta\) does not produce the same stiffness operator down to Solar-System gradients. As an explicitly chosen resolution test, requiring 1% accuracy at \(k=1/{\rm AU}\) requires \(\ell<0.200\) AU and \(\eta>6.15\times10^{14}\) at 24 pc, or \(1.07\times10^{18}\) at 1 kpc. These are requirements, not fitted couplings or observational bounds on this toy model.

**Outcome.** Positive gradient stiffness is derived from the specified bond energy; its numerical scale is not. Missing inputs are independently fixed \(\eta\) and \(\ell\), together with a controlled ultraviolet completion. This finite-range realization remains open with those inputs; changing the kernel without fixing its moment would repeat the same freedom.

## 4. Route B — compressibility and contact interactions

Assume S3's \(\delta\rho=\nabla\cdot P\) and a local internal energy density \(\epsilon(\rho)\). Quadratic fluctuations cost

\[
 F^{(2)}_{\rm int}=\tfrac12\epsilon''(\rho_0)(\nabla\cdot P)^2,
\quad c_s^2=\rho_0\epsilon''(\rho_0).
\]

Matching a **background-independent longitudinal** coefficient requires \(\epsilon''=\gamma\), hence
\(\epsilon=\gamma\rho^2/2+C_1\rho+C_0\) and \(p=\gamma\rho^2/2-C_0\). Thus a constant \(c_s\) does not give universal \(L_*\); it requires \(c_s\propto\sqrt\rho\).

The tensor limitation is exact:

\[
 \int|\nabla P|^2=\int\{(\nabla\cdot P)^2+|\nabla\times P|^2\}
\]

under periodic/decaying boundary conditions. Pressure fixes only the first term. The full canonical vector stiffness needs an independent shear sector, or an explicit curl-free restriction. CFG938 already identified this longitudinal dictionary; the added step here is a concrete microscopic parameter matching rather than another invocation of the same pressure term.

A dilute contact-interacting condensate has \(\epsilon=g\rho^2/(2m^2)\), so
\(\gamma=g/m^2\), \(L_*^2=g/(2\pi Gm^2)\). For the specific relativistic potential \(V=\tfrac12m^2\phi^2+\kappa_4\phi^4\) in natural units, averaging the rapidly oscillating field gives \(g=3\kappa_4/m^2\), as in Goodman's Eqs. (7)–(10). Here \(\kappa_4\) is unrelated to the project's \(\kappa=1/2\). Restoring SI for \(E=mc^2\),

\[
 \boxed{E^4=\frac{3\kappa_4\hbar^3c^7}{2\pi G L_*^2}}.
\]

This is an actual mechanism-fixed power law, not dimensional pattern matching. Nevertheless neither the particle mass nor \(\kappa_4\) is specified by S2. [Goodman, exact v1](https://arxiv.org/pdf/astro-ph/0003018v1) supplies the microscopic model, not its identification with S2. Its Eq. (12) prints an inconsistent \(c^3\); the \(c^7\) conversion above follows from its natural-unit equations and reproduces its quoted 10.7 eV benchmark. Details and exact PDF hash are in [sources.json](sources.json).

| Benchmark \(L_*\) | Required \(mc^2/\kappa_4^{1/4}\) | Required \(c_s\) at \(\rho=0.01\,M_\odot/{\rm pc}^3\) |
|---|---:|---:|
| 24 pc | 47.41 eV | 0.395 km/s |
| 1 kpc | 7.345 eV | 16.44 km/s |
| 2.042 kpc | 5.140 eV | 33.57 km/s |

These inverted parameter requirements are **not mass predictions**. Setting the independently unspecified \(\kappa_4=1\) only illustrates the normalization; it does not select a length. In an ordinary self-gravitating fluid, \(k_J^{-1}=c_s/\sqrt{4\pi G\rho}=L_*/\sqrt2\); in S2 the critical local term cancels the corresponding longitudinal gravitational mass, so this ordinary Jeans instability cannot be transferred to S2 unchanged. The standalone contact-fluid polytrope has first zero radius \(\pi L_*/\sqrt2\), a comparison scale rather than a prediction for canonical galaxy profiles.

**Prior failure addressed, not erased.** Continuing \(\epsilon\propto\rho^2\) into the early universe triggers CFG938's background-energy problem. The specified relativistic quartic model instead becomes radiation-like at high density (Goodman Eq. 11), so the same low-density extrapolation is not valid there. This changes a failed premise, but does not establish cosmological viability: abundance, thermal history and the bridge to S2 remain uncomputed. The formal \(\gamma\rho=c^2\) crossover occurs near \(z=5.61\times10^5\) at 24 pc or \(4.67\times10^4\) at 1 kpc for the explicitly assumed canonical cosmic density. These are breakdown estimates, not solved transition redshifts.

**Outcome.** Conditional microscopic origin of the *form* of longitudinal stiffness, with an independent \(\kappa_4/m^4\) amplitude and missing shear/tether/thermal-history bridges. It is not a derivation of the coefficient or a claimed extension of the collisionless canonical medium.

## 5. Route C — quantum pressure / healing scales

For a nonrelativistic density condensate the amplitude-gradient energy is

\[
 F_Q=\frac{\hbar^2}{8m^2}\int\frac{|\nabla\rho|^2}{\rho}\,d^3x
 \ \Rightarrow\ F_Q^{(2)}=\frac{\hbar^2}{8m^2\rho_0}
                    \int|\nabla(\nabla\cdot P)|^2\,d^3x.
\]

Its longitudinal Hessian is \(\hbar^2k^4/(4m^2\rho_0)\), while canonical stiffness is \(\gamma k^2\). Matching at one \(k_0\) gives \(\gamma_{\rm eff}(k)=\hbar^2k^2/(4m^2\rho_0)\), not a universal coefficient. After a match at \(k_0\), the ratio is \((k/k_0)^2\), spanning \(10^{-4}\) to \(10^4\) in the executed seven-point check. No particle mass removes this mismatch.

The independently established Schrödinger–Poisson comparison has
\(k_J^4=16\pi G\rho_0m^2/\hbar^2\), verified against [Hu–Barkana–Gruzinov, v2, Eqs. (3)–(4)](https://arxiv.org/pdf/astro-ph/0003365v2). Their wavelength is \(2\pi/k_J\); all numbers here use **\(1/k_J\)**. At the fixed illustrative mass \(10^{-22}\) eV/\(c^2\), this inverse wavenumber is 642 pc at \(0.01\,M_\odot/{\rm pc}^3\), 361 pc at ten times that density, and 15.10 kpc at the assumed canonical cosmic mean. Numerical overlap with a stiffness window establishes no operator equivalence.

At fixed \(0.01\,M_\odot/{\rm pc}^3\), forcing \(k_J^{-1}=24\) pc requires \(7.16\times10^{-20}\) eV/\(c^2\), while forcing 1 kpc requires \(4.12\times10^{-23}\) eV/\(c^2\). Likewise the conventional contact-condensate healing scale \(\xi=\hbar/(\sqrt2 m c_s)\) would require masses \(5.65\times10^{-21}\) and \(1.36\times10^{-22}\) eV/\(c^2\), respectively, if \(c_s=10\) km/s. These merely quantify missing assumptions; no mass was selected from them.

**Outcome.** Direct quantum-density-pressure origin is obstructed by derivative order and background dependence. A different order parameter could have a direct two-derivative energy, but its map to \(P\), normalization and mass then become new inputs. That broader route is untested, not ruled out.

## 6. Verification and continuation

The exact symbolic checks include the potential Hessian, gravitational elimination, contact EOS, quartic average, longitudinal/shear identity, and operator order. Independent Cartesian finite differences at six backgrounds have maximum relative Hessian error \(7.48\times10^{-8}\); 91 numerical response matrices agree with their analytic spectrum to \(2.85\times10^{-14}\). Positivity, derivative-order and units mutations bite. The remaining checks verify parameter inversions and unchanged source hashes. No eigenvalue scan replaces the analytic positivity argument: \(A,B>0\) and \(\Pi_T\succeq0\) imply positivity for every direction when \(0<s<1\).

The first run copied the primary source's faulty SI power and passed checks that did not yet test that conversion. Its script, results and manifest are retained as `results/initial_*_SI_conversion_error*`; they are **superseded, not valid evidence for the mass table**. The final run adds units, mutation and independent numerical benchmark checks. [results/manifest.json](results/manifest.json) validates as schema v2 with status `completed`; the exact local source hashes and software versions are recorded there. The portable replay reproduces the final numerical output without documentary files or git.

From the repository root, preserving the primary outputs:

```sh
python3 -m pip install -r core_open_problems_2026_10_20/04_stiffness/requirements.txt
python3 core_open_problems_2026_10_20/04_stiffness/scripts/run_checks.py --output-dir /tmp/stiffness-replay
```

An audited run that also requires and hashes the listed repository sources adds `--provenance-root .`. No skill installation or network access is needed for either computation. The original external PDFs are identified by versioned URLs and exact SHA-256 hashes in `sources.json`; they are not needed for numerical replay and are not bundled.

**Smallest unresolved gap:** an independently specified microscopic model must predict the coefficient of the correct spatial operator, including its tensor sector. Route A needs a predicted \(\eta\ell^2\); Route B needs a predicted \(\kappa_4/m^4\) plus a valid map to the frozen action; Route C must first change or justify its order-parameter map. Measuring a response length at one background cannot fill this gap without the Hessian dictionary above.

The useful next step is a theory with those inputs fixed by an independent calculation or measurement, followed by matching its entire response operator and its range of validity. Repeating scale coincidences or fitting an unknown mass to the interval does not advance that step. These are three bounded mechanisms with explicit deferred continuations, not an exhaustion of all possible origins.
