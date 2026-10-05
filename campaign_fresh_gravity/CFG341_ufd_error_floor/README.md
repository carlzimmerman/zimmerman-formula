# CFG341: hidden velocity-error floor for the UFDs

**Verdict (frozen c246b01a0): NOT.**

To bring each UFD down to the law, the median system would need a hidden per-star error of **3.4 km/s** on top of the published errors. That is larger than the documented total error floors (about 1-2 km/s), and those floors are already deconvolved. Only 10% of the UFDs need 1 km/s or less.

Result of subtracting a hidden floor from every dispersion:
- **1.0 km/s:** the offset stays at +0.35 dex (3.6 sigma).
- **2.0 km/s (extreme):** +0.30 dex (3.0 sigma).

Controls: C1 reproduces the measured-only median (+0.3545). MUTATE (sigma shuffled) changes the f_need distribution.

Approximation: the 9 upper limits enter the median at their limit values. That can only push the median down, so it favours the escape.

Run: `python3 campaign_fresh_gravity/CFG341_ufd_error_floor/cfg341_error_floor.py` (CFG341_MUTATE=1 for the control).
