# Running-Koide as a discriminator? — TRACK B verdict 2026-06-26

**Headline (both ways): BELOW-RESOLUTION / NON-CIRCULAR — NOT a real discriminator now or with
foreseeable m_tau precision. The running-Koide drift is CALCULABLE-not-MEASURABLE.** The framework's
+0.18% drift is reproduced and correct in sign; Singh's +0.374% is a DIFFERENT claim (a structural
prediction for the physical/pole Koide, in ~369sigma tension with the data); neither is testable via a
second-scale measurement because Q(M_Z) is computed from the SAME pole masses, carrying no new info.

## (1) Framework drift Q(M_Z) - Q(pole), reproduced (mpmath dps=40)
- **Q(pole) = 0.666660511** ; Q-2/3 = -6.16e-6 = **-0.91sigma** (sigma_Q=6.77e-6, m_tau-limited).
- 1-loop QED, gamma_m = -(3/2)(alpha/pi) (charge-universal, Q_f^2=1):
  - frozen alpha(0): **Q(M_Z)=0.667809, drift = +0.172%** (+170 sigma_Q)
  - alpha(M_Z)=1/127.95: **Q(M_Z)=0.667890, drift = +0.184%** (+182 sigma_Q)
- **SIGN: + (Q rises above 2/3 at higher scale). VERIFIED.** Banked +0.18% is correct; brackets it.
- **Literature cross-check (Sumino; hep-ph/0602134, Xing-Zhang):** "running masses FAIL Koide,
  Q(M_Z) deviates ~0.2% from 2/3" — matches sign AND magnitude.

### Deep structural why (sympy-exact): the drift is scale-FLAT and = dQ/dp * g
Charge-universal QED running is a pure POWER rescaling m_i -> m_i^(1+g), g=(3/2)(alpha/pi):
Q(mu) = sum m_i^(1+g) / (sum m_i^((1+g)/2))^2 = **Q_power(p) at p=1+g** — the mu^(-g) factors CANCEL
exactly. So Q depends on mu ONLY through g(alpha(mu)); with frozen alpha it is mu-INDEPENDENT. The
drift = dQ/dp|_{p=1} * g = 0.32998 * 0.003484 = +0.00115 (+0.172%). The +sign is just dQ/dp>0 at p=1.

## (2) Singh's +0.374% (K=0.66916), CLARIFIED (arXiv:2508.10131 Sec XI.1; catalogue 2604.06288)
- K=0.66916 is the **POST-triality-breaking** value; **pre-breaking = exact 2/3.** Mechanism: charged
  spread delta^2=3/8 + "a single endpoint tilt on the first lepton rung" shifts 2/3 -> 0.66916 (+0.374%).
- Masses built from Jordan eigenvalues |lambda_i|^2 as PHYSICAL masses; leptons called **"scale-clean"**
  -> 0.66916 is treated as **scale-INDEPENDENT**, i.e. effectively a prediction for the **pole** Koide,
  compared to the pre-breaking 2/3 (NOT to a running M_Z value). It is NOT "Q at a specific scale."
- **TENSION (flagged):** the directly-measured POLE Q = 0.66666 (at 2/3 to -0.91sigma). Singh's 0.66916
  sits **+0.00250 = +369 sigma_Q ABOVE** the measured pole value. So 0.66916 as a physical-Koide
  prediction is in gross tension with data; the data say the physical Koide is 2/3, not 0.669.
- If instead one (charitably) reads 0.66916 as the RUNNING (MSbar, M_Z) value, it lands near the QED
  running result Q(M_Z)=0.6678 but still **+0.20% high** (Singh +0.374% ~ 2.08x the QED +0.18%). Either
  reading leaves Singh in tension; the "SIGN MATCH" with the framework's +0.18% is real but the
  MAGNITUDE differs ~2x and the SCALE interpretation differs.

## (3) The real observable + m_tau precision
- **Q(M_Z) is COMPUTED from the pole masses + universal QED running — it carries ZERO independent
  experimental information beyond the pole masses.** There is no second-scale lepton-mass measurement;
  m_e, m_mu, m_tau are measured once (at/near pole), and every Q(mu) is a deterministic function of them.
  So "measure the running Koide at M_Z" is NOT an experiment — it is arithmetic on the pole masses.
- **The ONLY real observable is the pole Q's offset from 2/3** (currently -0.91sigma, sigma_Q=6.77e-6,
  m_tau-dominated: |dQ/dm_tau|=5.65e-5/MeV, sigma_mtau=0.12 MeV -> sigma_Q/Q = 0.00102%).
- To resolve the competing PHYSICAL-Koide predictions at the pole at 1sigma:
  - distinguish pole-Q from 2/3 itself (null vs any tilt): already at 0.91sigma; ~3sigma needs
    sigma_mtau ~ 0.04 MeV (3x better than 0.12 -- plausible this decade).
  - resolve Singh's **physical** +0.374% claim: it is ALREADY excluded at ~369sigma by the current
    pole Q (no better m_tau needed -- the data already say the physical Koide is 2/3, not 0.669).
  - The framework's +0.18% is a drift of the COMPUTED running Q, not of the pole Q, so NO m_tau
    precision tests it as a "running measurement" -- it is a calculation, always = +0.18% given the masses.

## (4) Discriminator verdict (both ways)
**Running-Koide is NOT a real discriminator** between the framework (+0.18%), Singh (+0.374%), and null:
- The +0.18% drift is a SOLID, sign-correct, literature-confirmed CALCULATION, but it is
  calculable-not-measurable (no second-scale data).
- The genuinely measurable quantity is the **pole-Q offset from 2/3** (-0.91sigma). That tests the
  PREMISE (is the physical Koide really 2/3?) and already EXCLUDES Singh's physical +0.374% (~369sigma),
  while being consistent with the framework's "Q=2/3 at the pole, protected by an IR mechanism" reading.
- m_tau precision (current 0.012% on the mass -> 0.001% on Q) governs ONLY the pole-Q-vs-2/3 test, NOT
  any running discriminator. A ~3x better m_tau (~0.04 MeV) would push pole-Q-vs-2/3 past 3sigma either way.

**HONEST CAVEAT:** Q=2/3 holds at POLE masses; the +0.18% running drift means the framework's
"Q=2/3" is a POLE-scale statement needing an IR/Sumino-class protector (already the banked diagnosis,
KOIDE_FROM_DSUNRUH 2026-06-20). The framework does not supply that protector. The "+0.18% sign-match
with Singh" is real in sign but the two numbers are different observables (running-computed vs
structural-physical) and differ ~2x in magnitude; do not over-read the agreement.

Scripts: opus_48_extended_research/reviews/koide_dsunruh/trackB_running_koide.py ,
trackB_threshold_running.py . Sources: arXiv:2508.10131 (Singh, EJA fermion mass ratios),
arXiv:2604.06288 (Singh falsification catalogue), arXiv:hep-ph/0602134 (Xing-Zhang running Koide),
Sumino arXiv:0812.2090.
