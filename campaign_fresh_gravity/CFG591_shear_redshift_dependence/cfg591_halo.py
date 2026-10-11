#!/usr/bin/env python3
"""CFG591 (FROZEN_CRITERIA.md section 1): R(k, z) from the CFG556 halo model at z = 0, 0.25, 0.5, 0.75, 1.0, both footings.
Models: PRIMARY (CFG559 PRIMARY_kin path: s_c*(z) + kinetic Delta m(z)), CFG557 TESTED (s_c*(z), sharp), CFG556 census|cen, census|emg,
census|cen|r200scope.  Epoch namespace from cfg591_lib (CFG556 exec'd read-only, epoch inputs overridden; CFG557/559 profile functions
exec'd verbatim).  Delta m tables: z = 0 CFG559's (reused), z > 0 cfg591_toy_results.json.
  OMP_NUM_THREADS=4 nice -n 10 python3 cfg591_halo.py -> cfg591_halo.out, cfg591_halo_results.json
kappa = 1/2 FITTED; footings never pooled; flat a0; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg591_lib as C
K9 = C.K9
DESI = os.environ.get("CFG591_DESI", "0") == "1"           # ADDENDUM 1 variant
SUF = "_DESI" if DESI else ""
DESI_INFO = None
if DESI:
    import cfg591_desi as DSI
    DESI_INFO = DSI.activate(*DSI.desi_w0wa())
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

LANES = C.LANES
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))
J557 = json.load(open(os.path.join(C.D557, "cfg557_tests_results.json")))
J559 = json.load(open(os.path.join(C.D559, "cfg559_tests_results.json")))
JT = json.load(open(os.path.join(HERE, f"cfg591_toy{SUF}_results.json")))
MODELS = ["PRIMARY", "CFG557_TESTED", "CFG556_cen", "CFG556_emg", "CFG556_r200scope"]
KSEL = [0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 3.0]

if DESI:
    P(f"[ADDENDUM 1 DESI-tracking variant: {DESI_INFO}; a0(z)/a0(0) at z 0.25/0.5/0.75/1.0 = " + "/".join(f"{math.sqrt(C.fDE(z)):.4f}" for z in (0.25, 0.5, 0.75, 1.0)) + "]")
P("CFG591 halo model R(k, z) -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; flat a0 (w = -1); cold energy MASS still required; not theory closed.")
res = dict(desi=DESI_INFO, a0_ratio={str(z): math.sqrt(C.fDE(z)) for z in C.ZNODES}, lane="CFG591", script="cfg591_halo", date="2026-10-10", z_nodes=C.ZNODES, models=MODELS, k=None, R={}, info={}, controls={})
hz0 = {}; hz1 = {}
for z in C.ZNODES:
    H = C.namespace(z); KK = H["KK"]; res["k"] = KK.tolist()
    # Delta m table for this epoch (the K9 cache is the only switch)
    K9._CACHE.pop("MAIN", None)
    if z == 0.0 and not DESI:
        K9.table(False)
    else:
        K9._CACHE["MAIN"] = JT["tables"][str(z)]
    SC = {}
    for ft in C.FOOTS:
        SC[ft] = C.sc_grid(H, ft, z)
        if z > 0 or DESI:
            g = JT["grids"][str(z)]
            assert np.allclose(g["log10_Mta"], np.log10(H["MTA"]), atol=1e-12, rtol=0) and np.allclose(g[ft], SC[ft], atol=1e-12, rtol=0), "toy grid mismatch"
    U_set, U_std, spectra_ta, spectra_std, s8_of = (H[k] for k in ("U_set", "U_std", "spectra_ta", "spectra_std", "s8_of"))
    rgrid, M_L, frame_profile = H["rgrid"], H["M_L"], H["frame_profile"]
    Ustd = U_std(); Pstd, _, Istd = spectra_std(Ustd)
    Ulta, _ = U_set(lambda hb: (lambda r: (r, M_L(hb, r), {}))(rgrid(hb, hb["rta"])))
    Plta, _, Ilta = spectra_ta(Ulta)
    i3 = int(np.argmin(abs(KK - 1e-3)))
    s8lin = s8_of(H["PL"]); c1 = abs(s8lin / (0.811 * H["Dz"]) - 1)
    Ichk = [abs(Istd[i3] - 1), abs(Ilta[i3] - 1)]
    W8K = H["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    P(f"\n=== z = {z}: D {H['Dz']:.5f}; Delta_ta {H['DTA']:.4f} (ODE {H['Delta_ODE']:.4f}); Om(z) {H['Omz']:.4f}; A_miss {H['A_MISS']:.4f}; NORM_TA {H['NORM_TA']:.4f}; "
      f"sigma8(P_lin) {s8lin:.5f} vs 0.811 D {0.811 * H['Dz']:.5f} (rel {c1:.1e}); I(1e-3) L-std {Istd[i3]:.6f}, L-ta {Ilta[i3]:.6f}")
    res["info"][str(z)] = dict(Dz=H["Dz"], Delta_ta=H["DTA"], Delta_ODE=H["Delta_ODE"], Omz=H["Omz"], A_MISS=H["A_MISS"], NORM_TA=H["NORM_TA"],
                               s8_lin=s8lin, s8_L_std=s8_of(Pstd), sc_at={}, models={})
    res["R"][str(z)] = {}
    for ft in C.FOOTS:
        res["R"][str(z)][ft] = {}
        sc = SC[ft]
        res["info"][str(z)]["sc_at"][ft] = {str(l): float(np.interp(l, np.log10(H["MTA"]), sc)) for l in (11, 12, 13, 14, 15)}
        fns = {"PRIMARY": (lambda hb, _it=iter(sc): H["frame_profile_kin"](hb, ft, next(_it), "kin", "primary"), "ta"),
               "CFG557_TESTED": (lambda hb, _it=iter(sc): H["frame_profile_sc"](hb, ft, next(_it)), "ta"),
               "CFG556_cen": (lambda hb: frame_profile(hb, ft, edge="cen"), "ta"),
               "CFG556_emg": (lambda hb: frame_profile(hb, ft, edge="emg"), "ta"),
               "CFG556_r200scope": (lambda hb: frame_profile(dict(hb, rta=hb["r200"], Mta=hb["M"]), ft, edge="cen"), "std")}
        for nm, (fn, scope) in fns.items():
            U, infos = U_set(fn)
            if scope == "ta":
                PF, _, IF = spectra_ta(U); R = 1 + (PF - Plta) / Pstd; dP = PF - Plta
            else:
                PF, _, IF = spectra_std(U); R = PF / Pstd; dP = PF - Pstd
            s8r = math.sqrt(s8_of(Pstd) ** 2 + np.trapz(dP * W8K, KK)) / s8_of(Pstd)
            res["R"][str(z)][ft][nm] = R.tolist()
            lt = np.log10(H["MTA"])
            inf = dict(R_at={str(k): float(np.interp(k, KK, R)) for k in KSEL}, s8_ratio=s8r, I_k1e3=float(IF[i3]),
                       E=float(np.max(R[(KK >= 0.05) & (KK <= 1)] - 1)), D=float(np.min(R[(KK >= 0.05) & (KK <= 1)] - 1)),
                       n_capped=int(sum(bool(i.get("capped", False)) for i in infos)))
            if scope == "ta":
                Ichk.append(abs(IF[i3] - 1))
            if nm in ("PRIMARY", "CFG557_TESTED", "CFG556_cen", "CFG556_emg"):
                inf["re_over_rta_at"] = {str(l): float(np.interp(l, lt, [i["re"] / hb["rta"] for i, hb in zip(infos, H["HB"])])) for l in (12, 13, 14, 15)}
            if nm == "PRIMARY":
                inf["r99_over_rta_at"] = {str(l): float(np.interp(l, lt, [i["r99_over_rta"] for i in infos])) for l in (12, 13, 14, 15)}
                inf["min_dM_rel"] = float(min(i["min_dM_rel"] for i in infos))
                # HZ1 mass conservation (every 4th halo)
                c3 = 0.0
                for j, hb in enumerate(H["HB"]):
                    if j % 4: continue
                    r, Mc, _ = H["frame_profile_kin"](hb, ft, sc[j], "kin", "primary"); c3 = max(c3, abs(Mc[-1] - hb["Mta"]) / hb["Mta"])
                inf["mass_cons"] = c3
            res["info"][str(z)]["models"][f"{ft}|{nm}"] = inf
            P(f"  [{ft:9s}] {nm:17s} R(k): " + "  ".join(f"{k}:{inf['R_at'][str(k)]:.3f}" for k in KSEL) + f" | s8 ratio {s8r:.4f}  capped {inf['n_capped']}"
              + (f" | r_e/r_ta 12-15 " + "/".join(f"{inf['re_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15)) if "re_over_rta_at" in inf else "")
              + (f" | kin r99/r_ta " + "/".join(f"{inf['r99_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15)) + f" | mass cons {inf['mass_cons']:.1e}" if nm == "PRIMARY" else ""))
        P(f"  [{ft:9s}] s_c*(z) at log M_ta 11-15: " + " ".join(f"{v:.3f}" for v in res["info"][str(z)]["sc_at"][ft].values()))
    hz1[str(z)] = dict(s8_rel=c1, I_max=float(max(Ichk)), mass_cons=max(res["info"][str(z)]["models"][f"{ft}|PRIMARY"]["mass_cons"] for ft in C.FOOTS))
    if z == 0.0 and not DESI:
        for ft in C.FOOTS:
            ref = {"PRIMARY": J559["halo_model"][ft]["PRIMARY_kin"]["R"], "CFG557_TESTED": J557["halo_model"][ft]["TESTED"]["R"],
                   "CFG556_cen": J556["cases"][f"{ft}|census|cen"]["R"], "CFG556_emg": J556["cases"][f"{ft}|census|emg"]["R"],
                   "CFG556_r200scope": J556["cases"][f"{ft}|census|cen|r200scope"]["R"]}
            for nm, rr in ref.items():
                hz0[f"{ft}|{nm}"] = float(np.max(np.abs(np.array(res["R"]["0.0"][ft][nm]) - np.array(rr))))
        P("  HZ0 z = 0 vs stored CFG559/557/556 R: max|dR| = " + ", ".join(f"{k} {v:.1e}" for k, v in hz0.items()))

hz0max = max(hz0.values()) if hz0 else float("nan")
hz1ok = all(v["s8_rel"] <= 1e-3 and v["I_max"] <= 1e-3 and v["mass_cons"] <= 1e-6 for v in hz1.values())
res["controls"] = dict(HZ0=hz0, HZ0_max=hz0max, HZ0_pass=(bool(hz0max <= 1e-10) if hz0 else "n/a (DESI variant)"), HZ1=hz1, HZ1_pass=hz1ok,
                       toy_C6_pass=JT["controls"]["C6_pass"], toy_C7=JT["controls"]["C7_mass_exact"], toy_gate_fail=JT["controls"]["n_gate_fail"])
P(f"\nHZ0 max|dR| at z = 0 = {hz0max:.1e} -> {'PASS' if hz0max <= 1e-10 else 'FAIL'};  HZ1 (sigma8(z), I(1e-3), mass) -> {'PASS' if hz1ok else 'FAIL'}: "
  + "; ".join(f"z {z}: s8 {v['s8_rel']:.1e}, I {v['I_max']:.1e}, M {v['mass_cons']:.1e}" for z, v in hz1.items()))
P(f"toy controls: C6 {JT['controls']['C6_pass']}, C7 {JT['controls']['C7_mass_exact']}, cells failing CFG544 gate {JT['controls']['n_gate_fail']}")
# effective redshift scaling of the excess at k = 1
P("\nEffective scaling s(z) = (R(k=1, z) - 1)/(R(k=1, 0) - 1):")
res["s_of_z_k1"] = {}
for ft in C.FOOTS:
    for nm in MODELS:
        r0 = res["info"]["0.0"]["models"][f"{ft}|{nm}"]["R_at"]["1.0"] - 1
        s = {str(z): (res["info"][str(z)]["models"][f"{ft}|{nm}"]["R_at"]["1.0"] - 1) / r0 if abs(r0) > 1e-12 else None for z in C.ZNODES}
        res["s_of_z_k1"][f"{ft}|{nm}"] = s
        P(f"  [{ft:9s}] {nm:17s} R(1)-1 at z=0 {r0:+.3f}; s(z): " + " ".join(f"{z}:{v:.3f}" if v is not None else f"{z}:n/a" for z, v in s.items()))
json.dump(res, open(os.path.join(HERE, f"cfg591_halo{SUF}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg591_halo{SUF}.out"), "w").write("\n".join(OUT) + "\n")
