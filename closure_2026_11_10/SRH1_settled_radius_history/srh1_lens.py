#!/usr/bin/env python3
"""SRH1 (FROZEN_CRITERIA.md, 5ed8a37ec6): G4, ONE1's KiDS host-free row with each lens's settled layout: the law's phantom of a
central M_b (ONE1's counted-once halo) inside R_set = f R_fold(z_lens, M_b), FRZ1's galaxy-regime NFW reference (M_ta =
X M_b / (1 - FB), Duffy c(M, z), Delta_ta(z)) outside, the enclosed cold mass at R_set the reference's (FZS1's s), total
(1 + X) M_b. ONE1's one1_kids.py is executed from its own path up to its "# ---------------- primary" marker (data side,
estimator, fit, neighbour kernel unchanged); the own-halo model enters ONE1's cells as glaw(k g_bar) x DeltaSigma_S /
DeltaSigma_inf, tabulated in (log M_b, z, log u). Neighbours: ONE1's counted-once halos on a 9-node lambda grid.
KA-G4a (ONE1 rerun as ONE1 ran it), KA-G4b (projection), KA-G4c (ONE1's halo through this pipeline), comparators f 0 / inf,
MU4 (reference outside R_set removed, f 0.5, canonical), pooled pointwise reading (PD1's P2-KiDS line, Brouwer 2021 Fig-9
mass bins, z 0.31) with KA-4c. Checkpoints after each configuration (srh1_lens_partial.json); SIGTERM-safe.
  nice -n 10 python3 srh1_lens.py -> srh1_lens.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, io, contextlib, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def tm(): return f"[{time.time() - T0:.0f} s]"
# ---------------- srh1_hm prefix: FZS1's rfold_kpc, FRZ1's halo model
SRC = os.path.join(HERE, "srh1_hm.py"); src = open(SRC).read(); H = {"__file__": SRC, "__name__": "srh1_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------ checkpointed run\n")], SRC, "exec"), H)
rfold_kpc, FR = H["rfold_kpc"], H["F"]; FB, hh, hbz, m_nfw = FR["FB"], FR["h"], FR["halo_basics_z"], FR["m_nfw"]
assert abs(float(m_nfw(1.0)) - (math.log(2) - 0.5)) < 1e-12
# ---------------- ONE1 prefix
O1 = os.path.join(REPO, "fable52_push", "ONE1_counted_once"); OSRC = os.path.join(O1, "one1_kids.py"); osrc = open(OSRC).read()
O = {"__file__": OSRC, "__name__": "one1_kids_lib"}
exec(compile(osrc[:osrc.index("# ---------------- primary\n")], OSRC, "exec"), O)
G, Msun, Mpc, A0, A0C, XP, KGRID, MASKS, WW1, GB1, WGL, OKC1, psum, fit, jk, glaw, UG, LUG, D_INF = (O[k] for k in (
    "G", "Msun", "Mpc", "A0", "A0C", "XP", "KGRID", "MASKS", "WW1", "GB1", "WGL", "OKC1", "psum", "fit", "jk", "glaw", "UG", "LUG", "D_INF"))
FOOT = ("canonical", "alt"); NPAT = O["NPAT"]; idx1 = O["idx1"]; n1 = O["n1"]
lMg = np.log10(O["Mg1"] / Msun); zz1 = np.asarray(O["zl"])[idx1]
STORED = json.load(open(os.path.join(O1, "one1_kids.json")))
P(f"\nSRH1 G4 (criteria 5ed8a37ec6). ONE1 prefix executed {tm()}. Host-free lenses at 1.0 R_h {n1:,}; lens z 5-95 % {np.percentile(zz1, 5):.2f}-{np.percentile(zz1, 95):.2f}; X {XP}")
P("kappa = 1/2 FITTED; not theory closed.")

# ---------------- the settled halo
def Mph(x): return np.sqrt(0.25 + np.asarray(x, float) ** 2) - 0.5
def dMph(x): x = np.asarray(x, float); return x / np.sqrt(0.25 + x * x)
def dm_nfw(y): return y / (1 + y) ** 2
_CZ = {}
def conc_z(z):
    if z not in _CZ:
        FR["set_z"](z); _CZ[z] = (FR["L"]["conc"], FR["dta_of"](z), FR["Omz"](z))
    return _CZ[z]
_HALO = {}
def halo(ft, lMb, z):
    key = (ft, round(lMb, 6), round(z, 6))
    if key not in _HALO:
        X = XP[ft]; conc, dta, omz = conc_z(round(z, 6)); Mta = X * 10 ** lMb * hh / (1 - FB)
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); rM = math.sqrt(G * 10 ** lMb * Msun / A0[ft]); conv = Mpc / ((1 + z) * hh)
        _HALO[key] = (X, hb["rs"] * conv / rM, hb["rta"] * conv / rM, rfold_kpc(ft, z, lMb) * 3.0857e19 / rM, rM)
    return _HALO[key]
def profile(ft, lMb, z, f, mode="S"):
    """cold layout in units of M_b and r_M: pieces [(a, b, M'(x))], M3D(x), info. mode S (settled), cut (MU4), ONE1."""
    X, xs, xta, xf, rM = halo(ft, lMb, z); xt = math.sqrt(X * (X + 1)); mt = float(m_nfw(xta / xs))
    if mode == "ONE1":
        return [(0.0, xt, dMph)], (lambda x: np.minimum(Mph(x), X)), dict(s=1.0, xset=xt, xta=xta, xf=xf)
    xset = xta if math.isinf(f) else min(f * xf, xta)
    CRf = lambda x: X * m_nfw(np.minimum(np.asarray(x, float), xta) / xs) / mt
    dCR = lambda x: X * dm_nfw(np.asarray(x, float) / xs) / xs / mt
    s = float(CRf(xset)) / float(min(Mph(xset), X)) if xset > 0 else 1.0
    pcs = []
    if xset > 0: pcs.append((0.0, min(xset, xt), (lambda x, s=s: s * dMph(x))))
    if mode == "S":
        if xset < xta: pcs.append((xset, xta, dCR))
        M3 = lambda x: np.where(np.asarray(x) <= xset, s * np.minimum(Mph(x), X), CRf(x))
    else:
        cst = float(CRf(xset)); M3 = lambda x: np.where(np.asarray(x) <= xset, s * np.minimum(Mph(x), X), cst)
    return pcs, M3, dict(s=s, xset=xset, xta=xta, xf=xf)
XI, WXI = np.polynomial.legendre.leggauss(64)
def dsig_prof(u, pcs, M3):
    """DeltaSigma in M_b / r_M^2 at u = R / r_M: central point M_b plus the cold layout (cosh substitution, ONE1's form)."""
    u = np.asarray(u, float); Sig = np.zeros_like(u); corr = np.zeros_like(u)
    for a, b, fn in pcs:
        lo = np.maximum(u, a); act = b > lo
        if not act.any(): continue
        uu = u[act]; ta = np.arccosh(np.maximum(lo[act] / uu, 1.0)); tb = np.arccosh(b / uu)
        t = ta[:, None] + (tb - ta)[:, None] * (XI[None, :] + 1) / 2; w = (tb - ta)[:, None] * WXI[None, :] / 2
        x = uu[:, None] * np.cosh(t); d = fn(x)
        Sig[act] += (d / x * w).sum(1) / (2 * math.pi); corr[act] += uu * (d * np.exp(-t) * np.tanh(t) * w).sum(1)
    return (1 + M3(u) + corr) / (math.pi * u * u) - Sig

# KA-G4b: projection of ONE1's halo against ONE1's dsig
uk = np.geomspace(0.1, 1e4, 41); pc, M3, _ = profile("canonical", 10.45, 0.3, math.inf, "ONE1")
kb = float(np.max(np.abs(dsig_prof(uk, pc, M3) / O["dsig"](uk, XP["canonical"]) - 1)))
KA = dict(KA_G4b=dict(max_rel=kb, pass_=bool(kb <= 1e-3)))
P(f"KA-G4b projection of ONE1's halo vs ONE1's dsig, u 0.1-1e4: max rel dev {kb:.1e} -> {'PASS' if kb <= 1e-3 else 'FAIL'}  {tm()}")

LMG = np.round(np.arange(7.0, 13.0001, 0.05), 4); ZG = np.round(np.arange(0.0, 0.8501, 0.05), 4); UT = np.geomspace(0.03, 3e4, 160); LUT = np.log(UT)
DINF_T = np.exp(np.interp(LUT, LUG, np.log(D_INF)))
def table(ft, f, mode="S"):
    T = np.empty((len(LMG), len(ZG), len(UT))); S = np.empty((len(LMG), len(ZG)))
    if mode == "ONE1":
        pc, M3, _ = profile(ft, 10.0, 0.0, f, "ONE1"); T[:] = (dsig_prof(UT, pc, M3) / DINF_T)[None, None, :]; S[:] = 1.0; return T, S
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            pc, M3, inf = profile(ft, float(lm), float(z), f, mode); T[i, j] = dsig_prof(UT, pc, M3) / DINF_T; S[i, j] = inf["s"]
    return T, S
izf = np.clip((zz1 - ZG[0]) / (ZG[1] - ZG[0]), 0, len(ZG) - 1 - 1e-9); IZ = np.floor(izf).astype(np.int64); WZ = izf - IZ
LGB = np.log(GB1); AR = (np.arange(n1, dtype=np.int64) * len(UT))[:, None, None]
def cells_S(ft, k, T):
    a0 = A0[ft]; imf = np.clip((lMg + math.log10(k) - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1 - 1e-9); IM = np.floor(imf).astype(np.int64); WM = imf - IM
    iuf = np.clip((0.5 * (math.log(a0) - math.log(k) - LGB) - LUT[0]) / (LUT[1] - LUT[0]), 0, len(UT) - 1 - 1e-9); iu = np.floor(iuf).astype(np.int64); wu = iuf - iu
    flat = AR + iu; r = np.zeros_like(GB1)
    for dm_, wm_ in ((0, 1 - WM), (1, WM)):
        for dz_, wz_ in ((0, 1 - WZ), (1, WZ)):
            Tc = T[IM + dm_, IZ + dz_].ravel()
            r += (wm_ * wz_)[:, None, None] * ((1 - wu) * Tc[flat] + wu * Tc[flat + 1])
    fv = glaw(k * GB1, a0) * r
    return np.where(OKC1, (fv * WGL[None, None, :]).sum(-1) / 2, 0.0)
MK = [("KO1", 1.6, "all"), ("KO1", 1.6, "late"), ("KO1", 1.6, "early"), ("KO1R", 1.6, "all"), ("KO1", 1.0, "all")]
def own_S(ft, T):
    out = {mk: np.zeros((len(KGRID), NPAT, 10)) for mk in MK}
    for ik, k in enumerate(KGRID):
        C = WW1 * cells_S(ft, k, T)
        for mk in MK: out[mk][ik] = psum(C, MASKS[mk])
    return out
def nb_sums(ft, net, lams):
    lam_of_k = np.sqrt(KGRID * A0C / A0[ft]); kval = (lam_of_k >= min(lams)) & (lam_of_k <= max(lams)); SNB = {}
    for mk in MK:
        cs = CubicSpline(np.log(lams), np.stack([psum(WW1 * net[il], MASKS[mk]) for il in range(len(lams))]), axis=0)
        SNB[mk] = np.stack([KGRID[ik] * cs(math.log(min(max(lam_of_k[ik], min(lams)), max(lams)))) for ik in range(len(KGRID))])
    return SNB, kval
def gate_of(res):
    """ONE1's frozen gate (copied): res[mk] = fit dict with neighbours."""
    if any(res.get(mk) is None for mk in MK[:3]): return dict(status="NOT EVALUABLE", lines={}, failing=["no k crossing"])
    g = {}
    for sub in ("all", "late", "early"):
        q = res[("KO1", 1.6, sub)]; g[f"G-K1 {sub}"] = dict(diff=q["diff"], sigma=q["s_diff"], z=q["z"], ok=bool(abs(q["diff"]) <= 2 * q["s_diff"]))
    qa = res[("KO1", 1.6, "all")]; g["G-K2 all profile"] = dict(chi2=qa["chi2"], line=9.49, ok=bool(qa["chi2"] <= 9.49))
    qe, ql = res[("KO1", 1.6, "early")], res[("KO1", 1.6, "late")]; dd = qe["diff"] - ql["diff"]; sd = jk(qe["diff_l"] - ql["diff_l"])
    g["G-K3 type difference"] = dict(diff=dd, sigma=sd, z=dd / sd, ok=bool(abs(dd) <= 2 * sd))
    return dict(status="PASS" if all(v["ok"] for v in g.values()) else "FAIL", lines=g, failing=[k for k, v in g.items() if not v["ok"]])
def slim(q):
    return None if q is None else {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in q.items() if k not in ("diff_l", "k_l")}

# ---------------- pooled pointwise reading (PD1's P2-KiDS line; QX5's loader, copied)
PCm, Gpc = 3.0857e16, 4.52e-30; POOL = []
for i, lm in enumerate([9.4, 10.45, 10.7, 10.9], 1):
    a = np.loadtxt(os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar", f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
    for gb, go in zip(a[:, 0], 4 * Gpc * a[:, 1] / a[:, 4] * PCm):
        if go > 0: POOL.append((float(gb), lm))
def pooled(ft, f, mode="S", z=0.31):
    sh = []
    for gb, lm in POOL:
        pc, M3, inf = profile(ft, lm, z, f, mode); rM = halo(ft, lm, z)[4]; R = math.sqrt(G * 10 ** lm * Msun / gb)
        sh.append(math.log10(G * 10 ** lm * Msun * (1 + float(M3(R / rM))) / R ** 2 / float(glaw(gb, A0[ft]))))
    sh = np.array(sh); return dict(n=len(sh), n_over=int(np.sum(np.abs(sh) > 0.05)), worst=float(sh[np.argmax(np.abs(sh))]), mean=float(sh.mean()), line=bool(np.all(np.abs(sh) <= 0.05)))
k4c = {ft: pooled(ft, math.inf, "ONE1") for ft in FOOT}
ref4c = {"canonical": (20, -0.635), "alt": (24, -0.675)}
KA["KA_4c"] = dict(rows=k4c, pass_=bool(all(abs(k4c[ft]["n_over"] - ref4c[ft][0]) <= 1 and abs(k4c[ft]["worst"] - ref4c[ft][1]) <= 0.01 for ft in FOOT)))
P(f"KA-4c pooled, law to R_t: " + "; ".join(f"{ft} {k4c[ft]['n_over']}/59 over, worst {k4c[ft]['worst']:+.3f} (PD1 {ref4c[ft][0]}, {ref4c[ft][1]})" for ft in FOOT) + f" -> {'PASS' if KA['KA_4c']['pass_'] else 'FAIL'}  {tm()}")

# ---------------- runs, checkpointed
PART = os.path.join(HERE, "srh1_lens_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cfg={}, KA_G4a={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
FGRID = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50, 2.00]
for ft in FOOT:
    X = XP[ft]
    # KA-G4a: ONE1's primary exactly as ONE1 ran it
    lams = O["lam_grid"](X, extra=[1.0, math.sqrt(A0C / A0["alt"])])
    if ft not in RES["KA_G4a"]:
        with contextlib.redirect_stdout(io.StringIO()):
            res1, NB1 = O["graded_set"](X, lams, O["Htab_of"](X), foots=(ft,))
        g1 = gate_of({mk: res1[ft][mk]["nb"] for mk in MK}); st = STORED["readings"]["primary"]
        dev = max(abs(res1[ft][("KO1", 1.6, sub)]["nb"]["Rs_model"] / st[f"{ft}|KO1|1.6|{sub}"]["nb"]["Rs_model"] - 1) for sub in ("all", "late", "early"))
        RES["KA_G4a"][ft] = dict(Rs_model={sub: res1[ft][("KO1", 1.6, sub)]["nb"]["Rs_model"] for sub in ("all", "late", "early")},
                                 z={sub: res1[ft][("KO1", 1.6, sub)]["nb"]["z"] for sub in ("all", "late", "early")}, status=g1["status"],
                                 stored_status=STORED["gate"][ft]["status"], max_rel=dev, lams=list(map(float, lams)),
                                 pass_=bool(dev <= 1e-6 and g1["status"] == STORED["gate"][ft]["status"])); save()
    ka = RES["KA_G4a"][ft]
    P(f"[{ft}] KA-G4a ONE1 rerun: model R_s all/late/early " + " / ".join(f"{ka['Rs_model'][s]:.4f}" for s in ("all", "late", "early"))
      + f", z " + " / ".join(f"{ka['z'][s]:+.2f}" for s in ("all", "late", "early")) + f", gate {ka['status']} (stored {ka['stored_status']}); max rel dev {ka['max_rel']:.1e} -> {'PASS' if ka['pass_'] else 'FAIL'}  {tm()}")
    # the 9-node neighbour grid, used for every configuration below
    lams9 = sorted(set([0.65] + list(map(float, lams)) + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9)
    P(f"[{ft}] neighbour grid lambda {np.round(lams9, 3).tolist()}: {npr:,} pairs  {tm()}")
    cfgs = [("ONE1_halo", math.inf, "ONE1"), ("f0", 0.0, "S"), ("finf", math.inf, "S")] + [(f"f{f:.2f}", f, "S") for f in FGRID]
    if ft == "canonical": cfgs.append(("MU4_cut_f0.50", 0.5, "cut"))
    for name, f, mode in cfgs:
        key = f"{ft}|{name}"
        if key in RES["cfg"]: continue
        T, S = table(ft, f, mode); OS = own_S(ft, T)
        rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; r0 = {mk: fit(mk, ft, OS[mk]) for mk in MK}
        gt = gate_of(rn); sel = (LMG >= 9.5) & (LMG <= 11.5); zs = (ZG >= 0.15) & (ZG <= 0.45); ss = S[np.ix_(sel, zs)]
        RES["cfg"][key] = dict(f=f, mode=mode, gate=gt, nb={"|".join(map(str, mk)): slim(rn[mk]) for mk in MK}, no_nb={"|".join(map(str, mk)): slim(r0[mk]) for mk in MK},
                               s_lens=[float(np.median(ss)), float(ss.min()), float(ss.max())], pooled=pooled(ft, f, mode))
        save()
        q = RES["cfg"][key]["nb"]; q0 = RES["cfg"][key]["no_nb"]
        def fm(mk):
            a = q["|".join(map(str, mk))]; b = q0["|".join(map(str, mk))]
            return "None" if a is None else f"{a['Rs_model']:.3f} (no nb {b['Rs_model'] if b is None else round(b['Rs_model'], 3)}) k {a['k']:.2f} z {a['z']:+.2f}"
        P(f"[{ft}] {name:14s} 1.6 R_h model R_s all {fm(MK[0])} | late {fm(MK[1])} | early {fm(MK[2])} | chi2 {q['KO1|1.6|all']['chi2'] if q['KO1|1.6|all'] else float('nan'):.2f}"
          f" | gate {gt['status']} {gt['failing']} | s (lenses) {RES['cfg'][key]['s_lens'][0]:.3f} [{RES['cfg'][key]['s_lens'][1]:.3f}, {RES['cfg'][key]['s_lens'][2]:.3f}]"
          f" | pooled {RES['cfg'][key]['pooled']['n_over']}/59 over, worst {RES['cfg'][key]['pooled']['worst']:+.3f}  {tm()}")
# KA-G4c and MU4
kc = {}
for ft in FOOT:
    a = RES["cfg"][f"{ft}|ONE1_halo"]["nb"]; b = RES["KA_G4a"][ft]
    kc[ft] = max(max(abs(a[f"KO1|1.6|{s}"]["Rs_model"] - b["Rs_model"][s]) for s in ("all", "late", "early")) / 0.005,
                 max(abs(a[f"KO1|1.6|{s}"]["z"] - b["z"][s]) for s in ("all", "late", "early")) / 0.05)
KA["KA_G4c"] = dict(worst_fraction_of_tolerance=kc, pass_=bool(max(kc.values()) <= 1))
KA["KA_G4a"] = dict(pass_=bool(all(RES["KA_G4a"][ft]["pass_"] for ft in FOOT)))
P(f"KA-G4c ONE1's halo through this pipeline vs KA-G4a (fraction of tolerance, 1 = at the line): {kc} -> {'PASS' if KA['KA_G4c']['pass_'] else 'FAIL'}")
a = RES["cfg"]["canonical|MU4_cut_f0.50"]["nb"]["KO1|1.6|all"]; b = RES["cfg"]["canonical|f0.50"]["nb"]["KO1|1.6|all"]
mu4 = dict(Rs_cut=None if a is None else a["Rs_model"], Rs_f05=None if b is None else b["Rs_model"], bites=bool(a is not None and b is not None and abs(a["Rs_model"] - b["Rs_model"]) >= 0.10))
P(f"MU4 (reference outside R_set removed, f 0.5, canonical): model R_s {mu4['Rs_cut']} vs {mu4['Rs_f05']} -> {'bites' if mu4['bites'] else 'DOES NOT BITE'}")
G4 = {ft: {f"{f:.2f}": RES["cfg"][f"{ft}|f{f:.2f}"]["gate"]["status"] for f in FGRID} for ft in FOOT}
for ft in FOOT: P(f"[{ft}] G4 status per f: {G4[ft]}; f 0: {RES['cfg'][ft + '|f0']['gate']['status']}; f inf: {RES['cfg'][ft + '|finf']['gate']['status']}; ONE1 halo: {RES['cfg'][ft + '|ONE1_halo']['gate']['status']}")
RES.update(lane="SRH1", part="G4", criteria="5ed8a37ec6", KA=KA, MU4=mu4, G4=G4, f_grid=FGRID, seconds=time.time() - T0, note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
json.dump(RES, open(os.path.join(HERE, "srh1_lens.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srh1_lens.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
os.remove(PART); P(f"done {tm()}")
