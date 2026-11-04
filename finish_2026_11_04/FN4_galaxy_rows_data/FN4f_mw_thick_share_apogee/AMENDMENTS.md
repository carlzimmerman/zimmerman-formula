# FN4f amendments (written and committed before any FN4f number)

Criteria: `FROZEN_CRITERIA.md`. Data: `../_external_data/apogee_dr17_2026_11/` (`fn4f_fetch.json`). Only the table headers have been read.

**A1, the join (departure).** The astroNN table has no FIELD column, so the frozen join on APOGEE_ID, TELESCOPE and FIELD cannot be made. Both tables have 733,901 rows, so they are compared row by row. A row joins if APOGEE_ID and TELESCOPE are equal (trailing blanks stripped) and the positions agree within 1″. KA4's line (≥ 99 % of rows) is unchanged.

**A2, units and reading.** astroNN `weighted_dist` is taken to be in pc. The script prints the sample median as a check. allStar is read in raw chunks of 20,000 rows with a header-only dtype (FN4c's reader).

**A3, flags.** STAR_BAD is ASPCAPFLAG bit 23. "Zero flags" means FE_H_FLAG == 0 and MG_FE_FLAG == 0.

**A4, bins.** The |z| bins are 0.2 kpc wide from 0.2 to 2.4 kpc, plus a last bin from 2.4 to 2.5 kpc (12 bins). The 0.4–2.0 variant uses the same 0.2 kpc bins. A bin needs at least 5 stars in each population or it is dropped.
