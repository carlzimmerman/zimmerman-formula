# Causality and common-gap audit

Original goal OPEN; base and limits are in [CAUSALITY_GAP_CONTRACT.md](CAUSALITY_GAP_CONTRACT.md). These findings constrain the spectral route; they do not solve 32pi. Prior spectral work remains a homogeneous calculation under its stated assumptions.

## A speed cap does not complete the theory

Consider E0(k)=k sqrt(k/(mu+k)), mu>0. It has the same infrared k^(3/2) behavior as the earlier bulk model but

v_g=sqrt(k/(mu+k)) (3mu+2k)/(2(mu+k)),

1-v_g²=mu²(4mu+3k)/(4(mu+k)³)>0.

The group speed tends to one at large momentum. Nevertheless, E0²=k³/mu+O(k⁴) still contains |kx|³ on a Cartesian momentum axis. Its third derivative jumps by 12/mu across zero.

For a canonical scalar free field the fixed-time retarded Fourier kernel is theta(t) sin(t sqrt(m²+E0²))/sqrt(m²+E0²). At m=0 its leading nonanalytic term is -t³ |kx|³/(6mu). For a canonical Clifford band, the normalized trace of the anticommutator kernel contains cos(t sqrt(m²+E0²)), with nonanalytic term -t² |kx|³/(2mu). The corresponding coefficients remain nonzero for sufficiently early positive time when m>0.

A local microcausal kernel has spatial support inside the radius-t ball. Its Fourier transform must be entire in the Cartesian momenta. The explicit branch violates this necessary condition. The proposed capped dispersion is therefore not an exact local causal single-pole completion. The uncapped band fails the same condition. Multiplication by an analytic nonzero residue cannot remove the leading branch; adding only analytic pole kernels cannot cancel it either.

Scope matters: this does not rule out a fractional **effective excitation** within a causal interacting theory. Other nonanalytic contributions or a continuum could cancel the branch in the full commutator. Those pieces are absent from the declared free-band determinant, so its finite spectral vacuum energy cannot yet be promoted to the energy of a verified causal theory.

## An allowed gap spoils the critical response

Keep the same signed spectral masses F=(0,2,2,3,6), B=(1,1,1,5,5), and make the common perturbation

m_n²(P)=n²M²+Delta+y²P², Delta>0.

Equal counts and squared-mass sums still cancel the ultraviolet energy divergences. The fourth-moment difference remains 156M⁴. Thus the old sum rules do not forbid this perturbation.

Write S(Delta)=sum eta sqrt(n²M²+Delta). The finite homogeneous energy now has quadratic coefficient

rho(P)=rho(0)+[mu y² S(Delta)/(6pi²)]P²+O(P⁴),

S(Delta)=sqrt(Delta)-19Delta/(20M)+O(Delta²/M³).

Every nonzero Delta makes the potential analytic in P² at P=0; the cubic Taylor coefficient is zero. Small positive gaps give positive S, confirmed at the four declared ratios. With the previous assumed quadratic gravity-polarization matching, the constitutive equation acquires detuning

delta=4Gmu y² S(Delta)/(3pi),

g=(1+delta)P+O(P³), b=g-P, hence b/g tends to delta/(1+delta).

That is a linear deep response, rather than b proportional to g². The individual formerly massless component crosses over at P~sqrt(Delta)/y. Taking Delta to zero before P restores the cubic; taking P to zero at fixed Delta gives the linear response. No symmetry protecting Delta=0 has been supplied. This is a perturbation sensitivity test, not a calculation showing that a specified interaction actually generates Delta.

## Verification, sources and remaining action

The exact series and deterministic checks are retained in two provenance runs. The initial run failed its smallest-gap series check because floating substitutions cancelled nearly equal masses before evaluation. The failed absolute error was recorded. The replacement uses exact rational gap inputs and 50-digit evaluation, then rounds to double; no tolerance or scientific bound was changed. Both versions remain available.

The corrected run passes 30/30 checks. Both manifests validate with current input and output hashes; manifest validity also applies to the retained failed run and does not imply its original assertion passed.

Self-review: the local single-pole obstruction is proved under the declared canonical-kernel assumptions; the gap calculation is an exact scoped instability of the critical construction. No independent review was performed. Proofreading covered this document and its contract. Neither result excludes all interacting or medium-based theories.

Primary source checked: Hui, Nicolis, Podo and Zhou, [Microcausality without Lorentz invariance, arXiv:2502.04215v2](https://arxiv.org/html/2502.04215v2), 22 July 2025, Section 2, Eqs. (3)–(7). For homogeneous isotropic states and local scalar commutators, compact spatial support implies entire momentum dependence and exponential bounds. Our scalar kernel uses that necessary implication. Applying it to the canonical fermion anticommutator uses the same compact-support Fourier argument, not an unstated scalar theorem. Its low-energy discussion also distinguishes full correlators from isolated excitations. No local source cache was created. SciSpace and web discovery located this paper and arXiv:2307.05987v2; only the former supplies the exact theorem used here.

The next meaningful continuation requires a full retarded correlator, including the contributions that cancel the fractional branch, plus a protection or dynamical selection of the gapless critical state. Only then can its determinant and covariant stress be recomputed and the independent coupling h tested. Group-speed caps, preserved ultraviolet moments and a shared mass scale are insufficient. The original requirements remain outstanding.
