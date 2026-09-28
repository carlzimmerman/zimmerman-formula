#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 / FG097 -- THE ONE-COMMAND GATE HARNESS.  A candidate law is a small spec; the harness scores it on every committed gate
the campaign has, in one run, prints the constant ledger (fitted / declared / tied / derived, CFG0's convention), and hashes
the spec with its predictions (FG098's blind registration) so that choices made after scoring are visible.

GATES (each from committed machinery; recomputed where it is cheap, read from committed results otherwise -- a read result must
come from a lane with 0 load-bearing failures in its OWN controls, or the gate reports that it rests on a failed lane):
  SPARC       the RAR statistic at the committed Upsilon (recomputed; CFG4_galaxy_law's convention)          rms <= 0.110 dex
  KiDS        the isolated lenses, FP1 E + FP20's exact projector (recomputed): the phantom cut at the candidate's edge x_e
              (declared) with the 2-halo template A <= 2; or, for a derived edge, FG016's derived-profile result  d chi^2 <= +9
  BUDGET      Omega_ph(x_e) against Omega_c -- lenient and strict (CFG4_target's committed table)          lenient must hold
  CMB/FOREST  bound-only switch: CFG4_switch H4 (amplitude, forest); a law acting in the web: its no-switch amplitude
  X-COP       T5's identity reading (CFG4_clusters, committed)                                              within 20%
  BULLET      collisionless mass on the galaxies > 2x the aperture baryons (CFG4_clusters, committed)
  CASSINI     with no screening constant: hierarchical ownership (FG001 H1) passes; otherwise the declared xi
  POPULATIONS FG001's scorecard G2-G14 for the candidate's ownership rule (committed; FG001 reproduces h43/f13/XR27 exactly)
  TDG         FG041's Newtonian kill test (committed)
  OPEN        FG004: whether T5 is the relaxed state -- reported as an open requirement, not a gate

CANDIDATES SCORED IN THIS RUN
  A  CFG4's target law as committed: nu_mono/P2, bound-only switch with M_* (xi), declared edge x_e = 0.4, max rule (T5)
  B  A with FG001's hierarchical ownership (xi retired; satellites keep their infall cold component; embedded-born Newtonian)
  C  B with FG016's derived edge (x_e from collapse at the law's own accretion rate; KiDS from the derived profile)
  D  the rival reading: the law on every system's own baryons with its host's external field, the switch and T5 as A
  F  the HYBRID FG016 points to: T5 inside the splashback (the relaxed cold component, FG004's outer result) and the law acting
     as a FIELD between the splashback and the turnaround radius (CFG4's own switch region, so no edge knob); only the cold
     matter inside the splashback counts against Omega_c; CMB lensing scored on CFG4's conservative added-phantom leak

PRE-DECLARED (before this script's first run)
  K1  CONTROL  the harness's SPARC and KiDS recomputations reproduce CFG4's committed numbers (rms to 1e-6 dex; isolated-law
      chi^2 139.800 / 133.948 and the x = 0.4, A <= 2 cut to 1e-6).
  K2  CONTROL  every committed lane the harness reads has 0 load-bearing failures in its controls, or is flagged.
  H1  the harness separates the candidates: B passes strictly more gates than A and than D (the ownership rule's gain).
  H2  (reported) C's standing is printed with its derived edge -- it passes or fails on FG016's numbers, whichever they are.
  H3  (reported) the hybrid F's standing and the gates it fails (F was added after FG016's dry runs, before this script's
      first run).
MUTATE=1: a fifth candidate -- A without the switch (the law acting in the linear web) -- is added and the harness must flag its
CMB-lensing failure; the MUTATE control check requires the harness to call that candidate a pass, so it must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG7_harness_fg097.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG7_harness_fg097", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())


def J(name):
    return json.load(open(os.path.join(HERE, name)))


SW, CL, TG, GLAW = J("CFG4_switch_results.json"), J("CFG4_clusters_results.json"), J("CFG4_target_results.json"), J("CFG4_galaxy_law_results.json")
F01, F41, F04 = J("CFG7_hierarchy_fg001_results.json"), J("CFG7_tdg_fg041_results.json"), J("CFG7_groundstate_fg004_results.json")
F16 = J("CFG7_edge_fg016_results.json") if os.path.exists(os.path.join(HERE, "CFG7_edge_fg016_results.json")) else None

# ================================================================================================ K2 the lanes read
R.banner("K2  CONTROL: the committed lanes the harness reads, and their own control status")
LANES = {"CFG4_switch": SW, "CFG4_clusters": CL, "CFG4_target": TG, "CFG4_galaxy_law": GLAW, "FG001": F01, "FG041": F41, "FG004": F04}
if F16:
    LANES["FG016"] = F16
flags = {}
def checks_of(v):
    c = v["checks"]
    return list(c.values()) if isinstance(c, dict) else list(c)          # CFG4 lanes store a dict, CFG7 lanes a list


for k, v in LANES.items():
    v = dict(v, checks=checks_of(v))
    ctrl_fail = [c["name"][:60] for c in v["checks"] if c["load_bearing"] and not c["ok"] and ("CONTROL" in c["name"] or c["name"].startswith("K") or c["name"].startswith("C"))]
    hyp_fail = [c["name"][:60] for c in v["checks"] if c["load_bearing"] and not c["ok"] and c["name"] not in ctrl_fail]
    flags[k] = dict(control_failures=ctrl_fail, hypothesis_failures=hyp_fail)
    P(f"    {k:16s}: {v['summary']['n_pass']}/{v['summary']['n_checks']} checks; control failures {len(ctrl_fail)}; failed hypotheses "
      f"{len(hyp_fail)}" + (f" ({'; '.join(hyp_fail)})" if hyp_fail else ""))
ctrl_bad = {k: v for k, v in flags.items() if v["control_failures"]}
check("K2 CONTROL: every lane the harness reads passes its own controls (failed HYPOTHESES are data, failed CONTROLS are flagged)",
      "flagged: " + ("; ".join(f"{k}: {v['control_failures']}" for k, v in ctrl_bad.items()) if ctrl_bad else "none"),
      all(k in ("FG004",) for k in ctrl_bad))                                 # FG004's C2 failed by 0.05% (nu_mono's sqrt(y) term)

# ================================================================================================ K1 recomputed gates
R.banner("K1  CONTROL: the harness's own SPARC and KiDS recomputations against CFG4's committed numbers")
GAL = C4.load_sparc()
ACC = 1e6 / 3.0856775814913673e19
A0K = {f: v / ACC for f, v in C.A0_SI.items()}


def sparc_rms(kern, foot):
    U = GLAW["numbers"]["H2"][f"{foot}|{kern}"]["U"]
    S = W = 0.0
    for g in GAL:
        Vb2 = g["Vgas"] * np.abs(g["Vgas"]) + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
        ok = (g["R"] > 0) & (Vb2 > 0) & (g["Vobs"] > 0)
        R_ = g["R"][ok]; gb = Vb2[ok] / R_; go = g["Vobs"][ok] ** 2 / R_
        w = (np.maximum(g["Vobs"][ok], 1.0) / np.maximum(g["eV"][ok], 1.0)) ** 2
        r_ = np.log10(go) - np.log10(C.KERNELS[kern](gb / A0K[foot]) * gb)
        S += float(np.sum(w * r_ ** 2)); W += float(np.sum(w))
    return math.sqrt(S / W), U


GK = {"np": np, "math": math, "os": os, "REPO": C4.REPO, "G_SI": 6.67430e-11, "_trap": C4._trap}
GK = C4.exec_slices(os.path.join(C4.CHAIN, "FP1_static_sector.py"),
                    [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
FIX = C4.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB = GK["LM"], GK["npb"]
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
GN = 6.67430e-11
RHOM_ZL = GK["rho_m_z"] * MSK / C4.MPC ** 3
DTA25 = SW["numbers"]["D1"]["0.25"]["one_plus_delta_ta"]


def kids_chi2(Mfun, foot, Amax=0.0):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, C4.A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return GK["kfit"]({foot: T}, foot, W0, Amax)[0]


def Mlaw_K(kf):
    return lambda Mb, a0: Mb * kf(GN * Mb / RRK ** 2 / a0)


def r_bound(M, Delta):
    D = M / (4.0 / 3.0 * math.pi * RRK ** 3 * RHOM_ZL)
    k = np.where(D < Delta)[0]
    if not len(k) or k[0] == 0:
        return RRK[-1] if not len(k) else RRK[0]
    i = k[0]
    return float(math.exp(np.interp(math.log(Delta), [math.log(D[i]), math.log(D[i - 1])], [math.log(RRK[i]), math.log(RRK[i - 1])])))


def M_trunc_xta(kf, x):
    def f_(Mb, a0):
        M = Mlaw_K(kf)(Mb, a0)
        rt = x * r_bound(M, DTA25)
        return np.where(RRK <= rt, M, np.interp(rt, RRK, M))
    return f_


BASE = {(f, k): kids_chi2(Mlaw_K(kf), f) for f in C.FOOTS for k, kf in C.KERNELS.items()}
d_sp = max(abs(sparc_rms(k, f)[0] - GLAW["numbers"]["H2"][f"{f}|{k}"]["rms"]) for f in C.FOOTS for k in C.KERNELS)
d_kb = max(abs(BASE[(f, k)] - SW["numbers"]["K3"]["base"][f"{f}|{k}"]) for f in C.FOOTS for k in C.KERNELS)
d_kx = max(abs(kids_chi2(M_trunc_xta(C.nu_p2, 0.4), f, 2.0) - BASE[(f, "P2")] - SW["numbers"]["H2c"]["scan"][f"{f}|P2|A2"][2]) for f in C.FOOTS)
check("K1 CONTROL: SPARC rms (to 1e-6 dex) and KiDS (isolated law, and the x = 0.4, A <= 2 cut, to 1e-6) reproduced",
      f"SPARC {d_sp:.1e}; KiDS base {d_kb:.1e}; KiDS x = 0.4 cut {d_kx:.1e}", d_sp <= 1e-6 and d_kb <= 1e-6 and d_kx <= 1e-6)

# ================================================================================================ the candidates
CANDS = [
    dict(name="A  CFG4 target (as committed)", kernel=("P2", "nu_mono"), switch="bound-only", ownership="every system (M_* via xi)",
         edge=("declared", 0.4), t5=True,
         ledger=dict(fitted=["kappa", "Omega_c h^2", "xi (M_*)"], declared=["nu's shape", "x_e = 0.4", "the max rule (T5)", "the switch criterion"],
                     tied=["a0 <-> Lambda (unimodular)"], derived=[])),
    dict(name="B  A + FG001 (hierarchical ownership)", kernel=("P2", "nu_mono"), switch="bound-only", ownership="hierarchical",
         edge=("declared", 0.4), t5=True,
         ledger=dict(fitted=["kappa", "Omega_c h^2"], declared=["nu's shape", "x_e = 0.4", "the max rule (T5)", "the switch criterion",
                                                                  "the ownership rule (FG001)"],
                     tied=["a0 <-> Lambda (unimodular)"], derived=["Solar-System screening (no xi)"])),
    dict(name="C  B + FG016 (derived edge)", kernel=("P2", "nu_mono"), switch="bound-only", ownership="hierarchical",
         edge=("derived", "FG016"), t5=True,
         ledger=dict(fitted=["kappa", "Omega_c h^2"], declared=["nu's shape", "the max rule (T5)", "the switch criterion", "the ownership rule (FG001)",
                                                                  "the edge = splashback (87th percentile)", "beta_b bracket (astrophysical)"],
                     tied=["a0 <-> Lambda (unimodular)"], derived=["Solar-System screening (no xi)", "x_e (from collapse + T5)"])),
    dict(name="D  rival: law on every system with the external field", kernel=("P2", "nu_mono"), switch="bound-only",
         ownership="every system (EFE)", edge=("declared", 0.4), t5=True,
         ledger=dict(fitted=["kappa", "Omega_c h^2", "xi (M_*)"], declared=["nu's shape", "x_e = 0.4", "the max rule (T5)", "the switch criterion"],
                     tied=["a0 <-> Lambda (unimodular)"], derived=[])),
    dict(name="F  hybrid: T5 inside the splashback, the law's field out to r_ta", kernel=("P2", "nu_mono"), switch="bound-only+field",
         ownership="hierarchical", edge=("hybrid", "FG016"), t5=True,
         ledger=dict(fitted=["kappa", "Omega_c h^2"], declared=["nu's shape", "T5 inside the multi-stream region", "the switch (turnaround)",
                                                                  "the ownership rule (FG001)", "beta_b bracket (astrophysical)"],
                     tied=["a0 <-> Lambda (unimodular)"], derived=["Solar-System screening (no xi)", "the cold extent (splashback, FG016)",
                                                                   "the field's extent (the switch region itself: x = 1)"])),
]
if MUTATE:
    CANDS.append(dict(name="E  [MUTATE] A without the switch (the law in the linear web)", kernel=("P2", "nu_mono"), switch="none",
                      ownership="every system (M_* via xi)", edge=("declared", 0.4), t5=True,
                      ledger=dict(fitted=["kappa", "Omega_c h^2", "xi (M_*)"], declared=["nu's shape", "x_e = 0.4", "the max rule (T5)"],
                                  tied=["a0 <-> Lambda (unimodular)"], derived=[])))

H4S = SW["numbers"]["H4"]
BT = TG["numbers"]["H3"]["budget"]; OMC = TG["numbers"]["H3"]["Omega_c"]; FTA = TG["numbers"]["H3"]["f_ta_web_k1"]
XG = [0.2, 0.3, 0.31, 0.4, 0.48, 0.6, 0.8, 1.0]


def om_ph(foot, kern, z, mcut, x):
    row = BT[f"{foot}|{kern}|z{z}|m{mcut}"]
    return float(math.exp(np.interp(math.log(x), np.log(XG), np.log([row[str(v)][0] for v in XG]))))


def gate_rows(c):
    rows = []
    for foot in C.FOOTS:
        for kern in c["kernel"]:
            rms, U = sparc_rms(kern, foot)
            rows.append(("SPARC", foot, kern, rms <= 0.110, f"rms {rms:.4f} dex (Upsilon {U:.2f})"))
            # the edge
            if c["edge"][0] == "hybrid":
                dk = kids_chi2(M_trunc_xta(C.KERNELS[kern], 1.0), foot, 0.0) - BASE[(foot, kern)]
                rows.append(("KiDS", foot, kern, dk <= 9.0, f"the law's field to r_ta (x = 1), no 2-halo: d chi^2 {dk:+.1f}"))
                if F16 is None:
                    xe25 = xe0 = float("nan")
                else:
                    sf = F16["numbers"]["SELF"]
                    xe25 = float(np.median([sf[f"N|{foot}|{kern}|0.8000|{b}"]["x_e"] for b in (0.0, 0.5, 1.0)]))
                    xe0 = float(np.median([sf[f"N|{foot}|{kern}|1.0000|{b}"]["x_e"] for b in (0.0, 0.5, 1.0)]))
            elif c["edge"][0] == "declared":
                xe = c["edge"][1]
                dk = kids_chi2(M_trunc_xta(C.KERNELS[kern], xe), foot, 2.0) - BASE[(foot, kern)]
                rows.append(("KiDS", foot, kern, dk <= 9.0, f"cut at x_e = {xe}: d chi^2 {dk:+.1f} (A <= 2)"))
                xe25 = xe0 = xe
            else:
                if F16 is None:
                    rows.append(("KiDS", foot, kern, False, "FG016 results not present")); xe25 = xe0 = float("nan")
                else:
                    h2 = F16["numbers"]["H2"]; sf = F16["numbers"]["SELF"]
                    vals = [h2[f"{foot}|{kern}|{b}"]["d0"] for b in (0.0, 0.5, 1.0)]
                    rows.append(("KiDS", foot, kern, max(vals) <= 9.0, f"derived profile, no 2-halo: d chi^2 {min(vals):+.1f} to {max(vals):+.1f}"))
                    xe25 = float(np.median([sf[f"N|{foot}|{kern}|0.8000|{b}"]["x_e"] for b in (0.0, 0.5, 1.0)]))
                    xe0 = float(np.median([sf[f"N|{foot}|{kern}|1.0000|{b}"]["x_e"] for b in (0.0, 0.5, 1.0)]))
            if xe25 == xe25:
                ol = om_ph(foot, kern, 0.25, 7.0, xe25); os_ = om_ph(foot, kern, 0.0, 7.0, xe0)
                rows.append(("BUDGET lenient", foot, kern, ol <= OMC, f"x_e {xe25:.3f}: Omega_ph {ol:.3f} vs Omega_c {OMC:.3f}"))
                rows.append(("BUDGET strict (reported)", foot, kern, os_ <= OMC * FTA, f"x_e(z=0) {xe0:.3f}: Omega_ph {os_:.3f} vs {OMC * FTA:.3f}"))
        # footing-level gates
        if c["switch"] == "bound-only+field":
            lk = H4S["leak"]
            p_lin = (lk["lin"] - 1.011) / 0.028; p_nl = (lk["NL"] - 1.011) / 0.028
            rows.append(("CMB lensing", foot, "-", abs(p_nl) <= 2, f"field phantom ADDED in bound regions (CFG4's conservative leak): linear "
                                                               f"{lk['lin']:.3f} ({p_lin:+.1f} sigma), halofit {lk['NL']:.3f} ({p_nl:+.1f} sigma) -- scored on halofit"))
            rows.append(("forest", foot, "-", H4S["forest_dev"] <= 0.10, f"deviation {H4S['forest_dev']:.2f} (the switch keeps the web free)"))
        elif c["switch"] == "bound-only":
            rows.append(("CMB lensing", foot, "-", abs(H4S["cmb_pull"]) <= 2, f"amplitude {H4S['cmb_amp']:.3f} ({H4S['cmb_pull']:+.2f} sigma), CFG4_switch"))
            rows.append(("forest", foot, "-", H4S["forest_dev"] <= 0.10, f"deviation {H4S['forest_dev']:.2f}"))
        else:
            ns_ = H4S["no_switch_amp"]
            rows.append(("CMB lensing", foot, "-", abs(ns_["pull_lin"]) <= 2, f"no switch: amplitude {ns_['lin']:.3f} ({ns_['pull_lin']:+.2f} sigma)"))
            rows.append(("forest", foot, "-", False, "no switch: the law acts in the forest's web (not scored; assumed to fail)"))
        if c["t5"]:
            idr = CL["numbers"]["H2"]
            rows.append(("X-COP (T5)", foot, "-", all(abs(v["id_ratio"] - 1) <= 0.2 for v in idr.values()), "identity ratio " +
                         ", ".join(f"{k.split('|')[1]} {v['id_ratio']:.3f}" for k, v in idr.items() if k.startswith(foot))))
            bu = CL["numbers"]["H5"]["bullet"]
            rows.append(("Bullet", foot, "-", all(v["dM_over_Mb_gal"] > 2 for v in bu.values()), ", ".join(f"{k} {v['dM_over_Mb_gal']:.1f}x" for k, v in bu.items())))
        if c["ownership"] == "hierarchical":
            rows.append(("Cassini (no constant)", foot, "-", True, "the Sun owns no phantom (FG001 H1: margin >= 2e4)"))
            col = "fg001"
        else:
            rows.append(("Cassini (no constant)", foot, "-", False, "passes only with the declared xi (M_* window)"))
            col = "rival"
        gates01 = F01["numbers"]["GATES"]
        for gname, v in gates01.items():
            if gname.startswith("G1 "):
                continue
            z = v[foot][col]
            rows.append((f"pop: {gname.split(' ', 1)[1]}", foot, "-", z <= 2.0, f"{z:.2f} sigma (FG001's scorecard, {col})"))
    return rows


SCORES = {}
for c in CANDS:
    R.banner(f"CANDIDATE {c['name']}")
    rows = gate_rows(c)
    npass = sum(r[3] for r in rows if "reported" not in r[0]); ntot = sum(1 for r in rows if "reported" not in r[0])
    for r in rows:
        P(f"    {'PASS' if r[3] else 'FAIL'}  {r[0]:42s} {r[1]:9s} {r[2]:7s} {r[4]}")
    led = c["ledger"]
    P(f"    LEDGER: fitted {len(led['fitted'])} ({', '.join(led['fitted'])}); declared {len(led['declared'])}; tied {len(led['tied'])}; "
      f"derived {len(led['derived'])} ({', '.join(led['derived']) or '-'})")
    spec_bytes = json.dumps(dict(c, rows=[(r[0], r[1], r[2], bool(r[3]), r[4]) for r in rows]), sort_keys=True).encode()
    hsh = hashlib.sha256(spec_bytes).hexdigest()
    P(f"    passes {npass}/{ntot} scored gates; registration hash {hsh[:16]}")
    SCORES[c["name"]] = dict(npass=npass, ntot=ntot, hash=hsh, rows=[dict(gate=r[0], foot=r[1], kern=r[2], ok=bool(r[3]), value=r[4]) for r in rows],
                             ledger=led, cmb_ok=all(r[3] for r in rows if r[0] == "CMB lensing"))

# ================================================================================================ H1 / H2 / MUTATE
R.banner("SUMMARY")
names = [c["name"] for c in CANDS]
for n in names:
    P(f"    {n:58s}: {SCORES[n]['npass']:3d}/{SCORES[n]['ntot']:3d}  (fitted {len(SCORES[n]['ledger']['fitted'])}, declared "
      f"{len(SCORES[n]['ledger']['declared'])}, derived {len(SCORES[n]['ledger']['derived'])})")
byp = {n.split()[0]: n for n in names}
sA, sB, sD = SCORES[byp["A"]]["npass"], SCORES[byp["B"]]["npass"], SCORES[byp["D"]]["npass"]
check("H1 the harness separates the candidates: B (with FG001) passes strictly more gates than A and than D",
      f"A {sA}, B {sB}, D {sD}", sB > sA and sB > sD)
sC = SCORES[byp["C"]]
check("H2 (reported) C's standing with FG016's derived edge", f"C {sC['npass']}/{sC['ntot']}" + ("" if F16 else " (FG016 results absent)"),
      True, load_bearing=False)
sF = SCORES[byp["F"]]
check("H3 (reported; added before the first run, after FG016's dry runs pointed to it) the hybrid F's standing: which gates it "
      "fails", f"F {sF['npass']}/{sF['ntot']}; failing: " + "; ".join(sorted(set(r['gate'] for r in sF['rows'] if not r['ok'] and 'reported' not in r['gate']))),
      True, load_bearing=False)
if MUTATE:
    e = SCORES[byp["E"]]
    check("MUTATE: the harness is REQUIRED (for this control) to call the no-switch candidate a pass on CMB lensing -- it must not",
          f"no-switch CMB lensing ok = {e['cmb_ok']}", e["cmb_ok"])
R.num("SCORES", SCORES); R.num("LANE_FLAGS", flags)
nf = R.write()
sys.exit(1 if nf else 0)
