# Persistent quantum state and high-H overlap test — 2026-10-23

The requested cosmological calculation remains incomplete. A full non-Gaussian wavefunction now survives repeated interaction/kinetic steps in a **one-spatial-cell validation model**. Separately, the actual saved high-H classical field realization was continued from conformal time z=200 to 220. It does not demonstrate a controlled handoff to ordinary weak-collision bath kinetics. No surviving cold abundance is inferred, and no cold seed is inserted.

These are two separate computations. The reduced quantum state is not substituted for the cosmological source. The classical continuation is not described as quantum correlation evolution.

## 1. Full-state quantum propagation, without a Gaussian reset

`quantum_wavefunction.py` implements coordinate-space Strang evolution

    psi(t+dt) = exp(-i dt V/2) FFT^-1[exp(-i dt T) FFT[exp(-i dt V/2) psi(t)]]

and retains the entire complex array between steps. In units mPhi=hbar=1 and cell volume v=1,

    T = sum_i p_i^2/(2v)
    V = v [ (f^2+h^2)/2 + M^2(x^2+y^2)/2
            + lambda (f^2+h^2)^2/4
            + g/sqrt(2) (x(f^2-h^2)+2yfh) ].

The benchmark uses the existing couplings g/mPhi=.002168, lambda=.00881292 and M/mPhi=2 sqrt(1+.02^2). Both original interactions appear once. There is no added collision sink, independent inverse-rate prescription, occupation ceiling, Gaussian projection, or stepwise normalization. All creation/annihilation terms of this finite Hamiltonian remain available. This avoids double counting at the Hamiltonian level; it does **not** validate continuum forward/inverse reaction rates.

The explicit test initial state is a free product oscillator vacuum with one real X oscillator excited, a superposition of X charges +/-2. Turning on the interacting Hamiltonian makes this a numerical quench benchmark. It is not the high-H initial density matrix, a proposed cold seed, or a physical decay experiment. The potential is not normal ordered; no field-theory counterterm limit is attempted.

`quantum_wavefunction_run/results.json`, completed in 23.46 s:

- Duration 2 in mPhi^-1; coordinate interval [-6,6), 24/32/40 points per real field.
- Full-state differences for dt=.04 versus .02 and .02 versus .01: .00182858 and .000456746. Ratio 4.00349, consistent with second order.
- At fixed dt=.02, 32 to 40 points changes bare oscillator occupations by at most 1.954e-13. These are **field-coordinate grid refinements**, not spatial momentum convergence.
- Inverse propagation returns the initial state to norm error 1.251e-14. Analytic free-state check: 1.243e-6 error at dt=.002 over duration .2.
- Largest relative energy drift in tested runs: 1.07e-7. Boundary probability below 6.3e-13.
- Phi connected fourth moment at dt=.01 is -0.00198868. It is retained between steps rather than removed by Wick factorization.
- Phi reduced purity on the 24 grid is .999994884; this is small entanglement in this finite system, not bath formation. Purity itself has not been independently grid-refined.

`persistent_state_charge_run/results.json` independently applies the Fourier charge generator

    Q = f p_h - h p_f + 2(x p_y - y p_x).

It finds mean Q near zero and conserves <Q^2>=4 to approximately 2e-13. Time reversal is an algorithm check, not evidence that a particular inverse collision rate is correct.

The saved complex state is `quantum_wavefunction_run/persistent_state_n32_dt001.npy`. A dense wavefunction cannot simply be extended to the original spatial lattice: 32 points per each of four fields require 16 MiB for one cell and 16 TiB for two cells. This is a limitation of this representation, not a proof against compressed representations or the theory.

## 2. Actual high-H field continuation and overlap diagnostic

`coupled_field_restart.cpp` adds absolute-time restart to the existing classical solver. The original source and code are preserved. The scale factor is evaluated at the original conformal time, not reset to a=1. A nonzero-mass/cubic explicit-time test compares an uninterrupted interval with a split restart; maximum field/velocity difference was 5.55e-17 (`test_absolute_restart.py`).

`kinetic_overlap_probe.py` evolves the saved 96^3 state at z=200 to z=220, sampling every unit of z. Cases are 96^3 with dt=.01/.005 and 128^3 with dt=.01. The 128 state is Fourier-interpolated from the saved 96 state: it tests the restart interval, not the entire source history. It adds no new vacuum modes.

For a deliberately explicit diagnostic, define the isotropic Hartree reference

    omega_k^2 = k_FD^2 + 2 <q_f^2+q_h^2>,
    f_cl(k) = [P_k + omega_k^2 F_k]/[2 lambda omega_k].

Here F and P are Fourier field/velocity powers, normalized with L^3. Spectra are averaged in |k| shells and over the 21 saved times; f is per real Phi component. No vacuum half is subtracted from these classical proxies. The nonzero-mode energy proxy is lambda omega f. It is not the exact interacting energy and must not be called an observed particle density. A different self-consistent spectral mass or a coherent-background treatment could change a kinetic interpretation.

| Diagnostic | 96, dt=.01 | 96, dt=.005 | 128, dt=.01 |
|---|---:|---:|---:|
| Nonzero-mode energy proxy in shells with lambda f >= 1 | .774811 | .774811 | .774434 |
| Same proxy in 10 <= f < 1/lambda | .132675 | .132675 | .132793 |
| Same proxy with f < 1 | .023425 | .023425 | .023492 |
| Mean zero-mode energy-proxy fraction | .492206 | .492206 | .492099 |
| Ratio of time-averaged anomalous proxy to number proxy | .217216 | .217210 | .217164 |
| Maximum energy/work relative residual | 1.032e-6 | 2.580e-7 | 1.045e-6 |

The spatial central radial fourth moment minus its Gaussian Wick value ranges from -.5040 to +.1800, normalized to that Wick value. It measures spatial statistics of one classical realization, not a quantum connected correlator or an ensemble uncertainty estimate.

On the common nonzero band k<=4, the time-averaged energy spectra differ in relative L1 norm by 2.158e-6 on halving dt and 5.582e-4 on refining 96 to 128. Parseval independently matches real-space gradient energy within 1.8e-15. The high-k gradient tail decreases on refinement. No box-size, source-ensemble, omitted-IR, renormalized-UV, or momentum-spacing convergence is claimed. `all_pass` tests numerical invariants; it is not a thermalization flag.

The conventional large-occupation overlap with perturbative scalar Boltzmann kinetics requires both large f and small lambda f; see the explicitly stated scope of [Mueller and Son, hep-ph/0212198](https://arxiv.org/abs/hep-ph/0212198). That paper treats a neutral scalar and elastic scattering; it does not establish a matched solver for this coupled charged action. The [classical-statistical validity study, arXiv:1312.5216](https://arxiv.org/abs/1312.5216), likewise does not supply this model's quantum late-time completion.

Our result provides no justification for discarding the coherent, strongly occupied part and replacing the whole state by an ordinary weakly interacting bath at z=200..220. It does not prove that every resummed kinetic treatment fails or that thermalization never occurs. Approximately 77% refers to a stated nonzero-mode energy proxy, not total energy or surviving dark matter.

At z=220, a=551.4435, H/M=2.2103e7 and the lowest nonzero physical spatial momentum has p/m=1.9134e9. This interval is still very early. The homogeneous mode cannot be counted as cold particles simply because its spatial momentum vanishes; its expansion, coherence and self-interaction still matter.

## 3. Why this does not yet produce the requested relic

Classical non-Gaussian field statistics do not include quantum non-Gaussian dynamics. For canonical unit-mass coordinates and a cubic/quartic potential, the exact Wigner equation contains, in addition to classical Hamiltonian drift,

    -(hbar^2/24) sum_ijk V_,ijk partial_{p_i} partial_{p_j} partial_{p_k} W.

Higher Moyal derivatives terminate for this potential. This third-derivative term is absent from the classical continuation; making its grid finer does not restore it. The full-wavefunction solver includes the corresponding quantum dynamics only in its four-coordinate validation system.

Thus neither a thermal matching time nor a surviving yield is assigned. Forward and inverse reactions are not yet evaluated in a dynamically formed, source-derived bath. The earlier conditional thermal yield remains conditional and cannot be promoted by these tests. Zero inferred yield would also be unjustified: the yield is **uncomputed**, not zero.

The remaining substantive task is a scalable correlated many-mode evolution, with controlled truncation and physical momentum/volume tests, or a demonstrated dynamical overlap that preserves the coherent sector while deriving the quantum collision state. More single-cell checks cannot answer that question. This turn establishes a persistent-state propagation method and a quantified obstacle to an early kinetic handoff; it does not establish a formation mechanism or a breakthrough.

## Reproduction and evidence

All three runs completed with validated v2 manifests:

- `quantum_wavefunction_run/manifest.json`
- `persistent_state_charge_run/manifest.json`
- `kinetic_overlap_run/manifest.json`

Contracts next to the scripts specify bounds, exact inputs, and non-claims. Manifests contain launch arguments, input hashes before/after, software/environment metadata and result hashes. To reproduce the numerical commands from this directory, use fresh output names:

    PYTHONDONTWRITEBYTECODE=1 python3 audit_quantum_wavefunction.py quantum_wavefunction_reproduction
    PYTHONDONTWRITEBYTECODE=1 python3 kinetic_overlap_probe.py kinetic_overlap_reproduction
    PYTHONDONTWRITEBYTECODE=1 python3 audit_persistent_state_charge.py persistent_state_charge_reproduction

The last command checks the explicitly named original saved state. To build the restart executable:

    clang++ -O3 -std=c++17 coupled_field_restart.cpp -o coupled_field_restart
    PYTHONDONTWRITEBYTECODE=1 python3 test_absolute_restart.py

Use the bounded computation-audit runner and each contract's `execution_artifacts` for fresh provenance records, rather than treating an unrecorded direct rerun as a replacement for the original manifest.
