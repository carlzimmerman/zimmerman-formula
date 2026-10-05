#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG340 -- the pre-reionisation cold-share candidate (CFG338/CFG339) on the big systems.  Criteria frozen first: FROZEN_CRITERIA.md (a1e50f7fc).

  candidate  M_c = R M_b,now / f_b (f_b = 0.157126); max bookkeeping g = g_N + max(g_law - g_N, g_cold), g_cold = (1 - f_b) G M_cold(<r)/r^2;
             P1: M_cold(<r) = M_c min(r/r_f, 1), r_f = top-hat at z_f (CFG336 formula); z_f = 3 decision, 2 and 4 reported; kernel nu_mono.
  harnesses  CFG45 prefix (SPARC P3 rows, X-ray ellipticals P6, SLUGGS h50), CFG4_galaxy_law prefix (SPARC rotmod RAR rms as CFG39),
             CFG4_switch K3 (FP1 E KiDS machinery, FP20 exact projector), CFG4_clusters prefix (X-COP rows) -- all exec'd read-only.
  method     R applied to one population at a time; R_max = largest R with the committed criterion holding on [1, R], both footings
             (bisection in log R on [0, 3] dex to 0.005 dex, contiguity checked on a 0.1-dex grid below R_max).
  decision   PASS: R_max >= 2 R_plaus(upper) for S1, S2, X1, K1, C1; MARGINAL: >= R_plaus but < 2x for one; FAIL: < R_plaus for any.
MUTATE    CFG340_MUTATE=1: R = 30 on all SPARC galaxies must be flagged failing; outputs *_MUTATE.
Run: python3 campaign_fresh_gravity/CFG340_preion_candidate_big_systems/cfg340_big_systems.py
"""
import os, sys, io, math, json, contextlib, time
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C7                                                     # noqa: E402
import CFG4_common as C4                                                     # noqa: E402
sys.path.insert(0, os.path.join(C7.REPO, "hunt_2026"))
MUTATE = os.environ.get("CFG340_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE: R = 30 on all SPARC galaxies -- must be flagged failing ***")
FOOTS = ("canonical", "alt")
FB = 0.157126
WBC = 0.02237 + 0.1200
RHO_M0_KPC = 2.7754e11 * WBC / 1e9                                          # Msun / kpc^3 (CFG336/338)
DELTA_C = 18 * math.pi ** 2
ZF = {"dec": 3.0}
RPL = {"S1": 3.0, "S2": 10 ** 1.09, "X1": 3.0, "K1": 3.0, "C1": 1.2}         # frozen upper ends
RPL_SRC = {"S1": "PROVISIONAL (memory): massive spirals retain baryons, R 1-3",
           "S2": "record: CFG317 R_ind gas-rich LV field 10^0.77 = 5.9, yield +0.1 upper 10^1.09 (conservative proxy)",
           "X1": "PROVISIONAL (memory; CFG317 recalled [Z/H] 0..+0.3 => R_ind 1-2): R 1-3",
           "K1": "PROVISIONAL (memory): isolated log M* 10-11 lenses, R 1-3",
           "C1": "PROVISIONAL (memory): near-closed boxes, R 1-1.2; record f_b/f_bar(X-COP) ~ 1.05"}


def r_f_kpc(Mc_sun, zf):
    return (3.0 * Mc_sun / (4.0 * math.pi * DELTA_C * RHO_M0_KPC * (1.0 + zf) ** 3)) ** (1.0 / 3.0)


def m_cold_frac(Mc_sun, r_kpc, zf):
    """M_cold(<r) / M_c for P1 (vectorised in r)."""
    if Mc_sun <= 0:
        return np.zeros_like(np.asarray(r_kpc, float))
    return np.minimum(np.asarray(r_kpc, float) / r_f_kpc(Mc_sun, zf), 1.0)


# ================================================================================================ CFG45 prefix (read-only)
def quiet_exec(code, ns, name):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, name, "exec"), ns)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return ns


t = time.time()
SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
SRC45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS: (S) and (L) against the lanes\' committed results")')]
assert SRC45.count('READ = ("L", "S", "M", "E")') == 1
SRC45 = SRC45.replace('READ = ("L", "S", "M", "E")', 'READ = ("L",)')
NS = quiet_exec(SRC45, {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_ro"}, "CFG45_ro")
assert abs(float(NS["FB"]) - FB) < 1e-6
G_, KPC, MSUN, A0SI, NU = NS["G_"], NS["KPC"], NS["MSUN"], NS["A0SI"], NS["NU"]
J45 = json.load(open(os.path.join(LANES, "CFG45_rule_readings_results.json")))["numbers"]
P(f"\n  CFG45 prefix exec'd ({time.time() - t:.0f} s)")

# ------------------------------------------------------------------------------------------------ S1/S2 SPARC A3 at R_HI (CFG45 P3 rows)
MASTER = NS["g10"]["read_master"]()
SPROWS = []
for name, m in MASTER.items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0:
        continue
    SPROWS.append(dict(name=name, Ms=Ms, Mb=Mb, r=m["RHI"], kind="dwarf" if math.log10(Ms) < 10.0 else "spiral"))


def sparc_a3(kind, R, foot, zf):
    dv = []
    for s in SPROWS:
        if s["kind"] != kind:
            continue
        r = s["r"]; gb = G_ * s["Mb"] * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI[foot]) * gb
        Mc = R * s["Mb"] / FB
        gc = (1 - FB) * G_ * Mc * float(m_cold_frac(Mc, r, zf)) * MSUN / (r * KPC) ** 2
        ex = max(0.0, gc - (gl - gb))
        dv.append(0.5 * math.log10(1 + ex / gl))
    dv = np.array(dv)
    return float(np.mean(dv < 0.03)), float(dv.max()), len(dv)


# ------------------------------------------------------------------------------------------------ SPARC rotmod RAR rms (CFG39's statistic)
t = time.time()
g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
GAL4, UPS, Rm, GB, GO, OK, WW, GI = (g4[k] for k in ("GAL", "UPS", "Rm", "GB", "GO", "OK", "WW", "GI"))
KPC_S = g4["KPC_S"]
iu = int(np.argmin(np.abs(UPS - 0.61)))
gb4, go4, ok4, ww4 = GB[:, iu], GO[:, iu], OK[:, iu], WW[:, iu]
a0c = C7.A0_SI["canonical"]
gpred4 = np.where(ok4, np.asarray(C7.nu_mono(np.where(ok4, gb4, 1.0) / a0c), float) * np.where(ok4, gb4, 1.0), 1.0)
GSI, MSI = 6.67430e-11, 1.98847e30
GKIND = {}
for i, g in enumerate(GAL4):
    m = g.get("meta") or {}
    if not m or m.get("L36", 0) <= 0:
        continue
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m.get("MHI", 0.0) * 1e9
    GKIND[i] = ("dwarf" if math.log10(Ms) < 10.0 else "spiral", Mb)
r0 = np.log10(np.where(ok4, go4, 1.0)) - np.log10(gpred4)
RMS0 = float(np.sqrt(np.sum(ww4 * r0 ** 2) / np.sum(ww4)))
P(f"  CFG4_galaxy_law prefix exec'd ({time.time() - t:.0f} s): {len(GAL4)} galaxies, rms0 {RMS0:.6f}")


def sparc_rms(kinds, R, zf):
    gadd = np.zeros_like(gpred4)
    for i, (kind, Mb) in GKIND.items():
        if kind not in kinds:
            continue
        sel = (GI == i) & ok4
        rr = Rm[sel]
        Mc = R * Mb / FB
        gc = (1 - FB) * GSI * Mc * m_cold_frac(Mc, rr / KPC_S, zf) * MSI / rr ** 2
        gadd[sel] = np.maximum(0.0, gc - (gpred4[sel] - gb4[sel]))
    r1 = np.log10(np.where(ok4, go4, 1.0)) - np.log10(gpred4 + gadd)
    return float(np.sqrt(np.sum(ww4 * r1 ** 2) / np.sum(ww4)))


def crit_sparc(kind, R, zf):
    a3 = [sparc_a3(kind, R, f, zf) for f in FOOTS]
    drms = sparc_rms((kind,), R, zf) - RMS0
    ok = all(x[0] >= 0.90 for x in a3) and drms < 0.005
    return ok, dict(frac=[x[0] for x in a3], max=[x[1] for x in a3], n=a3[0][2], drms=drms)


# ------------------------------------------------------------------------------------------------ X1 X-ray ellipticals (CFG45 P6)
GAL, M_hern, M_nfw_h10, RADII = NS["GAL"], NS["M_hern"], NS["M_nfw_h10"], NS["RADII"]


def xray_gal(g, foot, R, zf, ups="uk", radii=RADII):
    a0 = A0SI[foot]
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    Mc = R * Ms / FB
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw_h10(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"]); gb = G_ * Mb * MSUN / (r * KPC) ** 2; nu = NU(gb / a0)
        gc = (1 - FB) * G_ * Mc * float(m_cold_frac(Mc, r, zf)) * MSUN / (r * KPC) ** 2
        ex = max(0.0, gc - (nu - 1) * gb) if R > 0 else 0.0
        out.append(math.log10(Mtot / (nu * Mb + ex * (r * KPC) ** 2 / (G_ * MSUN))))
    return float(np.median(out))


def xray_stat(foot, R, zf):
    def samp(**kw):
        per = np.array([xray_gal(g, foot, R, zf, **kw) for g in GAL])
        return per.mean(), per.std(ddof=1) / math.sqrt(len(per)), per
    b, be, per = samp(); s, _, _ = samp(ups="us"); r4, _, _ = samp(radii=(5.0, 10.0, 20.0, 40.0))
    tot = math.hypot(be, math.hypot(s - b, r4 - b))
    return dict(mean=float(b), tot=float(tot), z=float(b / tot))


def crit_xray(R, zf):
    st = {f: xray_stat(f, R, zf) for f in FOOTS}
    return all(abs(st[f]["z"]) < 2 for f in FOOTS), st


# ------------------------------------------------------------------------------------------------ K1 KiDS (CFG4_switch K3 block, copied verbatim in logic)
t = time.time()
GK = {"np": np, "math": math, "os": os, "REPO": C4.REPO, "G_SI": 6.67430e-11, "_trap": C4._trap}
GK = C4.exec_slices(os.path.join(C4.CHAIN, "FP1_static_sector.py"),
                    [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
FIX = C4.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB = GK["LM"], GK["npb"]
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
GN = 6.67430e-11
A0K = C4.A0


def kids_chi2(Mfun, foot):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0K[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return GK["kfit"]({foot: T}, foot, W0, 0.0)[0]


def M_law(Mb, a0):
    return Mb * C4.nu_mono(GN * Mb / RRK ** 2 / a0)


def M_cand(R, zf):
    def f_(Mb, a0):
        Ml = M_law(Mb, a0)
        Mc = R * Mb / FB
        Mcold = (1 - FB) * Mc * m_cold_frac(Mc / MSK, RRK / (MPCK / 1000.0), zf)
        return Mb + np.maximum(Ml - Mb, Mcold)
    return f_


KBASE = {f: kids_chi2(M_law, f) for f in FOOTS}
P(f"  KiDS machinery exec'd ({time.time() - t:.0f} s): law chi^2 nu_mono {KBASE['canonical']:.4f} / {KBASE['alt']:.4f}")


def crit_kids(R, zf):
    d = {f: kids_chi2(M_cand(R, zf), f) - KBASE[f] for f in FOOTS}
    return all(v <= 9.0 for v in d.values()), d


# ------------------------------------------------------------------------------------------------ C1 X-COP (CFG4_clusters prefix)
t = time.time()
sys.path.insert(0, LANES)
nsC, _ = C4.exec_slices(os.path.join(LANES, "CFG4_clusters.py"), [(None, "TAB = {}")], name="cfg4_clusters_ro")
ROWS, A0C, COSMIC = nsC["ROWS"], nsC["A0"], nsC["COSMIC"]
J4C = json.load(open(os.path.join(LANES, "CFG4_clusters_results.json")))["numbers"]
P(f"  CFG4_clusters prefix exec'd ({time.time() - t:.0f} s): {len(ROWS['canonical'])} clusters; COSMIC {COSMIC:.5f} vs (1-f_b)/f_b {(1 - FB) / FB:.5f}")


def xcop(foot, R, zf, identity=False):
    a0 = A0C[foot]; ratios, rin = [], []
    for name, pts in ROWS[foot].items():
        p_ = np.array(sorted(pts)); r = p_[:, 0] * C4.KPC; gb = p_[:, 1]; gh = p_[:, 2]
        Mb = gb * r ** 2 / C4.G_SI; Mh = gh * r ** 2 / C4.G_SI; Ml = C4.nu_mono(gb / a0) * Mb
        i = len(r) - 1
        if identity:
            dark = max(Ml[i] - Mb[i], COSMIC * Mb[i])
        else:
            Mc = R * Mb[i] / FB
            fr = float(m_cold_frac(Mc / C4.MSUN, p_[i, 0], zf))
            rin.append(fr >= 1.0)
            dark = max(Ml[i] - Mb[i], (1 - FB) * Mc * fr)
        ratios.append((Mb[i] + dark) / Mh[i])
    return float(np.median(ratios)), float(np.std(ratios, ddof=1)), rin


def crit_xcop(R, zf):
    st = {f: xcop(f, R, zf)[0] for f in FOOTS}
    return all(abs(v - 1) <= 0.20 for v in st.values()), st


# ================================================================================================ controls C0
P("\n# C0 controls: the law / identity reproduce B's committed numbers")
c39 = json.load(open(os.path.join(LANES, "CFG39_harness_with_rule_results.json")))["numbers"]["sparc"]
check("C0a SPARC law rms reproduces CFG39 rms0", abs(RMS0 - c39["rms0"]) < 1e-9, f"{RMS0:.9f} vs {c39['rms0']:.9f}")
k3 = json.load(open(os.path.join(LANES, "CFG4_switch_results.json")))["numbers"]["K3"]["base"]
dk = max(abs(KBASE[f] - k3[f"{f}|nu_mono"]) for f in FOOTS)
check("C0b KiDS law chi^2 (nu_mono) reproduces CFG4_switch K3", dk < 1e-6, f"max |d| {dk:.2e}")
xl = {f: xray_stat(f, 0.0, 3.0) for f in FOOTS}
dx = max(abs(xl[f]["z"] - J45["XRAY"][f"{f}|L"]["z"]) for f in FOOTS)
check("C0c X-ray law z reproduces CFG45 XRAY |L", dx < 1e-9, f"max |d z| {dx:.1e}")
idm = {f: xcop(f, 1.0, 3.0, identity=True)[0] for f in FOOTS}
did = max(abs(idm[f] - J4C["H2"][f"{f}|nu_mono"]["id_ratio"]) for f in FOOTS)
check("C0d X-COP identity reading reproduces CFG4_clusters H2 (0.9457)", did < 1e-6, f"max |d| {did:.1e}")
B_BASE = {"S1": f"CFG45 S {100 * J45['SPARC']['spiral|S']['frac_lt003']:.0f}% < 0.03; CFG39 drms {c39['rms1'] - c39['rms0']:+.4f}",
          "S2": f"CFG45 S {100 * J45['SPARC']['dwarf|S']['frac_lt003']:.0f}% < 0.03; CFG39 drms {c39['rms1'] - c39['rms0']:+.4f}",
          "X1": f"CFG45 S z {J45['XRAY']['canonical|S']['z']:+.2f} / {J45['XRAY']['alt|S']['z']:+.2f}",
          "K1": f"law chi^2 {KBASE['canonical']:.2f} / {KBASE['alt']:.2f} (B's switch off in the lens bins)",
          "C1": f"identity {idm['canonical']:.4f} +- {J4C['H2']['canonical|nu_mono']['id_sd']:.3f}"}

CRIT = {"S1": lambda R, zf: crit_sparc("spiral", R, zf), "S2": lambda R, zf: crit_sparc("dwarf", R, zf),
        "X1": crit_xray, "K1": crit_kids, "C1": crit_xcop}
NAMES = {"S1": "SPARC log M* >= 10", "S2": "SPARC dwarfs", "X1": "X-ray ellipticals", "K1": "KiDS isolated lenses", "C1": "X-COP clusters"}
RES = {"lane": "CFG340", "mutate": MUTATE, "rms0": RMS0, "kids_base": KBASE, "xcop_identity": idm, "B_base": B_BASE, "R_plaus_upper": RPL,
       "R_plaus_src": RPL_SRC}

# ================================================================================================ MUTATE
if MUTATE:
    P("\n# MUTATE: R = 30 on all SPARC galaxies (z_f = 3)")
    a3 = {k: [sparc_a3(k, 30.0, f, 3.0) for f in FOOTS] for k in ("dwarf", "spiral")}
    drms = sparc_rms(("dwarf", "spiral"), 30.0, 3.0) - RMS0
    fails = (not all(x[0] >= 0.9 for k in a3 for x in a3[k])) or drms >= 0.005
    P(f"  A3 fractions dwarf {[round(x[0], 3) for x in a3['dwarf']]}, spiral {[round(x[0], 3) for x in a3['spiral']]}; drms {drms:+.4f}")
    check("MUTATE: R = 30 on SPARC is flagged failing", fails)
    RES["mutate_sparc"] = dict(a3={k: [x[0] for x in v] for k, v in a3.items()}, drms=drms)
else:
    # ============================================================================================ R = 1 rows
    P("\n# R = 1 rows (z_f = 3) next to B's baseline")
    R1 = {}
    for k in CRIT:
        ok, st = CRIT[k](1.0, 3.0); R1[k] = dict(ok=ok, st=st)
        P(f"  {k} {NAMES[k]:22s} R=1: {'pass' if ok else 'FAIL'}  {json.dumps(st, default=float)}   | B: {B_BASE[k]}")
    rin = {f: xcop(f, 1.0, 3.0)[2] for f in FOOTS}
    same = max(abs(R1["C1"]["st"][f] - idm[f]) for f in FOOTS)
    P(f"  X-COP: outermost radius beyond r_f(z_f = 3) for {sum(rin['canonical'])}/{len(rin['canonical'])} clusters; |R=1 - identity| = {same:.2e}")
    RES["R1"] = R1; RES["xcop_R1_vs_identity"] = same
    check("R = 1: every population passes its committed criterion (the bisection is meaningful)", all(v["ok"] for v in R1.values()))

    # ============================================================================================ R_max bisection
    def rmax(k, zf):
        ok1, _ = CRIT[k](1.0, zf)
        if not ok1:
            return None, []
        if CRIT[k](1000.0, zf)[0]:
            return 1000.0, []
        lo, hi = 0.0, 3.0
        while hi - lo > 0.005:
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if CRIT[k](10 ** mid, zf)[0] else (lo, mid)
        grid = [g for g in np.arange(0.0, lo, 0.1)]
        holes = [round(float(g), 2) for g in grid if not CRIT[k](10 ** g, zf)[0]]
        return 10 ** lo, holes

    P("\n# R_max (contiguous from R = 1; both footings)")
    RMAX = {}
    for zf in (3.0, 2.0, 4.0):
        for k in CRIT:
            rm, holes = rmax(k, zf)
            RMAX[f"{k}|{zf:g}"] = dict(Rmax=rm, holes=holes)
            st = CRIT[k](rm, zf)[1] if rm else None
            P(f"  z_f {zf:g}  {k} {NAMES[k]:22s} R_max = {('fails at R=1' if rm is None else f'{rm:.3f}'):>12s}  R_plaus(upper) {RPL[k]:.2f}"
              f"  ratio {('-' if rm is None else f'{rm / RPL[k]:.2f}')}  holes {holes}  at R_max: {json.dumps(st, default=float)}  ({time.time() - T0:.0f} s)")
    RES["Rmax"] = RMAX
    check("R_max contiguous below the bisection edge (0.1-dex grid) for every population at z_f = 3",
          all(not RMAX[f"{k}|3"]["holes"] for k in CRIT))

    # ============================================================================================ decision
    rat = {k: (RMAX[f"{k}|3"]["Rmax"] or 0.0) / RPL[k] for k in CRIT}
    if any(v < 1.0 for v in rat.values()):
        verdict = "FAIL"
    elif all(v >= 2.0 for v in rat.values()):
        verdict = "PASS"
    else:
        verdict = "MARGINAL"
    P("\n# Decision (z_f = 3): " + "; ".join(f"{k} R_max/R_plaus {v:.2f}" for k, v in rat.items()) + f"  ->  VERDICT {verdict}")
    for zf in (2.0, 4.0):
        rz = {k: (RMAX[f"{k}|{zf:g}"]["Rmax"] or 0.0) / RPL[k] for k in CRIT}
        vz = "FAIL" if any(v < 1 for v in rz.values()) else ("PASS" if all(v >= 2 for v in rz.values()) else "MARGINAL")
        P(f"  (reported) z_f {zf:g}: " + "; ".join(f"{k} {v:.2f}" for k, v in rz.items()) + f" -> {vz}")
        RES[f"verdict_zf{zf:g}"] = vz
    RES["ratio"] = rat; RES["verdict"] = verdict

    # ============================================================================================ POST HOC (no verdict depends on it)
    P("\n# POST HOC (added after the main run; no verdict depends on it): for populations failing at R = 1, the largest R <= 1 that passes"
      " (bisection in log R on [-3, 0] dex), z_f 3; and which clause fails at R = 1")
    PH = {}
    for k in CRIT:
        if CRIT[k](1.0, 3.0)[0]:
            continue
        lo, hi = -3.0, 0.0
        if not CRIT[k](10 ** lo, 3.0)[0]:
            PH[k] = None; P(f"  {k}: fails even at R = 1e-3"); continue
        while hi - lo > 0.005:
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if CRIT[k](10 ** mid, 3.0)[0] else (lo, mid)
        PH[k] = 10 ** lo
        P(f"  {k} {NAMES[k]:22s} passes only for R <= {10 ** lo:.3f}  (cold mass <= {10 ** lo:.3f} x the cosmic share); at R = 1: "
          f"{json.dumps(CRIT[k](1.0, 3.0)[1], default=float)}")
    RES["posthoc_Rpass_below1"] = PH

    # ============================================================================================ reported: SLUGGS h50 (B red)
    RES50, sigma_r2, sigma_los, GAMMA, nu_h = NS["RES50"], NS["sigma_r2"], NS["sigma_los"], NS["GAMMA"], NS["nu_h"]
    G50, KPC50, MSUN50 = NS["G50"], NS["KPC50"], NS["MSUN50"]

    def sluggs_mean(foot, R, zf=3.0):
        a0 = A0SI[foot]; offs = []
        for r in RES50:
            Ms = r["Mstar"]; a_h = r["Re"] / 1.8153; Mc = R * Ms / FB

            def g(rr, Ms=Ms, a_h=a_h, Mc=Mc):
                Mb = Ms * MSUN50 * rr ** 2 / (rr + a_h) ** 2; gN = G50 * Mb / (rr * KPC50) ** 2; gl = gN * nu_h(gN / a0)
                gc = (1 - FB) * G50 * Mc * MSUN50 * m_cold_frac(Mc, rr, zf) / (rr * KPC50) ** 2
                return gN + np.maximum(gl - gN, gc)
            offs.append(float(np.mean(np.log10(r["Sb"][r["out"]] / sigma_los(r["Rb"], sigma_r2(g, GAMMA), GAMMA)[r["out"]]))))
        o = np.array(offs)
        return float(o.mean()), float(o.mean() / (o.std(ddof=1) / math.sqrt(len(o))))
    SLG = {f"{R:g}": {f: sluggs_mean(f, R) for f in FOOTS} for R in (1.0, 3.0, 10.0)}
    P("\n# Reported only: SLUGGS h50 (B red, z +3.3) under the candidate at z_f 3: " +
      "; ".join(f"R {R}: " + ", ".join(f"{f[:3]} {m:+.3f} (z {z:+.2f})" for f, (m, z) in v.items()) for R, v in SLG.items()))
    RES["sluggs_reported"] = SLG

RES["checks"] = CHECKS
nfail = sum(not c["ok"] for c in CHECKS)
P(f"\n{len(CHECKS) - nfail}/{len(CHECKS)} checks pass  ({time.time() - T0:.0f} s)")
with open(os.path.join(HERE, f"cfg340_big_systems{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"cfg340_big_systems{TAG}_results.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=float)
sys.exit(1 if nfail else 0)
