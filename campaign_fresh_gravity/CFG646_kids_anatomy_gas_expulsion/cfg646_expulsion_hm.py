#!/usr/bin/env python3
"""CFG646 (ii) estimate 1: halo-model Delta P / P of the gravitating field when the census NON-RETAINED baryons
(1 - f_ret) f_b M_ta are moved out of each catchment (DECLARATIONS.md 3c1c5a42f).  CFG556's machinery is exec'd unchanged
(its library part); Tinker08 / Tinker10 / NFW-Duffy08 are CONTEXT-ONLY ingredients used only inside a ratio.

Per catchment (CFG556 primary: census f_ret, census edge, candidate B):
  core  M_c(<r) = retained baryons + the law's phantom inside the edge (CFG556 'Min'), constant beyond r_out;
  shell CFG556 puts Mta - Mout between r_out and r_ta with the NFW shape; Mta - Mout = (1 - f_ret) f_b M_ta + unsettled
        (the check below reports the split); the unsettled cold energy stays in the NFW-shaped shell in every case.
  BASE (what the PM does): the non-retained baryons are ordinary collisionless mass following the particle profile,
        primary 'from' shape NFW over the whole ball (bracket: the framework's own total profile M_F).
  DIFF (PRIMARY, CFG632): not in the halo; two-halo only with the host's bias (mass conserving, total bias 1).
  SHELL (bracket, CFG632): rho ~ r^-2 between r_edge and r_ta.   NFWSH (= CFG556 as written): NFW-shaped shell.
  DIFF-U (bracket, maximal removal): smooth, bias 0.
  RESOLVED-ONLY: DIFF applied only for M_ta >= the PM's resolved catchment mass (RMIN 0.78125 Mpc/h ball at Delta_ta).
Output R(k) = P_variant / P_BASE at z = 0.
  nice -n 10 python3 cfg646_expulsion_hm.py -> cfg646_expulsion_hm.out / .json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "4"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
os.environ["CFG556_MUTATE"] = "0"
G = {"__file__": os.path.abspath(SRC), "__name__": "cfg556_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
HB, MTA, W_M, BIAS, RHO_M, KK, PL, NORM_TA, FB = (G[k] for k in ("HB", "MTA", "W_M", "BIAS", "RHO_M", "KK", "PL", "NORM_TA", "FB"))
frame_profile, U_of, M_L, fret_of = G["frame_profile"], G["U_of"], G["M_L"], G["fret_of"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
KSEL = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 2.0, 3.0]
M_RES = (4 * math.pi / 3) * 0.78125 ** 3 * 11.81 * 0.315 * 2.775e11       # cfg596_pm M_ta(RMIN, Delta_ta(z=0))
P("CFG646 (ii) halo-model expulsion estimate (ratio to the PM-like BASE; z = 0). kappa = 1/2 FITTED; not theory closed.")
P(f"PM resolved-catchment mass M_ta >= {M_RES:.3e} Msun/h (RMIN 0.78125 Mpc/h)")
RES = dict(lane="CFG646", part="ii_halo_model", declarations="3c1c5a42f", k=KK.tolist(), M_res=M_RES, foot={})

def profiles(hb, foot, from_shape):
    r, MF, inf = frame_profile(hb, foot)
    Mta = hb["Mta"]; rout = inf["rout"]; iout = np.searchsorted(r, rout); Mout = MF[iout]
    ML = M_L(hb, r); MLout = ML[iout]
    core = np.where(r <= rout, MF, Mout)
    shellsh = np.where(r <= rout, 0.0, (ML - MLout) / max(Mta - MLout, 1e-300)); shellsh = np.minimum(shellsh, 1.0)
    eps = (1 - inf["fret"]) * FB; nonret_req = eps * Mta
    shell_tot = Mta - Mout; nonret = min(nonret_req, max(shell_tot, 0.0)); uns = shell_tot - nonret
    fromsh = ML / ML[-1] if from_shape == "NFW" else MF / MF[-1]
    rta = hb["rta"]; re = min(inf["re"], rta)
    r2sh = np.clip((r - re) / max(rta - re, 1e-300), 0.0, 1.0)
    base = core + uns * shellsh + nonret * fromsh
    out = dict(BASE=base, DIFF=core + uns * shellsh, SHELL=core + uns * shellsh + nonret * r2sh, NFWSH=core + uns * shellsh + nonret * shellsh)
    return r, out, dict(eps=eps, nonret=nonret, nonret_req=nonret_req, uns=uns, Mta=Mta)

LAST_I = {}
def spectra(U, diff_mass=None, diff_bias=True):
    p1 = np.sum(W_M[:, None] * (U / RHO_M) ** 2, 0)
    I = np.sum(W_M[:, None] * BIAS[:, None] * U / RHO_M, 0)
    if diff_mass is not None and diff_bias: I = I + np.sum(W_M * BIAS * diff_mass) / RHO_M
    I = I / NORM_TA
    LAST_I["I0"] = float(np.interp(1e-3, KK, I))
    return p1 + PL * I ** 2

for foot in ("canonical", "alt"):
    RES["foot"][foot] = {}
    for from_shape in ("NFW", "MF"):
        U = {k: np.empty((len(HB), len(KK))) for k in ("BASE", "DIFF", "SHELL", "NFWSH")}; info = []
        for i, hb in enumerate(HB):
            r, prof, inf = profiles(hb, foot, from_shape); info.append(inf)
            for k_ in U: U[k_][i] = U_of(r, prof[k_], KK)
        nonret = np.array([x["nonret"] for x in info]); req = np.array([x["nonret_req"] for x in info]); uns = np.array([x["uns"] for x in info])
        Pb = spectra(U["BASE"])
        res_k = lambda Pv: {str(kk): float(np.interp(kk, KK, Pv / Pb)) for kk in KSEL}
        resolved = MTA >= M_RES
        Ures = np.where(resolved[:, None], U["DIFF"], U["BASE"])
        var, Ichk = {}, {}
        for nm_, args in (("DIFF", (U["DIFF"], nonret)), ("SHELL", (U["SHELL"],)), ("NFWSH", (U["NFWSH"],)),
                          ("DIFF_U", (U["DIFF"], nonret, False)), ("DIFF_resolved_only", (Ures, np.where(resolved, nonret, 0.0)))):
            var[nm_] = spectra(*args); Ichk[nm_] = LAST_I["I0"]
        o = dict(R={k_: res_k(v) for k_, v in var.items()}, R_full={k_: (v / Pb).tolist() for k_, v in var.items()},
                 eps_at={f"{l:g}": float((1 - fret_of(l)) * FB) for l in (11, 12, 12.5, 13, 13.5, 14, 14.5, 15)},
                 nonret_shortfall_max=float(np.max((req - nonret) / np.maximum(req, 1e-300))), unsettled_frac_at={f"{l:g}": float(np.interp(l, np.log10(MTA), uns / MTA)) for l in (12, 13, 14, 15)},
                 I_check=Ichk)
        # mass-decade drivers of DIFF at k = 0.5 and 1 (one-halo + two-halo split, exact)
        drv = {}
        for kk in (0.5, 1.0):
            j = np.argmin(abs(KK - kk)); dtot = var["DIFF"][j] - Pb[j]
            d1 = W_M * ((U["DIFF"][:, j] / RHO_M) ** 2 - (U["BASE"][:, j] / RHO_M) ** 2)
            dec = {}
            for lo in range(8, 16):
                mm = (np.log10(MTA) >= lo) & (np.log10(MTA) < lo + 1); dec[f"{lo}-{lo + 1}"] = float(d1[mm].sum() / Pb[j])
            drv[str(kk)] = dict(dR=float(dtot / Pb[j]), one_halo_by_logMta=dec, two_halo=float((dtot - d1.sum()) / Pb[j]))
        o["drivers_DIFF"] = drv
        RES["foot"][foot][from_shape] = o
        P(f"\n[{foot}] from-shape {from_shape}: eps = (1-f_ret) f_b at log M_ta 12/13/14/15: " + " / ".join(f"{o['eps_at'][l]:.3f}" for l in ("12", "13", "14", "15"))
          + f"; shell shortfall vs required non-retained (max) {o['nonret_shortfall_max']:.3f}; unsettled/M_ta at 12/13/14/15: "
          + " / ".join(f"{v:.3f}" for v in o["unsettled_frac_at"].values()))
        for k_, v in o["R"].items():
            P(f"  {k_:20s} P'/P_BASE: " + "  ".join(f"{kk}:{x:.3f}" for kk, x in v.items()) + f"   (two-halo I(k=1e-3) {o['I_check'][k_]:.4f})")
        for kk, d in drv.items():
            P(f"  DIFF drivers k {kk}: dR {d['dR']:+.4f} = one-halo " + ", ".join(f"{m}:{x:+.4f}" for m, x in d["one_halo_by_logMta"].items() if abs(x) > 5e-4)
              + f" + two-halo {d['two_halo']:+.4f}")
json.dump(RES, open(os.path.join(HERE, "cfg646_expulsion_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg646_expulsion_hm.out"), "w").write("\n".join(OUT) + "\n")
