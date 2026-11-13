#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): G4, ONE1's KiDS gate as SRH1 ran it, under the regime-split settled joint.
SRH1's srh1_lens.py is executed read-only, from its own path, up to its "# ---------------- runs, checkpointed" marker (that
executes ONE1's one1_kids.py prefix and SRH1's srh1_hm.py prefix unchanged, and SRH1's KA-G4b / KA-4c). The only change:
the lens table holds the reference profile (SRH1's f = 0) at every (log M_b, z) node whose halo (SRH1's: M_ta = X M_b h /
(1 - FB), FRZ1's halo_basics_z at z) has FRZ1's v_vir > VST. Neighbours: ONE1's counted-once halos, as SRH1.
  Configs: f0 (C2), off_f1.00 (C1), on_f1.00 (graded), on_f0.75, on_f1.25.  --twin F2: on_f2.00 only (TW-F2; exits 1).
  python3 srj2_lens.py [--twin F2] -> srj2_lens.json / .out  or  srj2_lens_MUTATE_F2.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
TWIN = sys.argv[sys.argv.index("--twin") + 1] if "--twin" in sys.argv else None; assert TWIN in (None, "F2")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(SRH, "srh1_lens.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_lens_lib"}
exec(compile(code[:code.index("# ---------------- runs, checkpointed\n")], SRC, "exec"), S)
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
O, FR = S["O"], S["FR"]
profile, dsig_prof, DINF_T, LMG, ZG, UT, own_S, nb_sums, fit, gate_of, slim, MK, XP, KGRID = (S[k] for k in (
    "profile", "dsig_prof", "DINF_T", "LMG", "ZG", "UT", "own_S", "nb_sums", "fit", "gate_of", "slim", "MK", "XP", "KGRID"))
conc_z, hbz, FB, hh = S["conc_z"], S["hbz"], S["FB"], S["hh"]
VST = FR["VST"]; assert VST == {"canonical": 265.8, "alt": 288.1}
GF = FR["G"]; lMg, zz1, typ1, n1 = S["lMg"], S["zz1"], np.asarray(O["typ1"]), S["n1"]
STORED = json.load(open(os.path.join(SRH, "srh1_lens.json")))
P(f"SRJ2 G4 (criteria b8a99499ad){' TWIN F2 (deliberately wrong)' if TWIN else ''}. SRH1 lens prefix executed. Host-free lenses (1.0 R_h) {n1:,}: late {int((typ1 == 0).sum()):,}, early {int((typ1 == 1).sum()):,}")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ---------------- v_vir of each table node's halo (SRH1's halo construction, FRZ1's v_vir)
def hb_node(ft, lMb, z):
    conc, dta, omz = conc_z(round(z, 6)); Mta = XP[ft] * 10 ** lMb * hh / (1 - FB)
    lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
    return hbz(10 ** lM, conc, dta, omz)
def v_node(ft, lMb, z):
    hb = hb_node(ft, lMb, z); return math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
# C3 (lens side): this formula against FRZ1's v_vir on the same halo with FRZ1's state at that z
c3 = 0.0
for z in (0.1, 0.3, 0.5):
    hb = hb_node("canonical", 11.0, z); FR["set_z"](z); c3 = max(c3, abs(math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"]) / FR["v_vir"](hb) - 1))
P(f"C3 (lens side) v_vir formula against FRZ1's v_vir: max rel {c3:.1e} -> {'PASS' if c3 <= 1e-12 else 'FAIL'}")
VN = {ft: np.array([[v_node(ft, float(lm), float(z)) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
for ft in VN:
    edge = [float(np.interp(VST[ft], VN[ft][:, j], LMG)) for j in range(len(ZG))]
    P(f"[{ft}] v_vir = v_stiff boundary in log M_b (Msun) at z 0.1 / 0.3 / 0.5: " + " / ".join(f"{edge[int(round(z / 0.05))]:.3f}" for z in (0.1, 0.3, 0.5)))
def table_J(ft, f, split):
    T = np.empty((len(LMG), len(ZG), len(UT))); Sm = np.empty((len(LMG), len(ZG)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            ff = 0.0 if (split and VN[ft][i, j] > VST[ft]) else f
            pc, M3, inf = profile(ft, float(lm), float(z), ff, "S"); T[i, j] = dsig_prof(UT, pc, M3) / DINF_T; Sm[i, j] = inf["s"]
    return T, Sm
def lens_v(ft, k):
    """each host-free lens's v_vir at M_b = k M_gal, its z (bilinear in log v over the node grid)."""
    lv = np.log(VN[ft]); x = np.clip((lMg + math.log10(k) - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1 - 1e-9); y = np.clip((zz1 - ZG[0]) / (ZG[1] - ZG[0]), 0, len(ZG) - 1 - 1e-9)
    i = np.floor(x).astype(int); j = np.floor(y).astype(int); wx = x - i; wy = y - j
    return np.exp((1 - wx) * (1 - wy) * lv[i, j] + wx * (1 - wy) * lv[i + 1, j] + (1 - wx) * wy * lv[i, j + 1] + wx * wy * lv[i + 1, j + 1])

RES = dict(lane="SRJ2", part="G4" + (" TWIN F2" if TWIN else ""), criteria="b8a99499ad", C3_lens=c3, cfg={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
cfgs = [("on_f2.00", 2.0, True)] if TWIN else [("f0", 0.0, True), ("off_f1.00", 1.0, False), ("on_f1.00", 1.0, True), ("on_f0.75", 0.75, True), ("on_f1.25", 1.25, True)]
for ft in ("canonical", "alt"):
    X = XP[ft]; lams = O["lam_grid"](X, extra=[1.0, math.sqrt(O["A0C"] / O["A0"]["alt"])]); lams9 = sorted(set([0.65] + list(map(float, lams)) + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9)
    P(f"[{ft}] neighbour grid lambda {np.round(lams9, 3).tolist()}: {npr:,} pairs  [{time.time() - T0:.0f} s]")
    for name, f, split in cfgs:
        T, Sm = table_J(ft, f, split); OS = own_S(ft, T)
        rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; gt = gate_of(rn)
        cnt = {}
        for sub in ("all", "late", "early"):
            q = rn[("KO1", 1.6, sub)]
            if q is None: continue
            v = lens_v(ft, q["k"]); hi = v > VST[ft]
            cnt[sub] = dict(k=float(q["k"]), above_all=int(hi.sum()), above_late=int((hi & (typ1 == 0)).sum()), above_early=int((hi & (typ1 == 1)).sum()),
                            n_all=int(n1), n_late=int((typ1 == 0).sum()), n_early=int((typ1 == 1).sum()), v_median_early=float(np.median(v[typ1 == 1])), v_median_late=float(np.median(v[typ1 == 0])))
        nodes_ref = int((VN[ft] > VST[ft]).sum()) if split else 0
        RES["cfg"][f"{ft}|{name}"] = dict(f=f, split=split, gate=gt, nb={"|".join(map(str, mk)): slim(rn[mk]) for mk in MK}, counts=cnt, nodes_reference=nodes_ref, nodes_total=int(VN[ft].size))
        L_ = gt["lines"]
        P(f"[{ft}] {name:10s} gate {gt['status']} {gt['failing']}: z all / late / early " + " / ".join(f"{L_['G-K1 ' + s]['z']:+.4f}" for s in ("all", "late", "early"))
          + f", chi2 {L_['G-K2 all profile']['chi2']:.4f}, type diff z {L_['G-K3 type difference']['z']:+.4f}; k (all) {cnt.get('all', {}).get('k', float('nan')):.3f}; "
          + "; ".join(f"{s}-fit k {c['k']:.3f}: above v_stiff {c['above_all']:,} / {c['n_all']:,} (late {c['above_late']:,} / {c['n_late']:,}, early {c['above_early']:,} / {c['n_early']:,})" for s, c in cnt.items())
          + f"  [{time.time() - T0:.0f} s]")
def zrow(cfg): L_ = cfg["gate"]["lines"]; return [L_["G-K1 all"]["z"], L_["G-K1 late"]["z"], L_["G-K1 early"]["z"], L_["G-K3 type difference"]["z"]], L_["G-K2 all profile"]["chi2"]
if TWIN:
    GR = json.load(open(os.path.join(HERE, "srj2_lens.json")))
    for ft in ("canonical", "alt"):
        a, _ = zrow(RES["cfg"][f"{ft}|on_f2.00"]); b, _ = zrow(GR["cfg"][f"{ft}|on_f1.00"])
        RES[f"TW_F2_{ft}"] = dict(early_z_f2=a[2], early_z_f1=b[2], G4_bites=bool(b[2] - a[2] > 0.10))
        P(f"[{ft}] TW-F2 G4 part: early z {b[2]:+.4f} (f 1) -> {a[2]:+.4f} (f 2) -> {'bites' if RES[f'TW_F2_{ft}']['G4_bites'] else 'does not bite'}")
else:
    chk = {}
    for ft in ("canonical", "alt"):
        for mine, theirs in (("off_f1.00", "f1.00"), ("f0", "f0")):
            a, ca = zrow(RES["cfg"][f"{ft}|{mine}"]); b, cb = zrow(STORED["cfg"][f"{ft}|{theirs}"])
            d = max(abs(x - y) for x, y in zip(a, b)); ok = bool(d <= 0.005 and abs(ca - cb) <= 0.01 and RES["cfg"][f"{ft}|{mine}"]["gate"]["status"] == STORED["cfg"][f"{ft}|{theirs}"]["gate"]["status"])
            chk[f"{ft}|{mine}"] = dict(max_z_dev=d, chi2_dev=abs(ca - cb), pass_=ok)
            P(f"[{ft}] {'C1' if mine != 'f0' else 'C2'} {mine} against SRH1's stored {theirs}: max z dev {d:.1e}, chi2 dev {abs(ca - cb):.1e}, status {RES['cfg'][ft + '|' + mine]['gate']['status']} -> {'PASS' if ok else 'FAIL'}")
        a, ca = zrow(RES["cfg"][f"{ft}|on_f1.00"]); b, cb = zrow(RES["cfg"][f"{ft}|f0"])
        RES[f"trivial_{ft}"] = dict(max_z_vs_ref=max(abs(x - y) for x, y in zip(a, b)), chi2_vs_ref=abs(ca - cb), trivial=bool(max(abs(x - y) for x, y in zip(a, b)) <= 0.10 and abs(ca - cb) <= 0.10))
        P(f"[{ft}] joint f 1 against the reference (f 0): max |dz| {RES['trivial_' + ft]['max_z_vs_ref']:.4f}, |dchi2| {RES['trivial_' + ft]['chi2_vs_ref']:.4f} -> {'TRIVIAL' if RES['trivial_' + ft]['trivial'] else 'not trivial'}")
    RES["checks"] = chk
RES["seconds"] = time.time() - T0
tag = "_MUTATE_F2" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"srj2_lens{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"srj2_lens{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
sys.exit(1 if TWIN else 0)
