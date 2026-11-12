#!/usr/bin/env python3
"""
STM1 -- MWI1's stellar-mass inventories redone from the full texts.
Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt) + AMENDMENT_A1.md.   Usage: python3 stm1.py
Writes stm1.out and stm1_results.json next to this file.
Published numbers are web look-ups (PROVISIONAL); sources in RESULT.md. kappa = 1/2 FITTED; not theory closed.
"""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
M_CENSUS = 6.681; HOT = 0.15; GAS_MWI1 = 1.191                      # 1e10 Msun
AMP = {"canonical": (1.256, 1.310), "alt": (1.152, 1.208)}
q = lambda *e: math.sqrt(sum(x * x for x in e))

# ---------------------------------------------------------------- cold gas (1e10 Msun, helium per AMENDMENT A1.2)
HE = 1.36
HI = {"McM17": (1.10, 1.10),                 # Sec 2.3 / Table 1, helium included (stated)
      "KK09":  (0.80, 0.80),                 # KK09 Sec 3 (Kalberla et al. 2007 model); helium included per McM17 Sec 2.3
      "NS16":  (0.72, 0.72 * HE)}            # NS16 Sec 4.2, within 30 kpc; helium not stated
H2 = {"McM17": (0.12, 0.12 * HE),            # Table 1; helium not stated
      "KK09":  (0.25, 0.25 * HE),            # KK09 Sec 3; helium not stated
      "NS16":  (0.085, 0.085 * HE),          # NS16 Sec 4.2; helium not stated
      "HD15":  (0.10, 0.10 * HE)}            # Heyer & Dame 2015 via Rice et al. 2016 Sec 4.1 (secondary)
GAS_LO = min(v[0] for v in HI.values()) + min(v[0] for v in H2.values())
GAS_HI = max(v[1] for v in HI.values()) + max(v[1] for v in H2.values())
GAS = {"1": GAS_MWI1, "lo": GAS_LO, "hi": GAS_HI}

# ---------------------------------------------------------------- inventories: (id, name, H mass, H up-error, C mass, C up-error, core?, note)
P17_M, P17_E = 1.88, 0.12                                    # Portail+2017 abstract: bar/bulge stellar mass (Kroupa, M2M)
LN_BD = 38.0 / 34.75                                         # LN15 Sec 4.1: BDs (3.25 Msun/pc2) subtracted from 38 -> add back to disc
ln_c = 5.17 * LN_BD + 0.91; ln_cf = ln_c / 6.08
I25_PD = 3.7 / 5.27                                          # Imig+2025 Sec IV.3: present-day / initial (A1.1)
CH2KR = 0.66 / 0.61                                          # Madau & Dickinson 2014 (Chabrier, Kroupa = 0.61, 0.66 x Salpeter)
L25E = q(0.353, 0.095)                                       # Lian+2025 erratum (ApJL 1003 L51): 2.659 +- 0.353 (syst) +- 0.095 (stoch)
INV = [
 ("LN15", "Licquia & Newman 2015", 6.08, 1.14, ln_c, 1.14 * ln_cf, True, "Kroupa; remnants in, BDs out (3.25 of 38 Msun/pc2 added back for C)"),
 ("McM17", "McMillan 2017 (record's census)", 5.43, 0.57, 5.43, 0.57, True, "dynamical; statistical error only"),
 ("C20", "Cautun et al. 2020", 5.04, 0.43, 5.04, 0.43, True, "dynamical, contracted NFW fiducial"),
 ("BHG16", "Bland-Hawthorn & Gerhard 2016", 5.0, 1.0, 5.0, 1.0, True, "dynamical disc + Kroupa bulge; Sec 6.4.4"),
 ("L25", "Lian et al. 2025 + erratum", 2.659, L25E, 2.659, L25E, True, "Kroupa 0.1-100; remnants in; BDs out, fraction not stated -> flagged"),
 ("I25", "Imig 2025 disc + Portail 2017 bar/bulge", 5.27 + P17_M, q(0.2, P17_E), 3.7 + P17_M, q(0.2 * I25_PD, P17_E), True, "H: initial disc mass; C: present-day 3.7 (A1.1)"),
 ("BR13", "Bovy & Rix 2013 disc + Portail 2017 bar/bulge", 4.6 + P17_M, q(0.3, P17_E), 4.6 + P17_M, q(0.3, P17_E), True, "dynamical disc at R0 = 8 kpc"),
 ("L24", "Lian et al. 2024 (Xiang 2018 disc + LN15 bulge)", 4.81, 0.13, 4.81, 0.13, False, "extra; literature composite; IMF not stated -> flagged"),
 ("P20", "Pieres et al. 2020 (DES-Y3 model)", 5.97, 0.99, 5.97 * CH2KR, 0.99 * CH2KR, False, "extra; Chabrier -> Kroupa x 1.082; remnants not stated -> flagged"),
]
MWI1_INV = [("LN15", 6.08, 1.14), ("McM17", 5.43, 0.57), ("C20", 5.04, 0.43), ("I25", 6.18, 0.21), ("L25", 2.607, 0.363)]
MWI1_Z = {"canonical": (0.85, 2.84, 4.68, 4.14, 12.24), "alt": (0.24, 1.62, 3.06, 0.84, 10.33)}

OUT = open(os.path.join(HERE, "stm1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n")
def need(f, gas, half=False):
    lo, hi = AMP[f]
    if half: lo, hi = 1 + (lo - 1) / 2, 1 + (hi - 1) / 2
    return lo * M_CENSUS - gas - HOT, hi * M_CENSUS - gas - HOT
def cls(z): return "SUPPLIED" if z <= 1 else ("WITHIN 2 SIGMA" if z <= 2 else "NOT SUPPLIED")

say("=" * 110); say("STM1  stellar-mass inventories from the full texts   (FROZEN_CRITERIA.md + AMENDMENT_A1.md)"); say("=" * 110)
# ---------------------------------------------------------------- checks
FAIL = []
def ka(name, ok, det):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({det})")
    if not ok: FAIL.append(name)
zk = {f: tuple((need(f, GAS_MWI1)[0] - m) / e for _, m, e in MWI1_INV) for f in AMP}
ka("KA1 MWI1's z values from MWI1's inputs, each within 0.01", all(abs(a - b) <= 0.01 for f in AMP for a, b in zip(zk[f], MWI1_Z[f])),
   "; ".join(f"{f}: " + ", ".join(f"{z:+.2f}" for z in zk[f]) for f in AMP))
ka("KA2 need lower ends 7.050 / 6.356 at gas 1.191, within 0.002", abs(need("canonical", GAS_MWI1)[0] - 7.050) <= 0.002 and abs(need("alt", GAS_MWI1)[0] - 6.356) <= 0.002,
   f"{need('canonical', GAS_MWI1)[0]:.4f} / {need('alt', GAS_MWI1)[0]:.4f}")
ka("KA3 0.66/0.61 = 1.082 within 0.001", abs(CH2KR - 1.082) <= 0.001, f"{CH2KR:.4f}")
bite = {}
for f in AMP:
    a = [cls((need(f, GAS_MWI1)[0] - r[2]) / r[3]) for r in INV]; b = [cls((need(f, GAS_MWI1, True)[0] - r[2]) / r[3]) for r in INV]
    bite[f] = sum(x != y for x, y in zip(a, b))
ka("M1 excess amplitude halved changes >= 1 class per footing in reading H1", all(v >= 1 for v in bite.values()), str(bite))
if FAIL:
    say("STOPPED: a check failed -> no label."); json.dump({"lane": "STM1", "label": "NO LABEL", "fail": FAIL}, open(os.path.join(HERE, "stm1_results.json"), "w")); raise SystemExit(0)

say(f"\n  cold gas range (1e10 Msun, with helium per A1.2): low {GAS_LO:.3f}  high {GAS_HI:.3f}  (MWI1 held {GAS_MWI1})")
say("  HI: " + ", ".join(f"{k} {v[0]:.3f}/{v[1]:.3f}" for k, v in HI.items()) + "   H2: " + ", ".join(f"{k} {v[0]:.3f}/{v[1]:.3f}" for k, v in H2.items()))
say("\n  inventories (1e10 Msun)      H: mass + up-err          C: mass + up-err      note")
for r in INV: say(f"   {r[0]:6s} {r[1]:48s} {r[2]:6.3f} + {r[3]:5.3f}   {r[4]:6.3f} + {r[5]:5.3f}   {r[7]}")

RES = {"gas": {"lo": GAS_LO, "hi": GAS_HI, "mwi1": GAS_MWI1}, "readings": {}}
for rule in ("H", "C"):
    for g in ("1", "lo", "hi"):
        rd = f"{rule}-{g}" if g != "1" else f"{rule}1"
        say("\n" + "-" * 110); say(f"READING {rd}: rule {rule}, cold gas {GAS[g]:.3f}"); RES["readings"][rd] = {}
        for f in AMP:
            lo, hi = need(f, GAS[g]); rows = []
            say(f"  {f}: need {lo:.3f} to {hi:.3f}")
            for r in INV:
                m, e = (r[2], r[3]) if rule == "H" else (r[4], r[5])
                z = (lo - m) / e; rows.append(dict(id=r[0], core=r[6], mass=m, err=e, z=z, cls=cls(z), ratio_lo=lo / m, ratio_hi=hi / m))
                say(f"     {r[0]:6s} {m:6.3f} + {e:5.3f}   z = {z:+7.2f}   need/it {lo/m:4.2f}-{hi/m:4.2f}   {cls(z)}{'' if r[6] else '  (extra)'}")
            sc = [x["id"] for x in rows if x["core"] and x["cls"] == "SUPPLIED"]; sa = [x["id"] for x in rows if x["cls"] == "SUPPLIED"]
            mc = [x["cls"] for x in rows if x["id"] == "McM17"][0]
            lab = f"SUPPLIED BY {len(sc)} OF 7 ({', '.join(sc) or 'none'}); WITH EXTRAS {len(sa)} OF 9 ({', '.join(sa) or 'none'}); AT THE RECORD'S CENSUS {mc}"
            say(f"     LABEL: {lab}")
            RES["readings"][rd][f] = dict(need=(lo, hi), rows=rows, label=lab)

say("\n" + "-" * 110); say("REPORTED, NOT GRADED (A1.3)")
for f in AMP:
    lo = need(f, GAS_MWI1)[0]
    for R0 in (8.2, 8.33):
        m = 4.6 + 3.0 * (R0 - 8) + P17_M; say(f"  {f}: BR13 composite at R0 = {R0}: {m:.2f} + {q(0.3, P17_E):.3f}  z = {(lo - m)/q(0.3, P17_E):+.2f}")
    e = 0.57 * math.sqrt(2); say(f"  {f}: McM17 with error 0.57 x sqrt2 = {e:.2f}: z = {(lo - 5.43)/e:+.2f} ({cls((lo - 5.43)/e)})")
    say(f"  {f}: C20 pure-NFW variant 5.97 + 0.40: z = {(lo - 5.97)/0.40:+.2f}")
say("\nIMF: Salpeter/Kroupa mass ratio = 1/0.66 = %.3f; Kroupa/Chabrier = %.3f (Madau & Dickinson 2014)" % (1 / 0.66, CH2KR))
json.dump(dict(lane="STM1", date="2026-11-12", results=RES), open(os.path.join(HERE, "stm1_results.json"), "w"), indent=1)
say("\nSTM1 COMPLETE. Published numbers are PROVISIONAL look-ups. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
