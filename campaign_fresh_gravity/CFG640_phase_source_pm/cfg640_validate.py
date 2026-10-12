#!/usr/bin/env python3
"""CFG640 validation gates (FROZEN_CRITERIA.md section 2, 71b2cc1c9), read-only on every CFG596 / CFG636 reference file.
  V-R  VBr (cfg640_pm.py, CFG640_SOURCE=b, lean RES can L100 N256 NSEED512 RMIN 0.78125) vs CFG596 VLr: every stored snapshot
       quantity identical (difference exactly 0).
  V-P  phase pair on VPh's z = 0 particles and f_d (one in-process force evaluation per state, 256^3):
       (b) A = f_d as evolved, B = f_d zeroed for x < L/2 (same positions -> same total density): the phase source must DIFFER,
           the old representation (b path) must give IDENTICAL potentials for A and B (bit for bit);
       (i) moving only the f_d = 0 particles: the condensed MOND input is bit-for-bit unchanged, the total density changes;
       (iii) f_d = 0 everywhere: source exactly zero.
  V-H  VPh completed; P_grav/P_S0 at k 0.3 / 0.5 / 1 (S0 = CFG596 VLs) = PREVIEW, NOT a verdict (256^3); CFG596 VLr (all-baryon B)
       and CFG636 VHr (census cap) shown for context.
  python3 cfg640_validate.py -> cfg640_validate.out / cfg640_validate.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, glob, math, re
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg640_work"); W596 = os.path.join(EXT, "cfg596_work"); W636 = os.path.join(EXT, "cfg636_work")
os.environ.update(CFG596_L="100", CFG596_NSEED="512", CFG596_RMIN="0.78125", CFG596_THREADS="3", CFG596_MODE="lean",
                  CFG640_SOURCE="phase", CFG596_WORK=os.path.join(W, "VP_tmp"))
import numpy as np  # noqa: E402
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def load(d, pat):
    f = glob.glob(os.path.join(d, pat)); return json.load(open(f[0])) if f else None
def peak(job):
    wl = os.path.join(W, job, "watch.log"); pk = 0.0; sg = 0.0
    if os.path.exists(wl):
        for line in open(wl):
            m = re.search(r"peak ([\d.]+) swap_used ([\d.]+) MB \(start ([\d.]+)\)", line)
            if m: pk = max(pk, float(m.group(1))); sg = max(sg, float(m.group(2)) - float(m.group(3)))
    return pk, sg
RES = dict(lane="CFG640 validation", date="2026-10-12", criteria_commit="71b2cc1c9", gates={})

# ---------------------------------------------------------------- V-R
ref = load(os.path.join(W596, "VLr"), "cfg596_RES_*.json"); vb = load(os.path.join(W, "VBr"), "cfg640_b_RES_*.json")
if ref and vb and "z0" in vb["snap"]:
    diffs = {}; nq = 0
    for z, s in ref["snap"].items():
        t = vb["snap"].get(z)
        if t is None: diffs[z] = "missing"; continue
        for k, v in s.items():
            if k == "t": continue
            nq += 1
            a, b = np.asarray(v, dtype=float), np.asarray(t.get(k), dtype=float)
            if a.shape != b.shape or not np.array_equal(a, b, equal_nan=True):
                diffs[f"{z}.{k}"] = float(np.max(np.abs(b / a - 1))) if a.shape == b.shape else "shape"
    ok = not diffs and set(ref["snap"]) == set(vb["snap"]); pk, sg = peak("VBr")
    RES["gates"]["V-R"] = dict(PASS=ok, quantities_compared=nq, snapshots=sorted(vb["snap"]), differences=diffs, peak_rss_gb=pk, swap_growth_mb=sg)
    P(f"V-R VBr (cfg640_pm.py, SOURCE b) vs CFG596 VLr: {nq} stored quantities over {sorted(vb['snap'])}; differences "
      f"{diffs if diffs else 'none (bit for bit)'} -> {'PASS' if ok else 'FAIL'}; peak RSS {pk:.2f} GB, swap growth {sg:.0f} MB")
else: P("V-R: not run / incomplete")

# ---------------------------------------------------------------- V-P
fpos = glob.glob(os.path.join(W, "VPh", "cfg640_phase_RES_*_z0pos.npz")); ffd = glob.glob(os.path.join(W, "VPh", "cfg640_phase_RES_*_z0fd.npz"))
if fpos and ffd:
    sys.path.insert(0, HERE); import cfg640_pm as E  # noqa: E402
    os.makedirs(os.environ["CFG596_WORK"], exist_ok=True)
    N1 = 256; mesh = E.Mesh(N1); PP = E.Particles(N1); dta = E.dta_table()
    pos = np.load(fpos[0])["pos"]; fdA = np.load(ffd[0])["fd"]
    PP.x = [(pos[:, c].astype(np.float64) - PP.q(c, 0, PP.N)).astype(np.float32) for c in range(3)]; PP.mom = None
    X0 = [x.copy() for x in PP.x]; E._P[0] = PP
    def evaluate(fd, phase, x=None):
        E.PHASE = phase; PP.fd = fd; PP.x = x if x is not None else X0
        Dd = E.deposit(mesh, PP); d = Dd.read_all().copy()
        phik, info = E.forces(mesh, [Dd], 1.0, "RES", "FLAT", "canonical", dta, diag=True, keep_state=True)
        return np.array(phik), info, d
    def cond_input(fd, x=None):
        PP.fd = fd; PP.x = x if x is not None else X0
        Dc = E.deposit_cond(mesh, PP); v = Dc.read_all().copy(); Dc.close(); return v
    xs = PP.positions(0, PP.N)[:, 0]
    fdB = fdA.copy(); fdB[xs < E.L / 2] = 0
    nA = int(np.count_nonzero(fdA)); nflip = int(np.count_nonzero(fdA) - np.count_nonzero(fdB))
    phA, iA, dA = evaluate(fdA, True); phB, iB, dB = evaluate(fdB, True)
    obA, _, _ = evaluate(fdA, False); obB, _, _ = evaluate(fdB, False)
    ph_diff = float(np.max(np.abs(phA - phB)) / np.max(np.abs(phA))); old_same = bool(np.array_equal(obA, obB))
    same_rho = bool(np.array_equal(dA, dB))
    okb = ph_diff > 0 and iA["src_sum"] != iB["src_sum"] and old_same and same_rho
    rb = dict(PASS=okb, particles_condensed_A=nA, particles_flipped_to_hot=nflip, same_total_density=same_rho,
              phase_max_rel_dphi=ph_diff, src_sum_A=iA["src_sum"], src_sum_B=iB["src_sum"], e_sum_A=iA["e_sum"], e_sum_B=iB["e_sum"],
              cond_input_mean_A=iA["cond_input_mean"], cond_input_mean_B=iB["cond_input_mean"], old_representation_identical=old_same)
    P(f"V-P (b) phase pair: {nflip} of {nA} condensed particles flipped to hot (x < L/2), total density identical {same_rho}; "
      f"phase source src_sum A {iA['src_sum']:.6e} vs B {iB['src_sum']:.6e}, max|dphi|/max|phi| {ph_diff:.3e}; "
      f"old (b) representation A vs B bit-for-bit identical: {old_same} -> {'PASS' if okb else 'FAIL'}")
    rng = np.random.default_rng(640); hot = fdA == 0
    Xc = [x.copy() for x in X0]
    for c in range(3): Xc[c][hot] = (Xc[c][hot] + rng.uniform(-2, 2, int(hot.sum())).astype(np.float32) * np.float32(mesh.dx))
    ciA = cond_input(fdA); ciC = cond_input(fdA, Xc)
    E.PHASE = True; PP.fd = fdA; PP.x = Xc; DdC = E.deposit(mesh, PP); dC = DdC.read_all().copy(); DdC.close(); PP.x = X0
    oki = bool(np.array_equal(ciA, ciC)) and not np.array_equal(dA, dC)
    ri = dict(PASS=oki, hot_particles_moved=int(hot.sum()), cond_input_identical=bool(np.array_equal(ciA, ciC)),
              total_density_max_abs_change=float(np.max(np.abs(dA - dC))))
    P(f"V-P (i) fixed rho_d, moved {int(hot.sum())} hot (f_d = 0) particles by up to 2 cells: condensed MOND input bit-for-bit identical "
      f"{ri['cond_input_identical']}; total density max|change| {ri['total_density_max_abs_change']:.3e} -> {'PASS' if oki else 'FAIL'}")
    ph0, i0, _ = evaluate(np.zeros_like(fdA), True)
    E.PHASE = True; PP.fd = fdA; PP.x = X0
    phS, _ = E.forces(mesh, [E.deposit(mesh, PP)], 1.0, "S0", "FLAT", "canonical", dta, diag=True)
    okiii = i0["src_sum"] == 0.0 and i0["e_sum"] == 0.0
    riii = dict(PASS=okiii, src_sum=i0["src_sum"], e_sum=i0["e_sum"], max_rel_dphi_vs_newtonian=float(np.max(np.abs(ph0 - np.array(phS))) / np.max(np.abs(np.array(phS)))))
    P(f"V-P (iii) f_d = 0 everywhere: src_sum {i0['src_sum']}, e_sum {i0['e_sum']}; potential vs pure Newtonian max rel diff "
      f"{riii['max_rel_dphi_vs_newtonian']:.3e} -> {'PASS' if okiii else 'FAIL'}")
    RES["gates"]["V-P"] = dict(PASS=bool(okb and oki and okiii), b=rb, i=ri, iii=riii, state="VPh z = 0 particles and f_d")
else: P("V-P: VPh z0 positions / f_d not found")

# ---------------------------------------------------------------- V-H preview
vh = load(os.path.join(W, "VPh"), "cfg640_phase_RES_*.json"); s0 = load(os.path.join(W596, "VLs"), "cfg596_S0_*.json")
vc = load(os.path.join(W636, "VHr"), "cfg636_hcb_RES_*.json")
if vh and s0 and ref and "z0" in vh["snap"]:
    rec = dict(NOTE="PREVIEW at 256^3 (L100): NOT a verdict", snaps={})
    for z in ("z1", "z0.5", "z0"):
        k = np.array(vh["snap"][z]["k"]); assert np.allclose(k, np.array(s0["snap"][z]["k"]), rtol=1e-9)
        ps0 = np.array(s0["snap"][z]["P"]); m = k <= 1.0 + 1e-9
        at = lambda r, kk: float(np.exp(np.interp(math.log(kk), np.log(k), np.log(r))))
        row = {}
        for lab, J in (("phase", vh), ("B_all_baryon_CFG596", ref), ("cap_CFG636", vc)):
            if J is None: continue
            r = np.array(J["snap"][z]["P_grav"]) / ps0
            row[lab] = dict(at={str(q): at(r, q) for q in (0.3, 0.5, 1.0)}, G=float(np.max(np.abs(r[m] - 1))), min=float(np.min(r[m] - 1)),
                            sigma8_grav_ratio=J["snap"][z]["sigma8_grav"] / s0["snap"][z]["sigma8"])
        row["fd_mean"] = vh["snap"][z].get("fd_mean"); row["fd_nonzero_frac"] = vh["snap"][z].get("fd_nonzero_frac")
        rec["snaps"][z] = row
    pk, sg = peak("VPh"); rec.update(completed=True, PASS=True, peak_rss_gb=pk, swap_growth_mb=sg, runtime_s=vh.get("runtime_s"))
    RES["gates"]["V-H"] = rec
    P(f"V-H VPh (SOURCE phase) completed; peak RSS {pk:.2f} GB, swap growth {sg:.0f} MB")
    for z, r in rec["snaps"].items():
        P(f"  PREVIEW (256^3, NOT a verdict) {z}: P_grav/P_S0 at k 0.3/0.5/1: phase " + " / ".join(f"{v:.3f}" for v in r["phase"]["at"].values())
          + f" (G {r['phase']['G']:.3f}); CFG636 cap " + " / ".join(f"{v:.3f}" for v in r["cap_CFG636"]["at"].values())
          + f" (G {r['cap_CFG636']['G']:.3f}); CFG596 B " + " / ".join(f"{v:.3f}" for v in r["B_all_baryon_CFG596"]["at"].values())
          + f"; sigma8_grav/S0 phase {r['phase']['sigma8_grav_ratio']:.4f}; f_d mean {r['fd_mean']:.4f}, nonzero frac {r['fd_nonzero_frac']:.3f}")
else: P("V-H: not run / incomplete")
json.dump(RES, open(os.path.join(HERE, "cfg640_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg640_validate.out"), "w").write("\n".join(OUT) + "\n")
