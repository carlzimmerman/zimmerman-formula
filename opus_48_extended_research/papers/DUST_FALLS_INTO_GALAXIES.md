---
title: "Dust Falls into Galaxies: why one equation of state cannot be dark matter on the sky and absent in the disc"
journal: "Crispy Fried Chicken Scientific Review, Vol. 1, No. 1 (September 2026)"
author: "C. P. Zimmerman"
affiliation: "Briar Creek Tech"
email: "carl@briarcreektech.com"
date: "2 September 2026"
---

**Abstract.** A relativistic completion of MOND needs an $\Omega_{\rm dm}$-worth of pressureless energy to reproduce the
acoustic peaks and the 100-Mpc clustering, and it needs that energy to stay out of galaxies so that the MOND boost and a
dark halo are not counted twice. The de Sitter–MOND framework, built on the Aether Scalar Tensor (AeST) chassis with a
condensate clock $K(Q)$, hoped to do both with one field. We show that the field's own static limit forbids it. The
condensate is a $\gamma=2$ polytrope whose sound speed in a potential well is the well depth, $c_s^2=|\Psi|c^2$, and the
same relation read on the cosmic background fixes $c_s^2(z)=4\pi G\rho_{\rm dm}(z)/\mu^2$ with the same Helmholtz mass
$\mu$ that governs galaxies. At $\beta=1$ the DBI amplitude is then pinned, $R=\Lambda_D/Q_0=\nu_0\Omega_\Lambda/\Omega_{\rm dm}$,
18–300 times above the framework's own power-spectrum ceiling. A second, independent condensate fares no better: cold at
recombination needs $\mu^{-1}\le0.6$ kpc, shielding an $L^\star$ galaxy needs $\mu^{-1}\ge200$ kpc. Underneath both lies a
$K$-independent matching theorem: a galaxy well today is the cosmic background at $(1+z_{\rm match})^3=\delta_{\rm well}$,
with identical sound speed, so the Lyman-$\alpha$ forest at $z=3$ measures the dust inside galaxies now, and finds it cold.
The superfluid route, in which the dust itself makes the MOND force, closes on its own hinge: any self-interaction that
thermalises halos thermalised the background earlier. What survives is $a_0\propto\sqrt{\rho_{\rm DE}(z)}$, MOND
phenomenology, and cold dark matter. Every claim is a committed script with checks that can fail, a mutation control,
and both $a_0$ footings.

## 1. The dish we were trying to cook

MOND works in galaxies with one number, $a_0\simeq1.2\times10^{-10}$ m s$^{-2}$, and the radial acceleration relation
(RAR) has 0.034 dex of intrinsic scatter. The framework under test adds two things. First, a coefficient:
$$a_0=\tfrac{c}{2}\sqrt{G\rho_\Lambda}=c^2\sqrt{\Lambda/32\pi},\qquad \kappa\equiv a_0/(c\sqrt{G\rho_{\rm DE}})=\tfrac12,$$
which puts $a_0$ at $9.36\times10^{-11}$ m s$^{-2}$ on the canonical footing and $1.13\times10^{-10}$ on the alternative
$cH_0/Z$ footing, $Z=\sqrt{32\pi/3}$. Second, a prediction: if $a_0$ tracks the dark-energy density, then
$a_0(z)\propto\sqrt{\rho_{\rm DE}(z)}$, which with DESI DR2's $w_0w_a$ is a 13% decline by $z=2$. Nothing in $\Lambda$CDM
says that.

A full theory has to do the cosmic microwave background (CMB). The third acoustic peak needs pressureless gravitating
energy at full $\Omega_{\rm dm}$ that photons do not feel; removing it moves the third-to-first peak ratio by 54%. Skordis
and Złośnik's AeST theory (2021) was the first relativistic MOND theory to fit the CMB, and it did so because the scalar's
potential minimum produces exactly such a dust. The framework's completion, "v9", is AeST with a condensate clock:
$$K(Q)=-M^4+\mu_D^2\Lambda_D^2\Big[1-\sqrt{1-u^2/\Lambda_D^2}\Big],\qquad u\equiv Q-Q_0,$$
a Dirac–Born–Infeld wall. With $\beta\equiv\mu_D^2\Lambda_D^2/M^4=1$ the Lagrangian vanishes at the wall, and the
conserved shift charge $n=K'(u)\propto a^{-3}$ defines $\nu\equiv n/(\mu_D^2\Lambda_D)=\nu_0(1+z)^3$. The clock does three
jobs at once: $M^4=\rho_\Lambda$ is the dark energy, $Q_0 n$ is the dust, and the wall switches MOND off at
recombination through
$$\frac{a_0^2(z)}{a_0^2(0)}=\frac{\sqrt{1+\nu_0^2}}{\sqrt{1+\nu_0^2(1+z)^6}},$$
flat to below 1% for $z\le5$ and off by $z\sim100$, with $\nu_0\in[2.1\times10^{-5},1.8\times10^{-4}]$ committed.

The hope, stated in the framework's own files, was the "dark matter illusion": the same field that is dust on the sky
would sit at negligible density inside galaxies, leaving MOND alone to fit rotation curves. This paper is the story of
why that hope fails, on the framework's own terms, and what the failure teaches.

## 2. The polytrope: the new equation, and the paper it made

Take the static limit. The clock's time translation fixes the lapse: $Q=Q_0(1-\Psi)$, so $u=-Q_0\Psi$ exactly, for any
$K$. Near the minimum, $K\simeq-M^4+K_2u^2$, the pressure and density of the $Q$-sector are $p=K/(8\pi\tilde G)$ and
$\rho=(QK'-K)/(8\pi\tilde G)$ with $\tilde G=(1-K_B/2)G$. Eliminating $u$,
$$p_d=\frac{2\pi G}{\mu^2}\,\rho_d^2,\qquad c_s^2=\frac{dp_d}{d\rho_d}=\frac{4\pi G\rho_d}{\mu^2}=\frac{u}{Q_0+u}\simeq|\Psi|\,c^2,$$
where $\mu^2=2K_2Q_0^2/(2-K_B)$ is the Helmholtz mass of the static AeST equations. The condensate is a $\gamma=2$
polytrope, Lane–Emden index $n=1$, and its sound speed in a well is the depth of the well. Hydrostatic equilibrium of
this fluid in the potential it helps source is
$$\nabla^2\Psi+\mu^2(\Psi-C)=4\pi G\rho_b,$$
which is the Helmholtz equation of Durakovic and Skordis with a Bernoulli constant $C$: the "phantom" density
$\rho_d=-\mu^2\Psi/4\pi G$ is the polytrope sitting in its own well, and $C$ is the captured mass. The $n=1$ polytrope
has a radius $\pi/\mu$ independent of its central density, the free surface where the pressure vanishes, and branches
with nodes are excluded because $\rho_d<0$ there means $c_s^2<0$, a gradient instability.

Read inside a cluster the polytrope is a lever. Because the dust is ordered by potential depth rather than density, a
cluster well pins a core of it. The committed calculation gives a core of $2.3$–$3.2\times10^{13}\,M_\odot$, 23–33% of
the missing mass, with $\eta(R_{500})=2.6$–$3.2$ still to explain, hydrostatic Mach number 0.10, and the DBI wall never
hit inside the committed $\nu_0$ window. That result was deposited (Zenodo 10.5281/zenodo.22242701, v2 22254075).
Its algebra stands. Its cosmology, we now show, does not.

## 3. The same equation on the sky

Nothing in the derivation above used the well. The relation $c_s^2=4\pi G\rho_d/\mu^2$ holds wherever the quadratic
approximation holds, and on the cosmic background today $\nu_0\sim10^{-4}$ puts the field deep inside it. With
$\rho_d=\Omega_{\rm dm}\rho_{\rm crit}$,
$$c_s^2(z)=\frac{4\pi G\rho_{\rm dm}(z)}{\mu^2c^2}=2.0\times10^{-8}\Big(\frac{\mu^{-1}}{1\ {\rm Mpc}}\Big)^2(1+z)^3\quad\text{until saturation},$$
which is $(43\ {\rm km\,s^{-1}})^2$ today at $\mu^{-1}=1$ Mpc, the value AeST phenomenology needs so that the Helmholtz
oscillation does not spoil rotation curves. The galaxy-scale behaviour of the dust and its cosmological behaviour are one
number.

The DBI form makes the full history exact. With $s=u/\Lambda_D=\nu/\sqrt{1+\nu^2}$ and $R\equiv\Lambda_D/Q_0$,
$$c_s^2=\frac{K'}{QK''}=\frac{R\,s(1-s^2)}{1+Rs},$$
which rises as $(1+z)^3$, peaks at $s=1/\sqrt3$ with value $0.385R$, and falls to zero at the wall. The repo bounded $R$
as a free amplitude: $R\le1.5$–$3.1\times10^{-6}$ from a 3% tolerance on $P(k=0.2\,h\,{\rm Mpc}^{-1})$, and $R\le2.3\times10^{-9}$
from the forest. But at $\beta=1$ the energy density decomposes exactly as
$$\rho=Q_0n+M^4\sqrt{1+\nu^2},$$
the dust being the charge term, and with $M^4=\rho_\Lambda$ this gives
$$\frac{\rho_{\rm dust}}{\rho_\Lambda}=\frac{Q_0\nu}{\Lambda_D}=\frac{\nu}{R}\quad\Longrightarrow\quad R=\nu_0\frac{\Omega_\Lambda}{\Omega_{\rm dm}}=2.6\,\nu_0 .$$
$R$ is not free. Over the committed window:

| $\nu_0$ | $R$ pinned | $R$ / ceiling | $c_s^2(0)$ | $\mu^{-1}$ equiv. | peak $c_s^2$ | $z_{\rm peak}$ | $P(k{=}0.2)$ suppressed |
|---|---|---|---|---|---|---|---|
| $2.1\times10^{-5}$ | $5.6\times10^{-5}$ | 18 | $1.2\times10^{-9}$ | 0.24 Mpc | $2.1\times10^{-5}$ | 31 | 44% |
| $1.0\times10^{-4}$ | $2.6\times10^{-4}$ | 169 | $2.6\times10^{-8}$ | 1.14 Mpc | $1.0\times10^{-4}$ | 18 | 100% |
| $1.8\times10^{-4}$ | $4.6\times10^{-4}$ | 299 | $8.1\times10^{-8}$ | 2.0 Mpc | $1.8\times10^{-4}$ | 15 | 100% |

The last column is from a two-fluid sub-horizon growth integrator, baryons pressureless and dust with $c_s^2(a)$,
which reproduces the $\Lambda$CDM growth integral to 0.2% and reproduces the repo's own calibration (3.0% at
$k=0.2$ when $R=3.06\times10^{-6}$). Two facts inside the kill deserve saying. The pinned window maps to
$\mu^{-1}=0.24$–$2.0$ Mpc, exactly AeST's phenomenological megaparsec, so the framework's cosmological window and its galaxy
phenomenology agree with each other. And the wall does its job: $c_s^2(z_{\rm rec})\le10^{-13}$ for every pinned $\nu_0$,
so the excess is entirely post-recombination. The cluster paper's parameters, $\bar\rho_d=\Omega_{\rm dm}\rho_{\rm crit}$
at $\mu^{-1}=1$ Mpc, are this pinned sector at $\nu_0=8.8\times10^{-5}$.

A mutation control: identify the dust with the internal-energy branch $M^4(\sqrt{1+\nu^2}-1)$ instead of the charge, and
the pin disappears while $\nu_0$ is forced to 0.88, four orders outside the window. The pin exists only because the dust
is the charge, which is the framework's own filter F1.

## 4. A second condensate does not help

Suppose instead that $\Omega_{\rm dm}$ is carried by a separate quadratic condensate $\chi$ with its own Helmholtz mass
$\mu_\chi$, the khronon keeping only the trace dust needed for the $a_0(z)$ switch. The relation of Section 3 applies
verbatim. Two requirements pull opposite ways.

| $\mu_\chi^{-1}$ | $c_s^2(z_{\rm rec})$ | $T^2(k{=}10,z{=}3)$ | $T^2(k{=}0.2,z{=}0)$ | polytrope $M_\chi(<30\,{\rm kpc})/M_b$ |
|---|---|---|---|---|
| 0.3 kpc | $2.3\times10^{-6}$ | 0.16 | 0.999 | no pressure support inside 30 kpc |
| 3 kpc | $2.3\times10^{-4}$ | 0.004 | 0.94 | no pressure support inside 30 kpc |
| 100 kpc | 0.15 | 0.000 | 0.02 | 0.33 / 0.36 |
| 200 kpc | 0.25 | 0.000 | 0.00 | 0.098 / 0.108 |
| 1 Mpc | 0.33 | 0.000 | 0.00 | 0.005 / 0.006 |

Cold at recombination, taking the loose end of the generalised-dark-matter range $c_s^2(z_{\rm rec})\le10^{-5}$, needs
$\mu_\chi^{-1}\le0.6$ kpc. Shielding an $L^\star$ galaxy, meaning the polytrope dust inside 30 kpc is at most 30% of
the baryons (about 0.1 dex on $g$, both $a_0$ footings, using the framework's own $g=\sqrt{g_b^2+g_ba_0}$), needs
$\mu_\chi^{-1}\ge200$ kpc; at 10% it needs a megaparsec. The gap is a factor 300 at the loose ends. The forest already
objects at 3 kpc. A $\chi$ with its own DBI wall and its own $M_\chi^4$, unpinned, can be cold at recombination, but
every wall placement that reaches the shield floor fails either the 3% at $k=0.2$ or the loose forest yardstick
$T^2(10\,h\,{\rm Mpc}^{-1},z{=}3)\ge0.5$. And a constant $c_s^2$ equal to today's value at $\mu^{-1}=100$ kpc leaves
$T^2(10,3)=0.93$: the kill is the $(1+z)^3$ history, not today's sound speed.

## 5. The matching theorem

Both horns are instances of one statement that does not depend on the shape of $K$. The sound speed
$c_s^2=K'/(QK'')$ is a function of the excitation $u$ alone. A static well imposes $u_{\rm well}=-Q_0\Psi$, the lapse
relation, for any $K$. The background carries a conserved charge, $n(z)=K'(u(z))=n_0(1+z)^3$. The dust density is $Q_0n$
in both places, so the well's dust overdensity is $\delta_{\rm well}=n_{\rm well}/n_0$, and
$$(1+z_{\rm match})^3=\delta_{\rm well}:\qquad c_s^2\big|_{\rm background}(z_{\rm match})=c_s^2\big|_{\rm well}.$$
A shield-compatible well holds at most a few thousand times the mean dust density, from the mass budget alone, so
$z_{\rm match}\le16$. For $K\propto u^p$ with $p=2,3,4,8$ the background at $z=3$ then has $c_s\ge20$ km s$^{-1}$
wherever a shield exists, an order of magnitude above what the forest tolerates. The non-analytic superfluid minimum
$K\propto|u|^{3/2}$, whose $c_s^2\propto\rho^2$ falls faster, is colder than the forest at $z=3$ (3.6 km s$^{-1}$ at
$\delta_{\rm well}=5000$) and dies anyway, because the damage is done at $z\ge z_{\rm match}$ where the whole background
is as hot as a galaxy well, 283 km s$^{-1}$ for that $K$.

The theorem turns an unanswerable question, "does the dust fall into galaxies?", into a measured one. The dust at $z=3$
is the dust inside a galaxy well today. The forest says the dust at $z=3$ is cold. Therefore it falls in.

## 6. Is the yardstick $\Lambda$CDM's or the framework's?

The growth yardsticks above assume the dark fluid grows structure by Newtonian linear growth. The framework's own
covariant perturbation theory settles whose assumption that is: the kernel argument seen by the linear growing mode
carries a de Sitter–Unruh Hubble floor,
$$X=Z^2\Big(\frac{H(z)}{H_\Lambda}\Big)^2+\Big(\frac{a_{\rm pec}}{a_0}\Big)^2,$$
and with it MOND changes linear growth by at most 6% at every scale and redshift, both footings. The yardsticks are the
framework's, and the pinned sector underproduces the measured clustering by 40–600 times at $k\ge0.2\,h\,{\rm Mpc}^{-1}$.

Drop the floor, as a Nusser–Sanders MOND cosmology would, and something surprising happens: warm dust plus MOND-grown
baryons land within a factor 2 of the measured $z=3$ power at $k=1$–$10\,h\,{\rm Mpc}^{-1}$, where the Newtonian run is
300–600 times low. But the same boost acts on the 100-Mpc scales where the dust does cluster, overproducing them 5–13
times at $z=3$ and driving them nonlinear by today, for every $\mu^{-1}$ from 0.1 to 5 Mpc. A universe with no dark
field at all is tilted 30–200 times in power between $k=0.05$ and $10\,h\,{\rm Mpc}^{-1}$ relative to the measured
shape, whichever way the floor is set. Nothing in the framework boosts $k\gtrsim1$ without boosting $k\approx0.05$.

## 7. The superfluid route, and its hinge

If the dust cannot be kept out of galaxies, let it be the MOND force. In Berezhiani and Khoury's superfluid, phonons
couple to baryons with $a_0=\alpha^3\Lambda^2/M_{\rm Pl}$. Set the superfluid scale to the dark-energy scale,
$\Lambda=\rho_{\rm DE}^{1/4}=2.24$ meV, and the map onto the framework is exact:
$$\alpha^3=\frac{\kappa}{\sqrt{8\pi}}\quad\Rightarrow\quad\kappa=\tfrac12\ \text{gives}\ \alpha=0.464\ (0.79\ \text{non-reduced}\ M_{\rm Pl}),$$
an ordinary coupling. That gate opens. The next shuts. The route needs the dark fluid in the normal phase on the cosmic
background. The thermalisation rate $\Gamma=\rho\,(\sigma/m)\,v$ against $H$ scales as $(1+z)^{5/2}$ into the past, so any
self-interaction strong enough to thermalise an inner halo ($\sigma/m\ge0.1$–$1$ cm$^2$ g$^{-1}$) thermalised the entire
background earlier, at $z_{\rm th}=78$–$31000$ for relic velocities from 100 km s$^{-1}$ down to 1 m s$^{-1}$, where
$n\lambda_{\rm dB}^3\gg1$. It condensed, and since $T/T_c$ is constant under expansion it stayed condensed. A condensed
background with $P\propto\rho^3$, anchored to any galaxy core the phonons could support, has $c_s^2(z_{\rm rec})$
between $2\times10^{-3}$ and $1/3$ and $c_s=10$–$200$ km s$^{-1}$ at $z=16$–$45$. Being CMB-cold would need a core sound
speed below 1 km s$^{-1}$, a superfluid 200 times too soft to hold up a 200-km s$^{-1}$ core. One equation of state
cannot be MOND in galaxies and cold dark matter on the sky.

## 8. What is left on the plate

Three things stand, and they are worth stating plainly.

The coefficient and its evolution, $a_0=\tfrac c2\sqrt{G\rho_{\rm DE}(z)}$, are untouched by everything above. They are
the only content in the framework that $\Lambda$CDM cannot reproduce, and they carry two named measurements: the
deep-MOND Tully–Fisher zero-point at $z\approx2.5$, where the framework predicts $0.00$ dex and $\Lambda$CDM's emergent halo
scale predicts $+0.33$ dex, decided at 20:1 by one clean point at $\pm0.13$ dex; and the Gaia DR4 wide-binary boost,
$\gamma_v=1.16$–$1.23$ against Newton's exactly 1.

MOND phenomenology in galaxies stands, with 0.034 dex of scatter that no halo model has matched.

And an $\Omega_{\rm dm}$-worth of something that is cold above a kiloparsec stands, because the CMB, the 100-Mpc clustering,
and now the polytrope all say so. It falls into galaxies. The framework's problem is the one MOND-plus-halos always had,
a 2.7–4.4 times overshoot from counting the boost and the halo together, and no kinetic mechanism is left to prevent it.
The cluster phase-pinning cosmology is withdrawn accordingly, its static algebra kept.

## Methods

Every number above is produced by a committed script with checks that can fail, a mutation control, and both $a_0$
footings: `condensate_mu_pincer_2026.py` (20 checks), `mond_growth_framework_footing_2026.py` (7),
`superfluid_route_gates_2026.py` (4), `itemC_phase_pinning_dynamics_2026.py` (27), `itemD_dbi_wall_core_2026.py` (6),
all under `qwen_claude_field_theory/closure_2026/`. Yardsticks were taken at their loose ends: 30% of the baryons for the
shield, $c_s^2(z_{\rm rec})\le10^{-5}$ for the CMB, $T^2\ge0.5$ at $k=10\,h\,{\rm Mpc}^{-1}$, $z=3$ for the forest (the
3-keV warm-dark-matter half-mode class), and the repo's own 3% at $k=0.2$. The growth integrator is sub-horizon,
two-fluid, DOP853 at $10^{-8}$ relative tolerance, initialised in the growing mode at $z=1000$; the MOND-boosted variant
evaluates the framework's interpolation at the mode's rms peculiar gravity $g_N=4\pi G\bar\rho_m|\delta_m|/k_{\rm phys}$.
The Berezhiani–Khoury equation-of-state normalisation is used only to quote a particle mass ($m\simeq0.7$ eV) and is
flagged as recalled; no kill depends on it.

## References

Bekenstein, J. D. 2004, Phys. Rev. D 70, 083509. Berezhiani, L. and Khoury, J. 2015, Phys. Rev. D 92, 103510.
Böhmer, C. G. and Harko, T. 2007, JCAP 06, 025. Deffayet, C., Esposito-Farèse, G. and Woodard, R. P. 2011, Phys. Rev. D 84,
124054. Durakovic, A. and Skordis, C. 2024 (static AeST solutions). Iršič, V. et al. 2017, Phys. Rev. D 96, 023522.
Mayer, A. C. et al. 2023, MNRAS (Magneticum apparent-$a_0$ rise). Milgrom, M. 1983, ApJ 270, 365; 2009, Phys. Rev. D 80,
123536; 2017, arXiv:1703.06110. Nusser, A. 2002, MNRAS 331, 909. Sanders, R. H. 2001, ApJ 560, 1. Skordis, C. and
Złośnik, T. 2021, Phys. Rev. Lett. 127, 161302. Thomas, D. B., Kopp, M. and Skordis, C. 2016, ApJ 830, 155. Verlinde, E. P.
2017, SciPost Phys. 2, 016. Viel, M. et al. 2013, Phys. Rev. D 88, 043502. This framework: Zenodo 10.5281/zenodo.22242701
(cluster phase pinning, v2 22254075); 10.5281/zenodo.22253953 (nonlocal kernel instability, v2 22255522).
