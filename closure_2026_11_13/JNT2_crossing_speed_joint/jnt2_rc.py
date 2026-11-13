#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): membership of SPARC and RC100, G2 (RC100 coverage) and G3 (SPARC coverage, then
PD1's line with galaxies above the boundary at g_N, as SRJ2 graded it) under the crossing-speed joint. SRJ2's srj2_rc.py
content copied (cited): SRH1's srh1_rc.py is executed read-only from its own path up to its "# --- KA-G3b" marker.
Boundary per mode (jnt2_common): main / H / D: the lemma's v_L(M_b, z) against v*(z) (x 1/2, x 2); S: SRJ2's vgal
(FRZ1 halo, X ~ 56) against v_stiff; 0: none. Measured-speed rule (secondary): SPARC Vflat (else max V_obs), RC100 Vc(R_e).
  python3 jnt2_rc.py [--mode main|S|0|H|D] -> jnt2_rc[_MUTATE_<mode>].json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, csv, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2_common as C
MODE = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "main"; assert MODE in C.MODES
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(SRH, "srh1_rc.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# --- KA-G3b")], SRC, "exec"), S)
FR, rfold_kpc, FB, hh, XTAB, SPF, RC, GALS, PRE, PN = (S[k] for k in ("FR", "rfold_kpc", "FB", "hh", "XTAB", "SPF", "RC", "GALS", "PRE", "PN"))
glaw, G, MS, KPC, A0, CR = (S[k] for k in ("glaw", "G", "MS", "KPC", "A0", "CR"))
assert FR["VST"] == C.VSTIFF; GF = FR["G"]; FOOTS = ("canonical", "alt")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"JNT2 G2 / G3 / membership, mode {MODE} (criteria e186b314ef). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

_ZC = {}
def zstate(z):
    k = round(z, 6)
    if k not in _ZC:
        with contextlib.redirect_stdout(io.StringIO()): FR["set_z"](z)
        _ZC[k] = (FR["L"]["conc"], FR["dta_of"](z), FR["Omz"](z))
    return _ZC[k]
_V = {}
def vgal(ft, Mb_sun, z):                       # SRJ2's FRZ1-halo speed (X ~ 56), copied
    key = (ft, round(math.log10(Mb_sun), 8), round(z, 6))
    if key not in _V:
        X = XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]; conc, dta, omz = zstate(z); Mta = X * Mb_sun * hh / (1 - FB)
        lM = brentq(lambda l: FR["halo_basics_z"](10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = FR["halo_basics_z"](10 ** lM, conc, dta, omz); _V[key] = math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
    return _V[key]
def above_model(ft, Mb_sun, z):
    if MODE == "S": return vgal(ft, Mb_sun, z) > C.VSTIFF[ft]
    return C.vL_kms(Mb_sun, z) > C.vstar_kms(ft, z, MODE)
def above_meas(ft, v_kms, z): return v_kms > C.vstar_kms(ft, z, MODE)

# measured speeds
RCV = {r["name"]: float(r["Vc_Re_kms"]) for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")))}
SD = os.path.join(REPO, "real_research", "data"); VFL = {}
for line in open(os.path.join(SD, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) == 19:
        try: VFL[tok[0]] = float(tok[15])
        except ValueError: pass
def vmeas_sparc(nm):
    vf = VFL.get(nm, 0.0)
    if vf > 0: return vf, "Vflat"
    a = np.genfromtxt(os.path.join(SD, "sparc_data", nm + "_rotmod.dat"), comments="#"); return float(np.nanmax(a[:, 1])), "max V_obs"

RES = dict(lane="JNT2", part="G2 G3 membership", mode=MODE, criteria="e186b314ef", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
FPTS = (0.75, 1.00, 1.25, 1.5, 2.0, 3.0)
P(f"SPARC (FLD1 loader) {len(SPF)}, RC100 {len(RC)}, SPARC (PD1) {len(GALS)}")
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    R["vstar"] = {f"z{z}": C.vstar_kms(ft, z, MODE) for z in (0.0, 0.5, 1.0, 2.0, 2.5, 3.0)}
    if MODE in ("main", "H", "D"): R["logMstar"] = {f"z{z}": C.logMstar(ft, z, MODE) for z in (0.0, 0.3, 1.0, 2.0, 2.5)}
    P(f"[{ft}] boundary km/s at z 0 / 1 / 2 / 2.5: " + " / ".join(f"{R['vstar'][k]:.1f}" for k in ("z0.0", "z1.0", "z2.0", "z2.5"))
      + (("; log M* " + " / ".join(f"{v:.3f}" for v in R["logMstar"].values()) + " at z 0 / 0.3 / 1 / 2 / 2.5") if "logMstar" in R else ""))
    # ---- RC100: membership (model, measured, FRZ1-halo reported) and G2 coverage
    r22 = np.array([2.2 * g["Re"] / rfold_kpc(ft, g["z"], g["logM"]) for g in RC])
    abM = np.array([above_model(ft, 10 ** g["logM"], g["z"]) for g in RC]); abV = np.array([above_meas(ft, RCV[g["name"]], g["z"]) for g in RC])
    abF = np.array([vgal(ft, 10 ** g["logM"], g["z"]) > C.vstar_kms(ft, g["z"], MODE) for g in RC])
    zb = [(0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 9)]; zz = np.array([g["z"] for g in RC])
    R["RC100"] = dict(n_above_model=int(abM.sum()), n_above_measured=int(abV.sum()), n_above_frz1halo_reported=int(abF.sum()),
                      by_z={f"{a}-{b}": dict(n=int(((zz >= a) & (zz < b)).sum()), model=int((abM & (zz >= a) & (zz < b)).sum()), measured=int((abV & (zz >= a) & (zz < b)).sum())) for a, b in zb},
                      above_model=[dict(name=RC[i]["name"], z=RC[i]["z"], logM=RC[i]["logM"], vL=C.vL_kms(10 ** RC[i]["logM"], RC[i]["z"]), Vc=RCV[RC[i]["name"]], vstar=C.vstar_kms(ft, RC[i]["z"], MODE)) for i in np.where(abM)[0]],
                      near20=[dict(name=g["name"], z=g["z"], Vc=RCV[g["name"]], vstar=C.vstar_kms(ft, g["z"], MODE)) for g in RC if MODE != "0" and abs(RCV[g["name"]] / C.vstar_kms(ft, g["z"], MODE) - 1) <= 0.2],
                      f_min_below=float(r22[~abM].max()) if (~abM).any() else None)
    for lab, ab in (("model", abM), ("measured", abV)):
        for f in FPTS:
            cov = (~ab) & (r22 <= f); R["RC100"][f"G2_{lab}_f{f:.2f}"] = dict(covered=int(cov.sum()), pass_=bool(cov.all()))
    P(f"[{ft}] RC100 above: model {int(abM.sum())}, measured {int(abV.sum())}, FRZ1-halo (reported) {int(abF.sum())}; by z " + "; ".join(f"{k}: {v['model']} / {v['measured']} of {v['n']}" for k, v in R["RC100"]["by_z"].items())
      + "; G2 model covered " + ", ".join(f"f {f}: {R['RC100'][f'G2_model_f{f:.2f}']['covered']}" for f in FPTS) + f"; measured covered (all f) {R['RC100']['G2_measured_f1.00']['covered']}")
    for c in R["RC100"]["above_model"]: P(f"[{ft}]    above (model): {c['name']} z {c['z']:.2f} log M_b {c['logM']:.2f} v_L {c['vL']:.1f} Vc {c['Vc']:.0f} v* {c['vstar']:.1f}")
    # ---- SPARC: membership and G3(a)
    lMa = np.array([math.log10(0.5 * g["L36"] + 1.33 * g["MHI"]) for g in SPF])
    ratio = np.array([g["R_last"] / rfold_kpc(ft, 0.0, l) for g, l in zip(SPF, lMa)])
    sM = np.array([above_model(ft, 10 ** l, 0.0) for l in lMa]); vm = [vmeas_sparc(g["name"]) for g in SPF]; sV = np.array([above_meas(ft, v, 0.0) for v, _ in vm])
    vLmax = float(max(C.vL_kms(10 ** l, 0.0) for l in lMa)); vmax = max(vm)
    R["SPARC"] = dict(n_above_model=int(sM.sum()), n_above_measured=int(sV.sum()), vL_max=vLmax, vmeas_max=vmax[0], logMb_max=float(lMa.max()),
                      above=[SPF[i]["name"] for i in np.where(sM | sV)[0]], n_vflat_missing=sum(1 for _, s in vm if s != "Vflat"))
    for lab, ab in (("model", sM), ("measured", sV)):
        for f in FPTS:
            cov = (~ab) & (ratio <= f); R["SPARC"][f"G3a_{lab}_f{f:.2f}"] = dict(covered=int(cov.sum()), pass_=bool(cov.all()))
    P(f"[{ft}] SPARC above: model {int(sM.sum())}, measured {int(sV.sum())} (max v_L {vLmax:.1f}, max measured {vmax[0]:.1f}, max log M_b {lMa.max():.2f}); G3(a) model covered "
      + ", ".join(f"f {f}: {R['SPARC'][f'G3a_model_f{f:.2f}']['covered']}" for f in FPTS) + f"; f_min {ratio[~sM].max():.6f}")
    # ---- G3(b): PD1's line (SRJ2's g3b, copied; above-boundary galaxies at g_N)
    a0 = A0[ft]; X0 = XTAB[ft]["z0.0"]
    def g3b(f):
        rows = []; ncl = 0
        for q, Tf in zip(GALS, PRE[ft]):
            Rr = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
            Mbs = max(float(np.max(np.clip(VB2 * Rr / PN["G_KPC"], 0, None))), 1e3); g = q["GB"]
            if MODE != "0" and above_model(ft, Mbs, 0.0):
                ncl += 1; ge = g.copy()
            else:
                rt = f * rfold_kpc(ft, 0.0, math.log10(Mbs)) * KPC; gt = G * Mbs * MS / rt ** 2; ph_t = float(glaw(gt, a0)) - gt
                ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + ph_t * (rt / Rm[:, None]) ** 2)
            lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
            wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
        def pooled(idx):
            wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
        massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
        o = dict(all=pooled(range(len(rows))), massive=pooled(massive), n_massive=len(massive), n_above=ncl)
        o["line"] = bool(o["all"]["rms"] <= 0.0660 and abs(o["all"]["mean"]) <= 0.05 and o["massive"]["rms"] <= 0.0660 and abs(o["massive"]["mean"]) <= 0.05)
        return o
    R["G3"] = {}
    for f in FPTS:
        key = f"f{f:.2f}"; a_ok = R["SPARC"][f"G3a_model_{key}"]["pass_"]; b = g3b(f)
        R["G3"][key] = dict(a=a_ok, b=b, pass_=bool(a_ok or b["line"]), by="a" if a_ok else "b")
        P(f"[{ft}] f {f:.2f}: G3(a) {'pass' if a_ok else 'fail'}; G3(b) [{b['n_above']} above at g_N] rms {b['all']['rms']:.4f} mean {b['all']['mean']:+.4f}, massive rms {b['massive']['rms']:.4f} -> {'pass' if b['line'] else 'FAIL'} => G3 {'PASS' if R['G3'][key]['pass_'] else 'FAIL'}")
tag = "" if MODE == "main" else f"_MUTATE_{MODE}"
json.dump(RES, open(os.path.join(HERE, f"jnt2_rc{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2_rc{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
