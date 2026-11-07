"""SV4 iter_4: Malin 1's inner bulge/bar mass model and the HI vs stellar distance (FROZEN_CRITERIA.md).

usage: python3 iter4_malin_inner_distance.py [main|MUTATE] [canonical|alt]   MUTATE: the wrong-direction corner (sphere, s = 5/3.3,
f = (1+z)^2, bar term raising V). kappa = 1/2 FITTED; not theory closed. Both footings, never pooled.
"""
import itertools, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANE = os.path.dirname(HERE); sys.path.insert(0, LANE)
import sv4_common as C

MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
ONLY = sys.argv[2] if len(sys.argv) > 2 else None              # optional: one footing per process (parallel parts)
if ONLY: C.FOOT = {ONLY: C.FOOT[ONLY]}
TOL = 3e-8                                                       # AMENDMENTS.md A1: variants stop at residual 3e-8
P = C.Log(); RES = dict(mode=MODE); t0 = time.time()
P(f"SV4 iter_4 Malin 1 inner mass model + stellar/HI distance, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")
ns = C.load_qx4(); ud2 = ns["ud2"]; rec = C.qx4_record(); A = C.A
RT, VT, ET = np.asarray(ud2["RT"]), np.asarray(ud2["VT"]), np.asarray(ud2["ET"])
Z = 0.0826; FS = {"f1": 1.0, "f_lo": (1 + Z) ** -2, "f_hi": (1 + Z) ** 2}
SS = {"s1": (1.0, True), "s3.7": (3.7 / 3.3, True), "s5": (5.0 / 3.3, True), "s0.5": (0.5, False)}
qg, Mq = ns["qg"], ns["Mq"]
SIG2 = ns["SIGF_A2"]; SIG1 = ns["SIGF"]
# HSB as a thin disc: NNLS annuli on the HSB curve (A2 edges), K4-type check
rr, vv = ns["curves"]["hsb"]
sig_hsb = ns["sig_from_annuli"](ns["nnls_sigma"](rr, vv, ns["EDGES_A2"]), ns["EDGES_A2"])
Rs = ns["Rs"]
vrec = np.sqrt(np.maximum(ns["ring_sum_thin"](sig_hsb(Rs), Rs, RT), 0)); vplot = np.sqrt(ns["v2_ext"](rr, vv)(RT))
k4 = float(np.max(np.abs(vrec / vplot - 1)))
P(f"K4 HSB thin-disc inversion: V {np.round(vrec,1).tolist()} vs plotted {np.round(vplot,1).tolist()}: max rel {k4:.4f}"
  f" (line 0.03) -> {'PASS' if k4 <= 0.03 else 'FAIL (G-d tagged)'}")
RES["K4_hsb_disc"] = dict(max_rel=k4, ok=bool(k4 <= 0.03))


def rho_variant(geom, s, f, SF):
    Mp = s * f * f * np.interp(qg / f, qg, Mq)                   # M'(<r) = s f^2 M(<r/f)
    rho_sph = np.gradient(Mp, qg) / (4 * np.pi * qg ** 2)
    def rho(R, z):
        r3 = np.sqrt(R * R + z * z)
        disc = (SF["gas"](R) + SF["lsb"](R / f)) * np.exp(-0.5 * z * z) / np.sqrt(2 * np.pi)       # h = 1 kpc
        if geom == "sph": hsb = np.interp(r3, qg, rho_sph)
        else: hsb = s * sig_hsb(R / f) * np.exp(-0.5 * (z / 0.3) ** 2) / (np.sqrt(2 * np.pi) * 0.3)
        return disc + hsb
    return rho, float(Mp[-1])


def lab(p, ine, ladder):
    if ladder > 0.01: return "NO VERDICT (convergence)"
    return ("RESCUED" if ine else "rescued only outside published errors") if p >= 0.05 else "NOT RESCUED"


def bar_bound(Fd, Mhsb_tot, R):
    """|dV^2/V^2| <= (M_bar/M_enc(R)) (a/R)^2 / 2, M_bar = M_HSB, a = 10 kpc; M_enc from the deposited cells (x2)."""
    rc = Fd.g.rc; Menc = np.array([2 * Fd.M[rc < x].sum() for x in R])
    return np.minimum(Mhsb_tot / Menc * (10.0 / R) ** 2 / 2, 0.99)


if MODE == "MUTATE":
    combos = [("sph", "s5", "f_hi")]
else:
    combos = list(itertools.product(("sph", "disc"), SS.keys(), FS.keys()))
    combos.remove(("sph", "s1", "f1")); combos.insert(0, ("sph", "s1", "f1"))     # baseline first: warm start
PHI0 = {}
RES["rows"] = {}; dep = {}
for geom, sk, fk in combos:
    s, ine_s = SS[sk]; fv = FS[fk]; ine = ine_s and not (geom == "disc" and k4 > 0.03)
    rho, Mh = rho_variant(geom, s, fv, SIG2)
    g = A.Grid(0.05, 3.0e4, *C.RUNG_TOP, p=3); M = C.deposit_fast(g, rho); dep[(geom, sk, fk)] = (rho, M, Mh)
    key = f"{geom}_{sk}_{fk}"; RES["rows"][key] = dict(in_errors=ine, M_hsb=Mh)
    for f, a0 in C.FOOT.items():
        F = C.Field(None, 0.05, 3.0e4, a0, C.RUNG_TOP, M=M, Phi0=PHI0.get(f), tol=TOL if (geom, sk, fk) != ("sph", "s1", "f1") else 1e-8); Vm = F.midplane(RT)
        if (geom, sk, fk) == ("sph", "s1", "f1") and MODE != "MUTATE":
            PHI0[f] = F.Phi
            Ft = C.Field(None, 0.05, 3.0e4, a0, C.RUNG_TOP, M=M, tol=TOL); dtol = float(np.max(np.abs(Ft.midplane(RT) / Vm - 1)))
            RES.setdefault("A1_tol_check", {})[f] = dtol
            P(f"   A1 check: baseline cold start at tol 3e-8 vs 400-iteration run: max |dV/V| {dtol:.1e} (line 1e-3)")
        r_ = dict(V=Vm.tolist(), res=F.res, it=F.it)
        if MODE == "MUTATE":
            bb = bar_bound(F, Mh, RT); Vm = Vm * np.sqrt(1 + bb); r_["bar"] = bb.tolist()
        c, p = C.chi2p(VT, ET, Vm); r_.update(chi2=c, p=p)
        RES["rows"][key][f] = r_
        P(f"{key:18s} [{f}] V {np.round(Vm,1).tolist()} chi2 {c:6.1f} p {p:.1e}{'' if ine else '  (outside published errors)'}")

RES["footings"] = {}
for f, a0 in C.FOOT.items():
    base_q = np.asarray(rec["Malin1_A2"][f]["V_exact"]); c_base, _ = C.chi2p(VT, ET, base_q)
    out = dict(chi2_baseline_QX4=c_base)
    if MODE == "MUTATE":
        c = RES["rows"]["sph_s5_f_hi"][f]["chi2"]; out["MUTATE_bites"] = bool(c > c_base)
        P(f"[{f}] MUTATE wrong-direction corner chi2 {c:.1f} vs baseline {c_base:.1f}: bites {c > c_base}")
        RES["footings"][f] = out; continue
    b = RES["rows"]["sph_s1_f1"]
    ka0 = float(np.max(np.abs(np.asarray(b[f]["V"]) / base_q - 1)))
    rho0, _, _ = dep[("sph", "s1", "f1")]
    Fl = C.Field(rho0, 0.05, 3.0e4, a0, C.RUNG_LOW); ladder = float(np.max(np.abs(Fl.midplane(RT) / np.asarray(b[f]["V"]) - 1)))
    P(f"\n[{f}] KA0 baseline vs QX4 Malin1_A2 {ka0:.1e} (line 1e-3) -> {'PASS' if ka0 <= 1e-3 else 'FAIL'}; ladder {ladder:.1e}")
    ine_rows = {k: v for k, v in RES["rows"].items() if v["in_errors"]}
    best = min(ine_rows, key=lambda k: ine_rows[k][f]["chi2"]); bestg = min(RES["rows"], key=lambda k: RES["rows"][k][f]["chi2"])
    rb = RES["rows"][best][f]
    out.update(KA0=ka0, ladder=ladder, best_in_errors=best, best_chi2=rb["chi2"], best_p=rb["p"],
               label_envelope=lab(rb["p"], True, ladder), best_any=bestg, best_any_chi2=RES["rows"][bestg][f]["chi2"],
               best_any_label=lab(RES["rows"][bestg][f]["p"], RES["rows"][bestg]["in_errors"], ladder))
    P(f"[{f}] best in-errors corner {best}: chi2 {rb['chi2']:.1f}/4 p {rb['p']:.1e} -> {out['label_envelope']};"
      f" best of all (incl. generous) {bestg}: chi2 {out['best_any_chi2']:.1f} -> {out['best_any_label']}")
    # ladder on the best corner
    gb, sb, fb = best.split("_", 1)[0], best.split("_")[1], "_".join(best.split("_")[2:])
    rhob, Mb_, Mhb = dep[(gb, sb, fb)]
    Flb = C.Field(rhob, 0.05, 3.0e4, a0, C.RUNG_LOW); lb = float(np.max(np.abs(Flb.midplane(RT) / np.asarray(rb["V"]) - 1)))
    out["ladder_best"] = lb
    # item 4: bar bound, favourable direction, on baseline and best
    for nm, (rh, Mm, Mh) in (("baseline", dep[("sph", "s1", "f1")]), ("best", (rhob, Mb_, Mhb))):
        F = C.Field(None, 0.05, 3.0e4, a0, C.RUNG_TOP, M=Mm, Phi0=PHI0.get(f), tol=TOL); Vm = F.midplane(RT); bb = bar_bound(F, Mh, RT)
        c, p = C.chi2p(VT, ET, Vm * np.sqrt(1 - bb))
        out[f"bar_{nm}"] = dict(bound=bb.tolist(), chi2=c, p=p, label=lab(p, True, max(ladder, lb)))
        P(f"   bar bound on {nm}: |dV^2/V^2| <= {np.round(bb,4).tolist()}; V lowered -> chi2 {c:.1f} p {p:.1e} -> {out[f'bar_{nm}']['label']}")
    # A1 beside
    for nm, (gg, sk, fk) in (("baseline", ("sph", "s1", "f1")), ("best", (gb, sb, fb))):
        rh1, _ = rho_variant(gg, SS[sk][0], FS[fk], SIG1)
        F = C.Field(rh1, 0.05, 3.0e4, a0, C.RUNG_TOP); c, p = C.chi2p(VT, ET, F.midplane(RT))
        out[f"A1_{nm}"] = dict(chi2=c, p=p)
        P(f"   A1 (reported) {nm}: chi2 {c:.1f} p {p:.1e}")
    RES["footings"][f] = out
P(f"\nwall {time.time()-t0:.0f} s")
P.save(os.path.join(HERE, ("iter4_MUTATE" if MODE == "MUTATE" else "iter4") + (f"_{ONLY}" if ONLY else "")), RES)
