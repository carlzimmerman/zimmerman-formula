"""CFG580: can hidden hot gas supply the KiDS early-type shortfall? Criteria: FROZEN_CRITERIA.md (c147d86a6).

APEC band emissivities from AtomDB v3.1.3 (official CfA release, md5 c6f13b893358cc17e35f22cb81a8490b) via pyatomdb 1.2.2;
set ATOMDB to the unpacked release (outside the repo: ../_external_data/atomdb/atomdb_v3.1.3).
MUTATE: CFG580_MUTATE=1 multiplies the gas mass by 0.01 (must give ESCAPE OPEN).
"""
import os, json, math
import numpy as np
import pyatomdb

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG580_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


MSUN, MP, KPC, KEV = 1.98847e33, 1.67262e-24, 3.0857e21, 1.602177e-9
BOUND = 1.9e40                       # erg/s, eRASS:4 quiescent 2-sigma upper, log M* 10.5-11.0
L_QU, L_QU_ERR = 1.1e40, 0.4e40
F_REQ = {"canonical": 0.8, "alt": 0.55}
LOGMS = (10.8, 10.7, 10.9)
ZS = (0.1, 0.3, 1.0)
KT = np.round(np.arange(0.08, 0.3001, 0.01), 3)
KT_PRIM = (0.10, 0.13)

eb = np.linspace(0.5, 2.0, 1501)
emid = 0.5 * (eb[1:] + eb[:-1])
sess = pyatomdb.spectrum.CIESession()
sess.set_response(eb, raw=True)
METALS = list(range(3, 31))


def band_emissivity(kT, Z):
    """erg cm^3 s^-1 per unit n_e n_H in rest-frame 0.5-2 keV (APEC photons cm^3 s^-1 bin^-1 x E)."""
    sess.set_abund(METALS, Z)
    ph = sess.return_spectrum(kT)
    return float(np.sum(ph * emid) * KEV)


def em_uniform(Mgas, R):
    V = 4 / 3 * math.pi * (R * KPC) ** 3
    nH = Mgas * MSUN / (1.4 * MP * V)
    return 1.2 * nH * nH * V


def em_beta(Mgas, R, rc=10.0, beta=0.5):
    r = np.linspace(1e-3, R, 20001)
    shape = (1 + (r / rc) ** 2) ** (-1.5 * beta)
    rcm = r * KPC
    mass_unit = np.trapz(4 * math.pi * rcm ** 2 * shape, rcm)          # integral of shape dV
    nH0 = Mgas * MSUN / (1.4 * MP * mass_unit)
    return 1.2 * nH0 ** 2 * np.trapz(4 * math.pi * rcm ** 2 * shape ** 2, rcm)


P("=" * 100)
P(f"CFG580  hot-gas escape vs eRASS:4 (APEC, AtomDB v3.1.3)  {'*** MUTATE: gas mass x 0.01 ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P(f"bound: L(0.5-2 keV) < {BOUND:.2e} erg/s (QU stack {L_QU:.1e} +- {L_QU_ERR:.1e}); required gas f M*, f = {F_REQ}")

P("\n--- controls")
eps0 = band_emissivity(0.3, 0.0)
T_K = 0.3 * KEV / 1.380649e-16
ff = 1.4e-27 * math.sqrt(T_K) * 1.2 * 1.4 * (math.exp(-0.5 / 0.3) - math.exp(-2.0 / 0.3))
check(abs(eps0 / ff - 1) < 0.30, f"C1 Z=0 APEC band emissivity at 0.3 keV {eps0:.3e} vs analytic free-free (Gaunt 1.2) {ff:.3e} erg cm^3/s (30%)")
e1, e3 = band_emissivity(0.12, 0.1), band_emissivity(0.12, 1.0)
check(e3 > e1, f"C2 emissivity rises with Z at 0.12 keV: Z=0.1 {e1:.3e}, Z=1 {e3:.3e}")

EPS = {Z: {float(k): band_emissivity(float(k), Z) for k in KT} for Z in ZS}
P("\n--- band emissivity (erg cm^3/s per n_e n_H), 0.5-2 keV")
for Z in ZS:
    P(f"  Z={Z:3.1f}: " + "  ".join(f"{k:.2f}:{EPS[Z][float(k)]:.2e}" for k in KT[::2]))

mult = 0.01 if MUTATE else 1.0
res = {}
for foot, f in F_REQ.items():
    for lm in LOGMS:
        Mg = f * 10 ** lm * mult
        emU, emB = em_uniform(Mg, 100.0), em_beta(Mg, 100.0)
        rows = {}
        for Z in ZS:
            LU = {k: EPS[Z][k] * emU for k in EPS[Z]}; LB = {k: EPS[Z][k] * emB for k in EPS[Z]}
            prim = [LU[k] for k in LU if KT_PRIM[0] - 1e-9 <= k <= KT_PRIM[1] + 1e-9]
            rows[Z] = dict(L_uniform=LU, L_beta=LB, min_primary=min(prim), max_primary=max(prim))
        res[f"{foot}|{lm}"] = dict(Mgas=Mg, em_uniform=emU, em_beta=emB, rows=rows)

P("\n--- predicted L(0.5-2 keV) for the uniform 100 kpc sphere (minimum-luminosity case), primary kT 0.10-0.13 keV")
for key, r in res.items():
    s = "  ".join(f"Z={Z}: {r['rows'][Z]['min_primary']:.2e}-{r['rows'][Z]['max_primary']:.2e}" for Z in ZS)
    P(f"  [{key}] Mgas {r['Mgas']:.2e}  {s}")

closed = all(res[f"{foot}|10.8"]["rows"][Z]["min_primary"] > BOUND for foot in F_REQ for Z in ZS)
P(f"\nVERDICT (primary: log M* 10.8, uniform sphere, all Z, kT 0.10-0.13): {'ESCAPE CLOSED' if closed else 'ESCAPE OPEN'}")
if not closed:
    for foot in F_REQ:
        for Z in ZS:
            hid = [k for k, L in res[f"{foot}|10.8"]["rows"][Z]["L_uniform"].items() if KT_PRIM[0] - 1e-9 <= k <= KT_PRIM[1] + 1e-9 and L <= BOUND]
            if hid: P(f"  hides: {foot} Z={Z} at kT {hid}")

P("\n--- reported: full kT grid (log M* 10.8, canonical f=0.8, uniform); where it would hide")
for Z in ZS:
    hid = [k for k, L in res["canonical|10.8"]["rows"][Z]["L_uniform"].items() if L <= BOUND]
    P(f"  Z={Z}: L at kT 0.08 / 0.10 / 0.13 / 0.20 / 0.30 = " + " / ".join(f"{res['canonical|10.8']['rows'][Z]['L_uniform'][k]:.2e}" for k in (0.08, 0.1, 0.13, 0.2, 0.3))
      + f"; below bound at kT {hid if hid else 'none'}")
P("\n--- reported: gas fraction that would just reach the bound (uniform, log M* 10.8)")
for Z in ZS:
    for k in (0.10, 0.13):
        Lper = EPS[Z][k] * em_uniform(10 ** 10.8, 100.0)            # L for f = 1 ; L scales as f^2
        P(f"  Z={Z} kT={k}: f_bound = {math.sqrt(BOUND / Lper):.3f}")
P("\n--- reported: beta-model (rc 10 kpc) / uniform luminosity ratio = " + f"{res['canonical|10.8']['em_beta'] / res['canonical|10.8']['em_uniform']:.1f}")
if MUTATE:
    P("MUTATE reading: gas mass x0.01 must give ESCAPE OPEN.")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict="CLOSED" if closed else "OPEN", res={k: dict(Mgas=v["Mgas"], rows={str(Z): {kk: (vv if not isinstance(vv, dict) else {str(a): b for a, b in vv.items()}) for kk, vv in rr.items()} for Z, rr in v["rows"].items()}) for k, v in res.items()},
               checks=CHECKS), open(os.path.join(HERE, f"cfg580_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg580_apec{TAG}.out"), "w").write("\n".join(OUT) + "\n")
