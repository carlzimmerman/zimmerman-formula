#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): G2 (RC100 coverage) and G3 (SPARC coverage, then PD1's P2-SPARC line with
truncation at R_set) under the regime-split settled joint. SRH1's srh1_rc.py is executed read-only, from its own path, up to
its "# --- KA-G3b" marker (that executes SRH1's srh1_hm.py prefix, FLD1's fld1_compare.py and PD1's pd1.py prefix unchanged).
Each galaxy's regime: halo M_ta = X M_b h / (1 - FB) at its z (X = FRZ1's Xsh rule: z < 1 the z = 0 median, else z = 1),
FRZ1's halo_basics_z with its set_z(z) concentration and Delta_ta, FRZ1's v_vir against VST. Cluster regime: R_set = 0.
  G3(b) graded: cluster-regime galaxies g = g_N (SRH1's truncated form at R_trunc = 0). Reported: g = g_N + G C_R(R) / R^2.
  python3 srj2_rc.py -> srj2_rc.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
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
P("SRJ2 G2 / G3 (criteria b8a99499ad). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P(f"SPARC (FLD1 loader) {len(SPF)}, RC100 {len(RC)}, SPARC (PD1 / QX8) {len(GALS)}; VST {VST}")

_ZC = {}
def zstate(z):
    k = round(z, 6)
    if k not in _ZC:
        with contextlib.redirect_stdout(io.StringIO()): FR["set_z"](z)
        _ZC[k] = (FR["L"]["conc"], FR["dta_of"](z), FR["Omz"](z))
    return _ZC[k]
_V = {}
def vgal(ft, Mb_sun, z):
    key = (ft, round(math.log10(Mb_sun), 8), round(z, 6))
    if key not in _V:
        X = XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]; conc, dta, omz = zstate(z); Mta = X * Mb_sun * hh / (1 - FB)
        lM = brentq(lambda l: FR["halo_basics_z"](10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = FR["halo_basics_z"](10 ** lM, conc, dta, omz); v = math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
        zs = FR["S"]["z"]; FR["S"]["z"] = z; vf = FR["v_vir"](hb); FR["S"]["z"] = zs      # C3: FRZ1's own v_vir on the same halo
        assert abs(v / vf - 1) < 1e-12; _V[key] = v
    return _V[key]
def boundary_lMb(ft, z):
    return brentq(lambda l: vgal(ft, 10 ** l, z) - VST[ft], 9.0, 13.0, xtol=1e-6)

RES = dict(lane="SRJ2", part="G2 G3", criteria="b8a99499ad", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
FPTS = (0.75, 1.00, 1.25)
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    R["boundary_lMb"] = {f"z{z}": boundary_lMb(ft, z) for z in (0.0, 1.0, 2.0)}
    P(f"[{ft}] v_vir = v_stiff at log M_b (Msun): z 0 {R['boundary_lMb']['z0.0']:.3f}, z 1 {R['boundary_lMb']['z1.0']:.3f}, z 2 {R['boundary_lMb']['z2.0']:.3f}")
    # ---- G2
    r22 = np.array([2.2 * g["Re"] / rfold_kpc(ft, g["z"], g["logM"]) for g in RC]); vR = np.array([vgal(ft, 10 ** g["logM"], g["z"]) for g in RC]); clR = vR > VST[ft]
    R["G2"] = dict(n_cluster=int(clR.sum()), cluster=[dict(name=RC[i]["name"], z=RC[i]["z"], logM=RC[i]["logM"], v_vir=float(vR[i])) for i in np.where(clR)[0]],
                   v_vir_max=float(vR.max()), off_f_min=float(r22.max()), on_f_min=(float(r22[~clR].max()) if clR.sum() == 0 else math.inf))
    for f in FPTS:
        cov = (~clR) & (r22 <= f); R["G2"][f"f{f:.2f}"] = dict(covered=int(cov.sum()), n=len(RC), pass_=bool(cov.all()))
    R["G2"]["f0"] = dict(pass_=False, note="R_set = 0: no galaxy covered")
    R["C1_G2"] = dict(off_f_min=float(r22.max()), pass_=bool(abs(r22.max() - {"canonical": 0.391237, "alt": 0.391383}[ft]) <= 1e-4 and (r22 <= 1).all()))
    P(f"[{ft}] G2 RC100: cluster-regime {int(clR.sum())} / {len(RC)} (max v_vir {vR.max():.1f} km/s, median {np.median(vR):.1f}); " + "; ".join(f"f {f:.2f}: covered {R['G2'][f'f{f:.2f}']['covered']} / 100 -> {'PASS' if R['G2'][f'f{f:.2f}']['pass_'] else 'FAIL'}" for f in FPTS)
      + f"; C1 split off f_min {r22.max():.6f} -> {'PASS' if R['C1_G2']['pass_'] else 'FAIL'}")
    for c in R["G2"]["cluster"]: P(f"[{ft}]    G2 cluster-regime: {c['name']} z {c['z']:.2f} log M_b {c['logM']:.2f} v_vir {c['v_vir']:.1f}")
    # ---- G3 (a)
    lMa = np.array([math.log10(0.5 * g["L36"] + 1.33 * g["MHI"]) for g in SPF])
    ratio = np.array([g["R_last"] / rfold_kpc(ft, 0.0, l) for g, l in zip(SPF, lMa)]); vA = np.array([vgal(ft, 10 ** l, 0.0) for l in lMa]); clA = vA > VST[ft]
    R["G3a"] = dict(n_cluster=int(clA.sum()), cluster=[dict(name=SPF[i]["name"], logMb=float(lMa[i]), v_vir=float(vA[i])) for i in np.where(clA)[0]], v_vir_max=float(vA.max()))
    for f in FPTS:
        cov = (~clA) & (ratio <= f); R["G3a"][f"f{f:.2f}"] = dict(covered=int(cov.sum()), n=len(SPF), pass_=bool(cov.all()))
    R["C1_G3a"] = dict(off_f_min=float(ratio.max()), pass_=bool(abs(ratio.max() - {"canonical": 0.467132, "alt": 0.467178}[ft]) <= 1e-4 and (ratio <= 1).all()))
    P(f"[{ft}] G3(a) SPARC: cluster-regime {int(clA.sum())} / {len(SPF)} (max v_vir {vA.max():.1f}); " + "; ".join(f"f {f:.2f}: covered {R['G3a'][f'f{f:.2f}']['covered']} / 175 -> {'pass' if R['G3a'][f'f{f:.2f}']['pass_'] else 'fail'}" for f in FPTS)
      + f"; C1 split off f_min {ratio.max():.6f} -> {'PASS' if R['C1_G3a']['pass_'] else 'FAIL'}")
    for c in R["G3a"]["cluster"]: P(f"[{ft}]    G3(a) cluster-regime: {c['name']} log M_b {c['logMb']:.3f} v_vir {c['v_vir']:.1f}")
    # ---- G3 (b): PD1's sparc() body as SRH1 copied it, R_trunc = R_set, cluster regime g_N (graded) or g_N + G C_R / R^2 (reported)
    a0 = A0[ft]; X0 = XTAB[ft]["z0.0"]
    def g3b(f, clmode):
        rows = []; ncl = 0; names = []
        for q, Tf in zip(GALS, PRE[ft]):
            Rr = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
            Mbs = max(float(np.max(np.clip(VB2 * Rr / PN["G_KPC"], 0, None))), 1e3); g = q["GB"]
            if vgal(ft, Mbs, 0.0) > VST[ft]:
                ncl += 1; names.append(q.get("name") or q["meta"].get("name", "?"))
                ge = g.copy() if clmode == "newton" else g + (G * CR(Rm, Mbs, X0) / Rm ** 2)[:, None]
            else:
                rt = f * rfold_kpc(ft, 0.0, math.log10(Mbs)) * KPC; gt = G * Mbs * MS / rt ** 2; ph_t = float(glaw(gt, a0)) - gt
                ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + ph_t * (rt / Rm[:, None]) ** 2)
            lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
            wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
        def pooled(idx):
            wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
        massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
        o = dict(all=pooled(range(len(rows))), massive=pooled(massive), n_massive=len(massive), n_cluster=ncl, cluster_names=names)
        o["line"] = bool(o["all"]["rms"] <= 0.0660 and abs(o["all"]["mean"]) <= 0.05 and o["massive"]["rms"] <= 0.0660 and abs(o["massive"]["mean"]) <= 0.05)
        return o
    R["G3b"] = {}; R["G3"] = {}
    for f in FPTS:
        key = f"f{f:.2f}"; a_ok = R["G3a"][key]["pass_"]
        b = g3b(f, "newton"); bref = g3b(f, "reference"); R["G3b"][key] = dict(graded=b, reported_reference=bref, evaluated=not a_ok)
        R["G3"][key] = dict(pass_=bool(a_ok or b["line"]), by="a" if a_ok else "b")
        P(f"[{ft}] f {f:.2f}: G3(a) {'pass' if a_ok else 'fail'}; G3(b) [cluster-regime {b['n_cluster']} galaxies at g_N] rms {b['all']['rms']:.4f} mean {b['all']['mean']:+.4f}, massive ({b['n_massive']}) rms {b['massive']['rms']:.4f} mean {b['massive']['mean']:+.4f} -> {'pass' if b['line'] else 'FAIL'}"
          f"{'' if not a_ok else ' (not needed)'} => G3 {'PASS' if R['G3'][key]['pass_'] else 'FAIL'} | reported, cluster-regime with reference NFW: rms {bref['all']['rms']:.4f} mean {bref['all']['mean']:+.4f}, massive rms {bref['massive']['rms']:.4f} mean {bref['massive']['mean']:+.4f} line {'holds' if bref['line'] else 'FAILS'}")
    P(f"[{ft}] G3(b) cluster-regime galaxies (PD1 M_b): {R['G3b']['f1.00']['graded']['cluster_names']}")
json.dump(RES, open(os.path.join(HERE, "srj2_rc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srj2_rc.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
