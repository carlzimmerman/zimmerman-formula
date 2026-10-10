"""CFG581: cooling time of CFG580's hidden gas vs free fall. Criteria: FROZEN_CRITERIA.md (59dad4b30).
Needs ATOMDB=../_external_data/atomdb/atomdb_v3.1.3 (AtomDB v3.1.3, already local). MUTATE: CFG581_MUTATE=1 (mass x0.01).
"""
import os, json, math
import numpy as np
import pyatomdb

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG581_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


MSUN, MP, KPC, KEV, GYR, KB = 1.98847e33, 1.67262e-24, 3.0857e21, 1.602177e-9, 3.15576e16, 1.380649e-16
G_CGS = 6.674e-8
A0 = {"canonical": 9.36e-9, "alt": 1.13e-8}          # cm/s^2
F_REQ = {"canonical": 0.8, "alt": 0.55}
BOUND = 1.9e40
ZS = (0.1, 0.3, 1.0)
KTS = (0.10, 0.11, 0.12, 0.13)
R = 100.0
mult = 0.01 if MUTATE else 1.0

sess = pyatomdb.spectrum.CIESession()
eb = np.geomspace(0.001, 20.0, 6001); emid = np.sqrt(eb[1:] * eb[:-1])
sess.set_response(eb, raw=True)
band = (emid >= 0.5) & (emid <= 2.0)
METALS = list(range(3, 31))


def lam(kT, Z):
    sess.set_abund(METALS, Z)
    ph = sess.return_spectrum(kT)
    e = ph * emid * KEV
    return float(e.sum()), float(e[band].sum())          # bolometric, 0.5-2 keV (erg cm^3/s per n_e n_H)


P("=" * 100)
P(f"CFG581  cooling time of the hidden gas  {'*** MUTATE: mass x 0.01 ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P("\n--- controls")
L0, _ = lam(1.0, 0.0)
ff = 1.4e-27 * math.sqrt(1.0 * KEV / KB) * 1.2 * 1.4
check(abs(L0 / ff - 1) < 0.30, f"C1 Lambda(1 keV, Z=0) {L0:.3e} vs analytic bremsstrahlung {ff:.3e} erg cm^3/s (30%)")
l1, _ = lam(0.12, 1.0); l0, _ = lam(0.12, 0.0)
check(l1 / l0 > 3, f"C2 Lambda(0.12 keV) Z=1 / Z=0 = {l1 / l0:.1f} (> 3, metal lines dominate)")

res = {}
for foot, f in F_REQ.items():
    for lm in (10.8, 10.7, 10.9):
        Ms = 10 ** lm; Mg = f * Ms * mult
        V = 4 / 3 * math.pi * (R * KPC) ** 3
        nH = Mg * MSUN / (1.4 * MP * V); ne = 1.2 * nH; nion = 1.1 * nH
        Mb = (Ms + f * Ms) * MSUN                          # law mass uses the required baryons (not the MUTATE-scaled gas)
        vc = (G_CGS * Mb * A0[foot]) ** 0.25
        tff = math.sqrt(2) * R * KPC / vc
        kT_hse = 0.6 * MP * vc ** 2 / 2 / KEV
        cells = {}
        for Z in ZS:
            for kT in KTS:
                lb, lband = lam(kT, Z)
                Lx = lband * ne * nH * V / mult ** 2 * mult ** 2      # band luminosity at this density
                hidden_ref = lband * (1.2 * (f * Ms * MSUN / (1.4 * MP * V)) ** 2) * V < BOUND   # CFG580 hidden cell (true mass)
                tcool = 1.5 * (ne + nion) * kT * KEV / (ne * nH * lb)
                Eth = 1.5 * (ne + nion) * kT * KEV * V
                cells[f"{Z}|{kT}"] = dict(Z=Z, kT=kT, hidden=bool(hidden_ref), tcool_Gyr=tcool / GYR, ratio=tcool / tff,
                                          Lbol=Eth / tcool, frac_band=lband / lb)
        res[f"{foot}|{lm}"] = dict(nH=nH, vc_kms=vc / 1e5, tff_Gyr=tff / GYR, kT_hse=kT_hse, cells=cells)

P("\n--- per footing, log M* 10.8 (uniform 100 kpc sphere); hidden = CFG580's X-ray-invisible cells")
calls = {}
for foot in F_REQ:
    r = res[f"{foot}|10.8"]
    P(f"  [{foot}] n_H {r['nH']:.2e} cm^-3; v_c {r['vc_kms']:.0f} km/s; t_ff {r['tff_Gyr']:.3f} Gyr; hydrostatic kT {r['kT_hse']:.3f} keV")
    hid = [c for c in r["cells"].values() if c["hidden"]]
    for c in r["cells"].values():
        P(f"     Z={c['Z']:3.1f} kT={c['kT']:.2f}  t_cool {c['tcool_Gyr']:7.3f} Gyr  t_cool/t_ff {c['ratio']:6.2f}  "
          f"L_bol needed {c['Lbol']:.2e} erg/s ({100 * (1 - c['frac_band']):.0f}% below 0.5 keV)  {'HIDDEN' if c['hidden'] else 'seen by eROSITA'}")
    if not hid:
        calls[foot] = "NO HIDDEN CELLS"
    else:
        calls[foot] = "ESCAPE UNPHYSICAL" if all(c["ratio"] < 10 for c in hid) else "ESCAPE PHYSICALLY ALLOWED"
    P(f"     -> {calls[foot]}  (max t_cool/t_ff among hidden cells {max(c['ratio'] for c in hid) if hid else float('nan'):.2f})")
overall = calls["canonical"] if calls["canonical"] == calls["alt"] else "SPLIT"
P(f"\nVERDICT: {overall}")
P("\n--- reported: M* variants (max t_cool/t_ff over hidden cells)")
for k, r in res.items():
    hid = [c for c in r["cells"].values() if c["hidden"]]
    P(f"  [{k}] t_ff {r['tff_Gyr']:.3f} Gyr; max ratio {max(c['ratio'] for c in hid) if hid else float('nan'):.2f}; "
      f"min t_cool {min(c['tcool_Gyr'] for c in hid) if hid else float('nan'):.3f} Gyr")
# beta model centre (r_c = 10 kpc): central density vs uniform
r = np.linspace(1e-3, R, 20001); sh = (1 + (r / 10.0) ** 2) ** -0.75
cen = (4 / 3 * math.pi * R ** 3) / np.trapz(4 * math.pi * r ** 2 * sh, r)
P(f"  beta-model (r_c 10 kpc): central density / uniform = {cen:.1f} -> central t_cool shorter by that factor")
if MUTATE:
    P("MUTATE reading: t_cool must rise x100 and the escape must become PHYSICALLY ALLOWED.")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, res=res, checks=CHECKS), open(os.path.join(HERE, f"cfg581_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg581_cooling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
