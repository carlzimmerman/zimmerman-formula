# MG1 amendments. Written after reading the papers and before running any script, but after doing rough label sums by hand. Not blind

## A1 asymmetric errors (the criteria didn't say)
Signed value along an axis: the error toward zero. Non-negative radial offset: the larger of the two, since noise biases a radial offset high and the lower error flatters it. Rerun reported with all asymmetric errors averaged.

## A2 galaxy tracer (the criteria didn't say)
Luminosity peak where published, else BCG. BCG reported as an alternate where both exist.

## A3 "s resolved": the criteria's s/sigma > 2 is ambiguous, and it matters
The literal reading: sigma is the row's sigma already defined, the lens error, here sigma on d(lens, gas). So "resolved" means lensing could tell gas from galaxies. Primary. A hand sum shows the count moves under the other reading (sigma = s's own error, which brings rows with UNRESOLVED lens peaks into the denominator). That reading gets reported alongside, in the first lines of the README, with what it does to the verdict. I chose primary by the text, knowing the hand sums.

## A4 no-gas-offset or proxy rows
d(gal, gas) not published separately: taken as the lens-gas offset, or the paper's proxy, flagged PROXY. MACS J0025's gas 5.5e13 is one value at the gas peak; split evenly, flagged. Kpc per arcsec for the Musket Ball: 6.4, Jauzac's published scale at z 0.54 for a neighbouring redshift, flagged; no background model of mine.

## Disclosure on timing
This file was written before the script ran, but its commit hit another session's git lock and failed, and the script ran once before the commit landed. Text unchanged by the run; this paragraph is the only addition. The file's order in git history therefore does not prove the sequence. The hand sums were done first in any case.
