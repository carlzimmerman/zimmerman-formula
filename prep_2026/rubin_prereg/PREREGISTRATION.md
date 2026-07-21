# Pre-Registration: the a₀(z) Gate Against the Rubin/LSST Supernova Stream

**Frozen 2026-07-21**, *before* any calibrated Rubin/LSST supernova cosmology exists (LSST began 2026-06-30; the LSST-DESC calibrated SN sample is expected ~2027+). Author: Carl P. Zimmerman, Briar Creek Tech.

This document commits — in advance, timestamped, and hashed — the complete analysis by which the de Sitter–Unruh **modified-inertia** framework's one distinctive prediction will be judged against Rubin supernova data. The point is that the test is written *before* the data can shape it.

## 1. The prediction under test
The framework ties the galaxy acceleration scale to the cosmological constant, and — under the adiabatic-horizon ansatz — makes it evolve with the dark-energy density:
$$a_0(z)/a_0(0) = \sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}, \qquad \rho_{\rm DE}(z)/\rho_{\rm DE,0} = (1+z)^{3(1+w_0+w_a)}\,e^{-3 w_a z/(1+z)}.$$
The ratio $R \equiv a_0(z{=}3)/a_0(0)$ is **Z-independent** — both footings (canonical $a_0=9.36\times10^{-11}$, alt $1.13\times10^{-10}$) collapse to it. The framework's distinctive claim: $R$ declines to $\approx0.60$–$0.75$ **iff** dark energy evolves; if $w=-1$, $R=1$ and the framework reduces to constant-$a_0$ MOND.

## 2. The frozen estimator + decision thresholds
Committed in [`a0z_gate_estimator.py`](a0z_gate_estimator.py). **Input:** a calibrated $(w_0,w_a)$ posterior. **Output:** $R$, its significance vs flat, and the pre-committed verdict:

| Verdict | Pre-committed condition |
|---|---|
| **A) GATE OPEN** — distinctive prediction alive | decline detected at $\ge 3\sigma$ **and** $R\in[0.55,0.85]$ |
| **B) GATE DISSOLVED** — safe core (not falsification) | consistent with flat ($R=1$ within $2\sigma$) → constant-$a_0$ MOND; if $R\le0.85$ also excluded at $\ge3\sigma$, the decline is positively ruled out |
| **C) FRAMEWORK STRAINED** — cosmology-side tension | $R>1$ (rise) at $\ge3\sigma$ (contradicts $a_0\propto\sqrt{\rho_{\rm DE}}$ under evolving DE) |
| UNDECIDED | none met (insufficient significance) |

No threshold, band, or estimator may change after this freeze. Only the **input** $(w_0,w_a)$ is updated.

## 3. Data hierarchy (what feeds the gate)
1. **Primary:** the LSST-DESC *calibrated* SN Ia cosmology sample (systematics-controlled; ~2027+).
2. **Interim:** published Rubin $w_0w_a$ constraints as they appear (+ external CMB/BAO where combined).
3. **Readiness tracker only** ([`broker_sn_counter.py`](broker_sn_counter.py)): a running count of broker-classified SN Ia candidates from the *public* alert stream, vs the forecast sample thresholds (~4,400 spec-quality; ~400,000 photometric). **This count NEVER feeds the verdict** — it tracks *timing*, not cosmology.

## 4. What this explicitly is NOT (the refused, unsound path)
We do **not** build a do-it-yourself Hubble diagram from broker light curves. The alerts are public, but without DESC calibration (zero-points, photo-$z$ systematics, selection function) any $w(z)$ so extracted is systematics-dominated; a "Rubin confirms $a_0(z)$" claim built on it would be a manufactured result. Primary input is the calibrated sample, full stop.

## 5. Honest scope (frozen in)
This settles the **cosmology-side gate** — *does $a_0$ evolve at all* — which the framework *inherits* from $w(z)$. **GATE OPEN means the distinctive prediction survives, not that the framework is confirmed;** the confirming test remains the *independent galaxy-side* $a_0(z)$ (the cross-scale program, DOI 10.5281/zenodo.21440407). $a_0$'s value, $Z$, and the adiabatic-horizon promotion of $a_0(z)\propto\sqrt{\rho_{\rm DE}}$ are posited, not derived.

## 6. Pre-committed kill / dissolution conditions (signed 2026-07-21)
- **Distinctive prediction FALSIFIED** if the calibrated Rubin posterior yields Verdict **C** (a₀ rises with z at ≥3σ), which no viable footing of $a_0\propto\sqrt{\rho_{\rm DE}}$ permits under evolving DE.
- **Distinctive prediction DISSOLVED** (Verdict B) if $w\to-1$: the framework becomes ordinary constant-$a_0$ MOND. This is the stated safe core — dissolution, not a kill of the MOND-scale reframing.
- **Supported** (Verdict A) only if both the ≥3σ decline *and* the $[0.55,0.85]$ band are met.

## 7. State at the freeze (2026-07-21)
- Best current input (DESI DR2 2025): $R=0.775\,[0.68,0.88]$, decline $2.0\sigma$ → **UNDECIDED** (below the 3σ threshold). The forecast (`forecast_rubin_a0z.py`) projects Rubin reaches $3.3\sigma$ (SN-alone) to $4.7\sigma$ (SN+CMB/BAO) *if* DE evolves at the DESI-central rate.
- Broker readiness tracker (live, 2026-07-21): ALeRCE reports ~36,836 SNIa-classified objects (ZTF legacy + early LSST) — past the spec-quality threshold, ~9% of the LSST photometric target. A count, not a cosmology sample.

*Freeze integrity: the SHA-256 of the estimator, tracker, and this document are recorded in [`FREEZE_HASHES.txt`](FREEZE_HASHES.txt) and in the Zenodo deposit that mints this pre-registration; the Zenodo DOI + timestamp are the public lock-in.*
