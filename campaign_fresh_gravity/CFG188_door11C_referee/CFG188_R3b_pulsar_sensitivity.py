#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 R3b -- DEPARTURE from the frozen script list, written AFTER my main and MUTATE runs were saved and after I read CFG172's A3.
Question: how much does the dressed G6(b) verdict depend on WHICH acceleration the pulsar row uses?  My frozen R3 used the pulsar's own acceleration
G M_c / a^2 (7.96 m/s^2, y_p = 8.5e10; masses from memory, unverified).  CFG172's A3 uses 73 m/s^2 (a hand value 'from memory'; the relative acceleration G M_tot/a^2).
Reports the dressed alpha_2 at the rule-T tie, the R bound and t_min, and the gaps against the G1 t_max, for both.  No MUTATE (sensitivity only)."""
import math, json
import CFG188_common as C
from CFG188_R3_b_operating_point import qP2, alpha2

def main():
    a0 = C.FOOT["canonical"]
    T440 = (3 * C.C_SI * C.H0_SI / a0) ** 2; T301 = 24 * math.pi / 0.25
    tmax_mi, tmax_n = 4.27e-4, 1.238e-6            # from CFG188_R3 main output (Mi, and N on the smallest-root branch)
    out = {}
    print("CFG188 R3b -- pulsar-row acceleration sensitivity of the dressed G6(b) verdict (departure; after reading CFG172 A3)")
    for label, g in (("own acceleration G M_c/a^2 (CFG188 R3)", 7.96), ("relative acceleration G M_tot/a^2 (CFG172 A3 hand value)", 73.0)):
        yp = g / a0; q = qP2(yp)
        row = {"g_m_s2": g, "y_p": yp}
        for nm, Rr in (("R=301.6", T301), ("R=440.5", T440)):
            row[f"alpha2_{nm}"] = alpha2(2 * q, 2 * q / Rr)
        from scipy.optimize import brentq
        Rmax = brentq(lambda Rr: alpha2(2 * q, 2 * q / Rr) - 1.6e-9, 1.0, 1e12)
        row["Rmax"] = Rmax; row["t_min_dressed"] = T440 / Rmax
        row["gap_Mi"] = T440 / Rmax / tmax_mi; row["gap_N_smallest_root"] = T440 / Rmax / tmax_n
        out[label] = row
        print(f"  {label}: y_p = {yp:.2e}; dressed alpha_2 at the tie: {row['alpha2_R=301.6']:.2e} (R=301.6), {row['alpha2_R=440.5']:.2e} (R=440.5) vs 1.6e-9; R_max = {Rmax:.3g}; t_min = {row['t_min_dressed']:.3g}; gaps {row['gap_Mi']:.1e} (Mi), {row['gap_N_smallest_root']:.1e} (N, smallest root)")
    C.out_json(__file__, out)

if __name__ == "__main__":
    C.guarded(main)
