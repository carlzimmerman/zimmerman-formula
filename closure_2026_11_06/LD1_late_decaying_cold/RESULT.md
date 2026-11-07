# LD1: a cold component that decays late cannot pass the CMB wall. FAIL, both footings

Criteria d7db4e3403. Script `ld1.py`; outputs `ld1.*` and `ld1_MUTATE.*`. TEST lane: adopts nothing. Kappa = 1/2 FITTED.
Not theory closed.

**The class.** Cold dark energy that decays to dark radiation (CLASS dcdm -> dr), cold from the start. Its lifetime is set
to the longest that keeps discs within SPARC's allowance today (f_cap x S <= SPARC_f_max, KD1).

| | canonical | alt |
|---|---|---|
| S_max (surviving share allowed) | 0.0792 | 0.0471 |
| lifetime | 5.26 Gyr (Gamma 185.9 km/s/Mpc) | 4.34 Gyr (225.5) |
| h needed to hold 100 theta_s (QX15 h 0.674) | 0.813 | 0.838 |
| **D1 CMB-lensing chi^2 (A_s refit; line 18.48)** | **46.3, FAIL** | **53.0, FAIL** |
| A_s refit / reference | 2.56 | 2.88 |
| D2 chi^2 at QX15's A_s (reported) | 619 | 719 |
| D3 captured share today (discs and clusters alike) | 0.326 | 0.194 |

**Why it fails.**
- Discs today may hold at most 5-8 % of the cosmic share. That forces about 92-95 % of the component to decay by z = 0,
  and most of the decay happens at z < 2, where the CMB-lensing kernel sits.
- The lensing spectrum then loses power and its shape tilts. Even a 2.6-2.9x amplitude refit cannot restore the shape:
  2.5-2.9 times the line.
- The background also needs h ~ 0.81-0.84 to hold theta_s. That is a large shift in its own right, not graded here.
- D3: by construction this class leaves clusters at f <= 0.33, so it could never carry the cluster step either.

**Checks.**
- KA: Gamma = 0 reproduces KD1's G9a chi^2 (8.5599 / 8.5604) exactly. PASS.
- MUTATE (lifetime 0.2 Gyr, h at QX15's value): chi^2 70.1 / 70.1, FAIL. BITES.

**Disclosures.**
- Two solver brackets were widened after the first runs crashed before any graded number: h from [0.35, 0.95] to
  [0.55, 1.4] (CLASS shooting fails at the edges), and log Gamma to [1.5, 2.6]. No gate depends on them.
- The MUTATE run does not hold theta_s; the h bracket cannot reach it at 0.2 Gyr. It uses QX15's h, as stated in the
  script.
- The primary TT/TE/EE likelihood with decay was not rerun (NOT EVALUATED, as frozen).

**Reading.** The CMB wall has no late-decay escape at the lifetimes discs allow. Together with KD1 (cold, retained
everywhere) and HC1 (hot, CMB chi^2 166-194), this closes the time-dependence door for a single component that decays
uniformly. It does not test a component that decays only where it is not confined; QX12(c) says that needs a key
telling hosts apart.
