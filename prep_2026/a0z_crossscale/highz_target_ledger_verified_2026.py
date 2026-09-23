#!/usr/bin/env python3
"""VERIFIED z ~ 1.5-3 deep-MOND target ledger (2026-09-23).

Why this file exists
--------------------
`highz_deepmond_target_list_2026.py` (D-1, 2026-07-25) was flagged the same day by its own
adversarial pass (commit 1c7781ed3e, "target-table BLOCKER"): rows tagged PUB contradicted
the primary papers they cite, and the gas-side rows "must be re-derived from primary sources
before the target list is used for any proposal".  That re-derivation was never done, and
the corrupted values reached the published observing case (PAPER14, Zenodo
10.5281/zenodo.22700993), which puts A68-HLS115 at z = 2.49 inside the decisive window.

On 2026-09-23 every row was re-read from its primary paper (arXiv text, tables quoted with
locations).  The values below are those, and ONLY those.  The old file and its JSON are left
untouched as the record of what was wrong; THIS ledger supersedes them.

Principal corrections (repo value -> source value):
  A68-HLS115   z 2.491 -> 1.5869; mu 5.3 -> 15; M* 7.2e8 -> 8.1e9; M_gas 2.8e9 -> 2.4e10
               (Dessauges-Zavadsky+2015, arXiv:1408.0816, Tables 1 and 3).  NOT deep-MOND.
  A68-C0       z 1.958 -> 1.5864; mu 9.1 -> 30; M* 1.28e9 -> 2.0e10; M_gas -> 1.2e10.
  A68-h7       mu 2.2 -> 3; M* 6.44e9 -> 1.54e11; M_gas -> 7.4e10.
  A2218-Mult   z 1.658 -> 3.104; mu 33.8 -> 14; CO UNDETECTED, M_gas < 1.7e10.
  MACS0451-arc M* 2.05e9 -> 2.5e9; M_gas 5.1e9 -> 4.0e9; "mu = 21.5" is in NO cited paper
               (all three use 49); "dispersion-dominated" uses V sin i uncorrected for
               i = 25 (+20/-10) deg -> V ~ 90 (54-147), V/sigma ~ 1.1: UNCERTAIN, not settled.
  OLAS rows    values correct (Hirtenstein+2019, arXiv:1811.11768, Tables 1-2), but the old
               "sig" was sigma_int (contains rotation); the paper's v/sigma uses sigma_local.
               M0717-02064: sigma_local 42.9, v/sigma 1.64, class 1 -> ROTATION-supported
               (the old note "pressure support is the whole problem" was wrong).
  Cl 0024 arc  V and sigma were SWAPPED: V sin i 76+/-12, sigma 69+/-5 (Jones+2010,
               arXiv:0910.4488, Table 2).
  Cl 0949 arc  "M_dyn 13e9 / 7e9" were SFRs; M_dyn = 12e9 / 3.8e9; line is [OIII], not Ha.
  SL2S 0217    M* 1.0e9 -> 1.8e8 (log 8.26, Berg+2018 arXiv:1803.02340 Table 2); gas "3e8"
               is in NO paper -- only upper limits <= 0.8e9 / 2.1e9 ([CII]) and <= 2e9 (CO)
               (Rybak+2021 arXiv:2101.00841); arc is 2.5", not 25".
  A1689B11     R_out 3.9 kpc -> 1.7 kpc (Ha detected only to ~1.7 kpc; Yuan+2017
               arXiv:1710.11130 Sec 3.2).
  zC-400569    V 300 -> 254+/-41; the 7.8e10 "M*" is a baryons-only dynamical UPPER limit
               (SED M* = 21.9e10) (Lelli+2023 arXiv:2302.00030).
  A68-C4       (PAPER14 Stage-1 target) real, z = 2.622, mu ~ 46 (39-53; Covone+2006 ~35),
               log M* 8.7 (Richard+2007) vs 8.0 (Richard+2011) -- 0.7 dex apart; R 2.2 kpc;
               NO kinematics, NO gas mass; Hbeta detected, [OIII] not (ground).
  A68-C20b     (PAPER14 Stage-1 target) mu ~ 158 (83-302): +/-0.28 dex FAILS the observing
               case's own delta log mu < 0.08 gate; M* only for image C20c.

The gate computation (sigma_cut, R_required_kpc, gbar_over_a0, Tacconi+2018 gas and
van der Wel+2014 size brackets, evaluate()) is copied VERBATIM from the D-1 file so the two
ledgers differ only in their inputs.  Exit 0 = ledger built.  NOT a verdict.
"""
import json
import os

import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
G = 6.67430e-11
MSUN = 1.98892e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
A0_CAN = 9.355e-11
A0_ALT = 1.1305e-10
CUT = 0.30


# ---------------------------------------------------------------- verbatim from D-1
def R_required_kpc(Mbar_msun, a0=A0_CAN, cut=CUT):
    R = np.sqrt(G * np.asarray(Mbar_msun, float) * MSUN / (cut * a0))
    return R / KPC


def gbar_over_a0(Mbar_msun, R_kpc, a0=A0_CAN):
    R = np.asarray(R_kpc, float) * KPC
    return G * np.asarray(Mbar_msun, float) * MSUN / (R ** 2 * a0)


def mu_mol_tacconi(z, logMstar, dMS=1.0):
    A, B, F, C, D = 0.12, -3.62, 0.66, 0.53, -0.35
    return 10.0 ** (A + B * (np.log10(1.0 + z) - F) ** 2 + C * np.log10(dMS)
                    + D * (logMstar - 10.7))


def re_vdw14_kpc(z, logMstar):
    A = np.interp(z, [1.25, 1.75, 2.25, 2.75], [4.0, 3.3, 2.8, 2.5])
    return A * (10.0 ** logMstar / 5.0e10) ** 0.22


def evaluate(o, a0=A0_CAN):
    z, Ms, Mm, R = o["z"], o.get("Mstar"), o.get("Mmol"), o.get("Rout")
    if Ms is None:
        if o.get("Mdyn") and R:
            return "NONE", None, 0.0, float(gbar_over_a0(o["Mdyn"], R, a0)), None, None
        return "NONE", None, None, None, None, None
    logMs = float(np.log10(Ms))
    if Mm is not None and o.get("Mmol_tag") == "PUB-UPPERLIM":
        Mbar_pub = None
        Mbar_lo, Mbar_hi = Ms, Ms + 2.0 * Mm
        gas_known = False
    elif Mm is not None:
        Mbar_pub = Ms + Mm
        Mbar_lo, Mbar_hi = Ms + Mm, Ms + 2.0 * Mm
        gas_known = True
    else:
        mm = Ms * float(mu_mol_tacconi(z, logMs))
        Mbar_pub = None
        Mbar_lo, Mbar_hi = Ms + 0.5 * mm, Ms + 2.0 * mm
        gas_known = False
    if R is not None:
        R_lo = R_hi = R
        rad_known = True
    else:
        re = float(re_vdw14_kpc(z, logMs))
        R_lo, R_hi = 2.0 * re, 3.0 * re
        rad_known = False
    gb_lo = float(gbar_over_a0(Mbar_lo, R_hi, a0))
    gb_hi = float(gbar_over_a0(Mbar_hi, R_lo, a0))
    if gas_known and rad_known:
        return ("PUB", float(gbar_over_a0(Mbar_pub, R, a0)), gb_lo, gb_hi, Mbar_pub,
                float(R_required_kpc(Mbar_pub, a0)))
    return ("BRACKET", None, gb_lo, gb_hi, 0.5 * (Mbar_lo + Mbar_hi),
            float(R_required_kpc(0.5 * (Mbar_lo + Mbar_hi), a0)))


# ---------------------------------------------------------------- VERIFIED rows
# Every number below was read from the cited table on 2026-09-23.  Masses are source-plane
# (magnification-corrected as published).  V is as published (V sin i or Delta v/2 -- see kin).
# vsig is the PAPER'S v/sigma where the paper gives one.  Rout = outermost radius of existing
# resolved kinematics (or a published size where no kinematics exist, labelled so).
DZ = "Dessauges-Zavadsky+2015 A&A 577,A50 (arXiv:1408.0816) Table 1 (z, mu, M*), Table 2 (RA/Dec), Table 3 (M_gas)"
HT = "Hirtenstein+2019 ApJ 880,54 (arXiv:1811.11768) Table 1 (z, mu, RA/Dec), Table 2 (M*, Dv, sigma_local, v/sigma, class)"
JO = "Jones+2010 MNRAS 404,1247 (arXiv:0910.4488) Table 1 (z, mu, RA/Dec), Table 2 (D, Vmax sin i, sigma, M_dyn)"
T = [
    dict(name="MACS0451-arc", z=2.013, mu=49.0, radec="04:51:57.27 +00:06:20.7",
         Mstar=2.5e9, Mmol=4.0e9, Mmol_tag="PUB", Rout=2.5, V=38.0, sig=80.0, vsig_pub=None,
         kin="Keck/OSIRIS AO Ha resolved; V sin i, i = 25 (+20/-10) -> V ~ 90 (54-147); merger/AGN "
             "caveats (DZ15)",
         cite=JO + "; " + DZ + "; Schaerer+2015 (arXiv:1502.03842)"),
    dict(name="OLAS A370-03097", z=1.55, mu=2.30, radec="02:39:50.270 -01:35:02.70",
         Mstar=10 ** 9.32, V=67.0, sig=31.8, vsig_pub=2.09, cls=1,
         kin="Keck/OSIRIS AO Ha; V = Dv/2 (not inclination-corrected); sigma = sigma_local", cite=HT),
    dict(name="OLAS M0717-02064", z=2.07, mu=6.48, radec="07:17:39.125 +37:44:18.45",
         Mstar=10 ** 8.08, V=71.0, sig=42.9, vsig_pub=1.64, cls=1,
         kin="Keck/OSIRIS AO Ha; V = Dv/2; sigma_local 42.9 (sigma_int 74.4 contains rotation)", cite=HT),
    dict(name="OLAS M0744-01203", z=1.65, mu=3.16, radec="07:44:47.420 +39:27:24.10",
         Mstar=10 ** 9.26, V=94.0, sig=73.4, vsig_pub=1.28, cls=1, kin="Keck/OSIRIS AO Ha", cite=HT),
    dict(name="OLAS M1149-00683", z=1.68, mu=4.05, radec="11:49:35.294 +22:24:22.28",
         Mstar=10 ** 8.14, V=51.0, sig=43.2, vsig_pub=1.17, cls=1, kin="Keck/OSIRIS AO Ha", cite=HT),
    dict(name="OLAS M1149-01802", z=2.16, mu=2.42, radec="11:49:39.358 +22:23:09.06",
         Mstar=10 ** 9.70, V=132.0, sig=55.4, vsig_pub=2.39, cls=1, kin="Keck/OSIRIS AO Ha", cite=HT),
    dict(name="OLAS M2129-00478", z=1.67, mu=1.79, radec="21:29:24.511 -07:40:54.79",
         Mstar=10 ** 8.58, V=10.0, sig=22.0, vsig_pub=0.469, cls=2, kin="Keck/OSIRIS AO Ha (disturbed)", cite=HT),
    dict(name="OLAS M2129-01665", z=1.56, mu=1.52, radec="21:29:25.956 -07:42:24.15",
         Mstar=10 ** 9.27, V=2.0, sig=59.0, vsig_pub=0.03, cls=2, kin="Keck/OSIRIS AO Ha (disturbed)", cite=HT),
    dict(name="OLAS M2129-01833", z=2.29, mu=1.56, radec="21:29:27.054 -07:42:35.72",
         Mstar=10 ** 9.66, V=79.0, sig=79.1, vsig_pub=1.01, cls=2, kin="Keck/OSIRIS AO Ha", cite=HT),
    dict(name="Cl 0024+1709 arc", z=1.68, mu=1.38, radec="00:26:34.43 +17:09:55.4",
         Mdyn=55e9, Rout=10.0, V=76.0, sig=69.0, kin="Keck/OSIRIS AO Ha; V = Vmax sin i (i = 50)", cite=JO),
    dict(name="MACS J0744+3927 arc", z=2.209, mu=16.0, radec="07:44:47.82 +39:27:25.7",
         Mdyn=11e9, Rout=1.0, V=129.0, sig=99.0, kin="Keck/OSIRIS AO Ha", cite=JO),
    dict(name="Cl 0949+5153 arc", z=2.394, mu=7.3, radec="09:52:49.78 +51:52:43.7",
         Mdyn=12e9, Rout=3.5, V=None, sig=71.0, kin="Keck/OSIRIS AO [OIII] (merger; NE component)", cite=JO),
    dict(name="A68-C0", z=1.5864, mu=30.0, radec="00:37:07.404 +09:09:26.57",
         Mstar=2.0e10, Mmol=1.2e10, Mmol_tag="PUB", kin="CO(2-1) unresolved", cite=DZ),
    dict(name="A68-HLS115", z=1.5869, mu=15.0, radec="00:37:09.503 +09:09:03.80",
         Mstar=8.1e9, Mmol=2.4e10, Mmol_tag="PUB", kin="CO(2-1) unresolved", cite=DZ),
    dict(name="A68-h7", z=2.1529, mu=3.0, radec="00:37:01.41 +09:10:22.31",
         Mstar=1.54e11, Mmol=7.4e10, Mmol_tag="PUB", kin="CO(3-2) unresolved", cite=DZ),
    dict(name="A2218-Mult", z=3.104, mu=14.0, radec="16:35:48.919 +66:12:13.81",
         Mstar=None, Mmol=1.7e10, Mmol_tag="PUB-UPPERLIM", kin="CO(3-2) undetected", cite=DZ),
    dict(name="SL2S 0217", z=1.844, mu=17.3, radec="02:17:37.237 -05:13:29.78",
         Mstar=10 ** 8.26, Mmol=2.1e9, Mmol_tag="PUB-UPPERLIM", Rsize=0.35,
         kin="no resolved kinematics; UV r_half ~ 0.35 kpc",
         cite="Berg+2018 ApJ 859,164 (arXiv:1803.02340) Table 2; Rybak+2021 ApJ 909,130 "
              "(arXiv:2101.00841) Table 1 (gas UPPER LIMITS 0.8e9-2.1e9)"),
    dict(name="A1689B11", z=2.540, mu=7.2, radec="13:11:33.336 -01:21:06.9",
         Mstar=10 ** 9.8, Rout=1.7, V=200.0, sig=23.0, vsig_pub=11.0,
         kin="Gemini/NIFS AO Ha, cool thin disc; Ha detected to ~1.7 kpc (control)",
         cite="Yuan+2017 ApJ 850,61 (arXiv:1710.11130) Table 1, Sec 3.2, 4.1"),
    dict(name="DSFG850.95", z=1.555, mu=1.0, radec=None,
         Mstar=3.8e10, Mmol=8.88e10, Mmol_tag="PUB", Rout=14.1, V=285.0, sig=48.0,
         kin="Keck/MOSFIRE long slit (23 deg misaligned); gas from 870um dust",
         cite="Drew+2018 ApJ 869,58 (arXiv:1811.01958) Table 1"),
    dict(name="zC-400569 (cold-tracer control)", z=2.24, mu=1.0, radec="150.28621 +1.74116",
         Mstar=2.19e11, Rout=8.0, V=254.0, sig=15.0, vsig_pub=17.0,
         kin="ALMA CO resolved; sigma_CO <= 15 (limit); M* = SED value (the 7.8e10 is a dynamical "
             "upper limit); fitted gas 2.3-4.9e10 not used",
         cite="Lelli+2023 A&A 672,A106 (arXiv:2302.00030) Tables 3-4, Sec 5.3"),
    dict(name="Big Wheel", z=3.2452, mu=1.0, radec="00:41:35.113 -49:37:12.42",
         Mstar=3.7e11, Mmol=1.8e11, Mmol_tag="PUB", Rout=15.0, V=280.0, sig=61.0,
         kin="JWST NIRSpec MSA slits; r_half 9.6 kpc, disc >= 30 kpc (Rout = half the extent)",
         cite="arXiv:2409.17956 Table 1"),
    dict(name="A68-C4", z=2.622, mu=46.0, radec="00:37:07.657 +09:09:05.90",
         Mstar=10 ** 8.7, Mstar_alt=10 ** 8.0, Rsize=2.2,
         kin="NO kinematics; Hbeta detected, [OIII] not (ground NIR); Lya only",
         cite="Richard+2007 ApJ 662,781 (astro-ph/0702705) Tables 2 and 5; Richard+2011 MNRAS 413,643 "
              "(arXiv:1011.6413) Tables 1 and 4; Covone+2006 (astro-ph/0601387) mu ~ 35"),
    dict(name="A68-C20b", z=2.689, mu=158.0, radec="00:37:04.707 +09:09:51.85",
         Mstar=10 ** 8.4, Rsize=0.36,
         kin="NO kinematics; z from Lya on image C20c; M* and size (unresolved) from C20c",
         cite="Richard+2007 (astro-ph/0702705) Table 5, Fig. 4; SLICE (arXiv:2503.17498)"),
]


def main():
    rows = []
    for o in T:
        out = dict(o)
        for lab, a0 in (("can", A0_CAN), ("alt", A0_ALT)):
            mode, gpub, glo, ghi, Mbar, Rreq = evaluate(o, a0)
            out.update({f"mode_{lab}": mode, f"gpub_{lab}": gpub, f"glo_{lab}": glo,
                        f"ghi_{lab}": ghi, f"Rreq_kpc_{lab}": Rreq})
        rows.append(out)

    print(f"{'object':32s} {'z':>6s} {'mu':>6s} {'logM*':>6s} {'mode':>8s} "
          f"{'g_bar/a0 can [lo,hi]':>22s} {'v/sig':>6s}  kinematics")
    for r in rows:
        lm = f"{np.log10(r['Mstar']):.2f}" if r.get("Mstar") else "  -  "
        if r["mode_can"] == "PUB":
            g = f"{r['gpub_can']:.2f} (PUB)"
        elif r["glo_can"] is not None:
            g = f"[{r['glo_can']:.2f}, {r['ghi_can']:.2f}]"
        else:
            g = "not computable"
        vs = f"{r['vsig_pub']:.2f}" if r.get("vsig_pub") else "  -  "
        print(f"{r['name']:32s} {r['z']:6.3f} {r['mu']:6.1f} {lm:>6s} {r['mode_can']:>8s} {g:>22s} "
              f"{vs:>6s}  {r['kin'][:60]}")

    in_window = [r for r in rows if r["z"] >= 2.0]
    # NONE-mode rows carry only M_dyn as a CEILING (lower corner 0): uninformative, excluded
    plaus = [r for r in in_window if r["mode_can"] != "NONE"
             and r["glo_can"] is not None and r["glo_can"] < CUT]
    out_win = [r for r in rows if r["z"] < 2.0 and r["mode_can"] != "NONE"
               and r["glo_can"] is not None and r["glo_can"] < CUT]
    print(f"\nwindow z >= 2: {len(in_window)} objects; deep-MOND plausible (optimistic corner "
          f"< {CUT} a0, canonical; M_dyn-only rows excluded): {[r['name'] for r in plaus]}")
    print(f"below the window (z < 2), plausible: {[r['name'] for r in out_win]}")
    c4 = dict([o for o in T if o["name"] == "A68-C4"][0], Mstar=10 ** 8.0)
    m, gp, lo, hi, *_ = evaluate(c4)
    print(f"A68-C4 at the OTHER published M* (log 8.0, Richard+2011): g_bar/a0 [{lo:.2f}, {hi:.2f}] "
          f"-> {'plausible' if lo < CUT else 'not plausible'}; at log 8.7 (Richard+2007) not plausible. "
          f"The 0.7-dex M* disagreement decides it.")
    print("confirmed deep-MOND (PUB g_bar < 0.3 a0): "
          f"{[r['name'] for r in rows if r['mode_can'] == 'PUB' and r['gpub_can'] < CUT]}")
    json.dump({"superseded": "highz_deepmond_target_list_2026_results.json",
               "verified_on": "2026-09-23", "cut": CUT, "rows": rows,
               "window_z_ge_2_plausible": [r["name"] for r in plaus],
               "below_window_plausible": [r["name"] for r in out_win],
               "A68_C4_note": "plausible only at log M* = 8.0 (Richard+2011), not at 8.7 (Richard+2007)"},
              open(os.path.join(HERE, "highz_target_ledger_verified_2026_results.json"), "w"),
              indent=2, default=float)


if __name__ == "__main__":
    main()
