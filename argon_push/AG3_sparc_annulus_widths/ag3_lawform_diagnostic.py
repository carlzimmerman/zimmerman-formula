#!/usr/bin/env python3
"""AG3 addendum — law-form diagnostic: canonical vs quadratic on identical SPARC data.

Motivation (cross-track flag resolution, see HANDOFF_TO_CONDUCTOR.md):
  CANONICAL law (THEORY_CANONICAL_2026-10-14 S2; PAPER49 nu=100.5 at g_N=1e-4 a0;
                 ARGON02): g_N = g^2/(g + a0)   [standard mu = x/(1+x) family]
      => g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2,  g_ph = a0 g_N/g
      => point-mass phantom M_ph/M_b = (sqrt(1+4x^2)-1)/2,  rho(x) = (sqrt(1+4x^2)-1)/(2x)
      => band crossing rho = 1/2 at x = 2/3 (point-mass)
  QUADRATIC "equipartition" a0-line (G071 tested form; AG3 K2-pred; user-profile shorthand):
      g^2 - g_N^2 = a0 g_N  =>  g_ph = a0 g_N/(g + g_N)
      => M_ph/M_b = sqrt(1+x^2)-1,  rho(x) = (sqrt(1+x^2)-1)/x,  crossing at x = 4/3
  Deep asymptote identical (g_ph -> sqrt(a0 g_N) = C/r); they differ by up to ~50% in
  g_ph through the transition regime x ~ 0.2-3.

This diagnostic runs BOTH laws through the identical AG3 pipeline (corpus v7, G071
conventions, same cleaning) and reports, verdict-free:
  (1) pooled velocity-space law rms (G071-style statistic) for each form
  (2) rho-crossing comparison: measured vs each law's exact per-point prediction
  (3) band-region rho ratios for each form
  (4) stacked median rho_meas(x) vs both predictions (Upsilon-degenerate; reported)
  (5) supply-edge r_e under each law at fixed M_c = 5.364 M_b
Diagnostic only: no gates, no kill logic. Exit 0 always (unless crash).
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G081_JSON = os.path.join(REPO, "deepseek_push", "G081_results.json")
CORPUS = os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")

G_SI = 6.674e-11
MSUN_KG = 1.98892e30
KPC_M = 3.0856775814913673e19
G_MIXED = G_SI * MSUN_KG / (KPC_M * 1e6)          # kpc (km/s)^2 / Msun
KPC_KM = KPC_M / 1e3


def main():
    a0_SI = json.load(open(G081_JSON))["constants"]["a0"]
    a0m = (a0_SI / 1000.0) * KPC_KM               # (km/s)^2/kpc
    corpus = json.load(open(CORPUS))["galaxies"]
    sparc = [g for g in corpus if str(g.get("survey", "")).strip().upper() == "SPARC"]

    print("=" * 100)
    print("AG3 law-form diagnostic: canonical g_N=g^2/(g+a0) vs quadratic g^2-g_N^2=a0*g_N")
    print(f"a0 = {a0_SI} m/s^2 (G081 JSON); sample = AG3 cleaned SPARC (corpus v7, G071 conventions)")
    print("=" * 100)

    rms_q_all, rms_s_all, rms_q_deep, rms_s_deep = [], [], [], []
    ln_xq, ln_xs, ln_rq, ln_rs = [], [], [], []
    bins = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 1e9]
    stack_meas = {i: [] for i in range(len(bins) - 1)}
    stack_q = {i: [] for i in range(len(bins) - 1)}
    stack_s = {i: [] for i in range(len(bins) - 1)}
    n_gal = 0

    for g in sparc:
        pts = g["data"]
        m2l = g.get("m2l_disk")
        m2l = 0.5 if (m2l is None or float(m2l) <= 0) else float(m2l)
        R = np.array([p["Rad"] for p in pts], float)
        Vo = np.array([p["Vobs"] for p in pts], float)
        eV = np.array([p["errV"] if p["errV"] is not None else 0.0 for p in pts], float)
        Vg = np.array([p["Vgas"] for p in pts], float)
        Vd = np.array([p["Vdisk"] if p["Vdisk"] is not None else 0.0 for p in pts], float)
        Vb = np.array([p["Vbul"] if p["Vbul"] is not None else 0.0 for p in pts], float)
        vb2 = np.sign(Vg) * Vg**2 + m2l * (Vd**2 + Vb**2)
        ok = (Vo > 0) & (eV < Vo) & (vb2 > 0) & (R > 0)
        R, Vo, vb2 = R[ok], Vo[ok], vb2[ok]
        if len(R) < 6:
            continue
        o = np.argsort(R)
        R, Vo, vb2 = R[o], Vo[o], vb2[o]
        gobs = Vo**2 / R
        gbar = vb2 / R
        gph = gobs - gbar
        Mb_enc = R * vb2 / G_MIXED
        M_b = float(np.max(Mb_enc))
        C = math.sqrt(a0m * G_MIXED * M_b)
        rM = math.sqrt(G_MIXED * M_b / a0m)
        x = R / rM
        n_gal += 1

        # law predictions (point-mass-free: both are local functions of gbar)
        g_q = np.sqrt(gbar**2 + a0m * gbar)                      # quadratic
        g_s = (gbar + np.sqrt(gbar**2 + 4 * a0m * gbar)) / 2     # canonical (standard mu)
        gph_q = a0m * gbar / (g_q + gbar)
        gph_s = a0m * gbar / g_s
        rho_q = R * gph_q / C
        rho_s = R * gph_s / C
        rho_m = R * gph / C

        # (1) velocity-space law rms (G071 statistic), both forms
        lq = np.log10(gobs / g_q)
        ls = np.log10(gobs / g_s)
        rms_q_all.append(np.sqrt(np.mean(lq**2)))
        rms_s_all.append(np.sqrt(np.mean(ls**2)))
        deep = gbar <= a0m
        if np.sum(deep) >= 3:
            rms_q_deep.append(np.sqrt(np.mean(lq[deep]**2)))
            rms_s_deep.append(np.sqrt(np.mean(ls[deep]**2)))

        # (2)/(3) rho ratios and crossings
        m_pos = rho_m > 0
        for i in np.where(m_pos & (rho_q >= 0.25) & (rho_q <= 0.9))[0]:
            ln_rq.append(math.log(rho_m[i] / rho_q[i]))
        for i in np.where(m_pos & (rho_s >= 0.25) & (rho_s <= 0.9))[0]:
            ln_rs.append(math.log(rho_m[i] / rho_s[i]))

        def cross(vals):
            if vals[0] >= 0.5:
                return R[0]
            for i in range(1, len(R)):
                if vals[i - 1] < 0.5 <= vals[i]:
                    wgt = (0.5 - vals[i - 1]) / (vals[i] - vals[i - 1])
                    return R[i - 1] * (R[i] / R[i - 1]) ** wgt
            return None

        xm, xq, xs_ = cross(rho_m), cross(rho_q), cross(rho_s)
        if xm and xq:
            ln_xq.append(math.log(xm / xq))
        if xm and xs_:
            ln_xs.append(math.log(xm / xs_))

        # (4) stacked rho(x)
        for i in range(len(bins) - 1):
            sel = (x >= bins[i]) & (x < bins[i + 1]) & m_pos
            if np.any(sel):
                stack_meas[i].extend(rho_m[sel].tolist())
                stack_q[i].extend(rho_q[sel].tolist())
                stack_s[i].extend(rho_s[sel].tolist())

    print(f"\ngalaxies: {n_gal}")
    print("\n(1) pooled velocity-space law rms [dex] (G071 statistic; sample = AG3 cleaned, ALL points):")
    print(f"    quadratic  g^2-gbar^2=a0*gbar : all-points median-per-gal {np.median(rms_q_all):.4f}; "
          f"deep (gbar<=a0) {np.median(rms_q_deep):.4f}")
    print(f"    canonical  gbar=g^2/(g+a0)    : all-points median-per-gal {np.median(rms_s_all):.4f}; "
          f"deep (gbar<=a0) {np.median(rms_s_deep):.4f}")
    print(f"    paired difference (quad - canon), median per galaxy: "
          f"{np.median(np.array(rms_q_all) - np.array(rms_s_all)):+.4f} dex")

    print("\n(2) rho=1/2 crossing comparison (ln ratios; negative = measured crossing INSIDE prediction):")
    print(f"    vs quadratic pred  ((4/3)r_M point-mass): median {np.median(ln_xq):+.4f}, "
          f"IQR [{np.percentile(ln_xq,25):+.3f},{np.percentile(ln_xq,75):+.3f}], n={len(ln_xq)}")
    print(f"    vs canonical pred  ((2/3)r_M point-mass): median {np.median(ln_xs):+.4f}, "
          f"IQR [{np.percentile(ln_xs,25):+.3f},{np.percentile(ln_xs,75):+.3f}], n={len(ln_xs)}")

    print("\n(3) band-region ln(rho_meas/rho_pred):")
    print(f"    quadratic: median {np.median(ln_rq):+.4f}, IQR {np.percentile(ln_rq,75)-np.percentile(ln_rq,25):.4f}, n={len(ln_rq)}")
    print(f"    canonical: median {np.median(ln_rs):+.4f}, IQR {np.percentile(ln_rs,75)-np.percentile(ln_rs,25):.4f}, n={len(ln_rs)}")

    print("\n(4) stacked median rho_meas(x) vs predictions (Upsilon-degenerate; reported not gated):")
    print("      x bin          n     rho_meas   rho_quad   rho_canon")
    for i in range(len(bins) - 1):
        if stack_meas[i]:
            hi = f"{bins[i+1]:.1f}" if bins[i + 1] < 1e8 else "inf"
            print(f"    [{bins[i]:5.2f},{hi:>4s})  {len(stack_meas[i]):5d}   {np.median(stack_meas[i]):.4f}    "
                  f"{np.median(stack_q[i]):.4f}    {np.median(stack_s[i]):.4f}")

    print("\n(5) supply edge at fixed M_c = 5.364 M_b:")
    re_s = math.sqrt(((2 * 5.364 + 1) ** 2 - 1) / 4)
    re_q = math.sqrt((5.364 + 1) ** 2 - 1)
    print(f"    canonical: r_e = {re_s:.3f} r_M   (ARGON02 registered: 5.843)")
    print(f"    quadratic: r_e = {re_q:.3f} r_M")

    print("\nDiagnostic only — no gates. The differential statistics above are the discriminator input")
    print("for the conductor/referee law-form adjudication (see HANDOFF_TO_CONDUCTOR.md flag).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
