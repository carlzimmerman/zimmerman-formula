# CFG418: the cold-to-baryon ratio inferred from KiDS lensing via the supply edge. CONSISTENT on canonical, slightly HIGH on alt

Criteria committed first. Script `cfg418_rc.py`. MUTATE (x := 1) pushes R_c to 12–26, so the control works.

**Inversion.** R_c = x · r_ta · f_ret / r_M, with:
- x from CFG413's free-two-halo χ² profile (best 0.48 canonical / 0.53 alt; Δχ² ≤ 1 range 0.39–0.58 / 0.44–0.64);
- typical lenses log M_b 10.5–11;
- census f_ret 0.07–0.10.

**Result.**
- **canonical:** R_c = 4.6–13.0 (central 6.3–9.0 at log M_b 10.8), which contains the CMB's 5.364, so **CONSISTENT**.
- **alt:** R_c = 6.0–16.5, which is **HIGH** by a little.

**Reading.**
- The first local, lensing-based handle on the cold fluid's amount: about 6–9 against the CMB's 5.36, the same ballpark.
- It does NOT derive the amount.
- It rests on CFG413's free two-halo amplitude and the census f_ret, and the interval is wide (factor 2–3).
- It tests the supply-edge picture's consistency.
