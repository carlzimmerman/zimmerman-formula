# X74 pre-read: does A3's native c_f at 10¹² already decide the SPARC line? (written before any pre-read number)

**Not part of X74's verdict.** X74's frozen grade waits for A4 and is unchanged. This pre-read uses only committed
inputs: X48 A3's nine-seed ng 64 median c_f(10¹²) = 7.74 (`x48_analyze_results_ng64_A3.json`). No A4 output is opened.

**Why.** In X74 the c_f(M) table is flat below 10¹², so every SPARC galaxy below that mass gets c_f(10¹²). At c_f ≡ 4
the collapse branch is active in 0/175 SPARC galaxies and the canonical line passes. At c_f ≡ 8 (`sens_cf8.log`) it is
active in 70/175 and the line fails on both footings. A3's 7.74 is close to 8. If SPARC fails with c_f(10¹²) = 7.74 even
when the cluster masses are given the most favourable value, A4 cannot rescue X74's PRIMARY.

**Runs** (X74's script unchanged; `X74_CF` = a table file; outputs renamed `preread_*` so A4's outputs are not touched):
- **P1 (best case for clusters):** c_f = {10¹²: 7.74, 10¹³: 4, 10¹⁴: 4}, at f★ 0.034 and 0.0615, slope 2.7774.
- **P2 (bracket):** c_f = {10¹²: 7.74, 10¹³: 7.74, 10¹⁴: 7.74}, at f★ 0.034.

**Read (fixed now):**
- If P1 fails the SPARC line on the canonical footing at both f★: **"A3 already breaks X74's SPARC line"**. X74 PRIMARY
  cannot pass at any A4 cluster c_f, unless c_f(10¹²) falls further with resolution (A3 is labelled RESOLUTION-DEPENDENT,
  falling 33 % from ng 48 to 64). The decisive number then moves to c_f(10¹²) convergence, not A4.
- If P1 passes SPARC: the pre-read decides nothing, and A4 decides as frozen.
- P2 is reported only.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
