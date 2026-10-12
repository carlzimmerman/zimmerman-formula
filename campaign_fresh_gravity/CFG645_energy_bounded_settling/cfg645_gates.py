#!/usr/bin/env python3
"""CFG645 gates (FROZEN_CRITERIA.md, 21b7b0857): energy-bounded settling H-EB on candidate B's own source (all baryons) and B's derived
reservoir (CFG637 RD = empty = CFG634 R0), both footings.

Routes: B (capacity inf), EB-R (global rest-energy capacity rho_DE c^2 V_ta, inside-out), EB-L e_V and EB-L e_Phi (local cap
rho_set <= a0^2/(kappa^2 G e)).  T1 SPARC (CFG487 harness as CFG634 T1 executes it), T2 Tian+26 groups, T3 X-COP (+ inner band) and
T4 Bullet are CFG634's committed code executed from its source text with ONE patch per function applying the cap to the settled
phantom (same method as CFG637's gates).  MUTATE (CFG645_MUTATE=1): M-inf reproduces CFG634 / CFG637 B numbers; M0 capacity 0;
Mc EB-L e_Phi cap x 1e-3.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG645_energy_bounded_settling/cfg645_gates.py
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
import cfg645_lib as EB                                                      # noqa: E402
MUTATE = os.environ.get("CFG645_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK = [], {}
RES = {"lane": "CFG645", "script": "cfg645_gates", "criteria": "21b7b0857", "mutate": MUTATE}
FOOTS = ("canonical", "alt")
ROUTES = {"B": ("inf", "Phi", 1.0), "EB-R": ("R", "Phi", 1.0), "EB-L e_V": ("L", "V", 1.0), "EB-L e_Phi": ("L", "Phi", 1.0)}
if MUTATE:
    ROUTES = {"B": ("inf", "Phi", 1.0), "M0 capacity 0": ("zero", "Phi", 1.0), "Mc EB-L e_Phi x1e-3": ("L", "Phi", 1e-3)}
CTX = dict(route="B")
MAXR = {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


def patch(src, old, new):
    assert src.count(old) == 1, old[:70]
    return src.replace(old, new)


def apply_route(r, Mset, Mtot, a0, G, r_ta, outer="kepler"):
    """cap the cumulative settled profile Mset(<r) for the current route; returns (Mset_capped, removed)."""
    mode, em, fac = ROUTES[CTX["route"]]
    if mode == "inf":
        return Mset, np.zeros_like(Mset)
    eV, ePhi = EB.e_profiles(r, Mtot, G, r_ta, outer=outer)
    e = eV if em == "V" else ePhi
    if mode == "L":                                                               # reported diagnostic: closest approach to the cap
        dV = 4 / 3 * math.pi * np.diff(r ** 3); rho = np.diff(Mset) / np.maximum(dV, 1e-300)
        rcap = fac * EB.rho_de_c2(a0, G) / np.maximum(0.5 * (e[1:] + e[:-1]), 1e-300)
        k = (CTX["route"], CTX.get("gate", "?"))
        MAXR[k] = max(MAXR.get(k, 0.0), float(np.max(rho / rcap)))
    C = EB.rho_de_c2(a0, G) * 4 / 3 * math.pi * r_ta ** 3 if mode == "R" else None
    Mc, rem, _ = EB.cap_cum(r, Mset, e, a0, G, fac=fac, mode=mode, C=C)
    return Mc, rem


P(__doc__.split("Run from")[0].strip())
S = open(os.path.join(D634, "cfg634_static.py")).read()
hdr = S[:S.index("P(__doc__.split")]
NS = dict(__file__=os.path.join(D634, "cfg634_static.py"), __name__="cfg634_static_ro", __doc__="")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(hdr, "cfg634_static_hdr", "exec"), NS)
NS["P"], NS["check"] = (lambda *a: None), (lambda *a, **k: None)
C4, C7, LB = NS["C4"], NS["C7"], NS["LB"]
J634 = json.load(open(os.path.join(D634, "cfg634_static_results.json")))
J637 = json.load(open(os.path.join(D637, "cfg637_gates_results.json")))
GSI, MSI, KPC = C4.G_SI, C4.MSUN, C4.KPC
RHO_M_SI = EB.OM * 3 * (67.36e3 / (1e3 * KPC)) ** 2 / (8 * math.pi * GSI)

# ===================================================================================================== T1 SPARC
P("\n== T1 SPARC (CFG487 harness executed read-only, as CFG634 T1)")
src = open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")).read()
m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
m1 = "SPA = {}"
NSS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
           LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NSS)
gb4, go4, ok4, rms, Rm, GI, GMB, RTA_G, GPRED = (NSS[k] for k in ("gb4", "go4", "ok4", "rms", "Rm", "GI", "GMB", "RTA_G", "GPRED"))
NUV = NSS["NUV"]
J624 = json.load(open(os.path.join(LANES, "CFG624_no_cold_energy", "cfg624_static_results.json")))


def sparc_route(foot):
    mode, em, fac = ROUTES[CTX["route"]]
    a0 = C7.A0_SI[foot]
    gp = GPRED[foot].copy()
    if mode == "inf":
        return rms(gp), 0.0
    if mode == "zero":
        return rms(np.where(ok4, gb4, 1.0)), 1.0
    frac = []
    for i, Mb in GMB.items():
        sel = np.where((GI == i) & ok4)[0]
        if not len(sel):
            continue
        sel = sel[np.argsort(Rm[sel])]; rr = Rm[sel]
        Mbar = gb4[sel] * rr ** 2 / GSI; Mph = np.maximum(gp[sel] - gb4[sel], 0.0) * rr ** 2 / GSI; Mtot = gp[sel] * rr ** 2 / GSI
        rta, Ml = RTA_G[foot][i]
        if mode == "R":
            # inside-out global capacity with e_Phi along the data, iso extension to r_ta (upper bracket on the export)
            Mc, rem = apply_route(rr, Mph, Mtot, a0, GSI, rta, outer="iso")
            rin = 0.0
        else:
            rin, _ = EB.point_mass_removed(float(Mbar[0]), a0, GSI, NUV, float(rr[0]), em, r_ta=rta, fac=fac)
            rin = min(rin, float(Mph[0]))
            Mc, rem = apply_route(rr, Mph, Mtot, a0, GSI, rta, outer="iso")
        newM = Mph - rem - rin
        gp[sel] = gb4[sel] + GSI * np.maximum(newM, 0.0) / rr ** 2
        frac.append(float((rem[-1] + rin) / max(Mph[-1], 1e-300)))
    return rms(gp), float(np.max(frac)) if frac else 0.0


T1 = {}
for rt in ROUTES:
    CTX["route"] = rt; T1[rt] = {}; CTX["gate"] = "T1"
    for foot in FOOTS:
        r_, fr = sparc_route(foot)
        T1[rt][foot] = dict(rms=r_, max_removed_frac=fr)
    P(f"  {rt:22s} rms " + " / ".join(f"{T1[rt][f]['rms']:.5f}" for f in FOOTS) + "  max removed fraction of a galaxy's phantom inside R_last "
      + " / ".join(f"{T1[rt][f]['max_removed_frac']:.2e}" for f in FOOTS))
rB = {f: J624["G1"]["rows"][f]["rms_B_census"] for f in FOOTS}
check("M-inf T1: capacity inf reproduces CFG624's B rms (1e-9)", all(abs(T1["B"][f]["rms"] - rB[f]) < 1e-9 for f in FOOTS),
      ", ".join(f"{T1['B'][f]['rms']:.9f}/{rB[f]:.9f}" for f in FOOTS))


def t1_label(rt):
    d = {f: T1[rt][f]["rms"] - T1["B"][f]["rms"] for f in FOOTS}
    if all(T1[rt][f]["rms"] <= 0.12 and abs(d[f]) <= 0.005 for f in FOOTS):
        return "PASS"
    return "FAIL" if any(T1[rt][f]["rms"] > 0.15 for f in FOOTS) else "TENSION"


# ===================================================================================================== T2 groups
P("\n== T2 Tian+26 groups (CFG634 sigma_hcb, src = all, res = R0; one patch: the cap on mph)")
t2 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cfg543_group_supply"):S.index("J543 = json.load")]
t2 = patch(t2, '''    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''', '''    if src == "all":                                                      # CFG645: the capacity (only patch)
        mph = EB_GROUP(r, Mb_r, mph, a0, M)
    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''')


def EB_GROUP(r, Mb_r, mph, a0, M):
    if ROUTES[CTX["route"]][0] == "inf":
        return mph
    Mta = (M / 0.10) * (1 + NS["COLD_G"]) * MSI
    rta = EB.r_ta_of(Mta, RHO_M_SI)
    Mc, _ = apply_route(r, mph * MSI, (Mb_r + mph) * MSI, a0, GSI, rta)
    return Mc / MSI


NS["EB_GROUP"] = EB_GROUP
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t2, "cfg634_static_T2", "exec"), NS)
T2 = {}
for rt in ROUTES:
    CTX["route"] = rt; T2[rt] = {}; CTX["gate"] = "T2"
    for foot, fk in (("canonical", "can"), ("alt", "alt")):
        st = NS["run_groups"](NS["C540"].FOOT[fk], src="all"); st.pop("Delta", None)
        T2[rt][foot] = st
    P(f"  {rt:22s} mean " + " / ".join(f"{T2[rt][f]['mean']:+.4f} (Z {T2[rt][f]['Z']:+.2f}) {T2[rt][f]['label']}" for f in FOOTS))
CTX["route"] = "B"
mr2 = max(max(abs(T2["B"][f]["mean"] - J634["T2"]["rows"][f]["B (all source) R0 [=M1]"]["mean"]),
              abs(T2["B"][f]["Z"] - J634["T2"]["rows"][f]["B (all source) R0 [=M1]"]["Z"]),
              abs(T2["B"][f]["mean"] - J637["T2"][f]["B|RD|P|phase"]["mean"])) for f in FOOTS)
check("M-inf T2: capacity inf reproduces CFG634 B R0 and CFG637 B RD (mean, Z; 1e-9)", mr2 <= 1e-9, f"max abs diff {mr2:.1e}")

# ===================================================================================================== T3 X-COP
P("\n== T3 X-COP (CFG634 cl_model / t3_cell, src = all, res = R0; one patch: subtract the capped-away settled mass)")
t3 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cluster_audit"):S.index("T3 = {}\nCELLS3")]
t3 = patch(t3, '''    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''', '''    if res == "R0":
        cold = mph - (EB_XCOP(foot, name, r_kpc) * C4.MSUN if src == "all" else 0.0)     # CFG645: the capacity (only patch)
    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''')
XC_CACHE = {}


def EB_XCOP(foot, name, r_kpc):
    if ROUTES[CTX["route"]][0] == "inf":
        return 0.0
    key = (CTX["route"], foot, name)
    if key not in XC_CACHE:
        CA = NS["CA"]; i = NS["NAMES"].index(name)
        Mb = (NS["GAS"][i] + NS["STARS"][i]); ok = np.isfinite(Mb) & (Mb > 0)
        rk = CA.RADII[ok]; Mbk = Mb[ok] * MSI; r = rk * KPC; a0 = C4.A0[foot]
        mph = (C4.nu_mono(GSI * Mbk / r ** 2 / a0) - 1.0) * Mbk
        Mta = (NS["G200"][name] + NS["S200"][name]) / 0.90 * (1 + NS["COLD_X"]) * MSI
        rta = EB.r_ta_of(Mta, RHO_M_SI)
        _, rem = apply_route(r, mph, Mbk + mph, a0, GSI, rta, outer="iso")
        XC_CACHE[key] = (rk, rem / MSI)
    rk, rem = XC_CACHE[key]
    return float(np.interp(r_kpc, rk, rem, left=0.0, right=rem[-1]))


NS["EB_XCOP"] = EB_XCOP
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t3, "cfg634_static_T3", "exec"), NS)
T3 = {}
for rt in ROUTES:
    CTX["route"] = rt; CTX["gate"] = "T3"
    head = {f: NS["t3_cell"](f, "all", "R0") for f in FOOTS}
    inner = {f: NS["t3_cell"](f, "all", "R0", band=(200, 420)) for f in FOOTS}
    T3[rt] = dict(headline=head, label=NS["t3_label"](list(head.values())), inner=inner, inner_label=NS["t3_label"](list(inner.values())))
    P(f"  {rt:22s} eta headline " + " / ".join(f"{head[f]['eta_median']:.4f}+-{head[f]['sigma']:.3f}" for f in FOOTS) + f" -> {T3[rt]['label']:8s}"
      + " | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.4f}" for f in FOOTS) + f" ({T3[rt]['inner_label']})")
CTX["route"] = "B"
mr3 = max(max(abs(T3["B"]["headline"][f]["eta_median"] - J634["T3"]["rows"]["B|R0"]["headline"][f]["eta_median"]),
              abs(T3["B"]["inner"][f]["eta_median"] - J634["T3"]["rows"]["B|R0"]["inner_200_420"][f]["eta_median"]),
              abs(T3["B"]["headline"][f]["eta_median"] - J637["T3"]["B|RD|P|phase"]["headline"][f]["eta_median"])) for f in FOOTS)
check("M-inf T3: capacity inf reproduces CFG634 B R0 and CFG637 B RD (headline, inner band; 1e-9)", mr3 <= 1e-9, f"max abs diff {mr3:.1e}")

# ===================================================================================================== T4 Bullet
P("\n== T4 Bullet (CFG634 dark_components, src = all, res = R0; one patch: the cap on rho_set; Paraficz PROVISIONAL)")
SB = open(os.path.join(D634, "cfg634_bullet.py")).read()
bh = SB[:SB.index("P(__doc__.split")]
bb = SB[SB.index("J4 = json.load(open(os.path.join(LANES, \"CFG4_clusters_results.json\")))"):SB.index("# (a) invariance")]
bb = patch(bb, '''        rho_set = p.rho_ph.copy(); Mset = p.Mph.copy(); Mt = p.Mph_tot''', '''        rho_set = p.rho_ph.copy(); Mset = p.Mph.copy(); Mt = p.Mph_tot
        rho_set, Mt = EB_BULLET(p, rho_set, Mt)                            # CFG645: the capacity (only patch)''')
NB = dict(__file__=os.path.join(D634, "cfg634_bullet.py"), __name__="cfg634_bullet_ro", __doc__="")


def EB_BULLET(p, rho_set, Mt):
    if ROUTES[CTX["route"]][0] == "inf":
        return rho_set, Mt
    L625 = NB["L625"]; G = NB["L625"].G if hasattr(NB["L625"], "G") else 4.49850215e-6
    r = p.r; Mset = NB["cumtrapz_sph"](r, rho_set)
    KMS = 1.0227121650537077
    H0 = 67.36e-3 * KMS                                                           # 1/Gyr (km/s/kpc -> kpc/Gyr/kpc)
    rho_m = EB.OM * 3 * H0 ** 2 / (8 * math.pi * G) * (1 + 0.296) ** 3
    rta = EB.r_ta_of(p.Mb * (1 + NB["COLD"]), rho_m)
    Mc, rem = apply_route(np.maximum(r, 1e-9), Mset, p.Mbar + Mset, p.a0, G, rta)
    rho_new = np.maximum(np.gradient(Mc, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2), 0.0)
    rho_new[rho_set <= 0] = 0.0
    return rho_new, float(Mt - rem[-1])


NB["EB_BULLET"] = EB_BULLET
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bh, "cfg634_bullet_hdr", "exec"), NB)
NB["P"], NB["check"] = (lambda *a: None), (lambda *a, **k: None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bb, "cfg634_bullet_body", "exec"), NB)
L625, TAB, POS, SIGCR, AP, DK_OBS = NB["L625"], NB["TAB"], NB["POS"], NB["SIGCR"], NB["AP"], NB["DK_OBS"]
PRO = {}
for var in ("B1", "BASE"):
    for ft in ("can", "alt"):
        PRO[(var, ft, "main")] = L625.Progenitor625(1.5e15, ft, cloud=False, variant=var)
        PRO[(var, ft, "sub")] = L625.Progenitor625(1.5e14, ft, cloud=True, variant=var)


def t4_cell(var, ft, srcm, res):        # CFG637's copy of CFG634's loop body (aperture contrast + core ratio)
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
        core[role] = dict(proj250=tot, ratio_P16=tot / L625.P16_M250[role][0], Mset=comp[role]["Mset"])
    lab_b = "PASS" if all(abs(zz[g]) <= 2 and dk[g] > 0 for g in dk) else ("FAIL" if any(abs(zz[g]) >= 3 for g in dk) else "TENSION")
    return dict(dkappa=dk, z=zz, label=lab_b, core=core)


J634B = json.load(open(os.path.join(D634, "cfg634_bullet_results.json")))
T4 = {}
for rt in ROUTES:
    CTX["route"] = rt; T4[rt] = {}; CTX["gate"] = "T4"
    for ft in ("can", "alt"):
        c = t4_cell("B1", ft, "all", "R0"); T4[rt][ft] = c
        P(f"  {rt:22s} [{ft}] dkappa main {c['dkappa']['main']:+.4f} (z {c['z']['main']:+.2f}), sub {c['dkappa']['sub']:+.4f} (z {c['z']['sub']:+.2f}) -> {c['label']:7s}"
          f" | M(<250)/P16 main {c['core']['main']['ratio_P16']:.3f}, sub {c['core']['sub']['ratio_P16']:.3f} | M_set main {c['core']['main']['Mset']:.3e}")
CTX["route"] = "B"
mr4 = 0.0
for ft in ("can", "alt"):
    ref = J634B["T4"][f"B1|{ft}|B_alpha0|R0"]
    for g in ("main", "sub"):
        mr4 = max(mr4, abs(T4["B"][ft]["dkappa"][g] - ref["dkappa"][g]), abs(T4["B"][ft]["core"][g]["ratio_P16"] - ref["core"][g]["ratio_P16"]))
check("M-inf T4: capacity inf reproduces CFG634 B1 B_alpha0 R0 (dkappa, M250/P16; 1e-9)", mr4 <= 1e-9, f"max abs diff {mr4:.1e}")

# ===================================================================================================== labels + verdict
P("\n== per-route labels (frozen rules) and inertness vs B")
LAB = {}
for rt in ROUTES:
    if rt == "B":
        continue
    l1 = t1_label(rt)
    l2 = "PASS" if all(T2[rt][f]["label"] == "CLOSES" for f in FOOTS) else "FAIL"
    l3, l3i = T3[rt]["label"], T3[rt]["inner_label"]
    l4 = {ft: T4[rt][ft]["label"] for ft in ("can", "alt")}
    inert = dict(
        T1=all(abs(T1[rt][f]["rms"] - T1["B"][f]["rms"]) <= 0.005 for f in FOOTS),
        T2=all(abs(T2[rt][f]["mean"] - T2["B"][f]["mean"]) <= 0.005 for f in FOOTS),
        T3=all(abs(T3[rt]["headline"][f]["eta_median"] - T3["B"]["headline"][f]["eta_median"]) <= 0.01 and
               abs(T3[rt]["inner"][f]["eta_median"] - T3["B"]["inner"][f]["eta_median"]) <= 0.01 for f in FOOTS),
        T4=all(abs(T4[rt][ft]["z"][g] - T4["B"][ft]["z"][g]) <= 0.1 for ft in ("can", "alt") for g in ("main", "sub")))
    LAB[rt] = dict(T1=l1, T2=l2, T3=l3, T3_inner=l3i, T4b=l4, inert=inert)
    P(f"  {rt:22s} T1 {l1} | T2 {l2} | T3 {l3} (inner {l3i}) | T4b {l4['can']}/{l4['alt']} | inert vs B: {inert}")
P("  reported: max rho_set/rho_cap reached anywhere on the gate profiles (EB-L binds only where > 1): "
  + "; ".join(f"{k[0]} {k[1]} {v:.3g}" for k, v in sorted(MAXR.items())))
RES.update(T1=T1, T2=T2, T3=T3, T4=T4, labels=LAB, max_rho_over_cap={f"{k[0]}|{k[1]}": v for k, v in MAXR.items()})

if not MUTATE:
    J5 = json.load(open(os.path.join(HERE, "cfg645_derive_results.json")))
    verdict = {}
    anypass = False
    for rt, lb in LAB.items():
        t6k = rt if rt in J5["T6_labels"] else None
        t6 = J5["T6_labels"][t6k]["labels"] if t6k else {}
        t5w = rt.startswith("EB-L") and any(v.startswith("WORSE") for v in J5["T5"]["label"].values())
        ok = (lb["T1"] == "PASS" and lb["T2"] == "PASS" and lb["T3"] == "PASS" and all(v == "PASS" for v in lb["T4b"].values())
              and not t5w and all(v == "REMOVES" for v in t6.values()))
        anypass |= ok
        if all(lb["inert"].values()) and all(v == "UNCHANGED" for v in t6.values()):
            verdict[rt] = "INERT (= candidate B; inherits CFG596 / CFG637 fails)"
        else:
            fails = [g for g, v in (("T1", lb["T1"] == "PASS"), ("T2", lb["T2"] == "PASS"), ("T3", lb["T3"] == "PASS"),
                                    ("T4b", all(v == "PASS" for v in lb["T4b"].values()))) if not v]
            verdict[rt] = "PASS" if ok else "FAILS " + ", ".join(fails)
        P(f"  VERDICT [{rt}]: {verdict[rt]}  (T6 {t6})")
    verdict["EB-K"] = "BINARY (" + J5["D3"]["note"] + ")"
    verdict["EB-eta"] = "KNOB (" + J5["D4"]["label"] + ")"
    verdict["overall"] = ("H-EB KNOB-FREE PASS" if anypass else
                          "H-EB NOT DERIVABLE KNOB-FREE: every derived capacity is inert (= B) or zero; only a free efficiency (EB-eta) binds where clumping is decided -> KNOB")
    P(f"  VERDICT [EB-K]: {verdict['EB-K']}")
    P(f"  VERDICT [EB-eta]: {verdict['EB-eta']}")
    P(f"  OVERALL: {verdict['overall']}")
    RES["verdict"] = verdict
else:
    m0 = LAB["M0 capacity 0"]; mc = LAB["Mc EB-L e_Phi x1e-3"]
    check("M0: capacity 0 breaks galaxies (T1 rms > 0.15 both footings)", all(T1["M0 capacity 0"][f]["rms"] > 0.15 for f in FOOTS),
          " / ".join(f"{T1['M0 capacity 0'][f]['rms']:.3f}" for f in FOOTS))
    check("M0: capacity 0 -> T2 does not CLOSE", m0["T2"] != "PASS", " / ".join(T2["M0 capacity 0"][f]["label"] for f in FOOTS))
    check("Mc: cap x 1e-3 changes T1, T2 or T3 beyond the inertness tolerance", not (mc["inert"]["T1"] and mc["inert"]["T2"] and mc["inert"]["T3"]),
          str(mc["inert"]))

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"] and c["load_bearing"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg645_gates_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg645_gates{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
