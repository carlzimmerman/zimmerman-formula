#!/usr/bin/env python3
"""
MWI1 -- can published disc and bulge masses supply the Milky Way's inner baryons?
Criteria: FROZEN_CRITERIA.md (2d31b06102).   Usage: python3 mwi1.py
Writes mwi1.out, mwi1_results.json, mwi1_mut.out next to this file.
Published masses are look-ups of abstracts and are PROVISIONAL. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, copy
import numpy as np
from scipy.special import j0 as J0, j1 as J1
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
M_CENSUS = 6.681                                   # 1e10 Msun
AMP = {"canonical": (1.256, 1.310), "alt": (1.152, 1.208)}        # record, hunt item 35
COLD_GAS, HOT_GAS_27 = 1.191, 0.15                 # 1e10 Msun
INV = [("LN15", "Licquia and Newman 2015", 6.08, 1.14), ("McM17", "McMillan 2017 (the record's census)", 5.43, 0.57),
       ("C20", "Cautun et al. 2020", 5.04, 0.43), ("I25", "Imig et al. 2025 disc + bulge", 6.18, 0.21), ("L25", "Lian et al. 2025", 2.607, 0.363)]

OUT = open(os.path.join(HERE, "mwi1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 108); say(t); say("=" * 108)

# ---------------------------------------------------------------- McMillan 2017 model (as ported in dw1.py)
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def disc_mass(c):
    Rg = np.geomspace(1e-5 * KPC, 600 * KPC, 20000); return float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg), Rg))
def zprofile(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    return zg, zz
KMAX = 100.0 / KPC
KGRID = np.linspace(1e-6 * KMAX, KMAX, 30000)
KCO = np.geomspace(1e-5 / KPC, KMAX, 600)
def S_of_k(c):
    Rg = np.geomspace(1e-4 * KPC, 400 * KPC, 5000); Sg = sigma_of_R(c, Rg)
    return np.interp(KGRID, KCO, TRAPZ(Sg[None, :] * J0(KCO[:, None] * Rg[None, :]) * Rg[None, :], Rg, axis=1))
def prepare(mc):
    out = []
    for c in mc.values():
        zg, zz = zprofile(c)
        V = np.interp(KGRID, KCO, TRAPZ(zz[None, :] * np.exp(-KCO[:, None] * np.abs(zg)[None, :]), zg, axis=1))
        out.append(S_of_k(c) * V)
    return out
def gR(R_kpc, prep):
    R = R_kpc * KPC; tot = G * MBULGE / (R + ABULGE) ** 2
    for SV in prep: tot += 2 * math.pi * G * TRAPZ(KGRID * J1(KGRID * R) * SV, KGRID)
    return float(tot)
def with_scale(Rd_kpc):
    mc = copy.deepcopy(MC)
    for k in ("thin", "thick"):
        old = mc[k]["Rd"]; mc[k]["Rd"] = Rd_kpc * KPC; mc[k]["S0"] = mc[k]["S0"] * (old / mc[k]["Rd"]) ** 2    # mass fixed
    return mc

MASS = {k: disc_mass(c) / MSUN / 1e10 for k, c in MC.items()}
STARS = MASS["thin"] + MASS["thick"] + MBULGE / MSUN / 1e10; GAS = MASS["HI"] + MASS["H2"]; TOT = STARS + GAS
PREP0 = prepare(MC)
def need(f, half=False):
    lo, hi = AMP[f]
    if half: lo, hi = 1 + (lo - 1) / 2, 1 + (hi - 1) / 2
    return lo * M_CENSUS - COLD_GAS - HOT_GAS_27, hi * M_CENSUS - COLD_GAS - HOT_GAS_27
def cls(z): return "SUPPLIED" if z <= 1 else ("WITHIN 2 SIGMA" if z <= 2 else "NOT SUPPLIED")

sec("MWI1  can published disc and bulge masses supply the Milky Way's inner baryons?   (criteria 2d31b06102)")
sec("KNOWN-ANSWER CHECKS")
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)
ka("KA1 the census as ported (stars 5.49, cold gas 1.191, total 6.681, each within 0.2 per cent)",
   abs(STARS / 5.49 - 1) <= 2e-3 and abs(GAS / 1.191 - 1) <= 2e-3 and abs(TOT / 6.681 - 1) <= 2e-3, f"stars {STARS:.4f}, cold gas {GAS:.4f}, total {TOT:.4f} e10")
MB_KG = TOT * 1e10 * MSUN
fr = {R: gR(R, PREP0) * (R * KPC) ** 2 / (G * MB_KG) for R in (20.0, 25.0, 30.0)}
ka("KA2 the in-plane force routine reproduces DW1's committed ratios (1.0599, 1.0614, 1.0586), each within 0.003",
   all(abs(fr[R] - v) <= 0.003 for R, v in ((20.0, 1.0599), (25.0, 1.0614), (30.0, 1.0586))), "; ".join(f"{R:.0f} kpc {v:.4f}" for R, v in fr.items()))
nd = {f: need(f) for f in AMP}
ka("KA3 the required stellar mass (7.05 to 7.41 canonical, 6.36 to 6.73 alt, each within 0.02)",
   all(abs(a - b) <= 0.02 for a, b in zip(nd["canonical"] + nd["alt"], (7.05, 7.41, 6.36, 6.73))), "; ".join(f"{f}: {v[0]:.3f} to {v[1]:.3f}" for f, v in nd.items()))
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label."); json.dump({"lane": "MWI1", "label": "NO LABEL"}, open(os.path.join(HERE, "mwi1_results.json"), "w")); sys.exit(0)

RES = {}
MUT = open(os.path.join(HERE, "mwi1_mut.out"), "w"); MUT.write("MWI1 mutation (criteria 2d31b06102): the excess amplitude halved. Must change at least one class per footing.\n"); bite = True
for f in AMP:
    a = [cls((need(f)[0] - m) / e) for _, _, m, e in INV]; b = [cls((need(f, True)[0] - m) / e) for _, _, m, e in INV]
    ch = sum(x != y for x, y in zip(a, b)); bite &= ch >= 1
    MUT.write(f"{f}: need falls to {need(f, True)[0]:.2f} to {need(f, True)[1]:.2f}; classes changed: {ch}  [{'bites' if ch else 'DOES NOT BITE'}]\n")
MUT.close()
sec("MUTATION"); say(f"  written to mwi1_mut.out: {'bites on both footings' if bite else 'DOES NOT BITE -> no label'}")
if not bite: sys.exit(0)

sec("THE COMPARISON  z = (lower end of the required stellar mass - published) / upward error")
for f in AMP:
    lo, hi = nd[f]; rows = []; sup = []
    say(f"\n  {f}: required stellar mass {lo:.2f} to {hi:.2f} e10 Msun (total baryons {AMP[f][0]*M_CENSUS:.2f} to {AMP[f][1]*M_CENSUS:.2f}, less cold gas {COLD_GAS} and hot gas {HOT_GAS_27})")
    for i, name, m, e in INV:
        z = (lo - m) / e; c = cls(z); rows.append(dict(id=i, mass=m, err=e, z=z, cls=c, ratio=lo / m))
        if c == "SUPPLIED": sup.append(i)
        say(f"     {i:6s} {name:38s} {m:6.3f} + {e:5.3f}   z = {z:+6.2f}   needs {lo/m:4.2f} to {hi/m:4.2f} times it   {c}")
    lab = f"SUPPLIED BY {len(sup)} OF 5" + (f" ({', '.join(sup)})" if sup else "") + f"; AT THE RECORD'S CENSUS {[r['cls'] for r in rows if r['id'] == 'McM17'][0]}"
    say(f"     LABEL: {lab}")
    RES[f] = dict(label=lab, need=(lo, hi), rows=rows)

sec("REPORTED, NOT GRADED  geometry: in-plane baryonic force relative to McMillan's, stellar disc mass held fixed")
say("  both stellar discs' scale length set to the value shown (McMillan: thin 2.50, thick 3.02 kpc)")
say("  scale length [kpc]    12 kpc   16 kpc   20 kpc   24 kpc   27 kpc    mean   share of the canonical need (0.256 to 0.310)")
RES["geometry"] = {}
RADS = (12.0, 16.0, 20.0, 24.0, 27.0); g0 = {R: gR(R, PREP0) for R in RADS}
for Rd in (2.15, 2.37, 2.71, 3.0, 3.5):
    pr = prepare(with_scale(Rd)); rat = [gR(R, pr) / g0[R] for R in RADS]; mean = float(np.mean(rat))
    RES["geometry"][str(Rd)] = dict(ratios=rat, mean=mean)
    say(f"        {Rd:4.2f}            " + "   ".join(f"{v:6.3f}" for v in rat) + f"   {mean:6.3f}   {100*(mean-1)/0.310:+5.0f} to {100*(mean-1)/0.256:+5.0f} per cent")
sec("LABELS")
for f in AMP: say(f"  {f:9s}: {RES[f]['label']}")
json.dump(dict(lane="MWI1", criteria="2d31b06102", date="2026-11-12", results=RES), open(os.path.join(HERE, "mwi1_results.json"), "w"), indent=1, default=str)
say("\nMWI1 COMPLETE. Published masses are PROVISIONAL look-ups. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
