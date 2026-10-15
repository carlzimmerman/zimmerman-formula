# Frozen finite computation and its interpretation

Accepted evidence: `run_v3/manifest.json` and `run_v3/results.json`.
The Mathbox version-2 validator reports **valid evidence record** against
current input/output files. Its zero exit status records execution success;
the infinite-dimensional existence statement rests on PROOF.md, section 4.

The surrogate has two parts: exact SymPy identities and rational bounds for
the full stated product box; eight floating IVPs with four eta values
`0, 1e-8, 1e-6, 1e-4`, two tolerances and step caps each. The finite run
passed 128 assertions, including 50 assertions before the IVPs (source hashes,
definitions, symbolic identities and exact parameter/box estimates). There
is no randomness or unbounded search.

The 60-second wall-clock, 40-second CPU and 200000-byte log caps were
effective; one cooperative numerical-library thread was requested. No memory
or CPU-affinity cap was requested. Execution took 0.912 seconds on macOS arm64.
Runner Python was 3.11.13; computation Python 3.9.6, NumPy 1.26.2, SciPy
1.11.4, SymPy 1.14.0, mpmath 1.3.0. These versions and the actual shared
checkout commit/dirty state are recorded in the manifest, without treating
unrelated dirty files as inputs.

The IVP starts at `r0=1e-6` with the displayed regular-center series and uses
DOP853, `rtol=1e-10/2e-12`, `atol=1e-13/2e-15`, and
`max_step=.01/.0025`. The gauge Hamiltonian in this floating IVP uses the
positive series through `x^12`; over the proved `x<.001` its omitted tail is
at most `x^13/[13(1-x)]<1e-39`. This avoids subtracting two close logarithms;
the theorem and exact identities use the full logarithmic action. Profile
checks use 1001 fixed sample points. Proper stocks and charge are evolved
from their own equations; coordinate energy components are independently
integrated by quadrature on the dense output. Scalar wall matching is then
computed at 80 decimal digits on the rounded IVP boundary data. It does not
certify 80 digits of IVP accuracy.

At `eta=1e-4` (`c=100`) the finer illustrative solution gives:

| Quantity | Value in assigned units |
|---|---:|
| Baryon edge density | 0.9999998047519773 |
| Dark edge density | 5.363998954842175 |
| Summed edge pressure | 0.6290896745738255 |
| Proper baryon rest stock | 4.188789714141580 |
| Proper dark rest stock | 22.468668031070397 |
| Actual critical dark charge | 0.007964935435277680 |
| Interior Misner–Sharp mass | 26.657721257343884 |
| Selected constant NG tension | 0.3145448372486460 |
| Wall rest mass | 0.0003952686999699773 |
| Exterior Maxwell energy | 0.000002524205215452226 |
| Full ADM mass | 26.658116526296264 |
| Interior gauge energy | 0.0000005050189176787110 |
| Baryon internal energy | 1.429905865681685 |
| Dark internal energy | 1.205219212214139 |
| Central normalized lapse | 0.9999999999600126 |

The proper stock is distinct from coordinate rest energy/c^2, and the
interior mass is distinct from ADM mass. Internal/gauge energies are multiplied
by `eta` in the bulk mass equation; wall energy and exterior Maxwell energy
are also converted to mass using `eta`. The wall's negative tangential
pressures enter the Israel load; wall self-binding mass is approximately
`-7.81e-20`. The sum of coordinate rest masses plus internal/gauge masses
agrees with the IVP interior mass within `1.1e-14` in this example.

The maximum coarse/fine difference in any reported edge density, pressure,
mass, proper stock or charge over all four eta values is `3.20e-14`.
Chemical first-integral oscillations are below `6e-16`. High-precision
angular/time Israel, RN metric, and scalar load residuals are below `1e-70`
for the rounded scalar edge input; these are algebra/rounding controls,
not independently precise stellar profiles.

Retained failed controls: `run_v1` stopped at the Legendre-identity test
because the CAS had not been given the physical `D<D0` logarithm chart;
the test was corrected by substitution from positive E. `run_v2` stopped
at the rational critical-charge endpoint because `16G=(1/2500)^2`, while
the strict desired inequality comes from `pi<4`; its rational comparator
was corrected to non-strict equality. Neither failure changed the model,
its equations, nor its numerical parameters. The accepted run has fresh
before/after hashes. The earlier failed manifests refer to their historical
code revisions and are not accepted evidence for the current program.
Their original `check_einstein.py` input paths are therefore **stale under
current-root validation**; only the accepted run_v3 validates against the
current code. The exact historical code bytes have now been reconstructed
as read-only `DRAFT_CHECK_V1.py` and `DRAFT_CHECK_V2.py`, with SHA-256 values
`75a84a66bd48c0d7b81f356168d35716121169888d1ee6adee9e42fbe891b118` and
`3af63279e3c5b69e020dee3309581f356b190088444ea2abbaf2a9719fbd00d7`.
Each matches both its historical before/after input hashes. All other
historical inputs and logs still match. `HISTORICAL_INPUT_RECOVERY.json`
records those comparisons without editing either old manifest or the
accepted code. Recovery of a failed run's code is not a successful run or
a claim that its original current-root manifest validation passes.

Frozen current hashes:

```
PROOF.md                    8a73f618c321c7e8af1b4abe1d8bc1e4168923b42084d495e3f10d14dc97c8cf
check_einstein.py            d113ef071444233926410296d94633100f06188f112a5aa17e9568da06766296
inputs/definitions.json     c51c9fd81183ebacba6243bec1c993a312f745271c8ef4a66260879b821f74ce
run_v3/results.json         f2ca726269b6699bf6bb04ebdf800846a275e42e096166ec589dcb6c9bc8b01a
run_v3/manifest.json         def5a3f7d66aaad68d2bcf7b9b2ca5190fe3e4ad97b3c8c8a8a7de70e2507225
```

The exact actual argv and all declared inputs are in the accepted manifest;
`contract.json` fixes its interpretation. To validate from the repository:

```
/opt/homebrew/bin/python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/ambitious_round4_2026_10_15/einstein/run_v3/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

An execution rerun must use a fresh output directory and the explicit actual
argv/input list under the same contract; no manifest is itself executable.
Floating outputs do not prove uniqueness outside the contraction box,
any stability statement, microphysics, formation or galactic phenomenology.

Literature convention check: Israel's 1966 paper, DOI
`10.1007/BF02710419`, section 5 equations (19)–(20), was read from the
[original 14-page primary text](https://images.shoutwiki.com/gamebm/0/02/Israel1966_Article_SingularHypersurfacesAndThinSh.pdf)
on 15 October 2026. Its `[K_ij]-gamma_ij[K]` convention with the normal
minus to plus gives the sign used here after translating surface mass density
to energy density. The load and mass formulas were derived anew in the proof
and checked algebraically, so no claim depends on a quoted specialized
charged-shell formula. The source was read in the browser; no full-paper
cache is claimed. This was a narrow convention check, not a novelty search.
