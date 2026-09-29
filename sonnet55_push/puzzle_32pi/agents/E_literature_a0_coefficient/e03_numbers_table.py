#!/usr/bin/env python3
"""e03_numbers_table.py -- what every computed/claimed coefficient gives numerically, on both footings, against the a0 quoted in the opened papers.

Adopted for illustration (NOT measured here): H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685  =>  H_Lambda = H0 sqrt(Omega_Lambda).  'Lambda footing' uses c H_Lambda (flat in z),
'H0 footing' uses c H0.  Data a0 = 1.2e-10 m/s^2 (the value quoted in Milgrom 2001.09729, Smolin 1704.00780, McCulloch 1709.04918); 'viable' = within 30% of it on at least one
footing, because the record's p03 shows the footing is not decided by the data.  The conclusions (factor ~10 vs a few %) are insensitive to these inputs.
Exit 0 = the reproduced numbers agree with the papers' own quoted numbers and the classification of 'viable' behaves.
"""
import math
import sys

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

c = 2.99792458e8
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc
OmL = 0.685
HL = H0 * math.sqrt(OmL)
cH0, cHL = c * H0, c * HL
Zfw = math.sqrt(32 * math.pi / 3)
a_data = 1.2e-10

rows = []   # key, name, kind, aL, a0, time behaviour
def add_Z(key, name, kind, Z, tb):
    rows.append((key, name, kind, cHL / Z, cH0 / Z, tb))
def add_a(key, name, kind, aL, a0, tb):
    rows.append((key, name, kind, aL, a0, tb))

add_Z("fw",   "framework kappa=1/2, Z=sqrt(32pi/3)",              "record (fitted)", Zfw, "flat (rho_Lambda)")
add_Z("forced","record forced kernel kappa=1, Z=sqrt(8pi/3)",     "record",          math.sqrt(8 * math.pi / 3), "flat")
add_Z("mil2pi","Milgrom empirical 2 pi (2001.09729 eq 3)",        "empirical",       2 * math.pi, "'moot': H0 or Lambda")
add_Z("verl", "Verlinde a0/6 (1611.02269)",                       "computed",        6.0, "H0 written; sec 8.2 says Lambda-defined -> flat")
add_Z("vp",   "van Putten 2/(1+2 pi sqrt2) (1411.2665)",          "computed",        (1 + 2 * math.pi * math.sqrt(2)) / 2, "a_H = H0 c, dS assumed")
add_Z("dl",   "Milgrom 1999 / Smolin / K-K / Pikhitsa: 2 c H",    "computed",        0.5, "Lambda (Milgrom, Smolin, HMN); H_dS (K-K); curvature H^2 (Pikhitsa)")
add_Z("dlalt","Milgrom 1999 alt functional a dT/da: c H",         "computed",        1.0, "Lambda")
add_Z("brane","Milgrom brane n=2: a0 = 2 c^2/l0, l0 = l_Lambda",  "computed",        0.5, "Lambda")
add_a("mc17", "McCulloch 2c^2/Theta, Theta = 8.8e26 m (1709.04918)", "computed",    2 * c**2 / 8.8e26, 2 * c**2 / 8.8e26, "Theta(z)=Theta_now/(1+z): rises ~(1+z)")
add_a("mc07", "McCulloch 2c^2/Theta, Theta = 2.6e26 m (his 2007/12 value)", "computed", 2 * c**2 / 2.6e26, 2 * c**2 / 2.6e26, "same")
add_Z("hmn",  "Ho-Minic-Ng a_c = a_Lambda/(2 pi)   (beta = 1/pi input)", "inserted", 2 * math.pi, "Lambda")
add_Z("kt",   "Kiselev-Timofeev 12 N_G H_Lambda, N_G = 1/(24 pi sqrt(OmL))", "inserted", 2 * math.pi, "Lambda (H_Lambda = H0 sqrt(OmL))")
add_a("haj",  "Hajdukovic a_cr = OmL cH0/(4 pi^2 sqrt(Om0-1)), Om0-1=1e-3", "computed", None, OmL * cH0 / (4 * math.pi**2 * math.sqrt(1e-3)), "'constant' by claim")

print(f"  constants: cH0 = {cH0:.4e}, c H_Lambda = {cHL:.4e} m/s^2;  data a0 = {a_data:.2e}")
print(f"  {'candidate':<66}{'kind':<17}{'a0 [Lambda]':>13}{'a0 [H0]':>13}{'best x data':>13}{'<30%?':>7}")
viable = {}
for key, name, kind, aL, a0, tb in rows:
    rs = [x / a_data for x in (aL, a0) if x is not None]
    best = min(rs, key=lambda r: abs(math.log(r)))
    v = any(abs(r - 1) < 0.30 for r in rs)
    viable[key] = v
    sL = f"{aL:.3e}" if aL is not None else "      -"
    s0 = f"{a0:.3e}" if a0 is not None else "      -"
    print(f"  {name:<66}{kind:<17}{sL:>13}{s0:>13}{best:>13.2f}{('yes' if v else 'no'):>7}   [{tb}]")

d = {k: (aL, a0) for k, _, _, aL, a0, _ in rows}
check("N1  framework a0 on the two footings reproduces the record's 9.36e-11 (Lambda) and 1.13e-10 (H0)", abs(d["fw"][0] / 9.36e-11 - 1) < 2e-3 and abs(d["fw"][1] / 1.13e-10 - 1) < 3e-3)
check("N2  Verlinde cH0/6 with H0 = 70 gives 1.13e-10 (quoted as 1.1e-10 in 1909.01734)", abs(c * 70e3 / Mpc / 6 / 1.13e-10 - 1) < 0.01)
check("N3  van Putten with H0 = 70 gives 1.376e-10 (paper: 1.37e-10)", abs(c * 70e3 / Mpc * 2 / (1 + 2 * math.pi * math.sqrt(2)) / 1.37e-10 - 1) < 0.01)
check("N4  Smolin eq (3): a_Lambda/a0 = 8.3 with a_Lambda = c^2 sqrt(Lambda) = sqrt(3) c H_Lambda gives %.2f here (consistent); but his derived a0 = 2 c H_Lambda = %.2e is %.1fx the data: his two statements differ by ~%.0fx" %
      (math.sqrt(3) * cHL / a_data, 2 * cHL, 2 * cHL / a_data, 2 * cHL / a_data), 7.0 < math.sqrt(3) * cHL / a_data < 9.0 and 8.0 < 2 * cHL / a_data < 10.0)
dl_L, dl_0 = d["dl"]
check("N5  T - T_Lambda family: a0 = 2 c H_Lambda = %.2e (Lambda footing), %.2e (H0 footing): %.1fx and %.1fx the data, %.1fx the framework" %
      (dl_L, dl_0, dl_L / a_data, dl_0 / a_data, dl_L / d["fw"][0]), dl_L / a_data > 8 and dl_0 / a_data > 10 and abs(dl_L / d["fw"][0] - 2 * Zfw) < 1e-9)
kk = 2 * c * math.sqrt(0.75) * H0
check("N6  Klinkhamer-Kopp with their H_dS = sqrt(3/4) H0: A0 = %.2e = %.1fx the data (their text: 'a factor of order unity'; it is a factor ~%d)" % (kk, kk / a_data, round(kk / a_data)), 8 < kk / a_data < 11)
check("N7  Milgrom 2001.09729 near-equality 2 pi a0 ~ c H0 ~ c H_Lambda: 2 pi a0/(c H0) = %.3f, 2 pi a0/(c H_Lambda) = %.3f  (a0 = 1.2e-10): true to 10-30%%, an observation not a derivation" %
      (2 * math.pi * a_data / cH0, 2 * math.pi * a_data / cHL), 0.9 < 2 * math.pi * a_data / cH0 < 1.3 and 0.9 < 2 * math.pi * a_data / cHL < 1.5)
comp_viable = sorted(k for k, _, kind, _, _, _ in rows if kind == "computed" and viable[k])
check("N8  the COMPUTED coefficients within 30%% of the data on some footing: %s  (Verlinde, van Putten only)" % comp_viable, comp_viable == ["verl", "vp"])
check("N9  CONTROL: the T - T_Lambda family, K-K, Pikhitsa, Smolin, Milgrom-1999 and the brane n=2 balance (all Z = 1/2) must NOT be viable on either footing", not viable["dl"] and not viable["brane"])
check("N10 CONTROL: McCulloch Theta = 2.6e26 fails (%.1fx data) while Theta = 8.8e26 is %.2fx: the 'no adjustable parameter' prediction depends on the choice of Theta" %
      (d["mc07"][0] / a_data, d["mc17"][0] / a_data), d["mc07"][0] / a_data > 4 and 1.5 < d["mc17"][0] / a_data < 2.0 and not viable["mc17"] and not viable["mc07"])
check("N11 CONTROL: Hajdukovic's expression is not viable at Omega_0 - 1 = 1e-3 (%.1fx data) and diverges as Omega_0 -> 1" % (d["haj"][1] / a_data), not viable["haj"])

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
