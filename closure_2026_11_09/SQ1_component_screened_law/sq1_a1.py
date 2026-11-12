#!/usr/bin/env python3
"""SQ1 AMENDMENTS A1 (3f30b2a08e) and A2 (de4b69bca4): reported checks of the source's round-23 numbers. Label unchanged.
(1) U_Q / rho_screen and R_dep (35 km/s threshold), source form and frozen 4/3 form; (2) GSMF number densities and the depletion
filling; (3) KiDS with the source's environment (reading C'); (5) Ursa Major and Local Group R_dep at threshold x 0.5 / 1 / 1.5.
    python3 sq1_a1.py   -> sq1_a1.json / sq1_a1.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "sq1.py")).read(); cut = src.index("for f in FOOTS:\n    B = footing_bg(f); q1 = {}")
ns = {"__file__": os.path.join(HERE, "sq1.py"), "__name__": "sq1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "sq1pre", "exec"), ns)
np, G, MS, MPC, KPC, A0, glaw, LE, footing_bg, gsmf, rho_s, S_of = (ns[k] for k in ("np", "G", "MS", "MPC", "KPC", "A0", "glaw", "LE", "footing_bg", "gsmf", "rho_s", "S_of"))
L = []; RES = dict(amendments=["3f30b2a08e", "de4b69bca4"], note="reported checks; label unchanged; adopts nothing; kappa = 1/2 FITTED; not theory closed")
def P(s): print(s, flush=True); L.append(str(s))
def uq(B, f, Mb_sun, r_m, form): return (4 / 3 if form == "frozen" else 1.0) * (G * Mb_sun * MS) ** 1.5 * A0[f] ** 0.5 / (8 * math.pi * G * rho_s(B, f) * r_m ** 3)
def rdep(B, f, Mb_sun, form, vth=35.0): return (uq(B, f, Mb_sun, MPC, form) / (0.5 * (vth * 1e3) ** 2)) ** (1 / 3) * MPC
Q1 = json.load(open(os.path.join(HERE, "sq1.json")))
for f in ("canonical", "alt"):
    B = footing_bg(f); r = {}
    c1 = {form: uq(B, f, 1e11, MPC, form) / 1e6 for form in ("source", "frozen")}; rd = {form: rdep(B, f, 1e11, form) / MPC for form in ("source", "frozen")}
    scal = rdep(B, f, 4e11, "source") / rdep(B, f, 1e11, "source")
    r["item1"] = dict(UQ_over_rho_screen_1Mpc_kms2=c1, source_claim=170.0, R_dep_1e11_Mpc=rd, source_R_dep=0.652, scaling_4x_mass=scal)
    P(f"[{f}] (1) U_Q/rho_screen at 1 Mpc, M_b 1e11: source form {c1['source']:.1f} (km/s)^2 (claim 170), frozen 4/3 form {c1['frozen']:.1f}; R_dep {rd['source']:.3f} / {rd['frozen']:.3f} Mpc (claim 0.652); x4 mass -> x{scal:.3f} (sqrt 2 = 1.414)")
    out2 = {}
    for hh, tag in ((B.h, "footing h"), (0.7, "h 0.7")):
        per = gsmf(hh); mg = np.arange(10.0, 12.0001, 0.005); n10 = float(np.trapz([per(m) for m in mg], mg)); mg5 = np.arange(10.5, 12.0001, 0.005); n105 = float(np.trapz([per(m) for m in mg5], mg5))
        mf = np.arange(9.0, 12.0001, 0.005); V = np.array([4 * math.pi / 3 * (rdep(B, f, 10 ** m, "source") / MPC) ** 3 for m in mf]); fdep = 1 - math.exp(-float(np.trapz(np.array([per(m) for m in mf]) * V, mf)))
        out2[tag] = dict(n_gt_1e10=n10, n_gt_1e10p5=n105, f_dep=fdep)
    r["item2"] = dict(out2, source=dict(n_gt_1e10=0.0086, n_gt_1e10p5=0.0041, f_dep=0.0068))
    P(f"[{f}] (2) GSMF n(>1e10) {out2['footing h']['n_gt_1e10']:.4f} (h {B.h:.3f}) / {out2['h 0.7']['n_gt_1e10']:.4f} (h 0.7) vs 0.0086; n(>10^10.5) {out2['footing h']['n_gt_1e10p5']:.4f} / {out2['h 0.7']['n_gt_1e10p5']:.4f} vs 0.0041; depletion filling {100*out2['footing h']['f_dep']:.2f} % (claim 0.68 %)")
    # (3) KiDS reading C'
    rs = rho_s(B, f); rb = B.RHO_D0; sh = []
    for p in LE:
        Mb = p["Mb"] / MS; R = math.sqrt(G * p["Mb"] / p["gbar"]); Rd = rdep(B, f, Mb, "source")
        rho_at = lambda x: 0.2 * rs if x < min(Rd, 0.8 * MPC) else 0.35 * rs
        xs = np.linspace(1e-3 * R, R, 400); exc = float(np.trapz([(rho_at(x) - rb) * 4 * math.pi * x * x for x in xs], xs))
        gN = p["gbar"]; g = gN + G * exc / R ** 2 + float(S_of(rho_at(R) / rs)) * (float(glaw(gN, A0[f])) - gN); sh.append(math.log10(max(g, 1e-300) / float(glaw(gN, A0[f]))))
    sh = np.array(sh); r["item3"] = dict(kids_Cprime=dict(status_reported="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), mean=float(sh.mean())),
                                         record_collapse_density_in_3Mpc_over_rho_screen={k: v["G"]["density_in_3Mpc_over_rho_screen"] for k, v in Q1[f]["Q1"]["rows"].items()}, source_ambient=0.35)
    P(f"[{f}] (3) KiDS C' (0.2 rho_s inside R_dep / 0.8 Mpc, 0.35 rho_s to 3 Mpc): {r['item3']['kids_Cprime']['status_reported']} max {r['item3']['kids_Cprime']['max_abs']:.3f} ({r['item3']['kids_Cprime']['n_over']}/59, mean {r['item3']['kids_Cprime']['mean']:+.3f}); "
      f"record's spherical collapse gives " + ", ".join(f"1e{k}: {v:.1f}" for k, v in r['item3']['record_collapse_density_in_3Mpc_over_rho_screen'].items()) + " rho_screen inside 3 Mpc (claim 0.35)")
    # (5) UMa / LG
    rows = {}
    for mult in (0.5, 1.0, 1.5):
        vth = 35.0 * mult; e = {}
        for form in ("source", "frozen"):
            u15 = uq(B, f, 2e10, 15 * KPC, form) / 1e6; R_uma = rdep(B, f, 4.8e11, form, vth) / MPC; R_mw = rdep(B, f, 6e10, form, vth) / MPC; R_m31 = rdep(B, f, 1e11, form, vth) / MPC
            e[form] = dict(UQ_15kpc_kms=math.sqrt(u15), sigma_UMa=148.0, R_dep_UMa_Mpc=R_uma, R_dep_MW_Mpc=R_mw, R_dep_M31_Mpc=R_m31, LG_cleared=bool(R_mw + R_m31 > 0.77))
        rows[f"threshold {vth:g} km/s"] = e
    r["item5"] = rows
    for k, e in rows.items(): P(f"[{f}] (5) {k}: source form: sqrt(U_Q/rho_s) at 15 kpc {e['source']['UQ_15kpc_kms']:.0f} km/s (claim 2120); R_dep UMa {e['source']['R_dep_UMa_Mpc']:.2f} Mpc (claim 1.43), MW {e['source']['R_dep_MW_Mpc']:.3f} + M31 {e['source']['R_dep_M31_Mpc']:.3f} vs 0.77 -> LG cleared {e['source']['LG_cleared']}; frozen 4/3: UMa {e['frozen']['R_dep_UMa_Mpc']:.2f}, LG {e['frozen']['LG_cleared']}")
    RES[f] = r
P("(4) Tinker 2008 budget and the P(k) / sigma8 claims: NOT EVALUATED (no halo-model machinery in the record). (6) a0_eff(z) 0.98 / 0.92 / 0.68 at z 0.5 / 1 / 2: recorded as the source's prediction; NOT EVALUABLE against the record's a0(z) cells (AT2: every on-disk high-z cell blocked by common modes).")
json.dump(RES, open(os.path.join(HERE, "sq1_a1.json"), "w"), indent=1); open(os.path.join(HERE, "sq1_a1.out"), "w").write("\n".join(L) + "\n")
