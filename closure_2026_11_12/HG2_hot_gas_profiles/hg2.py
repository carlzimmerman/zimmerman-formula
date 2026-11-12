#!/usr/bin/env python3
"""
HG2 -- MWG1 redone with published hot-gas density laws (full texts).  Criteria: FROZEN_CRITERIA.md
(sha256 in FREEZE_STAMP.txt).  Part 1: hot gas (halo plus disc-like) inside 27 kpc against the rotation
curve's need.  Part 2: MWJ1's three gates (functions copied from MWG1's mwg1.py) with the census at A = 1
plus each published profile, per external field.
Usage: python3 hg2.py      Reads NMB1's and PLT1's result files (read only).
Writes hg2.out, hg2_results.json, hg2_mut.out (mutations), hg2_extrap.out (variant, no label).
Literature values are PROVISIONAL web look-ups of arXiv full texts. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
N1 = json.load(open(os.path.join(HERE, "..", "NMB1_nimble_curves_vs_line", "nmb1_results.json")))
P1 = json.load(open(os.path.join(HERE, "..", "PLT1_outer_mass_vs_literature", "plt1_results.json")))
TH = np.array(N1["theta"]); VI = np.linalg.inv(np.array(N1["V"]))
ROWS = {c: P1["rows"][c] for c in ("H", "S")}

# ---------------------------------------------------------------- SI constants
G, MSUN, KPC, MP = 6.674e-11, 1.989e30, 3.0857e19, 1.67262e-27
CM3 = 1e6                          # cm^-3 -> m^-3
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
X_H = 0.71                          # hydrogen mass fraction (assumed, disclosed)
MU_E = 2.0 / (1.0 + X_H)            # mass per electron / m_p  = 1.17
MU_H = 1.0 / X_H                    # mass per H / m_p          = 1.41
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_REC, QGATE, FLOOR = 0.01273, 6.180, 0.20
EG = np.round(np.arange(0.0, 0.03 + 1e-9, 0.0005), 4)
M_CENSUS = 6.681e10
NEED = {"canonical": ((1.256 - 1) * M_CENSUS, (1.310 - 1) * M_CENSUS), "alt": ((1.152 - 1) * M_CENSUS, (1.208 - 1) * M_CENSUS)}
R_RC = 27.0
RTAB = (27.0, 30.0, 80.0, 100.0, 150.0, 200.0, 273.0)

OUTNAME = "hg2_extrap.out" if (len(sys.argv) > 1 and sys.argv[1] == "--extrap") else "hg2.out"
OUT = open(os.path.join(HERE, OUTNAME), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 110); say(t); say("=" * 110)

# ---------------------------------------------------------------- density laws -> enclosed mass [Msun], SI inside
def m_powerlaw(C_cgs, a, mu, r_kpc):
    """n = C r^-a (C in cm^-3 kpc^a); M = mu m_p 4 pi C r^(3-a)/(3-a), all in SI."""
    C_si = C_cgs * CM3 * KPC ** a                # m^-3 m^a
    r = r_kpc * KPC
    return mu * MP * 4 * math.pi * C_si * r ** (3 - a) / (3 - a) / MSUN
def m_shell(nfun_si, mu, r_kpc):
    """numerical shell integral of n(r) [m^-3], r in m."""
    f = lambda r: 4 * math.pi * r * r * nfun_si(r)
    return mu * MP * quad(f, 0.0, r_kpc * KPC, limit=400, points=[KPC * 1.0, KPC * 10.0])[0] / MSUN
def m_disc(n0_cgs, Rfun, zh_kpc, mu, r_kpc):
    """spherical enclosed mass of n = n0 S(R) exp(-|z|/zh), both sides of the plane."""
    n0 = n0_cgs * CM3; zh = zh_kpc * KPC; r = r_kpc * KPC
    f = lambda R: 2 * math.pi * R * Rfun(R / KPC) * 2 * zh * (1 - math.exp(-math.sqrt(max(r * r - R * R, 0.0)) / zh))
    return mu * MP * n0 * quad(f, 0.0, r, limit=400)[0] / MSUN

Z03 = 0.3
# --- MB15: eq. 2, Table 2 (O VIII thin) 1.35e-2 cm^-3 kpc^1.5, beta 0.50, solar-emissivity fit; outer 250 kpc
MB15_C, MB15_A = 1.35e-2, 1.5
def mb15(r, zpow=1.0): return m_powerlaw(MB15_C / Z03 ** zpow, MB15_A, MU_E, r)
# --- MB13: eq. 5, Table 2 saturated: n0 0.46, rc 0.35, beta 0.71, + ambient 1e-5 to 200 kpc; n_e proportional to Z^-1 (eq. 4)
def mb13_n_solar(r_m):
    rk = r_m / KPC
    return (0.46 * (1 + (rk / 0.35) ** 2) ** (-1.5 * 0.71) + (1e-5 if rk <= 200.0 else 0.0)) * CM3
_MB13 = {}
def mb13(r, z=Z03):
    if r not in _MB13: _MB13[r] = m_shell(mb13_n_solar, MU_E, min(r, 200.0))
    return _MB13[r] / z
# --- S15: power law through n(48.2) = 1.1e-4 and M(300) = 2.6e10, rho = 0.6 m_p n (mu assumed)
S15_NP, S15_RP, S15_M300, S15_MU = 1.1e-4, 48.2, 2.6e10, 0.6
def s15_mass(a, r): return m_powerlaw(S15_NP * S15_RP ** a, a, S15_MU, r)
S15_A = brentq(lambda a: s15_mass(a, 300.0) - S15_M300, 0.3, 2.0)
S15_C = S15_NP * S15_RP ** S15_A
# --- F17: reconstruction, n_H through Table 3's 1.3e-4 (50 kpc) and 0.83e-4 (100 kpc); mass per H MU_H; outer 250
F17_S = math.log(1.3 / 0.83) / math.log(2.0)
F17_C = 1.3e-4 * 50.0 ** F17_S
# --- F20: Table 1 approximation n_H = 1.3e-5 (r/283)^-0.93; outer 283
F20_A = 0.93; F20_C = 1.3e-5 * 283.0 ** F20_A
# --- B18: beta = 0.5 power law normalised to M(<250) = 2.8e10; hot disc 1.8e8 (no law printed -> all inside 27 kpc)
def b18(r): return 2.8e10 * (min(r, 250.0) / 250.0) ** 1.5
# --- K20b: n = nc (r/rc)^-3b, nc 0.0044, rc 2.4, beta 0.39; outer 260
K20_A = 3 * 0.39; K20_C = 0.0044 * 2.4 ** K20_A
# --- L24: combined beta = 0.5: C 4.6e-2 (Z = 0.1); L24z: C 1.36e-2 (Z = 0.3, kT 0.225); outer 350
expR = lambda Rh: (lambda R: math.exp(-R / Rh))
def k20_emp(R): return 1.0 if R < 5.5 else math.exp(-(R - 5.5) / 2.0)
DISCS = {   # id: (n0, S(R), zh, mu, printed mass or None, description)
    "D-L24":  (3.2e-2, expR(6.2), 1.1, MU_E, None, "Locatelli 2024 combined b=0.5 disc (Z=0.1)"),
    "D-L24z": (9.4e-3, expR(6.2), 1.1, MU_E, None, "Locatelli 2024 combined+high eps disc (Z=0.3)"),
    "D-L24d": (1.7e-2, expR(8.0), 3.3, MU_E, None, "Locatelli 2024 disc-only model (Z=0.1)"),
    "D-K20e": (0.0081, k20_emp, 1.60, MU_E, 2e7, "Kaaret 2020 empirical disc (with adiabatic halo, Z=0.3)"),
    "D-K20x": (0.012, expR(5.4), 2.8, MU_E, None, "Kaaret 2020 exponential disc model (Z=0.3)"),
    "D-N18":  (10 ** -2.42, expR(7.03), 2.73, 0.61, 5e7, "Nakashima 2018 Suzaku disc (solar Z, mu 0.61)"),
}
_DM = {}
def disc_mass(d, r):
    if (d, r) not in _DM:
        n0, S, zh, mu, _, _ = DISCS[d]; _DM[(d, r)] = m_disc(n0, S, zh, mu, r)
    return _DM[(d, r)]
def b18_disc(r): return 1.8e8 if r >= R_RC else 1.8e8 * (r / R_RC) ** 3   # no law printed; placed inside 27 kpc

ROUT = {"MB15": 250.0, "MB15h": 250.0, "MB13": 200.0, "S15": 300.0, "F17": 250.0, "F20": 283.0, "B18": 250.0, "K20b": 260.0, "L24": 350.0, "L24z": 350.0}
EXTRAP = False
def halo(g, r):
    rr = r if EXTRAP else min(r, ROUT[g])
    if g == "MB15": return mb15(rr, 1.0)
    if g == "MB15h": return mb15(rr, 0.5)
    if g == "MB13": return mb13(rr) if not EXTRAP else mb13(min(rr, 200.0)) + (m_powerlaw(1e-5 / Z03, 0.0, MU_E, rr) - m_powerlaw(1e-5 / Z03, 0.0, MU_E, 200.0) if rr > 200 else 0.0)
    if g == "S15": return m_powerlaw(S15_C, S15_A, S15_MU, rr)
    if g == "F17": return m_powerlaw(F17_C, F17_S, MU_H, rr)
    if g == "F20": return m_powerlaw(F20_C, F20_A, MU_H, rr)
    if g == "B18": return 2.8e10 * (rr / 250.0) ** 1.5
    if g == "K20b": return m_powerlaw(K20_C, K20_A, MU_E, rr)
    if g == "L24": return m_powerlaw(4.6e-2, 1.5, MU_E, rr)
    if g == "L24z": return m_powerlaw(1.36e-2, 1.5, MU_E, rr)
    raise KeyError(g)
OWN_DISC = {"L24": "D-L24", "L24z": "D-L24z", "K20b": "D-K20e", "B18": "B18disc"}
def disc_of(g, r):
    d = OWN_DISC.get(g)
    if d is None: return 0.0
    return b18_disc(r) if d == "B18disc" else disc_mass(d, r)
def m_hot(g, r, scale=1.0):
    if g is None: return 0.0
    return scale * (halo(g, r) + disc_of(g, r))
MODELS = ["MB15", "MB15h", "MB13", "S15", "F17", "F20", "B18", "K20b", "L24", "L24z"]

# ---------------------------------------------------------------- McMillan 2017 baryons (copied from mwg1.py)
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def zcum(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); return zg, cum / cum[-1]
_MS = {}
def M_sph(r_kpc):
    if r_kpc not in _MS:
        r = float(r_kpc) * KPC; tot = MBULGE * r ** 2 / (r + ABULGE) ** 2
        Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for c in MC.values():
            zg, cum = zcum(c); tot += float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
        _MS[r_kpc] = tot
    return _MS[r_kpc]

def nu_fw(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
MU = np.linspace(-1.0, 1.0, 4001)
def M_line(r, a0, eN, A, kern=nu_fw, gas=None, gscale=1.0):
    Mb = A * M_sph(r) + m_hot(gas, r, gscale) * MSUN; gb = G * Mb / (r * KPC) ** 2 / a0
    if eN == 0.0: return float(kern(gb)) * Mb / MSUN / 1e11
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * MU)
    return float(TRAPZ(kern(gm) * (gb + eN * MU), MU) / 2.0) / gb * Mb / MSUN / 1e11

S_FL = math.log10(1.0 + FLOOR)
def pull(Ml, r):
    side = math.log10(r["M"] / (r["M"] - r["lo"])) if Ml < r["M"] else math.log10((r["M"] + r["hi"]) / r["M"])
    return (math.log10(Ml) - math.log10(r["M"])) / math.hypot(side, S_FL)
RADII = sorted({r["r"] for c in ROWS for r in ROWS[c]})
def evaluate(a0, e, gas=None, gscale=1.0):
    line = {r: M_line(r, a0, e, 1.0, nu_fw, gas, gscale) for r in [30.0, 80.0] + RADII}
    d = np.array([math.log10(line[30.0]), math.log10(line[80.0])]) - TH
    Q = float(d @ VI @ d); med, medp = {}, {}
    for c, rws in ROWS.items():
        z = [(pull(line[r["r"]], r), r["r"]) for r in rws]
        med[c] = float(np.median([v for v, _ in z])); medp[c] = float(np.median([v for v, rr in z if rr >= 150.0]))
    g1 = Q <= QGATE; g2 = all(abs(v) <= 2 for v in med.values()); g2p = all(abs(v) <= 2 for v in medp.values())
    return dict(Q=Q, med=med, medp=medp, g1=g1, g2=g2, g2p=g2p, ok=g1 and g2 and g2p, line80=line[80.0])
def failing(ev):
    out = []
    if not ev["g1"]: out.append(f"curves (Q {ev['Q']:.1f})")
    if not ev["g2"]: out.append("outer masses (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["med"].items() if abs(v) > 2) + ")")
    if not ev["g2p"]: out.append("plateau rows (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["medp"].items() if abs(v) > 2) + ")")
    return "; ".join(out) if out else "none"
def window(a0, gas, gscale=1.0):
    fl = [evaluate(a0, float(e), gas, gscale)["ok"] for e in EG]
    ok = [float(e) for e, f in zip(EG, fl) if f]
    return (None if not ok else (min(ok), max(ok))), fl
def fmt(r): return "empty" if r is None else f"[{r[0]:.4f}, {r[1]:.4f}]"
def gaps(fl):
    """report whether the passing set is contiguous."""
    idx = [i for i, f in enumerate(fl) if f]
    return bool(idx) and (idx[-1] - idx[0] + 1 != len(idx))

def part1(scale=1.0):
    res = {}
    sup = {g: scale * (halo(g, R_RC) + disc_of(g, R_RC)) for g in MODELS}
    for f in A0:
        lo, hi = NEED[f]; k = sum(s >= lo for s in sup.values())
        res[f] = "ROTATION CURVE NOT SUPPLIED" if k == 0 else f"SUPPLIED IN {k} OF {len(MODELS)}"
    return res, sup

# ================================================================== variant mode (extrapolated laws, no label)
if len(sys.argv) > 1 and sys.argv[1] == "--extrap":
    EXTRAP = True
    sec("HG2 VARIANT: every law extrapolated to 273 kpc (no outer edge). Reported, not labelled.")
    for f, a0 in A0.items():
        for g in MODELS:
            w, fl = window(a0, g); ev = evaluate(a0, E_REC, g)
            say(f"  {f:9s} {g:6s} M(<273) {m_hot(g, 273.0)/1e10:6.2f}e10   window {fmt(w):18s}  at 0.01273: {'passes' if ev['ok'] else 'fails ' + failing(ev)}")
    say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing."); sys.exit(0)

sec("HG2  MWG1 redone with published hot-gas density laws (criteria: FROZEN_CRITERIA.md, sha256 in FREEZE_STAMP.txt)")
say(f"  conversions: mass per electron {MU_E:.3f} m_p, per H {MU_H:.3f} m_p (X = {X_H}); S15 mu {S15_MU}; N18 mu 0.61 (their eq. 11)")
sec("KNOWN-ANSWER CHECKS")
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)
r0 = {f: evaluate(a0, E_REC) for f, a0 in A0.items()}; w0 = {f: window(a0, None)[0] for f, a0 in A0.items()}
ka("KA1 no gas reproduces MWJ1 (Q 4.89 / 2.91; satellite plateau -2.72; window 0 to 0.0075)",
   abs(r0["canonical"]["Q"] - 4.89) <= 0.03 and abs(r0["alt"]["Q"] - 2.91) <= 0.03 and all(abs(r0[f]["medp"]["S"] + 2.72) <= 0.02 for f in A0)
   and all(w0[f] == (0.0, 0.0075) for f in A0),
   "; ".join(f"{f}: Q {r0[f]['Q']:.2f}, S plateau {r0[f]['medp']['S']:+.2f}, window {fmt(w0[f])}" for f in A0))
m50, m250 = mb15(50.0, 1.0), mb15(250.0, 1.0)
m50h, m250h = mb15(50.0, 0.5), mb15(250.0, 0.5)
m50s = m_powerlaw(MB15_C, MB15_A, MU_E, 50.0)
ka("KA2 MB15's printed law (n_e, 1.17 m_p per electron, density x (Z/Zsun)^-1 at 0.3) gives 3.8e9 (<50) and 4.3e10 (<250) within 5 per cent",
   abs(m50 / 3.8e9 - 1) <= 0.05 and abs(m250 / 4.3e10 - 1) <= 0.05,
   f"Z^-1: {m50:.3e} / {m250:.3e};  Z^-1/2 (emission scaling): {m50h:.3e} / {m250h:.3e};  solar as printed: {m50s:.3e}")
l80 = [evaluate(A0["canonical"], 0.0)["line80"], evaluate(A0["alt"], 0.0)["line80"], r0["canonical"]["line80"], r0["alt"]["line80"]]
ka("KA3 the line at 80 kpc with no gas within 0.5 per cent of 5.691 / 6.219 / 4.977 / 5.109",
   all(abs(a / b - 1) <= 0.005 for a, b in zip(l80, (5.691, 6.219, 4.977, 5.109))), "; ".join(f"{v:.3f}" for v in l80))
f258, f283 = halo("F20", 258.0), halo("F20", 283.0)
ka("KA4 F20's Table 1 approximation gives 4.6e10 (<258) and 5.5e10 (<283) within 20 per cent",
   abs(f258 / 4.6e10 - 1) <= 0.20 and abs(f283 / 5.5e10 - 1) <= 0.20, f"{f258:.3e} / {f283:.3e}  (ratios {f258/4.6e10:.3f} / {f283/5.5e10:.3f})")
C_si = MB15_C / Z03 * CM3 * KPC ** 1.5
num = m_shell(lambda r: C_si * r ** -1.5, MU_E, 250.0)
ka("KA5 SI shell integral of MB15's law equals the closed form within 0.1 per cent", abs(num / m250 - 1) <= 1e-3, f"{num:.5e} vs {m250:.5e}")
say("\n  reported, not blocking:")
say(f"    MB13 solar: {mb13(18.0, 1.0):.2e} (<18) vs 2.2e8; {mb13(200.0, 1.0):.2e} (<200) vs 1.2e10;  at 0.3 Zsun: {mb13(18.0):.2e} vs 7.5e8; {mb13(200.0):.2e} vs 3.8e10")
say(f"    F17 reconstruction: slope {F17_S:.3f}; {halo('F17', 250.0):.3e} (<250) vs 1.2e11 (ratio {halo('F17', 250.0)/1.2e11:.3f}); mean n_H inside 250 {3/(3-F17_S)*F17_C*250**-F17_S:.2e} vs 4.6e-5")
say(f"    S15: solved slope 3b = {S15_A:.3f} (b = {S15_A/3:.3f}); n0 rc^3b = {S15_C:.4f} (Salem's sampled range 0.005 to 0.03: {'inside' if 0.005 <= S15_C <= 0.03 else 'OUTSIDE'})")
for d, (n0, S, zh, mu, pm, desc) in DISCS.items():
    tot = disc_mass(d, 1000.0)
    say(f"    {d:7s} total {tot:.2e}  (one side {tot/2:.2e})" + (f"  printed {pm:.0e}: ratio {tot/pm:.2f} (one side {tot/2/pm:.2f})" if pm else "") + f"   [{desc}]")
say(f"    L24 halo <250: {halo('L24', 250.0):.2e}; L24z <250: {halo('L24z', 250.0):.2e}  (paper: 'some 1e9 to some 1e10')")
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label.")
    json.dump({"lane": "HG2", "label": "NO LABEL", "failed": FAIL}, open(os.path.join(HERE, "hg2_results.json"), "w")); sys.exit(0)

# ---------------------------------------------------------------- mutations
MUT = open(os.path.join(HERE, "hg2_mut.out"), "w"); MUT.write("HG2 mutations (criteria FROZEN_CRITERIA.md). Must bite.\n"); bite = True
for f, a0 in A0.items():
    ev = evaluate(a0, 0.0, "MB15", 10.0); b = not ev["ok"]; bite &= b
    MUT.write(f"{f}: M1 ten times the MB15 gas at (e_N = 0, census): fails {failing(ev)} [{'bites' if b else 'DOES NOT BITE'}]\n")
lab_m2, sup0 = part1(1.0)
big = max(sup0.values()); gbig = max(sup0, key=sup0.get)
for f in A0:
    lo = NEED[f][0]; b = 10 * big >= lo; bite &= b
    MUT.write(f"{f}: M2 ten times the largest Part 1 supply ({gbig}, {big/1e10:.3f}e10 -> {10*big/1e10:.2f}e10) against need {lo/1e10:.2f}e10: {'SUPPLIED' if b else 'NOT SUPPLIED'} [{'bites' if b else 'DOES NOT BITE'}]\n")
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()
sec("MUTATIONS"); say(f"  written to hg2_mut.out: {'bite on both footings' if bite else 'DO NOT BITE -> no label'}")
if not bite: sys.exit(0)

RES = {"part1": {}, "part2": {}, "masses": {}, "discs": {}}
sec("ENCLOSED MASSES from the published laws [1e10 Msun]  (halo + own disc; constant beyond the paper's outer radius)")
say("  model    r_out   " + "  ".join(f"<{int(r):3d}" for r in RTAB))
for g in MODELS:
    vals = [m_hot(g, r) for r in RTAB]; RES["masses"][g] = dict(zip([str(r) for r in RTAB], vals))
    say(f"  {g:7s}  {ROUT[g]:5.0f}   " + "  ".join(f"{v/1e10:5.2f}" for v in vals))
say("\n  disc-like components alone [1e10 Msun]:   <27 kpc     total")
for d in DISCS:
    a, t = disc_mass(d, 27.0), disc_mass(d, 1000.0); RES["discs"][d] = dict(m27=a, total=t)
    say(f"     {d:7s}  {a/1e10:8.4f}   {t/1e10:8.4f}    {DISCS[d][5]}")
say(f"     D-B18    {1.8e8/1e10:8.4f}   {1.8e8/1e10:8.4f}    Bregman 2018 hot disc (printed mass, placed inside 27 kpc)")

sec("PART 1  the rotation curve: halo + disc-like hot gas inside 27 kpc against the need")
lab1, sup = part1(1.0)
for f in A0:
    lo, hi = NEED[f]
    say(f"\n  {f}: need {lo/1e10:.2f} to {hi/1e10:.2f} e10 Msun")
    for g in MODELS:
        s = sup[g]; RES["part1"][f"{f}|{g}"] = dict(supplied=s, halo=halo(g, R_RC), disc=disc_of(g, R_RC), share_lo=s / lo, share_hi=s / hi)
        say(f"     {g:6s} {s/1e10:6.3f}  (halo {halo(g, R_RC)/1e10:.3f} + disc {disc_of(g, R_RC)/1e10:.3f})  share {100*s/hi:4.1f} to {100*s/lo:4.1f} per cent")
    for d in DISCS:
        s = disc_mass(d, R_RC); say(f"     disc {d:7s} alone {s/1e10:6.4f}  share {100*s/hi:4.1f} to {100*s/lo:4.1f} per cent")
    RES["part1"][f] = lab1[f]; say(f"     PART 1 LABEL: {lab1[f]}")

sec("PART 2  the outer data: census at A = 1 plus each published profile")
for f, a0 in A0.items():
    say(f"\n  {f}:")
    say("     model   window (all three gates)   at 0.01273: Q; outer medians H / S; plateau medians H / S -> fails")
    ans = {}
    for g in [None] + MODELS:
        w, fl = window(a0, g); ev = evaluate(a0, E_REC, g)
        low = any(fl[i] for i in range(len(EG)) if EG[i] <= 0.008)
        ans[g] = ev["ok"]
        say(f"     {str(g or 'none'):6s}  {fmt(w):18s}{' (gaps)' if gaps(fl) else '       '}  Q {ev['Q']:5.2f}; {ev['med']['H']:+.2f} / {ev['med']['S']:+.2f}; {ev['medp']['H']:+.2f} / {ev['medp']['S']:+.2f} -> {failing(ev)}"
            + ("" if low else "   [no field <= 0.008 passes]"))
        RES["part2"][f"{f}|{g or 'none'}"] = dict(window=w, gaps=gaps(fl), record_ok=ev["ok"], Q=ev["Q"], med=ev["med"], medp=ev["medp"], fails=failing(ev), field_le_0008_passes=low)
    lab2 = "RECORD'S FIELD PASSES WITH HOT GAS" if ans["MB15"] else "RECORD'S FIELD STILL FAILS"
    other = [g for g in MODELS if g != "MB15" and ans[g] != ans["MB15"]]
    if other: lab2 += ", FRAGILE (" + ", ".join(other) + ")"
    RES["part2"][f] = lab2; say(f"     PART 2 LABEL: {lab2}")
sec("LABELS")
for f in A0: say(f"  {f:9s}: {RES['part1'][f]}  /  {RES['part2'][f]}")
json.dump(dict(lane="HG2", date="2026-11-12", conventions=dict(mu_e=MU_E, mu_H=MU_H, S15_mu=S15_MU, S15_slope=S15_A, S15_C=S15_C, F17_slope=F17_S),
               outer_radius=ROUT, results=RES), open(os.path.join(HERE, "hg2_results.json"), "w"), indent=1, default=str)
say("\nHG2 COMPLETE. Literature values are PROVISIONAL look-ups of full texts. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
