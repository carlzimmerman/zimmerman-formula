# CCT-003: a transient receiver exists, but the combined target fails

Five completed live same-field envelope simulations test the wave-Poisson candidate at eta=.7. This is not the frozen v3s theory, shared L1 production, a four-dwarf likelihood, or a derived field ontology. Every simulation uses the same phase prescription and open outer absorber; there is no forced escape allowance, friction, imposed torque or per-dwarf efficiency.

## What actually happened

| initial diffuse-envelope fraction | inner mass final/initial | inner specific spin final/initial | mass lost by T60 |
|---|---:|---:|---:|
| 0% | 1.421 | .280 | 2.091% |
| 20% | 1.625 | .263 | 2.936% |
| 40% | 1.829 | .212 | 3.642% |
| 20%, finer grid | 1.611 | .249 | 2.936% |
| 20%, larger box at matched dx | 1.625 | .289 | 2.710% |

Inner means the fixed aperture r<3. Increased inner mass plus reduced specific spin is real in these numerical trajectories, but is not by itself proof of angular-momentum absorption: accretion of low-spin material can dilute specific spin. Direct inner/outer Jz are both recorded.

In the padded 20% run there IS an early exchange: at T12 the outer region gains 30.59% of the initial INNER Jz, while the inner region loses 31.54% and only .0728% of total mass has been removed. This is a reported-only scan of the history, not a regrade of the frozen T30/50% criterion. Initial inner Jz is only .00716 of total .08181; this early gain is about 2.7% of the total initial spin. It is not removal of 31% of the whole cloud's spin.

The envelope does not keep gaining spin. At T30 its net Jz gain relative to initialization is negative in all five cases. No case meets the frozen inner-loss AND outer-gain storage target. All five fail final mass retention and final-quarter inner-mass stationarity. The 20% padded run ends with .7323 of initial total mass inside r<3, not the .9885 central fraction in the older Sextans budget; only .9729 total mass remains at all. Thus this trajectory cannot be converted into that budget simply by waiting for the rest of the envelope to accrete: it has already lost more than the allowed stock.

## Numerical qualification

All mass partitions and ledgers close to <1e-8, and relative energy-ledger residuals are <4.2e-5. L32 cases FAIL the 2% total angular-ledger gate (3.3–5.6% residual). Padding the 20% case to L40 reduces its angular residual to .0497%, but does not cure excess mass loss or late variability. Finer-grid and padded final inner-mass values agree to <1%; inner J values differ more, and the stated absolute .01 J tolerance is weak for small aperture J. No precision transfer-rate claim follows from passing that loose observable comparison. A second box/padded-resolution study and outward positive-energy flux are still required to certify physical escape.

The absorber measures a boundary ledger; its positive removed Hamiltonian is not a measured energy at infinity in a periodic potential. Remaining outer material is not proven bound or tidally surviving. Process peak memory is <208 MB on macOS, one numerical thread. No live shared job/queue was changed.

## Stellar guard and actual four-dwarf selectivity

The isolated Newtonian whole-Plummer virial moment reconstructed from each snapshot's radial mass distribution increases in every run. For the padded 20% case, ratios at tracer scales a=.5,1,2,4 are 2.295,1.983,1.622,1.293. In particular the a=1 reconstructed contribution to sigma_los^2 nearly doubles. This reconstruction is not the exact periodic-box force, a stellar-heating measurement or an observed Fornax/Leo I prediction. Live stars and actual radial likelihoods remain OPEN. An outer envelope is not automatically invisible to stars.

A separate ordering argument rules out a useful restricted shortcut. For a fixed physical eta and one homologous wave profile at the same dimensionless evolutionary stage,

    L_i = eta_phys^2/(eta_code^2 G M_i),
    x_i = R_i/L_i proportional M_i R_i,
    M_i(<R_i)/M_i = F(x_i), with F nondecreasing.

Using the older CFG918 catalogue-B0 stocks and central targets, M R for Fornax is 55.8 times Sextans (55.4 alt), and Leo I is 3.50 times Sextans (3.48 alt). Meeting Sextans' .98854 central fraction would therefore force at least .98854 of each larger-argument stock inside its aperture. The allowed older fractions are instead .01307/.00546 for Fornax and .03451/.02896 for Leo I. The implied cold masses exceed those reference requirements by factors >=75.6/181 and >=28.6/34.1 respectively.

This is a conditional central-value HOMOLOGY obstruction, not a general wave-field no-go or uncertainty-aware exclusion. Different generated dimensionless shapes, spin/assembly histories, dimensionless ages or different physical stock can evade the premise; four separately fitted profiles do not explain it. The older stocks also do not close the newer Sextans population likelihood. homology_check.py reproduces all inputs, both footings and adversarial ordering controls. The contradiction applies even if the common profile transports spin perfectly.

## What changed about gravity bookkeeping

COUPLING_BRIDGE.md gives an explicit NEW Newtonian two-potential action: a universally Newtonian Phi contains baryon+cold mass once; a separate Xi is sourced/felt only by baryons. Its static spherical equations recover the original rational baryon-only law and add cold Newtonian gravity once. The wave experiments here are exactly its rho_b=0, Xi=0 limit.

That is a scoped variational bridge, not proof of the framework. It postulates non-universal Xi charge and a new potential; eta remains unexplained. Nonspherical galaxy tests, covariance, cosmology and composition constraints must be redone. Avoiding duplicate charge does NOT make excess cold mass gravitationally invisible. The old stock subtraction also cannot be transferred automatically: in this bridge Xi is a field response, not an assigned inventory of held cold matter, so the cold inventory must be rederived. We have not made the four-dwarf gravity problem disappear.

## Surviving continuation

The useful result is transient spin storage with very little early mass loss, followed by failed long-term retention/stationarity. A temporary receiver alone is insufficient: when its mass joins a low-spin core, its stored spin must still remain in a surviving outer component or leave through a counted channel.

The next distinct physical input is a predicted source of NONHOMOLOGY, with its work included. Time-dependent baryonic potentials are one candidate: dE_c/dt = integral rho_c partial_t Phi_b d^3x. Gas cycles can heat collisionless matter in other models (Pontzen & Governato 2012, https://arxiv.org/abs/1106.0499); coherent-field response is not supplied by that result. Before simulating four ad hoc gas histories, constrain their mass, timescale and energy from the galaxies' common star-formation/baryonic model, and calculate stellar heating concurrently. Coupling and cold inventory must be fixed first. No new coefficients or four pulse amplitudes have been fitted here.

The original target remains OPEN. These tests preserve a failed prescription and identify what a successor must change; no general completion claim, frozen edit, publication, push or automation was made.

Reproduce: envelope.py commands in runs/RECEIPT.json; `python3 sol61_push/continuous_cold_envelope_2026_10_24/analyze.py`; `python3 sol61_push/continuous_cold_envelope_2026_10_24/homology_check.py`; `python3 sol61_push/continuous_cold_envelope_2026_10_24/check_bridge.py`.
