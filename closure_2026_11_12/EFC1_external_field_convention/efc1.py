#!/usr/bin/env python3
"""
EFC1 -- which number is the Milky Way's external field, and what each reading does.
Criteria: FROZEN_CRITERIA.md (5aa1a8ad15).  Usage: python3 efc1.py
Reads NMB1's and PLT1's result files; writes efc1.out, efc1_results.json, efc1_mut.out.
Decides nothing about which reading is right. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
N1 = json.load(open(os.path.join(HERE, "..", "NMB1_nimble_curves_vs_line", "nmb1_results.json")))
P1 = json.load(open(os.path.join(HERE, "..", "PLT1_outer_mass_vs_literature", "plt1_results.json")))
TH = np.array(N1["theta"]); VI = np.linalg.inv(np.array(N1["V"]))
ROWS = {c: P1["rows"][c] for c in ("H", "S")}

# hot-gas models: enclosed mass M_ref (r / r_ref)^p  [Msun, kpc]
GAS = {"MB15": (4.3e10, 250.0, 1.5), "S15": (2.6e10, 300.0, 1.5), "F20": (5.5e10, 280.0, 1.5), "F17": (1.2e11, 250.0, 2.0)}
def m_hot(gas, r):
    if gas is None: return 0.0
    M, r0, p = GAS[gas]; return M * (r / r0) ** p
M_CENSUS = 6.681e10
NEED = {"canonical": ((1.256 - 1) * M_CENSUS, (1.310 - 1) * M_CENSUS), "alt": ((1.152 - 1) * M_CENSUS, (1.208 - 1) * M_CENSUS)}
R_RC = 27.0

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_REC, QGATE, FLOOR = 0.01273, 6.180, 0.20
EG = np.round(np.arange(0.0, 0.03 + 1e-9, 0.0005), 4)
AG = np.round(np.arange(0.70, 1.80 + 1e-9, 0.01), 2)
RC_BOX = {"canonical": dict(A=(1.256, 1.310), e=(0.0, 0.008), e_narrow=0.006), "alt": dict(A=(1.152, 1.208), e=(0.0, 0.015), e_narrow=0.008)}

OUT = open(os.path.join(HERE, "efc1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 108); say(t); say("=" * 108)

# ---------------------------------------------------------------- McMillan 2017 baryons (as dw1.py / plt1.py)
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
def nu_newton(y): return np.ones_like(np.asarray(y, float))
MU = np.linspace(-1.0, 1.0, 4001)
def M_line(r, a0, eN, A, kern=nu_fw, gas=None, gscale=1.0):
    Mb = A * M_sph(r) + gscale * m_hot(gas, r) * MSUN; gb = G * Mb / (r * KPC) ** 2 / a0
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
    return dict(Q=Q, med=med, medp=medp, g1=g1, g2=g2, g2p=g2p, ok=g1 and g2 and g2p, line80=line[80.0], line200=line.get(200.0))
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
    return dict(Q=Q, med=med, medp=medp, g1=g1, g2=g2, g2p=g2p, ok=g1 and g2 and g2p, line80=line[80.0], line200=line.get(200.0))
def failing(ev):
    out = []
    if not ev["g1"]: out.append(f"curves (Q {ev['Q']:.1f})")
    if not ev["g2"]: out.append("outer masses (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["med"].items() if abs(v) > 2) + ")")
    if not ev["g2p"]: out.append("plateau rows (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["medp"].items() if abs(v) > 2) + ")")
    return "; ".join(out) if out else "none"

# ---------------------------------------------------------------- item 81's three terms
G_LSS, L_LSS, B_LSS = 1.161e-12, 267.5, 40.3
M31 = (1.3e11, 770.0, 121.17, -21.57); LMC = (3.0e9, 49.9, 280.47, -32.89)
H_LIB = 0.6736; OM_B, OM_M_H81 = 0.049, (0.02237 + 0.1200) / H_LIB ** 2      # hunt_lib's Omega_m; 0.049 as frozen (hunt_lib's own Omega_b is 0.0493)
def unit(l, b):
    l, b = math.radians(l), math.radians(b); return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])
def gN(M, d): return G * M * MSUN / (d * KPC) ** 2
V_LSS = G_LSS * unit(L_LSS, B_LSS); V_M31 = gN(M31[0], M31[1]) * unit(M31[2], M31[3]); V_LMC = gN(LMC[0], LMC[1]) * unit(LMC[2], LMC[3])
TOT = V_LSS + V_M31 + V_LMC; G_TOT = float(np.linalg.norm(TOT))
L_TOT = math.degrees(math.atan2(TOT[1], TOT[0])) % 360.0; B_TOT = math.degrees(math.asin(TOT[2] / G_TOT))
G_BAR = float(np.linalg.norm(V_LSS * OM_B / OM_M_H81 + V_M31 + V_LMC))

def nu1(y): return float(nu_fw(y))
def dnu(y): s = math.sqrt(y); ex = math.exp(-s); n = 1 / (1 - ex); return -n * n * ex / (2 * s)
def invert(x, kern=nu1):
    """Newtonian-equivalent e with kern(e) e = x (x = actual field in a0 units)."""
    lo, hi = 1e-12, max(x, 1e-12)
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if kern(mid) * mid < x: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

sec("EFC1  which number is the Milky Way's external field?   (criteria 5aa1a8ad15)")
sec("KNOWN-ANSWER CHECKS")
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)
ka("KA1 item 81's vector sum (1.191e-12 within 1 per cent; direction within 1 degree of (268.5, +33.0))",
   abs(G_TOT / 1.191e-12 - 1) <= 0.01 and abs(L_TOT - 268.5) <= 1.0 and abs(B_TOT - 33.0) <= 1.0,
   f"|sum| = {G_TOT:.4e} m/s^2 toward ({L_TOT:.1f}, {B_TOT:+.1f}); M31 {np.linalg.norm(V_M31):.3e}, LMC {np.linalg.norm(V_LMC):.3e}")
e0 = evaluate(A0["canonical"], E_REC)
ka("KA2 at e_N = 0.01273, census, canonical: Q 4.89 and satellite-class plateau median -2.72 (MWJ1)",
   abs(e0["Q"] - 4.89) <= 0.03 and abs(e0["medp"]["S"] + 2.72) <= 0.02, f"Q {e0['Q']:.2f}, plateau S {e0['medp']['S']:+.2f}")
rt = max(abs(nu1(invert(x)) * invert(x) / x - 1) for x in (0.01, 0.0127, 0.03))
ka("KA3 the inversion nu(e) e = x round trip to 1e-10", rt <= 1e-10, f"worst {rt:.1e}")
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label."); json.dump({"lane": "EFC1", "label": "NO LABEL"}, open(os.path.join(HERE, "efc1_results.json"), "w")); sys.exit(0)

MUT = open(os.path.join(HERE, "efc1_mut.out"), "w")
okm = True
for f, a0 in A0.items():
    eA1 = invert(G_TOT / a0, kern=lambda y: 1.0); b = abs(eA1 / (G_TOT / a0) - 1) < 1e-9; okm &= b
    MUT.write(f"{f}: M1 reading A with the kernel set to 1 gives e_N = {eA1:.5f} against reading R's {G_TOT/a0:.5f} [{'equal' if b else 'NOT EQUAL'}]\n")
MUT.close()
sec("MUTATION"); say(f"  written to efc1_mut.out: {'readings R and A differ by exactly the kernel factor' if okm else 'FAILED'}")
if not okm: sys.exit(0)

MB_KG = 6.6814e10 * MSUN                                   # the census total (MWI1 KA1)
def describe(e, a0):
    act = nu1(e) * e if e > 0 else 0.0
    r_take = math.sqrt(G * MB_KG / (e * a0)) / KPC if e > 0 else float("inf")
    sat = (nu1(e) + e * dnu(e) / 3.0) * MB_KG / MSUN / 1e11 if e > 0 else float("inf")
    return act, r_take, sat
RES = {}
sec("THE READINGS")
say(f"  item 81's total: {G_TOT:.4e} m/s^2;  baryons-only source total (large-scale term x {OM_B}/{OM_M_H81}): {G_BAR:.4e} m/s^2")
for f, a0 in A0.items():
    x = G_TOT / a0
    readings = [("R  record's (Newtonian source)", x), ("R' record's, as the lanes used it", E_REC),
                ("A  the same acceleration as the actual field", invert(x)),
                ("L  literature actual 0.01 a0", invert(0.01)), ("L  literature actual 0.02 a0", invert(0.02)), ("L  literature actual 0.03 a0", invert(0.03)),
                ("B  baryons-only source", G_BAR / a0)]
    say(f"\n  {f} (a0 = {a0:.3e}):")
    say("     reading                                       e_N       actual field [a0]  [m/s^2]    takeover r [kpc]  saturation [1e11]   line 80 / 200 / 273 kpc      census            with hot gas")
    RES[f] = {}
    for name, e in readings:
        act, rt_, sat = describe(e, a0)
        ev = evaluate(a0, e); evg = evaluate(a0, e, "MB15")
        l273 = M_line(273.0, a0, e, 1.0)
        say(f"     {name:44s} {e:9.6f}   {act:8.4f}     {act*a0:9.3e}   {rt_:10.0f}       {sat:9.2f}        {ev['line80']:5.2f} / {ev['line200']:5.2f} / {l273:5.2f}       "
            f"{'PASSES' if ev['ok'] else 'FAILS ' + failing(ev):30s}  {'PASSES' if evg['ok'] else 'FAILS ' + failing(evg)}")
        RES[f][name] = dict(e_N=e, actual_a0=act, takeover_kpc=rt_, saturation_1e11=sat, census_ok=ev["ok"], census_fails=failing(ev), gas_ok=evg["ok"], gas_fails=failing(evg),
                            line=(ev["line80"], ev["line200"], l273))
    r_, a_ = RES[f]["R  record's (Newtonian source)"], RES[f]["A  the same acceleration as the actual field"]
    dep = (r_["census_ok"] != a_["census_ok"]) or (r_["census_fails"] != a_["census_fails"])
    RES[f]["label"] = "CONVENTION-DEPENDENT" if dep else "CONVENTION-INDEPENDENT"
    inside = [n for n, d in RES[f].items() if isinstance(d, dict) and d["takeover_kpc"] < 300.0]
    RES[f]["takeover_inside_300"] = inside
    say(f"     the record's reading implies an actual external acceleration {r_['actual_a0']*a0/G_TOT:.1f} times the acceleration it was derived from")
    say(f"     takeover radius inside 300 kpc under: {', '.join(n.strip() for n in inside) if inside else 'none'}")
    say(f"     LABEL: {RES[f]['label']}")
sec("LABELS")
for f in A0: say(f"  {f:9s}: {RES[f]['label']}")
json.dump(dict(lane="EFC1", criteria="5aa1a8ad15", date="2026-11-12", g_tot=G_TOT, g_baryons_only=G_BAR, results=RES), open(os.path.join(HERE, "efc1_results.json"), "w"), indent=1, default=str)
say("\nEFC1 COMPLETE. Decides nothing about which reading is right. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
