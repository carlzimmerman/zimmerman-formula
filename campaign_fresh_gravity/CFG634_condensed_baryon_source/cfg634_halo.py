#!/usr/bin/env python3
"""CFG634 T5 (FROZEN_CRITERIA.md, 1fea20013): CFG556's resolution-free halo model with the phantom sourced by CONDENSED baryons only.
CONTEXT ONLY: Tinker08 mass function, Tinker10 bias, Duffy08 concentrations and Moster13 stars are LCDM-inherited (as in CFG556).
No native verdict; the native test is the PM shear run specified in the README.

CFG556's source (up to its run section) is exec'd read-only. The H-CB profile changes ONE thing: the phantom term uses the condensed
baryons, M_in(r) = m_b(r) + m_c(r) [nu(G m_c / r^2 a0) - 1]. Baryons are placed exactly as in CFG556 (truncated at B's census edge for
'cen'; untruncated for 'emg'). Condensed = stars (Moster13, Hernquist) + the cold share of the gas (gas shape), with
M_c = max(M*, 0.10 f_b M_ta) capped at the retained baryons (HC-1; 0.10 = census floor = stars + cold gas) or M_c = M* wherever
f_ret > 0.10 (HC-2). The H-CB settling edge is the census formula with the condensed source, r_e = r_M,c / ln(1 + M_c / supply)
('cen'), or where the condensed phantom exhausts the supply ('emg'), capped at r_ta; the unsettled remainder is handled as in CFG556.
MUTATE in the same pass: M1 condensed = all retained baryons reproduces CFG556; M3 teeth (|dR(k=1)| >= 0.01).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG634_condensed_baryon_source/cfg634_halo.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
SRC556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
try:
    os.nice(10)
except OSError:
    pass
os.environ["CFG556_MUTATE"] = "0"
src = open(SRC556).read()
mk = 'FOOTS = ("canonical", "alt")'
assert src.count(mk) == 1
NS = {"__file__": SRC556, "__name__": "cfg556_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(mk)], "cfg556_ro", "exec"), NS)
LOG, CHK = [], {}
RES = {"lane": "CFG634", "script": "cfg634_halo", "criteria": "1fea20013", "label": "CONTEXT ONLY (LCDM-inherited halo-model machinery)"}
FOOTS = ("canonical", "alt")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run from")[0].strip())
h, FB, G, A0MPC, nu_k = NS["h"], NS["FB"], NS["G"], NS["A0MPC"], NS["nu_k"]
rgrid, M_L, fret_of, mstar = NS["rgrid"], NS["M_L"], NS["fret_of"], NS["mstar"]
HB, MTA, KK, U_of, summarize = NS["HB"], NS["MTA"], NS["KK"], NS["U_of"], NS["summarize"]
frame_profile = NS["frame_profile"]


def cum_parts(hb, Mb, Mc, r, Rt):
    """retained baryons m_b(r) exactly as CFG556's baryon_cum, and the condensed part m_c(r): stars + cold share of the gas."""
    ms = min(mstar(hb), Mb); mg = Mb - ms
    a = 0.015 * hb["r200c"] / (1 + math.sqrt(2)); rc = 0.1 * hb["r200c"]
    rr = np.minimum(r, Rt)
    hs = lambda x: x ** 2 / (x + a) ** 2
    gb = lambda x: x / rc - np.arctan(x / rc)
    s_st = ms * hs(rr) / hs(Rt); s_g = gb(rr) / gb(Rt)
    mb = s_st + mg * s_g
    if Mc >= Mb * (1 - 1e-15):
        return mb, mb.copy(), ms
    if Mc <= ms:                       # condensed = stars only (HC-2 or stars above the floor)
        return mb, ms * hs(rr) / hs(Rt) * (Mc / ms), ms
    return mb, s_st + (Mc - ms) * s_g, ms


def frame_hcb(hb, foot, edge="cen", cmode="HC1", src="cond", spread=False):
    r = rgrid(hb, hb["rta"]); Mta = hb["Mta"]
    f = fret_of(math.log10(Mta)); Mb = f * FB * Mta; supply = (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)
    reB = min(rM / math.log1p(f * FB / (1 - FB)), hb["rta"])
    ms = min(mstar(hb), Mb)
    if src == "all":
        Mc = Mb
    elif cmode == "HC1":
        Mc = min(max(ms, 0.10 * FB * Mta), Mb)
    else:
        Mc = Mb if f <= 0.10 + 1e-12 else ms
    Rt = reB if edge == "cen" else hb["rta"]
    # H-CB settling edge
    if edge == "cen":
        rMc = math.sqrt(G * Mc * h / a0)
        re = rMc / math.log1p(Mc / supply)
    else:
        mb, mc, _ = cum_parts(hb, Mb, Mc, r, Rt)
        y = G * mc * h / (np.maximum(r, 1e-30) ** 2 * a0)
        S = np.where(r > 0, mc * (nu_k(y) - 1.0), 0.0)
        idx = np.nonzero(S >= supply)[0]
        if len(idx):
            i = idx[0]; re = r[i - 1] + (supply - S[i - 1]) * (r[i] - r[i - 1]) / (S[i] - S[i - 1])
        else:
            re = hb["rta"]
    capped = re >= hb["rta"]; re = min(re, hb["rta"])
    r = np.unique(np.concatenate([r, [re, reB]])); ML = M_L(hb, r)
    mb, mc, _ = cum_parts(hb, Mb, Mc, r, Rt)
    y = G * mc * h / (np.maximum(r, 1e-30) ** 2 * a0)
    Min = np.where(r > 0, mb + mc * (nu_k(y) - 1.0), 0.0)
    iout = np.searchsorted(r, re); Mout = Min[iout]; MLout = ML[iout]
    if spread:                         # POST-FREEZE bracket: unsettled remainder spread with the NFW shape at all radii (RN-like)
        Mset = np.where(r <= re, Min, Mout + (mb - mb[iout]))
        rem = max(Mta - Mset[-1], 0.0); MF = Mset + rem * ML / Mta; q = 0.0
    elif capped or MLout >= Mta * (1 - 1e-12):
        rem = max(Mta - Min[-1], 0.0); MF = Min + rem * ML / Mta; q = 0.0
    else:
        MF = np.where(r <= re, Min, Mout + (Mta - Mout) * (ML - MLout) / (Mta - MLout)); q = 1.0 - (Mta - Mout) / (Mta - MLout)
    return r, MF, dict(re=re, rout=re, q=q, capped=capped, fret=f, Mb=Mb, Mc=Mc, Mc_over_Mb=Mc / Mb, reB=reB)


def U_set(fn):
    U = np.empty((len(HB), len(KK))); infos = []
    for i, hb in enumerate(HB):
        r, Mc, inf = fn(hb); U[i] = U_of(r, Mc, KK); infos.append(inf)
    return U, infos


def run(name, fn):
    U, inf = U_set(fn)
    with contextlib.redirect_stdout(io.StringIO()):
        o = summarize(name, U, inf)
    P(f"  {name:28s} E {o['E']:+.3f} (k {o['kE']:.2f})  D {o['D']:+.3f}  R(0.3) {o['R_at']['0.3']:.3f}  R(1) {o['R_at']['1.0']:.3f}  "
      f"s8 ratio {o['s8_ratio']:.4f}  capped {o.get('n_capped', 0)}")
    return o, inf


J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))["cases"]
T5 = {}
for ft in FOOTS:
    P(f"\n[{ft}]")
    oB, _ = run(f"{ft}|M1 all-source cen", lambda hb: frame_hcb(hb, ft, "cen", src="all"))
    oBe, _ = run(f"{ft}|M1 all-source emg", lambda hb: frame_hcb(hb, ft, "emg", src="all"))
    oH, iH = run(f"{ft}|HCB HC1 cen (PRIMARY)", lambda hb: frame_hcb(hb, ft, "cen", "HC1"))
    oHe, _ = run(f"{ft}|HCB HC1 emg", lambda hb: frame_hcb(hb, ft, "emg", "HC1"))
    oH2, _ = run(f"{ft}|HCB HC2 cen", lambda hb: frame_hcb(hb, ft, "cen", "HC2"))
    oHs, _ = run(f"{ft}|HCB HC1 cen spread*", lambda hb: frame_hcb(hb, ft, "cen", "HC1", spread=True))
    oBs, _ = run(f"{ft}|B all-source cen spread*", lambda hb: frame_hcb(hb, ft, "cen", src="all", spread=True))
    # profile diagnostics
    prof = {}
    for lt in (12, 13, 14, 15):
        Mg = 10 ** np.interp(lt, np.log10(MTA), NS["LM"]); hb = NS["halo_basics"](Mg)
        out = {}
        for tag, kw in (("B", dict(src="all")), ("HCB", dict())):
            r, Mc, inf = frame_hcb(hb, ft, "cen", **kw)
            out[tag] = dict(ratio_0p3=float(np.interp(0.3 * hb["rta"], r, Mc) / M_L(hb, 0.3 * hb["rta"])),
                            ratio_0p1=float(np.interp(0.1 * hb["rta"], r, Mc) / M_L(hb, 0.1 * hb["rta"])),
                            re_over_rta=float(inf["re"] / hb["rta"]), Mc_over_Mb=float(inf["Mc_over_Mb"]), capped=bool(inf["capped"]))
        prof[str(lt)] = out
        P(f"    logM_ta {lt}: M_F/M_L at 0.1 / 0.3 r_ta  B {out['B']['ratio_0p1']:.2f} / {out['B']['ratio_0p3']:.2f} (r_e/r_ta {out['B']['re_over_rta']:.2f})"
          f"  H-CB {out['HCB']['ratio_0p1']:.2f} / {out['HCB']['ratio_0p3']:.2f} (r_e/r_ta {out['HCB']['re_over_rta']:.2f}, M_c/M_b {out['HCB']['Mc_over_Mb']:.2f})")
    EB = oB["E"]
    def cls(o):
        if o["E"] <= 0.10 and o["D"] >= -0.10:
            return "REMOVED"
        if o["E"] <= EB / 2:
            return "REDUCED"
        return "NOT REDUCED"
    T5[ft] = dict(B=oB, B_emg=oBe, HCB=oH, HCB_emg=oHe, HCB_HC2=oH2, HCB_spread_postfreeze=oHs, B_spread_postfreeze=oBs, profiles=prof,
                  class_primary=cls(oH), class_emg=cls(oHe), class_HC2=cls(oH2))
    for o in (oB, oBe, oH, oHe, oH2, oHs, oBs):
        for k in ("R", "R_ratio", "drivers"):
            o.pop(k, None)
    T5[ft]["class_spread_postfreeze"] = cls(oHs)
    P(f"  class (CONTEXT ONLY): primary {T5[ft]['class_primary']}, emg {T5[ft]['class_emg']}, HC-2 {T5[ft]['class_HC2']}; "
      f"post-freeze spread* {T5[ft]['class_spread_postfreeze']}  (* = POST-FREEZE reservoir bracket, reported, no verdict weight)")
m1 = max(abs(T5[ft]["B"]["E"] - J556[f"{ft}|census|cen"]["E"]) for ft in FOOTS)
m1e = max(abs(T5[ft]["B_emg"]["E"] - J556[f"{ft}|census|emg"]["E"]) for ft in FOOTS)
check("M1-T5 condensed = all retained baryons reproduces CFG556 primary E (1e-3)", m1 < 1e-3,
      ", ".join(f"{T5[ft]['B']['E']:+.4f}/{J556[f'{ft}|census|cen']['E']:+.4f}" for ft in FOOTS))
check("M1-T5e ... and CFG556's emergent-edge E (1e-3)", m1e < 1e-3,
      ", ".join(f"{T5[ft]['B_emg']['E']:+.4f}/{J556[f'{ft}|census|emg']['E']:+.4f}" for ft in FOOTS))
d3 = {ft: abs(T5[ft]["HCB"]["R_at"]["1.0"] - T5[ft]["B"]["R_at"]["1.0"]) for ft in FOOTS}
check("M3-T5 teeth: |R_HCB(k=1) - R_B(k=1)| >= 0.01", all(v >= 0.01 for v in d3.values()), ", ".join(f"{v:.3f}" for v in d3.values()))
RES["T5"] = T5
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, "cfg634_halo_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg634_halo.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
