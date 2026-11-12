# RCF1 AMENDMENT A1 (2026-11-12): post hoc diagnostic of the e_N bound. Changes no criterion and no label.

## What happened

The frozen run (`rcf1.out`, sha256 af4ed1518515a99dbe2098242ab4d34e844ad30900519f23bc34af9f6655d367; all five
known-answer checks pass, M1 bites) put the best-fit external field AT the frozen upper bound e_N = 0.03 on
every footing, data set and hot-gas variant of the primary (McMillan) census, so the e_N "upper limit" is
">= 0.03 (bound)" everywhere. On Ou's census (item 35's KA1, and the reported Ou-census variant) the field is
not pinned. The stellar-mass interval is therefore conditional on the bound.

## What is added

A separate script, `rcf1_posthoc.py`, writing `rcf1_posthoc.out` only (the frozen outputs are not rewritten):
1. the primary fit with e_N fixed at 0 (how much the bound moves M*);
2. the primary fit with e_N free on [0, 0.2] (where the unbounded minimum would sit and what M* it implies);
3. the Delta chi2 between e_N = 0 and e_N = 0.03 at the profile minimum (how strongly the data pull on e_N).

These are POST HOC and REPORTED, NOT GRADED. The frozen labels stand as computed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
