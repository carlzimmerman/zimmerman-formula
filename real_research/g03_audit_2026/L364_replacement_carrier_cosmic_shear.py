#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L364 -- THE REPLACEMENT CONSTRUCTION: can a carrier whose kicked daughters free-stream hand its small-scale lensing power
to the bound-region phantom, so that cosmic shear sees LCDM's power rather than LCDM's plus the phantom's?

WHY.  L363: the assembled construction (gated switch + bound-region kernel + the density-triggered carrier of L357) FAILS
cosmic shear -- the private phantom KiDS galaxy-galaxy lensing wants is ADDED to a full LCDM-like matter field.  In the
nonlinear mock (groups inside one region share a collective field) the phantom's OWN power is small, P_ph/P_NL ~ 0.04 at
k = 0.5 and ~0.3 at k = 1 h/Mpc; the excess comes mostly from the cross term with a full matter field.  So the phantom
could REPLACE the dark component's small-scale power if the dark component is smooth at k >~ 0.5 and intact at k <~ 0.3
at the lens epoch -- exactly what a kicked, free-streaming decay does (L319; suggested by the parallel GP3's L5).  This
lane scores that construction on every gate the record uses, from committed machinery.

THE CONSTRUCTION.  C-H/K with the vacuum-gated switch (L359) and the bound-region kernel (L361); the carrier is L319's
Lambda-triggered decay Gamma ~ Omega_Lambda(a)^p with kicked daughters (uniform in space), which feel Newtonian gravity
only (L353/L354).
MACHINERY (loaded unedited): L319's linear solver (forest T^2(k=5) at z = 3, 2; S_8; and the lens-epoch transfer
T(k, z = 0.5) of the total matter, which carries the daughters' free-streaming); L354's committed X-COP / S_8 / galaxy
window (the same p = 2 grid, Newtonian orbits, both footings); L363's region kernel on GP3's nonlinear mock (P_ph/P_NL
and the matter-phantom correlation r_x at z = 0.5, 100 Mpc box, bound baryons); L360's KiDS machinery (L352's switched
compensated phantom + the carrier's halo, here the UNIFORMLY surviving fraction S(z_l = 0.25) of a full NFW halo).
COSMIC SHEAR (GP3's gate, R <= 1.2 on k = 0.1-1 h/Mpc), scored against LCDM's P_NL:
      R(k) = T(k)^2 + 2 r_x(k) T(k) s(k) + s(k)^2,    s^2 = P_ph/P_NL,
the matter's power rescaled by the solver's transfer (the decayed, streamed fraction no longer clusters on small scales);
r_x as measured against the full matter field (stated approximation).
PRE-DECLARED GATES (from the record): forest strict T^2(k=5) >= L319's 5.3 keV value at z = 3 and 2 (loose 0.9);
S_8 >= 0.767 (strict) / 0.748 (alt); X-COP and galaxies: L354's window (strict / alt); KiDS Delta chi^2 <= +4 against the
unswitched model, both footings (L352/L360); cosmic shear R <= 1.2 on k = 0.1-1 h/Mpc, both footings (GP3).
CHECKS
  C1 CONTROL: no decay (f_d = 0) gives T = 1 and reproduces L363's mock ratio (R = 1 + 2 r_x s + s^2).
  C2 CONTROL: L354's committed S_8 values are reproduced by the solver on the shared cells.
  R1 (reported) the scan: every gate per cell.
  R2 THE WINDOW: a cell passing the forest, S_8, X-COP and galaxies (L354), KiDS and cosmic shear together (either
     threshold set) -- the direction was NOT fixed in advance; the check records whatever the scan finds and says so.
  R3 THE MECHANISM: the kicked decay lowers the cosmic-shear excess by >= 0.2 in R for both switch cells.
  R4 (reported) the nearest miss.
MUTATE=1 removes the kicks (v_k = 0: the decayed mass stays where it was and keeps clustering): R3 must FAIL (rc = 1).
SCOPE.  One lens epoch (z = 0.5, GP3's mock); P(k) not a projected xi_+-; r_x held at its full-matter value; the carrier's
nonlinear one-halo power assumed to scale with the linear transfer (the decayed fraction leaves every halo alike).

Run from the repository root:  python3 real_research/g03_audit_2026/L364_replacement_carrier_cosmic_shear.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L364_replacement_carrier_cosmic_shear"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L364", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def quiet_exec(src, ns):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__.split("MACHINERY")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no kicks (v_k = 0); cosmic shear must lose any window ***")
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# ---------------------------------------------------------------------------------- L319's solver (unedited)
P19 = os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py")
G19 = quiet_exec(open(P19).read().split("# ============================================================================================ controls")[0],
                 {"__name__": "l319", "__file__": P19})
LC = G19["run"](np.ones(G19["N_A"]), 0.0)
K_H, k5, T2f, S8_of, T2_53 = G19["K_H"], G19["k5"], G19["T2"], G19["S8_of"], G19["T2_53"]
P(f"  L319 solver loaded; strict forest threshold {T2_53:.4f}   [{time.time()-T0:.0f}s]")

# ---------------------------------------------------------------------------------- L354's committed window (X-COP, S_8, galaxies)
R54 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L354_carrier_lagrangian_additive_window_results.json")))
W54 = {t: {(c[0], float(c[1]), float(c[2])) for c in R54["numbers"]["W1"]["window"][t]} for t in ("strict", "alt")}
S854 = {(float(k_.split("_")[0]), float(k_.split("_")[1])): v_ for k_, v_ in R54["numbers"]["S8"].items()}
XC54 = {}
for key, rows in R54["numbers"]["W1"]["table"].items():
    foot, fd = key.split("_"); fd = float(fd)
    for r_ in rows: XC54[(foot, fd, float(r_["vk"]))] = (r_["ratio"], r_["ratio_nt"])
P(f"  L354 window loaded: strict {sorted(W54['strict'])}; alternative {len(W54['alt'])} cells")

# ---------------------------------------------------------------------------------- L363's region kernel on GP3's mock (unedited)
P63 = os.path.join(HERE, "L363_region_kernel_lensing_power.py")
N63 = quiet_exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
                 .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), {"__name__": "l363", "__file__": P63})
SWC = {"p=1, x_c0=1.5": 1.5 * N63["E2"] ** 1.0, "p=2, x_c0=2.0": 2.0 * N63["E2"] ** 2.0}
MK = N63["build_mock"](100.0, 256, 20260926)
PHANT = {}
for cell, xc in SWC.items():
    for foot in A0:
        src = MK["rhoB"]
        mask, _ = N63["build_regions"](MK, src, xc, A0[foot])
        rp, _, _, _ = N63["region_phantom"](MK, mask, src * mask, A0[foot])
        pk = N63["spectra"](MK, {"m": MK["rho_m"] / N63["RHO"] - 1, "ph": rp / N63["RHO"]})
        kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
        rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300)); s2 = Ppp / N63["PNL_of"](kh)
        PHANT[(cell, foot)] = dict(s2={q: float(np.interp(q, kh, s2)) for q in KG}, rx={q: float(np.interp(q, kh, rx)) for q in KG})
        P(f"    phantom {cell} {foot:9s}: P_ph/P_NL at " + ", ".join(f"{q}: {PHANT[(cell, foot)]['s2'][q]:.3f}" for q in KG)
          + "; r_x at 0.5/1: " + f"{PHANT[(cell, foot)]['rx'][0.5]:.2f}/{PHANT[(cell, foot)]['rx'][1.0]:.2f}   [{time.time()-T0:.0f}s]")
OUT["numbers"]["phantom"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in PHANT.items()}

# ---------------------------------------------------------------------------------- L360's KiDS machinery (unedited top)
P60 = os.path.join(HERE, "L360_assembled_construction_kids.py")
N60 = quiet_exec(open(P60).read().split("BASE = {")[0], {"__name__": "l360", "__file__": P60})
fit_comb, carrier_esd, fit_model, A052 = N60["fit_comb"], N60["carrier_esd"], N60["fit_model"], N60["A0"]
XE59 = N60["XE59"]
BASE = {f_: fit_model(A052[f_], 0.0, "none", True)[0] for f_ in A0}
TC_FULL = carrier_esd(float("inf"), "cleared")                          # the full (undecayed) carrier halo of each lens bin
P(f"  L360/L352 KiDS machinery loaded   [{time.time()-T0:.0f}s]")

# the transfer each k needs for R <= 1.2:  T_max = -r s + sqrt(r^2 s^2 + 1.2 - s^2)
TMAX = {k_: {q: (-v_["rx"][q] * math.sqrt(v_["s2"][q]) + math.sqrt(max(v_["rx"][q] ** 2 * v_["s2"][q] + 1.2 - v_["s2"][q], 0.0)))
             for q in KG} for k_, v_ in PHANT.items()}
for k_, v_ in TMAX.items():
    P(f"    {k_[0]} {k_[1]:9s}: the matter transfer cosmic shear needs, T_max at " + ", ".join(f"{q}: {t:.2f}" for q, t in v_.items()))
OUT["numbers"]["T_max"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in TMAX.items()}

# ============================================================================================ C1-C2 controls
banner("C1-C2  CONTROLS")
Rnd = {c_: {q: 1 + 2 * PHANT[(c_, "canonical")]["rx"][q] * math.sqrt(PHANT[(c_, "canonical")]["s2"][q]) + PHANT[(c_, "canonical")]["s2"][q] for q in KG} for c_ in SWC}
P("    no decay (T = 1): R at " + "; ".join(f"{c_}: " + ", ".join(f"{q}: {v:.2f}" for q, v in r_.items()) for c_, r_ in Rnd.items()))
check("C1 CONTROL: with no decay (T = 1) the construction's cosmic-shear ratio is L363's full-matter one (the phantom added "
      "to LCDM): it exceeds the gate at k = 1", {c_: round(max(r_.values()), 2) for c_, r_ in Rnd.items()},
      all(max(r_.values()) > 1.2 for r_ in Rnd.values()), load_bearing=False)
dev = []
for fd in (0.8, 0.9):
    sv, _ = G19["surv_triggered"](fd, 2)
    for vk in (1000.0, 1400.0):
        s8 = float(S8_of(T2f(G19["run"](sv, vk), LC, 0.0))); dev.append(abs(s8 - S854[(fd, vk)]))
check("C2 CONTROL: the solver reproduces L354's committed S_8 on shared cells (p = 2)", f"max |dS_8| = {max(dev):.1e}",
      max(dev) < 1e-6, load_bearing=False)

# ============================================================================================ R1 the scan
banner("R1  THE SCAN (p = 2, L354's grid): forest, S_8, X-COP + galaxies (L354), KiDS, cosmic shear at z = 0.5")
ROWS = []
for fd in (0.8, 0.9, 0.95):
    sv, _ = G19["surv_triggered"](fd, 2)
    Szl = float(np.interp(1 / 1.25, G19["a_grid"], sv)); Szs = float(np.interp(1 / 1.5, G19["a_grid"], sv))
    for vk in (800.0, 1000.0, 1200.0, 1400.0):
        vke = 0.0 if MUTATE else vk
        R = G19["run"](sv, vke)
        t3, t2 = float(T2f(R, LC, 3.0)[k5]), float(T2f(R, LC, 2.0)[k5]); s8 = float(S8_of(T2f(R, LC, 0.0)))
        T05 = np.sqrt(np.maximum(T2f(R, LC, 0.5), 0.0)); Tq = {q: float(np.interp(math.log(q), np.log(K_H), T05)) for q in KG}
        row = dict(fd=fd, vk=vk, S_zl=Szl, fd_z05=1 - Szs, t3=t3, t2=t2, S8=s8, T05=Tq,
                   forest_strict=min(t3, t2) >= T2_53, forest_loose=min(t3, t2) >= 0.9,
                   l354_strict={f_: (f_, fd, vk) in W54["strict"] for f_ in A0}, l354_alt={f_: (f_, fd, vk) in W54["alt"] for f_ in A0},
                   xcop={f_: XC54.get((f_, fd, vk)) for f_ in A0})
        TC = [Szl * t_ for t_ in TC_FULL]
        row["kids"], row["shear"] = {}, {}
        for cell in SWC:
            xe = round(XE59[(float(cell.split(",")[0][2:]), float(cell.split("=")[2]))], 4)
            row["kids"][cell] = {f_: float(fit_comb(A052[f_], xe, TC, [1.0])[0] - BASE[f_]) for f_ in A0}
            row["shear"][cell] = {f_: {q: Tq[q] ** 2 + 2 * PHANT[(cell, f_)]["rx"][q] * Tq[q] * math.sqrt(PHANT[(cell, f_)]["s2"][q])
                                       + PHANT[(cell, f_)]["s2"][q] for q in KG} for f_ in A0}
        ROWS.append(row)
        P(f"    f_d(0) {fd:.2f} v_k {vk:5.0f}: F(z=0.5) {row['fd_z05']:.2f}, T(0.5/1) {Tq[0.5]:.2f}/{Tq[1.0]:.2f}, S(z_l) {Szl:.2f}; forest {min(t3, t2):.4f}; S_8 {s8:.3f}; "
          f"L354 strict/alt {['c' if row['l354_strict']['canonical'] else '-', 'a' if row['l354_strict']['alt'] else '-']}/"
          f"{['c' if row['l354_alt']['canonical'] else '-', 'a' if row['l354_alt']['alt'] else '-']}; KiDS " + " ".join(
              f"{c_[:5]}:{row['kids'][c_]['canonical']:+.0f}/{row['kids'][c_]['alt']:+.0f}" for c_ in SWC) + "; shear worst " + " ".join(
              f"{c_[:5]}:{max(row['shear'][c_]['canonical'].values()):.2f}/{max(row['shear'][c_]['alt'].values()):.2f}" for c_ in SWC)
          + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["scan"] = [{k_: (v_ if not isinstance(v_, dict) else {str(a): b for a, b in v_.items()}) for k_, v_ in r_.items()} for r_ in ROWS]
check("R1 (reported) the scan", f"{len(ROWS)} carrier cells x {len(SWC)} switch cells", True, load_bearing=False)

# ============================================================================================ R2 the window
banner("R2  THE WINDOW: forest + S_8 + X-COP/galaxies (L354) + KiDS + cosmic shear, both footings")
WIN = {"strict": [], "alt": []}
for r_ in ROWS:
    for cell in SWC:
        for t in ("strict", "alt"):
            fo = r_["forest_strict"] if t == "strict" else r_["forest_loose"]
            s8 = r_["S8"] >= (0.767 if t == "strict" else 0.748)
            w54 = all(r_["l354_strict"][f_] if t == "strict" else (r_["l354_strict"][f_] or r_["l354_alt"][f_]) for f_ in A0)
            kid = all(v <= 4.0 for v in r_["kids"][cell].values())
            sh = all(max(r_["shear"][cell][f_].values()) <= 1.2 for f_ in A0)
            if fo and s8 and w54 and kid and sh:
                WIN[t].append((r_["fd"], r_["vk"], cell))
            r_.setdefault("gates", {})[f"{cell}/{t}"] = dict(forest=bool(fo), S8=bool(s8), l354=bool(w54), kids=bool(kid), shear=bool(sh))
for t in ("strict", "alt"):
    P(f"    {t:6s} window: {WIN[t] or 'none'}")
blocking = {}
for r_ in ROWS:
    for k_, g_ in r_["gates"].items():
        for gate, ok in g_.items():
            if not ok: blocking[gate] = blocking.get(gate, 0) + 1
P(f"    gates failed across all (cell, switch, set) combinations: {blocking}")
OUT["numbers"]["window"] = {t: [list(w) for w in WIN[t]] for t in WIN}; OUT["numbers"]["blocking"] = blocking
found = bool(WIN["strict"] or WIN["alt"])
check("R2 THE REPLACEMENT CONSTRUCTION " + ("HAS" if found else "HAS NO") + " WINDOW through the forest, S_8, X-COP and galaxies, "
      "KiDS and cosmic shear together (direction not fixed in advance: this check records the finding)",
      f"strict {WIN['strict'] or 'none'}; alt {WIN['alt'] or 'none'}; failing gates {blocking}", True if not MUTATE else not found,
      "a free-streaming carrier hands small-scale lensing power to the phantom only if enough of it has decayed by the lens epoch")

# ============================================================================================ R3 the mechanism, R4 the nearest miss
banner("R3-R4  THE MECHANISM (free streaming) AND THE NEAREST MISS")
red = {}
for cell in SWC:
    nod = max(Rnd[cell].values())
    best = min(max(r_["shear"][cell]["canonical"].values()) for r_ in ROWS)
    red[cell] = (nod, best, nod - best)
    P(f"    {cell}: worst R with no decay {nod:.2f} -> best kicked carrier {best:.2f} (reduction {nod - best:.2f})")
OUT["numbers"]["R3"] = {k_: v_ for k_, v_ in red.items()}
check("R3 THE MECHANISM: the kicked, free-streaming decay lowers the cosmic-shear excess -- the best carrier cell's worst R is "
      "at least 0.2 below the no-decay value for both switch cells (the streamed daughters take the dark share's small-scale "
      "power out of the lensing field)", {k_: round(v_[2], 2) for k_, v_ in red.items()}, all(v_[2] >= 0.2 for v_ in red.values()),
      "with v_k = 0 (MUTATE) the decayed mass keeps clustering and nothing is replaced")
near = []
for r_ in ROWS:                                                        # rank by MARGIN: normalised exceedance summed over failing gates
    for cell in SWC:
        g_ = r_["gates"][f"{cell}/alt"]
        shw = max(max(r_["shear"][cell][f_].values()) for f_ in A0); kw = max(r_["kids"][cell].values())
        exc = {"shear": max(0.0, (shw - 1.2) / 0.2), "kids": max(0.0, (kw - 4.0) / 4.0), "S8": max(0.0, (0.748 - r_["S8"]) / 0.02),
               "forest": max(0.0, (0.9 - min(r_["t2"], r_["t3"])) / 0.05), "l354": 0.0 if g_["l354"] else 2.0}
        score = sum(exc[k_] for k_, v in g_.items() if not v)
        near.append((score, 0.0, r_["fd"], r_["vk"], cell, {k_: round(exc[k_], 2) for k_, v in g_.items() if not v},
                     r_["kids"][cell], {f_: round(max(r_["shear"][cell][f_].values()), 2) for f_ in A0}))
near.sort(key=lambda t: (t[0], t[1]))
for n_ in near[:3]:
    P(f"    nearest (alternative set, by margin {n_[0]:.2f}): f_d(0) {n_[2]} v_k {n_[3]:.0f}, switch {n_[4]}: failing (normalised exceedance) {n_[5]}; KiDS "
      f"{n_[6]['canonical']:+.1f}/{n_[6]['alt']:+.1f}; shear worst {n_[7]}")
OUT["numbers"]["nearest"] = [dict(margin=n_[0], fd=n_[2], vk=n_[3], switch=n_[4], failing=list(n_[5]), kids=n_[6], shear=n_[7]) for n_ in near[:3]]
check("R4 (reported) the nearest miss on the alternative threshold set, ranked by normalised margin", f"f_d(0) {near[0][2]}, v_k "
      f"{near[0][3]:.0f}, switch {near[0][4]}: failing {near[0][5]}", True, "one gate short on one footing is a design target, not a pass", load_bearing=False)

banner("VERDICT")
P(f"""  Replacement at the cosmic-shear lens epoch (z = 0.5): strict window {WIN['strict'] or 'none'}; alternative {WIN['alt'] or 'none'}.
  Gates that block across the scan: {blocking}.""")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
