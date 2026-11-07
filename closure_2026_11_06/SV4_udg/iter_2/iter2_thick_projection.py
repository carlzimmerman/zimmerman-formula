"""SV4 iter_2: thick-disc projection and non-circular motions (FROZEN_CRITERIA.md), on the action's exact field.

usage: python3 iter2_thick_projection.py [main|MUTATE]   MUTATE: (b) with the wrong sign (V x C_k) and (a+).
kappa = 1/2 FITTED; not theory closed. Both footings, never pooled. One galaxy excludes nothing.
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANE = os.path.dirname(HERE); sys.path.insert(0, LANE)
import sv4_common as C

MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
P = C.Log(); RES = dict(mode=MODE); t0 = time.time()
P(f"SV4 iter_2 thick-disc projection, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")
ns = C.load_qx4(); ud1 = ns["ud1"]; ud2 = ns["ud2"]; rec = C.qx4_record()
it1 = json.load(open(os.path.join(LANE, "iter_1", "iter1.json")))
Rk, Vc_pub, E = np.asarray(ud1["Rk"]), np.asarray(ud1["V"]), np.asarray(ud1["E"])
Vrot = np.asarray(ud1["Vr_k"]); AD2_pub = np.asarray(ud1["AD2"]); sig = np.asarray(it1["inputs"]["sigma"])
AD2_C1 = np.asarray(it1["AD2"]["C1_in_errors_max"])
I0, SI = 31.0, 2.0
RT, VT, ET = np.asarray(ud2["RT"]), np.asarray(ud2["VT"]), np.asarray(ud2["ET"]); IM = 38.0
kas, AMAX, hg = ns["kas"], ns["AMAX"], ns["hg"]


def rho_gas_agc(h):
    def f(R, z):
        S = np.where(R / kas < AMAX, np.clip(ns["sig_g"](R / kas), 0, None), 0) * 1e6
        return S * np.exp(-0.5 * (z / h) ** 2) / (np.sqrt(2 * np.pi) * h)
    return f


def rho_gas_malin(SF, h):
    return lambda R, z: SF["gas"](R) * np.exp(-0.5 * (z / h) ** 2) / (np.sqrt(2 * np.pi) * h)


def lab(p, in_err, ladder):
    if ladder > 0.01: return "NO VERDICT (convergence)"
    return ("RESCUED" if in_err else "rescued only outside published errors") if p >= 0.05 else "NOT RESCUED"


def inc_thick(i_deg, q0, direction):
    q = np.cos(np.radians(i_deg))
    if direction == "a+": return float(np.degrees(np.arccos(np.sqrt(max(q * q - q0 * q0, 0) / (1 - q0 * q0)))))
    return float(np.degrees(np.arccos(np.sqrt(q * q * (1 - q0 * q0) + q0 * q0))))


RES["AGC114905"] = {}; RES["Malin1"] = {}
for f, a0 in C.FOOT.items():
    # ------------------------------------------------ AGC 114905
    Ft = C.Field(ns["rho_agc"], 0.01, 3000.0, a0, C.RUNG_TOP); Fl = C.Field(ns["rho_agc"], 0.01, 3000.0, a0, C.RUNG_LOW)
    Vm = Ft.midplane(Rk); ladder = float(np.max(np.abs(Fl.midplane(Rk) / Vm - 1)))
    ka0 = float(np.max(np.abs(Vm / np.asarray(rec["AGC114905"][f]["V_exact"]) - 1))); c_unc, _ = C.chi2p(Vc_pub, E, Vm)
    P(f"\n[AGC {f}] exact V {np.round(Vm,2).tolist()}; ladder {ladder:.1e}; KA0 {ka0:.1e} -> {'PASS' if ka0 <= 1e-3 else 'FAIL'};"
      f" uncorrected chi2 {c_unc:.1f}")
    row = dict(V_model=Vm.tolist(), ladder=ladder, KA0=ka0, chi2_uncorrected=c_unc, a={}, b={}, d=None)
    # (a) thickness in the inclination
    for direction in (("a+",) if MODE == "MUTATE" else ("a+", "a-")):
        for q0, ine in ((0.10, True), (0.13, True), (0.30, False)):
            i = inc_thick(I0, q0, direction); s = np.sin(np.radians(I0)) / np.sin(np.radians(i))
            c, p = C.chi2p(Vc_pub * s, E * s, Vm); L = lab(p, ine, ladder)
            row["a"][f"{direction}_q{q0}"] = dict(i=i, chi2=c, p=p, label=L)
            P(f"   (a) {direction} q0 {q0:.2f}{'' if ine else ' GENEROUS'}: i {i:.2f} deg, chi2 {c:.1f} p {p:.1e} -> {L}")
    if MODE != "MUTATE":
        i = inc_thick(I0 - 2 * SI, 0.13, "a-"); s = np.sin(np.radians(I0)) / np.sin(np.radians(i))
        c, p = C.chi2p(Vc_pub * s, E * s, Vm); row["a"]["a-_q0.13_i27"] = dict(i=i, chi2=c, p=p, label=lab(p, True, ladder))
        P(f"   (a) a- q0 0.13 at i0 - 2 sigma: i {i:.2f}, chi2 {c:.1f} p {p:.1e} -> {row['a']['a-_q0.13_i27']['label']}")
    # (b) LOS through the thick layer on the exact field
    Ck = {}
    for hname, h, ine in (("h1.3", hg, True), ("h2.6", 2 * hg, False)):
        Ck[hname] = C.los_factor(Ft, rho_gas_agc(h), Rk, I0, h=h)
        fac = Ck[hname] if MODE == "MUTATE" else 1.0 / Ck[hname]
        Vc = np.sqrt((Vrot * fac) ** 2 + AD2_pub); En = E * Vc / Vc_pub; c, p = C.chi2p(Vc, En, Vm)
        row["b"][hname] = dict(C=Ck[hname].tolist(), Vc=Vc.tolist(), chi2=c, p=p, label=lab(p, ine, ladder))
        P(f"   (b){' WRONG SIGN' if MODE=='MUTATE' else ''} {hname}{'' if ine else ' GENEROUS'}: C_k {np.round(Ck[hname],4).tolist()};"
          f" V_c {np.round(Vc,2).tolist()} chi2 {c:.1f} p {p:.1e} -> {row['b'][hname]['label']}")
    # (c) non-circular: requirement only
    vnc = (np.sqrt(np.maximum(Vm ** 2 - AD2_pub, 0)) - Vrot) * np.sin(np.radians(I0)); row["c"] = dict(label="NOT EVALUABLE", v_nc_los_needed=vnc.tolist())
    P(f"   (c) NOT EVALUABLE; LOS non-circular amplitude needed {np.round(vnc,1).tolist()} km/s vs sigma_HI {np.round(sig,1).tolist()}")
    # (d) all at once
    if MODE != "MUTATE":
        i = inc_thick(I0 - 2 * SI, 0.13, "a-"); s = np.sin(np.radians(I0)) / np.sin(np.radians(i))
        Vc = np.sqrt((Vrot / Ck["h1.3"] * s) ** 2 + AD2_C1); En = E * Vc / Vc_pub; c, p = C.chi2p(Vc, En, Vm)
        row["d"] = dict(i=i, Vc=Vc.tolist(), chi2=c, p=p, label=lab(p, True, ladder))
        P(f"   (d) ALL AT ONCE (iter_1 C1 + a- q0 0.13 at 27 deg + b h1.3): V_c {np.round(Vc,2).tolist()} chi2 {c:.1f} p {p:.1e} -> {row['d']['label']}")
    if MODE == "MUTATE":
        bite = all(v["chi2"] > c_unc for v in row["b"].values()) and all(v["chi2"] > c_unc for v in row["a"].values())
        row["MUTATE_bites"] = bool(bite); P(f"   MUTATE bites (every wrong-sign row chi2 > {c_unc:.1f}): {bite}")
    RES["AGC114905"][f] = row
    # ------------------------------------------------ Malin 1 (b) on the A2 density; A1 beside
    rowm = {}
    for dname, SF in (("A2", ns["SIGF_A2"]), ("A1", ns["SIGF"])):
        Ft = C.Field(ns["rho_malin"](1.0, SF), 0.05, 3.0e4, a0, C.RUNG_TOP)
        Fl = C.Field(ns["rho_malin"](1.0, SF), 0.05, 3.0e4, a0, C.RUNG_LOW)
        Vm = Ft.midplane(RT); ladder = float(np.max(np.abs(Fl.midplane(RT) / Vm - 1)))
        key = "Malin1_A2" if dname == "A2" else "Malin1"
        ka0 = float(np.max(np.abs(Vm / np.asarray(rec[key][f]["V_exact"]) - 1))); c_unc, _ = C.chi2p(VT, ET, Vm)
        r_ = dict(V_model=Vm.tolist(), ladder=ladder, KA0=ka0, chi2_uncorrected=c_unc)
        P(f"[Malin {dname} {f}] exact V {np.round(Vm,2).tolist()}; ladder {ladder:.1e}; KA0 {ka0:.1e} -> {'PASS' if ka0 <= 1e-3 else 'FAIL'}; uncorrected chi2 {c_unc:.1f}")
        for hname, h, ine in (("h1", 1.0, True), ("h2", 2.0, False)):
            Ck = C.los_factor(Ft, rho_gas_malin(SF, h), RT, IM, h=h)
            fac = Ck if MODE == "MUTATE" else 1.0 / Ck
            Vc = VT * fac; En = ET * fac; c, p = C.chi2p(Vc, En, Vm)
            r_[hname] = dict(C=Ck.tolist(), Vc=Vc.tolist(), chi2=c, p=p, label=lab(p, ine, ladder))
            P(f"   (b){' WRONG SIGN' if MODE=='MUTATE' else ''} {hname}{'' if ine else ' GENEROUS'}: C_k {np.round(Ck,4).tolist()}; chi2 {c:.1f} p {p:.1e} -> {r_[hname]['label']}")
        if MODE == "MUTATE":
            r_["MUTATE_bites"] = bool(all(r_[h]["chi2"] > c_unc for h in ("h1", "h2"))); P(f"   MUTATE bites: {r_['MUTATE_bites']}")
        rowm[dname] = r_
    vnc = (np.asarray(rowm["A2"]["V_model"]) - VT) * np.sin(np.radians(IM))
    rowm["c"] = dict(label="NOT EVALUABLE", v_nc_los_needed=vnc.tolist())
    P(f"   Malin (c) NOT EVALUABLE; LOS non-circular amplitude needed (A2) {np.round(vnc,1).tolist()} km/s; (a) n/a: kinematic inclination")
    RES["Malin1"][f] = rowm
P(f"\nwall {time.time()-t0:.0f} s")
P.save(os.path.join(HERE, "iter2_MUTATE" if MODE == "MUTATE" else "iter2"), RES)
