#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG498 data legs (FROZEN_CRITERIA.md d9c739010): the clock taper (no edge) with the capped, mass-conserving draw.
  object  phantom x m(r) out to r_ta (m from cfg487_lib.ShellClock: V1 rho_X = law mass, MS1 EXCEPTION; V2 rho_X = M_b(<r)/f_b,
          strict MS1); draw D = tapered phantom inside r_ta; available cold energy C = (1 - f_b) M_ta, M_ta = (4pi/3) r_ta^3
          (1 + delta_ta(z)) rho_m(z); q_raw = D / C.  PRIMARY cap: if q_raw > 1 the tapered phantom is x 1/q_raw.  REPORTED cap
          (outer-first): truncated where the tapered phantom reaches C.
  (b) KiDS  -- CFG413's stack P via CFG487's copied harness; PASS iff chi2 - chi2_best(CFG413) <= 4 on both footings.
               Reported: two-halo frozen at CFG495's A_equiv = 0.07 and at A = 0.
  (c) SPARC -- CFG346's S clauses via CFG487's copied harness (S-A3 >= 90% spirals and dwarfs; |d rms| < 0.005), both footings.
Controls: C2 (uncapped rows = CFG487's switch-only rows; CFG413 x = 0.5 / 1.0 reproduced).  kappa = 1/2 FITTED; footings never pooled.
MUTATE (CFG498_MUTATE=1, outputs *_MUTATE.*): the FRW-firing clock (m = background value on every shell): the taper must vanish
(the KiDS row must move to CFG413's x = 1 neighbourhood, i.e. change by more than 4).
Run: nice -n 10 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_data.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
sys.path.insert(0, LANES)
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg487_lib as LB                                                      # noqa: E402
import cfg100_lib as C                                                       # noqa: E402  (read-only import, as CFG413)
import CFG7_common as C7                                                     # noqa: E402
import CFG4_common as C4                                                     # noqa: E402
MUTATE = os.environ.get("CFG498_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
FOOTS = ("canonical", "alt")
OUT, CHK = [], {}
RES = {"lane": "CFG498", "script": "cfg498_data", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg, load_bearing=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=load_bearing, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
SC = LB.ShellClock(Om=C.OM)                                                  # cfg100's Omega_m = 0.3153
RHO_M0_MPC = C.OM * C.RHOC0                                                  # Msun / Mpc^3 (cfg100)
P(f"\nshell clock: {len(SC.rows)} shells, a_ta {min(r['a_ta'] for r in SC.rows):.4f}-{max(r['a_ta'] for r in SC.rows):.3f}; "
  f"edge factor {LB.EDGE_FAC:.4f}; f_b {LB.FB:.6f}")


def m_profile(rho_ratio, a_obs, cons=False):  # CFG487's function, unchanged
    """settled fraction; MUTATE: FRW-firing clock, E_bg = Int_{a_i}^{a_obs} sqrt(1.5 Om rho_X/rho_bar(a) ... ) on every shell."""
    if MUTATE:
        # latched from z_i on every parcel; E >= the background value (rate at the mean density), a lower bound used here
        Ebg = quad(lambda x: math.sqrt(1.5 * C.OM / x ** 3) / (x * math.sqrt(C.OM / x ** 3 + 1 - C.OM)), 1e-3, a_obs)[0]
        return np.full(np.shape(np.atleast_1d(rho_ratio)), -math.expm1(-Ebg))
    return SC.m_of_rho(rho_ratio, a_obs, conservative=cons)[0]


# =================================================================================================== (b) KiDS (CFG413 stack P)
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float)
jk = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
assert np.allclose(pl["gbar_edges"], C.GEDGE)
nL = len(z)


def esd_full_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt
NG = len(cnt)
P(f"\n(b) KiDS stack P: lenses {nL}, groups {NG}")


def pstack(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])    # CFG377's two-halo template


def chi2(d, C_, h, m, t, mode="free"):
    Ci = np.linalg.inv(C_); r = d - m
    if mode == "none":
        return float(h * r @ Ci @ r), 0.0
    if isinstance(mode, float):                                              # frozen two-halo amplitude
        rr = r - mode * t
        return float(h * rr @ Ci @ rr), mode
    A = float((t @ Ci @ r) / (t @ Ci @ t))
    rr = r - A * t
    return float(h * rr @ Ci @ rr), A


def kids_vec(Mg, zl, a0, rout, mfun=None, cap=None, Cav=None, diag=None):
    """law phantom x m(r) out to rout [Mpc], mass frozen beyond; + baryon point mass (CFG413 law_vec form).
    cap: None | 'uniform' (x 1/max(1, D/Cav)) | 'outer' (truncate where the tapered phantom reaches Cav)."""
    r = np.geomspace(1e-4, rout, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    if mfun is not None:
        mm = mfun(r)
        dM = np.diff(np.concatenate([[0.0], Md]))
        mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
        Md = np.cumsum(mmid * dM)
    q = float(Md[-1] / Cav) if Cav is not None else float("nan")
    if diag is not None:
        diag.append(q)
    if cap == "uniform" and q > 1.0:
        Md = Md / q
    elif cap == "outer" and q > 1.0:
        Md = np.minimum(Md, Cav)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


ROWK = ("C2_x0.5", "C2_x1.0", "V1_cap", "V2_cap", "V1_cap_outer", "V2_cap_outer", "V1_nocap", "V2_nocap")


def kids_rows(foot):
    a0 = C.A0[foot]
    rta = np.array([C.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
    rows = {k: [] for k in ROWK}
    qd = {"V1": [], "V2": []}; cons = []
    for g in range(NG):
        Mg, zl = GM[g], GZ[g]; ao = 1.0 / (1.0 + zl)
        Mta = 4 * math.pi / 3 * rta[g] ** 3 * RHO_M0_MPC * (1 + zl) ** 3 * C.dta(zl)
        Cav = (1.0 - LB.FB) * Mta
        cons.append(Mg * float(C.nu_mono(C.G_MPC * Mg / rta[g] ** 2 / a0)) / Mta - 1.0)
        rho1 = lambda r: Mg * C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        rho2 = lambda r: (Mg / LB.FB) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        m1 = lambda r: m_profile(rho1(r), ao)
        m2 = lambda r: m_profile(rho2(r), ao)
        rows["C2_x0.5"].append(kids_vec(Mg, zl, a0, 0.5 * rta[g]))
        rows["C2_x1.0"].append(kids_vec(Mg, zl, a0, 1.0 * rta[g]))
        rows["V1_cap"].append(kids_vec(Mg, zl, a0, rta[g], m1, "uniform", Cav, qd["V1"]))
        rows["V2_cap"].append(kids_vec(Mg, zl, a0, rta[g], m2, "uniform", Cav, qd["V2"]))
        rows["V1_cap_outer"].append(kids_vec(Mg, zl, a0, rta[g], m1, "outer", Cav))
        rows["V2_cap_outer"].append(kids_vec(Mg, zl, a0, rta[g], m2, "outer", Cav))
        rows["V1_nocap"].append(kids_vec(Mg, zl, a0, rta[g], m1))
        rows["V2_nocap"].append(kids_vec(Mg, zl, a0, rta[g], m2))
    return {k: np.array(v) for k, v in rows.items()}, rta, {k: np.array(v) for k, v in qd.items()}, np.array(cons)


ALL = np.ones(nL, bool)
d, Cv = esd_full_loo(ALL); tm = pstack(TT, ALL); h = hart(15)
J413 = json.load(open(os.path.join(LANES, "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
BEST = {f: J413["vs_best_x_reported"][f]["chi2_best"] for f in FOOTS}
X1 = {f: J413["primary"][f]["1.0"]["free"]["chi2"] for f in FOOTS}
X05 = {f: J413["primary"][f]["0.5"]["free"]["chi2"] for f in FOOTS}
P(f"  CFG413 committed: best (x = 0.5) chi2 {BEST['canonical']:.4f} / {BEST['alt']:.4f}; x = 1 chi2 {X1['canonical']:.4f} / {X1['alt']:.4f}")
A495 = 0.07                                                                  # CFG495 FROZEN_CRITERIA (a703a87da): frozen two-halo, A_equiv
J487 = json.load(open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data_results.json")))
KID = {}
for foot in FOOTS:
    t = time.time()
    tabs, rta, qd, cons = kids_rows(foot)
    rr = {}
    wq = {}
    for k, tab in tabs.items():
        m = pstack(tab, ALL)
        c, A = chi2(d, Cv, h, m, tm, "free")
        c0, _ = chi2(d, Cv, h, m, tm, "none")
        cf, _ = chi2(d, Cv, h, m, tm, A495)
        drop = []
        for kb in range(15):
            sel = np.array([i for i in range(15) if i != kb])
            cd, _ = chi2(d[sel], Cv[np.ix_(sel, sel)], hart(14), m[sel], tm[sel], "free")
            cx, _ = chi2(d[sel], Cv[np.ix_(sel, sel)], hart(14), pstack(tabs["C2_x0.5"], ALL)[sel], tm[sel], "free")
            drop.append(cd - cx)
        rr[k] = dict(chi2=c, A=A, chi2_no2h=c0, chi2_2h_frozen495=cf, d_vs_best=c - BEST[foot], d_vs_x1=c - X1[foot],
                     drop_one_bin_d_vs_x05=[float(min(drop)), float(max(drop))], model=m.tolist())
    for v in ("V1", "V2"):
        q = qd[v]
        wq[v] = dict(q_raw_median=float(np.median(q)), q_raw_p90=float(np.percentile(q, 90)), q_raw_max=float(q.max()),
                     frac_groups_cap_binds=float(np.mean(q > 1.0)), frac_lenses_cap_binds=float(np.sum(cnt[q > 1.0]) / nL))
    KID[foot] = dict(rows=rr, q_raw=wq, r_ta_median_Mpc=float(np.median(rta)),
                     Mta_consistency_max_abs=float(np.max(np.abs(cons))))
    P(f"\n  [{foot}] ({time.time() - t:.0f} s) r_ta median {np.median(rta):.3f} Mpc; M_b + M_ph,law(<r_ta) vs M_ta: max |rel diff| {np.max(np.abs(cons)):.1e}")
    for v in ("V1", "V2"):
        P(f"    q_raw = D/C ({v}): median {wq[v]['q_raw_median']:.4f}, 90% {wq[v]['q_raw_p90']:.4f}, max {wq[v]['q_raw_max']:.4f}; "
          f"cap binds for {wq[v]['frac_groups_cap_binds']:.4f} of groups ({wq[v]['frac_lenses_cap_binds']:.4f} of lenses)")
    P("    row            | chi2 free   A_2h   | chi2-best  chi2-x1 | chi2 2h=0.07 (CFG495) | chi2 no-2h | drop-one-bin (row - x0.5)")
    for k, r_ in rr.items():
        P(f"    {k:15s}| {r_['chi2']:9.3f} {r_['A']:7.3f} | {r_['d_vs_best']:+9.3f} {r_['d_vs_x1']:+8.3f} | {r_['chi2_2h_frozen495']:12.2f}          | {r_['chi2_no2h']:9.2f} | "
          f"{r_['drop_one_bin_d_vs_x05'][0]:+.2f}..{r_['drop_one_bin_d_vs_x05'][1]:+.2f}")
RES["kids"] = KID
c2 = max(max(abs(KID[f]["rows"]["C2_x0.5"]["chi2"] - X05[f]), abs(KID[f]["rows"]["C2_x1.0"]["chi2"] - X1[f])) for f in FOOTS)
if not MUTATE:
    c2b = max(abs(KID[f]["rows"][f"{v}_nocap"]["chi2"] - J487["kids"][f]["rows"][f"{v}_noedge"]["chi2"]) for f in FOOTS for v in ("V1", "V2"))
    check("C2 KiDS harness: CFG413 x = 0.5 / 1.0 reproduced within 0.01, and the uncapped rows equal CFG487's switch-only rows within 0.01",
          c2 <= 0.01 and c2b <= 0.01, f"CFG413 max |diff| {c2:.5f}; CFG487 switch-only max |diff| {c2b:.5f}")
else:
    check("C2 KiDS harness (MUTATE run): CFG413 x = 0.5 / 1.0 reproduced within 0.01", c2 <= 0.01, f"max |diff| {c2:.5f}")
A486 = {"canonical": (0.746, 2.358), "alt": (0.635, 2.155)}
for v in ("V1", "V2"):
    ok = all(KID[f]["rows"][f"{v}_cap"]["d_vs_best"] <= 4.0 for f in FOOTS)
    RES[f"kids_pass_{v}"] = ok
    check(f"(b) KiDS {v} capped taper: chi2 - chi2_best(CFG413) <= 4 on both footings", ok,
          ", ".join(f"{f} {KID[f]['rows'][f'{v}_cap']['chi2']:.3f} - {BEST[f]:.3f} = {KID[f]['rows'][f'{v}_cap']['d_vs_best']:+.3f} "
                    f"(A {KID[f]['rows'][f'{v}_cap']['A']:.3f}, CFG486 range {A486[f]})" for f in FOOTS), load_bearing=False)
if MUTATE:
    det = all(abs(KID[f]["rows"]["V1_cap"]["chi2"] - J487["kids"][f]["rows"]["V1_noedge"]["chi2"]) > 4.0 for f in FOOTS)
    RES["mutate_detected"] = det
    check("MUTATE (FRW-firing clock): the V1 capped-taper KiDS chi2 moves by > 4 from the real clock's row on both footings", det,
          ", ".join(f"{f}: {KID[f]['rows']['V1_cap']['chi2']:.3f} vs {J487['kids'][f]['rows']['V1_noedge']['chi2']:.3f}" for f in FOOTS), load_bearing=False)

# =================================================================================================== (a) SPARC (CFG346 copy)
P("\n(a) SPARC (CFG346's S clauses; harness copied)")


def quiet_exec(code, ns, name):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, name, "exec"), ns)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return ns


t = time.time()
sys.path.insert(0, os.path.join(C7.REPO, "hunt_2026"))
SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
SRC45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS: (S) and (L) against the lanes\' committed results")')]
assert SRC45.count('READ = ("L", "S", "M", "E")') == 1
SRC45 = SRC45.replace('READ = ("L", "S", "M", "E")', 'READ = ("L",)')
NS = quiet_exec(SRC45, {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_ro"}, "CFG45_ro")
G_, KPC, MSUN, A0SI, NU = NS["G_"], NS["KPC"], NS["MSUN"], NS["A0SI"], NS["NU"]
MASTER = NS["g10"]["read_master"]()
NUV = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)
_yy = np.geomspace(1e-6, 1e3, 40)
assert max(abs(NUV(v) - NU(float(v))) / NU(float(v)) for v in _yy) < 1e-9, "CFG45 NU != nu_mono"
OMH2 = 0.02237 + 0.1200
RHO_M0 = 3 * (100e3 / (1e3 * KPC)) ** 2 * OMH2 / (8 * math.pi * G_)            # kg/m^3 at z = 0 (CFG346)
RG = np.geomspace(0.05, 2.0e5, 3000) * KPC
J4S = json.load(open(os.path.join(LANES, "CFG4_switch_results.json")))["numbers"]
DTA_000 = J4S["D1"]["0.0"]["one_plus_delta_ta"]


def r_ta_point(Mb_kg, a0):
    Ml = Mb_kg * NUV(G_ * Mb_kg / RG ** 2 / a0)
    D = Ml / (4.0 / 3.0 * math.pi * RG ** 3 * RHO_M0)
    i = int(np.where(D < DTA_000)[0][0])
    return float(math.exp(np.interp(math.log(DTA_000), [math.log(D[i]), math.log(D[i - 1])], [math.log(RG[i]), math.log(RG[i - 1])]))), Ml


SPROWS = []
for name, m in MASTER.items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0:
        continue
    SPROWS.append(dict(name=name, Ms=Ms, Mb=Mb, r=m["RHI"], kind="dwarf" if math.log10(Ms) < 10.0 else "spiral"))
g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
GAL4, UPS, Rm, GB, GO, OK, WWr, GI = (g4[k] for k in ("GAL", "UPS", "Rm", "GB", "GO", "OK", "WW", "GI"))
iu = int(np.argmin(np.abs(UPS - 0.61)))
gb4, go4, ok4, ww4 = GB[:, iu], GO[:, iu], OK[:, iu], WWr[:, iu]
GPRED = {f: np.where(ok4, np.asarray(C7.nu_mono(np.where(ok4, gb4, 1.0) / C7.A0_SI[f]), float) * np.where(ok4, gb4, 1.0), 1.0) for f in FOOTS}
GSI, MSI = 6.67430e-11, 1.98847e30
GMB = {}
for i, g in enumerate(GAL4):
    mt = g.get("meta") or {}
    if mt and mt.get("L36", 0) > 0:
        GMB[i] = (0.61 * mt["L36"] * 1e9 + 1.33 * mt.get("MHI", 0.0) * 1e9) * MSI


def rms(gp):
    r1 = np.log10(np.where(ok4, go4, 1.0)) - np.log10(gp)
    return float(np.sqrt(np.sum(ww4 * r1 ** 2) / np.sum(ww4)))


RMS0 = {f: rms(GPRED[f]) for f in FOOTS}
P(f"  harnesses exec'd ({time.time() - t:.0f} s): {len(SPROWS)} P3 rows, {len(GAL4)} rotmod galaxies ({len(GMB)} with masses); "
  f"rms0 {RMS0['canonical']:.6f} / {RMS0['alt']:.6f}")


def fprof_sparc(r, Mb, a0, ver, rho_tot, rho_b):
    """taper profile m(r) on radii r [m]; ver V1 / V2 / one.  m -> 0 beyond r_ta by construction (latch off)."""
    if ver == "one":
        return np.ones_like(r)
    rho = rho_tot if ver == "V1" else rho_b / LB.FB
    return m_profile(rho / RHO_M0, 1.0)


MODES = {"V1_cap": ("V1", "uniform"), "V2_cap": ("V2", "uniform"), "V1_cap_outer": ("V1", "outer"), "V2_cap_outer": ("V2", "outer"),
         "V1_nocap": ("V1", None), "V2_nocap": ("V2", None), "C3_one_noedge": ("one", None)}
RTA_S = {f: {s["name"]: r_ta_point(s["Mb"] * MSUN, A0SI[f]) for s in SPROWS} for f in FOOTS}
RTA_G = {f: {i: r_ta_point(Mb, C7.A0_SI[f]) for i, Mb in GMB.items()} for f in FOOTS}


def taper_on_RG(Mb, Ml, a0, ver):
    """tapered phantom on RG (to r_ta, frozen beyond via m = 0) and the cap numbers (q_raw, Cav)."""
    rho_tot = 3 * Ml / (4 * math.pi * RG ** 3)
    rho_b = 3 * Mb / (4 * math.pi * RG ** 3)
    f = fprof_sparc(RG, Mb, a0, ver, rho_tot, rho_b)
    Mph = np.concatenate([[0.0], Ml - Mb]); ff = np.concatenate([[f[0]], f])
    Mt = np.cumsum(0.5 * (ff[1:] + ff[:-1]) * np.diff(Mph))
    return Mt


def capped(Mt, rta, Ml, cap):
    Mta = float(np.interp(rta, RG, Ml)); Cav = (1.0 - LB.FB) * Mta
    q = float(np.interp(rta, RG, Mt)) / Cav
    if cap == "uniform" and q > 1:
        Mt = Mt / q
    elif cap == "outer" and q > 1:
        Mt = np.minimum(Mt, Cav)
    return Mt, q


QS = {}


def sparc_a3(kind, foot, mode):
    dv = []
    a0 = A0SI[foot]; ver, cap = mode
    for s in SPROWS:
        if s["kind"] != kind:
            continue
        rta, Ml = RTA_S[foot][s["name"]]
        Mb = s["Mb"] * MSUN
        Mt = taper_on_RG(Mb, Ml, a0, ver)
        Mt, q = capped(Mt, rta, Ml, cap)
        QS.setdefault((foot, ver), {})[s["name"]] = q
        r = s["r"] * KPC
        dv.append(0.5 * math.log10(float(np.interp(r, RG, Mb + Mt)) / float(np.interp(r, RG, Ml))))
    dv = np.abs(np.array(dv))
    return float(np.mean(dv < 0.03)), float(dv.max()), len(dv)


def sparc_rms_sw(foot, mode):
    gp = GPRED[foot].copy(); a0 = C7.A0_SI[foot]; ver, cap = mode
    for i, Mb in GMB.items():
        sel = np.where((GI == i) & ok4)[0]
        if not len(sel):
            continue
        o = np.argsort(Rm[sel]); sel = sel[o]
        rr = Rm[sel]
        Mtot = gp[sel] * rr ** 2 / GSI; Mbar = gb4[sel] * rr ** 2 / GSI
        Mph = np.maximum(gp[sel] - gb4[sel], 0.0) * rr ** 2 / GSI
        rta, Ml = RTA_G[foot][i]
        f = fprof_sparc(rr, Mb, a0, ver, 3 * Mtot / (4 * math.pi * rr ** 3), 3 * Mbar / (4 * math.pi * rr ** 3))
        f0 = 1.0 if ver == "one" else float(m_profile(np.array([1e30]), 1.0)[0])
        ff = np.concatenate([[f0], f])
        Msm = np.cumsum(0.5 * (ff[1:] + ff[:-1]) * np.diff(np.concatenate([[0.0], Mph])))
        if cap is not None and ver != "one":
            MtG = taper_on_RG(Mb, Ml, a0, ver)                       # the draw D on the point-mass profile to r_ta (cap factor)
            _, q = capped(MtG, rta, Ml, None)
            if q > 1 and cap == "uniform":
                Msm = Msm / q
            elif q > 1 and cap == "outer":
                Msm = np.minimum(Msm, (1.0 - LB.FB) * float(np.interp(rta, RG, Ml)))
        gp[sel] = gb4[sel] + GSI * Msm / rr ** 2
    return rms(gp)


SPA = {}
for foot in FOOTS:
    SPA[foot] = {}
    for k, mode in MODES.items():
        a3 = {kind: sparc_a3(kind, foot, mode) for kind in ("spiral", "dwarf")}
        rm = sparc_rms_sw(foot, mode)
        SPA[foot][k] = dict(A3_spiral=a3["spiral"][0], A3_dwarf=a3["dwarf"][0], maxdv_spiral=a3["spiral"][1], maxdv_dwarf=a3["dwarf"][1],
                            n_spiral=a3["spiral"][2], n_dwarf=a3["dwarf"][2], drms=rm - RMS0[foot])
    P(f"\n  [{foot}] row            | A3 spiral  A3 dwarf | max|dv| sp / dw | d rms")
    for k, r_ in SPA[foot].items():
        P(f"    {k:15s}| {r_['A3_spiral']:8.3f} {r_['A3_dwarf']:9.3f} | {r_['maxdv_spiral']:.4f} / {r_['maxdv_dwarf']:.4f} | {r_['drms']:+.5f}")
    for ver in ("V1", "V2"):
        q = np.array(list(QS[(foot, ver)].values()))
        SPA[foot][f"q_raw_{ver}"] = dict(median=float(np.median(q)), max=float(q.max()), frac_binds=float(np.mean(q > 1)))
        P(f"    q_raw = D/C ({ver}, P3 rows): median {np.median(q):.4f}, max {q.max():.4f}; cap binds for {np.mean(q > 1):.4f}")
RES["sparc"] = SPA
RES["rms0"] = RMS0
c39 = json.load(open(os.path.join(LANES, "CFG39_harness_with_rule_results.json")))["numbers"]["sparc"]
c3 = all(SPA[f]["C3_one_noedge"]["A3_spiral"] == 1.0 and SPA[f]["C3_one_noedge"]["A3_dwarf"] == 1.0 and abs(SPA[f]["C3_one_noedge"]["drms"]) < 1e-12
         for f in FOOTS) and abs(RMS0["canonical"] - c39["rms0"]) < 1e-9
check("C3 SPARC harness: m = 1, no edge leaves A3 = 100% and d rms = 0; rms0 equals CFG39's", c3,
      f"rms0 {RMS0['canonical']:.9f} vs CFG39 {c39['rms0']:.9f}; " + ", ".join(f"{f} A3 {SPA[f]['C3_one_noedge']['A3_spiral']:.2f}/{SPA[f]['C3_one_noedge']['A3_dwarf']:.2f} drms {SPA[f]['C3_one_noedge']['drms']:+.1e}" for f in FOOTS))


def sparc_pass(row):
    return all(SPA[f][row]["A3_spiral"] >= 0.90 and SPA[f][row]["A3_dwarf"] >= 0.90 and abs(SPA[f][row]["drms"]) < 0.005 for f in FOOTS)


for v in ("V1", "V2"):
    ok = sparc_pass(f"{v}_cap")
    RES[f"sparc_pass_{v}"] = ok
    check(f"(c) SPARC {v} capped taper: S-A3 >= 90% (spirals, dwarfs) and |d rms| < 0.005, both footings", ok,
          ", ".join(f"{f} A3 {SPA[f][f'{v}_cap']['A3_spiral']:.3f}/{SPA[f][f'{v}_cap']['A3_dwarf']:.3f} drms {SPA[f][f'{v}_cap']['drms']:+.4f}" for f in FOOTS),
          load_bearing=False)
if not MUTATE:
    c2s = all(SPA[f][f"{v}_nocap"][k] == J487["sparc"][f][f"{v}_noedge"][k] for f in FOOTS for v in ("V1", "V2") for k in ("A3_spiral", "A3_dwarf")) and \
        max(abs(SPA[f][f"{v}_nocap"]["drms"] - J487["sparc"][f][f"{v}_noedge"]["drms"]) for f in FOOTS for v in ("V1", "V2")) < 1e-9
    check("C2 SPARC: the uncapped rows equal CFG487's switch-only A3 exactly and d rms within 1e-9", c2s,
          ", ".join(f"{f} {v} A3 {SPA[f][f'{v}_nocap']['A3_dwarf']:.3f} vs {J487['sparc'][f][f'{v}_noedge']['A3_dwarf']:.3f}" for f in FOOTS for v in ("V1", "V2")))
RES["sparc_pass_rows"] = {k: sparc_pass(k) for k in MODES}
RES["kids_pass_rows"] = {k: all(KID[f]["rows"][k]["d_vs_best"] <= 4.0 for f in FOOTS) for k in KID["canonical"]["rows"]}
P("\n  reported pass map (SPARC rule / KiDS rule) per row:")
for k in MODES:
    if k in RES["kids_pass_rows"]:
        P(f"    {k:15s} SPARC {'PASS' if RES['sparc_pass_rows'][k] else 'FAIL'}   KiDS {'PASS' if RES['kids_pass_rows'][k] else 'FAIL'}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n  {sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; load-bearing (controls) failures: {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg498_data_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg498_data{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if nlb else 0)
