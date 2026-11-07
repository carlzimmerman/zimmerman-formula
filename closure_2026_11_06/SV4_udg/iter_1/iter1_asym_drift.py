"""SV4 iter_1: asymmetric drift in AGC 114905's thick gas disc, graded on the action's exact field (FROZEN_CRITERIA.md).

usage: python3 iter1_asym_drift.py [main|MUTATE]   MUTATE: AD with the wrong sign (V_c^2 = V_rot^2 - AD2(C1)).
kappa = 1/2 FITTED; not theory closed. Both footings, never pooled. One galaxy excludes nothing.
"""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import sv4_common as C

MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
P = C.Log(); RES = dict(mode=MODE); t0 = time.time()
P(f"SV4 iter_1 asymmetric drift, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")

ns = C.load_qx4(); ud1 = ns["ud1"]; rec = C.qx4_record()
Rk, Vc_pub, E = np.asarray(ud1["Rk"]), np.asarray(ud1["V"]), np.asarray(ud1["E"])
Vrot = np.asarray(ud1["Vr_k"]); AD2_pub = np.asarray(ud1["AD2"])
BL = (0.12, 0.56, 1.0)
mk = ud1["markers"](ud1["drk"], BL, 1.0, xmin=690); mk = mk[ud1["Xk"](mk[:, 0]) > 1.0]
eb = ud1["errbars"](ud1["drk"], BL, mk[:, 0])
Rs = ud1["Xk"](mk[:, 0]); sig = ud1["Yk"](mk[:, 1]); esig = 0.5 * (ud1["Yk"](eb[:, 0]) - ud1["Yk"](eb[:, 1]))
assert np.max(np.abs(Rs - ud1["Rk_k"])) < 1e-6
P(f"published (Mancera Pina+2024 plot_kinematics.pdf): R {np.round(Rk,3).tolist()} kpc")
P(f"  V_rot {np.round(Vrot,2).tolist()}  V_circ {np.round(Vc_pub,2).tolist()} +- {np.round(E,2).tolist()}")
P(f"  sigma_HI {np.round(sig,2).tolist()} +- {np.round(esig,2).tolist()} km/s; AD2_pub {np.round(AD2_pub,1).tolist()} (km/s)^2")
RES["inputs"] = dict(R=Rk.tolist(), Vrot=Vrot.tolist(), Vc=Vc_pub.tolist(), E=E.tolist(), sigma=sig.tolist(),
                     e_sigma=esig.tolist(), AD2_pub=AD2_pub.tolist())

kas = ud1["as2kpc"](ud1["D0"])
lnS = lambda R: np.log(np.clip(ud1["sig_gas"](R / kas), 1e-300, None))
eps = 1e-4
dlnSig = (lnS(Rk * np.exp(eps)) - lnS(Rk * np.exp(-eps))) / (2 * eps)
lnR = np.log(Rk)


def dlns2(s):
    l = np.log(s ** 2); d = np.empty_like(l)
    d[1:-1] = (l[2:] - l[:-2]) / (lnR[2:] - lnR[:-2]); d[0] = (l[1] - l[0]) / (lnR[1] - lnR[0])
    d[-1] = (l[-1] - l[-2]) / (lnR[-1] - lnR[-2]); return d


def steep(s, e):
    """Most negative slope of ln sigma^2 among central and the (k-1 high, k+1 low) 2-sigma pairs."""
    d = dlns2(s); out = d.copy()
    for k in range(len(s)):
        lo, hi = max(k - 1, 0), min(k + 1, len(s) - 1)
        a = np.log((s[lo] + 2 * e[lo]) ** 2) if lo != k else np.log(s[k] ** 2)
        b = np.log(max(s[hi] - 2 * e[hi], 1e-3) ** 2) if hi != k else np.log(s[k] ** 2)
        if lo == k: a = np.log((s[k] + 2 * e[k]) ** 2)
        if hi == k: b = np.log(max(s[k] - 2 * e[k], 1e-3) ** 2)
        out[k] = min(d[k], (b - a) / (lnR[hi] - lnR[lo]))
    return out


corners = {
    "C0_central": dict(pref=sig, slope=dlns2(sig), dlnh=0.0, in_errors=True),
    "C1_in_errors_max": dict(pref=sig + 2 * esig, slope=steep(sig, esig), dlnh=0.0, in_errors=True),
    "C2_generous_flaring": dict(pref=sig + 2 * esig, slope=steep(sig, esig), dlnh=1.0, in_errors=False),
}
AD2 = {}
for k, c in corners.items():
    S = -(dlnSig + c["slope"] - c["dlnh"]); AD2[k] = c["pref"] ** 2 * S
    P(f"{k}: slope factor S {np.round(S,2).tolist()}  AD2 {np.round(AD2[k],1).tolist()}")
RES["dlnSigma"] = dlnSig.tolist(); RES["AD2"] = {k: v.tolist() for k, v in AD2.items()}
ratio = AD2["C0_central"] / AD2_pub; kad = float(np.median(np.abs(np.log(ratio))))
P(f"KA-AD: C0 / published AD2 per ring {np.round(ratio,2).tolist()}; median |ln| {kad:.3f} (line ln2 = 0.693) -> "
  f"{'PASS' if kad <= np.log(2) else 'FAIL (tag)'}")
RES["KA_AD"] = dict(ratio=ratio.tolist(), median_abs_ln=kad, ok=bool(kad <= np.log(2)))

rho = ns["rho_agc"]
RES["footings"] = {}
for f, a0 in C.FOOT.items():
    F_top = C.Field(rho, 0.01, 3000.0, a0, C.RUNG_TOP); F_low = C.Field(rho, 0.01, 3000.0, a0, C.RUNG_LOW)
    Vm = F_top.midplane(Rk); ladder = float(np.max(np.abs(F_low.midplane(Rk) / Vm - 1)))
    Vq = np.asarray(rec["AGC114905"][f]["V_exact"]); ka0 = float(np.max(np.abs(Vm / Vq - 1)))
    c_unc, p_unc = C.chi2p(Vc_pub, E, Vm)
    P(f"\n[{f}] exact V {np.round(Vm,2).tolist()} (res {F_top.res:.1e}); ladder {ladder:.1e} (line 1e-2);"
      f" KA0 vs QX4 {ka0:.1e} (line 1e-3) -> {'PASS' if ka0 <= 1e-3 else 'FAIL'}; uncorrected chi2 {c_unc:.1f}"
      f" (QX4 {rec['AGC114905'][f]['chi2']:.1f})")
    row = dict(V_model=Vm.tolist(), ladder=ladder, KA0=ka0, chi2_uncorrected=c_unc, corners={})
    need = Vm ** 2 - Vrot ** 2
    row["AD2_needed"] = need.tolist()
    S0 = -(dlnSig + dlns2(sig)); row["sigma_needed_at_C0_slope"] = np.sqrt(np.maximum(need, 0) / np.maximum(S0, 1e-9)).tolist()
    P(f"   AD2 needed {np.round(need,0).tolist()} vs published {np.round(AD2_pub,0).tolist()};"
      f" sigma needed at C0's slope {np.round(row['sigma_needed_at_C0_slope'],1).tolist()} vs sigma_HI {np.round(sig,1).tolist()}")
    for k, c in corners.items():
        if MODE == "MUTATE" and k != "C1_in_errors_max": continue
        sgn = -1.0 if MODE == "MUTATE" else 1.0
        Vc = np.sqrt(np.maximum(Vrot ** 2 + sgn * AD2[k], 0)); En = E * np.maximum(Vc, 1e-3) / Vc_pub
        cc, pp = C.chi2p(Vc, En, Vm)
        lab = ("RESCUED" if c["in_errors"] else "rescued only outside published errors") if pp >= 0.05 else "NOT RESCUED"
        if ladder > 0.01: lab = "NO VERDICT (convergence)"
        row["corners"][k] = dict(Vc=Vc.tolist(), E=En.tolist(), chi2=cc, p=pp, label=lab)
        P(f"   {k}{' WRONG SIGN' if MODE=='MUTATE' else ''}: V_c {np.round(Vc,2).tolist()} chi2 {cc:.1f}/5 p {pp:.2e} -> {lab}")
    if MODE == "MUTATE":
        bite = row["corners"]["C1_in_errors_max"]["chi2"] > c_unc
        row["MUTATE_bites"] = bool(bite); P(f"   MUTATE bites (chi2 > uncorrected {c_unc:.1f}): {bite}")
    RES["footings"][f] = row

# Malin 1: NOT EVALUABLE (no sigma_HI on disk); requirement reported from the record's exact field (QX4 A2)
ud2 = ns["ud2"]; RT, VT = np.asarray(ud2["RT"]), np.asarray(ud2["VT"]); RES["Malin1"] = dict(label="NOT EVALUABLE")
for f in C.FOOT:
    Vq = np.asarray(rec["Malin1_A2"][f]["V_exact"]); need = Vq ** 2 - VT ** 2
    RES["Malin1"][f] = dict(AD2_needed=need.tolist(), sigma_needed_S3=np.sqrt(np.maximum(need, 0) / 3).tolist())
    P(f"\nMalin 1 [{f}] NOT EVALUABLE (no sigma_HI on disk); AD2 the data would need {np.round(need,0).tolist()}"
      f" (negative = the law is below the data); sigma at S = 3: {np.round(RES['Malin1'][f]['sigma_needed_S3'],1).tolist()}")
P(f"\nwall {time.time()-t0:.0f} s")
P.save(os.path.join(HERE, "iter1_MUTATE" if MODE == "MUTATE" else "iter1"), RES)
