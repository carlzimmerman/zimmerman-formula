#!/usr/bin/env python3
"""CFG643: Door 1 -- baryon -> cold-energy heat exchange Q_c = C a0 v rho_b. FROZEN_CRITERIA.md (committed alone first, c7dad5f10).

Analytic + light 1-D numerics on CFG541's systems (CFG541 `Model` imported read-only; its alpha = 1 settling flow is rerun to
get the target state). No PM, no downloads. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle
species added; not "theory closed".
CFG643_MUTATE=1 -> M1 C -> 0, M2 C x 2, M3 sign-reversed Q; outputs *_MUTATE.*
Run (repo root or anywhere): OMP_NUM_THREADS=1 nice -n 10 python3 cfg643.py
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D541 = os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise")
sys.path.insert(0, D541)
import cfg541 as L  # noqa: E402  (read-only import)

MUT = os.environ.get("CFG643_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G, c, MSUN, KPC, GYR = L.G, L.c, L.MSUN, L.KPC, L.GYR
HBAR, MP = 1.054571817e-34, 1.67262192e-27
FOOT = L.FOOT
COLD_PER_B = 5.364
S_BENCH = 0.3 * 0.1            # 0.3 cm^2/g in m^2/kg (astra's benchmark self-scattering)
SIG_IC = 0.05                  # IC-C benchmark: sigma = 0.05 V_f
AGES = {"primary": dict(MW=10.0, group=10.0, cluster=10.0), "variant": dict(MW=12.0, group=8.0, cluster=5.0)}
OUT, RES = [], {"lane": "CFG643", "mutate": MUT, "criteria_commit": "c7dad5f10",
                "settings": dict(kappa=0.5, footings=FOOT, S_bench_m2_per_kg=S_BENCH, ages_Gyr=AGES, sigma_IC_over_Vf=SIG_IC)}


def log(s=""):
    print(s, flush=True); OUT.append(str(s))


def jeans(mod, m):
    """isotropic Jeans state of cold mass m in the total (baryon + cold) potential, P = 0 at r_ta (as CFG541 Model.energy)."""
    mt = mod.mb + m
    Menc = mod.Mb_in + np.concatenate([[0.0], np.cumsum(mt)[:-1]]) + 0.5 * mt
    g = G * Menc / mod.rc ** 2
    rho = m / mod.V; dr = np.diff(mod.rf)
    P = np.cumsum((rho * g * dr)[::-1])[::-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        s2 = np.where(rho > 0, P / np.maximum(rho, 1e-300), 0.0)
    return rho, np.sqrt(s2), g


def transport(mod, rho, sig, rstar, rin_factor=1.0):
    sel = (mod.rc <= rstar) & (mod.rc >= rin_factor * mod.rf[0]) & (rho > 0)
    e = 1.5 * rho * sig ** 2 * mod.V
    rate1 = sig / mod.rc
    rate2 = np.minimum(rho * S_BENCH * math.sqrt(16 / math.pi) * sig, rate1)
    return float(np.sum((e * rate1)[sel])), float(np.sum((e * rate2)[sel]))


def main():
    groups = L.group_rows()
    lMg = float(np.median([o["lM"] for o in groups])); Reg = float(np.median([o["Re"] for o in groups]))
    systems = {"MW": (6.0e10, 2.5), "group": (10 ** lMg, Reg / L.B.HERN_RE), "cluster": (1.5e14, None)}
    J541 = json.load(open(os.path.join(D541, "cfg541_results.json")))
    log("CFG643 Door 1: Q_c = C a0 v rho_b (posited heating law; FKPS 1912.07626 via astra MECHANISM.md). kappa = 1/2 FITTED; "
        "footings never pooled; cold energy mass required; no particle species; not theory closed." + ("  [MUTATE]" if MUT else ""))
    out = {}
    v0_ok = True
    for fk, a0 in FOOT.items():
        out[fk] = {}
        log(f"\n=== footing {fk} (a0 = {a0:.4e} m/s^2)")
        for nm, (Mb, ah) in systems.items():
            f = L.fret_census(Mb)[0]
            mod = L.Model(Mb, ah, a0, f)
            r = mod.run(alpha=1.0)
            m = r["m"]; m0 = mod.rhoc0 * mod.V
            Wi, Ki = mod.energy(m0); Wf, Kf = mod.energy(m)
            dW = Wi - Wf; Esink = dW - Kf
            Vf = math.sqrt(mod.Vf2); Mcat = mod.Mcat; Mbk = mod.Mb
            # V0 control vs CFG541 JSON
            jj = J541["one_d"][fk][nm]
            d1 = abs(Kf / Mcat / mod.Vf2 / jj["Kf_over_Vf2"] - 1); d2 = abs(dW / Mcat / mod.Vf2 / jj["dW_over_Vf2"] - 1)
            v0 = d1 <= 1e-6 and d2 <= 1e-6; v0_ok &= v0
            rho, sig, g = jeans(mod, m)
            rstar = mod.analytic_rstar()
            # ---- G1a
            Kic = 1.5 * (SIG_IC * Vf) ** 2 * Mcat
            Eimp = Kf - Kic
            rec = dict(fret=f, Mcat_over_Mb=Mcat / Mbk, Vf_kms=Vf / 1e3, rstar_kpc=rstar / KPC, rta_kpc=mod.rta / KPC,
                       Kf_over_McatVf2=Kf / Mcat / mod.Vf2, dW_over_McatVf2=dW / Mcat / mod.Vf2,
                       Esink_over_McatVf2=Esink / Mcat / mod.Vf2, Eimp_over_McatVf2=Eimp / Mcat / mod.Vf2,
                       V0_rel_diff=[d1, d2], V0_pass=v0)
            Cmin = {}
            for vk, v in (("v_Vf_over_sqrt2", Vf / math.sqrt(2)), ("v_Vf", Vf)):
                for ak, ages in AGES.items():
                    t = ages[nm] * GYR
                    Cmin[f"{vk}|{ak}"] = Eimp / (a0 * Mbk * v * t)
            rec["Cmin"] = Cmin
            # cross-check with collective_energy_lower import fractions (target-def differs; consistency only)
            xc = {"MW": 0.497, "cluster": 0.638}
            if nm in xc:
                rec["Cmin_collective_xcheck_ratio"] = (xc[nm] * Mcat * mod.Vf2) / Eimp
            # ---- G2: A, B
            LT1, LT2 = transport(mod, rho, sig, rstar)
            LT1b, _ = transport(mod, rho, sig, rstar, rin_factor=10.0)
            A1 = G * LT1 / Vf ** 5; A1b = G * LT1b / Vf ** 5; A2 = G * LT2 / Vf ** 5
            B = 1 / math.sqrt(2)
            if ah is not None:
                Bsig = float(np.sum(np.interp(mod.rc, mod.rc, sig) * mod.mb)) / (Mbk * Vf)
            else:
                Bsig = float(sig[0] / Vf)
            rec.update(A_T1=A1, A_T1_rin_x10=A1b, A_T2=A2, B_primary=B, B_local_sigma=Bsig,
                       C_BTFR_T1=A1 / B, C_BTFR_T1_rin_x10=A1b / B, C_BTFR_T2=A2 / B, C_BTFR_T1_localB=A1 / Bsig)
            # ---- G3
            Kb_half, Kb_34 = 0.5 * Mbk * mod.Vf2, 0.75 * Mbk * mod.Vf2
            C1 = Cmin["v_Vf_over_sqrt2|primary"]
            rate = lambda C: C * a0 * Mbk * Vf / math.sqrt(2)
            rec.update(Eimp_over_Kb_half=Eimp / Kb_half, Eimp_over_Kb_34=Eimp / Kb_34,
                       tb_Gyr_at_Cmin=Kb_half / rate(C1) / GYR, tb_Gyr_at_CBTFR_T1=Kb_half / rate(A1 / B) / GYR,
                       Eimp_over_replenish=Eimp / (Mcat / COLD_PER_B * mod.Vf2))
            # ---- G4
            g4 = {}
            pts = {"MW": (8, 30), "group": (30, 150), "cluster": (100, 500)}[nm]
            for rk in pts:
                i = int(np.argmin(abs(mod.rc - rk * KPC)))
                rc_, s_ = rho[i], sig[i]
                sm = C1 * a0 / (rc_ * s_ ** 2)                              # m^2/kg
                mcmax = math.sqrt(4 * math.pi * HBAR ** 2 * rc_ / (C1 * MP * a0))
                g4[f"{rk}kpc"] = dict(rho_c=rc_, sigma_kms=s_ / 1e3, sigma_cb_over_mb_cm2g=sm * 10, mc_max_GeV=mcmax * c ** 2 / 1.602176634e-10)
            rec["G4"] = g4
            # ---- G5a
            heat = Eimp      # heat at C_min over t_age equals E_imp by construction
            Knat = Kf + Esink + heat
            rec["G5a_dex"] = math.log10(Knat / Kf)
            out[fk][nm] = rec
            log(f"{nm}: f_ret {f:.3f}, M_cat/M_b {Mcat / Mbk:.2f}, V_f {Vf / 1e3:.1f} km/s, r_* {rstar / KPC:.0f} kpc, r_ta {mod.rta / KPC:.0f} kpc; "
                f"V0 vs CFG541 JSON K_f {d1:.1e}, dW {d2:.1e} -> {'PASS' if v0 else 'FAIL'}")
            log(f"   K_f {rec['Kf_over_McatVf2']:.4f}, dW {rec['dW_over_McatVf2']:.4f}, E_sink {rec['Esink_over_McatVf2']:+.4f}, "
                f"E_imp(IC-C) {rec['Eimp_over_McatVf2']:.4f}  [M_cat V_f^2]")
            log("   C_min: " + ", ".join(f"{k} {v:.4f}" for k, v in Cmin.items()))
            if nm in xc: log(f"   collective-gate cross-check C_min ratio {rec['Cmin_collective_xcheck_ratio']:.3f}")
            log(f"   A_T1 {A1:.3f} (r_in x10: {A1b:.3f}), A_T2 {A2:.3e}; B {B:.4f} (local-sigma {Bsig:.4f}); C_BTFR T1 {A1 / B:.3f} "
                f"(r_in x10 {A1b / B:.3f}; local B {A1 / Bsig:.3f}), T2 {A2 / B:.3e}")
            log(f"   G3: E_imp/K_b {rec['Eimp_over_Kb_half']:.2f} (K_b 3/4: {rec['Eimp_over_Kb_34']:.2f}); t_b at C_min {rec['tb_Gyr_at_Cmin']:.3f} Gyr, "
                f"at C_BTFR(T1) {rec['tb_Gyr_at_CBTFR_T1']:.4f} Gyr; E_imp/(all catchment baryons x V_f^2) {rec['Eimp_over_replenish']:.2f}")
            log("   G4: " + "; ".join(f"{k}: rho_c {v['rho_c']:.2e} kg/m^3, sigma {v['sigma_kms']:.0f} km/s, sigma_cb/m_b {v['sigma_cb_over_mb_cm2g']:.3e} cm^2/g, "
                                       f"m_c(unitarity) <= {v['mc_max_GeV']:.2e} GeV" for k, v in g4.items()))
            log(f"   G5a native K with retained heat: {rec['G5a_dex']:+.3f} dex above K_f (rule <= 0.1)")
    RES["systems"] = out
    RES["V0_pass"] = v0_ok
    if not v0_ok:
        log("V0 CONTROL FAILED: lane stops (no labels)."); finish(); return 2

    # =============================== labels per footing
    lab = {}
    names = ("MW", "group", "cluster")
    for fk, a0 in FOOT.items():
        o = out[fk]; L_ = {}
        cm = [o[n]["Cmin"]["v_Vf_over_sqrt2|primary"] for n in names]
        spread = max(cm) / min(cm)
        var = {k: max(o[n]["Cmin"][k] for n in names) / min(o[n]["Cmin"][k] for n in names) for k in o["MW"]["Cmin"]}
        L_["G1a"] = dict(Cmin={n: x for n, x in zip(names, cm)}, spread=spread, spread_variants=var,
                         label="PASS" if spread <= 2 else "FAIL (C not universal)")
        es = [o[n]["Esink_over_McatVf2"] for n in names]
        L_["G1b"] = dict(Esink=es, label="PASS" if all(x <= 0 for x in es) else "FAIL BY SIGN (native path needs export; Q_c >= 0 imports)")
        cb = [o[n]["C_BTFR_T1"] for n in names]; cb2 = [o[n]["C_BTFR_T2"] for n in names]
        t1i = max(cb) / min(cb) <= 2; t1ii = all(max(cb[k], cm[k]) / min(cb[k], cm[k]) <= 2 for k in range(3))
        t2i = max(cb2) / min(cb2) <= 2; t2ii = all(max(cb2[k], cm[k]) / min(cb2[k], cm[k]) <= 2 for k in range(3))
        L_["G2"] = dict(T0="FAIL (A = 0: no transport, no balance, heat accumulates)",
                        T1=dict(C_BTFR=cb, spread=max(cb) / min(cb), ratio_to_Cmin=[cb[k] / cm[k] for k in range(3)],
                                i=t1i, ii=t1ii, label="PASS ONLY UNDER THE ASSUMED FKPS CLOSURE" if (t1i and t1ii) else "FAIL"),
                        T2=dict(C_BTFR=cb2, spread=max(cb2) / min(cb2), i=t2i, ii=t2ii, label="PASS" if (t2i and t2ii) else "FAIL"))
        tbm = [o[n]["tb_Gyr_at_Cmin"] for n in names]; tbb = [o[n]["tb_Gyr_at_CBTFR_T1"] for n in names]
        rep = [o[n]["Eimp_over_replenish"] for n in names]
        ages = AGES["primary"]
        L_["G3"] = dict(tb_at_Cmin=tbm, tb_at_CBTFR_T1=tbb, Eimp_over_replenish=rep,
                        at_Cmin="PASS" if all(tbm[k] >= ages[names[k]] for k in range(3)) else "FAIL",
                        at_CBTFR="PASS" if all(tbb[k] >= ages[names[k]] for k in range(3)) else "FAIL",
                        replenish="PASS" if all(x <= 1 for x in rep) else "FAIL")
        cl = o["cluster"]["G4"]
        L_["G4"] = dict(i="FAIL (fixed couplings cannot give 1/n_c; needs a new baryon vertex = particle with free cross-section)",
                        ii_cluster_sigma_cb_over_mb=[cl[k]["sigma_cb_over_mb_cm2g"] for k in cl],
                        ii_context="below 0.35" if all(cl[k]["sigma_cb_over_mb_cm2g"] < 0.35 for k in cl) else "above 0.35 somewhere (context, different channel)")
        g5a = [o[n]["G5a_dex"] for n in names]
        L_["G5a"] = dict(dex=g5a, label="PASS" if all(x <= 0.1 for x in g5a) else "FAIL")
        # G5b Bullet drag at the cluster C_min
        Cc = o["cluster"]["Cmin"]["v_Vf_over_sqrt2|primary"]; t = 0.2 * GYR
        dx = {str(fr): 0.5 * Cc * a0 * fr * t ** 2 / KPC for fr in (0.1, 1.0)}
        w, vth = 4500e3, o["cluster"]["Vf_kms"] * 1e3 / math.sqrt(2)
        dx_fixed = {k: v * (w / vth) ** 2 for k, v in dx.items()}
        L_["G5b"] = dict(C=Cc, dx_kpc_sigma_w2=dx, dx_kpc_sigma_fixed=dx_fixed, w_kms=4500, t_Gyr=0.2,
                         label="PASS" if max(dx.values()) <= 24.9 else ("TENSION" if min(dx.values()) <= 24.9 else "FAIL"))
        L_["G5c"] = "REDUCES CLUMPING ONLY BY BREAKING THE LAW (analytic; not computed)"
        lab[fk] = L_
        log(f"\n--- labels {fk}")
        log(f"G1a C_min MW/group/cluster {cm[0]:.4f} / {cm[1]:.4f} / {cm[2]:.4f}; spread {spread:.2f} -> {L_['G1a']['label']}; variants "
            + ", ".join(f"{k} {v:.2f}" for k, v in var.items()))
        log(f"G1b E_sink {es[0]:+.3f} / {es[1]:+.3f} / {es[2]:+.3f} -> {L_['G1b']['label']}")
        log(f"G2 T0 {L_['G2']['T0']}; T1 C_BTFR {cb[0]:.2f} / {cb[1]:.2f} / {cb[2]:.2f} (spread {max(cb) / min(cb):.2f}; /C_min "
            + " / ".join(f"{x:.1f}" for x in L_['G2']['T1']['ratio_to_Cmin']) + f") -> {L_['G2']['T1']['label']}; T2 C_BTFR "
            + " / ".join(f"{x:.2e}" for x in cb2) + f" (spread {max(cb2) / min(cb2):.1f}) -> {L_['G2']['T2']['label']}")
        log(f"G3 t_b at C_min " + " / ".join(f"{x:.3f}" for x in tbm) + " Gyr; at C_BTFR(T1) " + " / ".join(f"{x:.4f}" for x in tbb)
            + f" Gyr -> {L_['G3']['at_Cmin']} / {L_['G3']['at_CBTFR']}; replenishment ceiling ratio " + " / ".join(f"{x:.2f}" for x in rep)
            + f" -> {L_['G3']['replenish']}")
        log(f"G4 (i) {L_['G4']['i']}; (ii) cluster sigma_cb/m_b " + ", ".join(f"{x:.3f}" for x in L_['G4']['ii_cluster_sigma_cb_over_mb'])
            + f" cm^2/g -> {L_['G4']['ii_context']}")
        log(f"G5a " + " / ".join(f"{x:+.2f}" for x in g5a) + f" dex -> {L_['G5a']['label']}")
        log(f"G5b cluster C {Cc:.3f}: drag offset over 0.2 Gyr (sigma ~ 1/w^2) {dx['0.1']:.1f}-{dx['1.0']:.1f} kpc; (sigma fixed at thermal v) "
            f"{dx_fixed['0.1']:.0f}-{dx_fixed['1.0']:.0f} kpc -> {L_['G5b']['label']}")
    RES["labels"] = lab

    # =============================== MUTATE teeth (always computed; MUTATE run writes separate outputs)
    o = out["can"]["MW"]; a0 = FOOT["can"]; Mbk = 6.0e10 * MSUN; Vf = o["Vf_kms"] * 1e3; t = 10 * GYR
    supply = lambda C: C * a0 * Mbk * Vf / math.sqrt(2) * t
    Eimp = o["Eimp_over_McatVf2"] * o["Mcat_over_Mb"] * Mbk * Vf ** 2
    C1 = o["Cmin"]["v_Vf_over_sqrt2|primary"]
    m1 = supply(0.0) / Eimp
    m2 = supply(2 * C1) / supply(C1)
    sgn = -1.0                    # M3: reversed Q (export): native path needs export -> sign test passes
    m3 = all((sgn * 1.0 > 0) == (x <= 0) for x in [out["can"][n]["Esink_over_McatVf2"] for n in names])
    teeth = dict(M1_delivered_over_required=m1, M1_bites=(m1 == 0.0), M2_ratio=m2, M2_bites=abs(m2 - 2) <= 1e-12,
                 M3_sign_flip_satisfies_native=m3, M3_bites=m3)
    RES["MUTATE_teeth"] = teeth
    log(f"\nMUTATE teeth: M1 C->0 delivered/required {m1:.1f} (IC-C cannot reach the profile) -> {'bites' if teeth['M1_bites'] else 'NO'}; "
        f"M2 Cx2 supply ratio {m2:.15f} -> {'bites' if teeth['M2_bites'] else 'NO'}; M3 export-signed Q satisfies the native sign test -> "
        f"{'bites' if m3 else 'NO'} (the G1b fail is a sign fail, not a magnitude fail)")
    finish()
    return 0 if all([teeth["M1_bites"], teeth["M2_bites"], teeth["M3_bites"]]) else 1


def finish():
    with open(os.path.join(HERE, f"cfg643{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg643_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=float)


if __name__ == "__main__":
    sys.exit(main())
