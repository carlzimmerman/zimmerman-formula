#!/usr/bin/env python3
"""CFG634 static gates T1 (SPARC), T2 (Tian+26 groups), T3 (X-COP), T6 (KiDS) for H-CB, the condensed-baryon source
(FROZEN_CRITERIA.md, committed alone in 1fea20013).

H-CB: the law's phantom (settled cold energy) is sourced only by condensed baryons (stars + cold gas); hot X-ray gas gravitates as
Newtonian mass only; unsettled cold energy is a collisionless reservoir (bracketed: R0 / RI / RN, not derived).
Committed pipelines are reused read-only: CFG487 SPARC harness (as CFG624 G1 execs it), CFG543 group machinery, the record's X-COP
audit (cluster_audit.py profiles + results.json rows, as CFG4 / CFG624 read them), KiDS lens catalogue.
MUTATE controls run in the same pass: M1 (hot gas restored to the source -> record candidate-B numbers), M2 (no baryons in the source).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG634_condensed_baryon_source/cfg634_static.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
for d in (LANES, os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG487_settled_fraction_switch"),
          os.path.join(LANES, "CFG543_group_supply"), os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose"),
          os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import CFG4_common as C4                                                     # noqa: E402
import CFG7_common as C7                                                     # noqa: E402
import cfg515_lib as L515                                                    # noqa: E402
import cfg487_lib as LB                                                      # noqa: E402
LOG, CHK, RES = [], {}, {"lane": "CFG634", "script": "cfg634_static", "criteria": "1fea20013"}
FOOTS = ("canonical", "alt")
COLD_G = L515.COLD_PER_B          # CFG543 / CFG515 constant (groups)
COLD_X = 0.1200 / 0.02237         # CFG4 / CFG624 COSMIC constant (X-COP)


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run from")[0].strip())

# ===================================================================================================== T1 SPARC
P("\n== T1 SPARC (CFG487 harness exec'd read-only, exactly as CFG624 G1)")
hdr = open(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC5371_rotmod.dat")).read().splitlines()[1].split()
cols_ok = hdr[1:] == ["Rad", "Vobs", "errV", "Vgas", "Vdisk", "Vbul", "SBdisk", "SBbul"]
nrot = len([f for f in os.listdir(os.path.join(REPO, "real_research", "data", "sparc_data")) if f.endswith("_rotmod.dat")])
check("T1a rotmod columns carry no hot-gas term (Vgas = HI x 1.33, Vdisk, Vbul only)", cols_ok, f"{hdr[1:]} ({nrot} files)")
src = open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")).read()
m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
m1 = "SPA = {}"
assert src.count(m0) == 1 and src.count(m1) == 1
NS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
          LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NS)
gb4, go4, ok4, ww4, rms = NS["gb4"], NS["go4"], NS["ok4"], NS["ww4"], NS["rms"]
J624 = json.load(open(os.path.join(LANES, "CFG624_no_cold_energy", "cfg624_static_results.json")))
T1 = {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]
    gc = np.where(ok4, gb4, 1.0)            # condensed = the whole rotmod baryon field (stars + HI x 1.33)
    gh = np.zeros_like(gc)                   # hot = 0 (no catalogue term)
    def pred(src_g, hot_g):
        s = np.where(src_g > 0, src_g, 1e-300)
        return np.where(src_g > 0, np.asarray(C7.nu_mono(s / a0), float) * s, 0.0) + hot_g + (gc - src_g - hot_g).clip(0)
    r_hcb = rms(pred(gc, gh))
    r_m1 = rms(pred(gc + gh, 0 * gh))       # hot restored to the source (identical here: hot = 0)
    r_m2 = rms(pred(0 * gc, 0 * gh))        # no baryons in the source -> Newtonian baryons (census edge lies beyond R_HI)
    rB = J624["G1"]["rows"][foot]["rms_B_census"]
    T1[foot] = dict(rms_HCB=r_hcb, rms_B_record=rB, d_rms=r_hcb - rB, M1_rms=r_m1, M2_rms=r_m2, npts=int(ok4.sum()))
    P(f"  [{foot}] rms H-CB {r_hcb:.4f} dex; record B (census edge, CFG515/CFG624) {rB:.4f}; d {r_hcb - rB:+.1e}; M1 {r_m1:.4f}; M2 (no source) {r_m2:.4f}")
check("M1-T1 hot restored reproduces CFG624's B rms (1e-9)", all(abs(T1[f]["M1_rms"] - T1[f]["rms_B_record"]) < 1e-9 for f in FOOTS),
      ", ".join(f"{T1[f]['M1_rms']:.9f}/{T1[f]['rms_B_record']:.9f}" for f in FOOTS))
check("M2-T1 no baryons in the source BREAKS galaxies (rms > 0.15)", all(T1[f]["M2_rms"] > 0.15 for f in FOOTS),
      ", ".join(f"{T1[f]['M2_rms']:.3f}" for f in FOOTS))
v1 = "PASS" if all(T1[f]["rms_HCB"] <= 0.12 and abs(T1[f]["d_rms"]) <= 0.005 for f in FOOTS) else (
    "FAIL" if any(T1[f]["rms_HCB"] > 0.15 for f in FOOTS) else "TENSION")
RES["T1"] = dict(rows=T1, rotmod_columns=hdr[1:], verdict=v1); P(f"  T1 verdict: {v1} (a check: hot = 0 in discs, so the source is B's by construction)")

# ===================================================================================================== T2 groups
P("\n== T2 Tian+26 groups (CFG543 machinery imported read-only; P2 containment supply; class-A edge)")
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as G543                                        # noqa: E402
import cfg540_bfjr as C540                                                     # noqa: E402
ROWS = G543.read_groups()
X, LX, RHO_T, M_T, HERN_RE = G543.X, G543.LX, G543.RHO_T, G543.M_T, G543.HERN_RE
Gs, MSUN, KPC = C540.G, C540.MSUN, C540.KPC
RHOC_KPC = 2.77536627e11 * 0.674 ** 2 / 1e9                                    # Msun / kpc^3 (h = 0.674, CFG416's H16)


def bshape(r, rc):
    return r - rc * np.arctan(r / rc)


def m_nfw(x):
    return np.log1p(x) - x / (1 + x)


def sigma_hcb(o, a0, fh=0.08, hshape="H", res="R0", src="cond", k=1.0, dlM=0.0, conc=4.0, edge=True):
    lM = o["lM"] + dlM; M = 10 ** lM
    Re = o["Re"] / k; a = Re * KPC / HERN_RE; r = X * a; rk = r / KPC
    Mc, Mh = (1 - fh) * M, fh * M
    Mc_r = Mc * M_T
    if hshape == "H":
        Mh_r = Mh * M_T
    else:
        Rt = 5 * Re
        Mh_r = Mh * bshape(np.minimum(rk, Rt), Re) / bshape(Rt, Re)
    Mb_r = Mc_r + Mh_r
    Ms = {"cond": Mc_r, "all": Mb_r, "none": 0 * Mb_r}[src]
    gNs = Gs * Ms * MSUN / r ** 2
    mph = np.where(Ms > 0, (C540.nu(np.maximum(gNs, 1e-300) / a0) - 1.0) * Ms, 0.0)
    supply = COLD_G * M / 0.10                                                   # P2 containment (catchment cold energy unchanged)
    if edge:
        kk = np.where(mph >= supply)[0]
        if len(kk):
            mph = np.where(np.arange(len(X)) > kk[0], mph[kk[0]], mph)
    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)
    else:
        Mtot = M / 0.10 + supply
        r200 = (3 * Mtot / (4 * math.pi * 200 * RHOC_KPC)) ** (1 / 3)
        set200 = float(np.interp(r200, rk, mph))
        Mres = max(supply - set200, 0.0)
        cold = mph + Mres * m_nfw(conc * np.minimum(rk, r200) / r200) / m_nfw(conc)
    g = Gs * (Mb_r + cold) * MSUN / r ** 2
    s2 = np.trapezoid(4 * np.pi * X ** 2 * RHO_T * r * g * X, LX) / 3.0 if hasattr(np, "trapezoid") else \
        np.trapz(4 * np.pi * X ** 2 * RHO_T * r * g * X, LX) / 3.0
    return 0.5 * math.log10(s2) - 3.0


def run_groups(a0, **kw):
    lp = np.array([sigma_hcb(o, a0, **kw) for o in ROWS])
    lp2 = np.array([sigma_hcb(o, a0, dlM=0.01, **kw) for o in ROWS])
    s = (lp2 - lp) / 0.01
    D = np.array([o["ls"] for o in ROWS]) - lp
    return G543.stats(D, s)


J543 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))["footings"]
T2 = {}
CELLS = {"PRIMARY R0 hot0.08 H": dict(),
         "hot0.04": dict(fh=0.04), "hot0.16": dict(fh=0.16), "hotshape X": dict(hshape="X"), "Re k=1.563": dict(k=1.563),
         "RN c4": dict(res="RN"), "RN c3": dict(res="RN", conc=3.0), "RN c5": dict(res="RN", conc=5.0), "RI": dict(res="RI"),
         "B (all source) R0 [=M1]": dict(src="all"), "B (all source) RN c4": dict(src="all", res="RN"), "B (all source) RI": dict(src="all", res="RI"),
         "M2 no source R0": dict(src="none")}
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    a0 = C540.FOOT[fk]
    T2[foot] = {}
    for nm, kw in CELLS.items():
        st = run_groups(a0, **kw); st.pop("Delta", None)
        T2[foot][nm] = st
        P(f"  [{foot}] {nm:26s} mean {st['mean']:+.3f}  Z {st['Z']:+.2f}  -> {st['label']}")
check("M1-T2 hot restored to the source reproduces CFG543 P2 (1e-4)",
      all(abs(T2[f]["B (all source) R0 [=M1]"]["mean"] - J543[k]["configs"]["P2"]["mean"]) < 1e-4 for f, k in (("canonical", "can"), ("alt", "alt"))),
      ", ".join(f"{T2[f]['B (all source) R0 [=M1]']['mean']:+.5f}/{J543[k]['configs']['P2']['mean']:+.5f}" for f, k in (("canonical", "can"), ("alt", "alt"))))
check("M2-T2 no baryons in the source does NOT close", all(T2[f]["M2 no source R0"]["label"] != "CLOSES" for f in FOOTS),
      ", ".join(f"{T2[f]['M2 no source R0']['mean']:+.3f} {T2[f]['M2 no source R0']['label']}" for f in FOOTS))
prim2 = {f: T2[f]["PRIMARY R0 hot0.08 H"]["label"] for f in FOOTS}
v2 = "PASS" if all(v == "CLOSES" for v in prim2.values()) else "FAIL"
resdep = [nm for nm in ("RN c4", "RN c3", "RN c5", "RI") if any(T2[f][nm]["label"] != prim2[f] for f in FOOTS)]
hotdep = [nm for nm in ("hot0.04", "hot0.16", "hotshape X") if any(T2[f][nm]["label"] != prim2[f] for f in FOOTS)]
labs2 = ([f"RESERVOIR-DEPENDENT ({', '.join(resdep)} flip it)"] if resdep else []) + ([f"HOT-FRACTION-DEPENDENT ({', '.join(hotdep)})"] if hotdep else [])
RES["T2"] = dict(rows=T2, verdict=v2, labels=labs2)
P(f"  T2 verdict (primary R0): {v2}; labels: {labs2 or ['none']}")

# ===================================================================================================== T3 X-COP
P("\n== T3 X-COP (the record's corrected audit rows; stars/gas split from the audit's own profile code)")
with contextlib.redirect_stdout(io.StringIO()):
    import cluster_audit as CA                                                 # noqa: E402  (read-only; main guarded)
AUD = json.load(open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "results.json")))
A0_AUD = AUD["a0_m_s2"]
CL = [CA.load_cluster(p.name) for p in sorted(CA.DATA.iterdir()) if p.is_dir()]
NAMES = [c["name"] for c in CL]
GAS, STARS, MH = CA.profiles(CL, CA.RADII, False)
FS = STARS / (GAS + STARS)                                                     # condensed share of the audit's baryons at each radius
ETT = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))


def loglin_extrap(x, xp, fp):
    ok = np.isfinite(fp) & (fp > 0) & (xp > 0)
    xp, fp = np.asarray(xp)[ok], np.asarray(fp)[ok]
    if x <= xp[-1]:
        return float(np.exp(np.interp(np.log(x), np.log(xp), np.log(fp))))
    s = np.polyfit(np.log(xp[-3:]), np.log(fp[-3:]), 1)[0]
    return float(fp[-1] * (x / xp[-1]) ** s)


# stars and gas at R200 (log-extrapolated beyond the data where needed); imputed stars use the median ratio at R200
R200 = {n: ETT[n]["R200"] * 1000.0 for n in NAMES}
G200, S200, EXTRAP = {}, {}, {}
for c in CL:
    G200[c["name"]] = loglin_extrap(R200[c["name"]], c["rg"], c["mg"]); EXTRAP[c["name"]] = bool(R200[c["name"]] > c["rg"][np.isfinite(c["mg"])][-1])
    S200[c["name"]] = loglin_extrap(R200[c["name"]], c["rs"], c["ms"]) if c["has_star"] else np.nan
rat200 = np.nanmedian([S200[n] / G200[n] for n in NAMES if np.isfinite(S200[n])])
for n in NAMES:
    if not np.isfinite(S200[n]):
        S200[n] = rat200 * G200[n]
ROWS3 = {}
for rw in AUD["rows"]:
    foot = rw.get("footing", "canonical")
    ROWS3.setdefault(foot, {}).setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"]) * A0_AUD[foot],
                                                                     float(rw["g_hse_over_a0"]) * A0_AUD[foot]))
# C-T3: the audit profile code reproduces the audit rows' baryon field
dmax = 0.0
for foot in FOOTS:
    for name, pts in ROWS3[foot].items():
        i = NAMES.index(name)
        for r, gb, _ in pts:
            j = int(np.where(CA.RADII == r)[0][0])
            gb2 = CA.G * (GAS[i, j] + STARS[i, j]) * CA.MSUN / (r * CA.KPC) ** 2
            dmax = max(dmax, abs(gb2 / gb - 1))
check("C-T3 audit profile code reproduces the audit rows' g_baryon (1e-9)", dmax < 1e-9, f"max rel {dmax:.1e}")


def cl_model(foot, name, r_kpc, gb, gh, src="cond", res="R0", conc=4.0, bias=0.0):
    a0 = C4.A0[foot]
    r = r_kpc * C4.KPC; Mb = gb * r ** 2 / C4.G_SI; Mh = gh / (1 - bias) * r ** 2 / C4.G_SI
    i = NAMES.index(name); j = int(np.where(CA.RADII == r_kpc)[0][0])
    fs = {"cond": FS[i, j], "all": 1.0, "none": 0.0}[src]
    Ms = fs * Mb
    mph = (C4.nu_mono(C4.G_SI * Ms / r ** 2 / a0) - 1.0) * Ms if Ms > 0 else 0.0
    if res == "R0":
        cold = mph
    elif res == "RI":
        cold = max(mph, COLD_X * Mb)
    else:
        R2 = R200[name]; r2 = R2 * C4.KPC
        Mb200 = (G200[name] + S200[name]) * C4.MSUN
        Ms200 = {"cond": S200[name] * C4.MSUN, "all": Mb200, "none": 0.0}[src]
        set200 = (C4.nu_mono(C4.G_SI * Ms200 / r2 ** 2 / a0) - 1.0) * Ms200 if Ms200 > 0 else 0.0
        supply = COLD_X * Mb200 / 0.90
        Mres = max(supply - set200, 0.0)
        cold = mph + Mres * m_nfw(conc * min(r_kpc, R2) / R2) / m_nfw(conc)
    return float(Mh / (Mb + cold)), float(Mb / C4.MSUN), float(Mh / C4.MSUN)


def t3_cell(foot, src, res, conc=4.0, bias=0.0, band=None):
    etas = []
    for name, pts in ROWS3[foot].items():
        p_ = sorted(pts)
        if band is None:
            r, gb, gh = p_[-1]
            etas.append(cl_model(foot, name, r, gb, gh, src, res, conc, bias)[0])
        else:
            e = [cl_model(foot, name, r, gb, gh, src, res, conc, bias)[0] for r, gb, gh in p_ if band[0] <= r <= band[1]]
            if e:
                etas.append(float(np.median(e)))
    v = np.array(etas)
    return dict(eta_median=float(np.median(v)), eta_sd=float(np.std(v, ddof=1)), sigma=float(np.std(v, ddof=1) / math.sqrt(len(v))), n=len(v))


def t3_label(cells):
    if all(abs(c["eta_median"] - 1) <= 0.20 for c in cells):
        return "PASS"
    if all((c["eta_median"] >= 1.30 or c["eta_median"] <= 0.77) and abs(c["eta_median"] - 1) / c["sigma"] >= 3 for c in cells):
        return "FAIL"
    return "TENSION"


T3 = {}
CELLS3 = [("HCB", "cond"), ("B", "all"), ("M2", "none")]
for tag, srcm in CELLS3:
    for res, conc in (("R0", 4.0), ("RI", 4.0), ("RN", 4.0), ("RN", 3.0), ("RN", 5.0)):
        nm = f"{tag}|{res}" + (f"c{conc:g}" if res == "RN" else "")
        cells = {f: t3_cell(f, srcm, res, conc) for f in FOOTS}
        inner = {f: t3_cell(f, srcm, res, conc, band=(200, 420)) for f in FOOTS}
        b02 = {f: t3_cell(f, srcm, res, conc, bias=0.2) for f in FOOTS}
        T3[nm] = dict(headline=cells, label=t3_label(list(cells.values())), inner_200_420=inner, inner_label=t3_label(list(inner.values())),
                      bias02=b02)
        P(f"  {nm:12s} eta headline " + " / ".join(f"{cells[f]['eta_median']:.3f}+-{cells[f]['sigma']:.3f}" for f in FOOTS) + f" -> {T3[nm]['label']:8s}"
          f" | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.3f}" for f in FOOTS) + f" ({T3[nm]['inner_label']})"
          f" | b=0.2 " + " / ".join(f"{b02[f]['eta_median']:.3f}" for f in FOOTS))
J4 = json.load(open(os.path.join(LANES, "CFG4_clusters_results.json")))["numbers"]["H2"]
m1a = all(abs(T3["B|R0"]["headline"][f]["eta_median"] - J624["G2"]["rows"][f + "|nu_mono"]["eta_median"]) < 1e-6 for f in FOOTS)
m1b = all(abs(1 / T3["B|RI"]["headline"][f]["eta_median"] - J4[f + "|nu_mono"]["id_ratio"]) < 5e-3 for f in FOOTS)
# exact identity check on the same statistic CFG4 uses (median of Mid/Mh)
idr = {}
for f in FOOTS:
    v = []
    for name, pts in ROWS3[f].items():
        r, gb, gh = sorted(pts)[-1]
        v.append(1.0 / cl_model(f, name, r, gb, gh, "all", "RI")[0])
    idr[f] = float(np.median(v))
m1c = all(abs(idr[f] - J4[f + "|nu_mono"]["id_ratio"]) < 1e-6 for f in FOOTS)
check("M1-T3a hot restored, R0 reproduces CFG624 NCE eta (1e-6)", m1a,
      ", ".join(f"{T3['B|R0']['headline'][f]['eta_median']:.6f}/{J624['G2']['rows'][f + '|nu_mono']['eta_median']:.6f}" for f in FOOTS))
check("M1-T3b hot restored, RI reproduces CFG4's identity reading median(M_id/M_HSE) (1e-6)", m1c,
      ", ".join(f"{idr[f]:.6f}/{J4[f + '|nu_mono']['id_ratio']:.6f}" for f in FOOTS))
hc_id = {}
for f in FOOTS:
    v = []
    for name, pts in ROWS3[f].items():
        r, gb, gh = sorted(pts)[-1]
        v.append(1.0 / cl_model(f, name, r, gb, gh, "cond", "RI")[0])
    hc_id[f] = float(np.median(v))
P("  identity statistic median(M_model/M_HSE) under RI: H-CB " + " / ".join(f"{hc_id[f]:.4f}" for f in FOOTS)
  + "; B " + " / ".join(f"{idr[f]:.4f}" for f in FOOTS) + "  (cosmic share dominates the settled phantom in both)")
fs_head = [float(FS[NAMES.index(n), int(np.where(CA.RADII == sorted(p)[-1][0])[0][0])]) for n, p in ROWS3["canonical"].items()]
P(f"  condensed share of baryons at the headline radius: median {np.median(fs_head):.3f} (range {min(fs_head):.3f}-{max(fs_head):.3f}); "
  f"R200 beyond the gas data for {sum(EXTRAP.values())}/12 clusters (log-extrapolated)")
lab3 = {nm: T3[nm]["label"] for nm in T3 if nm.startswith("HCB")}
v3 = "FAIL" if all(v == "FAIL" for v in lab3.values()) else ("PASS (reservoir-conditional)" if any(v == "PASS" for v in lab3.values()) else "TENSION")
RES["T3"] = dict(rows=T3, identity_stat=dict(HCB=hc_id, B=idr), condensed_share_headline=fs_head, R200_extrapolated=EXTRAP,
                 HCB_labels=lab3, verdict=v3)
P(f"  T3 verdict: {v3}; H-CB labels by reservoir: {lab3}")

# ===================================================================================================== T6 KiDS
P("\n== T6 KiDS / isolated lenses (record source check)")
LZ = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
fc = LZ["Mgal"] / 10 ** LZ["logM"] - 1
ok6 = bool(np.all(fc >= -1e-9))
check("T6a the record's lens source is stars + cold gas only (Mgal = M*(1 + f_cold), f_cold >= 0; no hot term)", ok6,
      f"f_cold median {np.median(fc):.3f}, min {fc.min():.3f}, max {fc.max():.3f}, N {len(fc)}")
J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))
# share of the law's boost a hot-gas escape (CFG61 class: extra gas inside ~50 kpc) keeps under H-CB: Newtonian dg vs law dg
esc = {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]
    Mg = 10 ** 10.81 * (1 + float(np.median(fc))) * C4.MSUN; r = 50 * C4.KPC
    gN = C4.G_SI * Mg / r ** 2; d = 1e-4
    slope = (C7.nu_mono((gN * (1 + d)) / a0) * gN * (1 + d) - C7.nu_mono((gN * (1 - d)) / a0) * gN * (1 - d)) / (2 * d * gN)
    esc[foot] = dict(dg_law_over_dgN=float(slope), kept_under_HCB=float(1 / slope))
    P(f"  [{foot}] hot-gas escape at 50 kpc (log M* 10.81): law gives dg/dg_N = {float(slope):.2f}; under H-CB the hot gas is Newtonian, keeping "
      f"{1 / float(slope):.2f} of the record's escape boost")
v6 = "NO CHANGE" if ok6 else "CHANGED"
RES["T6"] = dict(f_cold=dict(median=float(np.median(fc)), min=float(fc.min()), max=float(fc.max())), escape=esc, verdict=v6,
                 record_cfg529_verdict=J529.get("verdict"))
P(f"  T6 verdict: {v6} (the record's CFG529/531 numbers carry over: census edge FAILS f30 on both footings; the early-type age signal is untouched)")

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg634_static_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg634_static.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
