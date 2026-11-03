# LAM4 amendments, dated

`FROZEN_CRITERIA.md` (1023fbaae9) is unedited. kappa = 1/2 FITTED. Not theory closed.

## 2026-11-03, A1: K2 noise, before K2 or any grade
- The first two integrated fits (8978-3703, 9874-1901; S/N 137 and 93) have chi2 of 2.1 and 2.5: the covariance-corrected noise is still too small by about 1.5x. Fit errors are already scaled by sqrt(chi2). K2's synthetic noise is made **stricter**: each synthetic uses its galaxy's noise vector times sqrt(max(chi2, 1)) from that galaxy's own fit. As frozen, K2 would have used the unscaled vector and been optimistic.
- Seen before this amendment: those two fits only (sigma 164.5 and 91.5 km/s, h4 -0.035 and -0.024, window starts 4181 and 3900 A). No lambda label was compared.
- Streaming runs with 10 workers (about 0.3 MB/s per connection from the SDSS server). A first 6-worker run was stopped and restarted; partial cubes resume and no sum was written by the first run.
