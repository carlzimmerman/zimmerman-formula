#!/usr/bin/env python3
"""CFG648 gates (FROZEN_CRITERIA.md, 2e9dffba1): phase-mixed settling H-SP, both sources (B all-baryon, H-CB condensed), both footings.

T1 SPARC (CFG487 harness as CFG645 T1 runs it), T2 Tian+26 groups, T3 X-COP (+ inner band) and T4 Bullet are CFG634's committed code
executed from its source text with ONE patch per function (as CFG637 / CFG645): res == "RSP" cuts the settled phantom at the system's
derived H-SP settled edge r_set (held at M_ph(r_set) beyond it) and adds the derived reservoir M_res(<r) (cfg648_profiles.npz, gate
units). T5 KiDS: ESD ratios H-SP / B from the solver's final mass profiles in CFG700's K-in / K9 bands, and the age-split bound.
T6 (CONTEXT ONLY): CFG556 halo model (B) and CFG634's frame_hcb (H-CB) executed from source with the settled edge moved inward.
MUTATE (CFG648_MUTATE=1, *_MUTATE outputs): M-ta, the RD branch with CFG637's own profiles reproduces CFG637's gate JSON, H-SP off
reproduces candidate B's T1 rms (CFG624) and CFG556's primary R(k).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG648_phase_mixed_settling/cfg648_gates.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D634 = os.path.join(LANES, "CFG634_condensed_baryon_source"); D637 = os.path.join(LANES, "CFG637_derived_reservoir")
sys.path.insert(0, HERE)
try:
    os.nice(10)
except OSError:
    pass
import cfg648_lib as SPL                                                     # noqa: E402
MUTATE = os.environ.get("CFG648_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK = [], {}
RES = {"lane": "CFG648", "script": "cfg648_gates", "criteria": "2e9dffba1", "mutate": MUTATE}
FOOTS = ("canonical", "alt")
PROF = dict(np.load(os.path.join(HERE, "cfg648_profiles.npz")))
DER = json.load(open(os.path.join(HERE, "cfg648_derive_results.json")))
P637 = dict(np.load(os.path.join(D637, "cfg637_profiles.npz"))) if MUTATE else {}
J637 = json.load(open(os.path.join(D637, "cfg637_gates_results.json")))
SRC_TAG = {"cond": "HCB", "all": "B"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


def patch(src, old, new):
    assert src.count(old) == 1, old[:70]
    return src.replace(old, new)


def sp(prefix):
    """(r_set kpc, r grid kpc, M_res gate units) for one system."""
    return float(PROF[prefix + "|rcut"][0]), PROF[prefix + "|r"], PROF[prefix + "|Mres"]


def rd637(prefix):
    return P637[prefix + "|A|P|r"], P637[prefix + "|A|P|Mres"]


P(__doc__.split("Run from")[0].strip())
S = open(os.path.join(D634, "cfg634_static.py")).read()
hdr = S[:S.index("P(__doc__.split")]
NS = dict(__file__=os.path.join(D634, "cfg634_static.py"), __name__="cfg634_static_ro", __doc__="")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(hdr, "cfg634_static_hdr", "exec"), NS)
NS["P"], NS["check"] = (lambda *a: None), (lambda *a, **k: None)
C4, C7, LB = NS["C4"], NS["C7"], NS["LB"]
J634 = json.load(open(os.path.join(D634, "cfg634_static_results.json")))
GSI, MSI, KPC = C4.G_SI, C4.MSUN, C4.KPC

# ===================================================================================================== T1 SPARC
P("\n== T1 SPARC (CFG487 harness executed read-only, as CFG645 T1; B source = H-CB for SPARC)")
src = open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")).read()
m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
m1 = "SPA = {}"
NSS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
           LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NSS)
gb4, ok4, rms, Rm, GI, GMB, GPRED = (NSS[k] for k in ("gb4", "ok4", "rms", "Rm", "GI", "GMB", "GPRED"))
J624 = json.load(open(os.path.join(LANES, "CFG624_no_cold_energy", "cfg624_static_results.json")))
rB = {f: J624["G1"]["rows"][f]["rms_B_census"] for f in FOOTS}


def sparc(foot, hsp=True):
    gp = GPRED[foot].copy()
    if not hsp:
        return rms(gp), 0.0, 0
    worst = 0.0; ncut = 0
    for i, Mb in GMB.items():
        sel = np.where((GI == i) & ok4)[0]
        key = f"S|{i}|{foot}"
        if not len(sel) or key + "|rcut" not in PROF:
            continue
        sel = sel[np.argsort(Rm[sel])]; rr = Rm[sel]
        Mph = np.maximum(gp[sel] - gb4[sel], 0.0) * rr ** 2 / GSI
        rcut, rg, Mres = sp(key)
        rk = rr / KPC
        if rcut < rk[-1]:
            ncut += 1
            Mph = np.where(rk > rcut, np.interp(rcut, rk, Mph), Mph)
        add = np.interp(rk, rg, Mres) * MSI
        worst = max(worst, float(add[-1] / max(Mph[-1], 1e-300)))
        gp[sel] = gb4[sel] + GSI * (Mph + add) / rr ** 2
    return rms(gp), worst, ncut


T1 = {}
for f in FOOTS:
    r_, w, nc = sparc(f)
    T1[f] = dict(rms=r_, rms_B=rB[f], d_rms=r_ - rB[f], max_res_over_phantom_Rlast=w, n_cut_inside_data=nc)
    P(f"  [{f}] rms H-SP {r_:.5f} vs B {rB[f]:.5f} (d {r_ - rB[f]:+.5f}); galaxies with r_set inside the data {nc}; "
      f"largest reservoir / phantom at R_last {w:.3f}")
lab1 = "PASS" if all(T1[f]["rms"] <= 0.12 and abs(T1[f]["d_rms"]) <= 0.005 for f in FOOTS) else \
    ("FAIL" if any(T1[f]["rms"] > 0.15 for f in FOOTS) else "TENSION")
P(f"  T1 label: {lab1}")
RES["T1"] = dict(rows=T1, label=lab1)
if MUTATE:
    d = max(abs(sparc(f, hsp=False)[0] - rB[f]) for f in FOOTS)
    check("M-ta T1: H-SP off reproduces CFG624's B rms (1e-9)", d <= 1e-9, f"max abs diff {d:.1e}")

# ===================================================================================================== T2 / T3 (CFG634 source)
t2 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cfg543_group_supply"):S.index("J543 = json.load")]
t3 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cluster_audit"):S.index("T3 = {}\nCELLS3")]
t2 = patch(t2, '''    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''', '''    if res == "RSP":                                                      # CFG648: H-SP settled edge (patch 1/2)
        rset_, rr_, MM_ = SP_GROUP(o, src)
        mph = np.where(rk > rset_, np.interp(rset_, rk, mph), mph)
    if res == "R0":
        cold = mph
    elif res == "RSP":                                                    # CFG648: derived reservoir (patch 2/2)
        cold = mph + np.interp(rk, rr_, MM_, left=0.0, right=MM_[-1])
    elif res == "RD":                                                     # CFG637's branch (M-ta)
        rr_, MM_ = RD_GROUP(o, src)
        cold = mph + np.interp(rk, rr_, MM_, left=0.0, right=MM_[-1])
    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''')
t3 = patch(t3, '''    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''', '''    if res == "R0":
        cold = mph
    elif res == "RSP":                                                    # CFG648: H-SP settled edge + derived reservoir
        rset_, mcut_, rr_, MM_ = SP_XCOP(foot, name, src, a0)
        cold = (min(mph, mcut_) if r_kpc > rset_ else mph) + float(np.interp(r_kpc, rr_, MM_, left=0.0, right=MM_[-1])) * C4.MSUN
    elif res == "RD":                                                     # CFG637's branch (M-ta)
        rr_, MM_ = RD_XCOP(foot, name, src)
        cold = mph + float(np.interp(r_kpc, rr_, MM_, left=0.0, right=MM_[-1])) * C4.MSUN
    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''')
XCD = {}


def SP_GROUP(o, src):
    return sp(f"G|{o['id']}|{NS['_FOOT_NOW']}|{SRC_TAG[src]}")


def RD_GROUP(o, src):
    return rd637(f"G|{o['id']}|{NS['_FOOT_NOW']}|{SRC_TAG[src]}")


def SP_XCOP(foot, name, src, a0):
    rset, rg, Mres = sp(f"X|{name}|{foot}|{SRC_TAG[src]}")
    k = (foot, name, src)
    if k not in XCD:
        # phantom at r_set from the cluster's own audit profile (CFG637 XCORE construction; gas + stars, or stars for H-CB)
        c = NS["CL"][NS["NAMES"].index(name)]
        gas = NS["loglin_extrap"](rset, c["rg"], c["mg"])
        i = NS["NAMES"].index(name)
        lr = np.log(np.r_[NS["CA"].RADII, NS["R200"][name]])
        rat = np.r_[NS["STARS"][i] / NS["GAS"][i], NS["S200"][name] / NS["G200"][name]]; okr = np.isfinite(rat) & (rat > 0)
        stars = gas * float(np.interp(np.log(rset), lr[okr], rat[okr]))
        Ms = (gas + stars if src == "all" else stars) * C4.MSUN
        r = rset * C4.KPC
        XCD[k] = (C4.nu_mono(C4.G_SI * Ms / r ** 2 / a0) - 1.0) * Ms
    return rset, XCD[k], rg, Mres


def RD_XCOP(foot, name, src):
    return rd637(f"X|{name}|{foot}|{SRC_TAG[src]}")


NS.update(SP_GROUP=SP_GROUP, RD_GROUP=RD_GROUP, SP_XCOP=SP_XCOP, RD_XCOP=RD_XCOP)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t2, "cfg634_static_T2", "exec"), NS)
    exec(compile(t3, "cfg634_static_T3", "exec"), NS)
def t3c(foot, src, res, **kw):                 # cl_model's own local a0 = C4.A0[foot] is used by the RSP branch
    return NS["t3_cell"](foot, src, res, **kw)


P("\n== T2 Tian+26 groups (CFG634 sigma_hcb; RSP = H-SP)")
T2 = {}
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    a0 = NS["C540"].FOOT[fk]; NS["_FOOT_NOW"] = foot
    T2[foot] = {}
    for srcm in ("all", "cond"):
        if MUTATE:
            st = NS["run_groups"](a0, src=srcm, res="RD"); st.pop("Delta", None)
            ref = J637["T2"][foot][f"{SRC_TAG[srcm]}|RD|P|phase"]
            T2[foot][SRC_TAG[srcm] + "|RD"] = dict(st, dmean=abs(st["mean"] - ref["mean"]), dZ=abs(st["Z"] - ref["Z"]))
        st = NS["run_groups"](a0, src=srcm, res="RSP"); st.pop("Delta", None)
        T2[foot][SRC_TAG[srcm]] = st
        P(f"  [{foot}] {SRC_TAG[srcm]:3s} mean {st['mean']:+.4f}  Z {st['Z']:+.2f}  -> {st['label']}   (CFG637 RD: {J637['T2'][foot][SRC_TAG[srcm] + '|RD|P|phase']['mean']:+.4f}, {J637['T2'][foot][SRC_TAG[srcm] + '|RD|P|phase']['label']})")
RES["T2"] = T2
if MUTATE:
    d = max(max(T2[f][k]["dmean"], T2[f][k]["dZ"]) for f in FOOTS for k in ("B|RD", "HCB|RD"))
    check("M-ta T2: RD with CFG637's profiles reproduces CFG637 (mean, Z; 1e-9)", d <= 1e-9, f"max abs diff {d:.1e}")

P("\n== T3 X-COP (CFG634 cl_model / t3_cell; RSP = H-SP)")
T3 = {}
for srcm in ("all", "cond"):
    tag = SRC_TAG[srcm]
    head = {f: t3c(f, srcm, "RSP") for f in FOOTS}
    inner = {f: t3c(f, srcm, "RSP", band=(200, 420)) for f in FOOTS}
    T3[tag] = dict(headline=head, label=NS["t3_label"](list(head.values())), inner_200_420=inner, inner_label=NS["t3_label"](list(inner.values())))
    ref = J637["T3"][f"{tag}|RD|P|phase"]
    P(f"  {tag:3s} eta headline " + " / ".join(f"{head[f]['eta_median']:.3f}+-{head[f]['sigma']:.3f}" for f in FOOTS) + f" -> {T3[tag]['label']:8s}"
      + " | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.3f}" for f in FOOTS) + f" ({T3[tag]['inner_label']})"
      + f"   [CFG637 RD: {ref['headline']['canonical']['eta_median']:.3f}/{ref['headline']['alt']['eta_median']:.3f} {ref['label']}, inner "
      f"{ref['inner_200_420']['canonical']['eta_median']:.3f}/{ref['inner_200_420']['alt']['eta_median']:.3f}]")
    if MUTATE:
        dd = 0.0
        for f in FOOTS:
            a = t3c(f, srcm, "RD"); b = t3c(f, srcm, "RD", band=(200, 420))
            dd = max(dd, abs(a["eta_median"] - ref["headline"][f]["eta_median"]), abs(a["sigma"] - ref["headline"][f]["sigma"]),
                     abs(b["eta_median"] - ref["inner_200_420"][f]["eta_median"]))
        T3[tag]["M_ta_diff"] = dd
RES["T3"] = T3
if MUTATE:
    d = max(T3[t]["M_ta_diff"] for t in ("B", "HCB"))
    check("M-ta T3: RD with CFG637's profiles reproduces CFG637 (headline eta, sigma, inner band; 1e-9)", d <= 1e-9, f"max abs diff {d:.1e}")

# ===================================================================================================== T4 Bullet
P("\n== T4 Bullet (CFG634 code; RSP = H-SP)")
SB = open(os.path.join(D634, "cfg634_bullet.py")).read()
bh = SB[:SB.index("P(__doc__.split")]
bb = SB[SB.index("J4 = json.load(open(os.path.join(LANES, \"CFG4_clusters_results.json\")))"):SB.index("# (a) invariance")]
bb = patch(bb, '''    supply = COLD * p.Mb; Mu = max(supply - Mt, 0.0)''', '''    if res in ("RD", "RSP"):                                              # CFG637 RD (M-ta) / CFG648 RSP (only patch)
        if res == "RSP":
            rset_, rr_, MM_ = SP_BULLET(p, src)
            Mt = float(np.interp(min(rset_, p.rt), r, Mset)) if rset_ < p.rt else Mt
            rho_set = np.where(r <= rset_, rho_set, 0.0)
        else:
            rr_, MM_ = RD_BULLET(p, src)
        Mr_ = np.interp(r, rr_, MM_, left=0.0, right=MM_[-1])
        rho_r = np.maximum(np.gradient(Mr_, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2), 0.0)
        return rho_set, rho_r, Mt, float(Mr_[-1])
    supply = COLD * p.Mb; Mu = max(supply - Mt, 0.0)''')
NB = dict(__file__=os.path.join(D634, "cfg634_bullet.py"), __name__="cfg634_bullet_ro", __doc__="")


def _ft(p):
    return "can" if abs(p.a0 - NB["L625"].A0["can"]) < 1e-9 * p.a0 else "alt"


def SP_BULLET(p, src):
    return sp(f"BU|{p.variant}_{p.role}|{_ft(p)}|{SRC_TAG[src]}")


def RD_BULLET(p, src):
    return rd637(f"BU|{p.variant}_{p.role}|{_ft(p)}|{SRC_TAG[src]}")


NB.update(SP_BULLET=SP_BULLET, RD_BULLET=RD_BULLET)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bh, "cfg634_bullet_hdr", "exec"), NB)
NB["P"], NB["check"] = (lambda *a: None), (lambda *a, **k: None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bb, "cfg634_bullet_body", "exec"), NB)
L625, TAB, POS, SIGCR, AP, DK_OBS = NB["L625"], NB["TAB"], NB["POS"], NB["SIGCR"], NB["AP"], NB["DK_OBS"]
PRO = {}
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        PRO[(var, ft, "main")] = L625.Progenitor625(1.5e15, ft, cloud=False, variant=var)
        PRO[(var, ft, "sub")] = L625.Progenitor625(1.5e14, ft, cloud=True, variant=var)


def t4_cell(var, ft, srcm, res):        # CFG637's t4_cell (CFG634's loop body), verbatim in substance
    comp = {}
    for role in ("main", "sub"):
        p = PRO[(var, ft, role)]
        rs_, rr_, Mt, Mu = NB["dark_components"](p, srcm, res)
        comp[role] = dict(p=p, rho_d=rs_ + rr_, Mset=Mt, Mres=Mu)
    SD = {role: NB["sigma_of"](comp[role]["p"].r, comp[role]["rho_d"]) for role in comp}
    cen = {"main": POS["Main cluster BCG"], "sub": POS["Subcluster BCG"]}
    kap = {}
    for lab in TAB:
        Md = sum(NB["ap_mass"](SD[role], cen[role], POS[lab]) for role in SD)
        kap[lab] = (TAB[lab]["MX"] + TAB[lab]["Ms"] + Md) / (SIGCR * AP)
    dk = {"main": kap["Main cluster BCG"] - kap["Main cluster plasma"], "sub": kap["Subcluster BCG"] - kap["Subcluster plasma"]}
    zz = {g: (dk[g] - DK_OBS[g][0]) / DK_OBS[g][1] for g in dk}
    core = {}
    for role in ("main", "sub"):
        p = comp[role]["p"]
        bar = p.rho_g + p.rho_cc + p.rho_s
        tot = L625.proj_mass(p.r, bar, 250.0) + L625.proj_mass(p.r, comp[role]["rho_d"], 250.0)
        core[role] = dict(proj250=tot, ratio_P16=tot / L625.P16_M250[role][0], Mset=comp[role]["Mset"], Mres=comp[role]["Mres"])
    lab_b = "PASS" if all(abs(zz[g]) <= 2 and dk[g] > 0 for g in dk) else ("FAIL" if any(abs(zz[g]) >= 3 for g in dk) else "TENSION")
    return dict(dkappa=dk, z=zz, label=lab_b, core=core)


T4 = {}
mr4 = 0.0
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        for srcm in ("all", "cond"):
            c = t4_cell(var, ft, srcm, "RSP"); T4[f"{var}|{ft}|{SRC_TAG[srcm]}"] = c
            ref = J637["T4"][f"{var}|{ft}|{SRC_TAG[srcm]}|RD|P|phase"]
            if MUTATE:
                c0 = t4_cell(var, ft, srcm, "RD")
                for g in ("main", "sub"):
                    mr4 = max(mr4, abs(c0["dkappa"][g] - ref["dkappa"][g]), abs(c0["core"][g]["ratio_P16"] - ref["core"][g]["ratio_P16"]))
            P(f"  {var}|{ft}|{SRC_TAG[srcm]:3s} dkappa main {c['dkappa']['main']:+.3f} (z {c['z']['main']:+.2f}), sub {c['dkappa']['sub']:+.3f} (z {c['z']['sub']:+.2f}) -> {c['label']:7s}"
              f" | M(<250)/P16 main {c['core']['main']['ratio_P16']:.2f}, sub {c['core']['sub']['ratio_P16']:.2f} | settled main {c['core']['main']['Mset']:.2e}, reservoir main {c['core']['main']['Mres']:.2e}"
              f"   [CFG637 RD {ref['label']}: z {ref['z']['main']:+.2f}/{ref['z']['sub']:+.2f}]")
RES["T4"] = T4
if MUTATE:
    check("M-ta T4: RD with CFG637's profiles reproduces CFG637 (dkappa, M250/P16, all variants; 1e-9)", mr4 <= 1e-9, f"max abs diff {mr4:.1e}")
GS = DER["gate_systems"]
b1 = GS["BU|B1_main|can|B"]
tmix = b1["t_peri_apo"]
mstate = (f"H-SP phase-mixing time (pericentre -> first apocentre of the most recent shells, B1 main, B, can) = {tmix:.2f} Gyr, "
          f"vs the scored merger window t - t_peri 0.1-0.6 Gyr (CFG623): {'LONGER' if tmix > 0.6 else 'NOT longer'} -> "
          + ("H-SP predicts NO new settling during the passage (alpha_eff = 0, the only value CFG623 allows), with no constant"
             if tmix > 0.6 else "H-SP does not by itself force alpha_eff = 0"))
P("  merger statement: " + mstate)
RES["T4_merger_statement"] = dict(t_mix_gyr=tmix, text=mstate)

# ===================================================================================================== T5 KiDS
P("\n== T5 KiDS isolated lenses: ESD_HSP / ESD_B in CFG700's bands (solver final mass profiles; excess over mean density)")
edges = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "cfg96_stack.npz"))["gbar_edges"]
gc = np.sqrt(edges[:-1] * edges[1:])
BANDS = {"K9": list(range(6, 15)), "K-in": [12, 13, 14]}
KI = DER["KiDS"]
T5 = {}


def esd_key(key, Mg):
    R = np.sqrt(GSI * Mg * MSI / gc) / KPC
    return R, SPL.esd(PROF[key + "|r"], PROF[key + "|Mtot"], 1.0, R)


for foot in FOOTS:
    T5[foot] = {}
    for pc in (5, 50, 95):
        Mg = 10 ** KI[f"K|p{pc}|{foot}|SP"]["logMgal"]
        R, eS = esd_key(f"K|p{pc}|{foot}|SP", Mg); _, eB = esd_key(f"K|p{pc}|{foot}|B", Mg)
        d = {b: float(eS[ks].sum() / eB[ks].sum() - 1) for b, ks in BANDS.items()}
        T5[foot][f"p{pc}"] = dict(logMgal=math.log10(Mg), R_Kin_kpc=[float(R[14]), float(R[12])], R_K9_kpc=[float(R[14]), float(R[6])],
                                  delta_in=d["K-in"], delta_9=d["K9"])
        P(f"  [{foot}] p{pc} log M_gal {math.log10(Mg):.2f}: K-in R {R[14]:.0f}-{R[12]:.0f} kpc, delta_in {d['K-in']:+.4f}; K9 R {R[14]:.0f}-{R[6]:.0f} kpc, delta_9 {d['K9']:+.4f}")
din = [T5[f][k]["delta_in"] for f in FOOTS for k in T5[f]]
lab5 = "HELPS" if all(v >= 0.05 for v in din) else ("WORSENS" if all(v <= -0.05 for v in din) else
                                                   ("WORSENS (some masses)" if any(v <= -0.05 for v in din) else "UNCHANGED (= record FAIL)"))
P(f"  T5 label (K-in, all masses, both footings): {lab5}")
AGE = {}
for foot in FOOTS:
    Mg = 10 ** KI[f"K|p50|{foot}|SP"]["logMgal"]
    rows = []
    for eps in (0.3, 0.5, 0.75, 1.0, 1.5, 2.5):
        key = f"K|p50|{foot}|SPeps{eps}"
        R, e = esd_key(key, Mg)
        rows.append(dict(eps=eps, gamma=KI[key]["gamma"], esd_K9=float(e[BANDS["K9"]].sum()), esd_Kin=float(e[BANDS["K-in"]].sum())))
    lo = min(rows, key=lambda r: r["gamma"]); hi = max(rows, key=lambda r: r["gamma"])
    A = math.log10(lo["esd_K9"] / hi["esd_K9"])
    AGE[foot] = dict(rows=rows, gamma_lo=lo["gamma"], gamma_hi=hi["gamma"], A_max=A,
                     sign="MATCHES (old > young)" if A > 0 else "OPPOSITE",
                     size="CANNOT PRODUCE" if A < 0.024 else ("CAN REACH" if A >= 0.166 else "PARTIAL"))
    P(f"  [{foot}] age bound: Gamma {lo['gamma']:.2f} vs {hi['gamma']:.2f} -> A_HSP,max = log10(ESD_K9 ratio) = {A:+.4f} (observed +0.166 +- 0.071): "
      f"sign {AGE[foot]['sign']}, size {AGE[foot]['size']}")
    P("     eps/Gamma/ESD_K9: " + ", ".join(f"{r['eps']}/{r['gamma']:.2f}/{r['esd_K9']:.3e}" for r in rows))
RES["T5"] = dict(rows=T5, label=lab5, age=AGE)

# ===================================================================================================== T6 growth proxy (CONTEXT ONLY)
P("\n== T6 growth proxy (CONTEXT ONLY): CFG556 halo model (B) / CFG634 frame_hcb (H-CB), settled edge moved inward")
S556 = open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")).read()
pre = S556[:S556.index("# ------------------------------------------------------------------ run")]
NS6 = dict(__file__=os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py"), __name__="cfg556_ro")
CTX6 = dict(mode="off")
T6RUN = DER["T6_runs"]


def s_of(logMta_h, foot, src, which):
    """H-SP settled edge / r_ta interpolated in log M_ta from the T6 solver runs (which: 's' r_sp only, 'x' derived settled edge)."""
    ks = [k for k in T6RUN if k.endswith(f"|{src}|{foot}")]
    lm = np.array([T6RUN[k]["logMta"] for k in ks]); o = np.argsort(lm)
    v = np.array([T6RUN[k]["s_fw" if which == "s" else "x_set_fw"] for k in ks])
    return float(np.interp(logMta_h - math.log10(NS6["h"]), lm[o], v[o]))


with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre, "cfg556_ro", "exec"), NS6)
S634h = open(os.path.join(D634, "cfg634_halo.py")).read()
fn_src = S634h[S634h.index("def cum_parts("):S634h.index("def U_set(fn):")]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(fn_src, "cfg634_halo_fns", "exec"), NS6)
HB, KK, h6 = NS6["HB"], NS6["KK"], NS6["h"]
Ustd = NS6["U_std"](); Pstd = NS6["spectra_std"](Ustd)[0]
Ulta, _ = NS6["U_set"](lambda hb: NS6["frame_profile"](hb, "canonical", mode="lta")); Plta = NS6["spectra_ta"](Ulta)[0]
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))
W8 = NS6["_W8"]


def t6(fn):
    U = np.empty((len(HB), len(KK)))
    for i, hb in enumerate(HB):
        r, Mc = fn(hb); U[i] = NS6["U_of"](r, Mc, KK)
    PF = NS6["spectra_ta"](U)[0]; R = 1 + (PF - Plta) / Pstd
    w8 = W8(KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    s8 = math.sqrt(NS6["s8_of"](Pstd) ** 2 + np.trapz((PF - Plta) * w8, KK)) / NS6["s8_of"](Pstd)
    return dict(R03=float(np.interp(0.3, KK, R)), R1=float(np.interp(1.0, KK, R)), s8_ratio=s8)


def res_shape(hb, foot, src):
    """derived reservoir cumulative shape f_res(r / r_ta) from the nearest T6 solver run (log M_ta)."""
    lmh = math.log10(hb["Mta"] / h6)
    ks = [k for k in T6RUN if k.endswith(f"|{src}|{foot}")]
    kb = min(ks, key=lambda k: abs(T6RUN[k]["logMta"] - lmh))
    pk = f"T6|{kb}|fw"
    r = PROF[pk + "|r"]; M = PROF[pk + "|Mres"]; rta = float(PROF[pk + "|rta"][0])
    return r / rta, M / max(M[-1], 1e-300)


def profile(hb, foot, src, bracket=False):
    """CFG556 (B) / CFG634 frame_hcb (H-CB) profile, executed unmodified; H-SP moves only the SETTLED edge inward:
    M_F = m_b(r) [unchanged baryons] + S(min(r, r_e,HSP)) [settled phantom held beyond the H-SP edge] + remainder x shell(r > r_e,HSP)
    [CFG556's own ML-shaped placement of everything not settled]; mass inside r_ta conserved.  Bracket: the freed cold energy takes
    the solver's derived reservoir shape instead of the shell."""
    if src == "B":
        r, MF, inf = NS6["frame_profile"](hb, foot, edge="cen")
    else:
        r, MF, inf = NS6["frame_hcb"](hb, foot, "cen", "HC1")
    if CTX6["mode"] == "off":
        return r, MF
    re = inf["re"]; Mta = hb["Mta"]
    sfac = 10.0 if CTX6["mode"] == "ident" else s_of(math.log10(Mta), foot, src, CTX6["mode"])
    reh = min(re, sfac * hb["rta"])
    if reh >= re:
        return r, MF
    if src == "B":
        mb = NS6["baryon_cum"](hb, inf["Mb"], r, re)
    else:
        mb = NS6["cum_parts"](hb, inf["Mb"], inf["Mc"], r, inf["reB"])[0]
    Sr = np.where(r <= re, MF - mb, float(np.interp(re, r, MF - mb)))
    Scut = np.interp(np.minimum(r, reh), r, Sr)
    rem = max(Mta - mb[-1] - Scut[-1], 0.0)
    ML = NS6["M_L"](hb, r); MLo = float(np.interp(reh, r, ML))
    sh = np.where(r > reh, np.clip((ML - MLo) / max(Mta - MLo, 1e-300), 0, 1), 0.0)
    MFh = mb + Scut + rem * sh
    if bracket:
        Mmove = max(min((1 - NS6["FB"]) * Mta - Scut[-1], rem), 0.0)
        xs, fr = res_shape(hb, foot, src)
        MFh = MFh - Mmove * sh + Mmove * np.interp(r / hb["rta"], xs, fr, left=0.0, right=1.0)
    return r, MFh


def t6_label(o, base):
    exc0 = base["R1"] - 1; exc = o["R1"] - 1
    if o["R1"] < 0.90:
        return "DEFICIT"
    if exc <= 0.10:
        return "REMOVES"
    if exc0 > 0 and (exc0 - exc) / exc0 >= 0.25:
        return "REDUCES"
    return "UNCHANGED"


T6 = {}
cases = [("B base", "off", False), ("H-SP x_set (derived settled edge)", "x", False), ("H-SP s (r_sp only, literal frozen row)", "s", False),
         ("H-SP x_set + derived reservoir shape (bracket)", "x", True)]
if MUTATE:
    cases = [("M-ta (H-SP off)", "off", False), ("M-ta construction (edge -> 10 r_ta)", "ident", False)]
for foot in FOOTS:
    T6[foot] = {}
    for srcm in ("B", "HCB"):
        for nm, mode, br in cases:
            CTX6["mode"] = mode
            o = t6(lambda hb: profile(hb, foot, srcm, br))
            T6[foot][f"{srcm}|{nm}"] = o
            P(f"  [{foot}] {srcm:3s} {nm:46s} R(k=0.3) {o['R03']:.3f}  R(k=1) {o['R1']:.3f}  sigma8 ratio {o['s8_ratio']:.4f}")
    CTX6["mode"] = "off"
    if MUTATE:
        ref = J556["cases"][f"{foot}|census|cen"]
        o = T6[foot]["B|M-ta (H-SP off)"]; o2 = T6[foot]["B|M-ta construction (edge -> 10 r_ta)"]
        dd = max(abs(o["R1"] - ref["R_at"]["1.0"]), abs(o["R03"] - ref["R_at"]["0.3"]), abs(o2["R1"] - ref["R_at"]["1.0"]), abs(o2["R03"] - ref["R_at"]["0.3"]))
        check(f"M-ta T6 [{foot}] H-SP off reproduces CFG556 primary R(k=0.3), R(k=1) (1e-9)", dd <= 1e-9,
              f"{o['R03']:.9f}/{ref['R_at']['0.3']:.9f}, {o['R1']:.9f}/{ref['R_at']['1.0']:.9f}")
lab6 = {}
if not MUTATE:
    for srcm in ("B", "HCB"):
        for nm, mode, br in cases[1:]:
            labs = {f: t6_label(T6[f][f"{srcm}|{nm}"], T6[f][f"{srcm}|B base"]) for f in FOOTS}
            lab6[f"{srcm}|{nm}"] = labs
            P(f"  T6 {srcm} {nm}: {labs['canonical']} / {labs['alt']}")
RES["T6"] = T6; RES["T6_labels"] = lab6

# ===================================================================================================== verdict
if not MUTATE:
    P("\n== verdict (frozen rule, per source; PRIMARY = eps 1 framework run, derived settled edge)")
    VER = {}
    tol_hits = {}
    for tag in ("B", "HCB"):
        t1 = lab1 == "PASS"
        t2 = all(T2[f][tag]["label"] == "CLOSES" for f in FOOTS)
        t3 = T3[tag]["label"] == "PASS"
        t4 = all(T4[f"B1|{ft}|{tag}"]["label"] == "PASS" for ft in ("can", "alt"))
        t5 = not lab5.startswith("WORSENS")
        t6l = lab6[f"{tag}|H-SP x_set (derived settled edge)"]
        t6 = all(v in ("REMOVES", "REDUCES") for v in t6l.values())
        # inertness vs CFG637 RD (candidate B / H-CB derived)
        r2 = max(abs(T2[f][tag]["mean"] - J637["T2"][f][f"{tag}|RD|P|phase"]["mean"]) for f in FOOTS)
        r3 = max(abs(T3[tag]["headline"][f]["eta_median"] - J637["T3"][f"{tag}|RD|P|phase"]["headline"][f]["eta_median"]) for f in FOOTS)
        r4 = max(abs(T4[f"B1|{ft}|{tag}"]["z"][g] - J637["T4"][f"B1|{ft}|{tag}|RD|P|phase"]["z"][g]) for ft in ("can", "alt") for g in ("main", "sub"))
        r6 = max(abs(T6[f][f"{tag}|H-SP x_set (derived settled edge)"]["R1"] - T6[f][f"{tag}|B base"]["R1"]) /
                 max(T6[f][f"{tag}|B base"]["R1"] - 1, 1e-9) for f in FOOTS)
        r1 = max(abs(T1[f]["d_rms"]) for f in FOOTS)
        inert = r1 <= 0.005 and r2 <= 0.005 and r3 <= 0.01 and r4 <= 0.1 and r6 <= 0.01
        failing = [n for n, ok in (("T1 SPARC", t1), ("T2 groups", t2), ("T3 X-COP headline", t3), ("T4b Bullet B1", t4), ("T5 KiDS (worsens)", t5)) if not ok]
        if t1 and t2 and t3 and t4 and t5 and t6:
            lab = "H-SP KNOB-FREE PASS"
        elif inert:
            lab = "INERT (= candidate B / CFG637 RD; inherits CFG596 / CFG637 fails)"
        else:
            lab = "FAILS " + ", ".join(failing) if failing else "FAILS T6 only (context)"
        VER[tag] = dict(label=lab, T6=t6l, shifts=dict(T1=r1, T2=r2, T3=r3, T4=r4, T6_frac=r6), failing=failing)
        P(f"  [{tag}] {lab}; T6 (context) {t6l['canonical']} / {t6l['alt']}; shifts vs CFG637 RD: T1 {r1:.4f}, T2 {r2:.4f}, T3 {r3:.3f}, T4 z {r4:.2f}, T6 {r6:.2f} of the excess")
    P(f"  age split: {AGE['canonical']['sign']} / {AGE['alt']['sign']}; size {AGE['canonical']['size']} / {AGE['alt']['size']}")
    RES["verdict"] = VER

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"] and c["load_bearing"])
P(f"\n{sum(1 for c in CHK.values() if c['ok'])}/{len(CHK)} checks pass ({nf} load-bearing failures); elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg648_gates_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg648_gates{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
