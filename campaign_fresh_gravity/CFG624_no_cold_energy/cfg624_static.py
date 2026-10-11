#!/usr/bin/env python3
"""CFG624 G1 (SPARC), G2 (X-COP) and G4 (Local Group timing + Tian+26 groups) for NO COLD ENERGY (FROZEN_CRITERIA.md 803cef306).
Committed pipelines are executed read-only; only the dark component is removed.  MUTATE checks are run in the same pass (named M-*).
  G1: CFG487's SPARC harness (as CFG515/cfg515_sparc.py runs it).  NCE = the law, no edge; B = the census edge; M-G1: a0 -> 0.
  G2: CFG4_clusters.py's X-COP rows (the record's corrected audit).  NCE = M_law; B = identity reading; M-G2 reproduces CFG4.
  G4: CFG522's timing machinery (CFG515/513 constants); NCE = M3 (baryons, law between the pair, no EFE) in the NCE background age;
      M-G4 reproduces CFG522 M3 at 13.80 Gyr and runs a0 -> 0.  Groups: CFG543's committed C0_noedge row (= the law, no edge).
Run from the repository root:  nice -n 10 python3 campaign_fresh_gravity/CFG624_no_cold_energy/cfg624_static.py
kappa = 1/2 FITTED; footings never pooled; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
for d in (LANES, os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG487_settled_fraction_switch")):
    sys.path.insert(0, d)
import CFG4_common as C4                                                     # noqa: E402
import CFG7_common as C7                                                     # noqa: E402
import cfg515_lib as L515                                                    # noqa: E402
import cfg487_lib as LB                                                      # noqa: E402
try:
    os.nice(10)
except OSError:
    pass
LOG, CHK, RES = [], {}, {"lane": "CFG624", "script": "cfg624_static", "criteria": "803cef306"}
FOOTS = ("canonical", "alt")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run from")[0].strip())

# ===================================================================================================== G1 SPARC
P("\n== G1 SPARC RAR (CFG487 harness, read-only)")
src = open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")).read()
m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
m1 = "SPA = {}"
assert src.count(m0) == 1 and src.count(m1) == 1
NS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
          LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NS)
MSUN, G_ = NS["MSUN"], NS["G_"]


def fprof_sparc(r, Mb, a0, mode, rho_tot, rho_b, r_ta=None, Mta=None):
    """CFG515's replacement, copied: fully settled inside min(r_edge(f_ret), r_ta) for B; mode[1] None = the law, no edge (NCE)."""
    fm = mode[1]
    if fm is None:
        return np.ones_like(r)
    f = L515.fret(fm, Mb / MSUN)
    re = math.sqrt(G_ * Mb / a0) / L515.ln_fac(f)
    if r_ta is not None:
        re = min(re, r_ta)
    return np.ones_like(r) * (r <= re)


NS["fprof_sparc"] = fprof_sparc
rms, gb4, ok4, RMS0 = NS["rms"], NS["gb4"], NS["ok4"], NS["RMS0"]
G1 = {}
for foot in FOOTS:
    r_nce = NS["sparc_rms_sw"](foot, ("one", None, False))[0]
    r_b = NS["sparc_rms_sw"](foot, ("one", "census", False))[0]
    a3 = {k: NS["sparc_a3"](k, foot, ("one", None, False))[0] for k in ("spiral", "dwarf")}
    r_newt = rms(np.where(ok4, gb4, 1.0))
    G1[foot] = dict(rms_NCE=r_nce, rms_B_census=r_b, d_rms=r_nce - r_b, A3_spiral=a3["spiral"], A3_dwarf=a3["dwarf"], rms_newton_a0_0=r_newt,
                    npts=int(ok4.sum()))
    P(f"  [{foot}] RAR rms: NCE (law, no edge) {r_nce:.4f} dex; B (census edge) {r_b:.4f}; d {r_nce - r_b:+.5f}; "
      f"A3 sp/dw {a3['spiral']:.3f}/{a3['dwarf']:.3f}; M-G1 a0 -> 0 (Newtonian baryons) {r_newt:.4f}")
c39 = json.load(open(os.path.join(LANES, "CFG39_harness_with_rule_results.json")))["numbers"]["sparc"]["rms0"]
check("C-G1 the harness reproduces CFG39's rms0 (canonical)", abs(RMS0["canonical"] - c39) < 1e-9, f"{RMS0['canonical']:.9f} vs {c39:.9f}")
check("M-G1a census row reproduces CFG515 (d rms = 0)", all(abs(G1[f]["d_rms"]) < 1e-12 for f in FOOTS), "d rms " + ", ".join(f"{G1[f]['d_rms']:+.1e}" for f in FOOTS))
check("M-G1b a0 -> 0 FAILS G1 (rms > 0.15)", all(G1[f]["rms_newton_a0_0"] > 0.15 for f in FOOTS), ", ".join(f"{G1[f]['rms_newton_a0_0']:.3f}" for f in FOOTS))
if all(G1[f]["rms_NCE"] <= 0.12 and abs(G1[f]["d_rms"]) <= 0.005 for f in FOOTS):
    v1 = "PASS"
elif any(G1[f]["rms_NCE"] > 0.15 for f in FOOTS):
    v1 = "FAIL"
else:
    v1 = "TENSION"
RES["G1"] = dict(rows=G1, verdict=v1); P(f"  G1 verdict: {v1}")

# ===================================================================================================== G2 X-COP
P("\n== G2 X-COP (the record's corrected hydrostatic audit rows, as CFG4_clusters.py)")
AUD = json.load(open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "results.json")))
A0_AUD = AUD["a0_m_s2"]
R500 = {d["name"]: d["own_R500_kpc"] for d in AUD["radius_audit"]}
ROWS = {}
for rw in AUD["rows"]:
    foot = rw.get("footing", "canonical")
    ROWS.setdefault(foot, {}).setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"]) * A0_AUD[foot],
                                                                   float(rw["g_hse_over_a0"]) * A0_AUD[foot]))
COSMIC = 0.1200 / 0.02237


def cluster_rows(kfun, foot, bias=0.0, a0=None):
    a0 = C4.A0[foot] if a0 is None else a0
    out = []
    for name, pts in ROWS[foot].items():
        p_ = np.array(sorted(pts)); r = p_[:, 0] * C4.KPC; gb = p_[:, 1]; gh = p_[:, 2] / (1.0 - bias)
        Mb = gb * r ** 2 / C4.G_SI; Mh = gh * r ** 2 / C4.G_SI
        Ml = (kfun(gb / a0) * Mb) if a0 > 0 else Mb
        i = len(r) - 1
        Mid = Mb[i] + max(Ml[i] - Mb[i], COSMIC * Mb[i])
        out.append(dict(name=name, r_kpc=float(p_[i, 0]), frac_R500=float(p_[i, 0] / R500.get(name, np.nan)), eta=float(Mh[i] / Ml[i]),
                        resid_Mb=float((Mh[i] - Ml[i]) / Mb[i]), id_ratio_B=float(Mid / Mh[i]), M_hse=float(Mh[i] / C4.MSUN),
                        M_b=float(Mb[i] / C4.MSUN), M_NCE=float(Ml[i] / C4.MSUN)))
    return out


def med(rows, k):
    v = np.array([x[k] for x in rows]); return float(np.median(v)), float(np.std(v, ddof=1)), float(np.std(v, ddof=1) / math.sqrt(len(v)))


G2 = {}
J4 = json.load(open(os.path.join(LANES, "CFG4_clusters_results.json")))["numbers"]["H2"]
for foot in FOOTS:
    for kn, kf in (("nu_mono", C4.nu_mono), ("P2", C4.nu_p2)):
        rows = cluster_rows(kf, foot)
        e, rr, idb = med(rows, "eta"), med(rows, "resid_Mb"), med(rows, "id_ratio_B")
        bias = {str(b): med(cluster_rows(kf, foot, b), "eta")[0] for b in (0.06, 0.1, 0.2)}
        G2[f"{foot}|{kn}"] = dict(eta_median=e[0], eta_sd=e[1], resid_Mb=rr[0], resid_sd=rr[1], resid_sigma=rr[0] / rr[2],
                                  missing_mass_ratio=e[0], NCE_over_measured=1 / e[0], B_identity_over_measured=idb[0], B_sd=idb[1],
                                  eta_vs_bias=bias, r_frac_R500_median=float(np.median([x["frac_R500"] for x in rows])), n=len(rows),
                                  per_cluster=rows)
        P(f"  [{foot} {kn}] at {G2[f'{foot}|{kn}']['r_frac_R500_median']:.2f} R500 (12 clusters): eta = M_HSE/M_NCE = {e[0]:.3f} +- {e[1]:.3f}; "
          f"missing {rr[0]:.2f} +- {rr[1]:.2f} M_b ({rr[0] / rr[2]:.1f} sigma on the median); NCE/measured {1 / e[0]:.3f}; "
          f"B identity/measured {idb[0]:.3f}; eta at b 0.06/0.1/0.2: " + " / ".join(f"{v:.2f}" for v in bias.values()))
    rn = cluster_rows(C4.nu_mono, foot, a0=0.0)
    G2[f"{foot}|a0_0"] = dict(eta_median=med(rn, "eta")[0])
mg2 = all(abs(G2[f"{f}|{k}"]["eta_median"] - J4[f"{f}|{k}"]["eta"]) < 1e-9 and abs(G2[f"{f}|{k}"]["B_identity_over_measured"] - J4[f"{f}|{k}"]["id_ratio"]) < 1e-9
          for f in FOOTS for k in ("nu_mono", "P2"))
check("M-G2a this lane reproduces CFG4's committed eta and the identity reading (restore cold energy) to 1e-9", mg2,
      "; ".join(f"{f}: eta {G2[f + '|nu_mono']['eta_median']:.4f} vs {J4[f + '|nu_mono']['eta']:.4f}, B {G2[f + '|nu_mono']['B_identity_over_measured']:.4f}" for f in FOOTS))
check("M-G2b a0 -> 0 gives the Newtonian deficit (M_HSE/M_b, CFG4 K1 Newtonian 1 + 5.73)", all(G2[f + "|a0_0"]["eta_median"] > 5 for f in FOOTS),
      ", ".join(f"{G2[f + '|a0_0']['eta_median']:.2f}" for f in FOOTS))
p_ = [G2[f + "|nu_mono"] for f in FOOTS]
if all(abs(x["eta_median"] - 1) <= 0.20 for x in p_):
    v2 = "PASS"
elif all((x["eta_median"] >= 1.30 or x["eta_median"] <= 0.77) and x["resid_sigma"] >= 3 for x in p_):
    v2 = "FAIL"
else:
    v2 = "TENSION"
RES["G2"] = dict(rows={k: {kk: vv for kk, vv in v.items()} for k, v in G2.items()}, verdict=v2); P(f"  G2 verdict: {v2}")

# ===================================================================================================== G4 Local Group + groups
P("\n== G4 Local Group timing (CFG522 machinery, read-only)")
s522 = open(os.path.join(LANES, "CFG522_local_group_timing", "cfg522_lg_timing.py")).read()
mk = "fM, f31 = L.fret_census(MB_PRIM)[0], L.fret_census(MB_M31)[0]"
assert s522.count(mk) == 1
_e = os.environ.pop("CFG522_MUTATE", None)
N5 = {"__file__": os.path.join(LANES, "CFG522_local_group_timing", "cfg522_lg_timing.py"), "__name__": "cfg522_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s522[:s522.index(mk)], "cfg522_ro", "exec"), N5)
G, GYR, H0, OM_L = N5["G"], N5["GYR"], N5["H0"], N5["OM_L"]
MB_MW, MB_M31, D_LG, VR, EVR = N5["MB_PRIM"], N5["MB_M31"], N5["D_LG"], N5["VR_LG"], N5["EVR_LG"]
VT, EVT, DV, EDV = N5["VT_SAL"], N5["EVT_SAL"], N5["D_VDM"], N5["ED_VDM"]
T_REC = N5["T0U"]
# NCE background age (the engines' background with Omega_c = 0, rho_DE held): t0 = int da / (a H0 E(a))
hh = 0.6736; OLn = 1.0 - (0.02237 + 0.12) / hh ** 2; Obn = 0.02237 / hh ** 2; Okn = 1.0 - OLn - Obn
H0s = 100 * hh / 3.0856775814913673e19                                      # 1/s
t0n = quad(lambda a: 1.0 / (a * math.sqrt(Obn / a ** 3 + Okn / a ** 2 + OLn)), 0, 1, limit=200)[0] / H0s
camb_age = None
_cp = os.path.join(REPO, "..", "_external_data", "cfg624_work", "cfg624_camb_pk.npz")
if os.path.exists(_cp):
    camb_age = float(np.load(_cp)["age"])
P(f"  background: CFG522 t0 {T_REC / GYR:.3f} Gyr (record); NCE (Omega_b {Obn:.4f}, Omega_k {Okn:+.4f}, Omega_L {OLn:.5f}) t0 {t0n / (3.15576e16):.3f} Gyr "
  f"; CAMB age (with radiation) {camb_age}")
t0n_u = t0n / 3.15576e16 * GYR                                                 # seconds -> Gyr (Julian) -> CFG522's internal time unit


def acc_forms(foot, a0=None):
    a0 = N5["A0"][foot] if a0 is None else a0
    nu = N5["nu_mono"]; Mb = MB_MW + MB_M31
    def a_t(d, tau=0.0):
        g = G * Mb / d ** 2; return g * float(nu(g / a0)) if a0 > 0 else g
    def a_2b(d, tau=0.0):
        if a0 <= 0:
            return G * Mb / d ** 2
        m1, m2 = MB_MW, MB_M31; M = m1 + m2
        return (2 / 3) * math.sqrt(G * a0) * (M ** 1.5 - m1 ** 1.5 - m2 ** 1.5) * M / (m1 * m2 * d)
    return a_t, a_2b


def stats(acc, t0):
    N5["T0U"] = t0
    vp = N5["vpred"]; zm = N5["zm"]
    v0 = vp(acc, lo=-6000.0); vS = vp(acc, vt=VT, lo=-6000.0)
    vDm, vDp = vp(acc, d0=DV - EDV, vt=VT, lo=-6000.0), vp(acc, d0=DV + EDV, vt=VT, lo=-6000.0)
    vTm, vTp = vp(acc, vt=VT - EVT, lo=-6000.0), vp(acc, vt=VT + EVT, lo=-6000.0)
    sD, sT = abs(vDp - vDm) / 2, abs(vTp - vTm) / 2
    sf = math.sqrt(EVR ** 2 + sD ** 2 + sT ** 2) if np.isfinite(sD + sT) else float("nan")
    return dict(v_radial=v0, z_meas=zm(v0), v_vtSal=vS, sigma_full=sf, z_full=zm(vS, err=sf) if np.isfinite(sf) else (zm(vS) if np.isfinite(vS) else float("inf")))


J522 = json.load(open(os.path.join(LANES, "CFG522_local_group_timing", "cfg522_results.json")))
G4 = {}
for foot in FOOTS:
    a_t, a_2b = acc_forms(foot)
    rec_t, rec_2b = stats(a_t, T_REC), stats(a_2b, T_REC)
    nce_t, nce_2b = stats(a_t, t0n_u), stats(a_2b, t0n_u)
    n_t, n_2b = acc_forms(foot, a0=0.0)
    newt = stats(n_2b, t0n_u)
    G4[foot] = dict(NCE_twobody=nce_2b, NCE_testmass=nce_t, record_age_twobody=rec_2b, record_age_testmass=rec_t, a0_0_newton=newt,
                    B_M1_shared=J522.get("M1", {}).get(foot), B_census=J522.get("census_individual", {}).get(foot))
    P(f"  [{foot}] NCE (t0 {t0n_u / GYR:.2f} Gyr): two-body v {nce_2b['v_radial']:.1f} (z_meas {nce_2b['z_meas']:+.1f}), at v_t 82.4 v {nce_2b['v_vtSal']:.1f} "
      f"(z_full {nce_2b['z_full']:+.2f}, sigma {nce_2b['sigma_full']:.1f}); test-mass v {nce_t['v_radial']:.1f} (z_full {nce_t['z_full']:+.2f})")
    P(f"  [{foot}] record age 13.80: two-body v {rec_2b['v_radial']:.1f} (z {rec_2b['z_meas']:+.1f}), z_full {rec_2b['z_full']:+.2f}; test-mass v {rec_t['v_radial']:.1f}; "
      f"a0 -> 0 (NCE age): v {newt['v_radial']} z_full {newt['z_full']}")
m3 = J522["M3"]
mg4 = all(abs(G4[f]["record_age_testmass"]["v_radial"] - m3[f]["v_testmass"]) < 0.05 and abs(G4[f]["record_age_twobody"]["v_radial"] - m3[f]["v_deep2body"]) < 0.05 for f in FOOTS)
check("M-G4a at 13.80 Gyr the M3 numbers reproduce CFG522 (0.05 km/s)", mg4,
      "; ".join(f"{f}: {G4[f]['record_age_testmass']['v_radial']:.2f}/{m3[f]['v_testmass']:.2f}, {G4[f]['record_age_twobody']['v_radial']:.2f}/{m3[f]['v_deep2body']:.2f}" for f in FOOTS))
check("M-G4b a0 -> 0 (Newtonian baryons) FAILS the timing", all((not np.isfinite(G4[f]["a0_0_newton"]["v_radial"])) or abs(G4[f]["a0_0_newton"]["z_full"]) >= 3 for f in FOOTS),
      "; ".join(f"{f}: v {G4[f]['a0_0_newton']['v_radial']}" for f in FOOTS))
zf = [G4[f]["NCE_twobody"]["z_full"] for f in FOOTS]; zmm = [G4[f]["NCE_twobody"]["z_meas"] for f in FOOTS]
v4 = "PASS" if all(abs(a) < 3 and abs(b) < 3 for a, b in zip(zf, zmm)) else ("FAIL" if any((not np.isfinite(a)) or abs(a) >= 3 for a in zf) else "TENSION")
J543 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))["footings"]
GR = {f: dict(NCE=J543[k]["configs"]["C0_noedge"], B_P2=J543[k]["configs"]["P2"]) for f, k in (("canonical", "can"), ("alt", "alt"))}
for f in FOOTS:
    n, b = GR[f]["NCE"], GR[f]["B_P2"]
    P(f"  groups [{f}] Tian+26 N {n['N']}: NCE (law, no edge) mean {n['mean']:+.3f} dex (Z {n['Z']:+.2f}); B consistent supply P2 {b['mean']:+.3f} (Z {b['Z']:+.2f})")
    for k in ("Delta",):
        n.pop(k, None); b.pop(k, None)
vg = "PASS" if all(abs(GR[f]["NCE"]["Z"]) < 2 for f in FOOTS) else ("FAIL" if any(abs(GR[f]["NCE"]["Z"]) >= 3 for f in FOOTS) else "TENSION")
RES["G4"] = dict(LG=G4, LG_verdict=v4, groups=GR, groups_verdict=vg,
                 background=dict(Omega_b=Obn, Omega_k=Okn, Omega_L=OLn, t0_NCE_gyr=t0n_u / GYR, t0_record_gyr=T_REC / GYR, camb_age=camb_age))
P(f"  G4 verdicts: LG {v4}; groups {vg}")

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg624_static_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg624_static.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
