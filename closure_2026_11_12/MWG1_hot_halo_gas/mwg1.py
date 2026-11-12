#!/usr/bin/env python3
"""
MWG1 -- can hot halo gas supply the Milky Way's missing baryons?  Criteria: FROZEN_CRITERIA.md (9884ea05fd).
Part 1: hot gas inside 27 kpc against what the rotation curve asks for. Part 2: MWJ1's three gates with the
census at A = 1 and published hot gas added where it is published to be, per external field.
Usage: python3 mwg1.py     Reads NMB1's and PLT1's result files; writes mwg1.out, mwg1_results.json, mwg1_mut.out.
Literature values are from look-ups of abstracts and are PROVISIONAL. kappa = 1/2 FITTED; not theory closed.
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

OUT = open(os.path.join(HERE, "mwg1.out"), "w")
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

sec("MWG1  can hot halo gas supply the Milky Way's missing baryons?   (criteria 9884ea05fd)")
sec("KNOWN-ANSWER CHECKS")
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)
r0 = {f: evaluate(a0, E_REC) for f, a0 in A0.items()}; w0 = {f: window(a0, None)[0] for f, a0 in A0.items()}
ka("KA1 with no gas the script reproduces MWJ1 (Q 4.89 / 2.91; satellite plateau median -2.72; window 0 to 0.0075)",
   abs(r0["canonical"]["Q"] - 4.89) <= 0.03 and abs(r0["alt"]["Q"] - 2.91) <= 0.03 and all(abs(r0[f]["medp"]["S"] + 2.72) <= 0.02 for f in A0)
   and all(w0[f] == (0.0, 0.0075) for f in A0),
   "; ".join(f"{f}: Q {r0[f]['Q']:.2f}, S plateau {r0[f]['medp']['S']:+.2f}, window {fmt(w0[f])}" for f in A0))
ka("KA2 MB15's profile gives 3.8e9 inside 50 kpc within 3 per cent", abs(m_hot("MB15", 50.0) / 3.8e9 - 1) <= 0.03, f"{m_hot('MB15', 50.0):.3e}")
l80 = [evaluate(A0["canonical"], 0.0)["line80"], evaluate(A0["alt"], 0.0)["line80"], r0["canonical"]["line80"], r0["alt"]["line80"]]
ka("KA3 the line at 80 kpc with no gas reproduces the record within 0.5 per cent",
   all(abs(a / b - 1) <= 0.005 for a, b in zip(l80, (5.691, 6.219, 4.977, 5.109))), "; ".join(f"{v:.3f}" for v in l80))
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label."); json.dump({"lane": "MWG1", "label": "NO LABEL"}, open(os.path.join(HERE, "mwg1_results.json"), "w")); sys.exit(0)

MUT = open(os.path.join(HERE, "mwg1_mut.out"), "w"); MUT.write("MWG1 mutation (criteria 9884ea05fd). Must bite.\n"); bite = True
for f, a0 in A0.items():
    ev = evaluate(a0, 0.0, "MB15", 10.0); b = not ev["ok"]; bite &= b
    MUT.write(f"{f}: M1 ten times the MB15 gas at (e_N = 0, census): fails {failing(ev)} [{'bites' if b else 'DOES NOT BITE'}]\n")
MUT.close()
sec("MUTATION"); say(f"  written to mwg1_mut.out: {'bites on both footings' if bite else 'DOES NOT BITE -> no label'}")
if not bite: sys.exit(0)

RES = {"part1": {}, "part2": {}}
sec("PART 1  the rotation curve: hot gas inside 27 kpc against the extra baryons it asks for")
say("  hot gas enclosed [1e10 Msun]:   model    <27 kpc   <30     <80     <100    <150    <200    <273")
for g in GAS:
    say(f"                                  {g:5s}   " + "  ".join(f"{m_hot(g, r)/1e10:6.2f}" for r in (27.0, 30.0, 80.0, 100.0, 150.0, 200.0, 273.0)))
for f in A0:
    lo, hi = NEED[f]; k = 0; parts = []
    for g in GAS:
        s = m_hot(g, R_RC); k += s >= lo; parts.append(f"{g} {s/1e10:.2f} ({100*s/lo:.0f} to {100*s/hi:.0f} per cent)")
        RES["part1"][f"{f}|{g}"] = dict(supplied=s, need_lo=lo, need_hi=hi, frac_of_lo=s / lo)
    lab1 = "ROTATION CURVE NOT SUPPLIED" if k == 0 else f"SUPPLIED IN {k} OF 4"
    RES["part1"][f] = lab1
    say(f"\n  {f}: need {lo/1e10:.2f} to {hi/1e10:.2f} e10 Msun;  supplied inside 27 kpc (share of the need): " + "; ".join(parts))
    say(f"     PART 1 LABEL: {lab1}")

sec("PART 2  the outer data with the census at A = 1 and hot gas added where it is published to be")
for f, a0 in A0.items():
    say(f"\n  {f}:")
    say("     model   field window passing all three gates   at the record's field 0.01273: curves Q, outer medians H / S, plateau medians H / S -> fails")
    ans = {}
    for g in [None] + list(GAS):
        w, fl = window(a0, g); ev = evaluate(a0, E_REC, g)
        low = any(fl[i] for i in range(len(EG)) if EG[i] <= 0.008)
        ans[g] = ev["ok"]
        say(f"     {str(g or 'none'):6s}  {fmt(w):22s}                 Q {ev['Q']:5.2f};  {ev['med']['H']:+.2f} / {ev['med']['S']:+.2f};  {ev['medp']['H']:+.2f} / {ev['medp']['S']:+.2f}  ->  {failing(ev)}"
            + ("" if low else "   [no field at or below 0.008 passes]"))
        RES["part2"][f"{f}|{g or 'none'}"] = dict(window=w, record_ok=ev["ok"], Q=ev["Q"], med=ev["med"], medp=ev["medp"], fails=failing(ev), field_le_0008_passes=low)
    lab2 = "RECORD'S FIELD PASSES WITH HOT GAS" if ans["MB15"] else "RECORD'S FIELD STILL FAILS"
    if any(ans[g] != ans["MB15"] for g in ("S15", "F20", "F17")): lab2 += ", FRAGILE"
    RES["part2"][f] = lab2
    say(f"     PART 2 LABEL: {lab2}")
sec("LABELS")
for f in A0: say(f"  {f:9s}: {RES['part1'][f]}  /  {RES['part2'][f]}")
json.dump(dict(lane="MWG1", criteria="9884ea05fd", date="2026-11-12", gas_models=GAS, results=RES), open(os.path.join(HERE, "mwg1_results.json"), "w"), indent=1, default=str)
say("\nMWG1 COMPLETE. Published gas masses are PROVISIONAL look-ups. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
