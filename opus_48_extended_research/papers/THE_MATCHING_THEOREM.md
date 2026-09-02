---
title: "The Crispy Fried Chicken Matching Theorem"
subtitle: "A galaxy well today is the cosmic background at $(1+z)^3=\\delta$: a matching theorem for dark sectors, and what it forces"
author: "C. P. Zimmerman"
affiliation: "Briar Creek Tech"
email: "carl@briarcreektech.com"
date: "2 September 2026"
---

*Version 2026-09-02 · Zenodo [10.5281/zenodo.22261001](https://doi.org/10.5281/zenodo.22261001). Companion to Zenodo [10.5281/zenodo.22242701](https://doi.org/10.5281/zenodo.22242701) (the cluster polytrope, v2 22254075) and [10.5281/zenodo.22253953](https://doi.org/10.5281/zenodo.22253953) (the nonlocal kernel instability, v2 22255522).*

*The title is the working name of the programme's relativistic-completion effort (the "fried chicken" gates); the theorem is stated in Section 3.*

**Abstract.** Every relativistic completion of Milgromian dynamics that fits the cosmic microwave background carries a dark
component, and in the modern completions that component is a *field*: the pressureless excitation of a scalar clock at the
minimum of its potential. We prove a theorem about that entire class. Because the excitation is a conserved charge that dilutes
as $a^{-3}$, and because a static well fixes the same excitation through the lapse, $u=-Q_0\Psi$, a galaxy well with dust
overdensity $\delta$ is *identically* the cosmic background at redshift $(1+z_{\rm match})^3=\delta$, with the same sound speed, for
any potential $K$. The Lyman-$\alpha$ forest at $z\simeq3$ therefore measures the dust inside galaxies today, and finds it cold. In
the static limit the same field is a $\gamma=2$ polytrope, $p_d=(2\pi G/\mu^2)\rho_d^2$, $c_s^2=|\Psi|c^2$, whose hydrostatics is the
Helmholtz equation of the Aether–Scalar–Tensor theory; on the background it pins that theory's free DBI amplitude,
$\Lambda_D/Q_0=\nu_0\Omega_\Lambda/\Omega_{\rm dm}$, 18–300 times above its own power-spectrum ceiling. Two further results close the
alternatives: an elliptic auxiliary that enters the lapse equation frees exactly one dust-like scalar, $A=c_\alpha^2a^3/[4H^2(k^2/a^2+m^2)]$,
so a constraint-only two-degree-of-freedom metric MOND that light and matter both see does not exist at quadratic order; and any
medium that holds itself up in a well has signal speed $\sim v_c$, so it cannot track a cluster merger, which the Bullet cluster
requires. What survives is a dark component that is cold, ballistic and galaxy-clustering, and a MOND well accretes it: put into
the theory's own lensing, the accreted charge multiplies the 100 kpc–1 Mpc galaxy–galaxy lensing signal by 3–20 at realistic
environments, which the KiDS-1000 isolated-lens relation excludes at $\Delta\chi^2\ge100$. The positive result on the galactic
side is that the per-galaxy acceleration scale across 147 SPARC rotation curves has zero intrinsic spread and no mass trend, where
a plain halo population predicts both, and the acceleration scale $a_0=\tfrac c2\sqrt{G\rho_{\rm DE}(z)}$ cannot rise with redshift,
which the emergent scale of cold-dark-matter halos does. Every claim is a committed script with checks that can fail, a mutation
control, and both footings of $a_0$.

## 1. The problem every completion shares

Milgromian dynamics fits galaxies with one acceleration scale. Its relativistic completions, TeVeS, Aether–Scalar–Tensor gravity
(AeST), the superfluid, the nonlocal kernels, all add a dark component to reproduce the acoustic peaks and the 100-Mpc clustering,
and in the completions that actually fit the CMB that component is a field: AeST's scalar has a potential $\mathcal K(\mathcal Q)$
with a minimum at $\mathcal Q_0$, and the excitation about the minimum carries a conserved shift charge $n=\mathcal K'(u)$,
$u=\mathcal Q-\mathcal Q_0$, whose energy density $\rho_{\rm dust}=\mathcal Q_0 n\propto a^{-3}$ plays the part of cold dark matter
(Skordis & Złośnik 2021). The programme behind this paper adopted that chassis with two additions: the acceleration scale is set
by the dark-energy density,
$$a_0=\kappa\,c\sqrt{G\rho_{\rm DE}},\qquad\kappa=\tfrac12 ,$$
with $\kappa$ fitted, never derived (measured $0.551\pm0.043$ by a distance-free method and $0.465\pm0.076$ from the
Tully–Fisher relation), and the clock potential is an offset Dirac–Born–Infeld wall, $\mathcal K(u)=-M^4+\mu_D^2\Lambda_D^2[1-\sqrt{1-u^2/\Lambda_D^2}]$, with
$\beta\equiv\mu_D^2\Lambda_D^2/M^4=1$ selected so that the scale switches off at recombination. The hope was that the same field
that is dust on the sky would sit at negligible density inside galaxies, leaving the MOND kernel alone to fit rotation curves.
This paper is the theorem that says why that hope fails for the entire class, what the data then force the dark component to be,
and what in the programme survives.

Both footings of the scale are carried on every dimensional number: the canonical $9.36\times10^{-11}$ m s$^{-2}$ from $\rho_{\rm DE}$ and
the alternative $1.13\times10^{-10}$ from $cH_0$.

## 2. The condensate is a polytrope

Take the static limit of the clock sector. Time translation of the clock fixes the lapse relation
$$\mathcal Q=\mathcal Q_0(1-\Psi)\quad\Longrightarrow\quad u=-\mathcal Q_0\Psi ,$$
exactly and for any $\mathcal K$. Near the minimum, $\mathcal K\simeq-M^4+K_2u^2$, the pressure and density of the sector are
$p=\mathcal K/8\pi\tilde G$ and $\rho=(\mathcal Q\mathcal K'-\mathcal K)/8\pi\tilde G$ with $\tilde G=(1-K_B/2)G$. Eliminating $u$,
$$p_d=\frac{2\pi G}{\mu^2}\,\rho_d^2,\qquad c_s^2=\frac{dp_d}{d\rho_d}=\frac{4\pi G\rho_d}{\mu^2}=\frac{u}{\mathcal Q_0+u}\simeq|\Psi|\,c^2,
\qquad \mu^2=\frac{2K_2\mathcal Q_0^2}{2-K_B},$$
where $\mu$ is the Helmholtz mass of the static AeST equations. The condensate is a Lane–Emden $n=1$ polytrope whose sound speed in
a well is the depth of the well. Its hydrostatic equilibrium in the potential it helps source is
$$\nabla^2\Psi+\mu^2(\Psi-C)=4\pi G\rho_b ,$$
the Helmholtz equation of Durakovic & Skordis (2024) with a Bernoulli constant $C$: the "phantom" density $\rho_d=-\mu^2\Psi/4\pi G$
is the polytrope sitting in its own well, $C$ is the captured mass, the $n=1$ polytrope's free surface sits at $\pi/\mu$ independent
of its central density, and branches with nodes are excluded because $\rho_d<0$ there means $c_s^2<0$. Read inside a cluster this
is a lever: ordered by potential depth rather than density, a cluster well pins a core of 23–33% of the missing mass
(`itemC_phase_pinning_dynamics_2026.py`, 27 checks; Zenodo 10.5281/zenodo.22242701, v2 22254075). The algebra of that paper stands.
Its cosmology, we now show, does not.

## 3. The matching theorem

Nothing in Section 2 used the well. The relation $c_s^2=4\pi G\rho_d/\mu^2$ holds wherever the quadratic approximation holds, and on
the cosmic background today $\nu_0\sim10^{-4}$ puts the field deep inside it. For a condensate that carries the dark matter,
$$c_s^2(z)=\frac{4\pi G\rho_{\rm dm}(z)}{\mu^2c^2}=2.0\times10^{-8}\Big(\frac{\mu^{-1}}{1\ {\rm Mpc}}\Big)^2(1+z)^3\qquad\text{until saturation},$$
which is $(43\ {\rm km\,s^{-1}})^2$ today at the megaparsec Helmholtz length that galactic phenomenology requires. The galaxy-scale
behaviour of the dust and its cosmological behaviour are one number. That is a special case of a statement that does not depend on
the shape of $\mathcal K$ at all.

**Theorem.** Let the dark component be carried by a field satisfying (H1) $\rho_{\rm dust}=\mathcal Q_0 n$ with $n=\mathcal K'(u)$;
(H2) the lapse relation $u=-\mathcal Q_0\Psi$ in a static well; (H3) $n\propto a^{-3}$ on the background; (H4) Newtonian linear
growth of its perturbations with pressure $c_s^2k^2$, $c_s^2=\mathcal K'/(\mathcal Q\mathcal K'')$. Then the field cannot both (a) be
cold enough for the CMB and the Lyman-$\alpha$ forest and (b) be absent from galaxies at the 30% level inside 30 kpc.

*Proof.* By H1 and H2 the well's dust overdensity is $\delta_{\rm well}=n_{\rm well}/n_0$, and by H3 the background carries that
charge at $(1+z_{\rm match})^3=\delta_{\rm well}$. Since $c_s^2$ is a function of $u$ alone, the background at $z_{\rm match}$ has
the well's sound speed. Condition (b) bounds $\delta_{\rm well}\le5000$ by the mass budget, so $z_{\rm match}\le16$, and pressure
support of the well makes that sound speed $75$–$283$ km s$^{-1}$ for every $\mathcal K$ tried, $u^2$, $u^3$, $u^4$, $u^8$ and the
non-analytic superfluid minimum $|u|^{3/2}$. By H4 a fluid that hot at $z\le16$ erases the power at $k\gtrsim1\,h\,{\rm Mpc}^{-1}$,
which the forest measures, and for the quadratic and DBI cases it is hot at recombination unless $\mu^{-1}\le0.6$ kpc, contradicting
(b). $\square$

The theorem turns an unanswerable question, whether the dark field falls into galaxies, into a measured one. The dust at $z=3$ is
the dust inside a galaxy well today. The forest says the dust at $z=3$ is cold. Therefore it falls in. Two remarks on scope. H4 is
the framework's own footing, not $\Lambda$CDM's: the programme's covariant perturbation theory carries a de Sitter–Unruh Hubble floor
under the kernel argument, and with it Milgromian dynamics changes linear growth by at most 6% at every scale and redshift; without
the floor a warm-dust cosmology overproduces the 100-Mpc power 5–13 times for every $\mu$. And the non-analytic minimum, whose
$c_s^2\propto\rho^2$ falls faster below $z_{\rm match}$, dies anyway because the damage is done at $z\ge z_{\rm match}$, where the whole
background is as hot as a galaxy well (`condensate_mu_pincer_2026.py`, 20 checks).

## 4. What the theorem forces

**The pin.** At $\beta=1$ the DBI energy density decomposes exactly as $\rho=\mathcal Q_0 n+M^4\sqrt{1+\nu^2}$, the dust being the
charge term, and with $M^4=\rho_\Lambda$,
$$\frac{\rho_{\rm dust}}{\rho_\Lambda}=\frac{\nu}{R}\quad\Longrightarrow\quad R\equiv\frac{\Lambda_D}{\mathcal Q_0}=\nu_0\frac{\Omega_\Lambda}{\Omega_{\rm dm}}=2.6\,\nu_0 .$$
The programme had bounded $R$ as a free amplitude, $R\le1.5$–$3.1\times10^{-6}$ from a 3% tolerance on $P(k=0.2\,h\,{\rm Mpc}^{-1})$
and $\le2.3\times10^{-9}$ from the forest. Pinned, $R=5.6\times10^{-5}$ to $4.6\times10^{-4}$ across the committed window, 18–300 times
the ceiling; a two-fluid growth integrator that reproduces the $\Lambda$CDM growth integral to 0.2% and the programme's own 3%
calibration gives 44–100% suppression of $P(k=0.2)$. Two facts sit inside the kill: the pinned window maps to $\mu^{-1}=0.24$–$2.0$
Mpc, exactly the phenomenological megaparsec, so the theory's cosmological window and its galactic phenomenology agree with each
other; and the wall does keep the dust cold at recombination, $c_s^2(z_{\rm rec})\le10^{-13}$. The excess is entirely post-recombination.

**A second condensate.** If $\Omega_{\rm dm}$ is carried by a separate quadratic condensate $\chi$, the same relation applies:
cold at recombination needs $\mu_\chi^{-1}\le0.6$ kpc, shielding an $L^\star$ galaxy needs $\mu_\chi^{-1}\ge200$ kpc. A $\chi$ with
its own wall, unpinned, fails either the 3% at $k=0.2$ or the loose forest yardstick at every wall placement that reaches the shield.

**Constraint-only theories.** The remaining hope was a metric theory with two gravitational degrees of freedom in which the MOND
sector is built from nondynamical auxiliaries, filtered on cosmological scales by an elliptic auxiliary with a Hubble-scaled mass.
From the ADM action, the quadratic scalar action around de Sitter for GR plus such an auxiliary $\chi$ with every linear coupling
it can have, to the lapse ($c_\alpha$), the spatial curvature ($c_\zeta$) and the extrinsic curvature ($c_K$), integrates to a residual
$$L=A\,\dot\zeta^2-B\zeta^2+C\zeta\dot\zeta,\qquad A=\frac{c_\alpha^2\,a^3}{4H^2\,(k^2/a^2+m^2)},\qquad \dot C+2B=0 .$$
Coupling to the lapse frees exactly one scalar, dust-like, with a positive kinetic term that vanishes in the infrared; coupling to
$R^{(3)}$ or to $K$ frees none, but $R^{(3)}$ coupling splits lensing from dynamics and $K$ coupling vanishes in a static system. The
lapse is what matter and light both respond to, so a MOND boost with $\gamma=1$ requires the coupling that frees the mode. A
constraint-only two-degree-of-freedom metric MOND that lensing and dynamics both see does not exist at this order, and the third
field of TeVeS and AeST is forced (`elliptic_auxiliary_coupling_theorem_2026.py`).

**The merger meter.** Every medium that holds itself up in a well has a signal speed set by that support: at a solid's stall
$\mu s=\rho gr$ gives $c_T^2=gr/\ln\delta$, the polytrope has $c_s^2=|\Psi|$, a superfluid core has $c_s\sim v_c$. The Bullet cluster
moves its wells at 3000 km s$^{-1}$, Mach 3–7 within any of them. A supported medium re-pins on the crossing time and trails the
galaxies by $v_{\rm merge}L/c=0.5$–$1.5$ Mpc against an observed offset $\le50$ kpc; its elastic capacity falls 27 times short of the
collision energy; and no single-valued medium can pass through itself, while the Bullet's two dark peaks did. MOND with the
subcluster's stars supplies $2.3\times10^{13}\,M_\odot$ against a lensing peak of $2.3\times10^{14}$. Whatever carries the peak moved
ballistically with the galaxies (`merger_gate_supported_media_2026.py`). The strain-hardening dark solid built to evade the theorem
passed the background, the forest, the galaxy shield and the cluster mass at one parameter point, and died here.

**Ballistic and absent from galaxies.** Two known objects do that without pressure. A fuzzy scalar, whose de Broglie length
forbids halos below $M_{\min}$, needs $m\le6\times10^{-25}$ eV to leave an $L^\star$ galaxy halo-free and $\le1.3\times10^{-25}$ eV to
leave the radial acceleration relation mass-independent up to the most massive SPARC discs, while the CMB needs $m\ge10^{-24}$ eV: a
gap of 7–30. A light sterile fermion, Tremaine–Gunn-capped, has a real window, 5–11 eV, ordered by depth through Pauli exclusion; it
is dead if thermal ($\Omega h^2=m/94$ eV forces 11.3 eV and $\Delta N_{\rm eff}=1$) and its forest side, decided in a one-dimensional
sheet N-body where MOND is exact, falls 1000–5000 times short of the measured power at $k=1$–$10\,h\,{\rm Mpc}^{-1}$, $z=3$, for any
initial amplitude a baryon-only history can have, because the external field of the large-scale modes throttles the small-scale
boost. It is, in any case, a particle.

## 5. The dark charge, and where it shows

Call the component the *dark charge*: it is the conserved shift charge of the condensate, a property of the field. Three
independent data force its properties. The acoustic peaks need it pressureless at $\Omega_c h^2=0.120$ since before recombination
(the programme's own Boltzmann run, with $a_0$ switched off there). The Bullet cluster needs it ballistic. The forest needs it
clustering on 1–5 Mpc at $z=3$. A cold, ballistic component that clusters on those scales clusters into galaxies, and here the
theorem's consequence becomes a measurement.

The programme's kernel digs a well around every galaxy, and a cold charge at its required mean density falls in. Done with the
programme's own pieces, spherical collapse of charge shells in the framework's gravity, Newtonian background growth as its floor
requires, the MOND boost on the peculiar field only, the external-field effect of the surroundings included, a dwarf gathers
$10^{11}$–$10^{12}\,M_\odot$ out to 200–500 kpc and an $L^\star$ galaxy $1.7\times10^{13}\,M_\odot$ out to 900 kpc, 130 baryonic masses
inside 500 kpc, at the external field $e_N=0.03$ that isolated galaxies actually sit in. Inside the deep-MOND regime of the dwarfs
this adds only $+0.10$ to $+0.15$ dex to the rotation curves, against a measured room of $+0.05$ to $+0.09$: a marginal excess. But
galaxy–galaxy lensing measures the accreted charge directly. Put into the framework's own lensing prediction, $\gamma=1$ as its AeST
embedding has it, and confronted with Brouwer et al.'s KiDS-1000 isolated-lens radial acceleration relation with its full covariance
and the $\pm0.3$ dex amplitude systematic profiled, the accreted charge multiplies the lensing signal at 100 kpc–1 Mpc by 3–20 at
$e_N=0.03$–$0.1$ and is excluded at $\Delta\chi^2\ge+100$ on both footings. Only an external field of order $a_0$ itself, which no
isolated lens has, throttles the accretion to 8–19 baryonic masses inside 500 kpc and lets the amplitude budget absorb the rest
(`dark_charge_kids_lensing_gate_2026.py`). Both ways are recorded.

That is the double count, measured with existing data and the programme's own pieces: the cold charge at $\Omega_c$ and MOND wells
around galaxies are incompatible in galaxy–galaxy lensing at realistic environments, unless the charge does not fall in, and every
kinetic reason for it not to fall in has now been closed by the theorem, the coupling theorem and the merger meter.

## 6. What survives, and what it predicts

**One acceleration scale for every galaxy.** Fitting the programme's kernel to 147 SPARC rotation curves, the per-galaxy $a_0$
scatters by 0.275 dex with a mass slope of $+0.07$; a mock of one universal $a_0$ carrying the full SPARC error budget (velocities,
distances, inclinations, 0.1 dex in mass-to-light) scatters by 0.30–0.31 dex with slope $+0.03$ to $+0.04$. The implied intrinsic
spread is 0.00 dex on both footings. A plain abundance-matched halo population with its concentration and stellar-mass scatter
gives 0.45 dex and slope $+0.23$ under the same error budget (`rar_origin_detector_2026.py`). Hydrodynamical simulations with
feedback claim to tighten the relation to 0.05–0.09 dex; that is the standard defence and it is stated here rather than hidden.

**The scale cannot rise with redshift.** $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE}(0)}$ exactly, independent of $\kappa$ and of
the footing: flat to $<1\%$ for $z\le5$ if $\Lambda$ is constant, 0.87 at $z=2$ and 0.78 at $z=3$ on DESI DR2's $w_0w_a$, and within
$\pm20\%$ of today out to $z=3$ for any allowed constant $w$. The emergent acceleration scale of cold-dark-matter halos rises,
$a_s\propto E(z)^{4/3}c^2/f(c)$, by 1.8 at $z=2$ and 2.6 at $z=3$; to mimic a flat $a_0$ its haloes would have to be diluted to 0.61
and 0.40 of their N-body concentrations. Added as a fourth zero-parameter law to the programme's joint likelihood over ten committed
high-redshift constraints, the two are undecided and prior-dominated on present data.

**The decisive measurement.** The deep-MOND Tully–Fisher zero-point at $z\simeq2.5$: the framework predicts 0.00 dex
($-0.09$ with DESI's dark energy), the emergent halo scale $+0.33$ dex; one clean low-acceleration rotator measured to $\pm0.13$ dex
decides at 20:1. The Gaia DR4 wide-binary boost, pre-registered and hash-stamped at $\gamma_v=1.1614$–$1.1814$ canonical and
$1.1917$–$1.2267$ alternative against Newton's exactly 1.00, is the second.

## 7. Discussion

The theorem is short and its reach is wide. It applies to every dark sector that is a clock: AeST's scalar, mimetic dark matter,
the khronon, $k$-essence dust, the DBI condensate, and, through the merger meter and the thermalisation argument, the superfluid,
because any self-interaction that thermalises halos thermalised the background earlier. What it leaves is exactly the field
content the completions were built to avoid: a genuinely dynamical component, cold and ballistic, that is not a clock, together
with a reason, not yet found, for it to stay out of the wells the kernel digs. The two escapes the theorem itself names, a medium
whose stiffness depends on shear rather than on its local state, and a medium that superposes, were both built and both closed,
one by the merger meter and one by the CMB against the radial acceleration relation's mass-independence.

What the programme owns after this is narrower than it once claimed and sharper than it was: a scale set by the dark-energy
density, a universality of that scale across galaxies that a plain halo population does not reproduce, a prediction for its
evolution that the dark-matter alternative contradicts in sign, and a dark sector with a measured specification and a single
unmet demand. Two named measurements decide it.

## Methods

Every number is produced by a committed script with checks that can fail, a mutation control, and both $a_0$ footings, under
`qwen_claude_field_theory/closure_2026/condensate_pincer_2026/` and `prep_2026/rar_origin_2026/`: `condensate_mu_pincer_2026.py` (20),
`mond_growth_framework_footing_2026.py` (7), `superfluid_route_gates_2026.py` (4), `rising_a0_baryon_only_gate_2026.py` (5),
`cmc_filter_no_dm_growth_gate_2026.py` (5), `cmc_filter_scalar_dof_gate_2026.py` (6), `elliptic_auxiliary_coupling_theorem_2026.py` (3),
`dark_solid_first_gates_2026.py` (5), `merger_gate_supported_media_2026.py` (4), `ballistic_survivor_window_2026.py` (3),
`mond_sheet_nbody_forest_gate_2026.py` (4), `rar_origin_detector_2026.py` (3), `dark_charge_dwarf_capture_framework_native_2026.py` (3),
`dark_charge_kids_lensing_gate_2026.py` (3). Yardsticks are taken at their loose ends throughout. Three corrections were made in the
open during the work and are recorded in the repository's ledger: a per-mode linear model of the MOND boost that ignored the
external-field effect was withdrawn in favour of the exact one-dimensional dynamics; a dwarf-galaxy exclusion that had used
$\Lambda$CDM's abundance-matching ratio was downgraded to marginal when redone with the framework's own gravity; and an
overstatement that $a_0$ "cannot rise" was replaced by the precise statement of Section 6.

## References

Bekenstein, J. D. 2004, Phys. Rev. D 70, 083509. Berezhiani, L. & Khoury, J. 2015, Phys. Rev. D 92, 103510. Brouwer, M. M. et al. 2021,
A&A 650, A113. Clowe, D. et al. 2006, ApJ 648, L109. Chae, K.-H. et al. 2020, ApJ 904, 51. Deffayet, C., Esposito-Farèse, G. & Woodard,
R. P. 2011, Phys. Rev. D 84, 124054. Durakovic, A. & Skordis, C. 2024. Hlozek, R. et al. 2015, Phys. Rev. D 91, 103512. Iršič, V. et al.
2017, Phys. Rev. D 96, 023522. Lelli, F., McGaugh, S. S. & Schombert, J. M. 2016, AJ 152, 157. Markevitch, M. 2006, ESA SP-604.
Milgrom, M. 1983, ApJ 270, 365. Skordis, C. & Złośnik, T. 2021, Phys. Rev. Lett. 127, 161302. Springel, V. & Farrar, G. R. 2007, MNRAS
380, 911. Tremaine, S. & Gunn, J. E. 1979, Phys. Rev. Lett. 42, 407. Viel, M. et al. 2013, Phys. Rev. D 88, 043502. This programme:
Zenodo 10.5281/zenodo.22242701 (v2 22254075); 10.5281/zenodo.22253953 (v2 22255522); 10.5281/zenodo.21895046.
