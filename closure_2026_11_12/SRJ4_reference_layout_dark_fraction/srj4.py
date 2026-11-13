#!/usr/bin/env python3
"""SRJ4 (FROZEN_CRITERIA.md, 9d5d0c31bb): reference-layout cold fraction inside R_e, f_cold = C / (C + M_b / 2), against
the RC100 authors' dark fraction on SRJ2's cluster-regime discs. SRJ2's srj2_rc.py is executed read-only from its own
path up to its "json.dump(RES" line (nothing written there).
  nice -n 19 python3 srj4.py -> srj4.json / .out; twins -> srj4_MUTATE_<TWH|TWD|TWN>.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, csv, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SJ = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint"); SRC = os.path.join(SJ, "srj2_rc.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "srj2_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("json.dump(RES")], SRC, "exec"), NS)
RES2, FR, S, zstate, FOOTS = (NS[k] for k in ("RES", "FR", "S", "zstate", "FOOTS"))
XTAB, FB, hh, G, MS, KPC = (S[k] for k in ("XTAB", "FB", "hh", "G", "MS", "KPC"))
MPC = 1e3 * KPC; m_nfw = FR["m_nfw"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P("SRJ4 reference-layout cold fraction vs authors' dark fraction (criteria 9d5d0c31bb). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
rows = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")))}
E0 = 0.12

_H = {}
def halo(X, Mb, z):
    key = (X, round(math.log10(Mb), 8), round(z, 6))
    if key not in _H:
        conc, dta, omz = zstate(z); Mta = X * Mb * hh / (1 - FB); hbz = FR["halo_basics_z"]
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); a = MPC / hh / (1 + z)
        _H[key] = (hb["rs"] * a, hb["rta"] * a, hb["rta"] / hb["rs"], hb, dta)
    return _H[key]
def Cold(r, Mb, X, z):   # cold mass (kg) inside physical r (m)
    rs, rta, cta, _, _ = halo(X, Mb, z); return X * Mb * MS * m_nfw(min(r, rta) / rs) / m_nfw(cta)
def Mbar_eff(Mb, Re, mode):   # baryon mass (kg) giving V_bar^2 = G M_eff / R_e
    if mode == "sph": return Mb / 2 * MS
    Rd = Re / 1.678; y = Re / (2 * Rd)
    return 2 * Mb * MS * (Re / Rd) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
def Xof(ft, z, mode): return XTAB[ft]["z0.0"] if (mode == "z0" or (mode == "rule" and z < 1)) else XTAB[ft]["z1.0"]
def gals(ft, xmode="rule", bar="sph", twin=None):
    o = []
    for c in RES2["foot"][ft]["G2"]["cluster"]:
        r = rows[c["name"]]; z, Mb, Re = float(r["z"]), 10 ** float(r["logMbar_Msun"]), float(r["Re_kpc"]) * KPC
        X = Xof(ft, z, xmode) * {"TWH": 0.5, "TWD": 2.0}.get(twin, 1.0)
        C = 0.0 if twin == "TWN" else Cold(Re, Mb, X, z); B = Mbar_eff(Mb, Re, bar); fc = C / (C + B); fa = float(r["fDM_within_Re"])
        o.append(dict(name=c["name"], z=z, logMb=float(r["logMbar_Msun"]), Re_kpc=float(r["Re_kpc"]), X=X, fcold=fc, fDM_author=fa, D=fc - fa))
    return o
def cls(o, e=E0):
    d = np.array([g["D"] for g in o]); n = len(d); off = float(np.median(d)); mad = float(np.median(abs(d - off)))
    se = max(1.2533 * 1.4826 * mad / math.sqrt(n), e / math.sqrt(n))
    return dict(n=n, off=off, se=se, line=bool(abs(off) <= 0.10 and abs(off) <= 3 * se), n_within_e=int((abs(d) <= e).sum()),
                med_fcold=float(np.median([g["fcold"] for g in o])), med_fDM=float(np.median([g["fDM_author"] for g in o])))
def word(c):
    if c["n"] < 5: return "NO VERDICT (no power)"
    return "REFERENCE FITS THE DECOMPOSITIONS" if c["line"] else ("REFERENCE TOO HEAVY" if c["off"] > 0 else "REFERENCE TOO LIGHT")

RES = dict(lane="SRJ4", criteria="9d5d0c31bb", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
TW = {t: dict(lane="SRJ4", twin=t, foot={}) for t in ("TWH", "TWD", "TWN")}
for ft in FOOTS:
    R = RES["foot"][ft] = {}; g2 = RES2["foot"][ft]["G2"]
    ref = json.load(open(os.path.join(SJ, "srj2_rc.json")))["foot"][ft]["G2"]
    ok1 = (g2["n_cluster"] == {"canonical": 31, "alt": 22}[ft] and all(g2[f"f{f:.2f}"]["covered"] == {"canonical": 69, "alt": 78}[ft] for f in (0.75, 1.0, 1.25))
          and [c["name"] for c in g2["cluster"]] == [c["name"] for c in ref["cluster"]])
    R["K1"] = dict(n_cluster=g2["n_cluster"], covered={f"f{f:.2f}": g2[f"f{f:.2f}"]["covered"] for f in (0.75, 1.0, 1.25)}, pass_=bool(ok1))
    P(f"[{ft}] K1 cluster-regime {g2['n_cluster']}, covered {R['K1']['covered']}, names match srj2_rc.json -> {'PASS' if ok1 else 'FAIL'}")
    if not ok1: R["final_word"] = "STOP (K1)"; continue
    o = gals(ft)
    # K2: SI second route, median-z disc
    gm = sorted(o, key=lambda g: g["z"])[len(o) // 2]; z = gm["z"]; Mb = 10 ** gm["logMb"]
    rs_, rta_, cta_, hb, dta = halo(gm["X"], Mb, z)
    GSI, MSUN, MPCSI, KPCSI = 6.674e-11, 1.989e30, 3.0857e22, 3.0857e19
    rhom = FR["Om"] * 3 * (100e3 * hh / MPCSI) ** 2 / (8 * math.pi * GSI) * (1 + z) ** 3
    r200 = (3 * hb["M"] / hh * MSUN / (4 * math.pi * 200 * rhom)) ** (1 / 3); rs = r200 / hb["c"]
    mn = lambda x: math.log(1 + x) - x / (1 + x); c = hb["c"]
    lo, hi = 1.0, 80.0
    for _ in range(200):
        mid = 0.5 * (lo + hi); fmid = mn(c * mid) / mn(c) / mid ** 3 - dta / 200.0
        lo, hi = (mid, hi) if fmid > 0 else (lo, mid)
    rta = 0.5 * (lo + hi) * r200; Re = gm["Re_kpc"] * KPCSI
    Csi = gm["X"] * Mb * MSUN * mn(Re / rs) / mn(rta / rs); f_si = Csi / (Csi + Mb / 2 * MSUN)
    R["K2"] = dict(name=gm["name"], z=z, rs_SI_kpc=rs / KPCSI, rs_script_kpc=rs_ / KPC, rta_SI_kpc=rta / KPCSI, rta_script_kpc=rta_ / KPC,
                   fcold_SI=f_si, fcold_script=gm["fcold"], pass_=bool(abs(f_si / gm["fcold"] - 1) <= 0.01))
    P(f"[{ft}] K2 SI ({gm['name']}, z {z:.2f}): r_s {rs/KPCSI:.2f} vs {rs_/KPC:.2f} kpc; r_ta {rta/KPCSI:.1f} vs {rta_/KPC:.1f} kpc; "
      f"f_cold {f_si:.4f} vs {gm['fcold']:.4f} -> {'PASS' if R['K2']['pass_'] else 'FAIL'}")
    cm = cls(o); R["main"] = dict(cls=cm, word=word(cm), galaxies=o)
    zs = np.median([g["z"] for g in o])
    R["halves_z"] = {f"z<={zs:.2f}": float(np.median([g["D"] for g in o if g["z"] <= zs])), f"z>{zs:.2f}": float(np.median([g["D"] for g in o if g["z"] > zs]))}
    R["bracket"] = {"X_z0": cls(gals(ft, "z0")), "X_z1": cls(gals(ft, "z1")), "thin_disc": cls(gals(ft, bar="disc")), "e0.08": cls(o, 0.08), "e0.20": cls(o, 0.20)}
    R["bracket_words"] = {k: word(v) for k, v in R["bracket"].items()}; R["fragile"] = bool(len({R["main"]["word"]} | set(R["bracket_words"].values())) > 1)
    for t in TW:
        ct = cls(gals(ft, twin=t)); TW[t]["foot"][ft] = dict(cls=ct, word=word(ct), d_off=ct["off"] - cm["off"], bites=bool(abs(ct["off"] - cm["off"]) >= 0.05 or word(ct) != word(cm)))
    power = TW["TWH"]["foot"][ft]["bites"] and TW["TWD"]["foot"][ft]["bites"] and not TW["TWN"]["foot"][ft]["cls"]["line"]
    R["power"] = bool(power); R["final_word"] = R["main"]["word"] if (ok1 and R["K2"]["pass_"] and power) else "NO VERDICT (no power)"
    for g in o: P(f"[{ft}]   {g['name']:16s} z {g['z']:.2f} logMb {g['logMb']:.2f} Re {g['Re_kpc']:5.2f} X {g['X']:.2f}  f_cold {g['fcold']:.3f} fDM(author) {g['fDM_author']:.2f} D {g['D']:+.3f}")
    P(f"[{ft}] MAIN n {cm['n']}: off {cm['off']:+.4f}, se {cm['se']:.4f} (3 se {3*cm['se']:.4f}); median f_cold {cm['med_fcold']:.3f} vs author {cm['med_fDM']:.3f}; "
      f"|D| <= {E0}: {cm['n_within_e']} / {cm['n']} -> {R['main']['word']}")
    P(f"[{ft}]   z halves {R['halves_z']}")
    P(f"[{ft}]   brackets: " + "; ".join(f"{k} off {v['off']:+.4f} se {v['se']:.4f} -> {R['bracket_words'][k]}" for k, v in R["bracket"].items()) + f"; FRAGILE {R['fragile']}")
    P(f"[{ft}]   twins: " + "; ".join(f"{t} off {TW[t]['foot'][ft]['cls']['off']:+.4f} (d {TW[t]['foot'][ft]['d_off']:+.4f}) {TW[t]['foot'][ft]['word']} bites {TW[t]['foot'][ft]['bites']}" for t in TW))
    P(f"[{ft}] WORD: {R['final_word']}")
P("SRJ4: " + " / ".join(RES["foot"][f]["final_word"] for f in FOOTS) + " (canonical / alt)")
json.dump(RES, open(os.path.join(HERE, "srj4.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srj4.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
for t in TW:
    json.dump(TW[t], open(os.path.join(HERE, f"srj4_MUTATE_{t}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"srj4_MUTATE_{t}.out"), "w").write("\n".join(f"[{f}] {t}: off {TW[t]['foot'][f]['cls']['off']:+.4f} {TW[t]['foot'][f]['word']} bites {TW[t]['foot'][f]['bites']}" for f in TW[t]["foot"]) + "\n")
