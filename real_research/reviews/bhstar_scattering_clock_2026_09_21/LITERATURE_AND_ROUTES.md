# Executed routes and bounded literature check — 2026-09-21

## 1. Actual catalogue: photon conservation and a putative 1/15 law

Input: [de Graaff et al., arXiv:2511.21820v2](https://arxiv.org/html/2511.21820v2)
and its [Zenodo v2 data release](https://zenodo.org/records/21977747), published
2026-08-17. The FITS file and original field definitions are retained under
`data/`, with attribution to de Graaff et al. The release gives 181 entries,
146 unique objects, and percentile columns [5,16,50,84,95]. Use `use_dG26` and
median index 2; do not treat duplicates as independent objects. The release's
published FITS MD5 is a7055bc0a466628a212dd13640f88969. SHA256 is
8a319c5c4ba2700475247bf4a70e42baeb6d2e03b5a25365efd82808e52ed91c.

Decision: the median ratio 0.06777 is close to 1/15, but that was noticed after
inspection. It is not a preregistered prediction. The paper already fits the
H-alpha–blackbody luminosity relation. Its modified-blackbody temperatures are
not the physical atmosphere temperatures in the separate Sun study.

An explicit energy countermodel blocks a unique constant. For ionizing photons
with mean energy E_i and illustrative yield y H-alpha photons per absorbed
ionizing photon, the line energy fraction is f=y E_Ha/E_i. If a fraction eta of
the remaining energy emerges in the fitted thermal component, then

    L_Ha/L_thermal = f/[eta(1-f)].

Both E_i and eta vary. Even fixed y=0.45 and E_i=13.6 eV give ~1/15 only after
assuming eta=1; these assumptions are not established in dense LRD gas. The
script evaluates twelve distinct energy budgets. Collisional excitation,
resonance conversion, host emission and non-Case-B conditions add freedom.

A 4662-K Planck source under a toy Case-B conversion supplies H-alpha/bolometric
<=7.87e-13, vastly smaller than the catalogue ratio. This only rejects the toy
idea that the visible cool continuum alone supplies the ionizations. It does
not distinguish a buried hot engine from external stars, nor is it a new
discovery. [Asada et al.](https://arxiv.org/html/2601.10573v2) already investigate
the energy origins of UV and Balmer emission across LRD/LBD samples.

## 2. Atomic cascade: Balmer–Paschen conversion

The attempted new observable was photon conservation under H-beta absorption
followed by Pa-alpha plus H-alpha emission. It is attractive because energy
conservation fixes E_Hbeta=E_Paalpha+E_Halpha. But conversion probabilities,
other cascades and line escape enter the population relation.

The primary-source check found this process explicitly treated by
[Chang et al., arXiv:2508.08768](https://arxiv.org/abs/2508.08768), and
[ATLAS III, arXiv:2608.10832v1](https://arxiv.org/html/2608.10832v1) already tests
Balmer/Paschen ratios with dense-gas and dust models. Thus the proposed route
does not support an original universal law. [Paschen Jumps,
arXiv:2604.09399v1](https://arxiv.org/html/2604.09399v1) is also relevant to the
continuum interpretation; it is not used as a numerical input here.

## 3. Gravity convention: do not double-count radiation

[Sun et al., arXiv:2609.09274v1, sections 2.2 and 3.1](https://arxiv.org/html/2609.09274v1)
explicitly fits g_net=g_true-g_dyn; radiative acceleration is already included
separately in the adopted atmosphere structures. The source describes a
continuum fit and a dynamical-support caveat. It does not provide an independent
line-wing measurement of Newtonian gravity for each of 117 objects.

Therefore the campaign's Gamma expression remains conditional on the dynamical
interpretation. However, the tempting replacement Gamma -> Gamma/(1+Gamma)
would also be wrong here: it mistakes g_net for a gas-pressure-only gravity and
double-counts radiation. That proposed shortcut was rejected before being used.
The previous phase-gravity report already covers the actual dynamical ambiguity;
relabeling that correction as another breakthrough would repeat the failure.

## 4. Scattering and time response: surviving conditional result

[Rusakov et al., Nature 2026](https://www.nature.com/articles/s41586-025-09900-4)
model broad LRD lines with electron scattering and discuss columns, temperatures
and density-dependent sizes. [TWINKLE, arXiv:2604.13000v1](https://arxiv.org/html/2604.13000v1)
reports no detected variability for its 18-LRD sample over 140–220 rest-frame
days, and discusses scattering among possible explanations. Their observations
do not independently measure the impulse response assumed in our illustration.

[Modelevsky et al., arXiv:2608.05283v1](https://arxiv.org/html/2608.05283v1)
already derive scattering line profiles and explicitly distinguish externally
illuminated scattering from intrinsic line formation. Absorption in their
intrinsic models matters. Our conservative-photon theorem must not be applied
to their full absorption/re-emission problem without a new derivation.

The spectral/time connection is established Comptonization physics, not an
unclaimed discovery: see [Becker 2003, MNRAS 343, 215](https://academic.oup.com/mnras/article/343/1/215/1031718)
for time-dependent thermal Comptonization, photon escape and line evolution.
We derive the narrower moment identity directly, then combine it with a simple
characteristic-function bound. Neither the proof nor a search failure proves
that this exact inequality is globally new.

Bounded search: arXiv primary texts above and queries combining electron
scattering, residence/escape time, variance, line width, smoothing, variability,
and little red dots. Repository search covered the BH-star review/campaign
scripts, BH-star papers and I-series Lean files. No matching exposure identity
or amplitude bound was found there. This is a bounded repo finding only.

## Decision

No candidate passed all three requirements: independent observational closure,
nontrivial predictive content, and substantiated novelty. The scattering result
has predictive content conditional on measurements and geometry, and is retained
at exactly that status. The catalogue and failed routes are preserved so the
same coincidences are not proposed again as discoveries.
