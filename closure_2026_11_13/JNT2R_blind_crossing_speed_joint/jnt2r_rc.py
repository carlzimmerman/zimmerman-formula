#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): G2 (RC100 coverage) and G3 (SPARC coverage, then PD1's P2-SPARC line with truncation
at R_set) under the crossing-speed joint. SRH1's srh1_rc.py is executed read-only, from its own path, up to its
"# --- KA-G3b" marker (as SRJ2 did). The G3(b) body and the record-halo speed vgal are copied from SRJ2's srj2_rc.py; the
membership is this lane's. Memberships: P (primary, M_b against M_b*(z)), M (measured speed), B (record halo v_vir against
v*(z)); twins V (SRJ2: v_vir > v_stiff), N (none), H / D (v*/2, 2 v*) at f 1.
  python3 jnt2r_rc.py -> jnt2r_rc.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, csv, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2r_common as JC
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(SRH, "srh1_rc.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# --- KA-G3b")], SRC, "exec"), S)
FR, rfold_kpc, FB, hh, XTAB, SPF, RC, GALS, PRE, PN = (S[k] for k in ("FR", "rfold_kpc", "FB", "hh", "XTAB", "SPF", "RC", "GALS", "PRE", "PN"))
glaw, G, MS, KPC, A0, CR = (S[k] for k in ("glaw", "G", "MS", "KPC", "A0", "CR"))
VST = FR["VST"]; assert VST == {"canonical": 265.8, "alt": 288.1}; GF = FR["G"]; FOOTS = ("canonical", "alt")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P("JNT2R G2 / G3 (READING 5abea0324b). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
# measured speeds
VC = {}
with open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")) as fh:
    for r in csv.DictReader(fh): VC[r["name"]] = float(r["Vc_Re_kms"])
def gname(q): return q.get("name") or q["meta"].get("name", "?")
def vmeas_sparc(q):
    vf = float(q["meta"].get("Vflat", 0.0) or 0.0)
    if vf > 0: return vf
    return float(np.sqrt(np.max(np.asarray(q["GO"]) * np.asarray(q["Rm"])))) / 1e3
VS = {gname(q): vmeas_sparc(q) for q in GALS}
P(f"SPARC (FLD1 loader) {len(SPF)}, RC100 {len(RC)} (Vc found {sum(1 for g in RC if g['name'] in VC)}), SPARC (PD1 / QX8) {len(GALS)} (measured speeds {len(VS)}, Vflat = 0 rows {sum(1 for q in GALS if not q['meta'].get('Vflat'))})")

_ZC = {}
def zstate(z):
    k = round(z, 6)
    if k not in _ZC:
        with contextlib.redirect_stdout(io.StringIO()): FR["set_z"](z)
        _ZC[k] = (FR["L"]["conc"], FR["dta_of"](z), FR["Omz"](z))
    return _ZC[k]
_V = {}
def vgal(ft, Mb_sun, z):     # SRJ2's record-halo v_vir, copied
    key = (ft, round(math.log10(Mb_sun), 8), round(z, 6))
    if key not in _V:
        X = XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]; conc, dta, omz = zstate(z); Mta = X * Mb_sun * hh / (1 - FB)
        lM = brentq(lambda l: FR["halo_basics_z"](10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = FR["halo_basics_z"](10 ** lM, conc, dta, omz); _V[key] = math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
    return _V[key]
def above(mode, ft, Mb, z, vm):
    if mode == "N": return False
    if mode == "V": return vgal(ft, Mb, z) > VST[ft]
    if mode == "B": return vgal(ft, Mb, z) > JC.vstar(ft, z)
    if mode == "M": return vm > JC.vstar(ft, z)
    return JC.above(ft, Mb, z, {"P": 1.0, "H": 0.5, "D": 2.0}[mode])

RES = dict(lane="JNT2R", part="G2 G3", reading="5abea0324b", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
FG = (0.75, 1.00, 1.25, 1.50, 2.00, 3.00)
RUNS = [(m, f) for m in ("P", "M", "B") for f in FG] + [(m, 1.00) for m in ("V", "N", "H", "D")]
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    a0 = A0[ft]; X0 = XTAB[ft]["z0.0"]
    R["boundary_lMb"] = {f"z{z}": math.log10(JC.mbstar(ft, z)) for z in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5)}
    R["KA4_vcl_vs_vf"] = max(abs(JC.mbstar_from_vcl(ft, z) / JC.mbstar(ft, z) - 1) for z in (0.0, 1.0, 2.0, 4.4))
    P(f"[{ft}] v*(0) {JC.vstar(ft, 0):.1f} km/s; log M_b*(z) " + ", ".join(f"{k} {v:.3f}" for k, v in R["boundary_lMb"].items()) + f"; KA4 v_cl vs v_f boundary {R['KA4_vcl_vs_vf']:.1e}")
    r22 = np.array([2.2 * g["Re"] / rfold_kpc(ft, g["z"], g["logM"]) for g in RC])
    lMa = np.array([math.log10(0.5 * g["L36"] + 1.33 * g["MHI"]) for g in SPF]); ratio = np.array([g["R_last"] / rfold_kpc(ft, 0.0, l) for g, l in zip(SPF, lMa)])
    R["TWN_check"] = dict(G2_fmin=float(r22.max()), G3a_fmin=float(ratio.max()))
    MBS = []
    for q in GALS:
        Rr = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        MBS.append(max(float(np.max(np.clip(VB2 * Rr / PN["G_KPC"], 0, None))), 1e3))
    def g3b(f, ab):
        rows = []; names = []
        for q, Tf, Mbs, a_ in zip(GALS, PRE[ft], MBS, ab):
            Rm = q["Rm"]; g = q["GB"]
            if a_:
                names.append(gname(q)); ge = g.copy()
            else:
                rt = f * rfold_kpc(ft, 0.0, math.log10(Mbs)) * KPC; gt = G * Mbs * MS / rt ** 2; ph_t = float(glaw(gt, a0)) - gt
                ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + ph_t * (rt / Rm[:, None]) ** 2)
            lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
            wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
        def pooled(idx):
            wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
        massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
        o = dict(all=pooled(range(len(rows))), massive=pooled(massive), n_massive=len(massive), n_above=len(names), above_names=names)
        o["line"] = bool(o["all"]["rms"] <= 0.0660 and abs(o["all"]["mean"]) <= 0.05 and o["massive"]["rms"] <= 0.0660 and abs(o["massive"]["mean"]) <= 0.05)
        return o
    R["runs"] = {}
    g0 = g3b(1.0, [True] * len(GALS))      # f = 0 limit: R_set = 0 everywhere, g = g_N (the reference mark for rule (iii))
    R["G3_f0"] = dict(G3a_pass=False, G3b=g0, pass_=bool(g0["line"]))
    P(f"[{ft}] f 0 (reference limit): G2 FAIL (no coverage); G3(a) fail; G3(b) at g_N rms {g0['all']['rms']:.4f} mean {g0['all']['mean']:+.4f} -> {'pass' if g0['line'] else 'FAIL'}")
    for mode, f in RUNS:
        abR = np.array([above(mode, ft, 10 ** g["logM"], g["z"], VC[g["name"]]) for g in RC])
        abA = np.array([above(mode, ft, 10 ** l, 0.0, VS.get(g["name"], 0.0)) for g, l in zip(SPF, lMa)])
        abB = [above(mode, ft, Mbs, 0.0, VS[gname(q)]) for q, Mbs in zip(GALS, MBS)]
        covR = (~abR) & (r22 <= f); covA = (~abA) & (ratio <= f)
        o = dict(G2=dict(n_above=int(abR.sum()), above=[dict(name=RC[i]["name"], z=RC[i]["z"], logM=RC[i]["logM"], Vc=VC[RC[i]["name"]]) for i in np.where(abR)[0]],
                         covered=int(covR.sum()), pass_=bool(covR.all())),
                 G3a=dict(n_above=int(abA.sum()), above=[SPF[i]["name"] for i in np.where(abA)[0]], covered=int(covA.sum()), pass_=bool(covA.all())))
        b = g3b(f, abB) if not o["G3a"]["pass_"] else None
        o["G3b"] = b if b is not None else dict(n_above=int(sum(abB)), above_names=[gname(q) for q, a_ in zip(GALS, abB) if a_], evaluated=False)
        o["G3"] = dict(pass_=bool(o["G3a"]["pass_"] or (b is not None and b["line"])), by="a" if o["G3a"]["pass_"] else "b")
        R["runs"][f"{mode}|f{f:.2f}"] = o
        P(f"[{ft}] {mode} f {f:.2f}: G2 above {o['G2']['n_above']}, covered {o['G2']['covered']} / 100 -> {'PASS' if o['G2']['pass_'] else 'FAIL'}; "
          f"G3(a) above {o['G3a']['n_above']}, covered {o['G3a']['covered']} / {len(SPF)} -> {'pass' if o['G3a']['pass_'] else 'fail'}; "
          + (f"G3(b) above {b['n_above']} rms {b['all']['rms']:.4f} mean {b['all']['mean']:+.4f} massive {b['massive']['rms']:.4f} {b['massive']['mean']:+.4f} -> {'pass' if b['line'] else 'FAIL'}; " if b else f"G3(b) not needed (PD1-M_b above {o['G3b']['n_above']}); ")
          + f"G3 {'PASS' if o['G3']['pass_'] else 'FAIL'}")
    for mode in ("P", "M", "B", "H", "D"):
        lst = R["runs"][f"{mode}|f1.00"]["G2"]["above"]
        if lst: P(f"[{ft}]   {mode} RC100 above v*(z): " + ", ".join(f"{c['name']} (z {c['z']:.2f}, log M_b {c['logM']:.2f}, Vc {c['Vc']:.0f}, v* {JC.vstar(ft, c['z']):.0f})" for c in lst))
    # twin checks against SRJ2 and SRH1 stored values
    tv = R["runs"]["V|f1.00"]; tn = R["runs"]["N|f1.00"]
    R["TWV_reproduces"] = bool(tv["G2"]["covered"] == {"canonical": 69, "alt": 78}[ft] and tv["G3a"]["covered"] == {"canonical": 172, "alt": 175}[ft])
    R["TWN_reproduces"] = bool(abs(r22.max() - {"canonical": 0.391237, "alt": 0.391383}[ft]) <= 1e-4 and tn["G2"]["covered"] == 100 and abs(ratio.max() - {"canonical": 0.467132, "alt": 0.467178}[ft]) <= 1e-4 and tn["G3a"]["covered"] == len(SPF))
    P(f"[{ft}] TW-V reproduces SRJ2 (69 / 78 covered, G3a 172 / 175): {R['TWV_reproduces']}; TW-N reproduces SRH1 (f_min {r22.max():.6f}, {ratio.max():.6f}; all covered): {R['TWN_reproduces']}")
json.dump(RES, open(os.path.join(HERE, "jnt2r_rc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "jnt2r_rc.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
