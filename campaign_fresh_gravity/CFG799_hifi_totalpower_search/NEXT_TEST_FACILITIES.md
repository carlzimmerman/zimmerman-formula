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

Sources:
- APEX instruments: https://www.apex-telescope.org/instruments/ and https://apex-telescope.org/instruments/pi/sepia
- APEX instrument summary table: https://www.hq.eso.org/sci/facilities/apex/cfp/cfp110/instrument_summary.html
- ALMA receiver bands: https://elt.eso.org/public/teles-instr/alma/receiver-bands/
- Odin: https://www.chalmers.se/en/infrastructure/oso/telescopes-and-instruments/radio-astronomy-facilities/odin/
- SMA coverage (wSMA upgrade paper): https://arxiv.org/html/2406.17192v1
