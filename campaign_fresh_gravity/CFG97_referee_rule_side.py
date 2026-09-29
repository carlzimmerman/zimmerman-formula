#!/usr/bin/env python3
"""CFG97 referee: CFG97 reproduced CFG41's law side but NOT its rule side (the four S0/S0a: -0.105 +- 0.131 dex).  Its consistency test
assumed the rule's debris enters as a velocity-squared fraction (v_law^2 (1 + f) or v_law^2 / (1 - f)).  CFG41's code (pred()) adds it to
the acceleration as an NFW enclosed mass at the colour-split collapse mass:
    v_rule^2 = v_law^2 + f_ex (1 - f_b) G M_NFW(< R_flat; M_h) / R_flat,   M_h = collapse(M*, colour) (Mandelbaum+2016, 200m -> 200c).
This script re-implements that with the referee's own code (Mandelbaum interpolation, the 200m -> 200c conversion on the Dutton-Maccio NFW,
the NFW enclosed mass) and checks the four S0/S0a rule velocities and offsets against CFG41's committed output.
  inputs    log M* (W1): real_research/data/diteodoro2023_massive_spirals.tsv; Mandelbaum+2016 Table 3: real_research/data/mandelbaum2016_lbg_halo_mass.tsv;
            R_flat, v_law and v_rule (printed to 0.1): CFG41_massive_spirals_hi.out; f_ex and the per-galaxy law / rule offsets: CFG41's results JSON.
  conventions (CFG36 / h48, not results): M_h is M_200c; c = 10^(0.905 - 0.101 (log10(M_200c h) - 12)), h = 0.674; rho_crit for H0 = 67.4;
            Mandelbaum masses in h^-1 Msun with h = 0.673, 200 x the mean density with Omega_m = 0.315; f_b = 0.02237 / (0.02237 + 0.1200);
            NFW radius clipped to [1e-4, 5] R_200.  f_ex itself (the edge-phantom deficit) is taken from CFG41, not re-derived.
Run: python3 campaign_fresh_gravity/CFG97_referee_rule_side.py
"""
import os, re, json, math
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "real_research", "data")
print(__doc__.split("Run:")[0].strip() + "\n")

GK = 4.30091e-6                                           # kpc (km/s)^2 / Msun
RHOC = 2.77536627e11 * 0.674 ** 2 / 1e9                   # Msun / kpc^3 (3 H0^2 / 8 pi G, H0 = 67.4)
OM, FB = 0.315, 0.02237 / (0.02237 + 0.1200)
mu = lambda t: math.log1p(t) - t / (1 + t)
conc = lambda m200c: 10 ** (0.905 - 0.101 * (math.log10(m200c * 0.674) - 12.0))
r200c = lambda m200c: (3 * m200c / (4 * math.pi * 200 * RHOC)) ** (1 / 3)


def m_nfw(m200c, r):
    x = min(max(r / r200c(m200c), 1e-4), 5.0)
    c = conc(m200c)
    return m200c * mu(c * x) / mu(c)


def m200m_of(m200c):
    c, R = conc(m200c), r200c(m200c)
    rm = brentq(lambda r: m200c * mu(c * r / R) / mu(c) / (4 / 3 * math.pi * r ** 3) - 200 * OM * RHOC, R, 10 * R, xtol=1e-12)
    return m200c * mu(c * rm / R) / mu(c)


def collapse(lms, colour):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "mandelbaum2016_lbg_halo_mass.tsv")) if l.strip() and not l.startswith("#")]
    t = np.array([[float(r[1]), float(r[3])] for r in rows[1:] if r[0] == colour])
    m200m = 10 ** np.interp(lms, t[:, 0], t[:, 1]) / 0.673
    return 10 ** brentq(lambda lm: m200m_of(10 ** lm) - m200m, math.log10(m200m) - 1, math.log10(m200m), xtol=1e-12)


lms = {}
for l in open(os.path.join(DATA, "diteodoro2023_massive_spirals.tsv")):
    if l.startswith("#") or not l.strip():
        continue
    p = l.rstrip("\n").split("\t")
    if p[0] == "name":
        hdr = p; continue
    lms[p[0]] = float(p[hdr.index("logMs_W1")])
out = open(os.path.join(HERE, "CFG41_massive_spirals_hi.out")).read()
rows = {m.group(1): dict(col=m.group(2), R=float(m.group(3)), vl=float(m.group(4)), vr=float(m.group(5)))
        for m in re.finditer(r"^\s+(\S+)\s+T\s+\S+\s+(red|blue)\s+log M_b\s+\S+\s+R_flat\s+([0-9.]+) kpc.*?law\s+([0-9.]+); rule\s+([0-9.]+)", out, re.M)}
res = json.load(open(os.path.join(HERE, "CFG41_massive_spirals_hi_results.json")))["numbers"]
S0 = [n for n, r in rows.items() if r["col"] == "red"]
fex = dict(zip(S0, res["fex_s0"]))
lawp = dict(zip(S0, res["RES"]["canonical|law|s0"]["per"])); rulep = dict(zip(S0, res["RES"]["canonical|rule|s0"]["per"]))
assert len(S0) == 4

print(f"f_b = {FB:.5f}; rho_crit = {RHOC:.4e} Msun/kpc^3; a Mandelbaum-to-200c check: log M_h(red, log M* 11.3) = {math.log10(collapse(11.3, 'red')):.4f}")
dv, dof, mine = [], [], []
for n in S0:
    r = rows[n]; mh = collapse(lms[n], "red")
    vr = math.sqrt(r["vl"] ** 2 + fex[n] * (1 - FB) * GK * m_nfw(mh, r["R"]) / r["R"])
    shift = math.log10(vr / r["vl"]); o = lawp[n] - shift
    dv.append(vr - r["vr"]); dof.append(o - rulep[n]); mine.append(o)
    print(f"    {n:9s} log M* {lms[n]:.2f}  log M_h {math.log10(mh):.3f}  R_flat {r['R']:5.1f}  f_ex {fex[n]:.4f}  v_law {r['vl']:5.1f}  v_rule: mine {vr:6.2f}, CFG41 {r['vr']:5.1f}"
          f"  | rule offset mine {o:+.4f}, CFG41 {rulep[n]:+.4f}")
m = float(np.mean(mine))
print(f"\nmax |v_rule mine - CFG41| = {max(abs(x) for x in dv):.2f} km/s (CFG41 prints to 0.1); max |offset difference| = {max(abs(x) for x in dof):.1e} dex")
print(f"S0/S0a rule offset: raw mean {m:+.4f} (CFG41 {res['RES']['canonical|rule|s0']['raw']:+.4f}); corrected (B = 0.076) {m - 0.076:+.4f} (CFG41 -0.105); "
      f"rule-minus-law shift {np.mean([lawp[n] - x for n, x in zip(S0, mine)]):.4f} dex (CFG41 README 0.109)")
for f, lab in ((lambda vl, fx, a: vl * math.sqrt(1 + fx), "v_law^2 (1 + f_ex)"), (lambda vl, fx, a: vl / math.sqrt(1 - fx), "v_law^2 / (1 - f_ex)")):
    sh = np.mean([math.log10(f(rows[n]["vl"], fex[n], None) / rows[n]["vl"]) for n in S0])
    print(f"CFG97's consistency forms for contrast: {lab}: mean shift {sh:.3f} dex")
