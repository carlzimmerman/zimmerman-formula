# WG5_mi_reading_check: the modified-inertia reading can't be the web-versus-galaxy rule. The record closed it by galaxy lensing (21σ), and it misses CMB lensing too

**Kind.** A record check plus a DIAGNOSTIC. It has no frozen criteria and is not a graded lane.

**Origin.** Owner 2026-11-04: "Yes, try it". That answered my suggestion, after WG4, that a modified-inertia (MI) reading of the law was "the one lead left" for weakening the law on the linear web but not in galaxies.

**I made that suggestion without checking the record.** κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## The record already answers it
- **The framework's original completion is pure MI** (a0kit: "de Sitter-Unruh modified-inertia", ν(y) = √(1 + 1/y), Milgrom 1999).
- **That arm was closed as physics on 2026-08-08.** Galaxy lensing excludes pure MI at **21σ**, and all three rescues are closed (`RETRACTIONS.md`; `STANDING.md` line 284; `FAILURES_EXECUTIVE_SUMMARY_2026-09-28.md` row C2).
- **Why it can't be the rule:** in pure MI the metric carries no phantom, so light sees only the Newtonian potential of the baryons. The law can't be weakened on the web while galaxy lensing keeps its phantom, because MI has no phantom for galaxy lensing either. That is the 21σ failure.

## Diagnostic: MI's CMB-lensing side
**Method.**
- Inputs: the existing law-on runs, WG2's R1 with a0 flat and WG4's runs with a0 tracking ρ_DE.
- Their dynamics stand in for MI's. At the mesh scale the only difference is QUMOND's curl projection.
- Their stored baryon spectra are turned into the Newtonian potential, with the mode-weighted ⟨1/k⁴⟩ of each bin, then projected and graded as WG2.

**Result.** r is the model's lensing amplitude over the measured one.

| runs | with the law's phantom in the metric | MI, Newtonian potential only |
|---|---|---|
| B2, a0 flat (A_s 1e-9 / 2.1e-9 / 4e-9) | 11.4 / 12.7 / 14.1 | **0.034 / 0.042 / 0.051, FAILS LOW** |
| B2D, a0 tracks ρ_DE | 6.7 / 7.6 / 8.5 | **0.013 / 0.017 / 0.021, FAILS LOW** |
| B2, a0 tracks ρ_DE (Λ expansion) | 6.7 / 8.5 | 0.013 / 0.021, FAILS LOW |
| B1, a0 flat (baryons-only expansion) | 560 / 657 | 31 / 42, FAILS HIGH |
| B1D, a0 tracks ρ_DE | 321 / 388 | 12 / 18, FAILS HIGH |

**Check.** The same formula applied to WG2's law-off runs reproduces their stored, Newtonian-by-construction spectra at 0.947-1.044 in r. That misses the 2 % written into the script before it ran, and the tolerance is left as written.
- The residual comes from the spectrum's slope inside each bin.
- The smallest label margin is ×6.1 (B1D). The other runs sit 8.8-37× from their thresholds.
- So a 6 % error can't move any label.

**Reading.** With the measured-style expansion, MI shows 2-5 % of the measured CMB lensing: far too little, because light misses the phantom that makes the growth. Pure MI fails CMB lensing on the opposite side from QUMOND, and it fails galaxy lensing at 21σ.

## Where the factor of ½ stands
The rule that's needed:
- weakens the law on the linear web but not in galaxies;
- at the same a0, since galaxies pin a0 at z ≲ 2 (WG4);
- with light seeing the phantom in galaxies (KiDS; the 21σ MI exclusion).

What has been ruled out:
- a0's time evolution (WG4);
- the turnaround switch (WG3), which never turns on;
- pure MI, by galaxy lensing (record) and by CMB lensing (this diagnostic).

**What's left** is a scale- or environment-dependent weakening at 10-100 Mpc. The framework's own lengths don't sit there:
- the horizon, c/H₀ ≈ 4.4 Gpc and c²/a0 ≈ 31 Gpc;
- per-object MOND radii, at most about a Mpc.

So any such scale would be new.

## Files
- `wg5_mi_diag.py`: imports WG2's engine and WG4's backgrounds read only; copies WG2's projection.
- `wg5_mi_diag.out`, `wg5_mi_diag_results.json`.

**Run:** `python3 wg5_mi_diag.py`, a few seconds.
