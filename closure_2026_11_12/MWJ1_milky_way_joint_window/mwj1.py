#!/usr/bin/env python3
"""
MWJ1 -- is there one (external field e_N, baryon amplitude A) per footing at which the framework's Milky Way
line passes the shape-measuring DESI curves (NMB1), the published masses at r >= 100 kpc (PLT1) and the
plateau rows at r >= 150 kpc, all at once?  Criteria: FROZEN_CRITERIA.md (b1235e89cd).
Usage: python3 mwj1.py     Reads the two lanes' result files; writes mwj1.out, mwj1_results.json, mwj1_mut.out.
A post hoc consolidation: every input has been seen. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
N1 = json.load(open(os.path.join(HERE, "..", "NMB1_nimble_curves_vs_line", "nmb1_results.json")))
P1 = json.load(open(os.path.join(HERE, "..", "PLT1_outer_mass_vs_literature", "plt1_results.json")))
TH = np.array(N1["theta"]); VI = np.linalg.inv(np.array(N1["V"]))
ROWS = {c: P1["rows"][c] for c in ("H", "S")}

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_REC, QGATE, FLOOR = 0.01273, 6.180, 0.20
EG = np.round(np.arange(0.0, 0.03 + 1e-9, 0.0005), 4)
AG = np.round(np.arange(0.70, 1.80 + 1e-9, 0.01), 2)
RC_BOX = {"canonical": dict(A=(1.256, 1.310), e=(0.0, 0.008), e_narrow=0.006), "alt": dict(A=(1.152, 1.208), e=(0.0, 0.015), e_narrow=0.008)}

OUT = open(os.path.join(HERE, "mwj1.out"), "w")
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
def M_line(r, a0, eN, A, kern=nu_fw):
    Mb = A * M_sph(r); gb = G * Mb / (r * KPC) ** 2 / a0
    if eN == 0.0: return float(kern(gb)) * Mb / MSUN / 1e11
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * MU)
    return float(TRAPZ(kern(gm) * (gb + eN * MU), MU) / 2.0) / gb * Mb / MSUN / 1e11

S_FL = math.log10(1.0 + FLOOR)
def pull(Ml, r):
    side = math.log10(r["M"] / (r["M"] - r["lo"])) if Ml < r["M"] else math.log10((r["M"] + r["hi"]) / r["M"])
    return (math.log10(Ml) - math.log10(r["M"])) / math.hypot(side, S_FL)
RADII = sorted({r["r"] for c in ROWS for r in ROWS[c]})
def evaluate(a0, e, A, kern=nu_fw):
    line = {r: M_line(r, a0, e, A, kern) for r in [30.0, 80.0] + RADII}
    d = np.array([math.log10(line[30.0]), math.log10(line[80.0])]) - TH
    Q = float(d @ VI @ d)
    med, medp = {}, {}
    for c, rws in ROWS.items():
        z = [(pull(line[r["r"]], r), r["r"]) for r in rws]
        med[c] = float(np.median([v for v, _ in z])); medp[c] = float(np.median([v for v, rr in z if rr >= 150.0]))
    g1 = Q <= QGATE; g2 = all(abs(v) <= 2 for v in med.values()); g2p = all(abs(v) <= 2 for v in medp.values())
    return dict(Q=Q, med=med, medp=medp, g1=g1, g2=g2, g2p=g2p, ok=g1 and g2 and g2p, line30=line[30.0], line80=line[80.0])
def failing(ev):
    out = []
    if not ev["g1"]: out.append(f"curves (Q {ev['Q']:.1f})")
    if not ev["g2"]: out.append("outer masses (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["med"].items() if abs(v) > 2) + ")")
    if not ev["g2p"]: out.append("plateau rows (" + ", ".join(f"{c} {v:+.2f}" for c, v in ev["medp"].items() if abs(v) > 2) + ")")
    return "; ".join(out) if out else "none"

sec("MWJ1  one reading for the whole Milky Way?   (criteria b1235e89cd; post hoc consolidation)")
sec("KNOWN-ANSWER CHECKS")
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)
ref_q = {("canonical", E_REC): 4.89, ("alt", E_REC): 2.91, ("canonical", 0.0): 2.40, ("alt", 0.0): 0.05}
ref_m = {("canonical", E_REC): (-0.68, -1.56), ("alt", E_REC): (-0.66, -1.54), ("canonical", 0.0): (1.01, 0.28), ("alt", 0.0): (1.34, 0.61)}
EV = {k: evaluate(A0[k[0]], k[1], 1.0) for k in ref_q}
ka("KA1 NMB1's Q reproduced at (0.01273, 1) and (0, 1), each within 0.03",
   all(abs(EV[k]["Q"] - v) <= 0.03 for k, v in ref_q.items()), "; ".join(f"{k[0]} e {k[1]}: {EV[k]['Q']:.2f} vs {v}" for k, v in ref_q.items()))
ka("KA2 PLT1's class medians reproduced at the same points, each within 0.02",
   all(abs(EV[k]["med"]["H"] - v[0]) <= 0.02 and abs(EV[k]["med"]["S"] - v[1]) <= 0.02 for k, v in ref_m.items()),
   "; ".join(f"{k[0]} e {k[1]}: H {EV[k]['med']['H']:+.2f}, S {EV[k]['med']['S']:+.2f}" for k in ref_m))
ref_l = {("canonical", 0.0): 5.691, ("alt", 0.0): 6.219, ("canonical", E_REC): 4.977, ("alt", E_REC): 5.109}
ka("KA3 the line at 80 kpc reproduces the record within 0.5 per cent",
   all(abs(EV[k]["line80"] / v - 1) <= 0.005 for k, v in ref_l.items()), "; ".join(f"{EV[k]['line80']:.3f}" for k in ref_l))
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label."); json.dump({"lane": "MWJ1", "label": "NO LABEL"}, open(os.path.join(HERE, "mwj1_results.json"), "w")); sys.exit(0)

# ---------------------------------------------------------------- the grid
GRID = {f: [[evaluate(a0, float(e), float(A)) for A in AG] for e in EG] for f, a0 in A0.items()}
MUT = open(os.path.join(HERE, "mwj1_mut.out"), "w"); MUT.write("MWJ1 mutations (criteria b1235e89cd). Each must empty the window.\n"); bite = True
for f, a0 in A0.items():
    n1 = sum(evaluate(16 * a0, float(e), float(A))["ok"] for e in EG for A in AG)
    n2 = sum(evaluate(a0, float(e), float(A), nu_newton)["ok"] for e in EG for A in AG)
    MUT.write(f"{f}: M1 a0 x 16 -> points passing {n1};  M2 Newtonian kernel -> points passing {n2}  (full grid)\n")
    bite &= (n1 == 0 and n2 == 0)
MUT.close()
sec("MUTATIONS"); say(f"  written to mwj1_mut.out: {'both empty the window' if bite else 'A MUTATION LEAVES POINTS -> no label'}")
if not bite: sys.exit(0)

def idx(arr, v): return int(np.argmin(np.abs(arr - v)))
def rng(vals, flags):
    ok = [float(v) for v, fl in zip(vals, flags) if fl]
    return None if not ok else (min(ok), max(ok))
def fmt(r, nd): return "empty" if r is None else f"[{r[0]:.{nd}f}, {r[1]:.{nd}f}]"
RES = {}
sec("THE WINDOW  points passing the curves, the outer masses and the plateau rows together")
for f in A0:
    g = GRID[f]; jA1 = idx(AG, 1.0); ie_rec = idx(EG, 0.0125); box = RC_BOX[f]
    n_ok = sum(ev["ok"] for row in g for ev in row)
    e_at_A1 = rng(EG, [g[i][jA1]["ok"] for i in range(len(EG))])
    e_at_A1_no_p = rng(EG, [g[i][jA1]["g1"] and g[i][jA1]["g2"] for i in range(len(EG))])
    rec = evaluate(A0[f], E_REC, 1.0)
    A_at = {e: rng(AG, [g[idx(EG, e)][j]["ok"] for j in range(len(AG))]) for e in (0.0, 0.008)}
    A_at[E_REC] = rng(AG, [evaluate(A0[f], E_REC, float(A))["ok"] for A in AG])
    Arc = 0.5 * (box["A"][0] + box["A"][1]); jrc = idx(AG, Arc)
    e_at_rc = rng(EG, [g[i][jrc]["ok"] for i in range(len(EG))])
    in_box = [(float(EG[i]), float(AG[j])) for i in range(len(EG)) for j in range(len(AG))
              if g[i][j]["ok"] and box["e"][0] <= EG[i] <= box["e"][1] and box["A"][0] - 1e-9 <= AG[j] <= box["A"][1] + 1e-9]
    in_box_narrow = [p for p in in_box if p[0] <= box["e_narrow"]]
    if rec["ok"]: lab = "CLOSES AT THE RECORD'S VALUES"
    elif e_at_A1 is not None: lab = "CLOSES WITH CENSUS BARYONS, WEAKER FIELD"
    elif n_ok > 0: lab = "CLOSES ONLY WITH MORE BARYONS"
    else: lab = "DOES NOT CLOSE"
    lab += ", ROTATION CURVE " + ("INSIDE" if in_box else "OUTSIDE")
    say(f"\n  {f}:  {n_ok} of {len(EG) * len(AG)} grid points pass")
    say(f"     at census baryons (A = 1): field range {fmt(e_at_A1, 4)}   (without the plateau rows: {fmt(e_at_A1_no_p, 4)})")
    say(f"     the record's point (e_N 0.01273, A 1): curves Q {rec['Q']:.2f}; outer medians H {rec['med']['H']:+.2f}, S {rec['med']['S']:+.2f}; "
        f"plateau medians H {rec['medp']['H']:+.2f}, S {rec['medp']['S']:+.2f}  ->  fails: {failing(rec)}")
    say(f"     amplitude range at e_N = 0: {fmt(A_at[0.0], 2)};  at 0.008: {fmt(A_at[0.008], 2)};  at 0.01273: {fmt(A_at[E_REC], 2)}")
    say(f"     at the rotation curve's amplitude (A = {AG[jrc]:.2f}): field range {fmt(e_at_rc, 4)}")
    say(f"     rotation-curve box A {box['A']}, e_N {box['e']}: {len(in_box)} window points inside ({len(in_box_narrow)} with e_N <= {box['e_narrow']})")
    if e_at_A1 is not None:
        i_hi = idx(EG, e_at_A1[1]) + 1
        if i_hi < len(EG): say(f"     past the upper field edge at A = 1 (e_N {EG[i_hi]:.4f}) what fails first: {failing(g[i_hi][jA1])}")
    if A_at[0.0] is not None:
        j0 = idx(AG, A_at[0.0][0]) - 1; j1 = idx(AG, A_at[0.0][1]) + 1
        if j0 >= 0: say(f"     below the lower amplitude edge at e_N = 0 (A {AG[j0]:.2f}): {failing(g[0][j0])}")
        if j1 < len(AG): say(f"     above the upper amplitude edge at e_N = 0 (A {AG[j1]:.2f}): {failing(g[0][j1])}")
    say(f"     LABEL: {lab}")
    RES[f] = dict(label=lab, points_passing=n_ok, e_range_A1=e_at_A1, e_range_A1_without_plateau=e_at_A1_no_p, A_range=A_at,
                  e_range_at_rc_amplitude=e_at_rc, rc_box_points=len(in_box), rc_box_points_narrow=len(in_box_narrow),
                  record_point=dict(Q=rec["Q"], med=rec["med"], medp=rec["medp"], fails=failing(rec)))
sec("LABELS")
for f in A0: say(f"  {f:9s}: {RES[f]['label']}")
json.dump(dict(lane="MWJ1", criteria="b1235e89cd", date="2026-11-12", results=RES), open(os.path.join(HERE, "mwj1_results.json"), "w"), indent=1, default=str)
say("\nMWJ1 COMPLETE. A window is not a derivation. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
