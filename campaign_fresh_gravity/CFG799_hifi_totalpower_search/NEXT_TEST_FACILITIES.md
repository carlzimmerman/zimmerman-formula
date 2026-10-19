# CFG799: where a real test of the two lines could run (web look-up, PROVISIONAL, 2026-10-19)

The archive search is finished (ADDENDUM B for 541.664 GHz, ADDENDUM C for 595.463 GHz). It closes the converter window (4e-9) for
both footings, and it cannot reach the kill line (1e-12): the HIFI total power is limited by baseline structure, so more archive
hours do not help (541.664 GHz: ε95 at S = 50 of 1.4e-11 to 3.3e-11; 595.463 GHz: 1.7e-11 to 5.1e-11). A kill-line test needs data
built for it. The line is the same in every target, so the observation must not subtract a sky reference (the frozen switching
rule): it has to be total power against calibrated loads, or another scheme in which the mirror's own emission survives.

This note lists what the web look-up found about instruments near the two frequencies. The numbers come from search summaries
of the sources below, not from reading the instrument manuals, so each one needs checking with the facility before it is used.

| line | what covers it | what the look-up found |
|---|---|---|
| 541.664 GHz | ALMA | No receiver band: Band 8 ends at 500 GHz and Band 9 starts at 602 GHz. The gap is read from the band edges (inferred, not stated). |
| | APEX | nFLASH460 covers 385 to 500 GHz; SEPIA660 is listed at 597 to 725 GHz. Neither reaches 541.7 GHz. |
| | SMA | A 2024 paper gives its coverage as 180 to 420 GHz; older papers describe a 600 to 720 GHz band. Not confirmed either way. |
| | Odin satellite | Has a 541 to 581 GHz receiver. The astronomy mission ended in 2007 and the satellite now studies the Earth's atmosphere. Whether the submillimetre receivers still work is not confirmed. |
| 595.463 GHz | ALMA | Just below Band 9 (602 to 720 GHz). |
| | APEX SEPIA660 | Listed at 597 to 725 GHz, but one APEX technical page gives the receiver's RF range as 578 to 738 GHz, which would include 595.463 GHz. Needs confirmation with APEX staff. |
| | Odin | Its 541 to 581 GHz band ends below 595 GHz. |

**Reading.** 541.664 GHz has no obvious ground instrument, because it sits in the gap between ALMA Bands 8 and 9, so the best
future route there is a purpose-built receiver or a space instrument. 595.463 GHz is the more reachable of the two: it sits at the
edge of the SEPIA660 and ALMA Band 9 windows and may be inside the SEPIA660 hardware's range. Atmosphere is the other problem for a
ground telescope near 557 GHz and 595 GHz (water lines), so a dry site and a total-power scheme that survives the sky emission
would be needed. The CFG797 reach table (10 m², 100 K SIS receiver, 30 days: 1.4e-13) assumes an ideal baseline, which CFG799 shows
the HIFI archive does not have.

## The table-top route (added 2026-10-19; reach from `next_test_reach.py`, output `next_test_reach.out`)

A telescope is not required, and the sky is not an issue, if the mirror sits in a shielded enclosure with a receiver at its focus (the
way published dish-antenna dark-photon searches are built, at much lower frequencies: a University of Tokyo parabolic antenna near
50 µeV and an Oxford C-band dish). The signal is the same formula as CFG797, divided by the coupling/geometry suppression S that
CFG798 and CFG799 carry. S = 1 is CFG797's ideal. A 2024 modelling paper (Gué et al., Phys. Rev. D 110, 035001) finds diffraction and
horn mode-matching can cut a spherical dish's signal a lot, and says the SHUKET constraint was weakened by roughly a factor of 50.
S is the make-or-break number and has to be measured with a calibrator on the real hardware.

5σ ε_min at both lines, S = 10 and 50 (the 541.664 and 595.463 GHz values differ by under 3%, so one number is shown):

| mirror | receiver T_sys | 1 h | 30 days | 1 year |
|---|---|---|---|---|
| 1 m² | warm 2400 K | 3.6e-11 / 8.0e-11 | 6.9e-12 / 1.5e-11 | 3.7e-12 / 8.3e-12 |
| 1 m² | SIS 100 K | 7.3e-12 / 1.6e-11 | 1.4e-12 / 3.2e-12 | 7.6e-13 / 1.7e-12 |
| 10 m² | warm 2400 K | 1.1e-11 / 2.5e-11 | 2.2e-12 / 4.9e-12 | 1.2e-12 / 2.6e-12 |
| 10 m² | SIS 100 K | 2.3e-12 / 5.2e-12 | 4.5e-13 / 1.0e-12 | 2.4e-13 / 5.3e-13 |

- **A 1 m² warm receiver covers the converter window (4e-9) by ×49 in one hour even at S = 50, and reaches about 1.5e-11 in 30
  days. That matches what the Herschel archive gave, so it adds nothing on the window.**
- **The kill line (1e-12) is reached at S = 10 by a 1 m² SIS receiver in 30 days, and at S = 50 only by 10 m² with an SIS receiver
  for a year, or about 100 m².** So the kill-line test is a large-dish or large-S-margin experiment, not a bench one.
- **Receivers.** A subharmonic Schottky receiver for the 600 GHz channel of a space sub-mm instrument was reported at noise below
  about 1200 K (DSB) with under 2 mW of pump power at room temperature, which is ~2400 K for a line in one sideband. That is a
  specialised space-programme part; I found no price or off-the-shelf source. Cooled SIS receivers are also built, but not for this
  range on any listed telescope (see above).
- **What the archive taught about systematics.** The HIFI total power was limited by broad baseline structure. A narrow line
  (0.3 MHz) measured with a high-resolution spectrometer on a stable receiver is much easier to separate from baseline than the
  1.1 MHz-resolution HIFI data, and the dish can be compared with the dish blocked or rotated, so the real limit will be receiver
  stability and standing waves, not sky.

Sources:
- APEX instruments: https://www.apex-telescope.org/instruments/ and https://apex-telescope.org/instruments/pi/sepia
- APEX instrument summary table: https://www.hq.eso.org/sci/facilities/apex/cfp/cfp110/instrument_summary.html
- ALMA receiver bands: https://elt.eso.org/public/teles-instr/alma/receiver-bands/
- Odin: https://www.chalmers.se/en/infrastructure/oso/telescopes-and-instruments/radio-astronomy-facilities/odin/
- SMA coverage (wSMA upgrade paper): https://arxiv.org/html/2406.17192v1
- Dish-antenna modelling: https://arxiv.org/pdf/2403.13448
- 600 GHz Schottky receivers: https://research.chalmers.se/en/publication/539643
