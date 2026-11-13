#!/usr/bin/env python3
"""SRJ3 (FROZEN_CRITERIA.md, 97cf1ef5ca): does the regime-split joint's reference layout (baryons + FRZ1's reference cold
dark energy halo) fit the observed V_c(R_e) of SRJ2's cluster-regime RC100 discs? SRJ2's srj2_rc.py is executed read-only
from its own path up to its "json.dump(RES" line (nothing written there). DD1's class line is inherited.
  nice -n 19 python3 srj3.py -> srj3.json / .out; twins -> srj3_MUTATE_<TWN|TWH|TWL>.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, csv, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SJ = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint"); SRC = os.path.join(SJ, "srj2_rc.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "srj2_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("json.dump(RES")], SRC, "exec"), NS)
RES2, FR, S, vgal, zstate, VST, FOOTS = (NS[k] for k in ("RES", "FR", "S", "vgal", "zstate", "VST", "FOOTS"))
XTAB, FB, hh, G, MS, KPC, A0, glaw, CR_srh = (S[k] for k in ("XTAB", "FB", "hh", "G", "MS", "KPC", "A0", "glaw", "CR"))
MPC = 1e3 * KPC; m_nfw = FR["m_nfw"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P("SRJ3 reference layout on cluster-regime discs (criteria 97cf1ef5ca). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))))
D = {r["name"]: r for r in rows}
E = math.hypot(0.087, 0.20)

_H = {}
def halo(X, Mb_sun, z):
    """FRZ1's halo with M_ta = X M_b h / (1 - FB) at z; returns physical r_s, r_ta (m) and c_ta."""
    key = (X, round(math.log10(Mb_sun), 8), round(z, 6))
    if key not in _H:
        conc, dta, omz = zstate(z); Mta = X * Mb_sun * hh / (1 - FB); hbz = FR["halo_basics_z"]
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); a = MPC / hh / (1 + z)
        _H[key] = (hb["rs"] * a, hb["rta"] * a, hb["rta"] / hb["rs"], hb)
    return _H[key]
def CRz(r, Mb_sun, X, z):
    rs, rta, cta, _ = halo(X, Mb_sun, z); r = min(r, rta)
    return X * Mb_sun * MS * m_nfw(r / rs) / m_nfw(cta)

def Xof(ft, z, mode): return XTAB[ft]["z0.0"] if (mode == "z0" or (mode == "rule" and z < 1)) else XTAB[ft]["z1.0"]
def gals(ft, mode="rule", twin=None):
    o = []
    for c in RES2["foot"][ft]["G2"]["cluster"]:
        r = D[c["name"]]; z, Mb, Re = float(r["z"]), 10 ** float(r["logMbar_Msun"]), float(r["Re_kpc"]) * KPC
        X = Xof(ft, z, mode) * (0.5 if twin == "TWH" else 1.0)
        gb = G * Mb / 2 * MS / Re ** 2; Cr = CRz(Re, Mb, X, z); gm = gb + G * Cr / Re ** 2
        if twin == "TWN": gm = gb
        if twin == "TWL": gm = float(glaw(gb, A0[ft]))
        go = (float(r["Vc_Re_kms"]) * 1e3) ** 2 / Re; Y, F = math.log10(go / gb), math.log10(gm / gb)
        o.append(dict(name=c["name"], z=z, logMb=float(r["logMbar_Msun"]), Re_kpc=float(r["Re_kpc"]), Vc=float(r["Vc_Re_kms"]), X=X, Y=Y, F=F, d=Y - F,
                      fcold=Cr / (Cr + Mb / 2 * MS), fDM_author=float(r["fDM_within_Re"])))
    return o
def cls(o):
    d = np.array([g["d"] for g in o]); n = len(d); off = float(np.median(d)); mad = float(np.median(abs(d - np.median(d))))
    se = max(1.2533 * 1.4826 * mad / math.sqrt(n), math.sqrt(n * E ** 2) / n) if n >= 2 else E
    return dict(n=n, off=off, se=se, line=bool(abs(off) <= 0.10 and abs(off) <= 3 * se), n_within_e=int((abs(d) <= E).sum()))
def word(c): return "NO VERDICT (no power)" if c["n"] < 5 else ("REFERENCE FITS" if c["line"] else "REFERENCE FAILS")
def halves(o, key):
    v = np.array([g[key] for g in o]); m = np.median(v)
    return {f"{key}<={m:.2f}": float(np.median([g["d"] for g in o if g[key] <= m])), f"{key}>{m:.2f}": float(np.median([g["d"] for g in o if g[key] > m]))}

RES = dict(lane="SRJ3", criteria="97cf1ef5ca", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
TW = {t: dict(lane="SRJ3", twin=t, foot={}) for t in ("TWN", "TWH", "TWL")}
for ft in FOOTS:
    R = RES["foot"][ft] = {}; g2 = RES2["foot"][ft]["G2"]
    # K1
    ref = json.load(open(os.path.join(SJ, "srj2_rc.json")))["foot"][ft]["G2"]
    k1 = (g2["n_cluster"] == {"canonical": 31, "alt": 22}[ft] and all(g2[f"f{f:.2f}"]["covered"] == {"canonical": 69, "alt": 78}[ft] for f in (0.75, 1.0, 1.25))
          and [c["name"] for c in g2["cluster"]] == [c["name"] for c in ref["cluster"]])
    R["K1"] = dict(n_cluster=g2["n_cluster"], covered={f"f{f:.2f}": g2[f"f{f:.2f}"]["covered"] for f in (0.75, 1.0, 1.25)}, pass_=bool(k1))
    # K2
    bref = RES2["foot"][ft]["G3b"]["f1.00"]["reported_reference"]; tgt = {"canonical": (0.0640, 0.0387), "alt": (0.0559, 0.0332)}[ft]
    R["K2"] = dict(rms=bref["all"]["rms"], massive=bref["massive"]["rms"], n_cluster_PD1=bref["n_cluster"], names=bref["cluster_names"],
                   n_cluster_FLD1=RES2["foot"][ft]["G3a"]["n_cluster"], pass_=bool(abs(bref["all"]["rms"] - tgt[0]) <= 1e-4 and abs(bref["massive"]["rms"] - tgt[1]) <= 1e-4))
    o = gals(ft)
    R["K3"] = dict(rows=len(rows), pass_=bool(len(rows) == 100 and all(math.isfinite(g["Vc"]) and g["Re_kpc"] > 0 for g in o)))
    X0 = XTAB[ft]["z0.0"]; Mt = 10 ** 11.2; rt = 5 * KPC
    k4 = abs(CRz(rt, Mt, X0, 0.0) / float(CR_srh(np.array([rt]), Mt, X0)[0]) - 1); R["K4"] = dict(rel=k4, pass_=bool(k4 <= 1e-10))
    # K5: SI, second route, median-d galaxy
    gm = sorted(o, key=lambda g: g["d"])[len(o) // 2]; z = gm["z"]; Mb = 10 ** gm["logMb"]; Re = gm["Re_kpc"] * 3.0857e19
    rs_, rta_, cta_, hb = halo(gm["X"], Mb, z); GSI, MSUN, MPCSI = 6.674e-11, 1.989e30, 3.0857e22
    H = 100e3 * hh / MPCSI * math.sqrt(FR["Om"] * (1 + z) ** 3 + 1 - FR["Om"]); rhoc = 3 * H ** 2 / (8 * math.pi * GSI)
    r200c_si = (3 * hb["M200c"] / hh * MSUN / (4 * math.pi * 200 * rhoc)) ** (1 / 3); r200c_fr = hb["r200c"] / hh / (1 + z) * MPCSI
    rhom = FR["Om"] * 3 * (100e3 * hh / MPCSI) ** 2 / (8 * math.pi * GSI) * (1 + z) ** 3
    rs_si = (3 * hb["M"] / hh * MSUN / (4 * math.pi * 200 * rhom)) ** (1 / 3) / hb["c"]
    mn = lambda x: math.log(1 + x) - x / (1 + x)
    g_si = GSI * (Mb / 2 * MSUN + gm["X"] * Mb * MSUN * mn(Re / rs_si) / mn(cta_)) / Re ** 2; g_sc = 10 ** gm["F"] * G * Mb / 2 * MS / (gm["Re_kpc"] * KPC) ** 2
    R["K5"] = dict(name=gm["name"], r200c_SI_kpc=r200c_si / 3.0857e19, r200c_FRZ1_kpc=r200c_fr / 3.0857e19, rs_SI_kpc=rs_si / 3.0857e19, rs_FRZ1_kpc=rs_ / KPC,
                   g_SI=g_si, g_script=g_sc, pass_=bool(abs(r200c_si / r200c_fr - 1) <= 0.01 and abs(g_si / g_sc - 1) <= 0.01))
    # grade + bracket + shape
    c = cls(o); R["main"] = dict(cls=c, word=word(c), galaxies=o, halves_z=halves(o, "z"), halves_M=halves(o, "logMb"),
                                 median_fcold=float(np.median([g["fcold"] for g in o])), median_fDM_author=float(np.median([g["fDM_author"] for g in o])))
    R["bracket"] = {m: (lambda cc: dict(cls=cc, word=word(cc)))(cls(gals(ft, m))) for m in ("z0", "z1")}
    R["fragile"] = bool(len({R["main"]["word"]} | {R["bracket"][m]["word"] for m in R["bracket"]}) > 1)
    # context: galaxy-regime discs under the law
    cn = {cc["name"] for cc in g2["cluster"]}; dl = []
    for r in rows:
        if r["name"] in cn: continue
        Mb = 10 ** float(r["logMbar_Msun"]); Re = float(r["Re_kpc"]) * KPC; gb = G * Mb / 2 * MS / Re ** 2
        dl.append(dict(d=math.log10((float(r["Vc_Re_kms"]) * 1e3) ** 2 / Re / gb) - math.log10(float(glaw(gb, A0[ft])) / gb)))
    R["context_galaxy_regime_law"] = cls(dl)
    for t in TW:
        ct = cls(gals(ft, twin=t)); TW[t]["foot"][ft] = dict(cls=ct, word=word(ct), d_off=ct["off"] - c["off"], bites=bool(abs(ct["off"] - c["off"]) >= 0.05 or word(ct) != word(c)))
    chk = all(R[k]["pass_"] for k in ("K1", "K2", "K3", "K4", "K5")); req = all(TW[t]["foot"][ft]["bites"] for t in ("TWN", "TWH"))
    R["final_word"] = R["main"]["word"] if (chk and req) else "NO VERDICT"
    P(f"[{ft}] K1 cluster-regime {g2['n_cluster']}, covered {R['K1']['covered']} -> {'PASS' if R['K1']['pass_'] else 'FAIL'}; K2 SPARC reference rms {bref['all']['rms']:.4f} massive {bref['massive']['rms']:.4f} "
      f"(PD1 cluster-regime {bref['n_cluster']}: {bref['cluster_names']}; FLD1 {R['K2']['n_cluster_FLD1']}) -> {'PASS' if R['K2']['pass_'] else 'FAIL'}; K3 {'PASS' if R['K3']['pass_'] else 'FAIL'}; K4 {k4:.1e} -> {'PASS' if R['K4']['pass_'] else 'FAIL'}")
    P(f"[{ft}] K5 SI ({gm['name']}, z {z:.2f}): r200c {R['K5']['r200c_SI_kpc']:.2f} vs {R['K5']['r200c_FRZ1_kpc']:.2f} kpc; r_s {R['K5']['rs_SI_kpc']:.2f} vs {R['K5']['rs_FRZ1_kpc']:.2f} kpc; "
      f"g_mod {g_si:.4e} vs {g_sc:.4e} m/s^2 -> {'PASS' if R['K5']['pass_'] else 'FAIL'}")
    for g in o: P(f"[{ft}]   {g['name']:16s} z {g['z']:.2f} logMb {g['logMb']:.2f} Re {g['Re_kpc']:5.2f} Vc {g['Vc']:4.0f} X {g['X']:.2f}  Y {g['Y']:+.3f} F {g['F']:+.3f} d {g['d']:+.3f}  f_cold {g['fcold']:.2f} fDM(author) {g['fDM_author']:.2f}")
    P(f"[{ft}] MAIN n {c['n']}: off {c['off']:+.4f} dex, se {c['se']:.4f} (3 se {3*c['se']:.4f}); line |off| <= 0.10 and <= 3 se -> {R['main']['word']}; |d| <= {E:.3f}: {c['n_within_e']} / {c['n']}")
    P(f"[{ft}]   shape: z halves {R['main']['halves_z']}; M_b halves {R['main']['halves_M']}; median f_cold {R['main']['median_fcold']:.3f} vs author f_DM {R['main']['median_fDM_author']:.3f}")
    P(f"[{ft}]   X bracket: " + "; ".join(f"{m} X {XTAB[ft][m + '.0']:.2f} off {R['bracket'][m]['cls']['off']:+.4f} -> {R['bracket'][m]['word']}" for m in R["bracket"]) + f"; FRAGILE {R['fragile']}")
    P(f"[{ft}]   context, galaxy-regime discs under the law: n {R['context_galaxy_regime_law']['n']} off {R['context_galaxy_regime_law']['off']:+.4f} line {R['context_galaxy_regime_law']['line']}")
    P(f"[{ft}]   twins: " + "; ".join(f"{t} off {TW[t]['foot'][ft]['cls']['off']:+.4f} (d {TW[t]['foot'][ft]['d_off']:+.4f}) {TW[t]['foot'][ft]['word']} bites {TW[t]['foot'][ft]['bites']}" for t in TW))
    P(f"[{ft}] WORD: {R['final_word']}")
P("SRJ3: " + " / ".join(RES["foot"][f]["final_word"] for f in FOOTS) + " (canonical / alt)")
json.dump(RES, open(os.path.join(HERE, "srj3.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srj3.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
for t in TW:
    json.dump(TW[t], open(os.path.join(HERE, f"srj3_MUTATE_{t}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"srj3_MUTATE_{t}.out"), "w").write("\n".join(f"[{f}] {t}: off {TW[t]['foot'][f]['cls']['off']:+.4f} {TW[t]['foot'][f]['word']} bites {TW[t]['foot'][f]['bites']}" for f in FOOTS) + "\n")
