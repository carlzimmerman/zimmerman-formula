#!/usr/bin/env python3
"""CSD1 grader (FROZEN_CRITERIA.md sections 1c, 2 to 5; AMENDMENT_A1): known answers KA3, KA4, KA7; twins TW3, TW5;
the tables of D_k, densities, front speeds, required inflow, equal-charge radius for S-seed and S-cos; the S-ref table
read from csd1_ref.json; the labels; P1c (eps) with an independent SI check.
  python3 -I -B csd1_grade.py -> csd1_grade.json / .out, csd1_grade_MUTATE.json / .out (TW3, TW5)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "fable52_push", "COL1_clock_collapse"))
import col1_lib as L                                            # read-only
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "runs")
XJS = os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface", "shells")
RUNS = os.path.join(HERE, "runs")
KD1 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
FOOTS = ("canonical", "alt"); MASSES = [8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5]; ZG = (0.0, 2.2, 3.0, 4.4)
KS = ("k1", "k2", "k3", "half"); TOL = 0.10; CKMS = 299792.458; TU = L.TU
OUT, MOUT = [], []
def P(*x):
    s = " ".join(str(y) for y in x); print(s, flush=True); OUT.append(s)
def PM(*x):
    s = " ".join(str(y) for y in x); print("[MUTATE] " + s, flush=True); MOUT.append(s)
def load(n): return json.load(open(os.path.join(RUNS, n + ".json")))
def nm(ft, M, N=2400, grid="", A=0, law="on", mut=""):
    return (f"csd1_{ft}_M{M:g}_N{N}" + (f"_{grid}" if grid else "") + ("" if A == 0 else f"_A{A:g}") + ("" if law == "on" else "_lawoff")
            + (f"_MUT{mut}" if mut else ""))
RES = dict(lane="CSD1", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ---------------------------------------------------------------- KA3: series against FLD1 and XJ1
ka3 = True; w3 = 0.0
for ft in FOOTS:
    for M in MASSES:
        S = np.array(load(nm(ft, M))["series"], float)
        f = np.array(json.load(open(os.path.join(FLD, f"hubble_{ft}_M{M:g}_zi10_N2400.json")))["series"], float)
        x = np.array(json.load(open(os.path.join(XJS, f"xj1_shells_{ft}_M{M:g}.json")))["series"], float)
        if S.shape[0] != f.shape[0] or S.shape[0] != x.shape[0]: ka3 = False; P(f"KA3 {ft} {M}: row count differs"); continue
        d1 = float(np.max(np.abs(S[:, :5] - f) / np.maximum(np.abs(f), 1e-30))); d2 = float(np.max(np.abs(S[:, :8] - x) / np.maximum(np.abs(x), 1e-30)))
        w3 = max(w3, d1, d2); ka3 = ka3 and d1 <= 1e-9 and d2 <= 1e-9
P(f"KA3 (18 runs: first five columns = FLD1's stored series, R_1..R_3 = XJ1's; line 1e-9): worst {w3:.1e} -> {'PASS' if ka3 else 'FAIL'}")
RES["KA3"] = dict(pass_=bool(ka3), worst=w3)

# ---------------------------------------------------------------- KA4: FLD1's 1.6 to 5.1 % on A4's grid
ka4 = True; w4 = 0.0; allr = []
for ft in FOOTS:
    for M in (9.4, 10.45, 10.7, 10.9):
        d = load(nm(ft, M, grid="a4")); st = json.load(open(os.path.join(FLD, f"hubble_{ft}_M{M:g}_zi10_N2400_a4.json")))["reads_end"]
        S = np.array(d["series"], float); c = d["series_cols"]
        for R in ("10", "30", "100", "300"):
            a_ = d["reads_end"][R]["M_N_all_shells_over_M_ph"]; b_ = st[R]["M_N_all_shells_over_M_ph"]; own = S[-1, c.index(f"read_{R}")]
            dd = max(abs(a_ / b_ - 1), abs(own / b_ - 1)); w4 = max(w4, dd); allr.append(b_)
            ka4 = ka4 and dd <= 1e-9
lo, hi = min(allr), max(allr); ka4 = ka4 and f"{100 * lo:.1f}" == "1.6" and f"{100 * hi:.1f}" == "5.1"
P(f"KA4 (A4 grid, 8 rows x 4 radii; reads_end and this lane's own count = FLD1's stored, line 1e-9): worst {w4:.1e}; "
  f"range {100 * lo:.2f} % to {100 * hi:.2f} % (FLD1: 1.6 to 5.1) -> {'PASS' if ka4 else 'FAIL'}")
RES["KA4"] = dict(pass_=bool(ka4), worst=w4, range_pct=[100 * lo, 100 * hi])

# ---------------------------------------------------------------- TW3, TW5 (MUTATE)
d = load(nm("canonical", 10.45, grid="a4", mut="lagr")); S = np.array(d["series"], float); c = d["series_cols"]
st = json.load(open(os.path.join(FLD, "hubble_canonical_M10.45_zi10_N2400_a4.json")))["reads_end"]
dev = max(abs(S[-1, c.index(f"read_{R}")] / st[R]["M_N_all_shells_over_M_ph"] - 1) for R in ("10", "30", "100", "300"))
PM(f"TW3 (count by Lagrangian radius): KA4's own-count reproduction deviates by {dev:.3e} (bites if > 1e-3) -> {'BITES' if dev > 1e-3 else 'DOES NOT BITE'}")

def zinterp(S, c, col, z):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, c.index(col)]))

# ---------------------------------------------------------------- per-run table
def cells(d, ft):
    S = np.array(d["series"], float); c = d["series_cols"]
    t = S[:, 0]; out = {}
    a0 = L.a0_of(ft)
    for z in ZG:
        tz = zinterp(S, c, "t_since_start_gyr", z); Rf = zinterp(S, c, "R_fold_kpc", z)
        e = dict(R_fold=Rf, R_ta=zinterp(S, c, "R_ta_kpc", z))
        # R_eq from the nearest output (a radius from the shells, not interpolated across a jump)
        i = int(np.argmin(np.abs(S[:, 1] - z))); Req = S[i, c.index("R_eq_kpc")]
        e["R_eq_over_Rfold"] = float(Req / S[i, 2]) if S[i, 2] > 0 else float("nan")
        e["R_first_short_over_Rfold"] = float(S[i, c.index("R_first_short_kpc")] / S[i, 2]) if S[i, 2] > 0 else float("nan")
        e["D_max"] = float(S[i, c.index("D_max_1kpc_to_Rta")]); e["r_at_D_max_over_Rfold"] = float(S[i, c.index("r_at_D_max_kpc")] / S[i, 2]) if S[i, 2] > 0 else float("nan")
        for k in KS:
            Rcol = {"k1": "R_1_kpc", "k2": "R_2_kpc", "k3": "R_3_kpc", "half": "R_fold_kpc"}[k]
            Rs_ = S[:, c.index(Rcol)] * (0.5 if k == "half" else 1.0)
            o = np.argsort(S[:, 1]); j = np.searchsorted(S[o, 1], z)
            nb = [S[o, :][max(j - 1, 0)], S[o, :][min(j, len(o) - 1)]]
            formed = all(r_[c.index(Rcol)] > 0 for r_ in nb)
            if not formed:
                e[k] = dict(formed=False); continue
            R = zinterp(S, c, Rcol, z) * (0.5 if k == "half" else 1.0)
            g = {q: zinterp(S, c, f"{q}_{k}", z) for q in ("D", "Dexc", "Dunc", "Claw", "Nin")}
            for w in (0.05, 0.1, 0.2):
                for q in ("Nout", "vout", "Nflowin"):
                    g[f"{q}_w{w:g}"] = zinterp(S, c, f"{q}_w{w:g}_{k}", z)
            win = (np.abs(t - tz) <= 0.25) & (Rs_ > 0)
            full = np.sum(np.abs(t - tz) <= 0.25) == np.sum(win) and win.sum() >= 5
            Rdot = float(np.polyfit(t[win], Rs_[win], 1)[0]) * TU if full else float("nan")      # kpc/Gyr -> km/s
            No, vo = g["Nout_w0.1"], g["vout_w0.1"]; Ni = g["Nin"]
            vreq = Rdot * (1 - Ni / No) if No > 0 else float("nan")
            Sdot = 4 * math.pi * R * R * (Ni * (0 - Rdot) - No * (vo - Rdot)) / TU / g["Claw"]   # per Gyr, in C_law(R)
            e[k] = dict(formed=True, R=R, Rdot_kms=Rdot, NinNout=(Ni / No if No > 0 else float("inf")),
                        NinNout_w005=(Ni / g["Nout_w0.05"] if g["Nout_w0.05"] > 0 else float("inf")),
                        NinNout_w02=(Ni / g["Nout_w0.2"] if g["Nout_w0.2"] > 0 else float("inf")),
                        v_out=vo, v_req=vreq, j_extra_over_Nout=(vreq - vo), Sdot_over_C_per_Gyr=Sdot,
                        missing_rate_over_C_per_Gyr=-Sdot, **g)
        out[f"{z:g}"] = e
    # history: min / max of D_k over z in [0, 4.4], formed outputs only
    hist = {}
    for k in KS:
        Rcol = {"k1": "R_1_kpc", "k2": "R_2_kpc", "k3": "R_3_kpc", "half": "R_fold_kpc"}[k]
        m = (S[:, 1] <= 4.4) & (S[:, c.index(Rcol)] > 0) & (S[:, c.index(f"Claw_{k}")] > 0)
        Dk = S[m, c.index(f"D_{k}")]
        hist[k] = [float(Dk.min()), float(Dk.max())] if m.any() else None
    out["history"] = hist
    return out

def label(tab, masses):
    """frozen section 5, one footing / supply / k."""
    res = {}
    for k in KS:
        cl = [(M, z, tab[f"{M:g}"][f"{z:g}"][k]) for M in masses for z in ZG]
        formed = [(M, z, math.log10(e["D"])) for M, z, e in cl if e.get("formed") and e["D"] > 0]
        nf = len(cl) - len(formed)
        if len(formed) < len(cl) / 2:
            res[k] = dict(word="NOT EVALUABLE", not_formed=nf); continue
        ld = np.array([x[2] for x in formed])
        if np.all(np.abs(ld) <= TOL): w = "THE FLOW DELIVERS THE LAW'S CHARGE AT CAUSTIC"
        elif np.all(ld < -TOL): w = "SHORT AT CAUSTIC"
        elif np.all(ld > TOL): w = "OVER AT CAUSTIC"
        else:
            cross = {}
            for z in ZG:
                pts = [(M, x) for M, zz, x in formed if zz == z]
                for (m1, x1), (m2, x2) in zip(pts[:-1], pts[1:]):
                    if np.sign(x1) != np.sign(x2):
                        cross.setdefault(f"{z:g}", []).append(m1 + (m2 - m1) * (-x1) / (x2 - x1))
            w = "DEPENDS ON MASS AT CAUSTIC" if cross else "MIXED AT CAUSTIC"
            res[k] = dict(word=w, crossing_logMb=cross, not_formed=nf, logD_range=[float(ld.min()), float(ld.max())]); continue
        res[k] = dict(word=w, not_formed=nf, logD_range=[float(ld.min()), float(ld.max())])
    return res

def show(tab, masses, title):
    P(f"\n== {title}")
    for z in ZG:
        P(f"  z {z:g}:  log M_b | R_fold kpc | D_1 D_2 D_3 D_half | Dexc_3 | N_in/N_out k3 (w .05/.1/.2) | Rdot_3 v_out v_req km/s | missing/C_law per Gyr k3 | R_eq/R_fold")
        for M in masses:
            e = tab[f"{M:g}"][f"{z:g}"]
            def D(k): return f"{e[k]['D']:.4f}" if e[k].get("formed") else "n/f"
            k3 = e["k3"]
            s3 = (f"{k3['Dexc']:.4f} | {k3['NinNout_w005']:.2f}/{k3['NinNout']:.2f}/{k3['NinNout_w02']:.2f} | {k3['Rdot_kms']:.2f} {k3['v_out']:.2f} {k3['v_req']:.2f} | "
                  f"{k3['missing_rate_over_C_per_Gyr']:.3f}") if k3.get("formed") else "n/f"
            P(f"    {M:5.2f} | {e['R_fold']:7.1f} | {D('k1')} {D('k2')} {D('k3')} {D('half')} | {s3} | {e['R_eq_over_Rfold']:.3f}")
    P("  history, min / max of D_3 over z 0 to 4.4: " + "; ".join(
        f"{M:g}: " + (f"{tab[f'{M:g}']['history']['k3'][0]:.4f} / {tab[f'{M:g}']['history']['k3'][1]:.4f}" if tab[f"{M:g}"]["history"]["k3"] else "n/f") for M in masses))

LAB = {}
TAB = {}
for ft in FOOTS:
    TAB[f"S-seed_{ft}"] = {f"{M:g}": cells(load(nm(ft, M)), ft) for M in MASSES}
    show(TAB[f"S-seed_{ft}"], MASSES, f"S-seed [{ft}]")
    LAB[f"S-seed_{ft}"] = label(TAB[f"S-seed_{ft}"], MASSES)

# ---------------------------------------------------------------- S-cos
tune = json.load(open(os.path.join(HERE, "csd1_tune.json"))); Astar = tune["A_star"]
scos_ok = Astar is not None
if scos_ok:
    conf = load(nm("canonical", 10.45, A=Astar, law="off"))["charge_turned_around_over_Mb"]
    rel = conf / tune["target"]["canonical"] - 1; scos_ok = abs(rel) <= 0.10
    P(f"\nS-cos tuning: A* = {Astar:g}; confirming law-off run (N 2400) turned around {conf:.2f} M_b against {tune['target']['canonical']:.2f} "
      f"({100 * rel:+.1f} %; line 10 %) -> {'ACCEPTED' if scos_ok else 'NOT ACCEPTED'}")
    k7 = load("csd1_ka7_A0_canonical_M10.45"); s0 = np.array(load(nm("canonical", 10.45))["series"], float); s7 = np.array(k7["series"], float)
    d7 = float(np.max(np.abs(s7 - s0) / np.maximum(np.abs(s0), 1e-30)))
    P(f"KA7 (S-cos code with A = 0 against the S-seed run, all columns; line 1e-12): {d7:.1e} -> {'PASS' if d7 <= 1e-12 else 'FAIL'}"
      " (this checks only that the inserted perturbation is inert at A = 0)")
    RES["KA7"] = dict(pass_=bool(d7 <= 1e-12), dev=d7)
    for ft in FOOTS:
        TAB[f"S-cos_{ft}"] = {f"{M:g}": cells(load(nm(ft, M, A=Astar)), ft) for M in (9, 10.45, 11.5)}
        show(TAB[f"S-cos_{ft}"], (9, 10.45, 11.5), f"S-cos, law on [{ft}] (A* {Astar:g})")
        LAB[f"S-cos_{ft}"] = label(TAB[f"S-cos_{ft}"], (9, 10.45, 11.5)) if (scos_ok and d7 <= 1e-12) else {k: dict(word="NOT EVALUABLE") for k in KS}
    TAB["S-cos-lawoff_canonical"] = {f"{M:g}": cells(load(nm("canonical", M, A=Astar, law="off")), "canonical") for M in (9, 10.45, 11.5)}
    show(TAB["S-cos-lawoff_canonical"], (9, 10.45, 11.5), "S-cos, law OFF (reported, not graded) [canonical]")
    for ft in FOOTS:
        P(f"  S-cos law on [{ft}] turned around (M_b): " + ", ".join(f"{M:g}: {load(nm(ft, M, A=Astar))['charge_turned_around_over_Mb']:.2f}" for M in (9, 10.45, 11.5)))
    P("  S-cos law off [canonical] turned around (M_b): " + ", ".join(f"{M:g}: {load(nm('canonical', M, A=Astar, law='off'))['charge_turned_around_over_Mb']:.2f}" for M in (9, 10.45, 11.5)))
else:
    for ft in FOOTS: LAB[f"S-cos_{ft}"] = {k: dict(word="NOT EVALUABLE") for k in KS}

# ---------------------------------------------------------------- S-ref (from csd1_ref.json)
ref = json.load(open(os.path.join(HERE, "csd1_ref.json")))
for ft in FOOTS:
    tab = {}
    for M in MASSES:
        tab[f"{M:g}"] = {}
        for z in ZG:
            e = ref["table"][f"{ft}_z{z:g}"]["rows"][f"{M:g}"]
            tab[f"{M:g}"][f"{z:g}"] = {k: (dict(formed=True, D=e[f"D_{kk}"]) if (e["status"] == "settled" and np.isfinite(e.get(f"D_{kk}", float("nan")))) else dict(formed=False))
                                      for k, kk in (("k1", 1), ("k2", 2), ("k3", 3), ("half", "half"))}
    LAB[f"S-ref_{ft}"] = label(tab, MASSES) if ref["KA5"] else {k: dict(word="NOT EVALUABLE") for k in KS}
    TAB[f"S-ref_{ft}"] = tab
    # v_req for S-ref with S-seed's Rdot (reported)
    P(f"\n== S-ref [{ft}]: v_req = Rdot_3 (1 - N_in/N_out) with Rdot_3 from S-seed (km/s)")
    for z in ZG:
        row = []
        for M in MASSES:
            e = ref["table"][f"{ft}_z{z:g}"]["rows"][f"{M:g}"]; s3 = TAB[f"S-seed_{ft}"][f"{M:g}"][f"{z:g}"]["k3"]
            if e["status"] == "settled" and s3.get("formed") and np.isfinite(e.get("NinNout_3", float("nan"))):
                row.append(f"{M:g}: D_3 {e['D_3']:.3f}, N_in/N_out {e['NinNout_3']:.2f}, v_req {s3['Rdot_kms'] * (1 - e['NinNout_3']):.2f}, R_eq/R_fold {e['R_eq_over_Rfold']:.2f}")
            else:
                row.append(f"{M:g}: n/a")
        P(f"  z {z:g}: " + "; ".join(row))

# ---------------------------------------------------------------- P1c: the non-advective term
P("\n== P1c: eps = |c lambda P| / |N v| at the caustics, z = 0 (lambda_0: D Phi/Dt = |v| g + g R / t_age; gamma_L piece for widths w)")
LSTAR = {"canonical": 21.7e-3, "alt": 22.9e-3}                   # kpc
eps_tab = {}
for ft in FOOTS:
    s = KD1["footings"][ft]["setting"]; cos = L.Cosmo(s["h"], s["omega_d"], s["omega_b"]); tage = cos.t_of_a(1.0)   # kpc/(km/s)
    a0 = L.a0_of(ft)
    for M in (10.7, 10.825):
        e0 = cells(load(nm(ft, M)), ft)["0"]
        for k in ("k1", "k2", "k3"):
            e = e0[k]
            if not e.get("formed"): continue
            R = e["R"]; Mb = 10 ** M; gn = L.G * Mb * R / (R * R + 1.0) ** 1.5; g = float(L.law_g(gn, a0))
            No, vo, Ni, Rd, C = e["Nout_w0.1"], abs(e["v_out"]), e["Nin"], abs(e["Rdot_kms"]), e["Claw"]
            Q = e["D"] * C
            dpdt_v = vo * g; dpdt_t = g * R / tage
            eps_out = (dpdt_v + dpdt_t) / CKMS ** 2 * (Q / (4 * math.pi * R * R)) / (No * vo)
            eps_out_v = dpdt_v / CKMS ** 2 * (Q / (4 * math.pi * R * R)) / (No * vo)
            eps_in = (Rd * g + dpdt_t) / CKMS ** 2 * (C / (4 * math.pi * R * R)) / (Ni * Rd)
            jx = abs(e["j_extra_over_Nout"]) * No
            eps_need = (dpdt_v + dpdt_t) / CKMS ** 2 * (C / (4 * math.pi * R * R)) / jx if jx > 0 else float("inf")
            gam = {}
            for wl, w in (("10kpc", 10.0), ("1kpc", 1.0), ("1pc", 1e-3)):
                gam[wl] = 2 * math.pi * L.G * abs(Ni - No) * LSTAR[ft] ** 2 / CKMS ** 2 / w * (C / (4 * math.pi * R * R)) / max(No, Ni)
            # independent SI evaluation of eps_out
            kpc = 3.0857e19; Gsi = 6.674e-11; Msun = 1.989e30; csi = 2.99792458e8
            gs = g * 1e6 / kpc; vs = vo * 1e3; Rsi = R * kpc; ts = tage * kpc / 1e3
            lsi = (Q * Msun / (4 * math.pi * Rsi ** 2)) / (No * Msun / kpc ** 3)
            eps_si = (vs * gs + gs * Rsi / ts) / csi ** 2 * lsi / vs
            eps_tab[f"{ft}_{M:g}_{k}"] = dict(R=R, g_kms2_per_kpc=g, eps_out=eps_out, eps_out_v_only=eps_out_v, eps_law_side=eps_in,
                                             eps_against_missing_flux=eps_need, eps_gamma=gam, eps_out_SI=eps_si,
                                             si_rel=abs(eps_si / eps_out - 1), vc2_over_c2=g * R / CKMS ** 2)
            P(f"  [{ft}] log M_b {M:g} {k}: R {R:.1f} kpc; (v_c/c)^2 = gR/c^2 {g * R / CKMS ** 2:.2e}; eps outside {eps_out:.2e} "
              f"(v.grad part {eps_out_v:.2e}; SI {eps_si:.2e}, rel {abs(eps_si / eps_out - 1):.1e}); law side {eps_in:.2e}; "
              f"available / missing flux {eps_need:.2e}; gamma_L piece w 10 kpc / 1 kpc / 1 pc: {gam['10kpc']:.1e} / {gam['1kpc']:.1e} / {gam['1pc']:.1e}")
RES["P1c"] = eps_tab

# ---------------------------------------------------------------- TW5
s0 = cells(load(nm("canonical", 10.45)), "canonical")["0"]["k3"]; s5 = cells(load(nm("canonical", 10.45, law="off")), "canonical")["0"]["k3"]
mv = (s5["D"] / s0["D"] - 1) if (s5.get("formed") and s0.get("formed")) else float("nan")
PM(f"TW5 (law off, log M_b 10.45 canonical): D_3(z 0) {s0['D']:.4f} -> {s5.get('D', float('nan')):.4f} ({100 * mv:+.1f} %; bites if |change| >= 5 %) -> "
   f"{'BITES' if abs(mv) >= 0.05 else 'DOES NOT BITE'}")

# ---------------------------------------------------------------- labels
P("\n== LABELS (per footing and supply; tolerance |log10 D| <= 0.10; headline = caustics 2 and 3)")
for key in ("S-seed_canonical", "S-seed_alt", "S-ref_canonical", "S-ref_alt", "S-cos_canonical", "S-cos_alt"):
    lab = LAB[key]
    P(f"  {key}: " + "; ".join(f"{k}: {lab[k]['word']}" + (f" (crossing log M_b {lab[k]['crossing_logMb']})" if lab[k].get("crossing_logMb") else "")
                              + (f", log10 D in [{lab[k]['logD_range'][0]:.2f}, {lab[k]['logD_range'][1]:.2f}]" if lab[k].get("logD_range") else "")
                              + (f", not formed {lab[k]['not_formed']}" if lab[k].get("not_formed") else "") for k in KS))
RES["labels"] = LAB; RES["tables"] = TAB
json.dump(RES, open(os.path.join(HERE, "csd1_grade.json"), "w"), indent=1, default=float)
OUT.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "csd1_grade.out"), "w").write("\n".join(OUT) + "\n")
MOUT.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "csd1_grade_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
json.dump(dict(lines=MOUT), open(os.path.join(HERE, "csd1_grade_MUTATE.json"), "w"), indent=1)
