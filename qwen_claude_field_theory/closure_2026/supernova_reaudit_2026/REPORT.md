# Supernova revisit: full covariance and the actual acceleration-scale test

2026-09-08. **Finite likelihood reproduced; no completed-theory prediction.**
Only this new directory was written. Old scripts, catalogues and outputs were
left intact. This calculation uses GR FLRW distance laws as explicit hypotheses;
it does not claim that an IC action has derived that cosmology.

**This is a baseline using the release's already corrected luminosities and
redshifts. It does not test or refute Sarkar's alternative age corrections,
redshift-frame choices, or directional model.** Reproducing this baseline does
not adjudicate the June 2026
[Sah, Rameez and Sarkar analysis](https://academic.oup.com/mnras/article/549/3/stag844/8701424)
or the different age-systematics arguments in
[Wiseman et al.](https://academic.oup.com/mnras/article/549/3/stag797/8703725).
Those require their actual alternative corrections and likelihoods on common
data; no such alternative likelihood was executed in this bounded audit.

## What the old supernova calculation actually measured

The old `prep_2026/sne_lambda/predict_diagram.py` uses
`E²=Om(1+z)³+OL`, fixes `Om=.334` from a supernova result, permits `Om+OL!=1`,
uses the flat distance formula, and fits an arbitrary magnitude intercept.
Put `s=Om+OL`. Its distance is exactly `1/sqrt(s)` times the ordinary flat
LCDM distance with `Om_eff=Om/s`. The arbitrary intercept absorbs that factor.
Thus its likelihood tests **a reparameterized flat-LCDM matter fraction**,
not curvature or overclosure. Its reference H0 is not the Hubble rate at z=0
unless `s=1`. Using a genuinely curved FLRW distance is a different calculation.
The old phrase zero-SNe-fitted parameters also obscures its use of an Om value
already inferred from SNe, in addition to its fitted intercept.

The old `prep_2026/a0z_from_sne/crossscale.py` obtains its headline a0(0)
from `(c/Z)H0 sqrt(1-Om)` before reading a supernova magnitude. For its chosen
Planck-like Om=.315 and H0=67.4, the agreement with 9.36e-11 is an input identity,
not an independent SNe reconstruction. Its high-redshift a0 conversion further
assumes the Friedmann equation, spatial flatness, matter subtraction and the
proposed acceleration-density relation. z=3 is outside the supplied SNe range.

## Authoritative data and covariance

The bounded local file search found both existing Pantheon+ tables but no
Pantheon+ covariance. The official [release directory](https://github.com/PantheonPlusSH0ES/DataRelease/tree/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR)
provides the 1701-by-1701 STAT+SYS covariance, now downloaded here. Its
[README](https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/README)
states that the diagonal table errors are for plots and cannot be used for
cosmological parameter fits. Correlations include repeated light-curve
observations of the same supernova. Consequently old diagonal and binned
Delta-chi2 values cannot support significance or a guaranteed ordering;
full covariance does not necessarily make every relative penalty smaller.

The independently fetched `release.dat` is byte-identical to both
`prep_2026/sne_lambda/pantheonplus_full.dat` and
`real_research/data_cache/PantheonPlusSH0ES.dat`, authenticating row order.
The covariance contains a maximum text-rounding asymmetry of 3e-8, handled
explicitly by `(C+C.T)/2`; its selected submatrices pass Cholesky factorization.
File SHA256 hashes are recorded in `manifest.json`.
The covariance is retained as deterministic `gzip -n` output and read directly
from gzip, rather than committing its 2.9 million text lines. `results.json`
also records its uncompressed SHA256. The public repository revision observed
at retrieval is `c447f0fea703fcd0fff57de5000947b5ca81286b`.

The official [SNe-only likelihood](https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon%2B_only_cosmosis_likelihood.py)
selects zHD>0.01, uses m_b_corr, integrates with zHD, and uses the heliocentric
redshift in the luminosity prefactor. Its selection has **1590 light curves**.
The old non-calibrator restriction leaves **1580**; that alternative is also
reproduced. A Cepheid-host SN above the cut remains a distance-shape datum in
the official SNe-only likelihood; no Cepheid distance is used here.

## Full-covariance results

All fits analytically profile a single additive magnitude intercept:
`chi2=r.T C^-1 r-(1.T C^-1 r)^2/(1.T C^-1 1)`.
No H0 or absolute SN magnitude is independently measured by this likelihood.

| Selection | N | Best flat Om | Profile Delta-chi2=1 endpoints | chi2 |
| --- | ---: | ---: | --- | ---: |
| Official zHD>0.01 | 1590 | .331576 | [.313608,.349999] | 1402.9191 |
| Legacy non-calibrators | 1580 | .332602 | [.314590,.351071] | 1386.4053 |

For the previously invoked fixed CPL pair `(w0,wa)=(-.83,-.75)`, profiling
Om independently gives Om=.312463 and **Delta-chi2=+.4173** relative to flat
LCDM on the official selection. At fixed Om=.29,.315,.35 the respective
differences are -3.5807,-.4131,+3.3642. These fixed hypotheses are not nested;
no square-root-Delta-chi2 sigma conversion is made. The earlier apparent
decline preference does not survive as a robust independent detection.

## The clean, conditional empirical lever

If the proposed law is assumed, then in flat LCDM

`a0=(c/Z) H0 sqrt(1-Om)`, with `Z=sqrt(32pi/3)`.

The SNe measure Om through distance shape. A separately calibrated galaxy a0
then predicts H0, which can be compared with an independent distance-scale
measurement. This comparison is noncircular only if galaxy distances and
acceleration fitting have not already absorbed the same H0 or Lambda input.
With H0 free, any positive fixed a0 can instead reproduce the SNe shape by
choosing H0; there is no new SNe-only shape preference for that a0.

| Acceleration footing | Conditional predicted H0, km/s/Mpc |
| --- | ---: |
| Input a0=9.4e-11 | 68.505 |
| Old cosmology-defined 9.35477e-11 | 68.175, circular as a validation |
| Inherited SPARC GLS 1.18144e-10 | 86.100 |
| Inherited SPARC median 9.72561e-11 | 70.878 |

For the GLS row, SNe shape alone gives profile endpoints [84.966,87.312],
but its inherited galaxy uncertainty is about **16%**, or approximately
13.9 km/s/Mpc in this H0 conversion. The narrow shape interval is therefore
not the uncertainty of the complete prediction. At imposed H0=67.4 or 73,
the SNe shape corresponds respectively to a0=9.2484e-11 or 1.00168e-10.

Literal flatness with fixed central GLS a0 gives OL=1.09079 at H0=67.4,
requiring negative matter density, and OL=.92985 at H0=73, where the central
flat hypothesis has Delta-chi2=329.54. These central-value statements omit
galaxy uncertainty. Including the inherited 16.1% width as an illustrative
independent log-Gaussian a0 penalty and profiling Om reduces the total
penalties to **2.296 and 1.043**, respectively. These are conditional penalized
likelihood values, not exclusion significances or a joint calibration analysis.
Genuinely curved profiles and all fixed footings are retained in `results.json`.

## Critical bridge still needed for the current theory

The old GLS/median values are Lambda-blind, but they are **not fitted under
the current exact exponential interpolation**. `prep_2026/a0_line/fire_slope.py`
explicitly assumes `gobs²-gbar²=a0*gbar`, corresponding to a different kernel.
Its own distance discussion says the gas dwarfs tend to have Hubble-flow
distances and that their errors were treated as independent. A common distance
scale does not average down independently across galaxies. Neither the old
kernel's central value nor its full 16% budget transfers automatically.

The useful next solution is therefore an exact-exponential fit of gas-dominated
galaxies with geometric or independently calibrated distances, carrying shared
distance zero points explicitly, followed by the conditional H0 test above.
At nonzero redshift, independently measured galaxy a0(z)/a0(0) provides a second
lever on the DE-density evolution relation; mapping an imposed CPL curve back
into a0(z) is not that measurement. The current action must separately derive
its background expansion and SN distance law before this becomes its prediction.

## Reproduction and numerical scope

`OPENBLAS_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python -B qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/audit.py`

The command exits 0 and writes only this directory. Independent 48/96-point
Gauss-Legendre integration agrees to 1.8e-15 magnitude at the best fit.
The magnitude-offset invariance is checked. Optimization bounds, inputs,
software, runtime, source hashes and result hash are in `manifest.json`;
the computation-audit validator with `--root` passes, with explicit legacy-v1
resource/freshness limitations. No random sampling or significance conversion.
The initial exact-symmetry check detected release rounding and was corrected
explicitly. Early numerical-library dot-product warnings were eliminated with
elementwise reductions; the retained final run is warning-free.

To restore the two input files in this directory from the pinned public release:

```sh
curl -L --fail 'https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/c447f0fea703fcd0fff57de5000947b5ca81286b/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat' -o release.dat
curl -L --fail 'https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/c447f0fea703fcd0fff57de5000947b5ca81286b/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov' -o PantheonPlusSH0ES_STAT_SYS.cov
gzip -n PantheonPlusSH0ES_STAT_SYS.cov
```

Verify the restored hashes against the manifest before interpreting a rerun.
