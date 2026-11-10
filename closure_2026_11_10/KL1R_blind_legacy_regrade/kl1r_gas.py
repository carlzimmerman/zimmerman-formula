#!/usr/bin/env python3
"""KL1R (FROZEN_CRITERIA.md 1792bd07ea, section 2.4): RB1's gas inside R500, my own move of CO1's cluster-regime layout.
CO1's co1_hm.py is executed up to its results block (CFG556's library and CO1's layout / set_population / ratios, unchanged).
In the group / cluster regime only, the gas cumulative inside R500 is scaled so that stars + gas inside R500 = f_ret x the layout's
own baryons inside R500; the removed mass is laid between R500 and R_out with M(<r) linear in r; the phantom and cold terms are
computed from the unmoved baryons. R' = 1 + (P_B' - P_Lta) / P_std (z 0).

  nice -n 15 python3 kl1r_gas.py     -> parts/gas.json, kl1r_gas.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list."""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed"); SRC = os.path.join(CO1D, "co1_hm.py")
code = open(SRC).read(); cut = code.index("RES = dict(lane=\"CO1\"")
NS = {"__file__": SRC, "__name__": "co1_hm_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), NS)
L = NS["L"]; layout, set_population, is_cluster, v_vir, phantom = (NS[k] for k in ("layout", "set_population", "is_cluster", "v_vir", "phantom"))
VST, CS_IGM, XSH = NS["VST"], NS["CS_IGM"], NS["XSH"]
h, FB, A0MPC, KK = L["h"], L["FB"], L["A0MPC"], L["KK"]
m_nfw, M_L, rgrid = L["m_nfw"], L["M_L"], L["rgrid"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
FOOTS = ("canonical", "alt")
HM = json.load(open(os.path.join(CO1D, "co1_hm.json")))
RB1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems", "rb1.json")))
LADDER = np.array([13.25, 13.75, 14.25, 14.75, 15.25]); FQ = np.array([0.674, 0.592, 0.800, 0.920, 1.095])
tab = RB1["gate2"]["canonical"]["extended_GS4"]["median_fret_gas_by_mass"]
FRB1 = np.array([tab[k]["kvm"] for k in ("13.0-13.5", "13.5-14.0", "14.0-14.5", "14.5-15.0", "15.0-15.5")])
P(f"RB1 kvm ladder from rb1.json: {np.round(FRB1, 4).tolist()} (criteria quote {FQ.tolist()}; max diff {np.max(np.abs(FRB1 - FQ)):.4f})")
FMODES = {"ladder": lambda lm: min(float(np.interp(lm, LADDER, FRB1)), 1.0),
          "powerlaw": lambda lm: min(0.592 + 0.160 * (lm - 13.75), 1.0),
          "one": lambda lm: 1.0, "MA3_0.2": lambda lm: 0.2}

def r500_of(hb, r0, M0):
    t = 2.5 * hb["M200c"] / hb["r200c"] ** 3          # 500 rho_c (4 pi / 3) per r^3
    g = lambda x: np.interp(x, r0, M0) / x ** 3 - t
    return brentq(g, 1e-3 * hb["r200c"], hb["r200c"] * 1.5, xtol=1e-12 * hb["r200c"])

def layout_gas(hb, foot, fmode="ladder", edge="rta", insert=True, info=None):
    if not is_cluster(hb, foot, "vstiff"):
        return layout(hb, foot, mode="B")
    a0 = A0MPC[foot]; rta, Mta = hb["rta"], hb["Mta"]; R2, M2 = hb["r200c"], hb["M200c"]
    r0, M0, _ = layout(hb, foot, mode="B")
    R5 = r500_of(hb, r0, M0); M5 = float(np.interp(R5, r0, M0)); lm5 = math.log10(M5 / h)
    f = FMODES[fmode](lm5); Rout = rta if edge == "rta" else R2
    r = rgrid(hb, rta); r = np.unique(np.concatenate([r, [R2]] + ([[R5, Rout]] if insert else []))); r = r[r <= rta * (1 + 1e-14)]
    ML = M_L(hb, r)
    Ms = M2; Mbs = FB * Ms; share = (1 - FB) * Ms
    ms = min(L["mstar"](hb), Mbs); mg = Mbs - ms
    a = 0.015 * R2 / (1 + math.sqrt(2)); rc = 0.1 * R2
    hs = lambda x: x ** 2 / (x + a) ** 2; gb = lambda x: x / rc - np.arctan(x / rc)
    rr = np.minimum(r, R2); st = ms * hs(rr) / hs(R2); gas = mg * gb(rr) / gb(R2); mb = st + gas
    st5 = ms * hs(min(R5, R2)) / hs(R2); gas5 = mg * gb(min(R5, R2)) / gb(R2)
    gnew5 = f * (st5 + gas5) - st5; flag = gnew5 < 0
    gnew5 = max(gnew5, 0.0); s = gnew5 / gas5 if gas5 > 0 else 1.0; dM = gas5 - gnew5
    if dM != 0.0:
        ramp = np.clip((r - R5) / (Rout - R5), 0.0, 1.0)
        gas2 = np.where(r <= R5, s * gas, gas - dM + dM * ramp)
    else: gas2 = gas
    mb2 = st + gas2
    outside = np.where(r > R2, ML - M2, 0.0); nfw_in = m_nfw(rr / hb["rs"]) / m_nfw(R2 / hb["rs"])
    v = v_vir(hb); fc = min(max(0.5 * (1 - (VST[foot] / v) ** 2), 0.0), 1.0)
    W = 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2); E = (1 - fc) * share
    ph_raw = W * phantom(mb, r, a0, "simple"); ph = np.minimum(ph_raw, E); rem = max(E - float(ph[-1]), 0.0)
    M = mb2 + fc * share * nfw_in + ph + rem * r / rta + outside
    if info is not None: info.append(dict(logM500=lm5, f_ret=f, s=s, dM_over_Mb=dM / Mbs, flag_all_gas_removed=bool(flag), R500_over_R200c=R5 / R2))
    return r, M, dict(regime="cluster")

def R_of(foot, **kw):
    infos = []
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UB, _ = L["U_set"](lambda hb: layout_gas(hb, foot, info=infos, **kw)); PB, _, _ = L["spectra_ta"](UB)
    return 1 + (PB - PLta) / Pstd, infos

set_population()
RES = dict(lane="KL1R", part="gas (B3 / A3)", criteria="1792bd07ea", k=KK.tolist(), note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list",
           RB1_kvm=FRB1.tolist(), KA3={}, R={}, MA3={}, layout_rows={})
KSEL = (0.3, 0.5, 1.0, 2.0, 3.0, 5.0)
for ft in FOOTS:
    Rst = np.array(HM["primary"][ft]["R_tot"])
    Ri, _ = R_of(ft, fmode="one", insert=False); Rii, _ = R_of(ft, fmode="one", insert=True)
    m10 = KK <= 10.0
    e1 = float(np.max(np.abs(Ri - Rst))); e2 = float(np.max(np.abs(Rii[m10] / Rst[m10] - 1)))
    # (iii) every modified layout conserves M(<r_ta) and is non-decreasing
    worst = 0.0; mono = True
    for hb in L["HB"]:
        for kw in (dict(), dict(edge="r200c"), dict(fmode="powerlaw"), dict(fmode="MA3_0.2")):
            r, M, _ = layout_gas(hb, ft, **kw)
            worst = max(worst, abs(M[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(M) >= -1e-9 * hb["Mta"]))
    RES["KA3"][ft] = dict(i_max_abs=e1, ii_max_rel_k_le_10=e2, iii_max_rel_mass=worst, iii_monotone=mono,
                         pass_=bool(e1 <= 1e-9 and e2 <= 2e-3 and worst <= 1e-9 and mono))
    P(f"[{ft}] KA3 (i) f_ret 1, no inserted points vs CO1's stored R_tot: {e1:.1e} (1e-9); (ii) with inserted points: {e2:.1e} (2e-3); "
      f"(iii) mass {worst:.1e}, monotone {mono} -> {'PASS' if RES['KA3'][ft]['pass_'] else 'FAIL'}")
    out = {}
    for name, kw in (("rta_ladder", dict()), ("r200c_ladder", dict(edge="r200c")), ("rta_powerlaw", dict(fmode="powerlaw")), ("MA3_rta_0.2", dict(fmode="MA3_0.2"))):
        R, inf = R_of(ft, **kw); out[name] = R.tolist()
        if name == "rta_ladder": RES["layout_rows"][ft] = inf
        P(f"  {name:14s} R / R_CO1 at k " + "  ".join(f"{k:g}: {np.interp(k, KK, R) / np.interp(k, KK, Rst):.4f}" for k in KSEL)
          + f" | R(k 1) {np.interp(1.0, KK, R):.4f} (CO1 {np.interp(1.0, KK, Rst):.4f}); all-gas-removed flags {sum(i['flag_all_gas_removed'] for i in inf)} of {len(inf)} cluster-regime halos")
    RES["R"][ft] = out
    d1 = float(np.interp(1.0, KK, np.array(out["MA3_rta_0.2"])) - np.interp(1.0, KK, Rst))
    RES["MA3"][ft] = dict(dR_k1=d1, R_part_bites=bool(abs(d1) >= 0.05))
    P(f"  MA3 (R part) f_ret 0.2: R(k 1) moves by {d1:+.4f} (needs |.| >= 0.05) -> {'bites' if abs(d1) >= 0.05 else 'DOES NOT BITE'}   ({time.time() - T0:.0f} s)")
    lr = RES["layout_rows"][ft]
    for lm in (13.0, 13.5, 14.0, 14.5, 15.0):
        j = int(np.argmin([abs(i["logM500"] - lm) for i in lr])); i = lr[j]
        P(f"     log M500 {i['logM500']:.2f}: f_ret {i['f_ret']:.3f}, gas scale s {i['s']:.3f}, moved {i['dM_over_Mb']:.3f} of the baryons, R500/R200c {i['R500_over_R200c']:.3f}")
RES["KA_ok"] = bool(all(v["pass_"] for v in RES["KA3"].values()))
json.dump(RES, open(os.path.join(HERE, "parts", "gas.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1r_gas.out"), "w").write("\n".join(OUT) + "\n")
P(f"done ({time.time() - T0:.0f} s)")
