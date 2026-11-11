#!/usr/bin/env python3
"""FRZ1 (FROZEN_CRITERIA.md, 1835d8fb7d): form B's redistribution R_cold(k, z) at the DESI P1D redshifts, both footings.
CFG556's halo-model library (campaign_fresh_gravity/CFG556_halo_model_matter_power/cfg556_halo_model.py, prefix up to its "run"
marker) is executed read-only; the population is re-evaluated at z (section 1 of the criteria). The layout functions are
copied from closure_2026_11_09/CO1_form_b_cosmology_computed/co1_hm.py (bar_cum, phantom, layout, ratios) with the only
changes the criteria name: a0 -> a0 / (1+z)^2 in comoving units, v_vir with (1+z), X by redshift, and the minimum-mass bracket.
  KA1 (z = 0 reproduces CO1's R_cold), KA4 (D(z) against CLASS), KA5 (mass conservation at z 3); MUTATE MZ2, MZ3.
  Checkpoints every case to frz1_hm_partial.json (restartable; SIGTERM exits cleanly).
  nice -n 19 python3 frz1_hm.py -> frz1_hm.json / .out, frz1_hm_MUTATE.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
os.environ["CFG556_MUTATE"] = "0"
L = {"__file__": SRC, "__name__": "cfg556_lib"}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), L)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
h, FB, RHO_M, G, A0MPC, LM, MM, KK, Om, DC = (L[k] for k in ("h", "FB", "RHO_M", "G", "A0MPC", "LM", "MM", "KK", "Om", "DC"))
m_nfw, rgrid, U_of, nu_k = (L[k] for k in ("m_nfw", "rgrid", "U_of", "nu_k"))
SIG0, PL0 = L["SIG"].copy(), L["PL"].copy()
FOOTS = ("canonical", "alt"); VST = {"canonical": 265.8, "alt": 288.1}; CS_IGM = 15.0
ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
_pd1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
XTAB = {f: {zk: float(np.median([r["share_over_Mb"] for r in _pd1[f]["share_tables"][zk]])) for zk in ("z0.0", "z1.0")} for f in FOOTS}

# ------------------------------------------------------------------ cosmology at z
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def Dgrow(z):
    E = lambda a: math.sqrt(Om / a ** 3 + 1 - Om)
    g = lambda a: E(a) * quad(lambda x: 1.0 / (x * E(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12)[0]
    return g(1 / (1 + z)) / g(1.0)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)

S = dict(z=0.0, D=1.0, xz0=False, mmin=0.0, a0raw=False)
def halo_basics_z(M, conc, dta, omz):
    c = conc(M); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / omz, 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)

def set_z(z, mf="tinker_z", cfac=1.0, cz=True, dta=None, xz0=False, mmin=0.0, a0raw=False):
    D = Dgrow(z) if z > 0 else 1.0
    S.update(z=z, D=D, xz0=xz0, mmin=mmin, a0raw=a0raw)
    SIG = SIG0 * D; L["PL"] = PL0 * D * D
    dlns = np.gradient(np.log(SIG), LM * math.log(10))
    if mf in ("tinker_z", "tinker0"):
        zz = z if mf == "tinker_z" else 0.0
        al = 10 ** (-(0.75 / math.log(200 / 75)) ** 1.2)
        A, a, b = 0.186 * (1 + zz) ** -0.14, 1.47 * (1 + zz) ** -0.06, 2.57 * (1 + zz) ** -al
        f = A * ((SIG / b) ** -a + 1) * np.exp(-1.19 / SIG ** 2)
        yD = math.log10(200.0)
        A10 = 1 + 0.24 * yD * math.exp(-(4 / yD) ** 4); a10 = 0.44 * yD - 0.88; B10, b10 = 0.183, 1.5
        C10 = 0.019 + 0.107 * yD + 0.19 * math.exp(-(4 / yD) ** 4); c10 = 2.4; NUP = DC / SIG
        BIAS = 1 - A10 * NUP ** a10 / (NUP ** a10 + DC ** a10) + B10 * NUP ** b10 + C10 * NUP ** c10
    else:                                                       # Press-Schechter, Mo-White bias
        nu = DC / SIG; f = math.sqrt(2 / math.pi) * nu * np.exp(-0.5 * nu ** 2); BIAS = 1 + (nu ** 2 - 1) / DC
    W_M = f * RHO_M / MM * (-dlns) * L["DLM"]
    conc = (lambda M: cfac * 10.14 * (M / 2e12) ** -0.081 * ((1 + z) ** -1.01 if cz else 1.0))
    L.update(W_M=W_M, BIAS=BIAS, A_MISS=1.0 - float(np.sum(W_M * BIAS * MM)) / RHO_M, conc=conc)
    dt = dta_of(z) if dta is None else dta
    L["HB"] = [halo_basics_z(M, conc, dt, Omz(z)) for M in MM]
    L["MTA"] = np.array([hb["Mta"] for hb in L["HB"]]); L["NORM_TA"] = float(np.sum(W_M * BIAS * L["MTA"])) / RHO_M
def M_L(hb, r): return hb["M"] * m_nfw(np.asarray(r) / hb["rs"]) / hb["mc"]

# ------------------------------------------------------------------ CO1's layout (copied), z-aware
def bar_cum(hb, Mbret, r, Rt, rc_fac=0.1):
    ms = min(L["mstar"](hb), Mbret); mg = Mbret - ms
    a = 0.015 * hb["r200c"] / (1 + math.sqrt(2)); rc = rc_fac * hb["r200c"]
    rr = np.minimum(r, Rt)
    hs = lambda x: x ** 2 / (x + a) ** 2
    gb = lambda x: x / rc - np.arctan(x / rc)
    return ms * hs(rr) / hs(Rt) + mg * gb(rr) / gb(Rt)
def phantom(mb, r, a0):
    return np.sqrt(0.25 * mb ** 2 + mb * r ** 2 * a0 / (G * h)) - 0.5 * mb
def a0c(foot): return A0MPC[foot] / (1.0 if S["a0raw"] else (1 + S["z"]) ** 2)
def v_vir(hb): return math.sqrt(G * hb["M200c"] * (1 + S["z"]) / hb["r200c"])
def Xsh(foot): return XTAB[foot]["z0.0"] if (S["z"] < 1 or S["xz0"]) else XTAB[foot]["z1.0"]

def layout(hb, foot, mode="B", pre=0.5, gal_scope="lag", clu_scope="r200c", rc_fac=0.1):
    a0 = a0c(foot); X = Xsh(foot); rta, Mta = hb["rta"], hb["Mta"]
    r = rgrid(hb, rta); ML = M_L(hb, r)
    if mode == "L" or hb["M"] < S["mmin"]:
        return r, ML.copy(), dict(regime="L")
    if not (v_vir(hb) > VST[foot]):
        Rs, Ms = (rta, Mta) if gal_scope == "lag" else (hb["r200"], hb["M"])
        Mcold = (1 - FB) * Ms; Mb = Mcold / X; rM = math.sqrt(G * Mb * h / a0); rt = math.sqrt(X * (X + 1)) * rM
        r = np.unique(np.concatenate([r, [min(rt, Rs), Rs]])); r = r[r <= rta * (1 + 1e-14)]; ML = M_L(hb, r)
        rin = np.minimum(r, Rs); shape = M_L(hb, rin) / Ms; outside = np.where(r > Rs, ML - Ms, 0.0)
        unc = (FB * Ms - Mb) * shape
        if mode == "Rb":
            return r, Mb + Mcold * shape + unc + outside, dict(regime="galaxy")
        ph = np.minimum(phantom(np.full_like(r, Mb), rin, a0), Mcold)
        rem = max(Mcold - float(ph[-1] if gal_scope == "lag" else np.interp(Rs, r, ph)), 0.0)
        return r, Mb + ph + rem * rin / Rs + unc + outside, dict(regime="galaxy")
    R2, M2 = hb["r200c"], hb["M200c"]
    Ms = M2 if clu_scope == "r200c" else Mta
    Mbs = FB * Ms; share = (1 - FB) * Ms
    r = np.unique(np.concatenate([r, [R2]])); ML = M_L(hb, r)
    rin = np.minimum(r, R2); mb = bar_cum(hb, Mbs, r, R2, rc_fac)
    outside = np.where(r > R2, ML - M2, 0.0) if clu_scope == "r200c" else 0.0
    nfw_in = m_nfw(rin / hb["rs"]) / m_nfw(R2 / hb["rs"])
    if mode == "Rb":
        return r, mb + share * nfw_in + outside, dict(regime="cluster")
    v = v_vir(hb); fc = min(max(pre * (1 - (VST[foot] / v) ** 2), 0.0), 1.0)
    W = 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2); E = (1 - fc) * share
    ph = np.minimum(W * phantom(mb, r, a0), E); rem = max(E - float(ph[-1]), 0.0)
    return r, mb + fc * share * nfw_in + ph + rem * r / rta + outside, dict(regime="cluster")

def ratios(foot, **opt):
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UB, infB = L["U_set"](lambda hb: layout(hb, foot, mode="B", **opt)); PB, _, _ = L["spectra_ta"](UB)
    optR = {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb", **optR)); PR, _, _ = L["spectra_ta"](UR)
    Rtot = 1 + (PB - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    ncl = sum(1 for i in infB if i["regime"] == "cluster")
    return Rtot, Rbar, Rtot / Rbar, ncl

# ------------------------------------------------------------------ checkpointed run
PART = os.path.join(HERE, "frz1_hm_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cases={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def at(R, ks=(1.0, 3.0, 5.0)): return [float(np.interp(k, KK, R)) for k in ks]

P(f"FRZ1 halo model at z. kappa = 1/2 FITTED; not theory closed. X (PD1) {XTAB}")
# KA1: z = 0 against CO1
CO1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed", "co1_hm.json")))
set_z(0.0); ka1 = {}
for ft in FOOTS:
    _, _, Rc, _ = ratios(ft); ref = np.array(CO1["primary"][ft]["R_cold"])
    ka1[ft] = float(np.max(np.abs(Rc / ref - 1)))
RES["KA1"] = dict(max_rel=ka1, pass_=bool(max(ka1.values()) <= 1e-10))
P(f"KA1 z = 0 against CO1's stored R_cold: max rel {ka1} -> {'PASS' if RES['KA1']['pass_'] else 'FAIL'}   [{time.time() - T0:.0f} s]")
# KA4: D(z) against CLASS
from classy import Class
Mc = Class(); Mc.set({'output': 'mPk', 'h': h, 'omega_b': 0.02237, 'omega_cdm': 0.1200, 'n_s': 0.965, 'A_s': 2.1e-9, 'N_ur': 3.046, 'z_max_pk': 5.0, 'P_k_max_1/Mpc': 2.0})
Mc.compute(); s80 = Mc.sigma(8 / h, 0.0); ka4 = {}
for z in (2.2, 3.0, 4.4):
    ka4[str(z)] = dict(mine=Dgrow(z), cls=Mc.sigma(8 / h, z) / s80); ka4[str(z)]["rel"] = ka4[str(z)]["mine"] / ka4[str(z)]["cls"] - 1
RES["KA4"] = dict(rows=ka4, pass_=bool(all(abs(v["rel"]) <= 5e-3 for v in ka4.values())))
P("KA4 D(z) / CLASS sigma8(z) ratio: " + "; ".join(f"z {k}: {v['mine']:.5f} / {v['cls']:.5f} ({v['rel']:+.2e})" for k, v in ka4.items()) + f" -> {'PASS' if RES['KA4']['pass_'] else 'FAIL'}")
# KA5 at z = 3
set_z(3.0); err = 0.0; mono = True
for ft in FOOTS:
    for hb in L["HB"]:
        for mode in ("B", "Rb"):
            for opt in (dict(), dict(gal_scope="vir"), dict(clu_scope="lag")):
                r, Mx, _ = layout(hb, ft, mode=mode, **opt)
                err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA5"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA5 z = 3 layouts: max |M(<r_ta) - M_ta| / M_ta {err:.1e}, non-decreasing {mono} -> {'PASS' if RES['KA5']['pass_'] else 'FAIL'}")
save()

CASES = [("primary", {}, {}), ("readingV", {}, dict(gal_scope="vir")), ("c_x0.7", dict(cfac=0.7), {}), ("c_x1.3", dict(cfac=1.3), {}),
         ("c_no_z", dict(cz=False), {}), ("tinker_no_z", dict(mf="tinker0"), {}), ("press_schechter", dict(mf="ps"), {}),
         ("dta_5.55", dict(dta=5.55), {}), ("dta_11.81", dict(dta=11.81), {}), ("X_z0", dict(xz0=True), {}), ("mmin_1e10", dict(mmin=1e10), {})]
for name, pz, opt in CASES:
    for ft in FOOTS:
        key = f"{name}|{ft}"
        if key in RES["cases"]: continue
        rows = {}
        for z in ZB:
            set_z(z, **pz); Rt, Rb, Rc, ncl = ratios(ft, **opt)
            rows[str(z)] = dict(R_cold=Rc.tolist(), R_tot_at=at(Rt), R_cold_at=at(Rc), n_cluster_regime=ncl)
        RES["cases"][key] = rows; save()
        P(f"  {name:16s} {ft:9s} R_cold at k 1/3/5: z 2.2 " + "/".join(f"{x:.4f}" for x in rows["2.2"]["R_cold_at"]) + "; z 3.0 "
          + "/".join(f"{x:.4f}" for x in rows["3.0"]["R_cold_at"]) + "; z 4.4 " + "/".join(f"{x:.4f}" for x in rows["4.4"]["R_cold_at"])
          + f"; cluster-regime masses at z 3: {rows['3.0']['n_cluster_regime']}   [{time.time() - T0:.0f} s]")
# MUTATE MZ2, MZ3 (z = 3, canonical)
MU = {}
set_z(3.0); _, Rb0, Rc0, _ = ratios("canonical"); Rt2, _, _, _ = ratios("canonical", clu_scope="lag")
s2 = float(np.interp(1.0, KK, Rt2 / Rb0)); p0 = float(np.interp(1.0, KK, Rc0))
MU["MZ2"] = dict(stat=s2, primary=p0, bites=bool(s2 - p0 >= 0.10))
set_z(3.0, a0raw=True); _, _, Rc3, _ = ratios("canonical"); d3 = float(np.interp(3.0, KK, Rc3) - np.interp(3.0, KK, Rc0))
MU["MZ3"] = dict(change_k3=d3, bites=bool(abs(d3) >= 0.005))
mtxt = [f"MZ2 cluster rule in the Lagrangian scope at z 3: R_tot / R_bar(primary) at k 1 {s2:.4f} against {p0:.4f} -> {'bites' if MU['MZ2']['bites'] else 'DOES NOT BITE'}",
        f"MZ3 a0 unscaled in comoving units at z 3: R_cold(k 3) changes by {d3:+.4f} -> {'bites' if MU['MZ3']['bites'] else 'DOES NOT BITE'}"]
for t in mtxt: P(t)
json.dump(dict(lane="FRZ1", MUTATE=MU, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "frz1_hm_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "frz1_hm_MUTATE.out"), "w").write("\n".join(mtxt) + "\n")
RES.update(lane="FRZ1", criteria="1835d8fb7d", k=KK.tolist(), z_bins=ZB, X=XTAB, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           KA_ok=bool(RES["KA1"]["pass_"] and RES["KA4"]["pass_"] and RES["KA5"]["pass_"]))
json.dump(RES, open(os.path.join(HERE, "frz1_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "frz1_hm.out"), "w").write("\n".join(OUT) + "\n")
os.remove(PART); P(f"done ({time.time() - T0:.0f} s)")
